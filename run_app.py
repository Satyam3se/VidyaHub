import os
import sys

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

import django
import eventlet
import eventlet.wsgi

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from vidyahub.wsgi import application

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    
    print("\n" + "="*50)
    print("   SUCCESS: VIDYAHUB IS NOW LIVE!")
    print("="*50)
    print("LOCAL NETWORK:  http://172.16.102.168:8000")
    print("HOME COMPUTER:  http://127.0.0.1:8000")
    print("="*50)
    print("\n[INFO] Keep this window OPEN to stay live.")
    print("[INFO] Press Ctrl+C only when you want to stop the server.\n")
    
    # Run the eventlet server
    eventlet.wsgi.server(eventlet.listen(('', 8000)), application)