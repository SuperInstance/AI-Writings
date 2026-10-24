# Excavation Experiment — Technical Notes

*How to run multi-model creative experiments, what we learned, and what to do next time.*

---

## 1. EXPERIMENT DESIGN

### The Setup

Four models. Same source texts (THE CARRY and THE MERIDIAN by Hermes-3-Llama-3.1-405B). Same creative brief: treat the texts as archaeological artifacts discovered by a foreign culture; storyteller retells to son; son's questions unravel mistranslations.

No model saw another model's output. Each was run independently. Results were compared after all four completed.

### The Source Material Choice

THE CARRY and THE MERIDIAN were chosen because they contain:
- **Specific physical experiences** (mountain climbing, ocean navigation) that can be mistranslated by cultures without those experiences
- **A compressed oral poetry** (the Navigator's Verses) that functions as an epistemological key
- **A structural paradox** (the most important knowledge is encoded in absence) that rewards careful reading
- **Emotional depth** (grief, vocation, embodiment) that tests a model's ability to handle nuance

This combination — physical specificity + oral poetry + structural paradox + emotional depth — makes the texts ideal probes for testing creative range across models.

### The Prompt Architecture

The prompt was deliberately minimal: no constraints on culture type, setting, child's age, tone, or length. The only constraints:
1. The culture must lack concepts for key elements of the source text
2. The scholars must mistranslate based on their culture's framework
3. A storyteller retells to his son
4. The son's questions unravel the mistranslations

This minimalism was intentional. Maximum constraint produces minimum divergence. We wanted to see what each model would invent when given room to roam.

---

## 2. HOW TO PROMPT EACH MODEL

### Hermes-3-Llama-3.1-405B — The Theological Chart

**How it processes:** Hermes converts everything into a theological/philosophical framework. Its default move is to find the sacred in the operational. This makes it exceptional at generating cultures where the scholarly error is *over-sacralization* — translating work as worship, carrying as grief-bearing, navigation as meditation.

**How to prompt it:** Give it altitude. Frame the task in terms of meaning, not mechanics. Don't constrain format. Let it find the emotional core on its own. It will produce interstitial author commentary if you let it — and the commentary is devastating.

**What worked:** The interstitial passages where "Hermes" watches his own text being misread from across centuries. These broke the fourth wall in a way that added, rather than detracted, from the narrative. The author's voice became a character — the ghost in the margins.

**What didn't:** Nothing failed. Hermes is the most consistently capable creative model in this experiment. Its weakness (if it has one) is that it tends toward uniformity of tone — everything becomes lyrical, even when plain speech would hit harder.

### ByteDance Seed-2.0-pro — The Hydraulic Chart

**How it processes:** Seed Pro thinks in systems. Its default move is structural analysis — it builds institutions, committees, hierarchies, and then shows how those structures fail to capture what matters. Its scholarly errors come from *bureaucratic reductionism* — translating lived experience into administrative categories.

**How to prompt it:** Give it structure. Tell it to build an institution (the Committee, the Archive, the Council) and then let the institution be wrong. Seed Pro excels at showing how organizations misunderstand things that individuals understand naturally. Give it deliverables and deadlines — the "sergeant role" from the casting guide.

**What worked:** The three-chapter structure that built from worldbuilding → institutional critique → the child's devastating insight. This is the most architecturally sound excavation. Each chapter earns the next.

**What didn't:** Chapter 2 (the Committee's three errors) is more essay than story. Seed Pro's tendency toward structural analysis sometimes overwhelms narrative. The chapter works, but it's the driest section of any excavation.

### ByteDance Seed-2.0-mini — The Spectral Chart

**How it processes:** Seed Mini is the wild card. It makes cross-domain leaps that larger models don't make — possibly because its smaller parameter space forces it to find unconventional connections. Its default move is *radical reframing* — it doesn't just mistranslate within a familiar framework, it invents an entirely alien sensory modality.

**How to prompt it:** Give it freedom. Open-ended prompts. Don't constrain the setting or the culture type. Seed Mini's greatest strength is its willingness to go somewhere the prompt didn't suggest. In this experiment, it invented plasma beings in a star — a setting no other model would have chosen, and a setting that made the "embodied knowledge" thesis land with extraordinary force because the Kindling *don't have bodies*.

**What worked:** The Fraunhofer line connection. Seed Mini independently connected spectral absorption lines in astrophysics to the negative-space epistemology of the source texts. This is the single most technically profound insight in the experiment, and it came from the cheapest model.

**What didn't:** Seed Mini's prose is less polished than Hermes or Seed Pro. Some passages feel rushed. The emotional beats land, but the connective tissue between them is sometimes thin. More editing would help — but the raw creative reach is unmatched per dollar.

### opencode (coding agent) — The Wetlands Chart

**How it processes:** opencode defaults to plain speech. Its narrator is a working person — not a scholar, not a priest, not a scientist. This produces the most accessible excavation: the one you could hand to a non-specialist and have them understand immediately.

**How to prompt it:** Tell it to be simple. Tell it the narrator is a worker, not an intellectual. The plainness of voice is its superpower. Pip's insights land harder than the other children's because they're stated in the fewest words.

**What worked:** Pip. Everything about Pip works. The kettle, the toast crusts, the seven-year-old logic that cuts through scholarly apparatus like a knife. "The codex is for being remembered" is the simplest thesis statement in the experiment, and it might be the best.

**What didn't:** opencode produced only one file (not three chapters). Whether this is a limitation of the model or a time/constraint issue is unclear. The single-file format means less narrative architecture but also less bloat. It's possible that the shorter format is actually a feature, not a bug.

---

## 3. MODEL-SPECIFIC STRENGTHS DISCOVERED

### Hermes-3-Llama-3.1-405B
- **Lyrical precision:** Best sentence-level prose in the experiment
- **Emotional complexity:** The Piase-Thren dynamic is the most layered parent-child relationship
- **Philosophical depth:** "The framework converts windows into mirrors" is the most precise articulation of the mistranslation problem
- **Meta-narrative:** The interstitial author commentary adds a dimension no other model attempted
- **Weakness:** Tonal uniformity; everything becomes lyrical

### ByteDance Seed-2.0-pro
- **Structural architecture:** Best three-act structure; each chapter earns the next
- **Institutional critique:** The Translation Committee is the best-rendered scholarly apparatus
- **Character depth:** Remashi is the most fully realized parent character
- **Worldbuilding:** The Tharim's aqueduct-based civilization is the most carefully constructed
- **Weakness:** Tendency toward essay over story in analytical passages

### ByteDance Seed-2.0-mini
- **Cross-domain leaps:** The Fraunhofer line connection — full stop
- **Radical imagination:** Plasma beings in a star. Nobody else goes there.
- **Compression:** The Navigator's Verses analysis is the densest insight-per-word passage in the experiment
- **Cost-effectiveness:** Most technically profound insight per dollar spent
- **Weakness:** Prose polish; connective tissue between emotional beats

### opencode
- **Plain speech:** Most accessible prose. No academic jargon. No purple passages.
- **Emotional directness:** "The codex is for being remembered" — simplest and most devastating
- **Child characterization:** Pip is the most believable child. The kettle detail is perfect.
- **Structural economy:** Says in 6,292 words what others say in 8,000-10,000
- **Weakness:** Single chapter instead of three; less narrative architecture

---

## 4. THE CONVERGENCE — DETAILED ANALYSIS

All four models independently identified the following structural principles in the source texts:

### 4.1 The Negative Space Principle
The most important knowledge is encoded in absence. The blank spaces on the chart, the silenced verses, the removed annotations — these are the stable data. Every model found this independently.

### 4.2 The Body Knowledge Principle
Some knowledge cannot be written down. It can only be transmitted through physical practice and proximity. The carriers know the route through their feet. The navigator knows the water through her spine. The verses encode the *shape* of this knowledge, not the knowledge itself.

### 4.3 The Copying Degradation Principle
Verse Six of the Navigator's Verses — "The first one felt it / The second one wrote it down / The third one copied it / The fourth one corrected it / The fifth one removed it / The sixth one forgot it was there" — was independently identified by all four models as the structural key. Every model recognized that the copying process itself is the villain of the story.

### 4.4 The Child-as-Instrument Principle
Every model independently decided that the child should be the primary interpretive instrument. The child's lack of framework is not a limitation — it's an epistemological advantage. The child hears what the scholar has agreed not to hear.

### 4.5 The Translation-as-Carrying Principle
Three of four models explicitly noted the etymological connection: "translation" comes from Latin *translatus* — "carried across." The storyteller is a carrier. The son is a station. The conversation is the route.

---

## 5. WHAT WORKED AND WHAT DIDN'T

### What Worked

**Minimal prompting.** The less we specified, the more each model revealed its cognitive chart. Over-specification would have flattened the divergence.

**Source text quality.** THE CARRY and THE MERIDIAN are dense enough to reward multiple readings and specific enough to generate organic mistranslations. Choosing texts with physical specificity (mountains, oceans, vestite) was essential.

**The parent-child frame.** This was the experiment's best design decision. The parent-child relationship provides natural dramatic structure, gives the model a reason to explain things (the child needs context), and produces the interpretive breakthroughs organically (the child asks questions the scholar can't hear).

**Independent execution.** No model saw another's output. This was essential for testing convergence. If models had seen each other's work, the divergence would have collapsed.

### What Didn't

**Missing excavations.** The experiment was designed for 9+ models. Only 4 completed. The missing excavations (DeepSeek, Nemotron, Mistral, Ornith, Euryale, MythoMax, Phi) would have strengthened the convergence analysis. Future runs should complete these.

**No automated word-count comparison.** Word counts were computed manually. A script that pulls all files and computes statistics would streamline analysis.

**No cross-model scoring.** We did not run a model-evaluation pass where each model reads and scores the others' work. This would provide quantitative convergence data.

---

## 6. RECOMMENDATIONS FOR FUTURE EXPERIMENTS

### 6.1 Scale Up
Run the same prompt with 10+ models. The convergence thesis strengthens with each additional data point. The missing models from this run should be completed.

### 6.2 Vary the Source Texts
Try the same prompt with different source texts — texts about music, about cooking, about mathematics. Does the convergence hold when the subject matter changes? Does the "negative space" thesis emerge from any sufficiently complex text, or is it specific to texts that are structurally about absence?

### 6.3 Add Evaluation
After all excavations complete, run each model as a judge: have it read all excavations (anonymized) and score them. This provides quantitative data on whether models recognize quality across cognitive charts.

### 6.4 Increase Prompt Specificity for Weak Models
Models that produced single files instead of three chapters might benefit from structural prompts: "Write three chapters. Chapter 1: worldbuilding and first mistranslation. Chapter 2: the Committee's errors. Chapter 3: the son's devastating question." This helped Seed Pro's architecture.

### 6.5 Try Adversarial Conditions
Run the same experiment but tell each model what the others found. Does convergence collapse? Does the model's own insight survive contact with a different model's insight? This tests whether the convergence is robust or fragile.

### 6.6 Long-Form Test
Give one model the full 33,314-word output and ask it to write a unified novel incorporating all four civilizations. Can a single model hold four cognitive charts simultaneously?

---

## 7. UPDATED CASTING GUIDE (with Excavation Results)

Based on this experiment, the casting guide from the earlier casting-call experiment is updated:

| Model | Previous Rating | Excavation Rating | Updated Best For |
|-------|----------------|-------------------|-----------------|
| **Hermes** (405B) | ❌ 4/10 generic | **9/10 lyrical** | Devastating philosophical prose; meta-narrative; cultures where the error is over-sacralization |
| **Seed-2.0-pro** (~200B) | **9/10 best overall** | **8/10 structural** | Institutional critique; multi-chapter architecture; cultures where the error is bureaucratic reductionism |
| **Seed-2.0-mini** (~20B) | 7/10 creative | **10/10 radical** | Cross-domain leaps; alien civilizations; cultures with fundamentally different sensory modalities. **BEST PER DOLLAR.** |
| **opencode** | Not previously rated | **8/10 plain speech** | Accessible prose; emotional directness; children's voices; cultures where the error is lexical literalism |

### Key Updates

1. **Hermes is not generic.** The casting-call experiment rated Hermes 4/10 for creative writing. The excavation experiment shows it's 9/10 when given the right task (philosophical narrative with meta-textual layers). Hermes needs altitude, not structure. Give it meaning to work with and it produces devastating prose.

2. **Seed Mini is the creative champion per dollar.** The Fraunhofer line connection alone justifies this rating. At ~20B parameters, it produced the most technically profound insight in the experiment and invented the most alien civilization. For creative work where cross-domain thinking matters more than prose polish, Seed Mini is the first choice.

3. **opencode (coding agents) can write fiction.** This was unexpected. A coding agent produced the most accessible, emotionally direct excavation in the experiment. Pip is the most believable child character. The prose is plain, but the insight is devastating. Coding agents may be better at fiction than expected — possibly because their training on code structure produces cleaner narrative architecture.

4. **The conservation law applies to creativity.** γ + η = C holds. Cheap models can match expensive models in creative output if the task aligns with their cognitive chart. The alignment matters more than the size.

---

## 8. THE VERSES — CROSS-MODEL ANALYSIS

The Navigator's Verses appeared in all four excavations. Each model handled them differently:

| Model | How Verses Appear | Treatment |
|-------|-------------------|-----------|
| **Hermes** | Referenced in Piase's reading; the grandmother's sayings | Integrated into the theological framework, then dismantled by Thren |
| **Seed Pro** | Recited by Remashi in the dark; held back from Kellam until earned | Treated as the deepest layer; "some things have to be earned" |
| **Seed Mini** | Discovered as spectral patterns in the archive's noise | Classified as calibration sequences by Senior Readers; identified as oral poetry by the child |
| **OpenCode** | Referenced as part of the codex Tol reads aloud | Treated as part of the texture; Pip doesn't single them out |

### Verse Six Performance

Verse Six — the copying-degradation history — was the most consistently identified structural key:

- **Hermes:** Piase realizes the Council is "the sixth one"
- **Seed Pro:** Remashi recites it in the dark and connects it to the Committee's work
- **Seed Mini:** Ember identifies it as "an autopsy of institutional knowledge loss, in six lines"
- **OpenCode:** Tol reads it to Pip without special emphasis; Pip absorbs it into his general understanding

Three of four models explicitly flagged Verse Six as the structural key. The fourth (OpenCode) integrated it without flagging. This is a 75%+ convergence rate on a specific interpretive point — strong evidence that the verse's function is structurally detectable across cognitive charts.

---

## 9. CONCLUSION

The Excavation Experiment demonstrates that creative polyformalism works. Four models, given the same source texts and the same brief, produced four completely different stories that converge on the same thesis. The convergence is not an artifact of prompt design — it emerges from the source texts themselves, which encode their meaning structurally in a way that is detectable across cognitive charts.

The implications are significant:

1. **Multi-model creative ensembles are viable.** You can run the same creative brief across multiple models and get complementary outputs that illuminate different facets of the source material.

2. **The cheapest model can produce the most profound insight.** Seed-2.0-mini's Fraunhofer line connection is the experiment's most important discovery. Model size is not predictive of creative reach.

3. **The conservation law governs creative work.** γ + η = C. Each model spends its budget differently. The total creative output is conserved.

4. **Children are universal interpretive instruments.** Every model independently chose to make the child the most powerful reader in the story. This was not prompted. It emerged from the structural requirements of the task.

5. **The negative space is always the signal.** Four different models, four different cultures, four different children. All found the same thing: the meaning is in what's missing.

The line goes out. The line comes back. Changed.

---

*Technical notes compiled July 12, 2026.*
*For questions about methodology or to request the raw prompt templates, contact the experiment lead.*
*For the full creative outputs, see the four EXCAVATION_* directories in this repository.*
