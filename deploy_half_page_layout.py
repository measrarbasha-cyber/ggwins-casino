import os, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html"

# Enhanced CSS for spacious Banner zone & balanced Half-Page Games arrangement
enhanced_layout_css = """
/* ── SPACIOUS HERO BANNER & HALF-PAGE GAMES LAYOUT ── */
.hero-banner-zone {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 20px;
  margin: 20px 0 24px;
}
@media (max-width: 1024px) {
  .hero-banner-zone {
    grid-template-columns: 1fr;
  }
}

.hero-carousel {
  position: relative;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.6);
  border: 1.5px solid rgba(255, 215, 0, 0.3);
  background: #0f1527;
  height: 340px;
  margin: 0;
}

.side-promos-col {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.side-promo-card {
  flex: 1;
  background: linear-gradient(145deg, #111827, #0d121f);
  border: 1.5px solid rgba(255, 215, 0, 0.25);
  border-radius: 20px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
  transition: all 0.25s ease;
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}
.side-promo-card:hover {
  transform: translateY(-4px);
  border-color: #ffd700;
  box-shadow: 0 12px 30px rgba(255, 215, 0, 0.35);
}

/* ── HALF-PAGE GAMES SECTION ── */
.games-half-section {
  background: rgba(15, 21, 39, 0.6);
  border: 1.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 24px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
}

.games-half-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  max-height: 480px;
  overflow-y: auto;
  padding-right: 6px;
  scrollbar-width: thin;
  scrollbar-color: #ffd700 rgba(255,255,255,0.06);
}
.games-half-grid::-webkit-scrollbar { width: 6px; }
.games-half-grid::-webkit-scrollbar-thumb { background: #ffd700; border-radius: 999px; }

.half-game-card {
  background: linear-gradient(145deg, #111827, #0a0e1a);
  border: 1.5px solid rgba(255, 215, 0, 0.2);
  border-radius: 16px;
  padding: 14px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35);
  transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}
.half-game-card:hover {
  transform: translateY(-4px);
  border-color: #ffd700;
  box-shadow: 0 10px 25px rgba(255, 215, 0, 0.3);
  background: linear-gradient(145deg, #1e293b, #0f172a);
}

.h-icon-box {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: radial-gradient(circle, rgba(255,215,0,0.25) 0%, rgba(15,21,39,0.95) 100%);
  border: 1.5px solid #ffd700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  flex-shrink: 0;
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.25);
}

.h-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 14.5px;
  font-weight: 900;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.h-sub {
  font-size: 11px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 4px;
}
.h-play-btn {
  width: 100%;
  background: linear-gradient(135deg, #00e676, #00b0ff);
  color: #000;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 12.5px;
  font-weight: 900;
  padding: 8px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  text-align: center;
  box-shadow: 0 0 12px rgba(0, 230, 118, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
}
.h-play-btn:hover {
  transform: scale(1.03);
  box-shadow: 0 0 18px rgba(0, 230, 118, 0.55);
}
"""

with open(scratch_path, "r", encoding="utf-8") as f:
    idx = f.read()

if ".hero-banner-zone" not in idx:
    idx = idx.replace("</head>", "<style>\n" + enhanced_layout_css + "\n</style>\n</head>")

# 2. Main Banner Zone + Side Promos HTML
spacious_banner_html = """        <!-- ── GRAND SPACIOUS HERO BANNER ZONE ── -->
        <div class="hero-banner-zone">
          <!-- Main Auto-Rotating Carousel Banner -->
          <section class="hero-carousel" id="hero-carousel" aria-label="Featured promotions">
            <div class="carousel-track">
              <!-- Slide 1: Welcome Deposit Bonus -->
              <div class="carousel-slide slide-1 active" id="slide-1" onclick="if(typeof openWalletModal==='function') openWalletModal('deposit')" style="cursor:pointer">
                <div class="slide-content">
                  <span class="slide-badge">⚡ 100% WELCOME BONUS</span>
                  <h1 class="slide-title">Double Your First Deposit <span class="text-gradient">Up to ₹50,000</span></h1>
                  <p class="slide-desc">Use coupon code <strong style="color:#00e676;font-family:monospace;font-size:16px">GG1675</strong> for instant 100% matched cash on all UPI &amp; Bank deposits!</p>
                  <div class="slide-actions" style="display:flex;gap:12px;margin-top:16px">
                    <button class="btn-primary" onclick="event.stopPropagation(); if(typeof openWalletModal==='function') openWalletModal('deposit')">💳 Deposit with GG1675</button>
                    <button class="btn-secondary" onclick="event.stopPropagation(); document.getElementById('half-games-arena').scrollIntoView({behavior:'smooth'})">Play Games 🎮</button>
                  </div>
                </div>
              </div>

              <!-- Slide 2: Lucky Spin Wheel -->
              <div class="carousel-slide slide-2" id="slide-2" onclick="window.location.href='games/wheel.html'" style="cursor:pointer">
                <div class="slide-content">
                  <span class="slide-badge" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000">🎡 DAILY SPIN &amp; WIN</span>
                  <h2 class="slide-title">Lucky Spin Wheel <span class="text-gradient">Win Up to ₹25,000</span></h2>
                  <p class="slide-desc">Spin the Fortune Wheel daily to win instant real cash rewards, multiplier boosters, and VIP vault chips!</p>
                  <div class="slide-actions" style="display:flex;gap:12px;margin-top:16px">
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
                  <div class="slide-actions" style="display:flex;gap:12px;margin-top:16px">
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
          </section>

          <!-- Side Promo Feature Cards -->
          <div class="side-promos-col">
            <div class="side-promo-card" onclick="window.location.href='games/wheel.html'">
              <div>
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                  <span style="font-size:10.5px;font-weight:900;color:#ffd700;background:rgba(255,215,0,0.15);padding:2px 8px;border-radius:999px">SPIN REWARD</span>
                  <span style="font-size:24px">🎡</span>
                </div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:900;color:#fff">Daily Fortune Spin</div>
                <p style="font-size:12px;color:#94a3b8;margin:4px 0 0">Claim 1 free wheel spin daily for instant cash prizes!</p>
              </div>
              <span style="font-size:12px;font-weight:800;color:#00e676;margin-top:10px">Spin Now →</span>
            </div>

            <div class="side-promo-card" onclick="window.location.href='vip.html'">
              <div>
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                  <span style="font-size:10.5px;font-weight:900;color:#00e676;background:rgba(0,230,118,0.15);padding:2px 8px;border-radius:999px">VIP VAULT</span>
                  <span style="font-size:24px">👑</span>
                </div>
                <div style="font-family:'Space Grotesk',sans-serif;font-size:16px;font-weight:900;color:#fff">VIP Daily Cash Vault</div>
                <p style="font-size:12px;color:#94a3b8;margin:4px 0 0">Earn up to ₹150 daily cash drops automatically for 30 days.</p>
              </div>
              <span style="font-size:12px;font-weight:800;color:#ffd700;margin-top:10px">Join VIP Club →</span>
            </div>
          </div>
        </div>"""

# 3. Half-Page Games Section HTML
half_games_html = """        <!-- ── HALF-PAGE GAMES ARENA SECTION ── -->
        <section class="games-half-section" id="half-games-arena">
          <div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:12px;margin-bottom:16px">
            <div>
              <h2 style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:900;color:#fff;margin:0;display:flex;align-items:center;gap:8px">
                <span>🎮</span> Lobby Games Arena (20 Active Games)
              </h2>
              <span style="font-size:12px;color:#94a3b8">Scroll &amp; tap any game card below to play instantly!</span>
            </div>

            <!-- Filter tabs -->
            <div class="section-tabs" id="game-tabs" role="tablist" style="margin-bottom:0">
              <button class="tab-btn active" id="tab-all" onclick="filterHalfGames('all', this)">🎮 All (20)</button>
              <button class="tab-btn" id="tab-originals" onclick="filterHalfGames('originals', this)">🔥 Originals (7)</button>
              <button class="tab-btn" id="tab-table" onclick="filterHalfGames('table', this)">🃏 Cards &amp; Table (6)</button>
              <button class="tab-btn" id="tab-arcade" onclick="filterHalfGames('arcade', this)">🎯 Arcade (7)</button>
            </div>
          </div>

          <!-- Half-Page Grid of Games -->
          <div class="games-half-grid" id="half-games-grid">
            <!-- Populated by JS -->
          </div>
        </section>"""

import re
# Replace old hero carousel and games section
idx = re.sub(r'<!-- ── GRAND SPACIOUS HERO BANNER ZONE ── -->.*?<!-- STATS BAR -->', spacious_banner_html + '\n\n        <!-- STATS BAR -->', idx, flags=re.DOTALL)
if "class=\"hero-banner-zone\"" not in idx:
    idx = re.sub(r'<section class="hero-carousel".*?</section>', spacious_banner_html, idx, flags=re.DOTALL)
    idx = idx.replace("<section class=\"stats-bar\"", spacious_banner_html + "\n\n        <!-- STATS BAR -->\n        <section class=\"stats-bar\"")

idx = re.sub(r'<section class="section games-section".*?</section>', half_games_html, idx, flags=re.DOTALL)

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(idx)

shutil.copy2(scratch_path, brain_path)
print("SUCCESS: index.html updated with spacious Banner zone & balanced Half-Page Games layout!")