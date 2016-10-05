from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

STATUS_COLORS = {
    'default': 'blue',
    'queued': 'blue',
    'undetermined': 'blue',
    'infected': 'red',
    'uninfected': 'green',
    'deposited': 'blue',
    'rejected': 'red',
    'accepted': 'green',
    'valid': 'green',
    'invalid': 'red',
    'undefined': 'blue'
}

BOX_COLORS = {
    'blue': 'primary',
    'red': 'danger',
    'green': 'success',
    'grey': 'default'
}


@register.filter
@stringfilter
def status_color(status):
    """
    This method will return grey for a unkown status.
    """

    return STATUS_COLORS.get(status, 'grey')


@register.filter
def box_color(status):
    """
    This method will return grey for a unkown status.
    """

    return BOX_COLORS.get(STATUS_COLORS.get(status, 'grey'), 'default')


@register.filter
def status_sps(status):
    """
    This method will return valid, invalid or undefined for a given result of
    models.PackageMember.sps_validation_status().

    status: Tuple(None, {})
    status: Tuple(True, {'is_valid': True, 'sps_errors': [], 'dtd_errors': []})
    status: Tuple(False, {'is_valid': True, 'sps_errors': [], 'dtd_errors': []})
    """

    if status[0] is True:
        return 'valid'

    if status[0] is False:
        return 'invalid'

    return 'undefined'

@register.filter
def widget_scielops_colors_weight(xmls):
    """
    This method will return a color for the SciELO PS widget. The color will
    be matched according to the error level of any of the members of the package.

    status: Dict with xml's returned by models.Package.xmls().
    """

    if len(xmls['invalid']) > 0:
        return STATUS_COLORS['invalid']

    if len(xmls['undefined']) > 0:
        return STATUS_COLORS['undefined']

    if len(xmls['valid']) == 0:
        return STATUS_COLORS['undefined']

    return STATUS_COLORS['valid']