from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import loader
from django.http import (
        JsonResponse,
        HttpResponse,
        HttpResponseBadRequest,
        HttpResponseNotAllowed,
)

from . import transactions, forms


@csrf_exempt
def deposit_package(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = forms.DepositForm(request.POST, request.FILES)
    if form.is_valid():
        deposit_id = transactions.deposit_package(request.FILES['package'],
                request.POST['md5_sum'])

        return JsonResponse({'deposit_id': deposit_id})

    else:
        return HttpResponseBadRequest()


@csrf_exempt
def deposit_dashboard(request):

    template = loader.get_template('frontdesk/dashboard.html')

    return HttpResponse(template.render({}, request))
