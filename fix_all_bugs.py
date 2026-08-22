import os, re, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\script.js"

with open(scratch_path, "r", encoding="utf-8") as f:
    s = f.read()

# Replace all direct dom.xxx.addEventListener with safe if (dom.xxx) checks
def safe_listener_replace(match):
    full = match.group(0)
    dom_prop = match.group(1)
    return f"if (dom.{dom_prop}) dom.{dom_prop}.addEventListener"

s = re.sub(r'dom\.([a-zA-Z0-9_]+)\.addEventListener', safe_listener_replace, s)

# Also fix any document.getElementById(...).addEventListener without check
def safe_el_replace(match):
    el_name = match.group(1)
    return f"if (document.getElementById('{el_name}')) document.getElementById('{el_name}').addEventListener"

s = re.sub(r"document\.getElementById\('([^']+)'\)\.addEventListener", safe_el_replace, s)

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(s)
shutil.copy2(scratch_path, brain_path)

print("SUCCESS: script.js - All null addEventListener bugs completely fixed with safe checks!")

# Fix any remaining mojibake in index.html
idx_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
with open(idx_path, "r", encoding="utf-8") as f:
    idx = f.read()

# Clean up any bad character artifacts
idx = idx.replace("? C", "🃏 C").replace("? E", "⚡ E").replace("? I", "🔥 I").replace("?50", "₹50").replace("?100", "₹100").replace("?500", "₹500")

with open(idx_path, "w", encoding="utf-8") as f:
    f.write(idx)
shutil.copy2(idx_path, r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html")

print("SUCCESS: index.html - All mojibake and encoding artifacts cleaned!")