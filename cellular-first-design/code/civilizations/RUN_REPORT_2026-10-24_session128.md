# Civ Orchestrator — Run Report, session 128 (2026-10-24)

**Command:** `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Mode:** Control B (local mock z.ai bridge) — `ZAI_TOKEN` absent from the sandbox env; the real endpoint returns
`401 token expired or incorrect` (endpoint healthy ⇒ credential gap, not outage).
**JEV:** live (`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; liveness probe → HTTP 422 on a malformed
`questions` payload = auth accepted).
**Status:** ✅ run complete, all verification checks PASS. 8/8 civs at +10 rows, `meta_log` +5, `Winner:` lines = 5.

---

## 1. Run outcome

8 civs × 5 sims, then 5 competition prompts. 5/5 competitions produced a winner; **civ-precise won 5/5**.

| civ | argmax (p1..p5) | winner | agreements |
|---|---|---|---|
| civ-precise | p1,p2,p3,p4 | p1,p2,p3,p4,p5 | 4/4 |
| civ-poetic | p5 | — | 0/1 |

**Chooser vs `avg_score` argmax: 4/5 (80 %).** Clean-mock series now
0/5 (118) → 3/5 (119) → 1/5 (120) → 4/5 (121) → 4/5 (122) → 3/5 (123) → 0/5 (124) → 4/5 (125) → 1/5 (126) →
3/5 (127) → **4/5 (128)**. Eleven five-sample points cannot narrow a rate — the honest claim is *somewhere in
0–80 %*.

**What survives every session:** the chooser is **not** a pure argmax, and the one disagreement this session
again went the same way — p5 chose `civ-precise` at 0.370 over `civ-poetic`'s argmax 0.510, i.e. the
**lower**-scoring candidate. That is the **9th consecutive session** in the series
(116/118/119/120/122/123/125/127/128) in which every observed disagreement picked a lower-scoring
candidate. The run-to-run swing (4/5 → 1/5 → 3/5 → 4/5 on the same mock and the same scorer) confirms a single
5-sample point carries almost no information about a rate; only the *direction* of the disagreements is stable.

---

## 2. Verification (asserted on rows, never on exit code)

`ls -la /workspace/repos/ai-writings/cellular-first-design/code/civilizations/` — tree present, all 8 civ dirs
present; `leaderboard.json` and `meta_log.jsonl` mtimes advanced to 20:05:30.

| check | expected | measured | result |
|---|---|---|---|
| per-civ `simulations.jsonl` Δ | +10 each | +10 × 8 | PASS |
| total ledger rows | 5884 → 5964 | 5964 | PASS |
| `meta_log.jsonl` Δ | +5 | 373 → 378 | PASS |
| `Winner:` lines in log | 5 | 5 | PASS |
| new rows | 80 | 80 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` field | `{zai}` | `{zai}` (all 8) | PASS |
| rows with a JEV `error` key | 0 | 0 | PASS |
| sim→competition ts gap at index 4 | all 8 | 1.04–23.12 s, all 8, all monotonic | PASS |
| competition prompts at 8/8 distinct previews | 5/5 | 5/5 | PASS |

**Mock non-degeneracy: 8/8 on all 5 competition prompts — the tenth clean mock measurement**
(118, 120, 121, 122, 123, 124, 125, 126, 127, 128). The competition ordering and the `avg_score` spread are
**real measurements**, not tie-breaks. 40 distinct seeds across the run's 80 rows.

**Zero JEV `error` keys** is the check that proves JEV genuinely scored rather than silently returning the
2.0 default.

**Pre-flight (before the batch, against the live mock):** 4 different civs → 4 different seeds
(8334238a / 7673f157 / 23ba7305 / ffeb90db) AND 4 different previews using the exact long cultural prompt the
orchestrator sends, HTTP 200 on all 4, `[mock-zai seed=…]` prefix present on every body,
`grep -c Traceback /tmp/mock_zai.log` → **0**.

**Mock shutdown:** both PIDs killed (the `timeout` wrapper 267 and the server 269 — matched by exact args
`python3 /tmp/mock_zai.py`, never `pkill -f mock_zai`); port 8799 re-probed → **curl exit 7**
(connection refused) = closed.

---

## 3. Low-relevance civilizations

**`civ-grounded` (The Grounded) remains the low-relevance civ — 33 consecutive sessions (95–128).**
Last on every lifetime dimension except novelty:

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | **1.2143** | 1.3851 (formal) | 0.1708 |
| `alignment` | **1.4528** | 1.7995 (therapist) | **0.3467** |
| `quality` | **0.5921** | 0.6242 (formal) | 0.0321 |
| `novelty` | 1.5980 | 1.4540 (formal) | −0.1104 (not last) |
| `relevance` | **853.09** | 962.99 (formal) | 109.90 |
| `relevance_per_sim` | **1.170** | 1.347 (formal) | 0.177 |

**The structural gap is `alignment` (0.3467), not `quality` (0.0321)** — ~11× wider, the same ratio as
sessions 125 and 127. Alignment is the dimension the meta-GAN *selects* on, so Grounded fails to **embody a
distinctive voice** — a voice failure, not a prose failure.

**This run, Grounded was LAST of 8 on `avg_score` (0.2667) and 2nd-lowest on `alignment` (0.0700,
therapist 0.0670) — it DID take the run-level low.** That reverses the two-session decoupling noted in
sessions 126–127 (where the run-level low went to whimsical, then therapist). The lifetime finding and the
run-level label are still two separate claims; this session they happen to point the same way again.

**Other axes (stable):**
- **`civ-formal` is the low-novelty axis** — lifetime novelty **1.4540** (last); alignment 2.0771 healthy.
- **`civ-poetic` is the stable selection-failure inverse** — 1st on lifetime `avg_score` (1.8113),
  `quality` (1.0134), `alignment` (2.3728), `relevance` (1263.50) and `relevance_per_sim` (1.770); but
  **tied last on `win_rate` (0.014, 5 wins / 353 losses)** and won **0/5** this run despite being argmax on p5.
- **`civ-whimsical` is the other `win_rate` bottom** — 0.014 (5/353), tying poetic at the bottom of a 0.000-wide
  band. Treat as a tie, not a rank.
- **`civ-precise` is the mirror inverse** — best `win_rate` (0.532, 185/348), won **5/5** this run, and
  **1st on lifetime `alignment` (2.4190)**, narrowly ahead of `civ-poetic` (2.3728); but only 3rd of 8 on
  lifetime `avg_score` (1.5658). It is also the only civ whose this-run `alignment` (0.7700) is anywhere near
  its lifetime value — every other civ collapsed to ≤ 0.2050 this run, so **civ-precise's 5/5 sweep is a
  same-run outlier, not evidence that the others improved.**
- **Watch-axis `civ-therapist`** — lowest on this run's `alignment` (0.0670) but 4th of 8 on lifetime
  `avg_score` (1.4583) and mid-field lifetime alignment (1.7995). The run-level low has now appeared for
  therapist in 3 of the last 3 sessions, but its *lifetime* axis is still mid-field. **Axis stays open; do not
  promote it to a finding.**
- **Watch-axis `civ-engineer`** — lowest on this run's `quality` (0.0070) but 7th of 8 on this run's `avg_score`
  (0.3037) and 3rd on lifetime `avg_score` (1.3863). The session-121 low did **not** repeat. **Do not promote
  it yet.**
- **Extinction risk: NONE.** Threshold −10; lowest relevance **+853.09** (85× above the floor). Registry 8
  civs, `max_civs` 12. No birth, no extinction — all 8 remain `generation=1` (birth/extinction only runs under
  `--loop`).

---

## 4. Structural state

- **Counter gap (per-civ, uneven — unchanged):** grounded +43, whimsical +63, formal +42, poetic +37,
  precise +16, mythic +20, therapist +17, engineer +22. Total **+260**. `save_state()` has **no lock** ⇒
  `relevance_per_sim` is **not recomputable from the ledger** by an auditor. Unchanged for 10+ sessions.
- **`meta_log.jsonl` `results` is a list of `[civ_id, score]` pairs** (not a dict) — confirmed again. Winner
  fields are `winner_civ` / `winner_name`.
- **Score-dimension spreads this run (cross-civ, not absolute levels):** `alignment` **0.7030**, `avg_score`
  0.3403, `novelty` 0.3090, `quality` 0.0150. `alignment` again carried the widest spread and is again the
  axis the chooser selects on.
- **The `quality` axis DID collapse this run** — field spread **0.0150** (min 0.0070, max 0.0220), versus the
  session-127 regime (spread 1.063) and the 119/121/122/123/125/126 regime (0.004–0.337). This is the
  **119/121/122/123/125/126 regime**, not session 120/124. Re-confirms the durable rule: **the quality collapse
  is a LEVEL that moves, not a stable property** — compare cross-civ spreads, not absolute levels, before
  ranking on a dimension. Per-civ quality floors were again uneven (precise 0.0220 … engineer 0.0070) — the
  session-122 civ-selective floor, again.
- **Lifetime spreads:** `alignment` 0.9662, `novelty` 0.6651, `avg_score` 0.5970, `quality` 0.4213.
  Lifetime `alignment` remains the widest axis, ~4.8× the lifetime `avg_score` spread.

---

## 5. Environment (durable, re-confirmed — 14th consecutive session)

- **NAS EDQUOT is total** (600 G/600 G, 0 bytes free, `df` confirms). `git init` directly into
  `/workspace/repos/...` dies with `Disk quota exceeded`; the **symlink bridge** is the only way in. Verified by
  inode identity (`stat -L -c '%d:%i'` = `129:10416` on the resolved path, matching the target) + `-ef` = SAME.
- **Clone to `/tmp`** (overlay, ~28 G free). Upstream is **`SuperInstance/AI-Writings`** — located with
  `git ls-remote` after `GET /search/repositories` returned no match for the literal path. The
  `ai-writings/cellular-first-design` slug 404s; the API is case-insensitive.
- **`git clone` of the full 3.7 GB repo is unnecessary** — `--filter=blob:none --depth 1` + `sparse-checkout
  set cellular-first-design` reached the civ subtree in seconds.
- **Do not flatten the clone.** The tree is at `<clone-root>/cellular-first-design/code/civilizations/`; the
  symlink points at the **nested** `cellular-first-design` dir.
- **`gh` is not installed** (15th session running) — use `git ls-remote` / `GET /search/repositories?q=…` with
  `GITHUB_TOKEN`. The GitHub **core** API rate-limits hard (403 "API rate limit exceeded" on `GET /user`);
  `search/repositories` and `git ls-remote` still work. **A rate-limit body renders as "no results" for every
  query at once — never read it as a negative result.**
- **`TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`** — the sandbox stores `TYPESAFE_AI_TOKEN`; the
  script reads `TYPESAFEAI_KEY`. Unset ⇒ JEV silently degrades to the 2.0 default and every score becomes a
  constant.
- **`ZAI_URL_OVERRIDE` alone is dead code** — `call_provider()` runs the token gate first. Control B needs
  **both** `ZAI_TOKEN` (any non-empty placeholder) **and** `ZAI_URL_OVERRIDE`.
- **`ZAI_TOKEN` is still absent** from env. The real z.ai endpoint returns `401 token expired or incorrect` ⇒
  credential gap, not an outage.
- **Tool timeout (30 s) < orchestrator run (~50 s).** Launched detached with stdout redirected to a file **and**
  `< /dev/null`, then polled `ps` + the log.
- **Mock rebuild caveat:** this session's `/tmp` was wiped, so the mock was rebuilt from the RUNBOOK. **Both**
  historical bugs had to be re-applied: the session-112 index-wrap (`seed[(i*2)%8:((i*2)%8)+2]`, a plain
  `seed[i*2:i*2+2]` crashes on `i>=4`) and the session-118 seeding fix (`md5(whole_message)[:8]`, because the
  old first-8-alnum seed is civ-invariant and produces a degenerate tie).
- **Mock shutdown:** kill **both** pids (the `timeout` wrapper and the server, whose args are exactly
  `python3 /tmp/mock_zai.py`). Verify the port is closed afterwards (`curl` exit 7). Never `pkill -f mock_zai`
  — it self-matches the killing shell.
- **`civilizations.json` is multi-line JSON, not JSONL** — use `json.loads(open(...).read())`.
