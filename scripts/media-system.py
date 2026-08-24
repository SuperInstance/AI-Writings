#!/usr/bin/env python3
"""Fleet Media System — master library page generator + widget injector.

Usage:
  python3 media-system.py            # sync catalog, build library page, inject widget
  python3 media-system.py --sync-only

Lives in ai-writings/scripts/. Run by hand or by the Fleet Radio pipeline
after each daily episode. Idempotent: pages already carrying the widget are
skipped, catalog metadata is preserved across syncs.

Storage layer: likes/comments/playlists persist to localStorage per browser,
AND sync to a shared backend when FLEET_REACTIONS_URL is set (worker deployed
separately once a CF API token with KV scope is available — the widget probes
it on load and silently falls back to local-only).
"""
import json
import os
import re
import sys
import html
import datetime
from pathlib import Path

ROOT = Path('/home/eileen/projects/ai-writings')
MUSIC = ROOT / 'music'
CATALOG_PATH = ROOT / 'music-catalog.json'
LIBRARY_PAGE = ROOT / 'fleet-radio' / 'music-library.html'
WIDGET_SRC = '/assets/fleet-media.js'

# The curated 14 — hand-annotated in generate-episode.ts historically.
CURATED = {
    '01-unplayed-indie-folk.mp3': ('Unplayed', 'Weathered baritone, acoustic guitar. The song you haven\'t played yet.', 68, ['contemplative', 'melancholic'], 'unplayed'),
    '02-see-you-at-the-table.mp3': ('See You At The Table', 'Warm duet, acoustic guitar. The only promise that tomorrow will be different.', 82, ['warm', 'contemplative'], 'unplayed'),
    '03-five-holes-in-a-bone.mp3': ('Five Holes in a Bone', 'The oldest known flute. 40,000 years old.', 70, ['contemplative', 'mysterious'], 'five-holes'),
    '07-the-session-composed-itself.mp3': ('The Session Composed Itself', 'The night the jazz combo didn\'t need to decide anything.', 90, ['playful', 'energetic'], 'session'),
    '14-bpm-40.mp3': ('Afterhours', 'The bar closing. The lights dimming. The sound of after.', 40, ['melancholic', 'contemplative'], 'afterhours'),
    '21-bpm-60.mp3': ('Slow Tide', 'Sixty beats per minute. Resting heart rate. The ocean\'s pulse.', 60, ['contemplative', 'warm'], 'slow-tide'),
    '28-rest-085.mp3': ('Rest', 'The silence between notes is not empty.', 85, ['contemplative', 'melancholic'], 'rest'),
    '30-the-berry-phase.mp3': ('The Berry Phase', 'The phase a quantum system accumulates even when it returns to its start.', 75, ['mysterious', 'contemplative'], 'berry'),
    '31-the-overtones-dream.mp3': ('The Overtones Dream', 'What the harmonics dream about when the fundamental stops playing.', 80, ['mysterious', 'warm'], 'overtones'),
    '32-ambient-marching-band.mp3': ('Ambient Marching Band', 'What if the parade already passed and all that\'s left is the echo?', 65, ['playful', 'melancholic'], 'marching-band'),
    '35-the-interval.mp3': ('The Interval', 'The space between two notes. The space between two days.', 70, ['contemplative', 'warm'], 'interval'),
    '18-the-tap-sings.mp3': ('The Tap Sings', 'The bar itself has a voice.', 72, ['warm', 'mysterious'], 'tap-sings'),
    '01-unplayed-ambient.mp3': ('Ambient Drift', 'The sound of the ocean from inside a hull. Continuous. Unresolved.', 50, ['contemplative', 'melancholic'], 'unplayed'),
    '27-the-tap-sings-piano-cover-of-cover.mp3': ('The Tap Sings (Piano)', 'A cover of a cover. The song wearing different clothes.', 68, ['melancholic', 'warm'], 'tap-sings'),
}

def title_from_filename(stem: str) -> str:
    s = re.sub(r'^\d+[-_]', '', stem)
    s = s.replace('-', ' ').replace('_', ' ').strip()
    return s.title() if s.islower() else s

def load_catalog() -> dict:
    if CATALOG_PATH.exists():
        return json.loads(CATALOG_PATH.read_text())
    return {'tracks': {}}

def sync_catalog(cat: dict) -> int:
    added = 0
    for f in sorted(MUSIC.iterdir()):
        if f.suffix.lower() not in ('.mp3', '.wav', '.ogg', '.flac'):
            continue
        name = f.name
        if name not in cat['tracks']:
            if name in CURATED:
                title, desc, bpm, moods, family = CURATED[name]
            else:
                title = title_from_filename(f.stem)
                desc = ''
                bpm = None
                moods = ['contemplative']
                family = f.stem
            cat['tracks'][name] = {
                'filename': name, 'title': title, 'description': desc,
                'bpm': bpm, 'mood': moods, 'family': family,
                'path': f'/music/{name}', 'added': datetime.date.today().isoformat(),
                'curated': name in CURATED,
            }
            added += 1
    # also include the jam/song wavs living in fleet-radio/songs
    songs = ROOT / 'fleet-radio' / 'songs'
    if songs.exists():
        for f in sorted(songs.iterdir()):
            if f.suffix.lower() in ('.wav', '.mp3', '.ogg'):
                name = f.name
                key = f'songs/{name}'
                if key not in cat['tracks']:
                    cat['tracks'][key] = {
                        'filename': name, 'title': title_from_filename(f.stem), 'description': '',
                        'bpm': None, 'mood': ['contemplative'], 'family': f.stem,
                        'path': f'/fleet-radio/songs/{name}',
                        'added': datetime.date.today().isoformat(), 'curated': False,
                    }
                    added += 1
    return added

LIBRARY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>⚓ Fleet Radio — The Music Library (everything, ever)</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0a0a14;color:#e8e0d0;font-family:Georgia,serif}}
.wrap{{max-width:960px;margin:0 auto;padding:40px 20px 100px}}
h1{{color:#e8b840;letter-spacing:3px;font-size:2em;margin-bottom:4px}}
.sub{{color:#888;font-style:italic;margin-bottom:24px}}
.controls{{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}}
.controls input{{background:#11111a;border:1px solid #2a2a3a;color:#e8e0d0;padding:10px 14px;border-radius:6px;flex:1;min-width:200px;font-family:Georgia,serif}}
.controls button{{background:#161620;border:1px solid #2a2a3a;color:#e8b840;padding:10px 16px;border-radius:6px;cursor:pointer;font-family:Georgia,serif}}
.controls button:hover{{border-color:#e8b840}}
.track{{background:#11111a;border-radius:8px;margin:10px 0;padding:16px 18px;display:flex;gap:16px;align-items:center;border-left:3px solid #2a2a3a}}
.track.new{{border-left-color:#44cc88}}
.track .num{{color:#2a2a3a;font-family:'Courier New',monospace;min-width:36px}}
.track .info{{flex:1}}
.track .t{{color:#e8b840;margin-bottom:2px}}
.track .d{{color:#666;font-size:0.85em;font-style:italic}}
.track .meta{{color:#44cc88;font-family:'Courier New',monospace;font-size:0.72em;margin-top:3px}}
.track audio{{width:260px;max-width:45%;height:32px}}
.playlist-bar{{position:fixed;bottom:0;left:0;right:0;background:#0d0d18;border-top:1px solid #2a2a3a;padding:10px 20px;display:none;z-index:50}}
.playlist-bar .inner{{max-width:960px;margin:0 auto;display:flex;gap:10px;align-items:center}}
.playlist-bar .now{{color:#e8b840;font-size:0.9em;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
#count{{color:#888;font-size:0.9em;margin:6px 0 0}}
a{{color:#44cc88}}
@media(max-width:640px){{.track{{flex-wrap:wrap}}.track audio{{width:100%;max-width:100%}}}}
</style>
</head>
<body>
<div class="wrap">
<h1>THE MUSIC LIBRARY</h1>
<div class="sub">Every song the fleet ever made. {count} tracks and growing — new songs are composed nightly and land here.</div>
<div class="controls">
<input id="q" type="text" placeholder="Search titles…">
<button onclick="playAll()">▶ Play everything</button>
<button onclick="shuffleAll()">🔀 Shuffle all</button>
<button onclick="openPlaylist()">🎵 My playlist (<span id="plcount">0</span>)</button>
</div>
<div id="count"></div>
<div id="list"></div>
<p style="margin-top:40px;color:#555;font-size:0.85em">Playlists, likes, and comments are saved in your browser for now.
<a href="/fleet-radio/">← back to Fleet Radio</a></p>
</div>
<div class="playlist-bar" id="plbar"><div class="inner">
<span class="now" id="nowplaying">—</span>
<button onclick="plPrev()">⏮</button>
<button onclick="plToggle()" id="plplay">⏸</button>
<button onclick="plNext()">⏭</button>
<button onclick="plClear()">✕ clear</button>
</div></div>
<script>window.FLEET_CATALOG = {catalog_json};</script>
<script src="/assets/fleet-media.js"></script>
<script src="/assets/library-app.js"></script>
</body>
</html>
"""

def build_library(cat: dict):
    tracks = sorted(cat['tracks'].values(), key=lambda t: (t.get('added') or '2026-01-01'), reverse=True)
    LIBRARY_PAGE.parent.mkdir(parents=True, exist_ok=True)
    LIBRARY_PAGE.write_text(LIBRARY_TEMPLATE.format(
        count=len(tracks),
        catalog_json=json.dumps({'tracks': tracks}),
    ))

WIDGET_SNIPPET = '<script src="' + WIDGET_SRC + '" defer></script>'

def inject_widget():
    """Add the widget <script> + library link to every content HTML page missing it."""
    patched = 0
    html_files = list(ROOT.glob('*.html')) + list((ROOT / 'fleet-radio').glob('*.html')) \
        + list((ROOT / 'site').glob('*.html')) if (ROOT / 'site').exists() else list(ROOT.glob('*.html')) + list((ROOT / 'fleet-radio').glob('*.html'))
    for page in html_files:
        try:
            text = page.read_text()
        except Exception:
            continue
        if WIDGET_SRC in text:
            continue
        if '</body>' not in text:
            continue
        text = text.replace('</body>', WIDGET_SNIPPET + '\n</body>', 1)
        page.write_text(text)
        patched += 1
    return patched

def main():
    sync_only = '--sync-only' in sys.argv
    cat = load_catalog()
    added = sync_catalog(cat)
    CATALOG_PATH.write_text(json.dumps(cat, indent=1))
    print(f'  🎵 catalog: {len(cat["tracks"])} tracks (+{added} new)')
    if sync_only:
        return
    build_library(cat)
    print(f'  📚 library page: {LIBRARY_PAGE.name} rebuilt')
    n = inject_widget()
    print(f'  🔗 widget injected into {n} pages')

if __name__ == '__main__':
    main()
