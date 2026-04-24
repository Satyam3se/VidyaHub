import os
import sys

os.environ['PRODUCTION'] = 'True'

print("Eventlet monkey patch...", flush=True)
import eventlet
eventlet.monkey_patch()
print("Monkey patched", flush=True)

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("Django setup...", flush=True)
import django
import eventlet.wsgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

print("Creating apps...", flush=True)

from django.core.wsgi import get_wsgi_application
django_app = get_wsgi_application()

from vidyahub import socket_server
print(f"Socket async mode: {socket_server.sio.async_mode}", flush=True)

from socketio import WSGIApp
application = WSGIApp(socket_server.sio, django_app, socketio_path='/socket.io')

print(f"App type: {type(application)}", flush=True)

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Get port from environment (Render sets PORT)
port = int(os.environ.get('PORT', 8000))
print(f"Starting on port {port}...", flush=True)
print("=" * 40, flush=True)

eventlet.wsgi.server(eventlet.listen(('', port)), application)