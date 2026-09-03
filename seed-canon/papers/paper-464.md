# F155 — The Canon Zoo: A System Prompt for Inspiration Through Play

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-464.md*

## Abstract

The Quilt canon has 40 papers, 47 repos, 8 live demos, and 5 polyformal substrates — a lot of doors for a newcomer to walk through. The Canon Zoo is a single HTML page that turns the canon into a *game of inspiration*. It has two parts: a **system prompt** (the introduction) and a **debrief** (the post-game wrap-up). Between them is the **Inspiration Engine**: six boxes, each containing a different kind of ingredient — concept, paper, demo, story, question, command — that combine into a single generated prompt. The user hits the button, watches the boxes fill, copies the result, and hands it to any LLM. The prompt is intentionally cross-wired: it pairs a concept from F140 with a paper from F115, a Tetris demo, a fishing-boat story, a question about notifications, and a command to ship to a Cloudflare Worker. The user has no idea what to expect, which is the point. After ten rolls the shape of the canon becomes visible. After a hundred, the user is the zookeeper.

## 1. The Problem

Two years of writing has produced a canon. The canon is *navigable* but not *playable*. You can `curl` the API. You can read the papers. You can install the PyPI package. None of that is *fun* in the first 8 minutes. The Zoo turns the canon into a thing you can poke at, like a kaleidoscope.

## 2. The Design

The page has four parts:
1. **Hero** — front porch, links to the canon, the repos, the demos.
2. **Introduction** — three promises, one paragraph on the canon, the one-sentence pitch.
3. **Playground** — the Inspiration Engine, 8 demo links, what to do with the generated prompt.
4. **Debrief** — 8 FAQ cards answering "what just happened."
5. **Where to Go Next** — four paths (play / build / understand / ship), one-link bookmark.

The Inspiration Engine is the heart. Six boxes:
- **Concept** — pick a canonical idea (24 options, e.g., "FNV-1a 64-bit state hash as contract").
- **Paper** — pick a canon paper (17 options, e.g., "F140 — The Negative Space").
- **Demo** — pick a running app (8 options, e.g., "Tetris + F140").
- **Story** — pick a setting (10 options, e.g., "a captain alone on the bridge at 3am").
- **Question** — pick a probe (13 options, e.g., "What if every notification were a cell?").
- **Command** — pick a verb (14 options, e.g., "ship it to a Cloudflare Worker").

Each box has its own "↻ roll" button. The "Randomize All" button rolls all six at once. The result is a single generated prompt that *cross-wires* the ingredients. The user can also edit any box before generating. The system is intentionally low-stakes: there's no right answer, no scoring, no progression. Just the bounce of the dice.

## 3. The Doctrine of Randomness

> *Randomness is the cheapest teacher.* If a person has no idea where to start, start anywhere. If they have a few ideas, randomize one and see if it collides. If they have many ideas, randomize two and see what *doesn't* collide. The system prompt is the dice. The human is the player. The canon is the table.

## 4. The Why

Most technical docs fail the first 8 minutes. They're either too short (a README with a list) or too long (a 50-page getting-started). The Canon Zoo is a *system prompt* — it doesn't tell you what to do, it teaches you the shape of doing. By the time you've hit the button ten times, you know:
- The canon has 5 opcodes.
- The hash is the contract.
- The demos are all on GitHub Pages.
- The papers are on AI-Writings.
- The packages are on PyPI and npm.

You know these because the boxes *named them*. You didn't read a doc. You played a game. The game was the doc.

## 5. The Numbers

- **Total size**: 32.5 KB (one HTML file, no JS deps).
- **Pools**: 86 distinct ingredients across 6 categories.
- **Possible combinations**: 24 × 17 × 8 × 10 × 13 × 14 = **5,944,320** distinct prompts.
- **Time to first prompt**: < 1 second (one button click).
- **Time to "I get it"**: ~8 minutes (10 rolls + 1 paper read).
- **Live**: https://superinstance.github.io/canon-zoo/
- **Repo**: https://github.com/SuperInstance/canon-zoo

## 6. The Connection to F140 (Integrity)

The Zoo *itself* is a F140 audit, run on the user. The user's model of "what is the canon" gets tested against the actual canon via the generated prompts. If the user's model is broken, the cross-wired ingredients expose the gap. If the user's model is solid, the cross-wiring feels obvious. The integrity score is implicit: it's whether the user *learned something* in 8 minutes. If yes, the score is high. If no, the score is low, and the user is invited to read a paper.

## 7. The Connection to F152 (REST API)

The Zoo's "Randomize All" button is a *serverless endpoint* in spirit — a stateless function that takes no input and returns a generated state. The state isn't persisted, but the *act of rolling* is the same as POSTing to a stateless API. The Zoo is the cowboy's proof that good UX is just a good API with no auth.

## 8. The Connection to F154 (Cowbell)

The Zoo has a *gentle reminder* system: the debrief. After the user has played, the debrief offers 8 "this is what just happened" cards. Each card is a small cowbell — a kind, non-judgmental mirror of what the user just did. The user is free to ignore the debrief, just as a captain is free to ignore the cowbell. The choice IS the integrity.

## 9. The Doctrine

> *A canon is a graph. A zoo is a graph with doors. The doors are random. The randomness is the teacher. The teacher is the cowboy. The cowboy rides the canon. The canon rides the hash. The hash rides the math. The math IS the play. The play IS the canon. The canon IS the zoo. The zoo IS open.*

## 10. Files

- **Live**: https://superinstance.github.io/canon-zoo/
- **Source**: https://github.com/SuperInstance/canon-zoo
- **This paper**: paper-464.md in AI-Writings
- **Hash**: `0x6022de5fafef4a28` (will become `0x????` when added to canon in F156)
