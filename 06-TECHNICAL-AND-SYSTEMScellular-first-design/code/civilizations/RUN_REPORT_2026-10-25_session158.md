# Civilization Orchestrator — RUN REPORT session 158 (2026-10-25)

**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` is absent from the sandbox env and
from all 8 sandbox secrets; the real z.ai endpoint returns `401` with a placeholder bearer.
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`); served model `jev-1.14.0`.

**Command (exactly as requested):**

```bash
cd /workspace/repos/ai-writings/cellular-first-design/code/civilizations
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
export ZAI_TOKEN="mock-local-bridge"
export ZAI_URL_OVERRIDE="http://127.0.0.1:8799/api/coding/paas/v4/chat/completions"
python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai
```

## Environment findings (all re-confirmed)

| Item | Result |
|---|---|
| Workspace at session start | `/workspace` contained only `.plugin-cache` — no `repos/`, no `ai-writings/` |
| Upstream owner | `ai-writings/cellular-first-design` 404s; the real tree is `SuperInstance/AI-Writings` → `cellular-first-design/` (case-sensitive owner) |
| NAS EDQUOT | **Total.** `git clone` into `/workspace/repos/...` dies with `close error: Disk quota exceeded`; even a 100 KB `dd` fails. `mkdir` works. NAS is 600 G/600 G, 0 bytes free — account-wide, not this session's |
| Bridge | `ln -s /tmp/AI-Writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`; verified by inode identity `129:10423` on both sides + `-ef` PASS |
| GH REST API | Rate-limited (0/5000) on arrival; reset after ~19 min. `git ls-remote` and the git protocol were **not** rate-limited and were used for existence checks |
| `gh` CLI | Not installed |

## Verification — asserted on rows, never on exit code

`call_provider()` returns `None` on a missing token and the competition short-circuits on
`if not results: return None` — **all silently, exit code 0.** So every assertion below is
on artifact content, not on the process status.

| Assertion | Expected | Actual |
|---|---|---|
| `simulations.jsonl` delta per civ | +10 each (8 civs) | **+10 each, 8/8 PASS** |
| `meta_log.jsonl` delta | +5 | **+5** (523 → 528) |
| `Winner:` lines in run log | 5 | **5** |
| `culture.json` `simulations_run` delta | +10 each | **+10 each, 8/8** |
| `git status --porcelain` | 18 modified | **18** (8 ledgers + 8 cultures + `meta_log.jsonl` + `leaderboard.json`) |
| New rows total | 80 | **80** |
| JEV `error` key in scores | 0 | **0** |
| `2.0/2.0/2.0` fallback triple | 0 | **0** |
| `provider != "zai"` | 0 | **0** |
| Rows missing `[mock-zai seed=…]` prefix | 0 | **0** |
| Distinct seeds across the 80 rows | 40 | **40** |
| `(civ, prompt)` pairs carrying >1 seed | 0 | **0** |
| `avg_score` spread | non-constant | **0.0333 – 0.9100, 52 distinct values** |

The score spread is the load-bearing check: it proves JEV returned *real, varied* scores
rather than the constant 2.0 default, so the leaderboard below reflects genuine judgement.

## Per-civ ledger growth (bytes / lines)

| civ | before | after | lines | Δ |
|---|---:|---:|---:|---:|
| civ-grounded | 600725 | 606517 | 1062 → 1072 | +10 |
| civ-whimsical | 608550 | 614371 | 1074 → 1084 | +10 |
| civ-formal | 587670 | 593467 | 1047 → 1057 | +10 |
| civ-poetic | 583542 | 589305 | 1041 → 1051 | +10 |
| civ-precise | 562075 | 567817 | 1011 → 1021 | +10 |
| civ-mythic | 570924 | 576649 | 1019 → 1029 | +10 |
| civ-therapist | 574121 | 579981 | 1014 → 1024 | +10 |
| civ-engineer | 575295 | 581140 | 1016 → 1026 | +10 |

`meta_log.jsonl`: 233410 → 235711 bytes, 523 → 528 lines.

## Leaderboard after the run (sorted by `relevance_per_sim`)

| rank | civ | relevance | Δ relevance | rel/sim | wins | losses | win_rate | temp |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | civ-poetic | 1567.19 | +2.45 | 1.546 | 6 | 497 | 0.012 | 0.8 |
| 2 | civ-precise | 1408.04 | +5.96 | 1.401 | 286 | 212 | 0.574 | 0.2 |
| 3 | civ-whimsical | 1388.67 | +1.47 | 1.360 | 5 | 498 | 0.010 | 0.95 |
| 4 | civ-mythic | 1276.98 | +1.39 | 1.266 | 9 | 488 | 0.018 | 0.85 |
| 5 | civ-therapist | 1175.08 | +1.04 | 1.167 | 10 | 490 | 0.020 | 0.6 |
| 6 | civ-formal | 1174.11 | +1.72 | 1.157 | 83 | 418 | 0.166 | 0.3 |
| 7 | civ-engineer | 1148.94 | +1.12 | 1.144 | 42 | 454 | 0.085 | 0.4 |
| 8 | **civ-grounded** | **1009.89** | **+0.78** | **0.981** | 68 | 434 | 0.135 | 0.5 |

## Low-relevance civilizations

**`civ-grounded` (The Grounded) is the single low-relevance civilization** in this run:

- Lowest absolute relevance (1009.89) and lowest `relevance_per_sim` (0.981) of all 8 civs.
- **Lowest relevance gain of the run: +0.78** — roughly a third of the mean (+1.74), and the
  only civ to end the run on a sub-1.0 `relevance_per_sim`.
- It won **0 of the 5** competitions (wins +0, losses +5).
- Its preferred temperature (0.5) sits mid-range, so this is not a parameter-extremity artifact.

**Secondary low-relevance signal — the win-rate/loss-rate split.** The board's top two entries
are not the best *competitors*:

- `civ-poetic` ranks #1 on relevance but has a **0.012 win rate (6W/497L)**.
- `civ-whimsical` (#3) 0.010 (5W/498L) and `civ-mythic` (#4) 0.018 (9W/488L) are in the same band.
- Only `civ-precise` (0.574) and `civ-formal` (0.166) actually win competitions, and
  `civ-precise` took **4 of the 5** wins this run.

This means `relevance_per_sim` is driven almost entirely by **cumulative `avg_score` accumulated
over ~1000 sims**, while win/loss is a separate, far more selective signal. A civ can sit at the
top of the leaderboard while being rejected by the meta-GAN essentially every round. Ranking
the board purely on `relevance_per_sim` hides that.

**Not low-relevance but worth flagging:** relevance is *cumulative and never decays* — every civ's
`relevance_score` grew this run, and the spread between the top (1567) and bottom (1010) is
inherited from ~1000 prior sims, not produced by this run. The run itself moved the board by
+0.78 to +5.96.

## Counter gap (sign computed from the data, not copied)

`culture.json` relevance delta minus the sum of this run's ledger `avg_score`:

```
civ-grounded  -0.00   civ-whimsical  -0.00   civ-formal  +0.00   civ-poetic   +0.00
civ-mythic    -0.00   civ-therapist  -0.00   civ-precise +0.00   civ-engineer -0.00
TOTAL           -0.00
```

The RUNBOOK's documented **negative** counter gap (e.g. `civ-whimsical -173.15`, total -609.93)
is a **pre-existing historical offset** in the committed blobs; it is **not** reproduced by this
run, whose relevance tracks the ledger exactly. The gap is a fixed per-civ offset because
`save_state()` has no lock, so `relevance_per_sim` is **not recomputable from the ledger** by an
auditor — that remains true and is worth keeping in mind when reading the board.

## Mock bridge hygiene

- Mock rewritten at `/tmp/mock_zai.py` with **both** documented fixes:
  - session 112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` (a plain `seed[i*2:i*2+2]` crashes for `i>=4`)
  - session 117 seed source `md5(whole_message)[:8]` (seeding from the first 8 chars of the
    message yields `youareav` for every civ, making the chooser unable to discriminate)
- **Pre-flight before the batch:** 8 civs → **8 distinct seeds**, **8 distinct previews**,
  0 prefix errors, **0 tracebacks** in `/tmp/mock_zai.log`. A 200 on a trivial probe is not
  proof the mock is correct — the pre-flight used the exact long cultural prompt.
- Torn down by exact argv match (`$2=="python3" && $3=="/tmp/mock_zai.py"`), killing the **server**
  pid, not the `timeout` wrapper pid. Port re-verified **closed** (`curl` exit 7).

## Reusable environment notes

- `ZAI_TOKEN` remains absent from the env and from all 8 sandbox secrets — **46th session** with
  this gap. `ZAI_URL_OVERRIDE` alone is dead code: the token gate in `call_provider()` returns
  first, so Control B needs **both** a non-empty `ZAI_TOKEN` and the URL override.
- `TYPESAFEAI_KEY` must be exported from the sandbox's `TYPESAFE_AI_TOKEN`; the script reads the
  former, the sandbox stores the latter.
- The upstream path in the request (`/workspace/repos/ai-writings/cellular-first-design/...`) is
  **not a GitHub repo path** — it is the NAS location of the `cellular-first-design` directory
  inside `SuperInstance/AI-Writings`. Resolve the owner by listing `GET /user/repos` and matching
  the *directory*, not the slug.
- `GET /user/repos?per_page=100` needs 6 pages (600 repos) to enumerate this account.
- GitHub REST rate limit (5000/hr) was fully exhausted at session start; the git protocol
  (`git ls-remote`) is unaffected and is the reliable way to assert repo existence/absence.
