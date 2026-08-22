import re

files_to_clean = [
    r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\games\diamonds.html",
    r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\games\penalty.html",
    r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\games\rummy.html",
    r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\games\baccarat.html"
]

for fpath in files_to_clean:
    with open(fpath, "r", encoding="utf-8") as f:
        c = f.read()

    # Remove residual rebet CSS & elements
    c = re.sub(r'/\* Rebet Controls \*/[\s\S]*?\.btn-rebet:hover\s*\{[^}]*\}', '', c)
    c = re.sub(r'document\.getElementById\([\'"]modal-rebet-amt[\'"]\)[^;]*;', '', c)
    c = re.sub(r'document\.getElementById\([\'"]modal-rebet-2x[\'"]\)[^;]*;', '', c)
    c = re.sub(r'document\.getElementById\([\'"]rebet-amt-val[\'"]\)[^;]*;', '', c)
    c = re.sub(r'or <strong>Rebet</strong>', '', c)
    c = re.sub(r'<button[^>]*onclick="modalRebet[^"]*"[^>]*>.*?</button>', '', c)
    c = re.sub(r'<span id="rebet-amt-val">\d+</span>', '', c)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(c)

print("Finished deep cleaning rebet.")
