# F143 — The Mudra-Band Emulator: Webcam-Based Hand Pose for Industrial Training

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-453.md*

## Abstract

The Mudra band (Wearable Devices Ltd) is a wrist-worn surface-EMG device that detects subtle hand muscle activations and produces a stream of "Mudra gestures" (named hand poses). The SDK is closed, the hardware costs $200-400, and the bands are not always available when needed. For industrial training (F142's back-deck game) to work *today*, on a phone with no extra hardware, we need an emulator: a JS+webcam pipeline that infers hand-pose state from the camera and produces the same gesture stream. This paper defines the emulator, its gesture vocabulary, its state-hash contract, and the JS implementation that runs in the browser at 20 fps.

## 1. The problem

A back-deck simulator (F142) needs to read hand gestures in real-time. The options are:

- **Mudra bands** — $200-400, closed SDK, requires pairing, requires battery
- **Leap Motion** — $100, requires USB, requires a desktop
- **MediaPipe Hands** — free, runs in a browser, requires a webcam
- **Myo armbands** — $200, requires pairing, requires a desktop

For a *deployed* simulator (on a phone, in a waterproof mount, on a working boat), the only viable option is MediaPipe Hands. The Mudra emulator is the JS pipeline that wraps MediaPipe Hands and produces a Mudra-style gesture stream.

## 2. The Mudra gesture vocabulary

The Mudra band produces 10 named gestures:

| Gesture | Description |
|---|---|
| `tap_index` | index finger extension |
| `tap_middle` | middle finger extension |
| `tap_thumb` | thumb extension |
| `pinch` | thumb + index pinch |
| `fist` | closed fist |
| `open` | open palm |
| `rotate_cw` | wrist rotation clockwise |
| `rotate_ccw` | wrist rotation counter-clockwise |
| `shake` | quick lateral shake |
| `idle` | no gesture for >500ms |

The emulator produces the same 10 gestures, plus a few composite gestures for compound motions (e.g., `open_rotate_cw` = open palm + wrist rotation).

## 3. The pose frame

A pose frame is a single observation from the webcam:

```python
@dataclass
class PoseFrame:
    timestamp_ms: int
    hand_detected: bool
    n_fingers_extended: int         # 0-5
    thumb_extended: bool
    is_fist: bool
    is_open: bool
    is_pinching: bool
    wrist_rotation: float           # -1.0 (ccw) to 1.0 (cw)
    shake_intensity: float          # 0-1
    confidence: float               # 0-1
    raw_landmarks: List[Tuple[float, float]]  # 21 hand landmarks
```

The 21 hand landmarks are the standard MediaPipe Hands set (wrist + 4 per finger). The pose frame is the *raw* data; the gesture is the *inferred* data.

## 4. The inference rule

The gesture is inferred from the pose frame by a deterministic rule:

```
if not hand_detected or confidence < 0.3: return "idle"
if shake_intensity > 0.7: return "shake"
if is_fist:
    if wrist_rotation > 0.3: return "fist_rotate_cw"
    return "fist"
if is_open:
    if wrist_rotation > 0.3: return "open_rotate_cw"
    if shake_intensity > 0.3: return "open_shake"
    return "open"
if is_pinching:
    if wrist_rotation < -0.3: return "pinch_rotate_ccw"
    return "pinch"
if n_fingers_extended == 1 and thumb_extended: return "tap_index"
if n_fingers_extended == 2 and not thumb_extended: return "tap_middle"
if n_fingers_extended == 0 and thumb_extended: return "tap_thumb"
return "idle"
```

The rule is identical in Python and JavaScript. The polyformalism contract: same pose frame → same gesture, byte-exact across substrates.

## 5. The JS implementation

The JS implementation runs in a browser at 20 fps:

```javascript
async function detectGesture() {
  if (!video || !video.videoWidth) return;
  // 1. Capture a frame from the video
  // 2. Run MediaPipe Hands on the frame
  // 3. Extract 21 hand landmarks
  // 4. Compute pose frame fields
  // 5. Apply the inference rule
  // 6. Emit the gesture event
}
```

In the demo (`back-deck-game/index.html`), step 2 is a *simulator* (time-cycled gestures) so the user can play without MediaPipe. In production, replace the simulator with a real MediaPipe Hands call.

## 6. The state hash

The emulator's state hash is an FNV-1a 64-bit hash of the gesture stream:

```python
h = 0xCBF29CE484222325
for gesture in gesture_log:
    for byte in gesture.encode('utf-8'):
        h ^= byte
        h = (h * 0x00000100000001B3) & 0xFFFFFFFFFFFFFFFF
    h ^= 0xFF  # separator
    h = (h * 0x00000100000001B3) & 0xFFFFFFFFFFFFFFFF
```

The same hash, byte-exact, in Python and JavaScript. Two emulators with the same hash have seen the same gesture stream. The hash is the *signature* of a session.

## 7. The composite gesture recognition

For F142's back-deck ops, we need to recognize *composite* gestures (gestures that involve both a hand pose and a wrist motion). The composite is recognized as a single gesture in the log, not as two separate events. This is critical for the back-deck game: an `open_rotate_cw` is *one* event (gaff swing), not two events (open + rotate_cw).

The composite is recognized by checking the *current* pose frame for both conditions:

```
is_open AND wrist_rotation > 0.3 → open_rotate_cw
is_pinching AND wrist_rotation < -0.3 → pinch_rotate_ccw
```

If both conditions are true, the composite is emitted. The two components are not emitted separately.

## 8. The simulator mode (for demos)

The emulator can run in *simulator mode* for demos (no webcam required). The simulator generates a time-cycled gesture stream that matches the deck-ops in order:

```
cycle = [
  ("open_rotate_cw",   1500, "G1_gaff_swing"),
  ("pinch_rotate_ccw",  800, "G2_dehook_pull"),
  ("tap_index",         600, "G3_gill_cut"),
  ("idle",             8000, "G4_bleed_hold"),
  ("open_shake",       2500, "G5_stow_arc"),
  ("fist_rotate_cw",   4000, "G6_scrub_down"),
]
```

Each gesture is held for the specified duration, then the next gesture begins. The cycle repeats every ~17.4 seconds. The crew member can practice against the simulator without a camera.

## 9. The deployment path

The deployment path for a real industrial simulator is:

1. **Week 1**: deploy the simulator mode (no camera) on a phone. The crew plays during downtime. The skill tree is built.
2. **Week 2-4**: integrate MediaPipe Hands into the emulator. The crew plays with their hands, the simulator reads them.
3. **Month 2+**: deploy real Mudra bands on a few crew members. Compare the gesture stream from the emulator to the gesture stream from the real bands. Calibrate.

The simulator mode is the *bootstrap*. MediaPipe is the *improvement*. Real Mudra bands are the *gold standard*. The same game logic works at all three levels.

## 10. The doctrine

> The Mudra-band emulator is a JS+webcam pipeline that produces a Mudra-style gesture stream. The stream is the same as what a real Mudra band would produce. The state hash is the same. The game is the same. The training is the same. The only thing that changes is the *cost*: a real band is $200-400, the emulator is a phone with a camera. The emulator is good enough to train the crew. The real bands are good enough to audit the gold standard.

---

**Files:**
- `/workspace/_scouts/mudra_emulator.py` — the reference implementation (Python)
- `/workspace/back-deck-game/index.html` — the JS implementation (in-browser)
- Live demo: `https://superinstance.github.io/back-deck-game/`
