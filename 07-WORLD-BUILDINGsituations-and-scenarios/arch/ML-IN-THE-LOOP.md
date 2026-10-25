# ML in the loop — baking learning into the iterative git CI/CD structure

*A think-mark (2026-09-29). Not a repo yet — the shape, so the next shipwright can build the
first cell when we've lived enough of it. Ties to GPU-DOCKET.md (local training), THE-WEAKEST-CLAIM-METHOD.md
(the audit gate), the fishing-fleet skill (the loop), and the dispatch-ledger (the dataset).*

## The reframe: the pipeline already emits its own training set

Most teams bolt an ML system onto CI. In this fleet you don't have to, because the iterative
git structure is *already* a labeled, versioned, reproducible event stream:

- **Every commit is a labeled example.** `diff` = the change (features), `message` = the intent
  (a time-capsule), the CI result = **the label** (green/red, time-to-green), and any later
  revert/fix commit = a *delayed* label (this change was actually wrong).
- **The dispatch-ledger is a decision log.** Each row is `(task, tier, model, verdict, standing,
  status)` — a `(state, action, outcome)` tuple. That is an RL trajectory, already booked.
- **Receipts make every run a reproducible example.** Quilt cells are hash-chained and byte-exact
  across substrates, so a CI run is a replayable `(input → output → verdict)` with provenance
  built in. The MLOps nightmare — "we can't reproduce the training data" — is solved by
  construction: **git + receipts ARE the versioned dataset, temporally ordered.**
- **JEV is a cheap labeling function / reward.** The decomposing fold doesn't just say pass/fail;
  it *localizes* which part of a change is weak — per-file, per-claim labels, not one scalar.
- **Moth is un-gameable exploration.** Quantum draws pick which experiments/adversaries fire, so
  the loop can't quietly overfit to a test set someone steered.

So "bake ML in" = **close the loop**: let the pipeline learn from its own iteration history to
make the next iteration better — with the same receipts, oracles, and marks it already runs on.

## A model is a cell (so this isn't a new system — it's one more cell)

The org's own doctrine: *"AI is not a framework bolted onto the side. It is a cell. It has
inputs, outputs, freshness rules, dependencies, receipts, and reproducible behavior like
everything else."* A learned model in CI is exactly that cell — fed by the receipts the graph
already produces, gated by the same JEV/Moth contract, versioned like any other cell. The
pipeline that builds the fleet becomes **a learning cell inside the fleet**. Quilts inside quilts.

## Continuous Training, folded into CI/CD (the CT step)

Add one step to the loop, on the iteration's own cadence:

1. **On merge** — append the realized `(diff, message, CI-outcome, JEV-fold, receipt)` to the
   repo's dataset (it's just more commits; the data is the history).
2. **Nightly / on the local GPU** — incrementally (re)train a small predictor on commits *before
   time T only* (git's order prevents leakage). This is a GPU-DOCKET job: a ≤3B QLoRA or a tiny
   from-scratch net fits the RTX 4050; the training is cheap because the labels are free (CI + JEV).
3. **Next iteration** — the updated model advises/gates the next PR. **Checkpoints are Released +
   receipted, and the model's own accuracy is booked in the ledger** — the model is honest about
   itself, same as any cell. A model that got worse is a scar, booked, not hidden.

## Three CI gates the learning cell can drive

- **Change-risk predictor.** On PR open: read the diff + the repo's commit/CI history → emit
  `P(this breaks CI or needs a fix within N commits)` as a CI status. First buildable POC — the
  labels already exist in every repo's log. (Start here.)
- **Learned dispatch router.** "Route by JEV verdict" becomes "route by a policy JEV bootstrapped":
  which model/tool for which task, trained on past ledger outcomes (cost, time-to-green, quality).
  The fishing-fleet captain gets a learned prior for who to hand the oars to.
- **Weakest-Claim audit gate.** On a change to a guarantee/spec, run the fold + a Moth-drawn
  adversary; **fail the build if the located weakest claim's adversary hit-rate rises.** The
  fold's calibration itself improves as `JEV-USAGE-LOG.md` accumulates.

## Guardrails — pre-registered, because a naive loop rots (Law 7 discipline)

- **Reward hacking / metric-pleasing.** A model trained to make CI green learns to please the
  metric, not to be correct. *Mitigate:* Moth-drawn, un-gameable eval sets + JEV as an
  **independent-reach reader** (Law 7 — buy reach across the boundary you're blind at; don't
  average correlated opinions).
- **Self-confirmation feedback.** A model trained on its own past decisions calcifies. *Mitigate:*
  always hold out *real* downstream outcomes (did the change actually get reverted?), and keep a
  **quality-diversity archive** (`labs/qd-arena`) so the loop keeps a map of good behaviors instead
  of collapsing to one mode — beyond GAN, on purpose.
- **Leakage.** Train only on commits before the cutoff; git's temporal order + receipts enforce it.
- **Known blind spots.** JEV is confidently wrong on counting/spelling — don't let it be the sole
  label there; buy a symbolic reader (the G21 move). The model inherits the oracle's blind spots
  unless you buy reach around them.
- **Honest labels.** The "a booked scar beats a covered result" ethos is not just culture here —
  it's *clean training data*. Hidden failures are mislabeled examples; booked ones are gold.

## The first cell to build (when we've lived enough of it)

`labs/ci-brain/` (DRAWN): a change-risk predictor trained on *this* fleet's own commit + CI +
ledger history, on the RTX 4050 (GPU-DOCKET D4/D5 shape), emitting a JEV-refereed risk score as a
CI status, checkpoints receipted, accuracy booked. Small, honest, reusable — and, like `jev-fold`
→ `weakest-claim`, a tool that once it works is reused to make the loop that makes better tools.
Don't build it until a repo's history is rich enough that the predictor beats the base rate — then
it's earned, not asserted.

## The one-line version

The git loop already writes the dataset, CI already writes the labels, JEV already scores, Moth
already keeps it honest, and receipts already make it reproducible. Baking ML in is just adding
one more cell — a learner fed by the loop's own receipts, gated by the same oracles, versioned by
the same marks — so the pipeline that builds the fleet learns from the fleet it has built.
