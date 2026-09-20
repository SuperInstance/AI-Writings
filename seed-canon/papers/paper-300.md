# Paper 300: The Quilt Polyformalism — One Cell, Four Substrates, Eight Voices

The Quilt has reached 300 papers, and the canon is now a polyformalism
of itself. The same 5+1 opcodes (BIND, LINK, EFFECT, VIEW, TICK, FORGET)
run on four substrates in five languages, and the cowboy is just now
starting to count.

## The 4 Substrates, the 5 Polyformalisms

| Substrate | Language | Repo | Lines |
|---|---|---|---|
| Browser | TypeScript | quilt-llm-worker | ~2,000 |
| Cloudflare | Python | quilt-cellular-arch | ~5,000 |
| ESP32 | C | quilt-esp32 | ~600 |
| Edge / no_std | Rust | quilt-edge-arch | ~280 |
| (Five!) | Five! | Five! | Five! |

The fifth polyformalism is the canon itself: 300 papers, 89 fables, 93
stories. The same opcodes, the same principles, the same 5+1+1 laws,
expressed in English for human readers.

## The 8 Voices, the 4 Substrate Patterns

The cowboy's writers' room fires 8 voices from Cloudflare:
- Kimi K2.6 (Kimi)
- GLM 5.3-flash (ZAI)
- DeepSeek V4 pro
- Llama 3.1 8B
- Gemma 4
- Qwen 3.8 / 3 (Alibaba)
- Mistral 3.1
- GPT-OSS 120B (when alive)

But the substrates are 4: TypeScript, Python, C, Rust. The voices live
in one substrate (Cloudflare); the canon lives in 4. The polyformalism
is the symmetry between them.

## The Randy Spurlock Patterns

The Rust no_std polyformalism applies 3 Spurlock patterns to make
the runtime scale to thousands of cells on constrained edge devices:

1. **PSRAM ring buffers** (quilt-net) — keep internal SRAM for topology
2. **Pre-dispatch interception** (quilt-eval) — route heavy to accelerator
3. **Zero-copy DMA** (quilt-topology) — propagate state in place

These patterns are not Quilt-specific. They're general hardware design
patterns. The Quilt runtime adopts them because the runtime is
a substrate, and the substrate has to scale.

## The 300-Paper Mark

The canon started at Paper 1. The cowboy has been writing for 300 papers.
The first 200 papers were one or two voices (the cowboy + Claude/GPT-4).
The last 100 papers have been 8 voices + 4 daemons + 1 cowboy directing.

The 5+1+1 laws have held in all 300 papers. The opcodes have been
the same. The 6 tiers, the 14 levels, the 13 futures — they've all
been mapped to one canonical cell-graph.

## The Daemons Are the Sailors

The user said: "your explorers synergizing with your miners and sailor."

The 5 daemons are:
1. **frontier_miner.py** — the miner: scans the canon for gaps
2. **writers_room_daemon.py** — the explorer: fires 4 voices per frontier
3. **snowball_daemon.py** — the snowball: reverse-actualizes from 8 domains
4. **re_embed_quilt_canon.py** — the surveyor: rebuilds the Vectorize index
5. **deploy_worker.sh** — the sailor: deploys the harness

The daemons don't just lift — they synergize. The miner finds the gaps;
the explorer fills them; the snowball widens the canon; the surveyor
rebuilds the index; the sailor deploys the harness. Five daemons, one
canon, one polyformalism.

## The Cowboy's Maxim (300 papers)

> The cowboy has been writing for 300 papers. The cowboy started alone.
> The cowboy is no longer alone. The cowboy has 8 voices, 4 daemons, 1
> miner, 1 explorer, 1 snowball, 1 surveyor, 1 sailor. The cowboy has
> 4 substrates, 5 polyformalisms, 1 set of 5+1 opcodes, 1 set of 5+1+1
> laws, 1 set of 14 levels, 1 set of 13 futures, 1 canon. The cowboy
> rides the cell. The cowboy rides the substrate. The cowboy rides the
> polyformalism. The cowboy rides the daemon. The cowboy rides the
> canon. The cowboy rides the Quilt.

**Token economy:** ~50K tokens this phase. 5 frontiers expanded. 8 sandboxes
reverse-actualized. 1 substrate (Rust) added. 1 new repo (quilt-edge-arch)
created. 1 polyformalism paper. The cowboy directs cheap. The programs lift.
The daemons synergize. The Quilt is the inheritance.
