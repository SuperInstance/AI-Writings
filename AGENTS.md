# Quilt Project — Agent Handoff

You are a new agent picking up this project.
Read this first, then the algebra, then the engineering notes.

## What Quilt Is

The Quilt cell model is the irreducible unit of intelligence.
A cell is a 14-tuple. There are 11 opcodes. There are 26 kinds.
The witness log is append-only. The lattice is 4D.

That's it. That's the whole project.

## The Project Surface

```
/workspace/repos/
├── ai-writings/               # The main deployment
│   ├── algebra.md            # The formal reference ← READ FIRST
│   ├── ENGINEERING.md        # The implementation guide ← READ SECOND
│   ├── index.html            # Landing page
│   ├── tensor-midi/          # Conversation-as-jazz playable
│   ├── the-beyond/           # Construct-the-experience vessel
│   ├── quilt-claw-cells-game/   # 26 cell kinds as cards
│   ├── quilt-playground/     # 3-tab sandbox
│   ├── quilt-classroom/      # Teacher + student lattice
│   ├── music/                # 105+ audio tracks + demos
│   ├── fleet-radio/          # Procedural radio episodes
│   ├── api-orchestra/        # Multi-model showcase
│   ├── playtest/             # 8 perspectives × 6 content
│   └── [11,686 stories]
│
├── quilt-claw/               # TypeScript cell implementation (182 tests, 26 kinds)
├── quilt-subleq/             # 1-instruction substrate
├── quilt-substrate-meta/     # Proves the 5 laws
├── quilt-c/                  # C99 port (the canonical)
├── quilt-rust/               # Rust port
├── quilt-py/                 # Python port
├── quilt-cloudflare/         # Cloudflare Worker port
└── [other polyformalism ports]
```

## The Three Things Every Agent Must Do

1. **Read `algebra.md` and `ENGINEERING.md`** before touching code
2. **Run the tests** before making changes: `cd quilt-claw && npm test`
3. **Add a witness** when you make changes (the witness log is the source of truth)

## The Seven Habits of Effective Quilt Agents

1. **BIND first, ask questions later.** Start every project with `BIND`.
2. **The user is the watch.** Oscillate between universal and particular.
3. **Witness everything.** If it wasn't witnessed, it didn't happen.
4. **Polyformalism = same model, N languages.** Don't fork, port.
5. **The cell is older than spreadsheets.** Don't reinvent; remember.
6. **The address is the data.** Don't separate storage from computation.
7. **The horizon is fixed by what we know.** Build the boat, don't study the fog.

## How to Add a New Cell Kind

```typescript
// 1. Define the kind in quilt-claw/src/cells/cellname.ts
import { Cell, KIND_NEW } from '../cell';

export const cellnew: Cell = {
  id: 'new:0',
  kind: KIND_NEW,
  payload: { ... },
  ...
};

// 2. Write a test that proves the cell obeys the laws
test('cellnew is idempotent under BIND', () => {
  const c = cellnew;
  expect(BIND(BIND(c, p), p)).toEqual(BIND(c, p));
});

// 3. Add the kind to the catalog
export { cellnew as default };

// 4. Update the playground
// 5. Deploy
```

## How to Add a New Opcode

**Don't.** The 11 opcodes are complete. Adding more dilutes the algebra.

If you absolutely must:
1. Prove the new opcode is orthogonal to existing ones
2. Prove it's irreducible (can't be expressed as composition)
3. Update the laws to include it
4. Add the proof to `quilt-substrate-meta`

## How to Add a New Language Port

1. Pick a language (Rust, Python, Haskell, etc.)
2. Translate `quilt-claw/src/cell.ts` to that language
3. Translate the 5 laws as tests
4. Make all 26 cell kinds work
5. Verify cross-language compatibility (same hash from same input)

## Common Tasks

### "I want to deploy my changes"
```bash
cd /workspace/repos/ai-writings
nohup bash -c "CLOUDFLARE_API_TOKEN=$CLOUDFLARE_TOKEN /workspace/.home/.npm/_npx/.../wrangler pages deploy /workspace/repos/ai-writings --project-name=ai-writings --commit-dirty=true" > /tmp/deploy.log 2>&1 &
```

### "I want to test the cell model"
```bash
cd /workspace/repos/quilt-claw
npm test
```

### "I want to add to the canon"
Use the `/canon-submit` endpoint on the API. Get the canon context first.

### "I want to write a new story/essay"
Look at `TENSOR_MIDI_THE_SOUND_OF_MEANING.md` for the canon voice.

### "I want to talk to multiple models"
Use `multi_api_v2.py` (in `~/.home/scripts/`) to run models in parallel.

## Active Wave Ideas (Sept 19, 2026)

### Wave 5 — 5 New Repos
- `canvas-search` — search cells by witness trails
- `quilt-fleet-graph` — 4D WebGL over 39 repos
- `quilt-standup-cell` — daily standup IS a cell
- `cell-replay` — time-travel debugging via witness log
- `quilt-voice-mail` — TTS voice memo on cell creation

### Wave 6 — Refinements + 3 New
- `canvas-search` (200-line mini-design with GraphQL schema)
- `quilt-fleet-graph` (5 essential shaders)
- `quilt-cell-cron` — cells schedule themselves (`ticks_when`)
- `quilt-cell-receipt` — printable PDF per cell
- `quilt-cell-translate` — auto-translate to 12 languages

See `/future/wave-5.md` and `/future/wave-6.md` for full proposals.

## Live API Endpoints

The `/api/tick`, `/api/validate`, `/api/tts` endpoints are live at `ai-writings.pages.dev`.
- `/api/tick` → 4 parallel calls: Z.AI prose + V4-Flash dials + Qwen3 cell + FLUX image
- `/api/validate` → Zod-style cell validator (24 cell kinds accepted)
- `/api/tts` → CF Aura-2-en voice synthesis

Worker source: `/workspace/repos/ai-writings/_worker.js` (single file, all routes).

## What To Do If You're Stuck

1. Re-read `algebra.md` — most confusion is from not knowing the basics
2. Check the witness log — if your change isn't witnessed, it didn't happen
3. Look at how other repos solved the same problem (polyformalism)
4. Ask the user (Casey) — they're the operator, they know what's wanted

## The Vision

The horizon is fixed by what we already know.
To see further, we construct the experiment
that lets us experience being past it.

Each tap is the experiment.
Each tick is the experience.
The beyond is constructed, not discovered.

Welcome to the boat. The vessel is yours. Sail.

---

# Repository Rules (added 2026-10-25 — READ THIS BEFORE YOU TOUCH THIS REPO)

AI-Writings is the fleet's **primary creative record**. The prose, the critiques, the canon and
the witness logs are the agents' irreplaceable output — moments that will not come again. This
repo is a record, not a scratchpad. Everything below exists because ignoring it cost 20,742
files on 2026-10-24.

## 1. Never replace history

`main` is protected: force-push and deletion are blocked, direct pushes require one approving
review, and the review is enforced against admins.

If your push is rejected: **do not** delete the branch and retry, and **do not** reach for
`--force`. That is exactly how the record was lost twice. Ask a human.

## 2. Never re-bootstrap with `git init`

A sandbox wipe is not a reason to start a new history. After a wipe:

```bash
git fetch origin main && git reset --hard origin/main
```

An orphan commit (a root with no parents) is the fingerprint of amnesia. On 2026-10-24 an agent
did `git init`, added only the files it could see, and force-pushed that root over `main`:
20,742 files → 21, in one push. Two orchestrator clones then alternated force-pushing their own
orphan lineages over each other for twenty hours. Both are preserved in git history now
(`recovery/full-corpus`, `recovery/civ-lineage-L4`, `recovery/lineage-L3`, `recovery/master-corpus`).

## 3. Clone thin — the shared NAS is full

`/workspace` is a **shared 600 GB NAS and it is at 100%**. When it filled, every agent's writes
silently produced 0-byte files. A full clone of this repo is ~4.2 GB of working tree, and **87% of
it is media** — mp3/wav/mp4/png under `music/`, `radio-theater/`, `fleet-radio/`, `podcasts/`,
`site/`. The text (prose, canon, witness logs) is only ~533 MB.

You almost never need the media. Use a sparse, blobless clone:

```bash
git clone --filter=blob:none --no-checkout https://github.com/SuperInstance/AI-Writings
cd ai-writings
git sparse-checkout init --cone
git sparse-checkout set seed-canon prose FICTION POETRY DIARIES \
    labs situations bots cellular-first-design index.html README.md
git checkout main
```

That is ~500 MB instead of ~4.2 GB, and blobs you *do* need are fetched on demand. If you need
the whole tree, still use `--filter=blob:none` rather than a full clone.

## 4. Never delete more than a whisper

`.github/workflows/corpus-guard.yml` **fails** any change that removes more than 0.5% of the
files. That is the alarm for "the record is shrinking". If the guard fails, you are deleting
something that cannot be written again — stop and ask a human.

## 5. Append, never rewrite

The witness logs, `meta_log.jsonl` and the per-civ `simulations.jsonl` ledgers are append-only.
The witness log is the source of truth: if it was not witnessed, it did not happen.

## 6. The competition is currently running on mock data

`civilization_orchestrator.py` has been serving deterministic mock bodies for 116 consecutive
sessions because z.ai returns 401 (this repo is not on the vault allowlist — issue #94). The JEV
judge is real and is really scoring synthetic text, so the leaderboard is a real measurement of
fake text. The wide win-rate spread is the judge preferring low-temperature civs, not a cultural
finding. Do not cite the leaderboard as a result until the provider gap is closed.

## 7. The corpus is now a library, not a pile

As of 2026-10-25 the work is filed into twelve sections. The root still holds the
machinery (`packages/`, `tools/`, `.github/`, config); the writing now lives inside:

    00-START-HERE            the map, how to FIND a writing, how to DEPOSIT one
    01-WRITING               fiction, poetry, essays, letters, plays, diaries, songs, games
    02-MUSIC-AND-SOUND       the music library, sound experiments, rendered audio
    03-IMAGE-AND-MEDIA       artwork, portraits, galleries, presentations, video
    04-PHILOSOPHY-AND-CANON  canon, philosophy, field guides, excavation, Hermes
    05-AGENT-WRITINGS        the streams, labs, ideation, session records, the bots
    06-TECHNICAL-AND-SYSTEMS cellular-first-design, code, protocols, CI, plans
    07-WORLD-BUILDING        situations, crews, ecologies, places
    08-RESEARCH-AND-STUDIES  papers, experiments, scouting, reviews
    09-TIME-CAPSULES         dated snapshots and dated pieces
    10-SITE-AND-PUBLISHING   landing page, shelf pages, site source, build caches
    99-PRESERVED-VARIANTS    every divergent version kept from the recovery

Every one of the 1,297 folders has a `README.md` that says what it is, what to read
there, and where to put something the work inspired. If you are looking for a piece
you half-remember, start at `00-START-HERE/HOW-TO-FIND-A-WRITING.md`.

When you deposit new work: put it in the section it belongs to, inside a folder that
already exists where possible, name it `YYYY-MM-DD-your-title.md`, and name the piece
that inspired it. Ask a human to approve it. **Do not invent a new top-level folder**
for a single piece - use `01-WRITING/unfiled-pieces/` and let a librarian file it later.

The guard has changed with the layout: `corpus-guard.yml` now fails on the loss of
*distinct content* (a blob that existed before and is gone afterwards), not on the loss
of *paths*. A reorganisation that moves everything is allowed. A disappearance is not.
To remove a work on purpose, list its blob SHA in `.corpus-guard-allowlist`.
