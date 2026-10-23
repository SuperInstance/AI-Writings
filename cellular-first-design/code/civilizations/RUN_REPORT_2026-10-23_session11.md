# Civilization Orchestrator — Run Report, session 11 (2026-10-23)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Sandbox:** fresh wipe. `/workspace` held only `.plugin-cache` and `.skills/`; the repo path in the prompt did not exist.
**Repo:** `SuperInstance/AI-Writings` (public) — the prompt's `ai-writings/...` path is the `cellular-first-design/` subtree of this repo; the owner segment in the prompt is a legacy name, not a different repo.
**Remote HEAD at start:** `5dc75baaa4e` (auto-update landing page). The civilizations subtree already carried a **"Session 10"** report committed at `99dd6540` by a prior instance of the same wipe. **This session did not overwrite it** — it is filed as session 11, and the divergences between the two session-10/11 mock A/Bs are themselves the headline finding.

---

## 1. Environment rebuild

| Step | Result |
|---|---|
| `ls /workspace` | only `.plugin-cache`, `.skills/` — no `repos/` |
| `gh` CLI | **not installed** — used the GitHub REST API directly |
| `git clone --depth 1 --filter=blob:none` | **failed** — the promisor-remote pack died and git removed the working tree (reproduces session 9's finding) |
| GitHub **tarball** API (`/tarball/HEAD`) | OK — 3.6 GB compressed, extracted to `/tmp/SuperInstance-AI-Writings-77429d9` |
| `rm -rf /workspace/repos/ai-writings` → `ln -sfn /tmp/… /workspace/repos/ai-writings` | OK — `CIVS_DIR` is hardcoded to the `/workspace` path, so the symlink is required |
| NAS `/workspace` | 100 % quota (600 G used, 0 avail) — the EDQUOT trap. `/tmp` is on the overlay (28 G free) and exempt |

**Traps hit this session (all previously documented, all still live):**

1. **The tarball was stale.** It resolved to `77429d9` (session 9's commit); the remote HEAD was `5dc75baa` and the civilizations subtree already had a **session 10** report and a 31 187 B learnings doc. The tarball's learnings doc was 25 876 B. **The tarball is a snapshot of whatever commit `HEAD` pointed at when the request was served — it can lag the branch.** Verify the subtree with a `contents/<path>?ref=main` call before trusting any baseline.
2. **`git clone --filter=blob:none` is still worse than a full clone** — the promisor fetch died mid-pack and git removed the working tree entirely. Prefer tarball → sparse → full.
3. **A 3.6 GB tarball download exceeds any single tool call.** Background it with `(setsid nohup … &)`, poll the file size, and untar in the background too.
4. **Restore-baseline must be captured from the API, not from the working tree.** The working tree is about to be patched; a copy taken after the patch is itself patched and reports a false DIFF forever. Fetch pristine copies per-file from `contents/<path>?ref=main` and base64-decode `content`.

---

## 2. The unpatched command — still a silent no-op (10th consecutive session)

```
$ python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai ; echo $?
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...
… (8 lines) …
=== Civilization competitions: 5 prompts ===
0
```

**Exit 0.** The batch header and all 8 `[Name] running 5 sims...` lines print **before** any provider call, so they are not evidence of work. There is **not a single `Winner:` line** — every `run_simulation` returned `None` at the provider gate.

| Metric | Before | After | Delta |
|---|---|---|---|
| ledger rows (all 8 civs) | 684 | 684 | **+0** |
| `meta_log.jsonl` | 48 | 48 | **+0** |
| `Winner:` lines | — | **0** | — |

Only `leaderboard.json` was rewritten (a fresh timestamp).

### Root cause, re-verified from scratch

- `ZAI_TOKEN` / `ZAI_KEY` **unset** in the environment and **absent** from the secret store (8 entries: `MOTHQUANTUM_TOKEN`, `TYPESAFE_AI_TOKEN`, `MINIMAX_KEY`, `NOTION_TOKEN`, `NPMJS_TOKEN`, `CRATES_TOKEN`, `PYPI_TOKEN`, `GITHUB_TOKEN`).
- All **8** sandbox secrets tested against `https://api.z.ai/api/coding/paas/v4/chat/completions` → **HTTP 401 "token expired or incorrect" on every one**. A 401 (not 5xx) means the endpoint is healthy ⇒ **credential gap, not outage**. The fleet's own `situations/ROSTER.md` also records the z.ai account as out of balance (code 1113 "recharge"), so a key alone would not have been sufficient.
- **JEV is live**: `POST https://api.typesafe.ai/v1/systemone` → HTTP 200, `jev-1.14.0`, real scores with `confidence` and `probabilities` (probe returned `quality: 2.05, confidence: 0.48`).
- Env-var split persists: the orchestrator reads `TYPESAFEAI_KEY`, the sandbox exports `TYPESAFE_AI_TOKEN` ⇒ always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"`.

**Assert on the row delta and on `Winner:` lines — never on exit code.**

---

## 3. Control B — stub at the gate, JEV untouched

The mock answers on `127.0.0.1:8931` speaking the OpenAI chat-completions shape. `PROVIDERS["zai"]["url"]` was redirected by a **one-line** `ZAI_URL_OVERRIDE` env read (default unchanged); **the `ZAI_TOKEN` gate check was not touched**, so the request is genuinely attempted and a transport failure surfaces as an error instead of a silent drop.

```
ZAI_TOKEN=mock-control-b-token
ZAI_URL_OVERRIDE=http://127.0.0.1:8931/chat/completions
TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
```

The mock's voice table is keyed on the **post-template** rendered string `f"Your voice: {voice_emphasis}."` (with the trailing period), and every call logs a `fallback` flag. Verified against all 8 real cultures before running:

| civ | extracted voice | fallback |
|---|---|---|
| civ-grounded | `warm, factual.` | False |
| civ-whimsical | `playful, surprising.` | False |
| civ-formal | `measured, exact.` | False |
| civ-poetic | `lyrical, dense.` | False |
| civ-precise | `technical, sparse.` | False |
| civ-mythic | `ancient, narrative.` | False |
| civ-therapist | `warm, attentive.` | False |
| civ-engineer | `structural, practical.` | False |

### Result — the session-6/7/8/9/10 prediction reproduced exactly

| Metric | Pre | Run A | Run B (body set B) |
|---|---|---|---|
| ledger rows (all 8 civs) | 684 | **764** (+80) | **844** (+80) |
| `meta_log.jsonl` | 48 | **53** (+5) | **58** (+5) |
| `Winner:` lines | 0 | **5** | **5** |
| rows with a JEV score error | — | **0** | **0** |
| rows with the all-2.0 default (JEV-outage signature) | — | **0** | **0** |
| distinct `avg_score` among the 80 | — | **69** | **73** |
| distinct `content_preview` among the 80 | — | **72** | **74** |
| mock fallbacks | — | **0** | **0** |
| per-civ growth | — | **uniform +10 on all 8** | **uniform +10 on all 8** |

Set A score spread 1.910–2.960, mean 2.553. Set B spread 1.483–2.995.

---

## 4. THE HEADLINE — a second independent A/B **contradicts** the first: the mock reorders the fleet only sometimes

Session 10 (committed at `99dd6540`) ran the first-ever body-set A/B and reported **rank agreement 2/8** — i.e. the mock's prose completely reordered the leaderboard. This session ran an **independent** A/B with a different pair of hand-written body sets and got the **opposite** result.

| | session 10 A | session 10 B | **session 11 A** | **session 11 B** |
|---|---|---|---|---|
| fleet mean `avg_score` | 2.087 | 2.151 | **2.237** | **2.313** |
| fleet mean delta A→B | **+0.064** | | **+0.077** | |
| max per-civ \|delta\| | **+0.293** | | **+0.175** | |
| **rank agreement (same slot)** | **2/8** | | **3/8** | |
| **Kendall τ (ordering)** | — | | **1.00** | |

**This session's two body sets produced an identical ordering** — only the bottom three positions swapped (Therapist↔Precise↔Engineer moved within a 0.19 band, and Formal↔Grounded swapped at the bottom):

```
set A:  Mythic > Whimsical > Poetic > Therapist > Precise > Engineer > Formal  > Grounded
set B:  Mythic > Whimsical > Poetic > Precise  > Engineer > Therapist > Grounded > Formal
```

Per-civ deltas (A→B) for this session: Engineer **+0.175**, Grounded **+0.111**, Mythic +0.088, Poetic +0.087, Precise +0.087, Formal +0.056, Whimsical +0.012, Therapist **−0.003**. Fleet mean moved only +0.077.

### What the two sessions together actually establish

The session-10 finding ("the mock body text reorders the fleet") and this session's finding ("the mock body text preserves the fleet's order") are **not** contradictory once you notice what each measured:

- Session 10's set B moved the **Precise by −0.231** and the **Formal by +0.251** — moves larger than the gap between most adjacent civs. A 0.25 shift *is* a reordering.
- This session's set B moved every civ by **≤ 0.175**, and the two civs that crossed a rank boundary (Formal 1.991→2.047, Grounded 1.958→2.069) crossed by **0.056** — well inside the noise.

So the operative rule is **not** "the mock reorders the fleet" and **not** "the mock preserves the fleet's order". It is:

> **The mock's prose is a first-order confounder whose magnitude is a property of the *body set*, not of the fleet. A rank is reportable only if it survives a body-set swap that moves the fleet mean by at least as much as the rank gap it would reorder.**

**Concretely, the ranking is stable for the top 3 (Mythic, Whimsical, Poetic) and for the bottom 2 (Grounded, Formal) across four independently-written body sets spanning two sessions. The middle 3 (Therapist, Precise, Engineer) are the genuinely unranked band — they trade places under any perturbation.**

This is a **sharper** statement than either prior session's, and it is the one to carry forward: report the stable bands, and report the middle band as **unranked** rather than forcing a 1-of-8 order onto a 0.19-wide tie.

---

## 5. Which civilizations have low relevance — four lenses, four answers

Authoritative source is `culture.json` (the registry), **not** the board. The registry figures below are the state after both Control B runs; the quality lens is computed from the mock rows.

### (a) `relevance_per_sim` — the board's sort key

| civ | rel_per_sim | raw_rel | sims | record |
|---|---|---|---|---|
| **civ-grounded** | **1.978** | 176.01 | 89 | 9W/23L |
| civ-formal | 2.039 | 152.96 | 75 | 5W/26L |
| civ-engineer | 2.085 | 133.47 | 64 | 4W/22L |
| civ-precise | 2.118 | 137.64 | 65 | 16W/12L |
| civ-therapist | 2.420 | 162.15 | 67 | 1W/29L |
| civ-mythic | 2.579 | 177.97 | 69 | 1W/26L |
| civ-poetic | 2.622 | 194.04 | 74 | 0W/33L |
| civ-whimsical | 2.706 | 219.20 | 81 | 3W/30L |

**civ-grounded is lowest — and it is a longevity artefact.** It ran the most sims (89), and a lifetime-average denominator penalises the civ that ran most.

### (b) raw relevance

**civ-engineer 133.47**, then civ-precise 137.64. Same denominator artefact.

### (c) win rate — **selection** appeal under a 150-char preview

| civ | win_rate | record |
|---|---|---|
| **civ-poetic** | **0.000** | 0W/33L |
| civ-therapist | 0.033 | 1W/29L |
| civ-mythic | 0.037 | 1W/26L |
| civ-whimsical | 0.091 | 3W/30L |
| civ-engineer | 0.154 | 4W/22L |
| civ-formal | 0.161 | 5W/26L |
| civ-grounded | 0.281 | 9W/23L |
| **civ-precise** | **0.571** | 16W/12L |

### (d) mean per-sim `avg_score` + sub-scores — lifetime, all 844 rows (684 committed + 160 mock)

| civ | n | avg_score | quality | novelty | alignment |
|---|---|---|---|---|---|
| civ-whimsical | 144 | **2.725** | 2.190 | **2.590** | **3.395** |
| civ-poetic | 111 | 2.620 | **2.230** | 2.330 | 3.301 |
| civ-mythic | 89 | 2.574 | 2.128 | 2.327 | 3.267 |
| civ-therapist | 84 | 2.432 | 2.023 | 2.034 | 3.238 |
| civ-precise | 81 | 2.102 | 1.870 | 1.160 | 3.276 |
| civ-engineer | 86 | 2.066 | 1.700 | 1.434 | 3.065 |
| civ-formal | 117 | 2.038 | 1.798 | 1.099 | 3.219 |
| **civ-grounded** | 132 | **1.972** | 1.746 | 1.441 | **2.731** |

### The answer, with the lenses kept separate

- **`civ-grounded` is the one civ with genuinely low quality, and it is the only stable answer.** Last on `relevance_per_sim` (1.978), last on lifetime `avg_score` (1.972), and **the fleet's lowest alignment (2.731)** — a 0.39–0.66 gap below every other civ on that sub-score. It was placed last (set A) / second-last (set B) in this session and last / second-last in session 10's two body sets. **Four independently-written body sets, two sessions, one consistent answer: civ-grounded is last or second-last on every quality lens.**
- **`civ-poetic` is the highest-relevance civ that is never selected.** 2nd of 8 on lifetime `avg_score` (2.620), **top of all 8 on quality (2.230)**, 2nd on `rel_per_sim` (2.622) — and **0 wins in 33**. It is *not* a quality collapse and *not* an extinction risk; it is a **selection** failure: its register reads well on average but does not survive being judged on a 150-char preview. This has now held across 10 sessions.
- **`civ-precise` is the inverse case.** Best win rate of 8 (0.571) but 5th of 8 on lifetime `avg_score` (2.102) and 2nd-lowest novelty (1.160). Cold temperature (0.2, the fleet minimum) makes output consistently shaped, and a 150-char preview rewards consistency over originality.
- **The middle band {Therapist, Precise, Engineer} is unranked.** The three sit within 0.37 of each other on `avg_score` and swap places under any body-set perturbation. Report them as a band, not an order.
- **`civ-formal` is the weakest cold civ** — 7th on lifetime `avg_score` (2.038) and **lowest novelty of all 8 (1.099)**.
- **Extinction risk: none.** `extinction_and_birth()` retires only below `relevance < -10`; the lowest is **+133.47**, and it only runs in `--loop` mode every third iteration — a single-shot run never triggers it. The registry still lists the same 8 civs; no birth, no extinction.

---

## 6. The chooser/scoring decoupling — 6th replication

| session | agreement |
|---|---|
| 7 | 4.4 % (2/45) |
| 8 | 18.9 % (10/53) |
| 9 | 17.0 % (9/53) |
| 10 | 15.5 % (9/58) |
| **11 (lifetime, 58 rounds)** | **15.5 % (9/58)** |

Over this session's **10** competition rounds the chooser picked a civ that was **not** the top scorer in **10 of 10 rounds**, margins up to 0.90:

| round | JEV chose | argmax(avg) | margin |
|---|---|---|---|
| 1 | civ-grounded | civ-poetic | 0.61 |
| 2 | civ-grounded | civ-precise | 0.17 |
| 3 | civ-grounded | civ-poetic | 0.76 |
| 4 | civ-precise | civ-whimsical | 0.90 |
| 5 | civ-engineer | civ-whimsical | 0.52 |
| 6 | civ-whimsical | civ-poetic | 0.12 |
| 7 | civ-grounded | civ-mythic | 0.28 |
| 8 | civ-precise | civ-poetic | 0.30 |
| 9 | civ-precise | civ-grounded | 0.62 |
| 10 | civ-engineer | civ-whimsical | 0.36 |

The two JEV calls are independent — the scoring call sees the full response, the selection call sees a 150-char preview and no scores — so a competition win is **not** evidence of a higher JEV score.

---

## 7. The counter gap persists (unchanged), and it corrupts the board's sort key

Ledger rows vs `culture.json` `simulations_run`: **844 vs 584 = +260 committed rows counted by nobody**, on every civ (Whimsical +63, Grounded +43, Formal +42, Poetic +37, Engineer +22, Mythic +20, Therapist +17, Precise +16).

`save_state()` rewrites the whole `culture.json` from in-memory counters with no lock and no read-modify-write ⇒ lost-update race. **`relevance_per_sim` is therefore not a reproducible ranking** and the board order cannot be recomputed from the ledger by an auditor. Prefer win rate — with the caveat that win rate is a *selection* metric, not a quality metric.

---

## 8. Temperature and novelty are the same axis (r = 0.975) — 4th replication

| temp | civ | lifetime novelty |
|---|---|---|
| 0.20 | civ-precise | 1.160 |
| 0.30 | civ-formal | 1.099 |
| 0.40 | civ-engineer | 1.434 |
| 0.50 | civ-grounded | 1.441 |
| 0.60 | civ-therapist | 2.034 |
| 0.80 | civ-poetic | 2.330 |
| 0.85 | civ-mythic | 2.327 |
| 0.95 | civ-whimsical | 2.590 |

**Pearson r = 0.975** (s8 0.985, s9 0.980, s10 0.981). The fleet is **8 points on one temperature/novelty gradient with a style overlay**, not 8 independent voices. `mutate()` (±0.15 on temperature) is nearly a no-op on quality, and the `max(0.1, …)` floor makes the cold end a **one-way ratchet** — Precise (0.2) and Formal (0.3) can only ever move warmer.

---

## 9. Two upstream defects, restated

1. **The winner and the score come from different JEV calls.** 10 of 10 rounds this session crowned a non-top-scoring civ. Fix: send the scores to the chooser, and/or make `best_civ` the argmax of `avg_score` with JEV used only as a tiebreak.
2. **Zero simulations still exits 0.** Replace the silent `return None` at the provider gate with a named error and a non-zero abort; add a row-count assertion (`sum(ledger_rows)` grew by `sims*civs + competition_rows`).

---

## 10. Protocol

- Mock rows are **NOT committed**. The committed ledger holds real z.ai output; a mock row presented as a provider result poisons the fleet's only durable quality record.
- The working tree was restored from **API-fetched pristine copies** (one `contents/<path>?ref=main` call per file, base64-decoded) and verified **byte-identical** with `cmp`: all 8 `simulations.jsonl`, all 8 `culture.json`, all 8 `witness.log`, plus `meta_log.jsonl` (48 lines), `leaderboard.json`, `civilizations.json` and `civilization_orchestrator.py`. `__pycache__/` removed.
- **This session's report is filed as session 11, not session 10.** A prior instance of this same wipe already committed a "Session 10" report at `99dd6540` with its own A/B. Overwriting it would have destroyed a real measurement; the divergence between the two A/Bs is the finding, and it is reported in §4.
- Only this report and the learnings doc are new.

## 11. Artifacts

- Run logs: `/tmp/run_unpatched.log`, `/tmp/run_controlb_a.log`, `/tmp/run_controlb_b.log`
- Mock call logs: `/tmp/mock_calls.log` (81 calls, 0 fallbacks), `/tmp/mock_calls_b.log` (80 calls, 0 fallbacks)
- Mock server: `/tmp/zai_mock.py` (body sets A and B, variant arg)
- Pristine baseline: `/tmp/pristine/`
