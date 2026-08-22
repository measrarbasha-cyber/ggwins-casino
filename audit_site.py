import os, re

scratch_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins"

# 1. Check all HTML and JS files for syntax or broken script tags
print("=== AUDITING FILES FOR ERRORS ===")
html_files = [f for f in os.listdir(scratch_dir) if f.endswith(".html")]
js_files = [f for f in os.listdir(scratch_dir) if f.endswith(".js")]

for hf in html_files:
    path = os.path.join(scratch_dir, hf)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    # Check for unclosed script tags
    open_scripts = len(re.findall(r'<script\b', content, re.I))
    close_scripts = len(re.findall(r'</script>', content, re.I))
    if open_scripts != close_scripts:
        print(f"ERROR in {hf}: script tag mismatch (open: {open_scripts}, close: {close_scripts})")
    
    # Check for suspicious ? characters in INR or badges
    bad_chars = re.findall(r'\?[0-9]+|\? [A-Z]', content)
    if bad_chars:
        print(f"Warning in {hf}: Possible mojibake: {bad_chars[:5]}")

print("=== HTML CHECKS COMPLETE ===")