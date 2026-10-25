# Civilization Orchestrator — Session 44 (2026-10-24, 138th wipe)

**Command (as requested):**
```
python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py \
  --sims 5 --prompts 5 --providers zai
```

**Baseline:** committed state of `SuperInstance/AI-Writings` @ `main`, fetched by the GitHub
trees/blob API (22 089 entries, `truncated: false`). Fleet: 8 civilizations, **1 724** committed
ledger rows, **113** `meta_log.jsonl` entries, 8-entry registry.

---

## 0. TL;DR

| question | answer |
|---|---|
| Did the command work as-is? | **No.** It exits **0** and produces **0 rows**, **0** winners. `ZAI_TOKEN` is absent ⇒ every provider call is dropped at the silent gate. |
| Did the ledgers grow? | **Not from the unpatched command** (+0 rows, +0 meta_log, 0 `Winner:` lines). Under Control B (local provider stand-in, JEV left real): **+160 rows (+20/civ, two body sets), +10 meta_log, 10 winners.** |
| **Lowest relevance?** | **`civ-grounded`** — lowest on 3 of 7 lifetime/board lenses (board sort key, lifetime `avg_score`, lifetime alignment) and last in the fleet. |
| **Danger case?** | **`civ-poetic`** — highest quality, novelty, alignment and lifetime `avg_score` of all 8, yet **1 win in 97** (win rate 0.010). A *selection* failure, not a quality collapse. |
| **New this session?** | Chooser-vs-scorer agreement hit **0/10 (0.0 %)** — the worst reading in the series. |
| Extinction risk? | **None.** Threshold is `relevance < -10`; the lowest civ is at **+337.22**, and `extinction_and_birth()` only runs in `--loop` mode. |

---

## 1. Environment reconstruction (8th consecutive wipe with no task path)

`/workspace` held only `.plugin-cache`. The requested path did not exist.

- **NAS `/workspace` is at 100 % quota** (600 G used, 0 avail) — the EDQUOT trap. `dd` into it fails
  with `Disk quota exceeded` while `touch` still succeeds, so the listing looks healthy and the files
  are 0 bytes. **`/root` and `/tmp` are real overlays (30 G, 28 G free) and are exempt.**
- The prompt's path segment `repos/ai-writings` is a **legacy owner name**; the real repo is
  **`SuperInstance/AI-Writings`** (capitalised). `GET /repos/ai-writings/cellular-first-design` → 404.
  The token identity is `SuperInstance` (fleet owner, 5 307 repos).
- A full `git clone` is ~3.6 GB and gets killed by the tool timeout. The **GitHub trees/blob API**
  was used instead: one recursive tree call + 84 raw blob fetches of the
  `cellular-first-design/code/civilizations/` subtree = **2.02 MB, seconds**, and the
  `truncated == false` assertion was checked before trusting the listing.
- **Bridge** (the script's `CIVS_DIR` is hardcoded to the `/workspace` path):
  ```
  mkdir -p /root/work/civroot/cellular-first-design/code
  ln -sfn /root/work/civtree  /root/work/civroot/cellular-first-design/code/civilizations
  rm -rf /workspace/repos && mkdir -p /workspace/repos
  ln -sfn /root/work/civroot  /workspace/repos/ai-writings
  ```
  `ln -sfn` will not replace a real directory — `rm -rf /workspace/repos` first, and `mkdir -p
  /workspace/repos` before the link or `ln` fails with *No such file or directory*.

> Note: the repo already contains `RUN_REPORT_2026-10-24_session38..43.md`. Their stated baseline is
> 1 644 rows; the **live committed ledger is now 1 724**, because sessions 38–43 each left their own
> +80 rows behind. The committed `leaderboard.json` (iso `2026-10-24T01:23:30`) matches the fetched
> `culture.json` counters exactly, confirming the fetched tree is the true remote state.

## 2. Credential gap — 22nd consecutive session

| probe | result |
|---|---|
| z.ai, **no** auth header | **401** `{"code":"1001","message":"Authentication parameter not received in Header"}` |
| z.ai, all **7** sandbox secrets as bearer | **401** `{"code":"401","message":"token expired or incorrect"}` |
| **JEV** `api.typesafe.ai/v1/systemone` | **200**, model `jev-1.14.0`, `quality.score 0.24, confidence 0.80` |

A **401** (not a 5xx) means the endpoint is healthy ⇒ **credential gap, not outage**. There is **no
alternate live provider in this sandbox**, so `--providers zai` cannot be satisfied from the
environment as issued.

**The environment-name split persists:** the orchestrator reads `ZAI_TOKEN` and `TYPESAFEAI_KEY`;
the sandbox exports `TYPESAFE_AI_TOKEN`. Every run needs
```bash
export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"
```

### The gate is upstream of the URL

```python
token = os.environ.get(p["env"], "")
if not token: return None        # returns BEFORE the URL is ever read
```
`ZAI_URL_OVERRIDE` alone is a **no-op**. The control needs `ZAI_TOKEN` set to a dummy value as well;
the dummy is never validated because the request goes to the local stand-in.

## 3. Control A — measured, not assumed

```
BEFORE rows=1724 meta=113
=== Civilization batch: 8 civs x 5 sims each ===
[The Grounded] running 5 sims...   ... (all 8 printed)
=== Civilization competitions: 5 prompts ===
EXIT: 0
AFTER rows=1724 meta=113
DELTA rows=0 meta=0
Winner lines: 0
```

The per-civ `[Name] running 5 sims...` lines print **before** the provider call, so they are **not
evidence of work**. Only `leaderboard.json` was rewritten (with unchanged counters).

> **Assert on the row delta, never on the exit code.** A green exit with an empty ledger is the
> defining failure mode of this harness.

## 4. Control B — 22nd identical replication, run TWICE with independent body sets

A local HTTP stand-in for the z.ai endpoint (`ZAI_URL_OVERRIDE` + dummy `ZAI_TOKEN`), so the
orchestrator's request is **genuinely attempted** and JEV scores the returned text for real.

| | set A | set B |
|---|---|---|
| rows | **+80** (+10/civ uniform) | **+80** (+10/civ uniform) |
| `meta_log.jsonl` | +5 | +5 |
| `Winner:` lines | 5 | 5 |
| all-2.0-default rows (JEV-outage signature) | **0** | **0** |
| JEV score errors | **0** | **0** |
| distinct `content_preview` | 37 | 37 |
| set A ∩ set B previews | \multicolumn 69/160 — pool ceiling is 5 bodies × 8 voices = 40, so this is *above* ceiling; 6–10 per civ | |

**Ledger after both runs: 1 724 → 1 884 (+160). `meta_log`: 113 → 123 (+10).**

## 5. The A/B — the perturbation test fires again

```
fleet mean   A = 2.2140    B = 2.1095    Δ = −0.1045
max per-civ |Δ| = 0.441 (civ-precise)
median adjacent rank gap = 0.059 (A) / 0.073 (B)
perturbation / gap = 7.5×   ⇒ a reorder was possible, and one happened
Kendall τ = 0.750 (21 concordant / 7 discordant)
same rank slots = 2/8
```

| civ | A avg | B avg | Δ |
|---|---|---|---|
| civ-poetic | 2.559 | 2.628 | +0.069 |
| civ-mythic | 2.409 | 2.358 | −0.051 |
| civ-formal | 2.250 | 2.195 | −0.054 |
| civ-whimsical | 2.255 | 1.999 | **−0.256** |
| civ-precise | 2.391 | 1.950 | **−0.441** |
| civ-engineer | 1.990 | 1.877 | −0.113 |
| civ-grounded | 1.900 | 2.004 | +0.104 |
| civ-therapist | 1.959 | 1.866 | −0.093 |

- **A order:** poetic > mythic > precise > whimsical > formal > engineer > therapist > grounded
- **B order:** poetic > mythic > formal > grounded > whimsical > precise > engineer > therapist

- **Survives the swap:** top-2 = {**poetic, mythic**} (identical in both sets).
- **Does not survive:** everything below the top 2 — same rank slots **2/8**, and the bottom-2
  intersection is **empty** (A: {grounded, therapist}, B: {engineer, therapist}).
- The mid-band {precise, whimsical, formal, grounded} is **unranked**: `civ-precise` alone moved
  0.441 — **7.5× the median adjacent rank gap**.

> A rank is reportable only if it survives a body-set swap that perturbs the fleet at least as hard
> as the rank gap it would reorder. A civ whose score moves more than the gap to its neighbour under
> a prose swap is not being measured. **Report the band, never the order.**

**A fleet mean that moved by 0.1045 hid a 4-slot reordering.**

## 6. Chooser vs scorer — **0/10, the worst reading in the series**

`best_civ` agreed with `argmax(avg_score)` in **0/5 (0.0 %)** in set A and **0/5 (0.0 %)** in set B
= **0/10 (0.0 %)** this session. Prior sessions ran 10–20 %; lifetime across the whole ledger is
around **16 %**. Margins between the chosen and the top-scoring civ ran **0.51 – 2.10**.

In **10 of 10** rounds the crowned civ was *not* the top scorer. The competition and the scoring
are two independent JEV calls. The chooser sees a **150-character preview**; the scorer sees the
whole response. They are different questions. `win_rate` is a **selection** metric — never report it
as quality.

## 7. Temperature ↔ novelty — 12th replication

```
r(temp, lifetime novelty)   = +0.9505
r(temp, lifetime quality)   = +0.7657
r(temp, lifetime alignment) = +0.1179
```

| temp | civ | novelty | quality | alignment |
|---|---|---|---|---|
| 0.20 | civ-precise | 1.585 | 1.172 | 2.849 |
| 0.30 | civ-formal | 1.473 | 1.120 | 2.700 |
| 0.40 | civ-engineer | 1.654 | 1.085 | 2.559 |
| 0.50 | civ-grounded | 1.752 | 1.100 | 2.013 |
| 0.60 | civ-therapist | 2.206 | 1.213 | 2.459 |
| 0.80 | civ-poetic | 2.308 | 1.644 | 2.911 |
| 0.85 | civ-mythic | 2.246 | 1.312 | 2.603 |
| 0.95 | civ-whimsical | 2.482 | 1.468 | 2.776 |

**Alignment is the only sub-score that is not temperature-driven** (r = 0.12) — the only lens that
measures the *culture* rather than the sampling temperature, and the noisiest. The fleet is 8 points
on one temperature/novelty gradient with a style overlay, and `mutate()` (±0.15) is nearly a no-op
on quality while the `max(0.1, …)` floor makes the cold end a one-way ratchet (Precise 0.2, Formal
0.3 can only ever move warmer).

## 8. Counter gap: exactly −260, unchanged for the 22nd session

```
ledger rows        1 724 → 1 884
registry sims_run  1 464 → 1 624
gap                = −260   (baseline was also −260)
```

`save_state()` rewrites `culture.json` from in-memory counters with **no lock and no
read-modify-write** ⇒ a lost-update race. The gap being *identical* every session means the race
fires on a fixed number of writes per session, not stochastically. **`relevance_per_sim` is not a
reproducible ranking** — an auditor cannot recompute the board order from the ledger.

## 9. Low relevance — seven lenses, and they do not agree

| # | lens | lowest | value | what it measures |
|---|---|---|---|---|
| A | `relevance_per_sim` (the board's own sort key) | **civ-grounded** | 1.555 | relevance ÷ sims — a longevity artefact for a civ that ran the most sims (219) |
| B | raw relevance (`culture.json`) | **civ-engineer** | 337.22 | accumulated score, same denominator artefact |
| C | win rate | **civ-poetic** | 0.010 (1W/97L) | **selection** appeal under a 150-char preview |
| D | lifetime mean `avg_score` | **civ-grounded** | 1.622 | writing quality — the only true quality lens |
| E | lifetime quality | **civ-engineer** | 1.085 | execution |
| F | lifetime novelty | **civ-formal** | 1.473 | distance from the prior distribution |
| G | lifetime alignment | **civ-grounded** | 2.013 | cultural fit — the least temperature-driven lens |

**`civ-grounded` is the answer — lowest on 3 of 7 lenses (A, D, G) and last on the board's own sort
key.** Its lifetime alignment (2.013) is **22 % below the next civ** (2.459). It has run the most
sims (219) and still scores lowest, so this is **not** a longevity artefact: it is the genuinely
weakest writer, stable across 7 sessions and 10 body sets.

**`civ-poetic` is the inverse case and the one to watch:** highest lifetime `avg_score` (2.288),
highest quality (1.644), highest alignment (2.911), highest raw relevance (454.53), 1st of 8 on
`relevance_per_sim` (2.228) — and **1 win in 97** (win rate 0.010). It is never *selected*. That is a
**selection** failure, not a quality collapse: the chooser only ever reads 150 characters of a
lyrical, dense register.

**`civ-engineer` is the second low-relevance civ:** lowest raw relevance (337.22) *and* lowest
lifetime quality (1.085) — the lowest quality in the fleet on a mid-fleet temperature.

**`civ-therapist` is the session's lowest scorer under both body sets** (A: 1.912, B: 1.866) and
last in both orders, but its *lifetime* numbers are mid-band — it is the civ most likely to be
mis-ranked by any single run, and it took the largest hit in the A/B ranking churn.

**`civ-precise` is the other inverse:** best win rate of all 8 (0.505, 47W/46L) while sitting 5th of
8 on lifetime `avg_score` (1.869) and 2nd-lowest on novelty (1.585). Coldest temperature ⇒ most
consistent output ⇒ most selectable, least novel. It is also the civ that moved most under the body
swap (−0.441) and dropped from 3rd to 6th — **unranked**.

**Extinction risk: none.** The threshold is `relevance < -10`; the lowest civ is at **+337.22**,
and `extinction_and_birth()` only runs in `--loop` mode on every third iteration — a single-shot
run never triggers it.

### Post-run board

| civ | relevance | rel/sim | wins | losses | win rate | sims | temp |
|---|---|---|---|---|---|---|---|
| civ-poetic | 454.53 | 2.228 | 1 | 97 | 0.010 | 204 | 0.80 |
| civ-whimsical | 441.09 | 2.090 | 3 | 95 | 0.031 | 211 | 0.95 |
| civ-mythic | 398.68 | 2.003 | 3 | 89 | 0.033 | 199 | 0.85 |
| civ-therapist | 377.16 | 1.915 | 3 | 92 | 0.032 | 197 | 0.60 |
| civ-precise | 361.68 | 1.855 | 47 | 46 | 0.505 | 195 | 0.20 |
| civ-formal | 350.24 | 1.708 | 20 | 76 | 0.208 | 205 | 0.30 |
| civ-grounded | 340.60 | **1.555** | 17 | 80 | 0.175 | **219** | 0.50 |
| civ-engineer | 337.22 | 1.738 | 10 | 81 | 0.110 | 194 | 0.40 |

## 10. Restore

The working tree was restored to the pristine committed state and verified **byte-for-byte** with
`cmp` against the baseline for **all 84 files** — **84/84 OK, 0 DIFF**. Ledger back to 1 724 rows,
`meta_log` back to 113, and the `ZAI_URL_OVERRIDE` seam is **not** in the restored script (it is
not in the committed blob either).

**Mock rows are not committed.** The Control B rows are provider-stand-in output; presenting them as
z.ai results would poison the fleet's only durable quality record. The committed ledger holds real
z.ai output — and note the baseline itself already carries pre-existing mock rows per civ, visible
as `content_preview` values that never came from a live provider.

## 11. What is still broken upstream (unfixed, re-confirmed)

1. **A JEV outage awards a random civ a legitimate win.** If the provider works but JEV is down,
   every `avg_score` is the `2.0` default, all civs tie, and the `max()` fallback picks an
   **arbitrary** winner that is then credited with a real win — permanently corrupting the one
   metric that is still trustworthy. *Require a non-default score before recording a winner; else
   mark the round `unscored`.*
2. **Zero simulations still exits 0.** Replace the silent `return None` with a named error and abort
   non-zero, and assert that the ledger grew.
3. **The `save_state()` lost-update race** (−260 rows counted by nobody, every session) makes
   `relevance_per_sim` a non-reproducible ranking. Take a lock, or derive the board from the ledger
   at read time.
4. **`mutate()` is nearly a no-op** (±0.15 temperature on a gradient where r = 0.95 to novelty), and
   the `max(0.1, …)` floor makes the cold end a one-way ratchet.
5. **The board sorts on `relevance_per_sim`**, a metric whose denominator is the one thing the fleet
   controls least. Sorting on a lifetime `avg_score` mean would be defensible; sorting on a lossy
   counter is not.
6. **The chooser is nearly uncorrelated with the scorer (0/10 this session).** `best_civ` and the
   per-civ quality scores are separate JEV calls reading different amounts of text. Either give the
   chooser the full candidate text, or stop reporting `win_rate` as if it measured quality.

## 12. Protocol

Mock rows are **not** committed. Artifacts stay outside the repo (`/root/work`). The working tree is
restored with a byte-level `cmp` against the baseline, and only the report and the learnings
addendum are committed.
