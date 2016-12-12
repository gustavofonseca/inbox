import logging

from django.views.decorators.csrf import csrf_exempt
from django.http import (
        JsonResponse,
        HttpResponseBadRequest,
)
from django.views.decorators.http import require_http_methods

from . import (
        transactions,
        forms,
)


LOGGER = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def deposit_package(request):
    form = forms.DepositForm(request.POST, request.FILES)
    if form.is_valid():
        try:
            deposit_id = transactions.deposit_package(
                form.cleaned_data['package'],
                form.cleaned_data['md5_sum'],
                form.cleaned_data['depositor']
            )

        except transactions.ChecksumError as exc:
            LOGGER.exception(exc)
            return HttpResponseBadRequest()

        return JsonResponse({'deposit_id': deposit_id})

    else:
        return HttpResponseBadRequest()
