with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

print("--- SLIDER SLIDES IN INDEX.HTML ---")
import re
slides = re.findall(r'<div class="slide[^"]*".*?</div>\s*</div>', idx, re.DOTALL)
for i, s in enumerate(slides):
    print(f"Slide {i+1}:")
    print(s[:300])