"""
WSGI config for vidyahub project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import socketio
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
from .socket_server import sio

django_app = StaticFilesHandler(get_wsgi_application())
application = socketio.WSGIApp(sio, django_app)
