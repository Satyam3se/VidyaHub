import subprocess
import re
import os
import time
import sys

def start_global():
    # Fix Windows console encoding for emojis
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    print("\n" + "="*50)
    print("VIDYAHUB GLOBAL ORCHESTRATOR")
    print("="*50 + "\n")

    # 1. Get Public IP (Needed for Localtunnel's 'Friendly Reminder' page)
    try:
        ip = subprocess.check_output(['curl', '-s', 'ifconfig.me'], timeout=10).decode().strip()
        print(f"TUNNEL PASSWORD: {ip}")
        print("(Note: If the website asks for a password, enter the IP above)\n")
    except Exception:
        print("⚠️ Could not fetch public IP automatically.")

    # 2. Start Tunnel
    print("Establishing Secure Tunnel via Localtunnel...")
    # Use shell=True for npx on Windows
    tunnel = subprocess.Popen('npx localtunnel --port 8000', 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.STDOUT, 
                            text=True, 
                            shell=True)

    # 3. Wait for URL to be generated
    url = ""
    start_time = time.time()
    while time.time() - start_time < 30: # 30 second timeout
        line = tunnel.stdout.readline()
        if not line:
            break
        print(line.strip())
        if "your url is:" in line:
            url = line.split("your url is:")[1].strip()
            break
        
    if not url:
        print("\n❌ FAILED: Localtunnel did not provide a URL.")
        tunnel.terminate()
        return

    print(f"\nGLOBAL LIVE URL: {url}")

    # 4. Update .env for Global Socket.io
    try:
        with open('.env', 'r') as f:
            content = f.read()
        
        # Replace local URL with Global URL
        if 'SOCKETIO_SERVER_URL=' in content:
            content = re.sub(r'SOCKETIO_SERVER_URL=.*', f'SOCKETIO_SERVER_URL={url}', content)
        else:
            content += f'\nSOCKETIO_SERVER_URL={url}\n'
            
        with open('.env', 'w') as f:
            f.write(content)
        print("✅ .env Auto-configured for Global Socket.io Sync")
    except Exception as e:
        print(f"⚠️ Warning: Could not update .env automatically: {e}")

    # 5. Start the main app server
    print("\nLAUNCHING VIDYAHUB PRODUCTION SERVER...")
    print("Keep this window open to stay live!\n")
    
    try:
        # Start the Django/Socket.io server
        # We use subprocess.run so it keeps the script alive
        subprocess.run(['python', 'run_app.py'], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Global Server...")
    finally:
        tunnel.terminate()

if __name__ == "__main__":
    start_global()
