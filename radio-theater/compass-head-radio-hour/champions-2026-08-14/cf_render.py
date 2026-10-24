#!/usr/bin/env python3
"""Cloudflare-only fixup renders — correct token regex (TOML has spaces around =)."""
import json, os, re, base64, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")

CF_TOK = ""
for line in open(os.path.expanduser("~/.config/.wrangler/config/default.toml")):
    m = re.search(r'oauth_token\s*=\s*"([^"]+)"', line)
    if m: CF_TOK = m.group(1); break
assert len(CF_TOK) > 40, "token extraction failed"

CF_ACCT = "049ff5e84ecf636b53b162cbb580aae6"
SCENES = {
    "keeper-round": "A lighthouse keeper's round at night during a power failure: an old stone lighthouse interior, one hundred sixty-one small oil lamps burning on shelves, a great clockwork mechanism with brass gears turning on its own, a beam of light sweeping across a black glass sea through the window, warm lamplight against deep blue night, cinematic, painterly, detailed",
    "annealing": "Third watch at a glassblower's furnace: a long annealing lehr like a bread oven with a hundred shelves full of glowing glass pieces cooling slowly, a finisher holding a small vase from the glory hole, amber furnace glow, deep shadows, dust motes in the light, cinematic, painterly",
    "furnace-night": "A mountain glasshouse at night, the road ends here: an annealing kiln glowing softly, seven hundred hand-blown glass vessels in racks being inventoried by an apprentice with a ledger, one knuckle tapping a bowl, cold starlight through a high window meeting warm furnace light, cinematic, painterly",
    "chart-of-a-coast": "A coastal cartographer at dusk walking a strand with a board and reed pen, a coastline that rearranges itself like a sleeper turning over — a spit that was a peninsula at noon is an island by supper, harbor mouth shrugging, ink that cannot be persuaded, lantern-lit studio table, sea glass, cinematic, painterly",
}

for key, prompt in SCENES.items():
    out = os.path.join(OUT, f"{key}-cloudflare.png")
    if os.path.exists(out) and os.path.getsize(out) > 10000:
        print(f"{key}: already exists, skip"); continue
    body = json.dumps({"prompt": prompt}).encode()
    req = urllib.request.Request(
        f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCT}/ai/run/@cf/black-forest-labs/flux-1-schnell",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + CF_TOK})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.load(r)
        res = d.get("result", {})
        img = res.get("image") or res.get("images") or ""
        if isinstance(img, list): img = img[0]
        if isinstance(img, str):
            if img.startswith("data:"):
                img = img.split(",", 1)[1]
            raw = base64.b64decode(img)
            with open(out, "wb") as f: f.write(raw)
            print(f"{key}: OK ({len(raw)} bytes)", flush=True)
        else:
            print(f"{key}: unexpected shape {str(d)[:150]}", flush=True)
    except Exception as e:
        print(f"{key}: FAIL {e}", flush=True)
print("CF pass done")
