import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import eventlet
eventlet.monkey_patch()

import django
django.setup()

import eventlet.wsgi
import socketio
from django.core.wsgi import get_wsgi_application
from vidyahub.socket_server import sio

# Create the apps
django_app = get_wsgi_application()

# Combined app
combined_app = socketio.Middleware(sio, django_app)

if __name__ == '__main__':
    port = 8000
    print(f"Starting VidyaHub Combined Server on port {port}...")
    eventlet.wsgi.server(eventlet.listen(('', port)), combined_app)
