from unittest import TestCase

from django.template import Template, Context

from frontdesk.models import (
        Package,
        PACKAGE_VIRUSSCAN_STATUS_QUEUED,
        PACKAGE_VIRUSSCAN_STATUS_UNDETERMINED,
        PACKAGE_VIRUSSCAN_STATUS_INFECTED,
        PACKAGE_VIRUSSCAN_STATUS_UNINFECTED,
)
from frontdesk.templatetags import frontdesk_extras as tags


class WidgetScielopsColorsWeightTests(TestCase):
    """Testa a regra de precedência para a obtenção da cor que representa o
    status geral do pacote.
    """

    def test_implicitly_undefined(self):
        xmls = {
            'valid': [],
            'invalid': [],
            'undefined': [],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['undefined'])

    def test_explicitly_undefined(self):
        xmls = {
            'valid': [],
            'invalid': [],
            'undefined': [True],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['undefined'])

    def test_explicitly_invalid(self):
        xmls = {
            'valid': [],
            'invalid': [True],
            'undefined': [],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['invalid'])

    def test_invalid_prevails_over_undefined(self):
        xmls = {
            'valid': [],
            'invalid': [True],
            'undefined': [True],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['invalid'])

    def test_explicitly_valid(self):
        xmls = {
            'valid': [True],
            'invalid': [],
            'undefined': [],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['valid'])

    def test_undefined_prevails_over_valid(self):
        xmls = {
            'valid': [True],
            'invalid': [],
            'undefined': [True],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['undefined'])

    def test_invalid_prevails_over_valid(self):
        xmls = {
            'valid': [True],
            'invalid': [True],
            'undefined': [],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['invalid'])

    def test_invalid_prevails_over_all(self):
        xmls = {
            'valid': [True],
            'invalid': [True],
            'undefined': [True],
        }

        self.assertEqual(tags.widget_scielops_colors_weight(xmls),
                tags.STATUS_COLORS['invalid'])


class TemplatetagsTest(TestCase):
    def test_status_widget_scielops_colors_weight_invalid(self):
        template = Template(
            "{% load frontdesk_extras %} {{ xmls|widget_scielops_colors_weight }}")

        xmls = {
            'valid': ['item', 'item'], 'invalid': ['item'], 'undefined': ['item', 'item']
        }

        rendered = template.render(Context({'xmls': xmls}))

        self.assertIn('red', rendered)

    def test_status_widget_scielops_colors_weight_undefined(self):
        template = Template(
            "{% load frontdesk_extras %} {{ xmls|widget_scielops_colors_weight }}")

        xmls = {
            'valid': ['item', 'item'], 'invalid': [], 'undefined': ['item']
        }

        rendered = template.render(Context({'xmls': xmls}))

        self.assertIn('blue', rendered)

    def test_status_widget_scielops_colors_weight_valid(self):
        template = Template(
            "{% load frontdesk_extras %} {{ xmls|widget_scielops_colors_weight }}")

        xmls = {
            'valid': ['item', 'item'], 'invalid': [], 'undefined': []
        }

        rendered = template.render(Context({'xmls': xmls}))

        self.assertIn('green', rendered)

    def test_status_widget_scielops_colors_weight(self):
        template = Template(
            "{% load frontdesk_extras %} {{ xmls|widget_scielops_colors_weight }}")

        xmls = {
            'valid': ['2'], 'invalid': ['3'], 'undefined': ['2']
        }

        rendered = template.render(Context({'xmls': xmls}))

        self.assertIn('red', rendered)

    def test_status_sps_valid(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_sps }}")

        rendered = template.render(Context({'status': (True, {})}))

        self.assertIn('valid', rendered)

    def test_status_sps_invalid(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_sps }}")

        rendered = template.render(Context({'status': (False, {})}))

        self.assertIn('invalid', rendered)

    def test_status_sps_undefined(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_sps }}")

        rendered = template.render(Context({'status': (None, {})}))

        self.assertIn('undefined', rendered)

    def test_status_color_default(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({}))

        self.assertIn('grey', rendered)

    def test_status_color_infected(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'infected'}))

        self.assertIn('red', rendered)

    def test_status_color_unknow(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'unknow'}))

        self.assertIn('grey', rendered)

    def test_status_color_rejected(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'rejected'}))

        self.assertIn('red', rendered)

    def test_status_color_uninfected(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'uninfected'}))

        self.assertIn('green', rendered)

    def test_status_color_deposited(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'deposited'}))

        self.assertIn('blue', rendered)

    def test_status_color_queued(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'queued'}))

        self.assertIn('blue', rendered)

    def test_status_color_accepted(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'accepted'}))

        self.assertIn('green', rendered)

    def test_status_color_valid(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'valid'}))

        self.assertIn('green', rendered)

    def test_status_color_invalid(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'invalid'}))

        self.assertIn('red', rendered)

    def test_status_color_undefined(self):
        template = Template(
            "{% load frontdesk_extras %} {{ status|status_color }}")

        rendered = template.render(Context({'status': 'undefined'}))

        self.assertIn('blue', rendered)

    def test_should_warn_before_downloading_queued(self):
        result = tags.should_warn_before_downloading(
                PACKAGE_VIRUSSCAN_STATUS_QUEUED)
        self.assertTrue(result)

    def test_should_warn_before_downloading_undetermined(self):
        result = tags.should_warn_before_downloading(
                PACKAGE_VIRUSSCAN_STATUS_UNDETERMINED)
        self.assertTrue(result)

    def test_should_warn_before_downloading_infected(self):
        result = tags.should_warn_before_downloading(
                PACKAGE_VIRUSSCAN_STATUS_INFECTED)
        self.assertTrue(result)

    def test_should_warn_before_downloading_uninfected(self):
        result = tags.should_warn_before_downloading(
                PACKAGE_VIRUSSCAN_STATUS_UNINFECTED)
        self.assertFalse(result)

    def test_should_warn_before_downloading_unknown_status(self):
        self.assertRaises(ValueError,
                          lambda: tags.should_warn_before_downloading(Package()))
