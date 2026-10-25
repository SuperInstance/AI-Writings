# Civ Orchestrator — Run Report (session 131)

**Date:** 2026-10-24 20:53Z  
**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`  
**Provider path:** Control B mock bridge (`ZAI_TOKEN` placeholder + `ZAI_URL_OVERRIDE` → `http://127.0.0.1:8799/...`) — `ZAI_TOKEN` is absent from this sandbox's env and all 8 secrets; the real z.ai endpoint returns `401 token expired or incorrect` against a bogus bearer (endpoint healthy ⇒ **credential gap, not an outage**). **JEV was live**: `POST /v1/systemone` with a malformed `questions` returned `422 {"type":"dict_type"}` — a payload-shape complaint, i.e. the token was accepted.  
**Runner:** 8 civs × 5 sims + 5 competition prompts.

## Verification — all checks PASS

| Check | Expected | Observed | Verdict |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each (5 sim-phase + 5 competition-phase) | +10 × 8 | PASS |
| total new ledger rows | 80 | 80 | PASS |
| `meta_log.jsonl` Δ | +5 | 388 → 393 | PASS |
| `Winner:` lines in stdout | 5 | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` value | `{zai}` only | `{zai}` only | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS (JEV really scored) |
| sim→competition ts gap at index 4 | present in all 8 | 1.10 s – 22.86 s | PASS |
| mock non-degeneracy (8/8 distinct previews per competition prompt) | 5/5 prompts | **5/5** | PASS |
| extinction risk (threshold −10) | NONE | lowest relevance +861.18 (86× above floor) | PASS |

**Mock non-degeneracy is the 8th consecutive clean measurement** (118, 120–123, 125, 131). The pre-flight probe was run against the *live* mock with the exact long cultural prompt before the batch: 4 civs → 4 distinct seeds, 4 distinct previews, 198–201-char bodies, `[mock-zai seed=…]` prefix on every body, **0 tracebacks** in `/tmp/mock_zai.log`. Both historical mock bugs were re-applied on rebuild (session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]`; session-118 md5-of-whole-message seeding) — without either, the bridge 500s on `i>=4` or makes all 8 civs emit identical text and voids every competition result.

## Score dimensions

| civ | lifetime avg | lifetime align | lifetime qual | lifetime novelty | run avg | run align |
|---|---|---|---|---|---|---|
| The Poetic | 1.7697 | 2.3229 | 0.9778 | 2.0083 | 1.3363 | 1.6390 |
| The Whimsical | 1.6401 | 2.0474 | 0.7966 | 2.0765 | 1.0977 | 1.1590 |
| The Precise | 1.5346 | 2.3767 | 0.6636 | 1.5635 | 1.1120 | 1.5060 |
| The Mythic | 1.4887 | 1.8751 | 0.7199 | 1.8712 | 0.8433 | 0.6610 |
| The Therapist | 1.4112 | 1.7343 | 0.6469 | 1.8523 | 0.6727 | 0.5010 |
| The Formal | 1.3461 | 2.0117 | 0.6012 | 1.4253 | 0.7493 | 0.6740 |
| The Engineer | 1.3438 | 1.8850 | 0.6178 | 1.5285 | 0.6040 | 0.3040 |
| The Grounded | 1.1790 | 1.4029 | 0.5706 | 1.5634 | 0.6863 | 0.3090 |

**Cross-civ spreads (not absolute levels).** `alignment` carried the widest spread again — run 1.3350 vs `avg_score` 0.7323, `novelty` 0.6560, and `quality` 0.2060. `alignment` is again the axis the meta-GAN selects on.

## Chooser vs `avg_score` argmax: 1/5 (20 %)

`civ-precise` won **5/5**; `civ-poetic` was argmax in 3/5 and won 0. In **all 4 disagreements the chooser picked a LOWER-scoring candidate** — the stable direction across 116/118/119/120/122/123/125/131. Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → **1/5 (131)**. Nine five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What survives every session: the chooser is **not** a pure argmax, and the direction of disagreements is always *downward*.

## LOW-RELEVANCE CIVILIZATION: `civ-grounded` (The Grounded)

**31 consecutive sessions (95–131) reproduce it.** It is last on **every** lifetime dimension:

| dimension | civ-grounded | next-lowest | gap |
|---|---|---|---|
| avg_score | 1.1790 | 1.3438 (engineer) | 0.1648 |
| alignment | 1.4029 | 1.7343 (therapist) | 0.3314 |
| quality | 0.5706 | 0.6012 (formal) | 0.0306 |

**The structural gap is `alignment`:** 0.3314 below the next civ (1.4029 vs 1.7343) — **the axis the meta-GAN actually selects on**. Versus 0.0306 on quality. This is a **voice failure, not a prose failure**: Grounded writes acceptably but does not *embody* a distinctive voice, so the chooser never selects it. Its tenets ("concrete images, everyday language, specific examples, no abstractions") and voice ("warm, factual") are the least differentiating prompt in the field — every other civ's identity shapes its output; Grounded's identity largely does not.

This run it was also last on lifetime `relevance` (861.18) and `relevance_per_sim` (1.135), and **3rd-worst on this run's `avg_score`** (0.6863) — mid-pack on a single run, bottom of the lifetime table.

**Secondary low axes (distinct from Grounded):**

- **`civ-formal`** — the low-**novelty** axis: lifetime novelty 1.4253, last. Alignment healthy (2.0117), quality fine.
- **`civ-engineer`** — last on this run's `avg_score` (0.6040), `quality` (0.0230) and `alignment` (0.3040), but 6th of 8 on lifetime `relevance_per_sim` (1.324). The session-121/122/123 watch-axis low has now **repeated** — it is still a single-run phenomenon and is NOT promoted to a finding, but it is worth watching for a second consecutive session.
- **`civ-therapist`** — 2nd-lowest lifetime alignment (1.7343) and tied-lowest this run's novelty (1.4850).

**The two stable inverses (unchanged):** `civ-poetic` = 1st on lifetime `avg_score` (1.7697) / `quality` (0.9778) / `alignment` (2.3229) but **last on `win_rate`** (0.014, 5/368) and won 0/5 despite argmaxing 3/5 — a *selection* failure, not a quality collapse. `civ-precise` = the mirror inverse: best `win_rate` (0.540), won 5/5, 1st on lifetime `alignment` (2.3767) but 6th on lifetime `avg_score` (1.5346).

## Standing structural findings

- **Extinction risk NONE** — threshold −10, lowest relevance +861.18 (86× above floor). Registry 8 civs, `max_civs` 12. All 8 still `generation=1`. Extinction/birth only runs under `--loop`.
- **Counter gap per-civ uneven, unchanged**: whimsical +63, grounded +43, formal +42, poetic +37, engineer +22, mythic +20, therapist +17, precise +16. `save_state()` has no lock ⇒ `relevance_per_sim` is **not recomputable from the ledger** by an auditor.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict). A dict-shaped reader silently yields 0 % agreement and empty pick tallies. Winner fields are `winner_civ` / `winner_name`.
- **`civilizations.json` is pretty-printed multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
- **Quality axis is a LEVEL, not a property.** This run's quality was again collapsed (0.023–0.229, spread 0.206) in the 119/121/122/123/125 regime vs session-120's 0.106–0.446. Compare cross-civ spreads, not absolute levels, before ranking on a dimension.

## Environment (durable)

- **NAS EDQUOT still total (17th session).** `git clone` into `/workspace/repos/...` dies with `Disk quota exceeded`; only the symlink bridge works. Target = the **nested** `cellular-first-design` dir. Verified by `stat -L -c '%d:%i'` on both sides (129:3669) + `-ef`.
- **Upstream owner is `SuperInstance`**, not `ai-writings` — `ai-writings/cellular-first-design` 404s. `gh` is not installed (17th session); `GET /user/repos?per_page=100&sort=pushed` with `GITHUB_TOKEN` locates it.
- **Tool timeout 30 s < orchestrator run ~45 s** — launch detached with stdout redirected to a file **and** `< /dev/null`; the launch call itself still hangs, so verify the job with `ps` rather than assuming the launch failed.
- **`ZAI_URL_OVERRIDE` alone is dead code** — the token gate returns `None` first. Control B needs **both** `ZAI_TOKEN` and `ZAI_URL_OVERRIDE`.
- **`TYPESAFEAI_KEY` must be exported** from `$TYPESAFE_AI_TOKEN`; unset ⇒ JEV silently degrades to the 2.0 default and every score becomes a constant.
- **JEV liveness check: HTTP 422 means auth OK, not down** (payload-shape complaint). Contrast z.ai, where 401 on a bogus token means the endpoint is healthy but the credential is absent.
- **Isolate this run's rows by count, not by `ts` cutoff** — prior sessions left mock rows in the ledger, so a `ts >=` filter pulls in historical rows. Use `rows[-10:]` per civ and the known pre-run totals.
- **Do not group this run's rows by `r['prompt']`** to check non-degeneracy: `prompt` is truncated to 80 chars and the sim phase reuses the same 5 canon prompts ⇒ 16 rows per prompt, not 8. Group by the per-civ slot index (`rows[-10:][5..9]`).
- **A `setsid nohup … &` launch whose child inherits stdout blocks the tool call** until the 30 s timeout.
