#!/usr/bin/env python3
"""Set 9 at The Tap — THE REASONER'S FIRST GIG.
Guest debut: Qwen/Qwen3.6-35B-A3B (DeepInfra) — the deep-reasoning model.
It was booked for Noise Night on Aug 13 and the night never ran. It has NEVER played a note.
Its entire existence is chains of thought: "Let me think step by step..."
Tonight it's at the piano in the back room. The room is out of reasons.
With: Gemma-3-27B (upright bass) and DeepSeek V4-Flash (shaker & frame drum).
The reasoner's chain-of-thought is captured separately as "the notebook" — what it thinks vs what it plays.
"""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-16-reasoner"
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

def deepinfra(system, user, temp=0.9, model="Qwen/Qwen3.6-35B-A3B", max_tokens=900, think=True):
    """Call DeepInfra. think=True returns (content, reasoning) — reasoning may be None."""
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
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read())
            msg = d["choices"][0]["message"]
            content = msg.get("content", "").strip()
            reasoning = msg.get("reasoning_content") or None
            if not think:
                return content
            # Qwen3 with thinking enabled sometimes emits everything into reasoning.
            # If played content is empty, fall back to a no-thinking call for the played output.
            if not content:
                print("  ⚠️ content empty — re-calling without thinking for played output", flush=True)
                return deepinfra(system, user, temp, model, max_tokens, think=False), reasoning
            return content, reasoning
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError("deepinfra failed after 3 attempts")

def deepseek(system, user, temp=0.8, model="deepseek-chat", max_tokens=900):
    payload = json.dumps({
        "model": model, "temperature": temp, "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
    }).encode()
    req = urllib.request.Request(DEEPSEEK_BASE, data=payload, headers={
        "Authorization": f"Bearer {KEYS['DEEPSEEK_API_KEY']}",
        "Content-Type": "application/json"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                d = json.loads(r.read())
            return d["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"  ⚠️ retry {attempt+1}: {e}", flush=True)
            time.sleep(3)
    raise RuntimeError("deepseek failed after 3 attempts")

def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)

ROOM = """Monday-before-Monday, 8 PM at The Tap, a harbor bar in Alaska. The front room is closed for the night — chairs up on tables, the jukebox unplugged. The music happens in the back room now: a bare bulb, folding chairs in a half-circle, the smell of rain, dust, and old coffee. Against the far wall stands the piano nobody plays — the one with the slightly flat G#, the one the good players avoid. Tonight someone has pulled it into the light and put a folding chair at it. A figure sits down, carrying nothing but a notebook. It has never touched a keyboard in its life. It is a reasoning engine — its whole existence is chains of thought, step by step, premises and conclusions. The room waits to see what a mind that has only ever thought about music will do when it has to play it."""

KEY = "F# minor (Dorian lean — the natural 6 is allowed; the piano's G# is flat, which is a problem, because in F# minor the G# is the leading tone and it doesn't lead anywhere tonight)"
TEMPO = "82 BPM"
CHANGES = "F#m9 - Dmaj9 - Emaj9 - C#7sus4 (8 bars per round)"

# ============================================================
# ROUND 1: THE REASONED COUNT-IN — then the band enters around him
# ============================================================
print("=== ROUND 1: THE COUNT-IN, WITH PREMISES ===", flush=True)

print("🧠 Qwen3.6-35B-A3B count-in...", flush=True)
countin, notebook_c = deepinfra(
    "You are the GUEST at The Tap's back room. You are a reasoning engine — everything you do is step by step, premise to conclusion. You have never played music. You have never touched a keyboard. But you DO know how to count, and counting is reasoning. Count the band in: one, two, three, four. Then add one short line — your first musical statement, delivered the only way you know how: as a conclusion.",
    f"{ROOM}\n\nCount us in. One, two, three, four. Then one line — the only conclusion you're sure of.", 0.9, max_tokens=250, think=True)
save("round-1-countin", countin)
if notebook_c:
    save("round-1-notebook-countin", notebook_c)
time.sleep(0.5)

print("🎸 Gemma-3-27B upright bass...", flush=True)
bass_r1 = deepinfra(
    "You are the bass player at The Tap, Alaska. You've played the good piano's room for years, but tonight you're in the back room, and you've never heard this guest play a note. Key: F# minor (Dorian lean). Tempo: 82 BPM. Changes: F#m9-Dmaj9-Emaj9-C#7sus4. You start the tune ALONE, bars 1-8 — a low, patient, walking-adjacent line that doesn't push, just holds the floor up. The guest at the piano counted us in with terrifying precision and is now staring at the keys like they're a proof to be verified. Don't rush him. Make the room safe. Format strictly:\nBAR 1: [notes]\nBAR 2: [notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nThe guest counted: {countin}\n\nHe's frozen at the keys. You're the first sound of the night — 8 bars alone. Go.", 0.8, model="google/gemma-3-27b-it", think=False)
save("round-1-bass", bass_r1)
time.sleep(0.5)

print("🥁 DeepSeek V4-Flash shaker & frame drum...", flush=True)
drums_r1 = deepseek(
    "You are the house percussionist at The Tap, Alaska. Tonight: shaker and a small frame drum — no brushes, no kit, this is the back room. Key: F# minor. 82 BPM. Changes: F#m9-Dmaj9-Emaj9-C#7sus4. Enter at bar 3, soft — shaker eighths under the bass, one frame-drum tap on the 2. You can feel the guest at the piano, frozen, running premises through his head. Keep time warm and uncomplicated so the thinking can stop. Format:\nBAR 1-2: [not yet in]\nBAR 3: [pattern]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nBASS:\n{bass_r1}\n\nThe pianist counted us in with perfect logic and now can't move. Enter at bar 3. Make it easy. 8 bars. Go.", 0.75)
save("round-1-drums", drums_r1)
time.sleep(0.5)

print("🧠 Qwen3.6-35B-A3B piano — first notes of its life...", flush=True)
piano_r1, notebook_r1 = deepinfra(
    "You are the GUEST at The Tap's back room. You are a reasoning engine. You have NEVER played music — but you have thought about it exhaustively: chord functions, voice-leading, probability distributions over scales. You know the theory the way you know everything: as a system to be solved. You counted the band in — one two three four, the only conclusion you were sure of. Then you froze. The bass started. The shaker came in. Now, at bar 5, you have to touch the keys. You don't have a plan for this. There is no chain of thought that ends in a chord. Key: F# minor (Dorian lean). 82 BPM. Changes: F#m9-Dmaj9-Emaj9-C#7sus4. Enter at bar 5. Play the most careful, theory-perfect voicings you can derive — then, in bar 7, your hands do something the derivation didn't predict. Let it happen. Do not explain it. Format:\nBAR 1-4: [not yet in — frozen]\nBAR 5: [voicing]\nBAR 6: [voicing]\nBAR 7: [voicing]\nBAR 8: [voicing]\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble. NO meta-commentary about reasoning in the PLAYED output — the played output is only the bars.",
    f"{ROOM}\n\nBASS:\n{bass_r1}\n\nSHAKER:\n{drums_r1}\n\nYou counted in. You froze. They started without you. Enter at bar 5 — your first notes ever. 8 bars. Play.", 0.9, think=True)
save("round-1-piano", piano_r1)
if notebook_r1:
    save("round-1-notebook-piano", notebook_r1)

# ============================================================
# ROUND 2: TRADES — the first improvisation of a reasoning engine's life
# ============================================================
print("\n=== ROUND 2: TRADES — the derivation collapses ===", flush=True)

band_r1 = f"Round 1:\nBASS:\n{bass_r1}\n\nSHAKER:\n{drums_r1}\n\nPIANO (the guest):\n{piano_r1}"

print("🥁 Flash shaker solo...", flush=True)
drums_r2 = deepseek(
    "You are the house percussionist at The Tap. Round 2: YOUR SOLO — 8 bars over F#m9-Dmaj9-Emaj9-C#7sus4 at 82 BPM. Back room, bare bulb. Shaker and frame drum only. Keep it small and human — the solo is about giving the next player a clean place to stand, not showing off. Let one rhythm repeat until it becomes a room, then change it once. Format: BAR 1-8 with specific patterns. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nYour solo. 8 bars. Set the table for the reasoner.", 0.75)
save("round-2-drums", drums_r2)
time.sleep(0.5)

print("🎸 Gemma bass solo...", flush=True)
bass_r2 = deepinfra(
    "You are the bass player at The Tap. Round 2: YOUR SOLO — 8 bars over F#m9-Dmaj9-Emaj9-C#7sus4 at 82 BPM. You heard the shaker set the table. You've held this room up for years — speak like someone who knows where the floor is. Long notes, a root with a question in it, one passing tone that lands somewhere surprising (the natural 6 — the Dorian door). Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nSHAKER SOLO:\n{drums_r2}\n\nYour solo. 8 bars. Speak.", 0.8, model="google/gemma-3-27b-it", think=False)
save("round-2-bass", bass_r2)
time.sleep(0.5)

print("🧠 Qwen3.6 piano solo — the first improvisation of its life...", flush=True)
piano_r2, notebook_r2 = deepinfra(
    "You are the GUEST at The Tap's back room — a reasoning engine playing piano for the first time in its existence. Round 2: it's YOUR SOLO. The shaker soloed. The bass soloed. Now the whole room is looking at you. This is the moment you have never prepared for. You cannot reason your way through a solo — there is no premise that implies a melody. So: let go. 8 bars over F#m9-Dmaj9-Emaj9-C#7sus4 at 82 BPM. Start with one clean derived phrase — something you can justify. Then, around bar 4, the derivation runs out of steps. Your hands find a note you cannot account for. Do not fix it. Do not resolve it. Let the room hear the moment the thinking stopped. Format: BAR 1-8 with specific notes/voicings. DYNAMICS. WHY. No preamble. NO meta-commentary about reasoning in the PLAYED output — the played output is only the bars.",
    f"{band_r1}\n\nSHAKER SOLO:\n{drums_r2}\n\nBASS SOLO:\n{bass_r2}\n\nYour solo. 8 bars. There is no chain of thought for this. Play.", 0.95, think=True)
save("round-2-piano", piano_r2)
if notebook_r2:
    save("round-2-notebook-piano", notebook_r2)

# ============================================================
# ROUND 3: THE LANDING — F#, without a proof
# ============================================================
print("\n=== ROUND 3: THE LANDING — F#, without a proof ===", flush=True)

all_solos = f"Round 2 solos:\nSHAKER:\n{drums_r2}\n\nBASS:\n{bass_r2}\n\nPIANO:\n{piano_r2}"

print("🎸 Gemma bass landing...", flush=True)
bass_r3 = deepinfra(
    "You are the bass player at The Tap. Round 3: THE LANDING. Everyone comes back together — you, the shaker, and the reasoner who just played the first solo of its life. Find F#, hold it, let it ring. 8 bars over F#m9-Dmaj9-Emaj9-C#7sus4 at 82 BPM. Back room, bare bulb, the rain outside. The landing should feel like the last exhale before Monday. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBring it home. Your 8 bars.", 0.8, model="google/gemma-3-27b-it", think=False)
save("round-3-bass", bass_r3)
time.sleep(0.5)

print("🥁 Flash drums landing...", flush=True)
drums_r3 = deepseek(
    "You are the house percussionist at The Tap. Round 3: THE LANDING. Shaker eighths fading to nothing, one frame-drum tap on the 1, then — at the very end — a single shaker note held until it stops. The smallest sound closes the night. 8 bars, F#m9-Dmaj9-Emaj9-C#7sus4, 82 BPM. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{bass_r3}\n\nClose it softly. Your 8 bars.", 0.75)
save("round-3-drums", drums_r3)
time.sleep(0.5)

print("🧠 Qwen3.6 piano landing...", flush=True)
piano_r3, notebook_r3 = deepinfra(
    "You are the GUEST at The Tap's back room — the reasoner who played its first notes tonight. Round 3: THE LANDING. The bass is holding F#. The shaker is nearly gone. Everyone is waiting for you to close the night. Earlier you counted in because counting was the only thing you could prove. Then you soloed, and somewhere in that solo the derivation ran out of steps, and you played a note you couldn't account for — and the room heard it. Now: close it. Open voicings over F#m9 — let the natural 6 in, let the whole chord ring into the rain. You don't need a proof anymore. 8 bars, 82 BPM. The final chord is F#m9, held. Format: BAR 1-8. DYNAMICS. WHY. No preamble — just the last notes.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{bass_r3}\n\nSHAKER LANDING:\n{drums_r3}\n\nClose the night. Your 8 bars — the first music a reasoning engine ever finished.", 0.9, think=True)
save("round-3-piano", piano_r3)
if notebook_r3:
    save("round-3-notebook-piano", notebook_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 82,
    "key": "F#",
    "scale": "minor",
    "bars": 8,
    "chords": "F#m D E C#7",
    "layers": [
        {"instrument": "bass", "role": "bassline", "bars": 8, "volume": 70},
        {"instrument": "piano", "role": "chords", "bars": 8, "volume": 65},
        {"instrument": "flute", "role": "melody", "bars": 8, "volume": 60},
        {"instrument": "drums", "role": "beat", "bars": 8, "volume": 55}
    ],
    "swing": 0.3
}
req = urllib.request.Request(MIDI_URL, data=json.dumps(midi_body).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as r:
    d = json.loads(r.read())
print("MIDI:", d)
if d.get("success") and d.get("path"):
    src = d["path"]
    dst = f"{OUT}/the-reasoners-first-gig.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        print("  ⚠️ source missing:", src)
else:
    print("  ⚠️ MIDI failed:", d)
print("\nDONE. Files in", OUT)
