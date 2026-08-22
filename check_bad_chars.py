import os
from pathlib import Path

workspace = Path(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins")

for fn in ['help-centre.html', 'index.html', 'tournaments.html']:
    p = workspace / fn
    with open(p, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
    
    bad_chars = set()
    for char in content:
        code = ord(char)
        if code == 0xFFFD or (0x80 <= code <= 0x9F):
            bad_chars.add(f"U+{code:04X}")
            
    print(f"{fn}: bad characters = {bad_chars}")
