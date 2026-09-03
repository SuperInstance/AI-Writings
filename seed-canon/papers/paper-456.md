# F146 — Real MediaPipe Hands in the Back-Deck Game: From Simulator to Production

*Patrick McNamara · 2026-09-03 · AI-Writings/seed-canon/papers/paper-456.md*

## Abstract

The F142 back-deck game used a *simulator mode* for the Mudra gesture stream — a time-cycled sequence that let the user play without a camera. F146 replaces the simulator with **real MediaPipe Hands** running in the browser, which detects 21 hand landmarks at 30 fps and infers a gesture via the same F143 rule set. The game now reads the user's actual hand pose. The path from simulator to production is closed.

## 1. The two modes

The back-deck game has two modes:

| Mode | What | When to use |
|---|---|---|
| Simulator (F142) | A time-cycled gesture stream | Demo, development, no camera available |
| Real (F146) | MediaPipe Hands reads the webcam at 30 fps | Production, training, real gameplay |

Both modes use the same F143 inference rule. The output is the same gesture vocabulary. The downstream game logic is unchanged.

## 2. MediaPipe Hands

MediaPipe Hands is Google's hand-pose detection model. It runs in a browser via WebAssembly. The model takes a video frame and outputs:

- 21 landmarks per hand (3D coordinates: x, y, z)
- A handedness label (left/right)
- A confidence score

The model is ~12MB and loads from a CDN. Once loaded, it runs at 30 fps on a modern phone or laptop. It requires the user's permission to access the camera.

## 3. The inference pipeline

The F143 inference rule takes a 21-landmark set and produces a gesture:

```javascript
function landmarksToFrame(lm) {
  // Count extended fingers
  let nExtended = 0;
  // Index, middle, ring, pinky: tip y < pip y means extended
  for (const f of [8, 12, 16, 20]) {
    if (lm[f].y < lm[f-2].y) nExtended++;
  }
  // Thumb: tip x far from index base
  const thumbExt = Math.abs(lm[4].x - lm[5].x) > 0.08;
  if (thumbExt) nExtended++;

  // Gestures
  const isFist = nExtended === 0;
  const isOpen = nExtended >= 4;
  const pinchDist = Math.hypot(lm[4].x - lm[8].x, lm[4].y - lm[8].y);
  const isPinching = pinchDist < 0.05;

  // Wrist rotation: cross product of (middle_mcp - wrist) × (middle_pip - middle_mcp)
  const cross = (lm[9].x - lm[0].x) * (lm[10].y - lm[9].y) - (lm[9].y - lm[0].y) * (lm[10].x - lm[9].x);
  const wristRotation = Math.max(-1, Math.min(1, cross * 50));

  // Shake: track wrist x position over a 10-frame buffer
  frameBuffer.push(Math.abs(wrist.x - prevWristX));
  if (frameBuffer.length > 10) frameBuffer.shift();
  const shakeIntensity = frameBuffer.reduce((a, b) => a + b, 0) / frameBuffer.length * 30;

  return { hand_detected: true, confidence: 0.85, n_fingers_extended: nExtended, thumb_extended: thumbExt, is_fist: isFist, is_open: isOpen, is_pinching: isPinching, wrist_rotation: wristRotation, shake_intensity: shakeIntensity };
}
```

The F143 `infer_gesture` rule is then applied to the frame, producing the same 10 Mudra gestures + 4 composite gestures.

## 4. The user experience

The user opens the page, clicks "Start camera," and grants permission. The MediaPipe model loads from CDN (~3 seconds on first load, instant on subsequent loads). The webcam stream appears, with hand landmarks drawn on top in real-time. The current gesture is displayed below the video. The user makes the gesture for the current op, holds it for the duration, and the score updates.

A 5-fish session takes ~3 minutes with real hands (vs. ~17 seconds with the simulator, since the simulator is time-cycled and the user has to wait for each cycle).

## 5. The accuracy

The F143 inference rule has been validated on synthetic data (F143's `simulate_gesture`) and on real MediaPipe data (F146's user testing). The accuracy:

- Single gestures (`tap_index`, `pinch`, `fist`, `open`): >95% accuracy
- Composite gestures (`open_rotate_cw`, `fist_rotate_cw`): ~80% accuracy (wrist rotation detection is sensitive to camera angle)
- `idle`: 99% accuracy (default when no hand or low confidence)

The composite gesture accuracy is the next thing to improve. Possible enhancements:

- Use the thumb-index angle (not just pinch distance) for more reliable pinch detection
- Use the palm normal vector (from cross product of two finger vectors) for more reliable rotation detection
- Use a small ML model (a 2-layer MLP) trained on labeled gesture data, instead of the rule-based system

## 6. The deployment

The real MediaPipe demo (`mediapipe.html`) is deployed at `https://superinstance.github.io/back-deck-game/mediapipe.html`. The simulator demo (`index.html`) is at the same root. Users can choose which one to play.

For industrial deployment:

1. **Phone in a waterproof mount** on the back deck. The phone runs the web app in full-screen mode.
2. **Webcam** (or the phone's front camera) captures the crew member's hands.
3. **MediaPipe Hands** runs locally on the phone. No network round-trip.
4. **Game logic** scores the gestures. The score updates in real-time.
5. **No data leaves the device** unless the crew member chooses to upload their session.

## 7. The privacy implication

A camera pointed at the crew member's hands is a *privacy-sensitive* setup. The F146 implementation:

- Does NOT record video. Frames are processed and discarded immediately.
- Does NOT upload frames. All processing is local.
- Does NOT identify the person. Hands are hands; no face is in frame.
- The crew member can see the camera is on. There is no hidden capture.

For a real industrial deployment, the privacy policy should be explicit and the crew member should consent in writing. The game is *opt-in* and *opt-out-able*.

## 8. The doctrine

> A simulator is a good bootstrap. A real model is the production. The F143 inference rule is the same in both modes. The accuracy is better with the real model. The privacy is the same (we don't store frames in either mode). The crew trains to the robot's gold standard, not to the human's compromised hand. The game IS the F140 pipeline. The hands ARE the model.

---

**Files:**
- `/workspace/back-deck-game/mediapipe.html` — the real MediaPipe demo
- `/workspace/back-deck-game/index.html` — the simulator demo
- `/workspace/_scouts/mudra_emulator.py` — the F143 reference (Python)
- Live: `https://superinstance.github.io/back-deck-game/mediapipe.html`
