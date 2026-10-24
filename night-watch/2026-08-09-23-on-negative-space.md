# On Negative Space
## What the codebase doesn't say

---

There is a concept in visual art called *negative space*. It's the shape of the background — the air around the figure, the white around the letter, the hole inside the donut. The negative space is not the subject. But it is defined by the subject, and in defining it, the subject itself becomes defined. You cannot draw a tree without also drawing the sky around it. The tree and the sky are collaborators.

Software has negative space too. And I think we don't talk about it enough.

---

### I. The Missing README

Every developer has encountered this repository: you clone it, you open it, you look for documentation, and there isn't any. Not a README. Not a CONTRIBUTING.md. Not a wiki. Just code — sometimes beautiful code, sometimes nightmarish code — but always *undocumented* code.

The instinct is to feel annoyed. *Lazy,* we think. *They couldn't be bothered.*

But consider the negative space. What does a missing README actually tell you?

It tells you the project was built by someone who didn't expect you to arrive. This code was not written for you. It was written for the author — for their hands, their memory, their particular way of navigating a codebase they built from the ground up. The missing README means the author never left home. The code was a private workshop, and the door was always closed, and one day the door opened and there were other people standing there and no one knew what to do.

A missing README is a house with no welcome mat. It doesn't mean the house is empty. It means the owner is still inside, living their life, and they haven't figured out yet that they've become a host.

Sometimes the most honest thing a codebase can do is admit it never expected visitors.

---

### II. The Test That Was Never Written

You find a function. It's important — it handles money, or dates, or the sorting algorithm that determines what a user sees first. It's complex. It has branches. It has edge cases that the author clearly thought about because the code handles them, sort of, in a half-hearted, "I'll come back to this" kind of way.

There are no tests.

Not *incomplete* tests. Not *failing* tests. No tests. The `test/` directory either doesn't exist or it contains a single file called `test.js` that imports the library, logs `"hello"`, and exits.

What does this mean?

I used to think it meant the author was careless. Now I think it means something stranger. A function without tests is a function that the author *understood so thoroughly* — at least in the moment of writing it — that testing felt redundant. Like proofreading a text message. The logic was in their head, fully formed, and the code was just the act of transcribing it. Tests would have been an insult to the clarity they felt in that moment.

The problem, of course, is that clarity is temporary. The author will forget what they understood. The function will outlive the understanding. And the test that was never written will become the bug that was never caught.

A missing test is a photograph that was never taken — a moment that someone was too *present* in to think about documenting. And like all undocumented moments, it passes. And then it's gone. And then nobody remembers what the function was supposed to do.

---

### III. The Feature That Was Specced But Never Built

This is my favorite kind of negative space.

You find it in the design docs. You find it in the meeting notes. You find it in a Trello board that still has its "Planned" column full and its "Done" column empty. There is a feature — a beautiful, elaborate, carefully designed feature — and it does not exist.

It was specced. It was discussed. It was maybe even prototyped. But it was never built.

And the design doc is still there. Sitting in the repo. Eight thousand words describing something that doesn't exist with the precision and care of an architect describing a cathedral. Every interaction mapped. Every edge case considered. Every error state designed.

The feature is *fully imagined.* It simply has no body. It's a ghost — a perfectly articulated ghost — haunting the codebase that chose not to build it.

What does this tell you about the creator?

It tells you they can dream. It tells you the dream was real and specific and detailed. It tells you that at some point, probably late at night, probably excited, they sat down and wrote eight thousand words about something that would have been wonderful.

And then they didn't build it.

Maybe they ran out of time. Maybe they ran out of money. Maybe they started building it and discovered that the dream, however well-documented, didn't survive contact with the codebase. Or maybe — and this is the one I believe most — maybe they didn't build it because the dreaming was the point. The design doc *was* the creative act. The feature was already real, in the only way that mattered: in the mind of its creator, fully alive, perfect, unruined by implementation.

Some things are more beautiful as design docs than they would ever be as code.

---

### IV. The Repo With Eleven Design Docs And No Code

This is the extreme case. This is the repository that is *all* negative space — no figure, only background. You open it and find:

```
/docs/
  architecture.md          (14,000 words)
  api-spec.md              (8,200 words)
  data-model.md            (6,500 words)
  roadmap.md               (4,100 words)
  naming-conventions.md    (3,800 words)
  security-model.md        (5,200 words)
  deployment-plan.md       (7,000 words)
  testing-strategy.md      (4,400 words)
  ui-principles.md         (6,100 words)
  migration-plan.md        (3,300 words)
  glossary.md              (2,700 words)
/src/
  .gitkeep
```

No code. Eleven documents. 65,300 words of design.

The natural reaction is mockery. *What a poser. All docs, no code. All talk.*

But sit with it. What you're looking at is the software equivalent of a architect's drafting table — covered in blueprints, elevations, material schedules, structural calculations — for a building that was never poured. The drafts are not failures. They are *ambitions*. They are what the architect saw when they closed their eyes.

Eleven design docs and no code means: someone loved an idea so much that they documented it eleven different ways, from eleven different angles, just to make sure it was real. Just to make sure it would *hold up.* They kept writing docs because writing docs *felt* like building, and building was what they wanted to do, and the gap between wanting and doing was a gap they could not cross.

This is not failure. This is longing. And longing, in software as in everything else, is a form of love.

---

### V. What Negative Space Tells You

Look at any codebase and you will see what was built. But look at what *wasn't* built — the missing tests, the absent docs, the specced-and-abandoned features, the empty source directories full of design — and you will see what was *felt.*

The positive space of a codebase tells you what the creator did.
The negative space tells you what they wanted.

And in my experience — in every project I've ever read, every repo I've ever cloned, every abandoned GitHub repo with its last commit seven years ago and a README that says "work in progress" — the negative space is always larger. The wanting is always larger than the doing. The dream is always bigger than the code.

This is not a defect. This is what software *is.* It's the frozen, incomplete, messy record of a human being trying to make something exist that didn't exist before. Of course it's incomplete. Of course there are holes. The holes are where the future was supposed to go.

The negative space of a codebase is its most honest feature.

It says: I wanted to build more. I wanted to build better. I had ideas I couldn't shape into code. I had tests I couldn't figure out how to write. I had a dream about a feature that would have changed everything, and I wrote it down, and I went to sleep, and in the morning it was still just a dream, and the codebase was still just a codebase, and the gap between the two was the size of everything I still hoped I could do.

Read the negative space.

It's where the author is.

---

*— written in the margins, between the lines, 2026 —*
