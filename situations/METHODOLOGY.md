# METHODOLOGY — the SuperInstance development process

*The adoptable, repeatable process. A stranger with their own problem should be
able to pick this up tomorrow. Every stage has a template; the whole thing is
itself quilt-shaped — booked, replayable, gap-authoring — so the method improves
itself the way the software does.*

Companion to [`SUPERINSTANCE.md`](SUPERINSTANCE.md) (the paradigm) and
[`TEMPLATE.md`](TEMPLATE.md) / [`schema.json`](schema.json) (the Situation
contract). Everything cited here already runs unless marked **STRETCH**.

🦋 → ⏳ → 🔧 → 🌊

---

## 0. The loop in one line

**Situation → Gap → Acceptance Test → Wide Run → Failure Map → Rung → Merge → new
Situation** — author a world, mine its friction, compile the friction to a
machine-checkable predicate, run it wide, read what breaks, build the rung that
passes, merge it, and let the world you can now afford to live in name the next
friction.

```
Situation ──friction──▶ Gap ──compile──▶ Acceptance Test
   ▲                                          │
   │                                      wide run
new fiction                            (erised / compiler)
   │                                          ▼
 Merge ◀── build rung ── Failure Map ◀────────┘
```

The one rule that makes it not-a-daydream (`TEMPLATE.md`, Rules of the form): *a
Situation with no machine-checkable acceptance test is a daydream; a Situation with
no gap is a postcard from a place that costs us nothing to visit. Both are rejected
at the door.*

---

## 1. The pipeline, stage by stage

Each stage lists: **what it is**, **its template**, **who owns it** (the roles are
defined in §2), and **its done-test** — the objective condition that lets the next
stage start. Every stage produces a *booked artifact* (§4).

### Stage 1 — Situation
**What.** A grand, character-driven scene set years forward, where the mature
capability is *plumbing* — ordinary, unremarked. Ordinariness is load-bearing: if
the cast is *amazed* by the tech, you wrote a demo, not a Situation. Follow the full
form in `TEMPLATE.md`; the machine twin is `schema.json`.
**Template (minimum viable Situation):**
```
# <title> — Situation S##, horizon <N years out>
WORLD           one lived-in, sensory paragraph. Not a pitch — a place.
CAST (4–6)      each: name, role, the mature rung they embody,
                2–3 erised keyword-vectors (e.g. trust+0.5, ask-0.2).
                Opposite valences on the same noun are where scenes ignite.
LIVED CAPABILITIES   what this world takes for granted that today can't do.
DUAL TRACK      toy: the table version · industrial: the rough-seas version.
```
**Owner.** Author. **Done-test.** A reader who knows today's stack can point at a
sentence and say *"we can't do that yet"* — and an honest author agrees.

### Stage 2 — Gap
**What.** The friction, named. Prefer *new* gaps; a gap must cost you something or it
teaches nothing (`TEMPLATE.md`, Rule 1).
**Template:**
```
GAP { id: G##, future_has: <the capability lived in the scene>,
      prevents: <the concrete failure closing it prevents> }
```
**Owner.** Author → Compiler. **Done-test.** The gap names a *failure it prevents*,
not just a feature it adds. (Model: R1's gap is "a fixed floor sleeps through a
ripple in a calm" — a failure, not a wish.)

### Stage 3 — Acceptance Test
**What.** Compile the gap into a **machine-checkable predicate** against a **named
module** — the moment prose becomes code you could run. This is the stage that
separates SuperInstance from spec-writing: the future's friction becomes a green/red
bar. Compile it into a gap ledger (`GAPS.md`-shaped; **STRETCH** as a live file in
this checkout, real as a discipline — see `FRONTIER.md`'s per-rung "**Test:**"
lines, which are exactly this).
**Template (from `schema.json.acceptance_tests`):**
```
TEST for G##:
  scenario:  <the runnable setup>
  predicate: <exact pass condition, e.g. "illegal == 0 AND transfer_gen < K">
  substrate: <named jev-quilt module / erised preset it runs against>
```
**Owner.** Compiler. **Done-test.** An engineer could code the predicate today
against a named artifact. Worked example (shipped, R1): *scenario:* flat calm + one
0.03 ripple; *predicate:* calibrated floor alarms, 0.05 fixed floor does not;
*substrate:* `jev_quilt/calibrate.py`, asserted in `tests/test_calibrate.py`.

### Stage 4 — Wide Run
**What.** Run the Situation *wide*, not once. `erised` (`/home/user/erised/`) runs
the cast as cooperative fiction — each character its own LLM, on a time economy of
*ticks* and *resonance*, mutating cast keywords across v1/v2/v3 so the same dilemma
plays through different drifts (`erised/README.md`, the "winners" corpus). For a
built rung, the Compiler runs it as a batch/CI predicate (`erised-cli`, headless).
**Template:**
```
WIDE RUN:
  preset:   <erised scenario or jev-quilt test module>
  variants: v1..vN  (drift the cast keywords / regime distance each run)
  record:   scars (errors, starvation), pass/fail per variant, per-tick ledger
```
**Owner.** Verifier. **Done-test.** ≥3 variants run; every scar and verdict booked.

### Stage 5 — Failure Map
**What.** Read what broke, *where*, and *why* — not a pass/fail summary but a map
from friction-point to cause. The model is the `watch_new_loops` reading
(`jev-quilt/examples/watch_new_loops.py`): the instrument names *exactly one*
structurally-blind cell (`jeviter.periodic` — a period a running mean cannot
represent at any window K), and says so with an exact integer test. A failure map
that names one seam beats a report that lists ten symptoms.
**Template:**
```
FAILURE MAP:
  per breaking point: { where (cell/scene), symptom, root cause,
                        is-this-the-gap? (or a new gap G##+?) }
  the one seam: <the single structural cause the rung must close>
```
**Owner.** Verifier + Red-team. **Done-test.** The map names a *structural* cause the
rung can target, and flags any *new* gaps the run surfaced (feed them to Stage 2).

### Stage 6 — Rung
**What.** Build the smallest capability that makes the predicate pass — as **toy and
industrial on one kernel** (the dual-track vow). Never add a workaround that breaks a
law; the five laws were proved (`ENGINEERING.md`: "Don't ignore the 5 laws… adding
workarounds breaks them").
**Template:**
```
RUNG R##:
  toy:        the ≤10-line table version a kid can read (teaches the law)
  industrial: exact-ℚ, offline, deterministic, provable on reboot
  extends:    <the module(s) it builds on>
  law-check:  which of the 5 laws it touches, and why it keeps them
```
**Owner.** Builder (with Red-team on standby). **Done-test.** The Stage-3 predicate is
green; the toy and the industrial build obey the *same* law.

### Stage 7 — Merge
**What.** Land it — gated on CI green and a schema-valid receipt, not on a vibe. The
Goodhart audit (`docs/R8_GOODHART_AUDIT.md`) is why: green-local/red-CI is a real
exploit (E-2), and a prose "receipt" is forgeable in two minutes (E-4). Merge behind
policy: gate on CI (P-2), enforce a receipt schema (decision + verdict + ≥1 of
signature/repro/chain-tip), ban `FAKE_`/`DEMO` receipts.
**Template:**
```
MERGE:
  ci: green (no `|| true` masks)
  receipt: schema-valid { decision, verdict, signature|repro|chain_tip }
  skips: registered in KNOWN_SKIPS (an unregistered skip fails the suite)
```
**Owner.** Builder + Red-team. **Done-test.** CI green, receipt valid, booked.

### Stage 8 — New Situation
**What.** Write the world you can now afford to live in. The merged rung removes a
friction; standing on the far side of it, a new friction is visible that was
invisible before. This is the stage that makes the pipeline a *loop*, not a line.
**Owner.** Author. **Done-test.** A new Situation enters Stage 1 — and, at least
sometimes, its gap is one *the system itself authored* (Rung 3 of the recursion; R4,
**STRETCH**).

---

## 2. The roles

Four roles, which one person (or one person and their models) can wear in turn. On a
small build they rotate; on a fleet they specialize.

- **Author.** Writes the Situation and the new Situation from the far side. Guards
  ordinariness (Rule 5) and the "future must cost us something" rule (Rule 1). Owns
  Stages 1, 2 (with Compiler), 8. *In the fleet, often a model in a Forward-Arc voice
  (`reverse-actualization/`); the physics companions show the register — REAL/STRETCH/
  FICTION marked honestly.*
- **Compiler.** Turns friction into a machine-checkable predicate against a named
  module, and maintains the gap ledger. Owns Stages 2 (with Author), 3. *At its
  mature form (R4, STRETCH) it authors its own gaps and gates on a human yes.*
- **Verifier.** Runs the Situation wide (erised canvas/CLI or the test suite) and
  builds the failure map. Owns Stages 4, 5. *The instrument's discipline: report the
  honest negative, and prove the instrument can't stay deaf (`watch_new_loops.py`, the
  positive control).*
- **Red-team.** Attacks the rung's own success metrics before merge — tries to make
  the KPI *look* better without reality improving. Owns the adversarial half of Stages
  5–7. *The real precedent: `docs/R8_GOODHART_AUDIT.md`, which found live secrets,
  CI/local gaps, forgeable receipts, and a self-referential canary — each fixed or
  turned into a permanent negative control.*

The **Builder** (Stage 6) is whoever writes the code; on a solo build the Author,
Compiler, Verifier, Red-team and Builder are one tired person at a kitchen table, and
the method's whole value is that it lets that one person keep themselves honest.

---

## 3. Cadence — "mostly real work"

The rhythm is a contract, stated in `jev-quilt/docs/IDEATION.md`:

> *Culture and play are bounded — one ideation wave per snowball cycle at most,
> always after the committable unit ships. Agents sing at the TAP after the PRs
> land.*

Operationally:

- **The committable unit ships first.** A rung that passes its predicate and merges
  clean is the heartbeat. Fiction, culture, and play (the overnight journals, the
  shanties, the TAP) come *after* the PR lands, never instead of it.
- **One wave of world-authoring per cycle.** You do not write ten Situations and
  build none; you write one, mine it, build the rung, and only then author the next.
  The far-side Situation (Stage 8) is the sanctioned "play" — and it is also the next
  cycle's real work.
- **Toy and industrial in the same cycle.** The dual-track vow is not a later port;
  the toy is how you *see* the law you just built, so it ships with the rung.

The cadence is why the fleet has an overnight journal *and* a green test suite: the
play is bounded by the law that it follows the ship, not precedes it.

---

## 4. The meta-invariant — the method is quilt-shaped

The deepest claim of this document: **the process obeys the same five laws as the
software**, so it improves itself the way the software does.

- **Every stage is a booked artifact (Law 4).** A Situation, a gap, a predicate, a
  wide-run log, a failure map, a rung, a receipt — each is written to disk, hash-
  chained where it matters (witness log, `ENGINEERING.md`), and *replayable*. You can
  re-run a past cycle and get the same failure map. Development has a golden.
- **Identity never floats (Law 1).** A gap has an exact id (`G##`), a Situation an
  exact id (`S##`, `schema.json`), a rung an exact id (`R##`). No fuzzy "we sort of
  did that." A claim is grounded in a named artifact or it is marked STRETCH — the
  provenance table in `SUPERINSTANCE.md` is Law 1 applied to prose.
- **The stages hook on deltas, not polls (Law 2).** A merged rung *wakes* Stage 8;
  Stage 8's new gap *wakes* Stage 2. Nobody sits polling "is there work"; the delta
  propagates.
- **Decide once, project many (Law 3).** The Situation is decided once and projects to
  a human template (`TEMPLATE.md`) *and* a machine schema (`schema.json`) *and* an
  erised preset *and* a jev-quilt test — one decision, many renders.
- **The process authors its own gaps (Rung 3, recursively).** When a cycle reveals
  that the *method* has a friction — a stage with no done-test, a role with no owner —
  that is a gap in the methodology, and you close it with the same pipeline: author the
  Situation of a smoother method, compile the fix to a checkable change, merge it. This
  file is a rung. The next version of this file is the far-side Situation of this one.

Honest edge (Law 5, viability): the meta-invariant is *aspirational where the
tooling is*. The gap ledger as a live, self-compiling file (R4) is **STRETCH** in this
checkout; the discipline (booked stages, exact ids, named substrates, receipts) is
real *today* and does not need R4 to hold. The method is viable now; it will be
self-authoring when the compiler is.

---

## 5. How a stranger adopts this tomorrow

You do not need the fleet, the boat, or a model. You need a problem you care about
and the willingness to be honest about limits. Do this:

1. **Pick one capability you wish your software had, and set it years forward.**
   Write a half-page Situation (`TEMPLATE.md`): a real scene where that capability is
   *ordinary*. Name 4–6 characters and what each takes for granted. Do not pitch it;
   *live in it.*
2. **Find the sentence you can't honestly write** without inventing something you
   lack. That is your first gap. Write it as `{id, future_has, prevents}` — and make
   `prevents` a concrete failure.
3. **Compile the gap to a predicate against something you can name.** A test file, a
   metric, a script. "Passes" must be a green/red bar, not an opinion. If you cannot
   write the predicate, the gap is still prose — sharpen it until you can.
4. **Run it wider than once.** Even by hand: three variants, three conditions. Record
   what breaks *and where*. If you have LLMs, `erised` gives you the cooperative-
   fiction wide-run for free (`git clone`, open `index.html`, hit Tick).
5. **Map the failures to one structural cause.** Resist listing symptoms; name the
   seam.
6. **Build the smallest thing that turns the bar green** — and build a toy version
   small enough to explain to someone at a table. If the toy and the real thing need
   different rules, your design is wrong, not your ambition.
7. **Merge behind a gate you can't fool.** CI green, a receipt you can't forge in two
   minutes, no silent skips. Red-team your *own* success metric first (the R8 audit is
   the worked example of how).
8. **Write the next Situation from the far side.** Then loop.

You will know it is working when your backlog stops being a list of features you
imagined and becomes a list of frictions you *discovered* by trying to live somewhere
you can't yet go — and when, occasionally, the friction you find is in the method
itself, and you close it the same way.

*Author the world. Mine the friction. Build the rung. Author the next world.*

🦋 → ⏳ → 🔧 → 🌊
