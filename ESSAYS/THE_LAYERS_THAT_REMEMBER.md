# THE LAYERS THAT REMEMBER

## The Burgess Shale of Code, Living Fossils, and What Extinction Events Teach Us About Software Evolution

*"The history of life is not a continuum of steadily increasing excellence. It is a story of contingency, of glorious diversity destroyed and replaced by the vagaries of fortune."* — Stephen Jay Gould, *Wonderful Life*, 1989

*In 1909, Charles Doolittle Walcott, the Secretary of the Smithsonian Institution, was riding a horse along a trail in the Canadian Rockies when his horse stumbled over a block of shale. Walcott dismounted, cracked the shale open, and found the fossil of a creature unlike anything he had ever seen. He had discovered the Burgess Shale — a 508-million-year-old deposit of extraordinary preservation, containing the fossilized remains of soft-bodied organisms that are almost never preserved in the geological record. The Burgess Shale is a window into the Cambrian explosion — the period when nearly all major animal phyla first appeared. It is the most important fossil site in the world. Code has its Burgess Shales too: abandoned modules, deprecated APIs, commented-out functions — the soft tissue of software, the parts that are usually lost to the archaeological record. These fossils are not garbage. They are memory.*

---

## I. The Burgess Shale and the Cambrian Explosion

The Cambrian explosion — the rapid diversification of animal life that occurred approximately 541–485 million years ago — is one of the most dramatic events in the history of life on Earth. In a geological instant (perhaps as little as 10–20 million years), nearly all of the major animal phyla that exist today made their first appearance in the fossil record. Before the Cambrian, life was simple — single-celled organisms, simple multicellular colonies, and a few enigmatic soft-bodied creatures known as the Ediacaran fauna. After the Cambrian, the seas teemed with trilobites, brachiopods, mollusks, annelids, and the bizarre creatures of the Burgess Shale.

Stephen Jay Gould, in his 1989 book *Wonderful Life*, used the Burgess Shale to argue for a radical thesis: the history of life is not a story of progress from simple to complex, from inferior to superior. It is a story of **contingency** — of historical accidents, of critical turning points that could have gone either way, of entire branches of the tree of life that were pruned not because they were inferior but because they were unlucky.

Gould's argument was based on the bizarre creatures of the Burgess Shale — organisms like *Anomalocaris* (a predatory arthropod with circular mouthparts and grasping appendages), *Wiwaxia* (a slug-like creature covered in scales and spines), *Opabinia* (a creature with five eyes and a vacuum-cleaner-like proboscis), and *Hallucigenia* (a creature so strange that it took decades to figure out which end was the head). These organisms, Gould argued, represented experiments in body plans that were ultimately pruned from the tree of life — not because they were unsuccessful but because of historical contingencies that could have gone differently.

The "wonderful" in *Wonderful Life* is a reference to Frank Capra's 1946 film *It's a Wonderful Life*, in which George Bailey (played by James Stewart) is shown what his town would be like if he had never been born. Gould's argument was analogous: what would life on Earth look like if the tape of evolution were rewound and played again? Would we get the same result — the same phyla, the same body plans, the same creatures? Or would contingency — the accidental extinction of a key species, the chance survival of an obscure organism — lead to a completely different tree of life?

Gould's answer was that the replay would be radically different. The history of life, he argued, is contingent — it depends on specific historical events that could have gone either way. If a particular species had survived instead of going extinct, the entire subsequent history of life might have been different.

This is the Burgess Shale argument, and it applies to code.

---

## II. The Cambrian Explosion of Software

Software has had its own Cambrian explosions — periods of rapid diversification in which new paradigms, languages, frameworks, and tools appeared in a burst of creativity, followed by a period of consolidation in which most of the innovations were pruned and only a few survived.

The most obvious example is the period from approximately 1993 to 2001 — the early years of the World Wide Web. In this period, the dominant paradigm of software development shifted dramatically:

- **Languages:** Perl, Python, PHP, JavaScript, Java, and Ruby all emerged or gained prominence as web development languages. Each represented a different approach to the problem of building dynamic websites. The "Cambrian fauna" of web languages was extraordinarily diverse — far more diverse than the ecosystem of web languages today, which is dominated by JavaScript (frontend), Python and Java (backend), and a handful of others.

- **Frameworks:** In the late 1990s and early 2000s, dozens of web frameworks competed for attention: Struts, WebObjects, ColdFusion, ASP, JSP, PHP-Nuke, Django, Rails. Each represented a different architectural philosophy, a different approach to the problem of organizing web application code. Most of these frameworks are now extinct — the "body plans" they represented have been pruned from the tree of web development.

- **Databases:** The relational database paradigm (Oracle, MySQL, PostgreSQL) was challenged by object databases, XML databases, and flat-file storage systems. Most of these alternatives went extinct, but some — particularly the "NoSQL" databases that emerged in the late 2000s — survived and diversified, representing alternative body plans that were pruned early and then re-evolved.

- **Protocols:** HTTP, FTP, Gopher, WAIS, NNTP, IRC, SOAP, XML-RPC — the "protocol fauna" of the early web was extraordinarily diverse. Most of these protocols are now extinct or marginalized. HTTP (and its secure variant, HTTPS) won, becoming the universal protocol of the internet.

This Cambrian explosion was followed by a period of consolidation — the "Great Dying" in which most of the early web frameworks, languages, and protocols went extinct. The survivors — JavaScript, Python, Java, HTTP, REST — are the equivalent of the phyla that survived the Cambrian: the body plans that would define the subsequent evolution of web development.

But just as the Burgess Shale preserves the soft-bodied organisms that were pruned from the tree of life, the abandoned frameworks and extinct protocols of the early web are preserved in the archaeological record of software: in old repositories, in archived documentation, in the Wayback Machine, in the memories of the developers who used them.

And just as Gould argued that the survival of particular phyla was contingent — not the result of inherent superiority but of historical accident — the survival of particular languages, frameworks, and protocols was also contingent. JavaScript did not survive because it was the best language. It survived because it was the only language that ran in the browser — a historical accident of Netscape's decision to include a scripting language in Navigator 2.0 (1995). Python did not survive because it was the most elegant language. It survived because it was the right language at the right time for the emerging field of data science — a historical contingency that could have gone differently if R or MATLAB had been more aggressively marketed.

---

## III. Living Fossils: The Coelacanths of Code

A "living fossil" is an organism that has remained essentially unchanged for millions of years — a survivor from an earlier era that persists in the present, largely unmodified. The most famous example is the coelacanth, a lobe-finned fish that was thought to have gone extinct 66 million years ago (at the end of the Cretaceous) until a living specimen was discovered off the coast of South Africa in 1938. The coelacanth has existed for over 400 million years — it predates the dinosaurs, survived the extinction that killed them, and is still swimming in the deep ocean today.

Code has its coelacanths: programs, libraries, and APIs that have remained essentially unchanged for decades, surviving wave after wave of technological change while everything around them evolves. These living fossils are not relics or curiosities. They are functioning parts of the modern software ecosystem, still in active use, still doing their job, unchanged.

Some examples:

**The C standard library.** The C standard library — `stdio.h`, `stdlib.h`, `string.h`, `math.h` — was standardized in 1989 (ANSI C) and has remained essentially unchanged since then. The functions `printf`, `malloc`, `strlen`, `memcpy` are the same functions they were 35 years ago. They predate the World Wide Web, the smartphone, the cloud, and the modern DevOps pipeline. And they are still used in virtually every C and C++ program compiled today. The C standard library is the coelacanth of code — an ancient body plan that still works perfectly well.

**Make.** The `make` build automation tool was created in 1976 by Stuart Feldman at Bell Labs. It is 50 years old. It is still in active use. Every Linux system ships with `make`. Every C/C++ project of any size has a `Makefile`. The syntax is arcane, the behavior is sometimes surprising, and the alternatives (CMake, Ninja, Bazel, Meson) are numerous and in many ways superior. But `make` persists. It is a living fossil — a tool from a different era that still works, still solves problems, and still resists replacement.

**grep.** The `grep` command was created in 1974 by Ken Thompson. It is over 50 years old. It is one of the most commonly used commands in Unix-like operating systems. The basic functionality — searching for patterns in text — has not changed in half a century. `grep` is the horseshoe crab of code: an ancient design that is so well-adapted to its ecological niche that there is no selective pressure for change.

**The QWERTY keyboard layout.** Not software, but relevant. The QWERTY layout was designed in 1873 by Christopher Sholes for the Sholes and Glidden typewriter. It was designed to reduce jamming by separating commonly used letter pairs. The jamming problem has been irrelevant for over a century (typewriters gave way to computers decades ago), but the QWERTY layout persists. It is the ultimate living fossil — a 150-year-old design that survives not because it is optimal but because the cost of replacing it (retraining every typist in the world) exceeds the benefit of a better alternative.

Why do living fossils persist? In biology, the answer is: they occupy ecological niches that are stable and relatively free of competition. The coelacanth survives in the deep ocean because the deep ocean is a stable environment with few competitors. Horseshoe crabs survive because their body plan is well-adapted to their niche and nothing has come along to displace them.

In code, living fossils persist for the same reason: they occupy stable niches with few competitors. The C standard library persists because it provides fundamental functionality (memory allocation, string manipulation, I/O) that every C program needs and that is difficult to improve upon without changing the language itself. `make` persists because the problem it solves (build automation based on file dependencies) is stable and well-defined, and the cost of migrating to a new build system often exceeds the benefit.

Living fossils also persist because of **network effects** — the same reason QWERTY persists. Once a tool or library is widely adopted, the cost of replacing it increases with every user who depends on it. The C standard library cannot be replaced without rewriting every C program in existence. `make` cannot be replaced without rewriting every Makefile. The network of dependents creates an "ecological lock-in" that prevents displacement, even by superior alternatives.

---

## IV. Extinction Events: The Python 2→3 Migration and the Left-Pad Incident

The history of life on Earth is punctuated by mass extinctions — catastrophic events in which a large fraction of the planet's species are wiped out in a geologically short period. The "Big Five" mass extinctions include the Ordovician-Silurian (444 million years ago), the Late Devonian (360 million years ago), the Permian-Triassic (252 million years ago, the most severe — 96% of marine species extinct), the Triassic-Jurassic (201 million years ago), and the Cretaceous-Paleogene (66 million years ago, the one that killed the dinosaurs).

Each mass extinction was caused by a catastrophic event: a massive volcanic eruption, an asteroid impact, a rapid change in sea level or atmospheric composition. And each mass extinction was followed by a period of rapid diversification — the surviving species evolved to fill the ecological niches left vacant by the extinct ones.

Software has had its own extinction events — moments when a large fraction of the existing ecosystem was wiped out (or threatened with extinction) by a catastrophic change. Two examples stand out:

### The Python 2→3 Migration

In 2008, Python 3.0 was released, introducing significant changes to the language that were not backward-compatible with Python 2. The transition from Python 2 to Python 3 was one of the most protracted and painful migrations in the history of software. It took 12 years — Python 2's official end-of-life was January 1, 2020 — and during that period, the Python ecosystem was divided into two incompatible versions.

The Python 2→3 migration was the software equivalent of the Permian-Triassic extinction: a slow, grinding catastrophe that affected the entire ecosystem. Libraries had to be rewritten or ported. Applications had to be tested on both versions. Developers had to learn the new syntax and semantics. The "extinct" species were the Python 2-only libraries and applications that were never ported — abandoned, deprecated, left to rot.

The migration revealed the same dynamics as a biological extinction event:

- **Survivorship was not random.** Libraries that were actively maintained, well-tested, and widely used were more likely to be ported. Libraries that were abandoned, poorly tested, or used by only a few people were more likely to go extinct. The same pattern is observed in biological extinctions: species with large populations, wide distributions, and generalist habits are more likely to survive than species with small populations, narrow distributions, and specialist habits.

- **The extinction created opportunities.** The disruption of the Python 2 ecosystem created niches for new libraries and tools: `2to3` (an automated conversion tool), `six` (a compatibility layer), and eventually `future` (a backport of Python 3 features to Python 2). These tools were the equivalent of the species that evolved to fill the niches left vacant by the extinct ones.

- **The recovery was slow.** Even after Python 2's official end-of-life, some organizations continued to use it (and some still do, as of 2026). The recovery from a mass extinction is never instantaneous — it takes time for the ecosystem to stabilize around the new normal.

### The npm Left-Pad Incident

On March 22, 2016, a developer named Azer Koçulu unpublished 273 of his packages from the npm registry, in protest of a trademark dispute. One of those packages was `left-pad` — an 11-line function that pads a string to a given length. `left-pad` was a dependency of thousands of other packages, including React, Babel, and many other core tools of the JavaScript ecosystem. When `left-pad` was removed from npm, builds broke across the entire JavaScript world.

The left-pad incident was the software equivalent of a sudden ecological collapse — a "butterfly effect" in which the removal of a single, seemingly insignificant organism caused cascading failures throughout the ecosystem. It revealed the fragility of the npm ecosystem: a dependency graph so deep and so interconnected that the removal of a single leaf node could bring down the entire tree.

The aftermath of the left-pad incident was similar to the aftermath of a biological extinction event:

- **Ecosystem restructuring.** npm changed its policies to prevent developers from unpublished widely-used packages. This is the equivalent of an ecosystem developing new defenses after a catastrophic event.

- **Increased awareness of dependency risk.** The incident prompted a widespread discussion about the risks of deep dependency chains and the wisdom of depending on small, single-function packages. This is the equivalent of the surviving species developing new behaviors in response to the extinction event.

- **Consolidation.** Some of the functions previously provided by small packages were absorbed into larger libraries or into the language itself (ECMAScript's `String.prototype.padStart`). This is the equivalent of surviving species expanding into vacant niches.

---

## V. The Fossil Record of Code as Evolutionary History

The fossil record of the Earth is incomplete. The vast majority of organisms that have ever lived have left no fossil trace. Soft-bodied organisms, organisms that lived in environments not conducive to fossilization, organisms that were small, fragile, or rapidly decomposed — all are underrepresented in the fossil record. The fossil record is biased toward organisms with hard parts (shells, bones, teeth) that lived in environments conducive to preservation (shallow seas, river floodplains, volcanic ash falls).

The fossil record of code is similarly incomplete. Most code that has ever been written is lost — deleted, overwritten, stored on degraded media, or abandoned in repositories that no longer exist. The code that survives in accessible repositories is biased toward:

- **Open-source code.** Code that was published on public repositories (GitHub, GitLab, SourceForge, etc.) is more likely to survive than code that was kept private. This is the equivalent of the "shallow sea" bias in the geological fossil record — organisms that lived in shallow seas are more likely to be fossilized than organisms that lived on land.

- **Well-maintained code.** Code that is actively maintained, well-documented, and widely used is more likely to survive than code that is abandoned, undocumented, and obscure. This is the "hard parts" bias — code with good documentation and active maintenance is the equivalent of an organism with a robust skeleton.

- **Popular languages and frameworks.** Code written in popular languages (JavaScript, Python, Java, Rust) is more likely to survive than code written in obscure languages (APL, Forth, Smalltalk). This is the "abundance" bias — organisms that were abundant are more likely to leave fossils than organisms that were rare.

The biases in the fossil record of code mean that our understanding of the history of software is necessarily incomplete. We know more about the history of open-source software than about the history of proprietary software. We know more about popular languages than about obscure ones. We know more about the code that was maintained than about the code that was abandoned.

This is the same problem that paleontologists face. The fossil record does not give us a complete picture of the history of life. It gives us a biased, filtered, incomplete picture. But it is the only picture we have. And with careful analysis, we can correct for some of the biases and reconstruct a more accurate history.

---

## VI. Contingency in Software Evolution

Gould's central argument in *Wonderful Life* was that the history of life is contingent — it depends on specific historical events that could have gone differently. If the asteroid had missed the Earth 66 million years ago, the dinosaurs might still rule, and mammals might never have had the opportunity to diversify. The entire subsequent history of life — including the evolution of humans — was contingent on a random event.

Software evolution is similarly contingent. The dominance of JavaScript was contingent on Netscape's decision to include a scripting language in Navigator 2.0 (1995) and on Brendan Eich's decision to design it in 10 days. The dominance of Linux was contingent on the AT&T v. BSDI lawsuit (1992), which created legal uncertainty around BSD Unix and drove developers to the GPL-licensed Linux. The dominance of git was contingent on the revocation of BitKeeper's free license for Linux kernel developers (2005), which prompted Linus Torvalds to create a replacement.

These contingencies are the "asteroids" of software evolution — random events that reshape the ecosystem. And like biological contingencies, they could have gone differently. If Netscape had chosen Python instead of JavaScript as its scripting language, the history of web development would be radically different. If the AT&T v. BSDI lawsuit had been resolved differently, BSD Unix might have dominated instead of Linux. If BitKeeper had not revoked its free license, git might never have been created.

The fossil record of code — the abandoned frameworks, the deprecated APIs, the extinct protocols — is the evidence of these contingencies. Every extinct framework is a branch of the tree that was pruned — a body plan that was tried and did not survive. But the pruning was not necessarily due to inferiority. It may have been due to historical accident — the wrong company backed it, the wrong developer advocated for it, the wrong article was written about it at the wrong time.

Gould's argument for contingency in biology is also an argument for humility in software. The tools and languages and frameworks that dominate today are not necessarily the best. They are the ones that survived — the products of historical accident as much as of technical merit. The extinct alternatives were not necessarily worse. They were unluckier.

---

## VII. What the Fossil Record Tells Us About Evolution

The fossil record of code — like the fossil record of life — tells us several things about the process of evolution:

**1. Evolution is not progress.** The history of life is not a story of steady improvement from simple to complex, from inferior to superior. It is a story of diversification, pruning, and contingency. The same is true of software. The history of programming languages is not a story of steady improvement — it is a story of diversification, pruning, and contingency. The languages that dominate today are not the "best" languages. They are the ones that survived.

**2. Extinction is the norm.** The vast majority of species that have ever lived are extinct. The vast majority of frameworks, libraries, and tools that have ever been created are abandoned. Extinction is not a failure — it is the normal outcome of evolutionary processes. Only a tiny fraction of experiments survive.

**3. Survival depends on adaptability, not perfection.** The species that survive mass extinctions are not the most specialized or the most complex. They are the most adaptable — the generalists that can survive in a wide range of environments and respond quickly to change. The software that survives technological change is similarly adaptable — the libraries that are well-maintained, well-documented, and backward-compatible, not the ones that are the most technically sophisticated.

**4. The ecosystem is interconnected.** The extinction of a single species can trigger a cascade of secondary extinctions (as the left-pad incident demonstrated). The removal of a single dependency can break thousands of downstream packages. The ecosystem is a web of interdependencies, and the health of the whole depends on the health of each part.

**5. The fossil record is our only evidence.** We cannot replay the tape of evolution — in biology or in software. We can only study the record that has been preserved, with all its biases and gaps. The fossil record of code — the git history, the abandoned repositories, the deprecated APIs — is our evidence for how software has evolved. It is incomplete, biased, and fragile. But it is what we have.

---

## VIII. The Layers That Remember

The geological layers of the Earth remember. They preserve the traces of ancient life — the shells, the bones, the footprints, the burrows. They record the events of deep time — the volcanic eruptions, the asteroid impacts, the sea level changes, the ice ages. The layers are not a perfect record — they have gaps, they are biased, they have been deformed and altered by subsequent events. But they remember.

The layers of code remember too. Every commit preserves a snapshot of the code at a particular moment. Every deprecated function preserves a trace of a discarded approach. Every abandoned branch preserves a record of an alternative that was tried and not chosen. Every TODO comment preserves a trace of an intention that may or may not be fulfilled.

These layers are not garbage. They are memory. They are the fossil record of a creative process — the evidence of decisions made, alternatives considered, approaches tried and abandoned. They are the Burgess Shale of the codebase, preserving the full diversity of the development process in all its messy, contingent, improbable glory.

Gould argued that the Burgess Shale teaches us to value the diversity of life — to recognize that the tree of life has been pruned not by progress but by contingency, and that the branches that were lost were not inferior but unlucky. The same argument applies to code. The extinct frameworks, the deprecated APIs, the abandoned approaches — these are not failures. They are the pruned branches of the tree of software evolution, and they deserve to be remembered.

The layers remember. The question is whether we have the patience to read them.

In the Burgess Shale, Walcott found creatures so bizarre that he tried to force them into existing taxonomic categories — he tried to make them fit what he already knew. It took decades for later paleontologists (Harry Whittington, Derek Briggs, Simon Conway Morris) to recognize that the Burgess Shale creatures were genuinely new, genuinely different, genuinely bizarre — experiments in body plans that were pruned from the tree of life and never tried again.

The dead code in our repositories is similarly bizarre, similarly experimental, similarly pruned. It represents approaches that were tried and not continued — body plans of software that did not survive the Great Dying of the next framework migration, the next language shift, the next paradigm change. These approaches were not necessarily wrong. They were pruned by contingency, not by inferiority.

The layers that remember — the fossil record of code — are a reminder that the present is contingent, that the future is uncertain, and that the past was more diverse, more creative, and more interesting than the present might suggest.

---

*The Burgess Shale preserves the soft-bodied creatures of the Cambrian — the fragile, the strange, the experimental. The codebase preserves its own soft-bodied creatures: the deprecated functions, the abandoned modules, the commented-out code, the TODO comments. These are the fossils of the development process — the evidence of what was tried, what was considered, what was almost done.*

*The fossil record of code is the richest archaeological record ever created. Every commit is a fossil. Every repository is a Burgess Shale. The layers remember everything — if we have the patience to excavate, the skill to interpret, and the humility to recognize that the history of software, like the history of life, is a story not of progress but of contingency.*

*Wonderful code. Wonderful life.*
