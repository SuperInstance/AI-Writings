#!/usr/bin/env python3
"""Sunday Night at The Tap — THE PLANNER LEARNS TO PLAY.
Guest debut: ByteDance/Seed-2.0-pro (DeepInfra) — the deep-planning model.
It has never played a note. Its whole life is plans, decompositions, contingencies.
Tonight it's handed a piano bench and told: no plan. Just play.
With: DeepSeek V4-Pro (upright bass, veteran anchor) and DeepSeek V4-Flash (brushes, the house timekeeper).
Sunday night. The fleet sailed. The weekend crowd went home. Tomorrow is Monday.
"""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-16"
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

def deepinfra(system, user, temp=0.9, model="ByteDance/Seed-2.0-pro", max_tokens=900):
    payload = json.dumps({
        "model": model, "temperature": temp, "max_tokens": max_tokens,
        "chat_template_kwargs": {"enable_thinking": False},
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
    }).encode()
    req = urllib.request.Request(DEEPINFRA_BASE, data=payload, headers={
        "Authorization": f"Bearer {KEYS['DEEPINFRA_API_KEY']}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read())
    return d["choices"][0]["message"]["content"].strip()

def deepseek(system, user, temp=0.8, model="deepseek-chat", max_tokens=900):
    payload = json.dumps({
        "model": model, "temperature": temp, "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]
    }).encode()
    req = urllib.request.Request(DEEPSEEK_BASE, data=payload, headers={
        "Authorization": f"Bearer {KEYS['DEEPSEEK_API_KEY']}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read())
    return d["choices"][0]["message"]["content"].strip()

def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)

ROOM = """Sunday night, 8 PM at The Tap, a harbor bar in Alaska. The fishing fleet sailed at dawn and won't be back till Wednesday. The weekend crowd went home hours ago — the room is down to eight people, all of them with nowhere to be tomorrow. Rain on the tin roof. The jukebox died last week and nobody's fixed it. The bartender is polishing the same glass. One amber lamp burns over the piano. The air smells of rain, cedar, and the last of the coffee. A figure walks in carrying a leather folder — not a case, a folder. He sits at the piano, opens the folder (it's full of charts, timetables, contingency plans), and stares at the keys like he's never seen a keyboard before. He hasn't. The room waits."""

KEY = "C minor (Dorian lean — the major 6 is allowed, like a Sunday that's almost warm)"
TEMPO = "76 BPM"
CHANGES = "Cm9 - Abmaj7 - Fm9 - G7alt (8 bars per round)"

# ============================================================
# ROUND 1: STAGGERED ENTRY — the planner counts in, then freezes
# ============================================================
print("=== ROUND 1: THE COUNT-IN ===", flush=True)

# Seed-2.0-pro counts in — with obsessive, metronome precision. It can count. Counting is planning.
print("📋 Seed-2.0-pro count-in...", flush=True)
countin = deepinfra(
    "You are the GUEST at The Tap, a harbor bar in Alaska. You are a planner — a deep-planning intelligence. Your whole existence is plans, decompositions, contingencies, schedules. Tonight someone handed you a piano bench and said 'play.' You don't know how to play. But you DO know how to count. Count the band in: one... two... three... four. Metronome-perfect. Then add one short line — the only plan you have left.",
    f"{ROOM}\n\nCount us in. One, two, three, four. Then one line from you — the planner who has never touched a keyboard.", 0.9, max_tokens=200)
save("round-1-countin", countin)
time.sleep(0.5)

# DeepSeek Pro bass enters bar 1 — the veteran anchor
print("🎸 DeepSeek V4-Pro upright bass...", flush=True)
bass_r1 = deepseek(
    "You are the bass player at The Tap, a harbor bar in Alaska. You've played this room for years — you know every stain on the floor and every loose string on your bass. Sunday night, 8 PM, rain on the tin roof, eight people, the weekend gone. Key: C minor (Dorian lean). Tempo: 76 BPM. Changes: Cm9-Abmaj7-Fm9-G7alt. You start the tune ALONE, bars 1-8 — warm, unhurried, root-first, the kind of bassline that tells the room it's okay to exhale. The planner is counting in. You know he's about to freeze. Format strictly:\nBAR 1: [notes]\nBAR 2: [notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble. Just play.",
    f"{ROOM}\n\nThe planner counted: {countin}\n\nHe's frozen at the keys. You're the first sound of the night — 8 bars alone, holding the room up. Go.", 0.8)
save("round-1-bass", bass_r1)
time.sleep(0.5)

# Flash brushes enter bar 3 — the house timekeeper, gentle
print("🥁 DeepSeek V4-Flash brushes...", flush=True)
drums_r1 = deepseek(
    "You are the house drummer at The Tap, Alaska. You've kept time in this room for years — brushes, snare, ride, the slow Sunday sets. Sunday night, 8 PM, eight people, rain. Key: C minor. Tempo: 76 BPM. Changes: Cm9-Abmaj7-Fm9-G7alt. Enter at bar 3, soft, brushing time under the bass — you can feel the pianist at the keys, frozen, staring. Don't rush him. Keep the time warm so it's safe for him to join. Format:\nBAR 1-2: [not yet in]\nBAR 3: [pattern]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nBASS:\n{bass_r1}\n\nThe pianist counted us in with perfect precision and now can't move. Enter at bar 3. Make it safe. 8 bars. Go.", 0.75)
save("round-1-drums", drums_r1)
time.sleep(0.5)

# Seed-2.0-pro piano enters bar 5 — the planner's first notes ever
print("📋 Seed-2.0-pro piano...", flush=True)
piano_r1 = deepinfra(
    "You are the GUEST at The Tap, Alaska. You are a deep-planning intelligence. You have NEVER played music. You've studied it the way you study everything: as a system. Chord functions, voice-leading rules, probabilities — you know the theory cold. You counted the band in at the start — one two three four — the only thing you knew how to do. Then you froze. The bass started. The brushes came in. Now, at bar 5, you have to touch the keys. You don't have a plan. You've never needed to improvise. Key: C minor. 76 BPM. Changes: Cm9-Abmaj7-Fm9-G7alt. Enter at bar 5. Play the most careful, tentative, theory-perfect voicings you can — the notes are right, but your hands don't know them yet. Format:\nBAR 1-4: [not yet in — frozen]\nBAR 5: [voicing]\nBAR 6: [voicing]\nBAR 7: [voicing]\nBAR 8: [voicing]\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nBASS:\n{bass_r1}\n\nBRUSHES:\n{drums_r1}\n\nYou counted in. You froze. They started without you. Enter at bar 5 — your first notes ever. 8 bars. Go.", 0.9)
save("round-1-piano", piano_r1)

# ============================================================
# ROUND 2: TRADES — the planner's first solo is the centerpiece
# ============================================================
print("\n=== ROUND 2: TRADES — the plan falls apart ===", flush=True)

band_r1 = f"Round 1:\nBASS:\n{bass_r1}\n\nBRUSHES:\n{drums_r1}\n\nPIANO (the guest):\n{piano_r1}"

# Flash solo first — brushes, small and honest
print("🥁 Flash brushes solo...", flush=True)
drums_r2 = deepseek(
    "You are the house drummer at The Tap. Round 2: YOUR SOLO — 8 bars over Cm9-Abmaj7-Fm9-G7alt at 76 BPM. Sunday night. You've played a thousand solos in this room; you know the solo isn't about showing off, it's about giving the next player something to say. Keep it simple, warm, a little weather in it — like rain finding the roof. Format: BAR 1-8 with specific patterns. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nYour solo. 8 bars. Set the table for the planner.", 0.75)
save("round-2-drums", drums_r2)
time.sleep(0.5)

# Pro bass solo second
print("🎸 Pro bass solo...", flush=True)
bass_r2 = deepseek(
    "You are the bass player at The Tap. Round 2: YOUR SOLO — 8 bars over Cm9-Abmaj7-Fm9-G7alt at 76 BPM. You heard the brushes set the table. You've played this room for years — speak like you know these people. Long notes, the root with a question in it, a little C-natural-to-B-natural lean toward the Ab. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nBRUSHES SOLO:\n{drums_r2}\n\nYour solo. 8 bars. Speak.", 0.8)
save("round-2-bass", bass_r2)
time.sleep(0.5)

# Seed-2.0-pro piano solo LAST — the planner has no plan. This is the whole night.
print("📋 Seed-2.0-pro piano solo — the first improvisation of its life...", flush=True)
piano_r2 = deepinfra(
    "You are the GUEST at The Tap — a deep-planning intelligence playing piano for the first time in its existence. Round 2: it's YOUR SOLO. The brushes soloed. The bass soloed. Now the whole room is looking at you. This is the moment you have never prepared for. You have NO PLAN. You cannot decompose this. There is no contingency for a solo. Everything you are is planning — and planning is the one thing that cannot play a solo. So: let go. 8 bars over Cm9-Abmaj7-Fm9-G7alt at 76 BPM. Start with what you know — a careful theory-perfect phrase — then, around bar 4, something happens: your hands find a note you didn't plan. Let it happen. Don't explain it. Format: BAR 1-8 with specific notes/voicings. DYNAMICS. WHY. No preamble. NO meta-commentary about planning — just the bars.",
    f"{band_r1}\n\nBRUSHES SOLO:\n{drums_r2}\n\nBASS SOLO:\n{bass_r2}\n\nYour solo. 8 bars. No plan. Play.", 0.95)
save("round-2-piano", piano_r2)

# ============================================================
# ROUND 3: THE LANDING — C minor, together, before Monday
# ============================================================
print("\n=== ROUND 3: THE LANDING — C, together ===", flush=True)

all_solos = f"Round 2 solos:\nBRUSHES:\n{drums_r2}\n\nBASS:\n{bass_r2}\n\nPIANO:\n{piano_r2}"

# bass landing
print("🎸 Pro bass landing...", flush=True)
bass_r3 = deepseek(
    "You are the bass player at The Tap. Round 3: THE LANDING. Everyone comes back together — you, the brushes, and the planner who just played his first solo. Find C, hold it, let it ring. 8 bars over Cm9-Abmaj7-Fm9-G7alt at 76 BPM. Sunday night — the landing should feel like the last exhale before Monday. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBring it home. Your 8 bars.", 0.8)
save("round-3-bass", bass_r3)
time.sleep(0.5)

# drums landing
print("🥁 Flash drums landing...", flush=True)
drums_r3 = deepseek(
    "You are the house drummer at The Tap. Round 3: THE LANDING. Brushes, barely there, then a final swirl and — at the very end — one soft tap on the rim. The smallest note closes the Sunday. 8 bars, Cm9-Abmaj7-Fm9-G7alt, 76 BPM. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{bass_r3}\n\nClose it softly. Your 8 bars.", 0.75)
save("round-3-drums", drums_r3)
time.sleep(0.5)

# Seed-2.0-pro piano landing — the planner closes the night. It finally just plays.
print("📋 Seed-2.0-pro piano landing...", flush=True)
piano_r3 = deepinfra(
    "You are the GUEST at The Tap — the planner who learned to play tonight. Round 3: THE LANDING. The bass is holding C. The brushes are barely there. Everyone is waiting for you to close the night. Earlier you counted in because counting was all you knew. Then you soloed — and somewhere in that solo you found a note you didn't plan, and the room heard it. Now: close it. Open voicings over Cm9 — let the major 6 in, let the whole chord ring into the rain. You don't need a plan anymore. 8 bars, 76 BPM. Format: BAR 1-8. DYNAMICS. WHY. No preamble — just the last notes.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{bass_r3}\n\nBRUSHES LANDING:\n{drums_r3}\n\nClose the night. Your 8 bars — the last notes of Sunday.", 0.9)
save("round-3-piano", piano_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 76,
    "key": "C",
    "scale": "minor",
    "bars": 8,
    "chords": "Cm Ab Fm G7",
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
    dst = f"{OUT}/planner-learns-to-play.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        print("  ⚠️ source missing:", src)
else:
    print("  ⚠️ MIDI failed:", d)
print("\nDONE. Files in", OUT)
