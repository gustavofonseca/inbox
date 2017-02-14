from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def app_build_ref(left_token='', right_token=''):
    """Exibe o valor de referência da revisão mais recente do projeto.

    O valor de referência é obtido por meio da variável ``settings.VCS_REF``,
    No caso de implantações com base em imagens Docker, o valor é definido
    automaticamente na construção da imagem ``scieloorg/inbox``.

    Caracteres arbitrários poderão ser utilizados para encerrar o valor, e.g.:
    ``app_build_ref('[', ']')  == '[foobar]'``.
    """
    vcs_ref = getattr(settings, 'VCS_REF', None)
    return ''.join([left_token, vcs_ref, right_token]) if vcs_ref else ''

