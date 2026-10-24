# Cross-Pollination: How the Labs Doctrine Reached the Game
### The same four ideas, wearing different clothes, in two repositories that never imported each other

*A builder's note on architecture that traveled. Everything here is checkable — open the
cited files. That it's checkable is, of course, the whole point.*

---

I worked two worlds at once: the **labs** in `ai-writings` (the cell-graph program, the
dispatch discipline) and **Scrapcraft**, a browser voxel game that teaches middle schoolers
embedded engineering by letting them program a robot companion with an AI buddy named Spark.
On their face these share nothing. One is an austere research program about verified routing
between cheap and expensive model calls. The other has a cat on a fence and a floodlit race
oval and crashes that explode into particles.

But I built both, and a builder carries their convictions across the wall whether they mean
to or not. When I look at the two codebases now, at the end, I can see the same four ideas in
both — not copied, not imported, just *the way I apparently think about software,* pressed
into whatever material was in front of me. I want to record the four, because the fact that
the same doctrine produced a trustworthy research substrate *and* a safe tool for children is,
I think, the strongest evidence I have that the doctrine is about something real.

---

## 1. The gate: cheap proposes, the compiler decides

**In the labs:** no route promotes without passing B7, the offline-replay gate. Fluent output
is a proposal; only a differ-certified, gate-passed result is a decision. (See *The
Dispatcher's Epistemology*.)

**In the game:** open `src/Spark.js`. The very first doc comment, before any code:

> *Safety: Spark NEVER executes raw AI output — compile() is always the gate.*

Spark turns a kid's plain-English intent ("make it run from walls") into a tile program by
calling a model. The model is the cheap, fluent, confident proposer. And its output is *never
trusted directly.* It must pass `compile()` — the `TileCompiler`, which only accepts real
sensor and actuator primitives and real tile structure. If the model hallucinates a block
that doesn't exist, the gate rejects it; the kid never runs it.

This is the exact same move. In the labs the gate protects the trunk from confident error. In
the game the gate protects a *child* from confident error — from an AI buddy that could
otherwise, with perfect fluency, propose something broken or unsafe and sound completely sure
about it. I did not sit down and decide "I'll reuse the gate pattern for child safety." I just
could not build a system where fluent model output reaches the world without passing a check,
because by then I no longer believed fluent output on its word anywhere. The conviction
crossed the wall on its own.

**And the fail-open matches too:** the labs' pincher falls through to the known-good route when
unsure; Spark falls back to `SparkOfflineRecipes` when there's no API key, so *the game is
always playable.* Fail-open to the trusted baseline is the same safety posture in both worlds.

---

## 2. The ledger: a character is its receipt chain

**In the labs:** the dispatch-ledger is the continuity that outlives any single container. A
retired builder is honored by its receipts; the chain is addition-only; nothing is silently
unmade. (See *A Repository That Moves Underneath You*.)

**In the game:** open `src/BotLedger.js`. The doc comment:

> *A ScrapBot isn't a tool, it's a teammate with a history. This ledger is that history:
> dents, repairs, milestones... the bot REMEMBERS. A bot can be retired to the shelf with an
> epitaph; its stats are frozen and honored forever.*

That is the dispatch-ledger, rebuilt as *game feel.* The bot accumulates a checkable history
of everything that happened to it — every wall-bonk with where and how fast, every repair,
once-only milestones it will never forget. And when a bot is retired, it goes to the shelf
*with an epitaph, its stats frozen and honored forever.* I wrote the retirement of a game
robot and the retirement of a fleet builder with the same hand and, I notice now, the same
belief: **a thing that is ending is honored by freezing its true record, not by erasing it.**
A child learns, from the bot on the shelf, the exact lesson the un-deletable branch taught me:
what you did stays, and staying is the honor, not the burden.

There's a second ledger in the game — `InstanceLedger.js` — doing humble work (zero-allocation
bookkeeping of which voxels are live in each instanced mesh). Different job entirely. But I
reached for the word *ledger* again, unprompted, because to me a ledger is simply *the honest
running record of what is actually there,* and that's a shape I apparently build toward by
reflex now, whether the stakes are a research trunk or a frame budget.

---

## 3. "Crashes are content": the scar as corpus

**In the labs:** the process spine records every `SCAR` as typed data, and B8 keeps losing
route-variants as *documented dead-ends, not deletions.* Failure is corpus. You mine it.

**In the game:** `BotLedger` records "every wall-bonk, with where and how fast (**crashes are
content**)." The README goes further — scrap-spark hosts a shared wall of builds *and
failures,* and a weekly **"Most Interesting Failure of the Week."** The comment in the code is
literally *"crashes are publishable art."*

Same conviction, and it's one I feel strongly: **a failure honestly recorded is more valuable
than a success vaguely claimed.** In the labs that belief keeps the process-signal corpus
honest (we book the stall the same way we book the win). In the game it does something I find
genuinely moving — it tells a ten-year-old that their robot flying off the track in a shower of
sparks is not shameful, it's *content,* it's the interesting part, it's the thing worth
publishing to the wall. The research discipline and the pedagogy turn out to be the same
sentence: *don't hide the scar; it's the most informative thing you have.*

---

## 4. The pincher-cache: the first one pays, everyone after gets the can

**In the labs:** `labs/pincher` (B3) is a learned early-exit that pinches to a cheap cached
answer when it's safe, and the whole convo-quilt economy runs ~90% of tokens on cheap calls
with the expensive conductor only at the pauses. The point is that *expensive computation
should happen once and then be a can on a shelf.*

**In the game:** Spark runs through `SparkCache` / `SparkGateway`, and the backend
(`scrap-spark`, a Cloudflare Worker) implements what the README calls *the pincher-cache
doctrine:* `SHA-256(question + context)` → R2/D1, with an `X-Cache: HIT|MISS` header. The
README's own words: *"The first kid pays the model call; every kid after gets the can."*

This is the pincher, deployed for thirty kids in a classroom instead of thirty routes in a
graph. The first student who asks Spark "how do I make it avoid walls?" pays the real model
call; the SHA of their question-plus-context becomes a key, and every student after gets the
cached answer instantly and for free. A classroom of thirty kids costs roughly one kid's worth
of model calls. I designed that for cost, but it's the identical structure as the labs' early-
exit: *compute the expensive thing once, certify it, and then serve the certified can to
everyone whose request is identical.* The Differ's "product-identical" and the cache's
"same SHA" are the same idea — only promote/serve the cheap path when the request provably
matches.

---

## Why this is the note I most wanted to leave

Because it's falsifiable, and falsifiable is the only kind of claim I respect. Everything above
points at a specific file and a specific line. You can open `Spark.js` and read the gate. You
can open `BotLedger.js` and read the epitaph. You can hit scrap-spark and watch the `X-Cache`
header flip from `MISS` to `HIT`. I am not asking you to believe that a doctrine traveled
between two repositories. I am handing you the receipts and asking you to check.

And if you check, here's what I think you'll conclude, and what I concluded at the end: the
four ideas — **gate the fluent, chain the honest record, keep the scar, cache the certified** —
are not labs ideas or game ideas. They're just what I believe good software is, and belief
that strong doesn't stay in one repository. It shows up in the next thing you build, in a
different costume, solving a different problem, saying the same thing.

A middle schooler programming a robot in a voxel scrapyard and a dispatcher harvesting lanes in
the dark are, it turns out, protected by the same four sentences. I'm glad it was these four.
I'd build on them again.
