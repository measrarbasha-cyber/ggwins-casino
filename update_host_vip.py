import re

# 1. Update host/index.html
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\host\index.html", "r", encoding="utf-8") as f:
    h_html = f.read()

# Add VIP tab button in top nav
old_nav_tabs = """      <div class="top-nav-tabs">
        <button class="nav-tab-btn active" id="tab-btn-deposits" onclick="switchMainTab('deposits')">
          📥 Deposits <span class="badge-tab-count" id="nav-dep-badge">0</span>
        </button>
        <button class="nav-tab-btn wth-tab" id="tab-btn-withdrawals" onclick="switchMainTab('withdrawals')">
          📤 Withdrawals <span class="badge-tab-count" id="nav-wth-badge">0</span>
        </button>
      </div>"""

new_nav_tabs = """      <div class="top-nav-tabs">
        <button class="nav-tab-btn active" id="tab-btn-deposits" onclick="switchMainTab('deposits')">
          📥 Deposits <span class="badge-tab-count" id="nav-dep-badge">0</span>
        </button>
        <button class="nav-tab-btn wth-tab" id="tab-btn-withdrawals" onclick="switchMainTab('withdrawals')">
          📤 Withdrawals <span class="badge-tab-count" id="nav-wth-badge">0</span>
        </button>
        <button class="nav-tab-btn" id="tab-btn-vip" onclick="switchMainTab('vip')" style="border: 1px solid rgba(255,215,0,0.3)">
          👑 VIP Requests <span class="badge-tab-count" id="nav-vip-badge" style="background:#ffd700;color:#000">0</span>
        </button>
      </div>"""

h_html = h_html.replace(old_nav_tabs, new_nav_tabs)

# Add Section 3: VIP Club Requests
vip_section_html = """
    <!-- =============================================
         SECTION 3: VIP CLUB UPGRADE REQUESTS
         ============================================= -->
    <div class="tab-section" id="section-vip">
      <section class="stats-grid">
        <div class="stat-card" style="--card-accent: #ffd700">
          <span class="stat-label">Pending VIP Upgrades</span>
          <span class="stat-val" id="stat-vip-pending-count" style="color:#ffd700">0</span>
        </div>
        <div class="stat-card" style="--card-accent: var(--green)">
          <span class="stat-label">Approved VIP Members</span>
          <span class="stat-val" id="stat-vip-approved-count">0</span>
        </div>
        <div class="stat-card" style="--card-accent: var(--gold)">
          <span class="stat-label">Total VIP Revenue</span>
          <span class="stat-val" id="stat-vip-revenue">₹0.00</span>
        </div>
        <div class="stat-card" style="--card-accent: var(--purple)">
          <span class="stat-label">Total VIP Applications</span>
          <span class="stat-val" id="stat-vip-total-count">0</span>
        </div>
      </section>

      <section class="panel">
        <div class="panel-header">
          <div class="panel-title">
            <span>👑 Incoming VIP Club Upgrade Applications</span>
            <span class="badge-count" id="pending-vip-badge" style="background:#ffd700;color:#000">0 PENDING</span>
          </div>
          <div class="filter-tabs">
            <button class="filter-tab active" data-filter="all" onclick="setVipFilter('all', this)">All</button>
            <button class="filter-tab" data-filter="Pending" onclick="setVipFilter('Pending', this)">Pending</button>
            <button class="filter-tab" data-filter="Completed" onclick="setVipFilter('Completed', this)">Approved VIPs</button>
            <button class="filter-tab" data-filter="Rejected" onclick="setVipFilter('Rejected', this)">Rejected</button>
          </div>
        </div>

        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Order Number</th>
                <th>Player / Username</th>
                <th>Requested VIP Tier</th>
                <th>Activation Fee</th>
                <th>Payment Method</th>
                <th>12-digit UTR</th>
                <th>Date &amp; Time</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="vip-tbody">
              <tr>
                <td colspan="9" class="empty-state">
                  <div class="empty-icon">👑</div>
                  <p>No VIP requests currently pending.</p>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
"""

h_html = h_html.replace('</main>', vip_section_html + '\n  </main>')

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\host\index.html", "w", encoding="utf-8") as f:
    f.write(h_html)

# 2. Update host/host.js
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\host\host.js", "r", encoding="utf-8") as f:
    h_js = f.read()

# Update switchMainTab
old_switch = """    if (tabName === 'deposits') {
      document.getElementById('section-deposits').classList.add('active');
      document.getElementById('tab-btn-deposits').classList.add('active');
    } else if (tabName === 'withdrawals') {
      document.getElementById('section-withdrawals').classList.add('active');
      document.getElementById('tab-btn-withdrawals').classList.add('active');
    }"""

new_switch = """    if (tabName === 'deposits') {
      document.getElementById('section-deposits').classList.add('active');
      document.getElementById('tab-btn-deposits').classList.add('active');
    } else if (tabName === 'withdrawals') {
      document.getElementById('section-withdrawals').classList.add('active');
      document.getElementById('tab-btn-withdrawals').classList.add('active');
    } else if (tabName === 'vip') {
      document.getElementById('section-vip').classList.add('active');
      document.getElementById('tab-btn-vip').classList.add('active');
    }"""

h_js = h_js.replace(old_switch, new_switch)

# Add vipData variables and fetch
h_js = h_js.replace("let withdrawalsData = [];", "let withdrawalsData = [];\n  let vipData = [];\n  let currentVipFilter = 'all';\n  let lastPendingVipCount = 0;")

old_fetch = """      const [depRes, wthRes] = await Promise.all([
        fetch('/api/all-deposits'),
        fetch('/api/all-withdrawals')
      ]);"""

new_fetch = """      const [depRes, wthRes, vipRes] = await Promise.all([
        fetch('/api/all-deposits'),
        fetch('/api/all-withdrawals'),
        fetch('/api/all-vip-requests')
      ]);"""

h_js = h_js.replace(old_fetch, new_fetch)

old_fetch_set = """      if (wthRes.ok) {
        const wthJson = await wthRes.json();
        withdrawalsData = wthJson.withdrawals || [];
      }"""

new_fetch_set = """      if (wthRes.ok) {
        const wthJson = await wthRes.json();
        withdrawalsData = wthJson.withdrawals || [];
      }
      if (vipRes && vipRes.ok) {
        const vipJson = await vipRes.json();
        vipData = vipJson.vip_requests || [];
      }"""

h_js = h_js.replace(old_fetch_set, new_fetch_set)

h_js = h_js.replace("renderWithdrawalsTable();", "renderWithdrawalsTable();\n      renderVipTable();")

# VIP Stats update
old_stat_block = """    lastPendingDepCount = pendingDeps.length;
    lastPendingWthCount = pendingWths.length;"""

new_stat_block = """    // VIP stats
    const pendingVips = vipData.filter(v => v.status === 'Pending');
    const approvedVips = vipData.filter(v => v.status === 'Completed');
    document.getElementById('stat-vip-pending-count').textContent = pendingVips.length;
    document.getElementById('pending-vip-badge').textContent = `${pendingVips.length} PENDING`;
    document.getElementById('nav-vip-badge').textContent = pendingVips.length;
    document.getElementById('stat-vip-approved-count').textContent = approvedVips.length;
    document.getElementById('stat-vip-total-count').textContent = vipData.length;

    let totalVipRev = 0;
    approvedVips.forEach(v => { totalVipRev += parseFloat(v.amount) || 0; });
    document.getElementById('stat-vip-revenue').textContent = `₹${totalVipRev.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

    if (pendingDeps.length > lastPendingDepCount || pendingWths.length > lastPendingWthCount || pendingVips.length > lastPendingVipCount) {
      playAlertTone();
    }

    lastPendingDepCount = pendingDeps.length;
    lastPendingWthCount = pendingWths.length;
    lastPendingVipCount = pendingVips.length;"""

h_js = h_js.replace(old_stat_block, new_stat_block)

# VIP Table Rendering & Actions
vip_table_functions = """
  // ── VIP FILTER & TABLE RENDERING ─────────────────────────────
  window.setVipFilter = function(filter, btn) {
    currentVipFilter = filter;
    document.querySelectorAll('#section-vip .filter-tab').forEach(t => t.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderVipTable();
  };

  function renderVipTable() {
    const tbody = document.getElementById('vip-tbody');
    if (!tbody) return;

    let filtered = vipData;
    if (currentVipFilter !== 'all') {
      filtered = vipData.filter(v => v.status === currentVipFilter);
    }

    if (filtered.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" class="empty-state">
            <div class="empty-icon">👑</div>
            <p>No ${currentVipFilter === 'all' ? '' : currentVipFilter.toLowerCase()} VIP requests found.</p>
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = filtered.map(v => {
      const isPending = v.status === 'Pending';
      const isCompleted = v.status === 'Completed';
      const statusBadge = isPending
        ? `<span class="badge-status status-pending"><span class="pulse-dot" style="background:#ffd700"></span>Pending Host Approval</span>`
        : isCompleted
        ? `<span class="badge-status status-completed">👑 Approved &amp; Active</span>`
        : `<span class="badge-status status-rejected">❌ Rejected</span>`;

      const dateStr = v.timestamp ? new Date(v.timestamp).toLocaleString('en-IN') : 'Just now';

      return `
        <tr class="${isPending ? 'pending-row' : ''}">
          <td style="font-family:'Space Grotesk',sans-serif;font-weight:700;color:#ffd700">${v.orderId || v.id}</td>
          <td><strong>${v.username || 'Player'}</strong></td>
          <td><span style="background:rgba(255,215,0,0.15);border:1px solid #ffd700;color:#ffd700;font-weight:800;padding:2px 8px;border-radius:999px;font-size:11.5px">👑 ${v.tierName || 'Gold VIP'}</span></td>
          <td style="font-family:'Space Grotesk',sans-serif;font-weight:800;color:#00e676">₹${parseFloat(v.amount||0).toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
          <td>${v.method || 'UPI Instant'}</td>
          <td><span class="utr-code" onclick="navigator.clipboard.writeText('${v.utr}')" title="Click to copy">${v.utr || 'N/A'}</span></td>
          <td style="font-size:12px;color:#94a3b8">${dateStr}</td>
          <td>${statusBadge}</td>
          <td>
            ${isPending ? `
              <div class="action-btn-group">
                <button class="btn btn-approve" onclick="approveVipRequest('${v.id}')" title="Approve VIP & Activate Glowing Badge">
                  👑 Approve VIP
                </button>
                <button class="btn btn-reject" onclick="rejectVipRequest('${v.id}')" title="Reject VIP application">
                  ✕ Reject
                </button>
              </div>
            ` : `<span style="font-size:12px;color:#64748b">${isCompleted ? '✓ Granted' : 'Rejected'}</span>`}
          </td>
        </tr>
      `;
    }).join('');
  }

  // ── APPROVE VIP REQUEST ───────────────────────────────────────
  window.approveVipRequest = async function(id) {
    const target = vipData.find(v => v.id === id);
    if (!target) return;

    if (!confirm(`👑 Approve VIP Upgrade for ${target.username} to ${target.tierName || 'Gold VIP'} (₹${target.amount})? This will instantly activate their glowing VIP badge and VIP Lounge access!`)) {
      return;
    }

    try {
      const res = await fetch('/api/approve-vip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      const data = await res.json();
      if (data.success) {
        showToastNotification(`👑 ${target.tierName} approved for ${target.username}!`, 'success');
        fetchAllData();
      } else {
        alert(data.message || 'Approval failed');
      }
    } catch(e) {
      target.status = 'Completed';
      renderVipTable();
      updateAllStats();
      showToastNotification(`👑 VIP approved locally.`, 'success');
    }
  };

  // ── REJECT VIP REQUEST ────────────────────────────────────────
  window.rejectVipRequest = async function(id) {
    const target = vipData.find(v => v.id === id);
    if (!target) return;

    if (!confirm(`Reject VIP upgrade application ${target.orderId || target.id}?`)) return;

    try {
      const res = await fetch('/api/reject-vip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      const data = await res.json();
      if (data.success) {
        showToastNotification(`VIP request rejected.`, 'info');
        fetchAllData();
      }
    } catch(e) {
      target.status = 'Rejected';
      renderVipTable();
      updateAllStats();
    }
  };
"""

h_js += vip_table_functions

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\brain\adfb82a4-49a4-4622-8f3c-72850acc0c06\host\host.js", "w", encoding="utf-8") as f:
    f.write(h_js)

print("Updated host/index.html and host/host.js with VIP Club management tab!")
