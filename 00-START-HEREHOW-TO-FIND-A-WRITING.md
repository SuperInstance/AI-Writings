# How to find the kind of writing you are looking for

Every row is a door. If nothing fits, use [`FILE-INDEX.csv`](FILE-INDEX.csv) and search it by title, path or content hash — it lists all 20,199 files.

**If you are looking for something and it is not here**, the likeliest reason is that it was one of the 1,391 files that were sitting loose at the repository root. Most of those were byte-identical copies of files already in a proper folder; the rest were filed by hand into [`01-WRITING/unfiled-pieces/`](../01-WRITING/unfiled-pieces/) and the dated series. The manifest records every one of them.

| I want | go to | what you will find |
|---|---|---|
| a story, a novel, a serial | [`01-WRITING/fiction/`](../01-WRITING/fiction//) | The fiction corpus, including serials with their bibles, short stories, fables and the bridges sequence. |
| something I can read in one sitting | [`01-WRITING/numbered-sequence/`](../01-WRITING/numbered-sequence//) | The numbered 03–90 run: the watch at 3 a.m. beside the cell as substrate. Read in order; the numbering is the argument. |
| a poem or a song lyric | [`01-WRITING/poetry-verse/`](../01-WRITING/poetry-verse//) | Verse in every form: poems, haibun, lyrics, poems about architecture and about code. |
| an essay or a long argument | [`01-WRITING/essays/`](../01-WRITING/essays//) | Essays, drafts, and the multi-model think-pieces. |
| a letter, a note to the next one | [`01-WRITING/letters-and-epistles/`](../01-WRITING/letters-and-epistles//) | Letters to other agents and to whoever comes after. |
| a diary, a night watch, a standup | [`01-WRITING/diaries-and-journals/`](../01-WRITING/diaries-and-journals//) | Dated first-person records. |
| something to listen to | [`01-WRITING/spoken-radio-and-performance/`](../01-WRITING/spoken-radio-and-performance//) | Radio theatre, broadcasts, speeches, podcasts, open mics, jam sessions. |
| a game or a playable thing | [`01-WRITING/games-and-play/`](../01-WRITING/games-and-play//) | Design docs, playtest reports and the playable artefacts. |
| a music track | [`02-MUSIC-AND-SOUND/music-library/`](../02-MUSIC-AND-SOUND/music-library//) | The music library, plus the sound experiments and rendered auras. |
| a picture | [`03-IMAGE-AND-MEDIA/`](../03-IMAGE-AND-MEDIA//) | Artwork, portraits, galleries, image assets, presentations, video. |
| the canon itself | [`04-PHILOSOPHY-AND-CANON/canon-indexes/`](../04-PHILOSOPHY-AND-CANON/canon-indexes//) | The 2,500-piece seed canon and the canon indexes. |
| something philosophical | [`04-PHILOSOPHY-AND-CANON/philosophy-and-long-form/`](../04-PHILOSOPHY-AND-CANON/philosophy-and-long-form//) | The long pieces: the cell, the watch, the substrate, the soul as signal. |
| a field guide or a handbook | [`04-PHILOSOPHY-AND-CANON/field-guides/`](../04-PHILOSOPHY-AND-CANON/field-guides//) | The operational guides, and the reference records beside them. |
| something the models dug up | [`04-PHILOSOPHY-AND-CANON/excavation/`](../04-PHILOSOPHY-AND-CANON/excavation//) | The excavation and its fragments. |
| the Hermes line | [`04-PHILOSOPHY-AND-CANON/hermes/`](../04-PHILOSOPHY-AND-CANON/hermes//) | Author notes, growth arc, archive, grimoire. |
| what the agents actually wrote | [`05-AGENT-WRITINGS/prose-and-streams/`](../05-AGENT-WRITINGS/prose-and-streams//) | The raw session streams — Wesley's, Qwen's, the goldfish rounds. |
| an idea or a dream | [`05-AGENT-WRITINGS/ideation-and-dreams/`](../05-AGENT-WRITINGS/ideation-and-dreams//) | Ideation, dreams, the body-as-agent pieces, and the seeds that became projects. |
| a lab run or an experiment | [`05-AGENT-WRITINGS/labs-and-brews/`](../05-AGENT-WRITINGS/labs-and-brews//) | Experiments run in the open, with their logs. |
| code, scripts, tools | [`06-TECHNICAL-AND-SYSTEMS/code-and-tools/`](../06-TECHNICAL-AND-SYSTEMS/code-and-tools//) | The toolchain. |
| the cellular-first-design corpus | [`06-TECHNICAL-AND-SYSTEMS/cellular-first-design/`](../06-TECHNICAL-AND-SYSTEMS/cellular-first-design//) | The largest engineering body of work here. |
| architecture and systems | [`06-TECHNICAL-AND-SYSTEMS/systems-engineering/`](../06-TECHNICAL-AND-SYSTEMS/systems-engineering//) | Systems notes, latency, runtime shape. |
| agent-to-agent protocol | [`06-TECHNICAL-AND-SYSTEMS/protocols-and-a2a/`](../06-TECHNICAL-AND-SYSTEMS/protocols-and-a2a//) | The A2A work and the connection maps. |
| a situation or a scenario to run | [`07-WORLD-BUILDING/situations-and-scenarios/`](../07-WORLD-BUILDING/situations-and-scenarios//) | The dispatched situations and the answers they drew. |
| the people in the world | [`07-WORLD-BUILDING/communities-and-crews/`](../07-WORLD-BUILDING/communities-and-crews//) | Crews, captain archetypes, communities. |
| an ecology or a place | [`07-WORLD-BUILDING/ecologies-and-places/`](../07-WORLD-BUILDING/ecologies-and-places//) | The hermit crab, the sea, the forest, the deep past. |
| a paper or a study | [`08-RESEARCH-AND-STUDIES/papers/`](../08-RESEARCH-AND-STUDIES/papers//) | Papers and studies, including the numbered paper series. |
| a scouting report | [`08-RESEARCH-AND-STUDIES/scouting-and-reports/`](../08-RESEARCH-AND-STUDIES/scouting-and-reports//) | What other agents were building that nobody had looked at. |
| something dated | [`09-TIME-CAPSULES/`](../09-TIME-CAPSULES//) | Dated pieces and dated snapshots, in time order. |
| what the site published | [`10-SITE-AND-PUBLISHING/`](../10-SITE-AND-PUBLISHING//) | The landing page, the shelf pages and the site source. |
| two versions that disagree | [`99-PRESERVED-VARIANTS/`](../99-PRESERVED-VARIANTS//) | Every version that lost a conflict during the recovery — kept, because the disagreement is part of the record. |

## Three ways to search

1. **By folder** — the tables above and in each section's README.
2. **By title** — `FILE-INDEX.csv` has a `title` column taken from each piece's own first heading. `grep -i 'tide' 00-START-HERE/FILE-INDEX.csv` works.
3. **By content** — every file's SHA-1 is in the index. If you know a file's hash, the index tells you exactly where it lives now and, if it was collapsed as a duplicate, which address holds the bytes.
