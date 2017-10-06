# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),

    # Django Admin, use {% raw %}{% url 'admin:index' %}{% endraw %}
    url(settings.ADMIN_URL, admin.site.urls),

    # User management
    url(r'^users/', include('{{ cookiecutter.system_project_slug }}.users.urls', namespace='users')),
    url(r'^accounts/', include('allauth.urls')),

    # Your stuff: custom urls includes go here
]

from . import urls_error
urlpatterns += urls_error.urlpatterns

if settings.DEBUG:
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns += [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
                   + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if 'rest_framework_swagger' in settings.INSTALLED_APPS:
    from django.conf.urls import url
    from rest_framework_swagger.views import get_swagger_view
    schema_view = get_swagger_view(title='{{cookiecutter.project_name}} API')
    urlpatterns += [
        url(r'^$', schema_view)
    ]
