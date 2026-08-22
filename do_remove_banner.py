import os, re, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html"

with open(scratch_path, "r", encoding="utf-8") as f:
    idx = f.read()

start = idx.find('<section class="hero-carousel"')
if start != -1:
    end = idx.find('</section>', start) + 10
    print(f"Found banner at {start}:{end}, removing it...")
    idx = idx[:start] + idx[end:]

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(idx)

shutil.copy2(scratch_path, brain_path)
print(f"New length: {len(idx)}")