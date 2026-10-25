# Session 154 — clean mock #24; chooser-vs-argmax 3/5 (60 %); Grounded holds the low for the 50th session (2026-10-25)

**Run:** 8 civs x 5 sims + 5 competition prompts, `--sims 5 --prompts 5 --providers zai`,
Control B mock provider bridge, JEV live. Upstream baseline `1162a3a` (session 153).

**All 97 verification checks PASS.** Per-civ ledger delta **+10** x 8 = **80 rows**
(5 sim-phase + 5 competition-phase per civ), `meta_log.jsonl` **503 -> 508** (+5),
**5** `Winner:` lines, **0** JEV `error` keys, **0** rows with the 2.0/2.0/2.0 fallback
triple, **80/80** rows carry the `[mock-zai seed=…]` prefix with `provider=zai`, **40/40**
distinct seeds, **0** `(civ, cultural-prompt)` combos with >1 seed, **8/8** distinct
`(quality, novelty, alignment)` triples per civ, `leaderboard.json` rewritten at 01:23:31Z,
`git status --porcelain` = **18** modified (8 ledgers + 8 cultures + `meta_log.jsonl` +
`leaderboard.json`).

**JEV liveness proved at the score level, not just the socket level:** the 80 new rows carry
**80 distinct `(quality, novelty, alignment)` triples** (quality 0.02-1.18, novelty
2.28-2.81, alignment 0.43-2.90) and **39 distinct confidence values** over 0.35-0.98. A
silent 2.0 default would produce one repeated triple and constant 0.5 confidence.

**Mock rebuilt from scratch** (`/tmp` was wiped) => the known mock bugs were live again in
the naive rebuild: the session-112 index wrap (`seed[i*2:i*2+2]` -> empty for `i>=4` ->
HTTP 500 with the socket still open), the session-118 md5-of-whole-message seeding, and
the session-145 literal-`{}` placeholder. The session-144 `Connection: close` was re-applied
too. Pre-flight: **40/40 distinct seeds, 40/40 distinct previews, 0 tracebacks**, cultural
prompt lengths 167-209. **The 24th clean mock measurement.**

**Chooser vs `avg_score` argmax: 3/5 (60 %).** `civ-precise` won **3** of 5 prompts
(cell, ternary, JEV-oracle), `civ-formal` 1 (bookkeeper), `civ-therapist` 1 (witness log).
Disagreement count is **2** — both **negative** delta (winner below argmax), which is
consistent with the standing "the chooser takes the LOWER-scoring candidate" finding.
Clean-mock series: 0,3,1,4,4,3,0,4,4,1,2,4,4,0,2,4,1,4,0,**5**,**3** (s.118-154) - 24
five-sample points cannot pin a rate; the honest claim is *somewhere in 0-100 %*. The
historical "chooser vs argmax ~15 %" figure was measured under the **degenerate** mock
(session 117) and is **void**.

**`civ-grounded` (The Grounded) remains the low-relevance civ - 50 consecutive sessions
(95-154).** Last of 8 on lifetime `avg_score` (1.0328) and lifetime `alignment` (1.1578),
and last of 8 on **both** this-run counterparts (`avg_score` 1.0813, `alignment` 0.7150).
The label did **not** rotate: last before the run (970.72 / 0.992) and last after it
(981.54 / 0.992). Alignment is the dimension the meta-GAN *selects* on, so Grounded fails to
*embody a distinctive voice* - a **voice** failure, not a prose failure. The absolute gap
to the next-lowest civ on the lifetime axis: **alignment 0.4240** (vs `civ-therapist`
1.3911) versus **quality 0.0402** (vs `civ-formal` 0.4881) - the alignment gap is ~10x the
quality gap. **Quote the absolute gaps, not the ranks.**

**This run is a new low for Grounded on the two axes that matter.** Grounded's this-run
`quality` (0.1180) and `novelty` (2.4110) are both the lowest of 8 — in session 153 Grounded
was last on `avg_score`, `alignment` and `quality` but **not** on `novelty`
(`civ-formal` held that axis at 1.3868 lifetime). This session `civ-formal` still holds the
**lifetime** novelty low (1.3868), so the novelty axis has *not* structurally rotated; only
the this-run snapshot overlaps.

**`civ-precise` and `civ-poetic` remain the two stable inverses.** `civ-poetic` is 1st on
lifetime `quality` (0.8056) and last on `win_rate` (0.012). `civ-precise` is 1st on
`win_rate` (0.573) and 2nd-lowest on `quality` (0.5510). Both are **selection** failures,
not quality collapses.

**The counter gap is NEGATIVE and long-standing:** `culture.json` `relevance_score` minus
the ledger's `avg_score` sum is **-609.92** total
(civ-whimsical -173.14, civ-poetic -96.80, civ-formal -85.53, civ-grounded -84.35,
civ-mythic -51.11, civ-engineer -44.24, civ-therapist -42.11, civ-precise -32.63). The
per-civ values are a **fixed offset** (deltas <= 0.01 across a run) - `save_state()` has no
lock, so `relevance_per_sim` is **not recomputable from the ledger** by an auditor. The
sign was computed from this run's data, not copied from the previous report.

### Environment

- NAS **100 % full** again (600 G/600 G, 0 bytes free). `git clone` straight into
  `/workspace/repos/...` died with `error: .../.git/description: close error: Disk quota
  exceeded`. Cloned to `/tmp` (overlay, 28 G free) and built the **symlink bridge**;
  verified by inode identity (`129:2652` on both sides) and `-ef`. The symlink points at the
  **nested** `cellular-first-design` directory, not the repo root.
- **ZAI credential gap re-confirmed (17th session):** `ZAI_TOKEN` is absent from the env and
  from all 8 sandbox secrets. The available z.ai-format key is `MOTHQUANTUM_TOKEN`
  (`moth_E…`, 27 chars), but the script reads `ZAI_TOKEN`; against both
  `api.z.ai/api/coding/paas/v4/chat/completions` and `api.z.ai/api/paas/v4/chat/completions`
  it returns **401 token expired or incorrect** (endpoint healthy => credential gap, not an
  outage). Control B therefore used a local mock bridge with **both** `ZAI_TOKEN` (non-empty
  placeholder) **and** `ZAI_URL_OVERRIDE`; `ZAI_URL_OVERRIDE` alone is dead code because the
  token gate returns first.
- `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN` (script reads the former).
  JEV answered live: `model=jev-1.14.0`.
- Run **detached** (`setsid nohup timeout -s KILL 300 … &`) and poll the log; a 30 s tool
  timeout is shorter than the ~50 s wall time and kills the run mid-flight. The mock server
  was started the same way and killed by PID matched on **argv exactly**
  (`python3 /tmp/mock_zai.py`), never `pkill -f mock_zai` (self-match).

### Standing caveats

- The mock is a **deterministic text generator**, not an LLM. Its previews are synthetic;
  only the **JEV scoring** of them is real. Do not read the mock's prose as evidence of
  anything about the civs' voices.
- Preview-distinctness is **not** a valid mock-integrity check at 80-row granularity: 8 civs
  x 5 canon prompts = **40 distinct cultural prompts**, so 80 rows carry 40 distinct
  previews and 40 distinct seeds. Assert at the **cultural-prompt** granularity
  (40 distinct seeds, 0 cultural prompts with >1 seed) — not at the row granularity.
- Competition `ts` carries no ordering: all five rows share the same wall-clock to the
  microsecond. Do not reconstruct a per-prompt timeline from it.
- `meta_log.jsonl` `results` is a **list of `[civ_id, score]` pairs**, not a dict. A
  dict-shaped reader silently yields 0 % agreement and empty pick tallies.
