# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from inbox import views as pc_views  # views em nível de projeto


urlpatterns = [
    url(r'^$', pc_views.index, name='index'),
    url(r'^(?P<deposit_id>[0-9]+)/$', pc_views.package_report, name='package_report'),
    url(r'^(?P<deposit_id>[0-9]+)/reports/virus/', pc_views.package_report_virus, name='package_report_virus'),
    url(r'^(?P<deposit_id>[0-9]+)/reports/integrity/', pc_views.package_report_integrity, name='package_report_integrity'),
    url(r'^(?P<deposit_id>[0-9]+)/reports/scielops/', pc_views.package_report_scielops, name='package_report_scielops'),

    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include('inbox.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
    url(r'frontdesk/', include('frontdesk.urls', namespace='frontdesk')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
