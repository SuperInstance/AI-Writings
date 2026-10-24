# The Table and the Wheelhouse — Situation 02, horizon 6 years out (2032)

WORLD:
A two-room school on a spit of gravel above a working harbor, forty-one children,
one teacher, and a woodstove. This is not a coding class. On the long table in the
front room there is a **toy** — a wooden box with a single dial, a bell, and a
ledger of index cards — and the whole of the first grade's autumn is learning to
make the box tell the truth. A cell holds a number: *0.73 as what?* A hook eats a
change, not a value: nobody stares at the dial, the bell rings when it *moves* past
a line the child chose. Every change is written on a card; pull the box's plug, put
it back, read the cards, and the box is exactly where it was. The children learn the
five laws the way an earlier generation learned to tie a bowline — with their hands,
at a table, before they ever needed it.

Out the window, forty feet down the ramp, is the **wheelhouse** — the same law, with
the sea put back in. The boats run the industrial kernel: exact-ℚ decisions offline,
provable after a reboot, a calibrated floor that tightens in a flat calm because the
rogue set hides in the flat water. The doctrine the whole village lives by is *two
builds, one kernel* — the box on the table and the box in the wheelhouse must never
drift into two different laws, or the school is teaching a lie and the children will
find out in the worst possible way, at night, in weather.

The friction is the ramp itself. A child earns her *diploma* on the box — books three
correct decisions in a row on some small thing, and the box lets her **ANSWER**: stop
asking, recall the proven move. Everyone can see it happen; the bell goes quiet and
she just *acts*. The question the village has never been able to answer honestly is:
**what is that diploma worth forty feet down the ramp?** Does the standing she earned
at the calm table mean anything in the wheelhouse when the sea comes up — and if it
does, does it mean it *safely*?

CAST:
- **Mrs. Pell, the teacher.** Thirty years, half of them on deck before her knee gave
  out. Embodies **the toy→industrial morphism as a human act** — she is the one who
  decides, every year, which child is ready for the ramp. `trust+0.4, ask+0.3, calm+0.4`.
- **June, eleven, top of the class.** Earned every diploma the box offers. Embodies
  **portable earned standing** — and its temptation: she believes her table-standing
  is a wheelhouse-standing, and she is about to be right in a way that is dangerous.
  `trust+0.5, ask-0.4, count+0.5`.
- **Theo, nine, slow and stubborn.** Routes his ignorance beautifully — asks the exact
  right question every time. Embodies **the deckhand who is safe because he asks** and
  the proof that a diploma withheld is not a diploma failed. `ask+0.6, calm-0.2`.
- **Cap, June's father, a skipper.** The wheelhouse. He will honor a diploma from the
  table *only if the receipt verifies on his kernel* — and only if it was earned in a
  sea like the one he is in. Embodies **sea-graded admission**. `trust+0.3, ask-0.2, grudge+0.3`.
- **Dell, the watch (a cell on the school box and again on the boat).** The same
  calibrated floor in both rooms — quieter at the table, tighter in the chop. Embodies
  **the one law that must be identical across the ramp**. `ripple+0.5, calm+0.3, bored-0.3`.
- **The Inspector, from the state.** Wants a certificate: *this school's diploma is
  equivalent to a competency on the water.* Cannot get one, because no one can yet
  prove the two builds are the same law. Embodies **the gap made bureaucratic**.
  `count+0.4, trust-0.3, ask+0.2`.

LIVED CAPABILITIES:
- A child earns standing on a toy and it *transfers* — the exact receipt she earned at
  the table is admissible in the wheelhouse, honored not because she is trusted but
  because the book replays to the same root under the boat's own kernel.
- The transfer is *sea-graded*: standing earned in a calm does not silently confer in a
  gale; the calibrated floor she was proven under travels with the diploma and revokes
  it the moment the sea outruns it.
- A parent, an inspector, and a kernel all read the same proof of competence — teaching
  that transfers is teaching that *checks*, in both directions.

GAPS:
- **G13 — Cross-substrate standing morphism (the portable diploma).** *What the future
  has that today lacks:* today `Standing.from_book` derives standing from *one* book on
  *one* kernel; there is no proof that standing earned on the toy substrate is
  admissible on the industrial substrate. The future has a **morphism** — a signed,
  content-addressed receipt of an earned streak that a *different* kernel can verify by
  replay, conferring `earned(k)` there iff the receipt's book folds to a valid root
  under the receiving kernel's own law. *The failure it prevents:* the two builds
  drifting into two different laws — a diploma that means one thing at the table and
  nothing (or worse, something false) on the water.
- **G14 — Sea-graded standing transfer.** *What the future has that today lacks:*
  standing carries the *conditions it was earned under*. Today `verdict` returns
  `ANSWER` whenever the streak is met, blind to whether the sea has changed. The future
  binds a transferred diploma to the calibrated floor it was earned beneath, so an
  imported `ANSWER` **automatically degrades to `CONFIRM`** when the receiving sea's
  surprise exceeds that floor. *The failure it prevents:* June acting on her calm-water
  reflex in weather it was never proven in — the exact way confidence sinks boats.

ACCEPTANCE TESTS:
- **G13 (portable diploma).** Against `jev_quilt/standing.py` + `commons.py` + signed
  receipts:
  ```
  toy_book: 3 booked-correct decisions on key k  ->  S_toy = Standing.from_book(toy_book)
  receipt  = sign(S_toy.deposits())               # ed25519 / blake3, content-addressed
  S_ind    = Standing.from_receipt(receipt, verifier=industrial_kernel)
  PASS  iff  S_ind.earned(k) is True   when receipt.root replays valid on the industrial kernel
  AND   iff  Standing.from_receipt(tamper(receipt)).earned(k) is False   # inflated weight / bad sig / root mismatch rejected
  AND   iff  the same k, un-earned on the toy, yields earned(k) is False on transfer   # withheld != conferred
  ```
- **G14 (sea-graded transfer).** Against `standing.py` + `calibrate.py` + `predictor.py`:
  ```
  earn ANSWER for k under CalibratedFloor tightened in a calm regime (surprise << floor)
  transfer S into a rough regime where predictor.surprise(k) > floor_at_transfer
  PASS  iff  verdict(S, k) == ('ANSWER', a)      while surprise(k) <= floor
  AND   iff  verdict(S, k) == ('CONFIRM', None)  the tick surprise(k) > floor   # auto-degrade, not silent recall
  AND   iff  standing re-earns ANSWER once the sea calms and k books correct again  # revocable both ways
  ```
  The subtlety a mid-level planner misses: the diploma must carry its *floor*, not just
  its streak. Standing without its calibration is a certificate with the weather torn off.

TRAINING OBJECTIVE:
- *Human (child → deckhand → engineer → inspector):* a diploma is a *replayable proof*,
  not a paper — and a proof earned in calm water is honest only about calm water. The
  child learns the law with her hands; the inspector learns that "equivalent competency"
  is a thing you can *check*, not decree.
- *Model / agent:* transferring a learned policy across substrates is not copying
  weights; it is carrying a verifiable book *and the conditions it was valid under*. An
  agent learns to refuse its own imported confidence when the sea it is in outruns the
  sea it was proven in.

ITERATIVE LOOP:
The ramp (fiction) → the Inspector's impossible certificate names the gap → a wide run
of children earning table-diplomas and skippers refusing or honoring them →
`from_receipt` and sea-graded `verdict` ship as rungs → a fresh fiction: the first
season a state certificate is issued that means *the same law, at the table and at
sea*, because the kernel can finally prove it.

DUAL TRACK:
- **Toy (teach the law):** the wooden box, index-card ledger, a dial and a bell. A child
  earns the right to stop asking on one small thing and can watch the bell go quiet. The
  diploma is a card she can carry to the next box and have it *checked*, not believed.
- **Industrial (rough seas):** the wheelhouse kernel, offline exact-ℚ, ed25519 receipts,
  a calibrated floor over a real predictor, a diploma that is admitted only after its
  book replays and only while the sea stays inside the floor it was earned under.

LINEAGE:
- **erised preset:** blends `presets/FIRST_SEASON.md` (Jonah the apprentice, Dell the
  watch) with `presets/VALLEY.md` (the table of colliding roles). June is a new cast —
  earned standing that has not yet met the sea (`ask-0.4, trust+0.5`).
- **jev-quilt rung:** compiles toward the **teaching ladder** made rigorous, and toward
  R6 (the learning kernel that stays bit-checkable) — the toy and industrial kernels
  proven to be one law by an admissibility morphism on `standing.py`.
- **Forward Arc:** extends `reverse-actualization/05-the-lighthouse-keepers-son.md` (a
  boy learning the balance of a falling thing) and the apprentice-watch stories — the
  discovery that the thing you learn at the table and the thing that keeps the boat off
  the rocks are, provably, the same thing.

---

*Forty feet of gravel ramp between the table and the wheelhouse, and the whole village
built its schooling on the bet that the same law runs at both ends of it. The diploma
June carries down the ramp is not a paper her father chooses to honor; it is a proof his
kernel replays in front of him, and it comes with its weather stapled on. She earned the
right to stop asking in a flat calm. The sea will tell her, exactly and in time, when she
has to start again.*
