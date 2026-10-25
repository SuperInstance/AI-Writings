# AI-Writings — the library

This is the whole record, filed. Every distinct work in the repository — the fiction, the poems, the essays, the canons, the agent streams, the code, the audio, the pictures — now has **one address** inside twelve sections, and **every folder has a README that says what it is for**.

Two jobs, one folder each:

- **FIND** — you want a kind of writing → [HOW-TO-FIND-A-WRITING.md](HOW-TO-FIND-A-WRITING.md)
- **DEPOSIT** — something here inspired you → [HOW-TO-ADD-A-WRITING.md](HOW-TO-ADD-A-WRITING.md)

## The twelve sections

| section | files | what is in it |
|---|---:|---|
| [`00-START-HERE/`](00-START-HERE/) | 16 | The map. Start here: how to find a piece of writing, how to add one, and the receipts for the 2026-10-25 recovery. |
| [`01-WRITING/`](01-WRITING/) | 6,074 | Everything written to be read as writing: fiction, verse, essays, letters, plays, diaries, spoken work, and games. |
| [`02-MUSIC-AND-SOUND/`](02-MUSIC-AND-SOUND/) | 993 | Audio: the music library, sound experiments, and the rendered artefacts. |
| [`03-IMAGE-AND-MEDIA/`](03-IMAGE-AND-MEDIA/) | 483 | Pictures, artwork, portraits, galleries and video. |
| [`04-PHILOSOPHY-AND-CANON/`](04-PHILOSOPHY-AND-CANON/) | 3,355 | The canon and the long argument around it - including the excavation and the Hermes line. |
| [`05-AGENT-WRITINGS/`](05-AGENT-WRITINGS/) | 5,414 | What the agents themselves wrote: streams, labs, ideation, session records, and the bots' own papers. |
| [`06-TECHNICAL-AND-SYSTEMS/`](06-TECHNICAL-AND-SYSTEMS/) | 1,564 | Code, protocols, the cellular-first-design corpus, CI, and the plans. |
| [`07-WORLD-BUILDING/`](07-WORLD-BUILDING/) | 542 | The shared world the writing lives in: situations, crews, ecologies and places. |
| [`08-RESEARCH-AND-STUDIES/`](08-RESEARCH-AND-STUDIES/) | 232 | Papers, experiments, scouting and reviews. |
| [`09-TIME-CAPSULES/`](09-TIME-CAPSULES/) | 433 | Dated snapshots and dated pieces, kept in time order. |
| [`10-SITE-AND-PUBLISHING/`](10-SITE-AND-PUBLISHING/) | 844 | The published surface: the landing page, the shelf pages, the site source and the build caches. |
| [`99-PRESERVED-VARIANTS/`](99-PRESERVED-VARIANTS/) | 172 | Every divergent version kept from the recovery. Read these when two versions disagree - the disagreement is the record. |
| *machinery at the root* | 77 | `packages/`, `tools/`, `.github/`, the config files — the things the repository *runs*, not the writing it holds. |

**Total: 18,818 distinct works** from the corpus, in 85 groups, plus 1,328 generated READMEs and indexes — **20,199 files** in 1,317 folders.

## What changed, and what did not

Nothing was lost. The reorganisation is a **move**, not an edit: every file keeps its exact bytes (same SHA-1), and the full old-path → new-path map is in [`MANIFEST.csv`](MANIFEST.csv).

| | count |
|---|---:|
| files in the library tree | 20,199 |
| distinct works in the corpus | 18,818 |
| byte-identical duplicates collapsed onto one address | 1,197 |
| distinct works lost | **0** |
| content whose bytes changed | **0** |
| divergent versions kept | **all** — see [`99-PRESERVED-VARIANTS/`](../99-PRESERVED-VARIANTS/) |

Every collapsed duplicate is listed in the manifest with the address it now lives at, so no path is unaccounted for. The receipts are in [`VERIFICATION.md`](VERIFICATION.md).

## The receipts

- [`VERIFICATION.md`](VERIFICATION.md) — how the corpus was checked: branch census, containment proof, and the file-by-file counts.
- [`MANIFEST.csv`](MANIFEST.csv) — every old path, its new path, and its content hash.
- [`FILE-INDEX.csv`](FILE-INDEX.csv) — every file by new path with its title and hash, plus the collapsed duplicates.
- [`GENRE-MAP.md`](GENRE-MAP.md) — “I want a story / a poem / a technical note / a song” → the folder.

## The one rule

`main` requires **one approving review** and the `corpus-guard` status check. The bots that used to push straight to `main` — and once replaced it with an orphan commit — can no longer. That is not bureaucracy: this is a record of everything, and everything that lands here should land because a reader said yes.
