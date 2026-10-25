#!/usr/bin/env python3
import json, urllib.request, os, shutil
D = os.path.dirname(os.path.abspath(__file__))
prompt = """A late-night jazz-fusion jam titled "the kitchen after close", recorded in a bar kitchen.
Key: G major (the tonic G is sacred - resolved only on the final chord). Meter: 5/4, 88 BPM, loose swing.
Five instruments: muted trumpet (the line cook), steel-bowl percussion kit (the dishwasher), upright piano with a sticking low A (the waitress), baritone sax (the cook's nephew, plays loud), and a low drone pad = the walk-in refrigerator humming G throughout (track 5, bass).
Structure: Round 1 organic staggered entry (drone first, percussion bar 2, trumpet bar 3, piano bar 5, bari sax bar 7). Round 2 solos trading: bari sax, then piano, then trumpet, then percussion, one knocked-over bowl-clatter accent mid-round. Round 3 everyone together, diminuendo, instruments drop out one by one until only the refrigerator drone's low G remains, then a door hiss (noise swell) ends it.
Phrases should end with one damped/muted note each - choked articulation. Warm, small-room, after-hours vibe."""
req = urllib.request.Request("http://localhost:5556/api/generate-midi",
    data=json.dumps({"prompt": prompt, "filename": "the-kitchen"}).encode(),
    headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=300) as r:
    resp = json.load(r)
print("MIDI:", resp)
p = resp.get("path") or resp.get("file") or ""
for c in [p, os.path.expanduser(str(p))]:
    if c and os.path.exists(c):
        shutil.copy(c, f"{D}/the-kitchen.mid"); print("copied from", c); break
