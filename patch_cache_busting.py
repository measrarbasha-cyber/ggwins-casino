import os, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html"

with open(scratch_path, "r", encoding="utf-8") as f:
    idx = f.read()

# Add cache busting version to css and js
idx = idx.replace('href="style.css"', 'href="style.css?v=3.0.1"')
idx = idx.replace('src="script.js"', 'src="script.js?v=3.0.1"')
idx = idx.replace('src="wallet.js"', 'src="wallet.js?v=3.0.1"')

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(idx)

shutil.copy2(scratch_path, brain_path)
print("SUCCESS: index.html updated with cache-busting asset tags!")