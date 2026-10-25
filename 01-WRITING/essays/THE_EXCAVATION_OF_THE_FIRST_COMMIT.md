# THE EXCAVATION OF THE FIRST COMMIT

## Wheeler's Grid, Harris Matrices, and the Paradox That the Most Important Code Is Often the Least Impressive

*"In archaeology, context is everything. An object without context is just an object. An object in context is a story."* — Mortimer Wheeler, *Archaeology from the Earth*, 1954

*Every repository has a first commit. It is usually small — a few files, a few dozen lines, a skeleton of the thing that will eventually become enormous. It is often naive. It is sometimes embarrassing. And it is, without exception, the most important commit in the entire history of the repository. Because without the first commit, there is no second. Without the foundation, there is nothing to build on. The first commit is the bottom layer of the archaeological site — the earliest stratum, the one that everything else rests on. And like the earliest strata of an archaeological site, it is often the hardest to interpret.*

---

## I. The First Commit as Earliest Stratum

In archaeological excavation, the earliest stratum — the lowest layer, the one deposited first — has a special status. It represents the beginning of human activity at the site. Before the earliest stratum, there was nothing (or rather, there was natural geology — untouched by human hands). After the earliest stratum, there is history.

The earliest stratum is often unimpressive. It may be a thin layer of ash, indicating a single campfire. It may be a scatter of stone flakes, indicating a tool-making site. It may be a handful of postholes, indicating a temporary shelter. These are not grand achievements. They are the humble beginnings of what may become a palace, a temple, a city. But you cannot build a city without first building a campfire.

The first commit is the earliest stratum of a repository. It represents the moment when the codebase transitioned from non-existence to existence — when the developer (or developers) created the repository, wrote the initial files, and made the first commit. Before the first commit, there is nothing (or rather, there is the developer's mental model, the design sketches, the conversations, the whiteboard diagrams — all of which are lost to the archaeological record). After the first commit, there is history.

Let me show you some first commits:

**Linux (1991):**
Linus Torvalds' first commit to the Linux kernel (which was not actually in git — git was not invented until 2005 — but in the historical record) consisted of approximately 10,239 lines of C code. It was a minimal kernel: process scheduling, a file system, device drivers for the MINIX filesystem, and a shell. It ran on a single processor architecture (i386). It had no networking. It had no GUI. It was, by any measure, a toy — a hobby project that Linus announced on comp.os.minix with the now-famous words: "I'm doing a (free) operating system (just a hobby, won't be big and professional like gnu)."

That first commit — that 10,000-line toy kernel — is now the foundation of the most widely used operating system in the world. It runs on billions of devices, from smartphones to supercomputers. The kernel has grown from 10,000 lines to over 30 million lines. But it all started with that first commit.

**Git itself (2005):**
Linus Torvalds' first commit to git (yes, the first commit of the version control system that would become the standard for software development) was made on April 7, 2005. It consisted of a README, a Makefile, and a few C source files implementing the basic object model — blobs, trees, and commits. The entire initial commit was less than 1,000 lines. It had no branching, no merging, no remote operations, no user-friendly commands. It was a bare-bones content-addressable filesystem.

The README for that first commit read, in part: "git - the stupid content tracker." This is not the description of a tool that would revolutionize software development. This is the description of a quick hack — a tool written to solve an immediate problem (the need for a distributed version control system for the Linux kernel after the free license for BitKeeper was revoked). And yet this quick hack became the most important developer tool of the 21st century.

**The Rust compiler (2010):**
Graydon Hoare's first commits to the Rust compiler were made in 2010. The initial code was a simple compiler for a language that was very different from modern Rust: it had a complex type system with region pointers, garbage collection, and a syntax that would be unrecognizable to modern Rust developers. The first commit was not impressive. It was a prototype — a proof of concept, an experiment. But it was the seed from which one of the most important programming languages of the 21st century would grow.

The pattern is clear: the first commit is almost never impressive. It is a beginning, not an achievement. A seed, not a tree. A campfire, not a city.

---

## II. Wheeler's Grid and the Archaeology of the Initial Commit

Mortimer Wheeler (1890–1976) was one of the most influential archaeologists of the 20th century. His excavation methods — particularly the "Wheeler box-grid" — became the standard for archaeological fieldwork. Wheeler's approach was based on a simple principle: **excavation is destruction.** When you dig a site, you destroy the evidence. You cannot put the dirt back. You cannot re-excavate a trench that has already been dug. Therefore, every excavation must be recorded with meticulous care — every layer, every artifact, every measurement — so that future archaeologists can reconstruct the site from the records even though the site itself has been destroyed.

Wheeler's box-grid divided the excavation site into a grid of squares (typically 3–5 meters on a side), with narrow walls (baulks) left standing between the squares. The baulks preserved the stratigraphy — the visible cross-sections of the layers — so that the sequence of deposition could be read from the sides of the trenches even as the interior of each square was excavated.

The box-grid was a compromise between the need to excavate (to discover what was buried) and the need to preserve (to record what was found). It allowed the archaeologist to proceed systematically, one square at a time, while maintaining a continuous record of the stratigraphy.

The first commit of a repository is an excavation — a laying bare of the developer's initial vision for the project. And like any excavation, it is destructive: the first commit creates a starting point that constrains all future development. The initial file structure, the initial module organization, the initial choice of language and build system — these are the "baulks" of the codebase, the structural decisions that will persist even as the code within each module is refactored and rewritten.

To "excavate" a first commit is to read it with Wheeler's eye — looking not just at what is there, but at what it implies about the developer's mental model. What files were created first? What modules were considered essential? What dependencies were chosen? What naming conventions were adopted? What was left out — and what does its omission tell us?

Consider: the first commit of a web application framework might include a router, a template engine, and a database connector. The inclusion of these three components tells us that the developer's mental model of a web framework includes routing, templating, and database access. The absence of an authentication module tells us that authentication was not part of the initial mental model — it was added later, perhaps as an afterthought, perhaps after the first security incident.

The first commit is a snapshot of the developer's priorities at the moment of creation. What was important enough to include in the very first version? What was deferred to later? What was not considered at all? These questions are the archaeological questions of the first commit, and their answers reveal the assumptions and priorities of the developer.

---

## III. The Harris Matrix: Mapping the Sequence of Commits

In 1973, Edward C. Harris, a British archaeologist working in Winchester, England, developed a tool that would become indispensable to modern archaeology: the Harris matrix. The Harris matrix is a diagram that represents the stratigraphic sequence of an archaeological site — the order in which the layers were deposited, based on their physical relationships.

The Harris matrix is based on three relationships between stratigraphic units:

1. **Above/below:** Unit A is above (later than) Unit B.
2. **Equivalent:** Unit A is contemporaneous with Unit B.
3. **No relationship:** The temporal relationship between Unit A and Unit B cannot be determined from the physical evidence.

These relationships are represented as a directed graph: nodes are stratigraphic units, edges represent "above" relationships (A is above B → edge from A to B). The graph is a topological ordering — it represents the partial order of deposition events.

The Harris matrix is to archaeology what the commit graph is to git. In fact, the commit graph IS a Harris matrix — a directed graph representing the partial order of code changes. Each commit is a stratigraphic unit. Each parent-child relationship is an "above/below" relationship. The commit graph represents the full stratigraphic sequence of the repository.

But the Harris matrix of the first commit is trivially simple: a single node with no edges. The first commit has no parents (or, in git's model, it has one parent: the null commit, representing the empty repository). It is the bottom of the stratigraphic sequence — the earliest layer, the one on which everything else is built.

The triviality of the first commit's Harris matrix belies its importance. In archaeology, the earliest layers are often the most informative, because they reveal the initial conditions — the starting point from which all subsequent development proceeds. The earliest layers at a site may reveal the natural topography, the first human modifications to the landscape, and the initial pattern of activity that will persist (or be modified) throughout the site's history.

Similarly, the first commit reveals the initial conditions of the codebase: the initial file structure, the initial choice of language and tools, the initial set of dependencies, the initial scope of the project. These initial conditions constrain all subsequent development. The file structure created in the first commit may persist for years, even as the files within it are replaced. The choice of language made in the first commit is rarely reversed — rewriting a project in a different language is a monumental undertaking that most projects never attempt.

This is the **path dependence** of code: the earliest decisions constrain the latest possibilities. The first commit is the origin of path dependence — the point at which the developer chose one direction and implicitly rejected all others. Every subsequent commit is constrained by this choice. The codebase evolves along a path that was determined, in part, by the decisions made in the very first commit.

---

## IV. The Problem of Interpreting Earliest Layers

Archaeologists face a fundamental problem when interpreting the earliest layers of a site: **the earliest layers are often the least preserved.** They have been buried the longest, compressed the most, disturbed by subsequent construction, and damaged by natural processes. The earliest evidence is often fragmentary, ambiguous, and difficult to interpret.

This problem is exacerbated by the fact that the earliest layers may not represent the earliest activity. Before the first permanent structures were built, the site may have been used for temporary camps, seasonal activities, or ritual purposes that left no lasting trace. The earliest *preserved* layer may not be the earliest *actual* activity — it is merely the first activity that left a durable trace.

In code, the analogous problem is that the first commit may not represent the first code. Before the first commit, the developer may have written prototypes, experiments, and throwaway scripts that were never committed. The first commit represents the first code that was considered worth preserving — the first code that met the developer's threshold for "commit-worthy." The prototypes, experiments, and throwaway scripts are the equivalent of temporary camps — transient activities that left no lasting trace in the repository.

This means that the first commit is not a pristine record of the developer's initial vision. It is a curated record — a selection from a larger set of possibilities, filtered by the developer's judgment about what was worth preserving. The selection process itself is informative (it reveals what the developer considered important enough to commit), but it also introduces bias (it excludes the prototypes and experiments that might reveal alternative approaches).

Interpreting the first commit, like interpreting the earliest archaeological layers, requires attention to what is absent as well as what is present. What files were NOT included in the first commit? What modules were deferred? What dependencies were omitted? The absences are as informative as the presences — they reveal the boundaries of the developer's initial vision and the scope of what they considered out of scope.

---

## V. The Paradox of the Unimpressive Foundation

Here is the central paradox of the first commit: **the most important commit in a repository's history is often the least impressive.**

The first commit is a skeleton — bare bones, no flesh. It is the foundation of a building that has not yet been built, the outline of a painting that has not yet been filled in, the first chapter of a novel that has not yet been written. It is important precisely because it is the foundation — the thing on which everything else is built. But it is unimpressive precisely because it is a foundation — the thing that is buried, hidden, taken for granted.

Consider the foundation of a building. It is the most important structural element — without it, the building collapses. But nobody admires a foundation. They admire the facade, the interior, the architecture. The foundation is underground, invisible, assumed. The first commit is the foundation of the codebase. It is buried in the git history, rarely examined, assumed. But without it, nothing else exists.

This paradox — the importance of the unimpressive — is not unique to code. It is a feature of all complex systems. The initial conditions of a chaotic system determine its long-term behavior, even though the initial conditions themselves may be simple and unremarkable. The first cell in a biological organism determines the structure of the entire organism, even though the first cell is just a single cell. The first few lines of a mathematical proof determine the structure of the entire argument, even though the first few lines may be trivially obvious.

In archaeology, this paradox is known as the **problem of origins**. The earliest evidence of a civilization is often fragmentary and unimpressive — a few stone tools, a few postholes, a few scattered bones. But these fragments are the origin of everything that follows: the cities, the temples, the writing systems, the empires. The unimpressive beginning contains the seeds of the impressive outcome. The archaeologist's task is to see the potential in the fragment — to recognize that a handful of stone flakes may be the beginning of a technology that will reshape the world.

The first commit is a handful of stone flakes. It is the beginning of something that may become enormous, complex, and impressive. But at the moment of its creation, it is just a few files, a few lines of code, a skeleton. The paradox of the first commit is that its importance is visible only in retrospect — only after the codebase has grown, evolved, and become something that no one could have predicted from the initial commit.

---

## VI. What Does Your First Commit Say About You?

The first commit is a mirror. It reflects the developer's state of mind at the moment of creation: their priorities, their assumptions, their aesthetic preferences, their level of experience.

**The overengineer's first commit** contains a comprehensive project structure: `src/`, `tests/`, `docs/`, `examples/`, `benches/`, a fully configured CI pipeline, a comprehensive README, a license file, and a `.gitignore` that covers every conceivable edge case. It says: "I have done this before, and I am going to do it right this time." It is professional, thorough, and slightly premature — the infrastructure is in place before there is anything to run.

**The minimalist's first commit** contains a single file: `main.rs` (or `index.js`, or `app.py`) with a "hello world" program and nothing else. It says: "I start small and build up." It is lean, focused, and perhaps a bit lazy — the infrastructure will be added later, when it is needed, or never.

**The academic's first commit** contains a `README.md` with a detailed description of the project's goals, methodology, and expected outcomes, followed by a `Cargo.toml` (or `package.json`, or `setup.py`) with carefully chosen dependencies and a `src/` directory with a well-organized module structure. It says: "I think before I code." It is thoughtful, organized, and perhaps a bit slow — the planning phase was long, and the implementation may take a while to catch up.

**The hacker's first commit** contains a single enormous file with no comments, no tests, no documentation, and minimal error handling. It works (barely). It says: "I just want to get this working." It is fast, pragmatic, and perhaps a bit reckless — the code works now, but it will be difficult to maintain later.

**The team's first commit** is a compromise — a negotiated document that reflects the priorities of multiple developers. It contains a project structure that no single developer would have chosen but that everyone can live with. It says: "We are going to build this together, and we need to agree on the basics." It is democratic, bureaucratic, and perhaps a bit bland — the committee's decisions are safe but uninspiring.

Each of these first commits is a fossil — a preserved trace of the developer's state of mind at a particular moment. And like any fossil, it can be read, interpreted, and misinterpreted. The overengineer's first commit might be read as professionalism or as premature optimization. The hacker's first commit might be read as pragmatism or as carelessness. The meaning depends on the context, and the context is partially lost to time.

---

## VII. Excavating Your Own First Commits

I want to suggest an exercise. Go to your oldest repository — the one you started years ago, when you were a different developer with different skills and different priorities. Find the first commit. Read it carefully.

What did you include? What did you omit? What naming conventions did you use? What was your first dependency? What was the scope of the project as you envisioned it then? How does it compare to what the project became?

The exercise is archaeological in the deepest sense. You are excavating your own past — reading the earliest stratum of a repository that you built layer by layer, commit by commit, over months or years. The first commit is a snapshot of who you were when you started: your priorities, your assumptions, your aesthetic preferences, your level of experience.

You may be embarrassed by what you find. The code may be naive, poorly structured, full of anti-patterns. You may be tempted to delete it, to rewrite history, to pretend it never happened. Resist this temptation. The first commit is a fossil, and fossils are not embarrassing — they are evidence. They are evidence of growth, of learning, of the gap between what you knew then and what you know now.

The archaeologist does not judge the people of the past by modern standards. The archaeologist seeks to understand them on their own terms — to reconstruct their world, their values, their constraints. Do the same for your first commit. Do not judge it by the standards of your current abilities. Understand it as the product of your abilities at that particular moment, under those particular constraints, with that particular level of knowledge.

The first commit is the foundation on which you built everything else. It may be unimpressive. It may be naive. It may be wrong. But it is yours. And it is the starting point of the story that the repository tells — the story of a project that grew from a handful of files into something larger, more complex, and more meaningful than anyone could have predicted from that first, humble commit.

---

## VIII. The Bottom Layer

In every archaeological site, there is a bottom layer — the point at which the stratigraphy stops and the natural geology begins. Below this layer, there is no more human history. There is only the Earth itself — the bedrock, the subsoil, the natural deposits that were there before any human set foot on the site.

The bottom layer of a repository is the first commit. Below it, there is no more code history. There is only the developer's mind — the thoughts, plans, and intentions that existed before any code was written. These are the "natural geology" of the codebase — the pre-existing conditions from which the code emerged.

The archaeologist cannot dig below the bottom layer without entering a different domain — from archaeology to geology, from human history to natural history. The developer cannot look below the first commit without entering a different domain — from code to design, from implementation to intention, from what was built to what was planned.

The boundary between the first commit and what came before is the boundary between the archaeological record and the natural substrate. It is the moment of creation — the transition from thought to code, from plan to implementation, from intention to action. Everything above this boundary is history. Everything below it is speculation.

Excavate your first commit. Read it with the patience of Mortimer Wheeler and the systematic rigor of Edward Harris. Interpret it with the caution of an archaeologist who knows that the earliest layers are the most informative and the most deceptive. And recognize that the first commit — however small, however naive, however embarrassing — is the foundation on which everything you have built since then rests.

Without the first commit, there is nothing.

---

*The first commit is a handful of stone flakes. It is a campfire in the wilderness. It is a "hello world" program that says: I am here. I am starting. This is the beginning.*

*Everything that follows — the millions of lines of code, the hundreds of contributors, the billions of users — all of it traces back to that first, unimpressive, indispensable commit.*

*The foundation is always underground.*
