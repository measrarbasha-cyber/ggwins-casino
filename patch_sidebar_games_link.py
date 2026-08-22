with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

# Add All Games link in sidebar
old_nav = """      <nav class="sidebar-nav" aria-label="Main navigation">
        <!-- Casino Section -->
        <div class="nav-section">
          <span class="nav-section-label">Casino</span>"""

new_nav = """      <nav class="sidebar-nav" aria-label="Main navigation">
        <!-- Casino Section -->
        <div class="nav-section">
          <span class="nav-section-label">Casino</span>
          <a href="games.html" class="nav-item" id="nav-all-games" style="background:linear-gradient(135deg,rgba(0,230,118,0.18),rgba(0,176,255,0.12));border:1.5px solid #00e676;box-shadow:0 0 14px rgba(0,230,118,0.25)">
            <span class="nav-icon" style="color:#00e676">🎮</span>
            <span class="nav-label" style="color:#00e676;font-weight:900">All Games</span>
            <span class="nav-badge" style="background:#00e676;color:#000;font-weight:900">20 GAMES</span>
          </a>"""

if old_nav in idx:
    idx = idx.replace(old_nav, new_nav)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html sidebar updated with dedicated All Games tab!")