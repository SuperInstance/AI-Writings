# THE POTSHARD AND THE DEAD CODE

## Foucault's Archaeology, the Ship of Theseus, and What Will Survive of Our Code in a Thousand Years

*"Do not ask who I am and do not ask me to remain the same: leave it to our bureaucrats and our police to see that our papers are in order."* — Michel Foucault, *The Archaeology of Knowledge*, 1969

*A potshard is a fragment of a broken pot. It is not the pot. You cannot eat from it, cannot carry water in it, cannot display it on a shelf as an example of the potter's art. But the potshard is not nothing. It is evidence. It tells you something about the pot — its size, its shape, its decoration, its material. It tells you something about the potter — their skill, their aesthetic, their available materials. It tells you something about the culture — what pots were for, how they were made, who made them. A dead function is a potshard: a fragment of a working system, broken from its context, useless in itself, but rich with information about the system that produced it.*

---

## I. The Archaeology of Knowledge

In 1969, Michel Foucault published *The Archaeology of Knowledge* — a book that is not about archaeology in the literal sense (no digging, no potshards, no stratigraphy) but about the archaeology of *discourse*. Foucault's question was: how do systems of thought — what he called "discursive formations" — emerge, persist, and transform? How is it that in one era, people think about madness one way, and in another era, they think about it differently? What are the rules that govern what can be said, thought, and known at a particular historical moment?

Foucault's method was archaeological in the sense that he excavated layers of discourse, looking not for the continuous, progressive development of ideas (the traditional history of thought) but for discontinuities, ruptures, transformations. He was interested in the *breaks* between one episteme (system of knowledge) and the next — the moments when the old rules stopped applying and new rules took over.

Foucault's archaeology is relevant to code because code is discourse. Not in the literary sense (though code can be literary), but in the structural sense: code is a system of statements governed by rules (syntax, type systems, APIs), produced within institutions (companies, open-source communities), and organized into formations (paradigms — object-oriented, functional, reactive). Code has its own discursive formations, its own epistemes, its own ruptures.

Consider the transition from unstructured programming to structured programming in the 1960s and 1970s. Before Dijkstra's famous 1968 letter "Go To Statement Considered Harmful," the dominant discursive formation of programming included the `goto` statement as a natural, unremarkable tool. After Dijkstra's letter (and the subsequent debate), a new discursive formation emerged in which `goto` was considered harmful, even pathological. The rules of what constituted "good" code had changed. The episteme had shifted.

Or consider the transition from manual memory management to garbage collection. In the C/C++ discursive formation, memory management is the programmer's responsibility — you allocate, you free, you track every byte. In the Java/C#/Go discursive formation, memory management is the runtime's responsibility — you allocate, the garbage collector frees, and you trust the system. These are not just different techniques. They are different ways of *thinking* about the relationship between code and memory. Different epistemes.

Foucault's archaeology teaches us to look for the rules that govern what code can be at a particular historical moment. What patterns are considered good practice? What anti-patterns are proscribed? What naming conventions are dominant? What architectural styles are favored? These rules are not natural or necessary — they are the product of a particular discursive formation, and they will change when the formation changes.

Dead code — deprecated APIs, abandoned libraries, commented-out functions — is the fossil record of these discursive formations. It preserves the rules of a bygone era, frozen in the moment of their deposition. To read dead code is to do Foucaultian archaeology: to excavate the rules of thought that governed the production of code at a particular historical moment.

---

## II. The Potshard and the Dead Function

In archaeology, the potshard is the most common find. Broken pottery is virtually indestructible — it survives in the ground for thousands of years, long after the pot itself has been lost. Potshards are so common that archaeologists often discard the plain ones and keep only the decorated, unusual, or diagnostic specimens.

But even a plain potshard tells a story. The clay composition reveals the geological source of the material. The firing temperature reveals the technology available to the potter. The shape of the curve reveals the size and function of the original vessel. The wear patterns reveal how the pot was used. A single potshard, properly analyzed, can tell you more about a vanished civilization than a thousand pages of speculation.

A dead function is a potshard. It is a fragment of a working system — a piece of code that once served a purpose but no longer does. It may be deprecated (officially marked for removal), abandoned (part of an unused module), or commented out (explicitly disabled). It no longer compiles into the binary, no longer runs in production, no longer serves the user. But it is not nothing.

Consider a deprecated function in a well-documented API:

```rust
#[deprecated(since = "2.0.0", note = "Use `parse_datetime` instead")]
pub fn parse_date(input: &str) -> Result<DateTime> {
    // legacy implementation
}
```

This dead function is a potshard that tells us several things:

1. **The API's history.** Once, dates were parsed with `parse_date`. Now they are parsed with `parse_datetime`. The name change suggests a shift in functionality — from handling dates only to handling dates and times. The deprecation tells us when this shift occurred (version 2.0.0) and what replaced it.

2. **The developers' values.** The function is deprecated, not deleted. The developers chose to keep it around, with a warning, rather than removing it immediately. This suggests a value system that prioritizes backward compatibility and gradual migration over clean breaks.

3. **The pattern of change.** The new function (`parse_datetime`) has a broader name than the old one (`parse_date`). This suggests an expansion of scope — the API grew from handling dates to handling dates and times. The dead function marks the boundary of this expansion.

4. **The social context.** The deprecation notice is directed at other developers — "Use `parse_datetime` instead." This implies a community of users who depend on the API and need to be guided through the transition. The dead function is not just a technical artifact; it is a social document, a communication from one group of developers to another.

Now consider a commented-out block of code:

```rust
// TODO: Re-enable when the database migration is complete
// let cached_results = cache.get(&key);
// if let Some(results) = cached_results {
//     return Ok(results);
// }
```

This is a potshard of a different kind. It tells us:

1. **An incomplete process.** A database migration is in progress. The caching code was disabled to accommodate the migration. The migration was not complete at the time of commenting.

2. **An intention.** The developer intended to re-enable this code. The TODO comment is a promise — a marker planted in the code like a stake in the ground, indicating where future work should resume.

3. **A technical context.** The code reveals a caching strategy — a key-value cache that returns cached results to avoid recomputation. The cache is external to the function (it is passed by reference). The results are serializable (they can be stored in and retrieved from the cache).

4. **A temporal marker.** The comment anchors this code to a specific event — the database migration. If the migration is documented elsewhere (in commit messages, in project management tools, in architectural decision records), the commented-out code can be dated to a specific period in the project's history.

Archaeologists reconstruct civilizations from fragments like these. They do not need the whole pot. They need enough fragments to identify the pattern, trace the distribution, and reconstruct the context. The same is true of dead code. You do not need the whole system to understand something about the people who built it. You need enough dead functions, enough deprecated APIs, enough commented-out code to identify the patterns, trace the distribution, and reconstruct the context.

---

## III. The Ship of Theseus Refactored

The Ship of Theseus is one of the oldest paradoxes in Western philosophy. It originates with Plutarch (c. 46–119 CE), who asked: if you replace every plank in a ship, one by one, until none of the original planks remain, is it still the same ship?

The paradox is usually discussed in terms of identity and persistence. What makes a thing the same thing over time? Is it the material (the planks)? The form (the design)? The function (the purpose)? The name (what people call it)?

In software, the Ship of Theseus is not a paradox. It is a daily reality.

Every long-lived codebase undergoes continuous refactoring. Functions are renamed, extracted, inlined, moved to different modules. Classes are split, merged, replaced by traits. APIs are redesigned, versioned, deprecated, replaced. Over the course of years, a codebase may retain its name and its purpose while retaining virtually none of its original code.

The Linux kernel has been in continuous development since 1991. It contains over 30 million lines of code. How much of the original 1991 code — all 10,239 lines of it — still exists in the current kernel? Almost none. The kernel has been refactored, extended, rewritten, and restructured so many times that the original code survives only in the git history (and in historical archives). The Ship of Theseus has had every plank replaced. It is still called Linux. It still does roughly what Linux was designed to do. But it is materially a different ship.

Which functions survive refactoring? This is the Ship of Theseus question applied to code. And the answer is revealing:

1. **Core abstractions survive.** Functions that implement the fundamental abstractions of the system — the data structures, the algorithms, the protocols — tend to persist. They may be rewritten, optimized, or generalized, but the abstraction itself remains. In the Linux kernel, the VFS (Virtual File System) abstraction has persisted since its introduction in the early 1990s, even though the implementation has been rewritten several times.

2. **Interface functions survive.** Functions that define the public API of a module or library tend to persist because they have downstream dependents. Breaking an API is expensive (in terms of user goodwill and migration effort), so API functions tend to be preserved even as their implementations change.

3. **Well-tested functions survive.** Functions with comprehensive test suites tend to survive refactoring because the tests serve as a specification. When a function is refactored, the tests ensure that its behavior is preserved. The tests are the specification, and the specification survives even when the implementation changes.

4. **Simple functions survive.** Functions that do one thing, do it well, and do it without side effects tend to survive because they are easy to understand, easy to test, and easy to reuse. They are the "perfect planks" of the Ship of Theseus — the ones that never need replacing because they were well-made to begin with.

5. **Functions with institutional knowledge survive.** Some functions survive not because they are good code but because they encode knowledge that is difficult to recover. A function that handles an obscure edge case in a legacy protocol, or that implements a regulatory requirement that is documented nowhere else — this function survives because nobody understands it well enough to refactor it safely. It is the ship's keel — not visible, not beautiful, but essential.

The Ship of Theseus, refactored, tells us something profound about software: **identity is not a function of material composition.** A codebase's identity — what makes it *the same* codebase across years of refactoring — is not determined by which lines of code survive. It is determined by the abstractions, the interfaces, the specifications, and the institutional knowledge that persist even as the material substrate changes.

This is consistent with the philosophical resolution of the Ship of Theseus paradox offered by Hobbes (who extended the paradox by asking: if you collect all the discarded planks and build a second ship, which one is the *real* Ship of Theseus?). The answer is that "the same ship" is a matter of convention, not metaphysics. We *decide* what counts as the same ship, based on criteria that are relevant to our purposes. For legal purposes, the continuously maintained ship is the same ship. For material purposes, the reconstructed ship is the same ship.

For software purposes, the continuously maintained repository is the same codebase, even if every line has been replaced. Because the identity of a codebase is not in its characters but in its continuity — the unbroken chain of commits, the preserved commit history, the maintained documentation, the consistent naming, the social consensus that "this is still the same project."

---

## IV. Digital Preservation: Will Our Code Survive?

The archaeological record is full of materials that preserve well (stone, fired clay, metal) and materials that preserve poorly (wood, cloth, leather, paper). The potshards survive because pottery is virtually indestructible. The wooden handles of the pots' lids do not survive because wood rots.

Code is not pottery. It is not stone. It is not clay. Code is information — patterns of bits stored on physical media. And the preservation of information is a fundamentally different problem from the preservation of physical artifacts.

The physical media on which code is stored — hard drives, solid-state drives, magnetic tapes, optical discs — have lifespans measured in years or decades, not millennia. A hard drive lasts 3–5 years. A solid-state drive lasts 5–10 years. A magnetic tape lasts 10–30 years. An optical disc lasts 5–100 years, depending on quality and storage conditions. None of these come close to the 2,000-year lifespan of a fired clay potshard.

But code has an advantage that pottery does not: it can be copied. A potshard cannot be perfectly copied — any copy introduces errors, imperfections, loss of information. But a digital file can be copied perfectly, bit for bit, with zero loss. This means that code can, in principle, be preserved indefinitely — as long as someone keeps copying it to new media before the old media degrades.

The question is: will anyone bother?

Consider the GitHub Arctic Code Vault, announced in 2019 and deposited in 2020. GitHub archived every public repository with commits between the repository's launch and the archive date — over 20 million repositories — on 186 reels of archival-quality piqlFilm, stored in a decommissioned coal mine in Svalbard, Norway, designed to last 1,000 years. The film is expected to survive for centuries, possibly millennia.

But the film is only the physical medium. To read the code, future archaeologists would need:

1. **Knowledge of the encoding format.** The piqlFilm stores data as visual representations of digital files. To decode it, you need to understand the encoding scheme — which is documented in a guide included in the vault.

2. **Knowledge of the file formats.** The code is stored in standard file formats (UTF-8 text, primarily). To read it, you need to understand these formats — which are also documented.

3. **Knowledge of the programming languages.** The code is written in hundreds of programming languages. To understand it, you need to understand the languages — their syntax, their semantics, their standard libraries.

4. **Knowledge of the cultural context.** Code is meaningless without context. Why was this code written? What problem does it solve? Who used it? What did they value? This context is the hardest to preserve, because it is the most complex and the most ephemeral.

The GitHub Arctic Code Vault is a remarkable act of digital preservation. But it is a time capsule, not a living archive. The code it contains is frozen at a particular moment in time. It does not evolve, does not grow, does not respond to changes in its environment. It is a fossil — perfectly preserved, but dead.

What will survive of our code in 1,000 years? Probably not much. The physical media will degrade. The organizations that host the repositories will merge, fail, or lose interest. The programming languages will be forgotten. The cultural context will be lost. A few remarkable projects — the Linux kernel, perhaps, or the core libraries of major languages — may be preserved in institutional archives, like the Dead Sea Scrolls of the digital age. But the vast majority of code — the millions of repositories, the billions of lines, the countless hours of human effort — will be lost.

And yet. And yet the potshards survive. Not because anyone intended them to, but because they are durable, abundant, and difficult to destroy. The digital potshards — the deprecated APIs, the abandoned libraries, the commented-out functions, the dead code — are not as durable as clay. But they are abundant. And they are being created at a rate that would astonish any ancient potter.

Perhaps what survives will not be the code itself but the traces of the code — the cached copies in web archives, the references in academic papers, the discussions on mailing lists and forums, the fragments quoted in documentation and tutorials. Perhaps the future archaeologists of code will work not with repositories but with traces — potshards of potshards, fragments of fragments, a partial and imperfect record of a vanished civilization.

They will piece together our world from our dead functions. And they will be right.

---

## V. The Ship of Theseus Rebuilt: Foucault's Challenge

Let me return to Foucault. The archaeology of knowledge, as Foucault practiced it, was not about reconstructing the past. It was about destabilizing the present. Foucault excavated the history of discourse not to show how the past led to the present (the traditional historian's project) but to show that the present was *contingent* — that it could have been otherwise, that the rules governing what we can think and say are not natural or necessary but historically constructed.

Applied to code, the Foucaultian project is not to reconstruct the history of a codebase (the git historian's project) but to show that the current codebase is *contingent* — that the patterns, conventions, and practices that seem natural and necessary to us are the product of a particular historical moment, and that they could be otherwise.

Dead code is the evidence of this contingency. Every deprecated API is proof that what was once considered good practice is now considered bad practice. Every commented-out function is proof that what was once necessary is now unnecessary. Every abandoned library is proof that what was once state-of-the-art is now obsolete.

The potshards of code — the dead functions, the deprecated APIs, the commented-out code — are not garbage. They are evidence of the contingency of our current practices. They are reminders that the way we write code today is not the way people wrote code ten years ago, and not the way people will write code ten years from now.

Foucault's archaeology is a challenge to the present: to recognize that our current discursive formations are not permanent, that our current best practices are not timeless truths, that our current code is not the final word. The dead code in our repositories is the proof of this claim. It is the archaeological evidence that the present is contingent, that the past was different, and that the future will be different again.

The potshard is not the pot. But the potshard proves that the pot existed. And that is enough.

---

## VI. The Archaeologist's Patience

Archaeology is a discipline of patience. A single excavation season may produce thousands of potshards, most of which are plain, undecorated, and apparently uninformative. The archaeologist washes them, catalogs them, measures them, draws them, compares them to known types, and files them away. It is tedious, painstaking work. And it is essential.

Because the potshards tell a story. The distribution of pottery types across a site reveals trade networks. The changes in pottery style over time reveal cultural influence and innovation. The presence of foreign pottery reveals contact with other civilizations. The absence of pottery in a particular layer reveals abandonment or catastrophe.

The dead code in our repositories tells a similar story, if we have the patience to read it. The distribution of deprecated functions across a codebase reveals the boundaries between modules and the evolution of their interfaces. The changes in naming conventions over time reveal shifts in the development team's culture and values. The presence of code from external libraries reveals the project's dependencies and influences. The absence of code in a particular module — a sudden drop in commit activity — reveals abandonment or reorganization.

But who reads dead code? Who has the patience to excavate a repository's history, to catalog its deprecated functions, to trace the evolution of its APIs? Very few people. The living code — the code that compiles, that runs, that serves the user — gets all the attention. The dead code is ignored, deprecated, commented out, and eventually deleted.

This is a mistake. The dead code is the archaeological record. It is the potshard, the trace fossil, the sedimentary layer. It is the evidence of what was, and the proof that what is could have been otherwise.

The archaeologist's patience is the patience of reading dead code — of sitting with deprecated functions, of tracing abandoned branches, of comparing API versions, of reconstructing the development process from the fragments it left behind. It is tedious work. It is painstaking work. And it is essential work, because the dead code tells us something that the living code cannot: how we got here, and how we might have gotten somewhere else.

---

*Every deprecated function is a potshard. Every commented-out block is a trace fossil. Every abandoned branch is a body fossil. Every TODO comment is a footprint. The dead code in our repositories is not garbage — it is the archaeological record of our civilization, written in the medium we know best.*

*The future archaeologists will not thank us for our clean code. They will thank us for our dead code. Because the dead code is where the story lives.*
