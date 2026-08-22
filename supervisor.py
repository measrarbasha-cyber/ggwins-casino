import os
import sys
import time
import subprocess
import threading
import urllib.request
import urllib.error
import ctypes
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable
CLOUDFLARED_EXE = BASE_DIR / "cloudflared.exe"
SERVER_SCRIPT = BASE_DIR / "server.py"

TUNNEL_TOKEN = "eyJhIjoiNWJiYTM4NDUyYWMxOGRlOWFhOGMzZjA5YTE5ZTE1Y2MiLCJ0IjoiZjQyMGViNzItYjAwNi00NmExLTk0MjEtZjE3Yzk3MWM3ZDQ5IiwicyI6Ik9URXhZbUV4WkdRdE5tRmxOUzAwTWpRNExXRmlZalV0Tldaak5EVTRNemszT0dKaSJ9"

# Windows API constants to prevent sleep and network throttling
ES_CONTINUOUS = 0x80000000
ES_SYSTEM_REQUIRED = 0x00000001
ES_AWAYMODE_REQUIRED = 0x00000040

def prevent_windows_sleep():
    """Prevents Windows from entering sleep mode or throttling network 24/7."""
    try:
        if os.name == 'nt':
            ctypes.windll.kernel32.SetThreadExecutionState(
                ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_AWAYMODE_REQUIRED
            )
    except Exception:
        pass

class ProcessSupervisor:
    def __init__(self):
        self.server_proc = None
        self.tunnel_proc = None
        self.running = True
        self.lock = threading.Lock()

    def start_server(self):
        with self.lock:
            if self.server_proc and self.server_proc.poll() is None:
                return
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] Starting Python Web Server (server.py)...")
            sys.stdout.flush()
            self.server_proc = subprocess.Popen(
                [PYTHON_EXE, str(SERVER_SCRIPT)],
                cwd=str(BASE_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1
            )
            threading.Thread(target=self._stream_logs, args=(self.server_proc, "SERVER"), daemon=True).start()

    def start_tunnel(self):
        with self.lock:
            if self.tunnel_proc and self.tunnel_proc.poll() is None:
                return
            print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] Starting Cloudflare Edge Tunnel (ggwins.site)...")
            sys.stdout.flush()
            self.tunnel_proc = subprocess.Popen(
                [str(CLOUDFLARED_EXE), "tunnel", "run", "--token", TUNNEL_TOKEN],
                cwd=str(BASE_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1
            )
            threading.Thread(target=self._stream_logs, args=(self.tunnel_proc, "TUNNEL"), daemon=True).start()

    def _stream_logs(self, proc, prefix):
        try:
            for line in iter(proc.stdout.readline, ''):
                if not line:
                    break
                line_str = line.strip()
                if line_str and not line_str.startswith("[DEBUG"):
                    if any(k in line_str for k in ["Registered", "INF", "ERR", "SERVER", "ONLINE", "healthy", "Starting"]):
                        print(f"[{prefix}] {line_str}")
                        sys.stdout.flush()
        except Exception:
            pass

    def restart_server(self):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] [!] Health probe timeout. Auto-restarting server...")
        sys.stdout.flush()
        with self.lock:
            if self.server_proc:
                try:
                    self.server_proc.terminate()
                    self.server_proc.wait(timeout=3)
                except Exception:
                    try:
                        self.server_proc.kill()
                    except Exception:
                        pass
                self.server_proc = None
        time.sleep(0.5)
        self.start_server()

    def restart_tunnel(self):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] [!] Tunnel disconnected. Reconnecting Cloudflare...")
        sys.stdout.flush()
        with self.lock:
            if self.tunnel_proc:
                try:
                    self.tunnel_proc.terminate()
                    self.tunnel_proc.wait(timeout=3)
                except Exception:
                    try:
                        self.tunnel_proc.kill()
                    except Exception:
                        pass
                self.tunnel_proc = None
        time.sleep(1)
        self.start_tunnel()

    def check_health(self):
        """Performs HTTP health check on local port 8000."""
        try:
            req = urllib.request.Request("http://127.0.0.1:8000/api/health", headers={"User-Agent": "GGWins-Watchdog/2.0"})
            with urllib.request.urlopen(req, timeout=4) as response:
                return response.status == 200
        except Exception:
            return False

    def run(self):
        prevent_windows_sleep()
        self.start_server()
        time.sleep(1)
        self.start_tunnel()

        print("\n" + "="*60)
        print("  [GUARDIAN] GG WINS 24/7 CRASH-PROOF SUPERVISOR RUNNING")
        print("  [GUARDIAN] Monitoring: Python Server & Cloudflare Tunnel")
        print("  [GUARDIAN] Windows 24/7 Sleep Prevention: ACTIVE")
        print("  [GUARDIAN] Live URL: https://ggwins.site")
        print("="*60 + "\n")
        sys.stdout.flush()

        consecutive_failures = 0
        loop_counter = 0

        while self.running:
            try:
                # Re-assert Windows stay-awake state every 60s
                if loop_counter % 12 == 0:
                    prevent_windows_sleep()

                # 1. Process liveness check
                if not self.server_proc or self.server_proc.poll() is not None:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] Server died. Instantly recovering...")
                    sys.stdout.flush()
                    self.start_server()

                if not self.tunnel_proc or self.tunnel_proc.poll() is not None:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] Tunnel died. Instantly recovering...")
                    sys.stdout.flush()
                    self.start_tunnel()

                # 2. HTTP Health Probe
                if not self.check_health():
                    consecutive_failures += 1
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] Health probe failed ({consecutive_failures}/3)...")
                    sys.stdout.flush()
                    if consecutive_failures >= 3:
                        self.restart_server()
                        consecutive_failures = 0
                else:
                    if consecutive_failures > 0:
                        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SUPERVISOR] [OK] Health check restored.")
                        sys.stdout.flush()
                    consecutive_failures = 0

                loop_counter += 1
                time.sleep(5)

            except KeyboardInterrupt:
                print("\n[SUPERVISOR] Shutting down...")
                break
            except Exception as e:
                print(f"[SUPERVISOR] Watchdog error: {e}")
                sys.stdout.flush()
                time.sleep(5)

        if self.server_proc: self.server_proc.kill()
        if self.tunnel_proc: self.tunnel_proc.kill()

if __name__ == "__main__":
    supervisor = ProcessSupervisor()
    supervisor.run()
