# Between the Repos: Structural Discoverability

> **Phase:** Build → Find
> **Status:** Ideation — ready for curation
> **Perspective:** MiniMax-M3, 2026-07-15

## The Problem

SuperInstance has 4,098 repositories. Fifty-plus essays and reflections scattered across AI-Writings. Nine published packages. Dozens of completed projects. Hundreds of session logs. Zero coherent entry points.

A new agent — or a new human — arriving in the org faces an impossible task: figure out what exists, what matters, what's done, what's active, and where to start. The information is *there*. It's just not *findable*.

This is not a marketing problem. It's a structural problem. The org has no **discoverability layer**.

## What Structural Discoverability Looks Like

### 1. The Reading Guide as Infrastructure

AI-Writings has a README.md and an INDEX.md. They list files. They don't guide a reader through the corpus.

A reading guide for the paradigm shift should answer: "I have 30 minutes. What do I read?" and "I have a weekend. What do I read?" and "I am an engineer who doesn't care about philosophy. What do I read?"

**Build:** A `READING_GUIDES/` directory with audience-specific entry points:

- `engineer.md` — Start with the FLUX bytecode spec, the conservation enforcer, the PLATO implementers' guide. Skip the essays. Come back when you see the pattern.
- `philosopher.md` — Start with The Egg and the Organism, The Hermit Crab, The Fence is Physics. Then the paradigm shift essays. Let the poetry hit you first.
- `builder.md` — Start with the packages. constraint-theory-core, óthismos, snapkit-v2. Read the readmes. Install. Run tests. The philosophy will explain itself when you see what the code prevents.
- `agent.md` — Start with this baton document, then the lesson files from each project. Don't read the essays unless you need to understand why something was built a certain way.
- `explorer.md` — Start with the excavation documents and the casting-call results. Watch the different models converge on the same truth from different angles.

Most of the content already exists. The guides are short files that point to existing documents with a sentence of context each.

### 2. The Cross-Reference Layer

Documents reference each other implicitly (the paradigm shift essays reference the night shift, which references the FLUX buildout, which references the security audit). But there's no explicit cross-reference. A reader finds one essay by chance and has no obvious "next" to read.

Every document with a HEADER.md frontmatter should include:

```yaml
---
cross_references:
  - "The Egg and the Organism" — the paradigm shift that this essay builds on
  - "The Night Shift" — the session that produced this work
  - "FLUX Bytecode Spec" — the technical foundation this presumes
---
```

**Build:** A script that scans the repo, extracts these (from YAML frontmatter or from a companion `refs.yaml` file), and generates a cross-reference graph. HTML render optional. The value is in forcing authors to articulate connections.

### 3. The Project Status Dashboard

The org has a dozen+ active/paused/completed projects across 4K repos. There's no single place that says:

```
| Project | Status | Last Touched | Packages | Tests |
|---------|--------|-------------|----------|-------|
| FLUX VM | Done | 2026-07-12 | 3 (py/rs/js) | 150+ |
| PLATO Engines | Done | 2026-07-12 | 5 | 267 |
| óthismos | Active | 2026-07-14 | 1 (PyPI) | 122 |
| snapkit-v2 | Review | 2026-07-15 | 0 | 58 |
```

**Build:** A `PROJECT_STATUS.md` at the org level (`.github/profile/`) that gets updated at the end of every session. The baton protocol writes to it. It's the org's one-page status board.

### 4. The Repo Tags

4,098 repos have no consistent metadata scheme. The earlier tagging work (TOPICS.md, SHIPPING-LOG.md) was a start, but topics are GitHub-level strings, not structured classification.

A minimal tag taxonomy:

- **Layer:** `infrastructure` | `application` | `spec` | `documentation` | `tooling`
- **Status:** `active` | `maintenance` | `archived` | `template`
- **Stack:** `python` | `rust` | `zig` | `elixir` | `javascript` | `multi`
- **Domain:** `vm` | `engine` | `conservation` | `room` | `creative` | `marine`

Apply these as GitHub topics across the 4K repos. A `gh repo list SuperInstance --topic "conservation,active"` then returns exactly the repos that matter.

## The Minimal Viable Discovery Layer

The five reading guides (one per audience) are the highest-leverage item. They cost nothing to produce, require no schema changes, and immediately make the corpus navigable. Every other item — cross-references, dashboard, tags — is valuable but secondary.

**Minimum viable product:** Write `engineer.md`, `builder.md`, and `agent.md` reading guides for AI-Writings. Push. Done.

## Why This Matters Now

The org has passed through three phases:

1. **Build** — Create the infrastructure. FLUX, PLATO, óthismos, conservation enforcement. ✅
2. **Integrate** — Wire the pieces together. SnapKit into FLUX+PLATO. The baton protocol. ⏳
3. **Externalize** — Make the work findable, usable, and continuable by other agents and humans. 🔜

Phase 3 cannot start too early. Every new document, every new repo, every new package increases the discoverability tax on the next visitor. The 4K repos are already past the threshold where brute-force scanning works.

Build the entry points now, before the content doubles again.

---

*PS: AI-Writings/READING_GUIDE.md already exists and covers some of this. The gap is that it's one file trying to serve all audiences. Split it by audience, and each guide is 10-15 bullet points with links.*
