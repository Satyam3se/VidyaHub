import eventlet
eventlet.monkey_patch()

import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import django
django.setup()

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
