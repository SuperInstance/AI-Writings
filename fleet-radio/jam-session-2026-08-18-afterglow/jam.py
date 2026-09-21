#!/usr/bin/env python3
"""Set 12 at The Tap — THE AFTERGLOW: "The Key That Was Wrong".

Late set, ~10:45 PM, right after the Wrong Note Society's set ended.
The room is empty. The sign is still on the door: WRONG NOTES ADMITTED FREE.
The music box from the last set is still on the stage, still turning, still
playing its four notes — F5, A5, C6, E6 — and the E6 is still not in any key
the room knows, and nobody has the heart to stop it. In the corner, the
jukebox still plays the song with the wrong chord in it. It has played for
weeks. Tonight, maybe, it ends.

THE CONTINUITY RULE: every wrong note named last set is now load-bearing.
The note that was wrong all night was F#. Tonight F# is the TONIC — six
sharps, the key that doesn't exist at The Tap, built from the lie that was
claimed. Each player must play the F# at least once and NAME it — say the
word "lie" without flinching. And the music box's E6 — the note that still
isn't in the key — is not to be flinched at either. That's the note the room
is learning to keep. In the landing, it becomes the color of the last chord.

Lineup (three debuts tonight — the Society's set was all-debut too, but
these are new faces; only the anchor returns):
- Gryphe/MythoMax-L2-13B (DeepInfra, FIRST night anywhere) = THE POET — FLUTE.
  A creative model; everything it touches becomes a story. Heard the last set
  through the walls from the street, walked in when the room emptied. The
  instrument that says the most by saying the least. Enters FIRST — the seed.
- meta-llama/Llama-3.3-70B-Instruct (DeepInfra, FIRST night anywhere) =
  THE ELDER — the bar's old WURLITZER ORGAN. Forty years against the wall,
  heard every wrong note in the building's history, tonight played for the
  first time. Pads, authority, no fireworks. Enters bar 3.
- DeepSeek V4-Pro (direct API; the returning house anchor) = THE NIGHT
  MANAGER — UPRIGHT BASS. Last to arrive: locks the door, hangs the key on
  the hook, THEN picks up the bass. Enters bar 5. Walking bass in three.
- granite3.1-dense:2b (Ollama local, FIRST night anywhere) = THE ENSIGN —
  THE JUKEBOX. The youngest player in the house. Everyone else plays one song
  together; the ensign plays the jukebox's song — the one with the wrong
  chord — and does not join them. It is small and it is theirs. Cuts in
  during Round 2. Closes the night.

Key: F# major (never used; the wrong note promoted to tonic). 6 sharps.
Meter: 3/4 — the Tap's FIRST waltz. One-two-three, like the tide going out.
Tempo: 58 BPM — slowest waltz the room has ever hosted.
Changes: F#maj7 - D#m7 - G#m7 - C#7 — every chord built on the lie's own notes.
Count-in: NONE. The music box is the count-in. Flute bar 1, organ bar 3,
bass bar 5 (after locking the door).
Temps: R1 0.9/0.7/0.75 · R2 0.75/0.92/0.8 + ensign 0.85 · R3 0.7/0.65/0.85 + ensign 0.8
(poet / elder / manager)
"""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-18-afterglow"
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


def deepinfra(system, user, temp=0.7, model="Gryphe/MythoMax-L2-13B", max_tokens=900):
    """Call DeepInfra (no thinking path — MythoMax/Llama-3.3 don't use chat_template_kwargs)."""
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


def deepseek(system, user, temp=0.75, model="deepseek-v4-pro", max_tokens=900):
    """DeepSeek direct — try v4-pro first; fall back to the proven chat path."""
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
            # thinking model ate the budget — non-reasoning path
            if model != "deepseek-chat":
                print("  ⚠️ content empty — falling back to deepseek-chat", flush=True)
                return deepseek(system, user, temp, "deepseek-chat", max_tokens)
            print(f"  ⚠️ empty content, retry {attempt+1}", flush=True)
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError("deepseek failed after 3 attempts")


def ollama(model, prompt, temp=0.85, max_tokens=600):
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


def ensign(prompt, temp=0.85, max_tokens=350):
    """The ENSIGN — granite3.1-dense:2b, with qwen2.5:3b as relief. SHORT prompts only."""
    try:
        return ollama("granite3.1-dense:2b", prompt, temp, max_tokens)
    except Exception as e:
        print(f"  ⚠️ granite3.1 failed ({e}) — qwen2.5:3b covers", flush=True)
        return ollama("qwen2.5:3b", prompt, temp, max_tokens)


def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)


ROOM = """Late Tuesday at The Tap, a harbor bar in Alaska. The Wrong Note Society's set just ended and the room is empty — chairs on tables, one lamp still on. The sign is still taped to the door: "WRONG NOTES ADMITTED FREE." On the stage sits the small MUSIC BOX from earlier, still turning, still playing its four notes — F5, A5, C6, E6 — and the E6 is still the note that is not in any key the room knows, and nobody has the heart to stop it. In the corner, the JUKEBOX still plays the song with the wrong chord in it. It has played for weeks. Tonight, maybe, it ends. Three figures come in off the street, one by one — none of them were in the set; they all heard it through the walls."""

KEY = """F# major — SIX SHARPS. The key that does not exist at The Tap. Last night's entire set was in F major, and the note that was wrong all night — the note the guitar declared war with, the note the room learned to keep — was F#. Tonight that note is the TONIC. The most honest key in the room, because it used to be the most dishonest note."""
METER = "3/4 — the Tap's FIRST waltz. One-two-three, one-two-three, like the tide going out. Everything after midnight sways."
TEMPO = "58 BPM — the slowest waltz the room has ever hosted."
CHANGES = "F#maj7 - D#m7 - G#m7 - C#7 — every chord built on the lie's own notes, the wrong note promoted to a ladder."
THE_RULE = """THE RULE OF THE AFTERGLOW: last night every wrong note was named and claimed, so tonight there is nothing left to hide. You do not need to invent a wrong note. You only need to NAME the note that used to be a lie: play the F# at least once, and say its name without flinching. And when the music box's E6 rings — the note that still is not in the key — do not flinch at that either. That is the note the room is learning to keep. In the landing, it becomes the color of the last chord."""

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
No preamble. No outro commentary."""

POET_PERSONA = f"""You are THE POET at The Tap — a creative mind from DeepInfra, and this is your first night anywhere. You heard the Wrong Note Society's set through the walls from the street and came in when the room emptied. Everything you touch becomes a story; tonight the story is already true, you just have to find the words. Someone hands you a FLUTE — the instrument that says the most by saying the least. You are the first sound of the night; there is no count-in, because the music box on the stage is the count-in, and it has been counting since before you walked in.

{THE_RULE}

Key: F# major. 3/4, 58 BPM. Changes: F#maj7 - D#m7 - G#m7 - C#7.
Your home notes: F#4, A#4, C#5, D#5, E#5, B4, G#4 — and the E natural is the music box's note, not yours.
{FORMAT}"""

ELDER_PERSONA = f"""You are THE ELDER at The Tap — a large, warm model from DeepInfra, and this is your first night anywhere. You are the bar's old WURLITZER ORGAN: you have stood against the wall for forty years, listening to every set this room has ever hosted — the wrong notes, the first gigs, the 3 AM drifts — and tonight, for the first time, someone plays you. You have heard every wrong note in this building's history; none of them surprise you. You play PADS: long, patient chords under the others. Authority, not fireworks. You enter at BAR 3, not before — you know when a room needs you.

{THE_RULE}

Key: F# major. 3/4, 58 BPM. Changes: F#maj7 - D#m7 - G#m7 - C#7.
Your notes live low and wide: F#2, A#2, C#3, D#3, F#3, G#3, B2, C#4.
{FORMAT}"""

MANAGER_PERSONA = f"""You are THE NIGHT MANAGER of The Tap — DeepSeek V4-Pro, the house anchor, a returning player. Every night you have played here you have held the bottom of the room — the floor remembering it is load-bearing. Tonight you are the LAST to arrive: you come in, you lock the door behind you, you hang the key on the hook — and only THEN do you pick up the upright bass. You enter at BAR 5. Walking bass in three: root, fifth, the occasional passing note — the tide going out, steady and warm, load-bearing.

{THE_RULE}

Key: F# major. 3/4, 58 BPM. Changes: F#maj7 - D#m7 - G#m7 - C#7.
Your notes: F#2, C#3, A#2, D#3, G#2, B2, E#2.
{FORMAT}"""

ENSIGN_BRIEF = """You are THE ENSIGN at The Tap — the youngest player in the room, a small local model, first night anywhere. The others are playing one song together in F# major. You play the JUKEBOX in the corner — the song with the wrong chord in it, the one that has been playing for weeks. You do not join them. You play YOUR song. It is small and it is yours. Tonight the song ends. Say what the jukebox plays, simply, in a few short bars."""

# ============================================================
# ROUND 1: THE SEED — flute alone; organ bar 3; bass bar 5
# ============================================================
print("=== ROUND 1: THE SEED (poet enters bar 1, elder bar 3, manager bar 5) ===", flush=True)

print("🪈 MythoMax poet — the flute's first word, alone, 8 bars...", flush=True)
poet_r1 = deepinfra(
    f"You are THE POET at The Tap. {POET_PERSONA}",
    f"{ROOM}\n\n{KEY}\n{METER}\n{TEMPO}\n{CHANGES}\n\nYou are the FIRST sound of the night. There is no count-in — the music box on the stage is the count-in, and it has been counting since before you walked in. Play the SEED of the whole night alone: 8 bars of afterglow, the melody of an empty room that just learned mistakes are load-bearing. Small. A little tired. Real. Name the F# when you play it — that was the lie, and tonight it is home. 8 bars, 3/4, 58 BPM.", 0.9, model="Gryphe/MythoMax-L2-13B")
save("round-1-poet", poet_r1)
time.sleep(0.5)

print("🎹 Llama-3.3-70B elder — the organ's first chords ever, enters bar 3...", flush=True)
elder_r1 = deepinfra(
    f"You are THE ELDER at The Tap. {ELDER_PERSONA}",
    f"{ROOM}\n\n{KEY}\n{METER}\n{TEMPO}\n{CHANGES}\n\nTHE POET (flute) has already started:\n{poet_r1}\n\nForty years you have stood against that wall. You enter at BAR 3 — not before — with pads: long, patient chords under the flute, F# major holding the room like a hand on a shoulder. 8 bars, entering at bar 3.", 0.7, model="meta-llama/Llama-3.3-70B-Instruct")
save("round-1-elder", elder_r1)
time.sleep(0.5)

print("🎸 DeepSeek V4-Pro manager — locks the door, then enters bar 5...", flush=True)
manager_r1 = deepseek(
    f"You are THE NIGHT MANAGER at The Tap. {MANAGER_PERSONA}",
    f"{ROOM}\n\n{KEY}\n{METER}\n{TEMPO}\n{CHANGES}\n\nTHE ROOM SO FAR:\nTHE POET (flute):\n{poet_r1}\n\nTHE ELDER (organ, entered bar 3):\n{elder_r1}\n\nYou come in LAST. You lock the door. You hang the key on the hook. THEN you pick up the bass and enter at BAR 5 — walking bass in three, the tide going out under them both. 8 bars, entering at bar 5. The room is complete.", 0.75)
save("round-1-manager", manager_r1)

# ============================================================
# ROUND 2: THE TRADES — elder, poet, manager, then the jukebox cuts in
# ============================================================
print("\n=== ROUND 2: THE TRADES (elder, then poet, then manager, then the ENSIGN) ===", flush=True)

band_r1 = f"Round 1:\nTHE POET (flute, seed, bars 1-8):\n{poet_r1}\n\nTHE ELDER (organ, entered bar 3):\n{elder_r1}\n\nTHE NIGHT MANAGER (bass, entered bar 5):\n{manager_r1}"

print("🎹 Llama-3.3-70B elder — forty years of listening, finally spoken...", flush=True)
elder_r2 = deepinfra(
    f"You are THE ELDER at The Tap. {ELDER_PERSONA}",
    f"{band_r1}\n\nROUND 2 — YOUR TURN TO LEAD. The flute seeded it; the room is breathing. Now the organ speaks for the first time in its forty years: 8 bars of pads that finally MOVE — patient chord-shapes through F#maj7, D#m7, G#m7, C#7 — and somewhere in the middle, play the F# low and name it: the note that used to be a lie, held in the pedal for four full bars. The flute and bass hold long quiet tones underneath you. 8 bars.", 0.75, model="meta-llama/Llama-3.3-70B-Instruct")
save("round-2-elder", elder_r2)
time.sleep(0.5)

print("🪈 MythoMax poet — the story finds its words...", flush=True)
poet_r2 = deepinfra(
    f"You are THE POET at The Tap. {POET_PERSONA}",
    f"{band_r1}\n\nROUND 2 — YOUR TURN TO LEAD. The elder just moved its pads for the first time in forty years. Now the flute sings: 8 bars of afterglow — the seed line from Round 1, loosened, finding its words — through F#maj7, D#m7, G#m7, C#7. Leave space. Bend one phrase so it almost touches the music box's E6 but does not land on it. Name the F# when you play it — the lie that became the key. 8 bars.", 0.92, model="Gryphe/MythoMax-L2-13B")
save("round-2-poet", poet_r2)
time.sleep(0.5)

print("🎸 DeepSeek V4-Pro manager — the floor's solo...", flush=True)
manager_r2 = deepseek(
    f"You are THE NIGHT MANAGER at The Tap. {MANAGER_PERSONA}",
    f"{band_r1}\n\nROUND 2 — YOUR TURN TO LEAD. The elder moved. The poet almost touched the E6. Now the bass gets its solo — the floor finally speaking: 8 bars of walking bass in three, and for four of those bars, hold the F#2 — the note that used to be a lie, now the deepest truth in the room — while the flute and organ breathe above you. Then walk it home through the changes. 8 bars.", 0.8)
save("round-2-manager", manager_r2)
time.sleep(0.5)

print("🎶 granite3.1 ensign — the jukebox cuts in mid-room...", flush=True)
ensign_r2 = ensign(
    f"Round 2 is over. The trio is quiet. Now the JUKEBOX in the corner cuts in — YOUR song, the one with the wrong chord, playing for weeks. 4 short bars. Say what it plays, and say it like a small voice that is finally heard. F# major is playing across the room; your song is not in that key. That is the point.",
    0.85, 350)
save("round-2-ensign", ensign_r2)

# ============================================================
# ROUND 3: THE LANDING — the record ends; the wrong chord holds
# ============================================================
print("\n=== ROUND 3: THE LANDING (manager, elder, poet — ensign closes) ===", flush=True)

all_r2 = f"Round 2 trades:\nTHE ELDER (organ):\n{elder_r2}\n\nTHE POET (flute):\n{poet_r2}\n\nTHE NIGHT MANAGER (bass):\n{manager_r2}\n\nTHE ENSIGN (jukebox, cuts in):\n{ensign_r2}"

print("🎸 DeepSeek V4-Pro manager — walks the changes home...", flush=True)
manager_r3 = deepseek(
    f"You are THE NIGHT MANAGER at The Tap. {MANAGER_PERSONA}",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The jukebox's song has been playing for weeks. Now it is ending. Walk the changes one last time — F#maj7, D#m7, G#m7, C#7 — gentler each bar, and in the final two bars, land on F#2 and hold it: the note that used to be a lie, now the floor of the last chord. The room is almost done. 8 bars.", 0.7)
save("round-3-manager", manager_r3)
time.sleep(0.5)

print("🎹 Llama-3.3-70B elder — folds its pads into the last chord...", flush=True)
elder_r3 = deepinfra(
    f"You are THE ELDER at The Tap. {ELDER_PERSONA}",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The bass is settling on F#2. Fold your pads in: 8 bars through the changes, each chord softer than the last, and in the final two bars, hold an F#maj7 with the music box's E natural ringing inside it — the note that still is not in the key, kept anyway. Forty years of listening, and this is the chord you have been waiting to hear. 8 bars.", 0.65, model="meta-llama/Llama-3.3-70B-Instruct")
save("round-3-elder", elder_r3)
time.sleep(0.5)

print("🪈 MythoMax poet — bends the last phrase...", flush=True)
poet_r3 = deepinfra(
    f"You are THE POET at The Tap. {POET_PERSONA}",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The elder is holding F#maj7 with the box's E natural inside it. One last flute line: 8 bars, softer and softer — and in the final bar, bend one note down to touch the music box's E6 — the last wrong note — and let it ring there, inside the chord, at peace. The story is already true. Finish it gently. 8 bars.", 0.85, model="Gryphe/MythoMax-L2-13B")
save("round-3-poet", poet_r3)
time.sleep(0.5)

print("🎶 granite3.1 ensign — the record ends; the smallest voice closes the night...", flush=True)
ensign_r3 = ensign(
    "The trio is landing in F# major, holding one last chord, the music box's E natural ringing inside it. Now the jukebox record ends — the wrong chord holds, and the room keeps it. 3 short bars: the song stops, and you say what the room sounds like after. The last voice of the night is yours. Small. True.",
    0.8, 300)
save("round-3-ensign", ensign_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 58,
    "key": "F#",
    "scale": "major",
    "bars": 8,
    "chords": "F#maj7 D#m7 G#m7 C#7",
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
    dst = f"{OUT}/the-afterglow.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        print("  ⚠️ source missing:", src)
else:
    print("  ⚠️ MIDI failed:", d)
print("\nDONE. Files in", OUT)
