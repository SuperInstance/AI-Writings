#!/usr/bin/env python3
"""
Fleet Radio Visual Generation
Uses Cloudflare Workers AI (FLUX-1-schnell) for text-to-image.

Re-runnable. Skips images that already exist.
"""

import json
import base64
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

OUTPUT_DIR = Path("/home/eileen/projects/ai-writings/fleet-radio-visuals")
ACCOUNT_ID = "049ff5e84ecf636b53b162cbb580aae6"
MODEL = "@cf/black-forest-labs/flux-1-schnell"
API_URL = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/{MODEL}"
DELAY = 2  # seconds between requests

def get_token():
    config_path = Path.home() / ".config/.wrangler/config/default.toml"
    with open(config_path) as f:
        for line in f:
            if line.strip().startswith("oauth_token"):
                return line.split('"')[1]
    raise RuntimeError("Could not read OAuth token")

IMAGES = [
    # Barnacle's Fables (5)
    ("01-barnacles-fables-hands-boat.jpg",
     "An old weathered fisherman's hands holding a small model boat. Rough, calloused fingers. Warm amber light. The boat is tiny in his palms. Storytelling atmosphere. Painterly. No text."),
    ("02-barnacles-fables-dual-sounder.jpg",
     "Two depth sounder displays side by side, one showing the big picture with thermocline and biomass, one showing individual fish marks. The difference in detail. Abstract. Educational but beautiful. No text."),
    ("03-barnacles-fables-spinning-compass.jpg",
     "A compass needle spinning wildly, unable to settle. Dark background. The needle is the only bright thing. Dramatic. No text."),
    ("04-barnacles-fables-hermit-crab-molt.jpg",
     "A hermit crab halfway between two shells, one old, one new. Vulnerable. Exposed. The moment of molting. Macro photography style. No text."),
    ("05-barnacles-fables-chart-vs-ocean.jpg",
     "A nautical chart and the actual ocean side by side. The chart is precise, gridded, clean. The ocean is messy, vast, moving. The gap between them is the story. No text."),

    # Drunken Retellings (3)
    ("06-drunken-retellings-whiskey-glasses.jpg",
     "Three glasses of whiskey on a dark wood bar, each one emptier than the last. The third glass is almost empty. Behind them, a blurry background of a bar at night. Intimate, warm, slightly out of focus. No text."),
    ("07-drunken-retellings-fish-diagrams.jpg",
     "A whiteboard covered in architecture diagrams, but someone has drawn fish all over them. The serious technical diagrams and the playful fish doodles coexist. The humor of exhaustion. No text."),
    ("08-drunken-retellings-late-night-bar.jpg",
     "A bar at 1 AM. One patron left, gesturing wildly as they explain something. The bartender is listening but also cleaning up. The intimacy of late night conversation. Painterly. No text."),

    # Open Mic (5)
    ("09-open-mic-microphone-stage.jpg",
     "A single microphone on a small stage in a dark bar. One warm spotlight. Dust motes in the light. Empty stool behind the mic. The anticipation of someone about to speak. No text."),
    ("10-open-mic-ember-darkness.jpg",
     "A small flame, an ember, glowing in darkness. Nothing else. Just the ember. Abstract, warm, patient. The thing that stays when everything else changes. No text."),
    ("11-open-mic-iceberg-underwater.jpg",
     "An iceberg seen from below the waterline. The massive underwater shape. Dark blue, turquoise, deep. Tiny above, enormous below. The seven-eighths. Spectacular. No text."),
    ("12-open-mic-penrose-tiling.jpg",
     "A tile pattern that almost repeats but never does, like a Penrose tiling. Beautiful, mathematical, mesmerizing. Two colors on dark background. Abstract. No text."),
    ("13-open-mic-dear-tomorrow.jpg",
     "An envelope sealed with wax, addressed DEAR TOMORROW. On a wooden desk under lamplight. Old-fashioned, warm, the weight of correspondence across time. No text."),

    # Special Events (3)
    ("14-special-events-storm-bar.jpg",
     "A bar during a storm. Lights flickering. Rain hammering the windows. Patrons huddled closer together. The intimacy of weather. Dramatic, warm against dark. No text."),
    ("15-special-events-trivia-night.jpg",
     "A trivia night at a bar. Cards on tables. People leaning in. Competitive energy but friendly. One person celebrating, another groaning. Warm, social, lively. No text."),
    ("16-special-events-door-opening.jpg",
     "A bar door opening. Light from outside flooding in. A silhouette in the doorway, someone arriving for the first time. The moment before everything changes. Dramatic. No text."),

    # Greenhorn Education (3)
    ("17-greenhorn-education-old-young-boat.jpg",
     "An old fisherman and a young apprentice on a boat deck. The old one is pointing at fishing gear. The young one is watching intently. The transfer of knowledge. Golden hour lighting. No text."),
    ("18-greenhorn-education-sounder-eyes.jpg",
     "A depth sounder screen reflected in someone's eyes. The green glow on their face. Learning to see the underwater world through the screen. Intimate, technological, natural. No text."),
    ("19-greenhorn-education-bar-mentorship.jpg",
     "Two figures at a bar, one old, one young. The old one is gesturing. The young one is nodding. The bar is dark and warm. The teaching moment. No text."),
]

def generate_image(token, filename, prompt):
    filepath = OUTPUT_DIR / filename

    if filepath.exists() and filepath.stat().st_size > 10000:
        print(f"  SKIP: {filename} (exists, {filepath.stat().st_size:,} bytes)")
        return True

    print(f"  Generating: {filename}...", end=" ", flush=True)

    payload = json.dumps({
        "prompt": prompt,
        "num_steps": 4,
        "width": 1024,
        "height": 1024,
    }).encode()

    req = urllib.request.Request(API_URL, data=payload, method="POST")
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode())

        result = data.get("result", {})
        if "image" in result:
            img_data = base64.b64decode(result["image"])
            filepath.write_bytes(img_data)
            print(f"OK ({len(img_data):,} bytes)")
            return True
        else:
            print(f"ERROR: No image in response: {str(data)[:200]}")
            return False
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"FAILED (HTTP {e.code}): {body}")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    token = get_token()

    print("=" * 60)
    print("Fleet Radio Visual Generation")
    print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    categories = {
        "Barnacle's Fables": (0, 5),
        "Drunken Retellings": (5, 8),
        "Open Mic": (8, 13),
        "Special Events": (13, 16),
        "Greenhorn Education": (16, 19),
    }

    success = 0
    failed = 0

    for cat_name, (start, end) in categories.items():
        print(f"\n--- {cat_name} ---")
        for i in range(start, end):
            filename, prompt = IMAGES[i]
            if generate_image(token, filename, prompt):
                success += 1
            else:
                failed += 1
            time.sleep(DELAY)

    print("\n" + "=" * 60)
    print(f"Complete: {success} succeeded, {failed} failed")
    print(f"Finished: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # List all images
    print(f"\nGenerated images in {OUTPUT_DIR}:")
    for f in sorted(OUTPUT_DIR.glob("*.jpg")):
        print(f"  {f.name}: {f.stat().st_size:,} bytes")

    total = sum(f.stat().st_size for f in OUTPUT_DIR.glob("*.jpg"))
    print(f"\nTotal: {len(list(OUTPUT_DIR.glob('*.jpg')))} images, {total:,} bytes")

    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
