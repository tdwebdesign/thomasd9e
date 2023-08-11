"""
WSGI config for thomasd9e project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from .utils import download_service_account_key

# Download the service account key at startup
download_service_account_key()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thomasd9e.settings")

application = get_wsgi_application()
