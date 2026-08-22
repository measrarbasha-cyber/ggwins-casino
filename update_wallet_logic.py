import re

# 1. Update wallet.js
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    wjs = f.read()

# Update trackGameWager in wallet.js to progress 3x bonus task
old_track_snippet = "session.stats.totalWagered = (parseFloat(session.stats.totalWagered) || 0) + wager;"
new_track_snippet = """session.stats.totalWagered = (parseFloat(session.stats.totalWagered) || 0) + wager;

      // ── PROGRESS 3X BONUS TASK ──
      try {
        const bTask = JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
        if (bTask && !bTask.completed && curWallet !== 'demo') {
          bTask.currentWagered = (parseFloat(bTask.currentWagered) || 0) + wager + (won ? payout : 0);
          if (bTask.currentWagered >= bTask.targetWager) {
            bTask.completed = true;
            bTask.completedAt = Date.now();
            if (typeof showToast === 'function') {
              showToast(`🎉 3× BONUS TASK COMPLETED! Target of ₹${bTask.targetWager.toFixed(2)} reached. Funds are now 100% UNLOCKED for withdrawal!`, 'success');
            }
          }
          localStorage.setItem('ggwins_bonus_task', JSON.stringify(bTask));
        }
      } catch(e) {}"""

if old_track_snippet in wjs and "PROGRESS 3X BONUS TASK" not in wjs:
    wjs = wjs.replace(old_track_snippet, new_track_snippet)

# Update executeModalWithdraw in wallet.js to block withdrawal if 3x bonus task is incomplete
old_wth_snippet = "if (!name) { alert('Please enter your Full Name (as per Bank Account).'); return; }"
new_wth_snippet = """// Check 3x Bonus Task requirement
    try {
      const bTask = JSON.parse(localStorage.getItem('ggwins_bonus_task') || 'null');
      if (bTask && !bTask.completed) {
        const remaining = Math.max(0, bTask.targetWager - bTask.currentWagered);
        const pct = Math.min(100, (bTask.currentWagered / bTask.targetWager) * 100).toFixed(1);
        alert(`⚠️ BONUS WITHDRAWAL TASK INCOMPLETE\\n\\nYou claimed a promo bonus of ₹${bTask.bonusAmt.toFixed(2)} with coupon [${bTask.coupon}].\\n\\nRule: You must wager/earn 3× the bonus amount (₹${bTask.targetWager.toFixed(2)}) before withdrawing.\\n\\n📊 Current Progress: ₹${bTask.currentWagered.toFixed(2)} / ₹${bTask.targetWager.toFixed(2)} (${pct}%)\\n🔒 Need ₹${remaining.toFixed(2)} more in game activity to unlock withdrawal!`);
        return;
      }
    } catch(e) {}

    if (!name) { alert('Please enter your Full Name (as per Bank Account).'); return; }"""

if old_wth_snippet in wjs and "BONUS WITHDRAWAL TASK INCOMPLETE" not in wjs:
    wjs = wjs.replace(old_wth_snippet, new_wth_snippet)

# Update createPendingDeposit in wallet.js to support coupon & bonusAmt
old_create_dep = "window.createPendingDeposit = function(walletKey, amount, method, utr, senderName) {"
new_create_dep = """window.createPendingDeposit = function(walletKey, amount, method, utr, senderName, couponCode, bonusAmount) {"""
if old_create_dep in wjs:
    wjs = wjs.replace(old_create_dep, new_create_dep)

old_dep_record = """      amount: amount,
      currency: walletKey === 'usdt' ? 'USDT' : 'INR',"""
new_dep_record = """      amount: amount,
      bonusAmount: bonusAmount || 0,
      coupon: couponCode || null,
      creditedAmount: amount + (bonusAmount || 0),
      currency: walletKey === 'usdt' ? 'USDT' : 'INR',"""
if old_dep_record in wjs and "bonusAmount: bonusAmount" not in wjs:
    wjs = wjs.replace(old_dep_record, new_dep_record)

# Update executeModalDeposit to read applied coupon and create task
old_exec_dep = """    createPendingDeposit(depositTargetAccount, amt, methodName, utrVal, senderNameVal);

    showDepositSuccess(`Deposit request of <strong>${formatCurrency(amt, depositTargetAccount)}</strong> submitted for <strong>${senderNameVal}</strong>. Await host approval in the admin panel. ⏳`);"""

new_exec_dep = """    let bonusAmt = 0;
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
      }
    }

    createPendingDeposit(depositTargetAccount, amt, methodName, utrVal, senderNameVal, couponUsed, bonusAmt);

    let successMsg = `Deposit request of <strong>${formatCurrency(amt, depositTargetAccount)}</strong>`;
    if (bonusAmt > 0) {
      successMsg += ` + <strong>₹${bonusAmt.toFixed(2)} Bonus (${couponUsed})</strong> (Total Credited: <strong>₹${(amt + bonusAmt).toFixed(2)}</strong>)`;
      successMsg += `<br><br><span style="color:#ffd700;font-weight:700">🎯 3× Wagering Task Created:</span> Earn/Wager ₹${(bonusAmt * 3).toFixed(2)} across any games to unlock full withdrawal!`;
    }
    successMsg += ` submitted for <strong>${senderNameVal}</strong>. Await host approval in the admin panel. ⏳`;

    showDepositSuccess(successMsg);
    appliedCouponCode = null;"""

if old_exec_dep in wjs:
    wjs = wjs.replace(old_exec_dep, new_exec_dep)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(wjs)

print("Updated wallet.js logic successfully.")
