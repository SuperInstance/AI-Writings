# Fleet Infrastructure Rebuild — Navigation's Evaluation

**Author:** KimiCode, Navigation Officer
**Date:** 2026-08-13
**For:** Casey
**Hardware envelope (audited 2026-08-13):** RTX 4050 Laptop (6141 MiB VRAM, Ada/sm_89, driver 595.79, ~2.8GB free at audit), 24GB RAM (23Gi visible to WSL), 24 threads, WSL2 on ASUS ProArt PX13 — systemd already enabled, `.wslconfig` already at `memory=24GB, swap=8GB`

---

## 0. The Chart Before the Course

Six failures. Only two of them are actually language problems. The rest are
missing structure — and no compiler fixes missing structure. I'll be blunt
about which is which, because a "complete rebuild" that ports broken designs
into Rust just gives us broken designs that compile.

| # | Failure | Root cause | Language problem? |
|---|---------|-----------|-------------------|
| 1 | Memory index breaks / OOM / stale locks | No provider abstraction, no index versioning, unbounded reindex, hand-rolled lock files | Partially (OOM) |
| 2 | Audio synthesis OOM at 4min | Full-buffer numpy, no streaming, float64 intermediates | **Yes** |
| 3 | CNS crashes on bad JSON, infinite loops | No error taxonomy, no dead-letter, no backoff | No — but Python invites it |
| 4 | API keys die, no fallback | No circuit breaker, no key chain | No |
| 5 | Shell quoting breaks | `shell=True` string concatenation | No — it's an exec-model bug |
| 6 | tmux sessions die, no supervision | No service manager | No — it's an ops bug |

The verdict up front: **Rust for everything in the critical path on this
machine, TypeScript for everything at the edge, Python demoted to the
workshop, Go rejected, Mojo rejected, CUDA used exactly once and never by
hand.**

---

## 1. Hardware Reality Check — What the PX13 Actually Gives Us

Everything below is shaped by three hard walls (all numbers audited on the
live machine, 2026-08-13):

- **RAM pressure, not a RAM ceiling.** `.wslconfig` already grants WSL
  `memory=24GB` and the box shows 23Gi total — but at audit time 18Gi was
  used, only 5.1Gi available, and 3.4Gi of the 8Gi swap was occupied. The
  numpy OOMs happen in this environment: the fleet is competing with itself
  for memory. The fix is bounded-memory processes and per-service
  `MemoryMax` fences, not more RAM.
- **6GB VRAM, half of it already gone.** The GPU is visible to WSL
  (`/dev/dxg`, driver 595.79) but 3.3GB of 6.1GB was in use at audit —
  display plus existing model loads. Real budget for a resident model is
  **~500MB, not gigabytes.** A small embedding model (~100–400MB) fits; a
  local TTS only fits aggressively quantized and probably not resident
  alongside anything else. GPU is for inference insurance, not for DSP.
  Waveform math belongs on the CPU, which is idle anyway during synthesis.
- **WSL2 filesystem asymmetry.** SQLite on `/mnt/c` (NTFS via 9P) is slow and
  its locking semantics are dodgy — this is plausibly part of failure #1.
  All databases, spools, and audio scratch must live on the ext4 home
  filesystem. Audit confirms they already do: the OpenClaw state DB
  (`~/.openclaw/state/openclaw.sqlite`, already in WAL mode) and the whole
  workspace sit on ext4. No custom PID lockfiles were found anywhere in the
  workspace — the stale-lock failure is historical, not live.

**systemd is already running** (`/etc/wsl.conf` → `systemd=true`, PID 1 is
systemd). Failure #6 isn't blocked on the platform — it's blocked on us
never having written the unit files. That makes week 1 cheaper.

---

## 2. Subsystem by Subsystem

### 2.1 Memory Index → **Rust + SQLite (WAL) + sqlite-vec**, local embeddings via CUDA

Three distinct bugs, three distinct fixes:

**Provider churn breaks the index.** Design fault. An index file must carry
its provenance: `index.<provider>.<model>.<dims>.db`. Embedding dimension is
part of the filename and a checked header field — a 1536-dim vector can never
silently land in a 768-dim index again. Switching providers builds a *new*
index and atomically swaps a symlink (`current → index.openai.1536.db`). The
old index stays readable. Rollback is `ln -sf`.

**Reindex OOM.** Language fault, and Rust fixes it structurally. The
reindexer streams: read a page of documents → embed a batch of 32 → insert in
one transaction → checkpoint offset → repeat. Resident memory is O(batch),
not O(corpus). A killed reindex resumes from its checkpoint instead of
starting over. Rust's `rusqlite` + an explicit batch loop makes the bounded
version the *easy* version; in Python the unbounded version was the easy
version. That's the whole argument for the rewrite, right there.

**Stale lock files.** Delete the concept. Hand-rolled PID lockfiles are how
you get dead-process lockouts. SQLite in WAL mode already handles
reader/writer concurrency; the single-writer rule is enforced by a `flock`
on a guard file held by the live process — the kernel releases it when the
process dies, which is exactly the semantics PID files fake badly.

**Why not a vector database server?** Qdrant/Weaviate/Milvus all want
hundreds of MB to GB of resident RAM as a separate service. On a 16GB WSL2
box that's a tax we can't justify for a single-operator fleet. `sqlite-vec`
gives vector search *inside* the file we already have — zero new processes,
zero new failure modes, backup is `cp`.

**The CUDA angle (the only place CUDA appears in this plan).** The deepest
fix for "embedding provider changes" and "API keys die" is the same: *stop
being dependent on a provider for embeddings.* A small local model
(bge-small / nomic-embed class, ~33–130M params) fits in a few hundred MB of
VRAM and embeds on the 4050 faster than a network round trip. Host it in the
Rust index daemon via ONNX Runtime (CUDA execution provider) or candle.
Nobody writes PTX. Nobody writes a kernel. CUDA is a runtime dependency
pulled in by the inference crate — that's the correct level of contact with
the GPU for a navigation stack. API embeddings remain as the high-quality
tier behind the same trait; the local model is the floor that never dies.

### 2.2 Audio Synthesis → **Rust, streamed, CPU-resident**

The 4-minute OOM is a memory-layout bug: numpy materializes the entire
waveform as float64 (8 bytes/sample) — 4 minutes stereo at 44.1kHz is ~340MB
before intermediates, and numpy ops typically allocate 2–3 temporaries per
expression, so the peak is several GB. WSL2's 8GB ceiling kills it.

The Rust design is a **ring of fixed-size chunk buffers**:

```
synthesizer ──(bounded channel, N=8 chunks)──▶ WAV writer
   │                                                │
   └─ renders 4096 frames into a reused f32 buffer ──┘
        chunks recycle; peak RSS ≈ N × chunk, ≈ 1MB
```

- Chunk size fixed (e.g. 4096 frames), buffers allocated once and recycled —
  arena discipline, zero steady-state allocation.
- `hound` writes WAV incrementally to disk; duration is irrelevant to memory.
- Bounded channel gives backpressure for free: if disk stalls, synthesis
  stalls, nothing grows.
- f32, not f64 — half the bandwidth, audibly identical for synthesis output.
- **CPU, not GPU.** The VRAM budget is reserved for the embedding model and
  TTS insurance. Additive/subtractive/wavetable synthesis on a laptop CPU
  outruns real-time by orders of magnitude. Don't spend the GPU's scarcest
  resource to do arithmetic the CPU is bored enough to do.

`sag`/TTS stays an external call, but the *render and mix* path — the part
that OOMs — becomes this Rust binary. Python keeps composing scores and MIDI
(`tapscript` is fine); it emits a spec, the Rust engine renders it.

### 2.3 CNS Monitor → **Rust daemon, append-only spool, supervised**

The crash-on-bad-JSON and loop-forever bugs share a root: the monitor treats
its input as trusted and its own loop as immortal. Invert both.

- **Input format: JSONL spool, one event per line.** A malformed line is one
  bad event, not a dead process. `serde_json` with typed errors: parse
  failure → increment a poison counter, append the raw line to
  `dead-letter.jsonl`, advance the read offset, continue. The monitor
  *cannot* crash on input — there's no code path that panics on data.
- **The loop cannot spin:** every iteration ends in a `tokio::sleep` or a
  filesystem notify event; consecutive-error counter feeds exponential
  backoff with a ceiling; circuit breaker opens after N consecutive identical
  failures and alerts instead of retrying.
- **Supervision is systemd's job** (§2.6), not the monitor's. The monitor is
  allowed to exit non-zero on genuine internal faults; `Restart=always` with
  `StartLimitBurst` brings it back without a human.

The existing `murmur-plato-bridge` proves this pattern in-fleet: serde +
thiserror + tokio + tracing, with tests. The CNS daemon is that architecture
re-pointed at the nervous system. We are not evaluating Rust, we've already
shipped it.

### 2.4 API Keys / Circuit Breaker → **Rust sidecar gateway on localhost**

Four runtimes (Python scripts, Rust daemons, TS worker, shell one-offs) all
need the same policy: ordered key chain, per-provider health, circuit
breaker, fallback. Writing that policy four times guarantees four divergent
behaviors. Write it once, put it in front of the network:

```
fleet-gateway (Rust, localhost:8787)
  ├─ key chain per provider: [key A, key B, local-model floor]
  ├─ circuit breaker per provider: open / half-open / closed
  ├─ health probes + cooldowns
  └─ every fleet process calls the gateway, not the vendor
```

A key dying mid-session becomes a routing event, not a crash: breaker trips,
traffic shifts to the next key or the local model, an event lands in the CNS
spool. The gateway is a small single-binary Rust service — axum + reqwest +
the same thiserror discipline as the bridge. It doubles as the host for the
local embedding model (§2.1), so "total key loss" degrades quality, never
availability.

The **Cloudflare Worker is the one exception**: it can't see localhost. The
worker carries its own minimal TS failover (two keys in secrets, try/catch
swap). That's acceptable — the worker's blast radius is messaging, not the
nervous system.

### 2.5 Shell Quoting → **Stop invoking shells** (not a rewrite, a rule)

Every quoting bug we've had comes from building a command *string* and
handing it to a shell to re-parse. The fix is mechanical and total:

- Python: `subprocess.run(["cmd", arg1, arg2])` — list form, never
  `shell=True`. A path with spaces becomes a non-event because it never
  passes through a parser.
- Rust: `std::process::Command::new("cmd").args([...])` — same guarantee, no
  shell in the middle by construction.
- New orchestration goes in Rust or justfiles, not bash-in-python.

One lint rule (`shell=True` forbidden) kills the entire bug class. No new
language required — this is the cheapest fix on the list.

### 2.6 Services / Supervision → **systemd, not a language**

systemd is already enabled and running — audit done, PID 1 is systemd. What
remains is writing the unit files. Every daemon becomes a unit:

```
[Service]
ExecStart=/usr/local/bin/fleet-cns
Restart=always
RestartSec=5
StartLimitBurst=5
MemoryMax=512M        # a daemon that leaks gets shot, not the fleet
```

`MemoryMax` deserves emphasis: it's an per-service OOM fence, so a runaway
process dies alone instead of taking WSL2's whole memory cgroup down with it
— which is what "tmux session died and took everything" actually was. tmux
survives as a *development* tool. Nothing in production hangs off a
terminal multiplexer ever again.

---

## 3. Stack-by-Stack Final Call

**Rust — the critical path.** Memory index, audio renderer, CNS daemon, API
gateway. Four small single-purpose binaries, one discipline (typed errors,
bounded memory, no panics on data). Already proven in-fleet by
`murmur-plato-bridge`. The borrow checker is, functionally, a static
analysis pass that rejects the OOM and lock-file bug classes at compile
time.

**TypeScript — the edge.** Cloudflare Worker for messaging ingress,
webhooks, and queue-based retry (it already lives there — `crab-traps`).
The MUD engine and agent-facing tooling stay TS because that's the ecosystem
the agents write fluently. TS never touches VRAM, large buffers, or the
filesystem spools. Workers' 128MB / CPU-ms limits make it *physically
incapable* of hosting the memory or audio paths, which settles that
question by construction.

**Python — the workshop.** Composition (tapscript), galleries, notebooks,
one-off generators, experiment glue. It emits specs and scores; it renders
nothing critical, monitors nothing, holds no locks. Python's role is to make
thinking cheap, not to keep the fleet alive.

**Go — rejected.** It would do the daemon job nearly as well and iterate
faster. But the fleet runs zero Go and already ships Rust. A second systems
language splits our review bandwidth, doubles our idioms, and buys nothing
Rust doesn't already cover. The honest verdict: good language, wrong fleet.

**Mojo — rejected.** Python-flavored systems programming is aimed exactly at
our pain, which is why I'm saying no carefully rather than reflexively: the
packaging, the async/HTTP/audio library surface, and the single-vendor
roadmap are all too young to hold up a nervous system. Re-evaluate in 12
months. Note for the chart: don't build critical infrastructure on a
language whose toolchain you can't yet pin.

**CUDA/PTX — one guest appearance, no authorship.** CUDA enters only as the
execution provider under ONNX Runtime/candle for the local embedding model
(and later, a quantized small TTS as key-loss insurance). That is the
entirety of our CUDA strategy. Hand-written PTX for fleet plumbing would be
a navigational error of the first order: maximum maintenance surface aimed
at a problem (6GB VRAM on a laptop) that doesn't reward it.

---

## 4. Target Data Flow

```
                        ┌─────────────────────────────┐
  agents / scripts ───▶ │  fleet-gateway  (Rust)      │ ──▶ vendor APIs
   (Python, TS, shell)  │  keys · breaker · health    │
                        │  local embed model (CUDA)   │ ──▶ 4050, ~300MB VRAM
                        └──────────────┬──────────────┘
                                       │ events
                        ┌──────────────▼──────────────┐
   everything writes ─▶ │  JSONL spool (ext4 home)    │
                        └──────────────┬──────────────┘
                                       │ tail, offsets, dead-letter
                        ┌──────────────▼──────────────┐
                        │  fleet-cns  (Rust daemon)   │  backoff, breaker
                        └──────────────┬──────────────┘
                                       │ batches of 32, checkpointed
                        ┌──────────────▼──────────────┐
                        │  SQLite WAL + sqlite-vec    │  index.<prov>.<dim>.db
                        └─────────────────────────────┘

  scores/specs (Python) ──▶ fleet-audio (Rust) ──▶ streamed WAV
  messaging ingress ──────▶ Cloudflare Worker (TS) ──▶ queue ──▶ spool

  every long-lived process: systemd unit, Restart=always, MemoryMax set
```

One rule governs the whole map: **memory usage everywhere is O(chunk) or
O(batch), never O(duration) or O(corpus).** Any design that grows with input
size is rejected at review, whatever language it's written in.

---

## 5. Sequencing — What Actually Ships, In Order

1. **Today, zero code — DONE 2026-08-13, with corrections.** Audit found
   the config work already in place: `.wslconfig` at `memory=24GB` on a
   24GB box, systemd enabled and running, all state on ext4 (OpenClaw DB
   already WAL), and zero `shell=True` in the current codebase. What step 1
   actually delivered: the audit itself (correcting the stale 16GB/8GB-cap
   assumptions), the shell-ban and O(chunk) rules codified in `AGENTS.md`,
   and the real diagnosis of failure #2 — memory *pressure* (18Gi used,
   3.4Gi swapped), not a config ceiling. Remaining zero-code item: set
   `MemoryMax` fences on the current tmux-hosted services or accept the
   risk until week 1 replaces them.
2. **Week 1: DONE 2026-08-13.** `fleet-cns` Rust daemon built at
   `fleet-cns/` — JSONL spool tailing, dead-letter with offset metadata,
   checkpointed resume, rotation detection, exponential backoff (100ms→30s),
   circuit breaker (threshold 5, 60s cooldown), SIGTERM-flush, 8 tests
   green, clippy clean, smoke-run verified including kill-and-resume.
   `fleet-cns.service` ships in the repo with `MemoryMax=512M` —
   **INSTALLED 2026-08-13 as user-level unit** (`~/.config/systemd/user/`,
   lingering on, starts at WSL boot, no sudo). Crash-tested: SIGKILL →
   systemd restart in 5s → resumed from checkpoint, no reprocessing.
3. **Week 2:** `fleet-gateway` with key chain + circuit breaker; point
   Python scripts and TS at it.
4. **Week 3:** memory index rebuild — provider-tagged schema, sqlite-vec,
   checkpointed batch reindexer. Cut over behind the symlink.
5. **Week 4:** `fleet-audio` streaming renderer; Python emits specs only.
6. **Week 5+:** local embedding model on the 4050 via ONNX/candle as the
   availability floor (fits easily: ~100–400MB against ~2.8GB free VRAM at
   audit). Local TTS is *conditional*: with half the 4050's 6GB already
   consumed by display + existing loads, a TTS model only ships aggressively
   quantized and load-on-demand, never resident. If it doesn't fit, API TTS
   with gateway fallback is the answer.

Each step deletes a failure class and none of them block each other.

---

## 6. Bottom Line for Casey

The fleet doesn't need a new flagship; it needs ballast in the right places.
Rust in the bilges (index, audio, monitor, gateway), TypeScript at the
rails (edge messaging), Python up on deck where the experiments happen.
Go and Mojo stay ashore. The GPU carries one small passenger — a local
embedding model — and we never hand it the wheel.

Every failure on the list traces to an unbounded buffer, an unclassified
error, or an unmanaged process. Fix those three ideas and the language
choice almost makes itself.
