import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import django
django.setup()

import socketio
from django.core.wsgi import get_wsgi_application
from vidyahub.socket_server import sio
from wsgiref.simple_server import make_server

# Create the apps
django_app = get_wsgi_application()

# Combined app
combined_app = socketio.WSGIApp(sio, django_app)

if __name__ == '__main__':
    port = 8000
    print(f"Starting VidyaHub Combined Server on port {port}...", flush=True)
    server = make_server('0.0.0.0', port, combined_app)
    server.serve_forever()
