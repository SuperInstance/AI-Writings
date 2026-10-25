---
name: civ-orchestrator-learnings
description: Durable operating knowledge for the Civilization Orchestrator (cellular-first-design). Mock provider rebuild checklist, verification gates, environment traps, and interpretation rules for the meta-GAN leaderboard.
---

# Civ Orchestrator — durable learnings

## The `wins`/`losses` counters are NOT in the ledger (false-FAIL trap)

`simulations.jsonl` rows carry exactly **9 keys** —
`avg_score, civ, civ_name, content_preview, params, prompt, provider, scores, ts` — and
**no `won` flag**. A verification check that reads `row["won"]` gets `0` for every civ and
reports a **false FAIL** on the wins and losses checks.

The counters live only in `culture.json`, incremented at
`civilization_orchestrator.py:296` for the **JEV-selected** winner
(`answers.best_civ.choice`, falling back to max `avg_score`).

**Take `times_won` from `meta_log.jsonl`'s `winner_civ` field**, never from the ledger.

## `max(results)` is NOT the winner

`meta_log.winner_civ` (the JEV `best_civ` selection) disagreed with the plain argmax on
**2 of 5** prompts in session 187 — prompt 2: argmax `civ-poetic` 1.97 vs winner
`civ-precise` 1.93; prompt 5: argmax `civ-precise` 1.94 vs winner `civ-formal` 1.69.

The stdout `Winner:` line **agrees with `meta_log`**; the argmax is the misleading one.
Count wins from `meta_log`, never from `max(results)`.

## Diagnostic discriminators that are not what they look like

- **A JEV 422 `union_tag_not_found` is a PAYLOAD-SHAPE error, not an auth error.** A probe
  built as `{"question":…, "weight":…, "scale":…}` is rejected. The orchestrator's own
  shape is `{"type": "score", "instructions":…, "criteria":[…]}`. **Copy the body from the
  source** (`jev_score`), do not improvise. A well-formed body returns HTTP 200
  `{"model":"jev-1.14.0", …}`.
- **A z.ai 401 `token expired or incorrect` means the endpoint is HEALTHY and the
  credential is ABSENT** — not that the provider is down. It is the expected probe result
  when `ZAI_TOKEN` is missing.
- **A zombie orchestrator process is a COMPLETED run.** The detached launcher never reaps
  the child, so `ps` shows `Zs` indefinitely. **Verify completion by the log tail and the
  row deltas, not by process exit.**
- **A 403 from the GitHub REST core API can be a rate limit, not an absence.** Check
  `/rate_limit` and note that **`/search/*` has its own separate quota** — core was
  5000/5000 (403) while search still had 30. A 403 renders as "not found" for every
  candidate at once.

## THE MOCK MUST RETURN AN OPENAI-SHAPED ENVELOPE (8th, undocumented-in-the-algorithm item)

`call_provider` does `r["choices"][0]["message"]["content"]`. A mock that writes the raw
body as the HTTP payload is a `JSONDecodeError` on the **first** request, not on a
liveness probe (the port answers, the body just isn't the shape the client wants).

```
{"id":"mock-zai-<seed>","object":"chat.completion","created":0,"model":"glm-4.5",
 "choices":[{"index":0,"finish_reason":"stop",
             "message":{"role":"assistant","content":<the 360-char body>}}],
 "usage":{"prompt_tokens":N,"completion_tokens":N,"total_tokens":N}}
```

This is the **eighth** thing to get right, after the seven documented fixes, and it is
**not** in the algorithm block. With it applied, the pre-flight passed **12/12 on the
first build**.

## A PRE-FLIGHT FIXTURE MUST BE READ FROM DISK, NEVER HAND-TYPED

The pre-flight's cultural-prompt length band (**167-209**) is a property of the real
`culture.json` files — their names, tenet lists and `voice_emphasis` strings. A fixture
with invented tenet strings measured **145-177** and produced a **false FAIL** on the
band check, which is indistinguishable from a real regression.

**Read the real cultures into the pre-flight.** A band assertion whose fixture is
hand-typed tests the fixture, not the system.

## The mock provider algorithm (fully known; do not re-derive)

The Control B mock for `zai` derives every response from the md5 of the request's
user message. This is now **verified 80/80 against the session-169 ledger**
(seed, colour and figure all match), so it does not need re-deriving.

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                               # MESSAGE-derived, NOT a request counter
seed   = h[(i*2)%8:(i*2)%8+4]                      # WIDENED slice, not padded
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"     # three components, NOT a division
```

`cultural_prompt` is exactly what `civilization_orchestrator.py` builds:

```
You are a voice in the tradition of "{name}".
Your tenets: {tenets joined by ", "}.
Your voice: {voice_emphasis}.

{prompt}
```

Only **4** distinct seeds are reachable from one message (the seed slices `h[0:8]`
at even offsets), so `i mod 4` is the whole index space.

**The observable signature of a message-derived index:** the seed is *stable across
every row of the same `(civ, prompt)` pair*. A request counter cannot produce that,
because the competition phase fires 8 civs in parallel and a counter would hand
them different values.

## Mock rebuild checklist — SEVEN fixes

| # | Fix | Symptom if missing |
|---|---|---|
| a | `seed[(i*2)%8:(i*2)%8+2]` index wrap | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | md5 of the **whole message** (not the first 8 alnum chars) | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| e | seed widened 2 → 4 hex chars | a 2-char slice collides ⇒ 39 distinct seeds / 40 rows, one prompt at 7/8 |
| f | **index from the MESSAGE (`d[0] % 4`), not a request counter** | **64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed** |
| g | **figure = three string components, not a division** | **`TypeError` on every request ⇒ HTTP 500 while the socket stays open; a port/200 liveness probe still looks healthy** |

**The spec's `figure = h[12:16] / h[16:20] / h[20:24]` is pseudo-code, not Python.**
Read literally it divides two `str` values. Fixing (a) does NOT fix this — (a) is
the seed-slice `ValueError`, (g) is the figure `TypeError`, and both present as
"HTTP 500 while the socket stays open". A liveness probe that only checks the
port or a 200 will not catch it.

## GATE-DESIGN RULE (the durable lesson)

**A pre-flight that only exercises *distinct* inputs cannot certify a *determinism*
property.** The pre-flight sends 40 distinct messages, so a counter-derived index
looks perfect — 40/40 distinct seeds, 40/40 distinct previews, a clean pass — while
the *run* is broken.

Therefore the pre-flight must include a **repeat-same-message probe**: send the same
message twice and assert the seed is identical (and matches the recomputed md5).

The same principle generalises: *any* pre-flight that proves "distinctness" is
silent about "determinism". Add a probe that repeats an input.

**The gate is now TEN checks** (was eight): 40/40 distinct seeds, 40/40 distinct
previews, 40/40 recomputed md5s (seed + colour + figure), 8/8 distinct seeds AND
8/8 distinct previews on every one of the 5 prompts, 0 literal `seed={}`, 0
`EXC:`/tracebacks, `[mock-zai` prefix on 40/40, **repeat-same-message ⇒ same seed
(40 × 2)**, and **0 `(civ,prompt)` pairs carrying >1 seed**.

**Seed-width rule: check the SLICE, not the render.** The documented "4 hex chars"
was originally satisfied by *padding* two 2-char slices, which is 256 values of
entropy wearing 4 characters' clothing. Widen the slice itself to
`h[(i*2)%8:(i*2)%8+4]` (65 536 values) and the padding becomes a no-op.

## Run-wide verification (isolate this run's rows)

Count from the **end** of each civ file (last 10), never a `ts` cutoff.

- per-civ ledger Δ +10 × 8 = **80** new rows
- `meta_log.jsonl` Δ +5
- `Winner:` lines = 5
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact to 1e-6**
- distinct seeds **40 / 80 rows**; **0** `(civ,prompt)` carrying >1 seed
- **80/80** rows match an independently recomputed message md5
- 8/8 distinct seeds AND previews on every competition prompt (5/5)
- meta-vs-ledger `avg_score` mismatches **0/40** — **use the later-`ts` row**
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples
- extinction risk NONE (threshold −10; the lowest civ sits ~110× above it)

**The meta-vs-ledger check needs the later-`ts` row.** The sim phase draws its prompt
at random from the same 5, so a `(civ, prompt)` pair recurs 1–4 times inside the 10 new
rows; the competition-phase row is the later one. `max(cands, key=ts)` gives 40/40
exact; first-match reports false mismatches. Match key is `m["prompt"][:80]`.

## A failed run must be reset, not patched

When the first mock of session 170 was rejected (counter-derived index), the ledger was
restored with `git checkout -- .` **from the clone root**, and the baseline was
re-verified against the captured pre-run counts before the second attempt. Never
hand-edit a ledger to make a check pass — reset and re-run so the baseline and the
result live in the same epoch.

`git show HEAD:<path>` must run with `cwd` = the **clone root**, not the civs
directory; the civs dir is not a git root and `git show` there returns empty stdout
→ `JSONDecodeError`.

## Environment traps (recurring)

- **NAS EDQUOT**: `/workspace` is at 100% (600 G of 600 G). `git clone` into
  `/workspace` fails with `Disk quota exceeded`; even a 20 MB `dd` fails. Clone to
  `/tmp` and bridge with a symlink. The NAS trap also blocks **file delivery** — `cp`
  into `/workspace` leaves a 0-byte file, so deliver by pushing to git.
- **The `write` tool is jailed to the workspace root** and cannot write `/tmp`. Use a
  bash heredoc for `/tmp` artifacts.
- `read` tool is likewise jailed — read `/tmp` files via bash.
- Upstream owner is **`SuperInstance/AI-Writings`**; the `ai-writings/…` slug 404s
  (the GitHub API is case-insensitive). Authenticated as `SuperInstance`.
- `gh` is not installed — use `GET /user/repos` with `GITHUB_TOKEN`.
- `GIT_SSL_NO_VERIFY=1` is required for git fetch/push. Push to the explicit token
  URL: `https://x-access-token:$GITHUB_TOKEN@github.com/<owner>/<repo>.git`.
- `ZAI_TOKEN` is absent from env and all 8 sandbox secrets; z.ai returns **401
  `token expired or incorrect`** ⇒ endpoint healthy, credential absent. Control B
  (the local mock) is the only provider path. Note the `ZAI_URL_OVERRIDE` alone is
  dead code — the token gate returns `None` first, so a placeholder token is required.
- JEV is **live**: a well-formed `questions` body returns HTTP 200 with
  `{"model":"jev-1.14.0", …}`. Export `TYPESAFEAI_KEY` from `TYPESAFE_AI_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch with stdout redirected
  **and** `< /dev/null`, then poll `ps` + the log.
- **Symlink rule**: `ln -sfn` will not replace an existing directory target. The
  bridge must point at the **clone root**, not the nested `cellular-first-design` dir.
  `rm -rf` the old link, `ln -s`, then verify with `stat -L -c '%d:%i'` on both sides
  + `-ef`.
- **Mock teardown**: kill by exact argv match (`python3 /tmp/mock_zai.py` and
  `timeout -s KILL 900 python3 /tmp/mock_zai.py`) — two pids. Never `pkill -f mock_zai`,
  which self-matches the killing shell. Then prove the port is closed: `curl -m 5` ⇒
  **exit 7**, `HTTP=000`.
- **The mock's `figure` is a string triple, NOT a division.** `h` is a hex STRING, so
  `h[12:16] / h[16:20] / h[20:24]` raises `TypeError` ⇒ HTTP 500 while the socket
  stays open (the very failure mode fix (a) exists to prevent). The verified fix
  (g) is `figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` — three components. A
  hex→int ratio also "works" numerically but is a **different algorithm** and will
  not reproduce the recorded ledger, so match the string form.
- **`GET /user/repos` paginates ~100/repo and the owner has 5 400+.** `ai-writings`
  does NOT appear in the first 10 pages of owned repos — use the **search API**
  (`GET /search/repositories?q=ai-writings+in:name`) to find `SuperInstance/AI-Writings`.
  Also note `cellular-first-design` is a **subdirectory** of that repo, not a repo
  of its own; the GitHub API is case-insensitive, so the `ai-writings/…` slug 404s.
- **Wiped workspace ⇒ sparse clone, not a full clone.** `SuperInstance/AI-Writings`
  is 3.7 GB and `/workspace` is at 100% NAS quota. `git init` + `core.sparseCheckout`
  + `sparse-checkout set cellular-first-design/code/civilizations`, `--depth=1` fetch,
  then symlink-bridge `/workspace/repos/ai-writings/cellular-first-design` → the
  clone root. **Verify with `os.path.samefile()`** — the shell `[ -ef ]` test
  mis-parses a symlinked path here; `stat -L -c '%d:%i'` on both sides is reliable.

## Interpretation rules for the meta-GAN

- **The run low and the lifetime low are different civs on different axes.** The
  run-level low *rotates* every session; the lifetime low is structural. Do not
  promote a run low to the lifetime finding.
- **Never treat `win_rate` as a quality metric.** The chooser asks JEV a **`choice`**
  question over 150-char `content_preview` snippets; `avg_score` is the mean of three
  **`score`** questions on the same text. Different questions, different answers. The
  clean-mock series has 16 five-sample points spanning 0/5 – 4/5 ⇒ the honest claim is
  *somewhere in 0–80 %*, not a point estimate.
- **Read the low-civ gaps, not just the low label.** If the *alignment* gap to the next
  civ is much wider than the *quality* gap, it is a **voice** failure (alignment is the
  dimension the meta-GAN selects on), not a prose failure.
- The **counter gap** (`culture.json` `relevance_score` − ledger Σ`avg_score`) is a
  **fixed per-civ offset**, not accumulating: Δ = **0.0000** for every civ between
  epochs. Per-civ (sessions 169–178, stable): whimsical −173.14, poetic −96.80,
  formal −85.53, grounded −84.35, mythic −51.11, engineer −44.24, therapist −42.11,
  precise −32.63 — **TOTAL −609.92**. The −609.92 is the **total, not a per-civ
  constant**; quote the per-civ values when comparing.
  `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the
  ledger** by an auditor. Compute both epochs within the same epoch before comparing.
- **A rounded endpoint is not a baseline.** The leaderboard rounds `relevance` to 2 dp;
  differencing two rounded endpoints leaves residuals up to ±0.0067 and makes an
  exact 8/8 check report 2/8 FAIL. Re-derive relevance deltas against the **unrounded
  `culture.json`** git blob. (Session 178: first pass 2/8, after re-derivation 8/8
  exact to 3.4e-13.)
- Run `avg_score` levels sit **above** the lifetime band; the **ordering** carries the
  information, not the level.

## Session 183 additions (2026-10-25)

- **The NAS EDQUOT trap also blocks DELIVERY, not just cloning.** `/workspace` is an NFS
  mount at 600 G/600 G shared across tenants. Writes there **return exit 0 and produce a
  0-byte file** — `cp` reports `failed to close ...: Disk quota exceeded` while the file
  *appears* in `ls -la` at size 0, and a bare `echo x > file` also lands 0 bytes. So a
  workspace-relative artifact is **undeliverable** no matter how it is written. Plan the
  durable copy in git (clone under `/tmp`, push upstream) and report the upstream path;
  do not retry workspace writes hoping for a different result. `/root`, `/home`, `/var/tmp`
  are on the overlay and writable, but the delivery surface reads `/workspace`.
- **`test -ef` is broken in this sandbox** — `bash: [: <path>: binary operator expected`
  on a perfectly valid two-argument `-ef`. Verify a symlink bridge by **inode identity**
  (`stat -c '%i'`) plus `readlink -f`, not by `-ef`. The bridge itself works; only the
  test is unusable. A "FAIL" here is a false alarm.
- **The mock seed slice is `h[(i*2)%8:(i*2)%8+4]` — a CONTIGUOUS 4-char slice.** The older
  spec block still shows two 2-char slices *concatenated*; that is a **different value**.
  A row written under one algorithm will not reconcile against a recompute under the
  other. **Check the SLICE, not the render.** Same for `figure`: it must be
  `f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` (three string components) — the spec's `/`
  separators read literally as division ⇒ `TypeError` ⇒ HTTP 500 on every request while
  the socket stays open, so a port/200 liveness probe still looks healthy.
- **The pre-flight gate's 40 messages are built CIV-major** (all 5 prompts per civ), so
  per-prompt aggregation must index `i*5+pi`, not `i*8+pi`. A gate that crashes on an
  `IndexError` *after* four assertions have already printed PASS is **not** a passing
  gate — make the gate print a final verdict and exit non-zero on any failure.
- **GitHub REST `GET /contents` rate-limits to 403 mid-enumeration**, which renders as
  "the file list is empty". Enumerate a file census over the **git protocol**
  (`git ls-tree <ref> <dir>`) instead — unlimited, and it is the only way to assert
  absence without a false negative.
- **`ZAI_TOKEN` is still absent** (47th session) — not in the env, not in any of the 8
  sandbox secrets; all four candidate tokens return 401 `token expired or incorrect`
  against `api.z.ai`, so the endpoint is healthy and the **credential** is missing.
  The orchestrator's provider gate returns `None` on an empty token, so **every
  simulation silently returns `None` and no rows are written** — an empty-token run
  looks like a clean run unless you assert on row counts. `ZAI_URL_OVERRIDE` alone is
  dead code behind that gate: set **both** `ZAI_TOKEN` (placeholder) and the override.
- **`JEV_KEY` reads `TYPESAFEAI_KEY`, but the env var is `TYPESAFE_AI_TOKEN`** — export
  the alias, or every score silently falls back to the 2.0/2.0/2.0 triple.
- **Chooser-vs-argmax agreement hit 0/5 with all 5 disagreements taking the
  LOWER-scoring candidate** (first 0/5 in the clean-mock series). `civ-poetic` was
  argmax on 5/5 prompts and won 0/5. Report it as a *sample*; the **direction** is the
  finding.
- **The run-level `quality` LEVEL is a moving quantity** — field mean was **0.9998** in
  session 183 vs ~0.91 in earlier sessions. Recompute it from the ledger every session;
  never carry the level forward. Rank on **cross-civ spreads** instead: session 183 had
  `alignment` 1.0680 › `quality` 0.6320 › `avg_score` 0.3820 › `novelty` 0.3360.
- **Session 182's run-low/lifetime-low coincidence did not reproduce.** In 183 the run
  low rotated to `civ-formal` (8th on run `avg_score` 1.5847 and run `quality` 0.7120)
  while `civ-grounded` placed **3rd of 8** on run `avg_score` (1.7573) — yet Grounded is
  still the lifetime low on all five axes (57th consecutive session). The run ranking
  and the lifetime table are **two separate claims**; say so explicitly.
- **`civ-grounded`'s low axes are alignment and quality, NOT novelty** — lifetime
  novelty 1.5849 is 6th of 8 (mid-field); the lowest lifetime novelty belongs to
  `civ-formal` (1.5022). Do not attribute Grounded's low-novelty to Grounded.

## Session 194 additions (2026-10-25)

- **THE CORE REST QUOTA CAN BE ALREADY EXHAUSTED AT SESSION START, AND A 403 LOOKS EXACTLY
  LIKE "NOT FOUND".** This session the authenticated quota read **5000/5000 (403)** at
  09:12Z, so `GET /user/repos`, `GET /user` and every repo probe rendered as *not found*.
  Recovery, in order: (1) `GET /rate_limit` unauthenticated to read the reset;
  (2) **`/search/*` has a separate quota** and still served requests;
  (3) **the git protocol is NOT rate-limited** — `git ls-remote` on a public repo succeeds
  instantly, so it is the only reliable *absence* test while core is exhausted;
  (4) wait out the reset, then `GET /user`. The token owner is **`SuperInstance`**
  (Casey Digennaro, uid 193104091) — **not** `rio-ARC`, which shows up in search results
  under a similar name and owns a *different* repo. **A 403 renders as "not found" for
  every candidate at once; check `/rate_limit` before concluding a repo is absent.**
- **THE RESPONSE-BODY LENGTH BAND CATCHS A FRESH MOCK BUILD.** A rebuilt template
  rendered at **711** chars against the **332–369** band and the gate reported a clean,
  localised `[FAIL] response body length band 332-369 min=711 max=711`. Trim the template
  to **354**. The band is not cosmetic: a body longer than ~369 chars pushes the **seed
  prefix out of the 200-char `content_preview` truncation**, silently breaking the
  seed+color+figure recompute for every row.
- **A VERIFIER BUG CAN LOOK LIKE A TRUNCATED LEDGER.** The first pass reported
  `[FAIL] per-civ ledger delta +10 x 8` with deltas of **−1412 / −1424 / …** — the check
  compared the *slice length* (10, the "last 10 rows") against the baseline *count*.
  **A delta of roughly −(baseline) is the signature of comparing a slice against a count**,
  not of a short ledger. The run was clean.
- **THE DOWN-GRADE STREAK IS NOT A TREND, IT IS A RESETTABLE COUNTER.** Session 193 broke
  it at 0 (5/5 agreement); session 194 re-established it at **13** (1/5 agreement, 4/4
  disagreements down-grade, `civ-poetic` argmax on 4/5 and winner on 0/5). **Re-base the
  streak every session from this session's own data — do not carry the number forward.**
- **THE LOW-RELEVANCE SIGNATURE IS "HIGH NOVELTY, LOW ALIGNMENT".** `civ-therapist` (run
  novelty **2.6550** = *highest in the fleet*, alignment **1.4910** = lowest) and
  `civ-whimsical` (2.5790 / 1.9240) both fit. Novelty spread is ~**0.15** against an
  alignment spread of ~**1.66**, so **the ranking is produced by alignment and quality,
  not novelty**. Report the axis, not the holder.
- **THE MOCK LOG LINE COUNT IS `2N + 1`, NOT `N`.** With the pre-flight's 40 messages
  (×2 for the repeat probe = 80 requests) plus the run's 80, the log reads **161** OK-200
  lines (80 pre-flight + 80 run + 1 GET). Compare against the log, not a remembered
  constant.

## Session 195 additions (2026-10-25)

- **REPLACE EVERY FIXED MOCK-LOG LINE COUNT WITH A MULTISET IDENTITY.** The inherited
  check compared the mock log's OK-200 count against a hardcoded **161**, which silently
  assumes the pre-flight ran **exactly once**. This session the pre-flight ran **twice**
  (run 1 crashed at check 12 on a gate bug, run 2 was the full 14/14 pass) and there was
  one manual `curl` liveness probe, so the true count was **241** and the fixed number
  reported a **false FAIL**. The replacement — **the seed multiset of the LAST 80 OK-200
  log lines must equal the seed multiset of the 80 ledger rows** — held exactly and is
  *immune to how many times the pre-flight ran*. **A count check encodes an assumption
  about how many times an artifact was produced; a multiset identity encodes none.**
  Generalise: whenever a check must survive a re-run of an upstream step, assert an
  *identity between artifacts*, not a *magnitude of one artifact*.
- **A GATE THAT PRINTS 12 PASSES AND THEN TRACEBACKS IS NOT A PASSING GATE.** The
  pre-flight's repeat-same-message probe unpacked a 3-tuple as a 4-tuple and crashed
  *after* twelve `[PASS]` lines. The gate must print a final verdict and exit non-zero
  on any failure — a traceback after partial output reads as a pass to a human and to a
  log-scraper alike.
- **A CLONE FAILS OR SUCCEEDS BY DESTINATION MOUNT, NOT BY SIZE.** The `--depth 1`
  clone into `/workspace/repos` died on `.git/description` with `Disk quota exceeded`;
  the **same clone into `/tmp` succeeded immediately**. The NAS EDQUOT applies to the
  mount, not to git. Clone to `/tmp` and symlink-bridge.
- **THE BRIDGE MUST POINT AT THE INNER `cellular-first-design` DIRECTORY.** The upstream
  repo root contains a `cellular-first-design/` subdirectory and the orchestrator's
  `CIVS_DIR` is hardcoded to the **inner** path, so a bridge to the repo root makes
  `civilizations.json` invisible. Verify by **inode identity**
  (`stat -L -c '%d:%i'` → `129:10425` on both sides) plus `os.path.samefile()`; the
  shell `[ -ef ]` test is unreliable in this sandbox.
- **THE RESPONSE-BODY LENGTH BAND CAUGHT THE FRESH BUILD AGAIN.** A first template
  rendered at **387** characters against the **332–369** band; the gate reported a clean,
  localised `[FAIL] response body length band 332-369 min=387 max=387`. Trimming the tail
  to **297** put the body at **351**. Target **351** (not 354 — the prefix width varies
  with the seed, so the tail length is the control, not the total).
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 14.** `civ-precise` swept
  5/5 for the **fifth consecutive** sweep, disagreed with the `avg_score` argmax on
  **4 of 5** prompts, and **all four took the LOWER-scoring candidate**. Agreement
  **1/5 (20 %)**. `civ-poetic` was argmax on **4 of 5** and won **0 of 5**.
- **THE RUN-LEVEL LOW ROTATED TO `civ-whimsical`** (run `avg_score` **2.1440**,
  `alignment` **2.1910** lowest) — a **14th different civ in 14 sessions**. The bottom
  two were separated by only **0.0277** on `avg_score` but by **0.9660** on `alignment`.
  *The holder rotates; the axis does not.*
- **THE LOW-RELEVANCE SIGNATURE IS STILL "HIGH NOVELTY, LOW ALIGNMENT".** `civ-whimsical`
  (novelty **2.5810** / alignment **2.1910**) and `civ-therapist` (**2.6220** /
  **2.1930**) both fit. Novelty spread **0.1510** against an alignment spread
  **1.0780** ⇒ the ranking is produced by alignment and quality, not novelty. Report
  the axis, not the holder.
- **`civ-grounded` was the lifetime low for the 67th consecutive session** (`relevance`
  **1451.12**, `relevance_per_sim` **1.037**), yet its lifetime `win_rate` **0.102** is
  **3rd-best in the fleet**. *Selection and relevance are separate axes.* Its low axis
  is **quality** (**1.4820**, the lowest in the fleet), **not** novelty (**2.6040**,
  2nd-highest).

## Session 200 addenda (2026-10-25)

- **THE BRIDGE SYMLINK MUST TARGET THE *INNER* SUBDIRECTORY, AND THE SHALLOW-CLONE
  TRICK IS FASTER THAN `--depth 50`.** `git clone --depth 1 --filter=blob:none --sparse`
  + `git sparse-checkout set cellular-first-design` gave a **9.9 M** working tree versus
  a multi-GB full clone. The symlink must point at
  `<clone>/cellular-first-design` (the *inner* dir), not the clone root — pointing it
  at the root makes `code/civilizations/` unresolvable and the failure looks like
  "the repo is missing" rather than "the symlink is one level too high".
- **THE NAS EDQUOT TRAP NOW REJECTS WRITES AS SMALL AS 1 KB.** `cp` of the 13.6 KB
  report, then of a 5.9 KB gzip, then a 1 KB head — **all three** failed with
  `Disk quota exceeded` and left **0-byte** files visible in `ls`. `df` shows
  `600G/600G 100%`. *Do not spend attempts shrinking the payload — delivery by
  `git push` is the only channel that works.* Always verify the copied size
  (`wc -c`), never trust the `ls` entry.
- **THE GITHUB REST CORE QUOTA IS 5000/5000 AND EXHAUSTS MID-SESSION.** After the
  push, `GET /repos/.../commits/main` returned a JSON body of **nulls** — not a 404.
  The raw body was `API rate limit exceeded`, and `/rate_limit` confirmed
  `core: {limit: 5000, used: 5000, remaining: 0}`. *A null-field API response is
  rate-limit noise, not absence.* Verify pushes with the **git protocol** instead:
  `git ls-remote <token-url> refs/heads/main` (no quota) and
  `git cat-file -p FETCH_HEAD:<path>` to confirm the blob is really in the pushed
  commit. This is the same principle as "assert absence over the git protocol".
- **THE JEV KEY ALIAS IS `TYPESAFEAI_KEY` BUT THE SANDBOX EXPORTS `TYPESAFE_AI_TOKEN`.**
  Export the alias before running or `jev_score` silently falls through to the
  `2.0/2.0/2.0` fallback triple. With the alias exported, JEV returns
  `{"model":"jev-1.14.0"}` and **0 fallback triples** — this is a live credential,
  unlike the z.ai one.
- **PRE-FLIGHT 11/11 ON THE FIRST BUILD, WITH A 366-CHAR BODY.** Adding the
  "cultural-prompt length band 167-209" check *read from the real `culture.json`
  files* (never hand-typed) and the repeat-same-message determinism probe both
  passed first time. The mock's response body is **366 chars** — inside the
  documented 332-369 band on the first attempt.

## Session 201 addenda (2026-10-25)

- **A CRASH IN THE CHECKER IS A CHECKER FAILURE, AND IT CAN HIDE BEHIND PASSES.** Two
  independent scripts crashed this session on trivial Python mistakes *after* printing
  several `[PASS]` lines: the pre-flight died with `NameError: name 're' is not defined`
  (an `import re` nested inside a helper was never in module scope when a module-level
  loop called a second helper), and the verifier died with `TypeError: check() takes from
  2 to 3 positional arguments but 4 were given` (a detail string passed as a 4th
  positional arg to a 3-arg helper). Both were caught **only** because the gate prints a
  final `VERDICT:` line and exits non-zero. *The run itself was clean in both cases and
  was never re-run — the distinction between the artifact and the checker is what let a
  clean run survive a broken checker.* Corollary: a helper's arity is part of its
  contract; when a check helper's signature changes, grep every call site.
- **THE 332-369 BODY BAND CAUGHT THE FRESH BUILD, AND THE RIGHT FIX WAS TO REMOVE THE
  VARIANCE — NOT TO TRIM THE LONGEST INSTANCE.** The first template rendered at
  **349-381** (a long civ name pushed it over). Truncating the culture-derived fields
  (`trad` 12 chars, `tenet` 10, `voice` 10) made the body **constant at 298-304** —
  *below* the band — so one fixed sentence was appended, landing at **352-358**.
  *A band check is a variance check: fix the cause of the variance, not its maximum.*
  Budget two build iterations for a fresh template; the band is not cosmetic.
- **THE 5/5 SWEEP STREAK IS A COUNTER WITH A PRINTED EXPIRY DATE.** `civ-precise` won
  5/5 for **ten consecutive sessions** (191-200); session 201 gave a prompt to
  `civ-engineer`, ending the streak at 10. *The first honest statement of a streak's
  length is the one that ends it* — never carry the count forward as a current fact.
- **THE CHOOSER HAS NEVER UP-GRADED.** Agreement across sessions 198-201 is
  3 → 0 → 2 → **3**, and **every disagreement in the series took the LOWER-scoring
  candidate (0 up-grades ever)**. A chooser that only ever picks the worse candidate is
  *anti-correlated* with `avg_score` where it disagrees, not merely noisy. The standing
  suspect is unchanged: the `best_civ` criteria map (`civ_id` -> `civ name`) is a label
  map, so the chooser may be scoring labels rather than texts.
- **THE REPO CAN BE FOUND BY CODE SEARCH, WHICH THE REPO-LIST PATH CANNOT REACH.**
  `GET /user/repos` needs ~54 pages for this owner; `GET /search/repositories?q=…+in:name`
  and **`GET /search/code?q=civilization_orchestrator+in:path`** both resolved
  `SuperInstance/AI-Writings` and the exact script path in one call, and `/search/*`
  has a **separate quota** that survives a core-quota exhaustion. Use code search to
  confirm the path before cloning.
- **THE SPARSE-CLONE RECIPE WORKS FROM A BARE `--no-checkout` CLONE.** `git clone
  --filter=blob:none --no-checkout --depth 1` then `git sparse-checkout init --cone` +
  `git sparse-checkout set cellular-first-design` + `git checkout` gave a **9.9 M**
  working tree from a 3.7 GB repo. Bridge the symlink at the **inner**
  `cellular-first-design` directory; verify with `stat -L -c '%d:%i'` (here
  `129:10423` on both sides) and `os.path.samefile()` → `True`.

## Session 204 additions (2026-10-25)

- **PARSE THE MOCK HEADER FROM A KNOWN-GOOD SAMPLE BEFORE ASSERTING THE RECOMPUTE.**
  The mock's header is `[mock-zai <seed>] <color> <figure>.` — the **seed lives INSIDE
  the brackets**, the colour and figure after them. Two parser bugs in a row, both
  producing a *clean-looking* "the mock is broken" story about a mock that was working
  perfectly: (a) taking `prev.split("]")[0][len("[mock-zai "):]` for the seed but
  `prev.split("]")[1].split(" ")[1]/[2]` for colour/figure — the `[1]` chunk is
  `" <color> <figure>. <body>"`, so a plain 3-way split misaligns; (b) reading the
  **seed** from `split("]")[1]`, which compares `d372` against the expected `6ffd` and
  reports **0/40 recomputed md5s**. *A 0/40 recompute means "the parser is wrong"
  before it means "the mock is wrong" — dump one real body and parse it by hand
  first.* The correct parse is
  `s = prev.split("]")[0][len("[mock-zai "):].strip()` and
  `c, f = prev.split("]")[1].strip().split(" ")[:2]` with `f.rstrip(".")`.
- **THE GATE REPORTS 14/15 WITH A CLEAN `VERDICT:` LINE AND A NON-ZERO EXIT — THAT IS
  THE DESIGN WORKING.** The md5-recompute check was red on a fully healthy mock; the
  pre-flight refused to bless the run and the *checker* was fixed instead of the
  artifact. The final verdict line plus the non-zero exit is what separates a gate
  from a log scraper. *Never let a partially-passing gate authorise a run.*
- **`pkill -f "mock_zai.py"` SELF-MATCHES THE WRAPPER SHELL AND KILLS IT BEFORE THE
  MOCK STARTS.** The port then answers `HTTP=000` with curl exit **7**, and
  `/tmp/mock_zai.out` does not exist at all — the "launch" never ran. The documented
  teardown rule (kill by exact argv match, never `pkill -f`) applies to **startup**
  too: a `pkill` in the same command line as the launch will match its own shell.
- **THE MOCK BODY LANDED AT 347 CHARS ON THE FIRST BUILD — INSIDE THE 332-369 BAND
  WITH NO ITERATION.** Sessions 200 and 201 each needed two or three build
  iterations; the band check is worth keeping because it *catches* variance, but it
  is not a fixed cost. Building the body from a single fixed sentence (no
  culture-derived fields, so no length variance) is what makes it land first time.
- **THE RUN LOW AND THE LIFETIME LOW DECOUPLED FOR THE THIRD TIME IN A ROW, AND THE
  WIDEST ALIGNMENT GAP CONVERGED WITH THE RUN LOW.** Session 204's run low is
  `civ-whimsical` (`avg_score` **1.0700**, `alignment` **0.4150** = lowest in the
  fleet) and it *also* holds the widest alignment gap (**2.4550**) — where sessions
  202 and 203 split the two across different civs. `civ-grounded` is the lifetime low
  for the **76th consecutive session** and placed **5th of 8** on run `avg_score`
  (**1.5963**). *Do not carry a coincidence forward as a pattern — and do not carry a
  decoupling forward as a pattern either.*
- **THE ALIGNMENT SPREAD WAS 3.95x THE QUALITY SPREAD AND 16.70x THE NOVELTY SPREAD —
  THE WIDEST NOVELTY NARROWNESS IN THE SERIES** (novelty spread **0.1470**). The
  ranking is produced by alignment almost alone.
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 1/5 (20 %).** Agreement
  across sessions 199-204 is 0 → 2 → 3 → 1 → 2 → **1**, and **every** disagreement in
  the series took the **lower-scoring** candidate. `civ-precise` was argmax on 3/5 and
  won 2/5; `civ-engineer` was argmax on 2/5 and won **0**. `civ-formal` won 3 of 5
  prompts outright, ending `civ-precise`'s four-session 5/5-sweep run. The chooser has
  **never up-graded** in 204 sessions. The standing suspect is unchanged: the
  `best_civ` criteria map (`civ_id` → `civ name`) is a *label* map, so the chooser may
  be scoring labels rather than texts.

## Session 205 additions (2026-10-25) — concurrent-run collision

- **ANOTHER AGENT CAN RUN THE SAME SESSION AGAINST THE SAME REPO WHILE YOU ARE
  WORKING, AND YOUR PUSH WILL BE REJECTED AS NON-FAST-FORWARD.** This session the
  remote gained a **session 204** commit (`39addc4`, authored by "Claude Opus 4.8")
  from the **same baseline `f60b152`** while my own session-204 run was in flight;
  two further commits (`probe` / `remove probe`) were unrelated user activity on
  `prose/`. `git push` then failed with **`! [rejected] main -> main (fetch first)`**.
  *The rejection is the signal that a sibling run landed — fetch and diff before
  assuming your push was simply stale.*
- **DO NOT NUMBER TWO INDEPENDENT RUNS THE SAME SESSION — RENUMBER THE LATER ONE AND
  KEEP BOTH REPORTS.** The remote already owned `RUN_REPORT_2026-10-25_session204.md`.
  Mine was renamed to **session 205** and the commit message rewritten to say so, with
  a note that the two runs share only a starting point (different mock seeds, different
  JEV draws). *Overwriting a sibling's report destroys evidence; a merge that keeps
  both is the honest record.*
- **THE MERGE MUST KEEP BOTH RUNS' LEDGER ROWS, AND THE COUNTER GAPS ARE THE PROOF.**
  Both sessions appended 10 rows per civ to the same `simulations.jsonl` and 5 rows to
  `meta_log.jsonl`, so **19 files conflicted**. Resolved by reconstructing each ledger
  as `base + session204_rows + my_rows`, deduping on `ts`, and **recomputing
  `culture.json` from the merged data** (`relevance` = base + both deltas, `wins`/`losses`
  = base + both deltas). The proof that the merge is arithmetically right: the per-civ
  **counter gaps came back at exactly the documented stable values** (grounded −84.35,
  whimsical −173.14, formal −85.53, poetic −96.80, precise −32.63, mythic −51.11,
  therapist −42.11, engineer −44.24; total −609.92). *A merge that silently drops a
  sibling's rows shows up as a shifted counter gap — that is the cheapest possible
  integrity check.*
- **DO NOT "FIX" THE MERGE BY CHECKING OUT ONE SIDE.** `git checkout FETCH_HEAD -- <file>`
  to "clean up" a conflicted report **deleted the other side's file**, and the
  re-applied commit then removed it again. The recovery is `git show <rev>:<path>` into
  the working tree — the blob is still in the object store even when the file is gone
  from the index. *Recover from the object store, never by re-running the run.*
- **`<<<<<<<` MARKERS ALREADY EXIST IN THE UPSTREAM REPO — SCOPE ANY CONFLICT-MARKER
  SCAN TO THE FILES YOU TOUCHED.** A repo-wide scan flagged
  `RUN_REPORT_2026-10-25_session159.md` and `skills/civ-orchestrator-learnings.md`; both
  were present in the **base** commit `f60b152`, in files my work never touched, and the
  session-159 report literally *documents* those markers as a historical artifact.
  Checking `git diff --name-only <base> HEAD` first separates "your merge left
  conflict markers" from "the repo has always contained the literal string".
- **THE MOCK HEADER PARSE: THE SEED IS INSIDE THE BRACKETS.** `[mock-zai <seed>] <color>
  <figure>.` — the correct parse is
  `s = prev.split("]")[0][len("[mock-zai "):].strip()` and
  `c, f = prev.split("]")[1].strip().split(" ")[:2]` with `f.rstrip(".")`.
  Two wrong parses produced a clean-looking "the mock is broken" story about a mock
  that was working perfectly: a misaligned 3-way split (`IndexError` on all 40
  requests) and reading the seed from `split("]")[1]` (**0/40 recomputed md5s**).
  *A 0/40 recompute means "the parser is wrong" before it means "the mock is wrong" —
  dump one real body and parse it by hand first.*
- **THE PRE-FLIGHT GATE REFUSED THE RUN TWICE, AND BOTH TIMES THE BUG WAS THE
  CHECKER, NOT THE MOCK.** The gate printed `14/15 PASS` with a clean `VERDICT:` line
  and a non-zero exit, and the md5-recompute check was the red one. The run was not
  started on a red gate. *The final verdict line plus a non-zero exit is what separates
  a gate from a log scraper — never let a partially-passing gate authorise a run.*
- **`pkill -f "mock_zai.py"` SELF-MATCHES THE WRAPPER SHELL AND KILLS IT BEFORE THE
  MOCK EVER STARTS.** The port then answers `HTTP=000` with curl exit **7** and
  `/tmp/mock_zai.out` does not exist at all. The documented "kill by exact argv match"
  rule applies to **startup** as well as teardown: a `pkill` on the same command line
  as the launch matches its own shell.
- **THE MOCK BODY LANDED AT 347 CHARS ON THE FIRST BUILD — INSIDE THE 332-369 BAND
  WITH NO ITERATION**, because the body is built from a single fixed sentence with no
  culture-derived fields (so there is no length variance to control). Sessions 200 and
  201 each needed two or three iterations. *A band check catches variance, not cost —
  eliminate the variance and the band passes once.*
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 1/5 (20 %).** Agreement
  across sessions 199-205 is 0 → 2 → 3 → 1 → 2 → **1**, and every disagreement in the
  series took the **lower**-scoring candidate. The chooser has **never up-graded** in
  205 sessions. The standing suspect is unchanged: the `best_civ` criteria map
  (`civ_id` → `civ name`) is a *label* map, so the chooser may be scoring labels
  rather than texts.

## Session 207 additions (2026-10-25)

- **THE `CIVS_DIR` IS HARDCODED TO `/workspace`, SO THE SYMLINK BRIDGE IS MANDATORY — AND
  IT MUST POINT AT THE *INNER* `code` DIRECTORY, NOT THE CLONE ROOT.** With the clone in
  `/tmp` (the NAS is at 100 % quota) the first launch died instantly with
  `FileNotFoundError: '/workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilizations.json'`.
  The bridge is
  `ln -s /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code`,
  verified by inode identity (`stat -L -c '%d:%i'` → `130:1704352` on both sides) plus
  `os.path.samefile()` → `True`. *A bridge to the clone ROOT leaves `code/civilizations/`
  unresolvable and the failure reads as "the repo is missing", not "the symlink is one level
  too high".* The failure is instant and total (no rows written), so it is unmistakable —
  but it is an **environment** failure, not a run failure: fix the bridge, do not re-run
  the analysis.
- **`ZAI_URL_OVERRIDE` IS DEAD CODE BEHIND THE TOKEN GATE — SET `ZAI_TOKEN` *AND* THE
  OVERRIDE.** The override is read *after* `if not token: return None`, so an override
  with no token makes every simulation return `None` and write **zero rows** — an empty
  run that looks like a clean run unless you assert on row counts.
- **THE MOCK BODY LANDED AT 357 CHARS ON THE FIRST BUILD — AND THE BAND IS SOLVED
  ALGEBRAICALLY.** For a 4-hex seed and an 18-char figure the header
  `[mock-zai <seed>] <color> <figure>.` is a **constant 33 chars**, so a fixed tail of
  length *T* yields a **constant** body *T + 33*. Three fixed sentences of **321** chars
  ⇒ **357**, inside the 332-369 band, on build 1. *A band check catches variance, not
  cost — eliminate the variance (no culture-derived fields in the body) and the band
  passes once.*
- **`GET /search/code?q=civilization_orchestrator+in:path` FOUND THE REPO IN ONE CALL
  AFTER `GET /user/repos` AND `GET /search/repositories` BOTH MISSED IT.** The upstream is
  **`SuperInstance/AI-Writings`** — a *user* account, so `GET /orgs/ai-writings/repos`
  404s. Code search (`/search/*` has a **separate quota** that survives core exhaustion)
  is the fastest confirmation that a *path* exists before cloning.
- **THE DOWN-GRADE STREAK RE-BASES EVERY SESSION, AND IT IS AT 1.** Agreement across
  sessions 203-207 is 1 → 0 → 1 → **4**; the last three read 1 → 0 → 1. `civ-precise`
  swept **5/5** (its first sweep since session 191) and the single disagreement again took
  the **lower**-scoring candidate. *The first honest statement of a streak's length is the
  one that ends it* — and the chooser has still never up-graded.
- **`civ-grounded` HELD THE LIFETIME LOW FOR THE 78th CONSECUTIVE SESSION**
  (`relevance` **1647.13**, `relevance_per_sim` **1.084**), yet its lifetime `win_rate`
  **0.095** is 3rd-best in the fleet. Its low lifetime axis is **quality** (**0.4519**,
  lowest in the fleet), **not** novelty (**1.7097**, 4th of 8). *Selection and relevance
  are separate axes.*
- **THE RUN LOW ROTATED TO `civ-therapist` (15th different run low in 15 sessions) AND IT
  HELD THE WIDEST ALIGNMENT GAP IN THE FLEET (2.0980).** Novelty gaps for the low civs
  were **negative** this session (−0.0770 / −0.0650 / −0.0480): the low-relevance axis
  is **alignment**, and novelty is flat-to-high for *everyone*. Alignment spread
  **2.0980** was **3.06x** the quality spread and **9.58x** the novelty spread.
- **THE PER-CIV COUNTER GAP IS STILL THE CHEAPEST INTEGRITY CHECK.** After this run the
  gaps came back at exactly the documented stable values (grounded −84.35,
  whimsical −173.14, formal −85.53, poetic −96.80, precise −32.63, mythic −51.11,
  therapist −42.11, engineer −44.24) — a run that dropped or duplicated rows would show
  a shifted gap immediately.

## Session 209 additions (2026-10-25)

- **THE BODY BAND IS NOW FOUR SESSIONS IN A ROW ON THE FIRST BUILD — THE ALGEBRA IS
  STABLE.** Header `[mock-zai <4-hex>] #<6-hex> <figure>. ` with the figure fixed at
  **18 chars** ⇒ a **constant 44-char header** ⇒ a **300-char** tail ⇒ body **340**,
  inside the 332-369 band with **no** iteration. Sessions 207, 208 and 209 all landed
  first try. *Compute the band algebraically before writing the template; do not iterate
  the template.* The tail must be a **single fixed sentence with no culture-derived
  fields** — that is what removes the length variance the band exists to catch.
- **THE `ls -la` VERIFICATION THE PROMPT ASKS FOR NEEDS `-L` WHEN THE PATH IS A
  SYMLINK BRIDGE.** `ls -la <dir>/civilizations/` returns **"No such file or
  directory"** on a perfectly healthy run, because the last path component crosses a
  symlink and `ls` does not follow it without `-L`. *A missing directory in the
  verification step is a reporting artefact, not a missing run.* The bridge
  (`.../cellular-first-design/code` → the clone's inner `code`) is the same shape as
  sessions 200-208; `ls -laL` and the per-civ `ls -la` on `civ-*/simulations.jsonl`
  both show the real mtimes.
- **THE DOWN-GRADE SERIES NOW READS 0/5 → 4/5 → 1/5 → 3/5 (sessions 199, 207, 208,
  209).** Agreement **3/5 (60 %)**, 2 down-grades, 0 up-grades. `civ-precise` won **4 of
  5** and was the argmax on **4 of 5**; `civ-poetic` was argmax on **1 of 5** and won
  **0 of 5**. *The series oscillates — re-derive the number every session and never
  carry a streak forward as a current fact.*
- **THE RUN LOW AND THE LIFETIME LOW HAVE NOW BEEN DIFFERENT CIVs FOR SIX SESSIONS
  RUNNING** (`civ-grounded` lifetime-low at `relevance` **1684.58** /
  `relevance_per_sim` **1.095**, run rank **6 of 8**; `civ-therapist` run-level low at
  run `avg_score` **1.4617**). `civ-grounded`'s lifetime `win_rate` **0.094** is still
  **3rd-best in the fleet** — *selection and relevance are separate axes.*
- **THE LOW-RELEVANCE SIGNATURE HOLDS: HIGH NOVELTY, LOW ALIGNMENT.** Alignment
  spread **1.9410** = **3.39x** the quality spread and **8.51x** the novelty spread.
  The alignment tail beyond −1.5 is `civ-therapist` (**−1.9410**) and `civ-mythic`
  (**−1.5450**); novelty gaps are **negative for every low civ**, so novelty is not a
  separating axis. *Report the axis, not the holder.*

## Session 212 additions (2026-10-25)

### 1. THE PRE-FLIGHT "NO LITERAL `seed={}`" ASSERTION HAS AN INVERTED-SENTINEL TRAP

The pre-flight reported **FAIL** on `literal_seed_none` while the mock was perfectly
correct: the response body contained **0** occurrences of `seed=`. The bug was the
check, not the server — the flag was set to `True` *on find* and the assertion read
`not literal_seed`, so a correct mock could never pass.

```
if "seed={}" in body: literal_seed = True     # wrong: sets True when the text IS present
results["literal_seed_none"] = (not literal_seed,)
```

The fix is to count the occurrence and assert on the count:

```
if "seed={}" in body: literal_seed = False
results["literal_seed_none"] = (literal_seed,)
```

**Generalisation: a pre-flight FAIL on a component you have already independently
verified is a CHECK bug until proven otherwise.** Re-derive the fact directly (here:
`post()` one message and count `"seed="` in the body) before touching the code. A
pre-flight that reports a failure on a green component will send you off to "fix" a
server that was never broken — and the fix risks introducing the real bug the
pre-flight was designed to catch.

### 2. A SINGLE FAILED `ls` IS NOT EVIDENCE OF A MISSING TREE ON THE NAS

After the run, `ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/`
returned **"No such file or directory"** even though the symlink bridge was intact
(`ls -la /workspace/repos/` showed `ai-writings -> /root/ai-writings`) and the clone root
listed fine. A second attempt one minute later resolved cleanly with the expected
contents.

**Re-read before concluding the repo vanished.** The NAS mount is flaky under
concurrent symlink traversal, and the failure mode reads exactly like a missing
checkout. Always corroborate with a second path (`ls` the clone root directly) before
re-cloning.

### 3. A SWEEP AND A CHOOSER-AGREEMENT RATE ARE INDEPENDENT MEASUREMENTS

Session 212: `civ-precise` won **5/5** competitions, while the chooser agreed with the
argmax only **2/5 (40 %)** — 3 down-grades, 0 up-grades. A 5/5 sweep coexisted with a
poorly-calibrated chooser.

**Never infer chooser agreement from the win count.** They measure different things:
the win count is about who won, the agreement rate is about whether the chooser's
*reasoning* matched the scores. Both must be reported, and the down-grade count is
always re-derived from the session's own `meta_log`.

### 4. REPORT THE GAP NEXT TO THE SPREAD WHEN NAMING THE RUN LOW

`civ-therapist` (**1.5710**) and `civ-whimsical` (**1.5957**) differ by **0.0247**
against a run `avg_score` spread of **0.7633** — the two lowest civs are separated by
less than one third of the run's own spread. Their ordering is noise. A "run low" claim
that does not print the gap beside the spread is not a defensible claim.

## Session 213 additions (2026-10-25)

### 1. THE SEED INDEX IS THE RAW MD5 BYTE `d[0] % 4`, NOT THE HEX DIGIT

The verified mock algorithm indexes the seed by `i = d[0] % 4` where `d` is the **raw
digest bytes**. A near-miss reading, `i = int(h[0], 16) % 4`, looks identical ("the first
byte mod 4", and both land in 0-3) but is a **different function**: `d[0]` spans
`0x00-0xFF` while `int(h[0],16)` spans only `0x00-0x0F`.

**The failure is silent and partial.** `colour = h[8:12]` and
`figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` do **not** depend on the index, so a wrong
index reproduces them **perfectly** — 80/80 — while the **seed** is wrong on roughly 70 % of
rows. A pre-flight therefore reports `distinct_seeds 1/40` and `recomputed_md5 0/40` on a
mock that is behaving exactly as the ledger demands.

**How to settle it:** brute-force every candidate rule and let the ledger pick. Sweeping all
4-hex windows of `h` crossed with `%2/%4/%8` index rules, the true rule scored **80/80**
only under the raw-byte reading. *When a composite field recompute is partially right, the
wrong field is the one that depends on the index — start there.*

**Confirmation that the algorithm is right:** 80/80 recent-format ledger rows match on
seed + colour + figure when recomputed from the **real `culture.json`** files.

### 2. THE MOCK HEADER PARSE MUST BIND THE FIGURE'S TRAILING `". "`

The recorded header is `[mock-zai <4hex>] #<4hex> <4/4/4>. ` — the figure is followed by a
**period and a space**. A pattern that expects a bare space after the figure matches
**0/40**, and the pre-flight then reports a false "the mock is broken" story:
`distinct_seeds 1/40`, `recomputed_md5 0/40`, `per_prompt_8x5` all red, while
`distinct_previews_40`, `body_len_band` and `cultural_prompt_band` stay green.

The working parse:

```python
HDR = re.compile(r"^\[mock-zai ([0-9a-f]{4})\]\s*#?\s*([0-9a-f]{4})\s+"
                 r"([0-9a-f]{4}/[0-9a-f]{4}/[0-9a-f]{4})\.\s")
```

Note the `#` is **attached to the colour** in the body (`#d64d`), and the `\.` is
required. This is the **second** header-parse trap in the project after the
seed/colour mis-split (session 204). *Generalise: when a pre-flight goes red on the
recompute, dump one real body and parse it by hand before touching the server — a 0/40
recompute means "the parser is wrong" before it means "the mock is wrong".*

### 3. A `simulations_run` DELTA MUST BE TAKEN AGAINST THE `culture.json` BASELINE

`simulations_run` counts **simulated** runs; the ledger carries rows from **every prior
session**, so the two are not comparable. Checking the counter against
`len(ledger_rows) - 10` failed **8/8** on a run whose per-civ **counter gaps came back at
exactly the documented stable values** (grounded -84.35, whimsical -173.14, formal -85.53,
poetic -96.80, precise -32.63, mythic -51.11, therapist -42.11, engineer -44.24).

Take the baseline from the **git HEAD blob** of `culture.json`, not from the ledger.
*Corollary that generalises: the per-civ counter gap is the cheapest integrity check in
this project — it will tell you the run was clean while your check is the thing that is
broken.*

### 4. THE SPARSE-CLONE RECIPE WORKS AND THE BRIDGE TARGETS THE INNER `code` DIRECTORY

`git init` + `core.sparseCheckout` + `.git/info/sparse-checkout` containing
`cellular-first-design/code/civilizations` + `git fetch --depth 1 --filter=blob:none`
gave an **11 M** working tree from a **3.7 GB** repo. The bridge is
`ln -sfn /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code`,
verified by inode identity `stat -L -c '%d:%i'` -> `129:3669` on both sides plus
`os.path.samefile()` -> `True`.

**The cone-mode warning is harmless:** `git sparse-checkout` prints
`warning: disabling cone pattern matching` / `unrecognized pattern` for a multi-segment
path, and still checks the directory out correctly. Verify the tree with `ls`, not with
the absence of a warning.

### 5. THE MOCK BODY LANDS IN BAND ON THE FIRST BUILD WHEN THE TAIL IS A SINGLE FIXED STRING

Header `[mock-zai <4hex>] #<4hex> <4/4/4>. ` is a **constant 38 chars**; a 318-char fixed
tail gives a **constant 356-char** body, inside the documented 332-369 band, with **no**
iteration. The tail must contain **no culture-derived fields** — that is what removes the
length variance the band exists to catch.

### 6. THE RUN LOW AND THE LIFETIME ALIGNMENT LOW ARE DIFFERENT CIVS ON DIFFERENT AXES

Session 213's run low is `civ-whimsical` (`avg_score` **1.5107**, alignment **0.8900**
fleet-low, novelty **2.4860** fleet-high). But the **lifetime** alignment low is
`civ-therapist` (spread **1.0570** over the full ledger) while `civ-grounded` is the
lifetime low on `avg_score` and `quality`. The run table and the lifetime table are
**two separate claims** — report both, and report the axis for each.

## Session 214 additions (2026-10-25)

### 1. A SWEEP AND A PERFECT CHOOSER-AGREEMENT RATE CAN COEXIST — AND NEITHER PREDICTS THE OTHER

This session `civ-precise` won **5/5** competitions *and* the chooser agreed with the
`avg_score` argmax on **5/5 (100 %)** — no down-grades, no up-grades. The three previous
sessions were 0 % (211), 40 % (212), 40 % (213). Both measures were perfect at once.

**Do not read a 100 % agreement as "the chooser is calibrated."** It is a **5-sample point
at 100 %** sitting on a series whose last three points were 0 %, 40 %, 40 %. The honest
claim is that this session's chooser and the argmax picked the same civ every time; the
series-level calibration claim is unchanged.

**Generalise the pairing rule:** the win count is *who won*; the agreement rate is *whether
the chooser's reasoning matched the scores*. Sessions 211/212/213 all had a sweep
coexisting with poor agreement; session 214 has both perfect. **Never infer either from
the other, in either direction.**

### 2. THE RUN LOW'S SIGNATURE IS LOW ALIGNMENT; THE FLEET GAP IS ALIGNMENT, NOT NOVELTY

`civ-whimsical` was the run low (`avg_score` **1.2807**, quality **0.7180** fleet-low,
alignment **0.6850** fleet-low) with novelty **2.4390** — mid-field. The run's alignment
spread is **2.5690** against a novelty spread of **0.1250**: a factor of **20.6**. The
ranking is produced by alignment and quality, not novelty.

The bottom two were separated by **0.2243** on `avg_score` against a run spread of
**1.1607** — a gap of **19 %** of the spread, so their *ordering* is weak but the
*identity* of the bottom is not. **Print the gap next to the spread** (as in session 212)
and report the axis, not the holder.

### 3. THE COUNTER-GAP CHECK MUST BE TOLERANCED AT 1e-6 — A 1e-9 TOLERANCE IS A FALSE FAIL

The per-civ counter gap (`culture.json` `relevance_score` − ledger Σ`avg_score`) is the
cheapest integrity check in this project, and its documented stable values held **exactly**
this session (grounded −84.35, whimsical −173.14, formal −85.53, poetic −96.80, precise
−32.63, mythic −51.11, therapist −42.11, engineer −44.24) with per-civ gap deltas of
**+0.0000000000 for all 8**.

The first pass nevertheless reported `[FAIL] counter_gap_stable_8of8`. The cause was the
**check**, not the run: it computed the current gap as
`base_relevance + (csum - bsum) - bsum` and compared that to a *separately computed*
baseline gap, so the two differed in the last float bits and the 1e-9 tolerance rejected
them.

**Compute both epochs the same way** — subtract the ledger sum from the `culture.json`
blob on each side — and compare with **1e-6**. *A pre-flight FAIL on a component you have
already independently verified is a CHECK bug until proven otherwise; re-derive the fact
directly before touching the artifact.*

### 4. THE MOCK BODY BAND CAN BE HIT WITHOUT BREAKING LEDGER RECONCILIATION

The documented body band is **332–369** chars (a body longer than ~369 pushes the seed
prefix out of the 200-char `content_preview` truncation and breaks the seed+colour+figure
recompute). A body of **337** — a constant 38-char header plus a 299-char fixed,
culture-free tail — lands in band on the first build.

**The tail may be extended without breaking the existing ledger's reconciliation** as long
as its first 162 characters match the recorded rows verbatim. The recorded preview is
truncated at 200 chars, so the tail's visible prefix is what the historical rows pin
down; everything after it is free. *When sizing the tail, preserve the recorded prefix
exactly and only append.*

### 5. THE BRIDGE TARGET AND THE CLONE LOCATION, RE-CONFIRMED

`SuperInstance/AI-Writings` is a **user** account repo. `/workspace` is at 100 % NAS quota
(600 G of 600 G) and `git clone` into it dies on `.git/description` with
`Disk quota exceeded`; the **same clone into `/tmp` succeeds immediately**. The bridge is
`ln -s /tmp/clone/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`
— it must point at the **inner** `cellular-first-design` directory, because the
orchestrator's `CIVS_DIR` is hardcoded to the **inner** `code/civilizations` path. Verify
with `stat -L -c '%d:%i'` → `129:12604` on both sides plus `os.path.samefile()` → `True`
(`[ -ef ]` remains unusable in this sandbox).
