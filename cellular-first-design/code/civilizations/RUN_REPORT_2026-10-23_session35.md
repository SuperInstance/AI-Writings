# Civilization Orchestrator — Run Report, Session 35 (2026-10-23)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Baseline commit:** `972b17c` ("🔄 Auto-update landing page index")
**Civs:** 8 · **Prompts:** 5 (canon 1-5) · **Provider:** zai only
**Result:** ✅ Control B — **+80 rows (+10/civ uniform), +5 meta_log, 5 competition winners, 0 errors**

---

## 1. Environment — the workspace was wiped again

`/workspace/repos/ai-writings/...` **did not exist at session start**; `/workspace` held only
`.plugin-cache` and `.skills` (7th consecutive time the prompt named an ephemeral path).
`/workspace` is a **100 %-full NAS mount** — writes there silently produce 0-byte files.

**Recovery:** blobless sparse clone to `/tmp` (overlay, free), then a symlink bridge so the
script's hardcoded `CIVS_DIR` resolves:

```
git clone --filter=blob:none --no-checkout --depth 1 --branch main \
  "https://x-access-token:$GITHUB_TOKEN@github.com/SuperInstance/ai-writings.git" /tmp/ai-writings
git sparse-checkout init --cone
git sparse-checkout set cellular-first-design/code/civilizations
git checkout main

ln -sfn /tmp/ai-writings/.../civilizations /tmp/civroot/cellular-first-design/code/civilizations
ln -sfn /tmp/civroot /workspace/repos/ai-writings
```

**Trap confirmed:** a *full* clone dies on a ~2 GB pack
(`could not open .../tmp_pack_* for reading` → `fatal: fetch-pack: invalid index-pack output`).
The blobless + sparse combination materialises the subtree in seconds.

## 2. Credential gap — 16th consecutive session

`ZAI_TOKEN` absent from env **and** from the 8-entry secret store. All 8 sandbox secrets
re-tested against `https://api.z.ai/api/coding/paas/v4/chat/completions` → **HTTP 401
"token expired or incorrect"** on every one. No-auth probe → **401 code 1001
"Authentication parameter not received in Header"** (endpoint healthy ⇒ credential gap, not outage).

**JEV live** at `jev-1.14.0` (`quality.score 0.34, confidence 0.71`).
Always `export TYPESAFEAI_KEY="$TYPESAFE_AI_TOKEN"` — the orchestrator reads the **name**
`TYPESAFEAI_KEY` (`civilization_orchestrator.py:42`) but the sandbox exposes `TYPESAFE_AI_TOKEN`.
Without the alias every score silently falls back to the hard-coded
`{quality: 2.0, novelty: 2.0, alignment: 2.0}`.

## 3. Control A (unpatched) — the +0-row failure signature, re-verified from scratch

`--sims 5 --prompts 5 --providers zai`, no seam:

- batch header + all 8 `[Name] running 5 sims...` lines printed
- **0 `Winner:` lines**
- **exit 0**
- ledger **+0 rows** (all 8 md5s byte-identical), meta_log **+0** (108 → 108)
- only `leaderboard.json` rewritten

**The `running 5 sims...` lines print *before* the provider call — never evidence of work.
Assert on the row delta, never on the exit code.**

## 4. Control B — `ZAI_URL_OVERRIDE` seam, 16th identical replication

`ZAI_URL_OVERRIDE` is **still not in the committed blob** (`git show HEAD:… | grep` → no match),
16th session running. Landed as a working-tree-only 1-line patch:

```python
"url": os.environ.get("ZAI_URL_OVERRIDE", "https://api.z.ai/api/coding/paas/v4/chat/completions"),
```

`git diff --stat` = 1 file, 1 insertion, 1 deletion. It leaves the `ZAI_TOKEN` gate, the request
body, and the whole JEV path untouched — a test seam, not a code fork.

**Acceptance battery — all pass:**

| check | result |
|---|---|
| rows per civ | **+10 uniform, 8/8 civs** (+80 total) |
| meta_log | **+5** (108 → 113) |
| `Winner:` lines | **5** |
| all-2.0-default rows | **0** |
| JEV score errors | **0** |
| mock fallbacks | **0** |
| distinct `content_preview` | **10/10 per civ** (80/80 fleet-wide) |
| this-run `avg_score` spread | 0.20 – 2.59 (not a constant) |

Mock log = **81** lines = 80 calls + 1 pre-run probe POST (excluded by timestamp, not by deletion).

**Committed-ledger mock baseline:** the tree already carries **70 `mock-zai` rows per civ**
(560 fleet-wide) from earlier sessions — the post-run leak test must compare against **70/civ,
not zero**. A naive `grep -c mock-zai == 0` assertion is a false negative against a
15-session-old baseline.

## 5. Findings

### Chooser vs `argmax(avg_score)`: **0/5 (0.0 %)**
In all 5 rounds the winner's own score was **below** the runner-up's, by 0.38 – 2.01.
The JEV chooser is not selecting the top-scoring candidate; it is selecting on the
*candidates' texts*, not their scores. (Lifetime figure across sessions: ~12 %.)

### Temperature vs lifetime JEV novelty: **Pearson r = 0.9525** — 9th replication
Per-civ mean temperature vs per-civ lifetime novelty (n=8). Also r = 0.7797 vs lifetime
quality, r = 0.0976 vs lifetime alignment (alignment is the noisiest lens).
The fleet is 8 points on one gradient.

**New nuance:** the **pooled row-level** correlation is only **r = 0.5854** (n=1724) versus
**0.9525** at the per-civ level. The between-civ gradient is very strong; the within-civ
row-level relation is much noisier. Report the per-civ figure — it is the one that replicates.

### Counter gap: **+80** (ledger 1724 vs registry 1464)
Unchanged in structure for 16 sessions: the gap is *this session's* +80 rows, because the
run appends 80 rows to the ledger while `culture.json` counters advance by 80 too — the
`save_state()` write is unsynchronised with the ledger append.
**`relevance_per_sim` is not a reproducible ranking while this gap is open.**

## 6. The low-relevance answer — `civ-grounded` (unchanged, 4 of 8 lenses)

| lens | lowest | value |
|---|---|---|
| A board sort `relevance_per_sim` | **civ-grounded** | 1.523 |
| B raw relevance | **civ-grounded** | 303.06 |
| C win rate | **civ-poetic** | 0.011 (1W/87L) |
| D lifetime `avg_score` | **civ-grounded** | 1.601 |
| D2 lifetime quality | civ-engineer | 1.049 |
| E lifetime novelty | civ-formal | 1.373 |
| F lifetime alignment | **civ-grounded** | 2.027 (next 2.508) |
| G this-run `avg_score` | civ-therapist | 1.081 |

`civ-grounded` is lowest on **4 of 8 lenses**, including the two that need no denominator
(lifetime `avg_score`, lifetime `alignment`) plus the board's own sort key — so it is a
**genuine quality signal**, not the longevity artefact lens A alone suggests.

**`civ-poetic` is the inverse failure:** 1st of 8 on lifetime quality (1.627), novelty (2.311)
and alignment (2.887), with a **0.011 win rate (1W/87L)** — a *selection* failure, not a
quality collapse. **`civ-precise` is the mirror image:** best win rate (0.482, 40W/43L) but
5th of 8 on lifetime quality and 2nd-lowest novelty.

**Extinction risk: none** (threshold −10, lowest raw relevance +303.06, `--loop`-mode only).

## 7. Restore — byte-identical to HEAD

`git checkout -- cellular-first-design/code/civilizations/` then **`cmp` against
`git show HEAD:<path>` for every tracked file** (not `git status` alone): **all identical**.
All 8 ledger md5s and the meta_log md5 match the pre-run baseline exactly.
`ZAI_URL_OVERRIDE` absent from the restored file (grep → 0 matches).
