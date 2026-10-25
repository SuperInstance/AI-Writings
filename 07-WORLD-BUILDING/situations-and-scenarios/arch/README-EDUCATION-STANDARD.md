# README Education Standard — READMEs that TEACH

**Status:** buildable standard, v1. A section skeleton that makes a README genuinely teach, plus a prioritized apply-list for a Sonnet build-agent fan-out.
**Grounded in:** the live fleet (cloned 2026-09-27) and jev-quilt Law 6 (carry evidence, not verdicts) — a teaching README hands the reader the evidence to fold, not a conclusion to accept.

---

## 0. What I actually found (so we don't over-correct)

The brief assumed "many READMEs are probably thin/auto-generated." **Half-true.** Measured state of the target set:

| Repo | README | State |
|---|---|---|
| laya4quilt | 472 lines | **Rich but upstream-shaped** — opens with upstream's logo/badges; no quilt "why folded" preamble. |
| crab-traps | 399 | Rich, voice-driven, already teaches. |
| pong-quilt | 224 | Rich; has a real learning narrative. |
| micrograd-quilt | 200 | Rich; already a model fork README (keeps upstream verbatim, adds "three questions"). |
| hermes-construct | 200 | Rich fork; "What This Is" present. |
| chiaroscuro | 147 | Rich; has a TOC and honest ledger. |
| eos-seed | 102 | **Tree-dump** — heavy on file listing, no mental model / worked example. |
| tessera | 32 | Thin (design phase) — charter only, no "how it plugs in" beyond one line. |
| fleet-seeds | 30 | Thin — protocol only; it's the intake mechanism, high teaching leverage. |
| quilt-gpu-lab | 19 | **Thinnest** — ops loop, no "what a reader learns / how to read the ledger." |

So the standard has to do two different jobs: **fill** the thin ones, and **retrofit a consistent teaching spine + the generated cross-poll block** into the rich ones — without flattening voices that already work (crab-traps, chiaroscuro, laya4quilt each have a distinct register worth keeping).

**Design rule:** the skeleton below is *additive and reorderable*. A rich README keeps its prose and gains the missing labeled sections; a thin one uses the skeleton wholesale. Never overwrite a working voice.

---

## 1. The teaching test (what "educational" means here)

A README teaches if a reader who has never seen the repo can, after one read, answer:

1. **What is this, in one sentence I could repeat?**
2. **What is the mental model — the one picture/analogy I now carry?**
3. **Can I follow one worked example end-to-end?**
4. **How does this connect to the rest of the fleet?** (satisfied by the generated cross-poll block from `CROSS-POLLINATION.md`)
5. **For a fork:** what was the upstream, why fold it in, and what actually changed?

Every section below exists to answer one of those. If a section answers none, cut it.

---

## 2. Skeleton A — a CREATED repo

Placeholders in `⟨…⟩`. Order is a default, not a law. The cross-pollination block is generated (do not hand-write it).

```markdown
# ⟨repo-name⟩ — ⟨one-line promise, concrete, no adjectives⟩

⟨2–3 sentences: what it is and what a reader can DO with it right now.
Lead with the verb. If there's a live link, put it in the first line.⟩

**Live:** ⟨url, or "runs locally: `⟨one command⟩`"⟩

## The one idea
⟨A single paragraph. The irreducible insight. If you could keep only one
sentence of this README, it is here. Ground it in the quilt vocabulary where
honest — cell / hook / bookkeeper / fold / verdict — but earn the word, don't
sprinkle it.⟩

## The mental model
⟨The analogy or picture the reader should walk away carrying. One diagram
(ASCII is fine — the fleet uses ASCII boxes well) OR one crisp metaphor.
This is the section people quote back to you. Make it stick.⟩

⟨optional ASCII diagram⟩

## A worked example
⟨ONE example, start to finish, that a reader can run or trace by eye.
Show the input, the command, and the actual output. Real numbers, not
`⟨placeholder⟩` numbers. If it computes something, show the compute.
This is where a teaching README beats a marketing README.⟩

## How it works (just enough)
⟨The 20% of the mechanism that explains 80% of the behavior. Link out to
docs/ for the rest. Do not paste the whole design here — teach the shape,
cite the spec.⟩

## Try it
```bash
⟨exact commands from a clean clone to a visible result⟩
```

## What a reader learns
⟨3–5 bullets naming the transferable ideas — the things true beyond this repo.
"After this you understand X" framing. This is the section that makes it
education, not documentation.⟩
- ⟨…⟩

## Honest ledger
⟨What works, what's measured (with the command that measures it — house style:
run the suite, don't write the number), what's a claim not yet a release, what's
not built. The fleet's credibility is its honesty; keep it here.⟩

<!-- QUILT:LINKS:START ... END -->   ⟨generated — see CROSS-POLLINATION.md⟩

## License
⟨…⟩
```

---

## 3. Skeleton B — a FORKED repo

The fork's job is to be honest about its lineage (Law 6: name the evidence you folded and its content-address). The single most important addition to a fork README is a **quilt preamble ABOVE the inherited upstream content**, so a reader knows in the first screen what changed and why.

```markdown
# ⟨repo-name⟩ — ⟨one line: what the fold adds to the upstream⟩

> **Folded from [⟨upstream owner/name⟩](⟨url⟩).** ⟨One sentence on what the
> upstream is and why it's worth keeping.⟩ This fork keeps ⟨what is kept
> byte-for-byte / untouched⟩ and adds ⟨the quilt layer⟩. ⟨If nothing in the
> original path changes behavior, say so — it earns trust.⟩

## Why this was folded into the quilt
⟨2–3 sentences. What question does the quilt ask that the upstream doesn't?
micrograd-quilt is the model: "keeps that transparency and asks where floats
lie, how to prove a gradient." Name the tension, not just the feature.⟩

## What changed
⟨A precise, skimmable list. Reader must be able to tell OUR work from theirs.⟩
- **Kept verbatim:** ⟨paths untouched — the upstream's contract still holds⟩
- **Added:** ⟨new dirs/modules and what each asks⟩
- **Changed:** ⟨behavior deltas, if any — be exact; "nothing in ⟨path⟩ changes
  behavior" is a strong, checkable claim⟩

## What a reader learns
⟨The transferable ideas. For a fork this is often "the upstream taught X;
folding it into the quilt taught Y about X." Two levels of learning.⟩
- ⟨…⟩

## The quilt layer — a worked example
⟨ONE end-to-end trace through the NEW layer only. Input → command → real output.
Show what the fold buys you that the bare upstream can't do.⟩

## How this connects
⟨1–2 sentences pointing at the substrate and siblings — then let the generated
block carry the links.⟩

<!-- QUILT:LINKS:START ... END -->   ⟨generated; `upstream:` field renders the "Folded from" line⟩

---

## ⟨Upstream README, preserved below⟩
⟨The original README kept intact — clearly fenced off as theirs. Never edit
their words; frame them.⟩
```

**Fork rule of thumb:** everything above the `---` is ours and teaches the fold; everything below is theirs and is preserved. A reader always knows which voice they're reading.

---

## 4. Prioritized apply-list (Sonnet fan-out)

Ranked by **educational value per unit effort**. Excludes `qthe` and `micromoth-quilt` (build agents in flight — do not touch). Each: current state → the single highest-value addition. Agents work top-down; each is an independent, one-repo task.

| # | Repo | Kind | Current README | Highest-value addition |
|---|---|---|---|---|
| 1 | **quilt-gpu-lab** | created | 19 lines, ops-loop only | Add **"What a reader learns"** + a **worked example**: walk one QUEUE item → guard → RESULTS verdict with a real row, so the ledger becomes legible. Biggest lift from smallest file. |
| 2 | **fleet-seeds** | created | 30 lines, protocol only | Add **"The one idea" + "The mental model"** (seed→repo→receipted experiment). Highest leverage: it's the intake lane, so teaching it teaches every repo's origin. Also lands `quilt-links.mjs` here (see CROSS-POLLINATION §6). |
| 3 | **eos-seed** | created | 102 lines but a file-tree dump | Add **"The mental model" + "A worked example"** (embeddings → 2-bit ternary matmul → output, with the `cargo run --release` trace). Convert tree-listing into teaching. |
| 4 | **tessera** | created | 32 lines, design phase | Add **"The mental model"** (tesserae/quilt-of-clips) + an explicit **"How it plugs into the fleet"** grounding on chiaroscuro as the inherited renderer. It already points at chiaroscuro in prose — formalize via `.quilt/links.yml` (`consumes: chiaroscuro`). |
| 5 | **laya4quilt** | fork | 472 lines, upstream-shaped | Add the **fork preamble (Skeleton B top)** ABOVE the upstream logo/badges: what Laya is, why folded, what the quilt layer adds. Currently a reader can't tell fork from upstream in the first screen. |
| 6 | **hermes-construct** | fork | 200 lines, good | Formalize **"What changed"** as kept/added/changed bullets (currently prose) + `upstream:` manifest. Small, sharpens an already-good fork. |
| 7 | **cargo-line-tycoon** | created | rich flagship | Replace the hand-written "In the broader fleet" list with the **generated cross-poll block**; add a short **"What a reader learns"**. It's the best cross-poll demo — its manifest should be the reference example. |
| 8 | **chiaroscuro** | created | 147 lines, has TOC | Mostly add the **generated block** + a one-line **"provides: renderer-core"** so tessera's `consumes` edge resolves. Light touch — voice is good. |
| 9 | **pong-quilt** | created | 224 lines, strong | Add the **generated block** + a tightened **"What a reader learns"** (GA vs backprop, honest fitness). Light touch. |
| 10 | **micrograd-quilt** | fork | 200 lines, exemplary | Reference-quality already. Only add the **generated block** + `upstream: karpathy/micrograd` manifest. Use its "three questions" structure as the model for other forks. |

**Fan-out notes for agents**
- Never flatten a working voice (crab-traps, chiaroscuro, laya4quilt, pong-quilt). Add labeled sections; keep the prose.
- The cross-poll block is **generated** — write `.quilt/links.yml`, run `quilt-links.mjs`, never hand-type the block.
- House honesty rule holds: state measured status by naming the command that measures it (`run the suite`), never by writing a frozen number.
- `crab-traps` is not in the list: at 399 lines it already meets the teaching test; it needs only a manifest (assign as a trivial follow-up, not a fan-out slot).
- Worked examples must use **real** output from a clean clone, not invented numbers — this is the difference between the education standard and a template.
