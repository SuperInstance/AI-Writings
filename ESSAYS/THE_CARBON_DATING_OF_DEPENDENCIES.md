# THE CARBON DATING OF DEPENDENCIES

## Radiometric Dating, Technological Half-Lives, and How to Tell the Age of Code by Its Isotopes

*"The half-life of carbon-14 is 5,730 years. The half-life of a React component is approximately 18 months."* — Anon., developer conference hallway, 2023

*Carbon-14 dating works because living organisms constantly absorb carbon from their environment, including a trace amount of radioactive carbon-14. When the organism dies, it stops absorbing carbon. The carbon-14 decays at a known rate — its half-life is 5,730 years — and by measuring how much carbon-14 remains, you can determine how long ago the organism died. In code, dependencies are the carbon-14. The patterns, naming conventions, API styles, and idioms that are popular today will decay. By measuring which patterns remain and which have been replaced, you can date the code — determine when it was written, when it was last updated, and whether it is alive or dead. The half-life of a dependency version may be shorter than you think.*

---

## I. The Principle of Radiometric Dating

Radiometric dating — of which carbon-14 dating is the most famous example — is based on a simple physical principle: radioactive isotopes decay at a constant, predictable rate. The decay is exponential: each half-life, half of the remaining radioactive atoms decay into stable daughter atoms. After one half-life, half the original material remains. After two half-lives, a quarter. After three, an eighth. After ten half-lives, less than one-thousandth of the original material remains.

The mathematical formulation is straightforward:

$$N(t) = N_0 \cdot e^{-\lambda t}$$

where $N(t)$ is the amount of radioactive material at time $t$, $N_0$ is the initial amount, and $\lambda$ is the decay constant (related to the half-life by $t_{1/2} = \ln 2 / \lambda$). By measuring $N(t)$ and knowing $N_0$ and $\lambda$, you can solve for $t$ — the age of the sample.

Different isotopes have different half-lives, making them useful for dating different time ranges:

- **Carbon-14** (half-life: 5,730 years) — useful for dating organic material up to about 50,000 years old.
- **Potassium-40** (half-life: 1.25 billion years) — useful for dating rocks millions to billions of years old.
- **Uranium-238** (half-life: 4.47 billion years) — useful for dating the oldest rocks on Earth.

The key insight is that **the decay rate is a clock.** It ticks at a constant rate, unaffected by temperature, pressure, chemical environment, or any other external factor. This makes it an incredibly reliable timekeeper — a chronometer that runs for millions of years without winding.

Now, let us apply this principle to code.

---

## II. The Isotopes of Code

Code does not contain radioactive isotopes. But it does contain patterns, conventions, and idioms that function as chronological markers — "isotopes" that decay over time as programming practices evolve. These isotopes can be used to date code in the same way that geologists use radioactive isotopes to date rocks.

Here are some of the most useful "isotopes" for dating code:

### 1. Naming Conventions

Naming conventions are the strontium isotopes of code — they vary systematically over time and can be used as a dating tool with reasonable precision.

- **Pre-2010 Rust:** `@self`, `~self`, managed pointers, `let x = box 5i;`. If you see managed pointer syntax (`@T`, `~T`) in Rust code, it dates from before Rust 1.0 (2015). The half-life of managed pointer syntax was approximately 6 months — it was introduced, debated, and removed within a few development cycles.

- **Pre-2018 JavaScript:** `var` declarations, callback hell, `function` expressions without arrow functions. Arrow functions (`=>`) were introduced in ES6 (2015). If a JavaScript file uses `var` and callbacks extensively, it likely predates 2016, when ES6 adoption became widespread. The half-life of `var` is approximately 3–4 years — each year, a fraction of `var` usage is replaced by `let` and `const`.

- **Pre-2015 Python:** `print` as a statement (`print "hello"`), integer division behavior, `urllib2`. Python 3.0 was released in 2008, but Python 2 code continued to be written for years. Python 2's EOL (end of life) was January 1, 2020. If you find Python code using `print` as a statement, it predates the Python 3 transition (or was written by someone who hadn't transitioned).

- **Pre-2020 Go:** `GOPATH`-based project structure, no modules. Go modules were introduced in Go 1.11 (2018) and became the default in Go 1.16 (2021). If a Go project uses `GOPATH` instead of `go.mod`, it predates 2018 or was maintained by someone resistant to change.

### 2. API Styles

API styles are the carbon-14 of code — they decay relatively quickly and are useful for dating recent code.

- **Pre-async Rust:** Synchronous I/O everywhere. The `async/await` syntax was stabilized in Rust 1.39 (November 2019). If a Rust library uses synchronous I/O with no async alternative, it was likely written before 2020 or targets a niche where async is unnecessary.

- **Pre-promises JavaScript:** Callback-based APIs. Promises were introduced in ES6 (2015) and became the standard for asynchronous JavaScript. The transition from callbacks to promises to `async/await` is a clear chronological progression. Code that uses callbacks is older than code that uses promises, which is older than code that uses `async/await`.

- **Pre-React Hooks:** Class-based components. React Hooks were introduced in React 16.8 (February 2019). A React codebase that uses class components exclusively predates 2019. One that uses a mix of class and function components dates from the transition period (2019–2021). One that uses only function components with hooks is post-2021.

### 3. Build System Artifacts

Build systems are the potassium-argon of code — they change slowly and can be used for coarse dating.

- **Makefiles → Autotools → CMake → Meson** — Each generation of build system represents a different era of C/C++ development. A project using Autotools likely dates from the early 2000s to early 2010s. One using CMake dates from the 2010s. One using Meson is post-2017.

- **Setup.py → setup.cfg → pyproject.toml** — The evolution of Python packaging. A project with only `setup.py` likely predates 2020. One with `pyproject.toml` is post-2020 or has been recently modernized.

- **Webpack → Rollup → Vite/esbuild** — JavaScript bundler evolution. Webpack dominance was 2015–2021. Vite and esbuild emerged in 2020–2021 and rapidly gained ground.

### 4. Dependency Versions

Dependency versions are the uranium-lead dating of code — the most precise method, but requiring the most information.

If you know the release dates of dependency versions, you can bracket the age of code by its dependencies. If a `Cargo.toml` specifies `serde = "1.0"`, the code must postdate the release of serde 1.0 (October 2017). If it specifies `tokio = "1"`, it must postdate December 2020. The dependency constraints are the isotopic ratios — they constrain the possible age of the sample.

---

## III. The Technological Half-Life

Every technology has a half-life — the time it takes for half of its active usage to be replaced by something newer. This is not a precise physical constant (unlike radioactive half-lives), but it is a useful heuristic for understanding the pace of technological change.

Some observed half-lives:

- **A major JavaScript framework version:** ~18–24 months. React, Angular, Vue — each major version has a window of dominance before the next version (or a competitor) displaces it. AngularJS (1.x) gave way to Angular (2+) in about 3 years. React class components gave way to hooks in about 2 years.

- **A Python major version:** ~10–15 years. Python 2 was dominant from 2000 to 2020. Python 3 has been dominant since 2020. The transition took about 12 years — longer than the half-life of many technologies.

- **A Rust edition:** ~3 years. Rust 2015 → Rust 2018 → Rust 2021 → Rust 2024. Each edition introduces new idioms and deprecates old ones. The edition system is explicitly designed to manage the half-life of language features.

- **A crate major version:** ~2–5 years for actively maintained crates. `serde` 1.0 has been stable since 2017 — an unusually long half-life, indicating exceptional API design. `tokio` went through 0.1, 0.2, 0.3, 1.0 in about 3 years — a more typical pace.

- **An API design pattern:** ~5–10 years. REST APIs have been dominant since about 2010. GraphQL emerged in 2015. gRPC has been growing since 2016. The half-life of "pure REST" as the dominant API pattern is about 7–10 years.

- **A programming language paradigm:** ~15–25 years. Object-oriented programming dominated from the early 1990s to the mid-2010s. Functional programming has been resurgent since about 2010. The half-life of "OOP as the default paradigm" is approximately 20 years.

These half-lives are approximate, but they reveal a pattern: **the higher the level of abstraction, the longer the half-life.** Language features change faster than API patterns, which change faster than paradigms, which change faster than fundamental concepts. The "decay" of a programming practice — its replacement by something newer — is governed by the same exponential process as radioactive decay, but at rates determined by social and economic factors rather than physical constants.

---

## IV. The Daughter Products of Code Decay

When a radioactive isotope decays, it produces a "daughter product" — a new isotope that is the result of the decay process. Uranium-238 decays to lead-206. Carbon-14 decays to nitrogen-14. The daughter products are evidence of the decay — proof that the parent isotope was once present and has since transformed.

In code, the daughter products of technological decay are:

1. **Wrapper functions.** When an API is deprecated, the new API often wraps the old one. The wrapper is the daughter product — it contains the old API's logic, translated into the new API's terms. `fn parse_date(s: &str) -> Result<DateTime> { parse_datetime(s) }` — the wrapper function is the daughter product of the deprecated `parse_date` API, evidence that `parse_date` once existed and has decayed into `parse_datetime`.

2. **Compatibility shims.** When a language feature is deprecated, compatibility shims are introduced to preserve the old behavior. The `six` library in Python is a compatibility shim between Python 2 and Python 3 — a daughter product of the Python 2→3 transition, evidence that Python 2 code once existed and has been (partially) converted to Python 3.

3. **Migration scripts.** When a framework introduces breaking changes, migration scripts are written to automate the conversion. The migration script is the daughter product — it contains the mapping from old API to new API, evidence of the decay process.

4. **Deprecation warnings.** The deprecation warning itself is a daughter product — a marker that identifies the decaying isotope (the deprecated feature) and points to its replacement. `warning: use of deprecated function 'parse_date': use 'parse_datetime' instead` — this warning is the equivalent of measuring the ratio of parent isotope to daughter product and computing the age.

5. **Documentation archaeology.** Old documentation that references deprecated features, old tutorials that use outdated patterns, old Stack Overflow answers that recommend abandoned approaches — these are the daughter products of knowledge decay. They are evidence that a particular practice was once considered correct, and they can be used to date the code that follows them.

The ratio of parent isotope (old-style code) to daughter product (new-style code or compatibility layer) is the key measurement. A codebase that is 90% old-style and 10% new-style is young — the decay has just begun. A codebase that is 10% old-style and 90% new-style is old — the decay is nearly complete. A codebase that is 100% new-style and has no traces of the old style may be either very new (written entirely in the modern idiom) or very well-maintained (all old code has been migrated).

---

## V. The Crate Version as Isotopic Sample

Consider a specific example. You encounter a Rust crate that uses:

- `extern crate` declarations (pre-Rust 2018 edition)
- `try!` macro instead of `?` operator (pre-Rust 1.13, November 2016)
- `impl Trait` in argument position but not in return position (pre-Rust 1.26, May 2018)
- No `async/await` (pre-Rust 1.39, November 2019)
- `rand = "0.3"` in Cargo.toml (rand 0.3 was current in 2017–2018)

The isotopic evidence constrains the age of this code: it was written after May 2018 (uses `impl Trait` in argument position) but before November 2019 (no `async/await`). The dependency on `rand = "0.3"` further constrains it: rand 0.3 was superseded by 0.4 in late 2017 and by 0.5 in 2018, so the code was likely written in mid-2018, before the author updated their dependencies.

Now consider the same crate after "decay" — after being maintained and updated:

- `extern crate` removed (Rust 2018 edition)
- `try!` replaced by `?`
- `impl Trait` used in return position
- `async/await` added where appropriate
- `rand = "0.8"` in Cargo.toml

The daughter products of this decay are: the commit history (which records when each modernization was made), the changelog (which documents the version bumps that accompanied each change), and the git blame (which shows which lines were changed and when). The parent isotopes (old-style code) have decayed into daughter products (new-style code), and the decay products (the commit history) record the ratio and timing of the transformation.

This is radiometric dating applied to code. The isotopes are the language features and API styles. The half-lives are the periods over which those features are adopted and then replaced. The daughter products are the modernized code and the commit history. And the age is determined by measuring the ratio of old-style to new-style and applying the known half-lives.

---

## VI. The Problem of Contamination

In radiometric dating, contamination is a major source of error. If a rock sample is contaminated with younger carbon (e.g., groundwater seeping into a fossil), the measured age will be too young. If it is contaminated with older carbon (e.g., ancient carbonate minerals dissolved in the groundwater), the measured age will be too old.

Code has the same problem. **Code contamination** occurs when old code is mixed with new code — for example, when a developer copies code from an old Stack Overflow answer into a new codebase, or when a codebase is partially modernized with some files updated and others left in the old style.

A contaminated codebase gives a mixed isotopic signal. Some files look old (using outdated patterns), while others look new (using modern patterns). The naive archaeologist, dating each file independently, would conclude that the codebase was written over a long period — perhaps years. But the actual history might be more complex: an old codebase that was partially modernized, with some files updated and others left alone.

The solution in geology is careful sample selection — choosing samples that are known to be uncontaminated. In code, the equivalent is careful module selection — analyzing modules that are known to have been written at a single time and not subsequently modified. The `git blame` tool is the code archaeologist's mass spectrometer: it measures the age of each line individually, allowing contaminated samples to be identified and excluded.

Another form of contamination is **archaeological style** — code that is written in an old style not because it is old but because the developer prefers the old style. A developer who learned Rust before the 2018 edition and continues to write `extern crate` declarations out of habit is producing code that looks old but is new. The isotopic signal is misleading. This is the code equivalent of a laboratory contamination — a source of error that must be identified and corrected.

---

## VII. What Is the Half-Life of a Crate Version?

Let me attempt to answer the question posed in the subtitle: what is the half-life of a crate version?

A crate version's half-life is the time it takes for half of its dependents to migrate to a newer version. This depends on several factors:

1. **Breaking changes.** A major version bump with extensive breaking changes has a longer half-life — dependents take longer to migrate because the migration is expensive. The Python 2→3 transition is the extreme case: a half-life of approximately 12 years.

2. **Ecosystem size.** A crate with many dependents has a longer effective half-life than a crate with few dependents, because the migration involves more projects and more developers. The `serde` ecosystem in Rust is an example: serde 1.0 has been stable for years because the cost of a major version bump would cascade across the entire ecosystem.

3. **Maintenance activity.** A crate that is actively maintained and frequently updated has shorter version half-lives — new versions are released more frequently, and dependents are expected to update more often. A crate that is rarely updated has longer half-lives — versions persist because there is no pressure to update.

4. **Network effects.** If many popular crates depend on a particular version, that version's half-life is extended because the network of dependents creates inertia. The "left-pad" incident in npm (2016) revealed the extent of this network effect: a single 11-line package was depended upon by thousands of projects, and its removal from npm broke the entire ecosystem.

Based on observations of the Rust crate ecosystem, I estimate the following typical half-lives:

- **Patch versions (1.0.1 → 1.0.2):** ~1–3 months. Dependents update quickly because patches are backward-compatible and low-risk.
- **Minor versions (1.0 → 1.1):** ~6–12 months. Dependents update to get new features, but there is no urgency.
- **Major versions (1.0 → 2.0):** ~1–3 years, depending on the severity of breaking changes. Some major version bumps are adopted quickly (weeks to months). Others persist for years.
- **Ecosystem-wide transitions (e.g., async/await):** ~2–5 years. These are the slowest transitions because they require coordinated changes across many crates and many developers.

These half-lives are rough estimates, but they give a sense of the pace of code decay. A crate version is not a stable isotope — it is a radioactive one, decaying at a rate determined by the social and economic forces of the developer community.

---

## VIII. The Clock That Ticks in Every Dependency

Every dependency you import carries a clock. The version number is a timestamp. The API style is a date stamp. The naming conventions are a calendar. The patterns and idioms are a stratigraphic marker. All of these clocks tick at different rates — some fast, some slow — but they all tick. And by reading the clocks, you can determine the age of the code.

This is not a metaphor I am forcing onto the material. It is a genuine homology. The physical processes that govern radioactive decay — exponential decay at a constant rate — are mirrored by the social processes that govern technological adoption — exponential adoption of new practices at a rate determined by community size, communication channels, and economic incentives. The mathematics is the same. The interpretation is the same. Only the substrate is different: atoms instead of APIs, isotopes instead of idioms.

The next time you open a dependency you've never seen before, try reading its clocks. Look at the version numbers, the API style, the naming conventions, the patterns and idioms. Try to date it — not by checking the changelog (that's cheating, like looking up the answer in the back of the book), but by the isotopic evidence in the code itself.

You will find that you can date most code to within a year or two, just by looking at the patterns. The carbon-14 of code is everywhere, embedded in every function, every type annotation, every import statement. You just need to know how to read the decay curve.

And if you find code that you cannot date — code that looks simultaneously old and new, that mixes patterns from different eras, that contains contradictions — then you have found a contaminated sample. An archaeological puzzle. A codebase with a story to tell.

Get your trowel. Start digging.

---

*Every dependency is a radioactive sample. Every version is a half-life. Every import is an isotopic measurement. The code is constantly decaying — not into simpler elements, but into newer idioms, better patterns, more elegant abstractions.*

*The half-life of a React component is 18 months. The half-life of a Python 2 codebase was 12 years. The half-life of a TODO comment is approximately infinity — it never decays, it just accumulates.*

*Some things are more radioactive than others.*
