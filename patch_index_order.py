with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# 1. Update Game Tabs in index.html with clean UTF-8 icons & no tournament tab
clean_tabs = """<div class="section-tabs" id="game-tabs" role="tablist" style="margin-bottom:0">
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
            </div>"""

import re
idx = re.sub(r'<div class="section-tabs" id="game-tabs".*?</div>', clean_tabs, idx, flags=re.DOTALL)

# 2. Update Quick Play Bar to have ONLY all 20 ordered game icons (no tournament tab)
clean_quick_bar = """        <!-- ── ALL 20 GAMES IN ORDER (CLICK ANY ICON TO PLAY) ── -->
        <div class="lobby-quick-games-bar">
          <div class="quick-bar-header">
            <div class="quick-bar-title">
              <span>🎮</span> Quick Launch Games (Click Any Game Icon to Play)
            </div>
            <span style="font-size:11.5px;color:#94a3b8;font-weight:700">← Scroll All 20 Games →</span>
          </div>
          <div class="quick-games-scroll">
            <a href="games/crash.html" class="quick-game-item" title="GG Crash"><span class="quick-item-icon">🚀</span><span class="quick-item-name">Crash</span></a>
            <a href="games/mines.html" class="quick-game-item" title="GG Mines"><span class="quick-item-icon">💣</span><span class="quick-item-name">Mines</span></a>
            <a href="games/limbo.html" class="quick-game-item" title="GG Limbo Rocket"><span class="quick-item-icon">📈</span><span class="quick-item-name">Limbo</span></a>
            <a href="games/dragontower.html" class="quick-game-item" title="Dragon Tower"><span class="quick-item-icon">🐉</span><span class="quick-item-name">Dragon Tower</span></a>
            <a href="games/diamonds.html" class="quick-game-item" title="Diamond Rush"><span class="quick-item-icon">💎</span><span class="quick-item-name">Diamonds</span></a>
            <a href="games/slots.html" class="quick-game-item" title="Fortune Slots 777"><span class="quick-item-icon">🎰</span><span class="quick-item-name">Slots 777</span></a>
            <a href="games/plinko.html" class="quick-game-item" title="GG Plinko Drop"><span class="quick-item-icon">⚽</span><span class="quick-item-name">Plinko</span></a>
            <a href="games/rummy.html" class="quick-game-item" title="Indian Rummy 3D"><span class="quick-item-icon">🃏</span><span class="quick-item-name">Indian Rummy</span></a>
            <a href="games/baccarat.html" class="quick-game-item" title="Royale Baccarat 3D"><span class="quick-item-icon">👑</span><span class="quick-item-name">Baccarat</span></a>
            <a href="games/blackjack.html" class="quick-game-item" title="Blackjack 21 Pro"><span class="quick-item-icon">♣️</span><span class="quick-item-name">Blackjack</span></a>
            <a href="games/roulette.html" class="quick-game-item" title="Roulette Royale 3D"><span class="quick-item-icon">🔴</span><span class="quick-item-name">Roulette</span></a>
            <a href="games/sicbo.html" class="quick-game-item" title="Sic Bo 3-Dice"><span class="quick-item-icon">🎲</span><span class="quick-item-name">Sic Bo</span></a>
            <a href="games/hilo.html" class="quick-game-item" title="Hilo Master"><span class="quick-item-icon">🃏</span><span class="quick-item-name">Hilo</span></a>
            <a href="games/coinflip.html" class="quick-game-item" title="Coin Flip 3D"><span class="quick-item-icon">🪙</span><span class="quick-item-name">Coin Flip</span></a>
            <a href="games/penalty.html" class="quick-game-item" title="Penalty Shootout"><span class="quick-item-icon">⚽</span><span class="quick-item-name">Penalty</span></a>
            <a href="games/cups.html" class="quick-game-item" title="Magic Shells 3D"><span class="quick-item-icon">🪄</span><span class="quick-item-name">Magic Shells</span></a>
            <a href="games/ludo.html" class="quick-game-item" title="GG Ludo Champions"><span class="quick-item-icon">🎲</span><span class="quick-item-name">Ludo 3D</span></a>
            <a href="games/dice.html" class="quick-game-item" title="Classic Dice 3D"><span class="quick-item-icon">🎲</span><span class="quick-item-name">Dice 3D</span></a>
            <a href="games/wheel.html" class="quick-game-item" title="Wheel of Fortune"><span class="quick-item-icon">🎡</span><span class="quick-item-name">Wheel</span></a>
            <a href="games/keno.html" class="quick-game-item" title="Keno Classic"><span class="quick-item-icon">🎱</span><span class="quick-item-name">Keno</span></a>
          </div>
        </div>"""

idx = re.sub(r'<!-- ── QUICK-PLAY GAME ICONS STRIP ── -->.*?<!-- STATS BAR -->', clean_quick_bar + '\n\n        <!-- STATS BAR -->', idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html tabs, quick game bar, and game ordering updated!")