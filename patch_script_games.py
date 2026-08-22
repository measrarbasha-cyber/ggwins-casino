games_def = """const GAMES = [
  // Originals - linked to real playable game files
  { id: 1,  name: 'GG Crash',          provider: 'GG Originals',  icon: '🚀', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5821, gameUrl: 'games/crash.html' },
  { id: 2,  name: 'GG Mines',          provider: 'GG Originals',  icon: '💣', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 6420, gameUrl: 'games/mines.html' },
  { id: 3,  name: 'GG Coin Flip',      provider: 'GG Originals',  icon: '🪙', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4890, gameUrl: 'games/coinflip.html' },
  { id: 4,  name: 'GG Sic Bo',         provider: 'GG Originals',  icon: '🎲', grad: 'grad-original-1', category: 'originals', badge: 'new',      players: 3240, gameUrl: 'games/sicbo.html' },
  { id: 5,  name: 'GG Penalty',        provider: 'GG Originals',  icon: '⚽', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5610, gameUrl: 'games/penalty.html' },
  { id: 6,  name: 'GG Magic Shells',   provider: 'GG Originals',  icon: '🪄', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 6180, gameUrl: 'games/cups.html' },
  { id: 7,  name: 'GG Indian Rummy 3D',provider: 'GG Originals',  icon: '🃏', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 7450, gameUrl: 'games/rummy.html' },
  { id: 8,  name: 'GG Baccarat 3D',    provider: 'GG Originals',  icon: '👑', grad: 'grad-original-1', category: 'originals', badge: 'new',      players: 3870, gameUrl: 'games/baccarat.html' },
  { id: 9,  name: 'GG Roulette Royale',provider: 'GG Originals',  icon: '🔴', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4201, gameUrl: 'games/roulette.html' },
  { id: 10, name: 'GG Blackjack 21',   provider: 'GG Originals',  icon: '♣️', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 3980, gameUrl: 'games/blackjack.html' },
  { id: 11, name: 'GG Dice 3D',        provider: 'GG Originals',  icon: '🎲', grad: 'grad-original-1', category: 'originals', badge: 'original', players: 3102, gameUrl: 'games/dice.html' },
  { id: 12, name: 'Dragon Tower',      provider: 'GG Originals',  icon: '🐉', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5120, gameUrl: 'games/dragontower.html' },
  { id: 13, name: 'GG Ludo Champions', provider: 'GG Originals',  icon: '🎲', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 6420, gameUrl: 'games/ludo.html' },
  { id: 14, name: 'GG Diamond Rush',   provider: 'GG Originals',  icon: '💎', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4920, gameUrl: 'games/diamonds.html' },
  { id: 15, name: 'GG Hilo Master',    provider: 'GG Originals',  icon: '🃏', grad: 'grad-original-1', category: 'originals', badge: 'new',      players: 3410, gameUrl: 'games/hilo.html' },
  { id: 16, name: 'GG Limbo Rocket',   provider: 'GG Originals',  icon: '📈', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 3984, gameUrl: 'games/limbo.html' },
  { id: 17, name: 'Wheel of Fortune',  provider: 'GG Originals',  icon: '🎡', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4120, gameUrl: 'games/wheel.html' },
  { id: 18, name: 'GG Keno Classic',   provider: 'GG Originals',  icon: '🎱', grad: 'grad-original-1', category: 'originals', badge: 'new',      players: 2830, gameUrl: 'games/keno.html' },
  { id: 19, name: 'GG Fortune Slots',  provider: 'GG Originals',  icon: '🎰', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 5244, gameUrl: 'games/slots.html' },
  { id: 20, name: 'GG Plinko Drop',    provider: 'GG Originals',  icon: '⚽', grad: 'grad-original-1', category: 'originals', badge: 'hot',      players: 4891, gameUrl: 'games/plinko.html' }
];"""

with open("script.js", "r", encoding="utf-8") as f:
    s = f.read()

import re
s = re.sub(r'const GAMES = \[.*?\];', games_def, s, flags=re.DOTALL)

with open("script.js", "w", encoding="utf-8") as f:
    f.write(s)

print("SUCCESS: script.js GAMES array restored with vivid icons and all 20 direct links!")