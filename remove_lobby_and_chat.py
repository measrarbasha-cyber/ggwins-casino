# 1. Update index.html to remove Lobby and all Live Chat elements
with open("index.html", "r", encoding="utf-8") as f:
    idx = f.read()

import re

# Remove Lobby nav item in sidebar
idx = re.sub(r'<a href="index\.html" class="nav-item active" id="nav-lobby">.*?</a>\s*', '', idx, flags=re.DOTALL)

# Remove chat toggle button & vip chat mini badge from topbar
idx = re.sub(r'<span id="vip-chat-mini-badge".*?</span>', '', idx, flags=re.DOTALL)
idx = re.sub(r'<button class="chat-toggle-btn" id="chat-toggle-btn".*?</button>', '', idx, flags=re.DOTALL)

# Remove chat-sidebar aside element
idx = re.sub(r'<!-- LIVE CHAT SIDEBAR -->\s*<aside class="chat-sidebar" id="chat-sidebar">.*?</aside>', '', idx, flags=re.DOTALL)

# Remove bottom floating AI Chat Button & AI Chat Window
idx = re.sub(r'<!-- AI Chat Button -->\s*<button id="ai-chat-btn".*?<!-- AI Chat Window -->\s*<div id="ai-chat-window">.*?</div>\s*</div>', '', idx, flags=re.DOTALL)

# Remove mobile bottom nav chat button
idx = re.sub(r'<button class="mob-nav-item"[^>]*id="mob-nav-chat".*?</button>', '', idx, flags=re.DOTALL)

# Clean any leftover ai-chat-btn styles
idx = re.sub(r'#ai-chat-btn\s*\{.*?</style>', '</style>', idx, flags=re.DOTALL)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(idx)

print("SUCCESS: index.html - Lobby and Live Chat completely removed!")

# 2. Update tournaments.html to remove chat button and ai-chat-drawer
with open("tournaments.html", "r", encoding="utf-8") as f:
    t = f.read()

# Remove chat button from top nav
t = re.sub(r'<button onclick="toggleAiChatDrawer\(\)".*?</button>', '', t, flags=re.DOTALL)

# Remove ai-chat-drawer html & js
t = re.sub(r'<!-- ── FULLY AI ANIMATED LIVE CHAT DRAWER ── -->.*?</div>\s*</div>', '', t, flags=re.DOTALL)
t = re.sub(r'// ── AI LIVE CHAT DRAWER LOGIC ──.*?</script>', '</script>', t, flags=re.DOTALL)

with open("tournaments.html", "w", encoding="utf-8") as f:
    f.write(t)

print("SUCCESS: tournaments.html - Live Chat completely removed!")

# 3. Update vip.html to remove ai-chat-drawer
with open("vip.html", "r", encoding="utf-8") as f:
    v = f.read()

v = re.sub(r'<!-- ── FULLY AI ANIMATED LIVE CHAT DRAWER ── -->.*?</div>\s*</div>', '', v, flags=re.DOTALL)
v = re.sub(r'<script>\s*function toggleAiChatDrawer\(.*?</script>', '', v, flags=re.DOTALL)

with open("vip.html", "w", encoding="utf-8") as f:
    f.write(v)

print("SUCCESS: vip.html - Live Chat completely removed!")