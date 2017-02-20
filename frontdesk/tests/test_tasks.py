from django.test import TestCase

from frontdesk import (
        tasks,
        models,
)
from . import modelfactories


class ValidatePackageMemberTests(TestCase):

    def test_unknown_member_id_raises_value_error(self):
        self.assertRaises(ValueError,
                lambda: tasks.validate_package_member(10928374871234))

    def test_xml_members_are_validated(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0407.xml')

        _ = tasks.validate_package_member(member.pk)

        self.assertIsInstance(member.xml_control_attrs,
                models.XMLMemberControlAttrs)

    def test_validation_results_are_saved_correctely(self):
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0407.xml')

        _ = tasks.validate_package_member(member.pk)

        self.assertTrue(member.xml_control_attrs.sps_check_status in
                [models.SPSStatus.VALID, models.SPSStatus.INVALID])
        self.assertIsInstance(member.xml_control_attrs.sps_check_details,
                dict)

    def test_non_xml_members_are_skipped(self):
        """Testamos que a instância de ``models.XMLMemberControlAttrs`` não
        é criada e associada ao atributo ``member.xml_control_attrs``.
        """
        member = modelfactories.PackageMemberFactory(
                name='0004-2730-aem-60-4/0004-2730-aem-60-4-0407.pdf')

        _ = tasks.validate_package_member(member.pk)

        self.assertRaises(models.XMLMemberControlAttrs.DoesNotExist,
                lambda: member.xml_control_attrs)

