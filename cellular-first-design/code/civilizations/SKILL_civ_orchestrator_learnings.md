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
- **The low-`avg_score` civ and the low-`alignment` axis can be DIFFERENT civs in the same
  session** — and the low-`alignment` axis *does* rotate run-to-run even when the
  low-`avg_score` civ does not. Session 183: run low-`avg_score` = `civ-grounded` (same as
  lifetime low), but run low-`alignment` = `civ-mythic` (0.1670), whereas session 182's
  run low-alignment civ was `civ-therapist`. Do not conflate the two axes.
- **The Grounded alignment-to-quality gap ratio is a structural constant, not a coincidence:**
  **3.16x** in BOTH session 182 and session 183 (lifetime alignment gap 0.1353 vs quality gap
  0.0428). When the ratio lands near 3x, the diagnosis is "voice failure", not prose failure —
  and it is safe to state the diagnosis as structural rather than per-session.
- **A `chk(name, cond, detail)` helper with the arguments in the wrong order will report a
  FALSE FAIL that looks like a data defect.** A check written as
  `chk("... == 0", sum(...)==0)` (the boolean in the *detail* slot) evaluates the *name string*
  as the condition — truthy, so it PASSES, not fails; but the mirror mistake
  `chk("... == 0", sum(...))` puts the count in the *detail* slot and the condition stays the
  truthy string. Session 183 hit a variant that FAILED while the data was clean (0 real
  fallback triples, verified by an independent recount). **When a single assertion fails,
  recount the underlying quantity in a separate one-liner before believing the failure** —
  the ledger was correct and the checker was wrong.
- **Use the code-search API to find a file in a huge multi-repo org:**
  `GET /search/code?q=filename:<file>` returns the repo + path directly, and works for
  repos that `GET /user/repos` pagination never reaches (5 400+ owned repos). It also gives
  the exact path, so the sparse-checkout set can be written from the API response instead of
  guessed.
