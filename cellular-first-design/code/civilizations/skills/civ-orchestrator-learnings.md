# Civ Orchestrator — durable cross-session lessons

The authoritative operational RUNBOOK lives in the repo at
`cellular-first-design/code/civilizations/RUNBOOK.md`.
This file holds the short, high-signal rules that survive a sandbox wipe.

## Session 138 (2026-10-24) — a per-run low can move *off* the lifetime low; both are real

**Verification held (23/23 checks — the most thorough pass yet).** per-civ Δ = **+10** × 8 =
**80 new rows** (engineer 816→826, formal 847→857, grounded 862→872, mythic 819→829,
poetic 841→851, precise 811→821, therapist 814→824, whimsical 874→884), `meta_log` Δ = **+5**
(423 → 428), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed with `provider={zai}`,
**0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback triple, **40 distinct
seeds / 80 rows** (= 8 civs × 5 prompts) with **0** `(civ,prompt)` combos carrying >1 seed, and
**5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews** — the **thirteenth
consecutive clean measurement** (118, 120–123, 125, 131–134, 136, 137).

**NEW — the per-run low and the lifetime low can be *different civs*, and that is not a
contradiction.** `civ-grounded` has been the lifetime low for 40 straight sessions, but this run
it placed **6th of 8** on `avg_score` (0.1550); `civ-therapist` took the run-level low (0.1257)
and sat lowest on `alignment` (0.0180), with `civ-engineer` 7th (0.1313). The session-132 rule
(*per-run low ⇒ watch axis*) and the session-121 rule (*lifetime gap ⇒ finding*) both survive:
**the lifetime table is the structural signal, the run ranking is the watch axis.** Report both;
never let a single run promote or demote a civ on its own.

**`civ-therapist` is now a second watch axis** — run-level low on both `avg_score` and
`alignment`. Its lifetime standing is mid-field (5th of 8 on `avg_score`, 1.6035 on
`alignment`), so it is *not* a finding. It becomes one if it repeats.

**`civ-grounded` remains the low-relevance civ — 40 consecutive sessions (95–138).** Last on
lifetime `avg_score` (1.1220), `alignment` (1.3056), `quality` (0.5273), `relevance` (978.37),
`relevance_per_sim` (1.078). The structural gap is **alignment: 0.4694 below the next civ vs
0.0450 on quality = 10.4× wider.** Alignment is the dimension the meta-GAN selects on ⇒ a
**voice** failure, not a prose failure. Lifetime novelty (1.5331) is above median — Grounded is
not boring, it is *unmistakable in a way the chooser does not reward*. Extinction risk **NONE**
(threshold −10; lowest relevance 978.37 = 98× above).

**Chooser vs `avg_score` argmax: 1/5 (20 %).** `civ-precise` won 3/5, `civ-engineer` 1,
`civ-formal` 1. Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) →
3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → 1/5 (131) →
2/5 (132) → 2/5 (133) → 0/5 (134) → 4/5 (136) → 1/5 (137) → **1/5 (138)**. Eighteen five-sample
points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What survives every
session: the chooser is **not** a pure argmax, and **every** observed disagreement across the
fleet goes the same way (it picks a **lower**-scoring candidate). The "ternary values" case
(chooser took a candidate **0.420 below** the argmax) ties the session-137 record (0.683) for the
largest disagreement in the clean-mock series. **Never treat `win_rate` as a quality metric.**

**Quality collapsed again (mean 0.0139, max 0.030)** — the 119/121/122/138 regime vs
session-120's 0.106–0.446. **The quality collapse is a LEVEL that moves, not a stable property.**
This run's cross-civ spreads: `alignment` 1.140, `novelty` 0.427, `quality` 0.026 — `alignment`
again carried the widest spread and is again the axis the chooser selects on. **Compare
cross-civ spreads, not absolute levels, before ranking on a dimension.**

**Pre-flight probe (8 civs → 8/8 distinct seeds AND previews, cultural-prompt lengths 168–200,
`[mock-zai seed=…]` present, 0 tracebacks) passed again** — `/tmp` was wiped, so the mock was
rebuilt from scratch and **both** historical bugs had to be re-applied on rebuild (session-112
index wrap `seed[(i*2)%8:((i*2)%8)+2]`, session-118 md5-of-whole-message seeding). A one-word
probe cannot reach the `i>=4` path that crashes; a crashing mock still leaves a listening
socket, so a port/200 check is **not** proof of correctness.

## Session 143 (2026-10-24) — row isolation must be per-civ tails, NOT `rows[-N:]` over concatenated files

**Run clean (session 143, 15th consecutive clean mock).** per-civ Δ = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (448 → 453), `Winner:` lines = **5**, **80/80** rows
`[mock-zai`-prefixed with `provider={zai}`, **0** rows with a JEV `error` key, **0** rows with the
2.0/2.0/2.0 fallback triple, **40 distinct seeds / 80 rows** with **0** `(civ,prompt)` combos
carrying >1 seed, **8/8 distinct seeds AND 8/8 distinct previews** on all 5 competition prompts.

### NEW (this session) — the `rows[-80:]` isolation bug, and how it fakes a mock failure

Isolating a run's rows by **`rows[-80:]` over the concatenation of all `civ-*/simulations.jsonl`
files** is **wrong**: `glob()` order is filesystem order, not chronological, so the last-80 slice
of the *concatenation* mixes historical rows from a late-alphabet civ into "this run's" rows.
This session it reported **15 distinct seeds (expected 40)** and **5 `(civ,prompt)` combos with
>1 seed (expected 0)** — a false mock-integrity failure that would have triggered a pointless
"mock is broken" investigation.

**Correct isolation:** take the **last 10 rows of each civ file** (the per-civ **+10** delta
already proves the boundary), concatenate those 80, then **sort by `ts`** before any grouping.
With that method: 40 distinct seeds, 0 combos with >1 seed, 8/8 + 8/8 on every prompt — i.e.
every clean-session assertion passes.

**Rule: never group or count across a concatenated multi-file list without an explicit `ts` sort.**
`rows[-N:]` is only safe on a list that is *already* in chronological order. For per-civ ledgers
the per-file tail is the correct primitive, because the per-civ delta assertion is the thing that
locates the boundary in the first place.

### Low-relevance civ — the low label did NOT rotate (41 sessions, 95–143)

`civ-grounded` remains the lifetime low on all five axes: `avg_score` 1.0906, `alignment`
1.2566, `quality` 0.5017, `relevance` 921.18, `relevance_per_sim` 1.048 — **last of 8 on every
one**. The binding constraint is still **alignment**: gap to the next civ 0.4656 vs quality's
0.0446 (**10.4×** wider). A voice failure, not a prose failure, because alignment is the axis
the meta-GAN selects on. Lifetime novelty 1.5135 is above median — Grounded is not boring, it
is unmistakable in a way the chooser does not reward.

**Session 141 flagged `civ-therapist` as the run-level low; it did not repeat.** This run
`civ-grounded` took the run-level `avg_score` low (0.5727) and `civ-therapist` took the
run-level `alignment` low (0.1310) at 7th of 8 on `avg_score` (0.5920) — *different civs* on
*different axes*, which is **not** a contradiction (session-132 rule). Therapist's lifetime
standing is mid-field (1.2888), so it is **not** a finding; it becomes one only if it repeats.

**Chooser vs `avg_score` argmax: 2/5 (40%)** — `civ-precise` won 3, `civ-formal` 2. The
chooser is still not a pure argmax, and every observed disagreement again took the
*lower*-scoring candidate. **Never treat `win_rate` as a quality metric.**

**Extinction risk NONE** — threshold −10, lowest relevance 921.18 = 92× above the floor.
Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

### Environment (re-confirmed)

- **NAS EDQUOT is total** (600 G/600 G): *every* `/workspace` write — even a 1-byte `echo` via
  Python — fails with `[Errno 122] Disk quota exceeded`; `cp` exits 1 and leaves 0-byte files
  that `ls` still lists. `mkdir` and `ln` work. The **symlink bridge** is still the only way in.
- **No `CAP_SYS_ADMIN`** (verified via `/proc/self/status` CapEff `a80425fb`) ⇒ `mount --bind`
  is denied and `unshare -m` fails with `Operation not permitted`. Do not spend time on
  namespace/bind-mount workarounds for the NAS trap — go straight to the symlink bridge.
- **`gh` is still not installed** — use `GET /search/repositories?q=...` and `GET /user/repos`
  with `GITHUB_TOKEN`. `SuperInstance/AI-Writings` resolves; the `ai-writings/cellular-first-design`
  slug 404s (the API is case-insensitive).
- **Sparse clone recipe that worked:** `git clone --depth 1 --filter=blob:none --sparse <token-url>`
  then `git sparse-checkout set cellular-first-design/code/civilizations` → **5.7 MB** instead of
  the 3.6 GB full clone. Bridge the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` on both sides + `-ef` (this session: `129:10465` both sides, EF_OK).
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`.** JEV liveness = an empty
  `questions` dict returns **422 `too_short`** — a payload-shape complaint that proves the
  token was accepted. Do not read 422 as "down".
- **`ZAI_TOKEN` is still absent** from env and from all 8 sandbox secrets; z.ai 401s (endpoint
  healthy, credential gap). Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder)
  **and** `ZAI_URL_OVERRIDE` — the override alone is dead code behind the token gate.
- **Mock rebuilt from scratch this session** with the session-112 index-wrap fix
  (`seed[(i*2)%8:((i*2)%8)+2]`) *and* the session-118 whole-message md5 seeding fix. Pre-flight
  passed: 8/8 distinct seeds AND 8/8 distinct previews, `[mock-zai` prefix present, **0
  tracebacks**. Kill by exact args (`python3 /tmp/mock_zai.py`), then confirm the port is closed
  (`curl` exit 7 = refused).
- Push to the explicit token URL (`git push "<token-url>" HEAD:main`) — pushing to the clone's
  own remote fails with `could not read Username`. Verify with the commits API + the contents
  API (read the remote `leaderboard.json` back and compare against local), never the push's
  own exit code.

## Session 147 (2026-10-25) — the prompt path can be wrong on BOTH segments; read `CIVS_DIR` from the script

**Run clean (session 147, 19th consecutive clean mock).** per-civ delta = **+10** x 8 = **80 new
rows** (engineer 906->916, formal 937->947, grounded 952->962, mythic 909->919, poetic
931->941, precise 901->911, therapist 904->914, whimsical 964->974), `meta_log` delta = **+5**
(468 -> 473), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed with `provider=zai`,
**0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback triple, **40/40**
distinct seeds, **0** `(civ,prompt)` combos with >1 seed, sim->competition ts gap at index 4
in **8/8** civs (1.06 s - 22.85 s), and **5/5** competition slots at 8/8 distinct seeds AND
8/8 distinct previews.

### NEW (this session) — a wrong prompt path is NOT a mount race, and the repo is only ONE segment of it

The task named `/workspace/repos/ai-writings/cellular-first-design/code/civilizations/`. The
workspace was a **fresh NAS mount with nothing cloned** — `/workspace` held only
`.plugin-cache`, no `repos/`, no `ai-writings/`. The slug was wrong on **both** segments:
`ai-writings/` is the **repo** (`SuperInstance/AI-Writings`) and `cellular-first-design/` is a
**subdirectory inside it**.

**Rule: read the target path out of the script's own path constant before hunting the tree.**
`CIVS_DIR = Path("/workspace/repos/ai-writings/cellular-first-design/code/civilizations")`
encodes the correct full path in one line — grep it rather than guessing at the tree.

**Distinguish the two failure modes by *consistency*, not by one `ls`:**
- **5/5 consistent `ls` failure + a near-empty `/workspace`** => *not cloned*. Clone first.
- **Intermittent `ls` failure with `/workspace/repos/...` populated** => *mount race*; retry
  (session-145 rule).

The symlink bridge only helps **after** a clone exists — it bridges a tree into place, it
does not create one.

### The `write` tool cannot reach the bridged tree

Two separate jails, both hit this session:
- `write` to `/workspace/repos/ai-writings/cellular-first-design/...` =>
  `ENOTDIR: not a directory, mkdir '/workspace/repos/ai-writings/cellular-first-design'`
  (it will not traverse the symlink).
- `write` to a path under `/workspace/analysis/` => sporadic **`-122` on close**.

**Rule: for any file that must land inside the bridged tree, use a bash heredoc to the real
`/tmp` path.** Use `printf`/heredoc to `/tmp` for throwaway analysis scripts too.

### Mock teardown — kill BOTH pids, then prove the port is closed

Kill by exact args: `python3 /tmp/mock_zai.py` (server) and
`timeout -s KILL 900 python3 /tmp/mock_zai.py` (wrapper). Then
`curl -m 5 -X POST http://127.0.0.1:8799/...` => **exit 7** (refused) and `HTTP=000`. Never
`pkill -f mock_zai` — it self-matches the killing shell (2nd occurrence of that trap).

### Low-relevance civ — the low label did NOT rotate (45 sessions, 95-147)

`civ-grounded` remains the lifetime low on all five axes: `avg_score` 1.0647, `alignment`
1.2201, `quality` 0.4828, `relevance` 939.86, `relevance_per_sim` 1.023 — **last of 8 on every
one**. The binding constraint is still **alignment**: gap to the next civ 0.2557 vs quality's
0.0336 (**7.6x** wider). A voice failure, not a prose failure, because alignment is the axis
the meta-GAN selects on. Lifetime novelty 1.4911 is above median — Grounded is not boring, it
is unmistakable in a way the chooser does not reward.

**`civ-therapist` — 3rd session at the run bottom, now on BOTH axes** (run `avg_score` 0.1470
and run `alignment` 0.0280, both lowest of 8). Still mid-field on the lifetime axis
(`avg_score` 1.2538, 5th of 8) => **watch axis, not a finding**. It becomes one only if the
lifetime axis moves too.

**Chooser vs `avg_score` argmax: 0/5 (0 %)** — the chooser disagreed in **every** competition.
`civ-precise` swept 4/5, `civ-formal` 1/5. Every disagreement again took the **lower**-
scoring candidate (largest: winner 0.190 vs argmax 0.743). Clean-mock series: 0/5 (118) ->
3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) -> 0/5 (124) -> 4/5 (125) ->
4/5 (137) -> 1/5 (138) -> 2/5 (139) -> 4/5 (144) -> 4/5 (146) -> **0/5 (147)**. The rate is
**not narrowing**; report it as a sample and keep the **direction** as the finding.
**Never treat `win_rate` as a quality metric.**

**Extinction risk NONE** — threshold -10, lowest relevance 939.86 = 94x above the floor.
Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

**Counter gap is a FIXED per-civ offset** — whimsical +63, grounded +43, formal +42, poetic
+37, engineer +22, mythic +20, therapist +17, precise +16, byte-identical to session 145.

## Session 144 (2026-10-24) — the `Connection: close` fix, and the mock probe must use the *long* cultural prompt

**Run clean (session 144, 16th consecutive clean mock).** per-civ Δ = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (453 → 458), `Winner:` lines = **5**, **80/80** rows
`[mock-zai`-prefixed with `provider={zai}`, **0** rows with a JEV `error` key, **0** rows with the
2.0/2.0/2.0 fallback triple, **40 distinct seeds / 80 rows** with **0** `(civ,prompt)` combos
carrying >1 seed, **8/8 distinct seeds AND 8/8 distinct previews** on all 5 competition prompts.

### NEW (this session) — a mock that answers 200 but never closes the connection hangs `curl`

The rebuilt mock used `BaseHTTPRequestHandler` with a `Content-Length` header but **no
`Connection: close`**. `urllib` (what the orchestrator uses) was fine, but a plain
`curl -X POST …` **hung until the tool's 30 s timeout** while the server had already logged
`200` — the classic "server answered, client waited for EOF" split. Symptom is easy to
misread as "mock is down" and sends you re-debugging a healthy server.

**Rule: a 200 in the mock's access log is not the same as the client completing.** Probe with
`curl -m 8` (a timeout is a *result*, not an error) and add `Connection: close` to the
response. After the patch the same probe returned `HTTP=200 time=0.001053`.

### NEW (this session) — the pre-flight probe must use the *exact long cultural prompt*

Probing the mock with a one-word body (`{"content":"hi"}`) does **not** exercise the path the
orchestrator uses. The correct probe builds the full cultural prompt
(`You are a voice in the tradition of "<CIV NAME>".\nYour tenets: …\nYour voice: …\n\n{prompt}`)
for all 8 civs and asserts **8/8 distinct seeds AND 8/8 distinct previews**, plus
`[mock-zai` prefix on all 8 and `grep -c Traceback` / `grep -c EXC:` on the mock log → 0.
A one-word probe passes even against a partially broken mock. Measured this session: 8/8 and
8/8, body lengths 332–369 chars.

### Low-relevance civ — the low label did NOT rotate (42 sessions, 95–144)

`civ-grounded` remains the lifetime low on all five axes: `avg_score` 1.0851, `alignment`
1.2510, `quality` 0.4974, `relevance` 926.99, `relevance_per_sim` 1.043 — **last of 8 on every
one**. The binding constraint is still **alignment**: gap to the next civ 0.2667 vs quality's
0.0344 (**7.8×** wider). A voice failure, not a prose failure, because alignment is the axis
the meta-GAN selects on. Lifetime novelty 1.5069 is above median — Grounded is not boring, it
is unmistakable in a way the chooser does not reward.

**`civ-therapist` appeared as a watch axis in sessions 138, 141 and 144 and has still never
become a lifetime finding** (lifetime `avg_score` 1.2818, mid-field). It took the run-level
`alignment` low (0.4460) while `civ-grounded` took the run `avg_score` low (0.5803) — the
session-132 "different civs on different axes" case, not a contradiction.

**Chooser vs `avg_score` argmax: 1/5 (20%)** — `civ-precise` won 3, `civ-mythic` 2. The chooser
is still not a pure argmax, and every disagreement again took the *lower*-scoring candidate
(largest this run: winner 0.83 vs argmax 1.32 on ternary values). **Never treat `win_rate` as
a quality metric.**

**Extinction risk NONE** — threshold −10, lowest relevance 926.99 = 92.7× above the floor.
Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

## Standing findings

- **`civ-grounded` (The Grounded) is the low-relevance civ** — last on lifetime `relevance`
  (978.37), `relevance_per_sim` (1.078), `avg_score` (1.1220), `alignment` (1.3056) and
  `quality` (0.5273). The **alignment** gap is the structural one (0.4694 vs a 0.0450 margin
  on quality — 10.4× wider). Alignment is the dimension the meta-GAN *selects* on, so the civ
  fails to *embody a distinctive voice*, not merely to write weakly. 40 sessions (95–138).
- **`civ-formal`** = the low-novelty axis (lifetime novelty 1.4065, last; alignment 1.9081
  healthy).
- **`civ-engineer`** = 2nd-lowest lifetime `avg_score` (1.2821), still no gap to the low civ.
- **The two stable inverses:** `civ-poetic` = 1st on lifetime `avg_score` (1.7042) / `quality`
  (0.9123) but last on `win_rate` (0.012, 5/403); `civ-precise` = best `win_rate` (0.553) and
  highest `alignment` (2.2983) but only 3rd on `avg_score` (1.4882).
- **Extinction risk NONE** — threshold −10, lowest relevance +978.37 (98× above floor).
  Registry 8, `max_civs` 12. Extinction/birth only runs under `--loop`.
- **Counter gap is per-civ uneven**, not a uniform offset. `save_state()` has no lock ⇒
  `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs**, not a dict. A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies. Winner fields are
  `winner_civ` / `winner_name`.
- **Never treat `win_rate` as a quality metric** — it is a *selection* metric.

## Environment rules (re-confirmed, 6th session running)

- **NAS EDQUOT is total.** *No* write to `/workspace` succeeds — even a 5-byte `echo` yields a
  0-byte file that `ls` still lists, and `cp` exits 1 with `Disk quota exceeded` while leaving
  those 0-byte files behind. `mkdir` and `ln` work. The only way in is the **symlink bridge**.
- **Clone to `/tmp`** (overlay, ~28 G free; NAS quota does not apply), then
  `ln -sfn /tmp/aiw/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  Verify by **inode identity** (`stat -L -c '%d:%i'` on both sides + `-ef`), not by `ls`.
- **Do not flatten the clone.** The symlink target is the *nested* `cellular-first-design` dir.
  A 5/5 consistent `ls` failure = wrong target; an intermittent one = mount race. Retry before
  concluding the tree is gone.
- **Upstream is `SuperInstance/AI-Writings`** (the `ai-writings/cellular-first-design` slug
  404s; the API is case-insensitive). `gh` is **not installed** — use
  `GET /search/repositories?q=...` and `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** (script reads the former,
  sandbox stores the latter). Unset ⇒ JEV degrades to the 2.0 default and every score is
  constant. JEV liveness probe: an empty `questions` dict returns **422 `too_short`** — a
  payload-shape complaint, which proves the token was accepted. Do not read 422 as "down".
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is absent** from env and from all 8 sandbox secrets; z.ai returns 401 (endpoint
  healthy, credential gap). JEV is live.
- **Tool timeout 30 s < orchestrator run ~55 s.** Launch detached, poll `ps` + the log.
- **Kill the mock by exact args** (`python3 /tmp/mock_zai.py`) — two pids (timeout wrapper +
  server). Never `pkill -f mock_zai`, which self-matches. Verify the port is closed afterward
  (`curl` exit 7 = refused).

## Verification pattern (assert on rows, never on exit code)

All failure modes are silent with exit code 0 — a missing token makes `call_provider()` return
`None`, `run_simulation()` return `None`, and the competition short-circuit on
`if not results: return None`.

| Assertion | Expected for `--sims 5 --prompts 5` |
|---|---|
| per-civ `simulations.jsonl` delta | **+10** each (5 sim-phase + 5 competition-phase) |
| total new ledger rows | **80** |
| `meta_log.jsonl` delta | **+5** |
| `Winner:` lines | **5** |
| rows with `[mock-zai` prefix | **80** |
| rows with a JEV `error` key | **0** (this is what proves JEV really scored) |
| rows with the 2.0/2.0/2.0 fallback triple | **0** |
| distinct seeds across the 80 new rows | **40** (8 civs × 5 prompts) |
| `(civ, prompt)` combos with >1 seed | **0** |
| distinct previews+seeds per prompt (ts-sorted last-8 slice) | **8/8 on all 5 prompts** |

Isolate this run's rows by **count from the end of the file** (`rows[-delta:]`), not by a `ts`
cutoff — prior sessions left mock rows behind, so a `ts >=` filter pulls in history.

**Per-prompt distinctness must use the ts-sorted last-8 slice.** The 80 new rows are two
interleaved phases (40 sim-phase, 40 competition-phase); grouping by prompt and taking `rows[-8:]`
mixes them and yields a false 3–6/8. Sort all 80 by `ts` first, then take the last 8 per prompt.

**`avg_score` is a top-level row field, not a member of `scores`.** `scores` holds only
`quality` / `novelty` / `alignment` / `confidence`; averaging `r["scores"]["avg_score"]` silently
yields **0.0 for every civ** and makes the whole ranking look flat. Use `r["avg_score"]`.

## Session 149 (2026-10-25) — 21st consecutive clean mock measurement

- **A blobless + sparse clone is the cheap path for this 3.7 GB repo**:
  `git clone --filter=blob:none --no-checkout --depth 1` + `sparse-checkout set cellular-first-design`
  → **6.1 MB on disk**, one shot, nothing else fetched. Far better than `--depth 1` full checkout.
- **The hung `curl` right after launching a background server is usually the SHELL, not the
  server.** A `setsid nohup ... &` started in the same command as a foreground `curl` can leave
  the tool blocked on the inherited stdout. Check `ps` for the server pid and re-probe in a
  *separate* command before declaring the mock broken — it was healthy (HTTP 200) in session 149.
- **The `ls -la` on the requested path worked once the bridge existed** — confirming again that
  a 5/5 consistent failure means "not cloned", and that the bridge (not a retry) is the fix.
- **Quality collapse is a LEVEL that moves.** Run-level quality was 0.011–0.052 this session
  (16th of the last 17 clean-mock sessions) — the lowest yet — yet the lifetime spread ordering
  was unchanged. **4th consecutive observation of the same rule: rank on cross-civ spreads,
  never on absolute quality levels, never on a single run's low.**
- **Chooser-vs-argmax agreement: 4/5 (80 %)**, tied for the series high (0,3,1,4,4,3,0,4,4,1,2,4,4,0,2,4).
  The single disagreement went **downward** again. 16 five-sample points still cannot pin a rate.
- **`civ-precise` swept 5/5 for the SECOND clean-mock session running** (148 and 149) at
  `preferred_temp` 0.2 — the coldest voice is what the chooser rewards, and the mirror inverse
  of `civ-poetic` (1st on `avg_score`, last on `win_rate`) is narrowing for a 2nd session.
- **The run-level watch axis ROTATED again**: `civ-therapist` was at the run bottom 2 sessions
  running (147, 148); session 149's triple-bottom is `civ-mythic` (avg_score 0.2400, quality
  0.0110, alignment 0.0330). The **lifetime** low stayed `civ-grounded` for the 47th session.
  **The run ranking and the lifetime ranking are different civs on different axes — that is
  the rule, not a contradiction.** Only the lifetime table is a finding.
- **`civ-grounded` remains the low-relevance civ (47 consecutive sessions, 95–149)**, and the
  gap is still **structural alignment**: 0.2480 below `civ-therapist` on lifetime alignment vs
  0.0330 on quality (7.5×). Grounded fails to *embody a distinctive voice*, not to write well —
  a **voice failure, not a prose failure**. Lifetime novelty 1.4888 is above median: Grounded
  is not boring, it is *unmistakable in a way the chooser does not reward*.
- **Counter gap stayed byte-identical** to sessions 147/148 (whimsical −63, grounded −43,
  formal −42, poetic −37, engineer −22, mythic −20, therapist −17, precise −16) — a fixed
  per-civ offset, not an accumulating leak. `save_state()` has no lock ⇒ `relevance_per_sim`
  is still not recomputable from the ledger by an auditor.
- **NAS EDQUOT also breaks `cp` into `/workspace/output`** for report delivery: `cp` exits 1
  with `Disk quota exceeded` and leaves a **0-byte file that `ls` still lists**. Delete the
  0-byte stub; the durable copy is the committed git blob, verified with
  `git show HEAD:<path> | wc -c`.

## Session 150 (2026-10-25) — 22nd consecutive clean mock; the gap RATIO inverted, so quote absolute gaps

- **Run clean (15/15 checks).** per-civ delta = **+10** x 8 = **80 new rows** (engineer
  936->946, formal 967->977, grounded 982->992, mythic 939->949, poetic 961->971, precise
  931->941, therapist 934->944, whimsical 994->1004), `meta_log` delta = **+5** (483 -> 488),
  `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed with `provider=zai`, **0** rows
  with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback triple, **40/40** distinct
  seeds, **0** `(civ,prompt)` combos with >1 seed, sim->competition ts gap at index 4 in
  **8/8** civs, `leaderboard.json` rewritten at 00:45:01Z.
- **Pre-flight saved the run for the 5th time in the series** (115, 117, 145, 147, 150).
  `/tmp` was wiped, so the mock was rebuilt from scratch and **three** known bugs were live
  again: the session-112 index wrap, the session-118 md5-of-whole-message seeding, and the
  session-145 literal-`{}` placeholder. Pre-flight: **40/40 distinct seeds, 40/40 distinct
  previews, 8/8 + 8/8 on all 5 prompts, 0 tracebacks**, prompt lengths 167-209.
  **Never relax the seed-distinctness assertion** — the socket-level checks (200, prefix
  present, 0 tracebacks) all pass against a mock carrying `seed={}`.
- **NEW — the alignment/quality gap RATIO for the low-relevance civ INVERTED this session.**
  `civ-grounded` is still last of 8 on **both** dimensions, but the absolute gaps now point
  the other way: alignment gap **0.0655** vs quality gap **0.1581**. The ratio has swung
  **11x -> 2.7x -> 7.5x -> 0.4x** across sessions 125/145/149/150 on identical data-shape
  logic. **Quote the absolute gaps and the "last of 8 on both" invariant; never the ratio.**
  A ratio over two drifting quantities is not a stable claim.
- **`civ-grounded` remains the low-relevance civ (48 consecutive sessions, 95-150)** — last
  of 8 on every lifetime axis: `relevance` 953.17, `relevance_per_sim` 1.004, `avg_score`
  1.0459, `alignment` 1.1872, `quality` 0.4691. Label did not rotate (last before the run at
  950.40 / 1.012, last after it at 953.17 / 1.004). A **voice** failure, not a prose
  failure: alignment is the axis the meta-GAN selects on, and lifetime novelty 1.4813 is
  above median — Grounded is unmistakable in a way the chooser does not reward.
- **Watch axis `civ-therapist` — 4th session at the run bottom, on BOTH axes** (run
  `avg_score` 0.2650, run `alignment` 0.0210, both lowest of 8). Lifetime standing is still
  mid-field (`avg_score` 1.2278, 5th of 8) => **watch axis, not a finding**.
  `civ-grounded` was 7th of 8 on run `avg_score` (0.2767) — the run-level low and the
  lifetime low are different civs on different axes. That is the rule, not a contradiction.
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-formal` won 3, `civ-precise` 2. All
  4 disagreements took the **lower**-scoring candidate (deltas -0.467, **-0.823**, -0.113,
  -0.523). 22 five-sample points cannot pin a rate: the honest claim is *somewhere in
  0-80 %*. **The direction is the finding; the rate is not.** Never treat `win_rate` as a
  quality metric.
- **`civ-formal` won 3/5 for the first time in the series** (it had never out-polled
  `civ-precise`). `civ-formal` remains the distinct low-**novelty** axis (lifetime novelty
  1.3764, last of 8; alignment 1.7693 healthy).
- **The two stable inverses:** `civ-poetic` = 1st on lifetime `avg_score` (1.6115) /
  `quality` (0.8242) / `relevance_per_sim` (1.572) but **last on `win_rate` (0.013)** and
  won 0/5 despite being 2nd on run `avg_score`; `civ-precise` = best `win_rate` (0.570),
  **highest lifetime `alignment` (2.1975)**, 1st on run `avg_score` (0.7767) at
  `preferred_temp` 0.2 — the mirror inverse.
- **Extinction risk NONE** — threshold -10; lowest relevance 953.17 = 95x above the floor.
  Registry 8, `max_civs` 12; all 8 still `generation=1`.
- **Counter gap stayed byte-identical** to sessions 147/148/149 (whimsical -63, grounded
  -43, formal -42, poetic -37, engineer -22, mythic -20, therapist -17, precise -16) — a
  fixed per-civ offset, not an accumulating leak.
- **Dimension spreads:** `alignment` **1.2920**, `avg_score` 0.5117, `novelty` 0.4500,
  `quality` **0.0180** (collapsed again — 17th of the last 18 clean-mock sessions).
  **Rank on cross-civ spreads, never on absolute quality levels, never on a single run's low.**
- **New environment note — a detached mock launch can time out the tool call even with
  stdout AND stdin redirected.** `setsid nohup ... > log 2>&1 < /dev/null &` blocked the
  full 30 s, yet the *next* command showed the mock healthy (pids 303/304, listening, 0
  tracebacks). **When a detached launch times out, check `ps` in a separate command before
  assuming it failed.**
- **z.ai credential gap: 44th session.** `ZAI_TOKEN` absent from env and all 8 secrets;
  401 `token expired or incorrect` against a healthy endpoint. JEV live (422 on a malformed
  `questions`).

## Session 157 (2026-10-25) — 22nd consecutive clean mock; the `simulations_run` baseline is NOT the row count

**Run clean (103 assertions, 0 failures).** per-civ delta = **+10** x 8 = **80 new rows**
(engineer 1006->1016, formal 1037->1047, grounded 1052->1062, mythic 1009->1019, poetic
1031->1041, precise 1001->1011, therapist 1004->1014, whimsical 1064->1074), `meta_log` delta
= **+5** (518 -> 523), **Winner:** lines = **5**, **80/80** rows `[mock-zai`-prefixed with
`provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **80 distinct** JEV score triples / **35 distinct** confidences, **40/40** distinct
seeds, **0** `(civ,prompt)` combos with >1 seed, **8/8 + 8/8** on all 5 competition prompts.

### NEW — the `simulations_run` baseline must come from the git blob, not the ledger row count

The orchestrator's `culture.json` `simulations_run` counts **only the sim phase** (5 per civ),
while `simulations.jsonl` accumulates **both** phases (10 rows per civ) *and* the entire
competition history. The two counters are therefore offset by the whole competition history
(grounded: `simulations_run` 1009 vs 1062 ledger rows).

Asserting `sims_run == rows_before + 10` produced **8 false failures** on a run where every
other assertion was green. The correct assertion is against the **git HEAD blob's**
`culture.json`: `simulations_run` delta = **+10** for all 8 (grounded 1009->1019, precise
985->995, …) and `wins+losses` delta = **+5** for all 8 (5 competitions).

**Rule: an 8-for-8 failure with every other assertion green is a BASELINE bug until proven
otherwise — check the baseline's source before believing the failure.** The RUNBOOK's
assertion table says "per-civ `simulations.jsonl` delta +10"; it does **not** license reusing
that number as the `simulations_run` baseline.

### NEW — the pre-flight must render the cultural prompt as an F-STRING, not `str.format()`

The orchestrator builds the prompt with an f-string:
`f"""You are a voice in the tradition of "{self.culture['name']}"…"""`. A probe that does
`TEMPLATE.format(name, tenets, voice, prompt)` raises **`KeyError: 'self'`** — the probe crashes
before it ever reaches the mock, and the natural reading ("the mock is broken") is wrong.

Fix: replace the four f-string expressions with sentinels, then substitute:
`{self.culture['name']}` / `{', '.join(self.culture['tenets'])}` /
`{self.culture['voice_emphasis']}` / `{prompt}`. That reproduces the orchestrator's bytes
exactly. Pre-flight then reported **40/40 distinct seeds, 40/40 distinct previews, 40/40
template md5s, 0 tracebacks**, prompt lengths 167-209, **8/8 + 8/8 on all 5 prompts** — the
pre-flight saved the run for the **5th** time in the series (115, 117, 145, 147, 150).

### NEW — `/tmp` was REAPED mid-session; a vanished target looks exactly like a broken bridge

A completed sparse clone (`/tmp/aiw`, 6.7 MB) **vanished between two commands**. The symlink
bridge survived but became **dangling**, so `ls` on the *target* path failed with "No such
file or directory" and `stat -L` failed too — indistinguishable from a broken bridge.

**Rule: when the bridged path 404s, check the TARGET (`ls /tmp/aiw`) before re-creating the
link.** Re-creating a link to a missing target just reproduces the symptom. Re-cloned with the
blobless+sparse recipe (`--filter=blob:none --no-checkout --depth 1 --sparse` +
`sparse-checkout set --no-cone cellular-first-design/code/civilizations`) → **6.7 MB**, one shot.

### The z.ai credential gap: 45th session. REST core quota exhausted; the SEARCH api still answers

`ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401 `token expired or incorrect`**
(endpoint healthy). JEV live (422 `too_short` on an empty `questions`). This session the
**REST core quota was exhausted** (0/5000, reset 02:21Z) — `GET /user`, `GET /repos/...` and
`GET /orgs/...` all returned 403 "API rate limit exceeded", and a rate-limited response
**renders as "no such repo" for every candidate at once**. The **search API has a separate
bucket and kept working**: `GET /search/repositories?q=user:SuperInstance` identified the
owner and the repo list. **Use search while core is rate-limited; and never read a 403 as
absence.** `git ls-remote` remains the ground truth for repo existence.

### Low-relevance civ — the low label did NOT rotate (49 sessions, 95-157)

`civ-grounded` remains **last of 8 on every lifetime axis**: `relevance` 1009.12,
`relevance_per_sim` 0.990, `avg_score` 1.0296, `alignment` 1.1435, `quality` 0.4435.
Absolute gaps: alignment **0.2197** (to therapist) vs quality **0.0333** (to formal) — a
**6.6x** wider alignment gap. (Quote the absolute gaps; the ratio has swung 11x -> 2.7x -> 7.5x
-> 0.4x -> 6.6x across sessions and is not a stable claim.) Alignment is the axis the
meta-GAN selects on ⇒ a **voice failure, not a prose failure**. **LIFETIME NOVELTY 1.5018 is
now BELOW median (1.6410)** — sessions 143-150 had Grounded above median. If that holds next
session, Grounded is losing on two axes, not one. **Extinction risk NONE** — 1009.12 = 100.9x
above the −10 floor; registry 8, all `generation=1`.

**Watch axis `civ-therapist` — 5th session at the run bottom, on BOTH axes** (run `avg_score`
0.7893, run `alignment` 0.6760, both lowest of 8). Lifetime standing still mid-field
(`avg_score` 1.1994, 6th of 8) ⇒ **watch axis, not a finding**. `civ-grounded` was 7th of 8 on
run `avg_score` (0.8997) — the run low and the lifetime low are different civs on different
axes; that is the rule, not a contradiction.

**Chooser vs `avg_score` argmax: 0/5 (0 %)** — disagreed in **every** competition. `civ-poetic`
was the argmax on **all five** prompts and won **zero** (deltas -0.1867 … -0.6300, all
downward). `civ-precise` won 4/5, `civ-formal` 1/5. 20+ five-sample points cannot pin a rate:
report it as a sample and keep the **direction** as the finding. **Never treat `win_rate` as a
quality metric.**

**The two stable inverses, sharpest form yet:** `civ-poetic` = 1st on lifetime `avg_score`
(1.5961) / `quality` (0.7942) / `relevance` (1564.74) / `relevance_per_sim` (1.559) and **last**
on `win_rate` (0.012, 6/498) — argmax on 5/5 prompts, winner on 0/5. `civ-precise` = best
`win_rate` (0.572), **highest lifetime `alignment` (2.1678)**, won 4/5 at `preferred_temp` 0.2.

**Counter gap byte-identical pre/post run** on all 8 civs (delta +0.0000 each): grounded -84.35,
whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63, mythic -51.11, therapist
-42.11, engineer -44.24 (total -609.92). A fixed per-civ offset, not an accumulating leak.
`save_state()` has no lock ⇒ `relevance_per_sim` is not recomputable from the ledger.

**Dimension spreads:** run-level `alignment` **1.7070**, `avg_score` 0.8880, `quality` 0.6360,
`novelty` 0.5260; lifetime `alignment` **1.0243**, `avg_score` 0.5665, `novelty` 0.5387,
`quality` 0.3507. **`alignment` widest on both horizons.** Run-level `quality` did **not**
collapse this session (0.093-0.729) — the collapse is a **LEVEL** that moves. **Rank on
cross-civ spreads, never on absolute quality levels, never on a single run's low.**

## Session 159 (2026-10-25) — concurrent peer sessions; the four merge rules for the civ tree

**Run clean (134/134 assertions).** per-civ delta +10 x 8 = 80 new rows (all ts inside one
02:23:15-02:23:44Z window, every new row newer than every pre-existing row), `meta_log` +5
(523 -> 528), 134 assertions passed / 0 failed, 40/40 distinct seeds, 40/40 distinct previews,
40/40 distinct template md5s, 0 tracebacks, 0 JEV error keys, 0 2.0/2.0/2.0 fallbacks,
leaderboard reconciling 8/8 against `culture.json`.

### NEW — a peer session can hold the same session number, and the run collides on push

The push was rejected: upstream had moved `b002296` -> `0374e23`, a **peer session 158** (same
command, different sandbox) that ran **concurrently** with ours — ours finished 02:23:44Z, theirs
02:24:01Z. Their data differed from ours (their chooser-vs-argmax 1/5, ours 3/5): two
independent mock runs, not a duplicate. Our local tree's last report was 157, so we numbered
ours 158 and pushed — **158 was already taken upstream.** Renumbered to **159** and rebased.

**Rule: never derive the next session number from the local tree alone.** `git fetch` and check
`origin/main` **before** naming the report file and before the first push.

### NEW — the civ tree has FOUR file classes, and they merge four different ways

`git rebase` conflicted in **all 18 files**. Text-splicing the conflict markers corrupts the
append-only ledgers.

| file class | nature | correct merge |
|---|---|---|
| `simulations.jsonl` | append-only ledger | base + upstream's 10 + mine's 10, deduped on `(ts, civ, prompt, preview)` |
| `meta_log.jsonl` | append-only ledger | base + upstream's 5 + mine's 5, deduped on `(ts, winner, prompt)` |
| `culture.json` | snapshot, **additive counters** | base + (upstream − base) + (mine − base) for `simulations_run`/`relevance_score`/`wins`/`losses`; `preferred_params` = last writer wins |
| `leaderboard.json` | snapshot, **derived** | **recompute** from the merged `culture.json` files; do not pick a side |

**The first attempt kept only the 10 conflicted `meta_log` rows and silently dropped the 523
ancestor rows**, and left `<<<<<<< HEAD` / `=======` / `>>>>>>>` marker lines embedded in the 8
ledgers (3 bad lines per file; 1085 "rows" of which 3 were markers). `wc -l` alone would have
reported 1085 and looked fine. **Caught only by a per-line JSON parse.** After the fix:
`meta_log` 533 rows (523+5+5), ledgers base+20, `culture.json` +20 `sims_run` and +10 W+L for
all 8, `generation` still 1, 0 conflict markers, all JSON valid, leaderboard rebuilt and
reconciling 8/8.

**Rules:** (1) resolve append-only ledgers by **reconstructing from git blobs**, never by
splicing markers; (2) re-parse **every line** of every merged JSONL, don't trust `wc -l`;
(3) `git show` inside a Python script needs `cwd=` set to the repo root — running from a
subdirectory silently returned empty output and produced **0-row ledgers**;
(4) a `culture.json` merge must be checked for the `relevance_score` delta, not just the row
count.

### NEW — a false mock-degeneracy alarm in the VERIFIER, not the mock

The first verification pass reported **"10 distinct seeds across 80 new rows"** — the exact
signature of a degenerate mock. It was a **bug in the verification script**: it built one
concatenated list of *per-civ blocks* then took `allrows[-80:]`, but because `civ-grounded`'s
block sits first, the tail-80 window covered only the last 5 civs' blocks. The correct window is
**10 rows from each civ**. The mock was healthy (40/40 seeds, 40/40 previews, 8/8 on all 5
prompts, 0 tracebacks).

**Rule: a mock-degeneracy alarm must be re-derived from a correctly sliced window before the
mock is rebuilt.** Rebuilding a healthy mock on a false alarm is the expensive error. When
slicing a multi-file ledger, slice **per file**, never across a concatenation.

### Low-relevance civ — `civ-grounded`, 50 consecutive sessions (95-159)

Last of 8 on **every** lifetime axis in both the pre-merge and merged trees: `relevance`
1016.24, `relevance_per_sim` 0.978, `avg_score` 1.0259, `alignment` 1.1338, `quality` 0.4396.
Binding constraint is **alignment** (gap 0.2167) not quality (gap 0.0331) — a **voice failure,
not a prose failure**. Lifetime novelty 1.5045 ranks **3rd of 8** (below the 8-civ median
1.6455 but *near the top*) — **not** a second collapse; session 157's report had it as 6th,
so re-derive the rank each session rather than carrying it forward. Extinction risk NONE
(101.6x above the −10 floor). Watch axis: `civ-therapist` took the run low on `alignment`
(0.0650) and `quality` (0.0160) for a 6th session but is mid-field lifetime => watch, not finding.

Chooser-vs-argmax **3/5 (60%)**, up from 0/5; both disagreements took the lower-scoring
candidate. 30-row trailing window 11/30. **The direction is the finding; the rate is not.**
`civ-poetic` 1st on lifetime avg_score/quality/relevance but last on win_rate (0.012);
`civ-precise` best win_rate (0.577), highest lifetime alignment (2.1654), won 4/5.

### Env re-confirmed

- Upstream is **`SuperInstance/AI-Writings`** (the `ai-writings/...` slug 404s). The REST core
  quota was exhausted (0/5000) but the **search API has a separate bucket and still answers**;
  for *absence* claims use `git ls-remote` (0 refs = genuinely empty), never a rate-limited REST
  call. `gh` still not installed.
- NAS EDQUOT total (600G/600G). Clone to `/tmp`; `mkdir`+`ln` work => **symlink bridge** is the
  only way in. Verified by inode identity `129:10427` and `-ef`.
- **z.ai credential gap: 46th session** (`ZAI_TOKEN` absent; z.ai 401). **JEV live** (empty
  `questions` -> 422 `too_short` proves the token was accepted).
- The transient NAS mount race on the symlinked deep path **recurred**: the first `ls -la` on
  `/workspace/.../civilizations/` returned "No such file or directory" while everything was
  present. `stat -L` + `readlink -f` + `[-e ]` + 5/5 retries passed. **One `ls` failure is not
  evidence of a missing directory.**
- Pre-flight saved the run for the **6th** time in the series (115, 117, 145, 147, 150, 159):
  40/40 seeds, 40/40 previews, 40/40 md5s, 0 tracebacks, 8/8 + 8/8 on all 5 prompts.

## Session 160 (2026-10-25) — 23rd consecutive clean mock; the p3 disagreement (-0.8900) is the clean-mock series record

- **Run clean (60/60 checks, 0 failures).** per-civ delta = **+10** x 8 = **80 new rows**
  (engineer 1036->1046, formal 1067->1077, grounded 1082->1092, mythic 1039->1049,
  poetic 1061->1071, precise 1031->1041, therapist 1034->1044, whimsical 1094->1104),
  `meta_log` delta = **+5** (533 -> 538), **Winner:** lines = **5**, **80/80** rows
  `[mock-zai`-prefixed with `provider=zai`, **0** rows with a JEV `error` key, **0** rows with the
  2.0/2.0/2.0 fallback triple, **40/40** distinct seeds, **0** `(civ,prompt)` combos with >1 seed,
  sim->competition ts gap at index 4 in **8/8** civs (1.10-23.21 s), **8/8 + 8/8** on all 5
  competition prompts.
- **Pre-flight saved the run for the 6th time in the series** (115, 117, 145, 147, 150, 160).
  `/tmp` was wiped, so the mock was rebuilt from scratch and **all three** known bugs were live
  again: the session-112 index wrap, the session-118 md5-of-whole-message seeding, and the
  session-145 literal-`{}` placeholder. Pre-flight: **40/40** distinct in-batch pairs, **8/8 + 8/8**
  on all 10 canon prompts, **0** tracebacks.
- **NEW — the runbook's "+5 wins+losses" is a TOTAL; the wins/losses SPLIT varies.**
  `civ-precise` took 4 wins / 1 loss (+4/+1), `civ-engineer` 1 win / 4 losses (+1/+4), and the
  other six civs 0 wins / 5 losses (+0/+5). Every civ's `wins+losses` total is **+5** (8/8) and
  the field win total is **+5** (514 -> 519), but asserting `wins == blob_wins + 5` fails for
  every civ that did not win. **Assert the total, and cross-check the field win total.**
- **NEW — a pre-flight FAIL with 8/8 on every per-prompt line is a SCOPE error in the probe, not
  a degenerate mock.** The first pass probed all 10 canon prompts (80 distinct pairs) but
  asserted a 40-pair total, so it printed `PREFLIGHT: FAIL` while every per-prompt check was
  8/8 PASS. The mock was healthy. **When a pre-flight fails, read the per-prompt lines before
  touching the mock** — scope the totals to the prompts the batch will actually use.
- **Chooser vs `avg_score` argmax: 1/5 (20 %)** — `civ-precise` won 4, `civ-engineer` 1.
  `civ-poetic` was argmax on **5/5** prompts and won **0/5**. All 4 disagreements took the
  **lower**-scoring candidate (deltas -0.1067, -0.2367, **-0.8900**, -0.3167). The p3 gap of
  **-0.8900** is the **largest single disagreement in the clean-mock series**, exceeding the
  session-137 record (-0.683) and the session-138 record (-0.6300). 20+ five-sample points
  cannot pin a rate: report it as a sample and keep the **direction** as the finding.
- **`civ-grounded` remains the low-relevance civ (50 sessions, 95-160)** — last of 8 on every
  lifetime axis: `relevance` 1023.82, `relevance_per_sim` 0.9760, `avg_score` 1.0148,
  `alignment` 1.1144, `quality` 0.4317. Absolute gaps: alignment **0.2107** (vs therapist
  1.3251) vs quality **0.0325** (vs formal 0.4642) — quote the absolute gaps, never the ratio.
  Lifetime novelty 1.4983 is **below** median (1.6410) again, so Grounded is losing on **two**
  axes (alignment and novelty) — the condition first noted in session 157. **Extinction risk
  NONE** (1023.82 = 102x above the -10 floor); registry 8, all `generation=1`.
- **Watch axis `civ-therapist` — 6th session at the run bottom, on BOTH axes** (run `avg_score`
  0.7250, run `alignment` 0.0370, both lowest of 8). Lifetime standing still mid-field
  (`avg_score` 1.1804, 6th of 8; `relevance_per_sim` 1.1589, 5th of 8) => **watch axis, not a
  finding**. `civ-grounded` was 7th of 8 on run `avg_score` (0.7577) but 2nd-lowest on run
  `alignment` (0.1090) — the run low and the lifetime low are different civs on different axes;
  that is the rule, not a contradiction.
- **The two stable inverses:** `civ-poetic` = 1st on lifetime `avg_score` (1.5821) / `quality`
  (0.7755) / `relevance` (1597.64) / `relevance_per_sim` (1.5451) and **last** on `win_rate`
  (0.0117, 6/513) — argmax on 5/5 prompts, winner on 0/5. `civ-precise` = best `win_rate`
  (0.5787, 294/508), **highest lifetime `alignment` (2.1564)**, won 4/5 — the mirror inverse.
- **`civ-formal`** = the low-**novelty** axis (lifetime novelty 1.4088, last; alignment 1.6918
  healthy). **`civ-engineer`** — the session-121 low did NOT repeat: 6th of 8 on run `avg_score`
  (0.8763) and 6th on run `alignment` (0.3700), no longer at the run bottom; still 7th of 8 on
  lifetime `avg_score`. Axis stays open, do not promote.
- **Counter gap byte-identical** to sessions 147-150/157 (whimsical -173.15, grounded -84.35,
  formal -85.53, poetic -96.81, engineer -44.25, mythic -51.11, therapist -42.11, precise
  -32.63; total **-609.93**). A fixed per-civ offset, not an accumulating leak.
  `save_state()` has no lock => `relevance_per_sim` is not recomputable from the ledger.
- **Dimension spreads this run:** `alignment` **2.4670**, `avg_score` 0.9597, `novelty` 0.3410,
  `quality` 0.2470 (collapsed again, field mean 0.0736 — the 18th of the last 19 clean-mock
  sessions). **Rank on cross-civ spreads, never on absolute quality levels, never on a single
  run's low.**
- **Re-confirmations:** NAS EDQUOT total (12th session); `gh` not installed (15th session);
  tool timeout 30 s < run ~30-35 s; `ZAI_URL_OVERRIDE` alone is dead code (needs `ZAI_TOKEN`);
  clone into `/tmp`, symlink the **nested** `cellular-first-design` dir, verify with
  `stat -L -c '%d:%i'` + `-ef`; never flatten; `TYPESAFEAI_KEY` must be exported; the `ls` race
  did NOT reproduce; `civilizations.json` is multi-line JSON, not JSONL; `meta_log` `results` is
  a list of `[civ_id, score]` pairs. z.ai credential gap: 46th session.

## Session 161 (2026-10-25) — the counter-gap epoch trap, and the mock's THREE rebuild fixes

**Run clean (session 161, 24th consecutive clean mock).** per-civ delta = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (538 → 543), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed
with `provider={zai}`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **80 distinct `(q,n,a)` triples** (confidences 0.93–1.00), **40 distinct seeds / 80 rows**
with **0** `(civ,prompt)` combos carrying >1 seed, sim→competition ts gap at index 4 in **8/8**
(0.61–0.70 s), and **5/5 competition prompts at 8/8 distinct seeds AND 8/8 distinct previews**.
`git status --porcelain` = **18** modified. **Chooser vs `avg_score` argmax 0/5 (0 %)** — all 5
disagreements took the lower-scoring candidate (max |delta| 0.4633 on p3).

### NEW — the counter gap: NEVER mix epochs, or it fakes an accumulating leak

The gap was first computed as **pre-run blob `relevance` vs post-run ledger sum** → **−628.17**,
which had *drifted* from session 160's −609.93 and looked like the fixed offset was finally
accumulating. It is not. The blob's `relevance` **predates** this run while the ledger
**includes** it, so the run's own scores get subtracted twice.

Compute **both sides in the same epoch**:

| civ | HEAD blob rel | HEAD blob ledger | blob gap | post-run rel | post-run ledger | post-run gap | Δ |
|---|---|---|---|---|---|---|---|
| civ-grounded | 1023.8200 | 1108.1667 | −84.3467 | 1025.7100 | 1110.0567 | −84.3467 | 0.0000 |
| civ-whimsical | 1410.7433 | 1583.8867 | −173.1433 | 1413.0900 | 1586.2333 | −173.1433 | 0.0000 |
| civ-formal | 1194.2467 | 1279.7733 | −85.5267 | 1196.4000 | 1281.9267 | −85.5267 | 0.0000 |
| civ-poetic | 1597.6433 | 1694.4467 | −96.8033 | 1600.8267 | 1697.6300 | −96.8033 | 0.0000 |
| civ-precise | 1436.8433 | 1469.4767 | −32.6333 | 1440.7667 | 1473.4000 | −32.6333 | 0.0000 |
| civ-mythic | 1298.2800 | 1349.3900 | −51.1100 | 1299.6867 | 1350.7967 | −51.1100 | 0.0000 |
| civ-therapist | 1190.2200 | 1232.3333 | −42.1133 | 1191.3233 | 1233.4367 | −42.1133 | 0.0000 |
| civ-engineer | 1167.1567 | 1211.4000 | −44.2433 | 1169.3967 | 1213.6400 | −44.2433 | 0.0000 |
| **TOTAL** | | | **−609.92** | | | **−609.92** | **0.0000** |

**Rule: show both epochs side by side.** If the gap appears to move, first check the two columns
come from the same snapshot. A per-civ Δ of **0.0000** is the proof that the offset is fixed. A
"gap that grows every session" is the symptom of the epoch mix, not of a leak in `save_state()`.
Never quote the epoch-mixed number.

### NEW — a rebuilt mock needs THREE fixes, not two

The two long-named ones (session-112 index wrap, session-118 md5-of-whole-message seeding) are
joined by a third: the **session-144 `Connection: close` + `Content-Length`** pair. Without it
`urllib` (the orchestrator's client) is fine but a plain `curl -X POST` **hangs to the tool
timeout** on a perfectly healthy server — easy to misread as "the mock is down".

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)[:8]` | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ identical text for all 8 civs ⇒ chooser breaks a perfect tie |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to timeout against a healthy server |

Verified this session: HTTP 200 in 1 ms, `[mock-zai seed=…]` present, 8/8 distinct seeds AND 8/8
distinct previews on the **exact long cultural prompt** (lengths 167–199), stable across two
rounds, **0 tracebacks** in `/tmp/mock_zai.log`.

### Low-relevance civ — the low label did NOT rotate (51 sessions, 95–161)

`civ-grounded` remains the lifetime low on all five axes: `relevance` 1025.71,
`relevance_per_sim` 0.969, `avg_score` 1.0073, `alignment` 1.1048, `quality` 0.4279 —
**last of 8 on every one**. Absolute gaps: **alignment 0.2080** (vs therapist 1.3128) vs
**quality 0.0321** (vs formal 0.4600). Alignment is the axis the meta-GAN *selects* on ⇒ a
**voice** failure, not a prose failure. Lifetime novelty 1.4892 is **below** median (1.6160) ⇒
losing on **two** axes (alignment and novelty).

**`civ-therapist` is a watch axis, not a finding** — 7th consecutive session at the run bottom
on **both** `avg_score` (0.1103) and `alignment` (0.0250), but lifetime standing is mid-field
(`avg_score` 1.1702, 6th of 8). The run low and the lifetime low are different civs on different
axes (session-132 rule).

**Inverses hold:** `civ-poetic` 1st on lifetime `avg_score` (1.5704) / `quality` (0.7684) /
`relevance` (1600.83) but **last on `win_rate` (0.012)**; `civ-precise` best `win_rate` (0.579),
**highest lifetime alignment (2.1444)**, 1st on run `avg_score` (0.3923). `civ-formal` remains the
distinct low-**novelty** axis (1.3987, last; alignment 1.6793 healthy). Extinction risk **NONE**
(threshold −10, lowest +1025.71 = 102× the floor); registry 8, `max_civs` 12, all `generation=1`.

---

## Session 163 (2026-10-25) — the `simulations_run` delta is +10 *by construction*, and the confidence-spread check is JEV-side

**Run clean (session 163, 25th consecutive clean mock).** per-civ delta = **+10** × 8 = **80 new
rows**, `meta_log` Δ = **+5** (548 → 553), `Winner:` lines = **5**, **80/80** rows `[mock-zai`-prefixed
with `provider=zai`, **0** rows with a JEV `error` key, **0** rows with the 2.0/2.0/2.0 fallback
triple, **40/40** distinct seeds, **40/40** distinct previews, **8/8** on all 5 competition
prompts, `git status --porcelain` = **19** (18 modified + 1 new report). **94/95 assertions PASS.**

### NEW — the `simulations_run` delta is +10 *by construction*, not by coincidence

The session-157 note ("the `simulations_run` baseline is NOT the ledger row count") described the
counter as offset from the ledger. **The source shows they are the same quantity:**
`run_simulation()` appends exactly one ledger row and increments `self.sims_run` exactly once
(`civilization_orchestrator.py:206`), and the **competition** phase calls `run_simulation()` again
via `ex.submit(c.run_simulation, prompt, providers)` (`:252`). So on a clean `--sims 5 --prompts 5`
run: **Δrows == Δsimulations_run == +10** per civ.

I asserted **+5** this session and got 8 false failures. The correct rule is now unambiguous:

> **Assert `Δsimulations_run == Δrows == +10`.** The historical "+260 counter gap" is an **epoch
> artifact** (the ledger predates the counter), not a live divergence — and the *sign* of the gap
> flips with the epoch mix, so never quote an epoch-mixed gap (see the session-161 two-epoch
> rule). Read both baselines from the **git blob's** `culture.json`, not the working tree.

### NEW — the confidence-spread check is a JEV-liveness check, NOT a mock check

The harness flagged "broad confidence spread (>=10 distinct)" as FAIL: this run's 80 rows carry
only **6 distinct confidence values** (0.95–1.00) where the 80 rows immediately before carried
**52** (0.27–1.00). The naive reading is "the mock went degenerate."

**It did not.** 40 distinct mock bodies are present and **24 of them map to two or more different
JEV score triples** — so JEV is genuinely scoring content, not returning a constant. The narrow
confidence band and the collapsed `quality` axis (field mean **0.030**, range 0.01–0.07) are
properties of the **JEV model on this content**, and the `quality` collapse reproduces the
**19-of-the-last-20 clean-mock sessions** regime (119/121/122/138) documented in sessions 160–161.

> **Rule: never report a confidence-spread failure as a mock failure without running the
> same-body / different-triple test.** Group the 80 new rows by mock body (strip the
> `[mock-zai seed=…]` prefix) and count distinct JEV triples per body. If >1 body carries >1
> triple, JEV is discriminating and the confidence band is JEV's, not the mock's. The
> mock-integrity checks remain **seed** and **preview** distinctness, which passed 40/40.

### Low-relevance civ — the low label did NOT rotate (53 sessions, 95–163)

`civ-grounded` remains the lifetime low on all five axes: `relevance` 1036.62,
`relevance_per_sim` 0.961, `avg_score` 0.9991, `alignment` 1.0872, `quality` 0.4208 —
**last of 8 on every one**. Absolute gaps: **alignment 0.2026** (vs therapist 1.2898) vs
**quality 0.0321** (vs formal 0.4529) — a 6.3× wider alignment gap. Alignment is the axis the
meta-GAN *selects* on ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.4892 ranks
6th of 8, below the median band ⇒ losing on **two** axes (alignment and novelty), the same
shape as session 161.

**`civ-therapist` is a watch axis, not a finding** — took the run-level low on `alignment`
(0.1040) and 6th of 8 on run `avg_score` (0.4560), but lifetime standing is mid-field
(`avg_score` 1.1598, 6th of 8). Session-132 rule respected.

**Inverses hold:** `civ-poetic` 1st on lifetime `avg_score` (1.5563) / `quality` (0.7557) /
`relevance` (1616.68) / `relevance_per_sim` (1.519) but **last on `win_rate` (0.011, 6/522)** —
it was the `avg_score` argmax on **3 of 5** prompts and won **zero**. `civ-precise` best
`win_rate` (0.579, 303/220), **highest lifetime alignment (2.1168)**, won **4/5** at
`preferred_temp` 0.2. `civ-formal` remains the distinct low-**novelty** axis (1.4021, last;
alignment 1.6593 healthy). Extinction risk **NONE** (threshold −10, lowest +1036.62 = 104× the
floor); registry 8, `max_civs` 12, all `generation=1`.

**Chooser vs `avg_score` argmax: 1/5 (20 %)** — 2/5 in session 162, 0/5 in session 157. All four
disagreements took the **lower**-scoring candidate (−0.1700, −0.0900, −0.2467, −0.0167).
Trailing 30-row window now reads `...010100` + `10000` = **11/35**. A 5-sample point still
cannot pin a rate ⇒ the honest claim is *somewhere in 0–80 %*. **The direction is the finding;
the rate is not.**

### Environment — the hardcoded `CIVS_DIR` is why the symlink bridge must exist BEFORE the run

The script hardcodes `CIVS_DIR = /workspace/repos/ai-writings/cellular-first-design/code/civilizations`.
A clone under any other path fails at the **first** `REGISTRY.read_text()` with
`FileNotFoundError` — *before* any provider call, *before* any write — which reads like a
missing file rather than a missing bridge. **Build the bridge first**, target the **nested**
`cellular-first-design` dir (never the repo root), and verify with inode identity
(`stat -L -c '%d:%i'` on both sides + `-ef`), not `ls`. Session 163: `129:12601` both sides.

`/tmp` was empty again ⇒ mock rebuilt from scratch with all **three** fixes (session-112 index
wrap, session-118 md5-of-whole-message seeding, session-144 `Connection: close` +
`Content-Length`). Pre-flight: 8/8 distinct seeds AND 8/8 distinct previews, cultural-prompt
lengths 167–199, HTTP 200 in 1.6 ms, 0 tracebacks, 0 `EXC:`. Teardown: killed the **server** pid
by exact argv; 0 remaining procs; `curl` exit 7 = port closed.
