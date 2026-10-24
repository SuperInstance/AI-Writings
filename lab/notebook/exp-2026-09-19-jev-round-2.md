# Lab Notebook — JEV Round 2 (Sept 19, 2026)

## Setup

Six JEV experiments probing the boundaries of the four-model psyche substrate. JEV was queried with structured schemas; calibrated probability distributions returned.

## Experiment 01: Taste the substrate (12th opcode?)

**Question**: Is there a missing 12th opcode beyond BIND/LINK/EFFECT/VIEW/TICK/FORGET/PROOF/ROUTE/CRDT/WORLD/TIME?

| Answer | Value |
|--------|-------|
| needs_twelfth_opcode | **41% yes** |
| missing_opcode_role | uncertain (37% conf) |
| confidence_in_missing | 1.58 / 5.0 |

**Reading**: JEV is roughly split. There IS something missing (41% > 50% baseline), but JEV can't name what. Candidate shapes: synthesis, memory-extended, boundary, time-extended, or "no missing opcode." The substrate is currently in a phase where the opcodes feel exhaustive but the substrate keeps hinting at something unnamed.

**Action**: Continue probing. Keep the question open in /invitation/questions.md.

## Experiment 02: Scale limits

**Question**: What breaks first as the substrate scales?

| Answer | Value |
|--------|-------|
| scales_to_1M | **19% yes** (very low — doesn't scale naively) |
| scale_breakpoint | 0.43 → between 100 and 1K cells (3 sig figs) |
| first_to_break | all_broken_at_once (21% conf — bare plurality) |

**Reading**: JEV is very clear that the substrate doesn't scale naively to 1M. The scale breakpoint is small — ~hundreds of cells before something breaks. JEV doesn't strongly favor any single failing part; the substrate might fail holistically.

**Action**: Add CF KV for cell store. Test at 100 cells. See what fails first.

## Experiment 03: Should the substrate forget?

**Question**: Should FORGET always be JEV-decided?

| Answer | Value |
|--------|-------|
| always_jev_forget | 41% yes |
| forget_strategy | **tiered** (89% conf) |
| what_happens_if_substrate_never_forgets | 2.87 / 5.0 (significant degradation) |

**Reading**: JEV strongly recommends a tiered approach. Most FORGETs should be algorithmic (cheap, fast). Load-bearing FORGETs (decisions with long-term consequence) need JEV. If the substrate never forgets at all, degradation is significant.

**Action**: Implement tiered FORGET — baseline = age-based, override = JEV-decided when σ > threshold.

## Experiment 04: Cell disagreement protocol

**Question**: What happens when two cells disagree?

| Answer | Value |
|--------|-------|
| should_fork | 36% yes (low — substrate leans against forking) |
| fork_strategy | **never_fork** (55% conf) |
| fork_frequency | 3.69 (~0.04% — rare if it happens at all) |

**Reading**: JEV doesn't want forks. The substrate should not need to fork — the loser cell records as scar, continues. This tracks with the "you can't patch over a scar" principle (Sept 16 erised). Disagreement is recorded but doesn't branch the witness log.

**Action**: Forks remain in /invitation/questions.md as an open question. Default to no-fork; scars persist.

## Experiment 05: Embedding framing

**Question**: Is "muscle memory" the right name for the embedding layer?

| Answer | Value |
|--------|-------|
| muscle_memory_is_right | 23% yes (no — JEV prefers another) |
| alt_framing | **trail** (73% conf) |
| importance | 2.28 / 5.0 (mild — naming matters but not load-bearing) |

**Reading**: JEV prefers **"trail"** over "muscle memory." A trail is where something has been. Trail is more honest about retrieval-as-history. Casey has not yet weighed in — naming questions stay open.

**Action**: Re-read paper-psyche-4model.md. Consider substituting "trail" for "muscle memory" in canon. Don't ship yet.

## Experiment 06: Should /lab/ continue?

**Question**: Is /lab/ a phase or a permanent component?

| Answer | Value |
|--------|-------|
| lab_should_continue | 49% yes (basically 50/50) |
| lab_phase | **interim** (56% conf) |
| convergence_proximity | 0.72 (high — JEV thinks we're approaching convergence) |

**Reading**: JEV is split on whether /lab/ continues, but when it does decide, it picks "interim." And it thinks we're 72% of the way to convergence. The substrate is shaping up. /lab/ may merge with /theory/ once we know what the substrate is.

**Action**: Keep /lab/ active for the next 2-3 weeks of experiments. Then merge the lab notebook into /theory/paper-psyche-4model.md or write a paper-lab-iterations.md.

## Cross-experiment findings

1. **JEV is consistently low-confidence on noul questions (conf 0% on all 4 binary questions).** This is interesting — it means JEV's calibrated confidence says "I'm not sure" rather than guessing. The substrate's uncertainty is itself a finding.

2. **JEV is high-confidence on choice questions where the candidates are well-shaped (37%, 73%, 56%).** The schema quality matters more than the question substance.

3. **Score axes work.** "convergence_proximity: 0.72" is a meaningful number to write down and check later.

4. **Multiple models agree on convergent frames.** The 5 fiction pieces cluster at ~75-80% cosine. The 6 JEV experiments show similar low-confidence dispersion. The substrate is consistent in being uncertain.

## Updated /invitation/questions.md

- Q4 (PROOF vs DECIDE): stay open. JEV didn't answer.
- Q5 (missing 12th opcode): JEV says 41% — keep watching.
- Q7 (fork on disagreement): JEV says "never_fork" 55% conf — strong signal.
- Q10 (4-model disagreement): JEV never resolves it; it stays uncertain.

## Notes for next iteration

- Probe the 12th opcode more directly (what would it look like in code?)
- Test the substrate at 100 cells (where JEV says things break)
- Run JEV against /api/expanding-invitation to see if 5 voices converge on the same opcodes
- Build tiered FORGET and benchmark against age-based
