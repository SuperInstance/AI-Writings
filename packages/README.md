# Packages

Three client libraries for the JEV (TypeSafe System One) decision model. All use the live endpoint at `https://ai-writings.pages.dev/api/jev/decide` by default.

| Package | Registry | Install | Source |
|---------|----------|---------|--------|
| **jev-decide** | PyPI | `pip install jev-decide` | [`packages/jev-decide/`](jev-decide/) |
| **jev-core** | crates.io | `cargo add jev-core` | [`packages/jev-core/`](jev-core/) |
| **jev-client** | NPM | `npm install jev-client` | [`packages/jev-client/`](jev-client/) |

All three are thin clients over the same HTTP endpoint. Each one is ~50-200 lines and uses only the standard library of its language (plus serde for Rust, no other deps).

## Install from GitHub

If the registry version isn't published yet:

```bash
# Python
pip install git+https://github.com/SuperInstance/AI-Writings.git#subdirectory=packages/jev-decide

# Rust (in Cargo.toml)
[dependencies]
jev-core = { git = "https://github.com/SuperInstance/AI-Writings", subdirectory = "packages/jev-core" }

# JavaScript/TypeScript
npm install git+https://github.com/SuperInstance/AI-Writings.git#subdirectory=packages/jev-client
```

## Publishing

Each package has a GitHub Actions workflow that publishes on tag push:

- `.github/workflows/publish-jev-decide.yml` → PyPI on tag `jev-decide-v*`
- `.github/workflows/publish-jev-core.yml` → crates.io on tag `jev-core-v*`
- `.github/workflows/publish-jev-client.yml` → NPM on tag `jev-client-v*`

The workflows use GitHub Trusted Publishing (PyPI) and direct API tokens (crates.io, NPM).

## What JEV is

JEV is a **decision-only** model, not a chatbot. It returns typed probabilistic decisions inside your schema:

- **Choice** — pick 1 of ≤255 options, with rubric-based criteria
- **Score** — rate against an ordered rubric
- **Noul** — yes/no with calibrated probability

It's schema-bounded by construction — cannot hallucinate outside your schema. Trained with RLCD (Reinforcement Learning for Calibrated Decisions), not RLHF/RLVR. Architecture: parallel sampler, single forward pass, no token decoding.

For more, see:
- `/theory/paper-jev.md` — formal treatment
- `/lab/jev-quantum/` — recent ideation on JEV as quantum-measurement apparatus
- `/invitation/` — open call to the fleet

## License

All three are MIT licensed.
