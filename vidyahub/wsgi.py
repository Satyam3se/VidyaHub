"""
WSGI config for vidyahub project.
"""
import os

PRODUCTION = os.environ.get('PRODUCTION', 'True').lower() == 'true'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
