# The Hundred Boats — Situation 01, horizon 10 years out (2036)

WORLD:
Dutch Harbor, the second week of a bad season. A hundred and forty boats out of six
different companies work the same shrinking pollock, and they hate each other the
ordinary way — over price, over grounds, over a net cut in 1998 that three of the
skippers can still name by the hour. What they no longer do is *withhold the water*.
Each boat runs a cell. Each cell keeps its own book — where the fish were, at what
temperature, at what depth, an hour ago, exact — and each fleet keeps a **commons**,
a shared memory of the routes its own boats have proven. Ten years ago that was the
whole of it: your fleet, your commons, your secrets. Then the ice came early in '34
and killed two boats that each *separately* did not know what the boat a mile away
had already learned, and the harbor decided, in the ugly grudging way harbors decide
things, that dying of a fact your enemy already knew was too stupid to keep doing.

So now there is a thing above the six commons — the **Basin**, a commons of commons.
No company runs it. It has no server anyone trusts; it *has no server*. Each fleet
gossips its proven routes as content-addressed deposits, and any boat, in any
company, can read the Basin and answer instead of re-deriving. A greenhorn on a
Trident boat steers off a shoal she has never seen because a Fishermen's Finest
skipper, two seasons ago, booked the route correct forty times and it earned
standing in the Basin. She does not trust him. She does not have to. She trusts the
**root** — the 32-byte fold that says a hundred books agree.

The friction: the Basin works because everyone deposits honestly. And there is money
in the water.

CAST:
- **Renata, skipper of the *Kestrel* (Trident).** Forty seasons. She embodies
  **earned standing that crosses a fleet line** — she can act on the Basin's answer
  without asking her own company, the fastest path there is, and it is revocable the
  instant the Basin proves her wrong. `trust+0.5, ask-0.3, grudge+0.4`.
- **Sable, the Basin's gluer (a cell, not a person).** The role that merges six
  commons into one and must decide *whose weight counts*. Embodies **confluent,
  content-addressed federation across strangers**. `fold+0.6, calm+0.3, drift-0.2`.
- **Okonkwo, skipper of the *Second Wind* (independent, one boat, no fleet).** The
  newcomer with no commons of his own — pure consumer of the Basin, pure test of
  whether a stranger with nothing to deposit is safe anyway. `ask+0.6, trust+0.2`.
- **Vane, broker for a shore-side buyer.** Not a fisherman. Discovered that a route
  deposited into the Basin at a high weight *moves the fleet*, and that moving the
  fleet moves the price. Embodies **the adversary the commons never modeled**.
  `count+0.5, trust-0.4, ripple+0.5`.
- **Dell, the harbormaster's watch.** The calibrated floor at basin scale — in a
  flat market her guard tightens, because the poisoned deposit hides in the routes
  nobody bothers to check. `ripple+0.5, calm+0.3, bored-0.3`.
- **Ilya, who is leaving.** Sold the *Marlin* and is quitting the water. His boat's
  book is woven into two seasons of Basin routes. He wants his tracks *gone* — his
  grounds, his timing, the tell of where he fished when the price was high — and the
  Basin was built on a law that says the witness-referenced is never destroyed.
  `remember-0.4, ask+0.3, trust-0.2`.

LIVED CAPABILITIES:
- A boat answers from a fact a stranger's boat proved, and honors it exactly, because
  it can verify the fold rather than trust the man.
- Six mutually hostile commons converge to the same shared memory *in any gossip
  order*, over a bad radio link, with no coordinator — glue, don't fight.
- A route whose sea has changed loses its standing across the whole basin within a
  few tides of the first boat that books it wrong.

GAPS:
- **G11 — Trust-weighted cross-fleet gluing.** *What the future has that today lacks:*
  today `Commons.merge` sums weights blindly — it assumes every peer is honest, which
  is true inside one account and false between strangers. The Basin needs a merge that
  is still confluent and content-addressed but weights a peer's deposits by *earned
  provenance*, so an untrusted stranger (or a broker) cannot buy the fleet's helm by
  depositing a lie at weight 1000. *The failure it prevents:* Vane steering a hundred
  boats onto empty water — or onto a shoal — to move a price.
- **G12 — Provable forgetting.** *What the future has that today lacks:* the commons
  is append-only and content-addressed; the Forward Arc's own fabric story makes it a
  law — *"the witness-referenced is never destroyed."* But a person has a right to
  leave, and a fleet has a right to shed a route that turned out to encode a boat's
  private grounds. The future can *remove* a deposit and **prove the removal** — a
  tombstone that folds into the root, so replay ≡ live still holds, no phantom weight
  lingers, and no one can silently resurrect the forgotten route. *The failure it
  prevents:* a substrate that cannot forget becomes a surveillance archive nobody can
  leave; Ilya's whole life on the water, readable by his rival, forever.

ACCEPTANCE TESTS:
- **G11 (trust-weighted merge).** Against `jev_quilt/commons.py`:
  ```
  H = honest fleet commons: deposit(route_k, "safe_a", weight=3)   # earned from books
  P = untrusted peer commons: deposit(route_k, "onto_shoal_b", weight=1000)
  B = provenance_merge(H, P, trust={H: earned, P: 0.0})
  PASS  iff  B.recall(route_k) == "safe_a"                          # inflated lie loses
  AND   iff  provenance_merge(H,P,τ).root() == provenance_merge(P,H,τ).root()  # still confluent
  AND   iff  B.agrees_with(other_honest_node_running_same_τ)        # 32-byte agreement survives trust weighting
  ```
  A mid-level planner stops at "merge sums weights." The test is: weight must be
  *provenance × evidence*, and confluence must survive the multiplication.
- **G12 (provable forgetting).** Against `commons.py` + `fold.mmr_root`:
  ```
  C.deposit(k, a, 3); r0 = C.root()
  C.forget(k, a)                                    # books a tombstone leaf
  PASS  iff  C.recall(k) is None  and  C.weight(k, a) == 0
  AND   iff  C.root() != r0                         # removal is a real state change, booked
  AND   iff  mmr_root(surviving_leaves + [tombstone(k,a)]) == C.root()   # a peer replays the delta to the same root
  AND   iff  after C.deposit(k, a, 1): C.weight(k, a) == 1             # no silent resurrection of old weight
  ```
  The hard part is that forgetting must *itself* be a witnessed, content-addressed
  operation — you fold the erasure in, you do not mutate the past out.

TRAINING OBJECTIVE:
- *Human (deckhand → skipper → co-op board):* you can safely stand on a stranger's
  proven work if you verify the fold instead of trusting the man — and you learn, in
  your gut, the difference between "everyone I know agrees" and "the root agrees."
- *Model / agent:* federation across an adversary is not a bigger merge; it is a merge
  that carries provenance and can be *undone provably*. An agent learns that
  append-only is a floor, not a cage — that a substrate people can leave is a substrate
  people will join.

ITERATIVE LOOP:
The '34 ice deaths (fiction) → the Basin (a wide run of six commons gossiping) →
Vane's poisoned deposit surfaces G11, Ilya's exit surfaces G12 → provenance-weighted
merge and tombstone-fold ship as rungs on `commons.py` → a fresh fiction: the first
season the Basin holds against a broker who *knows* it holds, and fishes the seam.

DUAL TRACK:
- **Toy (teach the law):** two paper commons on a kitchen table, index cards for
  deposits, a stranger's card that says "weight 1000, trust me." The kid learns to ask
  *who proved this?* before *how heavy is it?* — and learns to physically tear a card
  out and staple a "removed, here's why" card in its place so the count still checks.
- **Industrial (rough seas):** the Basin over VHF and intermittent Starlink, six
  companies, ed25519-signed deposits, provenance derived from each fleet's booked
  correct/wrong history, tombstones that survive a cold reboot and a replay.

LINEAGE:
- **erised preset:** a fleet-scale fork of `presets/FIRST_SEASON.md` — Renata is Mara's
  earned standing extended across a company line; Vane is a new adversary token
  (`trust-0.4, ripple+0.5`) the preset library does not yet have; Dell is ported
  straight in as the basin-scale witness.
- **jev-quilt rung:** compiles toward `commons.py` past R2 — provenance-weighted
  `merge` and a `forget`/tombstone that folds into `mmr_root`.
- **Forward Arc:** extends `reverse-actualization/09-the-fabric.md` (the federation as
  body) and answers its own what-if — *"What if the glass could forget?"* — not by
  draining the witnesses into the sand, but by folding the erasure in where it can be
  proven.

---

*A hundred boats that hate each other, steering by the same root. Not because they
learned to trust each other — they did not, and Renata still will not say his name —
but because they learned to trust the fold, and the fold does not take sides. The
Basin holds because a stranger's proof and a friend's proof weigh the same on the
scale, and because the man who leaves can take his wake with him and the count still
comes out true.*
