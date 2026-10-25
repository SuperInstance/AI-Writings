# B8 system2-redesigner — DONE candidate

**Status:** DONE candidate (branch `claude/b8-system2-redesigner`, no PR by request). This note is for the operator to flip the B8 row in `situations/arch/ACTIVELEDGER-CELL-GRAPH.md`.

- **Loop closed:** propose (cheap-model crew or stubs, in a 12-op/5-guard route DSL) → B7 `backtest_pair` gate on 286 cases (product identity FIRST; one miss or crash = refused) → B4 `prefer`/`PreferenceBook`/`prefer_axes` promotion per traffic regime. B7 and B4 are imported unmodified (their selftests still pass at 38/0 and 57/0).
- **Selftest:** `python3 selftest.py` → `system2-redesigner selftest: 68 checks, 0 failures` (offline, stub proposals). It covers refusal of product-changing proposals, crash refusal, the B4 re-gate, regime-dependent promotion, and dedupe.
- **Live crew (measured):** 24 proposals from 5 distinct DeepInfra models across 2 rounds. **13 unique passed the gate, 5 were refused by B7 with counterexamples, 6 were duplicates (including the incumbent rediscovered twice), and 0 failed parse or execute.** 5 were promoted to a regime frontier. The plain round produced 0 refusals and the bold round produced 5. Pushing the crew to take risks is what exercises the judge.
- **Scar logged:** the first version priced the incumbent and the proposals with two different cost tables, and that made a re-expression of the incumbent look 30% cheaper. It is fixed now: there is one cost model, and the quilt run serves only as the product oracle.
- **Honest limits:** the budgets are modeled, not wall-clock. The gate is corpus-bound, so the risky passes were also audited exhaustively over 2-character prefixes, with 0 mismatches in 98,304 cases. Only one quilt (EX4 text-normalize) is wired so far; the other quilts need their own DSLs.
