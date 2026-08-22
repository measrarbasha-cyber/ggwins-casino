with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "r", encoding="utf-8") as f:
    wjs = f.read()

old_sync_block = """      if (updated) {
        saveWallets(wallets);"""

new_sync_block = """      // 4. Check for VIP Level approval from Admin in data.user
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
        }
      }

      if (updated) {
        saveWallets(wallets);"""

wjs = wjs.replace(old_sync_block, new_sync_block)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\wallet.js", "w", encoding="utf-8") as f:
    f.write(wjs)

print("Updated wallet.js with real-time VIP approval synchronization and badge unlock!")
