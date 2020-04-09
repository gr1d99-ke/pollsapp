def get_tenants_map():
    return {
        "thor.polls.local": "thor",
        "potter.polls.local": "potter"
    }


def hostname_from_request(request):
    return request.get_host().split(':')[0].lower()


def tenant_db_from_request(request):
    hostname = hostname_from_request(request)
    tenants_map = get_tenants_map()
    return tenants_map.get(hostname)

