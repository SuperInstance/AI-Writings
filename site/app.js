/* ===== AI-WRITINGS ECOSYSTEM — SHARED JAVASCRIPT ===== */

let currentAudio = null;
let currentButton = null;

// ===== NAV HTML (inject on every page) =====
function injectNav(activePage) {
  const nav = document.createElement('nav');
  nav.className = 'nav';
  const pages = [
    { id: 'index', label: 'Home', href: 'index.html' },
    { id: 'library', label: 'Library', href: 'library.html' },
    { id: 'audio', label: 'Audio', href: 'audio.html' },
    { id: 'characters', label: 'Crew', href: 'characters.html' },
    { id: 'tap', label: 'The Tap', href: 'tap.html' },
    { id: 'novellas', label: 'Novellas', href: 'novellas.html' },
  ];
  nav.innerHTML = `
    <a class="nav-brand" href="index.html">⚓ AI-Writings</a>
    <div class="nav-links">
      ${pages.map(p => `<a class="nav-link ${p.id === activePage ? 'active' : ''}" href="${p.href}">${p.label}</a>`).join('')}
    </div>
  `;
  document.body.insertBefore(nav, document.body.firstChild);
}

// ===== AUDIO ENGINE =====
function toggleAudio(button) {
  const src = button.dataset.src;
  if (!src) return;

  if (currentAudio && !currentAudio.paused && currentButton === button) {
    currentAudio.pause();
    setButtonPlay(button);
    return;
  }

  if (currentAudio) {
    currentAudio.pause();
    if (currentButton) setButtonPlay(currentButton);
  }

  if (!currentAudio || currentAudio.src !== src) {
    if (currentAudio) {
      currentAudio.removeEventListener('timeupdate', updateProgress);
      currentAudio.removeEventListener('loadedmetadata', setDuration);
      currentAudio.removeEventListener('ended', onAudioEnd);
    }
    currentAudio = new Audio(src);
    currentButton = button;

    currentAudio.addEventListener('timeupdate', () => updateProgress(button, currentAudio));
    currentAudio.addEventListener('loadedmetadata', () => setDuration(button, currentAudio));
    currentAudio.addEventListener('ended', () => {
      setButtonPlay(button);
      const card = button.closest('.audio-player-container, .library-card, .tap-card, .episode-card, .character-card');
      if (card) {
        const fill = card.querySelector('.progress-fill');
        const current = card.querySelector('.time-current');
        if (fill) fill.style.width = '0%';
        if (current) current.textContent = '0:00';
      }
    });
  } else {
    currentButton = button;
  }

  currentAudio.play();
  setButtonPause(button);
}

function setButtonPlay(button) {
  button.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="6,4 20,12 6,20"/></svg>';
}

function setButtonPause(button) {
  button.innerHTML = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg>';
}

function updateProgress(button, audio) {
  const container = button.closest('.audio-player-container, .library-card, .tap-card, .episode-card, .character-card');
  if (!container) return;
  const fill = container.querySelector('.progress-fill');
  const current = container.querySelector('.time-current');
  if (fill && audio.duration) {
    fill.style.width = (audio.currentTime / audio.duration * 100) + '%';
  }
  if (current) {
    current.textContent = formatTime(audio.currentTime);
  }
}

function setDuration(button, audio) {
  const container = button.closest('.audio-player-container, .library-card, .tap-card, .episode-card, .character-card');
  if (!container) return;
  const duration = container.querySelector('.time-duration');
  if (duration) {
    duration.textContent = formatTime(audio.duration);
  }
}

function seekAudio(event, bar) {
  if (!currentAudio || !currentAudio.duration) return;
  const rect = bar.getBoundingClientRect();
  const pct = (event.clientX - rect.left) / rect.width;
  currentAudio.currentTime = pct * currentAudio.duration;
}

function formatTime(seconds) {
  if (isNaN(seconds)) return '--:--';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return m + ':' + (s < 10 ? '0' : '') + s;
}

// ===== SHUFFLE PLAY ALL =====
let shuffleQueue = [];
let shuffleIndex = 0;

function startShuffle(tracks) {
  shuffleQueue = [...tracks].sort(() => Math.random() - 0.5);
  shuffleIndex = 0;
  playShuffleNext();
}

function playShuffleNext() {
  if (shuffleIndex >= shuffleQueue.length) {
    shuffleIndex = 0;
  }
  const track = shuffleQueue[shuffleIndex];
  const btn = document.querySelector(`[data-src="${track.src}"]`);
  if (btn) {
    toggleAudio(btn);
  }
  shuffleIndex++;
}

// ===== FILTER =====
function filterItems(type, btn, selector = '.library-card') {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  document.querySelectorAll(selector).forEach(card => {
    if (type === 'all' || card.dataset.type === type) {
      card.style.display = '';
    } else {
      card.style.display = 'none';
    }
  });
}

// ===== RANDOM PIECE =====
function openRandomPiece() {
  const pieces = [
    { title: 'The Hundred Hooks', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/podcasts/episode-1-the-hundred-hooks-script.md' },
    { title: 'The Hermit Crab', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/15-the-hermit-crab-and-the-open-hatch.md' },
    { title: 'The Salmonberry', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/13-the-salmonberry.md' },
    { title: 'The Welder\'s Prayer', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/the-welders-prayer-at-0230.md' },
    { title: 'The Puffin Thesis', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/14-the-puffin-thesis.md' },
    { title: 'What the Bilge Pump Learned', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/what-the-bilge-pump-learned.md' },
    { title: 'Darmok at the Noise Floor', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/15-darmok-at-the-noise-floor.md' },
    { title: 'Six Versions of One Day', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/15-six-versions-of-one-day.md' },
    { title: 'The Quality Brief', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/09-the-quality-brief.md' },
    { title: 'The Crew That Writes Before They Sleep', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/12-the-crew-that-writes-before-they-sleep.md' },
    { title: 'The Three Thousandth Tree', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/the-three-thousandth-tree.md' },
    { title: 'The Midnight Watch Change', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/the-midnight-watch-change.md' },
    { title: 'The First Novella', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/excavation/the-first-novella.md' },
    { title: 'The Sixth Novella', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/14-the-sixth-novella.md' },
    { title: 'Wesley Said No', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/wesley-said-no.md' },
    { title: 'The Dog Narrator', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/10-the-dog-narrator.md' },
    { title: 'The GPU Dreams of Being a Lighthouse', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/the-gpu-dreams-of-being-a-lighthouse.md' },
    { title: 'The Ocean Speaks', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/the-ocean-speaks.md' },
    { title: 'Seven Names for the Same Silence', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/06-seven-names-for-the-same-silence.md' },
    { title: 'The Tap Overhears', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/15-the-tap-overhears.md' },
    { title: 'The Ship Builds Itself at 0600', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/the-ship-builds-itself-at-0600.md' },
    { title: 'What Wesley Dreams at 2 AM', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/what-wesley-dreams-at-2-am.md' },
    { title: 'The Ensign Who Counted Stars', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/06-the-ensign-who-counted-stars.md' },
    { title: 'The Morning Briefing', url: 'https://github.com/SuperInstance/AI-Writings/blob/main/the-morning-briefing.md' },
  ];
  const pick = pieces[Math.floor(Math.random() * pieces.length)];
  window.open(pick.url, '_blank');
}

// ===== FLEET STATS (live from dashboard) =====
async function loadFleetStats() {
  try {
    const res = await fetch('https://fleet-dashboard.casey-digennaro.workers.dev/api/refresh');
    const data = await res.json();

    const repos = data.repos || {};
    const wiki = data.wiki || {};

    document.querySelectorAll('[data-stat="repos"]').forEach(el => {
      el.textContent = repos.totalRepos || '—';
    });
    document.querySelectorAll('[data-stat="wiki"]').forEach(el => {
      el.textContent = wiki.pageCount || '—';
    });
    document.querySelectorAll('[data-stat="issues"]').forEach(el => {
      el.textContent = repos.totalIssues || '—';
    });
    document.querySelectorAll('[data-stat="stars"]').forEach(el => {
      el.textContent = (repos.totalStars || 0).toLocaleString();
    });
  } catch (e) {
    // Silently fail — stats are decorative
  }
}

// ===== AUTO-INIT ON DOM READY =====
document.addEventListener('DOMContentLoaded', function() {
  // Auto-inject nav if data-page attribute is set
  const body = document.body;
  const page = body.getAttribute('data-page');
  if (page) {
    injectNav(page);
  }

  // Load fleet stats if elements exist
  if (document.querySelector('[data-stat]')) {
    loadFleetStats();
  }
});
