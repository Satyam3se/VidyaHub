"""
VidyaHub Socket Server for Live Battles
Run this separately: python socket_run.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

import eventlet
eventlet.monkey_patch()

from socketio import WSGIApp
from vidyahub.socket_server import sio

if __name__ == '__main__':
    port = 8001
    print(f'⚔️ VidyaHub Battle Server starting on port {port}')
    print('=' * 50)
    print('Battle Server Commands:')
    print('  - Join battle: emit "join_battle" with subject_id, user_id')
    print('  - Submit answer: emit "submit_answer" with room_id, answer')
    print('=' * 50)
    app = WSGIApp(sio)
    eventlet.wsgi.server(eventlet.listen(('', port)), app)