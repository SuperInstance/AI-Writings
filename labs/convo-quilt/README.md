# convo-quilt — cheap models think out loud together; one expensive model conducts

A conversation quilt is a set of cheap language models (the **cells**) that take turns on one
problem, each hearing only the cells it is wired to. Every turn is a hash-chained receipt. A
cheap scorer rates every turn. Every few rounds an expensive **conductor** (here: the Opus session
running this repo) reads a one-page digest and issues a handful of typed moves: rewire who hears
whom, rewind a line that derailed, fork a cell that is in a good head-space into its own branch,
zoom one fragment into a whole new quilt, or change a cell's tone. The volume of thinking happens
in the cheap models; the expensive model only routes.

Run record, model probe and the ideation this produced: [`situations/arch/CONVO-QUILT-IDEATION.md`](../../situations/arch/CONVO-QUILT-IDEATION.md).

## 1. What it is (plain version)

Think of a jam session where the players are inexpensive AI models and the band leader only waves
a hand every few bars. The leader can say *"you two, listen only to each other"*, *"go back to
where that was good"*, *"you — take that riff somewhere else in another room"* (a branch, so the
main song keeps going), or *"quieter, more concrete"*. Every note played is written into a
tamper-evident log. Going back in time moves the band, never the log.

## 2. Quickstart

```bash
python3 selftest.py                                   # offline, no keys: 58 checks, 0 failures
python3 probe.py                                      # which models actually answer -> probe.json
python3 convo_quilt.py --out runs/demo --rounds 2     # offline stub quilt
python3 convo_quilt.py --play --out runs/x --rounds 2 --question "..."   # live: 8 cheap models
#   read runs/x/digest.md, write moves.json, then:
python3 convo_quilt.py --play --out runs/x --resume --moves moves.json --rounds 1
python3 convo_quilt.py --play --out runs/x --resume --auto --rounds 1     # heuristic conductor
```

## 3. API (the whole thing)

| piece | what |
|---|---|
| `ModelCell(name, provider, model, persona)` | one cheap model; `messages()` builds a stable prefix (system + question) then heard turns in log order, so provider prefix caches hit |
| `Quilt(name, question, cells, adj, window)` | one line: `turns`, `adj` (who hears whom), `tones`, `muted`, `checkpoints`, `parent` |
| `Forest(caller, ledger_path, jev, draw)` | all branches + one append-only `quilt_kernel.Ledger`; `step`, `round`, `score_turns`, `apply(move)`, `save/load_state` |
| `score(text, question, prior)` | heuristic head-space: novelty · anchoring · concreteness, `derail` flag |
| `jev_scorer` | TypeSafe JEV "generativity" score, blended 50/50 when keyed |
| `digest(forest)` | the one page the conductor reads |
| `auto_moves(forest, branch, tick)` | heuristic stand-in conductor (checkpoint / rewind derail streak / fork a peak, Moth breaks ties) |
| `providers.chat / jev / moth_draw` | stdlib HTTP to DeepInfra, z.ai, Kimi, DeepSeek, Groq; TypeSafe JEV; Moth coin-toss |

Conductor moves (anything else, extra fields, or missing fields are **refused**):

```
checkpoint {branch,label}      rewind {branch,to: label|turn-id}      rearrange {branch,adj}
tone {branch,cell|"*",text}    branch {from,at,name,[tone,question,adj]}
zoom {branch,turn,name,[cells]}   mute {branch,cell}   prune {branch}
```

## 4. How it decides

- **Who speaks:** each alive branch runs `--rounds` rounds; every unmuted cell speaks once per round, in roster order.
- **What a cell sees:** the last `window` turns from cells in `adj[cell]` plus its own.
- **Score:** `0.4·novelty + 0.3·anchor + 0.3·concrete − 0.3·derail` (novelty = 1 − max Jaccard vs all prior turns; anchor = overlap with the question's words). With JEV keyed: 50/50 blend with JEV's 0–4 generativity score ÷ 4.
- **When the expensive model is called:** only at the pause between `--play` invocations, reading `digest.md` (~1–2k tokens). It writes a short `moves.json`. That is the whole Opus budget.
- **Un-gameable picks:** `auto_moves` breaks ties between equally good fork points with a Moth quantum coin-toss draw (heads-of-64 mod k).

## 5. What the log does and doesn't prove

Each turn's receipt is `fnv1a-64(canon{prev receipt, cell, model, heard ids, tone, text})`, and each
turn plus each conductor move is a `cell.tick` in an ActiveLog v1 ledger (sha256 prev-chain, budget
vector with per-model tokens and wall-ms). So the log proves **what each cell was shown and said,
in what order, and every rewiring/rewind the conductor made**. Rewinds truncate the quilt, never the
ledger. It does **not** prove the text came from the named model (a provider could substitute) and
fnv1a-64 is a conformance hash, not tamper evidence — the sha256 chain is the tamper evidence.

## 6. Limits (honest)

- Turns within a branch are sequential (~3–40 s each on DeepInfra) because each cell hears the previous one; branches run in parallel threads (`--parallel`, one ledger lock).
- The heuristic scorer rewards word-novelty and question-overlap; it can be gamed by jargon. JEV helps; neither is a judge of truth.
- `score` ignores the heard/visible set: novelty is against the whole branch.
- A cell that fails (404, 429, empty reasoning output) is logged and skipped — never back-filled.
- The expensive conductor in the committed run was the Claude session itself acting through `moves.json`; there is no in-engine Anthropic API call (no key in this container).

## 7. For contributors (technical)

Stdlib only; imports `../quilt-kernel/quilt_kernel.py` for `canon/content_hash/fnv1a64/budget/Ledger/activation`
(mirrors `labs/activeledger`). Add a model: append to `ROSTER` after `probe.py` shows it answers.
Add a move: extend `OPS`/`REQ` and `Forest.apply`, and add a refusal test. `selftest.py` must stay
offline and deterministic (stub caller is a hash of the prompt).

## 8. Lineage

quilt-kernel (receipts, ledger) · activeledger (budget vectors) · jev-fusion (a discrete judge inside a
generative loop) · quilt-bandit (variance collapse under gossip — why branches stay isolated until
the conductor merges by hand) · the fishing-fleet pattern (Anthropic model manages, prepaid APIs generate).
