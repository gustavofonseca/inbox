import hashlib

import pyclamd
from django.conf import settings


CLAMAV_HOST = settings.CLAMAV_HOST
CLAMAV_PORT = settings.CLAMAV_PORT


def checksum_file(file, algorithm=hashlib.md5):
    """Resumo do arquivo ``file``, em hexadecimal, usando ``algorithm``.

    A invocação dessa função altera o *offset* de ``file``. Caso esse
    comportamento seja indesejável, veja ``safe_checksum_file``.

    :param file: Objeto do tipo arquivo.
    :param algorithm: (opcional) Invocável que produz o algorítmo utilizado
                      na produção do hash. Ver: ``hashlib.algorithms_available``.
    """
    _algorith = algorithm()

    while True:
        chunk = file.read(1024)
        if not chunk:
            break

        _algorith.update(chunk)

    return _algorith.hexdigest()


def safe_checksum_file(file, algorithm=hashlib.md5):
    """Resumo do arquivo ``file``, em hexadecimal, usando ``algorithm``.

    A invocação dessa função *NÃO* altera o *offset* de ``file``.

    :param file: Objeto do tipo arquivo.
    :param algorithm: (opcional) Invocável que produz o algorítmo utilizado
                      na produção do hash. Ver: ``hashlib.algorithms_available``.
    """
    if not file.seekable():
        raise TypeError('Object "file" does not support random access.')

    former_offset = file.tell()
    try:
        return checksum_file(file, algorithm=algorithm)

    finally:
        file.seek(former_offset)


class AntivirusConnectionError(pyclamd.ConnectionError):
    """Erro de conexão com o serviço do ClamAV.
    """


class AntivirusBufferTooLongError(pyclamd.BufferTooLongError):
    """Excede o limite do buffer do ClamAV.
    """


def scan_file_for_viruses(file):
    """Varre ``file`` em busca de vírus, utilizando ClamAV.

    Pode levantar as exceções:
      - pyclamd.BufferTooLongError(ValueError)
      - pyclamd.ConnectionError(socket.error)

    Essa função traduz exceções a fim de isolar a dependência ``pyclamd``,
    portanto, para aumentar o isolamento é recomendado que sejam tratadas as
    exceções ``utils.AntivirusConnectionError`` e
    ``utils.AntivirusBufferTooLongError``. Exemplo:

      try:
          is_infected, details = scan_file_for_viruses(fileobject)
      except (AntivirusBufferTooLongError, AntivirusConnectionError):
          # ``fileobject`` excede o limite do buffer do ClamAV ou a instância
          # do ClamAV não pode ser contactada.
          pass

    :param file: Objeto do tipo arquivo.
    """
    try:
        antivirus = pyclamd.ClamdNetworkSocket(
                host=CLAMAV_HOST, port=CLAMAV_PORT)
    except pyclamd.ConnectionError as exc:
        raise AntivirusConnectionError() from exc

    try:
        result = antivirus.scan_stream(file.read())
    except pyclamd.ConnectionError as exc:
        raise AntivirusConnectionError() from exc
    except pyclamd.BufferTooLongError as exc:
        raise AntivirusBufferTooLongError() from exc
    finally:
        # O método ``antivirus.scan_stream`` não garante o fechamento da
        # socket em caso de exceções.
        antivirus._close_socket()

    if result:
        return True, result['stream']
    else:
        return False, ''

