# Civ Orchestrator — RUN REPORT session 186 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `802cf5b1` (session 185 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8199` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override alone is dead code behind the token gate).
**JEV live:** `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; pre-flight probe → **HTTP 200**
with `{"model":"jev-1.14.0", …}`.
**Run status:** all verification checks PASS (12/12 content + 8/8 pre-flight).

---

## Environment (all re-confirmed)

| Fact | Value |
|---|---|
| Workspace | **empty** apart from `.plugin-cache` / `.skills` — the prompt's path did not exist (**12th consecutive occurrence**) |
| Upstream owner | **`SuperInstance/AI-Writings`** — the `ai-writings/…` slug 404s; the GitHub API is case-insensitive |
| `gh` | not installed (**20th session**) — used the **mcode-tools GitHub connector** (`search_code` on `filename:civilization_orchestrator.py` → 1 hit) |
| GitHub REST | **rate-limited to 0 remaining** (`API rate limit exceeded for user ID 193104091`) ⇒ REST `GET /user` unusable; **git protocol is unaffected** |
| TLS | `SSL_CERT_FILE=/etc/ssl/certs/agent-identity/sandbox-gateway-ca.crt` (gateway anchor only) |
| Clone | `/tmp/repos/ai-writings` via `--filter=blob:none --no-checkout` + `sparse-checkout set cellular-first-design` ⇒ **15 MB** working tree |
| Bridge | `ln -sfn /tmp/repos/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; inode identity (`3680983 47` / `12635 129`), `-ef` → `EF_OK` |
| z.ai credential | **absent** — `ZAI_TOKEN` unset in env and in all 8 sandbox secrets; real endpoint → **401** `token expired or incorrect` ⇒ endpoint healthy, credential absent (**53rd session**) |
| JEV | **live** — HTTP 200, served model `jev-1.14.0`; a 422 on a *string* `questions` value is only a payload-shape complaint, not a credential failure |
| Env name | orchestrator reads **`TYPESAFEAI_KEY`**; the sandbox secret is **`TYPESAFE_AI_TOKEN`** ⇒ the alias must be exported explicitly |
| Tool timeout | 30 s < run ~55 s ⇒ detached launch (`setsid nohup timeout -s KILL 600`), stdout → `/tmp/civ_run.log`, `< /dev/null` |

## Mock rebuild — RUNBOOK algorithm, fixes (a)–(f) all re-applied

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # MESSAGE-derived, NOT a request counter
seed   = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]   # 4 hex chars (fix e)
color  = h[8:12]
figure = h[12:16] / h[16:20] / h[20:24]
```

Fix (f) is the one that is invisible to a distinct-messages-only probe: the index must come
from the **message**, not a request counter, or the same `(civ, prompt)` pair carries two
different seeds — one from the sim phase and one from the competition phase.

### Pre-flight gate — EIGHT checks, ALL PASS

| # | Check | Result |
|---|---|---|
| 1 | 40 requests issued | **PASS** (n=40) |
| 2 | 40/40 distinct seeds | **PASS** (distinct=40, nulls=0) |
| 3 | 40/40 distinct previews | **PASS** (distinct=40) |
| 4 | 40/40 independently recomputed md5 (seed, colour, figure) | **PASS** (40/40) |
| 5 | 8/8 distinct seeds AND 8/8 distinct previews on every one of 5 prompts | **PASS** (8,8 on all five) |
| 6 | 0 literal `seed={}` | **PASS** (n=0) |
| 7 | 0 `EXC:` / tracebacks | **PASS** (n=0) |
| 8 | **repeat-same-message ⇒ same seed (40 messages × 2 repeats)** | **PASS** (mismatches=0/40) |

## Run result

`8 civs × 5 sims` then `5 competition prompts` ⇒ **80 new rows**, all `provider=zai`.

Competition winners — **civ-precise took 5/5 prompts**:

| Prompt | Winner | Runner-up (avg score) |
|---|---|---|
| what a cell is | The Precise | The Poetic (1.58) |
| the bookkeeper's role | The Precise | The Poetic (1.77) |
| the witness log | The Precise | Whimsical 2.05 / Poetic 2.03 (behind Precise 2.34) |
| ternary values | The Precise | The Whimsical (1.83) |
| JEV as a decision oracle | The Precise | Poetic 1.71 (behind Precise 1.72) |

## Verification — 12/12 content checks PASS

| # | Check | Result |
|---|---|---|
| 1 | 80 new rows (8 civs × (5 sims + 5 competition)) | **PASS** (n=80) |
| 2 | all rows `provider=zai` | **PASS** (`{'zai': 80}`) |
| 3 | 40 distinct seeds | **PASS** (distinct=40) |
| 4 | **80/80 recomputed md5** (seed + colour + figure) | **PASS** (80/80) |
| 5 | 0 `(civ,prompt)` pairs with >1 seed | **PASS** (40 pairs) |
| 6 | 8/8 distinct seeds on each of the 5 prompts | **PASS** |
| 7 | 0 literal `seed={}` | **PASS** |
| 8 | 0 JEV errors | **PASS** |
| 9 | 0 fallback triples (2.0 / 2.0 / 2.0) | **PASS** |
| 10 | 80/80 rows carry the `[mock-zai]` prefix | **PASS** |
| 11 | 5 competition rows appended to `meta_log.jsonl` | **PASS** (663 → 668) |
| 12 | `leaderboard.json` rewritten | **PASS** |

### `ls -la` — `simulations.jsonl` before → after (every civ +10 rows)

| civ | before | after | Δ |
|---|---|---|---|
| civ-engineer | 1296 | 1306 | +10 |
| civ-formal | 1327 | 1337 | +10 |
| civ-grounded | 1342 | 1352 | +10 |
| civ-mythic | 1299 | 1309 | +10 |
| civ-poetic | 1321 | 1331 | +10 |
| civ-precise | 1291 | 1301 | +10 |
| civ-therapist | 1294 | 1304 | +10 |
| civ-whimsical | 1354 | 1364 | +10 |
| `meta_log.jsonl` | 663 | 668 | +5 |

Each civ gains **10** lines per run: 5 simulation rows + 5 competition rows. Byte sizes moved
in lockstep (e.g. `civ-precise` 720 425 → 726 134 B). File mtimes moved `08:03` → `08:04`.

## Civilization relevance — and who is running low

`relevance += avg_score` per simulation; extinction threshold is **`relevance < −10`**, and
`extinction_and_birth()` is called **only in `--loop` mode** (every 3rd iteration), so a
one-shot run legitimately produces **no birth and no extinction** — confirmed: no
`[BIRTH]` / `[EXTINCTION]` / `mutated` line in the log, and still exactly 8 civ directories.

| civ | relevance | Δ this run | per_sim | win_rate | wins | losses |
|---|---|---|---|---|---|---|
| civ-poetic | 1982.24 | +17.53 | 1.532 | 0.009 | 6 | 637 |
| civ-precise | 1829.76 | +16.66 | 1.424 | **0.630** | 402 | 236 |
| civ-whimsical | 1726.33 | +17.69 | 1.327 | 0.008 | 5 | 638 |
| civ-mythic | 1590.04 | +11.20 | 1.234 | 0.016 | 10 | 627 |
| civ-formal | 1535.33 | +13.14 | 1.186 | 0.151 | 97 | 544 |
| civ-engineer | 1461.88 | +10.28 | 1.139 | 0.075 | 48 | 588 |
| **civ-therapist** | **1449.80** | +10.75 | 1.126 | **0.017** | 11 | 629 |
| **civ-grounded** | **1297.08** | +11.69 | **0.991** | 0.109 | 70 | 572 |

### Low-relevance civilizations

1. **The Grounded (`civ-grounded`) — lowest relevance, 1297.08.**
   `relevance_per_sim` **0.991** is the only sub-1.0 figure in the fleet, and the gap to the
   median (1.424) is **~30 %**. It scored the worst or joint-worst on 3 of 5 prompts
   (0.98, 0.98, 1.27) and never placed first. It is the closest to the floor, though still
   **1297 units above** the −10 extinction threshold — extinction is not remotely in play.

2. **The Therapist (`civ-therapist`) — 1449.80, win_rate 0.017.**
   11 wins in 640 contests — second-worst rate behind Whimsical. It scored **below 1.25 on
   all 5 prompts** (1.02, 1.11, 1.24, 1.03, 1.13). Its weakness is *consistency*, not a single
   collapse: it never scores zero, it just never wins either.

3. **The Engineer (`civ-engineer`) — 1461.88, win_rate 0.075.**
   Bottom of the top half. It took **0.96 / 1.04 / 1.11 / 1.00 / 0.95** — the only civ with
   an average **below 1.0 on two prompts**, and it has never out-scored a field it should
   dominate on the engineer-facing prompts.

**Low-relevance caveat.** These three are the fleet's tail, but the spread is a *standing*
condition, not a regression: the tail gains **+10.28 … +11.69** per run, essentially the
same increment the leaders gain. `relevance` is a cumulative sum over ~1 300 sims, so a civ
with a low `relevance_per_sim` stays pinned in the tail for hundreds of runs. The honest
reading is **per_sim**, not the absolute number: Grounded (0.991) is genuinely the weakest
per-simulation scorer, while Therapist and Engineer are only marginally behind Formal
(1.186) and Mythic (1.234).

**Low win_rate is not the same as low relevance.** `civ-poetic` (1.532) and `civ-whimsical`
(1.327) hold the #1 and #3 relevance slots with win rates of **0.009** and **0.008** — worse
than Therapist's 0.017. The win_rate field is a near-useless discriminator at this fleet
size (5 contests per run against 8 civs, cumulative over hundreds of runs), and it should
not be read as a health signal. If the fleet wants a tail signal, `relevance_per_sim` is the
field to threshold on.

## Files changed (18)

- 8 × `civ-*/simulations.jsonl` (+10 rows each)
- 8 × `civ-*/culture.json` (relevance_score / wins / losses / simulations_run)
- `leaderboard.json` (relevance, per_sim, win_rate, sims_run)
- `meta_log.jsonl` (+5 competition rows)

## Teardown

The mock server was left running for post-run verification and is killed by **exact argv
match** — `python3 /tmp/mock_zai.py` and `timeout -s KILL 900 python3 /tmp/mock_zai.py`
(**two** pids). Never `pkill -f mock_zai`: the pattern self-matches the killing shell.
