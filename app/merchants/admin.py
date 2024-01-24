from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from . import models
from api.models import ServiceAPIKey
# Register your models here.
admin.site.site_header = 'IZIPAY ADMIN'

@admin.register(models.Service)
class ServiceAdmin(admin.ModelAdmin):
	list_display = ['name', 'traders', 'api_keys']
	readonly_fields = ['traders', 'api_keys']
	search_fields = ['name']

	def traders(self, obj):
		count = models.Trader.objects.filter(service=obj).count()
		url = f'/admin/merchants/trader/?service__id__exact={obj.pk}'

		return format_html(f'{count} - <a href="{url}" style="color: var(--link-hover-color);">{_("View")}</a>')
	traders.short_description = _('Traders')

	def api_keys(self, obj):
		count = ServiceAPIKey.objects.filter(service=obj).count()
		url = f'/admin/api/serviceapikey/?service__id__exact={obj.pk}'

		return format_html(f'{count} - <a href="{url}" style="color: var(--link-hover-color);">{_("View")}</a>')
	api_keys.short_description = _('API keys')

class AddressInline(admin.TabularInline):
	model = models.Address
	extra = 0

	def has_change_permission(self, request, obj=None):
		return False

@admin.register(models.Trader)
class TraderAdmin(admin.ModelAdmin):
	show_facets = admin.ShowFacets.ALWAYS
	
	list_display = ['name', 'service']
	list_filter = ['service']
	search_fields = ['name']

	def add_view(self, request, extra_context=None):
		self.readonly_fields = []
		self.inlines = []
		return super().add_view(request, extra_context=extra_context)

	def change_view(self, request, object_id, extra_context=None):
		self.readonly_fields = ['service']
		self.inlines = [AddressInline]
		return super().change_view(request, object_id, extra_context=extra_context)

	fieldsets = (
		('', {'fields': ('service', 'name')}),
	)



	