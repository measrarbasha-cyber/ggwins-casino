import os, re, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html"

with open(scratch_path, "r", encoding="utf-8") as f:
    idx = f.read()

# Remove the hero-carousel section
idx = re.sub(r'<!-- ── HERO PROMO CAROUSEL.*?<!-- ── FULL PAGE QUICK LAUNCH GAMES ARENA ── -->', '<!-- ── FULL PAGE QUICK LAUNCH GAMES ARENA ── -->', idx, flags=re.DOTALL)
idx = re.sub(r'<section class="hero-carousel".*?</section>', '', idx, flags=re.DOTALL)

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(idx)

# Sync to brain directory as well
shutil.copy2(scratch_path, brain_path)

print("SUCCESS: Hero banner completely removed from index.html in both locations!")