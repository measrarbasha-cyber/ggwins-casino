with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\help-centre.html", "r", encoding="utf-8", errors="replace") as f:
    lines = f.readlines()

for i, line in enumerate(lines, 1):
    if '\ufffd' in line or '' in line or 'â' in line or 'Ã' in line:
        print(f"Line {i}: {repr(line)}")
