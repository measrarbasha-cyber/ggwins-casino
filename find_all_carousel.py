path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
with open(path, "r", encoding="utf-8") as f:
    c = f.read()

import re
matches = [m.start() for m in re.finditer(r'hero-carousel', c)]
for m in matches:
    print(c[m-30:m+100])
    print("="*40)