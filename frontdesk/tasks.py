import logging

from django.db import transaction
from penne_core.taskapp.celery import app
from . import models

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

