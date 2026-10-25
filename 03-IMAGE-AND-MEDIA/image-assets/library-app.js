/* Library page app — renders catalog, search, play-all/shuffle, playlist builder.
 * Uses FleetMedia (fleet-media.js) for likes/comments storage.
 */
(function () {
  var tracks = (window.FLEET_CATALOG && window.FLEET_CATALOG.tracks) || [];
  var playlist = FleetMedia.get('fm_playlist', []);
  var order = [];          // currently displayed track order (indices)
  var queue = [];          // play queue of paths
  var current = -1;
  var audio = new Audio();
  var plbar = document.getElementById('plbar');
  var nowEl = document.getElementById('nowplaying');

  function fmtMeta(t) {
    var bits = [];
    if (t.bpm) bits.push(t.bpm + ' BPM');
    if (t.mood) bits.push(t.mood.join(' · '));
    if (t.added) bits.push('added ' + t.added);
    return bits.join(' · ');
  }

  function render() {
    var q = (document.getElementById('q').value || '').toLowerCase();
    var list = document.getElementById('list');
    var html = '';
    order = [];
    tracks.forEach(function (t, i) {
      if (q && (t.title + ' ' + t.description + ' ' + t.filename).toLowerCase().indexOf(q) === -1) return;
      order.push(i);
      var isNew = t.added && t.added >= new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 10);
      var inPl = playlist.indexOf(t.path) !== -1;
      html += '<div class="track' + (isNew ? ' new' : '') + '" data-i="' + i + '">' +
        '<div class="num">' + (order.length) + '</div>' +
        '<div class="info"><div class="t">' + t.title + (isNew ? ' <span style="color:#44cc88;font-size:0.7em">NEW</span>' : '') + '</div>' +
        (t.description ? '<div class="d">' + t.description + '</div>' : '') +
        '<div class="meta">' + fmtMeta(t) + '</div></div>' +
        '<audio controls preload="none"><source src="' + t.path + '"></audio>' +
        '</div>';
    });
    list.innerHTML = html;
    document.getElementById('count').textContent = order.length + ' of ' + tracks.length + ' tracks shown';
    // attach per-track widgets
    list.querySelectorAll('.track').forEach(function (el) {
      var t = tracks[+el.dataset.i];
      var w = FleetMedia.widgetFor('track:' + t.path, t.title);
      el.querySelector('.info').appendChild(w);
      var add = document.createElement('button');
      add.className = 'fm-pladd';
      add.style.cssText = 'margin:8px 0 0;background:#161620;border:1px solid #2a2a3a;color:#44cc88;padding:6px 12px;border-radius:6px;cursor:pointer;font-size:0.8em';
      function refresh() { add.textContent = playlist.indexOf(t.path) !== -1 ? '✓ in my playlist' : '+ add to my playlist'; }
      add.onclick = function () {
        var ix = playlist.indexOf(t.path);
        if (ix === -1) playlist.push(t.path); else playlist.splice(ix, 1);
        FleetMedia.set('fm_playlist', playlist);
        refresh(); updatePlCount();
      };
      refresh();
      el.appendChild(add);
    });
  }

  function updatePlCount() { document.getElementById('plcount').textContent = playlist.length; }

  function buildQueue(paths, shuffleQ) {
    queue = paths.slice();
    if (shuffleQ) { for (var i = queue.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var a = queue[i]; queue[i] = queue[j]; queue[j] = a; } }
    current = -1;
    plbar.style.display = 'block';
    next();
  }
  function next() { if (current < queue.length - 1) play(current + 1); else plbar.style.display = 'none'; }
  function prev() { if (current > 0) play(current - 1); }
  function play(i) {
    current = i;
    audio.src = queue[i];
    audio.play();
    var t = tracks.filter(function (x) { return x.path === queue[i]; })[0];
    nowEl.textContent = '▶ ' + (t ? t.title : queue[i]) + '  (' + (i + 1) + '/' + queue.length + ')';
  }
  audio.addEventListener('ended', next);

  window.playAll = function () { buildQueue(order.map(function (i) { return tracks[i].path; }), false); };
  window.shuffleAll = function () { buildQueue(order.map(function (i) { return tracks[i].path; }), true); };
  window.openPlaylist = function () {
    if (!playlist.length) { alert('Your playlist is empty — add tracks with "+ add to my playlist".'); return; }
    buildQueue(playlist, false);
  };
  window.plNext = next; window.plPrev = prev;
  window.plToggle = function () { if (audio.paused) audio.play(); else audio.pause(); };
  window.plClear = function () { playlist = []; FleetMedia.set('fm_playlist', []); updatePlCount(); plbar.style.display = 'none'; audio.pause(); };

  document.getElementById('q').addEventListener('input', render);
  updatePlCount();
  render();
})();
