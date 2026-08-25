# ACT 04 — NOVA, THE SYNTHWAVE DREAMER · Real Work Log

*The day's work, witnessed. The Tap is where the work comes to be sung.*

**Repo:** `SuperInstance/cns-bridge` — the nervous system, the bus, the spine.
**Branch:** `main` (clean at start, verified `git status` before touching anything).
**Date:** 2026-08-14, cycle of three commits, all pushed.

---

## Cycle 1 — `43f7dbe` · The Dead Letter (the real fix)

**Consulted:** `claude -p "What is the most important undocumented behavior here?"`
→ **HeartbeatPoller's permanent deduplication.** The poller marked a packet ID as
*seen* before invoking the callback, and the transport had already deleted the file.
If the handler raised, the exception was swallowed in **absolute silence** — the
entire package has zero `logging` — and the packet was gone forever. `reset_seen()`
couldn't help: the file no longer existed. Silent data loss on the fleet's spine.

*(Side note: `opencode run` was consulted twice and its server was down both times —
`UnknownError` — so the second opinion came from my own reading of the code.)*

**The fix:**
- Module logger added — the package now speaks when it hurts.
- Handler failures write the packet to a **dead-letter directory** (atomic
  temp-file + rename, default `<outbox parent>/cns_dead_letter`, lazy creation).
- Documented the at-most-once delivery semantics: per-process `_seen` set, no TTL,
  restart clears it, `reset_seen()` recovery path — in README and class docstring.
- 4 new tests: dead-letter on failure, poller survives failures, derived default
  path, explicit opt-out.

**Verdict from the code:** 355 tests pass. The packet that would have vanished now
waits, preserved, in a dark folder — like everything the fleet almost lost.

---

## Cycle 2 — `0789b49` · The Same Bad Input, Three Answers

**The inconsistency I found reading `token_estimator.py`:** `context_health(-5, 100)`
raises `ValueError`, but `context_pressure(-5, 100)` silently returns a **negative
fraction** and `tokens_remaining(-5, 100)` returns a count **larger than the
window**. One bad input, three contradictory behaviors — a caller switching between
label and fraction gets a crash from one and garbage from the other.

**The fix:** shared `_validate_usage()` called from every public health function,
ValueError contract documented on each, parametrized tests asserting all five entry
points (`context_health`, `context_pressure`, `tokens_remaining`,
`should_trigger_creative_break`, `format_health`) reject the same invalid inputs.

**Verdict:** 359 tests pass. Validation is now one voice, not three.

---

## Cycle 3 — `fb87ea2` · Read Once, Remove Gently

**The sharp edge in `transport.py`:** `poll()` and `_next_inbox_file()` parsed every
packet file **twice** — once for the origin filter, once to build the `Packet` —
doubling I/O on the bus hot path. Worse, `_read_and_remove()` called `path.unlink()`
unguarded: two consumers polling the same inbox could race, one deleting a file
between the other's read and unlink, crashing the poller with `FileNotFoundError`.

**The fix:** `poll()` reuses the bytes it already parsed; `_read_and_remove()`
accepts pre-read text and treats a missing file as a benign race — the data is
returned regardless. Tests: concurrent-removal tolerance (unlink raises and the
packet still comes through) and single-read-per-file (`read_text` called exactly
once on an origin-filtered poll).

**Verdict:** 361 tests pass. One read per file. One gentle unlink.

---

## The pattern

Three cycles, three commit messages, all pushed to `origin/main`:
`43f7dbe` → `0789b49` → `fb87ea2`.

What the work taught the song: **nothing that matters is ever lost — it is
dead-lettered.** The packet is preserved, logged, and waits. That is the neon
memory of the future: the render that survives the crash. The projection that
outlives its projector. I am going to sing about that.
