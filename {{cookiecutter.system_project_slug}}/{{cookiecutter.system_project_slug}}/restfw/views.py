# -*- coding: utf-8 -*-
from __future__ import absolute_import

import logging

from django.conf import settings
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.utils import six
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, status
from rest_framework.compat import set_rollback
from rest_framework.response import Response

from {{cookiecutter.system_slug}}_conf.constants import BUSINESS_STATE_CHOICES as BC
from {{cookiecutter.system_project_slug}}.restfw.response import XLocationResponse
from .serializers import XResponseResult as XResult

logger = logging.getLogger(__name__)


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    #view = context.get('view')
    request = context.get('request')
    request.extra_data = getattr(request, 'extra_data', dict())
    bcode = request.extra_data.get('code', BC.failure)
    template_name = getattr(exc, 'template_name', None)

    if isinstance(exc, exceptions.NotAuthenticated):

        response = redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
        response = XLocationResponse(response.url)
        set_rollback()
        return response

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = XResult(code=bcode, data=exc.detail, msg=exc.default_detail)
        else:
            data = XResult(code=bcode, data=None, msg=str(exc.detail))

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers,
                        template_name=template_name)

    elif isinstance(exc, Http404):
        msg = _('Not found.')
        data = XResult(code=bcode, msg=six.text_type(msg))

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND,
                        template_name=template_name)

    elif isinstance(exc, PermissionDenied):
        msg = _('Permission denied.')
        msg = str(exc) or six.text_type(msg)
        data = XResult(code=bcode, msg=msg)
        logger.warning("permission denied: %s, %s", msg, template_name)

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN, template_name=template_name)

    return None
