srv_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\server.py"
with open(srv_path, "r", encoding="utf-8") as f:
    s = f.read()

# Add end_headers override with no-cache headers in GGWinsHandler
no_cache_patch = """class GGWinsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()"""

target = """class GGWinsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=STATIC_DIR, **kwargs)"""

if target in s:
    s = s.replace(target, no_cache_patch)
    with open(srv_path, "w", encoding="utf-8") as f:
        f.write(s)
    print("SUCCESS: Added universal anti-cache headers to server.py!")