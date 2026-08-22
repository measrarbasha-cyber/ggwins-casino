/**
 * GG WINS — Centralized Multi-Account Wallet & Banking Engine
 * Supports 3 Accounts: Demo INR (₹), Deposited Money INR (₹), Deposited USDT (₮)
 * Seamless switching, persistent storage, INR payment methods, and strict deposit/withdrawal limits.
 */

(function() {
  'use strict';

  const WALLET_CONFIGS = {
    demo: {
      key: 'demo',
      name: 'Demo Account',
      shortName: 'Demo INR',
      symbol: '₹',
      code: 'INR',
      icon: '🎮',
      badge: 'DEMO',
      badgeColor: '#7c4dff',
      isCrypto: false,
      initial: 10000.00,
      description: 'Practice INR balance for testing games with zero risk'
    },
    real: {
      key: 'real',
      name: 'Deposited Money (INR)',
      shortName: 'Real INR',
      symbol: '₹',
      code: 'INR',
      icon: '💵',
      badge: 'REAL',
      badgeColor: '#00e676',
      isCrypto: false,
      initial: 0.00,
      description: 'Deposited real INR balance for cash wagering & withdrawals'
    },
    usdt: {
      key: 'usdt',
      name: 'Deposited USDT',
      shortName: 'USDT (₮)',
      symbol: '₮',
      code: 'USDT',
      icon: '🪙',
      badge: 'CRYPTO',
      badgeColor: '#26a17b',
      isCrypto: true,
      initial: 0.00,
      description: 'Tether USD (TRC-20 / ERC-20) crypto balance'
    }
  };

  // Limits Configuration
  const LIMITS = {
    inr: {
      depositMin: 500,
      depositMax: 100000,
      withdrawMin: 1500,
      withdrawMax: 200000
    },
    usdt: {
      depositMin: 10,
      depositMax: 5000,
      withdrawMin: 20,
      withdrawMax: 10000
    }
  };

  // ── INITIAL STORAGE SETUP ────────────────────────────────────
  function initWalletStorage() {
    const rawV2 = localStorage.getItem('ggwins_wallets_v2');
    const rawV1 = localStorage.getItem('ggwins_wallets');
    let wallets = null;
    try {
      wallets = JSON.parse(rawV2 || rawV1);
    } catch(e){}

    const txs = JSON.parse(localStorage.getItem('ggwins_transactions') || '[]');
    const hasApprovedDeposit = txs.some(t => t.type === 'deposit' && (t.status === 'Completed' || t.status === 'Approved') && t.wallet === 'real');

    if (!wallets) {
      wallets = {
        demo: 10000.00,
        real: 0.00,
        usdt: 0.00
      };
    } else {
      // Enforce 0rs default for real and USDT unless legitimately approved
      if (wallets.real === 25000 || (!hasApprovedDeposit && wallets.real > 0 && !localStorage.getItem('ggwins_session'))) {
        wallets.real = 0.00;
      }
      if (wallets.usdt === 500) {
        wallets.usdt = 0.00;
      }
      if (typeof wallets.demo !== 'number' || isNaN(wallets.demo)) {
        wallets.demo = 10000.00;
      }
    }
    localStorage.setItem('ggwins_wallets_v2', JSON.stringify(wallets));
    localStorage.setItem('ggwins_wallets', JSON.stringify(wallets));

    if (!localStorage.getItem('ggwins_active_wallet')) {
      localStorage.setItem('ggwins_active_wallet', 'demo');
    }
    if (!localStorage.getItem('ggwins_vip_level') || localStorage.getItem('ggwins_vip_level') === 'Standard') {
      localStorage.setItem('ggwins_vip_level', 'None');
    }
    if (!localStorage.getItem('ggwins_transactions')) {
      localStorage.setItem('ggwins_transactions', JSON.stringify([]));
    }
  }
  initWalletStorage();

  window.refreshDemoBalance = function() {
    let wallets = getWallets();
    wallets.demo = 10000.00;
    saveWallets(wallets);
    if (typeof showToast === 'function') {
      showToast('🔄 Demo Practice balance refilled to ₹10,000.00!', 'success');
    } else if (typeof showToastMsg === 'function') {
      showToastMsg('🔄 Demo Practice balance refilled to ₹10,000.00!');
    }
    updateAllWalletDisplays();
    if (typeof updateWalletUI === 'function') updateWalletUI();
    return formatCurrency(10000.00, 'demo');
  };

  // ── CORE WALLET GETTERS / SETTERS ────────────────────────────
  window.getWallets = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_wallets_v2')) ||
             JSON.parse(localStorage.getItem('ggwins_wallets')) ||
             { demo: 10000, real: 0, usdt: 0 };
    } catch(e) {
      return { demo: 10000, real: 0, usdt: 0 };
    }
  };

  window.saveWallets = function(wallets) {
    localStorage.setItem('ggwins_wallets_v2', JSON.stringify(wallets));
    localStorage.setItem('ggwins_wallets', JSON.stringify(wallets));
    const activeKey = getActiveWalletKey();
    const activeBal = wallets[activeKey] !== undefined ? wallets[activeKey] : (activeKey === 'demo' ? 10000 : 0);
    localStorage.setItem('ggwins_balance', activeBal.toFixed(2));
    updateAllWalletDisplays();

    // Persist reduced/updated balance to server so server record never resets lost money
    try {
      const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
      if (session.id || session.username) {
        fetch('/api/update-user-progress', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            userId: session.id || '',
            username: session.username || '',
            wallets: wallets
          })
        }).catch(() => {});
      }
    } catch(e) {}
  };

  window.getVipLevel = function() {
    return localStorage.getItem('ggwins_vip_level') || 'None';
  };

  window.getActiveWalletKey = function() {
    return localStorage.getItem('ggwins_active_wallet') || 'demo';
  };

  window.getActiveWalletConfig = function() {
    const key = getActiveWalletKey();
    return WALLET_CONFIGS[key] || WALLET_CONFIGS.demo;
  };

  window.setActiveWalletKey = function(key) {
    if (!WALLET_CONFIGS[key]) return;
    localStorage.setItem('ggwins_active_wallet', key);
    const wallets = getWallets();
    const bal = wallets[key] !== undefined ? wallets[key] : 0;
    localStorage.setItem('ggwins_balance', bal.toFixed(2));
    updateAllWalletDisplays();
    
    // Broadcast active account change
    window.dispatchEvent(new CustomEvent('walletChanged', {
      detail: { wallet: key, config: WALLET_CONFIGS[key], balance: bal }
    }));

    if (typeof showToast === 'function') {
      const cfg = WALLET_CONFIGS[key];
      showToast(`Switched account to ${cfg.icon} ${cfg.name} (${formatCurrency(bal, key)})`, 'success');
    }
  };

  window.switchWallet = window.setActiveWalletKey;

  window.getBalance = function() {
    const wallets = getWallets();
    const key = getActiveWalletKey();
    return parseFloat(wallets[key] !== undefined ? wallets[key] : 10000);
  };

  window.getActiveBalance = window.getBalance;

  window.setBalance = function(val) {
    const wallets = getWallets();
    const key = getActiveWalletKey();
    wallets[key] = Math.max(0, parseFloat(val) || 0);
    saveWallets(wallets);
  };

  window.adjustBalance = function(delta, description) {
    const wallets = getWallets();
    const key = getActiveWalletKey();
    const curr = parseFloat(wallets[key] !== undefined ? wallets[key] : 10000);
    const change = parseFloat(delta || 0);
    const next = Math.max(0, curr + change);
    wallets[key] = next;
    saveWallets(wallets);

    if (change > 0 && typeof window.flashBal === 'function') window.flashBal('flash-win');
    else if (change < 0 && typeof window.flashBal === 'function') window.flashBal('flash-lose');

    return next;
  };

  window.flashBal = function(cls) {
    const els = document.querySelectorAll('#bal-display, .gnav-balance-val, #gnav-balance-val, #lobby-balance-val');
    els.forEach(el => {
      el.classList.remove('flash-win', 'flash-lose');
      void el.offsetWidth; // trigger reflow
      el.classList.add(cls);
      setTimeout(() => el.classList.remove(cls), 600);
    });
  };

  // ── 🔄 REAL-TIME SERVER BALANCE SYNCHRONIZER ──
  window.syncWalletWithServer = async function() {
    try {
      const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
      const userId = session.id || localStorage.getItem('ggwins_user_id') || '';
      const username = session.username || '';
      
      if (!userId && !username) return;

      const res = await fetch(`/api/user-status?userId=${encodeURIComponent(userId)}&username=${encodeURIComponent(username)}`, {
        cache: 'no-store'
      });
      if (!res.ok) return;

      const data = await res.json();
      if (data && data.success && data.wallets) {
        const localWallets = getWallets();
        const serverWallets = data.wallets;
        
        let changed = false;
        ['real', 'usdt'].forEach(k => {
          if (serverWallets[k] !== undefined && Math.abs(parseFloat(serverWallets[k]) - parseFloat(localWallets[k] || 0)) > 0.009) {
            localWallets[k] = parseFloat(serverWallets[k]);
            changed = true;
          }
        });

        if (changed) {
          saveWallets(localWallets);
          updateAllWalletDisplays();
          if (typeof renderWalletSwitcherWidget === 'function') {
            renderWalletSwitcherWidget();
          }
          window.dispatchEvent(new CustomEvent('walletChanged', {
            detail: { wallet: getActiveWalletKey(), balance: getBalance() }
          }));
        }

        // Also sync VIP level if updated by Admin
        if (data.vipLevel && data.vipLevel !== localStorage.getItem('ggwins_vip_level')) {
          localStorage.setItem('ggwins_vip_level', data.vipLevel);
          if (typeof window.applyVipBadgeUI === 'function') window.applyVipBadgeUI();
        }
      }
    } catch(e) {}
  };

  // Cross-tab and return-to-page balance synchronizer
  window.addEventListener('storage', function(e) {
    if (e.key === 'ggwins_wallets_v2' || e.key === 'ggwins_active_wallet' || e.key === 'ggwins_balance') {
      updateAllWalletDisplays();
    }
  });
  window.addEventListener('focus', function() {
    updateAllWalletDisplays();
    syncWalletWithServer();
  });

  // Run server wallet sync on load, focus, and every 2.5 seconds
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { setTimeout(syncWalletWithServer, 500); });
  } else {
    setTimeout(syncWalletWithServer, 500);
  }
  setInterval(syncWalletWithServer, 2500);

  window.formatCurrency = function(amount, walletKey) {
    const key = walletKey || getActiveWalletKey();
    const cfg = WALLET_CONFIGS[key] || WALLET_CONFIGS.demo;
    const num = parseFloat(amount || 0);
    
    if (cfg.isCrypto) {
      return `${num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${cfg.symbol}`;
    }
    // Indian Currency Format
    return `${cfg.symbol}${num.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;
  };

  window.getTransactions = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_transactions')) || [];
    } catch(e) {
      return [];
    }
  };

  window.addTransaction = function(tx) {
    const list = getTransactions();
    const orderId = tx.orderId || ('ORD-' + (tx.type === 'withdraw' ? 'WTH-' : (tx.type === 'deposit' ? 'DEP-' : 'REF-')) + Math.floor(100000 + Math.random() * 900000));
    list.unshift({
      id: tx.id || orderId,
      orderId: orderId,
      timestamp: Date.now(),
      status: tx.status || 'Completed',
      ...tx
    });
    localStorage.setItem('ggwins_transactions', JSON.stringify(list.slice(0, 100)));
  };

  // ── 🏆 TOURNAMENT POINTS SCORING ENGINE ─────────────────────────
  // Points: +100 per Win, +50 per Loss ONLY IF player is registered for that particular game
  window.recordTournamentMatch = function(gameIdentifier, isWin) {
    if (!gameIdentifier) return;
    try {
      const cleanId = String(gameIdentifier).toLowerCase().replace(/[^a-z0-9]/g, '');
      const registered = JSON.parse(localStorage.getItem('ggwins_registered_tournaments') || '{}');
      
      // Match against registered tournaments
      let matchedTournId = null;
      for (const tId in registered) {
        const tGame = tId.replace('t_', '').toLowerCase().replace(/[^a-z0-9]/g, '');
        if (cleanId.includes(tGame) || tGame.includes(cleanId) || (cleanId.includes('snak') && tGame.includes('snak')) || (cleanId.includes('ludo') && tGame.includes('ludo'))) {
          matchedTournId = tId;
          break;
        }
      }

      if (matchedTournId && registered[matchedTournId]) {
        const entry = registered[matchedTournId];
        const ptsToAdd = isWin ? 100 : 50;
        entry.points = (entry.points || 0) + ptsToAdd;
        entry.matches = (entry.matches || 0) + 1;
        if (isWin) entry.wins = (entry.wins || 0) + 1;
        else entry.losses = (entry.losses || 0) + 1;

        localStorage.setItem('ggwins_registered_tournaments', JSON.stringify(registered));

        if (typeof showToast === 'function') {
          showToast(`🏆 Tournament: +${ptsToAdd} pts for ${entry.name || 'Tournament'}! (Total: ${entry.points} pts)`, isWin ? 'success' : 'info');
        }
      }
    } catch(e) {
      console.error('Tournament scoring error:', e);
    }
  };

  // ── PENDING DEPOSITS ──────────────────────────────────────────
  
  // ── PROMO COUPONS & 3X WAGERING TASK ENGINE ────────────────────
  window.COUPONS = {
    'GG1675': {
      code: 'GG1675',
      name: 'Deposit ₹1675+ (Up to 100% Scaled Bonus)',
      minDeposit: 1675,
      description: 'Deposit ₹1675 to get bonus up to 100%. The more you deposit above ₹1675, the higher deposit bonus you unlock!',
      calcBonus: function(amt) {
        if (amt < 1675) return 0;
        // At 1675 = 50%, scaling smoothly to 100% at 5000+
        const pct = Math.min(100, Math.round(50 + ((amt - 1675) / (5000 - 1675)) * 50));
        return Math.round(amt * (pct / 100) * 100) / 100;
      },
      getPercent: function(amt) {
        if (amt < 1675) return 0;
        return Math.min(100, Math.round(50 + ((amt - 1675) / (5000 - 1675)) * 50));
      }
    },
    'INSTANT1500': {
      code: 'INSTANT1500',
      name: 'Deposit ₹2500 Get Instant ₹1500 Bonus',
      minDeposit: 2500,
      description: 'Deposit ₹2500 to receive instant ₹1500 bonus added to your balance.',
      calcBonus: function(amt) {
        if (amt < 2500) return 0;
        return 1500.00;
      },
      getPercent: function(amt) {
        if (amt < 2500) return 0;
        return Math.round((1500 / amt) * 100);
      }
    }
  };

  let appliedCouponCode = null;

  window.applyPromoCoupon = function(code, autoAdjustAmount = true) {
    const codeClean = (code || '').toUpperCase().trim();
    if (!COUPONS[codeClean]) {
      if (typeof showToast === 'function') showToast('❌ Invalid coupon code', 'error');
      appliedCouponCode = null;
      renderWalletModalContent();
      return;
    }

    if (isCouponUsed(codeClean)) {
      if (typeof showToast === 'function') {
        showToast(`⚠️ Coupon ${codeClean} is already used. Each coupon is one-time use only.`, 'warning');
      }
      appliedCouponCode = null;
      renderWalletModalContent();
      return;
    }

    // Auto-enter money logic:
    // 1. If user amount is below coupon minimum, auto-enter the exact amount mentioned in coupon
    // 2. If user entered above coupon minimum (e.g. 2000, 3500, 5000), keep the higher amount and give scaled bonus accordingly
    const amtInput = document.getElementById('wm-amount-input');
    let curAmt = parseFloat(amtInput ? amtInput.value : 0) || 0;
    const minReq = COUPONS[codeClean].minDeposit;

    if (autoAdjustAmount) {
      if (curAmt < minReq) {
        curAmt = minReq;
        if (amtInput) amtInput.value = minReq;
      }
    }

    appliedCouponCode = codeClean;

    const bonus = COUPONS[codeClean].calcBonus(curAmt);
    const pct = COUPONS[codeClean].getPercent(curAmt);

    if (typeof showToast === 'function') {
      showToast(`🎟️ Coupon ${codeClean} Applied! +₹${bonus.toFixed(2)} (${pct}%) Bonus calculated on ₹${curAmt.toFixed(2)}.`, 'success');
    }

    renderWalletModalContent();
  };

  window.updateLiveBonusPreview = function() {
    const previewEl = document.getElementById('wm-coupon-live-preview');
    if (!previewEl || !appliedCouponCode || !COUPONS[appliedCouponCode]) return;

    const c = COUPONS[appliedCouponCode];
    const amtInput = document.getElementById('wm-amount-input');
    const curAmt = Math.max(0, parseFloat(amtInput ? amtInput.value : 0) || 0);

    const bonusAmt = c.calcBonus(curAmt);
    const totalCredit = curAmt + bonusAmt;
    const targetWager = bonusAmt * 3;
    const pct = c.getPercent(curAmt);

    if (curAmt < c.minDeposit) {
      previewEl.innerHTML = `
        <div style="margin-top:10px;background:rgba(239,68,68,0.1);border:1px solid #ef4444;border-radius:10px;padding:10px">
          <div style="font-size:12px;color:#ef4444;font-weight:700">⚠️ Minimum deposit of ₹${c.minDeposit} required for coupon ${c.code}.</div>
          <div style="margin-top:4px"><button onclick="setModalAmount(${c.minDeposit})" style="background:#ef4444;color:#fff;border:none;border-radius:6px;padding:4px 8px;font-size:11px;font-weight:700;cursor:pointer">Set to ₹${c.minDeposit}</button></div>
        </div>
      `;
      return;
    }

    previewEl.innerHTML = `
      <div style="margin-top:10px;background:rgba(0,230,118,0.1);border:1px solid #00e676;border-radius:10px;padding:10px;animation:modalSlideUp 0.2s ease">
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
          <span style="color:#94a3b8">Base Deposit:</span>
          <span style="font-weight:700;color:#fff">₹${curAmt.toFixed(2)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
          <span style="color:#00e676;font-weight:700">Coupon Bonus (${c.code}):</span>
          <span style="font-weight:900;color:#00e676">+₹${bonusAmt.toFixed(2)} (${pct}%)</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:13px;border-top:1px dashed rgba(255,255,255,0.2);padding-top:4px;margin-top:4px">
          <span style="color:#ffd700;font-weight:800">Total Credited Balance:</span>
          <span style="font-weight:900;color:#ffd700">₹${totalCredit.toFixed(2)}</span>
        </div>
        <div style="margin-top:8px;font-size:11px;color:#94a3b8;background:rgba(0,0,0,0.3);border-radius:6px;padding:6px 8px;line-height:1.4">
          🎯 <strong>3× Bonus Task Rule:</strong> You must wager/earn <strong>3× the bonus amount (₹${targetWager.toFixed(2)})</strong> across games before bonus withdrawal is unlocked.
        </div>
      </div>
    `;
  };

  window.removePromoCoupon = function() {
    appliedCouponCode = null;
    if (typeof showToast === 'function') showToast('Coupon removed', 'info');
    renderWalletModalContent();
  };

  // ── ONE-TIME COUPON TRACKING ──
  window.getUsedCoupons = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_used_coupons') || '[]');
    } catch(e) {
      return [];
    }
  };

  window.isCouponUsed = function(code) {
    const list = getUsedCoupons();
    return list.includes((code || '').toUpperCase().trim());
  };

  window.markCouponUsed = function(code) {
    const list = getUsedCoupons();
    const c = (code || '').toUpperCase().trim();
    if (!list.includes(c)) {
      list.push(c);
      localStorage.setItem('ggwins_used_coupons', JSON.stringify(list));
    }
  };

  window.restoreCoupon = function(code) {
    let list = getUsedCoupons();
    const c = (code || '').toUpperCase().trim();
    list = list.filter(item => item !== c);
    localStorage.setItem('ggwins_used_coupons', JSON.stringify(list));
  };

  window.getBonusTask = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
    } catch(e) {
      return null;
    }
  };

  
  // ── CANCEL BONUS TASK (DEDUCTS BONUS + 8% BALANCE PENALTY FEE) ──
  window.cancelBonusTask = function() {
    const task = getBonusTask();
    if (!task) {
      if (typeof showToast === 'function') showToast('No active bonus task found.', 'info');
      return;
    }

    const wallets = getWallets();
    const currentRealBal = parseFloat(wallets.real || 0);
    const bonusToDeduct = parseFloat(task.bonusAmt || 0);
    const penaltyFee = currentRealBal * 0.08; // 8% fee on current real balance
    const totalDeduction = bonusToDeduct + penaltyFee;

    const newRealBal = Math.max(0, currentRealBal - totalDeduction);
    wallets.real = newRealBal;
    saveWallets(wallets);

    // Restore the coupon so user can use it again
    if (task.coupon) {
      restoreCoupon(task.coupon);
    }

    // Remove active bonus task
    saveBonusTask(null);

    // Log transaction record
    addTransaction({
      id: 'FEE-' + Math.floor(100000 + Math.random() * 900000),
      orderId: 'TASK-CANCEL-' + Math.floor(100000 + Math.random() * 900000),
      type: 'fee',
      wallet: 'real',
      amount: -totalDeduction,
      currency: 'INR',
      method: `Bonus Forfeit (-₹${bonusToDeduct.toFixed(2)}) & 8% Balance Fee (-₹${penaltyFee.toFixed(2)})`,
      status: 'Completed',
      timestamp: Date.now()
    });

    if (typeof showToast === 'function') {
      showToast(`⚠️ Bonus task cancelled. -₹${bonusToDeduct.toFixed(2)} bonus and -₹${penaltyFee.toFixed(2)} (8% fee) deducted. Coupon [${task.coupon||'BONUS'}] has been restored for you!`, 'warning');
    }

    renderWalletModalContent();
    updateAllWalletDisplays();
  };

  window.openCancelBonusTaskModal = function() {
    const task = getBonusTask();
    if (!task) return;

    const wallets = getWallets();
    const currentRealBal = parseFloat(wallets.real || 0);
    const bonusToDeduct = parseFloat(task.bonusAmt || 0);
    const penaltyFee = currentRealBal * 0.08;
    const totalDeduction = bonusToDeduct + penaltyFee;
    const newBal = Math.max(0, currentRealBal - totalDeduction);

    const confirmMsg = `⚠️ CANCEL BONUS TASK & UNLOCK WITHDRAWAL\n\n` +
      `Are you sure you want to cancel your Active Bonus Task?\n\n` +
      `• Deposited Bonus to forfeit: -₹${bonusToDeduct.toFixed(2)}\n` +
      `• 8% Cancellation Fee on your balance (₹${currentRealBal.toFixed(2)}): -₹${penaltyFee.toFixed(2)}\n` +
      `• Total deduction from balance: -₹${totalDeduction.toFixed(2)}\n` +
      `• Remaining Real INR Balance: ₹${newBal.toFixed(2)}\n\n` +
      `Result: Your withdrawal lock will be immediately lifted.\n\n` +
      `Click OK to cancel the task or Cancel to keep playing your bonus task.`;

    if (confirm(confirmMsg)) {
      cancelBonusTask();
    }
  };

  window.saveBonusTask = function(task) {
    if (task) {
      localStorage.setItem('ggwins_bonus_task', JSON.stringify(task));
    } else {
      localStorage.removeItem('ggwins_bonus_task');
    }
    window.dispatchEvent(new CustomEvent('bonusTaskUpdated', { detail: task }));
  };

  window.createPendingDeposit = function(walletKey, amount, method, utr, senderName, couponCode, bonusAmount, qrNumParam) {
    const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
    const pendingId = 'DEP-' + Math.random().toString(36).substr(2, 8).toUpperCase();
    const orderId = 'ORD-DEP-' + Math.floor(100000 + Math.random() * 900000);
    const qrNum = qrNumParam || selectedPaymentQR || (parseInt(document.getElementById('wm-qr-img')?.dataset?.idx || 0) + 1);
    const qrTarget = QR_DATA[qrNum - 1] ? QR_DATA[qrNum - 1].upi : 'amdasrarbasha-1@oksbi';

    const pendingRecord = {
      id: pendingId,
      orderId: orderId,
      userId: session.id || '',
      username: session.username || senderName || 'Player',
      email: session.email || '',
      wallet: walletKey,
      amount: amount,
      bonusAmount: bonusAmount || 0,
      coupon: couponCode || null,
      creditedAmount: amount + (bonusAmount || 0),
      currency: walletKey === 'usdt' ? 'USDT' : 'INR',
      method: method,
      qrNumber: qrNum,
      qrTarget: qrTarget,
      qrLabel: `QR ${qrNum} (${qrTarget})`,
      utr: utr || ('UPI-' + Array.from({length: 12}, () => Math.floor(Math.random()*10)).join('')),
      senderName: senderName || session.username || 'Player',
      status: 'Pending',
      timestamp: Date.now()
    };

    // 1. Save to local pending deposits
    const pendingList = JSON.parse(localStorage.getItem('ggwins_pending_deposits') || '[]');
    pendingList.unshift(pendingRecord);
    localStorage.setItem('ggwins_pending_deposits', JSON.stringify(pendingList));

    // 2. Add to transaction history as Pending
    addTransaction({
      id: pendingId,
      orderId: orderId,
      type: 'deposit',
      wallet: walletKey,
      amount: amount,
      currency: pendingRecord.currency,
      method: method,
      qrNumber: qrNum,
      qrTarget: qrTarget,
      status: 'Pending',
      utr: pendingRecord.utr
    });

    // 3. Post to backend server API for cross-device sync with Admin terminal
    try {
      fetch('/api/deposit-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(pendingRecord)
      }).then(r => r.json()).then(data => {
        if (data && data.deposit) {
          console.log('Deposit synced to server:', data.deposit.id);
        }
      }).catch(err => {
        console.warn('Server sync error (saved locally):', err);
      });
    } catch (e) {
      console.warn('Fetch error:', e);
    }

    window.dispatchEvent(new CustomEvent('pendingDepositCreated', { detail: { id: pendingId, record: pendingRecord } }));
    return pendingId;
  };

  // ── BACKGROUND REAL-TIME SYNC WITH SERVER ─────────────────────
  let processedCompletedDepositIds = new Set();
  // Initialize with already completed deposits in storage so we don't duplicate notifications
  try {
    const existingTxs = JSON.parse(localStorage.getItem('ggwins_transactions') || '[]');
    existingTxs.forEach(t => { if (t.status === 'Completed') processedCompletedDepositIds.add(t.id); });
  } catch (e) {}

  window.syncWalletStatusFromServer = async function() {
    try {
      const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
      let url = '/api/user-status';
      if (session && (session.id || session.username)) {
        const p = new URLSearchParams();
        if (session.id) p.append('userId', session.id);
        if (session.username) p.append('username', session.username);
        if (session.email) p.append('email', session.email);
        if (session.vipLevel) p.append('vipLevel', session.vipLevel);
        url = `/api/user-status?${p.toString()}`;
      }

      const res = await fetch(url);
      if (!res.ok) return;
      const data = await res.json();
      if (!data) return;

      let wallets = getWallets();
      let updated = false;
      let newlyApprovedDeposit = null;

      // 1. Check for newly approved deposits in data.deposits (Sync wallet from server source of truth)
      if (data.deposits && Array.isArray(data.deposits)) {
        let localTxs = getTransactions();
        data.deposits.forEach(dep => {
          if (dep.status === 'Completed' && !processedCompletedDepositIds.has(dep.id)) {
            processedCompletedDepositIds.add(dep.id);
            newlyApprovedDeposit = dep;
            updated = true;

            const targetWallet = dep.wallet || (dep.currency === 'USDT' ? 'usdt' : 'real');
            const baseAmt = parseFloat(dep.amount || 0);
            const bonusAmt = parseFloat(dep.bonusAmount || 0);
            const creditedTotal = parseFloat(dep.creditedAmount || (baseAmt + bonusAmt));

            // Use server's authoritative wallet balance if provided, avoiding any double additions
            if (data.wallets && data.wallets[targetWallet] !== undefined) {
              wallets[targetWallet] = parseFloat(data.wallets[targetWallet]);
            } else {
              wallets[targetWallet] = (parseFloat(wallets[targetWallet]) || 0) + creditedTotal;
            }

            // Create 3X Wagering Bonus Task if coupon bonus was applied
            if (bonusAmt > 0) {
              const targetWager = (baseAmt + bonusAmt) * 3;
              const taskObj = {
                id: 'TASK-' + dep.id,
                depositId: dep.id,
                coupon: dep.coupon || 'GG1675',
                depositAmt: baseAmt,
                bonusAmt: bonusAmt,
                totalCredited: creditedTotal,
                targetWager: targetWager,
                currentWagered: 0,
                completed: false,
                createdAt: Date.now()
              };
              saveBonusTask(taskObj);
            }

            // Update or add in local transactions
            let localTx = localTxs.find(t => t.id === dep.id);
            if (localTx) {
              localTx.status = 'Completed';
              localTx.amount = creditedTotal;
            } else {
              localTxs.unshift({
                id: dep.id,
                type: 'deposit',
                wallet: targetWallet,
                amount: creditedTotal,
                baseAmount: baseAmt,
                bonusAmount: bonusAmt,
                coupon: dep.coupon || null,
                currency: dep.currency || (targetWallet === 'usdt' ? 'USDT' : 'INR'),
                method: dep.method || 'UPI Instant',
                status: 'Completed',
                timestamp: dep.timestamp || Date.now()
              });
            }
          }
        });
        localStorage.setItem('ggwins_transactions', JSON.stringify(localTxs.slice(0, 50)));
      }

      // 3. Check for withdrawal status updates in data.withdrawals
      if (data.withdrawals && Array.isArray(data.withdrawals)) {
        let localTxs = getTransactions();
        data.withdrawals.forEach(wth => {
          if (!processedCompletedDepositIds.has(wth.id)) {
            if (wth.status === 'Completed') {
              processedCompletedDepositIds.add(wth.id);
              let localTx = localTxs.find(t => t.id === wth.id);
              if (localTx) localTx.status = 'Completed';
              localStorage.setItem('ggwins_transactions', JSON.stringify(localTxs.slice(0, 50)));
              if (typeof showToast === 'function') {
                showToast(`💸 Withdrawal of ${formatCurrency(wth.amount, wth.wallet)} has been APPROVED & PAID via IMPS!`, 'success');
              }
            } else if (wth.status === 'Rejected') {
              processedCompletedDepositIds.add(wth.id);
              let localTx = localTxs.find(t => t.id === wth.id);
              if (localTx) localTx.status = 'Rejected (Refunded)';
              localStorage.setItem('ggwins_transactions', JSON.stringify(localTxs.slice(0, 50)));
              
              // Refund balance
              const wkey = wth.wallet || 'real';
              wallets[wkey] = (parseFloat(wallets[wkey]) || 0) + parseFloat(wth.amount);
              updated = true;

              if (typeof showToast === 'function') {
                showToast(`⚠️ Withdrawal of ${formatCurrency(wth.amount, wth.wallet)} was rejected. Funds refunded to your balance.`, 'info');
              }
            }
          }
        });
      }

      // 4. Check for VIP Level approval from Admin in data.user
      if (data.user && data.user.vipLevel) {
        const currentVip = localStorage.getItem('ggwins_vip_level') || 'Bronze';
        const serverVip = data.user.vipLevel;
        const serverExpires = data.user.vipExpiresAt || 0;

        if (serverVip !== currentVip) {
          localStorage.setItem('ggwins_vip_level', serverVip);
          localStorage.setItem('ggwins_vip_expires_at', serverExpires.toString());
          if (session) {
            session.vipLevel = serverVip;
            session.vipExpiresAt = serverExpires;
            localStorage.setItem('ggwins_session', JSON.stringify(session));
          }
          if (serverVip !== 'Bronze') {
            if (typeof showToast === 'function') {
              showToast(`👑 CONGRATULATIONS! Host approved your ${serverVip} Upgrade! Glowing VIP Badge & VIP Lounge unlocked!`, 'success');
            }
          }
          if (typeof updateAuthUI === 'function') updateAuthUI();
          if (typeof checkVipAccess === 'function') checkVipAccess();
      // 5. Direct Admin Balance Adjustment Live Sync
      if (data.wallets && typeof data.wallets === 'object') {
        const sReal = parseFloat(data.wallets.real);
        const sDemo = parseFloat(data.wallets.demo);
        const sUsdt = parseFloat(data.wallets.usdt);

        if (!isNaN(sReal) && Math.abs((parseFloat(wallets.real) || 0) - sReal) > 0.001) {
          wallets.real = sReal;
          updated = true;
        }
        if (!isNaN(sDemo) && Math.abs((parseFloat(wallets.demo) || 0) - sDemo) > 0.001) {
          wallets.demo = sDemo;
          updated = true;
        }
        if (!isNaN(sUsdt) && Math.abs((parseFloat(wallets.usdt) || 0) - sUsdt) > 0.001) {
          wallets.usdt = sUsdt;
          updated = true;
        }
      }

      if (updated) {
        saveWallets(wallets);
        
        // If a real or USDT deposit was just approved, auto-switch active wallet to it so user sees the funds immediately!
        if (newlyApprovedDeposit) {
          const targetWallet = newlyApprovedDeposit.wallet || (newlyApprovedDeposit.currency === 'USDT' ? 'usdt' : 'real');
          setActiveWalletKey(targetWallet);

          const formattedAmt = formatCurrency(newlyApprovedDeposit.amount, targetWallet);
          if (typeof showToast === 'function') {
            showToast(`🎉 Host approved deposit of ${formattedAmt}! Account credited & active balance switched to Real Money.`, 'success');
          }

          // Trigger celebratory sound
          try {
            const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const osc = audioCtx.createOscillator();
            const gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(523.25, audioCtx.currentTime); // C5
            osc.frequency.setValueAtTime(659.25, audioCtx.currentTime + 0.1); // E5
            osc.frequency.setValueAtTime(783.99, audioCtx.currentTime + 0.2); // G5
            osc.frequency.setValueAtTime(1046.50, audioCtx.currentTime + 0.3); // C6
            gain.gain.setValueAtTime(0.2, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + 0.5);
            osc.connect(gain);
            gain.connect(audioCtx.destination);
            osc.start();
            osc.stop(audioCtx.currentTime + 0.5);
          } catch(e) {}
        } else {
          updateAllWalletDisplays();
        }
      }
    } catch (e) {
      // Offline fallback
    }
  };

  // Poll server every 1.5 seconds for instant real-time response
  setInterval(window.syncWalletStatusFromServer, 1500);
  window.syncWalletStatusFromServer();

  // ── DEPOSIT / WITHDRAW ACTIONS ──────────────────────────────
  window.depositFunds = function(walletKey, amount, method, txid) {
    const amt = parseFloat(amount);
    if (isNaN(amt) || amt <= 0) return { success: false, message: 'Invalid deposit amount' };
    
    // Limits check
    if (walletKey === 'real' || walletKey === 'demo') {
      if (amt < LIMITS.inr.depositMin) {
        return { success: false, message: `Minimum deposit is ₹${LIMITS.inr.depositMin.toLocaleString('en-IN')}` };
      }
      if (amt > LIMITS.inr.depositMax) {
        return { success: false, message: `Maximum deposit is ₹${LIMITS.inr.depositMax.toLocaleString('en-IN')}` };
      }
    } else if (walletKey === 'usdt') {
      if (amt < LIMITS.usdt.depositMin) {
        return { success: false, message: `Minimum deposit is ${LIMITS.usdt.depositMin} USDT` };
      }
      if (amt > LIMITS.usdt.depositMax) {
        return { success: false, message: `Maximum deposit is ${LIMITS.usdt.depositMax} USDT` };
      }
    }

    const wallets = getWallets();
    if (wallets[walletKey] === undefined) wallets[walletKey] = 0;
    wallets[walletKey] += amt;
    saveWallets(wallets);

    const cfg = WALLET_CONFIGS[walletKey];
    addTransaction({
      type: 'deposit',
      wallet: walletKey,
      amount: amt,
      currency: cfg.code,
      method: method || (cfg.isCrypto ? 'USDT (TRC-20)' : 'UPI Instant'),
      status: 'Completed',
      txid: txid || ('UPI-' + Array.from({length: 12}, () => Math.floor(Math.random()*10)).join(''))
    });

    return { success: true, newBalance: wallets[walletKey], formatted: formatCurrency(wallets[walletKey], walletKey) };
  };

  window.withdrawFunds = function(walletKey, amount, destinationData, method) {
    const amt = parseFloat(amount);
    if (isNaN(amt) || amt <= 0) return { success: false, message: 'Please enter a valid withdrawal amount.' };
    const wallets = getWallets();
    const current = wallets[walletKey] || 0;

    if (walletKey === 'demo') {
      return { success: false, message: 'Demo practice funds cannot be withdrawn. Switch to Real INR or USDT.' };
    }

    if (amt > current) {
      return { success: false, message: `Insufficient balance. You only have ${formatCurrency(current, walletKey)}.` };
    }

    // Limits check
    if (walletKey === 'real') {
      if (amt < LIMITS.inr.withdrawMin) {
        return { success: false, message: `Minimum withdrawal is ₹${LIMITS.inr.withdrawMin.toLocaleString('en-IN')}` };
      }
      if (amt > LIMITS.inr.withdrawMax) {
        return { success: false, message: `Maximum withdrawal is ₹${LIMITS.inr.withdrawMax.toLocaleString('en-IN')}` };
      }
    } else if (walletKey === 'usdt') {
      if (amt < LIMITS.usdt.withdrawMin) {
        return { success: false, message: `Minimum withdrawal is ${LIMITS.usdt.withdrawMin} USDT` };
      }
      if (amt > LIMITS.usdt.withdrawMax) {
        return { success: false, message: `Maximum withdrawal is ${LIMITS.usdt.withdrawMax} USDT` };
      }
    }

    wallets[walletKey] -= amt;
    saveWallets(wallets);

    const cfg = WALLET_CONFIGS[walletKey];
    const wthId = 'WTH-' + Math.random().toString(36).substr(2, 8).toUpperCase();
    const destName = typeof destinationData === 'object' ? destinationData.name : 'Player';
    const destStr = typeof destinationData === 'object' 
      ? (destinationData.accountNo ? `A/C: ${destinationData.accountNo} (${destinationData.ifsc || ''})` : `TRC20: ${destinationData.address || ''}`)
      : destinationData;

    // Add local transaction as Pending
    addTransaction({
      id: wthId,
      type: 'withdraw',
      wallet: walletKey,
      amount: amt,
      currency: cfg.code,
      method: method || (cfg.isCrypto ? 'USDT (TRC-20)' : 'IMPS Bank Transfer'),
      destination: `${destName} • ${destStr}`,
      status: 'Pending',
      timestamp: Date.now()
    });

    // Post to server backend for Admin Terminal sync
    try {
      const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
      const payload = {
        id: wthId,
        userId: session.id || '',
        username: session.username || (typeof destinationData === 'object' ? destinationData.name : 'Player'),
        email: session.email || '',
        wallet: walletKey,
        amount: amt,
        currency: cfg.code,
        method: method || (cfg.isCrypto ? 'USDT (TRC-20)' : 'IMPS Bank Transfer'),
        name: typeof destinationData === 'object' ? destinationData.name : 'Player',
        accountNo: typeof destinationData === 'object' ? (destinationData.accountNo || '') : '',
        ifsc: typeof destinationData === 'object' ? (destinationData.ifsc || '') : '',
        aadhaar: typeof destinationData === 'object' ? (destinationData.aadhaar || '') : '',
        mobile: typeof destinationData === 'object' ? (destinationData.mobile || '') : '',
        address: typeof destinationData === 'object' ? (destinationData.address || '') : ''
      };

      fetch('/api/withdraw-request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      }).then(r => r.json()).then(data => {
        if (data && data.withdrawal) {
          console.log('Withdrawal request sent to server:', data.withdrawal.id);
        }
      }).catch(err => {
        console.warn('Server sync error for withdrawal:', err);
      });
    } catch (e) {
      console.warn('Fetch error:', e);
    }

    return { success: true, newBalance: wallets[walletKey], formatted: formatCurrency(wallets[walletKey], walletKey), id: wthId };
  };

  // ── CANCEL WITHDRAWAL & REFUND BALANCE (BY USER) ─────────────
  window.cancelUserWithdrawal = async function(txId) {
    if (!txId) return;
    if (!confirm("Are you sure you want to cancel this pending withdrawal?\n\nThe full amount will be immediately refunded back to your account balance!")) return;

    const txs = getTransactions();
    const tx = txs.find(t => t.id === txId || t.orderId === txId);
    if (!tx) {
      if (typeof showToast === 'function') showToast('Transaction record not found.', 'error');
      return;
    }

    if (tx.status !== 'Pending') {
      if (typeof showToast === 'function') showToast('Only Pending withdrawals can be cancelled.', 'warning');
      return;
    }

    const amt = parseFloat(tx.amount || 0);
    const wKey = tx.wallet || 'real';

    // 1. Instantly refund the balance to user's wallet
    const wallets = getWallets();
    wallets[wKey] = (parseFloat(wallets[wKey]) || 0) + amt;
    saveWallets(wallets);

    // 2. Mark transaction as Cancelled by User (Refunded)
    tx.status = 'Cancelled (Refunded)';
    tx.cancelledByUser = true;
    tx.cancelledAt = Date.now();
    localStorage.setItem('ggwins_transactions', JSON.stringify(txs));

    // 3. Post to backend server to update server database.json
    try {
      const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
      await fetch('/api/cancel-withdrawal', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: txId,
          userId: session.id || '',
          username: session.username || '',
          amount: amt,
          wallet: wKey
        })
      });
    } catch(e) {}

    if (typeof showToast === 'function') {
      showToast(`✅ Withdrawal cancelled! ${formatCurrency(amt, wKey)} has been returned to your balance.`, 'success');
    }

    renderWalletModalContent();
    updateAllWalletDisplays();
  };

  window.refillDemoAccount = function() {
    const wallets = getWallets();
    wallets.demo = 10000.00;
    saveWallets(wallets);
    addTransaction({
      type: 'refill',
      wallet: 'demo',
      amount: 10000.00,
      currency: 'INR',
      method: 'Demo Practice Reset',
      status: 'Completed',
      txid: 'DEMO-INR-10K'
    });
    return formatCurrency(10000.00, 'demo');
  };

  // ── DYNAMIC UI SYNC ──────────────────────────────────────────
  window.updateAllWalletDisplays = function() {
    const wallets = getWallets();
    const activeKey = getActiveWalletKey();
    const activeCfg = WALLET_CONFIGS[activeKey] || WALLET_CONFIGS.demo;
    const activeBal = wallets[activeKey] !== undefined ? wallets[activeKey] : 10000;
    const formatted = formatCurrency(activeBal, activeKey);

    // Update standard balance target elements
    const targets = [
      'lobby-balance-val', 'lobby-balance-val-2', 'bal-display',
      'nav-balance-val', 'header-balance-val'
    ];
    targets.forEach(id => {
      const el = document.getElementById(id);
      if (el) {
        el.textContent = formatted;
        el.title = `${activeCfg.name} (${activeCfg.code})`;
      }
    });

    // Update currency prefixes
    document.querySelectorAll('.bet-currency').forEach(el => {
      el.textContent = activeCfg.symbol;
    });

    // Update dropdown items
    document.querySelectorAll('.account-picker-item').forEach(item => {
      const key = item.dataset.walletKey;
      if (key && WALLET_CONFIGS[key]) {
        item.classList.toggle('active', key === activeKey);
        const balEl = item.querySelector('.acc-picker-bal');
        if (balEl) balEl.textContent = formatCurrency(wallets[key] || 0, key);
      }
    });

    // Update active badges & names
    document.querySelectorAll('.wallet-active-badge').forEach(badge => {
      badge.textContent = activeCfg.badge;
      badge.style.backgroundColor = activeCfg.badgeColor;
    });
    document.querySelectorAll('.wallet-active-icon').forEach(icon => {
      icon.textContent = activeCfg.icon;
    });
    document.querySelectorAll('.wallet-active-name').forEach(name => {
      name.textContent = activeCfg.shortName;
    });

    // Update user avatar & username in game navbar if available
    try {
      const session = JSON.parse(localStorage.getItem('ggwins_session') || 'null');
      if (session) {
        document.querySelectorAll('.gnav-user-avatar').forEach(el => el.textContent = session.avatar || '🎮');
        document.querySelectorAll('.gnav-user-name').forEach(el => el.textContent = session.username || 'Player');
        document.querySelectorAll('.gnav-vip-badge').forEach(el => el.textContent = session.vipLevel || 'Bronze');
      }
    } catch(e) {}
  };

  // ── SOUND FX ENGINE (Web Audio API Synthesizer) ─────────────
  let audioCtx = null;
  let soundEnabled = localStorage.getItem('ggwins_sound_enabled') !== 'false';

  window.isSoundEnabled = function() { return soundEnabled; };
  window.toggleSound = function() {
    soundEnabled = !soundEnabled;
    localStorage.setItem('ggwins_sound_enabled', soundEnabled ? 'true' : 'false');
    document.querySelectorAll('.btn-sound-toggle').forEach(btn => {
      btn.textContent = soundEnabled ? '🔊' : '🔇';
      btn.title = soundEnabled ? 'Mute Game Sounds' : 'Unmute Game Sounds';
    });
    if (typeof showToast === 'function') {
      showToast(soundEnabled ? '🔊 Sound effects ON' : '🔇 Sound effects muted', 'info');
    }
    return soundEnabled;
  };

  window.playGameSound = function(type) {
    if (!soundEnabled) return;
    try {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      if (audioCtx.state === 'suspended') audioCtx.resume();

      const now = audioCtx.currentTime;

      if (type === 'click' || type === 'bet') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(900, now);
        osc.frequency.exponentialRampToValueAtTime(450, now + 0.05);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.05);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.05);
      } else if (type === 'win' || type === 'cashout') {
        // Melodic Victory Arpeggio: C5 -> E5 -> G5 -> C6
        const notes = [523.25, 659.25, 783.99, 1046.50];
        notes.forEach((freq, i) => {
          const osc = audioCtx.createOscillator();
          const gain = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + i * 0.08);
          gain.gain.setValueAtTime(0.18, now + i * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.005, now + i * 0.08 + 0.35);
          osc.connect(gain);
          gain.connect(audioCtx.destination);
          osc.start(now + i * 0.08);
          osc.stop(now + i * 0.08 + 0.35);
        });
      } else if (type === 'lose' || type === 'bust') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(220, now);
        osc.frequency.exponentialRampToValueAtTime(80, now + 0.28);
        gain.gain.setValueAtTime(0.14, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.28);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.28);
      } else if (type === 'bomb' || type === 'crash') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.exponentialRampToValueAtTime(30, now + 0.4);
        gain.gain.setValueAtTime(0.22, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.4);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.4);
      } else if (type === 'gem') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(987.77, now);
        osc.frequency.exponentialRampToValueAtTime(1318.51, now + 0.15);
        gain.gain.setValueAtTime(0.18, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.18);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.18);
      } else if (type === 'card') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1200, now);
        osc.frequency.exponentialRampToValueAtTime(600, now + 0.04);
        gain.gain.setValueAtTime(0.1, now);
        gain.gain.exponentialRampToValueAtTime(0.01, now + 0.04);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.04);
      } else if (type === 'tick' || type === 'roll') {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(450, now);
        gain.gain.setValueAtTime(0.07, now);
        gain.gain.exponentialRampToValueAtTime(0.005, now + 0.03);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start(now);
        osc.stop(now + 0.03);
      }
    } catch(e) {}
  };

  // ── UNIFIED PLAYER STATS & GAME HISTORY TRACKER ──────────────
  window.getGameHistory = function() {
    try {
      return JSON.parse(localStorage.getItem('ggwins_game_history')) || [];
    } catch(e) {
      return [];
    }
  };

  window.trackGameWager = function(gameName, wagerAmt, payoutAmt, won) {
    try {
      const wager = parseFloat(wagerAmt || 0);
      const payout = parseFloat(payoutAmt || 0);
      const netProfit = payout - wager;
      const orderId = 'BET-' + Math.floor(100000 + Math.random() * 900000);
      const curWallet = typeof getActiveWalletKey === 'function' ? getActiveWalletKey() : 'demo';

      // 1. Save game history record
      const gameHistory = JSON.parse(localStorage.getItem('ggwins_game_history') || '[]');
      gameHistory.unshift({
        orderId: orderId,
        game: gameName || 'Casino Game',
        wager: wager,
        payout: payout,
        profit: netProfit,
        won: !!won,
        wallet: curWallet,
        timestamp: Date.now()
      });
      localStorage.setItem('ggwins_game_history', JSON.stringify(gameHistory.slice(0, 100)));

      // 2. Update player session stats
      const session = JSON.parse(localStorage.getItem('ggwins_session') || 'null');
      if (!session) return;

      session.stats = session.stats || { gamesPlayed: 0, totalWagered: 0, totalWon: 0, biggestWin: 0, xp: 100 };
      session.stats.gamesPlayed = (session.stats.gamesPlayed || 0) + 1;
      session.stats.totalWagered = (parseFloat(session.stats.totalWagered) || 0) + wager;

      // ── PROGRESS 3X BONUS TASK ──
      try {
        const bTask = JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
        if (bTask && !bTask.completed && curWallet !== 'demo') {
          bTask.currentWagered = (parseFloat(bTask.currentWagered) || 0) + wager + (won ? payout : 0);
          if (bTask.currentWagered >= bTask.targetWager) {
            bTask.completed = true;
            bTask.completedAt = Date.now();
            if (typeof showToast === 'function') {
              showToast(`🎉 3× BONUS TASK COMPLETED! Target of ₹${bTask.targetWager.toFixed(2)} reached. All funds are now 100% UNLOCKED for withdrawal!`, 'success');
            }
            // Remove the completed task bar from website
            saveBonusTask(null);
          } else {
            localStorage.setItem('ggwins_bonus_task', JSON.stringify(bTask));
          }
        }
      } catch(e) {}

      if (won && payout > 0) {
        session.stats.totalWon = (parseFloat(session.stats.totalWon) || 0) + payout;
        if (payout > (session.stats.biggestWin || 0)) {
          session.stats.biggestWin = payout;
        }
      }

      // XP: 10 XP per 1 currency wagered
      const earnedXp = Math.floor(wager * 10);
      session.stats.xp = (session.stats.xp || 100) + earnedXp;

      // 🏆 Record Tournament Points: +100 per Win, +50 per Loss ONLY IF player is registered
      if (typeof window.recordTournamentMatch === 'function') {
        window.recordTournamentMatch(gameName, !!won);
      }

      // VIP Level auto-upgrade
      const totalW = session.stats.totalWagered;
      let newVip = 'Bronze';
      if (totalW >= 500000) newVip = 'Diamond';
      else if (totalW >= 200000) newVip = 'Platinum';
      else if (totalW >= 50000) newVip = 'Gold';
      else if (totalW >= 10000) newVip = 'Silver';

      session.vipLevel = newVip;
      localStorage.setItem('ggwins_vip_level', newVip);
      localStorage.setItem('ggwins_session', JSON.stringify(session));

      // Sync progress to backend server
      fetch('/api/update-user-progress', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          userId: session.id || '',
          username: session.username || '',
          stats: session.stats,
          vipLevel: session.vipLevel
        })
      }).catch(() => {});
    } catch(e) {}
  };

  // ── INJECT WALLET MODAL & CSS ─────────────────────────────────
  function injectWalletStyles() {
    if (document.getElementById('ggwins-wallet-styles')) return;
    const style = document.createElement('style');
    style.id = 'ggwins-wallet-styles';
    style.textContent = `
      /* Wallet Dropdown & Switcher */
      .wallet-switcher-container {
        position: relative;
        display: inline-flex;
        align-items: center;
      }
      .wallet-chip-btn {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(17, 24, 39, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 5px 12px;
        border-radius: 20px;
        color: #f8fafc;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
        user-select: none;
      }
      .wallet-chip-btn:hover {
        background: rgba(30, 41, 59, 0.95);
        border-color: rgba(0, 230, 118, 0.4);
        box-shadow: 0 0 12px rgba(0, 230, 118, 0.15);
      }
      .wallet-chip-btn .wallet-active-badge {
        font-size: 9px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        color: #000;
        letter-spacing: 0.05em;
      }
      .wallet-chip-btn .chevron-arrow {
        width: 12px;
        height: 12px;
        transition: transform 0.2s;
        opacity: 0.7;
      }
      .wallet-switcher-container.open .chevron-arrow {
        transform: rotate(180deg);
      }

      /* Account Picker Dropdown */
      .account-picker-dropdown {
        position: absolute;
        top: calc(100% + 8px);
        right: 0;
        width: 310px;
        background: #111827;
        border: 1px solid rgba(255, 255, 255, 0.14);
        border-radius: 14px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.8);
        padding: 10px;
        z-index: 2000;
        display: none;
        flex-direction: column;
        gap: 6px;
        animation: ddFadeIn 0.2s cubic-bezier(0.2, 0.8, 0.2, 1);
      }
      .wallet-switcher-container.open .account-picker-dropdown {
        display: flex;
      }
      @keyframes ddFadeIn {
        from { opacity: 0; transform: translateY(-8px) scale(0.98); }
        to { opacity: 1; transform: translateY(0) scale(1); }
      }
      .account-picker-title {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        padding: 4px 8px 6px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      .account-picker-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.2s;
      }
      .account-picker-item:hover {
        background: rgba(255, 255, 255, 0.07);
        border-color: rgba(255, 255, 255, 0.1);
      }
      .account-picker-item.active {
        background: rgba(0, 230, 118, 0.08);
        border-color: rgba(0, 230, 118, 0.4);
      }
      .acc-picker-left {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .acc-picker-icon { font-size: 22px; }
      .acc-picker-info {
        display: flex;
        flex-direction: column;
        gap: 2px;
        text-align: left;
      }
      .acc-picker-name {
        font-size: 13px;
        font-weight: 700;
        color: #f8fafc;
      }
      .acc-picker-type {
        font-size: 10px;
        color: #94a3b8;
        font-weight: 600;
      }
      .acc-picker-right {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 2px;
      }
      .acc-picker-bal {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 800;
        color: #00e676;
      }
      .acc-active-check {
        font-size: 10px;
        color: #00e676;
        font-weight: 800;
      }
      .acc-dropdown-actions {
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        padding-top: 8px;
        margin-top: 4px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
      }
      .btn-acc-action {
        padding: 9px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid transparent;
        font-family: 'Space Grotesk', sans-serif;
      }
      .btn-acc-action.dep {
        background: #00e676;
        color: #000;
      }
      .btn-acc-action.dep:hover { filter: brightness(1.1); transform: translateY(-1px); }
      .btn-acc-action.wth {
        background: rgba(255, 255, 255, 0.06);
        color: #f8fafc;
        border-color: rgba(255, 255, 255, 0.12);
      }
      .btn-acc-action.wth:hover { background: rgba(255, 255, 255, 0.12); transform: translateY(-1px); }

      /* Full Wallet Modal */
      #ggwins-wallet-modal {
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.85);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        z-index: 99999;
        display: none;
        align-items: center;
        justify-content: center;
        padding: 16px;
      }
      #ggwins-wallet-modal.active {
        display: flex;
        animation: modalOverlayIn 0.2s ease;
      }
      @keyframes modalOverlayIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      .wallet-modal-card {
        width: 100%;
        max-width: 560px;
        background: #0f172a;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        box-shadow: 0 25px 70px rgba(0, 0, 0, 0.9);
        overflow: hidden;
        display: flex;
        flex-direction: column;
        max-height: 92vh;
        animation: modalSlideUp 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      }
      @keyframes modalSlideUp {
        from { transform: translateY(20px) scale(0.96); opacity: 0; }
        to { transform: translateY(0) scale(1); opacity: 1; }
      }
      .wm-header {
        padding: 16px 22px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #090e17;
      }
      .wm-title-group {
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .wm-title {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 18px;
        font-weight: 800;
        color: #f8fafc;
      }
      .wm-close {
        background: none;
        border: none;
        color: #94a3b8;
        font-size: 20px;
        cursor: pointer;
        padding: 4px;
        border-radius: 8px;
        transition: color 0.2s;
      }
      .wm-close:hover { color: #fff; }

      /* Modal Navigation Tabs */
      .wm-tabs {
        display: flex;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        background: rgba(0, 0, 0, 0.3);
      }
      .wm-tab {
        flex: 1;
        text-align: center;
        padding: 13px 8px;
        font-size: 13px;
        font-weight: 700;
        color: #94a3b8;
        cursor: pointer;
        border-bottom: 2px solid transparent;
        transition: all 0.2s;
      }
      .wm-tab:hover { color: #f8fafc; background: rgba(255,255,255,0.02); }
      .wm-tab.active {
        color: #00e676;
        border-bottom-color: #00e676;
        background: rgba(0, 230, 118, 0.05);
      }

      /* Modal Body */
      .wm-body {
        padding: 20px 22px;
        overflow-y: auto;
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      .wm-section-label {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        display: flex;
        justify-content: space-between;
      }

      /* Account Selector Pills inside Modal */
      .wm-account-pills {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 8px;
      }
      .wm-account-pill {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 10px 8px;
        cursor: pointer;
        text-align: center;
        transition: all 0.2s;
      }
      .wm-account-pill:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 255, 255, 0.15);
      }
      .wm-account-pill.active {
        border-color: #00e676;
        background: rgba(0, 230, 118, 0.08);
        box-shadow: 0 0 16px rgba(0, 230, 118, 0.15);
      }
      .wm-pill-icon { font-size: 20px; margin-bottom: 4px; }
      .wm-pill-name { font-size: 12px; font-weight: 700; color: #f8fafc; }
      .wm-pill-bal { font-family: 'Space Grotesk', sans-serif; font-size: 12px; font-weight: 800; color: #00e676; margin-top: 2px; }

      /* Method Cards */
      .wm-methods-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 8px;
      }
      .wm-method-card {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 10px 12px;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.2s;
        position: relative;
      }
      .wm-method-card:hover { background: rgba(255, 255, 255, 0.06); }
      .wm-method-card.active {
        border-color: #00e676;
        background: rgba(0, 230, 118, 0.08);
      }
      .wm-method-card.in-progress {
        opacity: 0.85;
      }
      .wm-method-card.in-progress:hover {
        opacity: 1;
        border-color: rgba(245, 158, 11, 0.4);
      }
      .wm-method-icon { font-size: 22px; flex-shrink: 0; }
      .wm-method-info { text-align: left; flex: 1; min-width: 0; }
      .wm-method-name { font-size: 12px; font-weight: 700; color: #f8fafc; }
      .wm-method-sub { font-size: 10px; color: #94a3b8; }
      .wm-method-badge {
        display: inline-flex;
        align-items: center;
        gap: 3px;
        font-size: 9px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        padding: 2px 6px;
        border-radius: 4px;
        white-space: nowrap;
      }
      .wm-method-badge.instant {
        background: rgba(0, 230, 118, 0.15);
        color: #00e676;
        border: 1px solid rgba(0, 230, 118, 0.3);
      }
      .wm-method-badge.progress {
        background: rgba(245, 158, 11, 0.16);
        color: #fbbf24;
        border: 1px solid rgba(245, 158, 11, 0.35);
      }
      .wm-badge-dot {
        width: 5px;
        height: 5px;
        border-radius: 50%;
        background: #fbbf24;
        display: inline-block;
        animation: wmPulse 1.4s infinite;
      }
      @keyframes wmPulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.3; transform: scale(0.7); }
      }

      /* Presets */
      .wm-presets {
        display: flex;
        gap: 6px;
        margin-top: 8px;
        flex-wrap: wrap;
      }
      .wm-preset-btn {
        flex: 1;
        min-width: 58px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 6px;
        padding: 6px;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        cursor: pointer;
        transition: all 0.15s;
      }
      .wm-preset-btn:hover {
        background: rgba(255, 255, 255, 0.1);
        color: #fff;
        border-color: #00e676;
      }

      /* Inputs */
      .wm-input-group {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .wm-input-label {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.04em;
      }
      .wm-input-box {
        display: flex;
        align-items: center;
        background: #090e17;
        border: 1.5px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 0 14px;
        transition: border-color 0.2s;
      }
      .wm-input-box:focus-within {
        border-color: #00e676;
        box-shadow: 0 0 0 2px rgba(0, 230, 118, 0.2);
      }
      .wm-input {
        flex: 1;
        background: none;
        border: none;
        color: #f8fafc;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 14px;
        font-weight: 700;
        padding: 10px 0;
        outline: none;
      }
      .wm-input-sym {
        font-weight: 700;
        color: #00e676;
        margin-right: 8px;
        font-size: 15px;
      }
      .wm-input-suffix {
        font-size: 11px;
        font-weight: 700;
        color: #94a3b8;
      }

      /* Form Grid */
      .wm-form-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
      }

      /* UPI / QR Box */
      .wm-upi-box {
        background: #090e17;
        border: 1px dashed rgba(0, 230, 118, 0.3);
        border-radius: 12px;
        padding: 12px 14px;
        display: flex;
        align-items: center;
        gap: 14px;
      }
      .wm-qr-placeholder {
        width: 64px;
        height: 64px;
        background: #fff;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4px;
        flex-shrink: 0;
      }
      .wm-qr-placeholder svg { width: 100%; height: 100%; }
      .wm-upi-details { flex: 1; overflow: hidden; }
      .wm-upi-label { font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; margin-bottom: 2px; }
      .wm-upi-id { font-family: monospace; font-size: 12px; font-weight: 700; color: #00e676; margin-bottom: 4px; }
      .wm-btn-copy {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 6px;
        color: #f8fafc;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 8px;
        cursor: pointer;
        transition: all 0.2s;
      }
      .wm-btn-copy:hover { background: #00e676; color: #000; }

      /* Action Buttons */
      .wm-action-btn {
        width: 100%;
        padding: 13px;
        border-radius: 12px;
        background: linear-gradient(135deg, #00e676, #00c96a);
        color: #000;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 15px;
        font-weight: 800;
        border: none;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(0, 230, 118, 0.3);
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
      }
      .wm-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 230, 118, 0.45);
        filter: brightness(1.05);
      }
      .wm-action-btn:active { transform: translateY(0); }

      /* History List */
      .wm-history-list {
        display: flex;
        flex-direction: column;
        gap: 8px;
        max-height: 380px;
        overflow-y: auto;
        padding-right: 4px;
      }
      .wm-tx-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
      }
      .wm-tx-left { display: flex; align-items: center; gap: 10px; }
      .wm-tx-icon {
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 14px;
        flex-shrink: 0;
      }
      .wm-tx-icon.deposit { background: rgba(0, 230, 118, 0.15); color: #00e676; }
      .wm-tx-icon.withdraw { background: rgba(239, 83, 80, 0.15); color: #ef5350; }
      .wm-tx-icon.refill { background: rgba(124, 77, 255, 0.15); color: #7c4dff; }
      .wm-tx-title { font-size: 12px; font-weight: 700; color: #f8fafc; }
      .wm-tx-meta { font-size: 10px; color: #94a3b8; }
      .wm-tx-right { text-align: right; }
      .wm-tx-amt { font-family: 'Space Grotesk', sans-serif; font-size: 13px; font-weight: 800; }
      .wm-tx-amt.positive { color: #00e676; }
      .wm-tx-amt.negative { color: #ef5350; }
      .wm-tx-status {
        font-size: 9px;
        font-weight: 700;
        padding: 2px 5px;
        border-radius: 4px;
        display: inline-block;
      }
      .wm-tx-status.completed { color: #00e676; background: rgba(0, 230, 118, 0.12); }
      .wm-tx-status.pending { color: #fbbf24; background: rgba(245, 158, 11, 0.15); }
      .wm-tx-status.rejected { color: #ef4444; background: rgba(239, 68, 68, 0.15); }

      /* History Tabs & Filters */
      .wm-filter-bar {
        display: flex;
        gap: 6px;
        margin-bottom: 10px;
        background: rgba(0,0,0,0.25);
        padding: 3px;
        border-radius: 8px;
      }
      .wm-filter-btn {
        flex: 1;
        padding: 5px 8px;
        border: none;
        border-radius: 6px;
        background: transparent;
        color: #94a3b8;
        font-family: 'Space Grotesk', sans-serif;
        font-size: 11px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s;
      }
      .wm-filter-btn.active {
        background: rgba(255, 255, 255, 0.12);
        color: #fff;
      }
      .wm-filter-btn.active.green {
        background: rgba(0, 230, 118, 0.2);
        color: #00e676;
      }
      .wm-filter-btn.active.red {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
      }
      .wm-order-badge {
        font-family: monospace;
        font-size: 10px;
        font-weight: 800;
        color: #ffd700;
        background: rgba(255, 215, 0, 0.12);
        border: 1px solid rgba(255, 215, 0, 0.3);
        padding: 1px 6px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        transition: all 0.15s;
      }
      .wm-order-badge:hover {
        background: rgba(255, 215, 0, 0.25);
        transform: scale(1.02);
      }
      .wm-utr-badge {
        font-family: monospace;
        font-size: 10px;
        color: #38bdf8;
        background: rgba(56, 189, 248, 0.12);
        padding: 1px 5px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        gap: 3px;
        cursor: pointer;
      }
      .wm-utr-badge:hover { background: rgba(56, 189, 248, 0.22); }
      .wm-game-hist-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px 12px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 10px;
        transition: all 0.2s;
      }
      .wm-game-hist-card:hover {
        background: rgba(255, 255, 255, 0.06);
        border-color: rgba(255, 255, 255, 0.12);
      }
      .wm-game-hist-card.win {
        border-left: 3px solid #00e676;
      }
      .wm-game-hist-card.loss {
        border-left: 3px solid #ef4444;
      }
      .wm-result-tag {
        font-size: 10px;
        font-weight: 800;
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
      }
      .wm-result-tag.win {
        background: rgba(0, 230, 118, 0.15);
        color: #00e676;
        border: 1px solid rgba(0, 230, 118, 0.3);
      }
      .wm-result-tag.loss {
        background: rgba(239, 68, 68, 0.15);
        color: #ef4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
      }
      .wm-stats-mini-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        margin-bottom: 12px;
      }
      .wm-mini-stat {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 7px 4px;
        text-align: center;
      }
      .wm-mini-stat-lbl {
        font-size: 9px;
        font-weight: 700;
        color: #94a3b8;
        text-transform: uppercase;
      }
      .wm-mini-stat-val {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 12px;
        font-weight: 800;
        margin-top: 2px;
      }

      /* QR Hover & Action Buttons */
      .wm-qr-placeholder {
        position: relative;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
      }
      .wm-qr-placeholder:hover {
        transform: scale(1.04);
        box-shadow: 0 0 16px rgba(124, 77, 255, 0.5);
      }
      .wm-qr-hover-hint {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        background: rgba(15, 23, 42, 0.85);
        color: #ffd700;
        font-size: 8px;
        font-weight: 800;
        padding: 2px 0;
        text-align: center;
        text-transform: uppercase;
        border-radius: 0 0 6px 6px;
        pointer-events: none;
      }
      .wm-btn-rot {
        background: rgba(124, 77, 255, 0.15);
        border: 1px solid rgba(124, 77, 255, 0.4);
        border-radius: 6px;
        color: #a78bfa;
        font-size: 10px;
        font-weight: 700;
        padding: 2px 7px;
        cursor: pointer;
        transition: all 0.2s;
      }
      .wm-btn-rot:hover {
        background: rgba(124, 77, 255, 0.3);
        color: #fff;
      }
      .wm-btn-enlarge {
        background: rgba(255, 215, 0, 0.12);
        border: 1px solid rgba(255, 215, 0, 0.35);
        border-radius: 6px;
        color: #ffd700;
        font-size: 10px;
        font-weight: 700;
        padding: 3px 8px;
        cursor: pointer;
        transition: all 0.2s;
      }
      .wm-btn-enlarge:hover {
        background: rgba(255, 215, 0, 0.25);
        transform: translateY(-1px);
      }

      /* QR Lightbox / Fullscreen Popup */
      .gg-lightbox-overlay {
        display: none;
        position: fixed;
        inset: 0;
        background: rgba(0, 0, 0, 0.88);
        backdrop-filter: blur(10px);
        z-index: 100000;
        align-items: center;
        justify-content: center;
        padding: 16px;
      }
      .gg-lightbox-overlay.show {
        display: flex;
      }
      .gg-lightbox-modal {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 2px solid #ffd700;
        border-radius: 20px;
        padding: 22px 20px 18px;
        width: min(380px, 94vw);
        box-shadow: 0 0 50px rgba(255, 215, 0, 0.25), 0 20px 60px rgba(0,0,0,0.85);
        position: relative;
        font-family: 'Space Grotesk', sans-serif;
        text-align: center;
        animation: wmPopIn 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
      }
      @keyframes wmPopIn {
        0% { transform: scale(0.85) translateY(20px); opacity: 0; }
        100% { transform: scale(1) translateY(0); opacity: 1; }
      }
      .gg-lightbox-close {
        position: absolute;
        top: 12px;
        right: 14px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        color: #94a3b8;
        font-size: 16px;
        padding: 4px 10px;
        cursor: pointer;
        line-height: 1;
        transition: all 0.2s;
      }
      .gg-lightbox-close:hover {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
        border-color: #ef4444;
      }
      .gg-lightbox-header {
        margin-bottom: 12px;
      }
      .gg-lightbox-title {
        font-size: 17px;
        font-weight: 800;
        color: #f8fafc;
      }
      .gg-lightbox-sub {
        font-size: 11px;
        color: #94a3b8;
        margin-top: 2px;
      }
      .gg-lightbox-img-box {
        background: #ffffff;
        border: 2px solid #7c4dff;
        border-radius: 14px;
        padding: 10px;
        margin: 0 auto 12px;
        width: min(250px, 72vw);
        aspect-ratio: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
      }
      .gg-lightbox-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        border-radius: 8px;
        user-select: all;
      }
      .gg-lightbox-badge {
        position: absolute;
        top: 8px;
        right: 8px;
        background: #7c4dff;
        color: #fff;
        font-size: 10px;
        font-weight: 800;
        padding: 3px 8px;
        border-radius: 999px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
      }
      .gg-lightbox-upi-row {
        background: #090e17;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 8px 12px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 12px;
      }
      .gg-lightbox-upi-info {
        text-align: left;
        overflow: hidden;
      }
      .gg-lightbox-upi-lbl {
        font-size: 9px;
        color: #94a3b8;
        font-weight: 700;
        text-transform: uppercase;
      }
      .gg-lightbox-upi-txt {
        font-family: monospace;
        font-size: 12px;
        font-weight: 700;
        color: #00e676;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .gg-lightbox-btn-copy {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 6px;
        color: #f8fafc;
        font-size: 11px;
        font-weight: 700;
        padding: 5px 10px;
        cursor: pointer;
        white-space: nowrap;
        transition: all 0.2s;
      }
      .gg-lightbox-btn-copy:hover {
        background: #00e676;
        color: #000;
      }
      .gg-lightbox-actions {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-bottom: 10px;
      }
      .gg-lightbox-btn-dl {
        background: linear-gradient(135deg, #00e676, #00c96a);
        color: #000;
        border: none;
        border-radius: 8px;
        padding: 9px;
        font-size: 12px;
        font-weight: 800;
        text-decoration: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
      }
      .gg-lightbox-btn-dl:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 230, 118, 0.35);
      }
      .gg-lightbox-btn-next {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 8px;
        color: #f8fafc;
        padding: 9px;
        font-size: 12px;
        font-weight: 700;
        cursor: pointer;
        transition: all 0.2s;
      }
      .gg-lightbox-btn-next:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: #ffd700;
      }
      .gg-lightbox-tip {
        font-size: 10px;
        color: #94a3b8;
        line-height: 1.4;
      }
    `;
    document.head.appendChild(style);
  }

  function injectWalletModalHTML() {
    if (document.getElementById('ggwins-wallet-modal')) return;

    const modal = document.createElement('div');
    modal.id = 'ggwins-wallet-modal';
    modal.innerHTML = `
      <div class="wallet-modal-card">
        <div class="wm-header">
          <div class="wm-title-group">
            <span style="font-size:22px">💳</span>
            <div class="wm-title">GG Wins Wallet &amp; Accounts</div>
          </div>
          <button class="wm-close" onclick="closeWalletModal()">✕</button>
        </div>

        <div class="wm-tabs">
          <div class="wm-tab active" data-tab="deposit" onclick="switchWalletModalTab('deposit')">⬇️ Deposit</div>
          <div class="wm-tab" data-tab="withdraw" onclick="switchWalletModalTab('withdraw')">⬆️ Withdraw</div>
          <div class="wm-tab" data-tab="payment-history" onclick="switchWalletModalTab('payment-history')">💳 Payment History</div>
          <div class="wm-tab" data-tab="game-history" onclick="switchWalletModalTab('game-history')">🏆 Game History</div>
          <div class="wm-tab" data-tab="accounts" onclick="switchWalletModalTab('accounts')">🔄 Accounts</div>
        </div>

        <div class="wm-body" id="wm-body-content">
          <!-- Dynamically rendered -->
        </div>
      </div>
    `;
    document.body.appendChild(modal);

    modal.addEventListener('click', e => {
      if (e.target === modal) closeWalletModal();
    });
  }

  let activeModalTab = 'deposit';
  let depositTargetAccount = 'real';
  let depositMethod = 'upi';
  let withdrawSourceAccount = 'real';

  window.openWalletModal = function(tab) {
    // Only allow logged-in users to access deposit/withdraw
    const session = typeof getSession === 'function' ? getSession() : JSON.parse(localStorage.getItem('ggwins_session') || 'null');
    if (!session) {
      // Close wallet if accidentally open
      const existingModal = document.getElementById('ggwins-wallet-modal');
      if (existingModal) existingModal.classList.remove('active');
      // Show login modal
      if (typeof openModal === 'function') {
        openModal('login');
      }
      // Show toast
      if (typeof showToast === 'function') {
        showToast('⚠️ Please sign in or register to deposit or withdraw.', 'error');
      }
      return;
    }
    injectWalletStyles();
    injectWalletModalHTML();
    if (tab) activeModalTab = tab;
    const modal = document.getElementById('ggwins-wallet-modal');
    if (modal) {
      modal.classList.add('active');
      renderWalletModalContent();
    }
  };

  window.closeWalletModal = function() {
    const modal = document.getElementById('ggwins-wallet-modal');
    if (modal) modal.classList.remove('active');
  };

  // QR Data & Rotator — cycles through 3 payment QR codes
  const QR_DATA = [
    { src: 'assets/qr1.jpg', upi: 'amdasrarbasha-1@oksbi' },
    { src: 'assets/qr2.jpg', upi: 'kabilanr2210@okhdfcbank' },
    { src: 'assets/qr3.jpg', upi: 'txchem@slc' }
  ];

  function getQRAsset(path) {
    if (window.location.pathname.includes('/games/')) {
      return '../' + path;
    }
    return path;
  }

  window.openQRLightbox = function(customIdx) {
    let idx = 0;
    if (customIdx !== undefined) {
      idx = customIdx;
    } else {
      const img = document.getElementById('wm-qr-img');
      if (img && img.dataset.idx !== undefined) idx = parseInt(img.dataset.idx);
    }
    idx = Math.max(0, Math.min(2, isNaN(idx) ? 0 : idx));

    let overlay = document.getElementById('gg-qr-lightbox-overlay');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'gg-qr-lightbox-overlay';
      overlay.className = 'gg-lightbox-overlay';
      document.body.appendChild(overlay);
    }

    const item = QR_DATA[idx];
    const src = getQRAsset(item.src);

    overlay.innerHTML = `
      <div class="gg-lightbox-modal" onclick="event.stopPropagation()">
        <button class="gg-lightbox-close" onclick="closeQRLightbox()">✕</button>
        <div class="gg-lightbox-header">
          <div class="gg-lightbox-title">📸 Scan &amp; Pay via UPI</div>
          <div class="gg-lightbox-sub">Option ${idx + 1} of 3 • Tap or Long-Press to Save / Screenshot</div>
        </div>

        <div class="gg-lightbox-img-box">
          <img src="${src}" alt="UPI QR Code" id="gg-lightbox-img" class="gg-lightbox-img">
          <div class="gg-lightbox-badge">${idx + 1}/3</div>
        </div>

        <div class="gg-lightbox-upi-row">
          <div class="gg-lightbox-upi-info">
            <div class="gg-lightbox-upi-lbl">Pay to UPI ID:</div>
            <div class="gg-lightbox-upi-txt" id="lightbox-upi-txt">${item.upi}</div>
          </div>
          <button class="gg-lightbox-btn-copy" onclick="copyLightboxUPI('${item.upi}', this)">📋 Copy</button>
        </div>

        <div class="gg-lightbox-actions">
          <a href="${src}" download="ggwins-upi-qr-${idx + 1}.jpg" class="gg-lightbox-btn-dl">
            📥 Save / Download
          </a>
          <button class="gg-lightbox-btn-next" onclick="rotateLightboxQR(${idx})">
            🔄 Next QR (${(idx + 1) % 3 + 1}/3)
          </button>
        </div>

        <div class="gg-lightbox-tip">
          💡 <strong>Tip:</strong> Take a screenshot or tap download to pay from your phone using GPay, PhonePe, Paytm, or BHIM.
        </div>
      </div>
    `;

    overlay.onclick = closeQRLightbox;
    overlay.classList.add('show');
  };

  window.closeQRLightbox = function() {
    const overlay = document.getElementById('gg-qr-lightbox-overlay');
    if (overlay) overlay.classList.remove('show');
  };

  window.rotateLightboxQR = function(currentIdx) {
    const nextIdx = (currentIdx + 1) % 3;
    openQRLightbox(nextIdx);
    // Also sync the main wallet modal QR
    const img = document.getElementById('wm-qr-img');
    const badge = document.getElementById('wm-qr-badge');
    const upiLabel = document.getElementById('wm-qr-upi-id');
    const rotBtn = document.getElementById('wm-rot-btn-text');
    if (img) {
      img.dataset.idx = nextIdx;
      img.src = getQRAsset(QR_DATA[nextIdx].src);
      if (badge) badge.textContent = (nextIdx + 1) + '/3';
      if (upiLabel) upiLabel.textContent = QR_DATA[nextIdx].upi;
      if (rotBtn) rotBtn.textContent = '🔄 Switch QR (' + (nextIdx + 1) + '/3)';
    }
  };

  window.copyLightboxUPI = function(upi, btn) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(upi);
    }
    btn.textContent = 'Copied! ✓';
    btn.style.background = '#00e676';
    btn.style.color = '#000';
    setTimeout(() => {
      btn.textContent = '📋 Copy';
      btn.style.background = '';
      btn.style.color = '';
    }, 1500);
  };

  let selectedPaymentQR = 1;

  window.selectPaymentQR = function(num) {
    selectedPaymentQR = Math.max(1, Math.min(3, parseInt(num) || 1));
    const idx = selectedPaymentQR - 1;
    const img = document.getElementById('wm-qr-img');
    const badge = document.getElementById('wm-qr-badge');
    const upiLabel = document.getElementById('wm-qr-upi-id');
    const rotBtn = document.getElementById('wm-rot-btn-text');
    if (img) {
      img.dataset.idx = idx;
      img.src = getQRAsset(QR_DATA[idx].src);
    }
    if (badge) badge.textContent = (idx + 1) + '/3';
    if (upiLabel) upiLabel.textContent = QR_DATA[idx].upi;
    if (rotBtn) rotBtn.textContent = '🔄 Switch QR (' + (idx + 1) + '/3)';

    // Update UI tabs
    [1, 2, 3].forEach(n => {
      const tab = document.getElementById(`qr-tab-${n}`);
      if (tab) {
        if (n === selectedPaymentQR) {
          tab.style.background = 'rgba(0,230,118,0.2)';
          tab.style.borderColor = '#00e676';
          const title = tab.querySelector('.qr-tab-title');
          if (title) title.style.color = '#00e676';
        } else {
          tab.style.background = 'rgba(255,255,255,0.04)';
          tab.style.borderColor = 'rgba(255,255,255,0.1)';
          const title = tab.querySelector('.qr-tab-title');
          if (title) title.style.color = '#fff';
        }
      }
    });
  };

  window.rotateQR = function() {
    let idx = (selectedPaymentQR % 3) + 1;
    window.selectPaymentQR(idx);
  };

  window.switchWalletModalTab = function(tab) {
    activeModalTab = tab;
    document.querySelectorAll('.wm-tab').forEach(t => {
      t.classList.toggle('active', t.dataset.tab === tab);
    });
    renderWalletModalContent();
  };

  window.setDepositTargetAccount = function(key) {
    depositTargetAccount = key;
    if (key === 'usdt') depositMethod = 'trc20';
    else depositMethod = 'upi';
    renderWalletModalContent();
  };

  window.setDepositMethod = function(method) {
    depositMethod = method;
    if (['netbanking', 'paytm', 'card'].includes(method)) {
      if (typeof showToast === 'function') {
        showToast('⏳ This method is under progress. Please use UPI / QR Code.', 'warning');
      }
    }
    renderWalletModalContent();
  };

  window.setWithdrawSourceAccount = function(key) {
    withdrawSourceAccount = key;
    renderWalletModalContent();
  };

  window.setModalAmount = function(val) {
    const input = document.getElementById('wm-amount-input');
    if (input) {
      input.value = val;
      if (typeof updateLiveBonusPreview === 'function') {
        updateLiveBonusPreview();
      }
    }
  };

  // ── EXECUTE DEPOSIT ──────────────────────────────────────────
  window.executeModalDeposit = function() {
    const amtInput = document.getElementById('wm-amount-input');
    const amt = parseFloat(amtInput ? amtInput.value : 0);

    if (depositTargetAccount === 'demo') {
      const formatted = refillDemoAccount();
      showDepositSuccess(`Demo account balance refilled to <strong>${formatted}</strong>! 🎉`);
      return;
    }

    // Validation
    if (depositTargetAccount === 'real') {
      if (isNaN(amt) || amt < LIMITS.inr.depositMin || amt > LIMITS.inr.depositMax) {
        alert(`Deposit amount must be between ₹${LIMITS.inr.depositMin.toLocaleString('en-IN')} and ₹${LIMITS.inr.depositMax.toLocaleString('en-IN')}.`);
        return;
      }
    } else if (depositTargetAccount === 'usdt') {
      if (isNaN(amt) || amt < LIMITS.usdt.depositMin || amt > LIMITS.usdt.depositMax) {
        alert(`Deposit amount must be between ${LIMITS.usdt.depositMin} USDT and ${LIMITS.usdt.depositMax} USDT.`);
        return;
      }
    }

    const btn = document.getElementById('wm-submit-btn');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Submitting Deposit Request... ⏳';
    }

    const methodName = (depositMethod === 'netbanking') ? 'Net Banking / IMPS'
                      : (depositMethod === 'paytm') ? 'Paytm Wallet'
                      : (depositMethod === 'card') ? 'RuPay / Debit Card'
                      : (depositMethod === 'trc20') ? 'USDT (TRC-20)'
                      : (depositMethod === 'erc20') ? 'USDT (ERC-20)'
                      : 'UPI Instant (GPay / PhonePe / Paytm)';

    const utrVal = document.getElementById('wm-utr-input')?.value?.trim() || '';
    const senderNameVal = document.getElementById('wm-sender-name')?.value?.trim() || (localStorage.getItem('ggwins_username') || 'Player');

    // Validate UTR for UPI method — must be exactly 12 digits
    if (depositMethod === 'upi' && !/^\d{12}$/.test(utrVal)) {
      alert('⚠️ Please enter a valid 12-digit UTR number to confirm your payment. You can find it in your payment app under transaction history.');
      if (btn) { btn.disabled = false; btn.textContent = '⚡ Submit Deposit Request'; }
      return;
    }

    let bonusAmt = 0;
    let couponUsed = appliedCouponCode;
    if (couponUsed && COUPONS[couponUsed] && depositTargetAccount === 'real') {
      const c = COUPONS[couponUsed];
      if (amt >= c.minDeposit) {
        bonusAmt = c.calcBonus(amt);
        // Create 3x wagering task
        const task = {
          coupon: couponUsed,
          depositAmt: amt,
          bonusAmt: bonusAmt,
          targetWager: bonusAmt * 3,
          currentWagered: 0,
          completed: false,
          createdAt: Date.now()
        };
        saveBonusTask(task);
        markCouponUsed(couponUsed);
      }
    }

    createPendingDeposit(depositTargetAccount, amt, methodName, utrVal, senderNameVal, couponUsed, bonusAmt, selectedPaymentQR);

    let successMsg = `Deposit request of <strong>${formatCurrency(amt, depositTargetAccount)}</strong>`;
    if (bonusAmt > 0) {
      successMsg += ` + <strong>₹${bonusAmt.toFixed(2)} Bonus (${couponUsed})</strong> (Total Credited: <strong>₹${(amt + bonusAmt).toFixed(2)}</strong>)`;
      successMsg += `<br><br><span style="color:#ffd700;font-weight:700">🎯 3× Wagering Task Created:</span> Earn/Wager ₹${(bonusAmt * 3).toFixed(2)} across any games to unlock full withdrawal!`;
    }
    successMsg += ` submitted for <strong>${senderNameVal}</strong>. Await host approval in the admin panel. ⏳`;

    showDepositSuccess(successMsg);
    appliedCouponCode = null;
    if (btn) { btn.disabled = false; btn.textContent = 'Submit Deposit Request'; }
  };

  // ── EXECUTE WITHDRAWAL ───────────────────────────────────────
  window.executeModalWithdraw = function() {
    if (withdrawSourceAccount === 'demo') {
      alert('Demo practice money cannot be withdrawn. Switch to Real INR or USDT.');
      return;
    }

    const amtInput = document.getElementById('wm-amount-input');
    const amt = parseFloat(amtInput ? amtInput.value : 0);
    const isUsdt = withdrawSourceAccount === 'usdt';

    // Check account fields
    let destData = {};
    if (!isUsdt) {
      const name = document.getElementById('wm-w-name')?.value.trim();
      const accountNo = document.getElementById('wm-w-acc')?.value.trim();
      const ifsc = document.getElementById('wm-w-ifsc')?.value.trim().toUpperCase();
      const aadhaar = document.getElementById('wm-w-aadhaar')?.value.trim();
      const mobile = document.getElementById('wm-w-mobile')?.value.trim();

      // Check 3x Bonus Task requirement
    try {
      const bTask = JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
      if (bTask && !bTask.completed) {
        const remaining = Math.max(0, bTask.targetWager - bTask.currentWagered);
        const pct = Math.min(100, (bTask.currentWagered / bTask.targetWager) * 100).toFixed(1);
        alert(`⚠️ BONUS WITHDRAWAL TASK INCOMPLETE\n\nYou claimed a promo bonus of ₹${bTask.bonusAmt.toFixed(2)} with coupon [${bTask.coupon}].\n\nRule: You must wager/earn 3× the bonus amount (₹${bTask.targetWager.toFixed(2)}) before withdrawing.\n\n📊 Current Progress: ₹${bTask.currentWagered.toFixed(2)} / ₹${bTask.targetWager.toFixed(2)} (${pct}%)\n🔒 Need ₹${remaining.toFixed(2)} more in game activity to unlock withdrawal!`);
        return;
      }
    } catch(e) {}

    if (!name) { alert('Please enter your Full Name (as per Bank Account).'); return; }
      if (!accountNo || accountNo.length < 9) { alert('Please enter a valid Bank Account Number (minimum 9 digits).'); return; }
      if (!ifsc || ifsc.length < 11) { alert('Please enter a valid 11-digit IFSC Code (e.g., HDFC0001234, SBIN0004567).'); return; }
      if (!aadhaar || aadhaar.replace(/\D/g, '').length < 12) { alert('Please enter a valid 12-digit Aadhaar Number.'); return; }
      if (!mobile || mobile.replace(/\D/g, '').length < 10) { alert('Please enter a valid 10-digit Mobile Number.'); return; }

      // Limits check
      if (amt < LIMITS.inr.withdrawMin || amt > LIMITS.inr.withdrawMax) {
        alert(`Withdrawal amount must be between ₹${LIMITS.inr.withdrawMin.toLocaleString('en-IN')} and ₹${LIMITS.inr.withdrawMax.toLocaleString('en-IN')}.`);
        return;
      }

      destData = { name, accountNo, ifsc, aadhaar, mobile };
    } else {
      const name = document.getElementById('wm-w-name')?.value.trim();
      const address = document.getElementById('wm-w-address')?.value.trim();
      const mobile = document.getElementById('wm-w-mobile')?.value.trim();

      if (!name) { alert('Please enter your Name.'); return; }
      if (!address || address.length < 25) { alert('Please enter a valid USDT TRC-20 Wallet Address.'); return; }
      if (!mobile || mobile.length < 10) { alert('Please enter your Mobile Number.'); return; }

      if (amt < LIMITS.usdt.withdrawMin || amt > LIMITS.usdt.withdrawMax) {
        alert(`Withdrawal amount must be between ${LIMITS.usdt.withdrawMin} USDT and ${LIMITS.usdt.withdrawMax} USDT.`);
        return;
      }

      destData = { name, address, mobile };
    }

    const btn = document.getElementById('wm-submit-btn');
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Processing Withdrawal... ⏳';
    }

    setTimeout(() => {
      const res = withdrawFunds(withdrawSourceAccount, amt, destData, isUsdt ? 'USDT (TRC-20)' : 'IMPS Bank Transfer');
      if (res.success) {
        showDepositSuccess(`Withdrawal request of <strong>${formatCurrency(amt, withdrawSourceAccount)}</strong> submitted successfully for <strong>${destData.name}</strong> (${destData.accountNo ? 'A/C: ' + destData.accountNo : 'USDT TRC20'}).<br><br><span style="color:#f59e0b;font-weight:700">⚠️ Note: It may take 5-7 business days to receive funds in your bank account.</span>`);
      } else {
        alert(res.message);
        if (btn) { btn.disabled = false; btn.textContent = 'Submit Withdrawal Request'; }
      }
    }, 1000);
  };

  function showDepositSuccess(msg) {
    const body = document.getElementById('wm-body-content');
    if (!body) return;
    body.innerHTML = `
      <div style="text-align:center;padding:26px 10px;animation:modalSlideUp 0.3s ease">
        <div style="font-size:52px;margin-bottom:12px">🎉</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-size:22px;font-weight:900;color:#00e676;margin-bottom:8px">Transaction Completed!</div>
        <p style="font-size:13.5px;color:#94a3b8;margin-bottom:24px;line-height:1.6">${msg}</p>
        <div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
          <button class="wm-action-btn" style="max-width:200px" onclick="closeWalletModal()">Back to Games 🎮</button>
          <button class="btn-acc-action wth" style="padding:12px 18px" onclick="switchWalletModalTab('history')">View Receipt 📜</button>
        </div>
      </div>
    `;
    updateAllWalletDisplays();
  }

  function renderWalletModalContent() {
    const body = document.getElementById('wm-body-content');
    if (!body) return;
    const wallets = getWallets();
    const activeKey = getActiveWalletKey();

    if (activeModalTab === 'deposit') {
      const isUsdt = depositTargetAccount === 'usdt';
      const isDemo = depositTargetAccount === 'demo';
      const cfg = WALLET_CONFIGS[depositTargetAccount];

      body.innerHTML = `
        
        ${(function(){
          const task = getBonusTask();
          if (!task || task.completed) return '';
          const pct = Math.min(100, (task.currentWagered / task.targetWager) * 100).toFixed(1);
          return `
            <div style="background:linear-gradient(135deg,rgba(124,77,255,0.15),rgba(0,230,118,0.1));border:1.5px solid #ffd700;border-radius:14px;padding:12px 14px;margin-bottom:12px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                <div style="display:flex;align-items:center;gap:6px">
                  <span style="font-size:16px">🎯</span>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12.5px;font-weight:800;color:#fff">
                    Active Bonus Task (3× Wagering Requirement)
                  </span>
                </div>
                <span style="font-size:10.5px;font-weight:800;padding:2px 8px;border-radius:999px;background:#ffd700;color:#000">
                  🔒 LOCKED
                </span>
              </div>
              <div style="font-size:11.5px;color:#94a3b8;margin-bottom:6px">
                Claimed <strong>₹${task.bonusAmt.toFixed(2)} Bonus</strong> (${task.coupon}). Target: Wager/Earn <strong>₹${task.targetWager.toFixed(2)}</strong>.
              </div>
              <!-- Progress Bar -->
              <div style="background:rgba(0,0,0,0.5);border-radius:999px;height:10px;overflow:hidden;position:relative;margin-bottom:4px">
                <div style="background:linear-gradient(90deg,#ffd700,#00e676);height:100%;width:${pct}%;transition:width 0.4s ease"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:11px;color:#cbd5e1;font-weight:700">
                <span>Progress: ₹${task.currentWagered.toFixed(2)} / ₹${task.targetWager.toFixed(2)}</span>
                <span style="color:#ffd700">${pct}% Remaining</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding-top:6px;border-top:1px dashed rgba(255,255,255,0.15)">
                <span style="font-size:11px;color:#94a3b8">Want to withdraw immediately?</span>
                <button onclick="openCancelBonusTaskModal()" style="background:rgba(239,68,68,0.2);border:1px solid #ef4444;border-radius:6px;padding:4px 10px;color:#ef4444;font-size:11px;font-weight:700;cursor:pointer;transition:all 0.2s" onmouseover="this.style.background='rgba(239,68,68,0.35)'" onmouseout="this.style.background='rgba(239,68,68,0.2)'">
                  🚫 Cancel Task (-Bonus &amp; -8% Fee)
                </button>
              </div>
            </div>
          `;
        })()}

        <div>
          <div class="wm-section-label">
            <span>1. Choose Account to Deposit Into</span>
            <span style="color:#00e676">Current: ${formatCurrency(wallets[depositTargetAccount], depositTargetAccount)}</span>
          </div>
          <div class="wm-account-pills">
            <div class="wm-account-pill ${depositTargetAccount === 'real' ? 'active' : ''}" onclick="setDepositTargetAccount('real')">
              <div class="wm-pill-icon">💵</div>
              <div class="wm-pill-name">Real INR</div>
              <div class="wm-pill-bal">${formatCurrency(wallets.real, 'real')}</div>
            </div>
            <div class="wm-account-pill ${depositTargetAccount === 'usdt' ? 'active' : ''}" onclick="setDepositTargetAccount('usdt')">
              <div class="wm-pill-icon">🪙</div>
              <div class="wm-pill-name">Deposited USDT</div>
              <div class="wm-pill-bal">${formatCurrency(wallets.usdt, 'usdt')}</div>
            </div>
            <div class="wm-account-pill ${depositTargetAccount === 'demo' ? 'active' : ''}" onclick="setDepositTargetAccount('demo')">
              <div class="wm-pill-icon">🎮</div>
              <div class="wm-pill-name">Demo Practice</div>
              <div class="wm-pill-bal">${formatCurrency(wallets.demo, 'demo')}</div>
            </div>
          </div>
        </div>

        ${isDemo ? `
          <div style="background:rgba(124,77,255,0.1);border:1px solid rgba(124,77,255,0.3);border-radius:12px;padding:22px;text-align:center">
            <div style="font-size:38px;margin-bottom:8px">🔄</div>
            <div style="font-family:'Space Grotesk',sans-serif;font-size:18px;font-weight:800;color:#f8fafc;margin-bottom:6px">Refill Demo Account</div>
            <p style="font-size:13px;color:#94a3b8;margin-bottom:18px">Reset your Demo practice balance to ₹50,000.00 INR at zero cost anytime.</p>
            <button class="wm-action-btn" id="wm-submit-btn" onclick="executeModalDeposit()" style="background:linear-gradient(135deg,#7c4dff,#651fff);color:#fff">
              Refill to ₹50,000.00 Demo INR
            </button>
          </div>
        ` : `
          <div>
            <div class="wm-section-label">2. Select Payment Method</div>
            <div class="wm-methods-grid">
              ${!isUsdt ? `
                <div class="wm-method-card ${depositMethod === 'upi' ? 'active' : ''}" onclick="setDepositMethod('upi')">
                  <div class="wm-method-icon">📱</div>
                  <div class="wm-method-info">
                    <div style="display:flex;align-items:center;justify-content:space-between;gap:4px">
                      <span class="wm-method-name">UPI / QR Code</span>
                      <span class="wm-method-badge instant">⚡ Instant</span>
                    </div>
                    <div class="wm-method-sub">GPay, PhonePe, Paytm, BHIM</div>
                  </div>
                </div>
                <div class="wm-method-card in-progress ${depositMethod === 'netbanking' ? 'active' : ''}" onclick="setDepositMethod('netbanking')">
                  <div class="wm-method-icon">🏦</div>
                  <div class="wm-method-info">
                    <div style="display:flex;align-items:center;justify-content:space-between;gap:4px">
                      <span class="wm-method-name">Net Banking / IMPS</span>
                      <span class="wm-method-badge progress"><span class="wm-badge-dot"></span>⏳ In Progress</span>
                    </div>
                    <div class="wm-method-sub">All Major Indian Banks</div>
                  </div>
                </div>
                <div class="wm-method-card in-progress ${depositMethod === 'paytm' ? 'active' : ''}" onclick="setDepositMethod('paytm')">
                  <div class="wm-method-icon">👛</div>
                  <div class="wm-method-info">
                    <div style="display:flex;align-items:center;justify-content:space-between;gap:4px">
                      <span class="wm-method-name">Paytm Wallet</span>
                      <span class="wm-method-badge progress"><span class="wm-badge-dot"></span>⏳ In Progress</span>
                    </div>
                    <div class="wm-method-sub">Instant Wallet Transfer</div>
                  </div>
                </div>
                <div class="wm-method-card in-progress ${depositMethod === 'card' ? 'active' : ''}" onclick="setDepositMethod('card')">
                  <div class="wm-method-icon">💳</div>
                  <div class="wm-method-info">
                    <div style="display:flex;align-items:center;justify-content:space-between;gap:4px">
                      <span class="wm-method-name">RuPay / Debit Card</span>
                      <span class="wm-method-badge progress"><span class="wm-badge-dot"></span>⏳ In Progress</span>
                    </div>
                    <div class="wm-method-sub">Visa, Mastercard, RuPay</div>
                  </div>
                </div>
              ` : `
                <div class="wm-method-card ${depositMethod === 'trc20' ? 'active' : ''}" onclick="setDepositMethod('trc20')">
                  <div class="wm-method-icon">⚡</div>
                  <div class="wm-method-info">
                    <div style="display:flex;align-items:center;justify-content:space-between;gap:4px">
                      <span class="wm-method-name">USDT (TRC-20)</span>
                      <span class="wm-method-badge instant">⚡ Active</span>
                    </div>
                    <div class="wm-method-sub">Fast, lowest network fees</div>
                  </div>
                </div>
                <div class="wm-method-card ${depositMethod === 'erc20' ? 'active' : ''}" onclick="setDepositMethod('erc20')">
                  <div class="wm-method-icon">🔷</div>
                  <div class="wm-method-info">
                    <div style="display:flex;align-items:center;justify-content:space-between;gap:4px">
                      <span class="wm-method-name">USDT (ERC-20)</span>
                      <span class="wm-method-badge instant">⚡ Active</span>
                    </div>
                    <div class="wm-method-sub">Ethereum Mainnet</div>
                  </div>
                </div>
              `}
            </div>
          </div>

          ${!isUsdt && depositMethod !== 'upi' ? `
            <div style="background:rgba(245,158,11,0.08);border:1px dashed rgba(245,158,11,0.35);border-radius:10px;padding:12px;text-align:center;margin-top:10px">
              <div style="display:flex;align-items:center;justify-content:center;gap:6px;font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:800;color:#fbbf24;margin-bottom:4px">
                <span>⏳ Gateway Under Progress</span>
              </div>
              <div style="font-size:11px;color:#94a3b8;margin-bottom:8px">This payment gateway is currently undergoing integration upgrade. Please use <strong>UPI / QR Code</strong> for instant deposit crediting!</div>
              <button onclick="setDepositMethod('upi')" style="background:linear-gradient(135deg,#7c4dff,#651fff);color:#fff;border:none;border-radius:6px;padding:5px 12px;font-size:11px;font-weight:700;cursor:pointer">
                ⚡ Use Instant UPI / QR Code
              </button>
            </div>
          ` : ''}

          ${!isUsdt && depositMethod === 'upi' ? `
            <div class="wm-upi-box" id="wm-qr-rotator-box">
              <div class="wm-qr-placeholder" id="wm-qr-img-wrap" onclick="openQRLightbox()" title="Click to pop up & save QR image" style="border:2px solid #7c4dff;border-radius:12px;overflow:hidden;background:#fff;padding:6px;position:relative">
                <img id="wm-qr-img" src="${getQRAsset('assets/qr1.jpg')}" alt="QR Code" data-idx="0" style="width:100%;height:100%;object-fit:contain;display:block;border-radius:8px">
                <div style="position:absolute;top:5px;right:6px;background:#7c4dff;color:#fff;font-size:9px;font-weight:800;padding:2px 6px;border-radius:999px" id="wm-qr-badge">1/3</div>
                <div class="wm-qr-hover-hint">🔍 View / Save</div>
              </div>
              <div class="wm-upi-details">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:2px">
                  <span class="wm-upi-label">Pay to UPI ID:</span>
                  <button class="wm-btn-rot" id="wm-rot-btn-text" onclick="rotateQR()" title="Switch to next UPI QR">🔄 Switch QR (1/3)</button>
                </div>
                <div class="wm-upi-id" id="wm-qr-upi-id">amdasrarbasha-1@oksbi</div>
                <div style="display:flex;gap:6px;margin-top:6px;flex-wrap:wrap">
                  <button class="wm-btn-copy" id="wm-copy-upi-btn" onclick="(function(btn){var ids=['amdasrarbasha-1@oksbi','kabilanr2210@okhdfcbank','txchem@slc'];var idx=parseInt(document.getElementById('wm-qr-img').dataset.idx||0);navigator.clipboard&&navigator.clipboard.writeText(ids[idx]);btn.textContent='Copied! ✓';setTimeout(()=>btn.textContent='Copy UPI ID',1500);})(this)">Copy UPI ID</button>
                  <button class="wm-btn-enlarge" onclick="openQRLightbox()">🔍 Pop up &amp; Save QR</button>
                </div>
              </div>
            </div>
          ` : ''}

          ${isUsdt ? `
            <div class="wm-upi-box">
              <div class="wm-qr-placeholder">
                <svg viewBox="0 0 24 24" fill="#000"><path d="M2 2h8v8H2zm2 2v4h4V4zm-2 8h8v8H2zm2 2v4h4v-4zm8-12h8v8h-8zm2 2v4h4V4zm0 8h2v2h-2zm2 2h2v2h-2zm2-2h2v2h-2zm-4 4h2v2h-2zm2 2h2v2h-2zm2-2h2v2h-2zm-2-6h2v2h-2z"/></svg>
              </div>
              <div class="wm-upi-details">
                <div class="wm-upi-label">Your USDT (TRC-20) Deposit Address:</div>
                <div class="wm-upi-id" style="font-size:11px">TJkw89vQN45xV7R3bYpQe98M2xZ1L0</div>
                <button class="wm-btn-copy" onclick="navigator.clipboard && navigator.clipboard.writeText('TJkw89vQN45xV7R3bYpQe98M2xZ1L0'); this.textContent='Copied! ✓'; setTimeout(()=>this.textContent='Copy Address', 1500)">Copy Address</button>
              </div>
            </div>
          ` : ''}

          <div>
            <div class="wm-section-label">
              <span>3. Enter Deposit Amount</span>
              <span style="color:#00e676">Min: ${isUsdt ? '10 ₮' : '₹500'} | Max: ${isUsdt ? '5,000 ₮' : '₹1,00,000'}</span>
            </div>
            <div class="wm-input-box">
              <span class="wm-input-sym">${cfg.symbol}</span>
              <input type="number" class="wm-input" id="wm-amount-input" value="${isUsdt ? '100.00' : (appliedCouponCode && COUPONS[appliedCouponCode] ? COUPONS[appliedCouponCode].minDeposit : '1000.00')}" min="${isUsdt ? 10 : 500}" max="${isUsdt ? 5000 : 100000}" step="${isUsdt ? 5 : 100}" oninput="updateLiveBonusPreview()">
              <span class="wm-input-suffix">${cfg.code}</span>
            </div>
            <div class="wm-presets">
              ${!isUsdt ? `
                <button class="wm-preset-btn" onclick="setModalAmount(500)">+₹500</button>
                <button class="wm-preset-btn" onclick="setModalAmount(1000)">+₹1,000</button>
                <button class="wm-preset-btn" onclick="setModalAmount(2500)">+₹2,500</button>
                <button class="wm-preset-btn" onclick="setModalAmount(5000)">+₹5,000</button>
                <button class="wm-preset-btn" onclick="setModalAmount(10000)">+₹10,000</button>
                <button class="wm-preset-btn" onclick="setModalAmount(50000)">+₹50,000</button>
                <button class="wm-preset-btn" onclick="setModalAmount(100000)">+₹1,00,000</button>
              ` : `
                <button class="wm-preset-btn" onclick="setModalAmount(25)">+25 ₮</button>
                <button class="wm-preset-btn" onclick="setModalAmount(50)">+50 ₮</button>
                <button class="wm-preset-btn" onclick="setModalAmount(100)">+100 ₮</button>
                <button class="wm-preset-btn" onclick="setModalAmount(250)">+250 ₮</button>
                <button class="wm-preset-btn" onclick="setModalAmount(500)">+500 ₮</button>
                <button class="wm-preset-btn" onclick="setModalAmount(1000)">+1,000 ₮</button>
              `}
            </div>
          </div>

          
          ${!isUsdt && (!isCouponUsed('GG1675') || !isCouponUsed('INSTANT1500')) ? `
          <!-- ── PROMO COUPONS & BONUS BOX ── -->
          <div style="background:linear-gradient(135deg,rgba(255,215,0,0.08),rgba(0,230,118,0.06));border:1.5px dashed rgba(255,215,0,0.4);border-radius:14px;padding:14px;margin-top:12px">
            <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
              <div style="display:flex;align-items:center;gap:6px;font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:800;color:#ffd700">
                <span>🎟️</span>
                <span>Promo Coupons &amp; Deposit Bonus</span>
              </div>
              <span style="font-size:11px;font-weight:700;color:#00e676;background:rgba(0,230,118,0.15);padding:2px 8px;border-radius:999px">NEW USERS</span>
            </div>

            <!-- Quick Coupon Cards (Only show unused coupons) -->
            <div style="display:grid;grid-template-columns:${!isCouponUsed('GG1675') && !isCouponUsed('INSTANT1500') ? '1fr 1fr' : '1fr'};gap:8px;margin-bottom:10px">
              ${!isCouponUsed('GG1675') ? `
                <div onclick="applyPromoCoupon('GG1675', true)" style="background:rgba(0,0,0,0.3);border:1px solid ${appliedCouponCode==='GG1675'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:pointer;transition:all 0.2s;box-shadow:${appliedCouponCode==='GG1675'?'0 0 15px rgba(0,230,118,0.3)':''}">
                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:#ffd700">GG1675</span>
                    <span style="font-size:10px;font-weight:800;color:#00e676">UP TO 100%</span>
                  </div>
                  <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹1675+ (More you pay = Higher bonus)</div>
                </div>
              ` : ''}

              ${!isCouponUsed('INSTANT1500') ? `
                <div onclick="applyPromoCoupon('INSTANT1500', true)" style="background:rgba(0,0,0,0.3);border:1px solid ${appliedCouponCode==='INSTANT1500'?'#00e676':'rgba(255,255,255,0.15)'};border-radius:10px;padding:8px 10px;cursor:pointer;transition:all 0.2s;box-shadow:${appliedCouponCode==='INSTANT1500'?'0 0 15px rgba(0,230,118,0.3)':''}">
                  <div style="display:flex;justify-content:space-between;align-items:center">
                    <span style="font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;color:#ffd700">INSTANT1500</span>
                    <span style="font-size:10px;font-weight:800;color:#00e676">⚡ +₹1500 FLAT</span>
                  </div>
                  <div style="font-size:11px;color:#94a3b8;margin-top:2px">Deposit ₹2500 to get instant ₹1500 bonus</div>
                </div>
              ` : ''}
            </div>

            <!-- Coupon Input & Apply -->
            <div style="display:flex;gap:6px">
              <input type="text" id="wm-coupon-input" placeholder="Enter coupon code (e.g. GG1675)" value="${appliedCouponCode||''}" style="flex:1;background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.2);border-radius:8px;padding:8px 12px;color:#fff;font-size:12px;text-transform:uppercase;font-weight:700">
              <button onclick="applyPromoCoupon(document.getElementById('wm-coupon-input').value, true)" style="background:linear-gradient(135deg,#00e676,#00b0ff);border:none;border-radius:8px;padding:8px 14px;color:#000;font-family:'Space Grotesk',sans-serif;font-size:12px;font-weight:900;cursor:pointer">Apply</button>
              ${appliedCouponCode ? `<button onclick="removePromoCoupon()" style="background:rgba(239,68,68,0.2);border:1px solid #ef4444;border-radius:8px;padding:8px 10px;color:#ef4444;font-size:12px;cursor:pointer">✕</button>` : ''}
            </div>

            <div id="wm-coupon-live-preview">
              ${appliedCouponCode && COUPONS[appliedCouponCode] ? (function(){
                const c = COUPONS[appliedCouponCode];
                const amtInput = document.getElementById('wm-amount-input');
                const curAmt = parseFloat(amtInput?.value || c.minDeposit);
                const bonusAmt = c.calcBonus(curAmt);
                const totalCredit = curAmt + bonusAmt;
                const targetWager = bonusAmt * 3;
                return `
                  <div style="margin-top:10px;background:rgba(0,230,118,0.1);border:1px solid #00e676;border-radius:10px;padding:10px;animation:modalSlideUp 0.3s ease">
                    <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                      <span style="color:#94a3b8">Base Deposit:</span>
                      <span style="font-weight:700;color:#fff">₹${curAmt.toFixed(2)}</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:12px;margin-bottom:4px">
                      <span style="color:#00e676;font-weight:700">Coupon Bonus (${c.code}):</span>
                      <span style="font-weight:900;color:#00e676">+₹${bonusAmt.toFixed(2)} (${c.getPercent(curAmt)}%)</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;font-size:13px;border-top:1px dashed rgba(255,255,255,0.2);padding-top:4px;margin-top:4px">
                      <span style="color:#ffd700;font-weight:800">Total Credited Balance:</span>
                      <span style="font-weight:900;color:#ffd700">₹${totalCredit.toFixed(2)}</span>
                    </div>
                    <div style="margin-top:8px;font-size:11px;color:#94a3b8;background:rgba(0,0,0,0.3);border-radius:6px;padding:6px 8px;line-height:1.4">
                      🎯 <strong>3× Bonus Task Rule:</strong> You must wager/earn <strong>3× the bonus amount (₹${targetWager.toFixed(2)})</strong> across games before bonus withdrawal is unlocked.
                    </div>
                  </div>
                `;
              })() : ''}
            </div>
          </div>
          ` : ''}

          ${!isUsdt && depositMethod === 'upi' ? `
            <div style="margin-top:12px;background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:12px">
              <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
                <span class="wm-input-label" style="margin:0;font-size:11px;font-weight:800;color:#ffd700">
                  🎯 Which QR Code did you pay with?
                </span>
                <span style="font-size:10px;font-weight:700;color:#94a3b8">Tap 1, 2, or 3</span>
              </div>
              <div style="display:grid;grid-template-columns:repeat(3, 1fr);gap:8px">
                <div class="qr-select-tab" id="qr-tab-1" onclick="selectPaymentQR(1)" style="background:${selectedPaymentQR===1?'rgba(0,230,118,0.2)':'rgba(255,255,255,0.04)'};border:1.5px solid ${selectedPaymentQR===1?'#00e676':'rgba(255,255,255,0.1)'};border-radius:10px;padding:9px 6px;text-align:center;cursor:pointer;transition:all 0.2s">
                  <div class="qr-tab-title" style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:900;color:${selectedPaymentQR===1?'#00e676':'#fff'}">QR 1</div>
                  <div style="font-size:9.5px;color:#94a3b8;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">amdasrarbasha-1</div>
                </div>
                <div class="qr-select-tab" id="qr-tab-2" onclick="selectPaymentQR(2)" style="background:${selectedPaymentQR===2?'rgba(0,230,118,0.2)':'rgba(255,255,255,0.04)'};border:1.5px solid ${selectedPaymentQR===2?'#00e676':'rgba(255,255,255,0.1)'};border-radius:10px;padding:9px 6px;text-align:center;cursor:pointer;transition:all 0.2s">
                  <div class="qr-tab-title" style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:900;color:${selectedPaymentQR===2?'#00e676':'#fff'}">QR 2</div>
                  <div style="font-size:9.5px;color:#94a3b8;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">kabilanr2210</div>
                </div>
                <div class="qr-select-tab" id="qr-tab-3" onclick="selectPaymentQR(3)" style="background:${selectedPaymentQR===3?'rgba(0,230,118,0.2)':'rgba(255,255,255,0.04)'};border:1.5px solid ${selectedPaymentQR===3?'#00e676':'rgba(255,255,255,0.1)'};border-radius:10px;padding:9px 6px;text-align:center;cursor:pointer;transition:all 0.2s">
                  <div class="qr-tab-title" style="font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:900;color:${selectedPaymentQR===3?'#00e676':'#fff'}">QR 3</div>
                  <div style="font-size:9.5px;color:#94a3b8;margin-top:2px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">txchem@slc</div>
                </div>
              </div>
            </div>
          ` : ''}

          <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px">
            <div class="wm-input-group">
              <label class="wm-input-label">Your Name</label>
              <div class="wm-input-box" style="padding:0 10px">
                <input type="text" class="wm-input" id="wm-sender-name" placeholder="Player Name" value="${localStorage.getItem('ggwins_username') || 'Player'}">
              </div>
            </div>
            <div class="wm-input-group">
              <label class="wm-input-label">${isUsdt ? 'Tx Hash (Optional)' : (depositMethod === 'upi' ? '12-digit UTR Number <span style="color:#f87171;font-weight:700">*Required</span>' : '12-digit UTR (Optional)')}</label>
              <div class="wm-input-box" style="padding:0 10px">
                <input type="text" class="wm-input" id="wm-utr-input" placeholder="${isUsdt ? 'TxID' : 'e.g. 423189012345'}" ${depositMethod === 'upi' ? 'required maxlength="12"' : ''}>
              </div>
            </div>
          </div>

          <button class="wm-action-btn" id="wm-submit-btn" onclick="executeModalDeposit()" style="margin-top:14px">
            <span>⚡</span> Submit Deposit Request (${cfg.symbol})
          </button>
        `}
      `;
    }

    else if (activeModalTab === 'withdraw') {
      const isUsdt = withdrawSourceAccount === 'usdt';
      const cfg = WALLET_CONFIGS[withdrawSourceAccount];
      const maxAmt = wallets[withdrawSourceAccount] || 0;

      body.innerHTML = `
        
        ${(function(){
          const task = getBonusTask();
          if (!task || task.completed) return '';
          const pct = Math.min(100, (task.currentWagered / task.targetWager) * 100).toFixed(1);
          return `
            <div style="background:linear-gradient(135deg,rgba(124,77,255,0.15),rgba(0,230,118,0.1));border:1.5px solid #ffd700;border-radius:14px;padding:12px 14px;margin-bottom:12px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
                <div style="display:flex;align-items:center;gap:6px">
                  <span style="font-size:16px">🎯</span>
                  <span style="font-family:'Space Grotesk',sans-serif;font-size:12.5px;font-weight:800;color:#fff">
                    Active Bonus Task (3× Wagering Requirement)
                  </span>
                </div>
                <span style="font-size:10.5px;font-weight:800;padding:2px 8px;border-radius:999px;background:#ffd700;color:#000">
                  🔒 LOCKED
                </span>
              </div>
              <div style="font-size:11.5px;color:#94a3b8;margin-bottom:6px">
                Claimed <strong>₹${task.bonusAmt.toFixed(2)} Bonus</strong> (${task.coupon}). Target: Wager/Earn <strong>₹${task.targetWager.toFixed(2)}</strong>.
              </div>
              <!-- Progress Bar -->
              <div style="background:rgba(0,0,0,0.5);border-radius:999px;height:10px;overflow:hidden;position:relative;margin-bottom:4px">
                <div style="background:linear-gradient(90deg,#ffd700,#00e676);height:100%;width:${pct}%;transition:width 0.4s ease"></div>
              </div>
              <div style="display:flex;justify-content:space-between;font-size:11px;color:#cbd5e1;font-weight:700">
                <span>Progress: ₹${task.currentWagered.toFixed(2)} / ₹${task.targetWager.toFixed(2)}</span>
                <span style="color:#ffd700">${pct}% Remaining</span>
              </div>
              <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding-top:6px;border-top:1px dashed rgba(255,255,255,0.15)">
                <span style="font-size:11px;color:#94a3b8">Want to withdraw immediately?</span>
                <button onclick="openCancelBonusTaskModal()" style="background:rgba(239,68,68,0.2);border:1px solid #ef4444;border-radius:6px;padding:4px 10px;color:#ef4444;font-size:11px;font-weight:700;cursor:pointer;transition:all 0.2s" onmouseover="this.style.background='rgba(239,68,68,0.35)'" onmouseout="this.style.background='rgba(239,68,68,0.2)'">
                  🚫 Cancel Task (-Bonus &amp; -8% Fee)
                </button>
              </div>
            </div>
          `;
        })()}

        ${(function(){
          const txs = getTransactions();
          const pendingWths = txs.filter(t => t.type === 'withdraw' && t.status === 'Pending');
          if (!pendingWths.length) return '';
          return `
            <div style="background:rgba(245,158,11,0.1);border:1.5px solid #f59e0b;border-radius:14px;padding:12px 14px;margin-bottom:12px">
              <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
                <span style="font-size:12.5px;font-weight:800;color:#ffd700">⏳ You have ${pendingWths.length} Pending Withdrawal(s)</span>
                <span style="font-size:10px;font-weight:800;background:#f59e0b;color:#000;padding:2px 6px;border-radius:4px">PROCESSING</span>
              </div>
              <div style="display:flex;flex-direction:column;gap:6px">
                ${pendingWths.map(pw => `
                  <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(0,0,0,0.3);padding:8px 10px;border-radius:8px;font-size:12px">
                    <div>
                      <strong style="color:#fff">${formatCurrency(pw.amount, pw.wallet)}</strong>
                      <span style="color:#94a3b8;font-size:11px"> · ${pw.method || 'IMPS'}</span>
                    </div>
                    <button onclick="cancelUserWithdrawal('${pw.id}')" style="background:rgba(239,68,68,0.25);border:1px solid #ef4444;color:#ef4444;border-radius:6px;padding:4px 10px;font-size:11px;font-weight:800;cursor:pointer">
                      ✕ Cancel &amp; Refund
                    </button>
                  </div>
                `).join('')}
              </div>
            </div>
          `;
        })()}

        <div>
          <div class="wm-section-label">
            <span>1. Select Account to Withdraw From</span>
            <span style="color:#00e676">Available: ${formatCurrency(maxAmt, withdrawSourceAccount)}</span>
          </div>
          <div class="wm-account-pills" style="grid-template-columns: 1fr 1fr">
            <div class="wm-account-pill ${withdrawSourceAccount === 'real' ? 'active' : ''}" onclick="setWithdrawSourceAccount('real')">
              <div class="wm-pill-icon">💵</div>
              <div class="wm-pill-name">Real INR</div>
              <div class="wm-pill-bal">${formatCurrency(wallets.real, 'real')}</div>
            </div>
            <div class="wm-account-pill ${withdrawSourceAccount === 'usdt' ? 'active' : ''}" onclick="setWithdrawSourceAccount('usdt')">
              <div class="wm-pill-icon">🪙</div>
              <div class="wm-pill-name">Deposited USDT</div>
              <div class="wm-pill-bal">${formatCurrency(wallets.usdt, 'usdt')}</div>
            </div>
          </div>
        </div>

        <div>
          <div class="wm-section-label">
            <span>2. Withdrawal Amount</span>
            <span style="color:#00e676">Min: ${isUsdt ? '20 ₮' : '₹1,500'} | Max: ${isUsdt ? '10,000 ₮' : '₹2,00,000'}</span>
          </div>
          <div class="wm-input-box">
            <span class="wm-input-sym">${cfg.symbol}</span>
            <input type="number" class="wm-input" id="wm-amount-input" value="${Math.max(isUsdt ? 20 : 1500, Math.min(isUsdt ? 100 : 5000, maxAmt)).toFixed(2)}" min="${isUsdt ? 20 : 1500}" max="${isUsdt ? 10000 : 200000}">
            <span class="wm-input-suffix">${cfg.code}</span>
          </div>
          <div class="wm-presets">
            <button class="wm-preset-btn" onclick="setModalAmount(${(maxAmt * 0.25).toFixed(2)})">25%</button>
            <button class="wm-preset-btn" onclick="setModalAmount(${(maxAmt * 0.50).toFixed(2)})">50%</button>
            <button class="wm-preset-btn" onclick="setModalAmount(${(maxAmt * 0.75).toFixed(2)})">75%</button>
            <button class="wm-preset-btn" onclick="setModalAmount(${maxAmt.toFixed(2)})" style="color:#00e676;border-color:#00e676">MAX</button>
          </div>
        </div>

        <div>
          <div class="wm-section-label">3. Bank &amp; Identity Verification Details (Required)</div>
          
          ${!isUsdt ? `
            <div style="display:flex;flex-direction:column;gap:10px">
              <div class="wm-form-grid">
                <div class="wm-input-group">
                  <label class="wm-input-label">Full Name (as per Bank)</label>
                  <div class="wm-input-box">
                    <input type="text" class="wm-input" id="wm-w-name" placeholder="e.g. Rahul Sharma">
                  </div>
                </div>
                <div class="wm-input-group">
                  <label class="wm-input-label">Mobile Number</label>
                  <div class="wm-input-box">
                    <input type="tel" class="wm-input" id="wm-w-mobile" placeholder="10-digit mobile" maxlength="10">
                  </div>
                </div>
              </div>

              <div class="wm-form-grid">
                <div class="wm-input-group">
                  <label class="wm-input-label">Bank Account Number</label>
                  <div class="wm-input-box">
                    <input type="text" class="wm-input" id="wm-w-acc" placeholder="Enter Account No">
                  </div>
                </div>
                <div class="wm-input-group">
                  <label class="wm-input-label">IFSC Code</label>
                  <div class="wm-input-box">
                    <input type="text" class="wm-input" id="wm-w-ifsc" placeholder="e.g. HDFC0001234" maxlength="11" style="text-transform:uppercase">
                  </div>
                </div>
              </div>

              <div class="wm-input-group">
                <label class="wm-input-label">Aadhaar Number (12-Digit)</label>
                <div class="wm-input-box">
                  <input type="text" class="wm-input" id="wm-w-aadhaar" placeholder="XXXX-XXXX-XXXX" maxlength="14">
                </div>
              </div>
            </div>
          ` : `
            <div style="display:flex;flex-direction:column;gap:10px">
              <div class="wm-form-grid">
                <div class="wm-input-group">
                  <label class="wm-input-label">Full Name</label>
                  <div class="wm-input-box">
                    <input type="text" class="wm-input" id="wm-w-name" placeholder="Enter your Name">
                  </div>
                </div>
                <div class="wm-input-group">
                  <label class="wm-input-label">Mobile Number</label>
                  <div class="wm-input-box">
                    <input type="tel" class="wm-input" id="wm-w-mobile" placeholder="10-digit mobile" maxlength="10">
                  </div>
                </div>
              </div>

              <div class="wm-input-group">
                <label class="wm-input-label">USDT TRC-20 Wallet Address</label>
                <div class="wm-input-box">
                  <input type="text" class="wm-input" id="wm-w-address" placeholder="Paste your USDT TRC-20 Address (starts with T...)">
                </div>
              </div>
            </div>
          `}
        </div>

        <div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:12px 14px;font-size:11px;color:#94a3b8;display:flex;flex-direction:column;gap:6px">
          <div style="display:flex;justify-content:space-between;align-items:center">
            <span>Processing Schedule: <strong style="color:#f8fafc">Bank Settlement</strong></span>
            <span style="color:#00e676;font-weight:700">0% Fee</span>
          </div>
          <div style="color:#f59e0b;font-weight:600;font-size:11.5px;line-height:1.4">
            ⚠️ Notice: It may take 5-7 business days to receive funds in your bank account.
          </div>
        </div>

        <button class="wm-action-btn" id="wm-submit-btn" onclick="executeModalWithdraw()" style="background:linear-gradient(135deg,#00c96a,#00a854)">
          <span>⬆️</span> Submit ${cfg.code} Withdrawal Request
        </button>
      `;
    }

    else if (activeModalTab === 'accounts') {
      body.innerHTML = `
        <div class="wm-section-label">Switch Active Game Currency / Account:</div>
        <div style="display:flex;flex-direction:column;gap:10px">
          ${Object.values(WALLET_CONFIGS).map(cfg => {
            const isActive = cfg.key === activeKey;
            const bal = wallets[cfg.key] || 0;
            return `
              <div class="account-picker-item ${isActive ? 'active' : ''}" style="padding:16px;border-radius:14px" onclick="setActiveWalletKey('${cfg.key}'); switchWalletModalTab('accounts');">
                <div class="acc-picker-left">
                  <div class="acc-picker-icon" style="font-size:28px">${cfg.icon}</div>
                  <div class="acc-picker-info">
                    <div class="acc-picker-name" style="font-size:15px;display:flex;align-items:center;gap:6px">
                      ${cfg.name}
                      <span style="font-size:9px;padding:2px 6px;border-radius:4px;background:${cfg.badgeColor};color:#000;font-weight:800">${cfg.badge}</span>
                    </div>
                    <div class="acc-picker-type">${cfg.description}</div>
                  </div>
                </div>
                <div class="acc-picker-right">
                  <div class="acc-picker-bal" style="font-size:18px">${formatCurrency(bal, cfg.key)}</div>
                  ${isActive ? '<span class="acc-active-check">● ACTIVE NOW</span>' : '<span style="font-size:11px;color:#94a3b8">Click to Switch</span>'}
                </div>
              </div>
            `;
          }).join('')}
        </div>
        <div style="margin-top:12px;padding:8px;background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.08);border-radius:8px;text-align:center;color:#94a3b8">
          VIP Level: <strong>${getVipLevel()}</strong>
        </div>
      `;
    }

    else if (activeModalTab === 'payment-history' || activeModalTab === 'history') {
      const txs = getTransactions();
      const currentTxFilter = window._curTxFilter || 'all';
      let filtered = txs;
      if (currentTxFilter === 'deposit') filtered = txs.filter(t => t.type === 'deposit');
      else if (currentTxFilter === 'withdraw') filtered = txs.filter(t => t.type === 'withdraw');

      body.innerHTML = `
        <div class="wm-filter-bar">
          <button class="wm-filter-btn ${currentTxFilter === 'all' ? 'active' : ''}" onclick="window._curTxFilter='all';renderWalletModalContent()">All Transfers (${txs.length})</button>
          <button class="wm-filter-btn green ${currentTxFilter === 'deposit' ? 'active green' : ''}" onclick="window._curTxFilter='deposit';renderWalletModalContent()">📥 Deposits (${txs.filter(t=>t.type==='deposit').length})</button>
          <button class="wm-filter-btn red ${currentTxFilter === 'withdraw' ? 'active red' : ''}" onclick="window._curTxFilter='withdraw';renderWalletModalContent()">📤 Withdrawals (${txs.filter(t=>t.type==='withdraw').length})</button>
        </div>

        <div class="wm-history-list">
          ${filtered.length === 0 ? '<div style="text-align:center;padding:36px;color:#94a3b8"><div style="font-size:32px;margin-bottom:8px">💳</div>No payment transactions found in this category.</div>' : ''}
          ${filtered.map(tx => {
            const isDep = tx.type === 'deposit';
            const isRef = tx.type === 'refill';
            const cfg = WALLET_CONFIGS[tx.wallet] || WALLET_CONFIGS.demo;
            const dateStr = new Date(tx.timestamp).toLocaleString();
            const orderNum = tx.orderId || tx.id || 'ORD-' + Math.floor(100000 + Math.random()*900000);
            const isPendingWth = tx.type === 'withdraw' && tx.status === 'Pending';
            const isCancelled = tx.status === 'Cancelled' || tx.status === 'Cancelled by User' || (tx.status && tx.status.includes('Refunded'));
            const statusClass = (tx.status === 'Completed' || tx.status === 'Approved') ? 'completed' : ((tx.status === 'Rejected' || isCancelled) ? 'rejected' : 'pending');
            const statusLabel = tx.status === 'Completed' ? '✓ Approved' : (isCancelled ? '✕ Cancelled (Refunded)' : (tx.status === 'Rejected' ? '✕ Rejected' : '⏳ Pending'));

            return `
              <div class="wm-tx-item">
                <div class="wm-tx-left">
                  <div class="wm-tx-icon ${tx.type}">${isDep ? '⬇️' : (isRef ? '🔄' : '⬆️')}</div>
                  <div>
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:2px">
                      <span class="wm-tx-title">${isDep ? 'Deposit' : (isRef ? 'Demo Refill' : 'Withdrawal')} • ${cfg.shortName}</span>
                      <span class="wm-order-badge" onclick="navigator.clipboard&&navigator.clipboard.writeText('${orderNum}');if(typeof showToast==='function')showToast('Order ID Copied: ${orderNum}')" title="Click to Copy Order Number">
                        📋 ${orderNum}
                      </span>
                    </div>
                    <div class="wm-tx-meta">
                      ${tx.method || 'UPI Instant'}
                      ${tx.utr ? ` · <span class="wm-utr-badge" onclick="navigator.clipboard&&navigator.clipboard.writeText('${tx.utr}');if(typeof showToast==='function')showToast('UTR Copied: ${tx.utr}')" title="Click to Copy UTR">UTR: ${tx.utr}</span>` : ''}
                      · ${dateStr}
                    </div>
                    ${isPendingWth ? `
                      <div style="margin-top:6px">
                        <button onclick="cancelUserWithdrawal('${tx.id}')" style="background:rgba(239,68,68,0.18);border:1px solid #ef4444;color:#ef4444;border-radius:6px;padding:3px 9px;font-size:11px;font-weight:800;cursor:pointer;display:inline-flex;align-items:center;gap:4px;transition:all 0.2s" onmouseover="this.style.background='rgba(239,68,68,0.35)'" onmouseout="this.style.background='rgba(239,68,68,0.18)'">
                          ✕ Cancel Withdrawal &amp; Refund Funds
                        </button>
                      </div>
                    ` : ''}
                  </div>
                </div>
                <div class="wm-tx-right">
                  <div class="wm-tx-amt ${isDep || isRef || isCancelled ? 'positive' : 'negative'}">${isDep || isRef ? '+' : (isCancelled ? '↺ ' : '-')}${formatCurrency(tx.amount, tx.wallet)}</div>
                  <div class="wm-tx-status ${statusClass}">${statusLabel}</div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }

    else if (activeModalTab === 'game-history') {
      const gHistory = getGameHistory();
      const currentGFilter = window._curGFilter || 'all';
      let filtered = gHistory;
      if (currentGFilter === 'win') filtered = gHistory.filter(g => g.won);
      else if (currentGFilter === 'loss') filtered = gHistory.filter(g => !g.won);

      const totalBets = gHistory.length;
      const totalWins = gHistory.filter(g => g.won).length;
      const totalLosses = gHistory.filter(g => !g.won).length;
      let netProfit = 0;
      gHistory.forEach(g => { netProfit += (parseFloat(g.profit) || 0); });

      const gameIcons = {
        'GG Ludo': '🎲', 'Ludo': '🎲',
        'GG Mines': '💣', 'Mines': '💣',
        'GG Crash': '🚀', 'Crash': '🚀',
        'GG Slots': '🎰', 'Slots': '🎰',
        'GG Wheel': '🎡', 'Wheel of Fortune': '🎡',
        'GG Hilo': '🃏', 'Hilo': '🃏',
        'GG Keno': '🎱', 'Keno': '🎱',
        'GG Dragon Tower': '🐉', 'Dragon Tower': '🐉',
        'GG Coin Flip': '🪙', 'Coin Flip': '🪙',
        'GG Penalty': '⚽', 'Penalty Shootout': '⚽',
        'GG Baccarat': '👑', 'Baccarat': '👑', 'GG Baccarat 3D': '👑',
        'GG Diamonds': '💎', 'Diamond Rush': '💎', 'GG Diamond Rush': '💎',
        'GG Sic Bo': '🎲', 'Sic Bo': '🎲',
        'GG Plinko': '⚪', 'Plinko': '⚪',
        'GG Roulette': '🎯', 'Roulette': '🎯',
        'GG Dice': '🎲', 'Dice': '🎲',
        'GG Limbo': '📈', 'Limbo': '📈',
        'GG Blackjack': '♠️', 'Blackjack': '♠️'
      };

      body.innerHTML = `
        <div class="wm-stats-mini-grid">
          <div class="wm-mini-stat">
            <div class="wm-mini-stat-lbl">Total Bets</div>
            <div class="wm-mini-stat-val" style="color:#fff">${totalBets}</div>
          </div>
          <div class="wm-mini-stat">
            <div class="wm-mini-stat-lbl">Wins</div>
            <div class="wm-mini-stat-val" style="color:#00e676">${totalWins} 👑</div>
          </div>
          <div class="wm-mini-stat">
            <div class="wm-mini-stat-lbl">Losses</div>
            <div class="wm-mini-stat-val" style="color:#ef4444">${totalLosses} 💀</div>
          </div>
          <div class="wm-mini-stat">
            <div class="wm-mini-stat-lbl">Net Profit</div>
            <div class="wm-mini-stat-val" style="color:${netProfit >= 0 ? '#00e676' : '#ef4444'}">${netProfit >= 0 ? '+' : ''}₹${netProfit.toLocaleString('en-IN', {minimumFractionDigits: 2})}</div>
          </div>
        </div>

        <div class="wm-filter-bar">
          <button class="wm-filter-btn ${currentGFilter === 'all' ? 'active' : ''}" onclick="window._curGFilter='all';renderWalletModalContent()">All Games (${totalBets})</button>
          <button class="wm-filter-btn green ${currentGFilter === 'win' ? 'active green' : ''}" onclick="window._curGFilter='win';renderWalletModalContent()">👑 Wins Only (${totalWins})</button>
          <button class="wm-filter-btn red ${currentGFilter === 'loss' ? 'active red' : ''}" onclick="window._curGFilter='loss';renderWalletModalContent()">💀 Losses Only (${totalLosses})</button>
        </div>

        <div class="wm-history-list">
          ${filtered.length === 0 ? '<div style="text-align:center;padding:36px;color:#94a3b8"><div style="font-size:32px;margin-bottom:8px">🎲</div>No game rounds recorded in this view. Play any game to see your real-time results!</div>' : ''}
          ${filtered.map(g => {
            const isWin = !!g.won;
            const dateStr = new Date(g.timestamp).toLocaleString();
            const icon = gameIcons[g.game] || '🎮';
            const orderNum = g.orderId || 'BET-' + Math.floor(100000 + Math.random()*900000);
            const profitFormatted = (g.profit >= 0 ? '+' : '') + '₹' + Math.abs(g.profit).toLocaleString('en-IN', {minimumFractionDigits: 2});

            return `
              <div class="wm-game-hist-card ${isWin ? 'win' : 'loss'}">
                <div class="wm-tx-left">
                  <div class="wm-tx-icon" style="background:${isWin ? 'rgba(0,230,118,0.15)' : 'rgba(239,68,68,0.15)'}">${icon}</div>
                  <div>
                    <div style="display:flex;align-items:center;gap:6px;margin-bottom:2px">
                      <span class="wm-tx-title">${g.game}</span>
                      <span class="wm-order-badge" onclick="navigator.clipboard&&navigator.clipboard.writeText('${orderNum}');if(typeof showToast==='function')showToast('Bet Order ID Copied: ${orderNum}')" title="Click to Copy Order Number">
                        📋 ${orderNum}
                      </span>
                    </div>
                    <div class="wm-tx-meta">
                      Wager: ₹${Number(g.wager).toLocaleString('en-IN', {minimumFractionDigits: 2})}
                      · Payout: ₹${Number(g.payout).toLocaleString('en-IN', {minimumFractionDigits: 2})}
                      · ${dateStr}
                    </div>
                  </div>
                </div>
                <div class="wm-tx-right">
                  <div class="wm-tx-amt ${isWin ? 'positive' : 'negative'}">${profitFormatted}</div>
                  <div class="wm-result-tag ${isWin ? 'win' : 'loss'}">${isWin ? '👑 WON' : '💀 LOST'}</div>
                </div>
              </div>
            `;
          }).join('')}
        </div>
      `;
    }
  }

  // ── INJECT TOPBAR ACCOUNT SWITCHER WIDGET ──────────────────────
  window.renderWalletSwitcherWidget = function(targetContainer) {
    injectWalletStyles();
    injectWalletModalHTML();

    const container = typeof targetContainer === 'string' ? document.getElementById(targetContainer) : targetContainer;
    if (!container) return;

    const wallets = getWallets();
    const activeKey = getActiveWalletKey();
    const activeCfg = WALLET_CONFIGS[activeKey] || WALLET_CONFIGS.demo;
    const formatted = formatCurrency(wallets[activeKey], activeKey);

    container.innerHTML = `
      <div class="wallet-switcher-container" id="ggwins-wallet-switcher">
        <button class="wallet-chip-btn" onclick="toggleWalletDropdown(event)" title="Switch Active Account / Currency">
          <span class="wallet-active-icon">${activeCfg.icon}</span>
          <span class="wallet-active-name" style="color:#94a3b8;font-size:11px">${activeCfg.shortName}</span>
          <span id="lobby-balance-val" style="color:#00e676;font-weight:800">${formatted}</span>
          <span class="wallet-active-badge" style="background:${activeCfg.badgeColor}">${activeCfg.badge}</span>
          <svg class="chevron-arrow" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="6 9 12 15 18 9"/></svg>
        </button>

        <div class="account-picker-dropdown" id="ggwins-account-dropdown">
          <div class="account-picker-title">
            <span>Select Active Account</span>
            <span style="font-size:10px;color:#00e676">3 Accounts</span>
          </div>

          ${Object.values(WALLET_CONFIGS).map(cfg => {
            const isActive = cfg.key === activeKey;
            const bal = wallets[cfg.key] || 0;
            return `
              <div class="account-picker-item ${isActive ? 'active' : ''}" data-wallet-key="${cfg.key}" onclick="switchActiveAccount('${cfg.key}')">
                <div class="acc-picker-left">
                  <div class="acc-picker-icon">${cfg.icon}</div>
                  <div class="acc-picker-info">
                    <div class="acc-picker-name">${cfg.name}</div>
                    <div class="acc-picker-type">${cfg.shortName}</div>
                  </div>
                </div>
                <div class="acc-picker-right">
                  <div class="acc-picker-bal">${formatCurrency(bal, cfg.key)}</div>
                  ${isActive ? '<span class="acc-active-check">✓ ACTIVE</span>' : ''}
                </div>
              </div>
            `;
          }).join('')}

          <div class="acc-dropdown-actions">
            <button class="btn-acc-action dep" onclick="openWalletModal('deposit')">⬇️ Deposit</button>
            <button class="btn-acc-action wth" onclick="openWalletModal('withdraw')">⬆️ Withdraw</button>
          </div>
        </div>
      </div>
    `;
  };

  window.toggleWalletDropdown = function(e) {
    if (e) e.stopPropagation();
    const switcher = document.getElementById('ggwins-wallet-switcher');
    if (switcher) switcher.classList.toggle('open');
  };

  window.switchActiveAccount = function(key) {
    setActiveWalletKey(key);
    const switcher = document.getElementById('ggwins-wallet-switcher');
    if (switcher) switcher.classList.remove('open');
    renderWalletSwitcherWidget(document.getElementById('wallet-chip-target') || switcher.parentElement);
  };

  // Close dropdown on outside click
  document.addEventListener('click', e => {
    if (!e.target.closest('#ggwins-wallet-switcher')) {
      const switcher = document.getElementById('ggwins-wallet-switcher');
      if (switcher) switcher.classList.remove('open');
    }
  });

  // Auto initialize on DOMContentLoaded
  document.addEventListener('DOMContentLoaded', () => {
    injectWalletStyles();
    injectWalletModalHTML();
    updateAllWalletDisplays();

    const target = document.getElementById('wallet-chip-target') || document.querySelector('.lobby-balance-chip');
    if (target && !document.getElementById('ggwins-wallet-switcher')) {
      target.id = 'wallet-chip-target';
      renderWalletSwitcherWidget(target);
    }
  });

})();
