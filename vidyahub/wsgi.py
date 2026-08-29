"""
WSGI config for vidyahub project with Socket.IO support.
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import django
django.setup()

# Auto-migrate database in background thread on startup
def _async_migrate():
    try:
        from django.core.management import call_command
        print("Running database migrations in background...", flush=True)
        call_command('migrate', interactive=False)
        print("Database migrations complete!", flush=True)
    except Exception as e:
        print(f"Migration note: {e}", flush=True)

import threading
threading.Thread(target=_async_migrate, daemon=True).start()

import socketio
from django.core.wsgi import get_wsgi_application
from vidyahub.socket_server import sio

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)
