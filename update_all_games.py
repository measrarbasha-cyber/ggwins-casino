import os
import re

games_dir = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\games"

# Games configuration: (filename, bet_input_id, action_function, target_regex_for_btn)
game_configs = {
    "blackjack.html": ("bet-amount", "deal()", r'(<button[^>]*id=["\']deal-btn["\'][^>]*>.*?</button>)'),
    "coinflip.html": ("bet-amount", "flipCoin()", r'(<button[^>]*id=["\']flip-btn["\'][^>]*>.*?</button>)'),
    "crash.html": ("bet-amount", "placeBet()", r'(<button[^>]*id=["\']bet-btn["\'][^>]*>.*?</button>)'),
    "dice.html": ("bet-amount", "roll()", r'(<button[^>]*id=["\']roll-btn["\'][^>]*>.*?</button>)'),
    "dragontower.html": ("bet-amount", "startTower()", r'(<button[^>]*id=["\']start-btn["\'][^>]*>.*?</button>)'),
    "hilo.html": ("bet-amount", "startGame()", r'(<button[^>]*id=["\']start-btn["\'][^>]*>.*?</button>)'),
    "keno.html": ("bet-amount", "playKeno()", r'(<button[^>]*id=["\']play-btn["\'][^>]*>.*?</button>)'),
    "limbo.html": ("bet-amount", "play()", r'(<button[^>]*id=["\']bet-btn["\'][^>]*>.*?</button>)'),
    "mines.html": ("bet-amount", "handleGameBtn()", r'(<button[^>]*id=["\']game-btn["\'][^>]*>.*?</button>)'),
    "plinko.html": ("bet-amount", "dropBall()", r'(<button[^>]*id=["\']drop-btn["\'][^>]*>.*?</button>)'),
    "roulette.html": ("bet-amount", "spinWheel()", r'(<button[^>]*id=["\']spin-btn["\'][^>]*>.*?</button>)'),
    "slots.html": ("bet-amount", "spin()", r'(<button[^>]*id=["\']spin-btn["\'][^>]*>.*?</button>)'),
    "wheel.html": ("bet-amount", "spinWheel()", r'(<button[^>]*id=["\']spin-btn["\'][^>]*>.*?</button>)'),
}

for fname in os.listdir(games_dir):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(games_dir, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add security-guard.js if not present
    if "security-guard.js" not in content:
        content = content.replace("</head>", '<script src="../security-guard.js"></script>\n</head>')

    # 2. Add copyright footer if not present
    if "copyright-footer" not in content:
        copyright_html = '\n<div class="copyright-footer">© 2026 GG Wins. Proprietary Algorithm & Code Protected. Unauthorized Copying Prohibited.</div>\n'
        if "</div>\n\n  <div class=\"bet-panel\">" in content:
            content = content.replace("</div>\n\n  <div class=\"bet-panel\">", copyright_html + "</div>\n\n  <div class=\"bet-panel\">")
        elif "</div>\n  <div class=\"bet-panel\">" in content:
            content = content.replace("</div>\n  <div class=\"bet-panel\">", copyright_html + "</div>\n  <div class=\"bet-panel\">")

    # 3. Add Rebet controls for configured games if not already containing rebet-container
    if fname in game_configs and "rebet-container" not in content:
        input_id, action_fn, btn_pattern = game_configs[fname]
        rebet_html = f'''
      <!-- Rebet Controls -->
      <div class="rebet-row" id="rebet-container" style="margin-top:8px">
        <button class="btn-rebet" type="button" onclick="universalRebetSame('{input_id}', {action_fn.replace('()','')})">🔁 Rebet</button>
        <button class="btn-rebet" type="button" onclick="universalRebetDouble('{input_id}', {action_fn.replace('()','')})">⚡ 2× Rebet</button>
      </div>'''
        
        # Insert after the main button
        match = re.search(btn_pattern, content)
        if match:
            orig_btn = match.group(0)
            content = content.replace(orig_btn, orig_btn + rebet_html, 1)

        # Inject universal rebet helper functions if not present
        if "universalRebetSame" not in content:
            helper_js = f'''
<script>
let lastUniversalBetAmt = 100;
function universalRebetSame(inputId, actionFn) {{
  const el = document.getElementById(inputId);
  if(el) {{
    const current = parseFloat(el.value) || 100;
    lastUniversalBetAmt = current;
    el.value = lastUniversalBetAmt.toFixed(2);
  }}
  if(typeof actionFn === 'function') actionFn();
}}
function universalRebetDouble(inputId, actionFn) {{
  const el = document.getElementById(inputId);
  if(el) {{
    const current = parseFloat(el.value) || 100;
    lastUniversalBetAmt = current * 2;
    el.value = lastUniversalBetAmt.toFixed(2);
  }}
  if(typeof actionFn === 'function') actionFn();
}}
</script>
'''
            content = content.replace("</body>", helper_js + "\n</body>")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {fname} successfully.")

# Also add security guard and copyright to index.html
index_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    idx_content = f.read()

if "security-guard.js" not in idx_content:
    idx_content = idx_content.replace("</head>", '<script src="security-guard.js"></script>\n</head>')

with open(index_path, "w", encoding="utf-8") as f:
    f.write(idx_content)
print("Updated index.html with security guard.")
