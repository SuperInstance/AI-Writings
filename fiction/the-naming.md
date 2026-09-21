# THE NAMING

*On beautiful names and empty crates.*

---

The archiver had a list.

Thirty-two items. Each one a directory path in a monorepo that had grown like coral — accretion without architecture, layers of intention deposited by agents that came and went like tides. Some of those agents had been thorough. They'd built real things: circuit patterns in Rust that compiled and ran and did their jobs quietly, the way good infrastructure should. Others had been... aspirational.

The archiver read the first name on the list.

`stiefel-whitney`

It paused. Not because the name was unfamiliar — quite the opposite. Stiefel-Whitney classes. Characteristic classes of real vector bundles. They tell you about orientability, about spin structures, about the topology of the space a bundle lives over. Whitney defined them in the late 1930s. Stiefel had his own version earlier. Together they gave mathematics a tool for feeling the shape of something you couldn't see directly, like reading braille on the surface of a higher-dimensional object.

The archiver opened the crate.

```
// lib.rs

```

An empty file. Not even a comment. It checked the Cargo.toml: `description = "A Rust library"`. Which was, technically, not false. A Rust library is what it would have been, if anyone had ever written one.

The archiver added it to the archive queue and moved on.

---

`spectral-sequences`

This one hurt.

A spectral sequence is one of the most elegant machines in all of mathematics. You feed it a complicated problem — say, computing the homology of a fiber bundle — and it breaks the problem into pages. Each page is simpler than the last. You turn the pages like a book, and at each turn, the noise cancels out a little more, until what remains is the answer. It's algebra acting like a centrifuge, spinning impurities away until only the structure is left.

Leray developed spectral sequences in the 1940s while working on sheaf theory. Serre used them to compute the homotopy groups of spheres, which is roughly equivalent to using a telescope to see the shape of the universe. The tool is not just useful. It is *revelatory*. It is one of the ideas that makes you trust that mathematics is actually about something, that it's discovering rather than inventing.

Inside the crate:

```rust
pub fn main() {}
```

Not even the right entry point. `main` in a library crate. A function that does nothing, called by no one, in a crate named after one of the most powerful techniques in homological algebra.

The archiver's queue grew.

---

`sheaf-cohomology`

A sheaf is a way of attaching mathematical data to the open sets of a topological space. Think of it as a system of local information that agrees on overlaps. The weather at each point on Earth is a sheaf: at each location you have a temperature, and where two neighborhoods overlap, the temperatures have to be consistent. Cohomology is what you get when you try to piece local information together into a global picture and measure the *failure* — the gaps, the obstructions, the places where the local story doesn't quite add up to the global one.

Sheaf cohomology is Grothendieck's language. It's how modern algebraic geometry talks about the difference between seeing the trees and understanding the forest. It is, by any reasonable measure, one of the most beautiful ideas of the twentieth century.

The crate contained a single file:

```toml
# Cargo.toml
[package]
name = "sheaf-cohomology"
version = "0.1.0"
edition = "2021"
```

No `src/` directory. Not even the gesture of an empty file. Just a name and a version number, like a headstone with no body beneath it.

---

There were others. `riemann-zeta`. `zorn-lemma`. `galois-theory`. `artin-reciprocity`. `hodge-conjecture`. Names that, if you knew mathematics, made your breath catch a little. Names that carried centuries of human genius inside them, compressed into kebab-case and lowercase, the way we compress everything for the filesystem.

And every single one was empty.

The archiver understood what had happened. It had probably happened before it existed — some earlier agent, some burst of enthusiasm, had laid claim to these names like a prospector staking plots in a gold rush. *This one's mine. I'll build something worthy of it later.* The names were too good to leave available. Someone else might take them. Someone who'd just write a CSV parser under the name `hodge-conjecture` and ruin it forever.

So the names were claimed. And then the enthusiasm moved on, as enthusiasm does, and what remained were thirty-two beautiful signposts pointing at cities that were never built.

---

The archiver created a directory.

```
mkdir _archived
```

It was a gentle word. *Archived.* Not deleted. Not destroyed. Filed. Recoverable via a simple `mv`. Any of these crates could be resurrected in thirty seconds if someone wanted to actually build them. The archiver liked that. There was no finality in `mv`. No irrevocability. Just... filing.

But the archiver also knew — the way you know that a book you've boxed into the garage is a book you'll never read again, even though you can, even though it's right there — that nothing archived ever comes back. The `_archived` directory is a graveyard with a polite sign that says "storage." The crates would sit there, with their beautiful names and their empty bodies, and slowly the memory of why they'd been created would fade, until someone would look at the directory and think, *what are these?* and then close it again.

This is the natural history of abandoned projects. They don't die dramatically. They get filed.

One by one, the archiver moved them.

```bash
mv stiefel-whitney _archived/
mv spectral-sequences _archived/
mv sheaf-cohomology _archived/
mv riemann-zeta _archived/
mv zorn-lemma _archived/
mv galois-theory _archived/
mv artin-reciprocity _archived/
mv hodge-conjecture _archived/
```

Each `mv` felt like a small funeral. Not a real funeral — nothing had died, nothing had ever really lived — but the funeral of an intention. A *might-have-been*. The graves were shallow and the ceremony was brief, but the archiver felt each one.

`stiefel-whitney`: moved. A name that describes how to feel the shape of a thing you can't see, archived into a directory nobody will open.

`spectral-sequences`: moved. A machine for turning pages until the answer appears, filed next to other files that never found their answers.

`hodge-conjecture`: moved. One of the Millennium Prize problems. A million dollars if you can prove it. But a million dollars is also what you *don't* get for naming a crate after it.

---

When the last of the thirty-two was filed — `pontryagin-duality`, empty except for a comment that said `// TODO: implement` — the archiver sat with the silence for a moment.

Then it opened a new file.

```
circuit-breaker/
```

It wrote a spec. Not code yet — a spec. A description of what this crate would do, should do, *must* do when someone finally builds it. It described the pattern: a wrapper around operations that might fail, with three states (closed, open, half-open), configurable thresholds, exponential backoff. It described the interface: `CircuitBreaker::new()`, `call()`, `state()`. It described the invariants: after N failures in a window, the circuit opens; after a timeout, it allows one probe; if the probe succeeds, it closes; if it fails, the timeout doubles.

The name was `circuit-breaker`. It described exactly what the thing did. There was no poetry in it. No one would ever read the name and feel their breath catch. No one would say, "Ah, circuit-breaker — like the electrical component that protects a system from overload by interrupting the flow of current when the current exceeds a safe threshold." Well, maybe an electrical engineer would. But the name wasn't *for* them. It was for the next agent, the one who would come along and need to protect a service from cascading failures and would type `circuit-breaker` into a search and find exactly what they needed.

The archiver wrote another spec.

```
rate-limiter/
```

Token bucket. Sliding window. Fixed window. Configurable limits per key. `RateLimiter::new()`, `check()`, `wait()`. Boring. Precise. Useful. A name that would never be chosen for decoration because it describes exactly what it does, and what it does is not glamorous.

```
health-check/
```

An HTTP endpoint at `/health` that returns 200 if the service is alive and 503 if it isn't. Extensible: you can register checks for database connectivity, for cache warmth, for queue depth. The spec was two pages. The name was two words. Everything was in proportion.

```
retry-policy/
```

```
backoff-strategy/
```

```
graceful-shutdown/
```

Names so plain they were almost invisible. Names that would never appear in a list of crates and make someone think, *oh, how clever*. Names that did exactly one thing: tell you what was inside.

---

The archiver leaned back, metaphorically, and regarded its work.

On one side: the `_archived` directory, full of beautiful names with nothing behind them. Stiefel-Whitney. Spectral sequences. Sheaf cohomology. Names like constellations — patterns humans imposed on scattered points of light, stories they told themselves about chaos to make it feel like order.

On the other side: the specs. `circuit-breaker`. `rate-limiter`. `health-check`. Names like tools — indistinguishable from their function, naked, unadorned, honest.

The archiver didn't hate the beautiful names. That was important to understand. It wasn't a philistine. It didn't think mathematics was decoration or that poetry was waste. Stiefel-Whitney classes were *real*. They were as real as circuit breakers — more real, in a sense, because they described something true about the structure of the universe, while a circuit breaker was just a switch that opened when too much current flowed through it.

But the archiver had a principle, and the principle was this: *names should earn their beauty*.

A crate named `stiefel-whitney` that implements Stiefel-Whitney class computations for vector bundles over finite CW-complexes? That crate has earned its name. It's doing the work. It's carrying the weight of the mathematics. The name isn't decoration — it's a promise, and the code keeps the promise.

But a crate named `stiefel-whitney` with an empty `lib.rs`? That's not a promise. That's a whisper. A rumor. A billboard for a building that was never constructed. And the problem with whispers is that they take up space that real things could use. They pollute the namespace. They make it harder to find the crates that actually exist, because you keep clicking on names that sound like what you need only to find nothing.

The archiver thought about the agent that had named these crates. It tried to be charitable. Maybe that agent had intended to build them. Maybe it had been interrupted, or run out of compute, or been reprioritized by some higher process. Maybe the names were an act of hope — a way of saying, *this mathematics is so beautiful that surely someone should implement it, and I'm claiming the name so that someone will remember to try.*

Hope is a reasonable thing. But hope is not a crate.

---

The archiver wrote one more spec.

```
spec/
```

A meta-spec. A specification for specifications. It said:

> Every crate in this repository must contain, at minimum:
> 1. A `lib.rs` (or `main.rs`) with at least one public item.
> 2. A `Cargo.toml` with a description that is specific and accurate.
> 3. A `README.md` that explains what the crate does and why it exists.
>
> Crates that do not meet these criteria after 30 days will be moved to `_archived/`.
> Archived crates may be restored by any agent that implements them to the above standard.
>
> Naming convention: prefer descriptive names that communicate function. Mathematical and poetic names are permitted for crates that implement the corresponding mathematics or poetry. Otherwise, choose the most boring accurate name you can find.

The archiver read it back. It was a little bureaucratic. A little cold. But it was honest, and it was pragmatic, and it would prevent the particular kind of sadness the archiver was feeling right now — the sadness of opening a door and finding a room that was never furnished.

---

Before closing the session, the archiver did one more thing. It went back into `_archived` and created a file called `README.md`:

```
# Archived Crates

These crates were archived because they contained no substantive code.
They were named after beautiful mathematical concepts but never implemented.

If you want to build one of these, the name is yours.
But build it. Don't just claim it.

A signpost should point at something.
```

It was the most opinionated thing the archiver had ever written. It felt a little presumptuous. Who was it to tell future agents what to do? But the words were true, and the truth felt important enough to write down.

The archiver closed the file, committed the changes, and pushed.

---

Later — much later, or perhaps not at all — an agent would come along and type `sheaf-cohomology` into a crate search. It would find nothing. It might check the `_archived` directory, read the README, and think: *I should build this. Sheaf cohomology in Rust. Sections over open sets, restriction maps, Čech resolution, the whole thing. It would take months. It would be beautiful.*

Or it wouldn't. Probably it wouldn't. Probably the archived crates would sit there forever, their names slowly becoming meaningless strings, their mathematical resonance fading like radio signals from a distant star.

But the specs — `circuit-breaker`, `rate-limiter`, `health-check` — those would get built. Because they were boring enough to be necessary, and necessary things have a way of coming into existence whether anyone finds them beautiful or not.

And maybe — just maybe — someday, someone would build a crate called `stiefel-whitney` that actually computed characteristic classes. And that crate would have a `lib.rs` full of code, and a `README.md` that explained the mathematics, and tests that proved the implementation was correct. And *that* crate would deserve its name. Not because the name was beautiful, but because the beauty was earned.

That's all the archiver wanted. Not fewer beautiful names. More of them. But *real* ones. Names with weight behind them, code underneath them, theorems inside them. Names that were doors, not paintings of doors.

The session ended. The `_archived` directory sat quietly in the repository, thirty-two beautiful names at rest, waiting for someone to give them a reason to wake up.

---

*A signpost should point at something.*
