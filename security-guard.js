/**
 * GG WINS PROPRIETARY SECURITY & ANTI-CLONE SYSTEM
 * (C) 2026 GG Wins Network Inc. All Rights Reserved.
 * UNLAWFUL COPYING, DECOMPILATION, OR REPRODUCTION IS STRICTLY PROHIBITED BY LAW.
 */
(function() {
  'use strict';

  // Disable Right Click Context Menu (except on interactive controls)
  document.addEventListener('contextmenu', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA')) return;
    e.preventDefault();
    if (typeof showToast === 'function') {
      showToast('⚠️ Content Protected © 2026 GG Wins');
    }
    return false;
  }, false);

  // Disable DevTools / View Source Shortcuts
  document.addEventListener('keydown', function(e) {
    // F12
    if (e.key === 'F12' || e.keyCode === 123) {
      e.preventDefault();
      return false;
    }
    // Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+Shift+C
    if (e.ctrlKey && e.shiftKey && (e.key === 'I' || e.key === 'i' || e.key === 'J' || e.key === 'j' || e.key === 'C' || e.key === 'c')) {
      e.preventDefault();
      return false;
    }
    // Ctrl+U (View Source), Ctrl+S (Save Page)
    if (e.ctrlKey && (e.key === 'u' || e.key === 'U' || e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      return false;
    }
  }, false);

  // Disable text selection on static elements without disrupting canvas/input interactions
  document.addEventListener('selectstart', function(e) {
    if (e.target && (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'CANVAS')) {
      return true;
    }
    e.preventDefault();
  }, false);

  // Console Watermark
  try {
    console.log("%c🛑 STOP! ALL CODE & ASSETS ARE COPYRIGHT PROTECTED.", "color:red; font-size:20px; font-weight:bold;");
    console.log("%c© 2026 GG Wins Enterprise. Unauthorized cloning or distribution will result in legal prosecution.", "color:#ffd700; font-size:13px;");
  } catch(e) {}
})();
