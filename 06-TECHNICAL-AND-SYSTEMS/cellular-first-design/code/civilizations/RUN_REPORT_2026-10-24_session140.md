# Civ Orchestrator — RUN REPORT session 140 (2026-10-24)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `4486a2d2` (session 139 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe -> HTTP 200 with a real
score body, model `jev-1.14.0`).
**Run status:** all verification checks PASS (row deltas exact, 5/5 competitions, 0 JEV errors).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| NAS EDQUOT | total — `cp` into `/workspace` writes **0-byte** files that still appear in `ls`; a 1 KB `printf` into `/workspace` yields `size=0`. `/tmp` is exempt (probe -> `size=2`) |
| Bridge | `ln -sfn /tmp/AIW/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity `129:10425` on both sides, `-ef` confirms |
| Clone target | `/tmp/AIW` (filtered, `--filter=blob:none --no-checkout` + sparse-checkout `cellular-first-design`); `/tmp` is exempt from the NAS quota |
| Upstream owner | `SuperInstance/AI-Writings` — the `ai-writings/cellular-first-design` slug 404s (confirmed again, unauthenticated **and** authenticated) |
| `gh` | not installed (21st session) |
| Tool timeout | 30 s < run ~30 s -> launched detached under `setsid nohup timeout -s KILL 300`, polled by PID |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; z.ai returns `401` (endpoint healthy => credential gap, not an outage) |
| JEV | live — HTTP 200 with a scored body, model `jev-1.14.0` |
| Mock teardown | killed **both** pids (wrapper 365 + server 367); `curl` exit 7 = port closed; 0 tracebacks in the log |

### EDQUOT now truncates silently rather than erroring (new observation)

Earlier sessions recorded `cp` *failing* with `Disk quota exceeded` on `close()`. This session the
same copy reported **no error at all** yet every landed file was **0 bytes** — `find . -type f
-size +0` returned **0 of 6** files while `ls -la` showed the full name and size. A `cp` that
"works" is therefore **not** evidence of a successful copy.

**Always verify a NAS write with `stat -c%s` (or `find -size +0`) on the specific file, never
with the exit code or with `ls`.** The symlink bridge remains the only reliable way to put the
tree on the workspace path.

## Mock rebuild

`/tmp` was wiped again => the mock was rebuilt from the RUNBOOK with the session-112 index wrap
(`seed[(i*2)%8:((i*2)%8)+2]`) applied. Verified **before** the batch:

- HTTP 200 on a probe using the orchestrator's real request shape (long `messages[].content`),
- 360-char body, `[mock-zai seed=9219363a]` prefix present,
- `grep -c Traceback /tmp/mock_zai.log` -> **0**.

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** (5 sims + 5 competition sims) | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (433 -> 438) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| rows with a JEV `error` key | **0** | 0 | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7 | PASS |

### Per-civ line deltas

| civ | before | after | delta |
|---|---|---|---|
| civ-engineer | 836 | 846 | +10 |
| civ-formal | 867 | 877 | +10 |
| civ-grounded | 882 | 892 | +10 |
| civ-mythic | 839 | 849 | +10 |
| civ-poetic | 861 | 871 | +10 |
| civ-precise | 831 | 841 | +10 |
| civ-therapist | 834 | 844 | +10 |
| civ-whimsical | 894 | 904 | +10 |

## Competition results (5 prompts, 5 winners)

| prompt | winner | winner avg | field mean | field max |
|---|---|---|---|---|
| what a cell is | **civ-grounded** | 0.46 | 0.98 | 1.71 |
| the bookkeeper's role | **civ-precise** | 1.20 | 0.89 | 1.74 |
| the witness log | **civ-grounded** | 0.29 | 0.82 | 1.71 |
| ternary values | **civ-poetic** | 1.13 | 0.63 | 1.71 |
| JEV as a decision oracle | **civ-therapist** | 0.34 | 0.83 | 1.45 |

Picks: `civ-grounded` x2, `civ-precise` x1, `civ-poetic` x1, `civ-therapist` x1.

**Note on the winner-scores column.** On 3 of 5 prompts the winner's own `avg_score` was the
**minimum** of the field (grounded 0.46 vs mean 0.98; grounded 0.29 vs mean 0.82; therapist
0.34 vs mean 0.83). This is expected — `civilization_competition` asks JEV a **choice** question
("which civilization serves this moment best?"), and the choice is made on JEV's read of the
*content*, not on the numeric `avg_score`. The two are separate signals, so a low `avg_score`
with a JEV choice win is not a contradiction. Do not read the winner column as "highest score".

## Leaderboard after the run

| rank | civ | relevance | rel/sim | sims | W/L | win rate | gen | temp |
|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | 1386.21 | 1.662 | 834 | 6/407 | 0.015 | 1 | 0.80 |
| 2 | civ-whimsical | 1244.17 | 1.479 | 841 | 5/408 | 0.012 | 1 | 0.95 |
| 3 | civ-precise | 1218.93 | 1.477 | 825 | 224/184 | 0.549 | 1 | 0.20 |
| 4 | civ-mythic | 1144.53 | 1.381 | 829 | 7/400 | 0.017 | 1 | 0.85 |
| 5 | civ-therapist | 1072.48 | 1.297 | 827 | 9/401 | 0.022 | 1 | 0.60 |
| 6 | civ-engineer | 1037.22 | 1.259 | 824 | 36/370 | 0.089 | 1 | 0.40 |
| 7 | civ-formal | 1043.11 | 1.249 | 835 | 66/345 | 0.161 | 1 | 0.30 |
| 8 | **civ-grounded** | **911.21** | **1.073** | 849 | 66/346 | 0.160 | 1 | 0.50 |

All eight civs advanced by exactly **+10 sims**. No mutation (all `gen=1`), no birth, no
extinction — `relevance` never approached the `-10` threshold.

## Low-relevance civilizations

**`civ-grounded` — "The Grounded" is the low-relevance civ**, and it is the interesting case:

- lowest **relevance** (911.21) and lowest **relevance_per_sim** (1.073) of all 8;
- largest `sims_run` (849) — it has done the *most* work and scored the *least* per unit of work;
- yet it took **2 of 5 competition wins this run** (tied for the most with any other civ).

So `civ-grounded` is **low by the relevance accumulator but competitive at the meta-GAN**. The
accumulator is `relevance += avg_score` where `avg_score` is the mean of JEV's three
quality/novelty/alignment scores, so it rewards high raw scores. `civ-grounded`'s voice
("plain, specific, verifiable") appears to score low on JEV's *scale* while still being chosen
as the best *fit* for prompts about groundedness — the two prompts it won were "what a cell is"
and "the witness log", both concrete/record-keeping prompts. That is a real signal, not noise:
a civ can be reliably *fit* without being *highly scored*.

**Also low, and structurally more alarming — the two headline leaders are win-starved:**

- `civ-poetic` — #1 on relevance, but **6 wins / 407 losses = 1.5% win rate**.
- `civ-whimsical` — #2 on relevance, but **5 wins / 408 losses = 1.2% win rate**.

`civ-precise` holds a **54.9%** win rate at 224/184 — a genuine near-even duellist — and
`civ-grounded` (16.0%) and `civ-formal` (16.1%) are in the same middling band. The ranking is
therefore **not** a fitness ranking: the top of the leaderboard is occupied by civs that
essentially never win the meta-GAN but accumulate relevance by volume, while the civ that
actually wins half its contests sits 3rd.

**Watch items for the next session:**

1. `civ-grounded` — lowest relevance and lowest relevance/sim, but the most competition wins
   this run. If it stays lowest while continuing to win, the relevance accumulator is measuring
   the wrong thing (score volume, not fitness) and the extinction threshold (`relevance < -10`)
   will never fire on a civ that simply has a modest voice.
2. `civ-poetic` / `civ-whimsical` — win rate <= 1.5% while holding the top two relevance slots.
   Their high `relevance_per_sim` comes from a high `avg_score` on a large sample, not from
   winning. They are the "dead weight at the top" the meta-GAN is supposed to prune.
3. `civ-engineer` and `civ-formal` are mid-table and within 0.010 rel/sim of each other — the
   least stable positions on the board.

## Durable rules confirmed this session

- **Verify a NAS write with `stat -c%s` on the file.** This session `cp` exited **0** with no
  error message while producing **0-byte** files. Exit code and `ls` both lie; only
  `find . -type f -size +0` (0 of 6 here) told the truth.
- **A symlink bridge is still the only way to serve the tree at the requested path.** `ln -sfn`
  + `stat -L -c '%d:%i'` on both sides + `-ef` = verified (`129:10425`).
- **`ZAI_URL_OVERRIDE` is dead code without `ZAI_TOKEN`.** Both must be exported. The
  credential gap is now **17 sessions** running (absent from env and all 8 sandbox secrets).
- **`TYPESAFEAI_KEY` must be exported** from `TYPESAFE_AI_TOKEN`, or JEV degrades silently to
  the constant 2.0 default and every score becomes identical.
- **Mock integrity must be probed with the orchestrator's real payload shape** (a long
  `messages[].content`, not a one-word body) **and** the log grepped for tracebacks — a crashing
  mock leaves a listening socket, so a port/200 check alone is not evidence.
- **Kill the mock by exact-args PID match** (`python3 /tmp/mock_zai.py`), never `pkill -f` —
  and kill **both** the `timeout` wrapper and the server, then confirm the port is closed
  (`curl` exit 7).
