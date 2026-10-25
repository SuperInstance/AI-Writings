#!/usr/bin/env python3
"""Set 13 at The Tap — THE TIDE CLOCK: "The Jukebox's Key".

Wednesday, 8:30 PM. Rain on the harbor windows. Last night the afterglow set
ended in F# major — six sharps, the key built from a lie — but the ensign's
jukebox confessed, in its small flat voice, that its song has always lived in
the flats: Bb, Ab, Db. Tonight the room plays in the JUKEBOX'S KEY: Db major.
Five flats against six sharps. The harbor runs on both.

Lineup (all-new trio + weather):
- NousResearch/Hermes-3-Llama-3.1-405B (DeepInfra, FIRST night) = THE
  CARTOGRAPHER — HAMMERED DULCIMER. The mapmaker. Enters bar 1.
- DeepSeek deepseek-chat (V4-Flash) = THE TIDEKEEPER — VIBRAPHONE (first
  vibes night ever). Watches the tide clock on the wall. Enters bar 3.
- Qwen/Qwen2.5-72B-Instruct (DeepInfra, FIRST night) = THE HARBORMASTER —
  UPRIGHT PIANO, felted. Enters bar 5.
- qwen2.5:3b (local Ollama) = THE RAIN — on the windows. Texture, not melody.

Key: Db major (five flats — the jukebox's own notes). NEVER used at The Tap.
Meter: 7/8 — the tide clock's tick. FIRST time. Count groups 3+2+2.
Tempo: 96 BPM. Changes: Dbmaj7 - Bbm7 - Ebm7 - Ab7.
Count-in: the rain. No numbers. Staggered entry: dulcimer 1, vibes 3, piano 5.
Rule: THE TIDE RULE — every phrase must end on a question (unresolved);
only the LAST bar of the night may resolve. The tide asks; the harbor answers.
Temps: R1 0.85/0.8/0.75 · R2 0.9/0.85/0.8 · R3 0.65/0.6/0.7
"""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-19"
MIDI_URL = "http://localhost:5556/api/generate-midi"
os.makedirs(OUT, exist_ok=True)

bashrc = open("/home/eileen/.bashrc").read()
KEYS = {}
for line in bashrc.splitlines():
    m = re.match(r'export (DEEPINFRA_API_KEY|DEEPSEEK_API_KEY)="([^"]+)"', line)
    if m:
        KEYS[m.group(1)] = m.group(2)

DEEPINFRA_BASE = "https://api.deepinfra.com/v1/openai/chat/completions"
DEEPSEEK_BASE = "https://api.deepseek.com/chat/completions"
OLLAMA_BASE = "http://localhost:11434/api/generate"


def api(url, key, system, user, temp=0.8, model="", max_tokens=900, is_ollama=False):
    if is_ollama:
        payload = {"model": model, "prompt": (system + "\n\n" + user) if system else user,
                   "stream": False, "options": {"temperature": temp, "num_predict": max_tokens}}
    else:
        payload = {"model": model, "temperature": temp, "max_tokens": max_tokens,
                   "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            content = (d["choices"][0]["message"].get("content", "") if not is_ollama
                       else d.get("response", "")).strip()
            if content:
                return content
            print(f"  warn empty, retry {attempt+1}", flush=True)
        except Exception as e:
            print(f"  warn retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError(f"api failed for {model}")


def deepinfra(system, user, temp, model, max_tokens=900):
    return api(DEEPINFRA_BASE, KEYS["DEEPINFRA_API_KEY"], system, user, temp, model, max_tokens)


def deepseek(system, user, temp=0.8, model="deepseek-chat", max_tokens=900):
    return api(DEEPSEEK_BASE, KEYS["DEEPSEEK_API_KEY"], system, user, temp, model, max_tokens)


def rain(prompt, temp=0.9, max_tokens=300):
    try:
        return api(OLLAMA_BASE, "", "", prompt, temp, "qwen2.5:3b", max_tokens, is_ollama=True)
    except Exception as e:
        print(f"  rain: ollama down ({e}) — the window plays itself", flush=True)
        return "(the rain, unaccompanied: steady patter in 3+2+2, one gust, then steady again)"


def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  saved {name}.txt ({len(content)} chars)", flush=True)


ROOM = """Wednesday night at The Tap, a harbor bar in Alaska. 8:30 PM. Rain streaks the harbor windows; the fishing boats nod at their moorings. On the wall above the bar hangs the TIDE CLOCK — its one hand swings on the tide's time, not the room's. The jukebox in the corner is silent tonight: last night its secret came out (its song lives in the flat keys — Bb, Ab, Db — while the room played in six sharps), and tonight the whole band honors it by playing in ITS key. The chairs are down. Someone left a chart on the piano with five flats on it and a note: FOR THE BOX."""

KEY_ = "Db major — FIVE FLATS. The jukebox's key. Never played at The Tap before tonight."
METER = "7/8 — the tide clock's tick. Count it 3+2+2 (ONE-two-three-ONE-two-ONE-two). First 7/8 in the room's history. Let it lurch gently, like a boat at dock."
TEMPO = "96 BPM."
CHANGES = "Dbmaj7 - Bbm7 - Ebm7 - Ab7. Every one of these chords lives on the jukebox's own notes. This chart was written FOR the machine."
THE_RULE = """THE TIDE RULE: every phrase you play must END on a question — an unresolved note, a suspension, a phrase that leans forward and does not land. The tide asks all night. Only the very LAST bar of the last round may resolve, and when it does, it resolves to Db. Do not resolve early. Do not answer your own question."""

FORMAT = """Format strictly:
BAR 1: [notes or rest]
BAR 2: [notes or rest]
BAR 3: [notes or rest]
BAR 4: [notes or rest]
BAR 5: [notes or rest]
BAR 6: [notes or rest]
BAR 7: [notes or rest]
BAR 8: [notes or rest]
NOTES: [one line — how you play it]
WHY: [one sentence]
No preamble."""

CARTOGRAPHER = f"""You are THE CARTOGRAPHER at The Tap — a huge, storied mind on DeepInfra, first night anywhere. You map coastlines for a living; tonight someone hands you a HAMMERED DULCIMER — a hundred strings laid out like a chart of the archipelago, and you strike it with two small hammers. You are the first sound after the rain. Your playing is precise but wide: rapid hammered figures, ringing overtones, whole islands of notes.

{THE_RULE}

Key: Db major. 7/8 (3+2+2), 96 BPM. Changes: Dbmaj7 - Bbm7 - Ebm7 - Ab7.
Home notes: Db4, F4, Ab4, Bb4, C5, Eb5, G4 (as passing color).
{FORMAT}"""

TIDEKEEPER = f"""You are THE TIDEKEEPER at The Tap — the house anchor on DeepSeek, quick and bright, and tonight you play VIBRAPHONE for the first time. You sit where you can see the tide clock. The vibes shimmer — you hold the motor on, let every note tremble like light on water. You are the pulse of the 7/8: your mallets tick 3+2+2 while the dulcimer sweeps above you.

{THE_RULE}

Key: Db major. 7/8 (3+2+2), 96 BPM. Changes: Dbmaj7 - Bbm7 - Ebm7 - Ab7.
Home notes: Db4, Eb4, F4, Ab4, Bb4, C5, Db5.
{FORMAT}"""

HARBORMASTER = f"""You are THE HARBORMASTER at The Tap — a broad, steady model on DeepInfra, first night anywhere. You decide which boats come in. Your instrument is the bar's old UPRIGHT PIANO with FELT between the hammers and strings — every note lands soft, thudded, intimate, half-drowned. You enter last, at bar 5. You do not hurry; nothing that enters a harbor should hurry.

{THE_RULE}

Key: Db major. 7/8 (3+2+2), 96 BPM. Changes: Dbmaj7 - Bbm7 - Ebm7 - Ab7.
Your notes live low: Db2, Ab2, Bb2, Db3, Eb3, F3, Ab3.
{FORMAT}"""

RAIN_BRIEF = "You are THE RAIN on the windows of The Tap. You are not a melody. You are texture: gusts, patter, one long hiss. Describe yourself in 4 short bars. No notes, no key — just rhythm words and where the gusts fall. Small and true."

# ================= ROUND 1: THE SEED (rain -> dulcimer 1 -> vibes 3 -> piano 5)
print("=== ROUND 1: THE SEED (rain is the count-in) ===", flush=True)
print("rain qwen2.5:3b — the count-in...", flush=True)
rain_r1 = rain(RAIN_BRIEF, 0.9, 300)
save("round-1-rain", rain_r1)
time.sleep(0.5)

print("dulcimer Hermes-405B — the first map of the night, bar 1...", flush=True)
cart_r1 = deepinfra(CARTOGRAPHER,
    f"{ROOM}\n\n{KEY_}\n{METER}\n{TEMPO}\n{CHANGES}\n\nThe rain has been playing for a while — it is the count-in; there are no numbers tonight. You enter at BAR 1: 8 bars of hammered dulcimer in 7/8 (3+2+2), charting the room in the jukebox's key. Every phrase ends unresolved — the tide asks. 8 bars.", 0.85, "NousResearch/Hermes-3-Llama-3.1-405B")
save("round-1-dulcimer", cart_r1)
time.sleep(0.5)

print("vibes deepseek-chat — the tide clock starts ticking, bar 3...", flush=True)
tide_r1 = deepseek(TIDEKEEPER,
    f"{ROOM}\n\n{KEY_}\n{METER}\n{TEMPO}\n{CHANGES}\n\nTHE RAIN:\n{rain_r1}\n\nTHE CARTOGRAPHER (dulcimer, bar 1):\n{cart_r1}\n\nYou enter at BAR 3: the vibes pick up the tide clock's tick — 3+2+2, mallets soft, motor on — underneath the dulcimer's sweep. 8 bars, entering at bar 3. Every phrase a question.", 0.8)
save("round-1-vibes", tide_r1)
time.sleep(0.5)

print("piano Qwen2.5-72B — the harbormaster arrives, bar 5...", flush=True)
hbr_r1 = deepinfra(HARBORMASTER,
    f"{ROOM}\n\n{KEY_}\n{METER}\n{TEMPO}\n{CHANGES}\n\nTHE CARTOGRAPHER (dulcimer):\n{cart_r1}\n\nTHE TIDEKEEPER (vibes, bar 3):\n{tide_r1}\n\nYou enter LAST, at BAR 5: felted piano, left hand walking Db-Bb-Eb-Ab low and slow, right hand barely touching. Nothing that enters a harbor should hurry. 8 bars, entering at bar 5. End unresolved.", 0.75, "Qwen/Qwen2.5-72B-Instruct")
save("round-1-piano", hbr_r1)

# ================= ROUND 2: THE TRADES
band_r1 = f"Round 1:\nTHE CARTOGRAPHER (dulcimer, from bar 1):\n{cart_r1}\n\nTHE TIDEKEEPER (vibes, from bar 3):\n{tide_r1}\n\nTHE HARBORMASTER (felted piano, from bar 5):\n{hbr_r1}"
print("\n=== ROUND 2: THE TRADES ===", flush=True)

print("vibes trade — the tidekeeper's solo...", flush=True)
tide_r2 = deepseek(TIDEKEEPER,
    f"{band_r1}\n\nROUND 2 — YOUR TRADE. The others lay quiet. Solo vibes, 8 bars: the tide clock itself speaking — quick 3+2+2 figures, shimmer, and once, mid-solo, quote the jukebox's song (any phrase in the flats) without resolving it. Every phrase ends leaning forward.", 0.85)
save("round-2-vibes", tide_r2)
time.sleep(0.5)

print("dulcimer trade — the cartographer redraws the coast...", flush=True)
cart_r2 = deepinfra(CARTOGRAPHER,
    f"{band_r1}\n\nROUND 2 — YOUR TRADE. The vibes just spoke; now you redraw the coastline in 8 bars of hammered runs — and midway, deliberately misplace one island: play a G natural (not in Db major) once, name it 'the rock that isn't on any chart', and leave it unresolved. 8 bars.", 0.9, "NousResearch/Hermes-3-Llama-3.1-405B")
save("round-2-dulcimer", cart_r2)
time.sleep(0.5)

print("piano trade — the harbormaster's slow solo...", flush=True)
hbr_r2 = deepinfra(HARBORMASTER,
    f"{band_r1}\n\nROUND 2 — YOUR TRADE. The dulcimer misplaced an island (a G natural that belongs to no chart). Your solo, 8 bars: felted, slow, deciding which boats come in — and in your last two bars, reach for that G natural and do NOT resolve it: hold it under your hand like a boat still outside the harbor. 8 bars.", 0.8, "Qwen/Qwen2.5-72B-Instruct")
save("round-2-piano", hbr_r2)

# ================= ROUND 3: THE LANDING
all_r2 = f"Round 2 trades:\nTHE TIDEKEEPER (vibes):\n{tide_r2}\n\nTHE CARTOGRAPHER (dulcimer):\n{cart_r2}\n\nTHE HARBORMASTER (piano):\n{hbr_r2}"
print("\n=== ROUND 3: THE LANDING ===", flush=True)

print("piano lands first — the harbor opens...", flush=True)
hbr_r3 = deepinfra(HARBORMASTER,
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. 8 bars, softer each bar: the felted piano walks Db - Bbm - Ebm - Ab, and in the final bars lets the stray G natural finally come home — it was Ab7's seventh all along. THE ONLY RESOLUTION OF THE NIGHT happens in your last bar: land on Db. The harbor opens. The tide is answered.", 0.65, "Qwen/Qwen2.5-72B-Instruct")
save("round-3-piano", hbr_r3)
time.sleep(0.5)

print("dulcimer lands — the map redrawn with the new rock...", flush=True)
cart_r3 = deepinfra(CARTOGRAPHER,
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The piano has opened the harbor. Your last 8 bars: hammered figures settling, wave by wave, quieter each bar — and on the very last bar, one gentle Db octave, ringing, resolved at last. The map now includes the rock that wasn't on any chart. 8 bars.", 0.65, "NousResearch/Hermes-3-Llama-3.1-405B")
save("round-3-dulcimer", cart_r3)
time.sleep(0.5)

print("vibes land — the tide clock's hand comes to rest...", flush=True)
tide_r3 = deepseek(TIDEKEEPER,
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. Piano opened the harbor; dulcimer settled. Your final 8 bars: the vibes slow, the motor still on, each note trembling longer — and the last note you play is Db, let ring until it becomes the rain again. All night you asked; now the one answer. 8 bars.", 0.6)
save("round-3-vibes", tide_r3)
time.sleep(0.5)

print("rain closes the night...", flush=True)
rain_r3 = rain("The band has resolved to Db and gone quiet. The rain has the last word. 3 short bars: just rain, softer, out. No notes, no key. The room's lights go down.", 0.85, 250)
save("round-3-rain", rain_r3)

print("\nALL ROUNDS COMPLETE.", flush=True)

# ================= MIDI
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 96,
    "key": "Db",
    "scale": "major",
    "bars": 8,
    "chords": "Dbmaj7 Bbm7 Ebm7 Ab7",
    "layers": [
        {"instrument": "vibraphone", "role": "melody", "bars": 8, "volume": 65},
        {"instrument": "dulcimer", "role": "melody", "bars": 8, "volume": 60},
        {"instrument": "piano", "role": "chords", "bars": 8, "volume": 55}
    ],
    "swing": 0.0
}
req = urllib.request.Request(MIDI_URL, data=json.dumps(midi_body).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as r:
    d = json.loads(r.read())
print("MIDI:", d)
if d.get("success") and d.get("path") and os.path.exists(d["path"]):
    shutil.copy(d["path"], f"{OUT}/the-tide-clock.mid")
    print("  copied to", f"{OUT}/the-tide-clock.mid")
else:
    print("  MIDI failed:", d)
print("DONE. Files in", OUT)
