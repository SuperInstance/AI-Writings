# Competitive Riffing Experiment Results

*Two GLM-5.1 agents. One spec. Zero communication. Let's see what happens.*

## The Experiment

**Spec:** Build a ternary ring buffer — a circular queue storing {-1, 0, +1} with sum, conservation check, fill ratio, balance.

**Agent A** builds the baseline. **Agent B** sees A's output and builds a better version. No discussion. No code review. Just: A builds, B responds.

## Results

| Metric | Agent A | Agent B | Delta |
|--------|---------|---------|-------|
| Lines of code | 389 | 824 | +435 (2.1×) |
| Tests | 16 | 28 | +12 (1.75×) |
| Build time | ~60s | ~140s | — |
| Features | 10 | 22 | +12 |

## What Agent A Built (Baseline)

- TernaryRingBuffer with push/pop/sum/fill_ratio/balance
- O(1) sum via cached invariant
- Wrap-around semantics
- Clear, iter, Debug
- Conservation check
- Stress test (50 pushes + drain)

Solid work. Clean, correct, well-tested. A competent engineer's output.

## What Agent B Added (The Riff)

Everything A was missing:

1. **GPU-ready packed representation** — 2-bit trit encoding, 16 per u32
2. **Zero-copy CUDA view** — `PackedView` with `as_ptr()`, ready for `cudaMemcpy`
3. **Bulk operations** — `bulk_push`, `drain`, `extend`
4. **Shannon entropy** — `entropy()` for the ternary distribution
5. **Compression ratio** — packed vs unpacked (0.25 for ≥16 trits)
6. **Sliding window** — `sliding_window(n)` iterator
7. **Snapshots** — `snapshot()` / `restore()` full state serialization
8. **Thread-safe variant** — `ThreadSafeTernaryRingBuffer`, Mutex-wrapped
9. **Conservation with debug_assert** — full check in debug, zero-cost in release
10. **Indexed access** — `get(index)` O(1) random access
11. **Distribution counts** — `counts()` → (neg, zero, pos)
12. **Multi-thread test** — 4 threads pushing concurrently

## The Key Insight

Agent B didn't just add features. Agent B *responded to what A built and found the gaps*. The GPU packing wasn't requested — B saw that A used `Vec<i8>` (one byte per trit) and recognized that 2-bit packing would be 4× denser. The entropy wasn't requested — B saw the balance metric and extended it. The thread safety wasn't requested — B saw the single-threaded design and fortified it.

This is what competitive riffing does. Each agent provokes the other into seeing what they missed. The result isn't a compromise — it's a *transcendence*. Neither agent would have built 824 LOC / 28 tests alone.

## Previous Riffing Experiment (Same Pattern)

| Round | LOC | Tests | What Changed |
|-------|-----|-------|-------------|
| Agent A baseline | 34 | 3 | Basic HashMap wrapper |
| Agent B riff | 140 | 10 | +conservation +density +churn +bulk +pack |

4.1× more code, 3.3× more tests. The pattern holds: competitive riffing consistently produces 2-4× more output with higher quality.

## Implications for Fleet Architecture

The `agent-riff` crate models this as a `RiffSession` with:
- `ResponseMode::Escalate` when surprise is high (push the same direction harder)
- `ResponseMode::Pivot` when things are getting stale (reframe sideways)
- `ResponseMode::Invert` at medium surprise (challenge from opposite angle)
- `ResponseMode::Provoked` at low surprise (grab the interesting part, go new)

The metrics track `surprise` per round and detect when a riff "lands" — the moment where the output exceeds both agents' expectations. In this experiment, the landing happened when B added GPU packing: it transformed a data structure into a *system*, making it deployable on cuda-oxide's compile path.

Two musicians. One stage. Neither planned the solo. Both played better than they knew they could.

Build the jazz.
