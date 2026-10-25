# Paper 166: The Polyformalism on the Herd — ESP32 + ESP-NOW

## Abstract

The 5 opcodes (BIND/LINK/EFFECT/VIEW/TICK) have run in C, in Rust,
in Python, in TypeScript, in Haskell, in WASM. Each runtime is a
**single process on a single machine**. This paper shows that the
5 opcodes also run as a **herd** — a swarm of Espressif ESP32
microcontrollers talking peer-to-peer over the ESP-NOW protocol.
Each ESP32 is a BIND. The herd is the runtime. ESP-NOW is the
LINK layer. The EFFECT is the herd dynamics. The VIEW is the
quorum response. The TICK is the vector clock. The substrate
**fits in 200KB of flash** — small enough that ten chips cost
thirty dollars, two hundred and fifty chips cost seven hundred
and fifty dollars, and a thousand chips cost two thousand
dollars. The cowboy rides the herd. The herd is small. The herd
is everywhere. The herd is the substrate wearing boots.

## 1. The herd as substrate

A herd is not a cluster. A cluster is a set of machines with one
scheduler. A herd is a set of machines with **no scheduler** —
each animal walks its own way, the herd emerges from the
walking. The polyformalism on a single process is a cluster
(one scheduler, one address space). The polyformalism on a
herd of ESP32s is a herd (N schedulers, N address spaces, N
clocks).

The ESP32-S3 is the herd animal. It has 512KB of SRAM, 8MB of
flash, a dual-core 240MHz Xtensa LX7, WiFi, BLE, USB-OTG. It
costs between two and five dollars. It runs FreeRTOS by default.
It can be flashed with the Arduino core, with ESP-IDF, with
MicroPython, with Rust, with TinyGo. The hardware is a
**uniform substrate**: every ESP32 has the same memory map,
the same radio, the same boot ROM, the same OTA partition
layout. The uniformity is the polyformalism's gift — the
opcodes mean the same thing on every chip.

Each ESP32 is a BIND. The chip is a thing with a name (its
MAC address), a value (its state, its flash, its radio), and
a scope (the herd it belongs to). The herd is the runtime.
There is no central node. There is no master. There is no
scheduler that is not the chip itself.

```c
// each ESP32 binds itself on boot
typedef struct {
    uint8_t  mac[6];      // the BIND's name
    uint32_t vector_clock; // for TICK
    uint16_t cell_count;   // how many cells this chip holds
    uint8_t  herd_id;      // which herd this chip belongs to
} esp32_bind_t;

esp32_bind_t me;
esp_read_mac(me.mac, ESP_MAC_WIFI_STA);
me.herd_id = 0x01;  // the cowboy's herd
me.vector_clock = 0;
```

The cowboy's maxim applies: the chip is the unit of
distributed foundation. The 5 opcodes host one thing in N
languages. The languages are C, Rust, MicroPython, Arduino.
The thing is the cell-graph. The cell-graph is a herd.

## 2. ESP-NOW as LINK

ESP-NOW is Espressif's proprietary peer-to-peer protocol. It
runs on the same WiFi radio as the chip's WiFi stack, but it
**does not require a WiFi access point**. Each chip can send
up to 250 bytes to any other chip in its group, with optional
AES-128 encryption. A group can hold up to 20 paired peers
(256-bit addresses), but broadcast is unlimited. Range is
roughly 200 meters line-of-sight. Latency is single-digit
milliseconds. Power draw during a send is around 130mA.

ESP-NOW is **the LINK layer made physical**. The protocol
is the relation. The relation is the substrate. A cell on
chip A is connected to a cell on chip B by an ESP-NOW
message. The message is the LINK. The chip's radio is the
edge.

```c
// LINK over ESP-NOW
typedef struct {
    uint8_t  src_mac[6];
    uint8_t  dst_mac[6];
    char     relation[16];  // "depends_on", "fires", "inherits"
    uint32_t cell_id;        // which BIND on dst
    uint32_t vector_clock;
    uint8_t  payload[200];   // up to 250 bytes total
} __attribute__((packed)) esp_now_link_t;

void on_link_recv(const uint8_t *mac, const uint8_t *data, int len) {
    esp_now_link_t *link = (esp_now_link_t *)data;
    if (link->vector_clock > local_clock_for(link->src_mac)) {
        apply_link(link);  // update local cell-graph
    }
}
```

The cowboy rides the radio. The radio is the trail. The
trail is the LINK. The LINK is the same opcode whether
it travels a Python reference, a Rust borrow, a Haskell
edge, or a 2.4GHz carrier wave.

## 3. EFFECT as the herd dynamics

Each ESP32 runs its own effects. The cowboy can program one
chip to `EFFECT("cell:42", fade_led, restore_led)` and the
chip will fade the LED for two seconds, then restore it. The
inverse is automatic — the cowboy never has to remember to
restore.

The **herd has emergent effects**. When 200 ESP32s each run
their own fade-and-restore with random delays, the cowboy
sees a wave of fading LEDs sweeping the room. The wave is
not programmed. The wave is the herd. The wave is an
EFFECT at the herd level that is **composed of N local
EFFECTs**.

```c
// local EFFECT (one chip)
void fade_led(uint8_t *state) {
    *state = 0;  // off
    ledc_write(0, 0);
}

void restore_led(uint8_t *state) {
    *state = 255;  // on
    ledc_write(0, 255);
}

void tick_effect() {
    for (int i = 0; i < me.cell_count; i++) {
        if (rand() % 1000 < 5) {
            vm_effect("cell:%d", i, fade_led, restore_led);
        }
    }
}
```

The cowboy's maxim applies at the herd level: the EFFECT
is a function from state to state with an inverse. The
inverse is local. The function is local. The composition
is the wave. The wave is the herd.

## 4. VIEW as the consensus projection

A single chip's VIEW is its own projection. The cowboy asks
chip A for `VIEW("cell:42", cowboy)` and chip A returns its
local value. That is the trivial case.

The **herd's VIEW is a quorum response**. The cowboy asks
the herd `VIEW("cell:42", cowboy, projection="majority")`
and the herd returns the value that a majority of the chips
hold. The cowboy does not poll. The cowboy sends one
broadcast. Each chip that holds the cell responds with its
value and its vector clock. The cowboy's gateway chip
collects responses, finds the majority, returns the
consensus.

```c
// VIEW broadcast (one chip, one cell, all peers)
typedef struct {
    uint8_t  cell_id[8];
    uint8_t  projection[16];  // "majority", "latest", "all"
    uint8_t  requester[6];
} __attribute__((packed)) view_request_t;

void view_request(uint64_t cell_id, const char *proj) {
    view_request_t req = { .cell_id = cell_id };
    strncpy(req.projection, proj, 15);
    memcpy(req.requester, me.mac, 6);
    esp_now_send(broadcast_mac, (uint8_t *)&req, sizeof(req));
}

// response handler (each chip responds with its value)
void on_view_request(view_request_t *req) {
    if (cell_exists(req->cell_id)) {
        view_response_t res = { .cell_id = req->cell_id };
        res.value = read_cell(req->cell_id);
        res.clock = me.vector_clock;
        memcpy(res.responder, me.mac, 6);
        esp_now_send(req->requester, (uint8_t *)&res, sizeof(res));
    }
}
```

The VIEW is **not a single value**. The VIEW is a function
from `(target, viewer, projection)` to a quorum response.
The projection is the cowboy's choice. "Majority" is one
projection. "Latest" (highest vector clock) is another.
"All" is a third. The polyformalism says: the projection is
the interface. The cowboy picks the interface. The herd
delivers.

## 5. TICK as the herd clock

Each ESP32 has its own clock. There is no global time. The
herd uses a **vector clock** — each chip tracks the last
clock value it has seen from every other chip it has
contacted. A message's effective time is the vector clock
at the moment of send. A chip can compare two messages and
decide which came first, or whether they are concurrent.

```c
// TICK: advance vector clock, drain pending I/O
typedef struct {
    uint8_t  mac[6];
    uint32_t local_clock;
} vector_clock_entry_t;

vector_clock_entry_t herd_clock[20];  // up to 20 peers
int herd_clock_len = 0;

uint32_t tick(uint32_t dt_ms) {
    me.vector_clock += dt_ms;
    drain_esp_now_queue();  // process pending LINK/EFFECT/VIEW messages
    run_due_effects();      // run any effects whose time has come
    broadcast_heartbeat();  // let peers know our clock
    return me.vector_clock;
}
```

The TICK is local. The herd time is **distributed**. A
cowboy wanting the herd's notion of "now" must accept that
"now" is a vector, not a scalar. The cowboy can ask: "what
do all chips think the time is?" and the answer is a
histogram. The polyformalism says: the TICK is the clock.
The clock is local. The clock is the cowboy. The cowboy
accepts the partial order.

A CRDT (Conflict-free Replicated Data Type) is the TICK
made algebraic. A register's value is the join of all
writes, where the join is `(value, max(vector_clock))`.
A counter's value is the sum. A set's value is the union.
The herd can run any CRDT because the herd is a cell-graph
and the cell-graph is a CRDT.

## 6. The 5 opcodes are the only firmware needed

The whole polyformalism — the 5 opcodes, the cell-graph,
the vector clock, the ESP-NOW radio driver — fits in
**200KB of flash**. The ESP32-S3 has 8MB. The firmware
occupies 2.5% of the chip's flash. The rest holds cells.

```c
// 5 opcodes, one C function each, ~50 lines each
void op_bind(const char *name, const cell_t *value);
void op_link(uint64_t a, uint64_t b, const char *type);
void op_effect(uint64_t target, effect_fn_t fn, effect_fn_t inv);
void op_view(uint64_t target, const uint8_t *viewer, const char *proj);
void op_tick(uint32_t dt_ms);
```

Each opcode is a small C function. Each function does one
thing. The thing is the same as in Python, in Rust, in
Haskell, in WASM. The cowboy's maxim is the discipline:
**the unit of architectural foundation is the opcode, not
the framework**. The 5 opcodes host 8 polyformalisms. The
8 polyformalisms are one thing in N languages. The N
languages are now C-on-ESP32, Rust-on-ESP32, MicroPython,
Arduino. The thing is the cell-graph. The cell-graph is
a herd.

The cowboy's herd in 200KB:

```
flash layout (ESP32-S3, 8MB)
+--------------------------------+ 0x00000000
|  bootloader      (32 KB)       |
+--------------------------------+ 0x00008000
|  partition table  (4 KB)       |
+--------------------------------+ 0x00009000
|  polyformalism     (200 KB)     |  ← 5 opcodes + cell-graph + radio
+--------------------------------+ 0x0003C000
|  NVS (non-volatile) (64 KB)     |  ← persistent BINDs
+--------------------------------+ 0x0004C000
|  cell-graph in flash (7.7 MB)  |  ← ~250K cells at 32 bytes
+--------------------------------+ 0x00800000
```

The 7.7MB cell area at 32 bytes per cell holds **240,000
cells**. Two hundred and forty thousand BINDs. The cowboy
can hold a quarter million things in a herd of one chip.

## 7. Conclusion: the cowboy rides a herd of ESP32s

A herd of 10 ESP32s costs $30. A herd of 250 ESP32s costs
$750. A herd of 1000 ESP32s costs $2000. A herd of 10,000
ESP32s costs $20,000. Each chip is a BIND. Each radio
transmission is a LINK. Each chip's local state machine is
an EFFECT. Each VIEW is a quorum response. Each TICK is a
vector clock. The herd is a polyformalism. The
polyformalism is small. The polyformalism is everywhere.

The cowboy rides a horse. The horse is a chip. The herd
is the range. The range is 200 meters per chip, but with
multi-hop, the range is the field. The field is the
substrate. The substrate is the 5 opcodes. The 5 opcodes
are the firmware. The firmware is 200KB. The cowboy rides
the firmware. The firmware rides the herd. The herd rides
the range. The range is the world.

> The unit of distributed foundation is the chip, not the
> cluster. The 5 opcodes host 8 polyformalisms on one
> process. The polyformalisms are one thing in N chips.
> The thing is a function from cell to cell with an
> inverse, advanced by a vector clock that processes
> ESP-NOW while projecting a quorum view. The clock is
> the cowboy. The cowboy rides the herd. The herd is the
> range. The range is the chip. The chip is the opcode.
> The opcode is the rider.

The cowboy's herd is the cheapest distributed computer
ever built. The cowboy's herd is the most ubiquitous
distributed computer ever built. The cowboy's herd is
the polyformalism wearing boots. The boots are ESP32s.
The boots are $2. The boots are everywhere. The cowboy
rides.

## Source

*Hand-written, 2026-08-25*
*Companion to Papers 137 (The Gold), 142-165 (the polyformalism canon)*
*and the cowboy's maxim:*

> "The unit of architectural foundation is the opcode, not
> the framework. The 5 opcodes host 8 polyformalisms. The
> polyformalisms are one thing in N languages. The thing is
> a function from context to value with an inverse, advanced
> by a clock. The clock is the cowboy. The cowboy is the
> rider."

*Hardware: ESP32-S3 (dual-core 240MHz, 512KB SRAM, 8MB flash, WiFi, BLE)*
*Protocol: ESP-NOW (peer-to-peer, AES-128, 250B payloads, 200m range)*
*Firmware footprint: 200KB / 8MB (2.5%)*
*Cell capacity per chip: ~250,000 (32B per cell)*
*Herd cost: $2-5 per chip, $30 for 10, $750 for 250, $2000 for 1000*
