with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Restore previous clean sidebar navigation with dedicated "All Games" tab
restored_sidebar = """      <nav class="sidebar-nav" aria-label="Main navigation">
        <!-- Casino Section -->
        <div class="nav-section">
          <span class="nav-section-label">Casino</span>
          <a href="games.html" class="nav-item" id="nav-all-games" style="background:linear-gradient(135deg,rgba(0,230,118,0.18),rgba(0,176,255,0.12));border:1.5px solid #00e676;box-shadow:0 0 14px rgba(0,230,118,0.25)">
            <span class="nav-icon" style="color:#00e676;font-size:18px">🎮</span>
            <span class="nav-label" style="color:#00e676;font-weight:900">All Games</span>
            <span class="nav-badge" style="background:#00e676;color:#000;font-weight:900">20 GAMES</span>
          </a>
          <a href="tournaments.html" class="nav-item" id="nav-tournaments" style="background:linear-gradient(135deg,rgba(255,215,0,0.18),rgba(0,230,118,0.12));border:1px solid rgba(255,215,0,0.35);box-shadow:0 0 12px rgba(255,215,0,0.15)">
            <span class="nav-icon" style="color:#ffd700;font-size:18px">🏆</span>
            <span class="nav-label" style="color:#ffd700;font-weight:900">Tournaments</span>
            <span class="nav-badge" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000;font-weight:900">₹50 ENTRY</span>
          </a>
          <a href="vip.html" class="nav-item" id="nav-vip" style="background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.2)">
            <span class="nav-icon" style="color:#ffd700;font-size:18px">👑</span>
            <span class="nav-label" style="color:#ffd700;font-weight:800">VIP Club</span>
            <span class="nav-badge vip-badge">VIP</span>
          </a>
          <a href="vip-lounge.html" class="nav-item" id="nav-vip-lounge">
            <span class="nav-icon" style="font-size:18px">💬</span>
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
idx = re.sub(r'<nav class="sidebar-nav".*?</nav>', restored_sidebar, idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

# Restore games.html original title and heading
with open("games.html", "r", encoding="utf-8") as f:
    g = f.read()

g = g.replace("🏠 Game Lobby – GG Wins Casino", "🎮 All Games – GG Wins Casino")
g = g.replace("GG Wins <span style=\"color:#00e676\">Game Lobby</span>", "GG Wins <span style=\"color:#00e676\">All Games Arena</span>")
g = g.replace("GG Wins <span>Game Lobby (20 Playable Games)</span>", "Explore All <span>20 Playable Games</span>")

with open("games.html", "w", encoding="utf-8") as f:
    f.write(g)

print("SUCCESS: Changes successfully reversed to previous state!")