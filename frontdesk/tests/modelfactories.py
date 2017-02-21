import os
import random

from django.db.models import signals
import factory
from packtools import utils as packtools_utils

from frontdesk import (
        models,
        utils,
)


_CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SAMPLE_PACKAGE = os.path.join(
        _CURRENT_DIR, 'fixtures', '0004-2730-aem-60-4.zip')
SAMPLE_PACKAGE_NOTWELLFORMED = os.path.join(
        _CURRENT_DIR, 'fixtures', '0004-2730-aem-60-4.notwellformed.zip')


class DepositFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Deposit

    depositor = factory.Sequence(lambda n: 'Dep %03d' % n)


@factory.django.mute_signals(signals.post_save)
class PackageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Package

    deposit = factory.SubFactory(DepositFactory)
    file = factory.django.FileField(data=open(SAMPLE_PACKAGE, 'rb').read(),
            filename='0004-2730-aem-60-4.zip')

    @factory.lazy_attribute
    def md5_sum(self):
        return utils.safe_checksum_file(self.file)


class PackageMemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.PackageMember

    package = factory.SubFactory(PackageFactory)

    @factory.lazy_attribute
    def name(self):
        with packtools_utils.Xray.fromfile(self.package.file.path) as xpack:
            members = xpack.show_members()

        return members[random.randint(0, len(members) - 1)]

