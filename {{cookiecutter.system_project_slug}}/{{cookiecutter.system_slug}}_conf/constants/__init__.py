from django.utils.translation import ugettext_lazy as _
from model_utils import Choices

# 业务码
BUSINESS_STATE = (
    (0, 'ok', _('OK')),
    (1, 'failure', _('Failure')),
)
BUSINESS_STATE_CHOICES = Choices(*BUSINESS_STATE)
