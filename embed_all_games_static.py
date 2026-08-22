import os, shutil

scratch_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html"
brain_path = r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\index.html"

# All 20 game cards directly baked into HTML for instant rendering
games_grid_static_html = """
          <!-- Half-Page Grid of Games (All 20 Pre-Rendered) -->
          <div class="games-half-grid" id="half-games-grid">
            <!-- 1. GG Crash -->
            <div class="half-game-card" onclick="window.location.href='games/crash.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🚀</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">GG Crash</div>
                  <div class="h-sub"><span>🔥 Original</span><span>•</span><span style="color:#ffd700">👥 5,821</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/crash.html'">▶ Play Now</button>
            </div>

            <!-- 2. GG Mines -->
            <div class="half-game-card" onclick="window.location.href='games/mines.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">💣</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">GG Mines</div>
                  <div class="h-sub"><span>🔥 Original</span><span>•</span><span style="color:#ffd700">👥 6,420</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/mines.html'">▶ Play Now</button>
            </div>

            <!-- 3. GG Limbo Rocket -->
            <div class="half-game-card" onclick="window.location.href='games/limbo.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">📈</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">GG Limbo</div>
                  <div class="h-sub"><span>🔥 Original</span><span>•</span><span style="color:#ffd700">👥 3,984</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/limbo.html'">▶ Play Now</button>
            </div>

            <!-- 4. Dragon Tower -->
            <div class="half-game-card" onclick="window.location.href='games/dragontower.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🐉</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Dragon Tower</div>
                  <div class="h-sub"><span>🔥 Original</span><span>•</span><span style="color:#ffd700">👥 5,120</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/dragontower.html'">▶ Play Now</button>
            </div>

            <!-- 5. GG Diamond Rush -->
            <div class="half-game-card" onclick="window.location.href='games/diamonds.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">💎</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Diamond Rush</div>
                  <div class="h-sub"><span>🔥 Original</span><span>•</span><span style="color:#ffd700">👥 4,920</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/diamonds.html'">▶ Play Now</button>
            </div>

            <!-- 6. GG Fortune Slots -->
            <div class="half-game-card" onclick="window.location.href='games/slots.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🎰</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Fortune Slots</div>
                  <div class="h-sub"><span>🔥 Original</span><span>•</span><span style="color:#ffd700">👥 5,244</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/slots.html'">▶ Play Now</button>
            </div>

            <!-- 7. GG Plinko Drop -->
            <div class="half-game-card" onclick="window.location.href='games/plinko.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">⚽</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Plinko Drop</div>
                  <div class="h-sub"><span>🔥 Original</span><span>•</span><span style="color:#ffd700">👥 4,891</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/plinko.html'">▶ Play Now</button>
            </div>

            <!-- 8. Indian Rummy 3D -->
            <div class="half-game-card" onclick="window.location.href='games/rummy.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🃏</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Indian Rummy 3D</div>
                  <div class="h-sub"><span>🃏 Table</span><span>•</span><span style="color:#ffd700">👥 7,450</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/rummy.html'">▶ Play Now</button>
            </div>

            <!-- 9. Royale Baccarat 3D -->
            <div class="half-game-card" onclick="window.location.href='games/baccarat.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">👑</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Royale Baccarat</div>
                  <div class="h-sub"><span>🃏 Table</span><span>•</span><span style="color:#ffd700">👥 3,870</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/baccarat.html'">▶ Play Now</button>
            </div>

            <!-- 10. Blackjack 21 -->
            <div class="half-game-card" onclick="window.location.href='games/blackjack.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">♣️</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Blackjack 21</div>
                  <div class="h-sub"><span>🃏 Table</span><span>•</span><span style="color:#ffd700">👥 3,980</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/blackjack.html'">▶ Play Now</button>
            </div>

            <!-- 11. Roulette Royale 3D -->
            <div class="half-game-card" onclick="window.location.href='games/roulette.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🔴</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Roulette Royale</div>
                  <div class="h-sub"><span>🃏 Table</span><span>•</span><span style="color:#ffd700">👥 4,201</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/roulette.html'">▶ Play Now</button>
            </div>

            <!-- 12. Sic Bo 3-Dice -->
            <div class="half-game-card" onclick="window.location.href='games/sicbo.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🎲</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Sic Bo 3-Dice</div>
                  <div class="h-sub"><span>🃏 Table</span><span>•</span><span style="color:#ffd700">👥 3,240</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/sicbo.html'">▶ Play Now</button>
            </div>

            <!-- 13. Hilo Master -->
            <div class="half-game-card" onclick="window.location.href='games/hilo.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🃏</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Hilo Master</div>
                  <div class="h-sub"><span>🃏 Table</span><span>•</span><span style="color:#ffd700">👥 3,410</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/hilo.html'">▶ Play Now</button>
            </div>

            <!-- 14. Coin Flip 3D -->
            <div class="half-game-card" onclick="window.location.href='games/coinflip.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🪙</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Coin Flip 3D</div>
                  <div class="h-sub"><span>🎯 Arcade</span><span>•</span><span style="color:#ffd700">👥 4,890</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/coinflip.html'">▶ Play Now</button>
            </div>

            <!-- 15. Penalty Shootout -->
            <div class="half-game-card" onclick="window.location.href='games/penalty.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">⚽</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Penalty Shootout</div>
                  <div class="h-sub"><span>🎯 Arcade</span><span>•</span><span style="color:#ffd700">👥 5,610</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/penalty.html'">▶ Play Now</button>
            </div>

            <!-- 16. Magic Shells 3D -->
            <div class="half-game-card" onclick="window.location.href='games/cups.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🪄</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Magic Shells</div>
                  <div class="h-sub"><span>🎯 Arcade</span><span>•</span><span style="color:#ffd700">👥 6,180</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/cups.html'">▶ Play Now</button>
            </div>

            <!-- 17. Ludo Champions -->
            <div class="half-game-card" onclick="window.location.href='games/ludo.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🎲</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Ludo Champions</div>
                  <div class="h-sub"><span>🎯 Arcade</span><span>•</span><span style="color:#ffd700">👥 6,420</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/ludo.html'">▶ Play Now</button>
            </div>

            <!-- 18. Classic Dice 3D -->
            <div class="half-game-card" onclick="window.location.href='games/dice.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🎲</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Classic Dice 3D</div>
                  <div class="h-sub"><span>🎯 Arcade</span><span>•</span><span style="color:#ffd700">👥 3,102</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/dice.html'">▶ Play Now</button>
            </div>

            <!-- 19. Wheel of Fortune -->
            <div class="half-game-card" onclick="window.location.href='games/wheel.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🎡</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Wheel of Fortune</div>
                  <div class="h-sub"><span>🎯 Arcade</span><span>•</span><span style="color:#ffd700">👥 4,120</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/wheel.html'">▶ Play Now</button>
            </div>

            <!-- 20. Keno Classic -->
            <div class="half-game-card" onclick="window.location.href='games/keno.html'">
              <div style="display:flex;align-items:center;gap:10px">
                <div class="h-icon-box">🎱</div>
                <div style="flex:1;min-width:0">
                  <div class="h-title">Keno Classic</div>
                  <div class="h-sub"><span>🎯 Arcade</span><span>•</span><span style="color:#ffd700">👥 2,830</span></div>
                </div>
              </div>
              <button class="h-play-btn" onclick="event.stopPropagation(); window.location.href='games/keno.html'">▶ Play Now</button>
            </div>
          </div>"""

with open(scratch_path, "r", encoding="utf-8") as f:
    idx = f.read()

import re
idx = re.sub(r'<div class="games-half-grid" id="half-games-grid">.*?</div>', games_grid_static_html, idx, flags=re.DOTALL)

with open(scratch_path, "w", encoding="utf-8") as f:
    f.write(idx)

shutil.copy2(scratch_path, brain_path)
print("SUCCESS: All 20 game cards permanently embedded into index.html!")