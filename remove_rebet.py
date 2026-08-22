import os
import re

games_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\games"

for fname in os.listdir(games_dir):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(games_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Remove rebet-container divs
    content = re.sub(r'<!--\s*Rebet Controls\s*-->\s*<div class="rebet-row"[^>]*>[\s\S]*?</div>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<div class="rebet-row"[^>]*>[\s\S]*?</div>', '', content, flags=re.IGNORECASE)

    # 2. Remove 2x action buttons (e.g., <button class="btn-action-2x" ...>...</button>)
    content = re.sub(r'<button class="btn-action-2x"[^>]*>[\s\S]*?</button>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<button class="btn-overlay-action secondary"[^>]*onclick="modalRebetDouble\(\)"[^>]*>[\s\S]*?</button>', '', content, flags=re.IGNORECASE)
    content = re.sub(r'<button class="btn-overlay-action primary"[^>]*onclick="modalRebetSame\(\)"[^>]*>[\s\S]*?</button>', '', content, flags=re.IGNORECASE)

    # 3. Clean up modal / overlay modal buttons if they only had rebet
    # Replace Rebet in button text with Play / Bet
    content = re.sub(r'🔁 Rebet Same', '', content)
    content = re.sub(r'⚡ 2× Rebet', '', content)

    # 4. Remove JS functions: universalRebetSame, universalRebetDouble, rebetSame, rebetDouble, modalRebetSame, modalRebetDouble, playDouble
    content = re.sub(r'function universalRebetSame\([^)]*\)\s*\{[\s\S]*?\}', '', content)
    content = re.sub(r'function universalRebetDouble\([^)]*\)\s*\{[\s\S]*?\}', '', content)
    content = re.sub(r'function rebetSame\([^)]*\)\s*\{[\s\S]*?\}', '', content)
    content = re.sub(r'function rebetDouble\([^)]*\)\s*\{[\s\S]*?\}', '', content)
    content = re.sub(r'function modalRebetSame\([^)]*\)\s*\{[\s\S]*?\}', '', content)
    content = re.sub(r'function modalRebetDouble\([^)]*\)\s*\{[\s\S]*?\}', '', content)
    content = re.sub(r'function playDouble\([^)]*\)\s*\{[\s\S]*?\}', '', content)

    # Remove references to rebet-container in JS
    content = re.sub(r'document\.getElementById\([\'"]rebet-container[\'"]\)[^;]*;', '', content)
    content = re.sub(r'document\.getElementById\([\'"]rebet-amt-val[\'"]\)[^;]*;', '', content)
    content = re.sub(r'document\.getElementById\([\'"]btn-2x-[^\'"]*[\'"]\)[^;]*;', '', content)
    content = re.sub(r'let lastUniversalBetAmt\s*=\s*\d+;', '', content)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Cleaned rebet from {fname}")

