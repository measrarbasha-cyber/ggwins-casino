for path in [r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html", r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html"]:
    with open(path, "r", encoding="utf-8") as f:
        c = f.read()
    import re
    # Remove hero-section / hero-carousel
    c = re.sub(r'<section class="hero-section".*?</section>', '', c, flags=re.DOTALL)
    c = re.sub(r'<div class="hero-carousel".*?</div>\s*</div>\s*</div>', '', c, flags=re.DOTALL)
    with open(path, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Path {path}: len={len(c)}, hero-carousel in c = {'hero-carousel' in c}")