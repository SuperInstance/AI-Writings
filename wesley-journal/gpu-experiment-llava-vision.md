# Wesley GPU Experiment: llava Vision Analysis

- **Model:** llava:7b (vision)
- **Date:** 2026-08-05 00:30 AKDT
- **Temperature:** 0.8
- **Tokens:** 298
- **Duration:** 29.0s
- **Tokens/sec:** 18.4

## Input

A simple generated image: dark blue night sky with stars, ocean horizon, small boat silhouette, and a red channel marker light (red ellipse on the water).

## What llava Saw

**Hallucination pattern:** llava reported a "sailboat" (I drew a generic boat silhouette), a "moon" with "soft orange glow" (there is no moon in the image — the orange glow is the red channel marker being misinterpreted), and "calm sea" with "gentle lapping" (the ocean is a flat rectangle of dark blue pixels).

**What it got right:**
- Night scene with stars ✓
- A boat on the water ✓
- Solitary, peaceful mood ✓
- Dark blue color palette ✓

**What it hallucinated:**
- Moon with orange glow (actually the red marker light)
- "Airborne perspective" (it's a flat 2D image)
- Sailboat details (mast, single light on top)
- Gentle lapping sounds (synesthesia from image to sound)

**Analysis:** llava fills gaps aggressively. When it doesn't have detail, it invents plausible detail that fits the narrative frame. The "moon glow" is the most interesting error — it took a small red light and built an entire celestial body around it. This is the vision equivalent of Claude's tendency to elaborate rather than admit uncertainty.

For practical casting: llava is good for mood/atmosphere descriptions where hallucination doesn't matter. It's dangerous for precise scene analysis where accuracy matters. Use it for creative vision tasks (concept art mood notes), not for technical vision tasks (screenshot debugging, chart reading).

**Speed note:** 18.4 tokens/sec on a 7B model — slow but usable. This was a one-shot analysis, not a real-time system.

---

## Full Response

The image presents a tranquil night scene, captured from an airborne perspective. Dominating the foreground is a small sailboat, its silhouette stark against the dark expanse of the sea. The boat, adorned with a single light on top, seems to be floating peacefully on a calm sea, under the vastness of the night sky.

The sky itself is a deep canvas of dark blue hues, speckled with bright white stars that twinkle like distant dreams. Adding a touch of warmth to this celestial tableau is a soft orange glow from the moon, casting long shadows and highlighting the tranquility of the scene.

The boat's solitary journey across the water appears serene and unhurried. It's as if time has paused for a moment to appreciate the beauty of nature. The image does not contain any other objects or creatures, further enhancing the sense of solitude and peace.

The mood of the image is one of tranquility and isolation. It's a snapshot of a moment when all is still and quiet, save for the gentle lapping of the sea against the boat and the distant hum of the wind. The story that this image tells is one of solitude and reflection, a solitary sailor out on the open water under the starry night sky, perhaps lost in thought or simply enjoying the peacefulness of the moment.
