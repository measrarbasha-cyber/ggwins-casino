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
    
    setElText('stat-pending-count', pendingDeps.length);
    setElText('pending-badge', `${pendingDeps.length} PENDING`);
    setElText('nav-dep-badge', pendingDeps.length);
    setElText('stat-total-count', depositsData.length);

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

    setElText('stat-wth-pending-count', pendingWths.length);
    setElText('pending-wth-badge', `${pendingWths.length} PENDING`);
    setElText('nav-wth-badge', pendingWths.length);
    setElText('stat-wth-total-count', withdrawalsData.length);

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

    setElText('stat-vip-pending-count', pendingVips.length);
    setElText('pending-vip-badge', `${pendingVips.length} PENDING`);
    setElText('nav-vip-badge', pendingVips.length);
    setElText('stat-vip-approved-count', approvedVips.length);
    setElText('stat-vip-total-count', vipData.length);

    let totalVipRev = 0;
    approvedVips.forEach(v => { totalVipRev += parseFloat(v.amount) || 0; });
    setElText('stat-vip-revenue', `₹${totalVipRev.toLocaleString('en-IN', {minimumFractionDigits: 2})}`);

    // Notification Triggers on New Requests
    if (!isFirstLoad) {
      if (pendingVips.length > lastPendingVipCount) {
        playAlertTone();
        showNotification('👑 NEW VIP MEMBERSHIP REQUEST RECEIVED!', '#ffd700');
      } else if (pendingDeps.length > lastPendingDepCount) {
        playAlertTone();
        showNotification('📥 NEW DEPOSIT REQUEST RECEIVED!', '#00e676');
      } else if (pendingWths.length > lastPendingWthCount) {
        playAlertTone();
        showNotification('📤 NEW WITHDRAWAL REQUEST RECEIVED!', '#38bdf8');
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

  // ── 7. APPROVAL ACTIONS ───────────────────────────────────────
  window.approveDeposit = async function(id) {
    if (!confirm(`Are you sure you want to APPROVE deposit ${id} and credit user balance?`)) return;
    try {
      const res = await fetch('/api/approve-deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`✅ Deposit ${id} APPROVED and credited!`, '#00e676');
      }
    } catch (e) { console.warn(e); }
  };

  window.rejectDeposit = async function(id) {
    if (!confirm(`Are you sure you want to REJECT deposit ${id}?`)) return;
    try {
      const res = await fetch('/api/reject-deposit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`❌ Deposit ${id} Rejected.`, '#ef4444');
      }
    } catch (e) { console.warn(e); }
  };

  window.approveWithdrawal = async function(id) {
    if (!confirm(`Mark withdrawal ${id} as PAID?`)) return;
    try {
      const res = await fetch('/api/approve-withdrawal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`✅ Withdrawal ${id} marked as PAID!`, '#38bdf8');
      }
    } catch (e) { console.warn(e); }
  };

  window.rejectWithdrawal = async function(id) {
    if (!confirm(`Reject withdrawal ${id} and REFUND balance to user?`)) return;
    try {
      const res = await fetch('/api/reject-withdrawal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`⚠️ Withdrawal ${id} Rejected & Refunded.`, '#f59e0b');
      }
    } catch (e) { console.warn(e); }
  };

  window.approveVipRequest = async function(id) {
    const target = vipData.find(v => v.id === id || v.orderId === id);
    const username = target ? target.username : 'User';
    const tier = target ? target.tierName : 'Gold VIP';

    if (!confirm(`👑 Approve VIP Upgrade for ${username} to ${tier}? This will instantly grant their Glowing VIP Badge and unlock the VIP Members Lounge for 1 Month (30 Days)!`)) return;

    try {
      const res = await fetch('/api/approve-vip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      const data = await res.json();
      if (data.success) {
        fetchAllData();
        showNotification(`👑 VIP UPGRADE APPROVED FOR ${username.toUpperCase()}! Badge Activated!`, '#ffd700');
      } else {
        alert(data.message || 'Approval failed');
      }
    } catch(e) { console.warn(e); }
  };

  window.rejectVipRequest = async function(id) {
    if (!confirm(`Reject VIP upgrade application ${id}?`)) return;
    try {
      const res = await fetch('/api/reject-vip', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
      });
      if (res.ok) {
        fetchAllData();
        showNotification(`VIP request rejected.`, '#ef4444');
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
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.type = 'triangle';
      osc.frequency.setValueAtTime(587.33, audioCtx.currentTime); // D5
      osc.frequency.setValueAtTime(880, audioCtx.currentTime + 0.12); // A5
      gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.35);
      osc.connect(gain);
      gain.connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 0.35);
    } catch (e) {}
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

  // ── 9. BOOTSTRAP (MANUAL REFRESH ONLY • NO AUTO-RELOAD) ─────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    const isUnlocked = checkAdminSession();
    if (isUnlocked) {
      fetchAllData();
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
