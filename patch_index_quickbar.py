with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Quick Play Game Bar CSS & HTML
quick_bar_css = """
/* ── TOP QUICK PLAY GAME ICONS STRIP ── */
.lobby-quick-games-bar {
  background: rgba(15, 21, 39, 0.85);
  border: 1px solid rgba(255, 215, 0, 0.25);
  border-radius: 16px;
  padding: 12px 14px;
  margin: 16px 0 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
}
.quick-bar-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
  padding: 0 4px;
}
.quick-bar-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 12.5px;
  font-weight: 800;
  color: #ffd700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: flex;
  align-items: center;
  gap: 6px;
}
.quick-games-scroll {
  display: flex;
  gap: 10px;
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 6px;
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: thin;
  scrollbar-color: #ffd700 rgba(255,255,255,0.06);
}
.quick-games-scroll::-webkit-scrollbar { height: 4px; }
.quick-games-scroll::-webkit-scrollbar-thumb { background: #ffd700; border-radius: 999px; }

.quick-game-item {
  flex: 0 0 auto;
  background: #111827;
  border: 1.5px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
  text-decoration: none;
  color: #f8fafc;
}
.quick-game-item:hover {
  transform: translateY(-2px);
  border-color: #ffd700;
  background: #1e293b;
  box-shadow: 0 4px 16px rgba(255, 215, 0, 0.35);
}
.quick-item-icon { font-size: 22px; line-height: 1; }
.quick-item-name { font-family: 'Space Grotesk', sans-serif; font-size: 11.5px; font-weight: 800; white-space: nowrap; }
"""

quick_bar_html = """        <!-- ── QUICK-PLAY GAME ICONS STRIP ── -->
        <div class="lobby-quick-games-bar">
          <div class="quick-bar-header">
            <div class="quick-bar-title">
              <span>🎮</span> Instant Play Games (Click Any Game Icon to Launch)
            </div>
            <a href="tournaments.html" style="font-size:11.5px;color:#00e676;font-weight:800;text-decoration:none">
              🏆 Tournaments Arena →
            </a>
          </div>
          <div class="quick-games-scroll">
            <a href="games/crash.html" class="quick-game-item"><span class="quick-item-icon">🚀</span><span class="quick-item-name">Crash</span></a>
            <a href="games/mines.html" class="quick-game-item"><span class="quick-item-icon">💣</span><span class="quick-item-name">Mines</span></a>
            <a href="games/coinflip.html" class="quick-game-item"><span class="quick-item-icon">🪙</span><span class="quick-item-name">Coin Flip</span></a>
            <a href="games/sicbo.html" class="quick-game-item"><span class="quick-item-icon">🎲</span><span class="quick-item-name">Sic Bo</span></a>
            <a href="games/penalty.html" class="quick-game-item"><span class="quick-item-icon">⚽</span><span class="quick-item-name">Penalty</span></a>
            <a href="games/cups.html" class="quick-game-item"><span class="quick-item-icon">🪄</span><span class="quick-item-name">Magic Shells</span></a>
            <a href="games/rummy.html" class="quick-game-item"><span class="quick-item-icon">🃏</span><span class="quick-item-name">Indian Rummy</span></a>
            <a href="games/baccarat.html" class="quick-game-item"><span class="quick-item-icon">👑</span><span class="quick-item-name">Baccarat 3D</span></a>
            <a href="games/roulette.html" class="quick-game-item"><span class="quick-item-icon">🔴</span><span class="quick-item-name">Roulette</span></a>
            <a href="games/blackjack.html" class="quick-game-item"><span class="quick-item-icon">♣️</span><span class="quick-item-name">Blackjack 21</span></a>
            <a href="games/dice.html" class="quick-game-item"><span class="quick-item-icon">🎲</span><span class="quick-item-name">Dice 3D</span></a>
            <a href="games/dragontower.html" class="quick-game-item"><span class="quick-item-icon">🐉</span><span class="quick-item-name">Dragon Tower</span></a>
            <a href="games/ludo.html" class="quick-game-item"><span class="quick-item-icon">🎲</span><span class="quick-item-name">Ludo 3D</span></a>
            <a href="games/diamonds.html" class="quick-game-item"><span class="quick-item-icon">💎</span><span class="quick-item-name">Diamonds</span></a>
            <a href="games/hilo.html" class="quick-game-item"><span class="quick-item-icon">🃏</span><span class="quick-item-name">Hilo Master</span></a>
            <a href="games/limbo.html" class="quick-game-item"><span class="quick-item-icon">📈</span><span class="quick-item-name">Limbo</span></a>
            <a href="games/wheel.html" class="quick-game-item"><span class="quick-item-icon">🎡</span><span class="quick-item-name">Wheel</span></a>
            <a href="games/keno.html" class="quick-game-item"><span class="quick-item-icon">🎱</span><span class="quick-item-name">Keno</span></a>
            <a href="games/slots.html" class="quick-game-item"><span class="quick-item-icon">🎰</span><span class="quick-item-name">Slots 777</span></a>
            <a href="games/plinko.html" class="quick-game-item"><span class="quick-item-icon">⚽</span><span class="quick-item-name">Plinko</span></a>
          </div>
        </div>"""

if ".lobby-quick-games-bar" not in idx:
    idx = idx.replace("</head>", "<style>\n" + quick_bar_css + "\n</style>\n</head>")

if "class=\"lobby-quick-games-bar\"" not in idx:
    # Insert right below carousel section
    idx = idx.replace("</section>\n\n        <!-- STATS BAR -->", "</section>\n\n" + quick_bar_html + "\n\n        <!-- STATS BAR -->")

# Clean up sidebar navigation items
sidebar_clean = """      <nav class="sidebar-nav" aria-label="Main navigation">
        <!-- Casino Section -->
        <div class="nav-section">
          <span class="nav-section-label">Casino</span>
          <a href="index.html" class="nav-item active" id="nav-lobby">
            <span class="nav-icon">🏠</span>
            <span class="nav-label">Lobby</span>
          </a>
          <a href="tournaments.html" class="nav-item" id="nav-tournaments" style="background:linear-gradient(135deg,rgba(255,215,0,0.18),rgba(0,230,118,0.12));border:1px solid rgba(255,215,0,0.35);box-shadow:0 0 12px rgba(255,215,0,0.15)">
            <span class="nav-icon" style="color:#ffd700">🏆</span>
            <span class="nav-label" style="color:#ffd700;font-weight:900">Tournaments</span>
            <span class="nav-badge" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000;font-weight:900">₹50 ENTRY</span>
          </a>
          <a href="vip.html" class="nav-item" id="nav-vip" style="background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.2)">
            <span class="nav-icon" style="color:#ffd700">👑</span>
            <span class="nav-label" style="color:#ffd700;font-weight:800">VIP Club</span>
            <span class="nav-badge vip-badge">VIP</span>
          </a>
          <a href="vip-lounge.html" class="nav-item" id="nav-vip-lounge">
            <span class="nav-icon">💬</span>
            <span class="nav-label">VIP Lounge</span>
            <span class="nav-badge" style="background:#ffd700;color:#000;font-weight:900">ROOM</span>
          </a>
        </div>

        <!-- Direct Play Games Menu -->
        <div class="nav-section">
          <span class="nav-section-label">Popular Games</span>
          <a href="games/crash.html" class="nav-item"><span class="nav-icon">🚀</span><span class="nav-label">GG Crash</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/mines.html" class="nav-item"><span class="nav-icon">💣</span><span class="nav-label">GG Mines</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/coinflip.html" class="nav-item"><span class="nav-icon">🪙</span><span class="nav-label">Coin Flip 3D</span></a>
          <a href="games/sicbo.html" class="nav-item"><span class="nav-icon">🎲</span><span class="nav-label">Sic Bo 3-Dice</span></a>
          <a href="games/penalty.html" class="nav-item"><span class="nav-icon">⚽</span><span class="nav-label">Penalty Shoot</span></a>
          <a href="games/cups.html" class="nav-item"><span class="nav-icon">🪄</span><span class="nav-label">Magic Shells</span></a>
          <a href="games/rummy.html" class="nav-item"><span class="nav-icon">🃏</span><span class="nav-label">Indian Rummy</span><span class="nav-badge" style="background:#00e676;color:#000">3D</span></a>
          <a href="games/baccarat.html" class="nav-item"><span class="nav-icon">👑</span><span class="nav-label">Royale Baccarat</span></a>
          <a href="games/roulette.html" class="nav-item"><span class="nav-icon">🔴</span><span class="nav-label">Roulette 3D</span></a>
          <a href="games/blackjack.html" class="nav-item"><span class="nav-icon">♣️</span><span class="nav-label">Blackjack 21</span></a>
          <a href="games/dragontower.html" class="nav-item"><span class="nav-icon">🐉</span><span class="nav-label">Dragon Tower</span></a>
          <a href="games/ludo.html" class="nav-item"><span class="nav-icon">🎲</span><span class="nav-label">Ludo Champions</span></a>
          <a href="games/slots.html" class="nav-item"><span class="nav-icon">🎰</span><span class="nav-label">Slots 777</span></a>
          <a href="games/limbo.html" class="nav-item"><span class="nav-icon">📈</span><span class="nav-label">Limbo Rocket</span></a>
          <a href="games/plinko.html" class="nav-item"><span class="nav-icon">⚽</span><span class="nav-label">Plinko Drop</span></a>
        </div>

        <!-- Banking & Support -->
        <div class="nav-section">
          <span class="nav-section-label">Account &amp; Banking</span>
          <a href="#" class="nav-item" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit'); return false;">
            <span class="nav-icon" style="color:var(--green)">💳</span>
            <span class="nav-label" style="font-weight:700">Deposit &amp; Wallet</span>
          </a>
          <a href="#" class="nav-item" onclick="if(typeof openWalletModal==='function') openWalletModal('payment-history'); return false;">
            <span class="nav-icon">📜</span>
            <span class="nav-label">Payment History</span>
          </a>
          <a href="help-centre.html" class="nav-item">
            <span class="nav-icon">❓</span>
            <span class="nav-label">Help Centre &amp; Support</span>
          </a>
        </div>
      </nav>"""

import re
idx = re.sub(r'<nav class="sidebar-nav".*?</nav>', sidebar_clean, idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html updated with Quick-Play Game Icons bar and full clickable navigation icons!")