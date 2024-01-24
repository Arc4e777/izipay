from django.db import models
from merchants.models import Service

from django.utils.translation import gettext_lazy as _

from rest_framework_api_key.models import AbstractAPIKey
# Create your models here.

class ServiceAPIKey(AbstractAPIKey):
	service = models.ForeignKey(
		Service,
		on_delete=models.CASCADE,
		related_name='api_keys',
		verbose_name=_('Service')
	)

	class Meta:
		verbose_name = _('Service API key')
		verbose_name_plural = _('Service API keys')