import logging

from django.db import transaction
from penne_core.taskapp.celery import app
from . import (
        models,
        utils,
)

from packtools import (
        stylechecker,
        utils as packtools_utils,
)


LOGGER = logging.getLogger(__name__)


@app.task(ignore_result=True)
def create_package_members(package_id):
    package = models.Package.objects.get(pk=package_id)

    with packtools_utils.Xray.fromfile(package.file.path) as xpack:
        with transaction.atomic():
            for member in xpack.show_members():
                models.PackageMember.objects.create(
                        package=package, name=member)


@app.task(bind=True, default_retry_delay=300, max_retries=5, ignore_result=True)
def scan_package_for_viruses(self, package_id):
    package = models.Package.objects.get(pk=package_id)

    try:
        is_infected, details = utils.scan_file_for_viruses(package.file)
    except utils.AntivirusConnectionError as exc:
        self.retry(exc)
    except utils.AntivirusBufferTooLongError as exc:
        scan_status = models.PACKAGE_VIRUSSCAN_STATUS_UNDETERMINED
        scan_details = str(exc)
    else:
        if is_infected:
            scan_status = models.PACKAGE_VIRUSSCAN_STATUS_INFECTED
        else:
            scan_status = models.PACKAGE_VIRUSSCAN_STATUS_UNINFECTED

        scan_details = str(details)  # representação textual de uma tupla

    package.virus_scan_status = scan_status
    package.virus_scan_details = scan_details
    package.save()

