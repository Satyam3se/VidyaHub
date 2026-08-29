"""
WSGI config for vidyahub project with Socket.IO support.
"""
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import django
django.setup()

# Auto-migrate database & seed course data on startup if empty
def _async_migrate():
    try:
        from django.core.management import call_command
        print("Running database migrations in background...", flush=True)
        call_command('migrate', interactive=False)
        print("Database migrations complete!", flush=True)
        
        # Auto-populate courses if new empty database is attached
        from main.models import Grade
        if Grade.objects.count() == 0:
            print("Fresh database detected! Auto-populating courses...", flush=True)
            from scripts.seeding.populate_cbse import populate_with_ultimate_cbse_data
            populate_with_ultimate_cbse_data()
            print("Courses auto-populated successfully!", flush=True)
    except Exception as e:
        print(f"Migration note: {e}", flush=True)

import threading
threading.Thread(target=_async_migrate, daemon=True).start()

import socketio
from django.core.wsgi import get_wsgi_application
from vidyahub.socket_server import sio

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)
