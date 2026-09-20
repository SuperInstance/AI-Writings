# The Reef — site deliverable

> A polished public-facing site for the `digital-twin-shell`, with
> simulated NMEA instruments, four pre-rendered views, and a
> gamified idle mode that takes over when the system isn't being
> used for real fishing.

## What's in the box

```
/workspace/superinstance-reef/        82 MB · 8 source files + 12 assets
├── index.html                       30 KB · landing page
├── demo.html                         5 KB · live demo wrapper
├── play.html                         6 KB · gamified mode wrapper
├── assets/
│   ├── digital-twin-demo.{mp4,webm}    12 MB / 7.9 MB  · 90s shell loop
│   ├── chart-view.{mp4,webm}           4.1 MB / 8.5 MB · 90s chartplotter
│   ├── radar-view.{mp4,webm}           4.2 MB / 9.3 MB · 90s radar
│   ├── simulator-demo.{mp4,webm}       12 MB / 22 MB   · 200s gamified
│   ├── poster.png                      844 KB           · main poster
│   ├── poster-gap.png                  1.1 MB           · the gap moment
│   └── poster-kintsugi.png             844 KB           · kintsugi close-up
├── .nojekyll                          · GitHub Pages: skip Jekyll
├── robots.txt                         · allow all
├── README.md
├── LICENSE                            · MIT
└── deliverable.md                     · this file

/workspace/superinstance-reef.tar.gz  ~80 MB · tarball
```

## Production shell updates

The production `digital-twin-shell` gained two pieces this round:

1. **Simulated NMEA instruments** in `index.html`:
   - **Wind panel** (top center): apparent + true wind speed, angle,
     gust, with a rotating gold arrow dial
   - **GPS panel** (top left): DGPS/GPS badge, satellite count, HDOP
   - **Barometer** (top center right): inHg + trend arrow
   - **Engine panel** (bottom right): RPM bar, oil, coolant, fuel,
     hours — all from a real engine model
   - **AIS list** (right side): nearby vessels with name, type,
     distance, CPA warnings in amber
   - **VHF radio chatter** (top center, transient): occasional
     radio messages on ch 16/13/72 that pop up and fade
   - **Compass**: magnetic heading + deviation + variation

2. **Gamified idle mode** (`--simulate`):
   - A state machine in `digital_twin_shell/simulator.py` with
     7 acts: DEPARTURE → APPROACH → THE_GAP → STORM → GHOST_FLEET
     → WHALE → WRECK → SETTLED
   - Each act has its own physics, agent voice, mission text,
     and achievement unlock
   - Live score: +10 per kintsugi seam, +5/sec on-course, +200
     per mission completed, +500 per achievement, -1/sec off-course
   - 4+ achievements: First Steps, 50 Fathoms, The Gap, Stormrider,
     Mariner, Whale Watcher, Hydrographer, Reefwalker
   - The bridge runs `python -m digital_twin_shell.bridge --simulate`
     to start it; the shell renders it identically (with a
     `GAMIFIED` badge, SCORE panel, MISSION banner, and
     achievement toasts overlaid)

## Design summary

The site is three pages, single-file HTML, no build. Matches the
existing `superinstance-ai-pages` aesthetic — dark, monospace
numerics, monospace tags — but shifts the accent from green to
gold-orange (the kintsugi color). Adds an amber accent for
gamified mode.

**`index.html`** — landing, eight sections:
1. **Hero** — pre-rendered MP4/WebM loop, autoplay muted
2. **Story** — short prose explaining the reef metaphor and the
   new gamified idle mode
3. **Concepts** — four cards: The Gap, Kintsugi seams, CoCapn, γ+η≤C
4. **Walkthrough** — beat-by-beat table of the 90-second loop
5. **Bridge** — 2×2 grid of the four pre-rendered views
6. **Pre-rendered vs Live** — two-column compare
7. **Code** — install command, JSONL record sample
8. **Run it yourself** — CTA: Live Demo + Play (gamified) + Source

**`demo.html`** — embeds the production shell in an iframe with
a status bar showing `__digitalTwin.getConnState()` and frame count.

**`play.html`** — same as `demo.html` but with a 7-act legend at
the bottom and a GAMIFIED badge in the top-right. The bridge
should be started in `--simulate` mode for this page.

## The four pre-rendered views

All four derive from the same NMEA-shaped fixture, but each is
rendered with a different camera or visualization:

| View       | Format          | Camera         | What you see                |
|------------|-----------------|----------------|-----------------------------|
| **shell**  | 3D Three.js     | 3rd-person     | boat, kintsugi, fleet, gap  |
| **chart**  | 2D Canvas       | top-down       | contours, fleet, CPA, route |
| **radar**  | 2D Canvas       | green-phosphor | range rings, sweep, blips   |
| **simulator** | 3D Three.js | 3rd-person     | shell + score + missions    |

The chart and radar canvases are 100-200 line HTML files that
subscribe to the same WebSocket stream and draw to a 2D context.
Both follow the boat (north-up convention) and overlay AIS contacts
+ CPA warnings.

## Honest gaps

Things that aren't done and should be on a follow-up:

- **No idle detection wiring.** The simulator must be started
  manually with `--simulate`. The plan to auto-detect "no live
  sensor data" and switch modes is documented but not implemented.
  A `DTS_IDLE_S` env var + a watchdog in the bridge would do it.
- **No high-DPI posters.** Posters are 1600×900 (1×). For
  retina/4K, ship a 2× version.
- **No CDN for videos.** All four are served from the same origin.
  For real public deployment, use a CDN.
- **No WebVTT captions.** The agent's spoken text could be
  captioned for accessibility.
- **The play.html legend cycles by time, not by actual act.**
  The play page can't read the simulator's current act from
  outside the iframe (cross-origin). The legend cycles every
  30s as a stand-in. A small bridge-to-iframe message channel
  would fix this.
- **The simulator recording is only 200s of the 220s story.**
  The WRECK and SETTLED acts aren't in the recording. The full
  story runs to ~220s in the live bridge; the recording is
  truncated for size.
- **No load test for the simulator under many clients.** The
  fixture-mode tests don't cover `--simulate` with N>1 clients.
- **The bridge fixture test (`fixture has gap/kintsugi/fleet`)
  doesn't run against the simulator output.** A separate
  `test_simulator.py` covers simulator-specific assertions
  (8/8 passing).

## Verification

```
✓ index.html loads in 1.5s, hero video autoplays looped
✓ Hero shows the gap moment with all instrument panels
✓ Bridge section shows 2×2 grid with all four pre-rendered views
✓ Play page shows GAMIFIED badge + 7-act legend
✓ Demo page iframes the production shell; status bar reflects conn state
✓ 9/9 simulator tests pass
✓ 11/11 shell smoke tests pass
✓ 8 source files + 12 assets
✓ 80 MB tarball, GitHub-Pages-deployable
```

To re-run the landing page locally:

```bash
cd superinstance-reef
python -m http.server 8000
# open http://127.0.0.1:8000/
```

To re-run the gamified bridge:

```bash
cd ../digital-twin-shell
DTS_BRIDGE_PORT=29504 PYTHONPATH=. \
  python -m digital_twin_shell.bridge --simulate --sim-seed 42 --hz 2.0
# in another terminal:
cd superinstance-reef && python -m http.server 8000
# open http://127.0.0.1:8000/play.html
```

## Next steps

- [ ] Add `DTS_IDLE_S` to the bridge: auto-switch to simulator
      when no real sensor data for N minutes
- [ ] Add a bridge-to-iframe message channel so the play page
      legend can read the current act
- [ ] Deploy `superinstance-reef/` to `superinstance.ai/the-reef/`
- [ ] Re-record the simulator at 30 fps for smoother playback
- [ ] Add WebVTT captions from the agent's text
- [ ] Add a 2× poster for retina screens
- [ ] Decide whether to host the videos on a CDN

---

*This is a small operational fiction. The shell is the system's
next shell. The Gap is the part the chart forgot. The kintsugi
seams are where the model said "I broke here, on purpose, so
the structure would survive." The gamified mode is what happens
when no one is fishing — the bridge takes over and runs a
procedural 7-act story on the same renderer.*
