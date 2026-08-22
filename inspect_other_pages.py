import os
from pathlib import Path

workspace = Path(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins")

for fn in ['terms.html', 'privacy-policy.html', 'promotions.html', 'refer.html']:
    p = workspace / fn
    if p.exists():
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
        for i, line in enumerate(lines, 1):
            if '\ufffd' in line or 'â€' in line or 'Ã' in line:
                print(f"{fn} Line {i}: {line.strip()[:100]}")
