# Rewriting main menu across index.html, games.html, tournaments.html, vip.html

sidebar_menu_html = """      <nav class="sidebar-nav" aria-label="Main navigation">
        <!-- Main Section -->
        <div class="nav-section">
          <span class="nav-section-label">Main Menu</span>
          <a href="index.html" class="nav-item active" id="nav-lobby-main" style="background:linear-gradient(135deg,rgba(0,230,118,0.2),rgba(0,176,255,0.12));border:1.5px solid #00e676;box-shadow:0 0 16px rgba(0,230,118,0.3)">
            <span class="nav-icon" style="color:#00e676;font-size:18px">🏠</span>
            <span class="nav-label" style="color:#00e676;font-weight:900;font-size:14px">Lobby</span>
            <span class="nav-badge" style="background:#00e676;color:#000;font-weight:900">20 GAMES</span>
          </a>
          <a href="tournaments.html" class="nav-item" id="nav-tournaments" style="background:linear-gradient(135deg,rgba(255,215,0,0.18),rgba(0,230,118,0.12));border:1px solid rgba(255,215,0,0.35)">
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

        <!-- All 20 Merged Games Menu -->
        <div class="nav-section">
          <span class="nav-section-label">All Games (20)</span>
          <a href="games/crash.html" class="nav-item"><span class="nav-icon">🚀</span><span class="nav-label">GG Crash</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/mines.html" class="nav-item"><span class="nav-icon">💣</span><span class="nav-label">GG Mines</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/limbo.html" class="nav-item"><span class="nav-icon">📈</span><span class="nav-label">GG Limbo</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/dragontower.html" class="nav-item"><span class="nav-icon">🐉</span><span class="nav-label">Dragon Tower</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/diamonds.html" class="nav-item"><span class="nav-icon">💎</span><span class="nav-label">Diamond Rush</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/slots.html" class="nav-item"><span class="nav-icon">🎰</span><span class="nav-label">Fortune Slots</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/plinko.html" class="nav-item"><span class="nav-icon">⚽</span><span class="nav-label">Plinko Drop</span><span class="nav-badge hot-badge">HOT</span></a>
          <a href="games/rummy.html" class="nav-item"><span class="nav-icon">🃏</span><span class="nav-label">Indian Rummy 3D</span><span class="nav-badge" style="background:#00e676;color:#000">3D</span></a>
          <a href="games/baccarat.html" class="nav-item"><span class="nav-icon">👑</span><span class="nav-label">Royale Baccarat</span></a>
          <a href="games/blackjack.html" class="nav-item"><span class="nav-icon">♣️</span><span class="nav-label">Blackjack 21</span></a>
          <a href="games/roulette.html" class="nav-item"><span class="nav-icon">🔴</span><span class="nav-label">Roulette Royale</span></a>
          <a href="games/sicbo.html" class="nav-item"><span class="nav-icon">🎲</span><span class="nav-label">Sic Bo 3-Dice</span></a>
          <a href="games/hilo.html" class="nav-item"><span class="nav-icon">🃏</span><span class="nav-label">Hilo Master</span></a>
          <a href="games/coinflip.html" class="nav-item"><span class="nav-icon">🪙</span><span class="nav-label">Coin Flip 3D</span></a>
          <a href="games/penalty.html" class="nav-item"><span class="nav-icon">⚽</span><span class="nav-label">Penalty Shootout</span></a>
          <a href="games/cups.html" class="nav-item"><span class="nav-icon">🪄</span><span class="nav-label">Magic Shells</span></a>
          <a href="games/ludo.html" class="nav-item"><span class="nav-icon">🎲</span><span class="nav-label">Ludo Champions</span></a>
          <a href="games/dice.html" class="nav-item"><span class="nav-icon">🎲</span><span class="nav-label">Classic Dice 3D</span></a>
          <a href="games/wheel.html" class="nav-item"><span class="nav-icon">🎡</span><span class="nav-label">Wheel of Fortune</span></a>
          <a href="games/keno.html" class="nav-item"><span class="nav-icon">🎱</span><span class="nav-label">Keno Classic</span></a>
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

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

import re
idx = re.sub(r'<nav class="sidebar-nav".*?</nav>', sidebar_menu_html, idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html main menu rewritten and merged with all 20 games and Lobby tab!")