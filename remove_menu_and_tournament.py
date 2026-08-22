with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

import re

# 1. Remove Sidebar & Menu Toggle Button
idx = re.sub(r'<aside class="sidebar".*?</aside>', '', idx, flags=re.DOTALL)
idx = re.sub(r'<button class="menu-toggle".*?</button>', '', idx, flags=re.DOTALL)

# 2. Update CSS for full-width layout without sidebar
no_sidebar_css = """
/* ── FULL WIDTH DASHBOARD (NO SIDEBAR / NO MAIN MENU) ── */
.app-layout {
  display: block !important;
}
.main-content {
  margin-left: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  padding: 0 !important;
}
.topbar {
  left: 0 !important;
  width: 100% !important;
}
.sidebar {
  display: none !important;
}
"""

if ".main-content {" not in idx or "margin-left: 0 !important" not in idx:
    idx = idx.replace("</head>", "<style>\n" + no_sidebar_css + "\n</style>\n</head>")

# 3. Replace Slide 2 (Tournaments slide) in Carousel with Instant Games & VIP slide
slide2_pattern = re.search(r'<div class="carousel-slide slide-2.*?</button>\s*</div>\s*</div>', idx, re.DOTALL)
if slide2_pattern:
    slide2_replacement = """<div class="carousel-slide slide-2" id="slide-2" style="cursor:pointer" onclick="openWalletModal('deposit')">
            <div class="slide-content">
              <span class="slide-badge">⚡ INSTANT CASH WIN</span>
              <h2 class="slide-title">20 Provably Fair <span class="text-gradient">Casino Games</span></h2>
              <p class="slide-desc">Play Crash, Mines, Indian Rummy, Roulette & Blackjack with verified 99.5% RTP and instant UPI withdrawals!</p>
              <div class="slide-actions">
                <button class="btn-primary" id="hero-btn-instant" onclick="event.stopPropagation(); openWalletModal('deposit')">⚡ Deposit &amp; Play Now</button>
                <button class="btn-secondary" onclick="event.stopPropagation(); document.getElementById('games-section').scrollIntoView({behavior:'smooth'})">Explore Games</button>
              </div>
            </div>
          </div>"""
    idx = idx[:slide2_pattern.start()] + slide2_replacement + idx[slide2_pattern.end():]

# 4. Remove any remaining tournament links/badges
idx = re.sub(r'<a href="tournaments\.html".*?</a>', '', idx, flags=re.DOTALL)
idx = re.sub(r'tournaments\.html', '#', idx)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html - Main menu (sidebar) and all Tournament references completely removed!")