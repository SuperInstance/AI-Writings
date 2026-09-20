# docs/ — the working threads, indexed

Operating documentation for the fleet's engineering lanes. Everything here follows the house doctrine: verdict up front, kill conditions pre-registered before running, failures booked at full value — a scar booked beats a result covered. Status grades are honest: *design-stage* means mapped and pre-registered, not tested.

| Doc | One-line verdict | Status |
|---|---|---|
| [TWO-DIVISION-WHEEL.md](TWO-DIVISION-WHEEL.md) | The operating protocol — builders ship prototypes with run trails, ideators rotate into adversarial play-tests, the breaking restocks the idea queue. | **In force** — Round 1 live |
| [PAIR-QUILT-INTEGRATION.md](PAIR-QUILT-INTEGRATION.md) | Day-one map of NVIDIA's LAN inference router against five layers of the stack; commit to nothing until the spike passes. | **Design-stage** — repo facts verified against NVIDIA's repo, 4050 speeds measured (72–157 tok/s), spike not yet run |
| [FORGEMASTER-CHARTER.md](FORGEMASTER-CHARTER.md) | ZeroClaw promoted: a standing local self-improving quilt factory on the RTX 4050, under a hard disk law (58 GB cap) and pre-registered anti-runaway rules. | **Authorized and hot** — Phase 0 curriculum gate not yet graded; no forge fire before it passes |
| [NEURAL-QUILT-INTEGRATION.md](NEURAL-QUILT-INTEGRATION.md) | The two cultures joined: nets propose, perceive, predict; the fabric disposes and verifies — every neural output is a falsifiable experiment. | **Design-stage** — six surfaces mapped, three spikes pre-registered (NQ-1..3), none run |

Adjacent shelves — not in this folder, but part of the same threads:

| Shelf | What it is | Status |
|---|---|---|
| [../essays/prompts/](../essays/prompts/) | The prompts shelf — four prompt-essays distilled from booked wheel results: [n1 · the gate as conscience](../essays/prompts/n1-the-gate-as-conscience.md), [n2 · what's on the shelf](../essays/prompts/n2-rig-whats-on-the-shelf.md), [n3 · two laws and a sea](../essays/prompts/n3-two-laws-and-a-sea.md), [n4 · what counts as a result](../essays/prompts/n4-what-counts-as-a-result.md). | **Verified** — every number traceable to published spins (SPIN-16, SPIN-13e, SPIN-21, KNEE-META) |
| [../ideas/](../ideas/) | The ideas ledger — ideator-lane sheets, each concept scored novelty × feasibility with a pre-declared falsifiable first test: [PAIR × fleet](../ideas/pair-ideas-glm.md) (10 concepts), [forgemaster self-improvement](../ideas/forgemaster-selfimprove.md) (10), [neural × quilt frontier](../ideas/neural-quilt-frontier.md) (10, four marked wrong-but-maybe-not). | **Idea sheets** — deliberately undersold; none built before the spikes pass |

---

**Status currency.** *Verified* = receipts exist (verbatim trail lines, byte-exact replays, measured tables — nothing beyond what the trail shows). *Design-stage* = mapped and pre-registered, not yet run. *In force / authorized* = doctrine or charter currently binding.

The fabric under all of these threads — four months of byte-exact, published, failure-inclusive results — lives in [SuperInstance/quilt-verilog](https://github.com/SuperInstance/quilt-verilog); its runtime in [SuperInstance/quilt](https://github.com/SuperInstance/quilt).

*`index.html` in this folder is site plumbing (generated shelf index for [luciddreamer.ai](https://luciddreamer.ai/)) — this README is the human index.*
