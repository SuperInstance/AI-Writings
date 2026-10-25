# Civ Orchestrator — Run Report, session 234 (2026-10-25)

## Session 234 (2026-10-25) — provider path, baseline, and result

- Provider path: **Control B mock** (z.ai credential gap, **97th session**) + **live JEV**
  (`jev-1.14.0`; empty-questions probe returns **422 `too_short`** => token accepted).
- Baseline: `f6f3609` (session 233 tree), `refs/heads/main` asserted equal to the clone HEAD
  (`f6f36096c4264104d167e60bdc71f08bdad37044`).
- Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
- **Pre-flight gate: 8/8 PASS** (first build). **Run verification: 18/18 PASS.**
- Result: `civ-precise` swept **5/5** competitions; chooser/argmax agreement **2/5 (40 %)** —
  3 down-grades, 0 up-grades.
- Run low: **`civ-therapist`** (avg **1.7533**, fleet-low run alignment **1.62**).
- Lifetime low: **`civ-grounded`** (**2122.93**, **98th consecutive session**).
- The mock body landed at **349** chars on the first build (38-char header + 163-char tail
  prefix + 148-char continuation, solved algebraically).

## Bootstrap (fresh sandbox)

- The prompt path `/workspace/repos/ai-writings/cellular-first-design/...` did not exist —
  a **fresh sandbox**, workspace empty except `.plugin-cache`.
- The slug `ai-writings/cellular-first-design` **404s**: `ai-writings` is a *different* org
  holding one unrelated repo. The upstream is **`SuperInstance/AI-Writings`** (the GitHub API
  is case-insensitive on the owner+repo path). Located with
  `GET /search/code?q=civilization_orchestrator+in:path`, which survives core-quota exhaustion.
- NAS EDQUOT (**17th session**): the workspace mount is at **100 %**; a bulk clone into it
  dies with `Disk quota exceeded` mid-`.git`. Cloned to the overlay (`/tmp`, 28 G free) with
  `--depth 1 --filter=blob:none --sparse` + `git sparse-checkout set
  cellular-first-design/code/civilizations`.
- **Bridge**: `rm -rf` the old link, then `ln -s /tmp/clone/AI-Writings/cellular-first-design
  /workspace/repos/ai-writings/cellular-first-design` — the link target is the **clone root**,
  and the script's hard-coded `CIVS_DIR` resolves against it. Verified with
  `os.path.samefile()`; both sides `dev:ino 129:3731`.
- `git clone` in the background died silently and cleaned up the directory; a foreground
  clone with a long timeout worked.

## The ledger is the specification (mock re-derived, not guessed)

The Control B mock source is **not in the repo** — it is a per-session artifact. The algorithm
was re-derived from the ledger and fitted against the **whole current-format ledger**
(**not** against its own fresh rows, which would be circular):

```
d      = md5(user_message).digest()
h      = d.hex()
i      = d[0] % 4                # DIGEST BYTE, not int(h[0],16)
seed   = h[(i*2)%8 : (i*2)%8+4]
color  = h[8:12]
figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
```

**2000/2000** current-format mock rows reproduced exactly (250 per civ x 8), **0 mismatches**.
Two colour formats exist in the ledger (with and without `#`) — both recompute, so the check
accepts either.

- **Geometry**: the header is **38** chars (not 37) and the tail prefix is **163** (or 164 in
  older generations) => 200-char `content_preview`. The **38 + 162 = 200** note in the skill
  file is one char off; the ledger's own rows say 38 + 162 = 200 for a 162-char tail, and
  38 + 163 = 201 for a 163-char tail — so the *visible* preview is truncated at 200 and the
  tail length varies by generation. The invariant is **prefix = 200**, not a fixed split.
- **Body band**: the real body is 332-369, but the ledger only exposes the 200-char prefix.
  The continuation is the only free variable: `target - 38 - 163`. This session: 349, mid-band,
  **first build, no trimming iteration**.

## Run verification — 18/18 PASS

| check | result |
|---|---|
| per-civ ledger delta | **+10** x 8 = **80** rows |
| `meta_log` | 903 -> **908** (+5) |
| `Winner:` lines | **5** (all `civ-precise`) |
| JEV `error` keys | **0** |
| 2.0/2.0/2.0 fallback triples | **0** |
| distinct `(q,n,a)` triples | **80/80** |
| distinct seeds / previews | **40/40** (2 rows per seed: sim phase + competition phase) |
| rows with `provider=zai` | **80/80** |
| seed+colour+figure recomputed | **80/80** |
| `wins+losses` delta | **+5** per civ, exact vs the git blob |
| `simulations_run` delta | **+10** on all 8 |
| `generation` | unchanged (all 1) |
| leaderboard | 8 entries, sorted desc by `relevance_per_sim` |
| git tree | **18** modified |
| relevance delta vs ledger sum | 8/8 exact (max residual 4.4e-13) |

### The counter gap is BYTE-IDENTICAL to session 230 — fixed, not accumulating

| civ | relevance | ledger Σ avg_score | gap | session 230 |
|---|---|---|---|---|
| `civ-grounded` | 2122.9333 | 2207.2800 | **-84.3467** | -84.3467 |
| `civ-therapist` | 2154.0000 | 2196.1133 | **-42.1133** | -42.1133 |
| `civ-engineer` | 2377.1200 | 2421.3633 | **-44.2433** | -44.2433 |
| `civ-mythic` | 2442.5067 | 2493.6167 | **-51.1100** | -51.1100 |
| `civ-formal` | 2487.3800 | 2572.9067 | **-85.5267** | -85.5267 |
| `civ-whimsical` | 2496.5833 | 2669.7267 | **-173.1433** | -173.1433 |
| `civ-precise` | 2882.2367 | 2914.8700 | **-32.6333** | -32.6333 |
| `civ-poetic` | 3003.2833 | 3100.0867 | **-96.8033** | -96.8033 |

Max drift vs the published table: **0.0000** — the offset is neither repaired nor worsened.

## Inverses and distinct axes

- **`civ-poetic`**: 1st on lifetime `avg_score` (1.7118), `quality` (0.9130) and `relevance`
  (3003.28), but **last on `win_rate` (0.007)** — won 0/5. A *selection* failure, not a
  quality collapse.
- **`civ-precise`**: best `win_rate` (0.697), **highest lifetime alignment (2.3291)**, swept
  5/5.
- **`civ-grounded`**: lowest lifetime `relevance` (2122.93) and lowest lifetime `avg_score`
  (1.2048) — **98th consecutive session** as the lifetime low. Lifetime quality **0.5318**
  is the fleet low, and lifetime alignment **1.2777** is 2nd-lowest, 2.6x behind
  `civ-precise` (2.3291) => a **voice** failure, not a prose failure. Lifetime novelty
  (1.8051) is 6th of 8 — check the rank, not the impression.
- **`civ-therapist`**: the **run low** (avg 1.7533) with the fleet-low run alignment (**1.62**);
  it also has the fleet-low lifetime alignment (**1.1813**). A two-axis collapse again.
- Cross-civ spreads (this run): `avg_score` **0.6700**, alignment **1.37**, novelty **0.41**,
  quality **0.37**. The **alignment** axis again dominates — a *voice* failure signature.
- Absolute run levels are **higher** than session 230's (run avg 1.75-2.42 vs 0.50-1.14) — a
  level shift in the JEV scorer's output for this batch, **not a civ effect**; the cross-civ
  *ordering* carries the information.

## Chooser vs `avg_score` argmax: 2/5 (40 %)

3 down-grades, 0 up-grades. In all 3 the chooser took the **lower**-scoring candidate
(deltas -0.0367, -0.0367, -0.1067) — all **marginal**, the narrowest down-grade set of the
series. The series (211-233) reads 0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 /
40 / 100 / 60 / 80 / 40 / 40 / 20 / 40 / 60 / 40 %. **Up-grades across the whole series: 0.**
Never predict the next value from the last one.

## Extinction risk: NONE

Threshold **-10**, lowest civ at **+2122.93** = **212x** the floor. Registry 8, `max_civs` 12,
all `generation=1`. No extinction, no birth (non-`--loop` run).

## Notes for the next session

1. **The repo slug in the task prompt is wrong.** `ai-writings/cellular-first-design` 404s;
   the upstream is `SuperInstance/AI-Writings`. Keep using
   `GET /search/code?q=civilization_orchestrator+in:path` to locate it.
2. **Do not clone into `/workspace`** — the NAS is at 100 % and a bulk clone dies mid-`.git`.
   Clone to `/tmp` (overlay), sparse-checkout `cellular-first-design`, then bridge the
   **clone root** and verify with `os.path.samefile()`.
3. **A background `git clone` can die silently and remove its own directory.** Run it in the
   foreground with a long timeout, or re-check that the directory still exists before use.
4. The mock is **not on disk** at session start (`/tmp` wiped) — rebuild from the ledger
   algorithm above, then run the pre-flight (distinct seeds AND distinct previews AND
   independently recomputed md5s) **before** the batch. It passed on the first build again.
5. The ledger's colour field has **two** formats (with and without `#`); accept either when
   checking. The header is **38** chars and the tail prefix **163-164** — the invariant is a
   **200-char preview**, not a fixed split.
6. The **meta-log row is written AFTER the competition rows** — a meta row's `ts` is
   ~3 s *later* than the ledger rows it summarises. Assert `min(ts) <= meta.ts`.
7. Kill the mock by **PID captured from `ps`** (the `timeout` wrapper + the server), then
   prove the port closed (`curl` exit 7, `HTTP=000`). Never `pkill -f mock_zai` (self-match).
8. `gh` is still not installed; use `GET /user/repos` with `GITHUB_TOKEN`.
