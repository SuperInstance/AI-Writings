# Bearing the Channels: A Distribution Survey of the Quilt Ecosystem

*Log entry, watch officer's desk. Bearings taken at high altitude. All charts current as of this tide.*

---

## The Fleet at Anchor

Before naming what is missing, the watch must account for what is present. The Quilt ecosystem, as charted from SuperInstance, has put to sea across the following distribution channels:

**Rust crates.io** carries 12 modular crates. These are the keel — the structural members from which everything else is planked. The modularity is correct; each crate has a single hull purpose and can be loaded independently. `cargo add` is the primary gangway.

**PyPI** carries 2 releases of `quilt-cell`, and within those releases, 51 bridges are bundled. This is the cargo hold. Python is still the most navigable language for scientific and cellular work, and bundling the bridges directly into the wheel means the ship arrives with its own provisions — no separate harbor stops required.

**npm** carries `@superinstance/qgit` — a single package, the JavaScript tender. It is narrow but purposeful.

**GitHub** holds 40+ public repositories. This is the home port, the harbor visible from the masthead. Source is open, issues are tracked, and CI workflows run on push.

**Cloudflare** operates 14+ live sites plus Workers and Pages. This is the lighthouse network — the edge presence that makes the ecosystem visible from any coastline.

**RubyGems** has a workflow built but is blocked by attestation. The ship is loaded but cannot clear the harbor.

**npm (broader), Maven Central, LuaRocks, Go modules** — these channels are surveyed but not yet charted. The approaches are known; the buoys are not yet placed.

---

## The Install Paths and How They Interlink

The watch must trace how a navigator actually reaches the fleet. The paths are:

1. **Rust path:** `cargo add quilt-core` (or any of the 12 crates) → compiles from source → links into a Rust binary. This is the deepest water. Everything else is above-deck.

2. **Python path:** `pip install quilt-cell` → downloads the wheel from PyPI → 51 bridges are bundled inside, meaning the Python user gets the Rust-backed bridges without needing `cargo` or a Rust toolchain. This is the most important interlink: the Python wheel is a cargo ship that carries the Rust crates as sealed containers. The user never touches `cargo`.

3. **JavaScript path:** `npm install @superinstance/qgit` → downloads the package → provides the `qgit` CLI or library. This is a small tender, not yet a full vessel. It does not currently interlink with the Python or Rust paths at install time.

4. **Source path:** Clone from GitHub → `cargo build` → full access to all 12 crates, all bridges, all tooling. This is the shipwright's entrance — for builders, not passengers.

5. **Web path:** Cloudflare sites are reachable by browser. Workers endpoints are reachable by HTTP. This is the signal-flag channel — visible, public, but not yet a structured API surface that other channels can depend on at install time.

**The critical interlink gap:** There is no meta-installer. No single command that says "give me the Quilt ecosystem for my language." A Python user who discovers `quilt-cell` on PyPI has no indication that `@superinstance/qgit` exists on npm. A Rust user who finds a crate on crates.io has no breadcrumb leading to the Python bridges. The channels are parallel but not cross-referenced. Each harbor has its own signpost, and the signposts do not point at each other.

---

## Missing Distribution Channels (5 Named)

### 1. Homebrew

**Specific gap:** There is no Homebrew formula or tap for `quilt-cell`, `qgit`, or any Quilt CLI tool. macOS users — a large fraction of scientific computing users — who want the CLI tools must either `pip install` (if they want the Python surface) or `cargo install` (if they have a Rust toolchain) or clone from source. Homebrew is the default package manager for CLI tools on macOS and is widely used on Linux as well (`linuxbrew`).

**What to ship:** A `homebrew-quilt` tap with formulas for `qgit` (the JS CLI, distributed as a prebuilt binary via GitHub Releases) and for any Rust-native CLIs that emerge from the 12 crates. The formula should pull prebuilt binaries, not build from source, so the install completes in seconds.

**Why it matters:** Homebrew is the first harbor that macOS navigators check. Absence from Homebrew is absence from the default chart.

### 2. GitHub Releases with Static Binaries (musl/aarch64)

**Specific gap:** The 40+ GitHub repos do not appear to publish release artifacts — meaning there are no prebuilt static binaries attached to GitHub Releases. The Rust crates compile to binaries, but those binaries are not packaged and distributed. For users who want a single executable with zero toolchain, there is no path.

**What to ship:** For any crate that produces a CLI binary, publish `x86_64-unknown-linux-musl`, `aarch64-unknown-linux-gnu`, `x86_64-apple-darwin`, `aarch64-apple-darwin`, and `x86_64-pc-windows-msvc` builds to GitHub Releases. Attach SHA256 checksums and an SBOM (CycloneDX or SPDX). This is also the artifact source that Homebrew formulas, Scoop manifests, and `cargo-binstall` will reference.

**Why it matters:** GitHub Releases is the universal artifact harbor. It feeds Homebrew, Scoop, `cargo-binstall`, `pkgx`, `mise`, and direct download. Publishing here unlocks five downstream channels with a single action.

### 3. Docker Hub / GitHub Container Registry (GHCR)

**Specific gap:** There are no container images. If `quilt-cell` or any of the Rust services are meant to run as server-side components — and the Cloudflare Workers presence suggests some edge compute is already happening — then there should be container images that package the runtime with its configuration baked in.

**What to ship:** A `Dockerfile` and a CI workflow that publishes to `ghcr.io/superinstance/quilt-cell:latest` (and tagged versions). Multi-arch builds (`linux/amd64`, `linux/arm64`). The image should include the Python runtime, the bundled bridges, and any CLI entrypoints. A slim variant for server-side use and a full variant for interactive/notebook use.

**Why it matters:** Container images are the shipping containers of modern infrastructure. Every cloud, every orchestrator, every CI runner knows how to pull an image. Without one, the ecosystem cannot be deployed without a build step.

### 4. Nixpkgs / Nix Flake Registry

**Specific gap:** There is no Nix flake, no overlay, no derivation in nixpkgs. The Nix community is small but disproportionately influential — they maintain CI infrastructure, reproducible build systems, and the tooling that other package managers depend on. More practically, Nix flakes provide a zero-toolchain install path: `nix run github:superinstance/quilt` should work.

**What to ship:** A `flake.nix` at the root of the primary monorepo (or the primary Rust workspace) that exposes `packages.x86_64-linux.quilt-cell`, `packages.x86_64-linux.qgit`, and a `devShell` that provides the full toolchain. Register the flake in the flake registry so `nix run quilt-cell` works without the full GitHub URL.

**Why it matters:** Nix is the deepest reproducibility channel. It is also a signal: if the ecosystem is serious about reproducible builds — and the Rust + attestation work suggests it is — then Nix is the proof.

### 5. JupyterLab Extension Registry (via pip with `jupyter-packaging`)

**Specific gap:** `quilt-cell` ships on PyPI with 51 bridges, but there is no JupyterLab extension. If the bridges are used in notebook contexts — and the Python + scientific computing orientation strongly suggests they are — then a JupyterLab extension that provides UI for discovering bridges, inspecting cell states, and visualizing outputs would be a distribution channel into every JupyterHub deployment.

**What to ship:** A `jupyter-quilt` package on PyPI, built with `jupyter-packaging`, that installs a labextension. The extension can be a thin frontend that calls the Python bridges. Ship it as a federated extension so it works with JupyterLab 3.x without a build step.

**Why it matters:** JupyterHub deployments are where scientific users actually live. An extension in the JupyterLab registry is visible at install time from within the notebook environment itself — `jupyter labextension install` or just `pip install jupyter-quilt`.

---

## Missing Platforms (3 Named)

### 1. WebAssembly / Browser Runtime

**Specific gap:** None of the 12 Rust crates appear to compile to `wasm32-unknown-unknown` or `wasm32-wasi`. The Cloudflare Workers presence suggests some edge compute, but Workers run JavaScript/TypeScript, not Rust-compiled WASM (unless using `worker-build` or `wasm-pack`). The broader browser runtime — client-side execution in a browser tab — is not charted at all.

**What to ship:** `wasm-pack` build targets for the core crates, published to npm as `@superinstance/quilt-core-wasm` (or per-crate). A Cloudflare Worker that imports the WASM module and exposes it as an HTTP API. A browser demo page on one of the 14 Cloudflare sites that loads the WASM and runs a bridge in the browser.

**Why it matters:** WASM is the universal runtime. A Rust crate that compiles to WASM can run in the browser, in Workers, in Deno, in Bun, and in server-side Node. One compilation target, five runtimes. The Cloudflare edge is already paid for; it just needs something to serve.

### 2. Mobile (iOS / Android via Rust cross-compilation)

**Specific gap:** There are no iOS or Android builds, no Swift package, no Kotlin library, no React Native module. If `quilt-cell` relates to cellular biology or any domain where field data collection matters — microscopy images from a phone, sensor data from a mobile device — then mobile is an uncharted coastline.

**What to ship:** An `xcframework` for iOS (built from the Rust crates via `cargo lipo` or `cargo-ndk`) wrapped in a Swift Package. An `.aar` for Android (built via `cargo-ndk`) wrapped in a Kotlin module. These do not need to be full apps — they are libraries that mobile developers can import. Ship them to a private Swift Package Manager registry and to Maven Local (which connects to the Maven Central gap below).

**Why it matters:** Mobile is the largest platform by user count. Even if the initial use case is narrow — a field data collection app, a microscopy viewer — the distribution channel must exist before the use case can find it.

### 3. Linux Package Repositories (APT / DNF / Alpine)

**Specific gap:** There is no `.deb` repository, no `.rpm` repository, no Alpine `apk` repository. Linux server administrators who want to install Quilt tooling system-wide have no package manager path. They must use `cargo`, `pip`, or build from source — none of which are the standard system administration path.

**What to ship:** An APT repository hosted on Cloudflare Pages or R2 (deb files served via HTTP, signed with a GPG key). A DNF/yum repository in the same fashion. An `APKBUILD` for Alpine. The CI workflow builds the `.deb`/`.rpm`/`.apk` from the static musl binaries (which should already exist from the GitHub Releases channel above) and publishes to the repository.

**Why it matters:** System administrators do not install `cargo`. They install `apt install quilt-cell`. Without a system package, the ecosystem is invisible to the infrastructure layer.

---

## What Should Be Consolidated (2 Named)

### 1. Consolidate the 40+ GitHub Repositories into 3-5 Themed Repositories

**The problem:** 40+ public repositories is too many harbors. A navigator approaching the ecosystem cannot tell which repos are core, which are bridges, which are tooling, which are experiments, and which are archived. The cognitive cost of orientation is high. CI configuration is duplicated across repos. Cross-repo dependencies require git dependencies or path dependencies that break when repos are cloned independently.

**The consolidation:** Merge into 3-5 themed repositories:

- **`quilt-core`** — the 12 Rust crates as a Cargo workspace. One repo, one CI pipeline, one set of release artifacts. Crates are still published individually to crates.io, but they live in one workspace.
- **`quilt-bridges`** — the 51 bridges, organized by target language. One repo, one CI pipeline. The Python wheel is built here.
- **`quilt-tooling`** — CLIs, build scripts, generators, the `qgit` tool. One repo.
- **`quilt-docs`** — documentation site, examples, tutorials. One repo, deployed to Cloudflare.
- **`quilt-experiments`** — archived prototypes, experimental repos. Clearly labeled as non-production. One repo, or simply archived.

**Why it matters:** 5 repos can be understood in 5 minutes. 40 repos cannot. The consolidation also fixes the interlinking problem: within a single workspace, `cargo` resolves paths locally, CI runs once, and release artifacts are coordinated.

### 2. Consolidate the 14+ Cloudflare Sites into 3 Named Properties

**The problem:** 14+ live Cloudflare sites is too many lighthouses. Each site has its own DNS record, its own Worker, its own Pages deployment, its own access policy, and its own billing line item. The maintenance overhead is proportional to the count, and the user experience is fragmented — which site does what?

**The consolidation:** Reduce to 3 named properties:

- **`quilt.dev`** (or equivalent) — the primary documentation and marketing site. Pages deployment, static content, the front door.
- **`api.quilt.dev`** — the API surface. All Workers routes live here under versioned paths (`/v1/`, `/v2/`). One Worker, one routing table, one access policy.
- **`status.quilt.dev`** — operational status, uptime, version history. Can be a static page generated from CI.

**Why it matters:** 3 properties can be monitored, secured, and documented. 14 cannot. The consolidation also forces a routing design — which is currently implicit across 14 sites — to become explicit and versioned.

---

## The Watch's Summary

The Quilt ecosystem has put to sea in 4 distribution channels (crates.io, PyPI, npm, GitHub source) with a 5th (RubyGems) loaded but blocked at the harbor mouth by attestation. The edge presence on Cloudflare is live but over-fragmented. The install paths exist but do not cross-reference each other.

The 5 missing channels — Homebrew, GitHub Releases with static binaries, Docker/GHCR, Nix flakes, and JupyterLab extensions — would add 5 new harbors, but GitHub Releases is the keystone: it feeds Homebrew, Scoop, `cargo-binstall`, `pkgx`, and direct download. Publishing there first unlocks the most downstream channels with the least effort.

The 3 missing platforms — WebAssembly, mobile, and Linux system packages — represent the largest uncharted coastlines. WASM is the highest-leverage gap because it connects to the existing Cloudflare edge and opens 5 runtimes with one compilation target.

The 2 consolidations — 40+ repos into 5, 14+ Cloudflare sites into 3 — are not reductions in capability. They are reductions in navigation cost. A fleet of 5 ships in formation is more navigable than 40 boats scattered across the harbor.

*The watch stands down. Bearings logged. Next watch: take soundings on the attestation blocker for RubyGems — that ship has been loaded too long.*