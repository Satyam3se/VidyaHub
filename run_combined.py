import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import django
django.setup()

# Auto-migrate database on startup
try:
    from django.core.management import call_command
    print("Running database migrations on startup...", flush=True)
    call_command('migrate', interactive=False)
    print("Database migrations complete!", flush=True)
except Exception as e:
    print(f"Migration on startup note: {e}", flush=True)

import socketio
from django.core.wsgi import get_wsgi_application
from vidyahub.socket_server import sio

# Create the apps
django_app = get_wsgi_application()

# Combined WSGI app: Socket.IO wraps Django
combined_app = socketio.WSGIApp(sio, django_app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting VidyaHub Combined Server on port {port}...", flush=True)
    eventlet.wsgi.server(eventlet.listen(('0.0.0.0', port)), combined_app)
