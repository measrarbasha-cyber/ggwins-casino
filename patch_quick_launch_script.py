with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

# Update renderGames to render cards into #full-quick-launch-grid
quick_launch_js = """
// ── FULL PAGE QUICK LAUNCH GAMES POPULATOR ──
let activeGamesCategory = 'all';

function filterGamesCategory(category, btn) {
  activeGamesCategory = category;
  document.querySelectorAll('#game-tabs .tab-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderQuickLaunchGames();
}

function renderQuickLaunchGames() {
  const container = document.getElementById('full-quick-launch-grid');
  if (!container) return;

  let filtered = GAMES;
  if (activeGamesCategory !== 'all') {
    filtered = GAMES.filter(g => g.category === activeGamesCategory);
  }

  container.innerHTML = filtered.map(g => {
    const isHot = g.badge === 'hot';
    const tagText = g.category === 'originals' ? '🔥 Original' : g.category === 'table' ? '🃏 Table Royale' : '🎯 Casual & Arcade';
    const playersCount = (g.players || 4200).toLocaleString();

    return `
      <div class="ql-card" onclick="window.location.href='${g.gameUrl}'">
        <div class="ql-card-top">
          <div class="ql-icon-box">${g.icon}</div>
          <div class="ql-meta">
            <div class="ql-title">${g.name}</div>
            <div class="ql-sub">
              <span class="ql-tag">${tagText}</span>
              ${isHot ? '<span style="font-size:9px;background:rgba(239,68,68,0.18);color:#ef4444;padding:2px 5px;border-radius:4px;font-weight:900">HOT</span>' : ''}
            </div>
          </div>
        </div>

        <div class="ql-stats-row">
          <span style="color:#94a3b8">Live Players</span>
          <span style="font-weight:800;color:#ffd700">👥 ${playersCount}</span>
        </div>

        <button class="ql-play-btn" onclick="event.stopPropagation(); window.location.href='${g.gameUrl}'">
          ⚡ Quick Launch ${g.name}
        </button>
      </div>
    `;
  }).join('');
}

// ── AUTO-ROTATING HERO CAROUSEL ENGINE ──
let heroCurrentSlide = 0;
let heroSlideInterval = null;

function initHeroSlider() {
  const heroSlides = document.querySelectorAll('.carousel-slide');
  const heroDots = document.querySelectorAll('.carousel-dots .dot');
  if (!heroSlides.length) return;

  function showSlide(idx) {
    heroSlides.forEach((sl, i) => sl.classList.toggle('active', i === idx));
    heroDots.forEach((dt, i) => dt.classList.toggle('active', i === idx));
    heroCurrentSlide = idx;
  }

  function nextSlide() {
    showSlide((heroCurrentSlide + 1) % heroSlides.length);
  }

  function prevSlide() {
    showSlide((heroCurrentSlide - 1 + heroSlides.length) % heroSlides.length);
  }

  function startAutoRotate() {
    clearInterval(heroSlideInterval);
    heroSlideInterval = setInterval(nextSlide, 4500);
  }

  const prevBtn = document.getElementById('prev-slide-btn');
  const nextBtn = document.getElementById('next-slide-btn');
  if (prevBtn) prevBtn.addEventListener('click', (e) => { e.stopPropagation(); prevSlide(); startAutoRotate(); });
  if (nextBtn) nextBtn.addEventListener('click', (e) => { e.stopPropagation(); nextSlide(); startAutoRotate(); });

  heroDots.forEach((dt, idx) => {
    dt.addEventListener('click', (e) => {
      e.stopPropagation();
      showSlide(idx);
      startAutoRotate();
    });
  });

  const carouselBox = document.getElementById('hero-carousel');
  if (carouselBox) {
    carouselBox.addEventListener('mouseenter', () => clearInterval(heroSlideInterval));
    carouselBox.addEventListener('mouseleave', startAutoRotate);
  }

  startAutoRotate();
}

document.addEventListener('DOMContentLoaded', () => {
  renderQuickLaunchGames();
  initHeroSlider();
});
renderQuickLaunchGames();
initHeroSlider();
"""

if "renderQuickLaunchGames" not in s:
    s += "\n" + quick_launch_js

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js updated with full-page quick launch games rendering & auto-rotating hero slider!")