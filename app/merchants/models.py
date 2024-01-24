from django.db import models
from django.core.exceptions import ValidationError

from django.utils.translation import gettext_lazy as _

import re
# Create your models here.

class Service(models.Model):
	name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))

	class Meta:
		verbose_name = _('Service')
		verbose_name_plural = _('Services')

	def __str__(self) -> str:
		return self.name

class Trader(models.Model):
	service = models.ForeignKey(Service, on_delete=models.CASCADE, verbose_name=_('Service'))
	name = models.CharField(max_length=100, verbose_name=_('Name'))

	class Meta:
		verbose_name = _('Trader')
		verbose_name_plural = _('Traders')

	def __str__(self) -> str:
		return f'{self.service}/{self.name}'

	def validate_unique(self, exclude=None):
		if hasattr(self, 'service'):
			qs = Trader.objects.filter(service=self.service, name=self.name)
			if qs.exists() and qs.first().pk != self.pk:
				raise ValidationError({'name': [_('This name already exists')]})

		super().validate_unique(exclude=exclude)

	def get_address_list(self) -> list:
		return [address.address for address in Address.objects.filter(trader=self)]

def validate_address(address: str) -> str:
	regex = r'^[T][a-km-zA-HJ-NP-Z1-9]{25,34}$'
	result = re.search(regex, address)
	if not result:
		raise ValidationError(_('Incorrect tron address'))

	return address

class Address(models.Model):
	trader = models.ForeignKey(Trader, on_delete=models.CASCADE, verbose_name=_('Trader'))
	address = models.CharField(max_length=100, validators=[validate_address], verbose_name=_('Address'))

	class Meta:
		verbose_name = _('Address')
		verbose_name_plural = _('Addresses')

	def __str__(self) -> str:
		return ''

	def validate_unique(self, exclude=None):
		qs = Address.objects.filter(trader=self.trader, address=self.address)
		if qs.exists() and qs.first().pk != self.pk:
			raise ValidationError({'address': [_('This address already exists')]})

		super().validate_unique(exclude=exclude)
















