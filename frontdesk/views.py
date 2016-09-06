from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import (
        render,
        get_object_or_404,
)
from django.http import (
        JsonResponse,
        HttpResponseBadRequest,
        HttpResponseNotAllowed,
)

from . import (
        transactions,
        forms,
        models,
)


@csrf_exempt
def deposit_package(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = forms.DepositForm(request.POST, request.FILES)
    if form.is_valid():
        deposit_id = transactions.deposit_package(
            request.FILES['package'],
            request.POST['md5_sum']
        )

        return JsonResponse({'deposit_id': deposit_id})

    else:
        return HttpResponseBadRequest()


def deposit_dashboard(request):
    show_deposit = request.GET.get('show', None)

    deposits = models.Deposit.objects.order_by('-created')[:10]
    if show_deposit:
        detailed_deposit = get_object_or_404(models.Deposit, pk=show_deposit)
    else:
        detailed_deposit = models.Deposit.objects.order_by('-created').first()

    context = {'deposits': deposits, 'detailed_deposit': detailed_deposit}
    return render(request, 'frontdesk/dashboard.html', context)

