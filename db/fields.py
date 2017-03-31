import hashlib

from django.db import models

from frontdesk import utils


class ChecksummedFieldFile(models.fields.files.FieldFile):
    def checksum(self, algorithm):
        """A soma do arquivo.

        Os algoritmos suportados são ``md5`` e ``sha256``.
        """
        if algorithm not in ['md5', 'sha256']:
            raise ValueError('cannot generate checksum: algorithm '
                             '"%s" is not supported' % algorithm)

        try:
            self.open()
            return utils.checksum_file(self,
                    algorithm=getattr(hashlib, algorithm))
        finally:
            self.close()

    @property
    def sha256(self):
        return self.checksum('sha256')

    @property
    def md5(self):
        return self.checksum('md5')


class ChecksummedFileField(models.fields.files.FileField):
    attr_class = ChecksummedFieldFile

