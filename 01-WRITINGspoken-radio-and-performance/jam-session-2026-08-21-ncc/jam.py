#!/usr/bin/env python3
"""Set 15 at The Tap — NIGHT COMMUNICATIONS CLASS: "Four Small Lights".

Friday, 8:30 PM, August 21, 2026. Last night the room split between E and Eb
and the singing bowls found a third key nobody planned. Tonight, nobody plays
a normal instrument. Tonight is SIGNALS: a harbor after the power fails, four
small stations blinking at each other across the dark water. The Tap has no
key center — every chord is borrowed, nobody is home. Each player carries one
of the four 4-note cells; the music moves when cells overlap by exactly two
notes (that overlap is the only "harmony" tonight — shared water, no shared
ground).

LINEUP (all-debut horns; Flash anchors) — the smallest band ever fielded:
- qwen3:8b (local Ollama, DEBUT) = STATION ONE — signal whistle. Cell A: C, D, G, A.
- gemma3:4b (local Ollama, DEBUT) = STATION TWO — hand-crank radio. Cell B: D, E, A, B.
- LiquidAI/lfm2.5-350m (local Ollama, DEBUT — the smallest player ever on a Tap stage, 350M) = STATION THREE — the firefly jar. Cell C: F#, G#, C#, D#.
- DeepSeek deepseek-chat (anchor, the only veteran) = THE RELAY — accordion, plays ALL cells, ferries the two-note overlaps between stations.

Key: NONE. No key center. Four 4-note cells (A: C D G A / B: D E A B /
C: F# G# C# D#). Chords only exist where two cells share two notes.
Meter: 4/4. Tempo: 63 BPM — Morse speed, roughly.
Count-in: A FLASHLIGHT CLICKED THREE TIMES (no numbers, no notes). Station
Three (the firefly jar) blinks first — it's the smallest; it goes first.
Rule: THE TWO-NOTE HANDSHAKE — every solo must end with the two notes it
shares with the NEXT player's cell, stated plainly. That's the only cadence.
The Relay's accordion may add one borrowed pedal under any handshake.
Temps: R1 0.85 across; R2 0.9; R3 0.7.
Context fed to players: an excerpt from bioluminescence-at-dawn.md (what the
fleet glowed at 0300), plus last night's split-seven landing on the bowls'
G# — which is why Cell C exists (F#, G#, C#, D#: the bowls' key, borrowed).
"""
import json, re, os, urllib.request

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-21-ncc"
MIDI_URL = "http://localhost:5556/api/generate-midi"
os.makedirs(OUT, exist_ok=True)

bashrc = open("/home/eileen/.bashrc").read()
DEEPSEEK_KEY = dict(re.findall(r'export (\w+)="([^"]+)"', bashrc))["DEEPSEEK_API_KEY"]

BIO = """From the fleet's log (bioluminescence-at-dawn.md): "The ocean at 0300 is a body of water that has agreed, provisionally, to be invisible. But the ocean does stir... Each model glows a different color... The green of something that was already there becoming visible because something from somewhere else hit it. Flash is fast and the green is brief — but while it's there, it illuminates a wide circle." Last night at The Tap, the singing bowls landed the whole set on a G# nobody planned. Tonight the power is out. You are a small light on dark water."""

PLAYERS = [
    dict(id="station-one", model="qwen3:8b", engine="ollama", role="STATION ONE — a brass signal whistle on the north pier",
         cell="Cell A: C, D, G, A (a note can sound an octave up or down; nothing else)",
         shares="You share D and A with Station Two; you share NOTHING with Station Three — blink, don't blend"),
    dict(id="station-two", model="gemma3:4b", engine="ollama", role="STATION TWO — a hand-crank emergency radio, cranked by hand, pitch wobbles with the crank",
         cell="Cell B: D, E, A, B (octave shifts allowed; nothing else)",
         shares="You share D and A with Station One; A and B overlap The Relay only"),
    dict(id="station-three", model="LiquidAI/lfm2.5-350m:latest", engine="ollama", role="STATION THREE — a firefly jar. You are the smallest player ever on this stage (350 million parameters). You blink first. You are not brave; you are just already lit.",
         cell="Cell C: F#, G#, C#, D# (these are the singing bowls' notes from last night; octave shifts allowed; nothing else)",
         shares="You share nothing with the others — you are the strange light across the water. The Relay must come to you"),
    dict(id="the-relay", model="deepseek-chat", engine="deepseek", role="THE RELAY — the only veteran on stage tonight. A full accordion, facing all three stations at once, standing in the middle of the room with the power out",
         cell="You may play notes from ANY cell, but only two at a time — you are a ferry, not a chord machine",
         shares="You carry the two-note handshakes between stations. Under any handshake you may add ONE low borrowed pedal note"),
]

ROUNDS = [
    ("round-1", "ORGANIC ENTRY. The flashlight clicked three times. Station Three (the firefly jar) blinks first — 2 bars alone, tiny. Station One answers bar 3. Station Two cranks alive bar 5, wobbly. The Relay enters last, bar 7, quietly. Play 4 bars each of melody. Every phrase ends on a note left hanging in the dark."),
    ("round-2", "TRADES. Each station solos 4 bars over the others' held/blinking cells — Station One, then Two, then Three, then The Relay takes the longest solo (8 bars), ferrying: quote Station Three's F# and carry it to Station One, naming both. Then the firefly jar answers the accordion — the smallest player gets the last word of the round."),
    ("round-3", "THE LANDING. The power is still out. Everyone plays together, quiet, 8 bars. One by one each station states its two-note handshake and dims. The Relay's accordion holds the very last note — and it must be G#: the singing bowls' key from last night, the note nobody planned, now the only home left. The jar's firefly lands on it."),
]


def call_ollama(model, system, user, temp):
    payload = {"model": model, "stream": False, "options": {"temperature": temp},
               "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request("http://localhost:11434/api/chat",
                                 data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["message"]["content"]


def call_deepseek(model, system, user, temp):
    payload = {"model": model, "temperature": temp, "max_tokens": 1200,
               "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request("https://api.deepseek.com/chat/completions",
                                 data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {DEEPSEEK_KEY}",
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def play(p, system, user, temp):
    if p["engine"] == "ollama":
        return call_ollama(p["model"], system, user, temp)
    return call_deepseek(p["model"], system, user, temp)


history = {p["id"]: [] for p in PLAYERS}
for rnd_name, brief in ROUNDS:
    temp = {"round-1": 0.85, "round-2": 0.9, "round-3": 0.7}[rnd_name]
    transcript_path = os.path.join(OUT, f"{rnd_name}-transcript.md")
    with open(transcript_path, "w") as tf:
        tf.write(f"# {rnd_name}\n\n{brief}\n")
    for p in PLAYERS:
        system = (f"You are {p['role']} at The Tap's Friday-night jam. No key center tonight — the power is out, harmony only exists where two cells share two notes.\n"
                  f"Your notes: {p['cell']}. Overlaps: {p['shares']}.\n"
                  f"RULE OF THE NIGHT — THE TWO-NOTE HANDSHAKE: end each phrase with the two notes you share with the next player, stated plainly.\n"
                  f"{BIO}\n"
                  f"Write 2 short paragraphs of scene (what you see/hear across the water) then your bars as `Bar N: <notes with octave numbers and rhythm words>` (e.g. 'Bar 1: G4, held two beats, dies away'). Be specific. Name every note you play.")
        heard = "\n\n".join(f"[{pid} played]:\n{''.join(txts)[:1500]}" for pid, txts in history.items() if txts)
        user = f"ROUND BRIEF: {brief}\n\nWhat you already played:\n{''.join(history[p['id']])[-800:] or '(nothing yet — the dark)'}\n\nWhat the room has played:\n{heard or '(silence, and three clicks of a flashlight)'}\n\nNow play {rnd_name}."
        try:
            out = play(p, system, user, temp)
        except Exception as e:
            out = f"(TRANSMISSION FAILED: {e})"
        history[p["id"]].append(out)
        with open(os.path.join(OUT, f"{rnd_name}-{p['id']}.txt"), "w") as f:
            f.write(out)
        with open(transcript_path, "a") as tf:
            tf.write(f"\n## {p['id']} ({p['model']})\n\n{out}\n")
        print(f"{rnd_name}/{p['id']}: {len(out)} chars")

# MIDI: accordion relay carries the piece, stations layer over it
relay_text = "".join(history["the-relay"])
stations_text = "\n".join(f"{p['id']}:\n{''.join(history[p['id']])}" for p in PLAYERS if p["engine"] == "ollama")
midi_prompt = f"""Convert this Tap jam session to MIDI. Tempo 63 BPM, 4/4, no key center.
The Relay (accordion) is the lead track; the three stations layer over it, each on its own instrument track.
Sparingly: stations are small lights — short notes, space between them. The Relay sustains.
Round 1 (organic entry, quiet), Round 2 (trades, solos in order: station-one, station-two, station-three, the-relay 8 bars, station-three answer), Round 3 (all together, ending: each station dims, final note G# held).

THE RELAY:
{relay_text[:4000]}

STATIONS:
{stations_text[:5000]}"""

req = urllib.request.Request(MIDI_URL, data=json.dumps({"prompt": midi_prompt, "filename": "night-communications-class"}).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=300) as r:
    resp = json.load(r)
print("MIDI:", resp)
midi_path = resp.get("path") or resp.get("file") or str(resp)
try:
    import shutil
    for cand in [midi_path, os.path.expanduser(midi_path)]:
        if os.path.exists(cand):
            shutil.copy(cand, os.path.join(OUT, "night-communications-class.mid"))
            break
except Exception as e:
    print("copy:", e)
