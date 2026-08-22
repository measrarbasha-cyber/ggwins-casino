import os
from pathlib import Path
import json

workspace = Path(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins")

errors_found = 0

for root, dirs, files in os.walk(workspace):
    for fn in files:
        if fn.endswith('.html'):
            p = Path(root) / fn
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            if '' in content:
                print(f"Replacement char in {p.relative_to(workspace)}")
                errors_found += 1

print(f"Total HTML files checked. Remaining anomaly count: {errors_found}")
