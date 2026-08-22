with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html", "r", encoding="utf-8") as f:
    ihtml = f.read()

# Add Tournaments link in sidebar
old_vip_nav = """          <a href="vip-lounge.html" class="nav-item" id="nav-vip-lounge" style="background:linear-gradient(135deg,rgba(255,215,0,0.12),rgba(168,85,247,0.12));border:1px solid rgba(255,215,0,0.25)">
            <span class="nav-icon" style="color:#ffd700">👑</span>
            <span class="nav-label" style="color:#ffd700;font-weight:800">VIP Lounge</span>
            <span class="nav-badge" style="background:#ffd700;color:#000;font-weight:900">ROOM</span>
          </a>"""

new_vip_nav = """          <a href="tournaments.html" class="nav-item" id="nav-tournaments" style="background:linear-gradient(135deg,rgba(255,215,0,0.15),rgba(0,230,118,0.1));border:1px solid rgba(255,215,0,0.3)">
            <span class="nav-icon" style="color:#ffd700">🏆</span>
            <span class="nav-label" style="color:#ffd700;font-weight:800">Tournaments</span>
            <span class="nav-badge" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000;font-weight:900">₹50 ENTRY</span>
          </a>
          <a href="vip-lounge.html" class="nav-item" id="nav-vip-lounge" style="background:linear-gradient(135deg,rgba(255,215,0,0.12),rgba(168,85,247,0.12));border:1px solid rgba(255,215,0,0.25)">
            <span class="nav-icon" style="color:#ffd700">👑</span>
            <span class="nav-label" style="color:#ffd700;font-weight:800">VIP Lounge</span>
            <span class="nav-badge" style="background:#ffd700;color:#000;font-weight:900">ROOM</span>
          </a>"""

ihtml = ihtml.replace(old_vip_nav, new_vip_nav)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html", "w", encoding="utf-8") as f:
    f.write(ihtml)

print("SUCCESS: Added Tournaments link to index.html!")
