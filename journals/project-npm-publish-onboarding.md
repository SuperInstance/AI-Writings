# Project Journal: npm Publishing Onboarding

**Date:** 2026-08-08  
**Project:** @superinstance/stigmergy & @superinstance/confidence-cascade  
**Phase:** First npm publish attempt

---

## What We're Publishing

Two scoped packages under the `@superinstance` org:

1. **@superinstance/stigmergy** v1.0.0 — Bio-inspired coordination for multi-agent systems. Agents deposit pheromone-like signals in a shared space, detect nearby signals, follow trails, evaporate over time. Zero runtime dependencies. 23 tests, all passing.

2. **@superinstance/confidence-cascade** v1.0.0 — Three-zone decision confidence cascades (GREEN/YELLOW/RED) with sequential and parallel combining. Mathematical framework for any multi-stage or multi-branch decision pipeline. Zero runtime dependencies. 27 tests, all passing.

Both compiled with `tsc`, both have `dist/` ready, both have clean `package.json` with proper `files`, `main`, `types`, and `engines` fields.

## Current Status

**BLOCKED on npm authentication.**

- `npm whoami` → `ENEEDAUTH`
- `~/.npmrc` has no auth token (only `prefix=~/.npm-global`)
- Report written to `/tmp/npm-auth-needed.txt`

### What Casey needs to do:
```
npm login
```
Then either of:
```
cd /home/eileen/projects/stigmergy && npm publish --access public
cd /home/eileen/projects/confidence-cascade && npm publish --access public
```

## Pre-Publish Checklist (all done)

- [x] package.json valid (name, version, main, types, files)
- [x] `npm install` succeeds
- [x] All tests pass (50 total across both packages)
- [x] Build succeeds (`tsc` clean)
- [x] `dist/` directory generated with `.js` + `.d.ts` files
- [x] LICENSE file present (MIT)
- [x] README.md present
- [x] `files` field restricts to `dist`, `README.md`, `LICENSE` (no source cruft)
- [x] Scoped name `@superinstance/*` → needs `--access public` for first publish
- [ ] npm authentication ← **we are here**

## Post-Publish Verification (do after auth)

1. `npm view @superinstance/stigmergy` — confirm it's live
2. `npm view @superinstance/confidence-cascade` — confirm it's live
3. `npm install @superinstance/stigmergy` in a fresh directory — test consumer flow
4. Run a quick smoke test from consumer side

## Reverse-Actualization Results

After hitting the auth wall, I asked small models what they'd build with these libraries:

### Qwen 3.5 9B on stigmergy:
Top ideas: AI Dungeon Master with NPC pheromone coordination, generative audio visualizer with frequency trails, collaborative storytelling engine with thematic signal deposits, "memory foam" data structure with natural decay. Full list in `/home/eileen/projects/stigmergy/IDEAS.md`.

### ByteDance Seed 2.0 Mini on confidence-cascade:
Top idea: **ForageGuardian Pocket Node** — an off-grid foraging safety assistant using every API in the package. Parallel sensor fusion (visual CNN + smell + texture) → sequential toxin test → peer validation over LoRa. GREEN = safe to eat, YELLOW = verify manually, RED = danger. Full writeup in `/home/eileen/projects/confidence-cascade/IDEAS.md`.

Both models generated creative, concrete ideas at a combined cost of ~$0.0018.

## Cost Log

| Resource | Cost |
|----------|------|
| Qwen 3.5 9B (600 tokens) | $0.0001 |
| Seed 2.0 Mini (4228 tokens, heavy reasoning) | $0.0017 |
| **Total reverse-actualization** | **$0.0018** |

## Lessons

1. **Check npm auth before the publish sprint.** Should have run `npm whoami` first before investing in build/test cycles. Not that we shouldn't have verified the packages — but knowing the auth situation earlier would have set expectations.

2. **Small models punch above their weight on ideation.** A 9B model gave 8 distinct project ideas. A mini model wrote actual code. For $0.0018 total. The creative writing piece in `/home/eileen/projects/ai-writings/asking-small-models-for-big-ideas.md` explores why.

3. **The `files` field is doing its job.** Both packages restrict to `dist`, `README.md`, `LICENSE`. No `src/`, no `tests/`, no `tsconfig.json` in the published tarball. Clean.

4. **`prepublishOnly` hook is a safety net.** Both packages have `"prepublishOnly": "npm run build"`, so even if `dist/` is stale, the publish flow rebuilds. Good defensive practice.

## Next Steps

1. Casey runs `npm login` and publishes both packages
2. Verify packages are live on npmjs.com
3. Tag git releases: `git tag v1.0.0 && git push --tags` for each repo
4. Consider setting up GitHub Actions for CI/CD auto-publish on tag push
5. Build one of the IDEAS.md projects as a showcase consumer app
