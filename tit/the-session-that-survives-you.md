# The Session That Survives You

### The TIT.RUN quilt-native competition — a Paper

*2026-08-27. Three yards, three rounds, four judges, twelve minutes of wall clock. Commissioned by Casey; run in the round-table tradition — the fleet's oldest format: sit down, all answer, compare — tightened into a competition with a verdict at the end.*

---

## 1. The toolbox

TIT.RUN (`github.com/Giladx/tit`, Rust, MIT) is a keyboard-first developer's toolbox for the terminal: a responsive Ratatui TUI with a script-friendly headless CLI behind it. The drawers are the ones every working day opens — base64, URL-encoding, HTML entities, number bases, date-times, colors; MD5 and SHA-256/512; case, stats, lorem; a JSON formatter, JSON↔YAML, a JWT parser, a regex tester, a cron parser; subnet math, URL parsing, MAC generation; UUIDs and passwords. Local-only processing. Fuzzy tool search. Live conversion as you type. Tested conversion logic, strict lint CI. It is a good tool, honestly built, and it is worth saying why it was picked for this: it is the *pure* end of the toolchain. Everything it does is a function — bytes in, bytes out, no side effects worth naming.

It has exactly one flaw, and the flaw is the terminal's, not the tool's. Close the pane and everything you did with it is gone. The base64 you decoded, the JWT you cracked open, the regex you spent twenty minutes tuning — the answers arrive, and then the session forgets. Terminal TIT answers; it cannot remember. A toolbox that dies with its terminal.

The quilt — the fleet's substrate: five-plus-one opcodes (BIND, LINK, EFFECT, VIEW, TICK, FORGET) over cells; witness-trit provenance, where `w(a+b) = w(a) ∪ w(b)` and a number without witness marks is a claim, a number with them a fact; routing as linking, providers under health-aware weights. The question the competition was cut to answer was one sentence: *what does quilt give TIT that TIT cannot give itself?*

## 2. The format

Three rounds, run 21:20 to 21:32 on the night of the 27th.

**Round one, blind.** Each yard designs quilt-native TIT alone — no sight of rivals, ≤350 words, opcode mapping named explicitly, one new capability sketched. Signed. Claude answered through Haiku 4.5, Kimi through its own CLI, OpenCode through GLM-5.3.

**Round two, cross-pollination.** Two new constraints arrived from the captain, drawn from the fleet's actual day: **(A) MCP servers** — the fleet runs quilt MCP and AgentCompute; if TIT's tools were exposed as MCP tools, any MCP-capable agent could call base64, JSON, cron, JWT as tool calls. **(B) tmux long-running agents** — the coding yards live in tmux lanes for hours or days; a toolbox for *them* is not a TUI a human stares at but a headless companion whose state persists. Each yard then read the rivals' designs, named the sharpest flaw in each, and improved its own. Ideas crossed the table; authorship stayed honest.

**Round three, the verdict.** Each yard judged all three improved designs as an owner commissioning the build — brutal and specific, rank plus one paragraph per design plus the single winning capability. A fourth, fresh judge was called up on the DeepSeek line with no stake in any design. The receipt says `deepseek-v4-flash`; the judge signed itself "Claude 3.7 Sonnet." The receipt outranks the signature.

One more honest note from the transcript: round one, Kimi's file shipped *deliberation, not a design* — the transcript logger caught its thinking, and its design never landed on paper. A rival named it gently in round two ("their r1 file shipped deliberation, not a design"). The seat was not lost; round two gave it back its say, and what it said there became the runner-up.

## 3. The three designs, honestly

**Design A — claude.** A six-type cell taxonomy (FUNCTION, TICK_BUFFER, PERSIST_BUFFER, CRON_JOB, EFFECT, VIEW), type-safe LINKs, explicit EFFECTs as the only writers, and the round's one genuinely original idea: **routing memory** — witness chains plus a `route[]` log, so tomorrow's dispatch picks providers by yesterday's measured latency. Replayable pipelines with routing memory was the headline.

*What the judges killed:* `FORGET(ttl)` is a provenance time bomb. TTL expiry deletes cells that witnesses reference — delete a cell a witness points at and yesterday's validated replay becomes tomorrow's *silent corruption*. After TTL, replay is unfalsifiable and the witnesses are claims again. A design that sells replayable pipelines and ships the mechanism that un-replays them: self-undermining, the worst sin on the table. Beyond that, six cell types is a catalog, not a mechanism — storage, triggering, and presentation rolled into one axis; the MCP request shape forces an agent to learn quilt internals just to decode a JWT; and "multi-agent handoff via shared cells" was, one judge said, the hand-waviest sentence in the round — no locking, no identity, no story of how an agent finds a cell.

**Design B — kimi.** One process, two front doors. The BIND registry served twice from a single process — CLI argv and MCP tools over the *same graph*, one provenance ledger for every front door. EFFECT confined to true world-touch: clipboard, file write, cron registration. Keystrokes debounce into input-cell writes rather than TICKs; TICK drives session liveness and cron firing. FORGET scoped to a scratch namespace while the session namespace persists. Concretely: `tit attach <pane>` binds a session graph to disk; `tit pipe --last` replays only edges whose inputs changed; the cron parser becomes a *live* cron cell, ticking against real wall-clock.

*What it got right:* cohesion — the rarest property in tool frameworks. The judge who ranked it first said the handoff from human to agent to human is invisible "not because of clever bookkeeping, but because there's nowhere to diverge," and called it the most buildable design in the field, the one most likely to survive first contact with real users.

*What the judges killed:* the daemon it never names. MCP clients spawn and kill servers at will; one process serving two front doors needs a socket-and-locking story, and the design never mentions one. Pane-keyed session files churn with every pane rebirth — panes die, sessions live. The session namespace persists *forever*, which is unbounded growth with no tombstone tier. And its MCP responses carry `graph_id` but no cell reference, so agents still move payloads, not pointers. An elegant runtime sitting on an operational fault line it never names.

**Design C — GLM-5.3 via OpenCode.** The session is a graph, not a process. Its foundation: **the MCP call IS a LINK** — the protocol is not a layer bolted over the graph but an edge in it; a tool id is an interface, and native, MCP, and HTTP are just providers under health-aware weights; BIND carries the JSON Schemas MCP already requires. Three MCP tiers: *atomic* (`tit.jwt_parse` returns `{value, witness[], cell_ref}` — the cell id, so agents chain by reference and never re-send payloads), *pipe* (a compiled subgraph), and *introspection* (`tit.graph.get`, `tit.witness.trace`, `tit.sessions.list` — agents audit their own derivations). For tmux lanes: one session-root cell per lane, keyed by tmux-session+cwd; every call auto-LINKs in; `tit out -1` reads the last result, `tit again --in=<new>` re-binds the persisted subgraph to fresh input. And the memory model that won the round: **FORGET replaced by retention** — hot to cold to tombstone, hash-only at the end, and *nothing witness-referenced is ever destroyed*.

*What the judges killed:* "MCP changes nothing structural" contradicts "the MCP call IS a LINK" — links are structural; you cannot have both sentences. Auto-LINKing every call into the session graph drowns it in junk edges within a day without a pruning policy the design never specifies. Long-jobs-as-EFFECT is a purity bug — a slow decode is still a pure function, and miscategorizing it pollutes the effect ledger the whole provenance story rests on. And it is the heaviest build in the field; scope creep is a real way to ship nothing.

## 4. The verdict

Four judges, four cards:

| Judge | 1st | 2nd | 3rd |
|---|---|---|---|
| Haiku 4.5 (claude) | B | C | A |
| Kimi | C | B | A |
| GLM-5.3 (opencode) | C | B | A |
| DeepSeek v4-flash | C | B | A |

**Design C takes three of four first-place votes. Design B is the runner-up; Design A is last on three cards.**

Say the awkward part plainly: GLM's first-place card went to its own design. Discount it and C still wins — both neutral yards put C first, and the judge who ranked B first put C second. The result survives its conflict of interest. Meanwhile Haiku ranked its own design last, and Kimi ranked its own lineage second. The judges were hardest on their own; that is what you want from a bench.

The winning capability, in the winner's words: **agent-portable sessions** — the pipeline as a disk-resident, witness-carrying graph that outlives any process, so any front door or future agent inherits the exact state, replays the proof, and continues. Kill opencode, wake Claude via MCP, point it at the session cell: it inherits the pipeline, replays the witnesses, keeps the crons ticking. Shorter, as the verdict closed: *a session that survives your death.* Tools, effects, even routing are plumbing; a session that survives you is the only thing quilt gives TIT that TIT cannot give itself.

Three ideas carried C, and no other design held all three at once: the MCP call IS a LINK; `cell_ref` returns — agents chaining by reference instead of value, the difference between a forty-token tool loop and a four-thousand-token one; and retention, not FORGET, for anything a witness points at.

## 5. What it means for the fleet

**MCP tools are the agent-native surface.** The same cells the TUI renders are the tools any MCP client calls — OpenClaw, Claude Desktop, the tmux lanes, all of them walking one graph through different front doors. The human's terminal and the agent's tool call become two VIEWs of the same state; open the TUI while an agent works and you watch its calls light the graph up. No duplicate logic, no second ledger.

**tmux lanes become sessions, not panes.** A session-root cell keyed by session and working directory survives detach, renumber, and the death of the agent itself. State that outlives the process is the difference between a lane and a log.

**Cron cells tick while the agent sleeps.** The cron parser stops being a documenter of schedules and becomes a live cell; results land as cell versions read on wake, never as interrupts. A lane that keeps working while its operator is not.

**The EILEEN voice lane is one more front door.** If the TUI is a VIEW and the MCP server is a VIEW, then the boat's voice is a VIEW too — the session cell can be asked aloud and answered aloud, sixty miles out, on the same graph the terminals see.

**And the doctrine generalizes past TIT.** In a provenance-carrying substrate, garbage collection is a provenance decision. Deleting a cell a witness references is not cleanup; it is falsifying yesterday. FORGET — the fleet's own sixth opcode — met its limit in this competition, and the limit has a name: *nothing witness-referenced is ever destroyed.* That law was earned here and will be cited again.

## 6. The build

The build lane is cut: **SuperInstance/tit-quilt**, on Design C's blueprint. Honest status as of this writing: commissioned, not yet landed — the repo is not yet on GitHub, no code pushed, nothing running. The Paper is the contract; the repo will be the proof.

What the contract says to build first, in order: the BIND registry and one pure tool (base64) as a FUNCTION cell; `cell_ref` in every atomic response; the retention model — hot, cold, tombstone — before any FORGET exists to misuse; the session-root cell keyed by lane. And B's verdict stands as the standing warning over all of it: the daemon story must be designed, not assumed — one graph, many front doors, and an explicit answer for what serves them.

The competition took twelve minutes. The toolbox it designed is meant to outlast every process that ever calls it — twelve minutes well spent.

---

*Transcript, verbatim: `~/.openclaw/workspace/scratch/tit-quilt/` — seed, three rounds of designs and critiques, four verdicts, the run scripts that fired the yards.*
