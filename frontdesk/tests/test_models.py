from django.test import TestCase

from . import modelfactories


class PackageMemberTests(TestCase):

    def test_type_guessing_for_xml_members(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0407.xml')
        self.assertEqual('application/xml', member.guess_type())

    def test_type_guessing_for_pdf_members(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0299.pdf')
        self.assertEqual('application/pdf', member.guess_type())

    def test_type_guessing_for_jpg_members(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0367-gf01.jpg')
        self.assertEqual('image/jpeg', member.guess_type())

    def test_type_guessing_for_jpeg_members(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0367-gf01.jpeg')
        self.assertEqual('image/jpeg', member.guess_type())

    def test_type_guessing_for_tif_members(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0367-gf01.tif')
        self.assertEqual('image/tiff', member.guess_type())

    def test_type_guessing_for_tiff_members(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0367-gf01.tiff')
        self.assertEqual('image/tiff', member.guess_type())

    def test_type_guessing_for_members_without_file_extension(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0367-gf01')
        self.assertEqual(None, member.guess_type())

