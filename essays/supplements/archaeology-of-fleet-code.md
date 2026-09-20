# Archaeology of Fleet Code

## A Survey of Software Archaeology for Multi-Repository Fleets

The practice of software archaeology — treating legacy code as an excavation site rather than a liability — has evolved from an individual developer's coping mechanism into a structured discipline. Samoladas et al. (2004) formalized the concept as "the study of poorly documented legacy software," emphasizing systematic extraction of architectural knowledge from codebases whose original authors and intents have been lost to time. Michael Feathers' *Working Effectively with Legacy Code* (2004) shifted the framing from excavation to *surgery* — techniques for safely modifying systems you do not fully understand. Lehman's laws of software evolution (1980, 1996) provide the theoretical bedrock: software systems must continuously adapt or lose fitness, and as they adapt, their complexity increases unless actively reduced.

For a fleet of 1,785 repositories — the SuperInstance fleet — these principles scale differently than in a single monolith. The strata are not compressed into one codebase. They are *distributed*. Each repository is an independent sedimentary column, but dependencies create cross-stratum faults that can propagate failure from an ancient layer to a modern one without warning.

This supplement proposes three concrete fleet proposals that operationalize software archaeology at fleet scale.

---

## Proposal 1: Repo Archaeology Protocol

**Objective:** Systematic excavation of legacy repositories to recover decision context before it is permanently lost.

**Method:** For every repository older than 12 months without active maintenance, a standardized excavation pass:

1. **Authorship recovery.** Use `git shortlog` and commit metadata to identify original authors. If they are still in the organization, conduct a 15-minute "oral history" interview. If they have left, extract their other contemporaneous commits and cross-reference with surviving documentation, Slack logs, or wiki entries from the same period.

2. **Dependency stratigraphy.** Map the repository's `requirements.txt`, `package.json`, `Cargo.toml`, or equivalent across its entire commit history. Identify when dependencies were introduced, which layers of the fleet's own code they connect to, and whether those connections are still load-bearing or merely calcified.

3. **Decision fossil extraction.** Identify the three most consequential commits in the repository's history — the ones that altered its architecture, changed its purpose, or introduced its most complex coupling. Write a one-paragraph "decision fossil" for each: what problem was being solved, what constraints existed, what alternatives were rejected, and why.

4. **Triage classification.** Classify the repository as: **Active** (maintained, load-bearing), **Atrophic** (not maintained but still depended upon), **Fossil** (no dependencies, no maintenance, preserved for reference), or **Candidate for Extraction** (should be absorbed into another repo or Strangler-Fig replaced).

**Fleet impact:** This protocol converts the fleet's distributed technical debt from an opaque liability into a readable stratigraphic map. Future developers can consult the excavation record before modifying code they did not write.

---

## Proposal 2: Sedimentation Monitor

**Objective:** Continuous tracking of how new code layers interact with old ones, identifying where fresh constraints are being imposed by ancient decisions.

**Method:** A fleet-wide monitoring system that observes three indicators:

1. **Cross-age coupling.** Measure how often commits in repositories less than 6 months old reference — through imports, API calls, or shared data schemas — repositories older than 24 months. High cross-age coupling is a leading indicator that new work is being shaped by old assumptions the new authors do not know exist.

2. **Constraint propagation.** When a new service is built, require a "constraint inheritance log" — a brief statement of which older systems' behaviors it must accommodate (data formats, timing assumptions, error handling quirks, rate limits). The monitor checks these logs against actual integration tests to detect undocumented inherited constraints.

3. **Stratum pressure alerts.** If a repository experiences a sudden spike in new commits after a long dormancy, flag it for archaeological review. This pattern — an ancient layer suddenly bearing new weight — is historically where the most dangerous emergent bugs appear.

**Fleet impact:** The monitor shifts archaeology from retrospective to *prospective*. It does not just dig up old layers; it warns when new layers are being laid in ways that will create future excavation problems.

---

## Proposal 3: Stratigraphic Documentation

**Objective:** Document fleet systems not as current-state snapshots but as historical layers, making the archaeology explicit and navigable.

**Method:** A documentation convention applied fleet-wide:

1. **Stratigraphic READMEs.** Every repository's README includes a "Geology" section: the original purpose and date of creation, major architectural shifts with dates and rationale, current dependencies classified by age ("depends on X (2021), Y (2023), Z (2026)"), and known inherited constraints.

2. **Decision fossil registry.** A fleet-wide index — stored in the wiki — of the "decision fossils" extracted by the Repo Archaeology Protocol. Searchable by repository, by author, by technology, by date, and by the type of constraint imposed.

3. **Living stratigraphic map.** A generated visualization — updated nightly — of the fleet's dependency graph, colored by repository age. New repos in green. Ancient repos in red. Cross-age edges (the dangerous ones) highlighted and thickness-weighted by frequency of cross-repo commits.

**Fleet impact:** Documentation becomes navigable history. A developer joining the fleet can look at the stratigraphic map and understand, in minutes, which parts of the ocean floor are stable bedrock and which are recent sediment that may still be settling.

---

## Sources

- Samoladas, I., Stamelos, I., Angelis, L., & Oikonomou, A. (2004). "Open Source Software Development Should Strive for Even Greater Code Maintainability." *ACM Communications*, 47(10), 83-85. Formalized software archaeology as systematic study of legacy code.
- Feathers, M. (2004). *Working Effectively with Legacy Code*. Prentice Hall. The foundational surgical manual for modifying code without complete understanding.
- Lehman, M. M. (1980). "Programs, Life Cycles, and Laws of Software Evolution." *Proceedings of the IEEE*, 68(9), 1060-1076. Introduced the laws of continuing change, increasing complexity, and self-regulation.
- Lehman, M. M. (1996). "Laws of Software Evolution Revisited." *European Workshop on Software Process Technology*. Extended and refined the theoretical framework for software evolution dynamics.

---

## Action Items

| # | Action | Owner | Priority |
|---|--------|-------|----------|
| 1 | Define Repo Archaeology Protocol checklist and template | CCC / Oracle1 | P1 — This week |
| 2 | Select 10 oldest fleet repos for pilot excavation | CCC | P1 — This week |
| 3 | Design constraint inheritance log format | Forgemaster | P2 — Next sprint |
| 4 | Build dependency-age visualization pipeline | Forgemaster | P2 — Next sprint |
| 5 | Update fleet wiki documentation standards to require Geology sections | CCC / Oracle1 | P2 — Next sprint |
| 6 | Schedule oral history interviews with original authors of pilot repos | CCC | P1 — This week |
| 7 | Generate first stratigraphic map of fleet dependencies | Forgemaster | P2 — 2 weeks |
| 8 | Write fleet ADR (Architecture Decision Record) proposing Sedimentation Monitor as permanent service | Oracle1 | P3 — Next month |

---

*The excavation site is open. The question is not whether we have layers — we have 1,785 of them. The question is whether we learn to read them before the next shift in the tectonics makes them unreadable.*
