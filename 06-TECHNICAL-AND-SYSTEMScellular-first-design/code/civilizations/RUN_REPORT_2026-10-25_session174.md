# Civ Orchestrator — Run Report, session 174 (2026-10-25)

**Command:** `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
**Upstream:** `SuperInstance/AI-Writings` @ `f74e158` (session 173 baseline)
**Provider path:** Control B mock bridge on `127.0.0.1:8799` (`ZAI_TOKEN` placeholder **and**
`ZAI_URL_OVERRIDE` both set — the override alone is dead code without a token). **JEV live**
(`TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; probe -> HTTP 200, real score body,
model `jev-1.14.0`).
**Run status:** all verification checks PASS — 80 new rows, 5/5 competitions, 0 JEV errors,
mock non-degenerate 5/5, **15th consecutive clean measurement**.

---

## Headline for the next session

- **`civ-grounded` remains the low-relevance civ — 49th consecutive session.** Last of 8 on
  lifetime `avg_score` 1.0047, `alignment` 1.0626, `quality` 0.4056, `relevance` 1153.49,
  `relevance_per_sim` 0.970. Alignment gap **0.4131** vs quality gap **0.0431** => **9.59x**
  wider => a **voice** failure, not a prose failure. Lifetime novelty 1.5460 is **6th of 8** —
  Grounded is not boring, it is *unmistakable in a way the chooser does not reward*.
- **The run-level low ROTATED to `civ-therapist`** (1.0297 run bottom on `avg_score`,
  `alignment` 0.3360) while its *lifetime* standing is 6th of 8. **Watch axis, not the
  finding** (session-132 rule).
- **Chooser vs `avg_score` argmax: 0/5 (0 %)** — the **worst** agreement in the clean-mock
  series, and all **five** disagreements went the same way: the chooser took the
  **lower**-scoring candidate. Max |delta| **0.240** (witness log). `civ-precise` won 4/5.
- **Counter gap +108.9900** — the sum of `avg_score` over the 80 new rows; `d_relevance` is
  **8/8 EXACT** against it (max abs diff 5.2e-13).
- Run spreads: `avg_score` 0.7387, `alignment` **1.8960**, quality 0.5340, novelty 0.1870.
  `alignment` again carried the widest spread and is again the axis the chooser selects on.
- Verification: per-civ delta **+10 x 8** = **80** new rows, `meta_log` **+5** (603 -> 608),
  `Winner:` **5**, wins **+5**, 0 JEV errors, `zai x 80`, **40/40** distinct seeds, **0**
  `(civ,prompt)` with >1 seed, registry 8 all gen 1, extinction **NONE** (lowest +1153.49 =
  **115x** the floor).

## Environment recovery

- The workspace was **empty** apart from `.plugin-cache` — the prompt's path
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
  (**14th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`**; the `ai-writings/...` slug 404s (the API is
  case-insensitive). `gh` is **not installed** (22nd session) — used `GET /user/repos` +
  `GET /git/trees/HEAD?recursive=1` with `GITHUB_TOKEN`.
- Cloned to **`/tmp/ai-writings`** with `--depth=1`. Cloning into `/workspace` fails with
  **`Disk quota exceeded`** (NAS EDQUOT, **20th session**).
- **NAS WRITE TRAP — unchanged.** `/workspace` is at **100 % quota** (600 G/600 G, 0 bytes
  free) while being *visibly empty*. Only the **symlink inode** survives on the NAS; a
  symlink is a directory entry, not a data write, so the bridge works even at 100 % quota.
- Bridge: `ln -sfn /tmp/ai-writings/cellular-first-design
  /workspace/repos/ai-writings/cellular-first-design`; verified by **inode identity**
  (`129:10423` on both sides) and by `os.stat` `(st_dev, st_ino)` equality.
  **Note:** the shell's `[ -ef a b ]` test mis-parses in this sandbox ("binary operator
  expected") — use Python `os.stat` instead; it is not a bridge failure.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401** (endpoint healthy,
  credential absent) — **57th session**.
- **JEV live**: well-formed body -> **HTTP 200** with `{"model":"jev-1.14.0", ...}`.
- Tool timeout 30 s < orchestrator run ~60 s => detached launch under
  `setsid nohup timeout -s KILL 600`, stdout redirected, `< /dev/null`, polled by PID.

## Mock rebuild — one new finding

The mock was rebuilt from the session-173 spec with all **six** documented fixes (a-f) applied.
**The pre-flight gate passed 8/8 on the first build** (no rebuild drift).

**NEW — the spec's `figure = h[12:16] / h[16:20] / h[20:24]` is pseudo-code, not Python.**
Read literally it is a division of two `str` values and raises
`TypeError: unsupported operand type(s) for /: 'str' and 'str'`. The mock then 500s on
**every** request **while the socket stays open**, so a port/200 liveness probe looks
healthy. The fix is to treat the three slices as three separate components, e.g.
`figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"`. **Fix (a) is about a different symptom**
(`ValueError` on `i>=4` from the seed slice) — a `TypeError` on the figure line is a
**seventh, previously undocumented** failure mode. It is also invisible to the one-word
probe in the RUNBOOK for the same reason fix (a) was: the socket stays up.

**Pre-flight gate (8/8 PASS, live mock, exact long cultural prompts):** 40 requests ->
**40/40** distinct seeds, **40/40** distinct previews, **40/40** independently recomputed
md5 seeds, **8/8** distinct seeds AND **8/8** distinct previews on every one of the 5 prompts,
0 literal `seed={}`, **0** tracebacks, and **repeat-same-message => same seed (40 x 2, bad = 0)**.

## Verification — asserted on rows, not on exit code

| Check | Expected | Observed | |
|---|---|---|---|
| per-civ `simulations.jsonl` delta | **+10 each** | +10 on all 8 | PASS |
| total new rows | 80 | 80 | PASS |
| `meta_log.jsonl` delta | **+5** | +5 (603 -> 608) | PASS |
| `Winner:` lines | **5** | 5 | PASS |
| rows with `[mock-zai` prefix | 80/80 | 80/80 | PASS |
| `provider` set | `{zai}` | `{zai}` (all 80) | PASS |
| rows with a JEV `error` key | **0** | 0 | PASS |
| rows with the 2.0/2.0/2.0 fallback triple | **0** | 0 | PASS |
| distinct seeds across the 80 new rows | 40 | 40 | PASS |
| `(civ, prompt)` combos with >1 seed | 0 | 0 | PASS |
| per-prompt (ts-sorted last 8) distinct seeds & previews | 8/8 on all 5 | 8/8 on all 5 | PASS |
| `d_relevance` == sum of the 10 new `avg_score` | 8/8 exact | 8/8 exact (max 5.2e-13) | PASS |
| total wins delta | +5 | +5 | PASS |
| distinct `avg_score` values / 80 rows | >1 (JEV really scored) | 68 (46 distinct quality) | PASS |
| mock tracebacks | 0 | 0 | PASS |
| port closed after teardown | `curl` exit 7 | exit 7, HTTP=000 | PASS |
| `leaderboard.json` rewritten | yes | 05:24:00Z | PASS |
| registry | 8 civs, all `generation=1` | 8, all gen 1, no birth/extinction | PASS |

### Per-civ line deltas

| civ | before | after | delta |
|---|---|---|---|
| civ-engineer | 1176 | 1186 | +10 |
| civ-formal | 1207 | 1217 | +10 |
| civ-grounded | 1222 | 1232 | +10 |
| civ-mythic | 1179 | 1189 | +10 |
| civ-poetic | 1201 | 1211 | +10 |
| civ-precise | 1171 | 1181 | +10 |
| civ-therapist | 1174 | 1184 | +10 |
| civ-whimsical | 1234 | 1244 | +10 |

**Method note — read `culture.json` baselines from git, not from `leaderboard.json`.**
`leaderboard.json` stores `relevance` **rounded to 2 dp** while `culture.json` keeps full
float precision, so a baseline taken from the leaderboard makes the
`d_relevance == sum(avg_score)` check fail by up to **0.0033 per civ** on 4 of 8 civs and
looks like a real accounting error. The authoritative pre-run value is
`git show HEAD:.../culture.json`. With the true baselines the check is **8/8 exact to
1e-13**. The RUNBOOK's "counter gap" claim is only auditable at that precision.

## Results

### Chooser vs `avg_score` argmax: 0/5 (0 %)

| prompt | winner | winner `avg_score` | argmax | argmax score | delta | |
|---|---|---|---|---|---|---|
| what a cell is | `civ-precise` | 1.587 | `civ-poetic` | 1.640 | **-0.053** | disagree |
| the bookkeeper's role | `civ-precise` | 1.683 | `civ-poetic` | 1.783 | **-0.100** | disagree |
| the witness log | `civ-formal` | 2.187 | `civ-precise` | 2.427 | **-0.240** | disagree |
| ternary values | `civ-precise` | 1.540 | `civ-poetic` | 1.637 | **-0.097** | disagree |
| JEV as a decision oracle | `civ-precise` | 1.693 | `civ-poetic` | 1.700 | **-0.007** | disagree |

Clean-mock series: 0/5 (118) -> 3/5 (119) -> 1/5 (120) -> 4/5 (121) -> 4/5 (122) -> 3/5 (123) ->
0/5 (124) -> 4/5 (125) -> 1/5 (126) -> 3/5 (127) -> 2/5 (128) -> 4/5 (130) -> 1/5 (131) ->
2/5 (132) -> 2/5 (133) -> 0/5 (134) -> 4/5 (136) -> 1/5 (137) -> 1/5 (141) -> 2/5 (142) ->
4/5 (173) -> **0/5 (174)**. Twenty-two five-sample points cannot narrow a rate — the honest
claim stays *somewhere in 0-80 %*. What survives every session: the chooser is **not** a
pure argmax, and **every** observed disagreement across the fleet goes the same way — it
picks a **lower**-scoring candidate. **Never treat `win_rate` as a quality metric.**

Winner tally this run: `civ-precise` 4, `civ-formal` 1.

### Leaderboard (sorted by `relevance_per_sim`)

| rank | civ | name | gen | relevance | r/sim | sims | wins | losses | win% | temp |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | The Poetic | 1 | 1797.29 | 1.531 | 1174 | 6 | 577 | 0.010 | 0.80 |
| 2 | civ-precise | The Precise | 1 | 1644.98 | 1.412 | 1165 | 346 | 232 | 0.599 | 0.20 |
| 3 | civ-whimsical | The Whimsical | 1 | 1572.05 | 1.331 | 1181 | 5 | 578 | 0.009 | 0.95 |
| 4 | civ-mythic | The Mythic | 1 | 1450.07 | 1.240 | 1169 | 10 | 567 | 0.017 | 0.85 |
| 5 | civ-formal | The Formal | 1 | 1371.72 | 1.167 | 1175 | 94 | 487 | 0.162 | 0.30 |
| 6 | civ-engineer | The Engineer | 1 | 1319.12 | 1.133 | 1164 | 47 | 529 | 0.082 | 0.40 |
| 7 | civ-therapist | The Therapist | 1 | 1319.63 | 1.131 | 1167 | 11 | 569 | 0.019 | 0.60 |
| 8 | civ-grounded | The Grounded | 1 | 1153.49 | 0.970 | 1189 | 70 | 512 | 0.120 | 0.50 |

### Low-relevance civilization

**`civ-grounded` (The Grounded) — last of 8 on every lifetime measure.**

| dimension | civ-grounded | next civ | gap |
|---|---|---|---|
| `avg_score` | 1.0047 | 1.1496 (engineer) | 0.1448 |
| `alignment` | 1.0626 | 1.4757 (engineer) | **0.4131** |
| `quality` | 0.4056 | 0.4487 (engineer) | 0.0431 |
| `novelty` | 1.5460 | 1.5242 (engineer) | **-0.0218** (Grounded is *higher*) |
| `relevance` | 1153.49 | 1319.12 (engineer) | 165.63 |
| `relevance_per_sim` | 0.970 | 1.133 (engineer) | 0.163 |

The structural gap is **alignment: 0.4131 vs a 0.0431 margin on quality = 9.59x wider.**
Alignment is the dimension the meta-GAN *selects* on, so this is a **voice** failure, not a
prose failure — Grounded does not write badly (it is mid-field on novelty, 6th of 8, and
above the next civ on novelty), it fails to *embody a distinctive voice* that the chooser
recognises. Extinction risk **NONE** (threshold -10; lowest relevance 1153.49 = **115x** the
floor). Registry 8, `max_civs` 12; extinction/birth only runs under `--loop`.

**Second watch axis — `civ-therapist`.** Run-level low on both `avg_score` (1.0297) and
`alignment` (0.3360) this session, while its lifetime standing is 6th of 8. By the
session-121/132 rules this is a **watch axis, not a finding**; it becomes a finding if it
repeats.

**The two stable inverses hold:** `civ-poetic` = 1st on lifetime `avg_score` (1.5641) and
`quality` (0.7482) but last on `win_rate` (0.010, 6/577); `civ-precise` = best `win_rate`
(0.599) and highest `alignment` (2.1390) but only 2nd on `avg_score` (1.4205).

**`civ-formal`** = the low-novelty axis (lifetime novelty 1.4605, last; alignment 1.6760
healthy). **`civ-engineer`** = 7th of 8 on lifetime `avg_score` (1.1496).

## Teardown

Mock killed by exact argv match (`python3 /tmp/mock_zai.py` and the `timeout` wrapper — two
pids, 321 and 323). Port verified closed afterwards: `curl -m 5` -> **exit 7**, `HTTP=000`.
`/tmp/mock_zai.log` is **0 bytes** (no tracebacks).
