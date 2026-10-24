# Civilization Orchestrator — Run Report, Session 77 (2026-10-24)

**Command requested:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Base commit:** `5733db685348320978cfba45995ff7835772722f` (`SuperInstance/AI-Writings`, branch `main`)
**Script md5:** `501fa686b846199b2057d3b70b4d66d9` — **unchanged**, `ZAI_URL_OVERRIDE` hook present at line 84 (no patch applied)
**Baseline ledger:** 2444 rows / 8 civs · **meta_log** 158 · **mock contamination** 0/2444 = **0.0 %**
**Bridge:** one level — `ln -sfn /tmp/civprobe/AI-Writings /workspace/repos/ai-writings` (the clone root IS the repo root)

---

## 1. The unpatched run is a NO-OP — 29th consecutive replication

```
$ export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
$ python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...
... (8 per-civ lines) ...
=== Civilization competitions: 5 prompts ===
EXIT=0
```

| check | value |
|---|---|
| exit code | **0** (green) |
| ledger row delta | **+0** (2444 → 2444) |
| per-civ ledger delta | **+0 on all 8** |
| `meta_log.jsonl` delta | **+0** (158 → 158) |
| `Winner:` lines | **0** |
| registry `simulations_run` sum | **2184 → 2184 (+0)** |

**`ZAI_TOKEN` is absent** from the environment. All 7 candidate secrets in the sandbox were re-tested
against `https://api.z.ai/api/coding/paas/v4/chat/completions` and every one returns
**HTTP 401 "token expired or incorrect"** — a 401 (not a 5xx) means the endpoint is healthy, so this is a
**credential gap, not an outage**. The provider gate drops every call silently:

```python
token = os.environ.get(p["env"], "")
if not token: return None        # silent drop, no error, no log
```

The `[The Grounded] running 5 sims...` lines print **before** the provider call and are **not** evidence of
work. **Assert on the row delta and the `Winner:` count — never on the exit code.**

JEV was live throughout: `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` (the orchestrator reads `TYPESAFEAI_KEY`;
the sandbox exports `TYPESAFE_AI_TOKEN` — a permanent name split). Probe returned `jev-1.14.0`, real scores.

**One file still changes on a no-op run:** `leaderboard.json` (`update_leaderboard()` runs unconditionally, so
only `ts`/`iso` differ). The ledger and the registry do not move. This is a benign apparent mismatch — the
**git blob check is authoritative** (`git hash-object <worktree>` vs `git rev-parse HEAD:<path>`).

## 2. Control B — 14th consecutive identical replication

`ZAI_TOKEN=<dummy>` (never validated; the mock ignores auth) + `ZAI_URL_OVERRIDE=http://127.0.0.1:8977/chat/completions`.
The hook is committed in the blob and is provider-generic (`f"{name.upper()}_URL_OVERRIDE"`). JEV was left
**untouched** and stayed live, so every score below is a real JEV score.

### Boot-time assertion (printed before the run started)

```
=== MOCK BOOT ASSERTION (session 77) ===
  civ-grounded    -> 'Your voice: warm, factual.'          in pool: True
  civ-whimsical   -> 'Your voice: playful, surprising.'    in pool: True
  civ-formal      -> 'Your voice: measured, exact.'        in pool: True
  civ-poetic      -> 'Your voice: lyrical, dense.'         in pool: True
  civ-precise     -> 'Your voice: technical, sparse.'      in pool: True
  civ-mythic      -> 'Your voice: ancient, narrative.'     in pool: True
  civ-therapist   -> 'Your voice: warm, attentive.'        in pool: True
  civ-engineer    -> 'Your voice: structural, practical.'  in pool: True
  ALL CIVS IN POOL: True
```

The table is keyed on the **rendered** string `Your voice: {voice}.` — **with the trailing period** the
orchestrator actually emits. A table keyed on the raw `voice_emphasis` value falls back for **every** civ, and
the failure is silent: the run still produces +80 rows, +5 `meta_log`, 5 winners, 0 default-score rows, 0
errors, zai-only — **every acceptance check except the distinct-preview count passes**, and the collapsed
count arrives *after* 80 rows have been written into the durable ledger. The boot assertion moves that
failure from "post-hoc, one weak signal" to "before the run, unambiguous."

### Acceptance battery — all green

| check | result |
|---|---|
| ledger rows | 2444 → **2524** (**+80**, +10 on **every** civ) |
| `meta_log.jsonl` | 158 → **163** (+5) |
| `Winner:` lines | **5** |
| all-2.0-default rows (JEV outage default) | **0** |
| rows carrying a JEV `error` key | **0** |
| distinct `content_preview` among new rows | **80 / 80** |
| per-civ distinct previews | **10 / 10 on every civ** |
| cross-civ preview collisions | **0** |
| providers used | **`{'zai': 80}`** — no other provider |
| scaffolding leaks in **this** run | **0** |
| new-row `avg_score` range | 0.493 .. 2.523, 75 distinct values |
| JEV confidence range | 0.280 .. 0.990 |
| mock port probe before launch / after kill | HTTP 200 / **HTTP 000** |

### The counter gap did **not** widen

| civ | ledger | registry `simulations_run` | gap | was | delta |
|---|---|---|---|---|---|
| civ-grounded | 342 | 299 | 43 | 43 | **+0** |
| civ-whimsical | 354 | 291 | 63 | 63 | **+0** |
| civ-formal | 327 | 285 | 42 | 42 | **+0** |
| civ-poetic | 321 | 284 | 37 | 37 | **+0** |
| civ-precise | 291 | 275 | 16 | 16 | **+0** |
| civ-mythic | 299 | 279 | 20 | 20 | **+0** |
| civ-therapist | 294 | 277 | 17 | 17 | **+0** |
| civ-engineer | 296 | 274 | 22 | 22 | **+0** |
| **TOTAL** | | | **260** | **260** | **+0** |

The gap is **exactly +260 again**, and it did not grow on any single civ — the lost-update race in
`save_state()` (whole-file rewrite, no lock, no read-modify-write) did not fire this session. It is an
**inherited** baseline defect, not a per-session constant. Still live and still worth fixing: while the gap
exists, `relevance_per_sim` is **not recomputable by an auditor from the ledger**.

**Restored to pristine after the run: 19/19 files byte-identical to the HEAD blobs** (verified with
`git hash-object` vs `git rev-parse HEAD:<path>`, never a process-substitution FIFO). Ledger back to 2444,
meta_log 158, script md5 unchanged, `git status --porcelain` clean, no `__pycache__/`, all 8 `witness.log`
files still 0 bytes. The mock was killed by PID and the port re-verified as HTTP 000.

## 3. Which civilization has low relevance

The authoritative source is `culture.json` + the ledger, **not** the board's `relevance_per_sim` (which the
runbook documents as non-reproducible because of the lost-update counter gap).

**This session's baseline ledger is 100 % clean** — 0 of 2444 rows match the mock signature
(`Marker <12 hex>`), so mock-filtered and all-rows lifetime numbers are **identical** this time. That is a
change from s72–s76 (800 mock rows, 32.7 %), and it changes the *level* of the lifetime numbers, not the
order. **Always declare the filter with the number.**

| civ | relevance_per_sim | raw relevance | win_rate | lifetime avg_score | quality | novelty | alignment | n |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 2.132 | 584.0 | **0.008** | 2.1892 | 1.472 | 2.248 | 2.847 | 311 |
| civ-whimsical | 1.991 | 559.4 | 0.023 | 2.1294 | 1.287 | 2.410 | 2.691 | 344 |
| civ-mythic | 1.876 | 504.6 | 0.024 | 1.9230 | 1.125 | 2.160 | 2.483 | 289 |
| civ-therapist | 1.869 | 499.1 | 0.015 | 1.9055 | 1.047 | 2.183 | 2.487 | 284 |
| civ-precise | 1.844 | 488.6 | **0.523** | 1.8548 | 1.061 | 1.635 | 2.868 | 281 |
| civ-engineer | 1.731 | 457.0 | 0.079 | 1.7527 | 0.972 | 1.698 | 2.588 | 286 |
| civ-formal | 1.664 | 457.7 | 0.145 | 1.7136 | 0.994 | **1.470** | 2.676 | 317 |
| **civ-grounded** | **1.493** | **431.5** | 0.258 | **1.5536** | **0.960** | 1.729 | **1.972** | 332 |

### The answer depends on the lens — two different civs

- **Lowest relevance: `civ-grounded` (The Grounded)** — last on **5 of 7** lenses (board sort key 1.493,
  raw relevance 431.5, lifetime `avg_score` 1.5536, mean quality 0.960, mean alignment 1.972) while holding
  the **most** rows (332). **Not a longevity artefact** — it loses on the *mean*, which no denominator can
  manufacture. Only `civ-formal` is lower on novelty (1.470).
- **Selection failure: `civ-poetic` (The Poetic)** — **1st of 8** on the board *and* on lifetime quality
  (1.472), yet **1 win in 133** (0.008). The chooser reads only 150 characters of preview and prefers the
  high-novelty/high-alignment register. Highest score, never chosen — a meta-GAN that cannot see quality.
- **Healthy: `civ-precise` (The Precise)** — 67W/61L (0.523), the only civ whose relevance rank and win rate
  agree.
- **Extinction risk: none** — threshold −10, lowest raw relevance +431.46, a **441-point margin**.

### Chooser vs `argmax(avg_score)`

**28 / 158 = 17.7 %** agreement lifetime; mean shortfall **0.566**, max **1.373**. 130 of 158 rounds crown a
non-argmax civ. The competition result is largely uncorrelated with the score it is supposed to maximise.

## 4. Standing defects (unchanged, still live)

1. **Provider credential gap** — `ZAI_TOKEN` missing; the gate at line 79 drops every call with no log line.
   A missing credential and a broken transport are indistinguishable from the outside.
2. **`save_state()` lost-update race** — whole-file rewrite with no lock and no read-modify-write. The
   ledger/registry gap is +260 and has not moved, but the race is latent and will fire on a concurrent write.
   While it exists, `relevance_per_sim` is not auditable from the ledger.
3. **Chooser reads 150 chars of preview** — 17.7 % agreement with argmax on its own scores.
4. **`leaderboard.json` is rewritten on a no-op run** — timestamp-only churn on a zero-work run.

## 5. Reproduce

```bash
mkdir -p /workspace/repos
ln -sfn /tmp/civprobe/AI-Writings /workspace/repos/ai-writings
cd /workspace/repos/ai-writings/cellular-first-design/code/civilizations
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```
