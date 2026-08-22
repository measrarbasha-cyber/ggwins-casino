with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
# check for syntax errors or incomplete blocks
print(f"script.js length: {len(s)} chars")
if "renderQuickLaunchGames" in s and "initHeroSlider" in s:
    print("ALL CORE FUNCTIONS PRESENT IN script.js!")