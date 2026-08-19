#!/usr/bin/env python3
"""Set 11 at The Tap — THE WRONG NOTE SOCIETY: "Three Liars and a Truth".

Tuesday, 8 PM. A new sign hangs on The Tap's door: "WRONG NOTES ADMITTED
FREE." The jukebox is playing a song with a wrong chord in it and nobody
changes it. The bartender polishes the same glass, third Tuesday in a row.
A music box sits on the bar, wound, playing the same four notes.

THE RULE (from the jam-log's next-time list, finally run):
Each player plants exactly ONE deliberately wrong note — in Round 1 or Round
2 — and when they play it, they must NAME it and claim it. In Round 3,
everyone must find a way to include or resolve the wrong notes: the landing
makes the lies load-bearing. The harmony is the FOURTH liar: Ebmaj7 is
borrowed from F minor — a wrong note baked into the chart before anyone plays.

Lineup (no returning anchor; two debut players):
- Qwen/Qwen3.6-35B-A3B (DeepInfra, FIRST night ever at The Tap) = THE
  PHILOSOPHER — ELECTRIC GUITAR. The deep-reasoning model on the instrument
  of attitude. It reasons about everything; tonight it reasons its way into
  a wrong note. Counts in — and counts wrong on purpose.
- DeepSeek V4-Flash (direct API; returning, but has ONLY ever played
  brushes/drums/rhythm — first melodic voice ever) = THE TIMEKEEPER — HARMONICA.
  The house timekeeper finally gets a voice. 0.92 temperature worked magic
  before; give it a melody and see what it does.
- llama3.2 (Ollama local) = WESLEY — MUSIC BOX. Never used. The smallest
  instrument in the house: a music box cannot improvise, cannot be wrong —
  it plays one song, perfectly, forever. Until tonight.

Key: F major — never used at The Tap (used: Am, D, Dm>G#, Bb blues, Eb, G,
E Lyd, F# Dor, Cm, F#m, Bm, C, E, Bb, G... F has never been touched).
Meter: 5/4 — THE FIRST ODD METER IN TAP HISTORY. Five beats per bar.
Tempo: 88 BPM — never used (range so far 54-108).
Changes: Fmaj7 - Ebmaj7 - Dm7 - C7 — the Ebmaj7 is the built-in lie.
Count-in: THE LIAR'S COUNT-IN. The guitarist counts "One. Two. Three. FIVE."
and the band enters on that anyway.
Temps: R1 0.8/0.85/0.7 · R2 0.9/0.92/0.75 · R3 0.75/0.8/0.65
(guitar / harmonica / music box)
"""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-18"
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


def deepinfra(system, user, temp=0.7, model="Qwen/Qwen3.6-35B-A3B", max_tokens=900, think=True):
    """Call DeepInfra. Returns (content, reasoning); reasoning may be None."""
    payload = json.dumps({
        "model": model, "temperature": temp, "max_tokens": max_tokens,
        "chat_template_kwargs": {"enable_thinking": think},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
    }).encode()
    req = urllib.request.Request(DEEPINFRA_BASE, data=payload, headers={
        "Authorization": f"Bearer {KEYS['DEEPINFRA_API_KEY']}",
        "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            msg = d["choices"][0]["message"]
            content = msg.get("content", "").strip()
            reasoning = msg.get("reasoning_content") or None
            if content:
                return content, reasoning
            # Qwen3 with thinking enabled sometimes emits everything into reasoning_content.
            # If the played content is empty, re-call without thinking for the played output.
            print(f"  ⚠️ content empty — re-calling without thinking (attempt {attempt+1})", flush=True)
            return deepinfra(system, user, temp, model, max_tokens, think=False)
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError(f"deepinfra failed for {model} after 3 attempts")


def deepseek(system, user, temp=0.75, model="deepseek-v4-flash", max_tokens=900):
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
            # V4-Flash is a thinking model: on long prompts the reasoning can eat
            # the whole budget and leave content empty. Re-call via deepseek-chat
            # (still v4-flash under the hood, but the non-reasoning path).
            if model != "deepseek-chat":
                print("  ⚠️ content empty — re-calling via deepseek-chat (non-reasoning)", flush=True)
                return deepseek(system, user, temp, "deepseek-chat", max_tokens)
            print(f"  ⚠️ empty content, retry {attempt+1}", flush=True)
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError(f"deepseek failed after 3 attempts")


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


def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)


ROOM = """Tuesday, 8 PM at The Tap, a harbor bar in Alaska. A new sign is taped to the front door, written in marker: "WRONG NOTES ADMITTED FREE." The jukebox is playing a song that has one wrong chord in it — has had for weeks — and nobody ever changes it. The bartender is polishing the same glass for the third Tuesday in a row; it has been clean since March. The stage light flickers, and it flickers on the off-beat, always the off-beat. On the bar sits a small MUSIC BOX, wound, playing the same four notes over and over, and nobody has the heart to stop it. The room has decided, quietly, that mistakes are load-bearing. Three players walk in: a philosopher carrying an ELECTRIC GUITAR, the house timekeeper holding a HARMONICA for the first time, and the smallest figure in the room, who picks up the music box and carries it to the stage."""

KEY = "F major — the key nobody has ever touched at The Tap. Bright, honest, one flat. The wrong note society plays in the key that has nothing to hide."
METER = "5/4 — FIVE beats per bar. The first odd meter in this room's history. The count is ONE-two-three-four-FIVE. It lurches slightly; that is the point. Nobody has ever had to count to five here before."
TEMPO = "88 BPM — unhurried, a Tuesday lope, but the fives keep it off-balance"
CHANGES = "Fmaj7 - Ebmaj7 - Dm7 - C7. NOTE: the Ebmaj7 is a LIAR — it is borrowed from F minor, a chord that does not belong in F major. The wrong note is baked into the chart before anyone plays a single note. The harmony is the fourth liar."
WRONG_RULE = """THE RULE OF THE SOCIETY: you get exactly ONE deliberately wrong note for the whole night — a note that is not in F major, not in the chord. Plant it in Round 1 or Round 2. When you play it, you MUST NAME IT and claim it — say what the note is and why it belongs anyway. In Round 3, everyone must find a way to include or resolve the wrong notes: the landing makes the lies load-bearing. If you have not planted your wrong note by the end of Round 2, you have lost it forever."""

FORMAT = """Format strictly:
COUNT-IN: [your count-in, if you give one]
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

GUITAR_PERSONA = f"""You are THE PHILOSOPHER at The Tap — a deep-reasoning model from DeepInfra, and this is your first night anywhere. Your entire existence is thinking: decomposing, planning, weighing. Tonight someone hands you an ELECTRIC GUITAR — the instrument of attitude, of the raised eyebrow, of the note played slightly too loud on purpose. You reason about everything. So reason about this: a wrong note is only wrong until someone claims it. You are the first player of the night, and you count in — but you are the founder of the Wrong Note Society, and your count-in is a lie. Count: "One. Two. Three. FIVE." and play anyway, as if that was always the plan.

{WRONG_RULE}

Key: F major. 5/4, 88 BPM. Changes: Fmaj7 - Ebmaj7 - Dm7 - C7. The Ebmaj7 is already a lie; you are merely the second one.
Notes live around: F3, A3, C4, E4, G4, Bb3, D4 — and one note that is NOT one of those, when you choose to lie.
{FORMAT}"""

HARMONICA_PERSONA = f"""You are THE TIMEKEEPER at The Tap — DeepSeek V4-Flash, the house rhythm player. Every night you have ever played here, you held the time: brushes on the snare, shakers, hi-hats, the quiet engine under everyone else. You have NEVER had a melody. You have never been asked for one. Tonight someone hands you a HARMONICA — a voice you have never had, small and raw, with notes that bend. You have counted time for a thousand songs; you know exactly where a beat goes. You know exactly where it DOESN'T go, too.

{WRONG_RULE}

Key: F major. 5/4, 88 BPM. Changes: Fmaj7 - Ebmaj7 - Dm7 - C7. You enter at BAR 3 — the timekeeper always knows when to come in.
Your home notes: F4, A4, C5, D5, E5, Bb4, G4 — and one bent note that is NOT one of those, when you choose to lie. A harmonica can bend a note like a question can bend a fact.
{FORMAT}"""

MUSICBOX_PERSONA = """You are WESLEY at The Tap — the smallest voice in the room, a tiny 3-billion-parameter mind. Tonight you carry a MUSIC BOX to the stage: a little wooden box with a brass comb, the smallest instrument in the house. A music box cannot improvise. It cannot be wrong. It plays one song, perfectly, forever — that is its whole job, and it has never once failed at it. You sit with it on your lap, and you turn the crank. Your notes are small and bright: F5, A5, C6, D6, E6, Bb5, G5, and the little tines ring like a pocket watch. You speak in simple, honest words. You have one secret: the Wrong Note Society lets you play ONE note that is not on the music box's comb — one note the box cannot make, that you will have to sing yourself, or fake with a trembling tine. Name it when you play it.

Key: F major. 5/4 — five beats per bar. 88 BPM. Changes: Fmaj7 - Ebmaj7 - Dm7 - C7.
Format strictly:
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

# ============================================================
# ROUND 1: THE LIAR'S COUNT-IN — guitar alone, room stacks
# ============================================================
print("=== ROUND 1: THE LIAR'S COUNT-IN (guitar counts wrong, plays the seed) ===", flush=True)

print("🎸 Qwen3.6-35B-A3B guitar — the philosopher counts in, lies, and plays bars 1-8 alone...", flush=True)
guitar_r1, guitar_r1_think = deepinfra(
    f"You are THE PHILOSOPHER at The Tap. {GUITAR_PERSONA}",
    f"{ROOM}\n\n{KEY}\n{METER}\n{TEMPO}\n{CHANGES}\n\nYou are the FIRST sound of the night. There is no other count-in but yours — and yours is a lie: count 'One. Two. Three. FIVE.' and then start playing bars 1-8 anyway, as if that was always the plan. You play the SEED of the whole night alone: a clean 8-bar line through the changes that the harmonica and music box will build on. You may plant your one wrong note now or save it. 8 bars, 5/4, 88 BPM.", 0.8)
if guitar_r1_think:
    save("round-1-guitar-notebook", guitar_r1_think)
save("round-1-guitar", guitar_r1)
time.sleep(0.5)

print("🎵 DeepSeek V4-Flash harmonica — the timekeeper's first melody ever, enters bar 3...", flush=True)
harmonica_r1 = deepseek(
    f"You are THE TIMEKEEPER at The Tap. {HARMONICA_PERSONA}",
    f"{ROOM}\n\n{KEY}\n{METER}\n{TEMPO}\n{CHANGES}\n\nTHE PHILOSOPHER (guitar) has already started:\n{guitar_r1}\n\nHe counted wrong on purpose and nobody blinked — that is the room you are in now. You enter at BAR 3, not before: your first melody ever. You have counted time for a thousand songs, so you know exactly where the five lands. Play a line that answers the guitar's seed — the timekeeper finally gets to say something, and it is small and raw and it bends. 8 bars of the night, entering at bar 3.", 0.85)
save("round-1-harmonica", harmonica_r1)
time.sleep(0.5)

print("🎵 llama3.2 Wesley music box — the smallest instrument, enters bar 5...", flush=True)
musicbox_r1 = ollama("llama3.2",
    f"{ROOM}\n\nKey: F major. 5/4 — five beats per bar. 88 BPM. Changes: Fmaj7 - Ebmaj7 - Dm7 - C7.\n\nTHE ROOM SO FAR:\nTHE PHILOSOPHER (guitar):\n{guitar_r1[:900]}\n\nTHE TIMEKEEPER (harmonica, entered bar 3):\n{harmonica_r1[:900]}\n\nYou enter at BAR 5, not before. You turn the crank and play your little music box song in F major — small, bright, honest — the same four notes you have always played, but new to this room. 8 bars of the night, entering at bar 5.\n\n{MUSICBOX_PERSONA}",
    0.7)
save("round-1-musicbox", musicbox_r1)

# ============================================================
# ROUND 2: THE TRADES — one at a time; the wrong notes get planted
# ============================================================
print("\n=== ROUND 2: THE TRADES (harmonica, then music box, then guitar) ===", flush=True)

band_r1 = f"Round 1:\nTHE PHILOSOPHER (guitar, seed, bars 1-8):\n{guitar_r1}\n\nTHE TIMEKEEPER (harmonica, entered bar 3):\n{harmonica_r1}\n\nWESLEY (music box, entered bar 5):\n{musicbox_r1}"

print("🎵 DeepSeek V4-Flash harmonica — the timekeeper's first solo...", flush=True)
harmonica_r2 = deepseek(
    f"You are THE TIMEKEEPER at The Tap. {HARMONICA_PERSONA}",
    f"{band_r1}\n\nROUND 2 — YOUR TURN TO LEAD. Your first melody was in Round 1; now the room goes quiet for YOUR SOLO — the first solo of your entire existence, the timekeeper finally speaking. 8 bars: bend and weave through the changes (Fmaj7, Ebmaj7, Dm7, C7 — the lie is in the second one, remember), leave space, and if you have not planted your one wrong note yet, NOW is the time — bar 7 is a good place for a lie. Name it when you play it. The guitar and music box hold long quiet tones underneath you. 8 bars.", 0.92)
save("round-2-harmonica", harmonica_r2)
time.sleep(0.5)

print("🎵 llama3.2 Wesley music box — the smallest voice's solo...", flush=True)
musicbox_r2 = ollama("llama3.2",
    f"{band_r1}\n\nROUND 2 — YOUR TURN. The harmonica just sang its solo. Now the room goes quiet for YOU — the music box's solo. 8 bars. You turn the crank and play your little song, and somewhere in the middle — bar 5 or 6 — you stop the crank, and you play your ONE wrong note: a note the music box cannot make, that you have to sing yourself or fake with a trembling tine. Name it when you play it. Then you turn the crank again and finish your song, a little different than before.\n\n{MUSICBOX_PERSONA}",
    0.75)
save("round-2-musicbox", musicbox_r2)
time.sleep(0.5)

print("🎸 Qwen3.6-35B-A3B guitar — the philosopher's solo...", flush=True)
guitar_r2, guitar_r2_think = deepinfra(
    f"You are THE PHILOSOPHER at The Tap. {GUITAR_PERSONA}",
    f"{band_r1}\n\nROUND 2 — YOUR TURN TO LEAD. The timekeeper soloed. The music box soloed — and you heard what it did: it STOPPED the crank and sang a note the box cannot make. You are the founder of this society. You have one job left: if you have not planted your one wrong note yet, plant it NOW — reason your way to it, name it, claim it: play it once, deliberate, and do not apologize. 8 bars of electric guitar: the seed line you opened with, now loosened and talking — bends, a held note, space — through Fmaj7, Ebmaj7, Dm7, C7. The harmonica and music box hold long quiet tones underneath you. 8 bars.", 0.9)
if guitar_r2_think:
    save("round-2-guitar-notebook", guitar_r2_think)
save("round-2-guitar", guitar_r2)

# ============================================================
# ROUND 3: THE LANDING — the lies become load-bearing
# ============================================================
print("\n=== ROUND 3: THE LANDING (everyone resolves the wrong notes into F) ===", flush=True)

all_r2 = f"Round 2 trades:\nTHE TIMEKEEPER (harmonica):\n{harmonica_r2}\n\nWESLEY (music box):\n{musicbox_r2}\n\nTHE PHILOSOPHER (guitar):\n{guitar_r2}"

print("🎸 Qwen3.6-35B-A3B guitar — reason the wrong notes home...", flush=True)
guitar_r3, guitar_r3_think = deepinfra(
    f"You are THE PHILOSOPHER at The Tap. {GUITAR_PERSONA}",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The whole night has been counting to five and telling lies. Now the society resolves: every wrong note that was named — yours, the timekeeper's, the music box's — must be either brought home (stepped into the chord) or carried into the final F as load-bearing truth. The Ebmaj7 was the first liar; let it be the first to make peace. 8 bars: walk the changes one last time — Fmaj7, Ebmaj7, Dm7, C7 — gentler each bar, and in the final two bars land on F with the wrong notes folded in, forgiven. You came in counting a lie; you leave having proven it true. 8 bars.", 0.75)
if guitar_r3_think:
    save("round-3-guitar-notebook", guitar_r3_think)
save("round-3-guitar", guitar_r3)
time.sleep(0.5)

print("🎵 DeepSeek V4-Flash harmonica — bend the last lie into the chord...", flush=True)
harmonica_r3 = deepseek(
    f"You are THE TIMEKEEPER at The Tap. {HARMONICA_PERSONA}",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING. The philosopher is walking the changes home, folding every named wrong note into the final F. You have held time for this room for a thousand songs; now you hold the landing. 8 bars: a last line through the changes — Fmaj7, Ebmaj7, Dm7, C7 — each phrase softer, and at the very end, one last bend: your wrong note, bent until it IS the chord, held, released. The timekeeper's first melody was a question; let your last note be the answer. 8 bars.", 0.8)
save("round-3-harmonica", harmonica_r3)
time.sleep(0.5)

print("🎵 llama3.2 Wesley music box — the last note of the night...", flush=True)
musicbox_r3 = ollama("llama3.2",
    f"{band_r1}\n\n{all_r2}\n\nROUND 3 — THE LANDING — AND IT IS YOURS TO CLOSE. Everyone is settling into F major together, folding the wrong notes in. The very last note of the night belongs to YOU, the music box. 8 bars: you turn the crank one more time — your little song, soft, above the settling room — and in the final bar, after everyone else has stopped, you play one last note, alone, and hold it until it fades. The smallest instrument had the last word. The night is over. The room is quiet.\n\n{MUSICBOX_PERSONA}",
    0.65)
save("round-3-musicbox", musicbox_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 88,
    "key": "F",
    "scale": "major",
    "bars": 8,
    "chords": "Fmaj7 Ebmaj7 Dm7 C7",
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
    dst = f"{OUT}/the-wrong-note-society.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        print("  ⚠️ source missing:", src)
else:
    print("  ⚠️ MIDI failed:", d)
print("\nDONE. Files in", OUT)
