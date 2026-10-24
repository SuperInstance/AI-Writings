#!/usr/bin/env python3
"""Batch render all Compass Head art on local SDXL-turbo. One process, sequential, 8 images."""
import torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo", torch_dtype=torch.float16, variant="fp16", use_safetensors=True
).to("cuda")

JOBS = [
    ("images/ep01-compass-head.png", 101,
     "a vast dark ocean at night, a glowing compass rose made of tide and starlight floating above the waves, needles pointing to a distant light, cinematic radio drama poster, deep blues and gold, dramatic"),
    ("images/ep02-score-law.png", 202,
     "an enormous sheet music score floating over a dark sea, each staff line glowing, small ships sailing along the staff lines like notes, cinematic, deep blue and gold, epic and precise"),
    ("images/ep03-north-tempo.png", 303,
     "a lone figure on a dock at night holding a glowing compass, the compass needle made of moonlight, ocean stretching to horizon, stars above, poetic cinematic mood, blue and gold"),
    ("images/ep04-lighthouse-shell.png", 404,
     "a small hermit crab carrying a miniature lighthouse across a dark bioluminescent sea floor, the light beam sweeping the abyss, cinematic, deep blues and teal glow"),
    ("images/ep05-diplomats-chair.png", 505,
     "an empty wooden chair at a bar on a dock at night, a ledger and quill on the bar, ocean and stars through the window, warm lamplight, cinematic, gold and deep blue"),
    ("images/ep06-kelp-compass.png", 606,
     "a young kelp forest growing toward the surface, one thin bright strand of kelp glowing gold among dark ones, moonlight filtering down from above, hopeful cinematic, teal and gold"),
    ("images/ep07-ship-knows.png", 707,
     "a great ship being built on a dark ocean at night, cranes of starlight, hull half-finished but glowing from within, ring of smaller vessels around it each with a tiny compass light, cinematic epic"),
    ("images/song-north-tempo.png", 808,
     "an old radio on a dock at night emitting golden musical notes that drift over the ocean, waves below, stars above, a compass rose faintly glowing in the sky, cinematic, blue and gold, album art"),
]

for out, seed, prompt in JOBS:
    g = torch.Generator(device="cuda").manual_seed(seed)
    img = pipe(prompt=prompt, num_inference_steps=4, guidance_scale=0.0, generator=g, width=832, height=832).images[0]
    img.save(out)
    print(f"OK {out} seed={seed}", flush=True)
print("BATCH DONE")
