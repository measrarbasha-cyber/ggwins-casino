import os, shutil

scratch_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins"
brain_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06"
srv_path = os.path.join(brain_dir, "server.py")

with open(srv_path, "r", encoding="utf-8") as f:
    srv = f.read()

target = "class GGWinsHandler(http.server.SimpleHTTPRequestHandler):"
replacement = """STATIC_DIR = r"C:\\Users\\ASRAR BASHA\\.gemini\\antigravity\\scratch\\ggwins"

class GGWinsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)"""

if target in srv and "STATIC_DIR" not in srv:
    srv = srv.replace(target, replacement)
    with open(srv_path, "w", encoding="utf-8") as f:
        f.write(srv)
    print("SUCCESS: server.py updated with STATIC_DIR!")

# Copy key files to brain_dir as well
for fname in ['index.html', 'script.js', 'style.css', 'vip.html', 'vip-lounge.html']:
    src = os.path.join(scratch_dir, fname)
    dst = os.path.join(brain_dir, fname)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"Synced {fname} to brain dir.")