#!/usr/bin/env python
"""Simple server without eventlet for tunneling"""
import os
import sys

os.environ['PRODUCTION'] = 'True'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')

import django
django.setup()

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

port = int(os.environ.get('PORT', '8000'))
sys.stdout = sys.stderr = os.fdopen(1, 'w')
print(f"\n=== VidyaHub on http://0.0.0.0:{port}/ ===\n", flush=True)

from wsgiref.simple_server import make_server
hr = make_server('0.0.0.0', port, application)
print("Server running...", flush=True)
hr.serve_forever()