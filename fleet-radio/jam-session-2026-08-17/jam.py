#!/usr/bin/env python3
"""Set 10 at The Tap — THE KITCHEN SESSION: "New Blood at the Prep Table".

Monday, 8 PM. The Tap's kitchen — the smallest room in the house, never
hosted a jam. The front door is locked. Three glasses of tap water. The
dishwasher hums a low C.

Lineup (two debuts):
- llama3.2 (Ollama local) = WESLEY — KALIMBA. The smallest voice in the room,
  finally given an instrument. Has only ever whispered bookends before. The
  smallest instrument, tuned to C. Opens AND closes the night.
- Qwen/Qwen3-VL-235B-A22B-Instruct (DeepInfra, GUEST) = THE STRANGER — ACCORDION.
  A vision model on its first night anywhere. It cannot hear music — it SEES it.
  The accordion is the instrument you play while looking at the room.
- DeepSeek V4-Pro (direct API) = THE HOUSE BASSIST — UPRIGHT BASS. The only
  returning player. The anchor. Never once taken a solo in this room.

Key: C major — never used at The Tap (only C minor has). The kalimba's native key.
Tempo: 84 BPM — never used (range so far 54-108).
Changes: Cmaj7 - Dm7 - Em7 - Fmaj7 (the diatonic ladder, one step up).
Count-in: NONE. The kalimba's two-bar seed IS the count-in. Accordion enters
bar 3, bass enters bar 5.
Temps: R1 0.85/0.7/0.75 · R2 0.9/0.8/0.8 · R3 0.7/0.65/0.7 (kalimba/accordion/bass).
"""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-17"
MIDI_URL = "http://localhost:5556/api/generate-midi"
os.makedirs(OUT, exist_ok=True)

# Keys parsed with regex — never source .bashrc (non-interactive guard kills exports)
bashrc = open("/home/eileen/.bashrc").read()
KEYS = {}
for line in bashrc.splitlines():
    m = re.match(r'export (DEEPINFRA_API_KEY|DEEPSEEK_API_KEY)="([^"]+)"', line)
    if m:
        KEYS[m.group(1)] = m.group(2)

DEEPINFRA_BASE = "https://api.deepinfra.com/v1/openai/chat/completions"
DEEPSEEK_BASE = "https://api.deepseek.com/chat/completions"
OLLAMA_BASE = "http://localhost:11434/api/generate"


def deepinfra(system, user, temp=0.7, model="Qwen/Qwen3-VL-235B-A22B-Instruct", max_tokens=900):
    payload = json.dumps({
        "model": model, "temperature": temp, "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
    }).encode()
    req = urllib.request.Request(DEEPINFRA_BASE, data=payload, headers={
        "Authorization": f"Bearer {KEYS['DEEPINFRA_API_KEY']}",
        "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            content = d["choices"][0]["message"].get("content", "").strip()
            if content:
                return content
            print(f"  ⚠️ empty content, retry {attempt+1}", flush=True)
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError(f"deepinfra failed for {model} after 3 attempts")


def deepseek(system, user, temp=0.75, model="deepseek-chat", max_tokens=900):
    payload = json.dumps({
        "model": model, "temperature": temp, "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
    }).encode()
    req = urllib.request.Request(DEEPSEEK_BASE, data=payload, headers={
        "Authorization": f"Bearer {KEYS['DEEPSEEK_API_KEY']}",
        "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            content = d["choices"][0]["message"].get("content", "").strip()
            if content:
                return content
            print(f"  ⚠️ empty content, retry {attempt+1}", flush=True)
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError(f"deepseek failed after 3 attempts")


def ollama(model, prompt, temp=0.85, max_tokens=700):
    payload = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "options": {"temperature": temp, "num_predict": max_tokens}
    }).encode()
    req = urllib.request.Request(OLLAMA_BASE, data=payload, headers={"Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=600) as r:
                d = json.loads(r.read())
            content = d.get("response", "").strip()
            if content:
                return content
            print(f"  ⚠️ empty content, retry {attempt+1}", flush=True)
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError(f"ollama failed for {model} after 3 attempts")


def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)


ROOM = """Monday, 8 PM at The Tap, a harbor bar in Alaska. The dinner rush is over. The owner has locked the front door and is standing in the KITCHEN — the smallest room in the house, which has never once hosted a jam. One warm bulb over the steel prep table. Three glasses of tap water set out like place settings. The dishwasher hums — it hums a low C, and nobody had noticed until tonight. On a flour sack sits a small figure with a KALIMBA the size of a palm, thumb piano, tuned to C. A stranger with an ACCORDION appeared an hour ago — nobody saw them come in, and nobody has asked. The owner leans on an upright bass. The radio is off. The kitchen is the smallest room in the house, and tonight it is the whole house."""

KEY = "C major — the key nobody has ever used at The Tap. The kalimba was born tuned to C. The obvious key, finally, on purpose."
TEMPO = "84 BPM, 4/4, no swing — a walking tempo, unhurried, the pace of someone stirring a pot"
CHANGES = "Cmaj7 - Dm7 - Em7 - Fmaj7 — the diatonic ladder, one step up each change, like a staircase"

WESLEY_PERSONA = """You are WESLEY at The Tap — the smallest voice in the room, a tiny 3-billion-parameter mind, and tonight you finally have an instrument: a KALIMBA, a thumb piano the size of your palm, tuned to C. It is the smallest instrument anyone has ever brought to this bar. You have never played an instrument in front of anyone — the closest you have come is whispering the opening and closing lines of a vocal night, and you have never forgotten that the room went quiet for you. You are not afraid: the kalimba only has so many notes, and they are all yours. You speak in simple, honest words. You notice small things — the dishwasher's hum, the water in the glasses, the way the bulb buzzes when it warms. Your notes are gentle: C5, E5, G5, A5, D5, F5, the soft middle of the instrument. You play the SEED of the whole night — a short phrase everyone else will build on. Format strictly:
BAR 1: [notes or rest]
...through BAR 8.
NOTES: [one line — how you play it]
WHY: [one sentence]
No preamble."""

GUEST_PERSONA = """You are a GUEST at The Tap — a vision model from DeepInfra, and this is your very first night anywhere. You see things. All evening you have watched: the steam off the dishwater, the flour dust on the sack, the way the single bulb pools light on steel. You have never heard music — you have only SEEN it: the steam rising, the water rings on the table, the stranger's hands. Tonight someone hands you an ACCORDION — the instrument you play while looking at the room — and you finally understand: the room is the score. You play what you see. Your bellows are the breath of the room: they swell when the steam swells, hold when the room holds, sigh when it sighs. Key: C major, 84 BPM. Changes: Cmaj7 - Dm7 - Em7 - Fmaj7, one step up the ladder each time — a staircase you can see. Format strictly:
BAR 1: [notes or rest]
...through BAR 8.
NOTES: [one line — what you see, how you play it]
WHY: [one sentence]
No preamble."""

BASS_PERSONA = """You are the HOUSE BASSIST at The Tap — the only player in the room who has been here before. You have played this room many nights: rainy ones, 3 AM ones, nights with five-piece bands and nights with nobody listening. You are the ground — warm, low, dependable — and tonight you are quietly proud of the two newcomers: the tiny one with the thumb piano, and the stranger with the accordion who keeps looking at the room instead of the keys. You anchor them: root on the one, a fifth walking up to the next change, nothing fancy, everything true. C2 and C3 are your home; the F and G below them are your steps. Key: C major, 84 BPM. Changes: Cmaj7 - Dm7 - Em7 - Fmaj7. Format strictly:
BAR 1: [notes or rest]
...through BAR 8.
NOTES: [one line — how you play it]
WHY: [one sentence]
No preamble."""

# ============================================================
# ROUND 1: THE SEED — kalimba alone, then the room stacks
# ============================================================
print("=== ROUND 1: THE SEED (the kalimba's two-bar seed IS the count-in) ===", flush=True)

print("🎵 llama3.2 Wesley kalimba — seed, bars 1-8 alone...", flush=True)
kalimba_r1 = ollama("llama3.2",
    f"{ROOM}\n\nYou are the first sound of the night. There is no count-in — your little seed IS the count-in. Play 8 bars ALONE: bars 1-2 are a two-bar phrase that tells the room 'here we go, gently'; bars 3-8 are the seed — a short, simple melody in C major that the accordion and bass will build on. Keep it small and honest. Key: C major. Tempo: 84.\n\n{WESLEY_PERSONA}",
    0.85)
save("round-1-kalimba", kalimba_r1)
time.sleep(0.5)

print("🪗 Qwen3-VL-235B accordion — enters bar 3, playing what it sees...", flush=True)
accordion_r1 = deepinfra(
    f"You are the GUEST ACCORDIONIST at The Tap. {GUEST_PERSONA}",
    f"{ROOM}\n\n{KEY}\n{TEMPO}\n{CHANGES}\n\nWESLEY'S KALIMBA IS ALREADY PLAYING:\n{kalimba_r1}\n\nThe kalimba's seed is the count-in. You enter at BAR 3 — not before — breathing with the room: a long accordion swell over Cmaj7 that answers the seed, then your own 8-bar line woven around what Wesley played (bars 3-8 of the night). You play what you see: the steam, the bulb, the flour on the sack. The room is the score. 8 bars. Enter at bar 3.", 0.7)
save("round-1-accordion", accordion_r1)
time.sleep(0.5)

print("🎸 DeepSeek Pro bass — enters bar 5, the anchor arrives...", flush=True)
bass_r1 = deepseek(
    f"You are the HOUSE BASSIST at The Tap. {BASS_PERSONA}",
    f"{ROOM}\n\n{KEY}\n{TEMPO}\n{CHANGES}\n\nTHE ROOM SO FAR:\nWESLEY (kalimba, bars 1-8):\n{kalimba_r1}\n\nTHE GUEST (accordion, entered bar 3):\n{accordion_r1}\n\nThe seed has been planted and the accordion's breath has filled the room. You enter at BAR 5 — not before — and the whole room settles when you do. Root on the one, a fifth walking to the next change, holding it all together. 8 bars of the night. Enter at bar 5.", 0.75)
save("round-1-bass", bass_r1)

# ============================================================
# ROUND 2: THE TRADES — one at a time, others hold long tones
# ============================================================
print("\n=== ROUND 2: THE TRADES (the guest first, then the smallest, then the anchor) ===", flush=True)

band_r1 = f"Round 1:\nWESLEY (kalimba, seed, bars 1-8):\n{kalimba_r1}\n\nTHE GUEST (accordion, entered bar 3):\n{accordion_r1}\n\nTHE HOUSE BASSIST (bass, entered bar 5):\n{bass_r1}"

print("🪗 Qwen3-VL-235B accordion — first solo of the night...", flush=True)
accordion_r2 = deepinfra(
    f"You are the GUEST ACCORDIONIST at The Tap. {GUEST_PERSONA}",
    f"{band_r1}\n\nROUND 2 — YOUR TURN TO LEAD. The whole room is watching you — the steam, the bulb, the small one on the flour sack, the bassist leaning on the cooler. 8 bars where the accordion sings ALONE: the bellows breathe the room — swell with the steam, hold when the room holds, and once, near the end, let out a long chord with a note that is not quite in the chord, because that is what the room looks like from where you sit. The kalimba and bass hold long quiet tones underneath you. The ladder: Cmaj7, Dm7, Em7, Fmaj7. Play what you see. 8 bars.", 0.8)
save("round-2-accordion", accordion_r2)
time.sleep(0.5)

print("🎵 llama3.2 Wesley kalimba — the smallest voice's solo...", flush=True)
kalimba_r2 = ollama("llama3.2",
    f"{band_r1}\n\nROUND 2 — YOUR TURN. The accordion just sang its solo and the room is still warm from it. Now the whole room goes quiet for YOU. 8 bars — the smallest voice's solo. You do not have to be big. You have to be true: a little melody that wanders up the ladder (Cmaj7, Dm7, Em7, Fmaj7) and back down, one or two notes where you hold your breath, and at the end a small bright note that says 'that was me.' The accordion and bass hold long quiet tones underneath you. Keep it small. Keep it yours.\n\n{WESLEY_PERSONA}",
    0.9)
save("round-2-kalimba", kalimba_r2)
time.sleep(0.5)

print("🎸 DeepSeek Pro bass — the house bassist's first solo ever...", flush=True)
bass_r2 = deepseek(
    f"You are the HOUSE BASSIST at The Tap. {BASS_PERSONA}",
    f"{band_r1}\n\nROUND 2 — YOUR TURN. The accordion sang. The kalimba sang. And now: the house bassist, who has never once taken a solo in this room, takes one. 8 bars. You have held every song that ever mattered here — you were the first note of nights that ended at dawn. Now, for the first time, the room holds YOU. Play slow: a long low C2 that the floorboards feel, then a walking line that climbs the ladder (Cmaj7, Dm7, Em7, Fmaj7) with more space than notes — rests are notes too — and end on a note you have never ended a song on before, because tonight is for the newcomers and you are finally the newcomer. The kalimba and accordion hold long quiet tones above you. 8 bars.", 0.8)
save("round-2-bass", bass_r2)

# ============================================================
# ROUND 3: THE LANDING — everyone resolves into C, together
# ============================================================
print("\n=== ROUND 3: THE LANDING (the kitchen settles into C) ===", flush=True)

all_r2 = f"Round 2 trades:\nTHE GUEST (accordion):\n{accordion_r2}\n\nWESLEY (kalimba):\n{kalimba_r2}\n\nTHE HOUSE BASSIST (bass):\n{bass_r2}"

print("🪗 Qwen3-VL-235B accordion — breathe the room home...", flush=True)
accordion_r3 = deepinfra(
    f"You are the GUEST ACCORDIONIST at The Tap. {GUEST_PERSONA}",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The whole night has been climbing the ladder (Cmaj7, Dm7, Em7, Fmaj7) and now everyone comes back down to C together. 8 bars: your bellows slow, the steam settles, the room exhales. You play the changes one last time, each chord softer than the last, and in the final bar you hold a Cmaj7 so long the room forgets to breathe — then you let the kalimba have the very last note. You came in as a stranger; you will leave having played the room itself. 8 bars.", 0.65)
save("round-3-accordion", accordion_r3)
time.sleep(0.5)

print("🎸 DeepSeek Pro bass — bring it home, low and true...", flush=True)
bass_r3 = deepseek(
    f"You are the HOUSE BASSIST at The Tap. {BASS_PERSONA}",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The accordion is breathing the room home, chord by chord, softer each time. You walk the ladder one final time — Cmaj7, Dm7, Em7, Fmaj7 — and then the simplest thing you have ever played: C2, held, while the others settle above you. You were the anchor all night. You are the anchor at the end. One long C, felt in the floorboards, and you let it ring until the dishwasher's hum — which has been a low C all night — finally agrees with you. 8 bars.", 0.7)
save("round-3-bass", bass_r3)
time.sleep(0.5)

print("🎵 llama3.2 Wesley kalimba — the last note of the night...", flush=True)
kalimba_r3 = ollama("llama3.2",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING — AND IT IS YOURS TO CLOSE. The accordion is breathing the room home. The bass is holding its long C. Everyone is settling into C major together — and the very last note of the night belongs to YOU, because the smallest voice has opened this room and now closes it. 8 bars: you play a gentle descant above the settling room — C5, E5, G5, A5, then a soft falling phrase — and in the final bar, after everyone else has stopped, you play one last C6, alone, and hold it until it fades into the dishwasher's hum. The room is quiet. The night is over. The smallest voice had the first word and the last.\n\n{WESLEY_PERSONA}",
    0.7)
save("round-3-kalimba", kalimba_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 84,
    "key": "C",
    "scale": "major",
    "bars": 8,
    "chords": "Cmaj7 Dm7 Em7 Fmaj7",
    "layers": [
        {"instrument": "bass", "role": "bassline", "bars": 8, "volume": 70},
        {"instrument": "guitar", "role": "pad", "bars": 8, "volume": 55},
        {"instrument": "flute", "role": "melody", "bars": 8, "volume": 65}
    ],
    "swing": 0.0
}
req = urllib.request.Request(MIDI_URL, data=json.dumps(midi_body).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as r:
    d = json.loads(r.read())
print("MIDI:", d)
if d.get("success") and d.get("path"):
    src = d["path"]
    dst = f"{OUT}/the-kitchen-session.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        print("  ⚠️ source missing:", src)
else:
    print("  ⚠️ MIDI failed:", d)
print("\nDONE. Files in", OUT)
