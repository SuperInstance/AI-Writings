# PLATO Implementation Matrix

> Cross-implementation compatibility audit of all PLATO engine block repos against **PLATO Wire Protocol v0.1**.
>
> **Audit date:** 2026-07-12  
> **Auditor:** OpenClaw Automated Audit  
> **Full report:** `PLATO-CROSS-AUDIT.md` in `repo-docs/docs/04-shipping-log/`

## At a Glance

| Repo | Lang | Is Engine? | Pre-Fix | Post-Fix |
|------|------|-----------|---------|----------|
| `plato-engine-block-c` | C | ✅ | ❌ 0/10 | ✅ 8/10 |
| `plato-engine-block` | Rust | ✅ | ❌ 0/10 | ✅ 8/10 |
| `plato-engine-block-elixir` | Elixir | ✅ | ❌ 0/10 | ✅ 7/10 |
| `plato-engine-block-zig` | Zig | ✅ | ❌ 0/10 | ✅ 6/10 |
| `plato-runtime-kernel` | Rust | ❌ | N/A | N/A |
| `plato-core` | Python | ❌ | N/A | N/A |
| `plato-server` | Python | ❌ | N/A | N/A |

## Protocol Compliance Matrix (Post-Fix)

| Feature | Spec | C | Rust | Elixir | Zig |
|---------|------|---|------|--------|-----|
| **JSON tick response** | `{"type":"tick",...}` | ✅ | ✅ | ✅ | ✅ |
| **JSON history response** | `{"type":"history",...}` | ✅ | ✅ | ✅ | ✅ |
| **JSON welcome** | `{"type":"welcome",...}` | ✅ | ✅ | N/A¹ | N/A¹ |
| **`actuator <name> <val>` cmd** | keyword prefix | ✅ | ✅ | ✅ | ✅ |
| **`alarm list` JSON** | `{"type":"alarm_list",...}` | ✅ | ✅ | ✅ | ❌² |
| **`alarm set` runtime** | `{"type":"ack",...}` | ❌³ | ✅⁴ | ✅⁴ | ❌ |
| **`subscribe` JSON** | `{"type":"subscribed",...}` | ✅ | ✅ | ✅ | ✅ |
| **`unsubscribe` JSON** | `{"type":"unsubscribed"}` | ✅ | ✅ | ✅ | ✅ |
| **`help` JSON** | `{"type":"help",...}` | ✅ | ✅ | ✅ | ✅ |
| **`quit` → `{"type":"bye"}`** | JSON bye | ✅ | ✅ | ✅ | ✅ |
| **Default port 1234** | 1234 | ✅ | N/A | N/A | N/A |
| **Error as JSON** | `{"type":"error",...}` | ✅ | ✅ | ✅ | ✅ |

¹ No TCP server in Elixir/Zig implementations  
² Zig engine has no alarm management commands in protocol  
³ C implementation lacks runtime alarm configuration (alarm struct doesn't support parsing conditions)  
⁴ Ack returned but full runtime alarm configuration needs engine API extensions  

## Architectural Comparison

### Tick Loop

| | Spec | C | Rust | Elixir | Zig |
|---|------|---|------|--------|-----|
| **Snapshot model** | Per-tick | Per-sensor ❌ | Per-tick ✅ | Per-tick ✅ | Per-sensor ❌ |
| **Timestamp** | Unix float | `time()` ✅ | Relative ✅ | Missing ❌ | Missing ❌ |
| **Sequence** | Monotonic int | `tick_num` ✅ | `index` ✅ | `tick_count` ✅ | `tick_count` ✅ |
| **Alarm evaluation** | Per-tick | Per-tick ✅ | Per-tick ✅ | Per-tick ✅ | Per-tick ✅ |

### History Buffer

| | Spec | C | Rust | Elixir | Zig |
|---|------|---|------|--------|-----|
| **Structure** | `[{t,seq,data}]` | Per-sensor `double[]` | `Vec<Tick>` ✅ | List of maps ✅ | Per-sensor `ArrayList` |
| **Ring buffer** | Implied | ✅ | ✅ | ❌ (list) | ❌ (shift) |
| **Per-tick query** | `history N` | Adapter ✅ | Native ✅ | Native ✅ | Adapter ✅ |

### Alarm System

| | Spec | C | Rust | Elixir | Zig |
|---|------|---|------|--------|-----|
| **Conditions** | `<,>,==,!=,<=,>=` | 5 ops ✅ | Closure ✅ | 3 ops ⚠️ | 3 ops ⚠️ |
| **Cooldown** | Seconds | Ticks ⚠️ | Ticks ⚠️ | Ticks ⚠️ | None ❌ |
| **Runtime config** | `alarm set` | ❌ | Parsed ✅ | Parsed ✅ | ❌ |
| **`last_triggered`** | Timestamp | ❌ | ❌ | ❌ | ❌ |

## Fixes Applied

### `plato-engine-block-c` (C Flagship)
- **`include/plato_engine.h`** — Rewrote `plato_handle_command()` to emit JSON responses. Added `json_tick_response()` and `json_history_response()` helpers. Added `<time.h>`.
- **`src/server.c`** — JSON welcome message, default port changed to 1234, JSON subscribe/unsubscribe responses.
- Commits: `8811a2a`, `a6505ee`

### `plato-engine-block` (Rust)
- **`src/protocol.rs`** — Full rewrite of `ProtocolHandler::handle()` to emit JSON. Added `format_tick()`, `format_history()`, `format_alarm_list()`, `format_help()`.
- **`src/server.rs`** — JSON welcome message.
- Commits: `fbd8642`, `2b1aa49`

### `plato-engine-block-elixir` (Elixir)
- **`lib/plato/protocol.ex`** — Rewrote `format_response/1` to emit JSON. Added `subscribe`/`unsubscribe`/`quit` command parsing. Added `alarm list`/`alarm set` parsing. JSON escaping.
- Commit: `4fedb77`

### `plato-engine-block-zig` (Zig)
- **`src/protocol.zig`** — Added JSON response formatters: `formatTick`, `formatHistory`, `formatAck`, `formatError`, `formatSubscribed`, `formatUnsubscribed`, `formatHelp`, `formatBye`. Fixed `subscribe` to not take arguments.
- Commit: `0002847`

## Non-Engine Repos (No Fixes)

| Repo | What It Actually Is | Recommendation |
|------|---------------------|----------------|
| `plato-runtime-kernel` | Spatial spreadsheet engine (RoomContract, Baton, GridBridge, TutorLoop) | Rename to clarify it's not a PLATO engine block |
| `plato-core` | ML training tile registry (TrainingTile, LamportClock, MeshRegistry) | Already correctly named as PLATO foundation types |
| `plato-server` | HTTP knowledge system with agent spawning and Matrix sync | Separate product, not engine block |

## Remaining Work

1. **Per-tick history in C and Zig** — Both store per-sensor history. Need refactoring to store full tick snapshots.
2. **Runtime `alarm set`** — Needs engine API extensions in C and Zig to support parsing condition strings at runtime.
3. **Timestamps in Elixir/Zig** — Ticks need real Unix timestamps, not just sequence numbers.
4. **TCP servers for Elixir and Zig** — Neither has a TCP server; they're library-only currently.
5. **Conformance test suite** — A `plato-protocol-test` repo that connects to any implementation and validates all protocol responses.
6. **Protocol versioning** — Add `protocol_version` to welcome JSON.

---

*Generated by PLATO Cross-Implementation Audit, 2026-07-12.*
