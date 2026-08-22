import re

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    content = f.read()

cancel_functions = """
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
      showToast(`⚠️ Bonus task cancelled. -₹${bonusToDeduct.toFixed(2)} bonus and -₹${penaltyFee.toFixed(2)} (8% fee) deducted. Withdrawals are now 100% unlocked!`, 'warning');
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

    const confirmMsg = `⚠️ CANCEL BONUS TASK & UNLOCK WITHDRAWAL\\n\\n` +
      `Are you sure you want to cancel your Active Bonus Task?\\n\\n` +
      `• Deposited Bonus to forfeit: -₹${bonusToDeduct.toFixed(2)}\\n` +
      `• 8% Cancellation Fee on your balance (₹${currentRealBal.toFixed(2)}): -₹${penaltyFee.toFixed(2)}\\n` +
      `• Total deduction from balance: -₹${totalDeduction.toFixed(2)}\\n` +
      `• Remaining Real INR Balance: ₹${newBal.toFixed(2)}\\n\\n` +
      `Result: Your withdrawal lock will be immediately lifted.\\n\\n` +
      `Click OK to cancel the task or Cancel to keep playing your bonus task.`;

    if (confirm(confirmMsg)) {
      cancelBonusTask();
    }
  };
"""

# Insert cancel functions right after saveBonusTask
if "window.cancelBonusTask" not in content:
    content = content.replace("window.saveBonusTask = function(task) {", cancel_functions + "\n  window.saveBonusTask = function(task) {")

# Update active task banner to include the Cancel Task button when !isDone
old_banner_bottom = """              <div style="display:flex;justify-content:space-between;font-size:11px;color:#cbd5e1;font-weight:700">
                <span>Progress: ₹${task.currentWagered.toFixed(2)} / ₹${task.targetWager.toFixed(2)}</span>
                <span style="color:${isDone?'#00e676':'#ffd700'}">${pct}% ${isDone?'✓ Completed':'Remaining'}</span>
              </div>
            </div>"""

new_banner_bottom = """              <div style="display:flex;justify-content:space-between;font-size:11px;color:#cbd5e1;font-weight:700">
                <span>Progress: ₹${task.currentWagered.toFixed(2)} / ₹${task.targetWager.toFixed(2)}</span>
                <span style="color:${isDone?'#00e676':'#ffd700'}">${pct}% ${isDone?'✓ Completed':'Remaining'}</span>
              </div>
              ${!isDone ? `
                <div style="display:flex;justify-content:space-between;align-items:center;margin-top:8px;padding-top:6px;border-top:1px dashed rgba(255,255,255,0.15)">
                  <span style="font-size:11px;color:#94a3b8">Want to withdraw immediately?</span>
                  <button onclick="openCancelBonusTaskModal()" style="background:rgba(239,68,68,0.2);border:1px solid #ef4444;border-radius:6px;padding:4px 10px;color:#ef4444;font-size:11px;font-weight:700;cursor:pointer;transition:all 0.2s" onmouseover="this.style.background='rgba(239,68,68,0.35)'" onmouseout="this.style.background='rgba(239,68,68,0.2)'">
                    🚫 Cancel Task (-Bonus &amp; -8% Fee)
                  </button>
                </div>
              ` : ''}
            </div>"""

content = content.replace(old_banner_bottom, new_banner_bottom)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(content)

print("Injected Cancel Bonus Task option with -bonus and -8% balance deduction into wallet.js")
