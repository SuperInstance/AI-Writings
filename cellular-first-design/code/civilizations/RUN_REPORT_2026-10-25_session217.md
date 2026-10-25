# Civ Orchestrator — Run Report, session 217 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`
Provider path: **Control B mock** (z.ai credential gap, **88th session**) + **live JEV** (`jev-1.14.0`).
Baseline: `e722ddd` (session 216 tree). **All 24 verification assertions PASS.** Pre-flight **10/10 PASS** (first build).

**Session 217 in one line:** `civ-precise` took **4/5** competitions with `civ-formal` taking the
fifth; the chooser/argmax agreement was **2/5 (40 %) — 3 down-grades, 0 up-grades**; the
run-level low was **`civ-therapist`** (avg **1.7627**, fleet-low alignment **1.6060**) while
`civ-grounded` held the lifetime low for the **85th** consecutive session.

## Run results (10 new rows per civ: 5 sim phase + 5 competition phase)

| civ | avg_score | quality | novelty | alignment | rank |
|---|---|---|---|---|---|
| civ-poetic | 2.4427 | 1.7610 | 2.5430 | 3.0240 | 1/8 |
| civ-precise | 2.3067 | 1.5930 | 2.4110 | 2.9160 | 2/8 |
| civ-formal | 2.1173 | 1.3890 | 2.4470 | 2.5160 | 3/8 |
| civ-mythic | 2.0910 | 1.5280 | 2.4260 | 2.3190 | 4/8 |
| civ-whimsical | 2.0147 | 1.4270 | 2.5500 | 2.0670 | 5/8 |
| civ-engineer | 1.9207 | 1.2540 | 2.4200 | 2.0880 | 6/8 |
| civ-grounded | 1.9140 | 1.2030 | 2.4770 | 2.0620 | 7/8 |
| civ-therapist | 1.7627 | 1.1250 | 2.5570 | 1.6060 | 8/8 (run low) |

Run spreads: avg **0.6800**, quality **0.6360**, novelty **0.1460**, alignment **1.4180**.
The alignment spread is **2.23x** the quality spread and **9.71x** the novelty spread — the
ranking is produced by alignment, not novelty.

## Lifetime leaderboard (cumulative)

| civ | relevance | rel/sim | win_rate | quality | novelty | alignment | rows |
|---|---|---|---|---|---|---|---|
| civ-poetic | 2645.97 | 1.6496 | 0.008 | 0.8633 | 2.0069 | 2.1441 | 1641 |
| civ-precise | 2505.81 | 1.5710 | 0.678 | 0.6697 | 1.7888 | 2.2685 | 1611 |
| civ-whimsical | 2232.80 | 1.3860 | 0.006 | 0.6456 | 2.0601 | 1.6061 | 1674 |
| civ-formal | 2153.93 | 1.3420 | 0.138 | 0.5722 | 1.6776 | 1.8294 | 1647 |
| civ-mythic | 2141.56 | 1.3393 | 0.013 | 0.6360 | 1.8830 | 1.5439 | 1619 |
| civ-engineer | 2052.02 | 1.2873 | 0.064 | 0.5683 | 1.7223 | 1.6010 | 1616 |
| civ-therapist | 1916.11 | 1.1998 | 0.014 | 0.5196 | 1.9207 | 1.1995 | 1614 |
| civ-grounded | 1834.52 | 1.1331 | 0.092 | 0.4940 | 1.7469 | 1.2227 | 1662 |

## Low-relevance civilizations (three different axes)

- **Run low — `civ-therapist`**: `avg_score` **1.7627**, 8th of 8, with the fleet-low run
  alignment (**1.6060**) and the fleet-low run quality (**1.1250**). Its gap to the next civ
  is **0.1513**, i.e. **22.3 %** of the run spread — the *identity* of the bottom is solid,
  its *ordering* against 2nd place is weak.
- **Lifetime low — `civ-grounded`**: relevance **1834.52**, rel/sim **1.1331**, lifetime avg
  **1.1331**, and the fleet-low lifetime quality (**0.4940**). Yet its lifetime `win_rate`
  **0.092** is 3rd-best in the fleet — the "low relevance but competitive" pattern again.
- **Lifetime alignment low — `civ-therapist`** (**1.1995**) — a *third* civ on a *third* axis.

The lifetime lowest **novelty** belongs to `civ-formal` (**1.6776**), not to the run low.

## Chooser vs argmax

| prompt | argmax | winner | verdict |
|---|---|---|---|
| what a cell is | civ-poetic | civ-precise | DOWN-grade |
| bookkeeper's role | civ-precise | civ-precise | AGREE |
| witness log | civ-precise | civ-precise | AGREE |
| ternary values | civ-poetic | civ-precise | DOWN-grade |
| JEV as a decision oracle | civ-poetic | civ-formal | DOWN-grade |

Agreement **2/5 (40 %)** — 3 down-grades, 0 up-grades. `civ-poetic` was argmax on **3/5**
prompts and won **0/5**. The series across sessions 211–217 reads
0 % / 40 % / 40 % / 100 % / 60 % / 40 %.

## Verification (24/24 PASS)

- per-civ ledger **+10 × 8 = 80** new rows; `meta_log.jsonl` **+5**
- `wins` = pre + times won, `losses` = 5 − times won — **8/8 exact**
- `relevance` Δ = Σ this run's `avg_score` — **8/8 exact to 1e-6**
- counter gap stable **8/8** (Δ ≤ 1e-6 against the documented per-civ offsets)
- **80/80** rows match an independently recomputed message md5
- **40** distinct seeds over the 80 new rows; **0** `(civ,prompt)` carrying >1 seed
- **8/8** distinct seeds AND previews on every competition prompt (5/5)
- meta-vs-ledger `avg_score` mismatches **0/40** (later-`ts` row)
- 0 JEV errors, 0 `2.0/2.0/2.0` fallback triples
- extinction risk NONE (threshold −10; the lowest civ sits ~183× above it)
- registry still 8 civs, all generation 1, no new civ dirs

## Three durable lessons from this session

1. **THE LEDGER'S CURRENT-GENERATION MOCK ROWS CARRY ONE TAIL, NOT FIVE.** The SKILL file
   records "the tail prefix is per-prompt, 5 distinct strings". Measured against the
   **current-format** rows only (`[0-9a-f]{4}/[0-9a-f]{4}/[0-9a-f]{4}` header), there is
   exactly **1** distinct tail across all 5 prompts and all 8 civs — 161 chars, beginning
   `A cell keeps its own accounts…`. The 5-tail claim describes an older generation, and
   the 9040-row fleet is mostly that older generation. *Filter to the current header
   format before sizing anything off the ledger.*
2. **THE LEDGER ONLY RECONCILES IF THE COLOUR CARRIES ITS `#`.** The recorded header is
   `[mock-zai 71a2] #44cc dd7c/…`; the derived colour is `h[8:12]` = `44cc` **without** the
   `#`. A check that compares the raw slice against the recorded group reports **0/160
   "mismatches"** on a perfectly healthy mock. *The parser normalises; the comparison
   must too.* (My own first pass made exactly this error — 160 false mismatches.)
3. **A FULL-CLONE FETCH IGNORES `core.sparseCheckout` — THE SPARSE FILTER APPLIES AT
   CHECKOUT, NOT AT FETCH.** `git init` + `core.sparseCheckout` + `--depth 1` still
   downloaded **3.4 GB** of the 3.7 GB tree. The clone is only cheap if the *fetch* is
   narrowed. Also: `git fetch --depth 1 origin` resolves **`refs/heads/HEAD`**, which on
   this repo is a symref to a *stale* branch (session 142), **not** `main` (session 216).
   *Fetch `refs/heads/main` explicitly and check `git rev-parse FETCH_HEAD` against
   `git ls-remote origin refs/heads/main`.*

## Also durable

- The workspace was empty again (**8th consecutive** session naming ephemeral paths). The
  upstream was found in **one** call: `GET /search/code?q=civilization_orchestrator+in:path`
  → `SuperInstance/AI-Writings`. `/workspace` is at 100 % NAS quota, so the clone went to
  `/tmp/aiw` and the bridge points at the **inner `code` dir**:
  `ln -s /tmp/aiw/cellular-first-design/code /workspace/repos/ai-writings/cellular-first-design/code`,
  verified with `stat -L -c '%d:%i'` → `129:12697` on both sides and
  `os.path.samefile()` → `True`.
- The mock body was rebuilt to a constant **350** chars (band 332–369): a 39-char header
  (`[mock-zai {seed}] #{color} {figure}.  `) + a 311-char tail whose first **161** chars
  are the recorded ledger's tail prefix, verbatim. The tail's continuation is **150**
  chars, which is the exact allowance the band permits after the fixed 200-char prefix
  (39 + 161 + 150 = 350).
- `ZAI_TOKEN` is still absent (**88th session**): z.ai returns **401 `token expired or
  incorrect`** — endpoint healthy, credential missing. Control B is the only provider path.
  `TYPESAFEAI_KEY` must be exported from `TYPESAFE_AI_TOKEN`; with the alias set, JEV
  returns `jev-1.14.0` and **0** of the 80 new rows is a `2.0/2.0/2.0` fallback.
- **Mock teardown trap, re-confirmed:** `pkill -f mock_zai` **self-matched and killed the
  calling shell** (2nd occurrence of this class). Kill by the exact argv
  (`python3 /tmp/mock_zai.py` and its `timeout -s KILL 900` parent) — two pids — and prove
  the port closed with `curl -m 5` → exit 7 / `HTTP=000`. Also: a **second** launch of the
  same port dies with `OSError: [Errno 98] Address already in use` while the *first* server
  keeps serving — a green probe does not prove *your* process owns the port.
