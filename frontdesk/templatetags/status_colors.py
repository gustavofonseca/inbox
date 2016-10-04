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
    'accepted': 'green'
}


@register.filter
@stringfilter
def status_color(status):
    """
    This method will return gray for a unkown status.
    """

    return STATUS_COLORS.get(status, 'grey')