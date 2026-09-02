// GG Wins Admin Host Terminal Engine (Deposits, Withdrawals & VIP Memberships)
(function() {
  'use strict';

  let depositsData = [];
  let withdrawalsData = [];
  let vipData = [];

  let currentDepositFilter = 'all';
  let currentWithdrawFilter = 'all';
  let currentVipFilter = 'all';

  let lastPendingDepCount = 0;
  let lastPendingWthCount = 0;
  let lastPendingVipCount = 0;
  let isFirstLoad = true;

  // ── 1. MAIN TAB SWITCHER ─────────────────────────────────────
  window.switchMainTab = function(tabName) {
    document.querySelectorAll('.tab-section').forEach(sec => sec.classList.remove('active'));
    document.querySelectorAll('.nav-tab-btn').forEach(btn => btn.classList.remove('active'));

    if (tabName === 'deposits') {
      const sec = document.getElementById('section-deposits');
      const btn = document.getElementById('tab-btn-deposits');
      if (sec) sec.classList.add('active');
      if (btn) btn.classList.add('active');
    } else if (tabName === 'withdrawals') {
      const sec = document.getElementById('section-withdrawals');
      const btn = document.getElementById('tab-btn-withdrawals');
      if (sec) sec.classList.add('active');
      if (btn) btn.classList.add('active');
    } else if (tabName === 'vip') {
      const sec = document.getElementById('section-vip');
      const btn = document.getElementById('tab-btn-vip');
      if (sec) sec.classList.add('active');
      if (btn) btn.classList.add('active');
    } else if (tabName === 'user-wallet') {
      const sec = document.getElementById('section-user-wallet');
      const btn = document.getElementById('tab-btn-user-wallet');
      if (sec) sec.classList.add('active');
      if (btn) btn.classList.add('active');
      loadAllUsersDirectory();
    } else if (tabName === 'email') {
      const sec = document.getElementById('section-email');
      const btn = document.getElementById('tab-btn-email');
      if (sec) sec.classList.add('active');
      if (btn) btn.classList.add('active');
      loadEmailConfigAndLogs();
    }
  };

  // ── 2. FETCH ALL DATA (REAL-TIME ENGINE) ──────────────────────
  async function fetchAllData() {
    try {
      const [depRes, wthRes, vipRes] = await Promise.all([
        fetch('/api/all-deposits'),
        fetch('/api/all-withdrawals'),
        fetch('/api/all-vip-requests')
      ]);

      if (depRes.ok) {
        const depJson = await depRes.json();
        depositsData = depJson.deposits || [];
      }
      if (wthRes.ok) {
        const wthJson = await wthRes.json();
        withdrawalsData = wthJson.withdrawals || [];
      }
      if (vipRes && vipRes.ok) {
        const vipJson = await vipRes.json();
        vipData = vipJson.vip_requests || [];
      }

      renderDepositsTable();
      renderWithdrawalsTable();
      renderVipTable();
      updateAllStats();
      loadAllUsersDirectory();

      const conn = document.getElementById('conn-status');
      if (conn) {
        conn.textContent = 'LIVE SYNC';
        conn.style.color = '#00e676';
      }
    } catch (e) {
      console.warn('API sync warning:', e);
      const conn = document.getElementById('conn-status');
      if (conn) {
        conn.textContent = 'RETRYING...';
        conn.style.color = '#f59e0b';
      }
    }
  }

  // ── 3. UPDATE STATS & PLAY NOTIFICATIONS ─────────────────────
  function updateAllStats() {
    // Deposits stats
    const pendingDeps = depositsData.filter(d => d.status === 'Pending');
    const completedDeps = depositsData.filter(d => d.status === 'Completed');
    const rejectedDeps = depositsData.filter(d => d.status === 'Rejected');
    
    setElText('stat-pending-count', pendingDeps.length);
    setElText('pending-badge', `${pendingDeps.length} PENDING`);
    setElText('nav-dep-badge', pendingDeps.length);
    setElText('stat-total-count', depositsData.length);

    // Update filter tabs with live counts
    const depFilterAll = document.querySelector('#section-deposits .filter-tab[data-filter="all"]');
    if (depFilterAll) depFilterAll.innerHTML = `All History <span style="opacity:0.8;font-size:11px;margin-left:4px">(${depositsData.length})</span>`;
    const depFilterPending = document.querySelector('#section-deposits .filter-tab[data-filter="Pending"]');
    if (depFilterPending) depFilterPending.innerHTML = `Pending <span style="background:rgba(255,215,0,0.25);color:#ffd700;padding:1px 6px;border-radius:10px;font-size:11px;margin-left:4px">${pendingDeps.length}</span>`;
    const depFilterCompleted = document.querySelector('#section-deposits .filter-tab[data-filter="Completed"]');
    if (depFilterCompleted) depFilterCompleted.innerHTML = `Approved / History <span style="background:rgba(0,230,118,0.2);color:#00e676;padding:1px 6px;border-radius:10px;font-size:11px;margin-left:4px">${completedDeps.length}</span>`;
    const depFilterRejected = document.querySelector('#section-deposits .filter-tab[data-filter="Rejected"]');
    if (depFilterRejected) depFilterRejected.innerHTML = `Rejected <span style="background:rgba(239,68,68,0.2);color:#ef4444;padding:1px 6px;border-radius:10px;font-size:11px;margin-left:4px">${rejectedDeps.length}</span>`;

    let totalInrDep = 0;
    let totalUsdtDep = 0;
    completedDeps.forEach(d => {
      if (d.wallet === 'usdt' || d.currency === 'USDT') totalUsdtDep += parseFloat(d.amount) || 0;
      else totalInrDep += parseFloat(d.amount) || 0;
    });
    setElText('stat-real-total', `₹${totalInrDep.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
    setElText('stat-usdt-total', `${totalUsdtDep.toFixed(2)} ₮`);

    // Withdrawals stats
    const pendingWths = withdrawalsData.filter(w => w.status === 'Pending');
    const completedWths = withdrawalsData.filter(w => w.status === 'Completed');
    const rejectedWths = withdrawalsData.filter(w => w.status === 'Rejected');

    setElText('stat-wth-pending-count', pendingWths.length);
    setElText('pending-wth-badge', `${pendingWths.length} PENDING`);
    setElText('nav-wth-badge', pendingWths.length);
    setElText('stat-wth-total-count', withdrawalsData.length);

    const wthFilterAll = document.querySelector('#section-withdrawals .filter-tab[data-filter="all"]');
    if (wthFilterAll) wthFilterAll.innerHTML = `All History <span style="opacity:0.8;font-size:11px;margin-left:4px">(${withdrawalsData.length})</span>`;
    const wthFilterPending = document.querySelector('#section-withdrawals .filter-tab[data-filter="Pending"]');
    if (wthFilterPending) wthFilterPending.innerHTML = `Pending <span style="background:rgba(56,189,248,0.25);color:#38bdf8;padding:1px 6px;border-radius:10px;font-size:11px;margin-left:4px">${pendingWths.length}</span>`;
    const wthFilterCompleted = document.querySelector('#section-withdrawals .filter-tab[data-filter="Completed"]');
    if (wthFilterCompleted) wthFilterCompleted.innerHTML = `Paid / History <span style="background:rgba(0,230,118,0.2);color:#00e676;padding:1px 6px;border-radius:10px;font-size:11px;margin-left:4px">${completedWths.length}</span>`;

    let totalInrWth = 0;
    let totalUsdtWth = 0;
    completedWths.forEach(w => {
      if (w.wallet === 'usdt' || w.currency === 'USDT') totalUsdtWth += parseFloat(w.amount) || 0;
      else totalInrWth += parseFloat(w.amount) || 0;
    });
    setElText('stat-wth-paid-inr', `₹${totalInrWth.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
    setElText('stat-wth-paid-usdt', `${totalUsdtWth.toFixed(2)} ₮`);

    // VIP stats
    const pendingVips = vipData.filter(v => v.status === 'Pending');
    const approvedVips = vipData.filter(v => v.status === 'Completed');
    const rejectedVips = vipData.filter(v => v.status === 'Rejected');

    setElText('stat-vip-pending-count', pendingVips.length);
    setElText('pending-vip-badge', `${pendingVips.length} PENDING`);
    setElText('nav-vip-badge', pendingVips.length);
    setElText('stat-vip-approved-count', approvedVips.length);
    setElText('stat-vip-total-count', vipData.length);

    const vipFilterAll = document.querySelector('#section-vip .filter-tab[data-filter="all"]');
    if (vipFilterAll) vipFilterAll.innerHTML = `All History <span style="opacity:0.8;font-size:11px;margin-left:4px">(${vipData.length})</span>`;
    const vipFilterPending = document.querySelector('#section-vip .filter-tab[data-filter="Pending"]');
    if (vipFilterPending) vipFilterPending.innerHTML = `Pending <span style="background:rgba(255,215,0,0.25);color:#ffd700;padding:1px 6px;border-radius:10px;font-size:11px;margin-left:4px">${pendingVips.length}</span>`;
    const vipFilterCompleted = document.querySelector('#section-vip .filter-tab[data-filter="Completed"]');
    if (vipFilterCompleted) vipFilterCompleted.innerHTML = `Approved VIPs <span style="background:rgba(0,230,118,0.2);color:#00e676;padding:1px 6px;border-radius:10px;font-size:11px;margin-left:4px">${approvedVips.length}</span>`;

    let totalVipRev = 0;
    approvedVips.forEach(v => { totalVipRev += parseFloat(v.amount) || 0; });
    setElText('stat-vip-revenue', `₹${totalVipRev.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);

    // Real-Time Notification Triggers on New Incoming Requests
    if (!isFirstLoad) {
      if (pendingVips.length > lastPendingVipCount) {
        const latestVip = pendingVips[0] || {};
        const u = latestVip.username || 'Player';
        const tier = latestVip.tier || 'VIP';
        showWhatsAppNotification({
          type: 'vip',
          title: `👑 New VIP Request: ${tier}`,
          subtitle: `@${u} requested upgrade • Tap to review`,
          targetTab: 'vip'
        });
      } else if (pendingDeps.length > lastPendingDepCount) {
        const latestDep = pendingDeps[0] || {};
        const amt = latestDep.amount ? `₹${parseFloat(latestDep.amount).toLocaleString('en-IN', {minimumFractionDigits: 2})}` : 'New Amount';
        const u = latestDep.username || 'Player';
        const utr = latestDep.utr || 'Proof Attached';
        showWhatsAppNotification({
          type: 'deposit',
          title: `💰 New Deposit: ${amt}`,
          subtitle: `From @${u} • UTR: ${utr} • Tap to approve`,
          targetTab: 'deposits'
        });
      } else if (pendingWths.length > lastPendingWthCount) {
        const latestWth = pendingWths[0] || {};
        const amt = latestWth.amount ? `₹${parseFloat(latestWth.amount).toLocaleString('en-IN', {minimumFractionDigits: 2})}` : 'New Amount';
        const u = latestWth.username || 'Player';
        const upi = latestWth.accountNo || latestWth.upiId || 'UPI';
        showWhatsAppNotification({
          type: 'withdraw',
          title: `📤 New Withdrawal: ${amt}`,
          subtitle: `Payout to @${u} (${upi}) • Tap to process`,
          targetTab: 'withdrawals'
        });
      }
    }

    isFirstLoad = false;
    lastPendingDepCount = pendingDeps.length;
    lastPendingWthCount = pendingWths.length;
    lastPendingVipCount = pendingVips.length;
  }

  function setElText(id, text) {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  }

  // ── 4. RENDER DEPOSITS TABLE ─────────────────────────────────
  window.setDepositFilter = function(filter, btn) {
    currentDepositFilter = filter;
    document.querySelectorAll('#section-deposits .filter-tab').forEach(t => t.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderDepositsTable();
  };

  function renderDepositsTable() {
    const tbody = document.getElementById('deposits-tbody');
    if (!tbody) return;

    let list = depositsData;
    if (currentDepositFilter !== 'all') {
      list = depositsData.filter(d => d.status === currentDepositFilter);
    }

    if (list.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" class="empty-state">
            <div class="empty-icon">📂</div>
            <p>No deposit requests found in <strong>${currentDepositFilter.toUpperCase()}</strong> tab.</p>
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = list.map(d => {
      const isPending = d.status === 'Pending';
      const isCompleted = d.status === 'Completed';
      const isUsdt = d.wallet === 'usdt' || d.currency === 'USDT';
      const baseAmt = parseFloat(d.amount || 0);
      let bonusAmt = parseFloat(d.bonusAmount || 0);
      
      // Auto compute 100% bonus for GG1675 if not set
      if (bonusAmt <= 0 && d.coupon) {
        if (String(d.coupon).toUpperCase().trim() === 'GG1675' && baseAmt >= 1675) {
          const pct = Math.min(1.0, baseAmt >= 5000 ? 1.0 : (0.5 + ((baseAmt - 1675) / (5000 - 1675)) * 0.5));
          bonusAmt = Math.round(baseAmt * pct * 100) / 100;
        } else if (String(d.coupon).toUpperCase().trim() === 'INSTANT1500' && baseAmt >= 2500) {
          bonusAmt = 1500.0;
        }
      }

      const totalCredit = parseFloat(d.creditedAmount || (baseAmt + bonusAmt));
      const hasBonus = bonusAmt > 0 || !!d.coupon;

      const amtFormatted = isUsdt 
        ? `${baseAmt.toFixed(2)} ₮` 
        : `₹${baseAmt.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

      const dateStr = d.timestamp ? new Date(d.timestamp).toLocaleString('en-IN') : 'Just now';
      const orderNum = d.orderId || d.id || 'DEP-' + Math.floor(Math.random()*90000);

      const statusBadge = isPending 
        ? `<span class="badge-status status-pending"><span class="pulse-dot"></span>Pending Approval</span>`
        : isCompleted 
        ? `<span class="badge-status status-completed">✓ Approved</span>`
        : `<span class="badge-status status-rejected">✕ Rejected</span>`;

      let actions = '-';
      if (isPending) {
        actions = `
          <div class="action-group">
            <button class="btn-approve" onclick="approveDeposit('${d.id}')">✓ Approve &amp; Credit (₹${totalCredit.toLocaleString('en-IN')})</button>
            <button class="btn-reject" onclick="rejectDeposit('${d.id}')">✕ Reject</button>
          </div>
        `;
      }

      return `
        <tr>
          <td>
            <div style="display:flex;align-items:center;gap:6px">
              <span class="tx-id">${orderNum}</span>
              <button class="btn-copy-mini" onclick="copyText('${orderNum}', this)">Copy</button>
            </div>
          </td>
          <td><strong>${d.username || 'Player'}</strong></td>
          <td><span class="wallet-badge ${isUsdt ? 'usdt' : 'real'}">${isUsdt ? 'USDT TRC20' : 'Real INR'}</span></td>
          <td class="tx-amount ${isUsdt ? 'usdt' : 'inr'}">
            <div style="font-weight:800">${amtFormatted}</div>
            ${hasBonus ? `
              <div style="font-size:11px;color:#00e676;font-weight:800;margin-top:2px">
                🎟️ ${d.coupon || '100% Promo'}: +₹${bonusAmt.toLocaleString('en-IN', {minimumFractionDigits:2})}
              </div>
              <div style="font-size:11.5px;color:#ffd700;font-weight:900;margin-top:1px">
                Total Credit: ₹${totalCredit.toLocaleString('en-IN', {minimumFractionDigits:2})}
              </div>
            ` : ''}
          </td>
          <td>
            <div style="font-weight:700">${d.method || 'UPI / QR Code'}</div>
            ${d.qrNumber ? `
              <div style="margin-top:4px;display:inline-flex;align-items:center;gap:4px;background:rgba(124,77,255,0.18);border:1px solid #7c4dff;border-radius:4px;padding:2px 6px;font-size:10.5px;color:#c084fc;font-weight:800">
                🎯 QR ${d.qrNumber} (${d.qrTarget || (d.qrNumber===1?'amdasrarbasha-1@oksbi':d.qrNumber===2?'kabilanr2210@okhdfcbank':'txchem@slc')})
              </div>
            ` : ''}
          </td>
          <td>
            <div style="display:flex;align-items:center;gap:6px">
              <span class="utr-code">${d.utr || 'N/A'}</span>
              ${d.utr ? `<button class="btn-copy-mini" onclick="copyText('${d.utr}', this)">Copy</button>` : ''}
            </div>
          </td>
          <td style="color:#94a3b8;font-size:12px">${dateStr}</td>
          <td>${statusBadge}</td>
          <td>${actions}</td>
        </tr>
      `;
    }).join('');
  }

  // ── 5. RENDER WITHDRAWALS TABLE ──────────────────────────────
  window.setWithdrawFilter = function(filter, btn) {
    currentWithdrawFilter = filter;
    document.querySelectorAll('#section-withdrawals .filter-tab').forEach(t => t.classList.remove('active'));
    if (btn) btn.classList.add('active');
    renderWithdrawalsTable();
  };

  function renderWithdrawalsTable() {
    const tbody = document.getElementById('withdrawals-tbody');
    if (!tbody) return;

    let list = withdrawalsData;
    if (currentWithdrawFilter !== 'all') {
      list = withdrawalsData.filter(w => w.status === currentWithdrawFilter);
    }

    if (list.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="9" class="empty-state">
            <div class="empty-icon">📂</div>
            <p>No withdrawal requests found in <strong>${currentWithdrawFilter.toUpperCase()}</strong> tab.</p>
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = list.map(w => {
      const isPending = w.status === 'Pending';
      const isCompleted = w.status === 'Completed';
      const isUsdt = w.wallet === 'usdt' || w.currency === 'USDT';
      const amtFormatted = isUsdt 
        ? `${parseFloat(w.amount).toFixed(2)} ₮` 
        : `₹${parseFloat(w.amount).toLocaleString('en-IN', {minimumFractionDigits: 2})}`;

      const dateStr = w.timestamp ? new Date(w.timestamp).toLocaleString('en-IN') : 'Just now';
      const orderNum = w.orderId || w.id || 'WTH-' + Math.floor(Math.random()*90000);

      const statusBadge = isPending 
        ? `<span class="badge-status status-pending"><span class="pulse-dot"></span>Pending Transfer</span>`
        : isCompleted 
        ? `<span class="badge-status status-completed">✓ Paid Out</span>`
        : `<span class="badge-status status-rejected">✕ Rejected</span>`;

      let bankHtml = '';
      if (!isUsdt) {
        bankHtml = `
          <div class="bank-info-box">
            <div class="bank-row"><span class="bank-lbl">Bank:</span><span class="bank-val">${w.bankName || 'Bank'}</span></div>
            <div class="bank-row"><span class="bank-lbl">A/C:</span><span class="bank-val">${w.accountNo || 'N/A'}</span></div>
            <div class="bank-row"><span class="bank-lbl">IFSC:</span><span class="bank-val">${w.ifsc || 'N/A'}</span></div>
          </div>
        `;
      } else {
        bankHtml = `<div class="bank-info-box"><div class="bank-row"><span class="bank-lbl">USDT TRC20:</span><span class="bank-val">${(w.address||'').slice(0,14)}...</span></div></div>`;
      }

      let actions = '-';
      if (isPending) {
        actions = `
          <div class="action-group">
            <button class="btn-approve" onclick="approveWithdrawal('${w.id}')">✓ Mark as Paid</button>
            <button class="btn-reject" onclick="rejectWithdrawal('${w.id}')">✕ Reject &amp; Refund</button>
          </div>
        `;
      }

      return `
        <tr>
          <td><span class="tx-id" style="color:#38bdf8">${orderNum}</span></td>
          <td><strong>${w.name || w.username || 'Player'}</strong></td>
          <td class="tx-amount ${isUsdt ? 'usdt' : 'inr'}">${amtFormatted}</td>
          <td>${bankHtml}</td>
          <td>${w.mobile || 'N/A'}</td>
          <td>${w.method || 'IMPS Bank Transfer'}</td>
          <td style="color:#94a3b8;font-size:12px">${dateStr}</td>
          <td>${statusBadge}</td>
          <td>${actions}</td>
        </tr>
      `;
    }).join('');
  }

  // ── 6. RENDER VIP CLUB TABLE ─────────────────────────────────
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
            <p>No VIP applications found in <strong>${currentVipFilter.toUpperCase()}</strong> tab.</p>
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = filtered.map(v => {
      const isPending = v.status === 'Pending';
      const isCompleted = v.status === 'Completed';
      const statusBadge = isPending
        ? `<span class="badge-status status-pending" style="background:rgba(255,215,0,0.15);color:#ffd700;border:1px solid #ffd700"><span class="pulse-dot" style="background:#ffd700"></span>Pending Host Approval</span>`
        : isCompleted
        ? `<span class="badge-status status-completed">👑 Approved &amp; Active</span>`
        : `<span class="badge-status status-rejected">❌ Rejected</span>`;

      const dateStr = v.timestamp ? new Date(v.timestamp).toLocaleString('en-IN') : 'Just now';
      const orderNum = v.orderId || v.id || 'ORD-VIP-' + Math.floor(Math.random()*900000);

      let actions = `<span style="font-size:12px;color:#64748b">${isCompleted ? '👑 Active VIP' : 'Rejected'}</span>`;
      if (isPending) {
        actions = `
          <div class="action-group">
            <button class="btn-approve-vip" onclick="approveVipRequest('${v.id}')" title="Approve VIP & Activate Glowing Badge">
              👑 Approve VIP
            </button>
            <button class="btn-reject" onclick="rejectVipRequest('${v.id}')" title="Reject Application">
              ✕ Reject
            </button>
          </div>
        `;
      }

      return `
        <tr class="${isPending ? 'pending-row' : ''}">
          <td>
            <div style="display:flex;align-items:center;gap:6px">
              <span class="tx-id" style="color:#ffd700;font-weight:900">${orderNum}</span>
              <button class="btn-copy-mini" onclick="copyText('${orderNum}', this)">Copy</button>
            </div>
          </td>
          <td><strong>${v.username || 'Player'}</strong></td>
          <td>
            <span style="background:rgba(255,215,0,0.15);border:1px solid #ffd700;color:#ffd700;font-weight:800;padding:2px 8px;border-radius:999px;font-size:11.5px">
              👑 ${v.tierName || 'Gold VIP (1 Month)'}
            </span>
          </td>
          <td class="tx-amount inr">₹${parseFloat(v.amount||0).toLocaleString('en-IN', {minimumFractionDigits: 2})}</td>
          <td>${v.method || 'UPI Instant QR'}</td>
          <td>
            <div style="display:flex;align-items:center;gap:6px">
              <span class="utr-code" style="font-family:monospace;font-size:13px;font-weight:800;color:#00e676">${v.utr || 'N/A'}</span>
              ${v.utr ? `<button class="btn-copy-mini" onclick="copyText('${v.utr}', this)">Copy</button>` : ''}
            </div>
          </td>
          <td style="font-size:12px;color:#94a3b8">${dateStr}</td>
          <td>${statusBadge}</td>
          <td>${actions}</td>
        </tr>
      `;
    }).join('');
  }

  // ── 7. APPROVAL ACTIONS (PERMANENT HISTORY PRESERVED) ───────
  window.approveDeposit = async function(id) {
    if (!confirm(`Are you sure you want to APPROVE deposit ${id} and credit user balance?`)) return;
    try {
      const target = depositsData.find(d => d.id === id || d.orderId === id);
      if (target) {
        target.status = 'Completed';
        target.approvedAt = Date.now();
        renderDepositsTable();
        updateAllStats();
      }

      const res = await fetch('/api/approve-deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`✅ Deposit ${id} APPROVED & Recorded in History!`, '#00e676');
      }
    } catch (e) { console.warn(e); }
  };

  window.rejectDeposit = async function(id) {
    if (!confirm(`Are you sure you want to REJECT deposit ${id}?`)) return;
    try {
      const target = depositsData.find(d => d.id === id || d.orderId === id);
      if (target) {
        target.status = 'Rejected';
        target.rejectedAt = Date.now();
        renderDepositsTable();
        updateAllStats();
      }

      const res = await fetch('/api/reject-deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`❌ Deposit ${id} Rejected & Saved to History.`, '#ef4444');
      }
    } catch (e) { console.warn(e); }
  };

  window.approveWithdrawal = async function(id) {
    if (!confirm(`Mark withdrawal ${id} as PAID?`)) return;
    try {
      const target = withdrawalsData.find(w => w.id === id || w.orderId === id);
      if (target) {
        target.status = 'Completed';
        target.approvedAt = Date.now();
        renderWithdrawalsTable();
        updateAllStats();
      }

      const res = await fetch('/api/approve-withdrawal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`✅ Withdrawal ${id} marked as PAID & Recorded in History!`, '#38bdf8');
      }
    } catch (e) { console.warn(e); }
  };

  window.rejectWithdrawal = async function(id) {
    if (!confirm(`Reject withdrawal ${id} and REFUND balance to user?`)) return;
    try {
      const target = withdrawalsData.find(w => w.id === id || w.orderId === id);
      if (target) {
        target.status = 'Rejected';
        target.rejectedAt = Date.now();
        renderWithdrawalsTable();
        updateAllStats();
      }

      const res = await fetch('/api/reject-withdrawal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`⚠️ Withdrawal ${id} Rejected, Refunded & Logged.`, '#f59e0b');
      }
    } catch (e) { console.warn(e); }
  };

  window.approveVipRequest = async function(id) {
    const target = vipData.find(v => v.id === id || v.orderId === id);
    const username = target ? target.username : 'User';
    const tier = target ? target.tierName : 'Gold VIP';

    if (!confirm(`👑 Approve VIP Upgrade for ${username} to ${tier}? This will instantly grant their Glowing VIP Badge and unlock the VIP Members Lounge for 1 Month (30 Days)!`)) return;

    try {
      if (target) {
        target.status = 'Completed';
        target.approvedAt = Date.now();
        renderVipTable();
        updateAllStats();
      }

      const res = await fetch('/api/approve-vip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      const data = await res.json();
      if (data.success) {
        fetchAllData();
        showNotification(`👑 VIP UPGRADE APPROVED FOR ${username.toUpperCase()}! Logged in VIP History.`, '#ffd700');
      } else {
        alert(data.message || 'Approval failed');
      }
    } catch(e) { console.warn(e); }
  };

  window.rejectVipRequest = async function(id) {
    if (!confirm(`Reject VIP upgrade application ${id}?`)) return;
    try {
      const target = vipData.find(v => v.id === id || v.orderId === id);
      if (target) {
        target.status = 'Rejected';
        target.rejectedAt = Date.now();
        renderVipTable();
        updateAllStats();
      }

      const res = await fetch('/api/reject-vip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`VIP request rejected & Logged.`, '#ef4444');
      }
    } catch(e) { console.warn(e); }
  };

  // ── 8. UTILITIES & NOTIFICATION AUDIO ────────────────────────
  window.copyText = function(text, btn) {
    navigator.clipboard.writeText(text).then(() => {
      const old = btn.textContent;
      btn.textContent = 'Copied! ✓';
      setTimeout(() => btn.textContent = old, 1500);
    });
  };

  function showNotification(msg, color = '#00e676') {
    const alertDiv = document.createElement('div');
    alertDiv.style.cssText = `
      position: fixed; bottom: 24px; right: 24px;
      background: #111827; border: 2px solid ${color};
      color: #fff; padding: 14px 20px; border-radius: 12px;
      box-shadow: 0 10px 40px rgba(0,0,0,0.8), 0 0 25px ${color}44;
      z-index: 99999; font-weight: 800; font-size: 13.5px;
      display: flex; align-items: center; gap: 10px;
      animation: modalSlideUp 0.3s ease;
    `;
    alertDiv.textContent = msg;
    document.body.appendChild(alertDiv);
    setTimeout(() => alertDiv.remove(), 4500);
  }

  function playAlertTone() {
    try {
      const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      // WhatsApp signature chime (800Hz followed by 1050Hz)
      const osc1 = audioCtx.createOscillator();
      const gain1 = audioCtx.createGain();
      osc1.type = 'sine';
      osc1.frequency.setValueAtTime(800, audioCtx.currentTime);
      gain1.gain.setValueAtTime(0.35, audioCtx.currentTime);
      gain1.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.10);
      osc1.connect(gain1);
      gain1.connect(audioCtx.destination);
      osc1.start();
      osc1.stop(audioCtx.currentTime + 0.10);

      const osc2 = audioCtx.createOscillator();
      const gain2 = audioCtx.createGain();
      osc2.type = 'sine';
      osc2.frequency.setValueAtTime(1050, audioCtx.currentTime + 0.12);
      gain2.gain.setValueAtTime(0.40, audioCtx.currentTime + 0.12);
      gain2.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.38);
      osc2.connect(gain2);
      gain2.connect(audioCtx.destination);
      osc2.start(audioCtx.currentTime + 0.12);
      osc2.stop(audioCtx.currentTime + 0.38);
    } catch (e) {}
  }

  function showWhatsAppNotification(data) {
    const { type, title, subtitle, targetTab } = data;
    playAlertTone();

    // 1. Android Native System Notification (heads-up status bar alert like WhatsApp)
    if (window.AndroidBridge && typeof window.AndroidBridge.notifyAdmin === 'function') {
      window.AndroidBridge.notifyAdmin(title, subtitle, type);
    }

    // 2. Browser Web Notification API
    if ('Notification' in window && Notification.permission === 'granted') {
      try {
        new Notification(title, {
          body: subtitle,
          icon: '/download/ggwins.apk'
        });
      } catch(e) {}
    }

    // 3. Floating in-app WhatsApp notification card
    const container = document.getElementById('whatsapp-toast-container');
    if (container) {
      const card = document.createElement('div');
      card.className = 'whatsapp-card';
      card.style.cursor = 'pointer';
      
      const iconEmoji = type === 'deposit' ? '💰' : (type === 'withdraw' ? '📤' : '👑');

      card.innerHTML = `
        <div style="display:flex;align-items:center;justify-content:space-between">
          <div style="display:flex;align-items:center;gap:7px">
            <span style="font-size:16px">💬</span>
            <span style="font-size:11.5px;font-weight:900;color:#25D366;text-transform:uppercase;letter-spacing:0.5px">WHATSAPP ALERT • GG WINS</span>
          </div>
          <button onclick="event.stopPropagation(); this.closest('.whatsapp-card').remove()" style="background:none;border:none;color:#94a3b8;font-size:16px;cursor:pointer;line-height:1">✕</button>
        </div>
        <div style="display:flex;align-items:center;gap:12px;margin-top:2px">
          <div style="width:40px;height:40px;border-radius:50%;background:radial-gradient(circle,#25D366,#128C7E);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0;box-shadow:0 0 15px rgba(37,211,102,0.4)">
            ${iconEmoji}
          </div>
          <div style="flex:1;text-align:left">
            <div style="font-size:13.5px;font-weight:800;color:#fff">${title}</div>
            <div style="font-size:12px;color:#cbd5e1;margin-top:2px">${subtitle}</div>
          </div>
          <button style="padding:6px 12px;background:#25D366;color:#000;border:none;border-radius:8px;font-weight:900;font-size:11.5px;cursor:pointer;flex-shrink:0;box-shadow:0 2px 10px rgba(37,211,102,0.4)">OPEN</button>
        </div>
      `;

      card.onclick = () => {
        if (typeof switchMainTab === 'function') switchMainTab(targetTab);
        card.remove();
      };

      container.appendChild(card);
      setTimeout(() => {
        card.classList.add('closing');
        setTimeout(() => card.remove(), 320);
      }, 7500);
    }
  }

  window.clearAllData = async function() {
    if (!confirm('Clear all old/test records and reset to clean state?')) return;
    try {
      const res = await fetch('/api/clear-data', { method: 'POST' });
      if (res.ok) {
        depositsData = [];
        withdrawalsData = [];
        vipData = [];
        fetchAllData();
        showNotification('🗑️ All history cleared! Admin terminal reset.', '#ef4444');
      }
    } catch(e) {}
  };

  // ── 8.5. ADMIN TERMINAL AUTHENTICATION & LOCK CONTROLS ─────
  const ALLOWED_ADMINS = {
    "ASRAR admin": "ArCot.co.in",
    "ASRAR": "ArCot.co.in",
    "KABILAN": "ValENtino",
    "REHAN": "QuResHi"
  };

  window.submitAdminLogin = function() {
    const userInp = document.getElementById('admin-lock-user');
    const passInp = document.getElementById('admin-lock-pass');
    const errBox = document.getElementById('admin-lock-error');

    const uRaw = (userInp?.value || '').trim();
    const p = (passInp?.value || '').trim();

    if (!uRaw || !p) {
      if (errBox) {
        errBox.textContent = '⚠️ Please enter both Admin Username and Master Passkey.';
        errBox.style.display = 'block';
      }
      return;
    }

    // Match exact or normalized username
    let matchedUser = null;
    for (const adminKey in ALLOWED_ADMINS) {
      if (adminKey.toLowerCase() === uRaw.toLowerCase() && ALLOWED_ADMINS[adminKey] === p) {
        matchedUser = adminKey;
        break;
      }
    }

    if (matchedUser) {
      // ⚡ INSTANT UNLOCK (0ms delay)
      if (errBox) errBox.style.display = 'none';
      const authSession = { username: matchedUser, loggedInAt: Date.now() };
      sessionStorage.setItem('ggwins_admin_auth', JSON.stringify(authSession));
      localStorage.setItem('ggwins_admin_auth', JSON.stringify(authSession));

      unlockAdminUI(matchedUser);
      showNotification(`👋 Welcome, Authorized Admin ${matchedUser}! Terminal Unlocked.`, '#00e676');

      // Async backend log (non-blocking)
      try {
        fetch('/api/admin/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: matchedUser, password: p })
        }).catch(()=>{});
      } catch(e){}
    } else {
      if (errBox) {
        errBox.textContent = '❌ Access Denied: Invalid Admin Username or Master Passkey.';
        errBox.style.display = 'block';
      }
      if (passInp) passInp.value = '';
    }
  };

  window.logoutAdmin = function() {
    sessionStorage.removeItem('ggwins_admin_auth');
    localStorage.removeItem('ggwins_admin_auth');
    lockAdminUI();
  };

  function unlockAdminUI(adminName) {
    const lockOverlay = document.getElementById('admin-lock-overlay');
    const mainWrapper = document.getElementById('admin-main-wrapper');
    const badge = document.getElementById('active-admin-badge');

    if (lockOverlay) lockOverlay.style.display = 'none';
    if (mainWrapper) mainWrapper.style.display = 'flex';
    if (badge) badge.textContent = '👑 ' + (adminName || 'Admin');

    fetchAllData();
  }

  function lockAdminUI() {
    const lockOverlay = document.getElementById('admin-lock-overlay');
    const mainWrapper = document.getElementById('admin-main-wrapper');
    const passInp = document.getElementById('admin-lock-pass');
    const errBox = document.getElementById('admin-lock-error');

    if (mainWrapper) mainWrapper.style.display = 'none';
    if (lockOverlay) lockOverlay.style.display = 'flex';
    if (passInp) passInp.value = '';
    if (errBox) errBox.style.display = 'none';
  }

  function checkAdminSession() {
    try {
      const auth = JSON.parse(sessionStorage.getItem('ggwins_admin_auth') || localStorage.getItem('ggwins_admin_auth') || 'null');
      if (auth && auth.username && ALLOWED_ADMINS[auth.username]) {
        unlockAdminUI(auth.username);
        return true;
      }
    } catch(e){}
    lockAdminUI();
    return false;
  }

  // ── 8B. USER WALLET & AUDIT SUITE ──────────────────────────
  let activeSelectedUserId = null;
  let allUsersData = [];

  window.closeUserInspector = function() {
    activeSelectedUserId = null;
    const card = document.getElementById('user-details-card');
    if (card) card.style.display = 'none';
    const searchInp = document.getElementById('user-wallet-search-input');
    if (searchInp) {
      searchInp.value = '';
      searchInp.focus();
    }
    const dirPanel = document.getElementById('all-users-directory-panel');
    if (dirPanel) {
      dirPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
    showNotification('👋 Closed user profile inspector.', '#94a3b8');
  };

  window.switchUserSubTab = function(subTab) {
    const gameBtn = document.getElementById('user-subtab-game');
    const payBtn = document.getElementById('user-subtab-pay');
    const refBtn = document.getElementById('user-subtab-ref');
    const gameView = document.getElementById('user-game-history-view');
    const payView = document.getElementById('user-payment-history-view');
    const refView = document.getElementById('user-referral-history-view');

    if (subTab === 'game') {
      if (gameBtn) gameBtn.classList.add('active');
      if (payBtn) payBtn.classList.remove('active');
      if (refBtn) refBtn.classList.remove('active');
      if (gameView) gameView.style.display = 'block';
      if (payView) payView.style.display = 'none';
      if (refView) refView.style.display = 'none';
    } else if (subTab === 'pay') {
      if (gameBtn) gameBtn.classList.remove('active');
      if (payBtn) payBtn.classList.add('active');
      if (refBtn) refBtn.classList.remove('active');
      if (gameView) gameView.style.display = 'none';
      if (payView) payView.style.display = 'block';
      if (refView) refView.style.display = 'none';
    } else if (subTab === 'ref') {
      if (gameBtn) gameBtn.classList.remove('active');
      if (payBtn) payBtn.classList.remove('active');
      if (refBtn) refBtn.classList.add('active');
      if (gameView) gameView.style.display = 'none';
      if (payView) payView.style.display = 'none';
      if (refView) refView.style.display = 'block';
    }
  };

  window.searchUserWallet = async function(queryParam) {
    let inputVal = (queryParam || (document.getElementById('user-wallet-search-input')?.value || '')).trim();
    // Strip quotes or hashes/at symbols if pasted
    inputVal = inputVal.replace(/^["']|["']$/g, '').replace(/^[#@]/, '').trim();

    if (!inputVal) {
      alert('Please enter a User ID, Username, or Email to search.');
      return;
    }

    try {
      showNotification('🔍 Searching player records...', '#38bdf8');
      const res = await fetch(`/api/admin/user-details?userId=${encodeURIComponent(inputVal)}&username=${encodeURIComponent(inputVal)}`);
      const data = await res.json();

      if (!res.ok || !data.success || !data.user) {
        alert(`❌ No user found matching "${inputVal}". Please check the User ID or Username.`);
        return;
      }

      displayUserDetails(data);
      loadAllUsersDirectory();
      showNotification(`✅ Loaded profile for @${data.user.username} (${data.user.id})`, '#00e676');
    } catch(e) {
      console.error(e);
      alert('Error connecting to server to search user.');
    }
  };

  function displayUserDetails(data) {
    const u = data.user;
    activeSelectedUserId = u.id;

    const detailsCard = document.getElementById('user-details-card');
    if (detailsCard) detailsCard.style.display = 'block';

    // Header Details
    setElText('u-avatar', u.avatar || '👑');
    setElText('u-username', u.username || 'Player');
    setElText('u-vip-badge', u.vipLevel && u.vipLevel !== 'None' ? `👑 ${u.vipLevel} VIP` : 'Standard Member');
    setElText('u-id', u.id || 'USER-N/A');
    setElText('u-referral-code', u.referralCode || ('GG-' + (u.id ? u.id.replace('USER-', '').substr(0, 6) : 'WIN777')));
    setElText('u-email', u.email || 'N/A');
    setElText('u-created-at', u.createdAt ? new Date(u.createdAt).toLocaleString('en-IN') : 'N/A');
    setElText('u-last-login', u.lastLogin ? new Date(u.lastLogin).toLocaleString('en-IN') : 'Just now');

    // Referral Summary
    const stats = u.stats || {};
    const refCount = stats.referralCount || (data.referredUsers ? data.referredUsers.length : 0);
    const refEarnings = stats.referralEarnings || (refCount * 50.0);
    setElText('u-referral-count', refCount);
    setElText('u-referral-earnings', `₹${refEarnings.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
    setElText('user-ref-tab-count', refCount);

    // Wallet Balances
    const w = u.wallets || { demo: 10000, real: 0, bonus: 0, usdt: 0 };
    const realBal = parseFloat(w.real || 0);
    const bonusBal = parseFloat(w.bonus || 0);
    const demoBal = parseFloat(w.demo || 0);
    const usdtBal = parseFloat(w.usdt || 0);

    setElText('current-real-bal-display', `₹${realBal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
    setElText('current-bonus-bal-display', `₹${bonusBal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
    setElText('current-demo-bal-display', `₹${demoBal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
    setElText('current-usdt-bal-display', `${usdtBal.toFixed(2)} ₮`);

    const editReal = document.getElementById('edit-real-bal');
    const editBonus = document.getElementById('edit-bonus-bal');
    const editDemo = document.getElementById('edit-demo-bal');
    const editUsdt = document.getElementById('edit-usdt-bal');
    if (editReal) editReal.value = realBal.toFixed(2);
    if (editBonus) editBonus.value = bonusBal.toFixed(2);
    if (editDemo) editDemo.value = demoBal.toFixed(2);
    if (editUsdt) editUsdt.value = usdtBal.toFixed(2);

    if (typeof updateLiveAdjustmentPreview === 'function') {
      updateLiveAdjustmentPreview();
    }

    // Game History
    const games = data.gameWagers || [];
    setElText('user-games-count', games.length);
    renderUserGamesTable(games);

    // Payment & Transaction History
    const txs = (data.transactions && data.transactions.length > 0) ? data.transactions : (data.deposits || []).concat(data.withdrawals || []);
    setElText('user-txs-count', txs.length);
    renderUserPaymentsTable(txs);

    // Referral Network Roster
    renderUserReferralsTable(data.referredUsers || []);

    // Scroll to user details smoothly
    detailsCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  function renderUserReferralsTable(referredUsers) {
    const tbody = document.getElementById('user-referrals-tbody');
    if (!tbody) return;

    if (!referredUsers || referredUsers.length === 0) {
      tbody.innerHTML = `<tr><td colspan="7" class="empty-state"><p>No players have used this user's referral code yet.</p></td></tr>`;
      return;
    }

    tbody.innerHTML = referredUsers.map((r, idx) => {
      const regDate = r.createdAt ? new Date(r.createdAt).toLocaleString('en-IN') : 'N/A';
      return `
        <tr>
          <td><span style="color:#64748b;font-weight:700">#${idx + 1}</span></td>
          <td>
            <div style="display:flex;align-items:center;gap:6px">
              <code style="color:#00e676;font-family:monospace;font-weight:800">${r.id || 'USER-N/A'}</code>
              <button class="btn-copy-mini" onclick="copyText('${r.id}', this)">Copy</button>
            </div>
          </td>
          <td><strong>👑 @${r.username || 'Player'}</strong></td>
          <td style="color:#cbd5e1">${r.email || '-'}</td>
          <td style="color:#94a3b8;font-size:12px">${regDate}</td>
          <td>
            <span class="badge-status status-completed" style="background:rgba(0,230,118,0.15);border:1px solid #00e676;color:#00e676;font-weight:800">
              +₹50.00 Real Cash
            </span>
          </td>
          <td>
            <button class="btn btn-primary" style="padding:4px 10px;font-size:11px;background:linear-gradient(135deg,#00e676,#00b0ff);color:#000;border:none;border-radius:6px;font-weight:800;cursor:pointer" onclick="searchUserWallet('${r.id}')">
              🔍 Inspect Player
            </button>
          </td>
        </tr>
      `;
    }).join('');
  }

  let currentWalletOperationMode = 'add'; // 'add' or 'deduct'

  window.setWalletOperationMode = function(mode) {
    currentWalletOperationMode = mode === 'deduct' ? 'deduct' : 'add';
    const btnAdd = document.getElementById('btn-mode-add');
    const btnDeduct = document.getElementById('btn-mode-deduct');
    const lblAmount = document.getElementById('lbl-action-amount');
    const btnExec = document.getElementById('btn-execute-action');
    const amountInput = document.getElementById('action-amount-input');
    const targetSelect = document.getElementById('wallet-action-target');
    const targetW = targetSelect ? targetSelect.value : 'real';
    const currSym = targetW === 'usdt' ? '₮' : '₹';

    if (currentWalletOperationMode === 'add') {
      if (btnAdd) {
        btnAdd.style.background = 'linear-gradient(135deg,#00e676,#00b0ff)';
        btnAdd.style.color = '#000';
      }
      if (btnDeduct) {
        btnDeduct.style.background = 'transparent';
        btnDeduct.style.color = '#94a3b8';
      }
      if (lblAmount) lblAmount.textContent = `Amount to Add (${currSym}):`;
      if (btnExec) {
        btnExec.style.background = 'linear-gradient(135deg,#00e676,#00b0ff)';
        btnExec.style.color = '#000';
        btnExec.textContent = `➕ Add Funds to User Wallet`;
      }
      if (amountInput) amountInput.style.borderColor = '#00e676';
    } else {
      if (btnDeduct) {
        btnDeduct.style.background = 'linear-gradient(135deg,#ef4444,#dc2626)';
        btnDeduct.style.color = '#fff';
      }
      if (btnAdd) {
        btnAdd.style.background = 'transparent';
        btnAdd.style.color = '#94a3b8';
      }
      if (lblAmount) lblAmount.textContent = `Amount to Deduct (${currSym}):`;
      if (btnExec) {
        btnExec.style.background = 'linear-gradient(135deg,#ef4444,#dc2626)';
        btnExec.style.color = '#fff';
        btnExec.textContent = `➖ Deduct Funds from User Wallet`;
      }
      if (amountInput) amountInput.style.borderColor = '#ef4444';
    }

    updateLiveAdjustmentPreview();
  };

  window.applyQuickAmount = function(amt) {
    const input = document.getElementById('action-amount-input');
    if (input) {
      input.value = amt;
      updateLiveAdjustmentPreview();
    }
  };

  window.updateLiveAdjustmentPreview = function() {
    const targetSelect = document.getElementById('wallet-action-target');
    const amountInput = document.getElementById('action-amount-input');
    const previewText = document.getElementById('action-preview-text');
    const previewPill = document.getElementById('action-preview-pill');
    const btnExec = document.getElementById('btn-execute-action');

    const targetW = targetSelect ? targetSelect.value : 'real';
    const currSym = targetW === 'usdt' ? '₮' : '₹';
    const delta = parseFloat(amountInput?.value || 0);

    const editReal = document.getElementById('edit-real-bal');
    const editBonus = document.getElementById('edit-bonus-bal');
    const editDemo = document.getElementById('edit-demo-bal');
    const editUsdt = document.getElementById('edit-usdt-bal');

    let curBal = 0;
    if (targetW === 'real') curBal = parseFloat(editReal?.value || 0);
    else if (targetW === 'bonus') curBal = parseFloat(editBonus?.value || 0);
    else if (targetW === 'demo') curBal = parseFloat(editDemo?.value || 0);
    else if (targetW === 'usdt') curBal = parseFloat(editUsdt?.value || 0);

    let nextBal = curBal;
    if (currentWalletOperationMode === 'add') {
      nextBal = curBal + delta;
    } else {
      nextBal = Math.max(0, curBal - delta);
    }

    if (previewText) {
      previewText.textContent = `${currSym}${curBal.toLocaleString('en-IN', {minimumFractionDigits: 2})} ➔ ${currSym}${nextBal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`;
      previewText.style.color = currentWalletOperationMode === 'add' ? '#00e676' : '#ef4444';
    }
    if (previewPill) {
      previewPill.style.background = currentWalletOperationMode === 'add' ? 'rgba(0,230,118,0.08)' : 'rgba(239,68,68,0.08)';
      previewPill.style.borderColor = currentWalletOperationMode === 'add' ? 'rgba(0,230,118,0.3)' : 'rgba(239,68,68,0.3)';
    }
    if (btnExec && delta > 0) {
      btnExec.textContent = currentWalletOperationMode === 'add' 
        ? `➕ Add ${currSym}${delta.toLocaleString('en-IN')} to ${targetW.toUpperCase()}`
        : `➖ Deduct ${currSym}${delta.toLocaleString('en-IN')} from ${targetW.toUpperCase()}`;
    }
  };

  window.executeWalletAction = async function() {
    if (!activeSelectedUserId) {
      alert('Please search and select a user first.');
      return;
    }

    const targetSelect = document.getElementById('wallet-action-target');
    const amountInput = document.getElementById('action-amount-input');
    const reasonInput = document.getElementById('action-reason-input');

    const targetW = targetSelect ? targetSelect.value : 'real';
    const currSym = targetW === 'usdt' ? '₮' : '₹';
    const delta = parseFloat(amountInput?.value || 0);
    const reason = (reasonInput?.value || '').trim() || (currentWalletOperationMode === 'add' ? 'Admin Deposit Credit' : 'Admin Deduction / Penalty');

    if (isNaN(delta) || delta <= 0) {
      alert('Please enter a valid amount greater than 0.');
      return;
    }

    const editReal = document.getElementById('edit-real-bal');
    const editBonus = document.getElementById('edit-bonus-bal');
    const editDemo = document.getElementById('edit-demo-bal');
    const editUsdt = document.getElementById('edit-usdt-bal');

    let curReal = parseFloat(editReal?.value || 0);
    let curBonus = parseFloat(editBonus?.value || 0);
    let curDemo = parseFloat(editDemo?.value || 0);
    let curUsdt = parseFloat(editUsdt?.value || 0);

    if (targetW === 'real') {
      curReal = currentWalletOperationMode === 'add' ? (curReal + delta) : Math.max(0, curReal - delta);
    } else if (targetW === 'bonus') {
      curBonus = currentWalletOperationMode === 'add' ? (curBonus + delta) : Math.max(0, curBonus - delta);
    } else if (targetW === 'demo') {
      curDemo = currentWalletOperationMode === 'add' ? (curDemo + delta) : Math.max(0, curDemo - delta);
    } else if (targetW === 'usdt') {
      curUsdt = currentWalletOperationMode === 'add' ? (curUsdt + delta) : Math.max(0, curUsdt - delta);
    }

    const actionVerb = currentWalletOperationMode === 'add' ? 'ADD' : 'DEDUCT';
    const confirmMsg = `⚠️ CONFIRM WALLET ${actionVerb}\n\nUser ID: ${activeSelectedUserId}\nAction: ${actionVerb} ${currSym}${delta.toLocaleString('en-IN')}\nAccount: ${targetW.toUpperCase()}\nReason: ${reason}\n\nThis will immediately update the live balance on the user's screen. Proceed?`;

    if (!confirm(confirmMsg)) return;

    try {
      const res = await fetch('/api/admin/update-user-wallet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: activeSelectedUserId,
          real: curReal,
          bonus: curBonus,
          demo: curDemo,
          usdt: curUsdt,
          reason: `${actionVerb}: ${reason}`
        })
      });

      const json = await res.json();
      if (res.ok && json.success) {
        showNotification(json.message || `✅ Successfully ${actionVerb.toLowerCase()}ed ${currSym}${delta.toLocaleString('en-IN')}!`, currentWalletOperationMode === 'add' ? '#00e676' : '#ef4444');
        if (amountInput) amountInput.value = '';
        if (reasonInput) reasonInput.value = '';
        if (editReal) editReal.value = curReal.toFixed(2);
        if (editBonus) editBonus.value = curBonus.toFixed(2);
        if (editDemo) editDemo.value = curDemo.toFixed(2);
        if (editUsdt) editUsdt.value = curUsdt.toFixed(2);

        setElText('current-real-bal-display', `₹${curReal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
        setElText('current-bonus-bal-display', `₹${curBonus.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
        setElText('current-demo-bal-display', `₹${curDemo.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
        setElText('current-usdt-bal-display', `${curUsdt.toFixed(2)} ₮`);
        updateLiveAdjustmentPreview();

        // Reload data
        loadAllUsersDirectory();
        searchUserWallet(activeSelectedUserId);
      } else {
        alert(json.message || 'Failed to execute wallet action.');
      }
    } catch(e) {
      console.error(e);
      alert('Error updating user wallet.');
    }
  };

  window.saveUserWalletBalance = async function() {
    if (!activeSelectedUserId) {
      alert('Please search and select a user first.');
      return;
    }

    const editReal = document.getElementById('edit-real-bal');
    const editBonus = document.getElementById('edit-bonus-bal');
    const editDemo = document.getElementById('edit-demo-bal');
    const editUsdt = document.getElementById('edit-usdt-bal');
    const editReason = document.getElementById('edit-bal-reason');

    const real = parseFloat(editReal?.value || 0);
    const bonus = parseFloat(editBonus?.value || 0);
    const demo = parseFloat(editDemo?.value || 0);
    const usdt = parseFloat(editUsdt?.value || 0);
    const reason = (editReason?.value || '').trim() || 'Admin Direct Adjustment';

    if (isNaN(real) || real < 0) {
      alert('Please enter a valid non-negative Real INR balance.');
      return;
    }

    if (!confirm(`⚠️ CONFIRM WALLET BALANCE UPDATE\n\nUser ID: ${activeSelectedUserId}\nNew Real INR: ₹${real.toLocaleString('en-IN')}\nNew Bonus: ₹${bonus.toLocaleString('en-IN')}\nNew Demo: ₹${demo.toLocaleString('en-IN')}\nNew USDT: ${usdt} ₮\nReason: ${reason}\n\nProceed?`)) {
      return;
    }

    try {
      const res = await fetch('/api/admin/update-user-wallet', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: activeSelectedUserId,
          real: real,
          bonus: bonus,
          demo: demo,
          usdt: usdt,
          reason: reason
        })
      });

      const json = await res.json();
      if (res.ok && json.success) {
        showNotification(json.message || '✅ User balance updated successfully!', '#00e676');
        setElText('current-real-bal-display', `₹${real.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
        setElText('current-demo-bal-display', `₹${demo.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
        setElText('current-usdt-bal-display', `${usdt.toFixed(2)} ₮`);
        if (editReason) editReason.value = '';
        
        // Refresh directory table and user details
        loadAllUsersDirectory();
        searchUserWallet(activeSelectedUserId);
      } else {
        alert(json.message || 'Failed to update balance');
      }
    } catch(e) {
      console.error(e);
      alert('Error updating user wallet.');
    }
  };

  function renderUserGamesTable(games) {
    const tbody = document.getElementById('user-games-tbody');
    if (!tbody) return;

    if (!games || games.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" class="empty-state"><p>No game records found for this player.</p></td></tr>`;
      return;
    }

    tbody.innerHTML = games.map(g => {
      const bet = parseFloat(g.betAmount || g.bet || 0);
      const payout = parseFloat(g.payout || g.win || 0);
      const isWin = g.won !== undefined ? g.won : (payout > bet);
      const profit = payout - bet;
      const dateStr = g.timestamp ? new Date(g.timestamp).toLocaleString('en-IN') : 'Recent';

      return `
        <tr>
          <td><strong style="color:#38bdf8">${g.gameName || g.game || 'GG Game'}</strong></td>
          <td style="font-weight:700">₹${bet.toLocaleString('en-IN', {minimumFractionDigits:2})}</td>
          <td style="font-weight:800;color:${isWin ? '#00e676' : '#94a3b8'}">₹${payout.toLocaleString('en-IN', {minimumFractionDigits:2})}</td>
          <td style="font-weight:900;color:${profit >= 0 ? '#00e676' : '#ef4444'}">
            ${profit >= 0 ? '+' : ''}₹${profit.toLocaleString('en-IN', {minimumFractionDigits:2})}
          </td>
          <td>
            <span class="badge-status ${isWin ? 'status-completed' : 'status-rejected'}">
              ${isWin ? '✓ Won' : '✕ Lost'}
            </span>
          </td>
          <td style="color:#94a3b8;font-size:12px">${dateStr}</td>
        </tr>
      `;
    }).join('');
  }

  function renderUserPaymentsTable(txs) {
    const tbody = document.getElementById('user-payments-tbody');
    if (!tbody) return;

    if (!txs || txs.length === 0) {
      tbody.innerHTML = `<tr><td colspan="8" class="empty-state"><p>No payment records found for this player.</p></td></tr>`;
      return;
    }

    tbody.innerHTML = txs.map(t => {
      const id = t.orderId || t.id || 'TX-N/A';
      const type = (t.type || 'deposit').toUpperCase();
      const amt = parseFloat(t.amount || 0);
      const isCompleted = t.status === 'Completed' || t.status === 'Approved' || t.status === 'PAID';
      const isPending = t.status === 'Pending';
      const dateStr = t.timestamp ? new Date(t.timestamp).toLocaleString('en-IN') : 'Recent';

      const typeBadge = type.includes('DEP') || type === 'DEPOSIT' 
        ? `<span class="wallet-badge real">📥 DEPOSIT</span>`
        : type.includes('WTH') || type === 'WITHDRAWAL'
        ? `<span class="wallet-badge usdt" style="background:rgba(239,68,68,0.15);border-color:#ef4444;color:#ef4444">📤 WITHDRAWAL</span>`
        : `<span class="wallet-badge" style="background:rgba(255,215,0,0.15);border-color:#ffd700;color:#ffd700">⚙️ ${type}</span>`;

      const statusBadge = isPending 
        ? `<span class="badge-status status-pending">Pending</span>`
        : isCompleted 
        ? `<span class="badge-status status-completed">✓ Completed</span>`
        : `<span class="badge-status status-rejected">✕ Rejected</span>`;

      return `
        <tr>
          <td><span class="tx-id">${id}</span></td>
          <td>${typeBadge}</td>
          <td class="tx-amount inr">₹${amt.toLocaleString('en-IN', {minimumFractionDigits:2})}</td>
          <td>${t.method || t.qrLabel || 'UPI Gateway'}</td>
          <td><span class="utr-code">${t.utr || 'N/A'}</span></td>
          <td>${statusBadge}</td>
          <td style="font-size:12px;color:#cbd5e1">${t.description || t.reason || '-'}</td>
          <td style="color:#94a3b8;font-size:12px">${dateStr}</td>
        </tr>
      `;
    }).join('');
  }

  let isUserDirectoryExpanded = false;
  const USER_DIR_COLLAPSED_LIMIT = 5;

  window.toggleUsersDirectoryExpansion = function() {
    isUserDirectoryExpanded = !isUserDirectoryExpanded;
    renderAllUsersTable();
  };

  window.showAllUsersDirectoryExplicit = function() {
    isUserDirectoryExpanded = true;
    renderAllUsersTable();
    const dirPanel = document.getElementById('all-users-directory-panel');
    if (dirPanel) {
      dirPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  window.loadAllUsersDirectory = async function() {
    const tbody = document.getElementById('all-users-tbody');
    if (!tbody) return;

    try {
      const res = await fetch('/api/admin/all-users');
      if (res.ok) {
        const data = await res.json();
        allUsersData = data.users || [];
      }

      // Check local storage for any legacy users that may exist
      try {
        const localUsers = JSON.parse(localStorage.getItem('ggwins_users') || '[]');
        localUsers.forEach(lu => {
          if (!allUsersData.some(u => (u.id && u.id === lu.id) || (u.username && lu.username && u.username.toLowerCase() === lu.username.toLowerCase()))) {
            allUsersData.push({
              id: lu.id || ('USER-' + Math.random().toString(36).substr(2, 8).toUpperCase()),
              username: lu.username || 'Player',
              email: lu.email || '-',
              avatar: lu.avatar || '👑',
              wallets: lu.wallets || { demo: 10000, real: 0, usdt: 0 },
              vipLevel: lu.vipLevel || 'None',
              createdAt: lu.createdAt || Date.now(),
              lastLogin: lu.lastLogin || Date.now()
            });
          }
        });
      } catch(e){}

      setElText('all-users-count', allUsersData.length);
      setElText('nav-users-count', allUsersData.length);
      setElText('stat-total-players-count', allUsersData.length);

      let totalPlayerReal = 0;
      let totalPlayerUsdt = 0;
      let totalVipCount = 0;

      allUsersData.forEach(u => {
        const w = u.wallets || {};
        totalPlayerReal += parseFloat(w.real || 0);
        totalPlayerUsdt += parseFloat(w.usdt || 0);
        if (u.vipLevel && u.vipLevel !== 'None' && u.vipLevel !== 'Standard') {
          totalVipCount++;
        }
      });

      setElText('stat-total-players-real', `₹${totalPlayerReal.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);
      setElText('stat-total-players-usdt', `${totalPlayerUsdt.toFixed(2)} ₮`);
      setElText('stat-total-vip-players', totalVipCount);

      renderAllUsersTable();
    } catch(e) {
      console.error(e);
    }
  };

  function renderAllUsersTable() {
    const tbody = document.getElementById('all-users-tbody');
    const rangeTxt = document.getElementById('showing-users-range-txt');
    const topToggleBtn = document.getElementById('btn-toggle-users-dir-top');
    const bottomBar = document.getElementById('users-dir-bottom-bar');
    const bottomTxt = document.getElementById('btn-toggle-users-dir-bottom-txt');
    if (!tbody) return;

    if (allUsersData.length === 0) {
      tbody.innerHTML = `<tr><td colspan="9" class="empty-state"><p>No registered players on platform yet.</p></td></tr>`;
      if (rangeTxt) rangeTxt.textContent = '0 players';
      if (topToggleBtn) topToggleBtn.style.display = 'none';
      if (bottomBar) bottomBar.style.display = 'none';
      return;
    }

    const total = allUsersData.length;
    let usersToDisplay = allUsersData;

    if (!isUserDirectoryExpanded && total > USER_DIR_COLLAPSED_LIMIT) {
      usersToDisplay = allUsersData.slice(0, USER_DIR_COLLAPSED_LIMIT);
      if (rangeTxt) rangeTxt.textContent = `Showing ${USER_DIR_COLLAPSED_LIMIT} of ${total} players`;
      if (topToggleBtn) {
        topToggleBtn.style.display = 'inline-flex';
        topToggleBtn.innerHTML = `🔽 Show All (${total})`;
      }
      if (bottomBar) bottomBar.style.display = 'block';
      if (bottomTxt) bottomTxt.textContent = `🔽 Show All ${total} Registered Players (+${total - USER_DIR_COLLAPSED_LIMIT} More)`;
    } else {
      if (rangeTxt) rangeTxt.textContent = `Showing all ${total} players`;
      if (topToggleBtn) {
        topToggleBtn.style.display = total > USER_DIR_COLLAPSED_LIMIT ? 'inline-flex' : 'none';
        topToggleBtn.innerHTML = `🔼 Show Less`;
      }
      if (bottomBar) bottomBar.style.display = total > USER_DIR_COLLAPSED_LIMIT ? 'block' : 'none';
      if (bottomTxt) bottomTxt.textContent = `🔼 Show Less (Collapse to ${USER_DIR_COLLAPSED_LIMIT} Players)`;
    }

    tbody.innerHTML = usersToDisplay.map((u, idx) => {
      const w = u.wallets || { demo: 10000, real: 0, usdt: 0 };
      const real = parseFloat(w.real || 0);
      const demo = parseFloat(w.demo || 0);
      const usdt = parseFloat(w.usdt || 0);
      const regDate = u.createdAt ? new Date(u.createdAt).toLocaleString('en-IN') : 'N/A';
      const isVip = u.vipLevel && u.vipLevel !== 'None' && u.vipLevel !== 'Standard';

      const refCode = u.referralCode || ('GG-' + (u.id ? u.id.replace('USER-', '').substr(0, 6) : 'N/A'));
      return `
        <tr>
          <td>
            <div style="display:flex;align-items:center;gap:6px">
              <span style="font-size:11px;color:#64748b;font-weight:700">#${idx + 1}</span>
              <code style="color:#00e676;font-family:monospace;font-weight:800;background:#0f172a;padding:3px 6px;border-radius:4px;border:1px solid rgba(0,230,118,0.3)">${u.id || 'USER-N/A'}</code>
              <button class="btn-copy-mini" onclick="copyText('${u.id}', this)">Copy</button>
            </div>
          </td>
          <td><strong>${u.avatar || '👑'} ${u.username || 'Player'}</strong></td>
          <td>
            <div style="display:flex;align-items:center;gap:6px">
              <code style="color:#ffd700;font-family:monospace;font-weight:900;background:#0f172a;padding:3px 6px;border-radius:4px;border:1px solid rgba(255,215,0,0.3)">${refCode}</code>
              <button class="btn-copy-mini" onclick="copyText('${refCode}', this)">Copy</button>
            </div>
          </td>
          <td style="color:#cbd5e1">${u.email || '-'}</td>
          <td class="tx-amount inr" style="font-size:14px;font-weight:900">₹${real.toLocaleString('en-IN', {minimumFractionDigits:2})}</td>
          <td style="color:#c084fc;font-weight:700">₹${demo.toLocaleString('en-IN', {minimumFractionDigits:2})}</td>
          <td style="color:#38bdf8;font-weight:700">${usdt.toFixed(2)} ₮</td>
          <td>
            <span class="badge-status" style="background:${isVip ? 'rgba(255,215,0,0.15)' : 'rgba(255,255,255,0.05)'};border:1px solid ${isVip ? '#ffd700' : '#475569'};color:${isVip ? '#ffd700' : '#94a3b8'};font-weight:800">
              ${isVip ? '👑 ' + u.vipLevel : 'Standard'}
            </span>
          </td>
          <td style="color:#94a3b8;font-size:12px">${regDate}</td>
          <td>
            <button class="btn btn-primary" style="padding:6px 12px;font-size:11.5px;background:linear-gradient(135deg,#00e676,#00b0ff);color:#000;border:none;border-radius:6px;font-weight:900;cursor:pointer;box-shadow:0 0 10px rgba(0,230,118,0.2)" onclick="searchUserWallet('${u.id}')">
              🔍 Inspect &amp; Edit Wallet
            </button>
          </td>
        </tr>
      `;
    }).join('');
  }

  // ── 8B. EMAIL ALERTS & NOTIFICATIONS ─────────────────────────
  window.loadEmailConfigAndLogs = async function() {
    const tbody = document.getElementById('email-logs-tbody');
    const receiverInput = document.getElementById('email-receiver-input');
    const senderInput = document.getElementById('email-sender-input');

    try {
      const res = await fetch('/api/admin/get-email-config');
      const data = await res.json();
      if (data.success && data.config) {
        if (receiverInput && data.config.receiver) receiverInput.value = data.config.receiver;
        if (senderInput && data.config.sender) senderInput.value = data.config.sender;
      }

      const logs = data.logs || [];
      if (!tbody) return;

      if (logs.length === 0) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" class="empty-state">
              <div class="empty-icon">📭</div>
              <p>No email alerts dispatched yet. Click "Send Test Notification Email Now" to test!</p>
            </td>
          </tr>
        `;
        return;
      }

      tbody.innerHTML = logs.map(l => {
        const isDelivered = l.status === 'Delivered';
        const dateStr = l.timestamp ? new Date(l.timestamp).toLocaleString('en-IN') : '-';
        return `
          <tr>
            <td style="font-family:monospace;font-weight:700;color:#94a3b8">${l.id || '-'}</td>
            <td style="color:#38bdf8;font-weight:700">${l.to || '-'}</td>
            <td style="color:#f8fafc;font-weight:600">${l.subject || '-'}</td>
            <td>
              <span class="badge-status" style="background:${isDelivered ? 'rgba(0,230,118,0.15)' : 'rgba(239,68,68,0.15)'};border:1px solid ${isDelivered ? '#00e676' : '#ef4444'};color:${isDelivered ? '#00e676' : '#ef4444'};font-weight:800">
                ${isDelivered ? '✅ Delivered' : '❌ ' + (l.error || 'Failed')}
              </span>
            </td>
            <td style="color:#94a3b8;font-size:12px">${dateStr}</td>
          </tr>
        `;
      }).join('');
    } catch(e) {
      if (tbody) {
        tbody.innerHTML = `
          <tr>
            <td colspan="5" class="empty-state" style="color:#ef4444">
              <p>Error loading email logs: ${e.message}</p>
            </td>
          </tr>
        `;
      }
    }
  };

  window.saveEmailConfig = async function() {
    const receiver = (document.getElementById('email-receiver-input')?.value || '').trim();
    const statusEl = document.getElementById('email-action-status');

    if (!receiver || !receiver.includes('@')) {
      alert('Please enter a valid email address.');
      return;
    }

    if (statusEl) statusEl.textContent = '⏳ Saving email configuration...';

    try {
      const res = await fetch('/api/admin/set-email-config', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receiver: receiver })
      });
      const data = await res.json();
      if (data.success) {
        if (statusEl) {
          statusEl.textContent = '✅ Receiver email saved!';
          statusEl.style.color = '#00e676';
        }
        showNotification(`✅ Email alerts will now be sent to ${receiver}`, '#00e676');
        loadEmailConfigAndLogs();
      } else {
        if (statusEl) {
          statusEl.textContent = '❌ Failed: ' + data.message;
          statusEl.style.color = '#ef4444';
        }
      }
    } catch(e) {
      if (statusEl) {
        statusEl.textContent = '❌ Network error: ' + e.message;
        statusEl.style.color = '#ef4444';
      }
    }
  };

  window.sendTestNotificationEmail = async function() {
    const receiver = (document.getElementById('email-receiver-input')?.value || '').trim();
    const statusEl = document.getElementById('email-action-status');

    if (!receiver || !receiver.includes('@')) {
      alert('Please enter a valid email address.');
      return;
    }

    if (statusEl) {
      statusEl.textContent = '📨 Dispatched test email to ' + receiver + '...';
      statusEl.style.color = '#ffd700';
    }

    try {
      const res = await fetch('/api/admin/send-test-email', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ receiver: receiver })
      });
      const data = await res.json();
      if (data.success) {
        if (statusEl) {
          statusEl.textContent = '🎉 Test email delivered to ' + receiver + '! Check your inbox / spam.';
          statusEl.style.color = '#00e676';
        }
        showNotification(`🎉 Test email sent to ${receiver}!`, '#00e676');
        loadEmailConfigAndLogs();
      } else {
        if (statusEl) {
          statusEl.textContent = '❌ ' + data.message;
          statusEl.style.color = '#ef4444';
        }
      }
    } catch(e) {
      if (statusEl) {
        statusEl.textContent = '❌ Network error: ' + e.message;
        statusEl.style.color = '#ef4444';
      }
    }
  };

  // ── 9. BOOTSTRAP (REAL-TIME AUTO-SYNC & NOTIFICATION ENGINE) ─────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    const isUnlocked = checkAdminSession();
    if (isUnlocked) {
      fetchAllData();
    }

    // Real-Time Background Auto-Sync Engine (polls every 3.5 seconds)
    setInterval(async () => {
      const unlocked = checkAdminSession();
      if (unlocked) {
        await fetchAllData();
      }
    }, 3500);

    // Request browser notification permission for background alerts
    if ('Notification' in window && Notification.permission === 'default') {
      try {
        Notification.requestPermission();
      } catch(e) {}
    }

    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        refreshBtn.style.opacity = '0.5';
        refreshBtn.style.pointerEvents = 'none';
        fetchAllData().then(() => {
          showNotification('🔄 Admin Data Refreshed Successfully!', '#38bdf8');
        }).finally(() => {
          setTimeout(() => {
            refreshBtn.style.opacity = '1';
            refreshBtn.style.pointerEvents = 'auto';
          }, 600);
        });
      });
    }
  });

})();
