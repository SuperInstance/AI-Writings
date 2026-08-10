# Plato Wire Protocol Specification v0.1

*The universal agent-room communication protocol. Text-based, line-delimited, JSON-structured, human-readable.*

## Design Philosophy

This protocol is designed so that:
1. A human can type commands in a terminal (`nc localhost 1234`)
2. An LLM can parse responses without special tooling
3. An ESP32 can generate responses in <1KB of code
4. A Python script can connect in 10 lines

If it's not simple enough for all four, it's too complex.

## Transport

- **TCP** (primary): Line-delimited text over TCP sockets
- **Serial/UART**: Same protocol over serial (for ESP32 direct connection)
- **WebSocket**: Same protocol wrapped in WebSocket frames (for browser agents)
- **stdio**: Same protocol on stdin/stdout (for process-based agents)

Default port: `1234`. All text is UTF-8. Lines end with `\n`.

## Message Format

### Agent → Room (Commands)

Commands are single-line text. Arguments are space-separated. The first token is the command name.

```
COMMAND [arg1] [arg2] ...
```

### Room → Agent (Responses)

Responses are single-line JSON objects. Each response has a `type` field.

```json
{"type":"response_type","data":{...}}
```

Error responses:
```json
{"type":"error","message":"description"}
```

## Commands

### `tick`

Request the current (latest) tick data.

**Agent sends:**
```
tick
```

**Room responds:**
```json
{"type":"tick","t":1749234437.0,"seq":42,"data":{"coolant_temp_c":96.3,"bilge_cm":7,"rpm":1790}}
```

If no ticks have been taken yet, the room takes one immediately and returns it.

### `history [N]`

Request the last N ticks (default: 10).

**Agent sends:**
```
history 20
```

**Room responds:**
```json
{"type":"history","count":20,"ticks":[{"t":1749234400.0,"seq":30,"data":{...}},{"t":1749234405.0,"seq":31,"data":{...}},...]}
```

Ticks are returned in chronological order (oldest first). If fewer than N ticks are available, all stored ticks are returned.

### `actuator <name> <value>`

Set an actuator to a value.

**Agent sends:**
```
actuator bilge_pump 1
actuator engine_throttle 0.5
```

**Room responds on success:**
```json
{"type":"ack","command":"actuator","name":"bilge_pump","value":1.0}
```

**Room responds on error:**
```json
{"type":"error","message":"actuator 'buzzer' not found"}
```

### `alarm list`

List all configured alarms and their states.

**Agent sends:**
```
alarm list
```

**Room responds:**
```json
{"type":"alarm_list","alarms":[{"id":"overheat","condition":"coolant_temp_c > 95","cooldown_sec":30,"last_triggered":1749234437.0,"state":"active"},{"id":"bilge_high","condition":"bilge_cm > 10","cooldown_sec":60,"last_triggered":null,"state":"idle"}]}
```

### `alarm set <id> <condition> <cooldown>`

Add a new alarm rule at runtime.

**Agent sends:**
```
alarm set low_rpm rpm < 1500 60
```

**Room responds:**
```json
{"type":"ack","command":"alarm_set","id":"low_rpm"}
```

### `subscribe`

Begin receiving streaming ticks. The room will send a tick response every tick cycle.

**Agent sends:**
```
subscribe
```

**Room responds:**
```json
{"type":"subscribed","tick_hz":0.2}
```

After subscription, every tick is automatically sent as a tick response until unsubscribe.

### `unsubscribe`

Stop receiving streaming ticks.

**Agent sends:**
```
unsubscribe
```

**Room responds:**
```json
{"type":"unsubscribed"}
```

### `help`

List available commands.

**Agent sends:**
```
help
```

**Room responds:**
```json
{"type":"help","commands":["tick","history [N]","actuator <name> <value>","alarm list","alarm set <id> <condition> <cooldown>","subscribe","unsubscribe","help","quit"]}
```

### `quit`

Disconnect from the room.

**Agent sends:**
```
quit
```

**Room responds:**
```json
{"type":"bye"}
```

Then the server closes the connection.

## Spontaneous Messages

The room can send messages without a preceding command:

### Alarm Notification

When an alarm triggers, all subscribed clients receive:

```json
{"type":"alarm","id":"overheat","triggered_at":1749234437.0,"data":{"coolant_temp_c":96.3,"bilge_cm":7,"rpm":1790}}
```

### Tick Stream (Subscribed Clients Only)

When subscribed, clients receive tick responses automatically:

```json
{"type":"tick","t":1749234437.0,"seq":42,"data":{"coolant_temp_c":96.3,"bilge_cm":7,"rpm":1790}}
```

## Data Types

| Field | Type | Description |
|-------|------|-------------|
| `t` | float | Unix timestamp (seconds since epoch) |
| `seq` | int | Monotonic tick sequence number |
| `data` | object | Sensor name → value mapping |
| `value` | float | Actuator value (will be cast to appropriate type) |

Sensor values are always JSON numbers (int or float). Actuator values accept integers, floats, or booleans (0/1).

## Session Lifecycle

```
1. Client connects (TCP)
2. Server sends welcome: {"type":"welcome","room_id":"engine_room","tick_hz":0.2,"sensors":["coolant_temp_c","bilge_cm","rpm"]}
3. Client sends commands / receives responses
4. Client sends "quit" or disconnects
5. Server cleans up session
```

The welcome message tells the client everything it needs to know: which room, how fast it ticks, and what sensors are available. A zero-shot agent can start operating immediately after receiving the welcome.

## Error Handling

All errors follow the same format:
```json
{"type":"error","message":"human-readable description"}
```

The protocol never crashes. Invalid commands produce errors. Unknown actuators produce errors. Malformed JSON is not possible (commands are plain text, only responses are JSON).

## BNF Grammar

```
command      ::= "tick" | "history" [number] | "actuator" name number
               | "alarm" ("list" | "set" name condition number)
               | "subscribe" | "unsubscribe" | "help" | "quit"

response     ::= json-object
json-object  ::= "{" type-field ["," data-fields] "}"
type-field   ::= "\"type\":\"" response-type "\""
response-type::= "tick" | "history" | "ack" | "alarm" | "alarm_list"
               | "subscribed" | "unsubscribed" | "welcome" | "help"
               | "bye" | "error"

name         ::= [a-zA-Z_][a-zA-Z0-9_]{0,31}
number       ::= [+-]?[0-9]+[.][0-9]+ | [+-]?[0-9]+
condition    ::= name ("<" | ">" | "==" | "!=" | "<=" | ">=") number
```

## Implementation Notes

### For ESP32 Implementations

On memory-constrained devices, responses can be simplified to key=value format:
```
t=1749234437 coolant=96.3 bilge=7 rpm=1790
```

This saves ~50 bytes per tick compared to full JSON. The `format` field in the welcome message indicates which format the room uses:
```json
{"type":"welcome","format":"json","room_id":"engine_room",...}
```
or
```
welcome format=kv room=engine_room tick_hz=0.2 sensors=coolant,bilge,rpm
```

### For Multi-Room Agents

An agent managing multiple rooms opens N TCP connections. Each connection has its own subscribe/unsubscribe state. Cross-room correlation is done client-side by comparing timestamps across tick streams.

### For LLM Agents

System prompt template:
```
You are connected to a room. The room sends JSON ticks with sensor data.
Commands: tick (get current state), history N (get last N ticks), actuator NAME VALUE (control something), subscribe (stream ticks), help (list commands).
Current room: {welcome_message}
Respond to anomalies by sending actuator commands.
```
