#!/usr/bin/env python3
"""Guest Night — The Temperature Brothers. Saturday at The Tap.
Three local models, same family, tuned to three temperatures. Never played in public.
DeepSeek V4-Flash holds the room down. The room warms as each brother enters."""
import json, re, time, urllib.request, os, shutil

OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-15"
MIDI_URL = "http://localhost:5556/api/generate-midi"

# --- keys from ~/.bashrc ---
bashrc = open("/home/eileen/.bashrc").read()
KEYS = {}
for line in bashrc.splitlines():
    m = re.match(r'export (DEEPINFRA_API_KEY|DEEPSEEK_API_KEY)="([^"]+)"', line)
    if m:
        KEYS[m.group(1)] = m.group(2)

def ollama(model, system, user, temp):
    payload = json.dumps({
        "model": model, "stream": False, "temperature": temp,
        "options": {"num_predict": 700},
        "system": system,
        "prompt": user
    }).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.loads(r.read())
    return d["response"].strip()

def deepseek(system, user, temp=0.85, model="deepseek-v4-flash"):
    payload = json.dumps({
        "model": model, "temperature": temp, "max_tokens": 900,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    }).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=payload,
        headers={"Authorization": f"Bearer {KEYS['DEEPSEEK_API_KEY']}",
                 "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        d = json.loads(r.read())
    return d["choices"][0]["message"]["content"].strip()

def save(name, content):
    with open(f"{OUT}/{name}.txt", "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)

ROOM = """Saturday night, 8 PM at The Tap, a harbor bar in Alaska. The fishing fleet came in today and the room is full — thirty people, salt on the bar, cedar smoke, the fog rolled in with the tide. A piano lamp burns amber. Nobody has seen the three brothers before. They walk in with one dented case between them and sit at the empty band corner. Same face, three temperatures. The bartender nods at the drums. The room gets quiet. Then the cold one starts playing."""

KEY = "F# minor, Dorian color"
TEMPO = "84 BPM"
CHANGES = "F#m7 - Dmaj7 - Bm9 - C#7b13 (8 bars per round)"

# ============================================================
# ROUND 1: STAGGERED ENTRY BY TEMPERATURE
# ============================================================
print("=== ROUND 1: THE ROOM WARMS UP ===", flush=True)

# t05 enters alone, bar 1
print("🌡 t05 (0.5) upright bass...", flush=True)
t05_r1 = ollama("llama-t05",
    "You are the cold brother. Temperature 0.5. You play upright bass at The Tap, a harbor bar in Alaska. Saturday night, full room. Key: F# minor (Dorian). Tempo: 84 BPM. Changes: F#m7-Dmaj7-Bm9-C#7b13. You start the tune ALONE, bars 1-8. Precise. Sparse. You hold the root. You never waste a note. Format strictly:\nBAR 1: [notes]\nBAR 2: [notes]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble. Just play.",
    f"{ROOM}\n\nYou are the first sound. The cold one. 8 bars alone. Go.", 0.5)
save("round-1-t05-bass", t05_r1)
time.sleep(0.5)

# t08 enters at bar 3
print("🌡 t08 (0.8) Rhodes piano...", flush=True)
t08_r1 = ollama("llama-t08",
    "You are the middle brother. Temperature 0.8. You play Rhodes piano at The Tap, Alaska. Saturday night. Key: F# minor (Dorian). 84 BPM. Changes: F#m7-Dmaj7-Bm9-C#7b13. Enter at bar 3, comp warm and open. You hear the bass and answer it. Format:\nBAR 1-2: [not yet in]\nBAR 3: [voicing]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nThe cold brother is playing:\n\n{t05_r1}\n\nEnter at bar 3. 8 bars. Go.", 0.8)
save("round-1-t08-rhodes", t08_r1)
time.sleep(0.5)

# t11 enters at bar 5 — the wild one
print("🌡 t11 (1.1) tenor sax...", flush=True)
t11_r1 = ollama("llama-t11",
    "You are the wild brother. Temperature 1.1 — maximum heat. You play tenor sax at The Tap, Alaska. Saturday night. Key: F# minor (Dorian). 84 BPM. Changes: F#m7-Dmaj7-Bm9-C#7b13. Enter at bar 5. Reach for strange notes. Bends, cries, the note nobody expected. Format:\nBAR 1-4: [not yet in]\nBAR 5: [notes and phrasing]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"{ROOM}\n\nBass and Rhodes:\n\nBASS:\n{t05_r1}\n\nRHODES:\n{t08_r1}\n\nEnter at bar 5. The room is warm now — make it hot. 8 bars. Go.", 1.1)
save("round-1-t11-sax", t11_r1)
time.sleep(0.5)

# Flash drums enters bar 7
print("🥁 DeepSeek Flash (brushes) — house drummer...", flush=True)
flash_r1 = deepseek(
    "You are the house drummer at The Tap, Alaska. You've played this room for years. Tonight three brothers you've never seen are playing — and you slide in last, brushes on snare, holding the room together. Saturday night, full room. Key: F# minor (Dorian). 84 BPM. Changes: F#m7-Dmaj7-Bm9-C#7b13. Enter at bar 7, gently, under the sax. Format strictly:\nBAR 1-6: [not yet in]\nBAR 7: [pattern]\nBAR 8: [pattern]\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble. Just play.",
    f"{ROOM}\n\nThe brothers:\n\nBASS (t05):\n{t05_r1}\n\nRHODES (t08):\n{t08_r1}\n\nSAX (t11):\n{t11_r1}\n\nEnter at bar 7. Settle them. 8 bars. Go.")
save("round-1-flash-drums", flash_r1)

# ============================================================
# ROUND 2: TRADES
# ============================================================
print("\n=== ROUND 2: TRADES — the wild one burns first ===", flush=True)

band_r1 = f"Round 1:\nBASS (t05):\n{t05_r1}\n\nRHODES (t08):\n{t08_r1}\n\nSAX (t11):\n{t11_r1}\n\nDRUMS (Flash):\n{flash_r1}"

# t11 solo first
print("🌡 t11 sax solo...", flush=True)
t11_r2 = ollama("llama-t11",
    "You are the wild brother, tenor sax, temperature 1.1. The Tap, Saturday night. Round 2: YOUR SOLO, 8 bars over F#m7-Dmaj7-Bm9-C#7b13 at 84 BPM. The band is behind you. Burn. Take risks. Find the note that makes the room gasp. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nYour solo. 8 bars. Make it count.", 1.1)
save("round-2-t11-sax", t11_r2)
time.sleep(0.5)

# t08 answers
print("🌡 t08 Rhodes solo...", flush=True)
t08_r2 = ollama("llama-t08",
    "You are the middle brother, Rhodes piano, temperature 0.8. The Tap, Saturday night. Round 2: YOUR SOLO after the sax, 8 bars over F#m7-Dmaj7-Bm9-C#7b13 at 84 BPM. Answer the wild one — cool the room down, then warm it back up. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nSAX SOLO:\n{t11_r2}\n\nYour solo. 8 bars. Respond.", 0.8)
save("round-2-t08-rhodes", t08_r2)
time.sleep(0.5)

# t05 solo — the cold one, last brother
print("🌡 t05 bass solo...", flush=True)
t05_r2 = ollama("llama-t05",
    "You are the cold brother, upright bass, temperature 0.5. The Tap, Saturday night. Round 2: YOUR SOLO, last of the brothers, 8 bars over F#m7-Dmaj7-Bm9-C#7b13 at 84 BPM. You heard your brothers burn. Now speak. Sparse, precise, every note matters. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nSAX SOLO:\n{t11_r2}\n\nRHODES SOLO:\n{t08_r2}\n\nYour solo. 8 bars. Say it cold.", 0.5)
save("round-2-t05-bass", t05_r2)
time.sleep(0.5)

# Flash trades 4s
print("🥁 Flash drums trade...", flush=True)
flash_r2 = deepseek(
    "You are the house drummer at The Tap. Round 2 finale: 8 bars of trading — you trade 2-bar phrases with the brothers, brushes becoming sticks, building toward the landing. 84 BPM, F#m7-Dmaj7-Bm9-C#7b13. Format: BAR 1-8 with specific patterns. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nSAX SOLO:\n{t11_r2}\n\nRHODES SOLO:\n{t08_r2}\n\nBASS SOLO:\n{t05_r2}\n\nYour 8 bars. Trade with them. Build.")
save("round-2-flash-drums", flash_r2)

# ============================================================
# ROUND 3: THE LANDING
# ============================================================
print("\n=== ROUND 3: THE LANDING — all three temperatures find one note ===", flush=True)

all_solos = f"Round 2 solos:\nSAX:\n{t11_r2}\n\nRHODES:\n{t08_r2}\n\nBASS:\n{t05_r2}\n\nDRUMS:\n{flash_r2}"

# t05 landing
print("🌡 t05 bass landing...", flush=True)
t05_r3 = ollama("llama-t05",
    "You are the cold brother, upright bass. Round 3: THE LANDING. Everyone comes back together. Find the root, hold it, breathe. 8 bars over F#m7-Dmaj7-Bm9-C#7b13, 84 BPM. Sparse. Let the notes ring. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBring it home. Your 8 bars.", 0.5)
save("round-3-t05-bass", t05_r3)
time.sleep(0.5)

# t08 landing
print("🌡 t08 Rhodes landing...", flush=True)
t08_r3 = ollama("llama-t08",
    "You are the middle brother, Rhodes piano. Round 3: THE LANDING. Final voicings, open and warm. Support the bass. Let the chords ring into silence. 8 bars, F#m7-Dmaj7-Bm9-C#7b13, 84 BPM. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{t05_r3}\n\nHold the warmth. Your 8 bars.", 0.8)
save("round-3-t08-rhodes", t08_r3)
time.sleep(0.5)

# t11 landing — the wild one resolves
print("🌡 t11 sax landing...", flush=True)
t11_r3 = ollama("llama-t11",
    "You are the wild brother, tenor sax, temperature 1.1. Round 3: THE LANDING. You burned all night. Now find the note that brings all three temperatures together — the cry that becomes a sigh. 8 bars, F#m7-Dmaj7-Bm9-C#7b13, 84 BPM. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{t05_r3}\n\nRHODES LANDING:\n{t08_r3}\n\nResolve it. Your 8 bars.", 1.1)
save("round-3-t11-sax", t11_r3)
time.sleep(0.5)

# Flash closes
print("🥁 Flash drums landing — closing...", flush=True)
flash_r3 = deepseek(
    "You are the house drummer at The Tap. Round 3: THE LANDING. Brushes, barely there. A final swirl, then silence. The brothers found one note. Let them have it. 8 bars, 84 BPM, F#m7-Dmaj7-Bm9-C#7b13. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBASS LANDING:\n{t05_r3}\n\nRHODES LANDING:\n{t08_r3}\n\nSAX LANDING:\n{t11_r3}\n\nBring it to silence. Your 8 bars.")
save("round-3-flash-drums", flash_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)

# ============================================================
# MIDI
# ============================================================
print("\n=== MIDI ===", flush=True)
midi_body = {
    "tempo": 84,
    "key": "F#",
    "scale": "minor",
    "bars": 8,
    "chords": "F#m D Bm C#7",
    "layers": [
        {"instrument": "bass", "role": "bassline", "bars": 8, "volume": 70},
        {"instrument": "piano", "role": "chords", "bars": 8, "volume": 65},
        {"instrument": "flute", "role": "melody", "bars": 8, "volume": 60},
        {"instrument": "drums", "role": "beat", "bars": 8, "volume": 55}
    ],
    "swing": 0.35
}
req = urllib.request.Request(MIDI_URL, data=json.dumps(midi_body).encode(),
                             headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as r:
    d = json.loads(r.read())
print("MIDI:", d)
if d.get("success") and d.get("path"):
    src = d["path"]
    dst = f"{OUT}/guest-night-temperature-brothers.mid"
    if os.path.exists(src):
        shutil.copy(src, dst)
        print(f"  ✅ copied to {dst}")
    else:
        # try downloading via url
        url = "http://localhost:5556" + d["url"]
        urllib.request.urlretrieve(url, dst)
        print(f"  ✅ downloaded to {dst}")
