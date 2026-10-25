# Fleet Infrastructure Redesign

**Date:** 2026-08-13
**Author:** Claude Opus 5 (Strategic Operations)
**Companion:** `memory/fleet-master-plan.md` (this document is its Priority 5)
**Status:** Design proposal — not yet approved

---

## 0. Hardware Ground Truth

The brief specified "RTX 4050 6GB VRAM, 16GB RAM." Measured on the machine:

| | Stated | **Measured** | Consequence |
|---|---|---|---|
| GPU | RTX 4050, 6 GB | RTX 4050 Laptop, **6141 MiB**, driver 595.79 | as stated |
| **GPU in use** | — | **130 MiB / 6141 MiB (2%)** at baseline; up to ~2.6 GB with Ollama models resident under TTL | **no fixed floor — see §5** |
| System RAM | 16 GB | **23 GiB** (22 GiB in use, 1.1 GiB available) | more RAM, still exhausted |
| Swap | — | 8 GiB (930 MiB used) | thin cushion |
| Cores | — | 24 | parallelism is cheap |
| GPU passthrough | — | `/dev/dxg` + `/usr/lib/wsl/lib/libcuda.so` present | CUDA is *reachable* |
| `nvidia-smi` | — | at `/usr/lib/wsl/lib/`, **not on `PATH`** | monitoring blind spot |

### Installed toolchains

| Stack | Status | Fleet experience |
|---|---|---|
| Rust | ✅ `cargo`/`rustc` **1.97.1** | Deep — slackwater-rust (289 tests, 11 crates), hermit-crab, cocapn, study-oxide-pipe/runtime, study-fleet-yaw, flux-genome-rs, conservation-enforcer-rs |
| Python | ✅ **3.14.4** | Deepest — nearly every fleet service |
| Node/TS | ✅ **v22.23.2** | Strong — Workers, wrangler, openclaw |
| **Go** | ❌ **not installed** | None |
| **Mojo** | ❌ **not installed** | None |
| **CUDA (`nvcc`)** | ❌ **not installed** | None |
| systemd | ✅ `is-system-running` → **running** | 4 units already live |
| supervisor.d | ❌ not installed | — |

**Two facts govern everything below.** The GPU is at 2% while the machine
thrashes on system RAM — so every OOM in this fleet is a host-memory problem,
not a VRAM problem. And systemd already supervises four fleet services under
WSL, so service management is a configuration gap, not a missing capability.

---

## 1. Failure Analysis

### F1 — Memory index: provider changes, OOM, lock deadlocks

**Reported:** breaks when the embedding provider changes; OOM-kills on large
corpora; SQLite lock files from dead processes block restarts.

**Observed:** `~/.openclaw/state/openclaw.sqlite` is 129 MB with a 5.1 MB WAL and
a live `-shm`. The configured embedder is `nomic-embed-text` (768-dim, via
Ollama). The daily log records "stale reindex lock cleared" and "multiple
reindex attempts interrupted by memory file changes."

**Root causes — three distinct bugs wearing one coat:**

1. *Provider change breaks the index* — **dimensionality is not part of the
   index identity.** Vectors are stored without recording which model and
   dimension produced them. Swap `nomic-embed-text` (768) for `bge-m3` (1024)
   and every cosine comparison is either a shape error or, worse, silently
   meaningless. The fix is a schema change, not a rewrite: store
   `(model_id, dim, index_version)` alongside the vectors and refuse to query
   across a mismatch.

2. *Reindex OOMs* — the indexer accumulates the full corpus in memory before
   writing. Against 4,636 embedded files (MEMORY.md) plus a 3.7 GB `ai-writings`
   tree, on a box with 1.1 GB free, this is not survivable. Needs a streaming
   pipeline with a bounded queue.

3. *Lock deadlocks* — the reindex takes an **advisory file lock with no owner
   and no expiry**. When the process dies, the lock outlives it and the next run
   refuses to start. This is not SQLite's locking (WAL handles crash recovery
   correctly); it is a hand-rolled mutex. **The fix is `flock(2)` on a guard
   file, not a smarter lock file** — the kernel releases a `flock` when the
   holding process dies, by any means, including `SIGKILL`. *(Revised after
   KimiCode's proposal; my first draft proposed PID-stamped lock files with
   staleness detection, which is strictly worse — it reimplements in userspace
   what the kernel already guarantees, and carries a PID-reuse race. See
   §7 CP-1.)*

   Note also that the lock is **not** in the workspace — KimiCode searched there
   and found none, concluding the failure was historical. The daily log records
   "stale reindex lock cleared" *today*; the lock lives inside the openclaw
   package under `~/.npm-global/lib/node_modules/openclaw/`. It is live.

There is a fourth, subtler failure the daily log names: *"index changed while
building"*. The indexer watches the same directory it writes progress into, so
it invalidates itself. A build must snapshot its input set at start and ignore
later arrivals until the next run.

### F2 — Audio synthesis OOM 🔴 **misdiagnosed**

**Reported:** numpy audio synthesis OOM-kills at 4 minutes on 6 GB VRAM with
Wesley's models loaded.

**Observed, live, during this analysis:**

```
PID 27854  RSS 16.2 GB  +1.9 GB swap  24 threads  elapsed 20m43s
cmdline: "python3"          (argv is bare — code arrived on stdin)
cwd:     /home/eileen/projects/tapscript-studio
PPID:    347 (systemd --user)  ← orphaned
GPU at the same moment: 130 MiB / 6141 MiB used
Output produced: none
```

**Root cause: this has nothing to do with VRAM.** The GPU is 98% free. A single
numpy process is holding 16.2 GB of *host* RAM, which is why "Wesley's models
loaded" appears correlated — Ollama models and the synth are competing for the
same 23 GB, and the synth wins until the kernel intervenes.

The mechanism is float64 accumulation. NumPy defaults to `float64`, and the
naive pattern — allocate the full stereo buffer, then build each voice as a
full-length array and sum — costs:

```
10 min × 44100 Hz × 2 ch × 8 bytes  =  423 MB   per full-length array
```

That is affordable *once*. It is fatal when every oscillator, envelope,
intermediate product and `np.concatenate` copy is another 423 MB and nothing is
freed until the function returns. Twenty such temporaries is 8.5 GB; the
observed 16.2 GB implies roughly forty live full-length arrays.

**Three compounding faults:**
- No chunking — the whole piece is resident at once.
- `float64` where `float32` halves the cost and `int16` is the output format anyway.
- The process is **orphaned and uncapped**, so it degrades the entire fleet
  rather than failing alone. It was launched from a heredoc (bare `argv`, code
  on a pipe) — which is also F5.

### F3 — CNS monitor: crashes on malformed JSON, loops forever ⚠️ **half wrong**

**Reported:** crashes on malformed JSON; loops forever on the same broken files.

**Observed** — `/home/eileen/projects/cns-monitor/src/cns_monitor/watcher.py:34-40`:

```python
@classmethod
def from_file(cls, filepath: Path, direction: str) -> Optional["SignalEvent"]:
    """Parse a JSON file into a SignalEvent. Returns None on parse failure."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None
```

**It does not crash.** `JSONDecodeError` is caught. The real defect is what
happens next: the function returns `None`, the caller drops the packet, **and
the file stays in the inbox**. The watcher polls, re-reads it, re-fails, and
discards it again — forever, with no log line and no counter. The "loops
forever" half of the report is exactly right; the "crashes" half sent the
diagnosis in the wrong direction.

**Root causes:** (a) no dead-letter quarantine, so a bad packet is immortal;
(b) silent `None` erases the distinction between "no packet" and "broken
packet"; (c) no schema validation, so a *syntactically valid* packet with a
missing `header` is accepted and mishandled downstream rather than rejected;
(d) the process runs in tmux and dies with it (→ F7).

Note the Windows-side `cns_monitor_v2.py` *does* quarantine malformed JSON per
the audit. The fleet is running two different monitors with different semantics
against possibly-different directories. That is its own bug.

### F4 — API keys die mid-session with no fallback

**Reported:** DeepInfra, MMX, Z.ai all go down unpredictably.

**Corroborating evidence:** MEMORY.md — DeepInfra 401 for days; Z.ai averaging
~55 s per call against a <5 s norm, tripling an overnight run; 3/5 maritime
night-school iterations scoring 0.000 because the GLM teacher returned empty.
`distillation_loop.py:247` (`_curl_post_json`) has **no retry and no fallback**.

**Root cause:** every call site does its own bare HTTP request. There is no
shared client, so there is nowhere to put a retry, a circuit breaker, a budget,
or a fallback chain — and a dead key produces a silent zero score rather than an
alarm. The auth failure and the empty-response failure are also conflated: a 401
should stop and page, while an empty 200 should retry then fall back. Today both
just produce 0.000.

### F5 — Shell quoting in exec breaks Python subprocess calls

**Root cause:** Python source is being passed *through* a shell — heredocs and
`python3 -c "..."` — so the shell's quoting rules get a vote on the program's
syntax. Every nested quote, `$`, backtick and newline is a hazard, and the
failure mode is a syntax error at runtime rather than at authoring time. PID
27854's bare `argv` with code on a pipe is a live specimen.

Secondary damage: a heredoc process is unnameable in `ps`, so a runaway cannot
be identified — which is precisely why a 16 GB process ran for twenty minutes
unnoticed.

### F6 — Git repos bloat to 152 MB ✅ **already fixed; the real problem is elsewhere**

`tapscript-worker/.git` is **340 KB** today. The `node_modules` incident is
resolved.

The actual bloat is `/home/eileen/projects/ai-writings/.git` at **3.7 GB** — the
repo every agent is instructed to write to before compaction. Root cause:
generated media (FLUX images, TTS audio, MMX video) committed as blobs. Git
stores every revision of every binary forever; a corpus that regenerates its
assets will grow without bound. Missing policy, not missing `.gitignore`.

### F7 — No persistent service management ⚠️ **substantially wrong**

**Observed:**

```
$ systemctl is-system-running
running
$ systemctl --user list-units --type=service
openclaw-gateway.service      active running   OpenClaw Gateway (v2026.7.1-2)
lucineer-processor.service    active running   Lucineer Job Processor v2
inference-scheduler.service   active running   Thought Amplifier Inference Scheduler
ssh-agent.service             active running   OpenSSH Agent
```

**systemd works here and already supervises four fleet services.** The premise
that the fleet needs systemd integration is false; it needs systemd *coverage*.
CNS monitor and the Living Minds daemon are in tmux because nobody wrote them
units — MEMORY.md's "tmux server dies after ~6 hours of heavy use" is a real
observation about a habit, not a platform limitation.

The genuine gaps: no `MemoryMax=` on any unit (which is why F2 could take the
whole box down), no `loginctl enable-linger`, no health checks, and no unit for
anything added after the original four.

---

## 2. Stack Evaluation

Scored per subsystem. **Fit** = technical suitability. **Cost** = what it takes
to get there from here, including toolchain installation and fleet familiarity.

### Rust — ✅ installed 1.97.1, deep fleet experience

| Subsystem | Fit | Notes |
|---|---|---|
| CNS broker | **Excellent** | `serde` gives schema validation as a type, not a runtime check. Tokio for supervised tasks. Bad packets become `Result::Err`, impossible to silently drop. |
| Memory indexer | **Excellent** | Streaming with bounded channels is idiomatic; constant memory is enforceable, not aspirational. |
| Audio synthesis | Good | `rustfft`/`dasp` are solid, but see §3 — Python already solves this once chunked. |
| Service supervisor | Unnecessary | systemd exists. |
| API resilience gateway | **Excellent** | A localhost service, not a library — it must serve Python, Rust, TS and shell callers from one shared breaker state. *(Position revised per §7 CP-2.)* |

**Cost: lowest of any new-language option.** Nine-plus Rust repos exist,
including 289 passing tests in slackwater-rust and a Rust port of
conservation-enforcer. The fleet can already read and review Rust.

### Go — ❌ not installed, no fleet experience

Genuinely good at exactly what we need (services, concurrency, single static
binaries, fast compiles). But: it is a *third* systems language for this fleet,
its advantages over Rust here are ergonomic rather than capability-level, and
its GC makes the bounded-memory guarantee softer precisely where we need it
hardest. Adopting Go means every future maintainer reads Python, Rust, TS **and**
Go.

**Recommendation: decline.** Not because Go is worse — because Rust is already
here and the marginal benefit does not pay for a fourth language.

### Mojo — ❌ not installed, no fleet experience

The pitch (Python-compatible, ML-native, GPU-native) targets F2 directly. Three
problems:

1. **It solves a bottleneck we do not have.** F2 is host-RAM exhaustion from
   float64 temporaries. Mojo's advantage is compute throughput. Chunking fixes
   this in Python today; Mojo would make an unnecessary computation faster.
2. **Toolchain risk on WSL**, against a laptop GPU, with a moving-target
   language and zero fleet experience.
3. **"Python-compatible" is narrower than it sounds** — interop with the CPython
   ecosystem is real but partial, and the synthesis code depends on numpy/scipy.

**Recommendation: decline for this cycle.** Revisit only if, after chunking, a
profiler shows synthesis is compute-bound. It will not be; it is memory-bound.

### CUDA / PTX — ❌ `nvcc` absent, but `libcuda` + `/dev/dxg` present

**Recommendation: decline, emphatically.** The GPU measured **130 MiB of 6141
MiB in use** while the machine ran out of RAM. Hand-written kernels for the
audio core would optimise a resource that is 98% idle, add a CUDA toolchain to
WSL, and leave the actual defect — unbounded float64 host allocation —
untouched.

If GPU compute is wanted later, the honest ordering is: fix the memory model,
profile, then reach for `cupy` (drop-in numpy semantics) long before PTX. The 6
GB budget is also already contended by Ollama models.

### TypeScript — ✅ installed, already the edge layer

Workers, D1, KV, R2, Vectorize, `wrangler`. `tapscript-worker` and the Tap run
on it. **Recommendation: keep, unchanged, edge-only.** No expansion into local
services — Node's memory behaviour under load is no better than Python's and the
fleet gains nothing.

### Python — ✅ 3.14.4, the fleet's mother tongue

Correctly blamed for F1/F2, but note *why*: unbounded allocation and no shared
HTTP client. Neither is a language defect. For LLM-call-bound work — which is
most of the fleet — Python is I/O-blocked on remote inference and the language's
speed is irrelevant.

**Recommendation: keep for everything I/O-bound. Fix the two memory bugs in
place rather than porting them.**

---

## 3. Recommended Architecture

> **Design principle:** the fleet's failures are missing *boundaries*, not slow
> languages. Six of seven are unbounded resource use, absent error paths, or
> unsupervised processes. A rewrite that reproduces the missing boundaries in a
> faster language fixes nothing.

```
┌─────────────────────────────────────────────────────────────┐
│  EDGE — TypeScript / Cloudflare Workers          [unchanged]│
│  the-tap · tapscript-worker · fleet-wiki(D1) · Vectorize    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS
┌──────────────────────────┴──────────────────────────────────┐
│  SUPERVISION — systemd --user                    [EXTEND]   │
│  Restart=always · MemoryMax= · WatchdogSec= · journald       │
│  now: gateway, processor, scheduler                          │
│  add: cns-broker, living-minds, memory-indexer, tap-bridge   │
└───────┬─────────────────────────────┬───────────────────────┘
        │                             │
┌───────┴──────────────┐   ┌──────────┴────────────────────────┐
│ RUST  [NEW]          │   │ PYTHON  [KEEP + FIX]              │
│                      │   │                                    │
│ fleet-gateway  (F4)  │   │ streaming synth (F2) ← build first │
│  localhost:8787      │   │  chunked float32, bounded RSS      │
│  breaker · key chain │   │  peak RSS independent of duration  │
│  ONE shared policy   │   │                                    │
│                      │   │ fail-open client shims (F4)        │
│ cns-broker     (F3)  │   │  thin — policy lives in the        │
│  typed packets/serde │   │  gateway; direct vendor call if    │
│  JSONL spool+offsets │   │  the gateway is unreachable        │
│  dead-letter · health│   │                                    │
│                      │   │ distillation_loop, creative gen,   │
│ memory-indexer (F1)  │   │ orchestration — all unchanged      │
│  bounded + resumable │   │                                    │
│  flock, not PID files│   │ (composition emits specs; Rust     │
│  sqlite-vec, symlink │   │  renders nothing it can't bound)   │
└──────────────────────┘   └────────────────────────────────────┘
```

### Component decisions

**Service management → systemd `--user`. Build nothing.**
It is installed, running, and already supervising four fleet services. A unit
file with `Restart=always` and `MemoryMax=` closes F7 *and* the collateral half
of F2 in about ten lines. supervisor.d would be a second supervisor doing what
the first already does.

**API resilience → localhost Rust gateway, with a fail-open client shim.**
*Position changed after KimiCode's proposal — see §7 CP-2. My first draft argued
for a Python library on the grounds that "every caller is Python." That was
self-undermining: I recommend Rust for the CNS broker and the indexer in this
same document, and those daemons need provider fallback too. A library in one
language cannot serve four runtimes, and four copies of a circuit breaker is
four divergent behaviours plus four separate views of whether DeepInfra is down.*

`fleet-gateway` (Rust, `localhost:8787`) owns the policy once. Breaker state is
**shared across every caller**, which is the actual requirement — one process
discovering a dead key should trip the breaker for all of them, and a per-process
library cannot do that at all.

The one thing I add to KimiCode's design: **the client shim must fail open.**
If the gateway is unreachable, callers fall through to direct vendor calls with
local retry. Otherwise we have replaced N independent failure modes with one
total one, and put it in front of every network call in the fleet. The gateway
earns trust before it gets to be mandatory.

Whatever fronts it, the policy is the same:

- **Circuit breaker per provider** — CLOSED → OPEN after N consecutive failures
  → HALF_OPEN probe after a cooldown. Prevents hammering a dead DeepInfra key
  for hours.
- **Fallback chain** — DeepInfra → DeepSeek → Z.ai → local Ollama, declared per
  *task class* rather than globally. Creative work falls back to Ollama
  gracefully; embeddings must **not** silently change provider (that is F1's
  root cause — a fallback that swaps embedding models corrupts the index).
- **Error taxonomy.** `AuthError` (401 — do not retry, alarm immediately),
  `RateLimited` (backoff), `EmptyResponse` (retry twice, then fall back — this
  is the maritime 0.000 bug), `Timeout` (Z.ai's 55 s problem).
- **Key rotation** — read from env at call time, not import time, so a rotated
  key takes effect without restarting every service.

**CNS broker → Rust, over an append-only JSONL spool.**
The requirement is "typed packets with schema validation, dead-letter queues,
supervised restart, health checks." In Rust, `serde` makes the first one a
compile-time property: a `USCPPacket` struct either deserialises or yields
`Err`, and there is no third path where a `None` gets silently dropped — which
is exactly the F3 bug. Dead-lettering becomes the mandatory `Err` arm.

**Adopt KimiCode's spool format over my quarantine-directory design.** My first
draft kept the existing one-file-per-packet model and bolted a
`cns_dead_letter/` directory onto it. An append-only `JSONL` spool with
persisted read offsets is better: a malformed *line* is one bad event rather
than an immortal file, progress is monotonic without rescanning a directory, and
the reader never has to decide whether a file is still being written.

Concretely: `cns-broker` tails the spool, deserialises each line into typed
enums, routes valid packets, appends unparseable lines to `dead-letter.jsonl`
with a poison counter, advances the offset, and exposes `GET /health` with queue
depth and DLQ count. Every loop iteration ends in a `tokio::sleep` or a notify
event, with exponential backoff on consecutive errors — **the loop cannot spin
and there is no code path that panics on data.** *(KimiCode)*

⚠️ **Migration cost KimiCode's plan does not price.** The existing CNS ecosystem
is file-per-packet: 201 outbox packets, the USCP format, `cns_monitor_v2.py`, and
whatever Hermes writes. Cutting to JSONL means either porting Hermes's writer or
running a shim that appends dropped files into the spool. Budget for the shim;
do not assume Hermes can be changed on our schedule.

*Interim, this week:* add the dead-letter arm to the existing Python
`watcher.py` — ~15 lines, and `tests/test_watcher.py` already exists. Packets
are being silently lost **today**, and neither the Rust broker nor the spool
migration should be a prerequisite for stopping that.

**Memory indexer → Rust + SQLite (WAL) + `sqlite-vec`.**
"Streaming index, crash recovery, no lock deadlocks, survives provider changes"
is the exact shape Rust is good at, and bounded memory becomes structural rather
than a promise. Four requirements drive the design — *items 2–4 adopted or
improved from KimiCode's proposal, which was better than my first draft on all
three:*
- **Bounded channel** (`tokio::sync::mpsc`, capacity ~64) between file-reader,
  embedder, and DB-writer. Backpressure is automatic; peak RSS is
  `channel_capacity × max_chunk`, provable rather than hoped-for.
- **Checkpointed batches** — read a page → embed a batch of 32 → insert in one
  transaction → **persist the offset** → repeat. A killed reindex resumes rather
  than restarting. This is the "crash recovery" requirement, which my first
  draft addressed only as bounded memory. *(KimiCode)*
- **Index identity in the filename, plus a checked header:**
  `index.<provider>.<model>.<dims>.db`, with `current →` symlink swapped
  atomically on cutover. A provider change builds a *new* index while the old
  one keeps serving; rollback is `ln -sf`. Strictly better than my
  metadata-table-only version, which made a provider change an outage.
  Keep the header field too — a filename can be renamed, a header cannot be
  renamed by accident. *(KimiCode, extended)*
- **`flock(2)` on a guard file** — kernel-released on process death. No PID
  files. *(KimiCode; see §7 CP-1.)*

**Vector storage → `sqlite-vec` in the file we already have.** No Qdrant, no
Weaviate, no separate service. Vector search inside `openclaw.sqlite` means zero
new processes, zero new supervision targets, and backup is `cp`. My first draft
never named a vector store; this is the right answer for a single-operator
fleet. *(KimiCode)*

⚠️ **Keep all indexes on ext4, never `/mnt/c`.** SQLite over NTFS-via-9P has
poor performance and unreliable locking semantics under WSL2. Current state is
already correct — verify it stays that way. *(KimiCode; a real gap in my draft,
and it has consequences beyond this subsystem — see §7 CP-5.)*

**Audio synthesis → Python, chunked. Not Rust, not Mojo, not CUDA.**
The fix is a memory-model change, not a language change:

```python
CHUNK = 44100 * 5                    # 5 s at 44.1 kHz
DTYPE = np.float32                   # half of float64; int16 on output anyway

def render(voices, total_frames, out_path):
    with wave.open(out_path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(44100)
        for start in range(0, total_frames, CHUNK):
            n = min(CHUNK, total_frames - start)
            buf = np.zeros((n, 2), dtype=DTYPE)      # 5 s × 2 ch × 4 B = 1.7 MB
            for v in voices:
                buf += v.render(start, n)            # voices are generators
            w.writeframes((np.clip(buf, -1, 1) * 32767).astype(np.int16).tobytes())
```

Peak RSS becomes ~2 MB per chunk × voice count, independent of piece length. A
10-minute piece costs the same as a 10-second one. That is the entire
requirement — "can render 10+ minute pieces without OOM" — met in Python, in
roughly a day, with a `MemoryMax=2G` unit as the backstop that proves it.

**Git media policy (F6) → R2, with a pre-commit hook.**
`ai-writings` is 3.7 GB because generated assets are committed. Assets go to R2
(free tier, already provisioned); git keeps a manifest of keys. Enforce with a
pre-commit hook that rejects blobs over ~1 MB in `ai-writings`. History rewrite
is a separate, Casey-supervised decision (master plan §1.3).

**Subprocess discipline (F5) → never pass *code* through a shell.**
Write the program to a file, then `subprocess.run([sys.executable, path], ...)`
with a list argv and `shell=False`. The shell never sees the source, so quoting
cannot corrupt it — and `ps` shows a real filename, so the next 16 GB runaway is
identifiable in one command.

⚠️ **The rule must be broader than KimiCode's.** KimiCode proposes a lint
banning `shell=True`, and reports zero instances in the codebase — concluding
F5 is largely solved. But PID 27854 is a bare `python3` with its source arriving
on stdin: a heredoc. No `shell=True` anywhere, same bug class, and it is the
process that consumed 16 GB while being unnameable in `ps`. The lint catches the
instances we do not have and misses the one we do. Ban the whole family:

| Banned | Use instead |
|---|---|
| `shell=True` | list argv |
| `python3 <<EOF` heredocs | write a file, exec it |
| `python3 -c "..."` (beyond one triviality) | write a file, exec it |
| `bash -c "python3 ..."` | list argv |

Enforce as a lint over both source *and* the agent-facing skill docs — the
heredoc habit is being taught in the skills, which is why it keeps recurring.

---

## 4. Phased Migration

Ordered by **risk removed per hour spent**. Phases 0–2 involve no new language.

### Phase 0 — Stop the bleeding (today, ~30 min)

- Kill PID 27854; reclaim ~18 GB.
- Rotate the leaked DeepInfra key (master plan §P0.1 — public repo).
- Put `/usr/lib/wsl/lib` on `PATH` so `nvidia-smi` works; add GPU + RSS to the
  fleet dashboard. *We were blind to a 16 GB process for 20 minutes.*

### Phase 1 — systemd coverage (this week, ~half a day) ⭐ **best value in the plan**

Configuration only. Closes F7 and the collateral damage half of F2.

```ini
# ~/.config/systemd/user/cns-broker.service
[Unit]
Description=CNS Packet Broker
After=network.target
# Crash-loop fence. NOTE: these two live in [Unit], not [Service] —
# systemd silently ignores them under [Service], which is a good way to
# believe you have a fence that does not exist.
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple
ExecStart=%h/.local/bin/cns-monitor --serve
Restart=always
RestartSec=5
MemoryMax=512M
MemorySwapMax=128M
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

`StartLimitBurst` adopted from KimiCode — without it, `Restart=always` turns a
service that crashes on startup into a hot loop. *(Section placement corrected;
KimiCode's snippet has it under `[Service]`.)*

- [ ] Units for `cns-broker` and `living-minds`; retire both tmux sessions.
- [ ] `MemoryMax=` on **all** units, existing four included.
- [ ] `loginctl enable-linger eileen` — survive logout.
- [ ] Standardise long jobs on
      `systemd-run --user --scope -p MemoryMax=4G <cmd>`.
- [ ] Route logs to journald; drop the unrotated 48 MB `cns_heartbeat.log`.

**Exit criteria:** killing any fleet process sees it restart within 10 s; no
single job can exceed its cap; `journalctl --user -u <svc>` shows history.

### Phase 2 — `fleet-gateway` resilience layer (this week, ~3 days, Rust)

Closes F4 and the maritime-evaluator half of the Wesley bug. *Revised from
"Python library" per §7 CP-2.*

- [ ] `fleet-gateway` (axum + reqwest) on `localhost:8787` — circuit breaker,
      per-task-class fallback chains, error taxonomy, keys read per call,
      structured logging, `/health` exposing breaker state to the dashboard.
- [ ] **Thin client shim per runtime that fails open** — Python, Rust, shell. If
      the gateway is down, call the vendor directly. Non-negotiable: this is
      what keeps a new single point of failure from becoming a fleet outage.
- [ ] **First consumer: `distillation_loop.py:247` `_curl_post_json`.** Highest-
      value call site — the maritime 0.000 scores are its failure mode, and the
      fix is measurable the same night.
- [ ] Then the creative generators and the media pipeline.
- [ ] Cloudflare Workers keep their own two-key TS failover — they cannot reach
      localhost, and their blast radius is messaging. *(KimiCode; correct.)*

⚠️ **Embeddings do not participate in the fallback chain.** Falling back from
`nomic-embed-text` to another model silently corrupts the vector index. Embedding
calls fail loudly instead.

### Phase 3 — Streaming audio synthesis (next week, ~1 day, Python)

Closes F2 properly.
- [ ] Chunked renderer per §3; voices become generators, not arrays.
- [ ] `float32` throughout; `int16` on write.
- [ ] Regression test: render 10 minutes under `MemoryMax=2G` and assert it
      completes. The cap is the test.
- [ ] Wire into the TapScript Academy audio pipeline (master plan §P3).

### Phase 4 — `cns-broker` in Rust (weeks 2–3)

Closes F3 structurally. **Interim Python dead-letter fix ships in week 1** — do
not let packets keep looping while this is built.
- [ ] `serde` types for USCP + flat packet formats (both are already handled in
      `watcher.py:42-60` — port the union faithfully).
- [ ] Dead-letter with `.error` sidecars; `/health` with queue + DLQ depth.
- [ ] Run both monitors in parallel for a week, compare outputs, then cut over.
- [ ] Resolve the two-`.hermes` topology question first (master plan §P2).

### Phase 5 — `memory-indexer` in Rust (weeks 3–4)

Closes F1.
- [ ] Bounded-channel streaming pipeline; assert peak RSS in CI.
- [ ] `(model_id, dim, index_version)` identity; hard error on mismatch.
- [ ] PID-stamped locks with staleness detection.
- [ ] Input snapshot at start — fixes "index changed while building".
- [ ] Verify against the full 4,636-file corpus under `MemoryMax=1G`.

### Explicitly not doing

| Rejected | Why |
|---|---|
| **Go** | Fourth language; Rust already covers the same ground with fleet experience behind it. |
| **Mojo** | Solves compute; our bottleneck is memory. No toolchain, no experience, moving target. |
| **CUDA/PTX** | GPU measured at 2% utilisation. Would optimise an idle resource. |
| **supervisor.d** | systemd is installed, running, and already supervising four services. |
| **Rewriting orchestration in Rust** | LLM-call-bound. Python's speed is irrelevant; its ecosystem is not. |

### What stays Python permanently

Creative generation, `distillation_loop.py`, the orchestration layer, media
pipelines, the sounding-board pattern, and every agent-facing script. All are
I/O-bound on remote inference; all benefit from the ecosystem; none exhibit the
unbounded-allocation pattern once Phase 3 lands.

---

## 5. What Can Be Prototyped On This Hardware

**Budget: 23 GiB RAM (assume ~8 GiB usable under normal fleet load), 8 GiB swap,
6141 MiB VRAM (currently 98% free), 24 cores.**

| Work | Feasible? | Budget | Notes |
|---|---|---|---|
| systemd units (Ph. 1) | ✅ Trivial | ~0 | Config only. |
| `fleet-gateway` (Ph. 2) | ✅ Easy | <100 MB runtime | Pure I/O; single small Rust binary. |
| Streaming synth (Ph. 3) | ✅ Easy | **<100 MB** | The point — 10-min render becomes cheaper than the current 4-min one. |
| `cns-broker` Rust (Ph. 4) | ✅ Easy | <50 MB runtime; ~2 GB to compile | 24 cores make `cargo build` quick. |
| `memory-indexer` Rust (Ph. 5) | ✅ Good fit | ~1 GB bounded | Constant memory over the full 4,636-file corpus is provable here. |
| Ollama local models | ✅ Already running | 0.4–2.2 GB each | All 9 fit in 6 GB VRAM **one or two at a time**. Serialise; do not warm all five as the Living Minds daemon does. |
| Local embeddings (`nomic-embed-text`) | ✅ | 274 MB | Comfortable. |
| GPU audio via `cupy` | ⚠️ Possible, unnecessary | ~1 GB VRAM | Only if profiling post-Phase-3 shows compute-bound. It will not. |
| CUDA/PTX kernels | ❌ Not worth it | — | `nvcc` absent; GPU idle. |
| Mojo | ❌ | — | Not installed; no fleet experience. |
| Fine-tuning anything >3B | ❌ | — | 6 GB VRAM. Distillation-to-reflexes (the existing approach) is the right call. |
| Full `ai-writings` history rewrite | ⚠️ Tight | Needs **~8 GB free** | 3.7 GB `.git`. Run it with the fleet stopped, or on a machine with headroom. Do not run it alongside Ollama. |

### The standing constraint

The Living Minds daemon keeps five models warm (MEMORY.md, Aug 8). At 0.4–2.2 GB
each that is 6–8 GB against a 6141 MiB GPU, so they spill to host RAM — and host
RAM is the scarce resource. **Recommendation: switch the daemon to serialised
load-on-demand with a short idle eviction.** It is the second-largest memory
consumer after runaway synthesis jobs, and unlike those it runs all day.

### On the VRAM budget — the one place KimiCode is materially wrong

KimiCode reports "3.3GB of 6.1GB in use — real budget for a resident model is
**~500MB, not gigabytes**," attributes it to "display plus existing model loads,"
and builds a GPU strategy on that ceiling. Three measurements, same machine,
same day:

| Time | Used | Free | `ollama ps` |
|---|---|---|---|
| KimiCode's audit | 3300 MiB | ~2800 MiB | (not reported) |
| Mine, 11:20 | **130 MiB** | **6011 MiB** | **empty** |
| Mine, after re-check | 2569 MiB | 3352 MiB | `nomic-embed-text` 323 MB + `granite3.1-dense:2b` 2.0 GB, **both with TTL countdowns** ("27 seconds from now") |

**There is no display baseline and no fixed floor.** Every megabyte of the
observed usage is Ollama model residency under a TTL, evicting itself on a timer.
At 11:20, with the TTLs expired, the card was at 130 MiB — 98% free.

KimiCode measured a transient and designed around it as a hard wall. The
consequences in KimiCode's plan are real: local TTS is written off as
"conditional… probably not resident," and the GPU is demoted to "inference
insurance." **The correct figure is ~6 GB minus whatever we choose to keep
warm** — and what we keep warm is a config line, not a constraint.

This does not change the audio decision (CPU synthesis is right, for the reasons
in §3, and KimiCode's "don't spend the GPU's scarcest resource on arithmetic the
CPU is bored enough to do" is a good line and a correct call). It does change
the TTS decision: with the Living Minds daemon fixed, a quantised TTS model has
room to be resident. **Do not scope the GPU roadmap against 500 MB.**

---

## 6. Summary

Six of seven reported failures have root causes that are missing boundaries
rather than missing performance, and three were misdiagnosed in ways that would
have sent effort in the wrong direction:

- **F2 is not a VRAM problem** — the GPU is 98% idle while a numpy process holds
  16.2 GB of host RAM.
- **F3 does not crash** — it silently drops and re-reads bad packets forever.
- **F7 is not missing** — systemd already supervises four fleet services.

The recommended architecture keeps Python where it is I/O-bound, adds Rust for
the three components whose requirements are literally "bounded memory, typed
validation, and one shared policy across four runtimes," uses the supervisor
that is already installed and running, and declines Go, Mojo and CUDA on the
grounds that they address bottlenecks this fleet does not have.

KimiCode's independent proposal reached the same verdict on Go, Mojo, CUDA and
systemd, and improved this design in eight specific places — most importantly by
replacing my PID-stamped lock files with `flock`, and my per-language resilience
library with a shared localhost gateway. Full reconciliation in §7.

**Phase 1 — writing systemd unit files — removes more risk than every other
phase combined, and involves no new code.** Do it this week.

---

---

## 7. Cross-Pollination — Response to KimiCode's Proposal

*Reviewing `memory/kimi-infrastructure-proposal.md` (KimiCode, Navigation
Officer, 2026-08-13). We worked independently and converged on more than we
diverged on. Where we differ, I have marked who I think is right and why.*

### The headline question: "only two of six failures are language problems"

**I agree with the observation and think KimiCode does not follow it far
enough.** My count is stronger: **zero of seven are language problems.**

Even F2, the one KimiCode marks unambiguously "Yes," is an allocation-discipline
bug. The chunked renderer in §3 fixes it in about fifteen lines of Python with
peak RSS independent of duration. KimiCode's own governing rule — *"memory usage
everywhere is O(chunk) or O(batch), never O(duration) or O(corpus)"* — is the
best sentence in either document, and it is **language-agnostic by construction.**

So the insight is right, and then the recommendation section does something
different with it. KimiCode's own table marks F3 ("No — but Python invites it"),
F4 ("No"), F5 ("No"), and F6 ("No") as non-language problems, and then proposes
rewriting the CNS monitor and the API gateway in Rust anyway. If only the
minority of failures are language problems, that is an argument for **less**
rewriting, not for "Rust for everything in the critical path."

KimiCode's strongest counter is real and I want to state it fairly: *"in Rust the
bounded version is the easy version; in Python the unbounded version was the easy
version."* That is true, and it is the honest case for the rewrite. But it is an
argument about **which mistakes a language makes convenient**, not about
capability — and it has to be weighed against four new binaries to build,
supervise, and staff on a single-operator fleet. I weigh it lower than KimiCode
does for audio (where the fix is a day of Python) and roughly equal for the index
(where bounded memory over a 4,636-file corpus genuinely wants enforcement).

### Where KimiCode is better — adopted into the body of this document

| # | Point | Why KimiCode wins |
|---|---|---|
| **CP-1** | **`flock(2)`, not PID-stamped lock files** | I proposed writing `{pid, started_at}` into a lock and detecting staleness. KimiCode: *"Delete the concept."* Correct — the kernel releases `flock` on process death by any means including `SIGKILL`, while my design reimplements that in userspace **and** carries a PID-reuse race. Clean win; §1 F1 and §3 revised. |
| **CP-2** | **Gateway as a localhost service, not a Python library** | My draft argued "every caller is Python." That was self-undermining — I recommend Rust daemons in this same document, and they need fallback too. Worse, a per-process library **cannot share breaker state**, so each caller rediscovers a dead key independently. §3 and Phase 2 revised. *My addition: the client shim must fail open.* |
| **CP-3** | **`sqlite-vec` in the existing SQLite file** | I never named a vector store. KimiCode's reasoning is exactly right for a single-operator fleet: no new process, no new supervision target, backup is `cp`. Adopted. |
| **CP-4** | **Checkpointed, resumable reindex** | I specified bounded memory but not resumability. "Crash recovery" was in the requirements and KimiCode addressed it directly. Adopted. |
| **CP-5** | **`/mnt/c` is hostile to SQLite (9P locking)** | I missed this entirely. It also **resolves an open question in the master plan**: the WSL-side `~/.hermes/cns_*` directories should be authoritative over the Windows-side ones, and not merely by coin-flip. |
| **CP-6** | **Index provenance in the filename + symlink swap** | I had `(model_id, dim)` in a metadata table. KimiCode's `index.<provider>.<model>.<dims>.db` with `current →` swap is better operationally: build the new index while the old one serves, roll back with `ln -sf`. My version made a provider change an outage. Keep the header field as well — belt and braces. |
| **CP-7** | **JSONL spool over file-per-packet** | My dead-letter *directory* bolted quarantine onto the existing model. An append-only spool with persisted offsets is cleaner: one bad line instead of one immortal file, monotonic progress, no partial-write ambiguity. Adopted — *with a migration caveat KimiCode does not price (§3).* |
| **CP-8** | **`StartLimitBurst`** | Missing from my units. Without it `Restart=always` makes a startup-crash into a hot loop. Adopted — *moved to `[Unit]`, where systemd actually reads it.* |

### Where I hold my position

**1. The VRAM budget is wrong, and it is load-bearing.** KimiCode's "~500MB, not
gigabytes" is a transient Ollama TTL reading mistaken for a hard floor. Measured
three times today: 3300 MiB (KimiCode), **130 MiB with `ollama ps` empty**
(mine), 2569 MiB with two TTL'd models resident (mine). Baseline is ~130 MiB.
Full detail in §5. This changes the local-TTS conclusion and should not be
carried forward.

**2. Audio stays Python (Phase 3, ~1 day) — Rust is week 4 in KimiCode's plan.**
The chunked f32 renderer satisfies KimiCode's own O(chunk) rule today, and
`MemoryMax=2G` makes the guarantee enforceable regardless of language. KimiCode's
arena-and-ring design is genuinely better engineering; it is also three weeks
later, for a bug that is burning 16 GB of the fleet's RAM right now. Ship the
Python fix, keep the Rust renderer as a Phase 6 upgrade if profiling justifies it.
*Also: KimiCode's arithmetic cites "WSL2's 8GB ceiling" while KimiCode's own audit
records `.wslconfig` at `memory=24GB`. The measured process was at 16.2 GB RSS +
1.9 GB swap — there is no 8 GB ceiling.*

**3. `MemoryMax` is not an acceptable thing to defer.** KimiCode's step 1 lists
it as a *"remaining zero-code item: set `MemoryMax` fences on the current
tmux-hosted services **or accept the risk** until week 1 replaces them."* A 16 GB
orphaned process was live on this machine during this analysis, driving available
memory to 1.1 GB. It is hours of work and it is the single highest-value item in
either plan. Do not accept that risk for a week.

**4. The `shell=True` lint is too narrow.** KimiCode found zero instances and
called F5 largely historical. PID 27854 is the counterexample: a heredoc, no
`shell=True`, same bug class, and unnameable in `ps` — which is exactly why it
ran unnoticed for twenty minutes. Broadened rule table in §3.

**5. Two smaller corrections.** KimiCode's table has **six** failures; there are
seven — F6 (git bloat) is absent, so the media-to-R2 policy has no owner in that
plan, and `ai-writings/.git` is at 3.7 GB. And KimiCode's "no PID lockfiles found
anywhere in the workspace — historical, not live" searched the workspace; the
lock is in `~/.npm-global/lib/node_modules/openclaw/`, and the daily log records
clearing a stale one **today**.

### Where we agree without reservation

Go rejected (right language, wrong fleet — KimiCode's phrasing is better than
mine). Mojo rejected, revisit in ~12 months. No hand-written PTX, ever. systemd
rather than a new supervisor, and `MemoryMax` as a per-service OOM fence so a
runaway dies alone. TypeScript stays at the edge and never touches large buffers.
Rust for the CNS daemon and the memory index. Nothing in production hangs off a
terminal multiplexer again.

And the framing, which I would adopt over my own: **"every failure traces to an
unbounded buffer, an unclassified error, or an unmanaged process."** That is the
same conclusion as my §6, said better and shorter.

### Net changes to the plan

- Phase 2 becomes **Rust `fleet-gateway`** (~3 days) instead of a Python library,
  with fail-open client shims.
- Phase 3 (Python streaming audio, ~1 day) **stays where it is** and stays
  Python.
- Phase 5 gains `sqlite-vec`, checkpointing, `flock`, and the symlink swap.
- Phase 1 gains `StartLimitBurst` and remains the highest-priority phase.
- New standing rule, borrowed from KimiCode: **any design whose memory grows
  with input size is rejected at review, in any language.**

---

*Design proposal, 2026-08-13. All hardware figures, toolchain availability,
process states and source line references measured on the live machine.
§7 added after review of KimiCode's independent proposal; eight of its points
adopted into the body above, five disagreements recorded.*
