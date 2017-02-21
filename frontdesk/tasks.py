import logging

from django.db import transaction

from lxml import etree
import packtools
from packtools import (
        stylechecker,
        utils as packtools_utils,
)

from inbox.taskapp.celery import app
from . import (
        models,
        utils,
        signals,
)


LOGGER = logging.getLogger(__name__)


@app.task(ignore_result=True)
def create_package_members(package_id):
    try:
        package = models.Package.objects.get(pk=package_id)
    except models.Package.DoesNotExist as exc:
        raise ValueError('Cannot find a package with id '
                         '"%s".' % package_id) from exc

    with packtools_utils.Xray.fromfile(package.file.path) as xpack:
        with transaction.atomic():
            # registra um transactional hook para a emissão do evento
            # ``frontdesk.signals.package_members_created`` caso a transação
            # seja efetivada.
            transaction.on_commit(
                    lambda: signals.package_members_created.send_robust(
                        sender=create_package_members, instance=package))

            for member in xpack.show_members():
                models.PackageMember.objects.create(
                        package=package, name=member)


@app.task(bind=True, default_retry_delay=300, max_retries=5, ignore_result=True)
def scan_package_for_viruses(self, package_id):
    try:
        package = models.Package.objects.get(pk=package_id)
    except models.Package.DoesNotExist as exc:
        raise ValueError('Cannot find a package with id '
                         '"%s".' % package_id) from exc

    try:
        is_infected, details = utils.scan_file_for_viruses(package.file)
    except utils.AntivirusConnectionError as exc:
        self.retry(exc)
    except utils.AntivirusBufferTooLongError as exc:
        scan_status = models.VirusScanStatus.UNDETERMINED
        scan_details = str(exc)
    else:
        if is_infected:
            scan_status = models.VirusScanStatus.INFECTED
        else:
            scan_status = models.VirusScanStatus.UNINFECTED

        scan_details = str(details)  # representação textual de uma tupla

    package.virus_scan_status = scan_status
    package.virus_scan_details = scan_details
    package.save()


@app.task(ignore_result=True)
def validate_package_member(member_id):
    """Valida uma instância de ``PackageMember`` contra a SciELO PS.

    Um membro só pode ser validado uma única vez.

    Pode levantar a exceção ``ValueError`` no caso de ``member_id`` não
    corresponder a uma instância de ``frontdesk.models.PackageMember``.
    """
    try:
        member = models.PackageMember.objects.get(pk=member_id)
    except models.PackageMember.DoesNotExist as exc:
        raise ValueError('Cannot find a package member with id '
                         '"%s".' % member_id) from exc

    if not member.is_xml():
        LOGGER.warning('Cannot run SPS validations against non XML files. '
                       'Skipping "%s".', member.name)
        return

    # Garante que ``member`` ainda não foi validado.
    # Uma maneira simples é acessar a entidade relacionada. Se essa entidade
    # existir é sinal que a validação já foi realizada.
    try:
        _ = member.xml_control_attrs
    except models.XMLMemberControlAttrs.DoesNotExist:
        pass
    else:
        LOGGER.warning('Cannot run SPS validations on XML files that are '
                       'already validated. Skipping "%s".', member.name)
        return

    with member.open() as member_file:
        try:
            validator = packtools.XMLValidator.parse(member_file)
        except (packtools.exceptions.PacktoolsError, etree.XMLSyntaxError) as exc:
            summary = {
                    'is_valid': False,
                    'exception_type': type(exc).__name__,
                    'exception_value': str(exc),
            }
        else:
            summary = stylechecker.summarize(validator)

    if summary['is_valid']:
        check_status = models.SPSStatus.VALID
    else:
        check_status = models.SPSStatus.INVALID

    models.XMLMemberControlAttrs.objects.create(
            member=member,
            sps_check_status=check_status,
            sps_check_details=summary)

