# 1. Update Slide 2 in index.html to Tournament redirection
with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

old_slide_2 = """            <!-- Slide 2: Weekly Race -->
            <div class="hero-slide" id="slide-2" onclick="if(event.target.tagName!=='BUTTON') document.getElementById('games-section')?.scrollIntoView({behavior:'smooth'})">
              <div class="slide-bg slide-bg-2"></div>
              <div class="slide-content">
                <span class="slide-tag">? Weekly Race</span>
                <h1 class="slide-title">?5,00,000 <span class="slide-accent">Prize Pool</span></h1>
                <p class="slide-desc">Compete with players across all games. Race to the top of the leaderboard and claim your cash share.</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="race-join-btn" onclick="event.stopPropagation(); document.getElementById('games-section')?.scrollIntoView({behavior:'smooth'})">Play Games ?</button>
                  <button class="btn-ghost btn-lg" id="race-view-btn" onclick="event.stopPropagation(); document.getElementById('recent-bets')?.scrollIntoView({behavior:'smooth'})">View Live Bets ?</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-2">
                <div class="trophy-anim">?</div>
              </div>
            </div>"""

new_slide_2 = """            <!-- Slide 2: Arena Tournaments -->
            <div class="hero-slide" id="slide-2" onclick="if(event.target.tagName!=='BUTTON') window.location.href='tournaments.html'">
              <div class="slide-bg slide-bg-2"></div>
              <div class="slide-content">
                <span class="slide-tag" style="background:rgba(255,215,0,0.18);border-color:#ffd700;color:#ffd700">🏆 Arena Tournaments</span>
                <h1 class="slide-title">₹4,85,000 <span class="slide-accent">Prize Pool</span></h1>
                <p class="slide-desc">Compete across all 20 game leaderboards! Pay ₹50 entry fee, climb ranks and win up to 60% grand cash share.</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="race-join-btn" onclick="event.stopPropagation(); window.location.href='tournaments.html'" style="background:linear-gradient(135deg,#00e676,#00b0ff);color:#000">Join Tournament 🏆</button>
                  <button class="btn-ghost btn-lg" id="race-view-btn" onclick="event.stopPropagation(); window.location.href='tournaments.html'">View Leaderboards 📊</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-2">
                <div class="trophy-anim">🏆</div>
              </div>
            </div>"""

if old_slide_2 in idx:
    idx = idx.replace(old_slide_2, new_slide_2)
else:
    # Use regex replacement if needed
    import re
    idx = re.sub(
        r'<!-- Slide 2:.*?</div>\s*</div>\s*</div>',
        new_slide_2,
        idx,
        flags=re.DOTALL
    )

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html Slide 2 updated to Tournament redirect!")