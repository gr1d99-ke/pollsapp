from contextvars import ContextVar

from tenants.utils import tenant_db_from_request

TENANT_DB = ContextVar('tenant_db')


class TenantMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        db = tenant_db_from_request(request)
        set_db_for_router(db)
        response = self.get_response(request)
        return response


def set_db_for_router(db):
    TENANT_DB.set(db)


def get_current_db():
    try:
        return TENANT_DB.get()
    except LookupError:
        return None
