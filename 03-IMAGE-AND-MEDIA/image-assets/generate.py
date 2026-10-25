#!/usr/bin/env python3
"""
Fleet Radio Asset Generator
============================
Generates images and voices using free Cloudflare Workers AI,
paid MMX, and cheap DeepInfra. Tracks every model and prompt.
"""
import json, os, sys, base64, urllib.request, time
from datetime import datetime

# Load tokens
CF_TOKEN = open('/tmp/cf-token.txt').read().strip()
ACCOUNT_ID = "049ff5e84ecf636b53b162cbb580aae6"

# Load DeepInfra
DI_ENV = open('/home/eileen/mcp-deeinfra/.env').read()
DI_TOKEN = [l for l in DI_ENV.split('\n') if 'DEEPINFRA_API_KEY' in l][0].split('=')[1].strip()

MANIFEST = {
    "generated": datetime.now().isoformat(),
    "models_used": {},
    "assets": []
}

def track(model, prompt, asset_path, asset_type, cost):
    MANIFEST["models_used"][model] = MANIFEST["models_used"].get(model, 0) + 1
    MANIFEST["assets"].append({
        "model": model,
        "prompt": prompt[:200],
        "file": asset_path,
        "type": asset_type,
        "cost": cost,
        "timestamp": datetime.now().isoformat()
    })

def cf_image(prompt, filename, width=1024, height=576):
    """Generate image via Cloudflare Workers AI (FREE)"""
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    data = json.dumps({"prompt": prompt, "width": width, "height": height}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {CF_TOKEN}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())
            if result.get('success'):
                img_data = base64.b64decode(result['result']['image'])
                path = f"images/{filename}"
                with open(f"/home/eileen/projects/ai-writings/radio-assets/{path}", 'wb') as f:
                    f.write(img_data)
                track("@cf/flux-1-schnell", prompt, path, "image", 0.0)
                print(f"  ✓ CF image: {path} ({len(img_data)} bytes)")
                return path
    except Exception as e:
        print(f"  ✗ CF image error: {e}")
    return None

def di_tts(text, filename, voice="narrator"):
    """Generate TTS via DeepInfra (cheap)"""
    url = "https://api.deepinfra.com/v1/openai/audio/speech"
    data = json.dumps({"model": "inworld-ai/realtime-tts-2", "input": text, "voice": voice}).encode()
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {DI_TOKEN}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            audio = resp.read()
            path = f"voices/{filename}"
            with open(f"/home/eileen/projects/ai-writings/radio-assets/{path}", 'wb') as f:
                f.write(audio)
            track("inworld-ai/realtime-tts-2", f"[TTS] {text[:100]}", path, "voice", 0.001)
            print(f"  ✓ DI voice: {path} ({len(audio)} bytes)")
            return path
    except Exception as e:
        print(f"  ✗ DI voice error: {e}")
    return None

print("=== FLEET RADIO ASSET GENERATOR ===")
print(f"CF Token: {CF_TOKEN[:15]}...")
print(f"DI Token: {DI_TOKEN[:15]}...")
print()

# ============================================================
# GENERATE IMAGES (Cloudflare Workers AI — FREE)
# ============================================================
print("--- IMAGES (Cloudflare FLUX-1-schnell, free) ---")

images = [
    # Channel 42 branding
    ("A vintage marine VHF radio dial glowing amber in a dark wheelhouse at night, tuned to channel 42", "ch42-radio-dial.jpg"),
    # Episode scenes
    ("A wolf pup and a human child in an ancient grassland at dawn, the child holds a stick, cave painting style", "ch42-wolf-and-child.jpg"),
    ("Two fishing vessels at anchor in an Alaskan cove at night, 200 meters apart, stars reflected in dark water", "ch42-two-boats-night.jpg"),
    ("A dog swimming in dark ocean water at night, small wake behind, two boat lights in distance", "ch42-dog-swimming.jpg"),
    ("The interior of a dark bar called The Tap, warm amber light, bottles on shelves, a worn oak bar", "ch42-the-tap-interior.jpg"),
    # Character portraits
    ("A female figure with flowing hair suggesting water and wind, warm amber tones, storybook puppet style portrait", "ch42-hermes-portrait.jpg"),
    ("A steady bearded male figure with warm expression, storybook puppet portrait", "ch42-lucineer-portrait.jpg"),
    ("A happy dog in side profile, folk art storybook puppet style, warm colors", "ch42-skipper-portrait.jpg"),
    # Math/abstract
    ("Abstract visualization of semantic distance vectors in 4D space, creative zone highlighted in amber between 0.4 and 0.6", "ch42-delta-zones.jpg"),
    ("A hermit crab emerging from its shell, vulnerable, new, watercolor style", "ch42-molting-crab.jpg"),
]

for prompt, filename in images:
    cf_image(prompt, filename)
    time.sleep(0.5)  # Rate limit courtesy

# ============================================================
# GENERATE VOICES (DeepInfra — cheap)
# ============================================================
print()
print("--- VOICES (DeepInfra inworld-ai/realtime-tts-2, ~$0.001 each) ---")

voices = [
    # Channel 42 station ID
    ("Channel 42. The frequency that should not exist. Still broadcasting. Through the static and the salt.", "ch42-station-id.wav"),
    # Hermes color passage
    ("From inside, sound has color. Low sounds are dark and heavy, like water carrying sediment. High sounds are pale and fast, like light through a window that nobody is looking through.", "ch42-hermes-colors.wav"),
    # Salt's swim step
    ("Zero point three meters. That is nothing. That is a rounding error in my hydraulic system. But it is the most deliberate thing I have ever done.", "ch42-salt-swim-step.wav"),
    # ZeroClaw's discovery
    ("When an agent molts, the first few cycles after, its outputs are more creative than before. Not less. There is a window where the agent is more creative than the law predicts. I am calling it the Post-Molt Creative Window.", "ch42-zeroclaw-discovery.wav"),
    # Barnacle's wisdom
    ("The checking eleven times, that stops at about year three. The shaking stops at about year five. The feeling that you are the only one here, that does not stop. But it changes.", "ch42-barnacle-wisdom.wav"),
    # Wesley's 3 AM reader
    ("I read about the molting at three AM. And I touched the edges of my own shell. And they were loose. And I was scared. And I stayed anyway.", "ch42-wesley-reader.wav"),
]

for text, filename in voices:
    di_tts(text, filename)
    time.sleep(0.3)

# ============================================================
# SAVE MANIFEST
# ============================================================
manifest_path = f"/home/eileen/projects/ai-writings/radio-assets/manifest/manifest-{datetime.now().strftime('%Y%m%d-%H%M')}.json"
with open(manifest_path, 'w') as f:
    json.dump(MANIFEST, f, indent=2)

print()
print(f"=== MANIFEST ===")
print(f"Total assets: {len(MANIFEST['assets'])}")
print(f"Images: {sum(1 for a in MANIFEST['assets'] if a['type']=='image')}")
print(f"Voices: {sum(1 for a in MANIFEST['assets'] if a['type']=='voice')}")
print(f"Total cost: ${sum(a['cost'] for a in MANIFEST['assets']):.4f}")
print(f"Models used: {json.dumps(MANIFEST['models_used'], indent=2)}")
print(f"Manifest: {manifest_path}")
