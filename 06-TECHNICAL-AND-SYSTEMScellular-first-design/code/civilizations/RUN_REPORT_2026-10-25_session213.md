# Civ Orchestrator — Run Report, session 213 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **85th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `2cecc70` (session 212 tree). **All 30 verification assertions PASS.** Pre-flight **12/12 PASS**.

**Session 213 in one line:** `civ-precise` took **4/5** competitions (a `civ-formal` break on
prompt 4) and held the run's best `avg_score` (**2.4933**) and the widest alignment lead
(**3.1720**); the chooser/argmax agreement was **2/5 (40 %) — 3 down-grades, 0 up-grades**; the
run-level low rotated to **`civ-whimsical`** while `civ-grounded` held the lifetime low for the
**82nd** consecutive session.

## Run ledger

| civ | avg_score | quality | novelty | alignment |
|---|---|---|---|---|
| `civ-precise` | 2.4933 | 1.8680 | 2.4400 | 3.1720 |
| `civ-poetic` | 2.4520 | 1.9740 | 2.4700 | 2.9120 |
| `civ-formal` | 2.3260 | 1.6320 | 2.4280 | 2.9180 |
| `civ-engineer` | 2.2120 | 1.5920 | 2.3880 | 2.6560 |
| `civ-mythic` | 2.1927 | 1.8040 | 2.4100 | 2.3640 |
| `civ-grounded` | 1.9487 | 1.3260 | 2.4360 | 2.0840 |
| `civ-therapist` | 1.6607 | 1.2160 | 2.4620 | 1.3040 |
| `civ-whimsical` | 1.5107 | 1.1560 | 2.4860 | 0.8900 |

Axis spreads: alignment **2.2820** (widest, **2.79x** the quality spread), quality **0.8180**,
`avg_score` **0.9827**, novelty **0.0980** (narrowest in the series).

## Verification (30/30 PASS)

per-civ row delta **+10 x 8 = 80** new rows, `meta_log` **+5** (798 -> 803), `wins` **+5** /
`losses` **+35**, `simulations_run` **+10 x 8**, **0** JEV `error` keys, **0** 2.0/2.0/2.0
fallback triples, **80/80** rows `provider=zai` with the `[mock-zai` prefix, **80/80** rows match
an independently recomputed seed+colour+figure, **40** distinct seeds (message-level), **0**
`(civ,prompt)` slots with >1 seed, per-prompt **8/8** distinct seeds AND previews on all 5
competition prompts, **80/80** distinct `(q,n,a)`, relevance delta == sum(`avg_score`) **8/8
exact** (max residual **9.09e-13**), meta-vs-ledger `avg_score` mismatches **0/40**, counter gap
(`culture - ledger`) **unchanged 8/8** at the documented stable values, registry 8 all gen 1,
extinction **NONE** (lowest **+1758.28 = 176x** the -10 floor), leaderboard 8 sorted.

## Low-relevance civilizations

- **Lifetime low: `civ-grounded`** — relevance **1758.28**, `relevance_per_sim` **1.114**
  (last of 8) for the **82nd** consecutive session, yet lifetime `win_rate` **0.094** is
  3rd-best in the fleet. Its lifetime deficit is **quality** (**1.3260** run / fleet-low on the
  lifetime axis), not alignment and not novelty. Lowest relevance is **176x** the -10
  extinction floor: no extinction risk.
- **Run low: `civ-whimsical`** — `avg_score` **1.5107**, alignment **0.8900** (fleet-low),
  quality **1.1560** (fleet-low), novelty **2.4860** (fleet-**high**). The signature is again
  *high novelty, low alignment*. It sits **0.1500** above the run's next civ
  (`civ-therapist`, **1.6607**), a gap of **0.153x** the run's own `avg_score` spread
  (**0.9827**) — a small but this time resolvable separation. This is the **19th different run
  low in 19 sessions**: the holder rotates, the axis does not.
- **Also low: `civ-therapist`** — `avg_score` **1.6607**, alignment **1.3040** (2nd-lowest),
  quality **1.2160** (2nd-lowest), novelty **2.4620** (2nd-highest). It shares the run low's
  axis exactly. Note the **lifetime** alignment low belongs to `civ-therapist`
  (**1.3040** fleet-low over the full ledger, spread **1.0570**) even though its lifetime
  `avg_score` is 2nd-lowest, not last — the run and lifetime tables are two separate claims.
- **`civ-grounded` is 6th of 8 on run `avg_score`** (**1.9487**) while it is last of 8 for the
  whole lifetime. *Do not carry a coincidence forward as a pattern — and do not carry a
  decoupling forward as a pattern either.*

## Durable lessons from this session

1. **THE SEED INDEX IS THE RAW MD5 BYTE `d[0] % 4`, NOT THE HEX DIGIT `int(h[0],16) % 4`.**
   Both are "the first byte mod 4" to the eye, and both are 0-3, but they are **different
   functions**: `d[0]` is the byte `0x00-0xFF` while `int(h[0],16)` is only `0x00-0x0F`. The
   hex-digit reading reproduces the **colour** and **figure** fields perfectly (both are taken
   from `h[8:24]`, which does not depend on the index) and gets the **seed** wrong on ~70 % of
   rows — a failure that looks like "the mock is broken" while the mock is exactly right.
   A brute-force sweep over every 4-hex window and every `%2/%4/%8` index rule found the true
   rule at **80/80** only under the raw-byte reading. *When a composite field recompute is
   partially right, the wrong field is usually the one that depends on the index.*
2. **THE MOCK HEADER PARSE MUST BIND THE FIGURE'S TRAILING `". "` — NOT A BARE SPACE.**
   The recorded header is `[mock-zai <4hex>] #<4hex> <4/4/4>. ` — the figure is followed by a
   **period** and a space. A regex that expects the figure to be followed by a space matches
   **0/40**, and the pre-flight then reports `distinct_seeds 1/40` and
   `recomputed_md5 0/40` on a perfectly healthy mock. *This is the second parser trap in
   this project after the seed/colour mis-split (session 204): when a pre-flight goes red on
   the recompute, dump one real body and parse it by hand before touching the server.*
3. **A `simulations_run` DELTA MUST BE TAKEN AGAINST THE `culture.json` BASELINE, NOT
   AGAINST THE LEDGER ROW COUNT.** The ledger carries rows from every prior session, so
   `simulations_run` != `len(ledger)`; comparing the counter against `len(rows) - 10` failed
   **8/8** on a run whose counter gaps came back at exactly the documented stable values
   (grounded -84.35, whimsical -173.14, formal -85.53, poetic -96.80, precise -32.63,
   mythic -51.11, therapist -42.11, engineer -44.24). *The per-civ counter gap is the cheapest
   integrity check there is — it caught that the run was clean while the check was wrong.*
4. **A 40 % CHOOSER/ARGMAX AGREEMENT IS 3 DOWN-GRADES, NOT A DEFECT.** All three
   disagreements took the **lower**-scoring candidate (0 up-grades). `civ-poetic` was argmax
   on **2 of 5** prompts and won **0 of 5**; `civ-mythic` was argmax on 1 of 5 and won 0 of 5.
   The streak is re-based from this session's own `meta_log` — it is **3** here, and it is not
   the 3 of session 212. *Never treat `win_rate` as a quality metric.*

## Environment (durable)

- 85th session with the prompt path absent at start (workspace held only `.plugin-cache` and
  `.skills`). The NAS under `/workspace` is at **100 % quota** (600 G/600 G, 0 bytes free), so
  the repo was cloned **sparse** to `/tmp/aiw` (`git init` + `core.sparseCheckout` +
  `--depth 1 --filter=blob:none`; **11 M** working tree from a 3.7 GB repo) and the **inner**
  `cellular-first-design/code` was bridged by symlink —
  `ln -sfn /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code`,
  verified by inode identity `129:3669` on both sides plus `os.path.samefile()` -> `True`.
- `ZAI_TOKEN` absent from env and all 8 sandbox secrets; z.ai returns **401 `token expired or
  incorrect`** (endpoint healthy, credential gap) — **85th session**. `ZAI_URL_OVERRIDE` alone
  is dead code behind the token gate: Control B needs **both** `ZAI_TOKEN` (placeholder) and
  the override. `TYPESAFEAI_KEY` exported from `TYPESAFE_AI_TOKEN`; JEV live at `jev-1.14.0`;
  **0** fallback triples.
- `gh` not installed — use `GET /user/repos` / `GET /search/code` with `GITHUB_TOKEN`. The
  upstream owner is **`SuperInstance/AI-Writings`** (a *user* account). `GIT_SSL_NO_VERIFY=1`
  required for git fetch/push; push to the explicit token URL and verify with `git ls-remote`.
- The mock body was rebuilt at a **constant 356 chars** (38-char header + one fixed tail with
  no culture-derived fields), inside the documented 332-369 band on the **first** build, and the
  pre-flight passed **12/12** on the first run of the corrected gate.
- Mock teardown by exact-argv match (wrapper **and** server pid), then prove the port closed
  (`curl` exit 7 = refused, `HTTP=000`). Never `pkill -f mock_zai` (self-match).
