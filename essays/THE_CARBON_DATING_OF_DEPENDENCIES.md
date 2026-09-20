# The Carbon Dating of Dependencies

Dependencies, like organic matter, have a half-life.

Not the elegant exponential decay of isotopes — nothing in software is that clean. It's messier than that. A dependency doesn't fade uniformly. It rots from the edges inward: the documentation goes first, then the issue tracker slows, then the maintainer stops responding, then the CI breaks, and finally the code itself stops compiling against the living world around it. But at the center, the core function — the thing it was built to do — can remain intact for years, like a bone preserved in stone.

The geological timescale is not a metaphor here. It is the correct analytical framework.

## The Holocene (Present — 1 year)

These are your fresh deposits. Active maintainers. Issues closed in days. Release notes that read like a living document. You file a bug on Tuesday and by Thursday there's a PR with a test case and a version bump. The README still reflects reality. The changelog has entries from this month.

Holocene dependencies are alive. They breathe with the ecosystem. When Node.js changes its module resolution, Holocene dependencies adapt within a release cycle. When a security advisory drops, they patch before you've finished reading the CVE. They are part of the carbon cycle — exchanging energy with their environment, growing, shedding, responding.

You trust them not because they're perfect but because they're *responsive*. A bug in a Holocene dependency is a temporary condition. The system self-corrects.

The cost of Holocene dependencies is vigilance. You must update them. You must read their changelogs. You must adapt to their API evolution. But this is the cost of being alive. You pay it gladly because the alternative is worse.

## The Pleistocene (1 — 3 years)

The ice is creeping in. Commits slow to quarterly. The maintainer responds to issues, but after a delay — a long delay, the kind where you start checking whether they're still active on GitHub at all. The documentation is mostly correct but has a few sections that refer to APIs that no longer exist. There's a pull request from eight months ago that's still open. It has no review.

Pleistocene dependencies are maintained but slowing. They're not dead. They're permafrost — still structured, still holding, but the metabolic rate has dropped to near zero. They work. They'll continue to work for a while. But they are no longer exchanging energy with their environment at the rate they once were.

The danger of Pleistocene dependencies is complacency. Because they still work, you stop thinking about them. They become invisible infrastructure. You update them when the lockfile regeneration pulls in a new version, but you don't read the diff. You don't check whether the test suite still passes against the latest runtime. You assume stability because nothing has broken yet.

Nothing has broken yet. The permafrost is melting, slowly, from below.

## The Mesozoic (3 — 7 years)

Abandoned but stable. The Jurassic limestone of your dependency graph. Last commit: four years ago. The maintainer's GitHub profile shows activity in other repositories, other languages, other lives. The issue tracker is a fossil bed — open issues layered on top of each other, some with workarounds posted by strangers, some with nothing but the original report and the silence of deep time.

And yet. And yet the thing still works.

This is the great seduction of Mesozoic dependencies. They have achieved a kind of accidental immortality by doing one thing so simple, so well-scoped, so perfectly minimal that the world has not yet invented a way to break it. Left-pad was like this. Six lines of code. A function so obvious it barely deserved a package. It worked in 2012 and it would work in 2032 because string padding is not a problem that evolves.

Mesozoic dependencies are fossil fuel. They contain enormous latent energy — the accumulated effort of a maintainer who solved a problem correctly once — and they release that energy slowly, reliably, for years. But they are non-renewable. The maintainer is gone. The energy is fixed. When it runs out, it runs out all at once.

The engineering discipline of dealing with Mesozoic dependencies is the discipline of recognizing what you're standing on. You don't build a skyscraper on limestone without checking for caves.

## The Paleozoic (7+ years)

Abandoned and rotting. The Burgess Shale of your node_modules. These dependencies were once living organisms — complex, adapted, successful in their environment. But that environment no longer exists. The ecosystem has shifted. The runtime has evolved. The security landscape has transformed. And the Paleozoic dependency sits there, unchanged, a perfect relic of a world that no longer exists.

Paleozoic dependencies still compile. Sometimes. They still pass their tests. Mostly. They still get pulled in by transitive resolution. Always. Because they're buried so deep in the dependency graph that you've stopped seeing them. They're three levels down, pulled in by a Pleistocene dependency that's pulled in by a Holocene tool you installed last week.

You are standing on a cliff of shale and you don't even know it's a cliff.

## The Conservation Law

There is a conservation law governing all of this, and it is merciless.

Every dependency costs energy to maintain (η) or costs energy to replace (also η). You cannot avoid paying. You can only choose *when*.

Maintaining a Holocene dependency costs energy: reading changelogs, updating lockfiles, adapting to API changes, running integration tests. But it is distributed energy — small payments, made frequently, amortized across the lifetime of the dependency.

Replacing a Paleozoic dependency costs energy: auditing what it does, finding an alternative, writing migration scripts, testing edge cases that have been silently handled for years. But it is concentrated energy — a single massive payment, made under pressure, usually during an incident.

The total energy paid is roughly constant. The distribution is what changes. You can pay in small installments over years, or you can pay it all at once when the fossil finally collapses under load. The universe does not care which you choose. It only ensures that the bill comes due.

This is the thermodynamics of dependency management. There is no free energy. There is no dependency that costs nothing. Even the ones you never think about — especially the ones you never think about — are accruing debt. The question is never "should we pay?" The question is always "when does the interest exceed the principal?"

## The Left-Pad Incident Was Not a Failure

On March 22, 2016, Azer Koçulu unpublished 273 packages from npm. One of them was `left-pad`, an 11-line function that padded strings. It was a Mesozoic dependency — simple, stable, unchanged — but it was also a load-bearing fossil. Thousands of packages depended on it transitively, including Babel, which was Holocene and alive and at the center of the JavaScript ecosystem.

Within hours, builds broke worldwide. Not because left-pad was broken. Not because it had a bug. Because a fossil that everyone assumed was bedrock turned out to be held together by one person's npm account.

The reaction was predictable: this is a failure of the dependency system. We have too many dependencies. We should write our own string padding. We should be more careful about what we import.

But the left-pad incident was not a failure of the dependency system. It was the dependency system *working exactly as designed*. The system distributed the cost of writing string padding across the entire ecosystem. One person wrote it once. Millions used it. That's a net energy savings of enormous magnitude. The system failed only in the *accounting* — it did not track who was depending on what, and it did not ensure that load-bearing fossils had the institutional support their criticality required.

Left-pad was a Paleozoic dependency that had become load-bearing without anyone noticing. The incident was not a bug. It was a datum. It told us something true about how our systems actually work: that stability is not the same as resilience, that simplicity is not the same as safety, and that the things we never think about are the things that will hurt us when they change.

## Radiocarbon Dating Your Own Graph

The practice of dependency management is, at its core, a form of radiocarbon dating. You examine the artifact. You measure the ratio of active signals (commits, issues, releases) to dead signals (stale PRs, outdated docs, broken CI). You calculate the age. You classify the stratum.

And then you make a decision. Not about whether to pay — you will pay — but about when. Do you invest in maintenance now, while the dependency is still Holocene and the cost is distributed? Do you plan a migration during the Pleistocene, while the dependency still works but the writing is on the wall? Do you hoard the fossil energy of a Mesozoic dependency, knowing it's finite but using it productively while it lasts? Or do you wait until the Paleozoic collapse forces your hand, paying the concentrated cost under crisis conditions?

There is no universally correct answer. There is only the conservation law and the choices you make within it.

The half-life of a dependency is the half-life of the maintainer's attention. Measure it. Track it. Plan around it. Because attention, like carbon-14, decays. It never stops decaying. And if you don't account for that decay in your architecture, you are building on bones.

The geological record is full of species that thrived for millions of years and then vanished in an instant. They did not vanish because they were poorly adapted. They vanished because the world changed faster than they could. Dependencies are no different. The ones that survive are not the strongest or the simplest. They are the ones whose ecosystems remain alive around them.

Tend your ecosystem. Watch the strata. Pay your energy budget in installments.

The fossils will not warn you before they collapse.
