# PRODUCTION-READINESS — SuperInstance flagship artifacts

*Dispatch: Opus 5.5 planning tier, 2026-09-27. This is a **plan**, not the work.
Every gap is cited to a real file surveyed read-only from the live repos this
cycle (clones: `/tmp/pg-clt` cargo-line-tycoon @ `claude/the-chart` 90cb222,
`/tmp/pg-sub` substrate-ts @ `claude/phase0-worldmodel`, `/tmp/pg-jev` jev-quilt
@ main + `g20b`/`g20c`). Aspirational or unverifiable items are marked
**STRETCH**. No real-world licensed data is proposed for shipping. This file is
uncommitted by design — the dispatcher books it.*

🚢 → ✅ → 🌊

---

## 0. Survey result (what is actually true on disk, 2026-09-27)

| Artifact | State verified this cycle | Evidence |
|---|---|---|
| **cargo-line-tycoon** (the Chart game) | Game logic clean + fully green. **5** test files, all pass under `node --test` (18 provenance checks, replay determinism, economy, loop, `fact_landed` offline predicate). | `game/test/*.js` ran green; `game/src/{engine,economy,pencil,provenance}.js` (1522 LoC) |
| — refusal law | Present and enforced in **two** layers: game `attest()` refuses source/trust/url-less cells; kernel `cellFor()`/`book()` refuse provenance-less world cells. | `game/src/provenance.js:63–72`, `substrate/ts/src/world.js:120,226` |
| — deployable bundle | **NOT self-contained.** `browser-deploy/tycoon-live.html` loads the engine via relative `../game/src/*.js` and `../substrate/ts/src/{index,world}.js` — paths that live *outside* `browser-deploy/`. | `tycoon-live.html:249,257,268–276` |
| — CI | **No test/lint/build gate exists.** `pages.yml` deploys `./substrate-bundle` (the legacy substrate demos, *not the game*) to GitHub Pages on push to main; `publish-pypi.yml` is Python. Neither runs `node --test`. | `.github/workflows/{pages,publish-pypi}.yml` |
| — packaging | No root `package.json`, no `game/package.json`. Tests run only via raw `node --test` in `game/`. | `ls package.json` → absent |
| — README accuracy | README is a **substrate** README (polyformalism, 11 opcodes, stress tests). It tells you to `npm install && npm test` at root — which **cannot work** (no root package.json). Barely mentions the game. | `README.md:137–138` |
| — LICENSE | **Absent.** | `ls LICENSE*` → NO LICENSE |
| — secrets in bundle | **Clean.** No API keys/tokens in `game/`, `browser-deploy/`, `substrate/` (only prose mentions of model names). | grep scan |
| — offline-first caveat | Game makes **zero network calls** for gameplay, but loads Google Fonts from `fonts.googleapis.com`. | `tycoon-live.html:8–10`; ui.js has no `fetch`/`WebSocket`/beacon |
| — legacy exposed API | `canon-api-worker/` is a Worker with `CORS: *`, **no auth**, POST endpoints writing arbitrary JSON to KV. Legacy substrate infra — **not** used by the offline game. | `canon-api-worker/src/index.js:20–40` |
| **substrate-ts kernel** | `claude/phase0-worldmodel` (2 commits over main), v0.2.0, `npm test` green (8 checks). **No CI.** Source-of-truth that is *vendored by hand* into CLT's `substrate/ts/src/`. | `/tmp/pg-sub` |
| **jev-quilt** | main carries G20a. Python **244 tests green** (3 skipped, 2 expected-fail) on py3.11/3.12; **CI exists** (`test.yml`: unittest + canary + wheel build). Rust g20c **18 tests green**. | ran both suites |
| — G20b/G20c | `g20c` is a **superset of** `g20b`: both branch from G20a; g20c re-includes every g20b file (`g20b.rs`, its test, its vectors) **plus** g20c, and adds *both* Rust CI jobs. | `git diff --stat main..g20c`; merge-base = G20a |
| — Rust CI on main | **None yet.** Rust is only gated once g20b/g20c land (they add the `cargo test` jobs). | `test.yml` on main has no Rust job |

**Stacked cargo-line branches** (none merged to main): `phase0-1-playable` (1 commit) → `phase2-ground-truth` (1) → `the-chart` (2). Total 4 commits over main, cleanly linear.

---

## Artifact A — cargo-line-tycoon (the Chart)

### A.1 Definition of "production grade"
The flagship deliverable is a **single-player, offline-first, deterministic web game** a
stranger can open at a URL (or from a file) and play with no install, no account, no
network. "Done for real users" =

1. **It loads and plays** on a clean machine, from the public URL, first try — no console
   errors, no broken asset paths, works offline after first load.
2. **What ships is what's tested.** The rendered game (the `ui.js`/`tycoon-live.html`
   layer) has at least a smoke-level automated check, not only the headless engine.
3. **CI is a gate**, not decoration: every push runs `node --test` + the deploy build; a
   red suite blocks merge and blocks deploy.
4. **Deploy is reproducible and self-contained** — a versioned artifact, not "the whole
   repo tree happens to resolve relative paths."
5. **Honest docs**: a README that describes *the game*, tells a user how to play/deploy,
   and states the offline/data/rights posture truthfully.
6. **Determinism holds in the browser**, not just in Node (replay ≡ live is the product's
   spine per PLAYTEST.md).
7. **Licensed** for its intended distribution; real-world data rights intact.

### A.2 Gap list (current state → the bar)
- **[Deploy] The bundle is not self-contained.** `tycoon-live.html:249/257/268–276` reaches
  up into `../game` and `../substrate`. Opening from disk works only because the whole repo
  tree is present; deploying *only* `browser-deploy/` breaks the game. → needs a build step
  that assembles a self-contained dir (copy `game/`, `substrate/ts/src/` under the deploy
  root, or inline/bundle them).
- **[CI] No test gate at all.** `pages.yml` never runs the game tests and deploys the wrong
  directory (`substrate-bundle`, the legacy demos). A broken game can merge and "deploy"
  today. → add a Node test workflow; repoint/replace the Pages/Cloudflare deploy at the game
  bundle.
- **[Tests] The UI layer is untested.** `game/src/*` is well covered, but `browser-deploy/game/ui.js`
  (618 LoC — the actual thing users touch) has no automated test. ui.js even references a
  `?seed=` "Playwright" convenience (`ui.js:611`) but **no Playwright test is committed**. →
  add one headless smoke test (load page, start seeded run, assert a stake lands, assert
  `window.pencilStakesPlaced` moves, no console errors).
- **[Docs] README describes the substrate, not the game**, and its `npm install && npm test`
  (`README.md:137`) fails at root (no package.json). `deploy-templates/README.md` calls
  tycoon-live "Multiplayer tycoon" — stale; the-chart is offline single-player. → rewrite a
  game-first README + a truthful play/deploy section (PLAYTEST.md is the good source).
- **[Packaging] No `package.json`.** No pinned Node version, no `npm test` script, no lint. →
  add a minimal `game/package.json` (`"test": "node --test"`, engines pin).
- **[Legal] No LICENSE.** A public game repo with no license is "all rights reserved" by
  default — ambiguous for users/contributors. → add one (owner's choice; MIT/Apache-2.0
  typical for a playable OSS game).
- **[Data provenance] Hand-mirrored canon can drift.** `game/data/ports.js` is a *by-hand*
  JS mirror of `locales/en/canon/ports.json` with a comment saying "mirror the change here
  by hand." No test enforces parity. → add a parity test (ports.js ≡ the json for the 10
  US/CA ports).
- **[Data rights] Cited price data.** `game/data/fuel_freight_snapshot.js` cites
  `oilpriceapi.com` and `ufreight.com` as `source_url`s. These are a handful of snapshot
  numbers used as seed-labeled baselines (fair-use-shaped, clearly marked "flavor + light
  price-model input"), **not** a shipped dataset. → **STRETCH**: confirm neither source's ToS
  forbids reproducing the cited figures before public launch; if in doubt, replace with a
  self-attributed synthetic baseline (the provenance layer already supports `procgen`+`seed_label`).
- **[Offline-first] Google Fonts is an external dependency.** `tycoon-live.html:8–10` pulls
  fonts from Google's CDN — a privacy call-out and a (graceful) degradation when truly
  offline. → self-host the two fonts, or accept the system-font fallback and drop the claim
  of *pure* offline. P2.
- **[a11y] Unassessed.** The Chart is a bespoke canvas/DOM "one screen, one verb" UI; no
  evidence of keyboard-operability, focus order, ARIA, or reduced-motion handling. → a11y
  pass (keyboard path for stake/recall, `prefers-reduced-motion` for the sound/animation,
  contrast check on the Pencil Sea palette). **STRETCH** on scope until surveyed live.
- **[Browser-compat] Unverified.** No matrix beyond "opened it in a browser" (PLAYTEST.md).
  Uses WebAudio (inline WAV), `performance.now`, ES modules-as-scripts via a `require` shim
  (`tycoon-live.html:233–248`). → smoke on current Chrome/Firefox/Safari + mobile Safari.
- **[Versioning] None.** No game version surfaced to the user or tagged. → stamp a version in
  the UI margin + git tag on release.

### A.3 Merge & release path (the stacked branches)
The four commits are clean and linear (`phase0-1` → `phase2` → `the-chart`), so this is
low-risk. Recommended:

1. **Keep history, merge the stack tip once.** Because the branches are strictly stacked and
   each is a coherent phase, open **one PR: `claude/the-chart` → `main`** (it already
   contains phase0-1 + phase2 as ancestors). A no-op fast-forward-shaped merge lands all four
   commits with their phase story intact. *Do not* squash — the phase commits are meaningful
   and small (4 total), and the corpus favors "a scar booked beats a result covered."
2. **Gate it first (P0 below): add the Node test workflow in that same PR** so the merge is
   the first commit CI ever guards. Merge only on green.
3. Alternative if the owner wants review granularity: three sequential PRs (phase0-1 → main,
   then phase2 → main, then the-chart → main), rebasing each on the new main. More ceremony,
   same result; the single-PR path is cheaper and the diff is already reviewable.
4. **Tag** `v0.1.0-game` on the merge commit; that tag is what deploys.

### A.4 Deploy — Cloudflare Pages (⚠️ OWNER-GATED OUTWARD ACTION)
> **This publishes a public URL. It is an outward, owner-gated action and needs an explicit
> "go" from the owner before anyone runs it.** `CF_API_TOKEN` is present in the dispatcher
> env; treat it as write-capable and never print/commit it.

Smallest safe path once A.3 has landed and the P0 bundle gap is fixed:
1. **Build a self-contained deploy dir** (fixes A.2 gap #1): a script that copies
   `browser-deploy/tycoon-live.html` + `browser-deploy/game/ui.js` and the referenced
   `game/` and `substrate/ts/src/` files into one `dist/` with paths that resolve *inside*
   `dist/` (or inline them). Verify by serving `dist/` alone (`python3 -m http.server` from
   `dist`) and confirming the game loads with **no 404s**.
2. **Deploy with Wrangler**: `wrangler pages deploy dist --project-name cargo-line-tycoon`
   (token via env, never inline). Or the Cloudflare Pages MCP path. Start with a
   **preview/branch deploy**, not production, so the first URL is disposable.
3. **Verify before sharing the URL** (all must pass): loads first-try in a fresh incognito
   window; **no console errors**; **no network calls except fonts** (DevTools network tab);
   a seeded run is reproducible (`?seed=` gives the same run); works with network throttled
   to offline after first load; secrets scan of the deployed bundle is clean (no keys — see
   A.2, already clean at source). Only then promote to production and share.
4. **Do NOT** deploy the whole repo root to get the relative paths to resolve — that would
   publish every legacy dir (`research/`, `motifs/`, `jev_diffusion/`, internal docs) at the
   public URL. Ship `dist/` only.

### A.5 Security / hardening
- **Secrets**: already clean at source; the deploy-time check (A.4 step 3) is the guard that
  keeps it clean. The offline game has no secret to leak.
- **Input validation**: the only user input is a seed string; `ui.js:569` funnels it straight
  into `new GameEngine({seed})`. Confirm a hostile seed (huge/emoji/`__proto__`) can't break
  the RNG or the DOM — quick fuzz. Low risk, worth a test.
- **Refusal-law coverage**: strong. Two independent layers refuse provenance-less cells
  (`provenance.js:63–72`, `world.js:120/226`), and a test proves the law "does not cost
  replay." No gap here — keep it as a CI invariant.
- **Supply chain**: the game has **zero runtime npm deps** (hand-vendored kernel, no
  bundler) — excellent supply-chain posture. The only external runtime fetch is Google
  Fonts (A.2). Keep it dependency-free.
- **Exposed API**: the offline game exposes none. **`canon-api-worker/` is a separate,
  legacy, unauthenticated `CORS:*` write API** — it must **not** be deployed as part of the
  game launch. If it is ever deployed for its own reasons, it needs auth + rate limiting
  before it faces the internet (flagged under jev/infra, not the game). Keep it out of the
  game's `dist/`.

### A.6 CI (what to add — there is none for the game today)
- **`node --test` gate** on push + PR to main (Node 22, matches the dev env), running
  `game/test/*.js`. **P0.**
- **Deploy build check**: run the self-contained-bundle build and fail if any referenced
  file is missing (this is also the deploy artifact). **P0/P1.**
- **Headless UI smoke** (Playwright) once written. **P1.**
- **Lint/format** (eslint or `node --check` on each file) — cheap, catches syntax rot. **P2.**
- **Retire or fix `pages.yml`** so it can't "successfully deploy" the wrong directory.

---

## Artifact B — jev-quilt (the substrate)

### B.1 Definition of "production grade"
jev-quilt is a **library/substrate** (a Python package + a Rust port + cross-language
proof vectors), not an end-user app. "Done for real users" (users = other agents/devs
building on the substrate) =

1. **Green, gating CI** across every language it claims parity in (Python **and** Rust),
   including the cross-language vector freshness checks.
2. **A published, versioned, installable package** with a stable public API and a changelog.
3. **The parity claim is enforced**, not asserted: the second-reader vectors regenerate and
   match in CI (byte-exact cross-language reproduction is the whole product).
4. **Refusal/robustness invariants are tested** (fail-closed revocation, tamper detection).
5. **Docs a stranger can build against** — install, the opcode algebra, the receipt/second-
   reader contract.
6. **Clean test hygiene** (no resource leaks, no masked failures).

### B.2 Gap list (current state → the bar)
- **[Merge] G20b/G20c are unmerged**, and they are what turns on **Rust CI**. main today
  has **no Rust gate** — the Rust port ships unguarded. → land them (see B.3).
- **[CI] No Rust job on main** until g20b/g20c land; `test.yml` on main is Python-only. The
  branches add the `cargo test` + vector-freshness jobs. → merging closes this.
- **[Test hygiene] Resource leaks.** The Python suite emits `ResourceWarning: unclosed file`
  (`tests/test_receipts_v2.py:58,245` — `json.load(open(...))` without a context manager).
  244 tests pass but leak handles. → wrap in `with open(...)`. P2, cheap.
- **[Vectors] Freshness is only enforced once g20b/g20c CI lands.** The generators
  (`gen_g20*_vectors.py`) + `git diff --exit-code` gate are exactly right — but only run in
  the new jobs. → confirm they run on main after merge.
- **[Versioning/release] No published release path verified for real users.** CI builds a
  wheel (`test.yml` build job) but there's no evidence of a tagged release/PyPI publish of
  the substrate itself, nor a Rust crate publish. → decide the distribution surface (PyPI for
  the Python package; crates.io or "vendored only" for Rust) and document it. **STRETCH** on
  which surfaces the owner actually wants public.
- **[Docs] Deep but sprawling.** Many round-summary/essay `.md`s at root; no single
  "install + use the substrate" entry that a new dev follows top-to-bottom. → one canonical
  README quickstart (the material exists; it needs a front door).
- **[Supply chain] Strong.** Python is **stdlib-only** (CI installs `--no-deps`, comments
  explicitly forbid requests/numpy/pytest); Rust is **pure std, no external crates**
  (`cargo test` needs no registry). Keep it. Add `cargo audit`/dependency review only if a
  crate is ever introduced.

### B.3 Merge & release path (G20b / G20c)
Because **g20c is a superset of g20b** (verified: g20c re-includes `g20b.rs`, the g20b test,
the g20b vectors, and adds *both* Rust CI jobs; both branch from G20a), there are two clean
options:

- **Recommended — one PR, keep history: merge `claude/g20c-deposit-reader` → main.** It lands
  G20b **and** G20c together (both Rust readers, both CI jobs, both vector sets) in one
  reviewed step. Do **not** squash — G20a/G20b/G20c are the corpus's rung story. Then
  **delete `g20b` branch** (fully subsumed).
- **Alternative — two PRs for review granularity:** merge `g20b` → main first (adds the g20b
  reader + its CI job), then **rebase `g20c` on the new main** so its duplicated g20b files
  collapse to a no-op, and merge the g20c-only delta. More faithful to the two-rung story but
  more work; only worth it if the owner wants G20b reviewed in isolation.
- **Gate on green:** the merge must show the new `g20b-second-reader` / `g20c-deposit-reader`
  jobs **passing** (they do locally: Rust 18/18, and the vector-freshness `git diff` clean).
- **Tag** the substrate version after merge; if publishing, that tag drives the wheel build
  that already exists in CI.

### B.4 Deploy
jev-quilt is a library — "deploy" = **publish**. No outward web surface to gate for the
substrate itself. If/when published: PyPI via the existing build job (needs a trusted-
publish release trigger); Rust crate is optional. **STRETCH** — confirm intent before any
publish; publishing a package name is also a semi-outward, owner-gated act.
> **Do not** deploy `canon-api-worker` / `cloudflare-stack` (in the *cargo-line* repo, but
> substrate-flavored) to the internet without auth + rate limiting first — `CORS:*`,
> no-auth, arbitrary KV writes. If it is ever exposed: add a token/HMAC on write endpoints,
> a per-IP/per-node rate limit (KV or DO counter), payload size caps, and drop `CORS:*` to an
> allowlist. **Owner-gated.**

### B.5 Security / hardening
- **Refusal law**: G20a closed C9 (fail-open revocation → typed uncapped Receipt); G20b/G20c
  add an independent non-Python reader that *re-derives* the pins/deposit table, i.e. the
  tamper-evidence is now cross-language checkable. Test `tampering_a_witness_magnitude_changes_the_derived_table`
  (Rust) is exactly the right invariant. Strong — land it.
- **Input validation / supply chain**: stdlib-only + pure-std Rust = minimal attack surface.
- **Secrets**: none required by the library.

### B.6 CI (already the strongest of the three; finish it)
- Python unittest matrix (3.11/3.12) + canary + wheel build: **present, good** (with the
  nice anti-masking comments about the old `|| true` bug).
- **Rust `cargo test` + vector-freshness**: lands with the g20b/g20c merge. **P0 to merge.**
- Add: `cargo fmt --check` / `clippy` (P2), and the ResourceWarning cleanup (P2).

---

## Artifact C (dependency) — substrate-ts kernel
Not a standalone flagship, but **A depends on it** (vendored by hand into `substrate/ts/src/`).
- **[Merge]** `claude/phase0-worldmodel` (2 commits, v0.2.0, `npm test` green/8 checks) is
  unmerged to its own main. → merge it (single small PR, keep history).
- **[CI]** none. → add the same `node test.js && node test-world.js` gate.
- **[Drift risk]** the CLT copy under `substrate/ts/src/` is a *hand* vendor of this repo.
  → **STRETCH**: a check (in CLT CI) that the vendored kernel matches a pinned upstream
  version, or a documented sync procedure. Today nothing catches divergence.

---

## THE PRIORITIZED CHECKLIST (centerpiece)

Tiers: **Opus** = architecture/irreversible calls · **Sonnet** = build · **Haiku** = mechanical
runner · **Dispatcher** = orchestration/outward-gated. Effort: S ≤1h · M ~half-day · L ~1–2 days.

### P0 — blockers to *any* production (nothing ships live until these are done)
| # | Item | Repo | Tier | Effort |
|---|---|---|---|---|
| P0-1 | Add a **`node --test` CI gate** (push+PR→main) running `game/test/*.js`; a red suite blocks merge. | cargo-line | Sonnet | S |
| P0-2 | Build a **self-contained deploy `dist/`** (bundle/copy `game/` + `substrate/ts/src/` under the deploy root so no `../` escapes); prove it serves standalone with **zero 404s**. | cargo-line | Sonnet | M |
| P0-3 | **Merge the stack**: one PR `claude/the-chart` → main, history kept, **only on green** (needs P0-1). Tag `v0.1.0-game`. | cargo-line | Dispatcher | S |
| P0-4 | **Merge `g20c` → main** (subsumes g20b; turns on Rust CI), history kept, delete g20b branch. Verify both new Rust jobs green. | jev-quilt | Dispatcher | S |
| P0-5 | **Fix/retire `pages.yml`** so CI can never "successfully deploy" the wrong dir (`substrate-bundle`) as if it were the game. | cargo-line | Sonnet | S |

### P1 — needed for a *real* launch (a stranger opens the URL and it's right)
| # | Item | Repo | Tier | Effort |
|---|---|---|---|---|
| P1-1 | **Cloudflare Pages deploy of `dist/`** — preview first, then the A.4 verify checklist, then production. ⚠️ **Owner-gated outward action; explicit go required.** | cargo-line | Dispatcher | M |
| P1-2 | **Game-first README** (play + deploy + honest offline/data/rights posture); fix the false `npm install` root claim; fix stale "multiplayer" wording. | cargo-line | Sonnet | S |
| P1-3 | **Headless UI smoke test** (Playwright): seeded load, a stake lands, `pencilStakesPlaced` moves, no console errors. Wire into CI. | cargo-line | Sonnet | M |
| P1-4 | **Add `game/package.json`** (`test` script, Node engines pin). | cargo-line | Haiku | S |
| P1-5 | **Add a LICENSE** (owner picks; MIT/Apache-2.0 typical). | cargo-line | Dispatcher | S |
| P1-6 | **Ports canon parity test** (`ports.js` ≡ `locales/en/canon/ports.json` for the 10 US/CA). | cargo-line | Sonnet | S |
| P1-7 | **Merge substrate-ts `phase0-worldmodel` + add its CI**; document/verify the CLT vendor matches. | substrate-ts | Sonnet | S |
| P1-8 | **Data-rights confirmation** on the fuel/freight cited figures (oilpriceapi/ufreight ToS); swap to self-attributed synthetic baseline if any doubt. **STRETCH** (needs ToS read). | cargo-line | Opus | S |

### P2 — polish
| # | Item | Repo | Tier | Effort |
|---|---|---|---|---|
| P2-1 | **Self-host fonts** (drop the Google-CDN dependency to make offline-first literally true). | cargo-line | Haiku | S |
| P2-2 | **a11y pass**: keyboard path for stake/recall, `prefers-reduced-motion`, palette contrast. **STRETCH** on scope. | cargo-line | Sonnet | M |
| P2-3 | **Browser-compat smoke** across current Chrome/Firefox/Safari + mobile Safari. | cargo-line | Haiku | S |
| P2-4 | **Surface a version** in the UI margin + confirm git tagging on release. | cargo-line | Haiku | S |
| P2-5 | **Seed input fuzz/validation** (hostile seed can't break RNG/DOM). | cargo-line | Sonnet | S |
| P2-6 | **Lint/format** gate (eslint or `node --check`) in CLT CI. | cargo-line | Haiku | S |
| P2-7 | **Fix `ResourceWarning` unclosed files** (`tests/test_receipts_v2.py:58,245` → `with open`). | jev-quilt | Haiku | S |
| P2-8 | **`cargo fmt --check` + clippy** job. | jev-quilt | Haiku | S |
| P2-9 | **Canonical substrate quickstart README** (front door over the sprawl). | jev-quilt | Sonnet | M |
| P2-10 | **Decide + document the release surface** (PyPI/crates.io/vendored-only). **STRETCH** (owner intent). | jev-quilt | Opus | S |
| P2-11 | If `canon-api-worker` is ever exposed: auth + rate-limit + drop `CORS:*` before any deploy. **Owner-gated.** | cargo-line/infra | Sonnet | M |

---

## Honesty ledger (what this plan does *not* claim)
- The **game logic and both refusal-law layers are genuinely solid and fully tested** — the
  gaps are almost entirely at the *edges* (deploy packaging, CI, UI-layer tests, docs,
  license), not the core. That is a good place to be.
- **jev-quilt is the most production-shaped of the three** already (real CI, 244+18 green,
  stdlib/pure-std supply chain); its main gap is *merging the Rust gate that already exists*.
- Items marked **STRETCH** (a11y scope, ToS read, release-surface intent, vendor-drift check)
  are inferences or need owner input / a live check I could not do read-only this cycle.
- The **JEV legality/quality scorer** (`api.typesafe.ai/v1/systemone`) was reachable but
  rejected both payload shapes I tried (`api_usage_error`); I did not reverse-engineer its
  schema for this plan — findings above stand on direct file evidence, not on a JEV score.
- No real-world licensed dataset is proposed for shipping; the only real-world data in the
  game is a handful of cited, seed-labeled snapshot figures, and P1-8 gates even those.
