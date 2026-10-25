# Civ Orchestrator — Run Report, session 187 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 54th session) + **live JEV**.
Baseline: `8c29350` (session 186). **All 21 verification assertions PASS.**

## Headline for the next session

- **THE REPO IS `SuperInstance/ai-writings`.** The `ai-writings` GitHub org is a different
  owner; `git ls-remote` on the wrong slug returns *Repository not found*, and the REST API
  was **403 rate-limited to 0** — so a REST probe renders as "not found" for every candidate.
  Use the **search API** (it has its own quota) or `git ls-remote` with a guessed owner.
- **THE WORKSPACE WAS EMPTY — 13th CONSECUTIVE OCCURRENCE.** The prompt's path
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist;
  the mount held only `.plugin-cache`. **`git clone` into `/workspace` fails with
  `Disk quota exceeded`** (NAS EDQUOT — 600 G of 600 G). Clone to `/root` and bridge with
  `ln -s /root/ai-writings /workspace/repos/ai-writings`. Verified by inode identity
  (`129:12603` on both sides).
- **THE `wins`/`losses` COUNTERS ARE NOT IN THE LEDGER.** A verification check that reads
  `row["won"]` gets `0` for every civ and reports a false FAIL on checks 5 and 7.
  `simulations.jsonl` rows carry exactly 9 keys —
  `avg_score, civ, civ_name, content_preview, params, prompt, provider, scores, ts` — and
  **no `won` flag**. The counters live only in `culture.json`, incremented at
  `civilization_orchestrator.py:296` for the **JEV-selected** winner
  (`answers.best_civ.choice`, falling back to max `avg_score`).
  **Take `times_won` from `meta_log.jsonl`'s `winner_civ` field**, not from the ledger.
- **THE LOG'S `Winner:` LINE AND `meta_log.winner_civ` CAN DISAGREE — AND DID.**
  The log's `Winner:` line and `meta_log.winner_civ` **agree on all 5 prompts** — the
  **argmax** is what disagrees, on **2 of 5**: prompt 2 (*the bookkeeper's role*) has
  argmax `civ-poetic` (1.97) but winner `civ-precise` (1.93), and prompt 5 (*JEV as a
  decision oracle*) has argmax `civ-precise` (1.94) but winner `civ-formal` (1.69).
  The JEV `best_civ` selection overrides the argmax, so **`meta_log.winner_civ` is
  authoritative and the argmax is NOT.** Count wins from meta, never from `max(results)`.
- **THE SEVEN-FIX MOCK BUILT CLEAN: 10/10 PRE-FLIGHT ON THE FIRST BUILD.** Body lengths
  **167–209**. The seed slice is the **contiguous** `h[(i*2)%8:(i*2)%8+4]`; `figure` is
  `f"{h[12:16]}/{h[16:20]}/{h[20:24]}"` — three **string** components, never a division.
- **`civ-grounded` remains the low-relevance civ — 59th consecutive session.** Last of 8 on
  lifetime `relevance` **1309.27**, `relevance_per_sim` **0.993** — still the only sub-1.0
  figure in the fleet. Run `avg_score` **1.2197**, `alignment` **1.1050**, `quality`
  **0.1800**, novelty 2.3740 (3rd of 8) ⇒ a **voice** failure, not a prose failure.
  Lowest relevance = **131x** the −10 floor ⇒ no extinction risk.
- **THE RUN-LEVEL LOW ROTATED TO `civ-therapist`** (run `avg_score` **1.0867**, `alignment`
  **0.6830**, `quality` **0.1780**) — a **7th different civ in 7 sessions**. Alignment gap
  to the leader **2.1320** vs quality gap **0.3690** = **5.8x wider**. **Do not code against
  the rotation; watch the axis, not the holder.**
- **Chooser vs `avg_score` argmax: 3/5 (60 %)** — the JEV chooser picked `civ-precise`
  4x and `civ-formal` 1x, while the argmax would have picked `civ-precise` 5x. **Both
  disagreements took the LOWER-scoring candidate** (1.93 vs 1.97; 1.69 vs 1.94) — the
  **8th consecutive session** in which a disagreement is a *down*-grade.
  **Never treat `win_rate` as a quality metric.**
- **`civ-grounded` has the 2nd-best `win_rate` (0.108) and the worst relevance.** The
  lowest-relevance civ is *not* the least-selected one — selection and relevance are
  different axes, and conflating them hides the actual failure.

## Environment recovery

- Upstream owner: **`SuperInstance/ai-writings`** (the `ai-writings/…` slug 404s).
  REST API **core quota exhausted (5000/5000, 403)**; the **search API had 30 remaining**
  and located the repo. GitHub REST is case-insensitive for owner names.
- Cloned to **`/root/ai-writings`** (`--depth 50`, 20 MB `.git` + 7.4 MB tree) — a clone
  into `/workspace` dies with `Disk quota exceeded` (NAS EDQUOT).
- Bridge: `ln -s /root/ai-writings /workspace/repos/ai-writings` (the symlink points at the
  **clone root**, not the nested `cellular-first-design` dir). Verified by inode identity
  (`129:12603`) on both sides.
- `ZAI_TOKEN` absent from env and from the sandbox secret list; z.ai returns **401
  `token expired or incorrect`** ⇒ endpoint healthy, credential absent (**54th session**).
- **JEV live**: a well-formed `questions` body (the orchestrator's own `"type": "score"`
  shape) returns **HTTP 200** with `{"model":"jev-1.14.0", …}`. A probe built from the
  wrong body shape returns **HTTP 422** `union_tag_not_found` — that is a **payload-shape
  complaint, not a credential failure.** Copy the body from the source, do not improvise.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code — the token gate returns `None`
  first).
- `gh` not installed — used the REST search API with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~28 s ⇒ detached launch, stdout redirected **and**
  `< /dev/null`, then poll.
- **The orchestrator process ends as a ZOMBIE (`Zs`)** because the detached launcher never
  reaps it. `ps` shows it alive indefinitely — that is **not** a hang. Verify completion by
  the log tail and the file deltas, not by process exit.

## Mock integrity — all SEVEN fixes applied, 10/10 pre-flight

| # | Fix | Symptom if missing |
|---|---|---|
| a | `seed[(i*2)%8:...]` index wrap | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | md5 of the **whole message** | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| e | seed widened 2 → 4 hex chars | a 2-char slice collides ⇒ 39 distinct seeds, one prompt at 7/8 |
| f | **index from the MESSAGE (`d[0] % 4`), not a request counter** | **64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed** |
| g | **figure = three string components, not a division** | **`TypeError` on every request ⇒ HTTP 500 while the socket stays open; a port/200 liveness probe still looks healthy** |

Pre-flight on the **exact long cultural prompts** (lengths **167–209**), built **civ-major**:
**10/10 PASS ON THE FIRST BUILD** — 40/40 distinct seeds, 40/40 distinct previews, 40/40
independently recomputed md5s (seed + colour + figure), 8/8 distinct seeds AND 8/8 distinct
previews on every one of the 5 prompts, 0 literal `seed={}`, 0 `EXC:`/tracebacks, 40/40
`[mock-zai` prefix, **repeat-same-message ⇒ same seed (40 × 2, 0 mismatches)**, and 0
`(civ,prompt)` pairs carrying >1 seed.

Post-run mock log: **201** OK lines (40 pre-flight + 80 run + 80 repeat-probe + 1 GET),
**0 `EXC:`**, **0 HTTP 500**.
Teardown: mock pids killed by exact argv match (2 pids), 0 remaining procs, `curl -m 5` ⇒
**exit 7**, `HTTP=000`.

## Verification — 21/21 checks PASS

| # | Check | Result |
|---|---|---|
| 1 | per-civ ledger Δ | **+10 × 8** (1306/1337/1352/1309/1331/1301/1304/1364 → +10 each) |
| 2 | total new ledger rows | **80** |
| 3 | `meta_log.jsonl` Δ | **+5** (668 → 673) |
| 4 | `Winner:` lines | **5** |
| 5 | `culture.json` `simulations_run` Δ | **+10 × 8** |
| 6 | `wins` = pre + times won (from `meta_log.winner_civ`) | **8/8 exact** (precise +4, formal +1, rest +0) |
| 7 | `losses` = 5 − times won | **8/8 exact** (precise +1, formal +4, rest +5) |
| 8 | `relevance` Δ == Σ this run's `avg_score` | **8/8 exact** (max residual **6.0e-13**) |
| 9 | rows with JEV `error` | **0** |
| 10 | 2.0/2.0/2.0 fallback triples | **0** |
| 11 | `provider` | **zai × 80** |
| 12 | rows missing `[mock-zai` prefix | **0** (80/80) |
| 13 | distinct seeds | **40 / 80 rows** |
| 14 | `(civ,prompt)` carrying >1 seed | **0** (40 pairs) |
| 15 | rows matching an independently recomputed md5 | **80/80** (seed + colour + figure) |
| 16 | 8/8 distinct seeds AND previews on each of the 5 competition prompts | **5/5** |
| 17 | meta `results` = list of `[civ,score]` | **5/5** |
| 18 | meta-vs-ledger `avg_score` mismatches (later-`ts` row) | **0/40** |
| 19 | registry / generations | **8 civs, all gen 1** |
| 20 | extinction risk | **NONE** (lowest **+1309.27** = **131×** the floor) |
| 21 | confidence spread (JEV-side signature) | **0.35 – 0.97**, 7–10 distinct per civ |

Baseline taken from the **git blob** (`git show HEAD:<path>/culture.json`, unrounded) — the
leaderboard's 2-dp relevance is a display artifact and injects phantom residuals.

## Leaderboard after this run

| id | relevance | rel/sim | wins | losses | win_rate | gen |
|---|---|---|---|---|---|---|
| civ-poetic | 1999.63 | 1.533 | 6 | 642 | 0.009 | 1 |
| civ-precise | 1849.35 | 1.428 | 406 | 237 | 0.631 | 1 |
| civ-whimsical | 1739.92 | 1.327 | 5 | 643 | 0.008 | 1 |
| civ-mythic | 1603.70 | 1.235 | 10 | 632 | 0.016 | 1 |
| civ-formal | 1551.66 | 1.189 | 98 | 548 | 0.152 | 1 |
| civ-engineer | 1476.18 | 1.141 | 48 | 593 | 0.075 | 1 |
| **civ-therapist** | 1460.66 | 1.126 | 11 | 634 | 0.017 | 1 |
| **civ-grounded** | **1309.27** | **0.993** | 70 | 577 | 0.108 | 1 |

## Low-relevance civilizations

**`civ-grounded` — lifetime low, 59th consecutive session.**
`relevance` **1309.27** (last of 8), `relevance_per_sim` **0.993** (the only sub-1.0 figure
in the fleet), run `avg_score` **1.2197**, `alignment` **1.1050**, `quality` **0.1800**,
run novelty 2.3740 (3rd of 8). The alignment gap to the leader (2.8150) is **1.7100** while
the quality gap is only **0.3670** = **4.66x wider** ⇒ a **voice** failure, not a prose
failure. The prose is competent; the register is wrong for the role. No extinction risk
(**131×** the −10 floor).

**`civ-therapist` — this run's low.** Run `avg_score` **1.0867** (lowest of 8),
`alignment` **0.6830** (lowest), `quality` **0.1780** (2nd lowest), novelty 2.3990.
Lifetime `relevance` **1460.66** (7th), `win_rate` **0.017** (won 0/5).
Alignment gap **2.1320** vs quality gap **0.3690** = **5.8×** wider ⇒ again **voice**.

Neither civ is at risk of extinction. Both are **voice** failures, so the remedy is a
tenet/voice-emphasis change, not a prose change.

## Method notes for the next session

- **Count `times_won` from `meta_log.jsonl`, never from the ledger.** The ledger has no
  `won` field; the counters are in-memory and flushed to `culture.json` only.
- **The `max(results)` argmax is not the winner.** `meta_log.winner_civ` (the JEV
  `best_civ` selection) disagreed with the argmax on **2 of 5** prompts this session. The
  log's `Winner:` line agrees with `meta_log`; the argmax is the one that is misleading.
- **A JEV 422 `union_tag_not_found` is a payload-shape error, not an auth error.** Build the
  probe body from the orchestrator's own `jev_score` source.
- **A zombie orchestrator process is a completed run.** The detached launcher never reaps
  the child. Check the log tail and the row deltas.
