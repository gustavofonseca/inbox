from django import template
from django.template.defaultfilters import stringfilter

from .. import models


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


ACCEPTED_VIRUS_SCAN_STATUSES = [
    models.VirusScanStatus.UNINFECTED,
    models.VirusScanStatus.QUEUED,
    models.VirusScanStatus.UNDETERMINED,
    models.VirusScanStatus.INFECTED,
]


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


@register.filter
def should_warn_before_downloading(virusscan_status):
    """
    Este método avalia o status da varredura de vírus no pacote para garantir
    que ele não está infectado.

    Quando o status for igual a constante do
    models.VirusScanStatus.UNINFECTED ele retornará falso.
    Não necessitando informar o usuário sobre a possibilidade de vírus no pacote.

    Este filtro foi projetado para auxiliar a confecção de templates,
    facilitando a decisão de exibição de um alerta especifico para a questão
    de vírus.

    :param virusscan_status: Valores válidos para o atributo
    ``models.Package.virus_scan_status.
    :return: bool

    """

    if virusscan_status not in ACCEPTED_VIRUS_SCAN_STATUSES:
        raise ValueError('Status not supported')

    if virusscan_status == models.VirusScanStatus.UNINFECTED:
        return False

    return True

