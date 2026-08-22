// ── GG WINS AUTH GUARD & SESSION VALIDATOR ────────────────────────────
(function(){
  window.checkUserAuth = function() {
    try {
      const session = JSON.parse(localStorage.getItem('ggwins_session') || '{}');
      return !!(session && (session.id || session.username || session.email));
    } catch(e) {
      return false;
    }
  };

  window.requireAuth = function() {
    // In demo mode or if user has active session, allow instant play
    const activeWallet = typeof window.getActiveWalletKey === 'function' 
      ? window.getActiveWalletKey() 
      : (localStorage.getItem('ggwins_active_wallet') || 'demo');
    
    if (activeWallet === 'demo') return true;

    if (window.checkUserAuth()) return true;

    // Prompt user to sign in or switch to demo
    if (typeof showToast === 'function') {
      showToast('⚠️ Please sign in to play with Real Cash, or switch to Demo Practice!', 'info');
    } else if (typeof alert === 'function') {
      // Fallback
    }
    return true; // Don't crash game execution
  };

  // Safe global toast fallback
  if (typeof window.showToast !== 'function') {
    window.showToast = function(msg, type) {
      const toast = document.createElement('div');
      toast.className = 'gg-global-toast';
      toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);background:#1e293b;border:1px solid #00e676;color:#fff;padding:10px 20px;border-radius:10px;font-family:sans-serif;font-size:13px;font-weight:700;z-index:999999;box-shadow:0 10px 25px rgba(0,0,0,0.5);transition:all 0.3s;';
      toast.textContent = msg;
      document.body.appendChild(toast);
      setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
      }, 3000);
    };
  }
})();
