import os
from pathlib import Path

workspace = Path(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins")

for root, dirs, files in os.walk(workspace):
    for fn in files:
        if fn.endswith(('.html', '.js')):
            p = Path(root) / fn
            with open(p, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            cleaned = content
            # Clean common corrupt mojibake sequences
            cleaned = cleaned.replace('\ufffd', '')
            cleaned = cleaned.replace('â€“', '–')
            cleaned = cleaned.replace('â€”', '—')
            cleaned = cleaned.replace('â€œ', '"')
            cleaned = cleaned.replace('â€', '"')
            cleaned = cleaned.replace('â€˜', "'")
            cleaned = cleaned.replace('â€™', "'")
            cleaned = cleaned.replace('â†', '←')
            cleaned = cleaned.replace('âœ•', '✕')
            cleaned = cleaned.replace('â€¦', '...')
            
            if cleaned != content:
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(cleaned)
                print(f"Fixed mojibake/replacements in {p.name}")

print("COMPLETED: All files scanned and cleaned!")
