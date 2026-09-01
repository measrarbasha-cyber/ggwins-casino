/**
 * GG WINS — UNIVERSAL GAME MOTION, VFX & SOUND ENGINE (game-fx.js)
 * Stake / Roobet Grade Canvas Particle Blasts, Spring Physics & Procedural Audio
 */
(function() {
  'use strict';

  // ── 1. WEB AUDIO API PROCEDURAL SOUND SYNTHESIZER ──
  let audioCtx = null;
  function getAudioContext() {
    if (!audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) audioCtx = new AudioContext();
    }
    if (audioCtx && audioCtx.state === 'suspended') {
      audioCtx.resume().catch(() => {});
    }
    return audioCtx;
  }

  function isSoundMuted() {
    return localStorage.getItem('ggwins_sound_muted') === 'true';
  }

  window.toggleSound = function() {
    const muted = !isSoundMuted();
    localStorage.setItem('ggwins_sound_muted', muted ? 'true' : 'false');
    const btns = document.querySelectorAll('.btn-sound-toggle');
    btns.forEach(b => {
      b.textContent = muted ? '🔇' : '🔊';
    });
    if (!muted) window.fxPlayClick();
  };

  // Sync sound toggle button UI
  document.addEventListener('DOMContentLoaded', () => {
    const muted = isSoundMuted();
    document.querySelectorAll('.btn-sound-toggle').forEach(b => {
      b.textContent = muted ? '🔇' : '🔊';
    });
  });

  // Sound: Crystal Gem Chime
  window.fxPlayGem = function(step = 0) {
    if (isSoundMuted()) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const baseFreq = 587.33; // D5
      const notes = [1, 1.122, 1.259, 1.334, 1.498, 1.681, 1.887, 2.0];
      const freq = baseFreq * (notes[step % notes.length] || 1.0) * (1 + Math.floor(step / notes.length) * 0.5);

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(freq * 1.5, ctx.currentTime + 0.18);

      gain.gain.setValueAtTime(0.18, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.35);

      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.36);
    } catch(e) {}
  };

  // Sound: Cascading Metallic Coin
  window.fxPlayCoin = function() {
    if (isSoundMuted()) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      [1800, 2400].forEach((freq, i) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq + (Math.random() * 200 - 100), ctx.currentTime + i * 0.04);
        gain.gain.setValueAtTime(0.12, ctx.currentTime + i * 0.04);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.04 + 0.22);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + i * 0.04);
        osc.stop(ctx.currentTime + i * 0.04 + 0.23);
      });
    } catch(e) {}
  };

  // Sound: Deep Mine Explosion Rumble
  window.fxPlayExplosion = function() {
    if (isSoundMuted()) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const bufferSize = ctx.sampleRate * 0.4;
      const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
      const data = buffer.getChannelData(0);
      for (let i = 0; i < bufferSize; i++) {
        data[i] = Math.random() * 2 - 1;
      }
      const noise = ctx.createBufferSource();
      noise.buffer = buffer;

      const filter = ctx.createBiquadFilter();
      filter.type = 'lowpass';
      filter.frequency.setValueAtTime(320, ctx.currentTime);
      filter.frequency.exponentialRampToValueAtTime(40, ctx.currentTime + 0.38);

      const gain = ctx.createGain();
      gain.gain.setValueAtTime(0.35, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.39);

      noise.connect(filter);
      filter.connect(gain);
      gain.connect(ctx.destination);
      noise.start();
      noise.stop(ctx.currentTime + 0.4);
    } catch(e) {}
  };

  // Sound: Victory Fanfare Chord Sweep
  window.fxPlayWin = function() {
    if (isSoundMuted()) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const chords = [523.25, 659.25, 783.99, 1046.50]; // C Major Triad
      chords.forEach((freq, idx) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, ctx.currentTime + idx * 0.08);
        gain.gain.setValueAtTime(0.15, ctx.currentTime + idx * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + idx * 0.08 + 0.6);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(ctx.currentTime + idx * 0.08);
        osc.stop(ctx.currentTime + idx * 0.08 + 0.62);
      });
    } catch(e) {}
  };

  // Sound: UI Click
  window.fxPlayClick = function() {
    if (isSoundMuted()) return;
    try {
      const ctx = getAudioContext();
      if (!ctx) return;
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.type = 'sine';
      osc.frequency.setValueAtTime(800, ctx.currentTime);
      osc.frequency.exponentialRampToValueAtTime(400, ctx.currentTime + 0.04);
      gain.gain.setValueAtTime(0.1, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.04);
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.start();
      osc.stop(ctx.currentTime + 0.05);
    } catch(e) {}
  };

  // ── 2. HIGH PERFORMANCE CANVAS PARTICLE ENGINE ──
  let canvas = null;
  let ctx = null;
  const particles = [];
  let animId = null;

  function initCanvas() {
    if (canvas) return;
    canvas = document.createElement('canvas');
    canvas.id = 'fx-canvas-overlay';
    document.body.appendChild(canvas);
    ctx = canvas.getContext('2d');

    function resize() {
      if (!canvas) return;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    }
    window.addEventListener('resize', resize);
    resize();
  }

  function loop() {
    if (!ctx) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vy += p.gravity;
      p.angle += p.vAngle;
      p.alpha -= p.decay;

      if (p.alpha <= 0 || p.y > canvas.height + 40) {
        particles.splice(i, 1);
        continue;
      }

      ctx.save();
      ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.translate(p.x, p.y);
      ctx.rotate(p.angle);

      if (p.type === 'coin') {
        // 3D Spinning Gold Coin
        const scaleX = Math.cos(p.angle * 2.5);
        ctx.scale(scaleX, 1);
        ctx.beginPath();
        ctx.arc(0, 0, p.size, 0, Math.PI * 2);
        ctx.fillStyle = '#ffd700';
        ctx.fill();
        ctx.lineWidth = 2;
        ctx.strokeStyle = '#fff';
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(0, 0, p.size * 0.6, 0, Math.PI * 2);
        ctx.fillStyle = '#ff9100';
        ctx.fill();
      } else if (p.type === 'gem') {
        // Sparkling 4-Point Star
        ctx.fillStyle = p.color || '#00f2fe';
        ctx.beginPath();
        ctx.moveTo(0, -p.size);
        ctx.quadraticCurveTo(0, 0, p.size, 0);
        ctx.quadraticCurveTo(0, 0, 0, p.size);
        ctx.quadraticCurveTo(0, 0, -p.size, 0);
        ctx.quadraticCurveTo(0, 0, 0, -p.size);
        ctx.fill();
      } else {
        // Confetti Streamer
        ctx.fillStyle = p.color || '#ffd700';
        ctx.fillRect(-p.size / 2, -p.size / 4, p.size, p.size / 2);
      }

      ctx.restore();
    }

    if (particles.length > 0) {
      animId = requestAnimationFrame(loop);
    } else {
      animId = null;
    }
  }

  function ensureLoopRunning() {
    if (!animId) animId = requestAnimationFrame(loop);
  }

  // Particle Cannon: Gold Coins
  window.fireGoldCoinShower = function(originX, originY, count = 35) {
    initCanvas();
    const startX = originX || window.innerWidth / 2;
    const startY = originY || window.innerHeight / 2;

    for (let i = 0; i < count; i++) {
      particles.push({
        type: 'coin',
        x: startX + (Math.random() * 40 - 20),
        y: startY + (Math.random() * 40 - 20),
        vx: (Math.random() - 0.5) * 14,
        vy: -Math.random() * 12 - 4,
        gravity: 0.42,
        size: Math.random() * 6 + 10,
        angle: Math.random() * Math.PI * 2,
        vAngle: (Math.random() - 0.5) * 0.25,
        alpha: 1.0,
        decay: 0.007
      });
    }
    window.fxPlayCoin();
    ensureLoopRunning();
  };

  // Particle Burst: Gem Sparkles
  window.fireGemSparkles = function(originX, originY, color = '#00e676', count = 22) {
    initCanvas();
    const startX = originX || window.innerWidth / 2;
    const startY = originY || window.innerHeight / 2;
    const colors = [color, '#ffffff', '#00f2fe', '#ffd700'];

    for (let i = 0; i < count; i++) {
      const angle = Math.random() * Math.PI * 2;
      const speed = Math.random() * 7 + 3;
      particles.push({
        type: 'gem',
        x: startX,
        y: startY,
        vx: Math.cos(angle) * speed,
        vy: Math.sin(angle) * speed,
        gravity: 0.15,
        size: Math.random() * 6 + 7,
        angle: Math.random() * Math.PI,
        vAngle: (Math.random() - 0.5) * 0.3,
        color: colors[Math.floor(Math.random() * colors.length)],
        alpha: 1.0,
        decay: 0.02
      });
    }
    ensureLoopRunning();
  };

  // Screen Vibration Impact
  window.triggerScreenShake = function(targetEl) {
    const el = targetEl || document.querySelector('.game-area') || document.body;
    el.classList.remove('fx-shake');
    void el.offsetWidth; // trigger reflow
    el.classList.add('fx-shake');
    setTimeout(() => el.classList.remove('fx-shake'), 460);
  };

  // ── 3. UNIVERSAL CELEBRATION MODAL ──
  window.showBigWinModal = function(payoutText, multText, onDone) {
    let overlay = document.getElementById('fx-celebrate-modal');
    if (!overlay) {
      overlay = document.createElement('div');
      overlay.id = 'fx-celebrate-modal';
      overlay.className = 'fx-celebrate-overlay';
      overlay.innerHTML = `
        <div class="fx-celebrate-card">
          <div class="fx-celebrate-rays"></div>
          <div class="fx-celebrate-badge">★ BIG WINNER ★</div>
          <div class="fx-celebrate-amount" id="fx-modal-amount">₹0.00</div>
          <div class="fx-celebrate-mult" id="fx-modal-mult">1.00×</div>
          <button class="fx-celebrate-btn" id="fx-modal-close-btn">COLLECT CASH</button>
        </div>
      `;
      document.body.appendChild(overlay);
    }

    document.getElementById('fx-modal-amount').textContent = payoutText || '₹0.00';
    document.getElementById('fx-modal-mult').textContent = multText || '';

    overlay.classList.add('active');
    window.fxPlayWin();
    window.fireGoldCoinShower(window.innerWidth / 2, window.innerHeight * 0.4, 50);

    const closeBtn = document.getElementById('fx-modal-close-btn');
    closeBtn.onclick = () => {
      overlay.classList.remove('active');
      window.fxPlayClick();
      if (typeof onDone === 'function') onDone();
    };
  };

  // ── 4. HIGH RESOLUTION SVG GRAPHICS GENERATOR ──
  window.GG_GRAPHICS = {
    // 3D Faceted Sparkling Emerald Gem SVG
    getGemSvg: function() {
      return `
        <svg viewBox="0 0 100 100" width="46" height="46" style="filter:drop-shadow(0 0 10px rgba(0,230,118,0.7));animation:fxSpringFlip 0.45s cubic-bezier(0.34, 1.56, 0.64, 1)">
          <defs>
            <linearGradient id="gemGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stop-color="#b9f6ca" />
              <stop offset="50%" stop-color="#00e676" />
              <stop offset="100%" stop-color="#00a854" />
            </linearGradient>
            <linearGradient id="gemGrad2" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stop-color="#ffffff" stop-opacity="0.8" />
              <stop offset="100%" stop-color="#ffffff" stop-opacity="0" />
            </linearGradient>
          </defs>
          <polygon points="50,6 88,32 88,68 50,94 12,68 12,32" fill="url(#gemGrad1)" stroke="#ffffff" stroke-width="2" />
          <polygon points="50,6 74,32 50,54 26,32" fill="#69f0ae" />
          <polygon points="50,6 88,32 74,32" fill="#a7f3d0" />
          <polygon points="50,6 26,32 12,32" fill="#34d399" />
          <polygon points="26,32 50,54 50,94 12,68" fill="#059669" />
          <polygon points="74,32 88,68 50,94 50,54" fill="#047857" />
          <polygon points="50,14 65,30 50,42 35,30" fill="url(#gemGrad2)" />
        </svg>
      `;
    },

    // 3D Cyber-Mine Bomb SVG
    getMineSvg: function() {
      return `
        <svg viewBox="0 0 100 100" width="46" height="46" style="filter:drop-shadow(0 0 12px rgba(255,23,68,0.85))">
          <defs>
            <radialGradient id="bombCore" cx="50%" cy="50%" r="50%">
              <stop offset="0%" stop-color="#ff1744" />
              <stop offset="60%" stop-color="#b71c1c" />
              <stop offset="100%" stop-color="#1a0005" />
            </radialGradient>
          </defs>
          <circle cx="50" cy="50" r="32" fill="url(#bombCore)" stroke="#ff5252" stroke-width="2.5" />
          <rect x="47" y="6" width="6" height="14" rx="2" fill="#94a3b8" />
          <rect x="47" y="80" width="6" height="14" rx="2" fill="#94a3b8" />
          <rect x="6" y="47" width="14" height="6" rx="2" fill="#94a3b8" />
          <rect x="80" y="47" width="14" height="6" rx="2" fill="#94a3b8" />
          <circle cx="50" cy="50" r="14" fill="#ff1744" style="animation: fxBorderPulse 1s infinite alternate" />
          <circle cx="50" cy="50" r="6" fill="#ffffff" />
        </svg>
      `;
    },

    // 3D Metallic Vault Unopened Tile Etching
    getVaultPatternSvg: function() {
      return `
        <svg viewBox="0 0 40 40" width="28" height="28" opacity="0.4" style="transition:transform 0.2s">
          <circle cx="20" cy="20" r="12" fill="none" stroke="#64748b" stroke-width="2" stroke-dasharray="4 2" />
          <polygon points="20,10 29,25 11,25" fill="none" stroke="#ffd700" stroke-width="1.5" />
        </svg>
      `;
    }
  };

  console.log('[GG Wins] Universal Graphics, VFX & Procedural Sound Engine loaded ✅');
})();
