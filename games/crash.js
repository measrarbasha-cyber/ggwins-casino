// ── BALANCE ──────────────────────────────────
function updateBalUI(){ updateAllWalletDisplays(); }

// ── STATE ─────────────────────────────────────
let phase = 'waiting'; // waiting | running | crashed
let multiplier = 1.00;
let crashPoint = 2.00;
let startTime = null;
let betPlaced = false;
let betAmount = 0;
let autoCashedOut = false;
let myBetMultiplier = null;
let totalProfit = 0;
let wins = 0;
let losses = 0;
let historyData = [];
let animFrame = null;
let countdownVal = 5;
let countdownTimer = null;
let autoBetsLeft = 0;
let mode = 'manual';

// Canvas
const canvas = document.getElementById('crash-canvas');
const ctx = canvas.getContext('2d');
const points = [];
let maxTime = 10000;
let gameStartTime = null;

function resizeCanvas(){
  const parent = canvas.parentElement;
  canvas.width = parent.clientWidth;
  canvas.height = parent.clientHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// ── CRASH POINT GENERATION (HEAVILY HOUSE-BIASED) ────
function genCrashPoint(){
  const isDemo = (typeof getActiveWalletKey === 'function' ? getActiveWalletKey() : (localStorage.getItem('ggwins_active_wallet') || 'demo')) === 'demo';
  if (isDemo) return parseFloat((4.50 + Math.random() * 10.0).toFixed(2));
  const r = Math.random();
  // 50% instant crash between 1.00x and 1.16x
  if(r < 0.50) return parseFloat((1.00 + Math.random() * 0.10).toFixed(2));
  // 35% low crash between 1.17x and 1.48x
  if(r < 0.85) return parseFloat((1.17 + Math.random() * 0.20).toFixed(2));
  // 12% crash between 1.49x and 2.05x
  if(r < 0.97) return parseFloat((1.49 + Math.random() * 0.35).toFixed(2));
  // 3% rare spike up to 2.80x
  return parseFloat((1.65 + Math.random() * 0.40).toFixed(2));
}

// ── FAKE LIVE BETS ────────────────────────────
const fakeNames = ['Shadow***','Crypto***','Star***','Gold***','Pro***','Win***','Ace***','King***','Fire***','Blaze***'];
let fakeBets = [];

function generateFakeBets(){
  fakeBets = Array.from({length: Math.floor(Math.random()*8)+3}, () => ({
    name: fakeNames[Math.floor(Math.random()*fakeNames.length)],
    amount: (Math.random()*200+0.5).toFixed(2),
    cashoutAt: Math.random() < 0.6 ? (Math.random()*5+1.2).toFixed(2) : null,
    cashedOut: false,
    cashedOutAt: null
  }));
  renderFakeBets();
}

function renderFakeBets(){
  const list = document.getElementById('live-bet-list');
  list.innerHTML = '';
  fakeBets.slice(0,6).forEach(b => {
    const row = document.createElement('div');
    row.className = 'live-bet-row';
    const val = b.cashedOut
          ? `<span class="lb-val cashed">${b.cashedOutAt}×</span>`
          : `<span class="lb-val">$${b.amount}</span>`;
    row.innerHTML = `<span class="lb-name">${b.name}</span>${val}`;
    list.appendChild(row);
  });
}

function updateFakeCashouts(){
  fakeBets.forEach(b => {
    if(!b.cashedOut && b.cashoutAt && multiplier >= parseFloat(b.cashoutAt)){
      b.cashedOut = true;
      b.cashedOutAt = parseFloat(b.cashoutAt).toFixed(2);
    }
  });
  renderFakeBets();
}

// ── PARTICLES & STARFIELD STATE ────────────────
let stars = [];
let thrustParticles = [];
let explosionParticles = [];
let shockwaveRadius = 0;

function initStars(W, H){
  stars = [];
  for(let i=0; i<60; i++){
    stars.push({
      x: Math.random() * W,
      y: Math.random() * H,
      size: Math.random() * 2 + 0.5,
      speed: Math.random() * 0.8 + 0.2,
      brightness: Math.random() * 0.7 + 0.3
    });
  }
}

// ── CANVAS DRAW ───────────────────────────────
function drawCanvas(){
  const W = canvas.width, H = canvas.height;
  if(stars.length === 0) initStars(W, H);
  ctx.clearRect(0, 0, W, H);

  // Deep space background gradient
  const grad = ctx.createLinearGradient(0,0,W,H);
  grad.addColorStop(0, '#040810');
  grad.addColorStop(0.5, '#091322');
  grad.addColorStop(1, '#050b14');
  ctx.fillStyle = grad;
  ctx.fillRect(0,0,W,H);

  // Starfield animation
  stars.forEach(s => {
    if(phase === 'running'){
      s.x -= s.speed * (1 + multiplier * 0.1);
      if(s.x < 0) s.x = W;
    }
    ctx.fillStyle = `rgba(255,255,255,${s.brightness})`;
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.size, 0, Math.PI*2);
    ctx.fill();
  });

  if(phase === 'crashed'){
    ctx.fillStyle = 'rgba(239,83,80,0.08)';
    ctx.fillRect(0,0,W,H);
  }

  if(points.length < 2) return;

  const currMult = multiplier;
  const logMax = Math.log(Math.max(currMult * 1.25, 2));
  const timeSpan = Math.max(Date.now() - gameStartTime, 1000);

  function toCanvas(t, m){
    const x = (t / timeSpan) * (W - 70) + 40;
    const y = H - 35 - (Math.log(m) / logMax) * (H - 70);
    return [x, y];
  }

  // Grid lines
  ctx.strokeStyle = 'rgba(255,255,255,0.04)';
  ctx.lineWidth = 1;
  for(let i=0; i<=4; i++){
    const y = 35 + (i/4)*(H-70);
    ctx.beginPath(); ctx.moveTo(35,y); ctx.lineTo(W-30,y); ctx.stroke();
    const mult = Math.exp((1 - i/4) * logMax);
    ctx.fillStyle = 'rgba(255,255,255,0.35)';
    ctx.font = '11px Space Grotesk, sans-serif';
    ctx.fillText(mult.toFixed(1)+'×', 6, y+4);
  }

  // Curve fill gradient
  const isCrashed = phase === 'crashed';
  const color = isCrashed ? '#ef4444' : '#00e676';
  ctx.beginPath();
  const [x0,y0] = toCanvas(0, 1);
  ctx.moveTo(x0, y0);
  points.forEach(p => {
    const [x,y] = toCanvas(p.t, p.m);
    ctx.lineTo(x,y);
  });
  const [lastX, lastY] = toCanvas(points[points.length-1].t, points[points.length-1].m);
  ctx.lineTo(lastX, H-35);
  ctx.lineTo(x0, H-35);
  ctx.closePath();

  const fillGrad = ctx.createLinearGradient(0, lastY, 0, H-35);
  fillGrad.addColorStop(0, isCrashed ? 'rgba(239,68,68,0.35)' : 'rgba(0,230,118,0.3)');
  fillGrad.addColorStop(1, 'rgba(0,0,0,0)');
  ctx.fillStyle = fillGrad;
  ctx.fill();

  // Glow line
  ctx.beginPath();
  ctx.moveTo(x0, y0);
  points.forEach(p => {
    const [x,y] = toCanvas(p.t, p.m);
    ctx.lineTo(x,y);
  });
  ctx.strokeStyle = color;
  ctx.lineWidth = 4;
  ctx.lineCap = 'round';
  ctx.lineJoin = 'round';
  ctx.shadowColor = color;
  ctx.shadowBlur = 16;
  ctx.stroke();
  ctx.shadowBlur = 0;

  // Rocket & Flame Thrust Particles
  if(!isCrashed){
    // Spawn thrust particles
    for(let i=0; i<3; i++){
      thrustParticles.push({
        x: lastX - 8,
        y: lastY + 6,
        vx: (Math.random() - 0.7) * 4 - 2,
        vy: (Math.random() - 0.3) * 3 + 1,
        size: Math.random() * 5 + 2,
        color: Math.random() > 0.5 ? '#ff9100' : '#ffd600',
        alpha: 1
      });
    }

    // Render thrust particles
    for(let i = thrustParticles.length - 1; i >= 0; i--){
      const p = thrustParticles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.size *= 0.94;
      p.alpha -= 0.04;
      if(p.alpha <= 0 || p.size < 0.5){
        thrustParticles.splice(i, 1);
      } else {
        ctx.fillStyle = p.color;
        ctx.globalAlpha = Math.max(0, p.alpha);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
        ctx.fill();
        ctx.globalAlpha = 1;
      }
    }

    // Draw Rocket
    ctx.font = '26px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('🚀', lastX + 6, lastY - 6);
  } else {
    // Render Explosion & Shockwave
    if(shockwaveRadius < 90){
      shockwaveRadius += 4;
      ctx.strokeStyle = `rgba(239,68,68,${Math.max(0, 1 - shockwaveRadius/90)})`;
      ctx.lineWidth = 3;
      ctx.beginPath();
      ctx.arc(lastX, lastY, shockwaveRadius, 0, Math.PI*2);
      ctx.stroke();
    }

    // Render explosion debris
    for(let i = explosionParticles.length - 1; i >= 0; i--){
      const p = explosionParticles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.alpha -= 0.025;
      if(p.alpha <= 0){
        explosionParticles.splice(i, 1);
      } else {
        ctx.fillStyle = p.color;
        ctx.globalAlpha = Math.max(0, p.alpha);
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI*2);
        ctx.fill();
        ctx.globalAlpha = 1;
      }
    }

    ctx.font = '32px sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('💥', lastX, lastY);
  }
}

// ── GAME LOOP ─────────────────────────────────
function startGame(){ if(typeof requireAuth==="function" && !requireAuth()) return;
  phase = 'running';
  gameStartTime = Date.now();
  startTime = Date.now();
  points.length = 0;
  multiplier = 1.00;
  autoCashedOut = false;
  generateFakeBets();

  const multEl = document.getElementById('mult-value');
  const lblEl = document.getElementById('mult-label');
  if(multEl) { multEl.className = 'mult-value'; multEl.textContent = '1.00×'; }
  if(lblEl) lblEl.textContent = 'CURRENT MULTIPLIER';

  if(betPlaced){
    const cb = document.getElementById('cashout-btn');
    if(cb) cb.disabled = false;
  }

  function loop(){
    const elapsed = Date.now() - startTime;
    multiplier = Math.pow(Math.E, 0.000065 * elapsed);

    // Auto cashout check
    const autoCashToggle = document.getElementById('auto-cashout-toggle');
    const autoCashVal = parseFloat(document.getElementById('auto-cashout-val').value) || 2;
    if(betPlaced && !autoCashedOut && autoCashToggle && autoCashToggle.checked && multiplier >= autoCashVal){
      cashOut();
      autoCashedOut = true;
    }

    updateFakeCashouts();
    points.push({ t: elapsed, m: multiplier });

    if(multEl) multEl.textContent = multiplier.toFixed(2) + '×';

    if(multiplier >= crashPoint){
      crash();
      return;
    }

    drawCanvas();
    animFrame = requestAnimationFrame(loop);
  }
  animFrame = requestAnimationFrame(loop);
}

function crash(){
  phase = 'crashed';
  cancelAnimationFrame(animFrame);

  // Spawn explosion debris
  explosionParticles = [];
  shockwaveRadius = 0;
  for(let i=0; i<45; i++){
    explosionParticles.push({
      x: canvas.width * 0.7,
      y: canvas.height * 0.3,
      vx: (Math.random() - 0.5) * 12,
      vy: (Math.random() - 0.5) * 12,
      size: Math.random() * 6 + 2,
      color: ['#ef4444', '#f97316', '#eab308', '#ffffff'][Math.floor(Math.random() * 4)],
      alpha: 1
    });
  }

  // Animate explosion aftermath
  let postCrashFrames = 0;
  function postCrashLoop(){
    if(postCrashFrames < 60){
      drawCanvas();
      postCrashFrames++;
      requestAnimationFrame(postCrashLoop);
    }
  }
  requestAnimationFrame(postCrashLoop);

  const multEl = document.getElementById('mult-value');
  const lblEl = document.getElementById('mult-label');
  if(multEl){
    multEl.className = 'mult-value crashed';
    multEl.textContent = crashPoint.toFixed(2) + '×';
  }
  if(lblEl) lblEl.textContent = 'CRASHED';

  const cb = document.getElementById('cashout-btn');
  if(cb) cb.disabled = true;

  if(typeof playGameSound === 'function') playGameSound('bomb');

  if(betPlaced && !autoCashedOut){
    resolveLoss();
  }

  addToHistory(crashPoint);
  betPlaced = false;

  const btn = document.getElementById('bet-btn');
  if(btn){ btn.disabled = false; btn.textContent = 'Place Bet'; }

  setTimeout(startWaiting, 3200);
}

function cashOut(){
  if(!betPlaced || autoCashedOut) return;
  autoCashedOut = true;

  const payout = betAmount * multiplier;
  const profit = payout - betAmount;
  setBalance(getBalance() + payout);
  totalProfit += profit;
  wins++;
  updateStats();
  addMyHistory(multiplier, true);
  showResult(true, payout, multiplier);
  betPlaced = false;
  myBetMultiplier = multiplier;

  if(typeof playGameSound === 'function') playGameSound('win');
  if(typeof trackGameWager === 'function') trackGameWager('GG Crash', betAmount, payout, true);

  const balEl = document.getElementById('bal-display');
  if(balEl){
    balEl.classList.remove('flash-win');
    void balEl.offsetWidth;
    balEl.classList.add('flash-win');
  }

  const btn = document.getElementById('cashout-btn');
  if(btn) { btn.disabled = true; btn.textContent = 'Cash Out'; }
}

function resolveLoss(){
  totalProfit -= betAmount;
  losses++;
  updateStats();
  addMyHistory(crashPoint, false);
  showResult(false, betAmount, crashPoint);
  if(typeof trackGameWager === 'function') trackGameWager('GG Crash', betAmount, 0, false);
}

function startWaiting(){
  phase = 'waiting';
  betPlaced = false;
  autoCashedOut = false;
  crashPoint = genCrashPoint();
  countdownVal = 5;
  points.length = 0;

  const multEl = document.getElementById('mult-value');
  const lblEl = document.getElementById('mult-label');
  if(multEl) { multEl.className = 'mult-value'; multEl.textContent = '1.00×'; }
  if(lblEl) lblEl.textContent = `Starting in ${countdownVal}s`;

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  drawCanvas();

  const btn = document.getElementById('bet-btn');
  if(btn){ btn.textContent = 'Place Bet'; btn.disabled = false; }

  countdownTimer = setInterval(() => {
    countdownVal--;
    if(lblEl) lblEl.textContent = `Starting in ${countdownVal}s`;
    if(countdownVal <= 0){
      clearInterval(countdownTimer);
      startGame();
    }
  }, 1000);
}

function placeBet(){
  const amt = parseFloat(document.getElementById('bet-amount').value);
  if(isNaN(amt) || amt <= 0){ showToast('Enter a valid bet amount'); return; }
  if(amt > getBalance()){ showToast('Insufficient balance'); return; }
  if(betPlaced){ showToast('Bet already placed for this round'); return; }

  betAmount = amt;
  setBalance(getBalance() - amt);
  betPlaced = true;

  if(typeof playGameSound === 'function') playGameSound('bet');

  const btn = document.getElementById('bet-btn');
  if(btn){ btn.textContent = 'Bet Placed ✓'; btn.disabled = true; }

  if(phase === 'running'){
    const cb = document.getElementById('cashout-btn');
    if(cb) cb.disabled = false;
  }
}

// Unused legacy function; kept for compatibility
function handleBetBtn(){
  // No action needed as UI uses separate start and cashout buttons
}

function halveBet(){
  const inp = document.getElementById('bet-amount');
  inp.value = Math.max(0.01, parseFloat(inp.value||1)/2).toFixed(2);
}
function doubleBet(){
  const inp = document.getElementById('bet-amount');
  inp.value = Math.min(getBalance(), parseFloat(inp.value||1)*2).toFixed(2);
}
function maxBet(){
  document.getElementById('bet-amount').value = getBalance().toFixed(2);
}

// Live cashout button text update
setInterval(() => {
  if(phase === 'running' && betPlaced){
      const btn = document.getElementById('cashout-btn');
      btn.textContent = `Cash Out ₹${(betAmount * multiplier).toFixed(2)}`;
  }
}, 100);

// ── HISTORY ───────────────────────────────────
function addToHistory(crash){
  historyData.unshift(crash);
  if(historyData.length > 20) historyData.pop();
  const container = document.getElementById('crash-history');
  container.innerHTML = '';
  historyData.forEach(c => {
    const chip = document.createElement('div');
    chip.className = 'crash-chip ' + (c < 1.5 ? 'low' : c < 3 ? 'mid' : c < 10 ? 'high' : 'mega');
    chip.textContent = c.toFixed(2) + '×';
    container.appendChild(chip);
  });
}

function addMyHistory(mult, won){
  const container = document.getElementById('my-history');
  const chip = document.createElement('div');
  chip.className = 'hchip ' + (won ? 'win' : 'lose');
  chip.textContent = mult.toFixed(2) + '×';
  container.insertBefore(chip, container.firstChild);
  if(container.children.length > 15) container.removeChild(container.lastChild);
}

// ── STATS ─────────────────────────────────────
function updateStats(){
  const profEl = document.getElementById('stat-profit');
  profEl.textContent = (totalProfit >= 0 ? '+' : '') + '₹' + totalProfit.toFixed(2);
  profEl.className = 'stat-box-val ' + (totalProfit >= 0 ? 'green' : 'red');
  document.getElementById('stat-wins').textContent = wins;
  document.getElementById('stat-losses').textContent = losses;
}

// ── RESULT BOX ────────────────────────────────
function showResult(won, amount, mult){
  const c = document.getElementById('result-container');
  c.innerHTML = `<div class="result-box ${won?'win':'lose'}">
    <div class="result-box-title">${won ? '🎉 Cashed Out' : '💥 Crashed at'}</div>
    <div class="result-box-val">${won ? '+₹'+amount.toFixed(2) : mult.toFixed(2)+'×'}</div>
  </div>`;
  setTimeout(() => c.innerHTML = '', 4000);
}

// ── MODE TABS ─────────────────────────────────
document.querySelectorAll('#mode-tabs .seg-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#mode-tabs .seg-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    mode = btn.dataset.mode;
    document.getElementById('auto-section').style.display = mode === 'auto' ? 'block' : 'none';
    if(mode === 'auto'){
      autoBetsLeft = parseInt(document.getElementById('auto-bets-count').value) || 10;
    }
  });
});

function showToast(msg){
  const t = document.createElement('div');
  t.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#1e2d3d;border:1px solid rgba(255,255,255,0.1);color:#e8edf5;padding:10px 16px;border-radius:8px;font-size:13px;z-index:999;animation:fadeIn 0.3s ease';
  t.textContent = msg;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2500);
}

// ── INIT FIRST ROUND ─────────────────────────
[1.05, 4.12, 2.88, 1.42, 11.5, 1.22, 7.33, 2.01, 1.85, 25.4].forEach(v => addToHistory(v));
crashPoint = genCrashPoint();
startWaiting();

