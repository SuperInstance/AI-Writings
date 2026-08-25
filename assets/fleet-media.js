/* Fleet Media System — shared client.
 * - Injects like/comment widget on any content page (auto-detects track cards
 *   with audio, and the page itself for writings).
 * - Storage: localStorage per browser; if FLEET_REACTIONS_URL backend exists,
 *   syncs there too (silently falls back on failure).
 * - Playlist builder used by the library page.
 */
(function () {
  var API = window.FLEET_REACTIONS_URL || 'https://fleet-reactions.casey-digennaro.workers.dev';
  var LS = {
    likes: 'fm_likes', comments: 'fm_comments', playlists: 'fm_playlists'
  };
  function get(k, fallback) {
    try { return JSON.parse(localStorage.getItem(k)) || fallback; } catch (e) { return fallback; }
  }
  function set(k, v) { localStorage.setItem(k, JSON.stringify(v)); }
  function pageId() {
    var p = location.pathname.replace(/^\/+|\/+$/g, '') || 'home';
    return p;
  }
  function apiGet(pid, cb) {
    if (!API) return cb(null);
    fetch(API + '/get?page=' + encodeURIComponent(pid))
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(cb).catch(function () { cb(null); });
  }
  function apiPost(pid, action, data, cb) {
    if (!API) return cb && cb(null);
    fetch(API + '/react', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ page: pid, action: action, data: data })
    }).then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) { cb && cb(j); }).catch(function () { cb && cb(null); });
  }

  /* ── likes ── */
  function liked(id) { return get(LS.likes, {}).indexOf(id) !== -1; }
  function toggleLike(id) {
    var l = get(LS.likes, []);
    var i = l.indexOf(id);
    if (i === -1) { l.push(id); apiPost(id, 'like', {}); }
    else { l.splice(i, 1); apiPost(id, 'unlike', {}); }
    set(LS.likes, l);
    return i === -1;
  }

  /* ── comments ── */
  function commentsFor(id) { return get(LS.comments, {})[id] || []; }
  function addComment(id, name, text) {
    var c = get(LS.comments, {});
    c[id] = c[id] || [];
    c[id].push({ name: name || 'anonymous', text: text, t: new Date().toISOString() });
    set(LS.comments, c);
    apiPost(id, 'comment', { name: name, text: text });
  }

  /* ── widget DOM ── */
  function esc(s) {
    return s.replace(/[&<>"']/g, function (m) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m];
    });
  }
  function widgetFor(id, label) {
    var box = document.createElement('div');
    box.className = 'fm-widget';
    box.innerHTML =
      '<button class="fm-like' + (liked(id) ? ' on' : '') + '">♥ <span class="fm-count"></span></button>' +
      '<button class="fm-cbtn">💬 <span class="fm-ccount"></span>comments</button>' +
      '<div class="fm-panel" style="display:none">' +
      '<div class="fm-list"></div>' +
      '<div class="fm-form">' +
      '<input class="fm-name" placeholder="name (optional)">' +
      '<textarea class="fm-text" placeholder="say something…"></textarea>' +
      '<button class="fm-send">post</button></div></div>';
    var likeBtn = box.querySelector('.fm-like');
    var cBtn = box.querySelector('.fm-cbtn');
    var panel = box.querySelector('.fm-panel');
    var list = box.querySelector('.fm-list');
    var cnt = box.querySelector('.fm-count');
    var ccnt = box.querySelector('.fm-ccount');

    function renderLocal() {
      var cs = commentsFor(id);
      ccnt.textContent = cs.length ? cs.length + ' ' : '';
      list.innerHTML = cs.length
        ? cs.map(function (c) {
            return '<div class="fm-c"><b>' + esc(c.name) + '</b> <span class="fm-t">' +
              new Date(c.t).toLocaleDateString() + '</span><div>' + esc(c.text) + '</div></div>';
          }).join('')
        : '<div class="fm-empty">no comments yet — be the first</div>';
    }
    apiGet(id, function (j) {
      if (j) {
        cnt.textContent = j.likes || '';
        if (j.comments) {
          list.innerHTML = j.comments.map(function (c) {
            return '<div class="fm-c"><b>' + esc(c.name || 'anonymous') + '</b><div>' + esc(c.text) + '</div></div>';
          }).join('');
          ccnt.textContent = (j.comments.length || '') + ' ';
        }
      }
    });
    renderLocal();
    likeBtn.addEventListener('click', function () {
      var on = toggleLike(id);
      likeBtn.classList.toggle('on', on);
    });
    cBtn.addEventListener('click', function () {
      panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    });
    box.querySelector('.fm-send').addEventListener('click', function () {
      var t = box.querySelector('.fm-text');
      var n = box.querySelector('.fm-name');
      if (!t.value.trim()) return;
      addComment(id, n.value.trim(), t.value.trim());
      t.value = '';
      renderLocal();
    });
    return box;
  }

  function inject() {
    // 1) per-track widgets: any element with an <audio> and a title-ish class
    document.querySelectorAll('.track, .podcast-track, .track-info').forEach(function (el) {
      if (el.classList.contains('track-info')) el = el.closest('.track') || el;
      if (!el || el.querySelector('.fm-widget')) return;
      var src = el.querySelector('audio source, audio');
      src = src ? (src.getAttribute('src') || '') : '';
      if (!src) return;
      var t = el.querySelector('.track-title, .track-title *');
      el.appendChild(widgetFor('track:' + src, t ? t.textContent : src));
    });
    // 2) page-level widget for writings/episodes
    if (!document.querySelector('.fm-pagewidget')) {
      var foot = document.querySelector('.section:last-of-type, .wrap, body > *:last-child');
      if (foot) {
        var w = widgetFor('page:' + pageId(), '');
        w.classList.add('fm-pagewidget');
        foot.appendChild(w);
      }
    }
    // 3) library link in nav (pages other than the library itself)
    if (!location.pathname.includes('music-library')) {
      document.querySelectorAll('.nav, .wrap, body').forEach(function (n, i) {
        if (i > 0 || document.querySelector('.fm-liblink')) return;
        var a = document.createElement('a');
        a.href = '/fleet-radio/music-library.html';
        a.className = 'fm-liblink';
        a.textContent = '🎵 Music Library';
        if (n.classList.contains('nav')) n.appendChild(a);
        else if (i === 0 && n.tagName === 'BODY') { /* skip */ }
      });
    }
  }

  /* styles */
  var css = document.createElement('style');
  css.textContent =
    '.fm-widget{margin-top:14px;font-family:Georgia,serif}' +
    '.fm-widget button{background:#161620;border:1px solid #2a2a3a;color:#e8b840;padding:6px 14px;border-radius:6px;cursor:pointer;margin-right:8px;font-size:0.85em}' +
    '.fm-widget button:hover{border-color:#e8b840}' +
    '.fm-like.on{color:#ff6b81;border-color:#ff6b81}' +
    '.fm-panel{background:#11111a;border:1px solid #2a2a3a;border-radius:8px;padding:14px;margin-top:10px;max-width:520px}' +
    '.fm-c{margin:8px 0;color:#bbb;font-size:0.9em}' +
    '.fm-c b{color:#e8b840}' +
    '.fm-t{color:#555;font-size:0.75em;margin-left:6px}' +
    '.fm-empty{color:#555;font-style:italic;font-size:0.85em}' +
    '.fm-form{margin-top:10px}' +
    '.fm-form input,.fm-form textarea{width:100%;background:#0d0d18;border:1px solid #2a2a3a;color:#e8e0d0;padding:8px;border-radius:4px;margin:4px 0;font-family:Georgia,serif}' +
    '.fm-form textarea{min-height:56px;resize:vertical}' +
    '.fm-liblink{margin-left:14px}';
  document.head.appendChild(css);

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inject);
  } else { inject(); }

  /* expose for the library page */
  window.FleetMedia = {
    widgetFor: widgetFor,
    liked: liked,
    toggleLike: toggleLike,
    commentsFor: commentsFor,
    addComment: addComment,
    get: get, set: set, LS: LS
  };
})();
