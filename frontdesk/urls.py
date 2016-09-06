from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^deposit/$', views.deposit_package),
        url(r'^dashboard/$', views.deposit_dashboard),
]
