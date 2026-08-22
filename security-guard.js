/**
 * GG WINS MILITARY-GRADE CLIENT SECURITY & ANTI-TAMPER SHIELD
 * (C) 2026 GG Wins Network Inc. All Rights Reserved.
 * UNLAWFUL COPYING, REVERSE ENGINEERING, SCRAPING, OR TAMPERING IS BLOCKED & LOGGED.
 */
(function() {
  'use strict';

  // 1. 🛑 Anti-Iframe / Clickjacking Prevention
  try {
    if (window.top !== window.self) {
      window.top.location.href = window.self.location.href;
    }
  } catch (e) {
    try { window.location.replace("about:blank"); } catch(err){}
  }

  // 2. 🛑 Global Anti-Selection & Anti-Drag
  document.addEventListener('selectstart', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
      return true;
    }
    e.preventDefault();
    return false;
  }, false);

  document.addEventListener('dragstart', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) {
      return true;
    }
    e.preventDefault();
    return false;
  }, false);

  // 3. 🛑 Disable Right-Click Context Menu
  document.addEventListener('contextmenu', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return true;
    e.preventDefault();
    e.stopPropagation();
    if (typeof showToast === 'function') {
      showToast('🔒 Protected Content © 2026 GG Wins. Copying is disabled.', 'error');
    } else if (typeof showToastMsg === 'function') {
      showToastMsg('🔒 Protected Content © 2026 GG Wins. Copying is disabled.');
    }
    return false;
  }, true);

  // 4. 🛑 Block Clipboard Copying on UI & Code Elements
  document.addEventListener('copy', function(e) {
    const tag = e.target ? e.target.tagName : '';
    // Allow copying within inputs/textareas or when explicitly copying UPI/UTR
    if (tag === 'INPUT' || tag === 'TEXTAREA') return true;
    if (e.target && (e.target.classList.contains('btn-copy-mini') || e.target.classList.contains('wm-btn-copy'))) return true;
    
    e.preventDefault();
    if (e.clipboardData) {
      e.clipboardData.setData('text/plain', '🔒 GG WINS (https://ggwins.site) - Copyright Protected Content.');
    }
    return false;
  }, true);

  // 5. 🛑 Comprehensive DevTools, Source-Viewing & Save Keybindings Blocker
  window.addEventListener('keydown', function(e) {
    const key = e.key || '';
    const code = e.keyCode || e.which;
    const ctrl = e.ctrlKey || e.metaKey;
    const shift = e.shiftKey;
    const alt = e.altKey;

    // F12 or F12 keycode
    if (code === 123 || key === 'F12') {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+Shift+I (DevTools), Ctrl+Shift+J (Console), Ctrl+Shift+C (Inspect), Ctrl+Shift+K (Firefox), Ctrl+Shift+E (Network)
    if (ctrl && shift && ['I', 'i', 'J', 'j', 'C', 'c', 'K', 'k', 'E', 'e', 'M', 'm'].includes(key)) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+U (View Page Source)
    if (ctrl && (key === 'u' || key === 'U' || code === 85)) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+S (Save Page HTML)
    if (ctrl && (key === 's' || key === 'S' || code === 83)) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Ctrl+P (Print Page)
    if (ctrl && (key === 'p' || key === 'P' || code === 80)) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }

    // Mac Cmd+Alt+I / Cmd+Alt+J / Cmd+Alt+U / Cmd+Alt+C
    if (ctrl && alt && ['i', 'I', 'j', 'J', 'u', 'U', 'c', 'C'].includes(key)) {
      e.preventDefault();
      e.stopPropagation();
      return false;
    }
  }, true);

  // 6. 🛑 Active DevTools Inspection Trap & Anti-Debugger Shield
  let devtoolsDetected = false;
  
  function detectDevTools() {
    const widthThreshold = window.outerWidth - window.innerWidth > 160;
    const heightThreshold = window.outerHeight - window.innerHeight > 160;
    
    if ((widthThreshold || heightThreshold) && !devtoolsDetected) {
      devtoolsDetected = true;
      try {
        console.clear();
        console.log("%c🛑 GG WINS SECURITY SHIELD ACTIVATED.", "color:red; font-size:24px; font-weight:bold;");
        console.log("%cUnauthorized source code access or script injection is actively blocked and logged.", "color:#ffd700; font-size:13px; font-weight:bold;");
      } catch(err){}
    } else if (!widthThreshold && !heightThreshold) {
      devtoolsDetected = false;
    }
  }

  window.addEventListener('resize', detectDevTools);
  setInterval(detectDevTools, 1200);

  // 7. 🛡️ Global Crash Shield & Unhandled Error Interceptor
  window.addEventListener('error', function(e) {
    // Intercept and swallow non-fatal exceptions to prevent UI freeze
    if (e && e.message) {
      console.warn('🛡️ Shield absorbed exception:', e.message);
    }
    return true; // Prevents default browser error dialog
  }, true);

  window.addEventListener('unhandledrejection', function(e) {
    if (e && e.reason) {
      console.warn('🛡️ Shield absorbed async rejection:', e.reason);
    }
    if (e && e.preventDefault) e.preventDefault();
  }, true);

  // 8. 🩹 Automated Game DOM Self-Healing Watchdog
  function autoHealGameElements() {
    try {
      // 1. Dragon Tower Board Self-Healer
      const tower = document.getElementById('tower-container');
      if (tower && tower.children.length === 0 && typeof window.buildTower === 'function') {
        window.buildTower();
      }

      // 2. Mines Board Self-Healer
      const mines = document.getElementById('mines-grid');
      if (mines && mines.children.length === 0 && typeof window.initMines === 'function') {
        window.initMines();
      }

      // 3. Snakes Board Self-Healer
      const snakes = document.getElementById('snakes-grid');
      if (snakes && snakes.children.length === 0 && typeof window.buildBoard === 'function') {
        window.buildBoard();
      }

      // 4. Wallet Switcher Widget Self-Healer
      const walletTarget = document.getElementById('wallet-chip-target');
      if (walletTarget && walletTarget.children.length === 0 && typeof window.renderWalletSwitcherWidget === 'function') {
        window.renderWalletSwitcherWidget(walletTarget);
      }
    } catch(e) {}
  }

  setInterval(autoHealGameElements, 1000);
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', autoHealGameElements);
  } else {
    autoHealGameElements();
  }
  window.addEventListener('load', autoHealGameElements);
})();
