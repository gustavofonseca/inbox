from django.conf.urls import url

from . import views


urlpatterns = [
        url(r'^$', views.main, name='main'),
        url(r'^deposits/$', views.deposit_package, name='deposits'),
]
