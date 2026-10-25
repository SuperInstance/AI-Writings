---
name: civ-orchestrator-learnings
description: Durable operating knowledge for the Civilization Orchestrator (cellular-first-design). Mock provider rebuild checklist, verification gates, environment traps, and interpretation rules for the meta-GAN leaderboard.
---

# Civ Orchestrator — durable learnings

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
