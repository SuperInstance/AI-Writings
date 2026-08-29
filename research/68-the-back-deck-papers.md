# The Back Deck Papers: The Tote Rule, the Night Cron, and Why the Paragraph Is the Pipeline

**Authors:** SuperInstance Research Team (back-deck lane)
**Paper Number:** 68
**Date:** August 2026
**Status:** Application doctrine — the canonical quilt application spec, formalized from the captain's dictation
**Subject:** A fish boat's camera system as the exemplar of distribution-first, application-first quilt thinking: the crew's existing sorting behavior is the labeling pipeline; the wiring that harvests it is quilt cells, not a programmer's ML stack. Companion fabric document: quilt-verilog `docs/BACK-DECK-APP.md`.
**Voice note:** The pipeline below was dictated by Casey (F/V EILEEN) in one sitting, in plain sentences about fish, totes, hooks, scales, and night shifts. The sentences are quoted where they matter. The formalization is ours; the constraints are his. Nothing in the dictation was dropped — every sentence below is load-bearing.

---

## Abstract

The fleet's iceberg has a tip called The Tap and a waterline called The Boat (F/V EILEEN). Between them sits an unanswered question: what does an *application* look like when the substrate is a quilt — cells, links, dials, ticks — instead of a programmed pipeline? This paper formalizes the answer using a real, dictated spec: a back-deck camera system that learns salmon species identification, hook-and-depth counting, weight record-keeping, and nightly self-improvement — with **zero extra work by the crew and zero programmers in the loop**. The load-bearing insight is that the crew already labels everything: *where a fish is thrown is what a fish is*. The port tote means pink/humpy. The center hold means chum/dog/keta. The fore and aft starboard half-totes mean king/chinook and coho/silver. A camera watching the existing gesture gets ground truth as good as the crew — because the crew **is** the ground truth. Every plain sentence in the dictation maps to one or two cells: constraint-cells, alias-tables, timestamp-match cells, count-cells, night-cron cells, A/B cells, audit cells, ledger cells. Spreadsheet-vibe wiring, no programmer. The paper gives (1) the sentence-by-sentence decomposition, (2) the argument for why this beats conventional ML-pipeline architecture, (3) the constraint vocabulary it implies for the cell layer above the silicon, (4) the data-flow diagram in text, (5) the generalization — the tote-rule pattern: human action as free labeling — and (6) the honest failure modes: mis-sorted fish poisoning labels, cross-camera overlap windows, and night-retrain drift, each with its mitigation wired as a cell.

---

## 1. Introduction: a spec dictated in fish

Conventional ML system design starts with a data problem: *we need labels.* Then it spends its budget solving the labeling problem — annotation contractors, labeling tools, active learning loops, human-in-the-loop review queues. The budget is spent where the work is invented, not where the work already happens.

The quilt doctrine (quilt-verilog `README.md`, `docs/DOCTRINE.md`) says intelligence is cellular: everything is a cell, everything touches everything through five opcodes (qm_bind / qm_link / qm_effect / qm_view / qm_tick), state is a file (QUF), and composition is wiring, not scheduling. The doctrine has been proven at the silicon layer. What it has lacked is a canonical *application*: a real system, dictated by a real practitioner in plain sentences, that a cell layer can host without a programmer translating the sentences into an ML stack.

The back deck of a salmon troller is that application. Casey dictated the whole system in one pass. This paper is the formalization. The dictation is reproduced as constraints in §2, one numbered block per pipeline stage, quotes preserved.

Three properties make this the exemplar:

1. **Distribution-first.** Ground truth is not collected and shipped to a training pipeline; it is *distributed at the point of action*. Every fish landing event creates a labeled example at the tote, where the label was already decided by a human hand.
2. **Application-first.** The spec never mentions model architecture, loss functions, or frameworks. It mentions fish, totes, hooks, fathoms, scales, openings, and nights. The cells that satisfy it are wired from those nouns.
3. **Self-improvement on schedule, no babysitting.** The system retrains itself overnight and A/B-tests the challenger against the incumbent the next day on the crew's continued sorting — no Wesley-iteration, no human in the retraining loop. As the iceberg's arc goes, this is Wesley moving to the wheelhouse and the system teaching itself underneath him.

---

## 2. The paragraph is the pipeline

The dictation, decomposed. Each block quotes the constraint (Casey's voice) and names the cells it implies. The cell names are the fabric's vocabulary; the full cell graph, links, and dials live in the companion doc `quilt-verilog/docs/BACK-DECK-APP.md`.

### 2.1 Tote placement is the ground truth

> "Deck cameras learn species ID from TOTE PLACEMENT as ground truth: fish thrown in the PORT tote = pink/humpy (either name overheard in deck conversation — aliases are data); center hold = chum/dog/keta; fore & aft starboard half-totes = king/chinook and coho/silver. The ML gets as good as the human crew because the crew's own sorting IS the label."

Cells:

- **TOTE-RULE cells (×4)** — constraint-cells, not classifiers. One per destination: TOTE-PORT, TOTE-HOLD, TOTE-STBD-F, TOTE-STBD-A. Each observes "a fish crossed into my volume" and *emits* the species ground truth as a hard rule, not a prediction: port → pink, hold → chum, fore-starboard → king, aft-starboard → coho.
- **ALIAS cell** — the alias-table. `pink ≡ humpy`, `chum ≡ dog ≡ keta`, `king ≡ chinook`, `coho ≡ silver`. Overheard deck conversation carries either name; both resolve to the same canonical ID. The table is data, not schema — a new alias overheard on the deck is a row, not a migration.

The sentence "the crew's own sorting IS the label" is the whole thesis. There is no labeling step, no annotator, no review queue for labels. The ML's ceiling is the crew's sorting accuracy, and its improvement path is the crew's consistency — which is high, because sorting is the crew's actual job.

### 2.2 Cross-camera identity handoff

> "Underwater camera watches a fish leave frame; a deck camera catches the first surface break; timestamps match → same fish → the tote label propagates back to the underwater sighting automatically."

Cells:

- **XID-MATCH cell** — a timestamp-match cell. Input: (leave-frame event with timestamp) from CAM-UW, (surface-break event with timestamp) from a deck camera. Within the match window: same fish. Output: the underwater sighting inherits the tote-derived species label retroactively. The underwater footage — the hardest, most valuable data (fish in their own element) — gets labeled for free by an event that happens *after* the camera stops seeing the fish.
- The handoff is asymmetric and that is the point: the deck is the label source, the underwater is the label *sink*, and the link is a timestamp correlation, not a tracker.

### 2.3 Sounder self-training by hook counting

> "The deck camera can COUNT HOOKS on the vertical troll gear (30 hooks, 1.5 fathoms apart) and the cannonball depth at the bottom is known by hook count — so the echogram-watching agent gets labeled training data WITHOUT the underwater camera. Sounder inferencing improves nightly."

Cells:

- **HOOK-COUNT cell** — a count-cell. The gear's geometry is known: 30 hooks, 1.5 fathoms apart. Counting visible hooks in the water column multiplies out to cannonball depth. Known depth + echogram at that moment = a labeled (sounder image, depth) pair. The trolling gear is a depth sensor made of rope, already deployed, already maintained, already paid for.
- **SOUNDER cell** — the echogram-watching agent. It receives labeled depth data *without* needing the underwater camera. This decouples the sounder's training from the most failure-prone sensor on the boat. "Sounder inferencing improves nightly" is not a hope; it is a schedule (§2.4).

### 2.4 Overnight autotrain, A/B the next day

> "The computer has the boat to itself at night — retrain the sounder model on the day's new labeled data, A/B test the updated version against feedback cells the next day. No Wesley-iteration babysitting; the system improves itself on schedule."

Cells:

- **NIGHT-CRON cell** — a cron-cell. At night, when the boat is idle, the day's labeled data retrains the sounder model. Night is a resource: free compute, free power headroom, no contention with live camera streams.
- **AB-PROMOTE cell** — the A/B cell. The retrained model is the *challenger*; the deployed model is the *incumbent*. The next day's fishing is the test set — because the crew keeps sorting into totes, the feedback cells (TOTE-RULE outputs) are continuous fresh ground truth. The challenger is promoted only if it beats the incumbent on that day's feedback; rollback is the default outcome.
- "No Wesley-iteration babysitting" — the improvement loop is scheduled, not agent-initiated. In silicon terms this maps to the tick: a hardware-interlocked deadline that traffic cannot starve. The system improves itself *on schedule* because the schedule is a property of the substrate, not a habit of a supervisor.

### 2.5 Weight: the camera keeps the records nobody keeps

> "A hanging scale with its dial in view of a camera — crew weighs fish normally when speed isn't a factor; nobody keeps records; the camera keeps them."

Cells:

- **CAM-SCALE + LEDGER-SCALE cells** — a ledger-cell pair. The crew's behavior is unchanged: hang the fish, read the dial, move on. The camera reads the same dial. The ledger records (timestamp, weight, species-from-tote) tuples whenever the scale is used. "Nobody keeps records; the camera keeps them" — passive capture of an existing workflow, zero marginal effort per datum. Note the honest scope: this runs *when speed isn't a factor*, i.e., the ledger samples opportunistically and never demands a weighing.

### 2.6 Review surface: the best-shot audit

> "Essential frames pulled from every fish's footage including one best-shot per fish — captain flips through pictures from the wheelhouse when correct identity is critical (e.g. openings where only pinks and chums are legal)."

Cells:

- **BESTSHOT cell** — the review-surface cell. Per fish: the essential frames, one best-shot. Selection criteria (sharpness, angle, lighting) are the cell's internals; the output is a flip-through, a contact sheet, not a dashboard.
- **AUDIT-CAPTAIN cell** — the audit cell. The captain reviews when identity carries legal weight — during openings where only pinks and chums are legal, a mislabeled king in the tally is a regulatory event. The captain's flip-through is not a QA theater; it is the audit gate that quarantines suspicious labels before they enter the night's training set (§6.1).

### 2.7 Hardware economics: scaffolding, not product

> "Global-shutter stereoscopic cameras added TEMPORARILY for training data, removed when the model is good enough without them — training rig becomes a rental business for technician-facing products and training courses."

This is not a cell; it is the economic shape of the whole system, and it deserves equal billing:

- The expensive sensing is **scaffolding**. Stereoscopic depth, global shutter — bought once, used to bootstrap the models, then *removed*. The end state runs on the cheap permanent cameras because the tote rule, not the stereo rig, is the label source.
- The rig itself depreciates into a **rental business**: the same training hardware serves technician-facing products and training courses. The capital asset outlives its deployment.
- The QUF analogy is exact: state is a file. The trained state is portable and sensor-independent; the rig that produced it is not part of the product. The weights are the fleet's; the scaffolding is rentable.

---

## 3. Why this beats conventional ML-pipeline architecture

A conventional deployment of the same capability looks like: annotation spec → contractors labeling fish images → a training pipeline (orchestrated jobs, experiment tracking) → a serving stack → a monitoring stack → a retraining trigger → a human deciding when to promote a new model. Every stage is invented work, and every stage has a failure mode named "nobody did the step."

The back-deck pipeline deletes those stages by distribution:

| Conventional stage | Back-deck replacement | Why it's better |
|---|---|---|
| Annotation contractors | Crew's tote sorting | Zero cost, zero latency, zero drift from the actual task; the label is made at the moment of the action it describes |
| Labeling tools & review queues | Alias-table (passive) + captain best-shot audit (targeted) | Review effort is spent exactly where identity is legally critical, not uniformly |
| Experiment tracking / orchestration | NIGHT-CRON + day's data | The day's catch *is* the experiment log; the schedule is substrate-guaranteed |
| Model promotion decisions | AB-PROMOTE cell, rollback default | Promotion is earned on next-day feedback, not argued in a meeting |
| Serving infrastructure | The same cameras, the same cells | No separate serving tier; inference lives where the data arrives |
| Data drift monitoring | Continuous tote labels | Drift is measured against ground truth that regenerates every day by itself |

The deep reason this works: **the ground truth is distributed at the point of action.** Conventional pipelines centralize labels (collect → ship → train → deploy → monitor) and pay a synchronization tax at every arrow. The back deck pays no synchronization tax anywhere except one timestamp match — and that match (fish leaves frame / fish breaks surface) is the shortest possible arrow, seconds long, between two cameras watching the same event.

And the ceiling argument is honest, not hand-wavy: "the ML gets as good as the human crew because the crew's own sorting IS the label." The system inherits the crew's accuracy as its ceiling — and the crew's sorting is professional-grade because it is the crew's job. You cannot get better labels than a working practitioner doing working-practitioner sorting, without inventing new work.

---

## 4. The constraint vocabulary: cells above the silicon

quilt-verilog hosts five opcodes and sixteen dials per cell. The Back Deck application is a *layer above that fabric* — the same law (everything is a cell, wiring not scheduling), expressed in application nouns. The fabric hosts this layer; it does not replace it. The dictation implies a minimal vocabulary of eight cell kinds. Every one of them is a spreadsheet-flavored object — a rule, a lookup, a windowed join, a counter, a schedule, a gate, a review pile, a ledger. A deckhand who understands totes can audit any of them. No programmer is implied by any of them.

1. **Constraint-cell** — emits ground truth as a *rule* from an observed action (tote volume entered → species). Distinct from a classifier: it cannot be wrong about its rule, only about the event it observed. Its failures are audit-able as single events.
2. **Alias-table** — many names, one referent (pink/humpy; chum/dog/keta; king/chinook; coho/silver). Overheard names are *data*: the table grows rows from conversation, not migrations. The passive twin of the constraint-cell.
3. **Match-cell** — propagates identity across sensors by timestamp correlation inside a window (leave-frame ↔ surface-break). Ambiguity inside the window is *flagged*, never guessed (§6.2).
4. **Count-cell** — turns known structure into labels (30 hooks × 1.5 fathoms → depth). Geometry the practitioner already maintains becomes instrumentation at zero marginal cost.
5. **Ledger-cell** — passively records an existing behavior the practitioners don't record ("nobody keeps records; the camera keeps them"). Never demands the behavior; only samples it.
6. **Cron-cell** — scheduled self-improvement as a substrate-guaranteed tick ("the computer has the boat to itself at night"). Cannot be starved by daytime traffic; no agent has to remember it.
7. **A/B-cell** — challenger vs. incumbent, promoted only on next-day feedback, rollback default ("A/B test the updated version against feedback cells the next day"). Improvement is earned, never assumed.
8. **Audit-cell** — targeted human review where identity carries consequence, whose disagreement quarantines labels out of the training set (captain flipping best-shots during a pinks-and-chums-only opening).

Two structural observations. First, **the crew's continued work is both training set and test set** — separated by a day and an A/B gate, which is the only separation this system needs. Second, the vocabulary contains no cell named "model," "pipeline," "service," or "queue." The intelligence is at the bottom (the fabric's Hebbian substrate and the models it hosts); what this layer contributes is *constraints, records, and gates* — the parts of the application that must never be mysterious.

---

## 5. The data-flow diagram, in text

```
                              DECK CONVERSATION (overheard: "humpy", "dog", "chinook"...)
                                        │
                                        ▼
                                  ┌───────────┐
                                  │   ALIAS   │  pink≡humpy  chum≡dog≡keta
                                  │  (table)  │  king≡chinook  coho≡silver
                                  └─────┬─────┘
                                        │ canonical species IDs
                                        ▼
  CAM-UW ──leave-frame(t)──┐   ┌──────────────────────────────────────────┐
  (underwater)             │   │              DECK CAMERAS                │
                           ▼   │  CAM-DECK-P  CAM-DECK-H  CAM-DECK-SF/SA  │
                     ┌───────────┐          ▲                             │
                     │ XID-MATCH │ surface- │  fish lands in view         │
                     │ (t-window)│──break(t)┘                             │
                     └─────┬─────┘          │                             │
                           │ same-fish ID   ▼                             │
                           │         ┌────────────┐  ┌────────────┐       │
                           │         │ TOTE-PORT  │  │  TOTE-HOLD │       │
                           │         │  → pink    │  │  → chum    │       │
                           │         └────────────┘  └────────────┘       │
                           │         ┌────────────┐  ┌────────────┐       │
                           │         │ TOTE-STBD-F│  │ TOTE-STBD-A│       │
                           │         │  → king    │  │  → coho    │       │
                           │         └────────────┘  └────────────┘       │
                           │                │                             │
   tote-derived label ─────┴────────────────┼─────────────────────────────┘
   propagates BACKWARD to                     │ ground-truth labels (live, all day)
   the underwater sighting                    ▼
                                        ┌───────────┐   hook geometry: 30 hooks ×
   CAM-DECK ──hooks in column──▶────────│ HOOK-COUNT│   1.5 fathoms → cannonball depth
                                        └─────┬─────┘
                                              │ labeled (echogram, depth) pairs —
                                              │ NO underwater camera needed
                                              ▼
   SOUNDER/NMEA ─────────────────────▶ ┌───────────┐
   (echogram)                          │  SOUNDER  │──▶ nightly-improving inference
                                       └─────┬─────┘
                                             │
   CAM-SCALE ──dial frames──▶ LEDGER-SCALE ──┤ (weight tuples join the same
   (crew weighs, nobody records)             │  timestamped stream, species
                                             │  attached via tote label)
                                             ▼
   every fish ──▶ BESTSHOT (essential frames + one best-shot)
                        │
                        ▼
                 AUDIT-CAPTAIN  (wheelhouse flip-through; identity-critical:
                        │         openings where only pinks and chums are legal)
                        │ disagreement → label quarantine
                        ▼
        ┌───────────────────── NIGHT (boat idle) ─────────────────────┐
        │  NIGHT-CRON: retrain SOUNDER on the day's labeled data      │
        │  AB-PROMOTE: challenger vs incumbent, next day's feedback   │
        │  cells are the test set; rollback default; promote = dial   │
        │  write (qm_bind). Repeat. Forever. No babysitting.          │
        └──────────────────────────────────────────────────────────────┘
```

Read it as two loops sharing one bus: a **label loop** (action → constraint-cell → canonical ID → backward propagation to sensors) that runs at fish-landing speed during the day, and an **improvement loop** (day's labels → night retrain → day-after A/B) that runs at boat-shift speed. The stereoscopic training rig hovers above the diagram temporarily and then leaves it.

---

## 6. Honest failure modes

The doctrine of this fleet: failures are first-class content. Each failure mode below is real, and each mitigation is already implied by a cell in the vocabulary — the system ships with its own immune response.

### 6.1 Mis-sorted fish poison the labels

The tote rule's ceiling is also its poison vector: a pink thrown in the center hold is recorded as — and teaches the system — *chum*. One bad throw is a mislabeled example; a bad thrower is a corrupted day. This is the failure mode that kills naive "behavior as label" systems.

**Mitigation: the audit cell.** The captain's best-shot review is the quarantine gate. When identity is critical (an opening where only pinks and chums are legal), the flip-through compares what the camera saw against what the tote claimed; disagreements quarantine that fish's label chain out of the night's training set — *and mark the underwater sighting that inherited it* (backward propagation propagates quarantine too). The audit is not aperiodic QA; it is scheduled exactly where the cost of a wrong label is legal, not cosmetic. Additionally: the constraint-cells emit *events*, so label poison is always traceable to (fish, tote, timestamp) — a single bad example can be excised precisely, not statistically.

### 6.2 Overlap windows in the cross-camera handoff

XID-MATCH works because the gap between "leaves underwater frame" and "breaks surface" is seconds long. But when fishing is hot, two fish can transit inside one match window — and the tote label attaches to the wrong underwater sighting. The window is a dial, and a dial is a bet: tighter windows miss matches (labels lost), wider windows cross-match (labels corrupted).

**Mitigation: flag, never guess.** When more than one candidate sits inside the window, the match-cell emits *ambiguous*, the underwater sighting goes unlabeled, and the best-shot pile shows both candidates. A lost label costs one training example; a crossed label costs trust in every label. Count reconciliation (hooks fished vs fish landed vs totes filled) runs as a cheap invariant cell that bounds how wrong the day's identity bookkeeping can silently be.

### 6.3 Night-retrain drift

Nightly retraining on freshly self-labeled data is a feedback loop, and feedback loops drift: a subtly degraded model mislabels more, the mislabels retrain the next model, and the system erodes while every dashboard stays green — each night's model is "better" than the last on data the previous nights contaminated. Silent compounding is the failure, not the first bad night.

**Mitigation: the A/B cell as circuit breaker.** Promotion is *earned* on next-day feedback cells — the crew's sorting, which is the one data source that does not pass through the model being promoted. Rollback is the default outcome of every night, not an emergency response. If the challenger does not beat the incumbent on tomorrow's tote labels, tonight's model never ships. Drift is bounded by one day, and the incumbent that gets rolled back to is always a model that earned its slot the same way.

### 6.4 Two more, for completeness

- **Alias collision.** Regional vocabulary drifts ("dog" means chum here, something else in another port). The alias-table grows rows, not schemas — but its growth should surface in the audit pile when a new alias suddenly wins a suspicious fraction of labels.
- **The ledger's blind spot.** The scale camera records when the crew weighs; it cannot notice that nobody weighed the big one because it was raining. Passive ledgers inherit the crew's attention patterns, not a sampling plan — honest records of actual behavior, but not a random sample of the catch.

---

## 7. What generalizes: the tote-rule pattern

Strip the fish nouns and the pattern is:

> **Find the gesture by which practitioners already sort, route, or file the things that matter. Point a dumb camera at it. The gesture becomes the label. Resolve names through aliases. Propagate identity by timestamps. Turn maintained structure into counted instrumentation. Let scheduled nights improve the models, gated by tomorrow's gestures. Audit where identity is consequential. Record what nobody records. When bootstrap sensing has done its job, remove it and rent it out.**

The tote-rule pattern — **human action as free labeling** — applies wherever a skilled existing behavior encodes a classification the practitioner would have to be paid to annotate:

- **A machine shop:** parts placed in the scrap bin vs. the finished-goods rack = quality labels, generated by the machinist's existing judgment, harvested by one camera over the bins.
- **A galley:** plates sent back vs. cleared = acceptance labels for the line's output.
- **A farm grading table:** produce into box A vs. box B = grade labels, at harvest speed, every harvest.
- **A triage desk:** patient routed to ward X vs. clinic Y = severity labels from the nurse's routing gesture (with the audit cell doing real work: routing errors here are consequential).
- **Any maintenance bay:** parts pulled to "rebuild" vs. "scrap" shelves = remaining-useful-life labels from the mechanic's existing decision.

In each case the pattern's honesty holds: the system's ceiling is the practitioner's sorting, the practitioner's sorting is professional because it is their job, and the audit cell sits exactly where the label's cost crosses from cosmetic to consequential. The expensive part of ML is not inference; it is ground truth. Skilled trades generate ground truth continuously and throw it away. The quilt's application layer is a net strung under an existing workflow — nothing upstream changes, everything downstream learns.

---

## 8. Closing: the layer the silicon hosts

The Back Deck Papers formalize an application layer that sits *above* quilt-verilog's fabric and speaks its law: cells that are rules, tables, windows, counters, schedules, gates, and ledgers — wired, not programmed; warm-started from a QUF file like everything else the fabric runs; improved by a night cron that is a tick, not a habit; promoted by an A/B gate that the next day's work — not a committee — decides.

The companion document `quilt-verilog/docs/BACK-DECK-APP.md` expresses this exact pipeline as a QUF-warmable cell graph: which cells, which links, which dials the A/B night-cron turns. The fabric does not know what a salmon is. That is the point. The intelligence is at the bottom; the application is cells all the way up; and somewhere in between, a deckhand throws a fish in a tote, and the system learns.

---

*Cross-references: quilt-verilog `README.md`, `docs/DOCTRINE.md`, `docs/SYNTHESIS.md` (the fabric and its law), `docs/QUF-SPEC.md` (state is a file), `docs/BACK-DECK-APP.md` (this pipeline as a cell graph). Fleet context: MEMORY.md iceberg — The Tap (tip), The Boat / F/V EILEEN (waterline), Wesley's arc from bar to wheelhouse. Paper 67 (dyadic staircases) is the silicon-layer theory this application layer stands on.*
