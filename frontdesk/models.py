import celery
from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver

from model_utils.models import TimeStampedModel
from model_utils.fields import StatusField, MonitorField
from model_utils import Choices

from packtools import utils as packtools_utils


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


@receiver(post_save, sender=Package)
def create_package_members(sender, instance, created, **kwargs):
    """Cria as entidades de representam cada arquivo membro de ``Package``.
    """
    if created:
        celery.current_app.send_task(
                'frontdesk.tasks.create_package_members',
                args=[instance.pk])

