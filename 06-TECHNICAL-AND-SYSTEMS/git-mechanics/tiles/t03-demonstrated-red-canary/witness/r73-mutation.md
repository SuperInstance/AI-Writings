# Witness: pong-quilt R73 franken-save guard, mutation-tested 2026-10-02

Source: playtest round 73 branch, `tests/r73-franken-save-guard-glue.test.js`
(4 tests). Audit procedure: clone to /tmp/pq-audit, checkout
`playtest-round-73`, run suite → 4/4 green. Mutate the guard at
index.html line 400 (`gen===coev.genC` → `false`), re-run →

    T1 FRANKEN-REFUSAL ......... RED
    T4 BOUNDARY-ESCAPE ......... RED
      exact assertion: "the franken file must never download"
    T2/T3 ...................... green (correctly unaffected)

Restore the guard → 4/4 green. Verdict: R73 is a real canary — its RED
state was demonstrated, not assumed.
