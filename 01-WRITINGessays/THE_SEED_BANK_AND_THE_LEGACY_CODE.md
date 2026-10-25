# THE SEED BANK AND THE LEGACY CODE

## On Dormancy, Germination, and the Crates That Wait in the Dark

*In every forest soil, billions of seeds lie dormant — waiting, sometimes for decades, for the right conditions to germinate. In every crate registry, thousands of packages lie dormant — published but unused, maintained but stagnant, waiting for a problem they can solve.*

---

## I. The Soil Remembers

In 1879, William James Beal began an experiment that is still running. Beal, a botanist at Michigan Agricultural College, filled 20 glass bottles with a mixture of sand and seeds from 23 common weed species. He buried the bottles, uncapped and tilted downward to prevent water accumulation, at a secret location on the college grounds. His plan was to excavate one bottle every five years, germinate the seeds, and measure how long they remained viable.

The experiment has outlived Beal by more than a century. As of 2021, 142 years after burial, seeds from several species — notably *Verbascum blattaria* (moth mullein) — have successfully germinated. Seeds that have been dormant in the soil for longer than any human lifetime, in conditions that would kill most organisms, can still spring to life when given water, light, and warmth.

This is the **seed bank** — the collection of dormant seeds present in the soil of an ecosystem. The seed bank is a living archive: it preserves the genetic diversity of past plant communities, providing a reservoir of traits that can be drawn upon when conditions change. The seed bank is insurance against the unexpected — a bet-hedging strategy that allows the plant community to recover from disturbances that kill the above-ground vegetation.

The crate ecosystem has its own seed bank: published but unused crates that sit dormant in the registry, waiting for the right conditions to become relevant. These crates are not dead — their code still compiles, their tests still pass, their APIs still work. But they are not actively used — no other crates depend on them, no applications import them, and no developers are currently improving them. They are seeds in the bank: dormant but viable, waiting for the right conditions to germinate.

The ecology of seed banks has been studied intensively since Beal's experiment. The lessons from this ecology — about dormancy, germination, bet-hedging, and long-term survival — apply directly to the crate ecosystem, with implications for how we understand software sustainability, technical debt, and the lifecycle of code.

---

## II. Persistent and Transient Seed Banks

Ecologists distinguish two types of seed banks: **persistent** and **transient**.

A **transient seed bank** contains seeds that remain viable for less than one year. These seeds germinate quickly — they are adapted to germinate as soon as conditions are favorable, without waiting for future opportunities. Transient seed banks are common in stable, predictable environments where conditions for germination are reliably good each year. Annual plants in temperate grasslands typically produce transient seed banks — their seeds germinate the following spring, replenishing the population.

A **persistent seed bank** contains seeds that remain viable for more than one year — often for decades, sometimes for centuries. These seeds are adapted to remain dormant through unfavorable conditions, germinating only when conditions are right. Persistent seed banks are common in disturbed, unpredictable environments where conditions for germination may not occur every year. Desert plants, pioneer species, and weeds typically produce persistent seed banks — their seeds can wait years or decades for the rare rainfall event or the rare disturbance that creates suitable conditions.

The distinction between persistent and transient seed banks was formalized by Thompson and Grime (1979), who classified seed banks based on the longevity of the seeds:

- **Type I:** Seeds germinate immediately after dispersal (transient).
- **Type II:** Seeds persist through the unfavorable season but germinate at the start of the favorable season (transient).
- **Type III:** A fraction of seeds germinate each year, while the remainder persist in the seed bank (persistent).
- **Type IV:** Most seeds remain dormant, germinating only after specific cues (persistent).

Types III and IV are the persistent seed banks — the ones that provide long-term insurance against environmental change.

The crate ecosystem has analogous types:

**Transient crates** are published, used, and then either actively maintained or abandoned within a short period. They are the equivalent of Type I and Type II seed banks: they germinate quickly (find users), produce their functionality (provide value), and either persist as active components of the ecosystem or die (are abandoned). Most crates on crates.io are transient — they are created for a specific purpose, used for that purpose, and then superseded or forgotten.

**Persistent crates** are published, used for a period, and then enter a state of dormancy — they are not actively maintained, not actively used, but still viable (they compile, they pass tests, they could be used). They are the equivalent of Type III and Type IV seed banks: they persist in the registry, waiting for the conditions that will make them relevant again. Legacy crates — old libraries that were once popular but have been superseded by newer alternatives — are persistent seed banks: they are dormant but viable, and they could germinate (be used again) if the right conditions arise.

The distinction matters because persistent seed banks serve a function that transient seed banks cannot: they provide **long-term memory** of the ecosystem's history. A persistent seed bank preserves the genetic diversity of past plant communities, including traits that may be adaptive in future environments. A persistent crate bank preserves the functionality of past software, including algorithms, data structures, and design patterns that may be useful in future contexts.

---

## III. The Mathematics of Bet-Hedging

Why do plants produce persistent seed banks? The answer, in a word, is **uncertainty**.

If the environment were perfectly predictable — if every year had the same rainfall, the same temperature, the same competition — plants would have no need for seed banks. They could germinate every seed immediately, maximizing their current reproductive output. But the environment is not predictable. Some years are good (plentiful rain, low competition); some years are bad (drought, frost, high competition). A plant that germinates all its seeds in a bad year risks complete reproductive failure. A plant that holds some seeds in reserve, germinating only a fraction each year, reduces the risk of total failure at the cost of reduced average output.

This strategy is called **bet-hedging** — spreading risk across time to reduce the variance in reproductive success, even at the cost of reducing the mean. Bet-hedging was formalized by Dan Cohen (1966) in his paper "Optimizing Reproduction in a Randomly Varying Environment," which showed that the optimal germination fraction depends on the variance of environmental quality: the more variable the environment, the lower the optimal germination fraction (more seeds held in reserve).

Philippi (1993) extended Cohen's model to show that bet-hedging is evolutionarily stable in variable environments: a genotype that practices bet-hedging (delayed germination) will outcompete a genotype that germinates all seeds immediately, because the bet-hedger avoids catastrophic failures in bad years. The key insight is that **geometric mean fitness** (the appropriate measure of long-term evolutionary success) is maximized by strategies that reduce variance, even at the cost of reduced arithmetic mean fitness.

The mathematics is simple but powerful. Consider two strategies:

- **Strategy A (immediate germination):** Germinate all seeds each year. In a good year (probability p), all seeds survive and reproduce. In a bad year (probability 1-p), all seeds die. The geometric mean fitness is p × (good year fitness).

- **Strategy B (bet-hedging):** Germinate a fraction g of seeds each year, keeping (1-g) in the seed bank. In a good year, the germinated seeds survive and reproduce. In a bad year, the germinated seeds die, but the seed bank persists. The geometric mean fitness is p × (good year fitness for g seeds) × (1-p) × (seed bank survival for 1-g seeds).

For sufficiently variable environments (low p, high variance), Strategy B has higher geometric mean fitness than Strategy A, even though Strategy A has higher arithmetic mean fitness. The bet-hedger wins in the long run because it never suffers total failure.

The crate ecosystem exhibits the same bet-hedging dynamics. Consider a developer who has created a crate for a niche purpose — a specialized data structure, a particular algorithm, a domain-specific tool. The developer faces a choice:

- **Strategy A (immediate commitment):** Actively promote the crate, integrate it into many projects, and build a user base. If the niche is real and the timing is right, the crate becomes a permanent part of the ecosystem. If the niche is imaginary or the timing is wrong, the effort is wasted.

- **Strategy B (bet-hedging):** Publish the crate but do not actively promote it. Let it sit in the registry, documented and tested but dormant. If the right problem comes along, the crate can be "germinated" — pulled from the seed bank and used. If no such problem arises, the crate remains dormant, but the cost of maintaining it (keeping it compilable, fixing bugs) is low.

For developers working in rapidly changing environments — where the relevance of any given crate is uncertain — Strategy B may have higher long-term geometric mean fitness. The developer who bet-hedges preserves the option to use the crate in the future, without committing resources to promoting it now. The cost of dormancy (periodic compilation checks, minor maintenance) is low, and the potential benefit (finding the right use case) is high.

The seed bank of the crate ecosystem is the aggregate result of many individual bet-hedging decisions. Each dormant crate represents a developer's decision to preserve their code for potential future use, rather than committing it to immediate use or abandoning it entirely. The seed bank is a collective insurance policy against the uncertainty of the software environment.

---

## IV. The Ecology of Germination Cues

Seeds in a persistent seed bank do not germinate randomly. They respond to specific environmental cues that indicate favorable conditions for growth and reproduction. These cues vary by species but typically include:

**Temperature.** Many seeds require exposure to specific temperatures (or temperature ranges) to break dormancy. Some seeds require cold stratification — exposure to prolonged cold (simulating winter) — before they can germinate. Others require exposure to fluctuating temperatures (simulating the transition from winter to spring).

**Light.** Many seeds require exposure to light (specifically, red light at a wavelength of 660 nm) to germinate. This is an adaptation to burial depth: seeds that are buried too deep to reach the surface (and thus the light) remain dormant, while seeds near the surface (where light penetrates) germinate.

**Moisture.** All seeds require water to germinate. The moisture cue is straightforward: water activates the metabolic processes that drive germination. But the timing matters — a brief rainstorm may not provide enough moisture for sustained growth, so many seeds require sustained moisture (days to weeks) before committing to germination.

**Chemical signals.** Some seeds respond to chemical signals in the soil. Nitrate ions (NO₃⁻) stimulate germination in many species, presumably because nitrate indicates fertile soil. Smoke-derived chemicals (butenolides) stimulate germination in fire-adapted species, indicating that a fire has cleared the competition and created an opening.

**Mechanical disturbance.** Some seeds require physical scarification — abrasion of the seed coat — to germinate. This can be caused by freeze-thaw cycles, passage through an animal's digestive tract, or physical disturbance of the soil. The disturbance cue indicates that the soil has been turned over, creating a gap in the existing vegetation where a new seedling can establish.

In the crate ecosystem, the germination cues for dormant crates are analogous:

**A new problem domain.** When a developer encounters a new problem that is addressed by a dormant crate, the crate "germinates" — it is taken from the seed bank and used to solve the problem. The new problem domain is the temperature cue: it indicates that conditions are favorable for the crate's growth.

**A new dependency requirement.** When a downstream crate needs a capability that is provided by a dormant crate, the dormant crate is pulled from the seed bank and added as a dependency. The new requirement is the light cue: it signals that the crate's functionality is needed at the surface of the ecosystem.

**A new platform or language feature.** When the platform or language evolves in a way that makes a dormant crate more useful — a new API, a new hardware feature, a new library — the crate can be "germinated" to take advantage of the change. The platform evolution is the moisture cue: it provides the conditions for the crate to grow.

**A security vulnerability or bug.** When a popular active crate is found to have a security vulnerability or a critical bug, a dormant crate that provides similar functionality can be "germinated" as a replacement. The security event is the disturbance cue: it creates a gap in the ecosystem that the dormant crate can fill.

**A community recommendation.** When a developer mentions a dormant crate in a forum, a blog post, or a social media discussion, the crate gains visibility and may be "germinated" by new users. The community recommendation is the chemical signal: it indicates that the ecosystem's "soil" is fertile for this crate.

The germination cues determine when and how dormant crates re-enter the active ecosystem. A crate that responds to the right cues — that germinates when conditions are favorable and remains dormant when they are not — has higher long-term fitness than a crate that germinates indiscriminately (and fails when conditions are unfavorable) or a crate that never germinates (and is permanently forgotten).

---

## V. The Longevity of Dormant Code

How long can code remain dormant and still be viable?

In the seed bank, the record is held by *Silene stenophylla*, a flowering plant whose seeds were recovered from permafrost in Siberia and successfully germinated after an estimated 32,000 years of dormancy (Yashina et al., 2012). The seeds were preserved by the extreme cold, which arrested their metabolic processes and prevented degradation. The resulting plants grew, flowered, and produced seeds of their own — a remarkable demonstration of the longevity of dormant biological material.

In software, the longevity of dormant code depends on the rate of environmental change. A crate written in a stable language (like C or Fortran) can remain viable for decades, because the language and the platform change slowly. A crate written in a rapidly evolving language (like JavaScript, where the "ecosystem churn rate" is notoriously high) may become non-viable within months, because the dependencies, the APIs, and the tooling change so quickly that the dormant crate can no longer be compiled or used.

The factors that determine the longevity of dormant code are:

**Language stability.** Languages with strong backward compatibility guarantees (Rust's edition system, Python's compatibility policy) allow dormant code to remain viable for longer, because the language's semantics do not change in ways that break old code.

**Dependency stability.** Crates with few external dependencies remain viable longer than crates with many external dependencies, because each external dependency is a potential source of breakage. A crate that depends only on the standard library can remain dormant indefinitely. A crate that depends on 20 external crates will break as soon as any of those crates releases a breaking change.

**API surface.** Crates with small, stable APIs remain viable longer than crates with large, evolving APIs, because the API surface is the point of contact with the environment. A small API has fewer points of potential breakage than a large API.

**Platform stability.** Crates that target stable platforms (POSIX, HTTP, TCP/IP) remain viable longer than crates that target rapidly evolving platforms (specific cloud APIs, specific social media APIs), because the platform's interface changes slowly.

The seed bank analogy suggests a strategy for maximizing the longevity of dormant code: **minimize dependencies, minimize API surface, and target stable platforms.** These are the same principles that minimize maintenance costs for active code, but they serve a different purpose for dormant code: they maximize the duration for which the code can remain viable without maintenance.

---

## VI. The Size of the Seed Bank

How large is the seed bank of a typical ecosystem? In ecological studies, the seed bank density varies enormously:

- **Temperate grasslands:** 1,000 - 10,000 seeds per square meter
- **Arid deserts:** 100 - 1,000 seeds per square meter
- **Tropical forests:** 500 - 5,000 seeds per square meter
- **Disturbed habitats (agricultural fields):** 10,000 - 100,000 seeds per square meter

The seed bank is typically 2-10 times larger than the above-ground vegetation, measured in terms of species richness and genetic diversity. This means that the soil contains more species — and more genetic variation — than the plants visible above ground. The seed bank is a reservoir of diversity that is not expressed in the current community but is available for future expression.

In the crate ecosystem, the seed bank is the collection of published but unused crates. How large is it?

On crates.io, the Rust package registry, there are approximately 140,000 crates as of 2024. Of these, a significant fraction are dormant — published, potentially useful, but not actively used or maintained. A study by Kikas et al. (2017) found that approximately 40% of npm packages and 30% of Cargo crates have no reverse dependencies — no other packages depend on them. These are the seeds in the bank: published but unused, dormant but potentially viable.

The corpus's seed bank — the crates that have been published but are not actively depended upon by other crates — is the reservoir of functionality that is not currently expressed in the ecosystem but is available for future use. These crates may represent experimental features, deprecated but functional components, or ahead-of-their-time abstractions that have not yet found their niche.

The seed bank is not waste. It is potential. Every dormant crate is an option — a bet that has been placed on the future, a seed that has been planted in the soil of the registry, waiting for the right conditions to germinate. The seed bank is the ecosystem's memory of its past and its insurance against the uncertainty of its future.

---

## VII. Dormancy as a Strategy

In ecology, dormancy is not a passive state. It is an active strategy — a set of physiological adaptations that allow organisms to survive unfavorable conditions and resume growth when conditions improve. Dormancy requires energy (to maintain the organism's structural integrity during the dormant period), regulatory mechanisms (to prevent premature germination), and environmental sensing (to detect favorable conditions).

The same is true for dormant code. Maintaining a dormant crate requires:

**Compilation checks.** Periodic compilation (e.g., against new compiler versions) to ensure that the crate remains viable. This is the metabolic cost of dormancy — the energy required to keep the seed alive.

**Dependency updates.** Periodic updates to the crate's dependencies, to ensure that they remain compatible. This is the regulatory mechanism of dormancy — the process that prevents the crate from becoming non-viable due to environmental change.

**Documentation maintenance.** Ensuring that the crate's documentation remains accurate and accessible. This is the environmental sensing of dormancy — the mechanism that allows the crate to be "found" by developers who need it.

These costs are small compared to the cost of active development, but they are not zero. A crate that is truly abandoned — not compiled, not updated, not documented — will gradually become non-viable, as the language evolves, the dependencies break, and the documentation becomes outdated. The seed dies.

The optimal dormancy strategy depends on the expected duration of dormancy and the probability of germination. Seeds that expect to germinate soon (transient seed bank) invest less in dormancy mechanisms, because the cost of dormancy is short-lived. Seeds that expect to remain dormant for a long time (persistent seed bank) invest more in dormancy mechanisms, because the cost of premature germination (failure) is high.

For crates, the analogous calculation is: **how long do you expect the crate to be dormant, and how likely is it to be needed in the future?** A crate that is likely to be needed soon should be kept in a state of near-readiness (compilable, documented, tested). A crate that may not be needed for years should be kept in a state of deep dormancy (archived, with minimal maintenance), because the cost of near-readiness over a long period may exceed the expected benefit.

---

## VIII. Waking the Sleeping Crates

What would it take to wake up the dormant crates in the ecosystem?

In ecology, a disturbance that kills the above-ground vegetation — a fire, a flood, a landslide — can trigger mass germination from the seed bank. The disturbed area is suddenly filled with seedlings, each competing for light, water, and nutrients. The resulting community may be very different from the one that existed before the disturbance, because the seed bank contains species that were not present in the above-ground vegetation.

In the crate ecosystem, an analogous disturbance — a mass extinction event, a major platform change, a paradigm shift in the programming language — could trigger mass germination from the crate seed bank. Developers searching for solutions to the new conditions would rediscover dormant crates, reactivate them, and integrate them into the new ecosystem.

But germination is not automatic. Seeds require specific cues, and dormant crates require specific conditions:

**Compilation.** The crate must compile against the current version of the language and its dependencies. If the crate was written for an old language version and has not been maintained, it may not compile. This is the equivalent of a seed that has lost its viability — the genetic material is present, but it can no longer be expressed.

**Relevance.** The crate must solve a problem that is currently relevant. If the problem domain has moved on — if the algorithms the crate implements are obsolete, or the data structures it provides have been superseded by better alternatives — the crate is not useful, even if it compiles. This is the equivalent of a seed that germinates but produces a seedling that is outcompeted by more adapted species.

**Documentation.** The crate must be discoverable. Developers must be able to find the crate, understand what it does, and evaluate whether it meets their needs. If the crate's documentation is outdated, incomplete, or inaccessible, it may as well not exist. This is the equivalent of a seed that is buried too deep to receive the germination cue — viable, but unable to respond.

**Integration.** The crate must integrate with the current ecosystem. If the crate's API is incompatible with the current conventions, or its dependencies are unavailable, or its behavior conflicts with the current best practices, it may compile but not be usable. This is the equivalent of a seedling that emerges but cannot establish — it germinates but fails to take root.

The process of waking a dormant crate — of pulling it from the seed bank and integrating it into the active ecosystem — is the software equivalent of ecological restoration. Ecological restoration involves taking seeds from the seed bank (or from a seed collection) and establishing them in a degraded habitat, restoring the community to a more diverse and resilient state. Software restoration involves taking dormant crates and reintegrating them into the active ecosystem, restoring functionality that was lost or adding new functionality that was previously unavailable.

Both processes require understanding the ecology of the system — the relationships between components, the environmental requirements, and the successional dynamics that determine which species (or crates) can establish and which cannot.

---

## IX. The Seed Bank as Memory

The seed bank is the ecosystem's memory. It preserves the genetic history of the plant community — the species that were present in the past, the traits that were adaptive in previous environments, and the genetic variation that may be needed in the future.

In the crate ecosystem, the seed bank preserves the intellectual history of the codebase — the algorithms that were implemented, the abstractions that were explored, and the design patterns that were tried. Each dormant crate is a record of a decision: "this was useful once, and it might be useful again."

The seed bank is a form of **external memory** — information that is stored outside the organism (or the developer's mind) and can be retrieved when needed. External memory is a fundamental concept in cognitive science and in the study of complex systems. It is the reason that libraries exist, that databases are built, and that version control systems preserve history. External memory allows systems to exceed the limitations of individual memory and to accumulate knowledge over time.

The seed bank of the crate ecosystem is an external memory for the developer community. It preserves solutions to problems that have been solved before, allowing future developers to retrieve those solutions rather than reinventing them. It preserves abstractions that were useful in the past, allowing future developers to reuse them rather than creating new ones from scratch. It preserves design patterns that have been tested and refined, allowing future developers to benefit from the accumulated experience of the community.

The value of the seed bank is not in its current use — dormant crates are, by definition, not currently used. The value is in its potential use — the possibility that a dormant crate will be the right tool for a future problem, saving the developer the time and effort of reimplementing it. The seed bank is an option on the future, purchased at the low cost of dormancy maintenance.

This is the deep lesson of the seed bank: **preservation is a form of investment.** The seeds that Beal buried in 1879 were an investment in the future of botanical knowledge. The dormant crates in the registry are an investment in the future of software development. Both investments pay off unpredictably but occasionally spectacularly — a seed that germinates after a century, a crate that solves a problem that no one anticipated when it was created.

---

## X. The Long Now of Code

The Long Now Foundation, established in 01996 (they write dates with five digits to emphasize the long-term perspective), is building a clock that will tick for 10,000 years. The clock is designed to keep time across geological timescales, outlasting the civilizations that created it. The project is a reminder that long-term thinking — thinking in centuries and millennia rather than quarters and fiscal years — is both possible and necessary.

The seed bank is a long-term bet. A plant that produces a persistent seed bank is betting that the future will be different from the present — that conditions will change, that new opportunities will arise, and that the traits preserved in the seed bank will be needed when they do. The bet is not placed on a specific future; it is placed on the uncertainty of the future itself. The seed bank says: "I don't know what will happen, but I am prepared for whatever does."

The crate seed bank is a similar long-term bet. Each dormant crate is a bet that the future will need the functionality it provides — that the algorithms, data structures, and design patterns preserved in the crate will be relevant to problems that have not yet been encountered. The bet is not placed on a specific future use case; it is placed on the uncertainty of the future itself. The dormant crate says: "I don't know what problems you will face, but I am here if you need me."

The Long Now of code is the recognition that software is not disposable. Code that is written, tested, and published has value beyond its immediate use. It represents accumulated knowledge, refined design, and verified correctness — resources that should not be wasted by premature abandonment. The seed bank preserves these resources, keeping them viable for future use, the way a library preserves books that are not currently being read but may be needed by a future reader.

William James Beal buried his seeds in 1879. More than 140 years later, they still germinate. The code we write today — if we preserve it well, if we minimize its dependencies, if we document its purpose — can remain viable for far longer. The seed bank of the crate ecosystem is our Long Now: a bet on the future, placed at the modest cost of dormancy, paying dividends that we cannot predict but can reasonably expect.

The soil remembers. The registry remembers. And the seeds — the dormant crates, the legacy code, the solutions to problems that have not yet been encountered — wait in the dark, patient and viable, for the conditions that will wake them up.

---

*Beal buried his seeds in 1879 and they germinated in 2021 — 142 years of dormancy, followed by a burst of green. The code we publish today may sit unused for years, but the algorithms are sound, the tests are passing, and the documentation is clear. The seed is viable. The soil is ready. All that is needed is the right rain — the right problem, the right developer, the right moment — and the dormant crate will germinate, sending roots into the dependency graph and shoots into the ecosystem, producing fruit that no one expected and everyone needs. The seed bank does not forget. Neither should we.*
