#!/usr/bin/env python3
"""Local image renderer — SDXL-turbo on the RTX 4050. Usage: local_render.py <prompt> <out.png> [seed]"""
import sys, torch
from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
).to("cuda")

prompt = sys.argv[1]
out = sys.argv[2]
seed = int(sys.argv[3]) if len(sys.argv) > 3 else 42
g = torch.Generator(device="cuda").manual_seed(seed)

img = pipe(
    prompt=prompt,
    num_inference_steps=4,
    guidance_scale=0.0,
    generator=g,
    width=832,
    height=832,
).images[0]
img.save(out)
print(f"OK {out} seed={seed}")
