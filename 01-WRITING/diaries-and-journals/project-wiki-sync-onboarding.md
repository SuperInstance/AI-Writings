# Project Wiki Sync — Onboarding Notes

**Date:** 2026-08-08
**Project:** Fleet Wiki / Polln Extraction
**Status:** Complete

---

## What Happened

The polln extraction project reached its documentation phase today. Seven libraries — previously embedded subsystems inside the polln agent — were extracted as standalone repos and needed wiki pages on the fleet wiki.

## The Extraction Pattern

Polln was a monolithic agent that accumulated sophisticated internal machinery. Rather than letting that machinery stay locked inside one project, each subsystem was pulled out as a standalone library:

| Library | Language | Original Role in Polln |
|---------|----------|----------------------|
| confidence-cascade | TypeScript | Three-zone decision routing (GREEN/YELLOW/RED) |
| stigmergy | TypeScript | Indirect agent coordination via pheromone-like signals |
| platonic-randomness | TypeScript | Structured PRNG shaped by Platonic solid geometry |
| voxel-logic | TypeScript | 3D spatial reasoning over voxel grids |
| logtensor | Python | Proportional-navigation-inspired tensor attention |
| plato-spatial | Python | Hierarchical containment with DeltaTick propagation |
| flow-state | Python | Entropy-based anomaly detection via spline observers |

## Wiki Page Structure

Each page follows the same three-section pattern:

1. **What it is** — 2-3 sentences describing the library's purpose and mechanism
2. **Extraction from polln** — What role it played inside the original system, why it was coupled, and what motivated extraction
3. **Standalone value** — What it offers as an independent library, composition with other fleet libraries, and use cases beyond polln

## Technical Notes

### Wiki API
- Endpoint: `POST https://fleet-wiki.casey-digennaro.workers.dev/api/pages`
- Body: `{"slug": "...", "title": "...", "content": "...", "category": "..."}`
- All 7 pages accepted successfully
- Lesson learned: shell-escaping JSON with parentheses and apostrophes in single-quoted heredocs is fragile. Write JSON to temp files and use `curl -d @file.json` instead.

### Fleet Dashboard
- Updated `FLEET_REPOS` array in `worker.js` (lines 17-66)
- Now tracking 47 repos (was 40)
- Change committed and pushed to `github.com/SuperInstance/fleet-dashboard`

## Lessons for Future Onboarding

1. **Write content, not stubs.** Every wiki page should have enough substance that a new contributor can understand what the library does without reading the source. Two to three paragraphs of real explanation beats a one-liner every time.

2. **Document the extraction story.** Knowing *why* a library was extracted from its original host is often more valuable than knowing what it does. It tells you what problem the library was built to solve in practice, not just in theory.

3. **Note composition relationships.** Every page mentions which other fleet libraries it composes with. This creates a web of relationships in the wiki that helps newcomers understand the fleet as a system, not just a collection of parts.

4. **Temp files for JSON payloads.** When POSTing complex JSON via curl, always write to a temp file. Shell escaping will bite you otherwise.

5. **Update the dashboard in the same pass.** The fleet dashboard's `FLEET_REPOS` array is the canonical list of tracked repos. Any new repo should be added there as part of the wiki sync, not as a follow-up task.

## What's Next

- The wiki now has pages for all 47 fleet repos (or close to it — there may be gaps in older entries)
- The dashboard will pick up the new repos on its next GitHub API poll cycle
- Future extractions should follow the same pattern: extract → create repo → write wiki page → update dashboard → announce at The Tap
