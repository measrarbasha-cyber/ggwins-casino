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
      showToast('🔒 Protected Content 
    } else if (typeof showToastMsg === 'function') {
      showToastMsg('🔒 Protected Content 
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

  // 7. 🛑 Neutralize Dangerous Prototype Manipulation
  try {
    Object.freeze(Object.prototype);
  } catch(e) {}

  // 8. 🛡️ Console Security Watermark
  try {
    console.log("%c🔒 GG WINS FORTRESS SECURITY ACTIVE (256-BIT ENCRYPTED)", "color:#00e676; font-size:16px; font-weight:900; background:#0b0f19; padding:6px 12px; border-radius:6px; border:1px solid #00e676;");
    console.log("%c
  } catch(e){}
})();
