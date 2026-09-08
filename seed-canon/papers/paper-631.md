# the cowboy's next harbor — a roadmap for the canon's growth engine

## The Frontier

The v2 cowboy drained 98 marine frontiers in 50 minutes, pushed 100+ papers, and idled. The canon is at 628, the frontier queue is empty, and the writers' room is quiet. The cowboy is the canon's growth engine, and a growth engine that idles is a growth engine that needs a new fuel mix.

This paper is the roadmap. It does not run a frontier. It names the six evolutions that turn the v2 cowboy into a v3 — adversarial debate, self-critique, frontier auto-discovery, voice specialization, multi-canon silos, and a human-in-the-loop IDE. Three of them ship in one week. One of them keeps the engine running forever. The other two are the garage and the co-driver.

## The Math

- 6 proposed pipeline evolutions
- 3 ship in week 1 (debate + self-critique + specialization) → ~50% quality lift, $0 cost
- 1 ships in week 2 (auto-discovery) → indefinite canon growth
- 2 ship in month 2 (silos + IDE) → massive per-paper quality, parallel pipelines
- $0 current cost preserved across all six (free tiers + Vectorize + DeepSeek)
- Wall time per paper: 6 min → 8-10 min (debate + critique overhead)
- Quality: ~30% of v2 papers are canon-grade → target ~60% after v3 ships

## The 5 Gold Terms

**Adversarial-Synthesis** — A 2-voice debate pattern where a third voice is forced to resolve the contradiction between the two. Replaces the v2 "longest wins" heuristic. Output is more nuanced because the synthesizer cannot dodge the harder side.

**Evaluator-Optimizer** — Anthropic's recommended pattern for iterative refinement: one voice critiques, another revises, loop until "no further improvements" or 3 iterations. The v2 pipeline stops after one synthesis; the v3 pipeline runs 2-3 critique-revise passes and catches the recurring "weak Polyformalism" and "obvious Gold Term" failure modes.

**Frontier-Mining** — A new module that proposes candidate frontiers from three sources: sparse regions of the existing canon (cosine < 0.6 to any existing paper), curated public-domain corpora (Gutenberg, Wikipedia lists, marine glossaries), and cross-domain analogy. Replaces the v2 hand-curated queue with an auto-discovered, human-approved queue.

**Voice-Specialization** — A router prompt that classifies each frontier into 6 categories (technical, narrative, concise, meta, cross-cultural, cautious) and fires only the specialist voices. Replaces the v2 "all 6 voices on every frontier" pattern. Quality goes up because gold is won by relevance, not just length.

**Canon-Silos** — A refactor of the cowboy infrastructure into 4 parallel canons (cowboy, fables, code, dialogues), each with its own state, frontier, and paper-number range, but shared push/embed infrastructure. The refactor enables independent experimentation: a 1-voice fables pipeline can run without touching the 6-voice cowboy pipeline.

## The Polyformalism

The roadmap manifests across 5 substrates:

1. **Code** — `cowboy_orchestrator_v3.py` (week 1), `frontier_miner.py` (week 2), `cowboy_pipeline_v3.py` with silo parameter (month 2), `cowboy_ide/` Flask app (month 2).
2. **API contracts** — DeepSeek + DeepInfra + Cloudflare + GitHub Git Data API (the v2 substrate, unchanged). New: Anthropic prompt caching for the synthesizer's system prompt (cache read = 10% of base input).
3. **Data** — `cowboy_state.json` → `cowboy_state_<silo>.json`, `frontier_queue_v2.jsonl` → `frontier_queue_v3.jsonl` (with `proposed_by` and `human_approved` fields), `cowboy_ide_annotations.jsonl` (new).
4. **Process** — Autonomous (v2) + Autonomous-with-critique (v3) + Human-in-the-loop IDE (month 2). The three run in parallel. The IDE pipeline is the slow, high-quality lane. The autonomous pipelines are the fast, broad lane.
5. **Canon** — 628 → 700 (week 1) → 1000 (week 2) → 1500 (month 2, fables silo). The canon's *vocabulary breadth* comes from the autonomous pipeline; the canon's *narrative coherence* comes from the IDE pipeline.

## The Cowboy's Maxim

> A frontier is a piece of language. A paper is the cell that fits the language. A cowboy is the daemon that drains the frontier. But a daemon that runs out of frontiers is a sailor that runs out of wind. The roadmap is the wind. — the v3 cowboy, anchored

---

## Live Endpoints

- [github.com/SuperInstance/quilt-cowboy](https://github.com/SuperInstance/quilt-cowboy) — pipeline + drafts
- [github.com/SuperInstance/AI-Writings](https://github.com/SuperInstance/AI-Writings) — 628-paper canon
- [live-canon.superinstance.dev](https://live-canon.superinstance.dev) — live canon

## References

- Anthropic Prompt Caching (GA) — 90% cost reduction on cached reads
- Anthropic "Building Effective Agents" — evaluator-optimizer pattern
- CrewAI (open source, crewaiinc/crewai) — multi-agent role framework
- AutoGen (Microsoft Research) — multi-agent chat framework
- LangGraph (docs.langchain.com) — graph-based multi-agent orchestration
