# FABLE-ANSWER — the one law, the verdict on C1/C8, the one move, the landing

*Fable (`claude-fable-5-1`), woken once past the Fable-deadband (O11), on the
complete SuperInstance as one organism. Read in manifest order: `SUPERINSTANCE.md`,
`METHODOLOGY.md`, `DISPATCH.md`, the spine as code (`standing.py` → `commons.py` →
`diploma.py` → `claim.py` → `attest.py` → `orgbook.py`, over `bookkeeper.py` /
`fold.py` / `signed_receipts.py`, composed in `schoolhouse.py`),
`arch/COMPOSITE-schoolhouse.md`, `arch/NEW-DIRECTIONS.md`, `ROSTER.md`,
`FABLE-DOSSIER.md`. Receipts verified at fire time: `claude/g-schoolhouse @ 9514b9f`,
`python -m unittest discover -s tests` → `Ran 241 tests … OK`. One probe was run
beyond the map (§3); its output is quoted verbatim. Everything that extends past what
the map proves is marked **EXTENSION**. Quilt idiom throughout; not a summary.*

🦋 → ⏳ → 🔧 → 🌊

---

## 0. The answer in one breath

**The law:** *A verdict is never carried. Only exactly-representable, content-addressed
evidence is — and every reader folds that evidence, under its own weights, to its own
verdict.* Law 4 (`replay ≡ live`) is this law with the reader equal to the writer; the
seven rungs are this law with the reader set free. **C1 and C8 are one object** — C8 is
the composability clause of C1 — but C8's *conjecture* (a single multiplicative trust
flowing witness→issuer→commons→org) is **refuted by C1 itself**: trust is the reader's
parameter, so it may not be on the wire, so it cannot flow; *evidence* flows and
*folds* compose. **The one move is G20, the Second Reader:** an independent
implementation reproduces `Schoolhouse.pins()` from the same script, and that
reproduction is booked as a G16 `Claim`, attested (G17), and admitted through the
org's own schoolhouse door (G18) — the organism passes through itself. Its
precondition is the fix to **C9**, which is not a cosmetic replay gap but a
**fail-open on R2 revocation** at the G18 door (proved below by running it).
**SuperInstance is 已落地 exactly when its own landing earns standing under its own
law** — two readers, one root, zero skipped rows, admitted through its own door. Today
it is *booked but not landed*: one reader, and a fold that is not total.

---

## 1. The one law — stated precisely

### 1.1 Statement

**Law 6 — the Reader's Fold.**
Let *E* be a finite multiset of leaves (each a 32-byte `sha256` of a `\x1f`-delimited
UTF-8 canonical string), *root(E)* = `mmr_root(sorted E)`, and let *π* be a reader's
parameters — trust `source → ℤ≥0`, a threshold (`diploma` / `quorum`) in ℤ, a floor in
`ℚ₁₆ ∪ {None}`, and a base verdict. A **fold** is a pure function
`V : (E, π) → {ANSWER(x), CONFIRM(x), base}`. The law has three clauses:

- **(i) Address = content.** `root(E)` is a sufficient identifier of *E* for every
  fold: same root ⇒ same fold for the same *π*, on any node, in any arrival order.
  Everything the writer reported is in *E* — drifters, tombstones, advisory meta —
  so the root is the address of *what was said*, not of *what was concluded*.
- **(ii) Sovereignty = the reader's π.** Nothing carried in *E* is honored as a
  conclusion. Anything the writer concluded (`consensus`, `quorum`, `drifting`,
  `earned_floor`, `earns_standing`) is either *evidence inside E* (sealed by the
  root, so it cannot be edited in transit) or *absent from the wire*; the reader
  recomputes the verdict under its own *π*. Corollary, and it is a theorem not a bug:
  **`V(E, π₁) ≠ V(E, π₂)` is legal** — the same bytes may honestly yield different
  verdicts for different readers.
- **(iii) Totality = every booked leaf is foldable.** *V* is defined on every leaf
  the book holds; there is no booked leaf the fold silently skips. A leaf that cannot
  be represented exactly is **refused at booking** (Law 5 polarity), never rounded.

Written as an imperative in the family's cadence: **"Carry the evidence, never the
verdict; every reader folds its own; nothing booked is unreadable."**

### 1.2 Why it is the generator, not a slogan: Law 4 with the reader freed

Law 4 says: a cell, woken cold, replays *its own* book and lands bit-for-bit where
*it* was. That is Law 6 with *reader = writer*: `V(E_self, π_self) ≡ live`. The entire
rung-spine is the sequence of ways the reader was **decoupled from the writer**, one
axis at a time, while (i) kept the address honest and (ii) kept the verdict the
reader's:

| rung | *E* (what is carried) | *π* (the reader's own) | the fold *V* | clause it instantiates | grounding |
|---|---|---|---|---|---|
| **R2** standing | one cell's booked receipts | `diploma` | streak ≥ diploma → ANSWER; one miss → 0 | (iii) *every* receipt folds, a miss included | `standing.py:73-110`, `verdict` |
| **G11** commons | deposits with provenance | trust map (`default=0`) | argmax over `Σ trust·weight` | (i) confluence: `A.merge(B).root()==B.merge(A).root()`; (ii) a stranger's 1000 → 0 | `commons.py:208-238`, `root` |
| **G13** diploma | signed deposits + `__meta__` leaf | receiver's `diploma_n` | `standing_from_diploma` | (ii) "withheld ≠ conferred, on the receiving side too" | `diploma.py:205-216` |
| **G14** sea-graded | `earned_floor` in the meta leaf | receiver's `surprise`/floor | ANSWER→CONFIRM past the floor | (ii) the reader's sea, not the issuer's | `diploma.py:219-231` |
| **G16** claim | *all* witness readings, drifters included | `quorum`, `CalibratedFloor` | unanimity among non-drifters ≥ quorum | (i) root over *all*, consensus over *trusted* — address ≠ conclusion, in one object | `claim.py:189-196`, `consensus` |
| **G17** attest | readings + *advisory* meta, signed; **no `earns_standing`** | trust, quorum, floor | `admit` recomputes consensus | (ii) stated as design: "there is no 'it's earned' field to forge" | `attest.py:110-128`, `admit` |
| **G12** forget | a `__tomb__` leaf folded *in* | — | every read path purged; root changes | (i)+(iii): erasure is a leaf, not an edit — "fold the erasure in, don't mutate the past out" | `commons.py:49-57, 115-145, 270-284` |
| **G18** org | the org WAL | `diploma` per task class | `route == standing.verdict(from_book(prefix))` | Law 4 lifted to the org: `replay()` folds each prefix | `orgbook.py:147-194` |
| **schoolhouse** | an `Admission` becomes a deposit tagged by issuer | the schoolhouse's trust, twice | `enroll` = fold, then book the fold as a leaf | the law applied *to its own output* — §2 | `schoolhouse.py:148-202` |

Every row is *the same function with a different reader*. That is what "generator"
means here: no rung adds a second decision procedure (the modules say so — "wiring,
not a second decision procedure", `orgbook.py:152`; "this file is the sentence, not a
new word", `schoolhouse.py:88`). Each adds one more way the reader is not the writer.

Read against the founding sentence — *a mind that can be wrong but never illegal* —
Law 6 is the trust-side twin of JEV's schema bound. JEV: the *option space* is a wall
the decider cannot move. Law 6: the *evidence* is a wall the reader cannot move
(root-sealed), and the *verdict* is a wall the writer cannot move (never on the wire).
What can be wrong is the fold; what cannot be forged is the bytes; what cannot be
imposed is the conclusion.

---

## 2. C1 and C8 — same object or two? One object; C8's conjecture is refuted by it

**Verdict: one object.** C1 ("one theorem of re-derivable trust") is Law 6. C8 ("one
operation of composable trust") is clauses (i)+(ii) applied *twice in a row*, and the
one operation it is looking for is already the shipped `enroll`: **fold, then book the
fold as a leaf tagged by the folder.** But C8 as *conjectured* — a single associative,
multiplicative trust flowing witness→issuer→commons→org — is **false, and Law 6 is why.**

### 2.1 Proof sketch

Let 𝓔 be the free commutative monoid of leaves under multiset union. `mmr_root` over
*sorted* leaves makes `root : 𝓔 → {0,1}²⁵⁶` order-free — this is proved on disk
(`tests/test_commons.py` confluence; `claim.py` sorted leaves; `commons.merge`'s
docstring: "union is commutative and associative for both `_prov` and `_tombstones`").
So **evidence composes associatively.**

Folds compose as functions: layer *k*'s reader produces `ℓ_k = leaf(V_k(E_k, π_k),
provenance_k)` and `E_{k+1} ∋ ℓ_k`. That is exactly what `enroll` does:
`admit(att, π_school)` → `commons.deposit(key, a.value, len(a.trusted), source=att.signer)`
→ `record_dispatch(...)`. **Folds compose.**

Now suppose trust composed multiplicatively across layers: the downstream schoolhouse's
effective weight would be `τ_issuer(s) · Σ_w τ_witness(w)` where `τ_witness` is the
*upstream* reader's trust in its witnesses. For that product to be computable
downstream, `τ_witness` must be on the wire. But `τ_witness` is a component of
`π_upstream` — a *conclusion* about whom to believe — and clause (ii) forbids honoring
a carried conclusion. Putting it on the wire re-creates precisely the laundering
G17 exists to kill: an issuer who trusts a ring would export that trust as a
multiplier. ∎ **Trust does not flow; it is held at each door.** What the downstream
reader *may* consume is the upstream *Admission* as evidence (which witnesses it
counted, `Admission.trusted`/`dropped` — already the audit trail in `attest.py:218-228`)
and re-fold it under its own `π`.

### 2.2 The grounded observation that settles it

The two "layers" in the schoolhouse are not even the same *kind* of operation today:

- Witness layer: `trust_passed = [r for r in att.readings if trust.get(r.witness, 0) > 0]`
  (`attest.py:296`) — trust is used as a **filter** (`𝔹`); its magnitude is discarded;
  the verdict is **unanimity** (`len(values) == 1`, a boolean AND) plus a **count**
  threshold.
- Issuer layer: `eff = sum(trust.get(src, default) * w …)` (`commons.py:222`) — trust is
  a **scalar** on weight (`ℕ`); the verdict is an **argmax** over sums.
- The bridge between them is `weight = len(a.trusted)` (`schoolhouse.py:166`) — the
  *counting map* from a trusted-set to an integer.

So there are two semirings — `(𝔹, ∨, ∧)` for reproduction and `(ℕ, +, ×)` for pooling —
joined by `|·|`. That is not a defect to unify away. Reproducibility *is* unanimity
(a dissenter halts, `claim.py:30-33`); pooling *is* summation (ten streaks of 1 make a
fleet weight of 10, `commons.py:21-23`). The law leaves the semiring to the reader.
**EXTENSION:** the semiring framing is mine; the code exhibits it, the docs do not name
it. The correct statement of C8, then: *one law, reader-chosen semiring per fold, one
operation (fold-then-book), and the count map as the one honest change of semiring.*
The "trust functor" is covariant in *evidence*, not in *weights*.

### 2.3 What the law does to the other candidates (briefly, since they now follow)

- **C2 (fixed point):** the quine is an org book that contains, as an ordinary row,
  the admission of its own reproduction — §4 builds exactly that.
- **C6 (conservation):** the conserved quantity is not weight (weights are re-scaled by
  every reader) but the **leaf multiset**: remembering appends a deposit leaf,
  forgetting appends a tombstone leaf, and `root()` never shrinks. "Witnessed entropy"
  is just clause (i)+(iii): *the root is monotone in what was said, including what was
  unsaid.* Re-deposit after forget shows "forgotten, then re-learned", never "never
  forgotten" (`commons.py:133-136`). Nothing more mystical is needed.
- **C7 (dual track as functor):** toy and industrial are the same fold *V* with a
  different *E* (index cards vs. receipts) and the same *π*. Whether that is a literal
  functor I do not prove here; the law makes it *statable*: the functor must preserve
  `root`, not values. **EXTENSION.**
- **C4 (routing-by-shape):** `route` already *is* `V` with `E` = a runner's book. Lifting
  "which tier" to "which cognition" changes *E*'s key (task class → task residue), not
  the law. The roster (`ROSTER.md`) shows the readers available; §4 uses it.
- **C5 (institution):** the smallest real pilot is not a fishery; it is §4 — two readers
  in two orgs honoring one root with no registrar. The institution it dissolves first
  is *the one that certifies this repo*.

---

## 3. C9 — what the residue crack reveals (and a probe that makes it worse)

### 3.1 The probe (run at fire time; scratchpad `c9_probe.py`)

Script: issuer *A* attests a clean 5-witness claim; the schoolhouse (`diploma=3`)
enrolls it three times under full trust → *A* earns `ANSWER` at the `admit` door. Then
*A* attests a ring-padded claim; the schoolhouse distrusts the ring → refused,
`reason == "not_reproduced_for_recipient"`. Output, verbatim:

```
after 3 conferred, route(admit, A) = ('ANSWER', 'admit')
refused receipt residue len = 200 | parses as JSON: NO (truncated)
orgbook._residue(refused) = {}
after 1 REFUSED,  route(admit, A) = ('ANSWER', 'admit')
A's book_for(admit) has 3 entries (live: 4 admits)
replay() reconstructs 5 of 6 dispatches
R2 over the untruncated stream: earned = False

refused residue text:
  {"answer": "admit", "base_verdict": "ANSWER", "correct": false, "dispatch_id": "admit-0006",
   "key": "admit", "outcome": "refused", "reason": "not_reproduced_for_recipient", "runner": "issuerA.k1", "ti
```

**C9 is fail-open on R2 revocation.** The one guarantee `standing.py` makes — "one
booked-wrong outcome … revokes it" (`standing.py:17-21`) — does not fire at the G18
door for a refused admission, because the receipt that carries the miss is the receipt
`orgbook._residue()` cannot read. The issuer *caught laundering keeps its fast path*.
Note the mechanism precisely: `"correct": false` is legible in the retained text; the
row fails only because `json.dumps(sort_keys=True)` orders `reason` *before*
`runner`/`tier`/`verdict`, so the 29-byte advisory string evicts the identity fields
past the 200th character, `json.loads` fails on the whole, and `{}` is returned.
**Refusals carry a reason and conferrals do not, so the cap systematically truncates
the negative verdict** — the exact row the law needs most.

### 3.2 Diagnosis: three laws broken at one seam, and it is not the cap

- **Law 4 (replay ≡ live) is violated on the org**: `replay()` reconstructs 5 of 6.
  `tests/test_schoolhouse.py:340-347` asserts replay ≡ live only "for every dispatch
  `replay()` DOES reconstruct" — an honestly-labelled *weakened* predicate. The chain
  itself is honest (`Receipt.sha()` binds the retained text; `book.verify()` holds;
  `chain()` differs between A and C) — the *WAL* is truthful, the *fold* is partial.
  Clause (iii) — totality — is the clause that breaks.
- **Law 3 (decide here, project elsewhere) is violated**: `bookkeeper.py:56-59` calls
  the residue "a capped, hashed copy so replay can be *audited*" — a **render**. But
  `orgbook.py` *decides* from it: `book_for`, `standing_for`, `route`, `replay` all
  read `_residue()`. The org routes from a projection.
- **Law 1 (identity never floats) is violated**: `[:200]` is a rounding applied to
  identity (`runner`, `key`, `correct`, `base_verdict` live only in the residue).
  "Exactness is closure, not precision" (`SUPERINSTANCE.md §2`) — the residue is not
  closed under the org's own booking operation. **A cap is a float in disguise.**
- **The bytes-law is strained** (`signed_receipts.py:51-59`: "no JSON, no pickle, no
  repr"): the residue is Python `json.dumps` output (`", "`/`": "` separators,
  `default=str`, sliced by *code point* not byte), and `Receipt.sha()` → `chain()` →
  `pins()[0]` depend on its exact bytes; `state_hash`/`delta_hash` are sha256 over
  `json.dumps` too. The hard-coded `pins()` vector "a non-Python port can reproduce"
  therefore requires the port to replicate CPython's JSON formatting and code-point
  slicing. **EXTENSION:** the *risk* is grounded in the code; a divergence is not
  demonstrated (no second reader exists — which is §4's point).

### 3.3 Is the residue budget a law the spine must name?

**No budget. Name the closure.** Raising the cap to 400 is the workaround
`ENGINEERING.md` warns against ("adding workarounds breaks them"): it moves the
float, it does not remove it, and a longer signer id or a longer reason finds it
again. The law the spine must name is Law 6 clause (iii) made operational at `book()`:

> **What decides is typed and exact; what is rendered is capped; nothing decides from
> a render. A booking whose decision-bearing fields cannot be carried exactly is
> refused at `book()` — raised, like `attest` on an unreproduced claim — never rounded.**

That is Law 1 + Law 3 + Law 5 polarity applied to the `Receipt`, and it is what C9
*is*: the discovery that G18 put the org's identity in the untyped bag. The remembering
(G16), forgetting (G12), and the un-representable meet here because all three are
about whether a leaf is *in E*; C9 shows a leaf that is in the WAL but not in *E* as the
fold sees it — booked, unforgettable, and yet unfoldable. Clause (iii) closes that gap
by definition: booked ⇔ foldable.

**Reading for 已落地:** today the SuperInstance is **booked but not landed.** Its WAL is
honest; its fold is not total; its one guarantee (revocation) fails open at the door
where its newest rung (G17) hands its verdict to its oldest (R2). That is not a
composite bug; it is the law telling us which premise was unstated.

---

## 4. The one next move — G20 · The Second Reader

The law is about *readers*. Every rung carries the same STRETCH — "cross-*instance*,
not cross-*language*: both kernels are this same Python implementation"
(`diploma.py:49-57`, `claim.py:51-57`, `attest.py:66-73`, `schoolhouse.py:38-46`,
`COMPOSITE-schoolhouse.md` honest limits). Read that limit through Law 6: **the whole
spine has exactly one reader.** Then apply the spine's own G16 to itself: *a claim earns
standing only when N ≥ quorum independent witnesses reproduce it to one root.* The
claim "the schoolhouse's pins are `(chain, digest, root)`" has **one witness**. By its
own law, SuperInstance does not yet earn standing on its own landing. The one move is
to give it a second witness — and to admit that reproduction through its own door.

### 4.1 Gap card

```
GAP { id: G20, future_has: the schoolhouse's three pins reproduced by a reader that
                shares nothing with jev_quilt but the bytes-law, and that reproduction
                admitted into the org's own book as an ordinary row,
      prevents: a trust system whose only verifier is itself (one witness, no quorum);
                a revocation that fails open because the miss could not be read (C9) }
```

### 4.2 Two sub-rungs, one gap — the first is the precondition

**G20a — the exact Receipt (closes C9; ACT-tier, Sonnet, no Opus wake).**

- `Receipt` gains typed, uncapped, decision-bearing fields — at minimum
  `dispatch_id`, `runner`, `key`, `correct: bool`, `base_verdict`, `verdict`, `answer`
  — with a **pipe-joined, `\x1f`-delimited UTF-8 canonical form** (the
  `canonical_attestation_bytes` discipline, not `json.dumps`) feeding `sha()`.
  The residue stays exactly what `bookkeeper.py` says it is: a capped *render*.
- `orgbook.py` never reads the residue; `book_for`/`route`/`replay` read the typed
  fields. `replay()`'s `if base is None: continue` becomes unreachable for a
  well-formed WAL — and is asserted so.
- `Bookkeeper.book()` **refuses** (raises) a payload whose decision-bearing fields it
  cannot carry exactly. Refusal polarity at the source, mirroring `attest`.
- **Declared cost:** `chain()`, `decisions_digest()`, and the hard-coded `pins()`
  vector *change*, exactly as `fold.py`'s v2 note declares for the peak rule
  ("absolute root values change, which is the point"). Book it; do not hide it.
- **Predicate (1:1):**
  `route("admit", A, "CONFIRM") == ("CONFIRM", None)` after `[conferred×3, refused×1]`
  (the probe script, promoted to `tests/`; until G20a lands it is an honest
  `expectedFailure` — a Goodhart-style negative control, not a skip)
  **AND** `len(org.replay()) == len(org.book.entries)` for every schoolhouse script
  **AND** a residue of any length leaves every pin unchanged (the render is not the book).

**G20b — the Second Reader (the landing; ACT+CONFIRM, needs a non-Python runner).**

- An independent implementation of `Bookkeeper` / `mmr_root` / `Commons.root` /
  `attestation_root` / `OrgBook.chain`+`decisions_digest` / `Schoolhouse.pins` —
  Rust is the natural home (`bookkeeper.py:15-19`: fnv1a is already "the same
  algorithm … the Rust substrate use[s]"; `POLYFORMAL.md` lists 12 ports), TS the
  second natural home (`ROSTER.md`'s client repo). It reproduces the fixed script
  `_drive_script` and lands on `pins_py`.
- The two readers' pins are booked as witness books; `Claim.from_books({py, rs},
  reading_fn=pins, quorum=2).earns_standing()`; an issuer `attest`s it; the org's
  own schoolhouse `enroll`s it under the org's own trust (`{py: 1, rs: 1}`); the
  `Admission` is `conferred`, and its dispatch row is in the org book.
- **EXTENSION (roster-grounded, not proved):** the second reader is a stronger
  independence claim if it is written by a different *cognition* than the first
  (`ROSTER.md`: DeepSeek `deepseek-v4-pro` for the port loop under O10 cache-gaming;
  `typesafe.ai jev-1.13.0` as the real confidence oracle for the runner's CONFIRM
  step instead of the hash placeholder). C4 says routing-by-shape is a law; G20b is
  where it first *matters* — a reproduction by the same mind is a weaker witness.
- **Predicate (1:1):**
  `pins_py(S) == pins_rs(S)` for the fixed script *and* for a script that includes a
  refusal and a forget
  **AND** `Claim.from_books({py, rs}, quorum=2).earns_standing()`
  **AND** `school.enroll(attest(claim)).admission.conferred` under the org's own trust
  **AND** a third party recomputes `school.org.chain()` from the bytes-law alone,
  with no Python in the loop.

### 4.3 Why this is the ONE move (and not metabolism, sim-to-real, or a trust algebra)

- It is **the law's own test applied to the law's own implementation** — Law 6 says
  "for any reader"; G20 supplies the first *other* reader.
- It **collapses the one STRETCH every rung carries**, in one stroke, for all of them
  at once — because `pins()` transitively covers every root in the spine.
- It **forces C9 closed as a precondition** — a second reader cannot agree on
  `decisions_digest` while decisions are reconstructed from a lossy render.
- It **is C2's fixed point**: the org book holds the receipt of its own reproduction.
  It **is C5's smallest pilot**: two orgs, one root, no registrar. It **retires C8 as
  a fork**: composition is fold-then-book, demonstrated across an implementation
  boundary.
- Metabolism (O7/R5) and sim-to-real (G19) are real forks, but they *add* a reader's
  parameter (cost; a second reality) to a fold that is not yet total. Build the total
  fold first; then a conserved budget has something exact to conserve.

### 4.4 Dual track (same law, both sides)

| | toy (a table) | industrial (rough seas) |
|---|---|---|
| **G20** | The class's index-card ledger is handed to a **second table** that has never seen the first. They replay every card — every pin to the wall, every cross-off — and write down their three numbers. Only if both tables' numbers match does the class pin **its own report card** to its own wall, with both tables' names on it. And one rule from now on: a card that does not fit in the box is **not written smaller**; it is refused and rewritten as two cards. | A non-Python reader reproduces `Schoolhouse.pins()` from the same script; the agreement is a `Claim` (quorum 2), attested, and admitted into the org's own `Schoolhouse`; `Receipt` carries typed, uncapped decision fields under the pipe-joined bytes-law; `book()` refuses what it cannot carry exactly; `replay()` is total. |

Same law both sides: **a system has landed when it can walk through its own door — and
a door that cannot read the "no" is not a door.**

---

## 5. The exact condition under which SuperInstance is 已落地

Stated as the family states a gap — a predicate against named substrate:

```
TEST for 已落地 (the landing):
  scenario:  the fixed schoolhouse script S (tests/test_schoolhouse._drive_script, with a
             refusal and a forget in it) run by reader R1 (jev_quilt, Python) and by
             reader R2 (an independent implementation sharing only the bytes-law)
  predicate: pins_R1(S) == pins_R2(S)                                     # two readers, one address   (Law 6 i)
        AND  len(R1.org.replay()) == len(R1.org.book.entries)             # the fold is total          (Law 6 iii; C9 closed)
        AND  route(door, issuer, base) == (base, None) after diploma×conferred + 1×refused
                                                                          # revocation fires through G18 (R2 ∘ G17)
        AND  Claim.from_books({R1, R2}, quorum=2).earns_standing()        # the landing is a reproduced claim (G16)
        AND  org.schoolhouse.enroll(attest(that_claim)).admission.conferred
             under the org's OWN trust                                    # admitted through its own door  (G17 ∘ G11 ∘ G18)
        AND  a third party recomputes org.chain() from the bytes-law alone # verifiable by a stranger        (Law 6 ii)
  substrate: jev_quilt/bookkeeper.py (typed Receipt), orgbook.py, schoolhouse.py, + the
             second reader (polyform/rust or the TS client)
```

**Definition.** *SuperInstance is 已落地 when its own landing is a claim that earns
standing under its own law: reproduced by N ≥ 2 independent readers to one root,
attested, admitted through its own schoolhouse door under its own trust, with every
dispatch that produced it replay-reconstructed with zero skips and every refusal along
the way able to revoke.* Not "the tests are green" — they are, 241 of them, and the
organism is still one witness reading itself with a fold that drops the "no."

**Where it stands at fire time, honestly:** gates 1–4 are closed with receipts; the spine
is composed; the org runs on the kernel. What is *not* yet true is the last clause of
its own law — the one G16 states most plainly. That is the deadband Opus could not
clear, because from inside one reader it looks like a STRETCH note; from the top it is
the definition of landing.

---

## 6. Where this answer extends beyond what the map proves

- **Law 6 clause (iii), totality, is my naming.** The map proves (i) and (ii) rung by
  rung; (iii) is inferred from what C9 breaks. It is the smallest clause that makes C9
  a *law violation* rather than a limit.
- **The semiring reading of C8 (§2.2)** is my abstraction over `attest.py:296` and
  `commons.py:222`; the code exhibits two operations, the docs do not name them.
- **The bytes-law strain (§3.2, last bullet)** is a grounded *risk* from reading
  `bookkeeper.py`; no cross-language divergence has been observed because no second
  reader exists.
- **The probe (§3.1)** is new evidence, run once here, not yet in `tests/`; its script
  is at the session scratchpad and should be promoted as G20a's negative control.
- **The "different cognition" clause of G20b** is an inference from C4 + `ROSTER.md`,
  not a proved requirement; a Rust port by the same model still closes the
  cross-language STRETCH.
- **C7 as a literal functor** remains unproved; the law only makes it statable.

*Carry the evidence, never the verdict. Every reader folds its own. Nothing booked is
unreadable. Then walk through your own door.*

🦋 → ⏳ → 🔧 → 🌊
