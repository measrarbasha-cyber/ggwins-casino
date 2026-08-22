import os, re
from pathlib import Path

workspace = Path(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins")

def check_file(p):
    try:
        with open(p, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return

    anomalies = []
    if '\ufffd' in content:
        anomalies.append('REPLACEMENT_CHAR')
    if '' in content:
        anomalies.append('QUESTION_MARK_DIAMOND')
    if 'â€' in content:
        anomalies.append('MOJIBAKE_DASH_QUOTE')
    if 'Ã' in content:
        anomalies.append('MOJIBAKE_UTF8')

    if anomalies:
        print(f"{p.name}: {', '.join(anomalies)}")

for root, dirs, files in os.walk(workspace):
    for fn in files:
        if fn.endswith(('.html', '.js', '.css', '.json')):
            check_file(Path(root) / fn)
