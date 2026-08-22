with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# 1. New Vertical Games List Section CSS & HTML
vertical_games_css = """
/* ── VERTICAL GAMES LIST STYLES ── */
.vertical-games-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  max-width: 100%;
}

.vertical-game-row {
  background: linear-gradient(145deg, #111827, #0b1120);
  border: 1.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 16px;
  padding: 14px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.4);
  transition: all 0.22s cubic-bezier(0.2, 0.8, 0.2, 1);
  cursor: pointer;
  text-decoration: none;
  color: inherit;
}
.vertical-game-row:hover {
  transform: translateX(6px);
  border-color: #ffd700;
  background: linear-gradient(145deg, #1e293b, #0f172a);
  box-shadow: 0 8px 30px rgba(255, 215, 0, 0.25);
}

.v-game-left {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
  min-width: 0;
}

.v-game-icon-box {
  width: 52px;
  height: 52px;
  border-radius: 14px;
  background: radial-gradient(circle, rgba(255,215,0,0.2) 0%, rgba(15,21,39,0.95) 100%);
  border: 1.5px solid #ffd700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
  box-shadow: 0 0 12px rgba(255, 215, 0, 0.25);
}

.v-game-meta {
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 0;
}

.v-game-title {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 16px;
  font-weight: 900;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.v-game-sub {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #94a3b8;
}

.v-game-tag {
  font-size: 10px;
  font-weight: 800;
  color: #00e676;
  background: rgba(0, 230, 118, 0.12);
  padding: 2px 7px;
  border-radius: 999px;
  text-transform: uppercase;
}

.v-game-right {
  flex-shrink: 0;
}

.v-play-btn {
  background: linear-gradient(135deg, #00e676, #00b0ff);
  color: #000;
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13.5px;
  font-weight: 900;
  padding: 10px 22px;
  border-radius: 10px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 0 14px rgba(0, 230, 118, 0.35);
  display: inline-flex;
  align-items: center;
  gap: 6px;
}
.v-play-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 22px rgba(0, 230, 118, 0.65);
}
"""

if ".vertical-games-container" not in idx:
    idx = idx.replace("</head>", "<style>\n" + vertical_games_css + "\n</style>\n</head>")

# Remove the bottom search bar and build vertical games section
new_games_section = """        <!-- GAME CATEGORY TABS (NO SEARCH BAR BELOW) -->
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
            </div>
          </div>

          <!-- Section: All 20 Games Arranged in Vertical Order -->
          <div class="subsection">
            <div class="subsection-header" style="margin-bottom:14px">
              <h2 class="subsection-title" style="font-family:'Space Grotesk',sans-serif;font-size:20px;font-weight:900;color:#fff;display:flex;align-items:center;gap:8px">
                <span>🎮</span> All Games (Vertical Play List)
              </h2>
              <span style="font-size:12.5px;color:#00e676;font-weight:800;background:rgba(0,230,118,0.12);padding:4px 10px;border-radius:999px" id="games-count-lbl">20 Games Active</span>
            </div>
            
            <div class="vertical-games-container" id="vertical-games-feed">
              <!-- Rendered vertically by JS -->
            </div>
          </div>
        </section>"""

import re
idx = re.sub(r'<section class="section games-section".*?</section>', new_games_section, idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html games section updated with vertical layout and search bar removed!")