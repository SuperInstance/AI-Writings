# Civ Orchestrator — Run Report, session 173 (2026-10-25)

Command: `python3 civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, 56th session) + **live JEV**.
Baseline: `14811af1` (session 172). **All 9 verification assertions PASS.**

## Headline for the next session

- **The mock needed SIX fixes, unchanged — and the gate passed 8/8 on the FIRST build.**
  No rebuild drift this session. Fix (f) (message-derived index) was confirmed by the
  **repeat-same-message probe** (check 7): 40/40 messages returned a stable seed on the
  second send, and **0** `(civ,prompt)` pairs carry more than one seed.
- **`civ-grounded` remains the low-relevance civ — 48th consecutive session.** Last of 8 on
  lifetime `avg_score` 1.0042, `quality` 0.4079, `alignment` 1.0672, `relevance` 1142.76,
  `relevance_per_sim` 0.969. Alignment gap **1.0715** vs quality gap **0.3410** ⇒ **3.15×**
  wider ⇒ a **voice** failure, not a prose failure. Lifetime novelty 1.5375 is **6th of 8**.
- **The run-level low ROTATED to `civ-therapist`** (1.2500 run bottom on `avg_score`,
  `alignment` 0.8640) while its *lifetime* standing is 7th of 8.
  **Watch axis, not the finding** (session-132 rule).
- **Chooser vs `avg_score` argmax: 4/5 (80 %)** — the single disagreement took the
  lower-scoring candidate (`civ-precise` 1.82 vs `civ-poetic` 1.92 on the bookkeeper
  prompt). `civ-precise` swept **5/5**. Max |delta| **0.1000**.
- **Counter gap +134.1633** — the Σ`avg_score` of the 80 new rows.
- Run spreads: `avg_score` 0.8550, `alignment` **2.0510**, quality 0.5390, novelty 0.1720.
- Verification: per-civ Δ **+10 × 8** = **80** new rows, `meta_log` **+5** (598 → 603),
  `Winner:` **5**, `wins` **579 → 584** (+5), `relevance` Δ = Σ`avg_score` **8/8 exact**,
  0 JEV errors, `zai × 80`, **40/40** distinct seeds, **0** `(civ,prompt)` with >1 seed,
  registry 8 all gen 1, extinction **NONE** (lowest +1142.76 = **114×** the floor). **9/9 PASS.**

## Environment recovery

- The workspace was **empty** apart from `.plugin-cache` — the prompt's path
  `/workspace/repos/ai-writings/cellular-first-design/code/civilizations` did not exist
  (**13th consecutive occurrence**).
- Upstream **`SuperInstance/AI-Writings`**; the `ai-writings/…` slug 404s (API is
  case-insensitive). HEAD `14811af1` = session 172.
- Cloned to **`/tmp/aiw2`** with `--filter=blob:none --no-checkout` +
  `sparse-checkout set cellular-first-design/code/civilizations` ⇒ 14 MB working tree.
  Cloning into `/workspace` fails with **`Disk quota exceeded`** (NAS EDQUOT, **19th session**).
- **NAS WRITE TRAP — unchanged.** `/workspace` is at **100 % quota** (600 G/600 G,
  account-level) while being *visibly empty*. A plain `echo hello > testwrite.txt` returns
  **exit 0** and produces a **0-byte file**. `cp -a` of the whole tree printed
  **"Disk quota exceeded" for every file** and left a corrupt 0-byte tree that had to be
  `rm -rf`'d. **A copy that reports success can still be empty** — verify with
  `stat -c %s` or a byte count, not with the exit code.
  Only the **symlink inode** survives on the NAS; a symlink is a directory entry, not a
  data write, so the bridge works even at 100 % quota.
- Bridge symlink points at the **clone root**; verified by inode identity (**`129:140`**) and
  `-ef` → `EF_OK`. A **write through the bridge was verified to land as real bytes**
  (6-byte file; a 12-byte append to `civ-grounded/simulations.jsonl` was observed in the
  target and then reverted).
- **`ls -la` on the bridged path hit a transient NAS directory-cache miss** immediately
  after the run (`No such file or directory`) while `stat` on the same path resolved the
  symlink correctly. **A single `ls` failure is not evidence of a missing tree** — retry
  before concluding, and cross-check with `stat`/`find`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai **401** `token expired or
  incorrect` ⇒ endpoint healthy, credential absent (**56th session**).
- **JEV live**: well-formed body → **HTTP 200** with `{"model":"jev-1.14.0", …}`.
- `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; `ZAI_TOKEN` = placeholder **and**
  `ZAI_URL_OVERRIDE` set (the override alone is dead code).
- `gh` not installed (**21st session**) — used `GET /repos/…/contents` with `GITHUB_TOKEN`.
- Tool timeout 30 s < orchestrator run ~60 s ⇒ detached launch, stdout redirected, `< /dev/null`.

## Mock rebuild checklist — SIX fixes

| # | Fix | Session | Symptom if missing |
|---|---|---|---|
| a | `seed[(i*2)%8:((i*2)%8)+2]` index wrap | 112 | `ValueError` on `i>=4` ⇒ HTTP 500 **while the socket stays open** |
| b | `md5(whole_message)` (not the first 8 alnum chars) | 118 | first 8 alnum chars are `YouAreA` for every civ ⇒ all 8 civs emit identical text |
| c | `Connection: close` + `Content-Length` | 144 | `curl` hangs to the tool timeout on a healthy server |
| d | interpolate the seed placeholder | 145 | every response carries literal `seed={}` ⇒ 1 distinct seed, not 40 |
| **e** | **seed widened 2 → 4 hex chars** | **169** | **2-char slice collides ⇒ 39 distinct seeds, one prompt at 7/8** |
| **f** | **index derived from the MESSAGE (`d[0] % 4`), not a request counter** | **170** | **64 distinct seeds / 80 rows; 20 `(civ,prompt)` pairs carry >1 seed** |

### The mock algorithm — fully specified (verified 80/80 against the session-172 ledger)

```
d      = md5(cultural_prompt).digest()          # the FULL user message, verbatim
h      = d.hex()
i      = d[0] % 4                              # MESSAGE-derived, NOT a counter
seed   = h[(i*2)%8:(i*2)%8+2] + h[((i*2)+2)%8:((i*2)+2)%8+2]
color  = h[8:12]
figure = h[12:16] / h[16:20] / h[20:24]
```

`cultural_prompt` is exactly what `civilization_orchestrator.py` builds:

```
You are a voice in the tradition of "{name}".
Your tenets: {tenets joined by ", "}.
Your voice: {voice_emphasis}.

{prompt}
```

Only **4** distinct seeds are reachable from one message (the seed slices `h[0:8]` at even
offsets), so `i mod 4` is the whole index space. The signature of a *message-derived* index
is that the seed is **stable across every row of the same `(civ, prompt)` pair** — a request
counter cannot produce that, because the competition phase fires 8 civs in parallel.

**Pre-flight gate (must pass before the batch) — EIGHT checks:** 40 requests using the
**exact long cultural prompts** ⇒ **40/40 distinct seeds**, **40/40 distinct previews**,
**40/40 independently recomputed md5s** (seed, colour and figure), **8/8 distinct seeds AND
8/8 distinct previews on every one of the 5 prompts**, 0 literal `seed={}`, 0 `EXC:`/
tracebacks, and **repeat-same-message ⇒ same seed (40 messages × 2 repeats)**.
The repeat probe is what catches fix (f); the pre-flight alone cannot, because it only ever
sends *distinct* messages.

**Teardown:** kill by exact argv match — `python3 /tmp/mock_zai.py` and
`timeout -s KILL 900 python3 /tmp/mock_zai.py` (**two** pids). Never `pkill -f mock_zai`
(self-matches the killing shell). Then prove the port is closed: `curl -m 5` ⇒ **exit 7**,
`HTTP=000`.

## Leaderboard (sorted by `relevance_per_sim`)

| rank | civ | name | gen | relevance | r/sim | sims | wins | losses | win% | temp |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | civ-poetic | The Poetic | 1 | 1779.61 | 1.529 | 1164 | 6 | 572 | 0.010 | 0.80 |
| 2 | civ-precise | The Precise | 1 | 1627.91 | 1.409 | 1155 | 342 | 231 | 0.597 | 0.20 |
| 3 | civ-whimsical | The Whimsical | 1 | 1557.81 | 1.330 | 1171 | 5 | 573 | 0.009 | 0.95 |
| 4 | civ-mythic | The Mythic | 1 | 1438.36 | 1.241 | 1159 | 10 | 562 | 0.017 | 0.85 |
| 5 | civ-formal | The Formal | 1 | 1355.36 | 1.163 | 1165 | 93 | 483 | 0.161 | 0.30 |
| 6 | civ-engineer | The Engineer | 1 | 1308.23 | 1.134 | 1154 | 47 | 524 | 0.082 | 0.40 |
| 7 | civ-therapist | The Therapist | 1 | 1309.34 | 1.132 | 1157 | 11 | 564 | 0.019 | 0.60 |
| 8 | **civ-grounded** | **The Grounded** | 1 | **1142.76** | **0.969** | 1179 | 70 | 507 | 0.121 | 0.50 |

**Ranks 6 and 7 are ordered by `relevance_per_sim`, not raw relevance.** `civ-therapist`
carries *more* total relevance (1309.34) than `civ-engineer` (1308.23) but has run more sims
(1157 vs 1154), so its per-sim rate is lower (1.1317 vs 1.1336). The board's sort key is
`relevance_per_sim`; the raw-relevance order is therapist **above** engineer. **Report the
axis you actually ranked on.**

## Per-axis — lifetime vs this run

| civ | life qual | life novel | life align | life avg | run qual | run novel | run align | run avg |
|---|---|---|---|---|---|---|---|---|
| civ-poetic | 0.7489 | 1.8810 | 2.0572 | 1.5624 | 0.9870 | 2.3350 | 2.3870 | 1.9030 |
| civ-precise | 0.5217 | 1.5937 | 2.1387 | 1.4181 | 1.0670 | 2.3330 | 2.9150 | 2.1050 |
| civ-whimsical | 0.5884 | 1.9427 | 1.6770 | 1.4027 | 0.5790 | 2.3920 | 1.0270 | 1.3327 |
| civ-mythic | 0.5312 | 1.7334 | 1.5254 | 1.2633 | 0.7740 | 2.2200 | 1.9410 | 1.6450 |
| civ-formal | 0.4553 | 1.4516 | 1.6743 | 1.1938 | 0.8550 | 2.2860 | 2.4780 | 1.8730 |
| civ-therapist | 0.4579 | 1.7540 | 1.2416 | 1.1511 | 0.5280 | 2.3580 | 0.8640 | 1.2500 |
| civ-engineer | 0.4513 | 1.5159 | 1.4830 | 1.1501 | 0.6460 | 2.3510 | 2.2610 | 1.7527 |
| **civ-grounded** | **0.4079** | **1.5375** | **1.0672** | **1.0042** | 0.5900 | 2.2680 | 1.8070 | 1.5550 |

- Lifetime quality gap **0.3410** (poetic 0.7489 − grounded 0.4079); alignment gap **1.0715**
  (precise 2.1387 − grounded 1.0672) ⇒ **3.15×** wider ⇒ **voice** failure, not a prose failure.
- `civ-grounded` run rank: **#7, #6, #6, #5, #5** of 8 across the 5 prompts — never top-3.
- `civ-therapist` run rank is the run-level low; its alignment (0.8640) is the run's worst.
- Extinction: floor is **−10**; lowest relevance **+1142.76** ⇒ **114×** the floor ⇒
  **NONE** retired. Registry unchanged at 8, all `generation` 1.

## Verification — 9/9 PASS

| # | check | result |
|---|---|---|
| 1 | per-civ `simulations.jsonl` delta | **+10 × 8 = 80** |
| 2 | `meta_log.jsonl` delta | 598 → **603** (+5) |
| 3 | `Winner:` lines in stdout | **5** |
| 4 | provider set | `{zai}` × 80 |
| 5 | distinct seeds | **40/40** |
| 6 | rows whose seed ≠ independently recomputed md5 | **0** |
| 7 | `(civ,prompt)` pairs carrying >1 seed | **0** |
| 8 | JEV errors | **0** |
| 9 | `relevance` Δ = Σ`avg_score` | **8/8 exact** |
| 10 | `wins` delta | 579 → **584** (+5) |
| 11 | mock log `EXC:` / traceback / HTTP 500 | **0 / 0 / 0** |
| 12 | teardown | 0 procs, `curl` exit 7, `HTTP=000` |

### Per-civ row counts

| civ | before | after | delta | bytes after |
|---|---|---|---|---|
| civ-grounded | 1212 | 1222 | +10 | 691067 |
| civ-whimsical | 1224 | 1234 | +10 | 698959 |
| civ-formal | 1197 | 1207 | +10 | 677428 |
| civ-poetic | 1191 | 1201 | +10 | 673177 |
| civ-precise | 1161 | 1171 | +10 | 651310 |
| civ-mythic | 1169 | 1179 | +10 | 660416 |
| civ-therapist | 1164 | 1174 | +10 | 664689 |
| civ-engineer | 1166 | 1176 | +10 | 665680 |

## Next session

- Rebuild the mock from the spec above; the pre-flight gate is **eight** checks and must
  pass **before** the batch. Fix (f) is covered only by the repeat-same-message probe.
- **Do not trust a copy into `/workspace`** — the NAS is at 100 % quota and writes land as
  0-byte files with exit 0. Clone and run from `/tmp`; bridge with a symlink; verify the
  bridge with `stat -L -c '%d:%i'` and `-ef`.
- **A transient NAS directory-cache miss can make `ls` on the bridged path fail once.**
  Retry, and cross-check with `stat`/`find` before declaring the tree missing.
- `civ-grounded` is the lifetime low for the **48th** consecutive session; the run-level
  low has now rotated to `civ-therapist`. Watch the **axis** (alignment vs quality), not
  the name.
