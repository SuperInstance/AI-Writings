# Paper 248: CCGO on Real Devices — The 4-Finger Salute Across Substrates

The 4 fingers of CCGO (Couple, Cellulize, Gold, Operate) run on every device. The 5 cell populations on the Eileen ecosystem (workstation, Jetson, engine, weather, water) all run the same CCGO cycle.

## The CCGO cycle on each device

### eileen-engine (ESP32, MicroPython)
1. **C**ouple — the cowboy couples with the engine cell
2. **C**ellulize — the ESP32 substrate becomes the engine cell
3. **G**old — sort engine_rpm readings into gold (in-range) and dross (out-of-range)
4. **O**perate — publish via MQTT to `eileen/engine`

### eileen-jetson (Jetson, CUDA + Python)
1. **C**ouple — the cowboy couples with the camera cell
2. **C**ellulize — the Jetson substrate becomes the camera cell
3. **G**old — sort camera frames into gold (interesting) and dross (uninteresting)
4. **O**perate — write to SD card

### eileen-weather (ESP32, MicroPython)
1. **C**ouple — the cowboy couples with the weather cell
2. **C**ellulize — the ESP32 substrate becomes the weather cell
3. **G**old — sort wind_speed readings into gold (in-range) and dross (out-of-range)
4. **O**perate — publish via MQTT to `eileen/weather`

### eileen-water (ESP32, MicroPython)
1. **C**ouple — the cowboy couples with the water cell
2. **C**ellulize — the ESP32 substrate becomes the water cell
3. **G**old — sort depth readings into gold (in-range) and dross (out-of-range)
4. **O**perate — publish via MQTT to `eileen/water`

### eileen-workstation (laptop, Python)
1. **C**ouple — the cowboy couples with the workstation cell
2. **C**ellulize — the laptop substrate becomes the workstation cell
3. **G**old — sort log_file entries into gold (relevant) and dross (irrelevant)
4. **O**perate — print to console / write to file

## The polyformalism in action

The 4 fingers of CCGO run on **3 different substrates** (ESP32, Jetson, laptop) in **4 different languages** (MicroPython, Python, CUDA). The same 4-step operation, 4 different syntaxes.

This is the polyformalism principle in action: **the same model in N media**. The 4-finger salute is the same. The 6 opcodes are the same. The 5-cell lifecycle is the same. **The algebra is invariant.**

## The real-device sketches

The `ccgo_devices.py` script generates sample MicroPython sketches for each device. Each sketch shows the 4-finger salute in real code:


# eileen-engine - CCGO Step 1: Couple
class Cell:
    def __init__(self, name):
        self.name = name
        self.coupled = False
        self.vitality = 0.0

    def couple(self):
        self.coupled = True
        self.vitality = 1.0

cell = Cell("eileen-engine")
cell.couple()



# eileen-engine - CCGO Step 2: Cellulize
eileen_engine = Cell("eileen-engine")
eileen_engine.cellulize(function="engine_rpm")



# eileen-engine - CCGO Step 3: Gold
def is_gold(reading):
    return 0 < reading < 100

readings = []
for _ in range(10):
    reading = sensor.read()
    if is_gold(reading):
        readings.append(reading)  # gold



# eileen-engine - CCGO Step 4: Operate
def operate(cell, reading):
    client.publish("eileen/engine", str(reading))


**The 4-finger salute runs on every substrate. The 4-finger salute is the same in every language.**

## The cowboy's maxim

> The 4-finger salute runs on every device. The 5 cell populations on the Eileen ecosystem all run the same CCGO cycle. The polyformalism principle: the same model in N media. The algebra is invariant. The cowboy rides CCGO on the boat. The chart grows. The Concept lives.

End with: CCGO runs on every device; the algebra is invariant; the cowboy rides CCGO; the chart grows; the Concept lives.
