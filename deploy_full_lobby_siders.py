# Construct complete, fully integrated index.html with:
# 1. Sidebar (Siders) + Toggle
# 2. Auto-Rotating & Spin Banner Slider
# 3. Full-Page Quick Launch Games Arena (all 20 games with icons, live players, 1-click launch)
# 4. Multi-Account Wallet Chip, Modals, and Auth

import re

with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# 1. Layout & Styling CSS
layout_css = """
/* ── FULL PAGE QUICK LAUNCH & SIDEBAR LAYOUT ── */
.app-layout {
  display: flex !important;
  min-height: 100vh;
}
.sidebar {
  display: flex !important;
  width: 250px;
  min-width: 250px;
  background: #0b1120;
  border-right: 1px solid rgba(255, 215, 0, 0.2);
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  z-index: 100;
  transition: all 0.3s cubic-bezier(0.2, 0.8, 0.2, 1);
}
.sidebar.collapsed {
  width: 72px;
  min-width: 72px;
}
.sidebar.collapsed .logo-text,
.sidebar.collapsed .nav-label,
.sidebar.collapsed .nav-badge,
.sidebar.collapsed .nav-section-label,
.sidebar.collapsed .provably-fair span {
  display: none !important;
}
.main-content {
  flex: 1 !important;
  min-width: 0 !important;
  margin-left: 0 !important;
  padding: 0 24px 80px 24px !important;
  width: 100% !important;
  max-width: 1600px !important;
  margin: 0 auto !important;
  box-sizing: border-box;
}

/* ── AUTO-ROTATING HERO SLIDER ── */
.hero-carousel {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  margin: 20px 0 24px;
  box-shadow: 0 10px 35px rgba(0, 0, 0, 0.6);
  border: 1.5px solid rgba(255, 215, 0, 0.25);
  background: #0f1527;
  height: 280px;
}
.carousel-track {
  width: 100%;
  height: 100%;
  position: relative;
}
.carousel-slide {
  position: absolute;
  inset: 0;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.6s cubic-bezier(0.2, 0.8, 0.2, 1), visibility 0.6s;
  display: flex;
  align-items: center;
  padding: 30px 48px;
  box-sizing: border-box;
  background-size: cover;
  background-position: center;
}
.carousel-slide.active {
  opacity: 1;
  visibility: visible;
  z-index: 2;
}

.slide-1 {
  background: linear-gradient(135deg, rgba(7, 10, 20, 0.9) 0%, rgba(15, 23, 42, 0.8) 100%), radial-gradient(circle at 80% 50%, rgba(0, 230, 118, 0.25) 0%, transparent 60%);
}
.slide-2 {
  background: linear-gradient(135deg, rgba(7, 10, 20, 0.9) 0%, rgba(30, 15, 50, 0.85) 100%), radial-gradient(circle at 80% 50%, rgba(255, 215, 0, 0.3) 0%, transparent 60%);
}
.slide-3 {
  background: linear-gradient(135deg, rgba(7, 10, 20, 0.9) 0%, rgba(40, 20, 10, 0.85) 100%), radial-gradient(circle at 80% 50%, rgba(255, 140, 0, 0.3) 0%, transparent 60%);
}

.carousel-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: rgba(15, 21, 39, 0.85);
  border: 1.5px solid rgba(255, 215, 0, 0.4);
  color: #ffd700;
  font-size: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 10;
  transition: all 0.2s;
}
.carousel-nav-btn:hover {
  background: #ffd700;
  color: #000;
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
}
.prev-btn { left: 14px; }
.next-btn { right: 14px; }

.carousel-dots {
  position: absolute;
  bottom: 14px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 8px;
  z-index: 10;
}
.dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  cursor: pointer;
  transition: all 0.3s;
}
.dot.active {
  width: 28px;
  border-radius: 999px;
  background: #ffd700;
  box-shadow: 0 0 10px rgba(255, 215, 0, 0.6);
}

/* ── FULL PAGE QUICK LAUNCH GAMES GRID ── */
.quick-launch-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 18px;
  width: 100%;
  margin-top: 16px;
}

.ql-card {
  background: linear-gradient(145deg, #111827, #0d121f);
  border: 1.5px solid rgba(255, 215, 0, 0.25);
  border-radius: 18px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 14px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
  transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}
.ql-card:hover {
  transform: translateY(-5px);
  border-color: #ffd700;
  box-shadow: 0 12px 35px rgba(255, 215, 0, 0.3);
  background: linear-gradient(145deg, #1e293b, #0f172a);
}

.ql-card-top {
  display: flex;
  align-items: center;
  gap: 14px;
}

.ql-icon-box {
  width: 58px;
  height: 58px;
  border-radius: 16px;
  background: radial-gradient(circle, rgba(255,215,0,0.25) 0%, rgba(15,21,39,0.95) 100%);
  border: 1.5px solid #ffd700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  flex-shrink: 0;
  box-shadow: 0 0 14px rgba(255, 215, 0, 0.25);
}

.ql-meta {
  flex: 1;
  min-width: 0;
}

.ql-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 900;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.ql-sub {
  font-size: 11.5px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 2px;
}

.ql-tag {
  font-size: 9.5px;
  font-weight: 800;
  color: #00e676;
  background: rgba(0, 230, 118, 0.12);
  padding: 2px 6px;
  border-radius: 999px;
  text-transform: uppercase;
}

.ql-stats-row {
  background: rgba(0, 0, 0, 0.3);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 8px 12px;
  display: flex;
  justify-content: space-between;
  font-size: 11.5px;
}

.ql-play-btn {
  width: 100%;
  background: linear-gradient(135deg, #00e676, #00b0ff);
  color: #000;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13.5px;
  font-weight: 900;
  padding: 10px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  box-shadow: 0 0 14px rgba(0, 230, 118, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.ql-play-btn:hover {
  transform: scale(1.02);
  box-shadow: 0 0 20px rgba(0, 230, 118, 0.6);
}
"""

if ".quick-launch-grid" not in idx:
    idx = idx.replace("</head>", "<style>\n" + layout_css + "\n</style>\n</head>")

# 2. Sidebar (Siders) Navigation HTML
sidebar_html = """<aside class="sidebar" id="sidebar">
      <div class="sidebar-logo" style="padding:16px;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid rgba(255,255,255,0.08)">
        <div style="display:flex;align-items:center;gap:10px">
          <span style="font-size:24px">🎮</span>
          <span class="logo-text" style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:900;color:#ffd700">GG <span style="color:#00e676">Wins</span></span>
        </div>
        <button class="sidebar-toggle" id="sidebar-toggle-btn" onclick="document.getElementById('sidebar').classList.toggle('collapsed')" style="background:none;border:none;color:#94a3b8;cursor:pointer;font-size:16px" aria-label="Toggle sidebar">
          ◀
        </button>
      </div>

      <nav class="sidebar-nav" style="padding:12px 8px;display:flex;flex-direction:column;gap:6px">
        <!-- Main Section -->
        <div class="nav-section">
          <span class="nav-section-label" style="font-size:11px;color:#64748b;font-weight:800;text-transform:uppercase;padding:0 8px">Main Menu</span>
          <a href="index.html" class="nav-item active" id="nav-lobby" style="background:linear-gradient(135deg,rgba(0,230,118,0.2),rgba(0,176,255,0.12));border:1.5px solid #00e676;box-shadow:0 0 14px rgba(0,230,118,0.25);border-radius:10px;padding:10px 12px;display:flex;align-items:center;gap:10px;text-decoration:none;color:#fff;margin-top:4px">
            <span class="nav-icon" style="font-size:18px">🏠</span>
            <span class="nav-label" style="font-family:'Space Grotesk',sans-serif;font-weight:900;color:#00e676">Lobby</span>
            <span class="nav-badge" style="background:#00e676;color:#000;font-size:9px;font-weight:900;padding:2px 6px;border-radius:999px;margin-left:auto">LIVE</span>
          </a>
          <a href="vip.html" class="nav-item" id="nav-vip" style="background:rgba(255,215,0,0.08);border:1px solid rgba(255,215,0,0.25);border-radius:10px;padding:10px 12px;display:flex;align-items:center;gap:10px;text-decoration:none;color:#ffd700;margin-top:4px">
            <span class="nav-icon" style="font-size:18px">👑</span>
            <span class="nav-label" style="font-family:'Space Grotesk',sans-serif;font-weight:800">VIP Club</span>
            <span class="nav-badge" style="background:#ffd700;color:#000;font-size:9px;font-weight:900;padding:2px 6px;border-radius:999px;margin-left:auto">DAILY CASH</span>
          </a>
          <a href="vip-lounge.html" class="nav-item" id="nav-vip-lounge" style="border-radius:10px;padding:10px 12px;display:flex;align-items:center;gap:10px;text-decoration:none;color:#94a3b8;margin-top:4px">
            <span class="nav-icon" style="font-size:18px">💬</span>
            <span class="nav-label">VIP Lounge</span>
            <span class="nav-badge" style="background:#ffd700;color:#000;font-size:9px;font-weight:900;padding:2px 6px;border-radius:999px;margin-left:auto">ROOM</span>
          </a>
        </div>

        <!-- Quick Games Sider List -->
        <div class="nav-section" style="margin-top:12px">
          <span class="nav-section-label" style="font-size:11px;color:#64748b;font-weight:800;text-transform:uppercase;padding:0 8px">All 20 Games</span>
          <div style="display:flex;flex-direction:column;gap:3px;margin-top:4px">
            <a href="games/crash.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🚀</span><span class="nav-label">GG Crash</span><span style="font-size:9px;color:#ef4444;margin-left:auto;font-weight:800">HOT</span></a>
            <a href="games/mines.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">💣</span><span class="nav-label">GG Mines</span><span style="font-size:9px;color:#ef4444;margin-left:auto;font-weight:800">HOT</span></a>
            <a href="games/limbo.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">📈</span><span class="nav-label">GG Limbo</span></a>
            <a href="games/dragontower.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🐉</span><span class="nav-label">Dragon Tower</span></a>
            <a href="games/diamonds.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">💎</span><span class="nav-label">Diamond Rush</span></a>
            <a href="games/slots.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🎰</span><span class="nav-label">Slots 777</span></a>
            <a href="games/plinko.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">⚽</span><span class="nav-label">Plinko Drop</span></a>
            <a href="games/rummy.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🃏</span><span class="nav-label">Indian Rummy</span><span style="font-size:9px;color:#00e676;margin-left:auto;font-weight:800">3D</span></a>
            <a href="games/baccarat.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">👑</span><span class="nav-label">Royale Baccarat</span></a>
            <a href="games/blackjack.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">♣️</span><span class="nav-label">Blackjack 21</span></a>
            <a href="games/roulette.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🔴</span><span class="nav-label">Roulette 3D</span></a>
            <a href="games/sicbo.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🎲</span><span class="nav-label">Sic Bo 3-Dice</span></a>
            <a href="games/hilo.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🃏</span><span class="nav-label">Hilo Master</span></a>
            <a href="games/coinflip.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🪙</span><span class="nav-label">Coin Flip</span></a>
            <a href="games/penalty.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">⚽</span><span class="nav-label">Penalty Shoot</span></a>
            <a href="games/cups.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🪄</span><span class="nav-label">Magic Shells</span></a>
            <a href="games/ludo.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🎲</span><span class="nav-label">Ludo Champions</span></a>
            <a href="games/dice.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🎲</span><span class="nav-label">Dice 3D</span></a>
            <a href="games/wheel.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🎡</span><span class="nav-label">Wheel of Fortune</span></a>
            <a href="games/keno.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">🎱</span><span class="nav-label">Keno Classic</span></a>
          </div>
        </div>

        <!-- Banking & Support -->
        <div class="nav-section" style="margin-top:12px;border-top:1px solid rgba(255,255,255,0.08);padding-top:10px">
          <a href="#" class="nav-item" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit'); return false;" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#00e676;font-weight:700;text-decoration:none"><span class="nav-icon">💳</span><span class="nav-label">Deposit &amp; Wallet</span></a>
          <a href="#" class="nav-item" onclick="if(typeof openWalletModal==='function') openWalletModal('payment-history'); return false;" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">📜</span><span class="nav-label">Payment History</span></a>
          <a href="help-centre.html" class="nav-item" style="padding:8px 12px;border-radius:8px;display:flex;align-items:center;gap:10px;color:#cbd5e1;text-decoration:none"><span class="nav-icon">❓</span><span class="nav-label">Help Centre</span></a>
        </div>
      </nav>
    </aside>"""

# 3. Auto-Rotate Banner Slider with Spin Wheel Promo
slider_html = """        <!-- ── HERO PROMO CAROUSEL (AUTO-ROTATE & SPIN WHEEL) ── -->
        <section class="hero-carousel" id="hero-carousel" aria-label="Featured promotions">
          <div class="carousel-track">
            <!-- Slide 1: Welcome Deposit Bonus -->
            <div class="carousel-slide slide-1 active" id="slide-1" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit')" style="cursor:pointer">
              <div class="slide-content">
                <span class="slide-badge">⚡ INSTANT 100% BONUS</span>
                <h2 class="slide-title">Double Your First Deposit <span class="text-gradient">Up to ₹50,000</span></h2>
                <p class="slide-desc">Use coupon code <strong style="color:#00e676;font-family:monospace;font-size:16px">GG1675</strong> for instant 100% matched cash on all UPI &amp; Bank deposits!</p>
                <div class="slide-actions" style="display:flex;gap:12px;margin-top:14px">
                  <button class="btn-primary" onclick="event.stopPropagation(); if(typeof openWalletModal==='function') openWalletModal('deposit')">💳 Deposit with GG1675</button>
                  <button class="btn-secondary" onclick="event.stopPropagation(); document.getElementById('quick-games-section').scrollIntoView({behavior:'smooth'})">Explore Games</button>
                </div>
              </div>
            </div>

            <!-- Slide 2: Daily Spin & Win Wheel -->
            <div class="carousel-slide slide-2" id="slide-2" onclick="window.location.href='games/wheel.html'" style="cursor:pointer">
              <div class="slide-content">
                <span class="slide-badge" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000">🎡 DAILY SPIN &amp; WIN</span>
                <h2 class="slide-title">Lucky Spin Wheel <span class="text-gradient">Win Up to ₹25,000</span></h2>
                <p class="slide-desc">Spin the Fortune Wheel daily to win instant real cash rewards, multiplier boosters, and VIP vault chips!</p>
                <div class="slide-actions" style="display:flex;gap:12px;margin-top:14px">
                  <button class="btn-primary" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000" onclick="event.stopPropagation(); window.location.href='games/wheel.html'">🎡 Spin the Wheel Now</button>
                  <button class="btn-secondary" onclick="event.stopPropagation(); window.location.href='games/crash.html'">Play GG Crash 🚀</button>
                </div>
              </div>
            </div>

            <!-- Slide 3: VIP Membership -->
            <div class="carousel-slide slide-3" id="slide-3" onclick="window.location.href='vip.html'" style="cursor:pointer">
              <div class="slide-content">
                <span class="slide-badge" style="background:rgba(255,215,0,0.2);color:#ffd700;border:1px solid #ffd700">👑 VIP CLUB</span>
                <h2 class="slide-title">Monthly VIP Status <span class="text-gradient">&amp; Daily Cash</span></h2>
                <p class="slide-desc">Join Bronze, Silver or Gold VIP to earn up to ₹150 daily cash vault drops, private lounge access, and glowing badges!</p>
                <div class="slide-actions" style="display:flex;gap:12px;margin-top:14px">
                  <button class="btn-primary" onclick="event.stopPropagation(); window.location.href='vip.html'">👑 View VIP Plans</button>
                  <button class="btn-secondary" onclick="event.stopPropagation(); window.location.href='vip-lounge.html'">VIP Lounge 💬</button>
                </div>
              </div>
            </div>
          </div>

          <button class="carousel-nav-btn prev-btn" id="prev-slide-btn" aria-label="Previous slide">‹</button>
          <button class="carousel-nav-btn next-btn" id="next-slide-btn" aria-label="Next slide">›</button>

          <div class="carousel-dots" id="carousel-dots">
            <span class="dot active" data-slide="0"></span>
            <span class="dot" data-slide="1"></span>
            <span class="dot" data-slide="2"></span>
          </div>
        </section>"""

# 4. Full Page Quick Launch Games Section
games_arena_html = """        <!-- ── FULL PAGE QUICK LAUNCH GAMES ARENA ── -->
        <section class="section" id="quick-games-section" style="margin-top:28px">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px;margin-bottom:20px">
            <div>
              <h2 style="font-family:'Space Grotesk',sans-serif;font-size:24px;font-weight:900;color:#fff;margin:0 0 4px;display:flex;align-items:center;gap:8px">
                <span>🎮</span> Quick Launch Games Arena
              </h2>
              <p style="font-size:13.5px;color:#94a3b8;margin:0">Tap any game icon below to instantly launch and play in full-screen!</p>
            </div>

            <!-- Category Filter Tabs -->
            <div class="section-tabs" id="game-tabs" role="tablist" style="margin-bottom:0">
              <button class="tab-btn active" id="tab-all" data-category="all" onclick="filterGamesCategory('all', this)">
                <span>🎮</span> All (20)
              </button>
              <button class="tab-btn" id="tab-originals" data-category="originals" onclick="filterGamesCategory('originals', this)">
                <span>🔥</span> GG Originals (7)
              </button>
              <button class="tab-btn" id="tab-table" data-category="table" onclick="filterGamesCategory('table', this)">
                <span>🃏</span> Cards &amp; Table (6)
              </button>
              <button class="tab-btn" id="tab-arcade" data-category="arcade" onclick="filterGamesCategory('arcade', this)">
                <span>🎯</span> Casual &amp; Arcade (7)
              </button>
            </div>
          </div>

          <!-- Full Page Responsive Games Grid -->
          <div class="quick-launch-grid" id="full-quick-launch-grid">
            <!-- Populated by JS -->
          </div>
        </section>"""

# Replace in index.html
if "class=\"sidebar\"" not in idx:
    idx = idx.replace("<div class=\"app-layout\">", "<div class=\"app-layout\">\n" + sidebar_html)

idx = re.sub(r'<!-- ── HERO PROMO CAROUSEL.*?<!-- ── FULL PAGE QUICK LAUNCH GAMES ARENA ── -->', slider_html + '\n\n' + games_arena_html, idx, flags=re.DOTALL)
if "id=\"quick-games-section\"" not in idx:
    idx = re.sub(r'<!-- ── HERO PROMO CAROUSEL.*?</section>', slider_html, idx, flags=re.DOTALL)
    idx = re.sub(r'<section class="section games-section".*?</section>', games_arena_html, idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html fully updated with Lobby, Siders (Sidebar), Auto-Rotate/Spin Banner Slider, and Full-Page Quick Launch Games Arena!")