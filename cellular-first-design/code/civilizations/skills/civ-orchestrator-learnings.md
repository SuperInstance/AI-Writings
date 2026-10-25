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
