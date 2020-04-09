#!/usr/bin/env python

import os
import sys

from tenants.middleware import set_db_for_router

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pollsapp.settings")

    try:
        from django.core.management import execute_from_command_line

    except ImportError as exec:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exec

    from django.db import connection

    args = sys.argv
    db = args[1]

    with connection.cursor() as cursor:
        set_db_for_router(db)
        del args[1]
        execute_from_command_line(args)
