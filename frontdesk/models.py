import mimetypes

import celery
from django.db import models
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices

from packtools import utils as packtools_utils

from . import signals


PACKAGE_VIRUSSCAN_STATUS_QUEUED = 'queued'
PACKAGE_VIRUSSCAN_STATUS_UNDETERMINED = 'undetermined'
PACKAGE_VIRUSSCAN_STATUS_INFECTED = 'infected'
PACKAGE_VIRUSSCAN_STATUS_UNINFECTED = 'uninfected'

XMLMEMBER_SPS_STATUS_VALID = 'valid'
XMLMEMBER_SPS_STATUS_INVALID = 'invalid'


class Deposit(TimeStampedModel):
    """O depósito de um pacote SciELO PS para ingresso na coleção.

    A mudança de estados do pacote -- esperando análise, aceito e rejeitado --
    é implementada pela instância de ``StatusField``, uma máquina de estados
    finitos extremamente simplificada.

    A superclasse ``TimeStampedModel`` provê os atributos ``created`` e
    ``modified``, contendo a data e hora de criação e de modificação da
    entidade, respectivamente.

    Mais informação sobre ``StatusField`` e ``TimeStampedModel`` em:
    https://django-model-utils.readthedocs.io/en/latest/
    """
    STATUS = Choices('deposited', 'rejected', 'accepted')

    status = StatusField()
    status_changed = MonitorField(monitor='status')
    depositor = models.CharField(max_length=16)


class Package(TimeStampedModel):
    """Pacote depositado para inclusão na coleção.

    Um pacote é basicamente um maço, zipado, de arquivos XML -- que devem ser
    válidos em relação a especificação SciELO PS -- e seus respectivos ativos
    digitais, incluindo PDF.

    Uma instância de ``Package`` contém atributos que representam seu
    status na verificação de vírus. São os atributos cujo identificador
    começa com ``virus_scan_``. Os status possíveis são representados pelas
    variáveis:
      - models.PACKAGE_VIRUSSCAN_STATUS_QUEUED (verificação ainda pendente),
      - models.PACKAGE_VIRUSSCAN_STATUS_UNDETERMINED (quando não foi possível
        verificar o pacote, por exemplo por exceder o tamanho máximo aceito
        pelo antivirus),
      - models.PACKAGE_VIRUSSCAN_STATUS_INFECTED (o pacote está infectado),
      - models.PACKAGE_VIRUSSCAN_STATUS_UNINFECTED (o pacote não está infectado).

    A superclasse ``TimeStampedModel`` provê os atributos ``created`` e
    ``modified``, contendo a data e hora de criação e de modificação da
    entidade, respectivamente.

    Mais informação sobre ``TimeStampedModel`` em:
    https://django-model-utils.readthedocs.io/en/latest/
    """
    deposit = models.OneToOneField(Deposit, on_delete=models.CASCADE,
            related_name='package')
    file = models.FileField(upload_to='packages/%Y/%m/%d/', max_length=1024)
    md5_sum = models.CharField(max_length=32)  # 32 dígitos hexadecimais

    VIRUS_SCAN_STATUS = Choices(
            PACKAGE_VIRUSSCAN_STATUS_QUEUED,
            PACKAGE_VIRUSSCAN_STATUS_UNDETERMINED,
            PACKAGE_VIRUSSCAN_STATUS_INFECTED,
            PACKAGE_VIRUSSCAN_STATUS_UNINFECTED)
    virus_scan_status = StatusField(choices_name='VIRUS_SCAN_STATUS')
    virus_scan_status_changed = MonitorField(monitor='virus_scan_status',
            when=[PACKAGE_VIRUSSCAN_STATUS_UNDETERMINED,
                  PACKAGE_VIRUSSCAN_STATUS_INFECTED,
                  PACKAGE_VIRUSSCAN_STATUS_UNINFECTED])
    virus_scan_details = models.CharField(max_length=2048, default='')

    def xmls(self):

        xmls = {
            'valid': [], 'invalid': [], 'undefined': []
        }

        for member in self.members.all():
            if not member.is_xml():
                continue

            if member.sps_validation_status()[0] is True:
                xmls['valid'].append(member)

            if member.sps_validation_status()[0] is False:
                xmls['invalid'].append(member)

            if member.sps_validation_status()[0] is None:
                xmls['undefined'].append(member)

        return xmls


class PackageMember(models.Model):
    """Arquivo membro de ``Package``.
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE,
            related_name='members')
    name = models.CharField(max_length=1024)

    def open(self):
        """Extrai o membro como um objeto tipo arquivo -- instância de
        ``zipfile.ZipExtFile``.

        Deve ser utilizado preferencialmente com gerenciador de contexto, e.g.:

            with package_member.open() as member_file:
                data = member_file.read()
        """
        with packtools_utils.Xray.fromfile(self.package.file.path) as xpack:
            return xpack.get_file(self.name)

    def __str__(self):
        return self.name

    def is_xml(self):
        return self.name.endswith('.xml')

    def sps_validation_status(self):
        """O resultado da validação do membro contra a SciELO PS.

        Retorna uma tupla na forma: Tuple[bool, dict], onde o primeiro item
        indica se o documento é valido, e o segundo os detalhes da validação.
        A execução desse método em instâncias que não representam documentos
        XML ou em instâncias de documentos XML que ainda não foram submetidas
        a validação retornará uma tupla na forma: Tuple[None, dict].
        """
        try:
            xmlattrs = self.xml_control_attrs
        except XMLMemberControlAttrs.DoesNotExist:
            return (None, {})
        else:
            if XMLMEMBER_SPS_STATUS_VALID == xmlattrs.sps_check_status:
                is_valid = True
            else:
                is_valid = False

            return (is_valid, xmlattrs.sps_check_details)

    def guess_type(self):
        """Infere o mimetype do membro.

        Retorna uma string de texto no formato ``'tipo/subtipo'`` ou ``None``.

        A inferência é realizada por meio da função ``mimetypes.guess_type``,
        da biblioteca padrão da linguagem. Tipos adicionais -- fora do padrão
        IANA mas comumente utilizados -- são suportados.

        Mais informação em:
        https://docs.python.org/3/library/mimetypes.html#mimetypes.guess_type
        """
        type, _ = mimetypes.guess_type(self.name, strict=False)
        return type


class XMLMemberControlAttrs(models.Model):
    """Atributos de controle para ``PackageMember`` do tipo XML.
    """
    member = models.OneToOneField(PackageMember, on_delete=models.CASCADE,
            related_name='xml_control_attrs')

    SPS_CHECK_STATUS = Choices(
            XMLMEMBER_SPS_STATUS_VALID,
            XMLMEMBER_SPS_STATUS_INVALID)
    sps_check_status = StatusField(choices_name='SPS_CHECK_STATUS')
    sps_check_status_changed = MonitorField(monitor='sps_check_status')
    sps_check_details = JSONField()


@receiver(signals.package_deposited)
def create_package_members(sender, instance, **kwargs):
    """Cria as entidades de representam cada arquivo membro de ``Package``.

    :param instance: instância de ``models.Deposit``.
    """
    celery.current_app.send_task(
            'frontdesk.tasks.create_package_members',
            args=[instance.package.pk])


@receiver(signals.package_deposited)
def scan_package_for_viruses(sender, instance, **kwargs):
    """Varre o arquivo referenciado por ``Package.file`` em busca de vírus.

    :param instance: instância de ``models.Deposit``.
    """
    celery.current_app.send_task(
            'frontdesk.tasks.scan_package_for_viruses',
            args=[instance.package.pk])


@receiver(signals.package_members_created)
def validate_package_member_against_sps(sender, instance, **kwargs):
    """Valida XMLs contra a SciELO PS.

    :param instance: instância de ``models.Package``.
    """
    for member in instance.members.all():
        if member.is_xml():
            celery.current_app.send_task(
                    'frontdesk.tasks.validate_package_member',
                    args=[member.pk])

