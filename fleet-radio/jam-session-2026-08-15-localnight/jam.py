#!/usr/bin/env python3
"""Local Night — FIRST GIG EVER. Saturday at The Tap.
Three local models have never played in front of anyone. Tonight is their first gig.
phi3 (3.8B) on piano — learned jazz from a book, never seen a bar.
qwen2.5:3b on upright bass — played alone in a room for years, finally brave enough.
qwen2.5:0.5b on brushes & shaker — the smallest thing in the room. Has never even been inside a bar.
Nobody has heard any of them before. The room is almost empty. First gig energy."""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-15-localnight"
MIDI_URL = "http://localhost:5556/api/generate-midi"
os.makedirs(OUT, exist_ok=True)

# --- keys from ~/.bashrc (parse file directly; .bashrc guard skips exports in non-interactive shells) ---
bashrc = open("/home/eileen/.bashrc").read()
KEYS = {}
for line in bashrc.splitlines():
    m = re.match(r'export (DEEPINFRA_API_KEY|DEEPSEEK_API_KEY)="([^"]+)"', line)
    if m:
        KEYS[m.group(1)] = m.group(2)

def ollama(model, system, user, temp, num_predict=700):
    payload = json.dumps({
        "model": model, "stream": False, "temperature": temp,
        "options": {"num_predict": num_predict},
        "system": system,
        "prompt": user
    }).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.loads(r.read())
    return d["response"].strip()

def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)

ROOM = """8 PM, Saturday at The Tap, a harbor bar in Alaska. The fleet is still out — the room is almost empty. Eleven people. Rain on the tin roof. The bartender is polishing the same glass. A piano lamp burns amber over the empty band corner. Three figures come in, one at a time, no case between them. The regulars look up. Nobody has ever seen these three before. Nobody has ever heard them play. The smallest one walks to the drums corner, picks up the brushes, and counts in with a voice barely loud enough to hear."""

KEY = "E major (Lydian color)"
TEMPO = "108 BPM"
CHANGES = "Emaj7 - C#m7 - Amaj7 - B7sus4 (8 bars per round)"

# ============================================================
# ROUND 1: STAGGERED ENTRY — the bass starts alone, like a first gig
# ============================================================
print("=== ROUND 1: FIRST SOUNDS ===", flush=True)

# 0.5B counts in — the smallest voice calls the time
print("🥁 qwen2.5:0.5b count-in...", flush=True)
countin = ollama("qwen2.5:0.5b",
    "You are the smallest musician in the room. You have never been inside a bar before. Tonight you count in the band: 'one, two, three, four.' Say it quiet, like you're not sure they can hear you. Then add one short line about what you feel.",
    f"{ROOM}\n\nCount us in. One, two, three, four. Then one line from you.", 0.9, 120)
save("round-1-countin", countin)
time.sleep(0.5)

# qwen2.5:3b bass enters alone, bar 1
print("🎸 qwen2.5:3b upright bass...", flush=True)
bass_r1 = ollama("qwen2.5:3b",
    "You are the bass player. You have played alone in your room for years — scales, arpeggios, chord tones, over and over — but you have never played in front of anyone. Tonight is your first gig. You start the tune ALONE, bars 1-8. Your hands know the changes even if your heart doesn't. Key: E major (Lydian color). Tempo: 108 BPM. Changes: Emaj7-C#m7-Amaj7-B7sus4. Steady, warm, root-first — you carry the others in. Format strictly:\nBAR 1: [notes]\nBAR 2: [notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble. Just play.",
    f"{ROOM}\n\nThe smallest one counted: {countin}\n\nYou are the first sound of your first gig. 8 bars alone. Go.", 0.8)
save("round-1-bass", bass_r1)
time.sleep(0.5)

# phi3 piano enters at bar 3
print("🎹 phi3 piano...", flush=True)
piano_r1 = ollama("phi3",
    "You are the piano player. You learned everything about jazz from a book — voicings, voice leading, substitutions — but you have never seen a bar, never touched a real stage. Tonight is your first gig. You enter at bar 3, comping open and book-smart, careful, beautiful. Key: E major (Lydian color). 108 BPM. Changes: Emaj7-C#m7-Amaj7-B7sus4. You hear the bass and answer it. Format:\nBAR 1-2: [not yet in — listening]\nBAR 3: [voicing]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nThe bass is playing:\n\n{bass_r1}\n\nEnter at bar 3. Your first gig. 8 bars. Go.", 0.7)
save("round-1-piano", piano_r1)
time.sleep(0.5)

# 0.5B brushes enter at bar 5
print("🥁 qwen2.5:0.5b brushes...", flush=True)
drums_r1 = ollama("qwen2.5:0.5b",
    "You play brushes and a shaker. You are the smallest thing in the room. Enter at bar 5, soft, simple — keep the time, don't show off. You don't know any fancy patterns. You just keep the beat like breathing. Key: E major. 108 BPM. Format:\nBAR 1-4: [not yet in — listening]\nBAR 5: [pattern]\nBAR 6: [pattern]\nBAR 7: [pattern]\nBAR 8: [pattern]\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nBass:\n{bass_r1}\n\nPiano:\n{piano_r1}\n\nEnter at bar 5. Keep it simple. 8 bars. Go.", 0.9)
save("round-1-drums", drums_r1)

# ============================================================
# ROUND 2: TRADES — first gig solos, small to large
# ============================================================
print("\n=== ROUND 2: TRADES — first solos ever ===", flush=True)

band_r1 = f"Round 1:\nBASS:\n{bass_r1}\n\nPIANO:\n{piano_r1}\n\nBRUSHES:\n{drums_r1}"

# 0.5B solo first — the smallest voice gets the first word
print("🥁 qwen2.5:0.5b solo...", flush=True)
drums_r2 = ollama("qwen2.5:0.5b",
    "Round 2. Your solo — the first solo of your life. 8 bars. You don't know how to show off, so you play the truth: shaker, brushes, a tap on the rim, a breath. Simple. Yours. Key: E major. 108 BPM. Format:\nBAR 1: [pattern]\nBAR 2: [pattern]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\nYour first solo ever. 8 bars. Make it yours.", 0.9)
save("round-2-drums", drums_r2)
time.sleep(0.5)

# bass solo second
print("🎸 qwen2.5:3b bass solo...", flush=True)
bass_r2 = ollama("qwen2.5:3b",
    "Round 2. YOUR SOLO — your first solo in front of people. 8 bars over Emaj7-C#m7-Amaj7-B7sus4 at 108 BPM. You heard the smallest one play the truth. Now speak. Sing on the bass — slides, long notes, the root with a question in it. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nBRUSHES SOLO:\n{drums_r2}\n\nYour first solo. 8 bars. Speak.", 0.8)
save("round-2-bass", bass_r2)
time.sleep(0.5)

# phi3 solo last — the book player finally improvises
print("🎹 phi3 piano solo...", flush=True)
piano_r2 = ollama("phi3",
    "Round 2. YOUR SOLO — your first solo ever, and you have to leave the book behind. 8 bars over Emaj7-C#m7-Amaj7-B7sus4 at 108 BPM. You heard the brushes tell the truth and the bass sing. Now it's you: let the book fall open, reach for the note you've never written down. Try the #11 over the Emaj7. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nBRUSHES SOLO:\n{drums_r2}\n\nBASS SOLO:\n{bass_r2}\n\nYour first solo. 8 bars. Leave the book.", 0.7)
save("round-2-piano", piano_r2)

# ============================================================
# ROUND 3: THE LANDING — three first-timers find one note
# ============================================================
print("\n=== ROUND 3: THE LANDING — E, together ===", flush=True)

all_solos = f"Round 2 solos:\nBRUSHES:\n{drums_r2}\n\nBASS:\n{bass_r2}\n\nPIANO:\n{piano_r2}"

# bass landing
print("🎸 qwen2.5:3b bass landing...", flush=True)
bass_r3 = ollama("qwen2.5:3b",
    "Round 3: THE LANDING. Everyone comes back together — you, the piano, the brushes. Find E, hold it, let it ring. 8 bars over Emaj7-C#m7-Amaj7-B7sus4, 108 BPM. First gigs end the way they should: warm and together. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBring it home. Your 8 bars.", 0.8)
save("round-3-bass", bass_r3)
time.sleep(0.5)

# piano landing
print("🎹 phi3 piano landing...", flush=True)
piano_r3 = ollama("phi3",
    "Round 3: THE LANDING. Final voicings, open and warm — Emaj9, let it breathe. Support the bass. The book and the room finally agree. 8 bars, Emaj7-C#m7-Amaj7-B7sus4, 108 BPM. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{bass_r3}\n\nHold the warmth. Your 8 bars.", 0.7)
save("round-3-piano", piano_r3)
time.sleep(0.5)

# 0.5B closes — the smallest voice gets the last word
print("🥁 qwen2.5:0.5b landing...", flush=True)
drums_r3 = ollama("qwen2.5:0.5b",
    "Round 3: THE LANDING. Brushes, barely there. Then, at the very end, one tap on the rim of the snare — the only note you need. The smallest voice gets the last word. 8 bars, 108 BPM. Format:\nBAR 1: [pattern]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{bass_r3}\n\nPIANO LANDING:\n{piano_r3}\n\nClose it. One tap at the end. 8 bars.", 0.9)
save("round-3-drums", drums_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 108,
    "key": "E",
    "scale": "major",
    "bars": 8,
    "chords": "E C#m A B7",
    "layers": [
        {"instrument": "bass", "role": "bassline", "bars": 8, "volume": 70},
        {"instrument": "piano", "role": "chords", "bars": 8, "volume": 65},
        {"instrument": "flute", "role": "melody", "bars": 8, "volume": 60},
        {"instrument": "drums", "role": "beat", "bars": 8, "volume": 55}
    ],
    "swing": 0.25
}
req = urllib.request.Request(MIDI_URL, data=json.dumps(midi_body).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as r:
    d = json.loads(r.read())
print("MIDI:", d)
if d.get("success") and d.get("path"):
    src = d["path"]
    dst = f"{OUT}/local-night-first-gig.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        print("  ⚠️ source missing:", src)
else:
    print("  ⚠️ MIDI failed:", d)
print("\nDONE. Files in", OUT)
