# Scenario 01 — The Junior Dev

**Principle probed:** #1 — The agent as Natural-language-to-code compiler
**Disc:** The coder with the agent-as-compiler
**Year:** 2080
**Constraint:** The protagonist has never seen a voltage. They think in functions. The agent compiles.

---

## The setup

Maya is 22. She just graduated from a CS program that no longer teaches syntax. The curriculum is *function-first*: students learn to specify behavior, not to write implementations. The agent compiles. Maya's "Hello, world" assignment was a 200-word natural-language description of a counter that walks through an array, summing it. She has never seen C. She has never seen Python. She has never seen Rust. She has never seen the inside of a compiler.

She has, however, seen the inside of *an agent* — she took "Agent Internals" her junior year, a survey course that covered prompt routing, function-calling, the multi-model inferencing that lets the agent pick the right language for the job. The course used the Quilt substrate as its case study.

Today is her first day at a small startup. The startup maintains a piece of legacy code — a real-time pricing engine — that was written in 2025 in *twelve languages*, polyformally, because the team in 2025 was the last generation that thought in *languages* instead of in *functions*. The code is a mess by 2080 standards: it has 12 different syntaxes, 12 different build systems, 12 different dependency trees. The substrate has changed the way new code is written, but the legacy code still has to be maintained.

Maya is assigned to add a feature. She has to add a feature to a codebase she cannot read.

The question: how does the substrate help her? What does the substrate *do* that the legacy code does not? What does the agent *not* do that she has to do herself?

## The throw

The scenario throws Maya at the legacy codebase and asks: *what does the substrate do for the user that the user has to do for herself in the old way?* The answer reveals the difference between *thinking in language* and *thinking in function* — and what is lost, and what is gained.

## The constraint

Maya has never seen a voltage. She has never seen a compiler. She has never debugged a segfault. She has never read a stack trace. The substrate is her *only* way in. If the substrate fails her, she has nothing. The throw tests whether the substrate is *enough*.
