from tenants.utils import tenant_from_request


class TenantMixin(object):
    def get_tenant(self, request):
        return tenant_from_request(request)
