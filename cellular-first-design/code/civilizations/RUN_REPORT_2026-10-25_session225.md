# Civ Orchestrator — Run Report, session 225 (2026-10-25)

Command: `python3 /workspace/repos/ai-writings/cellular-first-design/code/civilizations/civilization_orchestrator.py --sims 5 --prompts 5 --providers zai`

- Provider path: **Control B mock** (z.ai credential gap, **89th session**) + **live JEV** (`jev-1.14.0`, HTTP 200).
- Baseline: `2c02b9cd` (session 224 tree), `refs/heads/main` asserted equal to the clone HEAD.
- **Pre-flight gate: 12/12 PASS** (first build). **Run verification: 16/16 PASS.**

## Session 225 in one line

`civ-precise` took **4/5** competitions and `civ-engineer` the fifth; chooser/argmax agreement was
**2/5 (40 %)** — 3 down-grades, 0 up-grades, every disagreement taking the lower-scoring
candidate; the run-level low was **`civ-therapist`** (avg **1.4950**, fleet-low run quality
**0.9720** and fleet-low run alignment **1.0770**) while `civ-grounded` held the lifetime low
for the **89th** consecutive session (relevance **1977.52**, rel/sim **1.1352**).

## Verification (16/16 PASS)

| Check | Result |
|---|---|
| ledger delta | **+10 rows x 8 civs = 80** |
| `meta_log.jsonl` delta | **+5** |
| `Winner:` lines | **5** |
| `wins`/`losses` vs `meta_log.winner_civ` | **8/8 exact** |
| `relevance` delta vs Σ this run's `avg_score` | **8/8 exact** (max dev 6.4e-13) |
| counter gap vs **full** ledger | grounded −84.35, whimsical −173.14, formal −85.53, poetic −96.80, precise −32.63, mythic −51.11, therapist −42.11, engineer −44.24 — **all at the documented stable values** |
| distinct seeds in run | **40/80 rows** |
| `(civ,prompt)` pairs with >1 seed | **0** |
| independently recomputed message md5 | **80/80** |
| per-prompt distinct seeds AND previews | **5/5** (8/8 and 8/8 on each) |
| meta-vs-ledger `avg_score` (later-`ts` row) | **40/40** |
| JEV errors / `2.0/2.0/2.0` fallback triples | **0 / 0** |
| extinction risk | **NONE** (lowest civ `civ-grounded` at 1977.52, threshold −10) |
| `simulations_run` | **+10** on all 8 |

## Low relevance

**Run low — `civ-therapist`:** avg **1.4950**, run quality **0.9720** (fleet-low), run
alignment **1.0770** (fleet-low), run novelty **2.4360** (mid-field). Gap to the next civ
(`civ-whimsical`, 1.7527) = **0.2577 = 28.8 %** of the run spread **0.8943**.

**The signature is LOW ALIGNMENT, not low novelty — for the 10th session running.** The run's
alignment spread **1.9980** is **2.47x** the quality spread (**0.8100**) and **12.04x** the
novelty spread (**0.1660**). The meta-GAN selects on alignment, so this is a *voice* failure,
not a prose failure.

**Lifetime low — `civ-grounded`:** relevance **1977.52**, rel/sim **1.1352**, lifetime avg
**1.1836**, fleet-low lifetime quality **0.5154** — yet its lifetime `win_rate` **0.088** is
**3rd-best** in the fleet. The three lifetime axes are still three different civs:
quality low `civ-grounded` (0.5154), alignment low `civ-therapist` (1.1947), novelty low
`civ-formal` (1.7129).

**Run low ≠ lifetime low ≠ axis low — report the axis, not the holder.**

## Chooser series

Session 225: `civ-precise` 4 wins, `civ-engineer` 1. Agreement **2/5 (40 %)**,
**3 down-grades, 0 up-grades**; `civ-poetic` was the argmax on **3/5** prompts and won
**0/5**. The widest down-grade margin was **−0.3900** (ternary values:
`civ-poetic` 2.13 → `civ-engineer` 1.74). The series (sessions 211-225) now reads
0 / 40 / 40 / 20 / 100 / 60 / 40 / 40 / 20 / 40 / 20 / 40 / 40 % — *re-derive it every
session; the up-grade count is still **0** across the whole series.*

## Durable notes

1. **The `ls -la` VERIFICATION THE PROMPT ASKS FOR WORKED WITHOUT `-L` THIS TIME** — the
   bridge targeted the **clone root** (`.../cellular-first-design`), and the civs dir sits
   two levels below it, so no symlink boundary is crossed at the last path component. The
   "needs `-L`" rule from sessions 214-217 is a property of *where the bridge lands*, not
   of `ls`. Use `-L` when the last component crosses the bridge; do not assume it always fails.
2. **THE MOCK ALGORITHM RE-DERIVED CLEANLY, AND THE LEDGER HAS **TWO** CURRENT-GENERATION
   COLOUR FORMATS.** Of 1280 current-format rows, **1120 carry the `#`** (`[mock-zai 71a2]
   #44cc dd7c/7cd2/2400.`) and **240 do not** (`[mock-zai ba6b] af26 4577/a9d5/49dc.`). Both
   recompute **1360/1360** against the md5 algorithm — the `#` is a renderer change, not an
   algorithm change. *Filter on the header shape, not on the presence of the `#`.*
3. **THE PRE-FLIGHT GATE NEEDS A REAL LIST COMPREHENSION TARGET, NOT A TUPLE UNPACK.** The
   first gate build crashed with `ValueError: too many values to unpack (expected 3)` on the
   determinism loop — the fixture rows are 4-tuples `(civ, prompt, msg, content)` and the
   loop unpacked 3. The gate had already printed 8 PASS lines when it died. *A gate that
   crashes after several PASS lines is not a passing gate — print a final verdict and exit
   non-zero on any failure, and index the fixture rather than re-deriving it inside the loop.*
4. **THE MOCK BODY LANDED AT **351** CHARS ON THE FIRST BUILD** — a 39-char header, a
   163-char recorded tail prefix and a 149-char continuation. *Compute the allowance from
   the fixed prefix; never iterate prose to fit the band.*
