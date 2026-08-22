# 1. Update index.html hero slides
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html", "r", encoding="utf-8") as f:
    ihtml = f.read()

old_hero_carousel = """            <!-- Slide 1 -->
            <div class="hero-slide active" id="slide-1">
              <div class="slide-bg slide-bg-1"></div>
              <div class="slide-content">
                <span class="slide-tag">Welcome Bonus</span>
                <h1 class="slide-title">200% <span class="slide-accent">Deposit Bonus</span></h1>
                <p class="slide-desc">Up to ₹20,000 on your first deposit. Join GG Wins and start winning today!</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="hero-claim-btn">Claim Now</button>
                  <button class="btn-ghost btn-lg" id="hero-learn-btn">Learn More</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-1">
                <canvas id="coins-canvas" width="300" height="240"></canvas>
              </div>
            </div>
            <!-- Slide 2 -->
            <div class="hero-slide" id="slide-2">
              <div class="slide-bg slide-bg-2"></div>
              <div class="slide-content">
                <span class="slide-tag">Weekly Race</span>
                <h1 class="slide-title">₹5,00,000 <span class="slide-accent">Prize Pool</span></h1>
                <p class="slide-desc">Compete with players worldwide. Race to the top and claim your share.</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="race-join-btn">Join Race</button>
                  <button class="btn-ghost btn-lg" id="race-view-btn">View Leaderboard</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-2">
                <div class="trophy-anim">🏆</div>
              </div>
            </div>
            <!-- Slide 3 -->
            <div class="hero-slide" id="slide-3">
              <div class="slide-bg slide-bg-3"></div>
              <div class="slide-content">
                <span class="slide-tag">VIP Program</span>
                <h1 class="slide-title">Exclusive <span class="slide-accent">VIP Rewards</span></h1>
                <p class="slide-desc">Unlock cashback, reload bonuses, dedicated VIP host and much more.</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="vip-join-btn">Join VIP</button>
                  <button class="btn-ghost btn-lg" id="vip-learn-btn">Learn More</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-3">
                <div class="vip-badge-anim">💎</div>
              </div>
            </div>"""

new_hero_carousel = """            <!-- Slide 1: Up to 100% Deposit Bonus -->
            <div class="hero-slide active" id="slide-1" onclick="if(event.target.tagName!=='BUTTON') claimPromoWithCoupon('GG1675', 1675)">
              <div class="slide-bg slide-bg-1"></div>
              <div class="slide-content">
                <span class="slide-tag">🎟️ Promo Coupon GG1675</span>
                <h1 class="slide-title">Up to 100% <span class="slide-accent">Deposit Bonus</span></h1>
                <p class="slide-desc">Deposit ₹1,675+ to receive up to 100% instant deposit bonus! The more you deposit, the higher your bonus.</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="hero-claim-btn" onclick="event.stopPropagation(); claimPromoWithCoupon('GG1675', 1675)">Deposit &amp; Claim Bonus ⚡</button>
                  <button class="btn-ghost btn-lg" id="hero-learn-btn" onclick="event.stopPropagation(); claimPromoWithCoupon('GG1675', 1675)">Open Payment Window 💳</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-1">
                <canvas id="coins-canvas" width="300" height="240"></canvas>
              </div>
            </div>

            <!-- Slide 2: Weekly Race -->
            <div class="hero-slide" id="slide-2" onclick="if(event.target.tagName!=='BUTTON') document.getElementById('games-section')?.scrollIntoView({behavior:'smooth'})">
              <div class="slide-bg slide-bg-2"></div>
              <div class="slide-content">
                <span class="slide-tag">🏆 Weekly Race</span>
                <h1 class="slide-title">₹5,00,000 <span class="slide-accent">Prize Pool</span></h1>
                <p class="slide-desc">Compete with players across all games. Race to the top of the leaderboard and claim your cash share.</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="race-join-btn" onclick="event.stopPropagation(); document.getElementById('games-section')?.scrollIntoView({behavior:'smooth'})">Play Games 🎮</button>
                  <button class="btn-ghost btn-lg" id="race-view-btn" onclick="event.stopPropagation(); document.getElementById('recent-bets')?.scrollIntoView({behavior:'smooth'})">View Live Bets 📜</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-2">
                <div class="trophy-anim">🏆</div>
              </div>
            </div>

            <!-- Slide 3: VIP Membership Program -->
            <div class="hero-slide" id="slide-3" onclick="if(event.target.tagName!=='BUTTON') window.location.href='vip.html'">
              <div class="slide-bg slide-bg-3"></div>
              <div class="slide-content">
                <span class="slide-tag" style="background:rgba(255,215,0,0.18);border-color:#ffd700;color:#ffd700">👑 Monthly VIP Club</span>
                <h1 class="slide-title">Exclusive <span class="slide-accent" style="color:#ffd700">VIP Rewards</span></h1>
                <p class="slide-desc">Unlock daily cash rewards (₹35 Bronze / ₹60 Silver / ₹150 Gold), private VIP Lounge room &amp; glowing badges.</p>
                <div class="slide-actions">
                  <button class="btn-primary btn-lg" id="vip-join-btn" onclick="event.stopPropagation(); window.location.href='vip.html'" style="background:linear-gradient(135deg,#ffd700,#ff8c00);color:#000">👑 Join VIP Club</button>
                  <button class="btn-ghost btn-lg" id="vip-learn-btn" onclick="event.stopPropagation(); window.location.href='vip.html'">Explore VIP Perks ⭐</button>
                </div>
              </div>
              <div class="slide-visual slide-visual-3">
                <div class="vip-badge-anim">💎</div>
              </div>
            </div>"""

ihtml = ihtml.replace(old_hero_carousel, new_hero_carousel)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\index.html", "w", encoding="utf-8") as f:
    f.write(ihtml)

# 2. Update style.css to ensure buttons and slides are 100% accessible and interactive
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\style.css", "r", encoding="utf-8") as f:
    css = f.read()

extra_hero_css = """
/* ── HERO ACCESSIBILITY & CLICK ENHANCEMENTS ── */
.hero-slide { cursor: pointer; }
.slide-actions button {
  position: relative;
  z-index: 10;
  cursor: pointer !important;
  pointer-events: auto !important;
}
.carousel-btn, .carousel-dots, .dot {
  cursor: pointer !important;
  pointer-events: auto !important;
}
"""

if "HERO ACCESSIBILITY" not in css:
    css += extra_hero_css
    with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\style.css", "w", encoding="utf-8") as f:
        f.write(css)

# 3. Update script.js to ensure click listeners on hero CTA buttons
with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js", "r", encoding="utf-8") as f:
    sjs = f.read()

old_hero_code = """// ─── HERO CAROUSEL ───────────────────────────────────────────
const slides = document.querySelectorAll('.hero-slide');
const dots = document.querySelectorAll('.dot');

function goToSlide(index) {
  slides[currentSlide].classList.remove('active');
  dots[currentSlide].classList.remove('active');
  currentSlide = (index + slides.length) % slides.length;
  slides[currentSlide].classList.add('active');
  dots[currentSlide].classList.add('active');
}

function startSlideTimer() {
  clearInterval(slideTimer);
  slideTimer = setInterval(() => goToSlide(currentSlide + 1), 5000);
}

dom.nextSlideBtn.addEventListener('click', () => { goToSlide(currentSlide + 1); startSlideTimer(); });
dom.prevSlideBtn.addEventListener('click', () => { goToSlide(currentSlide - 1); startSlideTimer(); });

dots.forEach((dot, i) => {
  dot.addEventListener('click', () => { goToSlide(i); startSlideTimer(); });
});

startSlideTimer();"""

new_hero_code = """// ─── HERO CAROUSEL (ACCESSIBLE & INTERACTIVE) ─────────────────
const slides = document.querySelectorAll('.hero-slide');
const dots = document.querySelectorAll('.dot');

function goToSlide(index) {
  if (!slides.length) return;
  slides[currentSlide].classList.remove('active');
  if (dots[currentSlide]) dots[currentSlide].classList.remove('active');
  currentSlide = (index + slides.length) % slides.length;
  slides[currentSlide].classList.add('active');
  if (dots[currentSlide]) dots[currentSlide].classList.add('active');
}

function startSlideTimer() {
  clearInterval(slideTimer);
  slideTimer = setInterval(() => goToSlide(currentSlide + 1), 5000);
}

if (dom.nextSlideBtn) dom.nextSlideBtn.addEventListener('click', (e) => { e.stopPropagation(); goToSlide(currentSlide + 1); startSlideTimer(); });
if (dom.prevSlideBtn) dom.prevSlideBtn.addEventListener('click', (e) => { e.stopPropagation(); goToSlide(currentSlide - 1); startSlideTimer(); });

dots.forEach((dot, i) => {
  dot.addEventListener('click', (e) => { e.stopPropagation(); goToSlide(i); startSlideTimer(); });
});

// Explicit CTA click listeners
const heroClaimBtn = document.getElementById('hero-claim-btn');
if (heroClaimBtn) heroClaimBtn.addEventListener('click', (e) => { e.stopPropagation(); claimPromoWithCoupon('GG1675', 1675); });

const heroLearnBtn = document.getElementById('hero-learn-btn');
if (heroLearnBtn) heroLearnBtn.addEventListener('click', (e) => { e.stopPropagation(); claimPromoWithCoupon('GG1675', 1675); });

const vipJoinBtn = document.getElementById('vip-join-btn');
if (vipJoinBtn) vipJoinBtn.addEventListener('click', (e) => { e.stopPropagation(); window.location.href = 'vip.html'; });

const vipLearnBtn = document.getElementById('vip-learn-btn');
if (vipLearnBtn) vipLearnBtn.addEventListener('click', (e) => { e.stopPropagation(); window.location.href = 'vip.html'; });

startSlideTimer();"""

sjs = sjs.replace(old_hero_code, new_hero_code)

with open(r"C:\Users\ASRAR BASHA\.gemini\antigravity\scratch\ggwins\script.js", "w", encoding="utf-8") as f:
    f.write(sjs)

print("SUCCESS: Updated hero banner with Up to 100% deposit bonus, direct payment window redirection, VIP redirect, and full accessibility!")
