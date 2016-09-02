from django.db import transaction

from . import (
        models,
        utils,
)


class BaseFrontdeskException(Exception):
    """Raíz de todos os males.
    """


class ChecksumError(BaseFrontdeskException):
    """Soma de verificação dos arquivos não é idêntica.
    """


@transaction.atomic
def deposit_package(file, md5_sum):
    """Deposita o pacote.

    Essa função realiza a conferência da soma md5 de ``file``. Retorna o
    identificador do depósito.

    :param file: Instância de ``django.core.files.base.File``.
    :param md5_sum: String de texto contendo a soma md5 de ``file``.
    """
    if md5_sum != utils.safe_checksum_file(file):
        raise ChecksumError()

    deposit = models.Deposit.objects.create()
    package = models.Package.objects.create(
            deposit=deposit, file=file, md5_sum=md5_sum)

    return deposit.pk

