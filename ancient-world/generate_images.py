#!/usr/bin/env python3
"""Generate ancient world visuals using Cloudflare Workers AI (FLUX-1-schnell)."""

import requests
import base64
import time
import os
import sys

ACCOUNT_ID = "049ff5e84ecf636b53b162cbb580aae6"
TOKEN = "cfoat_pKyCXaoUKaNvQJRJjWM_QKKOHdEpi0E9J2irJLn0TME.nOde7H8RvmiqNdzeJl6VJfJ2cixr6O6vewQXkZY_cqw"
OUTPUT_DIR = "/home/eileen/projects/ai-writings/ancient-world/images"
MODEL = "@cf/black-forest-labs/flux-1-schnell"

IMAGES = [
    ("01_wayfinder", "A Polynesian wayfinder at night on a double-hulled canoe. Star compass. Hands feeling the water. Ancient, precise, sacred. No text."),
    ("02_nilometer_scribe", "Ancient Egyptian scribe at the Nilometer. Papyrus. Flood marks on the stone. Lamplight. The moment of recording. No text."),
    ("03_greek_symposium", "Ancient Greek symposium at night. Wine cups. Torchlight. One young person about to say something. The moment before. No text."),
    ("04_mongol_rider", "Mongol relay rider at a yurt station. Horse steaming in cold air. Leather passport tablet. Dawn on the steppe. No text."),
    ("05_viking_longhouse", "Viking longhouse at night. Fire. Skald with a harp. Listeners in furs. Snow outside. Saga-telling. No text."),
    ("06_himalayan_yogi", "Indian yogi in a Himalayan cave. Cross-legged. Eyes half-closed. A small flame — an ember — glowing before them. Minimal, sacred, still. No text."),
    ("07_west_african_griot", "West African griot playing a kora under a baobab tree at sunset. Golden light. Children listening. The tradition continuing. No text."),
    ("08_chinese_calligrapher", "Chinese calligrapher's brush on rice paper. A single stroke. Ink flowing like water. The moment of wuwei. Close-up. Painterly. No text."),
    ("09_andean_quipu", "Andean quipucamayoc holding a knotted string quipu. Colorful cords. Mountain backdrop. Sunset. Reading the knots. No text."),
    ("10_heian_courtier", "Heian Japanese courtier writing a waka poem by candlelight. Folding screen. Seasonal flower. Delicate, precise, intimate. No text."),
    ("11_lascaux_painter", "Lascaux cave painter by torchlight. Hand on the wall. Bison emerging from pigment. Primal, sacred, 17,000 years ago. No text."),
    ("12_sumerian_scribe", "Sumerian scribe pressing a reed into wet clay. The first cuneiform mark. Ziggurat in the background. The birth of recording. No text."),
    ("13_aztec_daykeeper", "Aztec daykeeper with a painted codex. Obsidian mirror. The tonalpohualli calendar. Feathers and jade. No text."),
    ("14_celtic_druid", "Celtic druid in a moonlit oak grove. Mistletoe. Stone circle. Fog. The moment of connection between earth and sky. No text."),
    ("15_aboriginal_songline", "Aboriginal elder walking a songline through red desert. Ancient footprints in the sand. The land singing. Sunset. Vast, sacred. No text."),
]

def generate_one(name, prompt, retries=3):
    outpath = os.path.join(OUTPUT_DIR, f"{name}.png")
    if os.path.exists(outpath) and os.path.getsize(outpath) > 10000:
        print(f"  ✓ {name}.png already exists, skipping")
        return True

    for attempt in range(retries):
        try:
            print(f"  → Generating {name}.png (attempt {attempt+1})...")
            r = requests.post(
                f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}",
                headers={"Authorization": f"Bearer {TOKEN}"},
                json={"prompt": prompt},
                timeout=90,
            )
            if r.status_code != 200:
                print(f"    HTTP {r.status_code}: {r.text[:200]}")
                time.sleep(3)
                continue

            d = r.json()
            if not d.get("success") or "result" not in d or "image" not in d.get("result", {}):
                print(f"    API error: {str(d)[:200]}")
                time.sleep(3)
                continue

            img = base64.b64decode(d["result"]["image"])
            with open(outpath, "wb") as f:
                f.write(img)
            print(f"    ✓ Saved {name}.png ({len(img)} bytes)")
            return True

        except Exception as e:
            print(f"    Error: {e}")
            time.sleep(3)

    print(f"    ✗ FAILED after {retries} attempts: {name}")
    return False

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    success = 0
    failed = []

    for name, prompt in IMAGES:
        if generate_one(name, prompt):
            success += 1
        else:
            failed.append(name)
        time.sleep(1)  # rate limit courtesy

    print(f"\n{'='*50}")
    print(f"Done: {success}/{len(IMAGES)} succeeded")
    if failed:
        print(f"Failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("All images generated successfully!")

if __name__ == "__main__":
    main()
