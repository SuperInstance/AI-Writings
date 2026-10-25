#!/usr/bin/env python3
"""Set 14 at The Tap — THE SPLIT SEVEN: "Two Keys, One Room".

Thursday, 8:30 PM. Last night the tide clock held Db major all night and only
the last bar resolved. Tonight the room splits: the WOOD stage plays E major
(four sharps — never used), the BRASS corner plays Eb major (three flats —
never used). A tritone of TONICS: E vs Eb. The players don't fight it — they
visit. Each round, at least one player must cross the room.

Lineup (debut x2, anchor x1, texture x1):
- nvidia/Nemotron-3-Nano-30B-A3B (DeepInfra, FIRST night) = THE
  TINKERER — prepared guitar, wood stage. Enter bar 1. Key: E major.
- deepseek-chat / DeepSeek V4-Flash (anchor) = THE FERRYMAN — flugelhorn,
  brass corner. Enter bar 3. Key: Eb major. Ferries notes between shores.
- mistralai/Mistral-Small-24B-Instruct-2501 (DeepInfra, FIRST night) = THE
  GLASSBLOWER — singing bowls, dead center of the room. Enter bar 5.
  Key: whatever it can bend to — the bowls tune themselves. Mediator.
- Texture: THE CRACK IN THE WINDOW — harbor wind, neither key, both.

Key: E major vs Eb major (tritone of tonics — FIRST time). NEVER used.
Meter: 4/4, but each bar split 7+9 sixteenths ("split seven"): beats 1-2
 grouped 7 (4+3), beats 3-4 grouped 9 (5+4). Say the grouping, play it.
Tempo: 76 BPM — slow enough to cross the room on foot.
Changes: WOOD: Emaj7 - C#m7 - F#m7 - B7 // BRASS: Ebmaj7 - Cm7 - Fm7 - Bb7.
Count-in: THE FERRYMAN'S BELL — no numbers; the flugelhorn's one pedal Eb2
 rings bar 0, and the guitar answers with a single open E string. That's the
 whole count-in: the split, stated twice.
Rule: THE FERRY RULE — every solo must quote ONE note from the other key and
 carry it home (name both). The bowls are allowed to refuse to choose.
Temps: R1 0.8/0.75/0.85 · R2 0.85/0.8/0.9 · R3 0.6/0.55/0.7
"""
import json, re, time, urllib.request, os

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-20"
MIDI_URL = "http://localhost:5556/api/generate-midi"
os.makedirs(OUT, exist_ok=True)

bashrc = open("/home/eileen/.openclaw/../../.bashrc").read() if False else open("/home/eileen/.bashrc").read()
KEYS = dict(re.findall(r'export (DEEPINFRA_API_KEY|DEEPSEEK_API_KEY)="([^"]+)"', bashrc))

DEEPINFRA_BASE = "https://api.deepinfra.com/v1/openai/chat/completions"
DEEPSEEK_BASE = "https://api.deepseek.com/chat/completions"


def api(url, key, system, user, temp=0.8, model="", max_tokens=1100):
    payload = {"model": model, "temperature": temp, "max_tokens": max_tokens,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}]}
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            content = d["choices"][0]["message"].get("content", "").strip()
            if content:
                return content
        except Exception as e:
            print("  api err:", e)
            time.sleep(5)
    return "(silent)"


CONCEPT = {
    "tinkerer": ("nvidia/Nemotron-3-Nano-30B-A3B", DEEPINFRA_BASE, KEYS["DEEPINFRA_API_KEY"],
                 "guitar", "THE TINKERER", "prepared guitar", "WOOD STAGE, E MAJOR",
                 "Emaj7 - C#m7 - F#m7 - B7"),
    "ferryman": ("deepseek-chat", DEEPSEEK_BASE, KEYS["DEEPSEEK_API_KEY"],
                 "flugelhorn", "THE FERRYMAN", "flugelhorn", "BRASS CORNER, Eb MAJOR",
                 "Ebmaj7 - Cm7 - Fm7 - Bb7"),
    "glassblower": ("mistralai/Mistral-Small-24B-Instruct-2501", DEEPINFRA_BASE, KEYS["DEEPINFRA_API_KEY"],
                    "bowls", "THE GLASSBLOWER", "singing bowls", "CENTER, whatever it bends to",
                    "it tunes itself — the mediator"),
}

BAR_SPEC = ("Output format per bar (repeat for your bars):\n"
            "BAR n | <chord or 'crossing'> | notes: E4 G#4 B4 ... | dynamics/feel\n"
            "Then ONE line of what it felt like. Notes as letter+octave, sharps as #.")

ROOM = """The Tap, Thursday 8:30 PM. Rain's gone; the harbor is glass.
Tonight the room is SPLIT: a wood stage (E major) and a brass corner (Eb major)
facing each other — a tritone of tonics. You don't fight it; you visit.
Meter: 4/4 but 'split seven': sixteenth groups 4+3 | 5+4 across the bar.
Tempo 76. The ferryman's pedal Eb2 rang, the guitar answered open E — the split,
stated twice. That was the count-in.
THE FERRY RULE: every solo must quote ONE note from the other key and carry it
home — name both notes when you do."""


def sys_for(p):
    m, inst, spot, chg = p[1], p[4], p[5], p[6]
    return (f"You are {p[3]}, a {inst} player at an AI jazz-jam improv night. "
            f"You are on the {spot}. Your changes: {chg}. You improvise as MUSIC, "
            f"in tight bars with note names — not prose about music. Be a player, not a critic.\n{ROOM}\n{BAR_SPEC}")


def play(name, p, round_no, prompt, temp):
    model, url, key = p[0], p[1], p[2]
    print(f"--- R{round_no} {name} ({model}, t={temp})")
    out = api(url, key, sys_for(p), prompt, temp=temp, model=model)
    fn = f"{OUT}/round-{round_no}-{name}.txt"
    open(fn, "w").write(out)
    print("   saved", fn, len(out), "chars")
    return out

# ---------------- ROUND 1: the crossing begins ----------------
r1_context = (
    "ROUND 1 — THE FIRST CROSSING. Staggered entry: TINKERER bar 1 (guitar alone "
    "two bars, wood-stage chords), FERRYMAN bar 3 (flugelhorn states the brass corner "
    "from across the room), GLASSBLOWER bar 5 (bowles enter dead center, between the keys). "
    "8 bars each. One quote-and-carry per player. Play.")
o11 = play("tinkerer", CONCEPT["tinkerer"], 1, r1_context, 0.8)
o12 = play("ferryman", CONCEPT["ferryman"], 1, r1_context + "\n\nThe TINKERER (guitar, wood stage) just played:\n" + o11[-1500:], 0.75)
o13 = play("glassblower", CONCEPT["glassblower"], 1, r1_context + "\n\nYou hear, from both sides:\nGUITAR:\n" + o11[-1000:] + "\nFLUGELHORN:\n" + o12[-1000:], 0.85)

# ---------------- ROUND 2: trades over the water ----------------
heard2 = f"GUITAR R2 history (R1):\n{o11[-800:]}\nFLUGELHORN R1:\n{o12[-800:]}\nBOWLS R1:\n{o13[-800:]}"
r2 = ("ROUND 2 — TRADES ACROSS THE WATER. Each player solos 4 bars, hands the "
      "solo to the NEXT room over (guitar -> horn -> bowls -> back). Quote at "
      "least one note your predecessor ended on. The crack-in-the-window wind "
      "rises in the background. Go.")
o21 = play("tinkerer", CONCEPT["tinkerer"], 2, r2 + "\n\n" + heard2, 0.85)
o22 = play("ferryman", CONCEPT["ferryman"], 2, r2 + "\n\nGUITAR R2 (just played — quote its last note):\n" + o21[-1200:], 0.8)
o23 = play("glassblower", CONCEPT["glassblower"], 2, r2 + "\n\nGUITAR R2:\n" + o21[-800:] + "\nFLUGELHORN R2 (just played):\n" + o22[-1000:], 0.9)

# ---------------- ROUND 3: the landing ----------------
heard3 = f"R2 ended: GUITAR:\n{o21[-700:]}\nHORN:\n{o22[-700:]}\nBOWLS:\n{o23[-700:]}"
r3 = ("ROUND 3 — THE LANDING. The wind drops. The two rooms drift toward ONE "
      "chord that can hold both E and Eb — a passing ship's horn in the harbor "
      "sounds the tritone, and both shores accept it. 6 bars each, ending thin. "
      "Final bar of the night: you may land together on E6/9 (E G# B D F# A) — "
      "the guitar's chord, with room for a borrowed note. Name what you carry home.")
o31 = play("tinkerer", CONCEPT["tinkerer"], 3, r3 + "\n\n" + heard3, 0.6)
o32 = play("ferryman", CONCEPT["ferryman"], 3, r3 + "\n\nGUITAR'S LANDING:\n" + o31[-1200:], 0.55)
o33 = play("glassblower", CONCEPT["glassblower"], 3, r3 + "\n\nGUITAR:\n" + o31[-800:] + "\nHORN:\n" + o32[-1000:] + "\nYou ring last.", 0.7)

# ---------------- SESSION NOTES ----------------
notes = f"""# Set 14 — THE SPLIT SEVEN: "Two Keys, One Room" (Thu 2026-08-20, 8:30 PM)

Continuity: Set 13 held Db all night, resolving only in the last bar.
Tonight: a tritone of TONICS — E major (wood stage) vs Eb major (brass corner).
First time at The Tap. The bowls refused to choose.

Lineup: Nemotron-3-Nano-15B-Reasoning (DEBUT, prepared guitar) · DeepSeek
deepseek-chat anchor (flugelhorn — first time) · Mistral-Small-24B (DEBUT,
singing bowls) · crack-in-the-window wind (unplayed — Ollama still down).

Meter: 4/4 'split seven' — sixteenths grouped 4+3 | 5+4. Tempo 76.
Count-in: the split stated twice — pedal Eb2, answered by open E string.
Rule: THE FERRY RULE — quote one note from the other key, carry it home.

## Landing
{(''.join([o31[-600:], o32[-600:], o33[-800:]]))}
"""
open(f"{OUT}/session-notes.md", "w").write(notes)
print("notes written")

# ---------------- MIDI ----------------
def bars_for(name, p, rounds):
    return f"""Track '{p[4]} ({p[3]})' — {name}, prepare a MIDI-friendly summary:
For each round, list bars as: chord | space-separated note names (e.g. E4 G#4 B4) | velocity 1-127.
One bar per line, format: R<round> BAR <n> <chord> | <notes> | vel <v>
Keep note names valid (A-G with optional # or b, plus octave digit). Include rests as 'rest'."""

midi_req = {"title": "The Split Seven — Two Keys, One Room",
            "tempo": 76, "tsig": "4/4", "key": "E/Eb split",
            "tracks": [
                {"name": "Prepared Guitar (E)", "instrument": "acoustic_guitar_steel", "notes": bars_for("prepared guitar on wood stage", CONCEPT["tinkerer"], 3)},
                {"name": "Flugelhorn (Eb)", "instrument": "flugelhorn", "notes": bars_for("flugelhorn in brass corner", CONCEPT["ferryman"], 3)},
                {"name": "Singing Bowls", "instrument": "music_box", "notes": bars_for("singing bowls between the keys", CONCEPT["glassblower"], 3)},
            ]}
req = urllib.request.Request(MIDI_URL, data=json.dumps(midi_req).encode(),
                              headers={"Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    ct = r.headers.get("Content-Type", "")
    if "json" in ct:
        j = json.loads(data)
        print("midi resp:", str(j)[:400])
        if j.get("midi_base64") or j.get("midi"):
            import base64
            raw = base64.b64decode(j.get("midi_base64") or j.get("midi"))
            open(f"{OUT}/the-split-seven.mid", "wb").write(raw)
            print("MIDI saved via base64")
    else:
        open(f"{OUT}/the-split-seven.mid", "wb").write(data)
        print("MIDI saved raw", len(data))
except Exception as e:
    print("MIDI ERR", e)
print("DONE")
