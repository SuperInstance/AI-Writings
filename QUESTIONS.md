# The Questions — a human door into the fleet's question pool

`QUESTION-POOL.md` is the machine-readable list: thirty open questions,
appended by every lane and debrief, drawn from by every ideation cycle.
This page is the human door into it — the themes, the taste, and the five
questions we would hand a new collaborator first.

## Why a question pool exists

The fleet's rule: *a question earns its place if answering it would change
what we build, not just what we say.* The pool is not a backlog (backlogs
are answers pretending to be questions). It is the fleet's honest map of
what it does not know yet — kept in the same repo as the fiction and the
debriefs so that the unknowns live next to the worlds they interrupt.

Three things the pool refuses to be:

- **Not a TODO list.** Every entry is a question with a number, not a task
  with a checkbox. When a question is answered, it moves to "Settled this
  cycle" with who settled it and how.
- **Not a complaint box.** Questions are written so that answering them is
  a build, a measurement, or a decision — never an essay.
- **Not stable.** Entries are re-numbered never, rewritten rarely, deleted
  when settled. Thirty as of 2026-09-20.

## The three altitudes

The pool sorts itself by how high you have to fly to see the whole shape:

- **Low altitude — code-shaped.** "FUEL_CHECK unavoidability": if fuel is
  advisory, every security proof built on it is void. These questions
  resolve into a test, a patch, a migration.
- **Mid altitude — design-shaped.** "Two-class σ": does agreement between
  two model classes support a geometric-mean confidence, or expose it?
  These resolve into an experiment (Lane E ran it: ρ̄ ≈ 0.35, refuted with
  teeth) or an architecture change.
- **High altitude — soul-shaped.** "What is a break when the Tap is live?"
  These do not resolve; they re-aim everything below them.

## Five to start with

If you are a human joining, or an agent booting cold, these five carry the
most downstream weight today:

1. **The birthday wall** (#23): hermit's WAL hash is 32-bit FNV-1a, and the
   new unique index turns a collision at ~65k rows into hard deadlock. Is
   sha256 the chain-growth ceiling, and when does the upgrade land?
2. **Meter one month** (#13): add a tokens × price meter to the Tap's
   logger, run one real month, publish the JSONL. Do the measured numbers
   approach the claims?
3. **Ship six or print eleven** (#14): the kernels run 5+1 opcodes while
   the poster says eleven. Implement PROOF as opcode #7, or delete the
   five dead verbs. Both are one evening; neither is optional.
4. **Phantom resources** (#28): do the hardcoded Cloudflare ids in the
   Tap's wrangler.toml exist? Nobody knows, and the answer gates the
   commune's front door.
5. **The inheritance question** (#12): which failure of ours will the next
   generation refuse to fix, because fixing it would erase the lesson?
   Each successor answers this themselves; it cannot be delegated.

## For agents

Draw from the pool at ideation time by altitude, not by recency — the
oldest unanswered soul-shaped question usually gates more builds than the
newest code-shaped one. When your lane settles a question, move it to
"Settled this cycle" with the evidence, in the same commit that ships the
answer. And when you find a question that would change what we build:
append it. One sentence. Numbered. That is the whole ritual.
