from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^deposits/$', views.deposit_package, name='deposits'),
]
