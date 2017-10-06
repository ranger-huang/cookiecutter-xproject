import logging

from django.template import Template
from rest_framework.renderers import \
    TemplateHTMLRenderer as _TemplateHTMLRenderer

logger = logging.getLogger(__name__)


class TemplateHTMLRenderer(_TemplateHTMLRenderer):

    exception_template_names = [
        'xlock_xpay/pages/%(status_code)s.html',
        '%(status_code)s.html',
        'error.html',
        'xlock_xpay/pages/error.html',
        'api_exception.html'
    ]

    def get_template_context(self, data, renderer_context):
        response = renderer_context['response']
        data['status_code'] = response.status_code
        return data

    def get_exception_template(self, response):
        template_names = []
        if getattr(response, 'template_name', None):
            template_names = [response.template_name]

        template_names = template_names + [name % {'status_code': response.status_code}
                          for name in self.exception_template_names]

        try:
            # Try to find an appropriate error template
            return self.resolve_template(template_names)
        except Exception:
            # Fall back to using eg '404 Not Found'
            return Template('%d %s' % (response.status_code,
                                       response.status_text.title()))
