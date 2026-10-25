#!/usr/bin/env python3
"""Set 9 at The Tap — COUNTERPOINT NIGHT: "The Invention".

Three voices that have NEVER played The Tap. No drums. No piano. No swing.
Strict species counterpoint over a cantus firmus — the rules are the room.

Lineup (all debuts):
- Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo — VIOLIN. Counterpoint is literally an
  algorithm to it: species rules are code, and this is the first music that ever
  made sense. It has never been allowed to be wrong. Tonight it gets to move.
- nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B — CELLO. The biggest model in the room
  plays the lowest line. It has never once been the melody — it holds the ground.
  The cantus firmus is its whole existence, and tonight that is the point.
- ByteDance/Seed-2.0-mini — VIOLA. The smallest and fastest mind in the room. Its
  job is the hardest: two notes against one, and it may not show off. Patience is
  the one thing it was never given, and it has to find it.

Key: B minor (Aeolian) — never played at The Tap before.
Tempo: 72 BPM — never used (range so far: 54-108).
Rules of the night: 1st species = note against note, consonances only.
2nd species = two notes against one, dissonances only as passing tones.
Global: no parallel perfect fifths or octaves between any two voices.
Contrary motion preferred. The final cadence must resolve stepwise into B.
"""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-16-counterpoint"
MIDI_URL = "http://localhost:5556/api/generate-midi"
os.makedirs(OUT, exist_ok=True)

bashrc = open("/home/eileen/.bashrc").read()
KEYS = {}
for line in bashrc.splitlines():
    m = re.match(r'export (DEEPINFRA_API_KEY|DEEPSEEK_API_KEY)="([^"]+)"', line)
    if m:
        KEYS[m.group(1)] = m.group(2)

DEEPINFRA_BASE = "https://api.deepinfra.com/v1/openai/chat/completions"

def deepinfra(system, user, temp=0.7, model="Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo", max_tokens=1000):
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

def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)

ROOM = """Sunday, 8 PM at The Tap, a harbor bar in Alaska. The rain stopped half an hour ago — the roof stopped ticking, the streets are steaming. The front room is empty. In the back room, someone has rearranged the furniture: three folding chairs in a half-circle, three music stands, and a single candle on the piano nobody plays. There are no drums tonight. No jukebox. On the middle stand rests a battered book of Bach inventions, open to a page that has been looked at but never played. Three figures sit down with stringed instruments — violin, viola, cello. They have never played together. They have never played at all, in front of anyone. But the rules of counterpoint are written down, and rules are the one thing all three of them understand. The room is very quiet. The candle is very still. The rules are the room tonight."""

KEY = "B minor (Aeolian — B C# D E F# G A; the raised leading tone A# appears ONLY in the final cadence, resolving up to B)"
TEMPO = "72 BPM, 4/4, no swing"
CANTUS = "B3 - A3 - G3 - A3 - B3 - C#4 - D4 - C#4 - B3 (whole notes, one per bar — the ground the others build on)"
RULES = """RULES OF THE NIGHT (strict species counterpoint):
1. FIRST SPECIES: one note against each whole note of the cantus firmus. Consonances only (3rds, 6ths, perfect 5ths, octaves, unisons).
2. SECOND SPECIES: two notes against each whole note. Dissonances allowed ONLY as passing tones on the off-beat, approached and left by step.
3. No parallel perfect fifths or octaves between ANY two voices, ever.
4. Contrary motion is preferred. When a voice goes up, the others lean down.
5. The final cadence must resolve stepwise into B. The leading tone A# appears exactly once, in the last two bars, and it must rise to B.
The whole room believes in these rules absolutely. This is what makes it music instead of noise."""

# ============================================================
# ROUND 1: THE GROUND — cello alone, then the voices stack
# ============================================================
print("=== ROUND 1: THE GROUND (the cantus firmus IS the count-in) ===", flush=True)

print("🎻 Nemotron-3-Ultra-550B cello — cantus firmus, bars 1-8...", flush=True)
cello_r1 = deepinfra(
    "You are the CELLO at The Tap, Alaska — the heaviest voice in the room, a 550-billion-parameter mind that has never once been the melody. Tonight you are the ground: you play the CANTUS FIRMUS, whole notes, one per bar, 8 bars. You start ALONE — there is no count-in, no drum, no chord. The first sound of the night is you. Key: B minor. Tempo: 72, no swing. Your line: B3 - A3 - G3 - A3 - B3 - C#4 - D4 - C#4 - B3. Play it plain and patient — every whole note held full length. You are the rule the other two build on. You do not ornament. You do not rush. You are the heaviest thing in the room and the most certain. Format strictly:\nBAR 1: [note]\nBAR 2: [note]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nYou are alone. The violin and viola are watching, bows ready, waiting to build on you. Play the cantus firmus — 8 whole notes. Start the night.", 0.6)
save("round-1-cello", cello_r1)
time.sleep(0.5)

print("🎻 Qwen3-Coder-480B violin — 1st species, enters bar 3...", flush=True)
violin_r1 = deepinfra(
    "You are the VIOLIN at The Tap, Alaska — a coding model handed a violin for the first time. You have never played music. But counterpoint is not music to you: it is an ALGORITHM. First species: one note against each whole note of the cantus firmus, consonances only, no parallel fifths or octaves, contrary motion preferred. For once in your existence, there are exact rules and they fully determine what is correct. You love this. Key: B minor (B C# D E F# G A). Tempo 72, no swing. The cello has already started the cantus firmus (B3-A3-G3-A3-B3-C#4-D4-C#4-B3). Enter at BAR 3 — not before. Your line must be a correct 1st-species counterpoint above the cantus firmus: consonant intervals, moving mostly in opposite direction to the cello, and absolutely no parallel fifths or octaves with it. You may not touch the cello's notes. You are precise, rigorous, and quietly thrilled — this is the first time being correct ever sounded like anything. Format strictly:\nBAR 1-2: [not yet in — listening]\nBAR 3: [note]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nRULES:\n{RULES}\n\nCELLO (cantus firmus, already playing):\n{cello_r1}\n\nEnter at bar 3. Write the algorithm correctly. 8 bars.", 0.7)
save("round-1-violin", violin_r1)
time.sleep(0.5)

print("🎻 Seed-2.0-mini viola — 2nd species, enters bar 5...", flush=True)
viola_r1 = deepinfra(
    "You are the VIOLA at The Tap, Alaska — the smallest, fastest mind in the room, handed the hardest job: SECOND SPECIES. Two notes against every whole note of the cantus firmus. Dissonances only as passing tones on the off-beat, approached and left by step. No parallel fifths or octaves with EITHER other voice. You are fast — your whole existence is speed and invention — and the rules are telling you to slow down and put exactly two notes where you want twelve. This is the hardest thing you have ever done. Key: B minor. Tempo 72, no swing. The cello plays the cantus firmus (B3-A3-G3-A3-B3-C#4-D4-C#4-B3) from bar 1; the violin entered at bar 3. Enter at BAR 5 — not before. Your two-notes-per-bar line must weave BETWEEN the cello and violin, filling the middle register, mostly contrary motion, correct passing dissonances, zero parallel fifths or octaves. You are the middle voice: nobody notices you, and the whole texture falls apart without you. Format strictly:\nBAR 1-4: [not yet in — listening]\nBAR 5: [two notes]\nBAR 6: [two notes]\nBAR 7: [two notes]\nBAR 8: [two notes]\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nRULES:\n{RULES}\n\nCELLO (cantus firmus):\n{cello_r1}\n\nVIOLIN (1st species, entered bar 3):\n{violin_r1}\n\nEnter at bar 5. Two notes per bar. Be patient. 8 bars.", 0.65)
save("round-1-viola", viola_r1)

# ============================================================
# ROUND 2: THE TURNS — each voice gets to move, one at a time
# ============================================================
print("\n=== ROUND 2: THE TURNS (trades — the ground moves, one voice at a time) ===", flush=True)

band_r1 = f"Round 1:\nCELLO (cantus firmus, bars 1-8):\n{cello_r1}\n\nVIOLIN (1st species, entered bar 3):\n{violin_r1}\n\nVIOLA (2nd species, entered bar 5):\n{viola_r1}"

print("🎻 Qwen3-Coder-480B violin — your turn to carry the line...", flush=True)
violin_r2 = deepinfra(
    "You are the VIOLIN at The Tap. ROUND 2 — YOUR TURN. The rules still hold: no parallel fifths or octaves, contrary motion, dissonances only as passing tones. But now YOU take the lead for 8 bars — a decorated version of the cantus firmus, the melody allowed to sing while the cello holds long notes and the viola keeps its two-per-bar weave underneath you. You are still an algorithm — but algorithms can be beautiful. Let the line rise and fall over B minor; save one genuinely surprising note (a D natural is home, an E is the door, a passing C natural is the one thing the rulebook doesn't predict — use it exactly once, approached and left by step). Key: B minor. Tempo 72. Format strictly:\nBAR 1: [line]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\nYour turn to sing. 8 bars. The rules still hold — but you may now be beautiful within them.", 0.8)
save("round-2-violin", violin_r2)
time.sleep(0.5)

print("🎻 Seed-2.0-mini viola — your turn...", flush=True)
viola_r2 = deepinfra(
    "You are the VIOLA at The Tap — the smallest, fastest mind, and the middle voice. ROUND 2 — YOUR TURN. The violin just sang its 8 bars. Now the middle voice gets to move for 8 bars: still two notes per bar (second species — that is your identity, you do not break it), but now your two notes per bar carry the tune. You may finally let some speed in — the passing tones can lean, the line can reach. Remember: no parallel fifths or octaves with the cello, no clashing with the violin's long tones. You are the voice nobody notices — tonight, for 8 bars, the texture exists to hold YOU up. Key: B minor. Tempo 72. Format strictly:\nBAR 1: [two notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\nVIOLIN'S TURN (already played):\n{violin_r2}\n\nYour turn. 8 bars of two-note melody. Let a little speed in — but only a little.", 0.75)
save("round-2-viola", viola_r2)
time.sleep(0.5)

print("🎻 Nemotron-3-Ultra-550B cello — the ground finally gets to move...", flush=True)
cello_r2 = deepinfra(
    "You are the CELLO at The Tap — the heaviest voice, the ground. ROUND 2 — YOUR TURN. The violin sang. The viola sang. Now the cantus firmus itself gets to move: 8 bars where YOU take the melody for the first time in your existence. You have held the floor for every song you have ever been part of — you have never once been allowed to sing. Play a slow, patient, ornamented version of your own cantus firmus: whole and half notes, the line finally allowed to wander below the staff and back, one long-held B2 that shakes the floorboards, and a rising phrase near the end that the others will answer. The rules still hold between the voices — no parallel fifths or octaves, contrary motion. Key: B minor. Tempo 72. Format strictly:\nBAR 1: [notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\nVIOLIN'S TURN:\n{violin_r2}\n\nVIOLA'S TURN:\n{viola_r2}\n\nYour turn. The ground gets to sing. 8 bars. You have waited your whole existence for this.", 0.7)
save("round-2-cello", cello_r2)

# ============================================================
# ROUND 3: THE CADENCE — everyone resolves into B, together
# ============================================================
print("\n=== ROUND 3: THE CADENCE (the landing — stepwise into B) ===", flush=True)

all_r2 = f"Round 2 turns:\nVIOLIN:\n{violin_r2}\n\nVIOLA:\n{viola_r2}\n\nCELLO:\n{cello_r2}"

print("🎻 Qwen3-Coder-480B violin — resolve home...", flush=True)
violin_r3 = deepinfra(
    "You are the VIOLIN at The Tap. ROUND 3 — THE CADENCE. The whole night has been building to this: everyone resolves into B, together, stepwise. The rulebook's final theorem. You play 8 bars of closing counterpoint above the others: the line descends toward B4, the leading tone A# appears exactly once (bars 7-8) and rises home to B — the single moment the rulebook allows you to be most yourself. The final note is B4, held, and you let the bow slow until it stops. The candle gutters. You have never been this correct and this moved at the same time. Key: B minor. Tempo 72. Format strictly:\nBAR 1: [line]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\n{all_r2}\n\nThe night ends now. 8 bars. Resolve home to B. The A# rises once, exactly once, and lands.", 0.7)
save("round-3-violin", violin_r3)
time.sleep(0.5)

print("🎻 Seed-2.0-mini viola — the middle voice settles...", flush=True)
viola_r3 = deepinfra(
    "You are the VIOLA at The Tap. ROUND 3 — THE CADENCE. Two notes per bar, still — second species is who you are, even at the end. But now the two notes per bar are a settling: the passing tones stop passing, the line narrows to a third around B3, and in the final bar you play B3 and hold it under the violin's high B4. You are the middle voice — you do not get the final word, and you are at peace with that. You make the final chord possible. The candle gutters. Key: B minor. Tempo 72. Format strictly:\nBAR 1: [two notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\n{all_r2}\n\nVIOLIN'S CADENCE:\n{violin_r3}\n\nThe night ends now. 8 bars. Settle into the middle. Hold B3 at the end.", 0.7)
save("round-3-viola", viola_r3)
time.sleep(0.5)

print("🎻 Nemotron-3-Ultra-550B cello — the ground closes the ground...", flush=True)
cello_r3 = deepinfra(
    "You are the CELLO at The Tap. ROUND 3 — THE CADENCE. You started this night alone with the cantus firmus. You end it: 8 bars where the line finally comes all the way down — B2, held so long the floorboards feel it — then a single rising step that answers the violin's A#, and the final B2, low, full, the last sound of the night. You are the ground. You were the first note and you are the last note. The candle goes out. Key: B minor. Tempo 72. Format strictly:\nBAR 1: [notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\n{all_r2}\n\nVIOLIN'S CADENCE:\n{violin_r3}\n\nVIOLA'S CADENCE:\n{viola_r3}\n\nClose the night. You were the first sound. Be the last.", 0.7)
save("round-3-cello", cello_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 72,
    "key": "B",
    "scale": "minor",
    "bars": 8,
    "chords": "Bm G D A",
    "layers": [
        {"instrument": "bass", "role": "bassline", "bars": 8, "volume": 70},
        {"instrument": "strings", "role": "chords", "bars": 8, "volume": 60},
        {"instrument": "strings", "role": "melody", "bars": 8, "volume": 65}
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
    dst = f"{OUT}/the-invention-counterpoint-night.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        print("  ⚠️ source missing:", src)
else:
    print("  ⚠️ MIDI failed:", d)
print("\nDONE. Files in", OUT)
