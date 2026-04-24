"""
WSGI config for vidyahub project.
"""
import os

PRODUCTION = os.environ.get('PRODUCTION', os.environ.get('RENDER_EXTERNAL_HOSTNAME') is not None).lower() == 'true'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

if PRODUCTION:
    import eventlet
    eventlet.monkey_patch()

from django.core.wsgi import get_wsgi_application

django_app = get_wsgi_application()

if PRODUCTION:
    from socketio import Server, WSGIApp
    from .socket_server import sio
    application = WSGIApp(sio, django_app, socketio_path='/socket.io')
else:
    application = django_app
