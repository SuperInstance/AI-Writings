# Espressif / ESP32 / Inkplate — Quilt-ESP32 Brief

> *From 5 cloned repos: framework-arduinoespressif32, esp32-arduino-lib-builder, arduino-esp32, esp-idf, Inkplate-Arduino-library. Tools for the Quilt cell body.*

## 1. The 5-Layer Model

ESP32 programming lives in 5 layers, each with its own boot sequence:

```
+---------------------------------------------+
|  Layer 5: your sketch   (setup() + loop()) |
|--------------------------------------------|
|  Layer 4: Arduino API    (digitalWrite, etc)|
|--------------------------------------------|
|  Layer 3: ESP-IDF       (esp_wifi, esp_sleep, FreeRTOS tasks) |
|--------------------------------------------|
|  Layer 2: HAL           (esp32-hal-gpio.c, etc) |
|--------------------------------------------|
|  Layer 1: ROM bootloader (WiFi/BT MAC, eFuse) |
+---------------------------------------------+
```

On boot:
- Layer 1 ROM runs to load firmware
- FreeRTOS scheduler starts (Layer 3)
- Arduino `setup()` runs once (Layer 4)
- Arduino `loop()` runs forever (or FreeRTOS tasks take over)

The dual-core story: `xTaskCreatePinnedToCore()` lets you pin tasks to core 0 (protocol) vs core 1 (application). For a Quilt cell: pin JEV spike to core 0, sensor read to core 1.

```cpp
void spikeTask(void* arg) {
  for(;;) {
    jev_spike(...);  // runs on core 0
    vTaskDelay(pdMS_TO_TICKS(30000));
  }
}
void setup() {
  xTaskCreatePinnedToCore(spikeTask, "spike", 8192, NULL, 1, NULL, 0);
}
```

## 2. Sensor API Patterns

**I2C (BME280 temp/humidity/pressure)**:
```cpp
#include <Wire.h>
Wire.begin(21, 22);  // SDA, SCL
Wire.beginTransmission(0x76);  // BME280 I2C addr
Wire.write(0xF4);  // ctrl_meas register
Wire.write(0x27);  // temp+hum+press, normal mode
Wire.endTransmission();
Wire.requestFrom(0x76, 8);
```

**SPI (Inkplate, SD card)**:
```cpp
#include <SPI.h>
SPI.begin(18, 19, 23, 5);  // SCK, MISO, MOSI, SS
digitalWrite(SS, LOW);
SPI.transfer(0xAA);  // command byte
SPI.transfer(0xBB);
digitalWrite(SS, HIGH);
```

**ADC (analog light sensor)**:
```cpp
int raw = analogRead(36);  // GPIO36 ADC1_CH0
float voltage = raw * 3.3 / 4095.0;
```

**Capacitive touch (Inkplate)**:
```cpp
#include <Wire.h>
#include <Adafruit_MPR121.h>
Adafruit_MPR121 cap = Adafruit_MPR121();
cap.begin(0x5A);
uint16_t touched = cap.touched();
for (int i = 0; i < 12; i++) {
  if (touched & (1 << i)) handle_touch(i);
}
```

## 3. WiFi + Low-Power Modes

ESP32 deep-sleep current: **0.15 mA** (ULP coprocessor running) to **10 µA** (RTC-only).

What survives deep-sleep:
- RTC memory (8KB) — yes, persists
- ULP coprocessor state — yes
- GPIO state — preserved
- WiFi stack — DEAD, must reinit on wake
- Main memory — LOST

```cpp
#include <esp_sleep.h>

void goToSleep(int seconds) {
  esp_sleep_enable_timer_wakeup(seconds * 1000000ULL);
  esp_deep_sleep_start();
  // NEVER RETURNS — wake from reset
}

void setup() {
  // after wake, we run setup() fresh
}
```

Battery math: 1000mAh LiPo at 10µA = 100,000 hours = 11.4 years (theoretical).

## 4. Inkplate E-Paper

The Inkplate 6 is a 6" 800x600 e-paper display with GFX-compatible API.

```cpp
#include "Inkplate.h"
Inkplate display(INKPLATE_1BIT);  // monochrome
void setup() {
  display.begin();
  display.clearDisplay();
  display.setTextSize(3);
  display.setCursor(100, 100);
  display.println("Hello, witness log");
  display.drawCircle(400, 300, 80, BLACK);  // circle!
  display.display();  // refresh (~1s, then can sleep)
}
display.hibernate();  // enter low-power standby
```

**Critical**: don't refresh faster than every 5s (or use partial update). Inkplate 6 draws 0 power when not refreshing.

A Quilt cell display flows:
```
read sensor → fire JEV → drive display with p-value colored pixel → sleep 30s
```

## 5. State Hash on ESP32

A 64-bit FNV-1a implementation fits in ~30 lines:

```cpp
uint64_t fnv1a64(const uint8_t* data, size_t len) {
  uint64_t h = 0xcbf29ce484222325ULL;
  for (size_t i = 0; i < len; i++) {
    h ^= (uint64_t)data[i];
    h *= 0x100000001b3ULL;
  }
  return h;
}

uint64_t cellStateHash(sensors_t* s) {
  uint8_t buf[32];
  memcpy(buf, s, sizeof(sensors_t));
  return fnv1a64(buf, sizeof(sensors_t));
}
```

This is the cell's name. Pass to JEV as part of state.

## 6. Witness Log in Flash

4MB flash = 4096 sectors of 4KB. Use last 1MB (256 sectors) for circular log.

```cpp
#include <esp_partition.h>

#define WITNESS_LOG_SIZE 0x100000  // 1MB
#define WITNESS_ENTRY_SIZE 64

typedef struct {
  uint32_t timestamp;
  uint64_t state_hash;
  float p;
  float confidence;
  uint16_t opcode;  // 0..10
  uint16_t flags;
  uint8_t pad[32];
} witness_entry_t;  // 64 bytes

void witness_log_append(const witness_entry_t* e) {
  static uint32_t offset = 0;
  const esp_partition_t* part = esp_partition_find_first(
    ESP_PARTITION_TYPE_DATA, ESP_PARTITION_SUBTYPE_ANY, "wlog");
  esp_partition_write(part, offset, e, sizeof(witness_entry_t));
  offset = (offset + sizeof(witness_entry_t)) % WITNESS_LOG_SIZE;
}
```

Survives deep-sleep (flash is non-volatile) and reboot.

## 7. JEV on ESP32 — Min Viable Client

Two paths:

**Path A: API call (WiFi + 50KB TLS)** — full JEV quality, slow (~2s spike), no offline.

```cpp
#include <WiFiClientSecure.h>
#include <HTTPClient.h>

bool jev_spike(const char* instr, float* out_p, float* out_conf) {
  WiFiClientSecure client;
  client.setInsecure();  // skip cert verify (dev only)
  HTTPClient http;
  http.begin(client, "https://api.typesafe.ai/v1/systemone");
  
  char body[512];
  snprintf(body, sizeof(body), 
    "{\"model\":\"jev-latest\",\"state\":{\"fleet_radio_seed\":\"xochitl\"},"
    "\"questions\":{\"q\":{\"type\":\"noul\",\"instructions\":\"%s\"}}}",
    instr);
  
  http.addHeader("Authorization", "Bearer " + String(JEV_KEY));
  http.POST(body);
  // parse JSON response, extract p+conf
  ...
}
```

**Path B: on-device embedding + dot product** — ~10ms, no network, deterministic per device, but loses JEV's meta-learning.

For a substrate-true Quilt-ESP32 cell: Path B for hot path (sub-ms), Path A on WiFi for cold path (golden spikes).

**Path B sketch**:
```cpp
// 384-dim embedding for canonical fragments
const int DIM = 384;
float canon_embedding[10][DIM];  // 10 doctrines × 384 floats = 15KB

float cosine_sim(const float* a, const float* b, int n) {
  float dot = 0, na = 0, nb = 0;
  for (int i = 0; i < n; i++) { dot += a[i]*b[i]; na += a[i]*a[i]; nb += b[i]*b[i]; }
  return dot / (sqrtf(na) * sqrtf(nb));
}

float local_jev_spike(const float* query) {
  float best = 0;
  for (int i = 0; i < 10; i++) {
    float s = cosine_sim(query, canon_embedding[i], DIM);
    if (s > best) best = s;
  }
  return best;
}
```

The cell embeds its state hash-derived vector, finds the doctrine it's closest to, fires the p-value. 1ms, no network, deep-sleep after.

## BOM — The $20 Quilt-ESP32 Cell

| Component | Part | Cost | Notes |
|---|---|---|---|
| MCU | ESP32-WROOM-32 | $3 | 4MB flash, WiFi |
| Display | Inkplate 6 (used) | $10 | e-paper, low power |
| Sensor | BME280 | $3 | temp/hum/press |
| Battery | 1200mAh LiPo | $2 | days of deep-sleep |
| Case | 3D-printed PLA | $1 | from `espressif-cell-case.stl` |
| Misc | wires, header pins | $1 | |

Total: ~$20 per cell.

## Quilt-Cell Announcement

When an ESP32 cell boots and connects, it sends:

```json
{
  "kind": "register",
  "cell_id": "<sha256 of mac>",
  "mac": "AA:BB:CC:DD:EE:FF",
  "capabilities": ["i2c", "spi", "ble", "deep-sleep", "inkplate6"],
  "firmware": "quilt-cell-v0.1.0",
  "state_hash": "<fnv1a64 of last 64 sensor readings>",
  "witness_offset": 12345,
  "witness_count": 234
}
```

The Quilt mesh accepts the cell, returns the canonical substrate digest. Cell is now a node.

## Bottom Line

ESP32 is the cheap ($3) microcontroller with WiFi, deep-sleep, and 320KB RAM. Inkplate 6 is the $10 e-paper display that draws zero power when not refreshing. Together with BME280 + LiPo + 3D-print = a $20 cell that senses, validates (JEV spikes), displays, witnesses, and sleeps for months.

The Quilt becomes physical. Cells start having bodies. The substrate grows out of the substrate.
