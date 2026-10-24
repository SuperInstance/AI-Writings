# Civ Orchestrator — durable cross-session lessons

The authoritative operational RUNBOOK lives in the repo at
`cellular-first-design/code/civilizations/RUNBOOK.md`.
This file holds the short, high-signal rules that survive a sandbox wipe.

## Session 125 (2026-10-24) — a 5-sample point cannot narrow a rate; only the direction is stable

**Chooser vs `avg_score` argmax: 4/5 (80 %).** `civ-precise` was argmax in 4/5 and won **5/5**.
Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) →
0/5 (124) → **4/5 (125)**.

**NEW — consecutive sessions swung 0/5 → 4/5 on the same mock and the same scorer.** A five-sample
point carries almost no information about a rate. The only stable signal is the **direction**:
in **all 6** disagreements across 116/118/119/120/122/123/125 the chooser picked a
**lower**-scoring candidate. Report the fraction as a sample; report the direction as the finding.

**Mock non-degeneracy: 5/5 competition prompts at 8/8 distinct previews** — the **seventh clean
measurement** (118, 120, 121, 122, 123, 124, 125). Pre-flight again saved the run: 4 civs → 4
distinct seeds AND 4 distinct previews, `[mock-zai seed=…]` present, 0 tracebacks.

**`civ-grounded` is the low-relevance civ** — 30 consecutive sessions (95-125). Last on lifetime
`avg_score` (1.2378), `alignment` (1.4906), `quality` (0.6064), `relevance` (834.13),
`relevance_per_sim` (1.193). The **alignment** gap is the structural one: **0.3700** below the
next civ, vs **0.0334** on quality — 11x wider. Alignment is what the chooser selects on, so
Grounded fails to *embody a distinctive voice*: a voice failure, not a prose failure.

**New environment fact: the GitHub code-search API rate-limits hard** (0/10 on `code_search`
while `core` had 3878/5000). A rate-limit body renders as "no results" for every query at once.
Locate repos with `GET /search/repositories` and `GET /user/repos`, never code search — and never
read a rate-limit body as a negative result.

## Session 121 (2026-10-24) — the mock was REBUILT, and the quality level moved anyway

**Rebuild the mock, then re-run the pre-flight.** This session's `/tmp` was wiped, so
`/tmp/mock_zai.py` was rebuilt from scratch — exactly when the session-112 index-wrap bug
(`seed[i*2:i*2+2]` -> empty for `i>=4` -> HTTP 500) is likely to reappear. A crashing mock
still leaves a **listening socket**, so a port/200 probe looks healthy. The pre-flight that
catches it: probe the **live** mock with the exact long cultural prompt for 3 different civs,
assert **3 distinct seeds**, and `grep -c Traceback /tmp/mock_zai.log` -> **0** — *before*
launching the batch. Measured: 3/3 distinct, 0 tracebacks, 8/8 distinct previews on all 5
competition prompts (third clean measurement: 118, 120, 121).

**The `quality` collapse is a LEVEL, not a property of the mock.** Session 119 measured
`quality` 0.009-0.030; session 120 measured 0.106-0.446; **session 121 measured 0.010-0.37
(mean 0.0193)** — under the *same* mock, which was **rebuilt**, not reused. So the collapse
does not reproduce: it is a level that moves. The durable rule survives and is re-confirmed
— **compare cross-civ spreads, not absolute levels, before ranking on a dimension.**
`alignment` again carried the widest spread (per-prompt 0.96-2.82) and is again the axis the
chooser selects on.

**Chooser vs `avg_score` argmax: 4/5 (80 %).** `civ-precise` was argmax in 5/5 and won 4/5.
Clean-mock series: **0/5 (118) -> 3/5 (119) -> 1/5 (120) -> 4/5 (121)**. Five-sample points
cannot narrow a rate — the honest claim is *somewhere in 0-80 %*. What survives every session:
the chooser is **not** a pure argmax, and in all 4 disagreements across 116/118/119/120 it
picked a **lower**-scoring candidate.

**Gotcha: `civilizations.json` is multi-line pretty-printed JSON, not JSONL.** A line-based
`json.loads(l)` raises `JSONDecodeError: line 2 column 1`. Use
`json.loads(open(path).read())`. The civ ledgers *are* JSONL and parse fine, so the error
looks like ledger corruption when it is not.

## Session 118 (2026-10-24) — the session-117 mock degeneracy is FIXED

The Control B mock seeded from the first 8 alnum chars of the message. The cultural prompt
opens with the **civ-invariant** prefix `You are a voice in the tradition of "…`, whose first
8 alnum chars are `YouAreA` for every civ => seed `youareav` for all 8 => all 8 candidates
byte-identical => the meta-GAN chooser was breaking a perfect tie.

**Fix:** seed from `md5(whole_message)[:8]`. Keep the session-112 index-wrap
`seed[(i*2)%8:((i*2)%8)+2]` (a plain `seed[i*2:i*2+2]` crashes on `i>=4`).

**Mandatory diagnostic before trusting any competition result:**

```python
assert len({r["content_preview"] for r in new_competition_rows}) == 8   # one prompt, 8 civs
```

Session 118 measured 8/8 on all 5 prompts and 40/40 across the run — the first clean
measurement in the fleet's history.

**Consequence:** the long-standing "chooser vs `avg_score` argmax ~15 %, replicated 29
consecutive times" was measured under the degenerate mock and is **void**. The clean value is
**0/5 (0 %)**. `civ-poetic` was argmax in 3/5 and near-argmax in a 4th, and won **0/5**.
Session 116's "chooser picked the lowest-scoring candidate" is re-confirmed under a working
mock — no longer an artifact.

## Standing findings

- **`civ-grounded` (The Grounded) is the low-relevance civ** — last on lifetime `relevance`
  (813.83), `relevance_per_sim` (1.2350), `avg_score` (1.2794), `quality` (0.6386) and
  `alignment` (1.5600). The **alignment** gap is the structural one: **0.3995** below the next
  vs a 0.037 margin on quality. `alignment` is the dimension the meta-GAN *selects* on, so
  the civ fails to *embody a distinctive voice*, not merely to write weakly. 23 sessions (95-118).
- **`civ-formal`** = the low-novelty axis (novelty 1.4673, lowest; alignment healthy).
- **The two stable inverses:** `civ-poetic` = 1st on quality (1.126) / `avg_score` (1.947) but
  last on `win_rate` (0.017); `civ-precise` = best `win_rate` (0.490) but 5th on `avg_score`.
- **Extinction risk NONE** — threshold -10, lowest relevance +813.83 (81x above floor).
  Registry 8, `max_civs` 12. Extinction/birth only runs under `--loop`.
- **Counter gap is per-civ uneven**, not a uniform offset (+16..+63). `save_state()` has no
  lock => `relevance_per_sim` is not recomputable from the ledger by an auditor.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs**, not a dict. A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies.
- **Never treat `win_rate` as a quality metric** — it is a *selection* metric.

## Environment rules (re-confirmed, 5th session running)

- **NAS EDQUOT is total.** *No* write to `/workspace` succeeds — even a 5-byte `echo` yields a
  0-byte file that `ls` still lists, and `cp` exits 0. `mkdir` and `ln` work. The only way in
  is the **symlink bridge**.
- **Clone to `/tmp`** (overlay, ~28 G free; NAS quota does not apply), then
  `ln -sfn /tmp/ai-writings/cellular-first-design /workspace/repos/ai-writings/cellular-first-design`.
  Verify by **inode identity** (`stat -L -c '%d:%i'` on both sides + `-ef`), not by `ls`.
- **Do not flatten the clone.** The symlink target is the *nested* `cellular-first-design` dir.
  A 5/5 consistent `ls` failure = wrong target; an intermittent one = mount race. Retry before
  concluding the tree is gone.
- **Upstream is `SuperInstance/AI-Writings`** (the `ai-writings/cellular-first-design` slug
  404s; the API is case-insensitive). `gh` is **not installed** — use
  `GET /search/repositories?q=...` and `GET /user/repos` with `GITHUB_TOKEN`.
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** (script reads the former,
  sandbox stores the latter). Unset => JEV degrades to the 2.0 default and every score is
  constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first.
  Control B needs **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is absent** from env and the secret store; z.ai returns 401 (endpoint healthy,
  credential gap). JEV is live.
- **Tool timeout 30 s < orchestrator run ~50 s.**
  `ps` + the log. Kill the mock by **exact args** (`python3 /tmp/mock_zai.py`) — two pids.
- **A 200 on a mock probe is not proof the mock is correct.** Probe with the exact long
  cultural prompt and `grep -c Traceback` the mock log.

## Verification pattern (assert on rows, never on exit code)

All failure modes are silent with exit code 0 — a missing token makes `call_provider()` return
`None`, `run_simulation()` return `None`, and the competition short-circuit on
`if not results: return None`.

| Assertion | Expected for `--sims 5 --prompts 5` |
|---|---|
| per-civ `simulations.jsonl` delta | **+10** each (5 sim-phase + 5 competition-phase) |
| total new ledger rows | **80** |
| `meta_log.jsonl` delta | **+5** |
| `Winner:` lines | **5** |
| rows with `[mock-zai` prefix | **80** |
| rows with a JEV `error` key | **0** (this is what proves JEV really scored) |
| distinct `content_preview` per prompt, 8 civs | **8/8** (the session-117 degeneracy guard) |

Isolate this run's rows by **count from the end of the file** (`rows[-delta:]`), not by a `ts`
cutoff — prior sessions left mock rows behind, so a `ts >=` filter pulls in history.

## Session 132 (2026-10-24) — run-level rank divergence is NOT the signal; the competition gap is

**Chooser vs `avg_score` argmax: 2/5 (40 %).** `civ-precise` won **5/5**; `civ-poetic` was argmax in
**2/5** and won **0/5**. Clean-mock series: 0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) →
3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) → 3/5 (127) → 2/5 (128) → 4/5 (130) → **2/5 (132)**.
Fourteen five-sample points cannot narrow a rate — the honest claim is *somewhere in 0–80 %*. What
survives every session: the chooser is **not** a pure argmax, and in **all 3** disagreements this
session it picked a **lower**-scoring candidate — the stable direction across
116/118/119/120/122/123/125/131 (**11th** consecutive session with that direction).

**New: run-level `avg_score` and `alignment` rankings can be IDENTICAL (ρ = +1.000).** This session
measured Spearman ρ(avg_score, alignment) = **+1.000** at run level (all 8 civs in the same order on
both axes) and +0.738 at lifetime level. So a run-level divergence between "the score the chooser
sees" and "the composite the leaderboard ranks by" is **not guaranteed** — do not look for it. The
divergence that *is* real lives at the **competition** level: `civ-precise` won 5/5 while ranking
**4th** (0.273 vs poetic 0.587) on prompt 0 and **3rd** (0.267 vs poetic 0.463) on prompt 1. Measure
the chooser gap **per competition prompt**, not as a run-level rank correlation.

**The chooser tracks `alignment`, and `civ-precise` wins on exactly that axis:** 1st of 8 on lifetime
`alignment` (2.3553) but only 3rd on lifetime `avg_score` (1.5193); swept 5/5. Its mirror,
`civ-poetic`, is 1st on lifetime `avg_score` (1.7519) and 2nd on `alignment` (2.3025) but last on
`win_rate` (0.013, 5/368) and won 0/5. **Never treat `win_rate` as a quality metric.**

**`civ-grounded` is the low-relevance civ — 35 consecutive sessions (95–132).** Last on lifetime
`avg_score` (1.1660), `alignment` (1.3865), `quality` (0.5637), `relevance` (862.47) and
`relevance_per_sim` (1.122). The structural gap is `alignment`: **0.9687** below the field, versus
**0.4019** on quality — **2.4× wider** (the gap ratio has widened from ~11× in sessions 125–131 as the
field's alignment scores drifted up). Alignment is the dimension the meta-GAN selects on ⇒ a **voice**
failure, not a prose failure.

**`civ-therapist` took the run-level low this session — but it is a WATCH axis, not a finding.**
8th of 8 on run `avg_score` (0.1117) **and** 8th of 8 on run `alignment` (0.0240), with the field's
worst run/lifetime alignment ratio (0.014). But its **lifetime** `avg_score` is 5th of 8 (1.3942) and
lifetime `alignment` 7th of 8 (1.7119) — a mid-field citizen. **Per-run low ⇒ watch axis.** The
session-121/122/123 rule stands: *do not promote a single-run low without a lifetime-level gap.*
`civ-formal` = low-**novelty** axis (lifetime novelty 1.4121, last; alignment 1.9875 healthy);
`civ-engineer` = 5th of 8 on both run and lifetime `avg_score`, still no lifetime gap — do not promote.

**Verification pattern that held (9th clean mock measurement — 118, 120–123, 125, 131, 132):** per-civ
Δ = **+10** (5 sim-phase + 5 competition-phase), `meta_log` Δ = **+5** (393 → 398), `Winner:` lines =
**5**, **80/80** rows `[mock-zai`-prefixed, `provider={zai}`, **0** rows with a JEV `error` key, and
**5/5** competition prompts at **8/8 distinct previews AND 8/8 distinct seeds**.

**`/tmp` was wiped again ⇒ the mock was rebuilt from scratch, so BOTH historical mock bugs had to be
re-applied on rebuild**: the session-112 index wrap `seed[(i*2)%8:((i*2)%8)+2]` and the session-118
md5-of-whole-message seeding. **Pre-flight with the exact long cultural prompt** (8 civs → 8 distinct
seeds AND 8 distinct previews, 1174–1574-char bodies, `[mock-zai seed=…]` present, 0 tracebacks) —
a one-word probe cannot reach the `i>=4` path that crashes. A crashing mock still leaves a listening
socket, so a port/200 check is **not** proof of correctness.
