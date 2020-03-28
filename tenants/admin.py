from django.contrib import admin

from .models import Tenant


class TenantAdmin(admin.ModelAdmin):
    fields = ['name', 'subdomain_prefix']
    list_display = ['name', 'subdomain_prefix']


admin.site.register(Tenant, TenantAdmin)