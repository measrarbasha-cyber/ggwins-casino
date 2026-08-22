import shutil
from pathlib import Path

# Paths
brain_host = Path(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\host")
scratch_host = Path(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\host")
scratch_host.mkdir(parents=True, exist_ok=True)

with open(brain_host / "index.html", "r", encoding="utf-8") as f:
    h_idx = f.read()

# Add CSS for .vip-tab
vip_tab_css = """
    .nav-tab-btn.vip-tab:hover {
      border-color: #ffd700;
      color: #ffd700;
    }
    .nav-tab-btn.vip-tab.active {
      background: linear-gradient(135deg, #ffd700, #ff8c00);
      color: #000;
      border-color: #ffd700;
      box-shadow: 0 0 16px rgba(255, 215, 0, 0.4);
    }
    .btn-approve-vip {
      background: linear-gradient(135deg, #ffd700, #ff8c00);
      color: #000;
      border: none;
      font-weight: 800;
      font-size: 12px;
      padding: 7px 14px;
      border-radius: 8px;
      cursor: pointer;
      box-shadow: 0 0 12px rgba(255, 215, 0, 0.3);
      transition: all 0.2s;
    }
    .btn-approve-vip:hover {
      transform: scale(1.04);
      box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
    }
"""

if ".nav-tab-btn.vip-tab" not in h_idx:
    h_idx = h_idx.replace("</style>", vip_tab_css + "\n</style>")

# Add VIP tab button in top-nav-tabs
old_nav_tabs = """    <!-- Main Section Switcher Tabs -->
    <div class="top-nav-tabs">
      <button class="nav-tab-btn active" id="tab-btn-deposits" onclick="switchMainTab('deposits')">
        <span>📥 Deposits</span>
        <span class="badge-tab-count" id="nav-dep-badge">0</span>
      </button>
      <button class="nav-tab-btn wth-tab" id="tab-btn-withdrawals" onclick="switchMainTab('withdrawals')">
        <span>📤 Withdrawals</span>
        <span class="badge-tab-count" id="nav-wth-badge">0</span>
      </button>
    </div>"""

new_nav_tabs = """    <!-- Main Section Switcher Tabs -->
    <div class="top-nav-tabs">
      <button class="nav-tab-btn active" id="tab-btn-deposits" onclick="switchMainTab('deposits')">
        <span>📥 Deposits</span>
        <span class="badge-tab-count" id="nav-dep-badge">0</span>
      </button>
      <button class="nav-tab-btn wth-tab" id="tab-btn-withdrawals" onclick="switchMainTab('withdrawals')">
        <span>📤 Withdrawals</span>
        <span class="badge-tab-count" id="nav-wth-badge">0</span>
      </button>
      <button class="nav-tab-btn vip-tab" id="tab-btn-vip" onclick="switchMainTab('vip')">
        <span>👑 VIP Club</span>
        <span class="badge-tab-count" id="nav-vip-badge" style="background:#ffd700;color:#000">0</span>
      </button>
    </div>"""

h_idx = h_idx.replace(old_nav_tabs, new_nav_tabs)

with open(brain_host / "index.html", "w", encoding="utf-8") as f:
    f.write(h_idx)

with open(scratch_host / "index.html", "w", encoding="utf-8") as f:
    f.write(h_idx)

# Sync host.js
shutil.copyfile(brain_host / "host.js", scratch_host / "host.js")

print("SUCCESS: Added separate VIP tab in Admin Terminal with real-time approval buttons & stats!")
