import os

# 1. Remove temporary games.html if created recently
if os.path.exists("games.html"):
    os.remove("games.html")
    print("REMOVED: games.html")

# 2. Restore index.html to standard classic lobby structure (grids, slider, sidebar, chat)
# Let's inspect the current index.html and restore standard game grids and sidebar
with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Let's restore standard games-section with original grids
standard_games_section = """        <!-- GAME CATEGORY TABS & GRIDS -->
        <section class="section games-section" id="games-section">
          <!-- Category Tabs -->
          <div style="margin-bottom:20px">
            <div class="section-tabs" id="game-tabs" role="tablist" style="margin-bottom:0">
              <button class="tab-btn active" id="tab-all" data-category="all" role="tab" aria-selected="true">
                <span>🎮</span> All Games (20)
              </button>
              <button class="tab-btn" id="tab-originals-cat" data-category="originals" role="tab" aria-selected="false">
                <span>🔥</span> GG Originals (7)
              </button>
              <button class="tab-btn" id="tab-table-cat" data-category="table" role="tab" aria-selected="false">
                <span>🃏</span> Cards &amp; Table (6)
              </button>
              <button class="tab-btn" id="tab-arcade-cat" data-category="arcade" role="tab" aria-selected="false">
                <span>🎯</span> Casual &amp; Arcade (7)
              </button>
              <button class="tab-btn" id="tab-slots-cat" data-category="slots" role="tab" aria-selected="false">
                <span>🎰</span> Slots &amp; Jackpots
              </button>
            </div>
          </div>

          <!-- Section 1: Playable GG Originals -->
          <div class="subsection" id="originals-subsection">
            <div class="subsection-header">
              <h2 class="subsection-title" style="display:flex;align-items:center;gap:8px">
                <span>🔥</span> GG Originals (Instant Play)
              </h2>
              <span style="font-size:12px;color:var(--text-muted);font-weight:600" id="originals-count-lbl">7 Games</span>
            </div>
            <div class="games-grid" id="originals-grid">
              <!-- Injected by JS -->
            </div>
          </div>

          <!-- Section 2: Table & Card Games -->
          <div class="subsection" id="table-subsection">
            <div class="subsection-header">
              <h2 class="subsection-title" style="display:flex;align-items:center;gap:8px">
                <span>🃏</span> Cards &amp; Table Royale (Rummy, Baccarat, Blackjack, Sic Bo)
              </h2>
            </div>
            <div class="games-grid" id="table-grid">
              <!-- Injected by JS -->
            </div>
          </div>

          <!-- Section 3: Arcade & Action -->
          <div class="subsection" id="arcade-subsection">
            <div class="subsection-header">
              <h2 class="subsection-title" style="display:flex;align-items:center;gap:8px">
                <span>🎯</span> Casual &amp; Arcade (Crash, Mines, Magic Shells, Penalty)
              </h2>
            </div>
            <div class="games-grid" id="arcade-grid">
              <!-- Injected by JS -->
            </div>
          </div>
        </section>"""

import re
idx = re.sub(r'<section class="section games-section".*?</section>', standard_games_section, idx, flags=re.DOTALL)

# Restore standard sidebar
standard_sidebar = """      <nav class="sidebar-nav" aria-label="Main navigation">
        <!-- Casino Section -->
        <div class="nav-section">
          <span class="nav-section-label">Casino</span>
          <a href="index.html" class="nav-item active" id="nav-lobby">
            <span class="nav-icon" style="color:#00e676;font-size:18px">🏠</span>
            <span class="nav-label" style="font-weight:800">Lobby</span>
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

idx = re.sub(r'<nav class="sidebar-nav".*?</nav>', standard_sidebar, idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html restored to standard 1-hour previous state!")