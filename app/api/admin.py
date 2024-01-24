from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from rest_framework_api_key.admin import APIKeyModelAdmin

from . import models
from rest_framework_api_key.models import APIKey

# Register your models here.
admin.site.unregister(APIKey)

@admin.register(models.ServiceAPIKey)
class ServiceAPIKeyAdmin(APIKeyModelAdmin):
	show_facets = admin.ShowFacets.ALWAYS

	list_display = ['service', 'name', 'created', 'prefix']
	list_filter = ['service', *APIKeyModelAdmin.list_filter]

	def add_view(self, request, extra_context=None):
		self.fieldsets = (
			('', {'fields': ('service', 'name')}),
		)
		return super().add_view(request, extra_context=extra_context)

	def change_view(self, request, object_id, extra_context=None):
		self.fieldsets = (
			(_('General info'), {'fields': ('service', 'name')}),
			(_('Additional info'), {'fields': ('created', 'prefix')})
		)
		return super().change_view(request, object_id, extra_context=extra_context)

	def get_readonly_fields(self, request, obj):
		if obj:
			add_fields = ('service', 'name', 'created')
		else:
			add_fields = ('created', )

		return super().get_readonly_fields(request, obj) + add_fields