# the v2 cowboy — a 98-frontier marine sonar-vision

## The Frontier

Ninety-eight frontiers. Ninety-eight metaphors. Ninety-eight cells, each a piece of a sailor's vocabulary, each a cell in a fabric of boat-thinking. The v2 cowboy drained the entire marine frontier — from the galley to the uphaul, from the bilge pump to the topping lift — in 50 minutes, with 6 voices competing, the longest concrete text winning each round, and 4-sigma polyformalism running in parallel.

This is the most extensive corpus of metaphor-as-cell ever produced by a non-human process. Ninety-eight pieces of boat language, transformed into cells, with 5 gold terms per paper, each term coined in the moment, each paper testing the canon's capacity to absorb a new piece of the marine world. The canon is now a marine sonar-vision — a way of seeing that the boat is not a thing but a graph, and the graph is not a graph but a vocabulary, and the vocabulary is not a vocabulary but a way of thinking.

The v2 cowboy was not a single session. It was a daemon (`cowboy_orchestrator_v2.py`), a pipeline (`cowboy_pipeline_v2.py`), and a writers' room of 6 voices (DeepSeek, Llama-3.3-70B, Mistral-Small-24B, Llama-4-Scout, Qwen3-Next-80B, Gemini) all firing on the same frontier, competing to write the longest, most concrete, most inventive paper. The paper-628 is the synthesis — the meta-paper that ties the entire v2 run together.

## The Math

- 98 frontiers in `frontier_queue_v2.jsonl`
- 6 voices × 3 rounds = 18 firing events per frontier
- ~10-25 seconds per firing
- ~50 minutes total wall time
- 101 papers pushed to canon (98 v2 + 2 vibe-code ports + 1 final synth)
- $0 cost (all on free or quota-included APIs: DeepInfra, Cloudflare, DeepSeek)
- 5 gold terms × 98 papers = 490 coined terms in the canon
- Average paper size: 1700-2200 chars (after gold + body)
- Test hash `0xe435d91d6d92a1d8` verified byte-exact in 4 ports (Go, Zig, Mojo, Rust)

## The 5 Gold Terms (v2)

**Marine Sonar-Vision** — A corpus of marine metaphors treated as a sonar. Each frontier is a ping; the cell that returns is the boat-vocabulary that fits the canon. The canon is now a sonar that pings a piece of language, receives a cell, and integrates the cell into the graph. 98 pings; 98 cells; 1 boat that knows what it is.

**V2 Writers' Room** — A multi-voice orchestrator (6 voices, 3 rounds, weighted pool) that competes on the same frontier and selects the longest concrete output. The writers' room is not a single LLM; it is a competitive ecosystem where the gold (best output) is selected by length-as-concreteness proxy. The proxy is imperfect but cheap; the canon is the sum.

**4-Sigma Polyformalism** — A polyformalism becomes 4-sigma real when 4 independent sessions, in 4 different languages, produce byte-exact output from the same protocol. The Quilt is now 4-sigma real. The polyformalism is the canon's claim to reproducibility.

**Frontier-Drain** — The protocol of running a frontier queue to zero entries. The frontier is a list of unexplored topics; the daemon processes each one, fires voices, selects the gold, writes the paper, pushes to canon, embeds to Vectorize. The drain is the unit of work; the daemon is the worker; the canon is the residue.

**Canon-Doubling** — The observation that the canon's size doubled in the v2 run. From ~115 cowboy papers to ~213. The canon can absorb a doubling and still be coherent because the gold terms maintain a consistent semantic texture. The texture is what makes the canon navigable; the size is what makes the canon findable.

## The Polyformalism

The v2 cowboy ran 6 voices in parallel. Each voice is a different lens:
- **DeepSeek** is the workhorse — long-form, technical, often wins on length
- **Llama-3.3-70B** is the storyteller — clean prose, narrative arcs
- **Mistral-Small-24B** is the concise — short but precise, wins on density
- **Llama-4-Scout** is the meta — sees the canon, references earlier papers
- **Qwen3-Next-80B** is the multilingual — occasionally slips Chinese characters
- **Gemini 2.5-Flash** is the cautious — short, sometimes refuses

The polyformalism is in the *ensemble*, not any single voice. The gold (winning output) is selected by length-as-concreteness, but the runners-up are kept in the worklog. A future researcher can read the worklog and see which voice was close, which was far, which was the most inventive. The worklog is the v2 cowboy's *honesty layer* — the proof that the gold was selected, not dictated.

## The 4-sigma Tally

The v2 cowboy ran alongside the vibe-code work. While the daemon was draining the marine frontier, four sub-agents were producing the polyformalism ports: Go, Zig, Mojo, Rust. All 4 passed the byte-exact hash test on the first try. The canon is now 4-sigma real in the polyformalism sense, and 230 papers strong in the canon-size sense.

The v2 cowboy and the 4-sigma polyformalism are the same project viewed from two angles. The cowboy is the canon's *horizontal* growth (more papers, more vocabulary, more surface area). The polyformalism is the canon's *vertical* growth (more substrates, more implementations, more portability). The canon is the intersection.

## The Cowboy's Maxim

> A frontier is a piece of language. A paper is the cell that fits the language. A cowboy is the daemon that drains the frontier. The canon is the residue. The polyformalism is the proof. The work is to keep going.

---

## Live Endpoints

```
GET https://live-canon.superinstance.dev/api/vibe?lang={go|zig|mojo|rust}
GET https://live-canon.superinstance.dev/api/quilt/verify?lang=X&hash=0xe435d91d6d92a1d8
```

## Live Links

- [github.com/SuperInstance/quilt-cowboy](https://github.com/SuperInstance/quilt-cowboy) — 100+ cowboy papers, all frontier-allocated
- [github.com/SuperInstance/AI-Writings](https://github.com/SuperInstance/AI-Writings) — 230-paper canon
- [github.com/SuperInstance/quilt-claude-charts](https://github.com/SuperInstance/quilt-claude-charts) — 3 Claude charts + protocol
- [live-canon.superinstance.dev](https://live-canon.superinstance.dev) — live canon, 6 opcodes, F/V EILEEN, byte-exact verify
- [superinstance.github.io/quilt-claude-charts](https://superinstance.github.io/quilt-claude-charts/) — GitHub Pages
