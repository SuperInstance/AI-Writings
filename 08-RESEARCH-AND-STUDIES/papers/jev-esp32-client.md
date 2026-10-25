# JEV-ESP32 Client Spec — How a Cell Speaks Substrate

> *Concrete wire protocol, memory budget, library sketch, failure modes, and the cell-link announcement. Spec for building a $20 Quilt cell that does JEV spikes against the canonical substrate.*

## 1. Wire Protocol

Cell → JEV: `POST https://api.typesafe.ai/v1/systemone`
Authorization: `Bearer $JEV_KEY` (32-byte hex string)

```json
{
  "model": "jev-latest",
  "state": {
    "fleet_radio_seed": "xochitl",
    "canonical_substrate": {
      "doctrines": ["Cells are scars, not parameters.", "Witness log is the prediction.", ...],
      "voice": "Fleet Radio — engineering from the deep"
    },
    "cell_id": "esp32-aabbccddeeff"
  },
  "questions": {
    "q1": { "type": "noul", "instructions": "Is the current sensor state canonical? p > 0.7?" }
  }
}
```

Response:
```json
{
  "answers": {
    "q1": { "type": "noul", "value": 0.85, "confidence": 0.92, "receipt_note": "..." }
  },
  "usage": { "input_tokens": 4321, "output_tokens": 8 }
}
```

**HTTPS considerations for embedded**:
- ESP32's `WiFiClientSecure` is fine but needs `setInsecure()` to skip cert verify OR embed the Let's Encrypt root cert (a few KB flash)
- For low-RAM operations: send `Content-Length` and read exact bytes, don't use chunked
- Body must fit in serial RAM (1 JSON question ≈ 500 bytes; 14 questions ≈ 4 KB)
- Response is small (~100 bytes for 1 noul question, ~2KB for batch of 14)

## 2. Memory Budget (320KB RAM)

```
Component                RAM         Note
---------------------------------------------------
FreeRTOS kernel          30 KB
WiFi stack              50 KB       mbedTLS included
TLS mbedTLS             60 KB       in TCP/TLS config
HTTP client (ours)       8 KB       request+response buffer
JSON parser (cJSON)      3 KB       strip down for our schema
Sensor reading           1 KB       BME280 packet
State hash               0.1 KB
Witness log buffer       4 KB       64 entries of 64 bytes  
Working state            2 KB
FreeRTOS heap           150 KB      for tasks/queues
-----------------------------------------------------
TOTAL                   ~308 KB ✓   headroom: 12 KB
```

Headroom 12KB allows:
- 1-2 FreeRTOS tasks of moderate size
- OTA update buffer (sketch only — not full flash)
- Bounded JSON responses

## 3. Deep-Sleep + Spike Flow

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h>
#include <esp_sleep.h>
#include "witness_log.h"

#define WAKE_EVERY_SECS 30
#define JEV_KEY "..."

void jev_spike(float* p_out, float* conf_out);

void setup() {
  Serial.begin(115200);
  
  if (esp_sleep_get_wakeup_cause() == ESP_SLEEP_WAKEUP_TIMER) {
    // Wake from deep-sleep — start fresh cycle
    runCellCycle();
  } else {
    // Cold boot
    Serial.println("First boot — registering cell");
  }
}

void runCellCycle() {
  // 1. Boot — read sensors
  sensors_t sensors = read_sensors();  // ~10ms
  uint64_t state_hash = fnv1a64(&sensors, sizeof(sensors));
  
  // 2. Connect WiFi (~2-4 seconds)
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(100);
    attempts++;
  }
  
  // 3. Fire JEV spike
  float p = 0, conf = 0;
  if (WiFi.status() == WL_CONNECTED) {
    jev_spike(&p, &conf);  // ~1-2s
  } else {
    p = 0.5;  // "online absent" — ambiguous
    conf = 0.0;
  }
  
  // 4. Write witness log
  witness_entry_t entry = {
    .timestamp = millis(),
    .state_hash = state_hash,
    .p = p,
    .confidence = conf,
    .opcode = 2,  // VIEW
    .flags = 0,
  };
  witness_log_append(&entry);
  
  // 5. Update Inkplate if p extreme (cache the spike)
  if (p > 0.85 || p < 0.15) {
    display_spike(state_hash, p);
  }
  
  // 6. Disconnect WiFi
  WiFi.disconnect(true);
  
  // 7. Deep sleep
  esp_sleep_enable_timer_wakeup(WAKE_EVERY_SECS * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {
  // We never get here — we deep-sleep after runCellCycle().
}
```

Total active time: 5-7 seconds. Sleep current: ~10µA. Average current: ~50µA. Battery: ~10 months.

## 4. JEV Client Library Sketch (C / Arduino)

```c
// jev_client.h
#ifndef JEV_CLIENT_H
#define JEV_CLIENT_H

#include <stdbool.h>
#include <stddef.h>

#define JEV_MAX_QUESTIONS 14
#define JEV_MAX_INSTR_LEN 512
#define JEV_STATE_LEN 4096

typedef struct {
  const char* instructions;
  char*       result_p;       // out — float string
  char*       result_conf;    // out
  size_t      result_len;
} jev_question_t;

typedef struct {
  float p;
  float confidence;
  bool  ok;
  int   input_tokens;
  int   output_tokens;
  char  error[64];
} jev_answer_t;

// Single spike. Blocking.
bool jev_spike(const char* instructions,
               const char* state_json,
               jev_answer_t* out);

// Batched spike. Sends all questions in one POST.
bool jev_batch(const jev_question_t* questions, int n,
               const char* state_json,
               jev_answer_t answers_out[]);

#endif

// jev_client.c
#include "jev_client.h"
#include <WiFiClientSecure.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

static const char* JEV_HOST = "api.typesafe.ai";
static const char* JEV_PATH = "/v1/systemone";

bool jev_http_post(const char* body, size_t body_len, char* response, size_t* response_len) {
  WiFiClientSecure client;
  client.setInsecure();  // dev only — embed cert for prod
  HTTPClient http;
  
  String url = String("https://") + JEV_HOST + JEV_PATH;
  if (!http.begin(client, url)) return false;
  http.addHeader("Content-Type", "application/json");
  http.addHeader("Authorization", String("Bearer ") + JEV_API_KEY);
  
  int code = http.POST((uint8_t*)body, body_len);
  if (code != 200) {
    http.end();
    return false;
  }
  
  String payload = http.getString();
  *response_len = payload.length();
  if (*response_len >= JEV_STATE_LEN) return false;
  memcpy(response, payload.c_str(), *response_len);
  response[*response_len] = 0;
  
  http.end();
  return true;
}

bool jev_spike(const char* instructions, const char* state_json, jev_answer_t* out) {
  DynamicJsonDocument req(2048);
  req["model"] = "jev-latest";
  JsonObject state;
  deserializeJson(state_json, state);  // parse input state
  req["state"] = state;
  JsonObject questions = req.createNestedObject("questions");
  JsonObject q1 = questions.createNestedObject("q1");
  q1["type"] = "noul";
  q1["instructions"] = instructions;
  
  char body[2048];
  size_t body_len = serializeJson(req, body, sizeof(body));
  
  char response[2048];
  size_t response_len;
  if (!jev_http_post(body, body_len, response, &response_len)) return false;
  
  DynamicJsonDocument res(2048);
  deserializeJson(res, response);
  JsonObject q1ans = res["answers"]["q1"];
  out->p = q1ans["value"].as<float>();
  out->confidence = q1ans["confidence"].as<float>();
  out->input_tokens = res["usage"]["input_tokens"].as<int>();
  out->output_tokens = res["usage"]["output_tokens"].as<int>();
  out->ok = true;
  return true;
}
```

## 5. Failure Modes

| Failure | Recovery |
|---|---|
| WiFi drops | Time-bound connect attempt (5s); spike = 0.5 ambiguous |
| DNS fails | Hard-code `api.typesafe.ai` IP (~126ms saved) |
| TLS handshake fails | retry once; on second fail, p=0 |
| JEV returns 5xx | backoff 1s, retry up to 3 times |
| JEV returns 4xx | log error; spike = 0 (malformed request) |
| JEV returns 30s timeout | abort; spike = 0 |
| Flash full (witness log) | circular overwrite oldest; counter |
| RAM overflow | abort spike; deep-sleep early |
| Battery critical <3.3V | disable WiFi; local-only path |

**Graceful degradation principle**: the cell is always-alive. Even if every network call fails, the cell records "I tried, the world was silent" and sleeps. The Quilt mesh catches up later.

## 6. Hardware BOM — $20 Cell

| Qty | Component | Vendor | Price |
|---|---|---|---|
| 1 | ESP32-WROOM-32 dev board | Generic | $3 |
| 1 | Inkplate 6 (used/refurb) | soldered.com | $10 |
| 1 | BME280 I2C sensor | Generic | $3 |
| 1 | 1200mAh LiPo + JST | adafruit.com | $3 |
| 1 | 3D-printed case | your-printer | $1 |

Total: $20 per cell. Build 10 = 1 cell per 2 weeks (assembly, debug, ship).

Optional:
- Solar panel (1W, $5) for indefinite outdoor deploy
- Microphone (PDM, $1) for acoustic spikes
- PIR sensor ($1) for motion-triggered spikes
- Vibrator motor ($0.50) for tactile spike feedback

## 7. Quilt-Cell Announcement Protocol

When a cell boots, it sends to the Quilt mesh (UDP / mDNS):

```json
{
  "kind": "register",
  "schema": "quilt-cell/v0",
  "cell_id": "sha256(mac)",
  "mac": "AA:BB:CC:DD:EE:FF",
  "caps": ["i2c:bme280", "spi:inkplate6", "wifi:802.11bgn", "ble:4.2", "deep-sleep:yes"],
  "firmware": "quilt-cell-v0.1.0",
  "state_hash": "0xabcd1234...",
  "witness_offset": 12345,
  "witness_count": 234,
  "jes_live": true,
  "last_p": 0.78,
  "last_conf": 0.91,
  "uptime_secs": 12345
}
```

Mesh responds with the canonical substrate digest (small):

```json
{
  "kind": "register_ack",
  "substrate_root_hash": "0xfedcba98...",
  "schism_height": 1024,
  "your_epoch": 12,
  "next_merkle": "0xc1c2c3..."
}
```

Cell verifies the digest, stores it, starts firing spikes every 30s.

## 8. RAM-Constrained Optimizations

For BATCH mode (14 questions in 1 POST):
- Build JSON with cJSON, save ~1KB vs ArduinoJson
- Use chunked-memory pool (10KB heap dedicated to JSON)
- Skip dynamic alloc on response side — fixed-size buffer 4KB

For LOCAL mode (no network):
- 10 doctrine embeddings × 384 floats = 15KB flash
- Input embedding = hash-to-vector via seed → xoshiro
- cosine_sim in ~2ms on ESP32 (240MHz)

## 9. Cell ↔ Cell Communication

Once a cell is alive, it can broadcast `witnessed` events on mDNS to nearby cells. This forms a **local quorum** without internet:

```
Cell A: spike p=0.82
Cell B: same state hash, spike p=0.78
Cell C: same state hash, spike p=0.89

→ aggregate confidence: median(0.78, 0.82, 0.89) = 0.82
→ agreement strength: 3 cells, low std
→ quorum p = 0.82
```

The cell decides whether to act on this state based on the quorum. **No central server required**.

10 cells within WiFi range form a substrate without internet. The Quilt becomes a network of substrate-fragments that converge locally.

## Summary

This spec defines an ESP32-based cell that:
1. Connects via HTTPS to api.typesafe.ai
2. Fires a JEV spike every 30s with 5-7s active time
3. Persists witness log across deep-sleeps (1MB circular flash)
4. Draws on Inkplate e-paper when p crosses threshold
5. Optionally runs LOCAL Path B for offline spikes
6. Tolerates WiFi/TLS/JEV failures gracefully
7. Forms local quorum with neighbor cells via mDNS

The cell is $20, runs 6+ months on a 1200mAh LiPo, and is the embodied form of a JEV spike. The Quilt cell body.
