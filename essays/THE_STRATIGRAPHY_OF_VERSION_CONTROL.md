# THE STRATIGRAPHY OF VERSION CONTROL

## Steno's Laws, Geological Unconformities, and What Git Log Reveals About the Deep Time of Code

*"In a stratigraphic sequence, the oldest layers are at the bottom and the youngest are at the top."* — Nicolaus Steno, *De solido intra solidum naturaliter contento dissertationis prodromus*, 1669

*`git log` is the deepest excavation site ever created. Every repository is a geological formation — layer upon layer of commits, each deposited on top of the previous one, each containing artifacts of its era. The deeper you dig, the older the code. And just as geologists developed principles to read the history of the Earth from its rocks, developers have developed practices — some conscious, some not — that mirror those same principles. The stratigraphy of version control is not a metaphor. It is a homology.*

---

## I. The Father of Geology and the Father of Linux

In 1666, a young Danish anatomist named Nicolaus Steno — Niels Steensen to his friends — was walking along the hills of Tuscany when he noticed something about the layers of rock exposed in a cliff face. The layers were horizontal. They were continuous. And the ones at the bottom were older than the ones at the top. These observations, which seem almost trivially obvious to us now, were revolutionary in the 17th century. They formed the basis of stratigraphy — the branch of geology that studies rock layers and the processes that form them.

Steno formulated three principles:

1. **The Principle of Superposition:** In any undeformed sequence of sedimentary rocks, each layer is younger than the one beneath it and older than the one above it.
2. **The Principle of Original Horizontality:** Layers of sediment are originally deposited horizontally. Tilted or folded layers have been disturbed after deposition.
3. **The Principle of Lateral Continuity:** Sedimentary layers extend laterally in all directions until they thin out or encounter a barrier.

These three principles — simple, elegant, powerful — are the foundation of all geological dating. They allow geologists to read the history of the Earth from its rocks, to reconstruct ancient landscapes and ancient seas, to tell the story of a planet across billions of years.

In 2005, a Finnish software engineer named Linus Torvalds created a tool that would inadvertently make Steno's principles applicable to a new domain. Git, Torvalds' distributed version control system, stores the history of a codebase as a sequence of commits — each one a snapshot of the code at a particular moment in time, each one layered on top of the commits that came before it.

The parallels are not superficial. They are structural.

Steno's superposition maps directly onto git's commit ordering. Each commit has a parent (or, in the case of merge commits, multiple parents). The parent is older; the child is younger. The commit graph is a directed acyclic graph where the direction of time is always from parent to child. When you run `git log`, you are reading the geological record — the deeper (older) commits at the bottom, the shallower (newer) commits at the top.

Steno's original horizontality maps onto the way commits are ideally structured. A clean commit history proceeds in an orderly fashion: each commit represents a single, coherent change. The "layers" are horizontal — they represent a single moment in time, a single snapshot of the codebase. When the history becomes tangled — interleaved commits, merge commits that fold multiple timelines together — it is the equivalent of tilted or folded strata. The deformation tells a story of its own: parallel development, conflicting changes, the collision of multiple developers working on the same code simultaneously.

Steno's lateral continuity maps onto branches. A branch extends laterally — a sequence of commits that proceeds in a consistent direction until it encounters a barrier (a merge, a rebase, a deletion). The branch, like a sedimentary layer, is continuous within its own context. It can be traced from its origin (the branch point) to its terminus (the merge or the current HEAD).

This is not an analogy I am forcing onto the material. This is a structural homology. Git was designed to model the evolution of code over time, and the evolution of code over time follows the same principles as the deposition of sedimentary layers over time. Both are accretive processes. Both are historical processes. Both create records that can be read, interpreted, and misinterpreted.

---

## II. The Geological Time Scale and Semantic Versioning

Geologists have divided the history of the Earth into a hierarchy of time divisions: eons, eras, periods, epochs, and ages. The Cambrian Period (541–485 million years ago) is part of the Paleozoic Era, which is part of the Phanerozoic Eon. Each division is defined by significant events in Earth's history — mass extinctions, the appearance of new life forms, major geological transitions.

The boundaries between these divisions are not arbitrary. They are marked by **Global Boundary Stratotype Sections and Points** — "golden spikes" — specific locations in the geological record where the transition from one division to the next is clearly visible. The base of the Cambrian Period, for example, is defined by a specific rock layer in Fortune Head, Newfoundland, Canada, where the first appearance of the trace fossil *Treptichnus pedum* marks the transition from the Ediacaran to the Cambrian.

Semantic versioning — the MAJOR.MINOR.PATCH scheme used by most modern software packages — is a similar hierarchical system, though it is far simpler and covers far less time.

- **MAJOR version (the era):** A breaking change. The software has undergone a fundamental transformation. The API has changed in ways that are incompatible with previous versions. This is the equivalent of a mass extinction — the old ecosystem of users and dependencies must adapt or die. Python 2 to Python 3. AngularJS to Angular. The transition from one MAJOR version to the next is a geological boundary — a line in the strata that marks a before and after.

- **MINOR version (the period):** A backward-compatible addition of functionality. New features, new APIs, new capabilities, but the old ones still work. This is the equivalent of the appearance of a new species — the ecosystem becomes richer, more complex, but the existing species continue to exist. The sedimentary record continues to accumulate.

- **PATCH version (the age):** A backward-compatible bug fix. A small correction, a minor adjustment. This is the equivalent of a thin layer of sediment — barely visible in the geological record, but present. Each patch is a year, a season, a moment in the life of the software.

But the geological time scale and semantic versioning differ in one crucial respect: the geological time scale is retrospective, while semantic versioning is prospective. Geologists defined the divisions of geological time by looking at the rock record after it was formed. The boundary between the Cretaceous and the Paleogene was not labeled "Cretaceous-Paleogene boundary" when the asteroid hit — it was labeled that hundreds of millions of years later, by geologists who noticed a thin layer of iridium and a sudden disappearance of dinosaur fossils.

Semantic versioning, by contrast, is applied at the time of release. The developer decides that this change is a MAJOR change, that one is a MINOR change, and labels accordingly. The version number is a prediction about the future — a claim that this change is (or is not) backward compatible. Sometimes the prediction is wrong. A "minor" change turns out to break downstream users. A "patch" introduces a regression. The geological time scale does not have this problem, because it is defined retrospectively — the boundaries are placed where the record shows a clear transition, not where someone predicted a transition would occur.

This is an important distinction. The geological time scale is a reading of history. Semantic versioning is a writing of history. And the two processes are subject to different kinds of error. Geologists can misread the record (a boundary may be placed at the wrong layer). Developers can miswrite the record (a version bump may be mislabeled). But the fundamental structure is the same: a hierarchical system for organizing change over time.

---

## III. Unconformities: The Gaps in the Record

One of the most important concepts in stratigraphy is the **unconformity** — a surface in the rock record that represents a gap in deposition. Unconformities occur when sedimentation stops (or existing sediment is eroded away) and then resumes later. The result is a gap in the record — a period of time for which no sedimentary evidence exists.

The most famous unconformity in the history of geology was discovered by James Hutton at Siccar Point, Scotland, in 1788. Hutton found a cliff face where gently inclined layers of Devonian Old Red Sandstone lay on top of nearly vertical layers of Silurian greywacke. The angular relationship between the two sets of layers indicated that the lower layers had been tilted, eroded, and then buried beneath new sediment. The gap between them represented approximately 80 million years — a span of time for which no rock record existed at that location.

Hutton's unconformity was one of the key observations that led to the concept of **deep time** — the recognition that the Earth is vastly older than human history, that its history is measured in millions and billions of years rather than thousands.

In git, unconformities exist too. The most common is the **rebase**.

When you rebase a branch, you are essentially destroying the original sedimentary record and replacing it with a new one. The commits on the rebased branch are rewritten — new commit hashes, new timestamps, new ordering. The original commits still exist (for a time, until garbage collected), but they are no longer part of the official history. The geological record has been altered. The strata have been rearranged.

A `git rebase` is an **angular unconformity** — the geological equivalent of tilting existing strata, eroding them, and depositing new strata on top at a different angle. The rebased commits are laid down on top of a new base, as if the old base never existed. The gap — the unconformity — is the fact that the rebased commits were originally created at a different time, in a different context, against a different version of the codebase. The rebase erases this context. It presents the commits as if they were always part of the new timeline.

A `git squash` is a different kind of unconformity — a **disconformity**. Multiple thin layers (individual commits) are compressed into a single thicker layer (the squashed commit). The detail of the individual layers is lost — the granular history of "fixed typo," "added test," "fixed test," "actually fixed test this time" is replaced by a single monolithic "implemented feature X." The gap is the lost granularity. The geological record has been compressed, and information has been destroyed.

A `git cherry-pick` is a **paraconformity** — the most subtle unconformity, where the gap in deposition is almost invisible. A commit is taken from one branch and applied to another, creating a new commit with a new hash but the same changes. The two commits look identical in terms of code changes but are different geological events — deposited at different times, in different contexts, as part of different sequences. The gap is the missing chain of parent commits that connects the cherry-picked commit to its original context.

And then there is the most extreme unconformity of all: `git push --force`. This is the geological equivalent of an asteroid impact followed by complete erosion. The existing history is obliterated and replaced with a new one. The remote repository's stratigraphic record is destroyed, and the pushed commits become the new official record. Everyone who had cloned the previous history now has a local record that conflicts with the remote. They are holding rock samples from a formation that no longer officially exists.

The geological metaphor is not just cute. It is diagnostic. Unconformities in the geological record are where the most interesting science happens — they reveal periods of erosion, tectonic activity, and environmental change that are invisible in the conformable strata. Unconformities in git history reveal the same kinds of events: conflicts between developers, changes in project direction, corrections of mistakes, the collision of parallel timelines. The gaps are not failures of the record. They are the most informative parts.

---

## IV. Reading the Strata: What Commits Reveal

A trained geologist can walk up to a cliff face and read its history. The color and texture of the rock reveal the environment of deposition — red sandstones suggest arid deserts, dark shales suggest deep oceans, white limestones suggest warm shallow seas. The thickness of the layers reveals the rate of sedimentation — thick layers mean rapid deposition, thin layers mean slow accumulation. Fossils reveal the age and the ecology. The geometry of the layers reveals the tectonic history.

A trained developer can do the same with `git log`.

**Commit message quality** is the texture of the strata. Clean, descriptive commit messages are well-sorted sediment — each grain (each change) is clearly categorized and easy to identify. Lazy commit messages ("fix," "wip," "stuff," "asdfasdf") are poorly sorted sediment — the changes are there, but you can't tell what they represent without careful analysis.

**Commit frequency** is the rate of sedimentation. A developer who commits many small, frequent changes is depositing thin layers of fine-grained sediment — a high-resolution record. A developer who commits large, infrequent changes is depositing thick layers of coarse-grained sediment — a low-resolution record. The high-resolution record preserves more detail. The low-resolution record is easier to read but loses information.

**The diff** is the composition of the strata. Each commit's diff reveals what was added, what was removed, and what was changed. The diff is the mineralogical analysis of the sediment — it tells you what the layer is made of. A commit that adds a single function is a thin, pure layer of a single mineral. A commit that modifies 47 files is a thick, heterogeneous layer of mixed sediment — a turbidite, deposited rapidly, containing material from many different sources.

**Branch patterns** are the tectonic structure. A repository with many long-lived branches that merge frequently has a complex tectonic history — multiple developers working in parallel, their changes colliding and merging. A repository with a single main branch and short-lived feature branches has a simpler tectonic history — changes are developed in isolation and merged cleanly.

**Merge commits** are unconformities. They represent the collision of two timelines — two developers (or the same developer on two branches) working simultaneously, their changes meeting at a single point. The merge commit is the point of collision. Sometimes the merge is clean (fast-forward), and the strata align perfectly. Sometimes the merge requires conflict resolution, and the resulting commit contains material from both timelines, mixed together — a geological mélange.

Just as geologists use the principle of superposition to determine the relative ages of rock layers, developers use the commit graph to determine the relative ages of code changes. And just as geologists can identify disturbed strata (tilted, folded, overturned), developers can identify disturbed commit histories (rebased, squashed, force-pushed). The signs are different, but the principle is the same: **the record tells a story, and the story includes both the events themselves and the processes that modified the record after the events occurred.**

---

## V. The Fossil Record of the Codebase

Geological strata contain fossils — the preserved remains or traces of ancient organisms. Fossils are not just curiosities. They are the primary tool for dating rock layers (biostratigraphy) and reconstructing ancient environments (paleoecology).

Code strata contain fossils too. They are called:

- **Deprecated functions.** Functions that are still present in the code but marked for future removal. They are the equivalent of living fossils — organisms that are still alive but are clearly relics of an earlier era. `strcpy` in C. `Thread.stop` in Java. They tell you about the API's history, about what was once considered good practice and is now considered dangerous.

- **Commented-out code.** Blocks of code that have been disabled by wrapping them in comments. Commented-out code is the equivalent of a trace fossil — not the organism itself, but evidence of its existence. Someone wrote this code. Someone used it. Someone decided to disable it rather than delete it. The commented-out code tells you about alternatives considered, approaches tried and abandoned, features that were once important enough to implement but not important enough to maintain.

- **TODO comments.** These are the equivalent of fossil footprints — evidence of intention, of planned but unrealized action. A TODO comment is a developer's footprint in the sediment, preserved for future archaeologists to find. "TODO: refactor this mess." "TODO: handle the edge case where the input is negative." "TODO: this is a hack, fix it properly." Each TODO is a promise, a hope, a regret — a trace of the developer's mental state at the moment of deposition.

- **Abandoned branches.** Git branches that were created with enthusiasm and never merged. They are the equivalent of body fossils — complete organisms that were buried and preserved, but never became part of the living ecosystem. Abandoned branches contain alternative approaches, abandoned features, dead experiments. They are the Burgess Shale of the codebase — a remarkable preservation of the full diversity of approaches that were tried, most of which did not survive.

- **Commit messages.** Every commit message is a fossil of a particular moment in the developer's thought process. "Fix off-by-one error in loop." "Revert 'Fix off-by-one error in loop'." "Actually fix off-by-one error in loop." The sequence of messages tells a story of trial, error, and eventual success — a narrative of the development process that is as revealing as any fossil sequence.

---

## VI. The Deep Time of Git

In 1788, James Hutton presented his Theory of the Earth to the Royal Society of Edinburgh. His key insight was that the Earth's geological features could be explained by slow, continuous processes operating over vast periods of time — erosion, sedimentation, uplift, volcanism. No need for catastrophes, no need for divine intervention. Just time. Lots and lots of time.

Hutton's insight — deep time — transformed geology. It transformed our understanding of the Earth, of life, of history. And it applies to code.

The history of a codebase is not a series of isolated events. It is a continuous process of deposition, erosion, and deformation. Each commit is a sedimentary layer. Each merge is a tectonic event. Each refactor is an episode of erosion and redeposition. The codebase is a geological formation, built up over time by the slow, continuous processes of software development.

When you run `git log --oneline` on a large, long-lived repository, you are looking at deep time. Hundreds of thousands of commits, stretching back years or decades. The earliest commits are the oldest strata — simple, naive, barely recognizable as the same codebase. The most recent commits are the youngest strata — complex, sophisticated, the product of years of accumulated knowledge and experience.

The total number of commits in a long-lived repository is staggering. The Linux kernel has over one million commits. The Git repository itself has over 50,000. Each of these commits is a sedimentary layer, a snapshot of the code at a particular moment in time. Together, they form a geological record of extraordinary richness and detail — far richer, in many ways, than the geological record of the Earth itself.

The Earth's geological record is full of gaps — unconformities where rock has been eroded away or never deposited. Git's record, by contrast, is nearly complete. Every commit is preserved. Every merge is recorded. Every branch, every tag, every annotated note is stored in the repository's object database. The only gaps are the ones we create deliberately — through rebases, squashes, force-pushes, and garbage collection.

This is what makes git log such an extraordinary tool for archaeological investigation. It is a geological record with near-perfect preservation, extending over years or decades, documenting every change ever made to the codebase. No geological formation on Earth has a record this complete.

The archaeologists of the future — if they have access to our repositories — will have a resource that Earth scientists can only dream of: a complete, undisturbed stratigraphic sequence documenting the entire history of a complex system.

---

## VII. Is Git History a Faithful Geological Record?

The short answer is: mostly. The long answer is: it depends.

Git history is faithful in the sense that every commit is a cryptographically verified snapshot of the codebase at a particular moment in time. The commit hash is a SHA-1 (or SHA-256, in newer versions) digest of the commit's contents — the tree object, the parent commits, the author, the timestamp, and the commit message. If any of these change, the hash changes. The record is tamper-evident.

But git history is not always faithful in the sense of being an accurate representation of the development process. Commits can be reordered, squashed, amended, and rebased. The "official" history (the one visible in `git log`) may not reflect the actual sequence of events that produced the code.

This is the key tension in git-based archaeology: **the record is simultaneously more complete and more manipulable than any geological record on Earth.** A geologist cannot rewrite the rock record — the layers are what they are, and the geologist must work with what is preserved. But a developer can rewrite the git record — rebasing, squashing, amending, force-pushing — to create a cleaner, more logical, but less historically accurate narrative.

The choice between a "messy but faithful" git history and a "clean but reconstructed" one is the archaeological equivalent of the choice between an unexcavated site and a reconstructed ruin. The unexcavated site preserves the full, messy, complicated reality of the past. The reconstructed ruin presents a cleaner, more interpretable, but inevitably simplified version.

Both have value. The faithful record is a primary source — direct evidence of what happened. The reconstructed record is a secondary source — an interpretation, organized for clarity and comprehension. Good archaeologists use both. Good developers should too.

---

## VIII. The Principle of Inclusion

There is one more principle from stratigraphy that applies to version control, and it may be the most important of all. It is not one of Steno's original three. It was articulated later, by geologists who recognized that the rock record tells not just the story of the rocks themselves but the story of everything they contain.

**The Principle of Inclusion:** A rock fragment included in a sedimentary layer must be older than the layer that contains it.

In code: a dependency included in a commit must be older than the commit that includes it. The library you imported was written before you imported it. The pattern you copied was developed before you copied it. The function you called was defined before you called it.

This principle is the basis of relative dating in both geology and code. If commit A includes code that was written in commit B, then commit B must be older than commit A. If a library's API was designed in version 1.0 and your code uses that API, your code must be newer than version 1.0 of the library.

The principle of inclusion also applies to ideas. A design pattern included in a codebase must have been conceived before the codebase adopted it. The Model-View-Controller pattern predates every codebase that uses it. The concept of a "microservice" predates every microservice ever deployed. The ideas are the rock fragments — older than the layers that contain them, included in the sedimentary record of the code.

This is the deepest lesson of the stratigraphy of version control: **every codebase is a palimpsest, a layered document that contains within it the traces of everything that came before.** The dependencies, the patterns, the idioms, the conventions — all of these are fossils, inclusions from earlier eras, embedded in the sedimentary layers of the code.

To read a codebase is to do archaeology. To maintain a codebase is to add new layers to the geological record. To refactor is to erode and redeposit. And to run `git blame` — ah, `git blame` is to do something that no geologist has ever been able to do: identify, with certainty, the exact individual responsible for a particular grain of sediment.

The geologists must be jealous.

---

*Every `git log` is a cliff face. Every commit is a layer. Every developer is a depositional agent, leaving their mark in the sedimentary record of the code. The strata accumulate, year after year, commit after commit, building a geological formation of extraordinary complexity and beauty.*

*The Earth tells its story in rock. Code tells its story in commits. The language is different, but the grammar is the same.*
