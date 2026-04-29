"""
VidyaHub Global Orchestrator
Uses Cloudflare Tunnel (cloudflared) for a free, public HTTPS URL
with NO password page - anyone in the world can access your site!
"""
import subprocess
import re
import os
import time
import sys
import threading

def start_global():
    print("\n" + "="*60)
    print("  VIDYAHUB GLOBAL ORCHESTRATOR")
    print("  Powered by Cloudflare Tunnel (Free, No Password!)")
    print("="*60 + "\n")

    # 1. Check cloudflared is installed
    # Try full install path first (common after winget install on Windows)
    CF_PATHS = [
        r"C:\Program Files (x86)\cloudflared\cloudflared.exe",
        r"C:\Program Files\cloudflared\cloudflared.exe",
        "cloudflared",  # fall back to PATH
    ]
    cf_cmd = None
    for p in CF_PATHS:
        try:
            subprocess.check_output([p, '--version'], stderr=subprocess.STDOUT)
            cf_cmd = p
            break
        except (FileNotFoundError, subprocess.CalledProcessError, OSError):
            continue

    if cf_cmd is None:
        print("!! cloudflared not found. Installing via winget...")
        try:
            subprocess.run(
                'winget install --id Cloudflare.cloudflared -e --silent '
                '--accept-source-agreements --accept-package-agreements',
                shell=True, check=True
            )
            print("OK cloudflared installed! Please restart this script.\n")
        except subprocess.CalledProcessError:
            print("❌ Auto-install failed.")
            print("   Download from:")
            print("   https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/")
        sys.exit(1)
    print(f"OK cloudflared found at: {cf_cmd}\n")

    # 2. Start Cloudflare Tunnel
    print(">> Starting Cloudflare Tunnel on port 8000...")
    tunnel = subprocess.Popen(
        [cf_cmd, 'tunnel', '--url', 'http://localhost:8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    # 3. Wait for URL
    url = ""
    print(".. Waiting for public URL (10-20 seconds)...\n")
    start_time = time.time()
    while time.time() - start_time < 40:
        line = tunnel.stdout.readline()
        if not line:
            break
        line = line.strip()
        # cloudflared prints the URL in stderr/stdout like:
        # "https://xxxx.trycloudflare.com"
        match = re.search(r'https://[a-z0-9\-]+\.trycloudflare\.com', line)
        if match:
            url = match.group(0)
            break
        # Show progress dots
        if 'INF' in line or 'connected' in line.lower():
            print(f"  {line}")

    if not url:
        print("\n!! Could not get tunnel URL automatically.")
        print("   The tunnel is still running - check the output above for your URL.")
        try:
            subprocess.run(['python', 'run_combined.py'], check=True)
        except KeyboardInterrupt:
            pass
        finally:
            tunnel.terminate()
        return

    # 4. Update .env for Socket.io
    try:
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
        with open(env_path, 'r') as f:
            content = f.read()
        if 'SOCKETIO_SERVER_URL=' in content:
            content = re.sub(r'SOCKETIO_SERVER_URL=.*', f'SOCKETIO_SERVER_URL={url}', content)
        else:
            content += f'\nSOCKETIO_SERVER_URL={url}\n'
        with open(env_path, 'w') as f:
            f.write(content)
        print(f"OK .env auto-configured for global Socket.io")
    except Exception as e:
        print(f"!! Could not update .env: {e}")

    # 5. Print the URL loud and clear
    print("\n" + "="*60)
    print("  >> YOUR GLOBAL LIVE URL:")
    print(f"\n       {url}\n")
    print("  >> Share this with ANYONE in the world!")
    print("  OK No password needed")
    print("  >> Secure HTTPS connection")
    print("="*60)
    print("\n  Keep this window open to stay live!")
    print("  Press Ctrl+C to stop the server.\n")

    # 6. Start VidyaHub server (keeps script alive)
    try:
        subprocess.run(['python', 'run_combined.py'], check=True)
    except KeyboardInterrupt:
        print("\n!! Shutting down...")
    finally:
        tunnel.terminate()
        print("OK Tunnel closed. Goodbye!")

if __name__ == "__main__":
    start_global()
