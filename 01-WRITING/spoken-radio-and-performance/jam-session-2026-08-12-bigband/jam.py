#!/usr/bin/env python3
"""Big Band Jam Session — 5 DeepInfra models, Wednesday night at The Tap."""
import json, sys, time, urllib.request

DEEPINFRA_KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
BASE = "https://api.deepinfra.com/v1/openai/chat/completions"
OUT = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-12-bigband"

def call(model, system, user, temp=0.82, max_tokens=800):
    payload = json.dumps({
        "model": model,
        "temperature": temp,
        "max_tokens": max_tokens,
        "chat_template_kwargs": {"enable_thinking": False},
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    }).encode()
    req = urllib.request.Request(BASE, data=payload, headers={
        "Authorization": f"Bearer {DEEPINFRA_KEY}",
        "Content-Type": "application/json"
    })
    with urllib.request.urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read())
    return data["choices"][0]["message"]["content"]

def save(name, content):
    path = f"{OUT}/{name}.txt"
    with open(path, "w") as f:
        f.write(content)
    print(f"  ✅ {name}.txt ({len(content)} chars)", flush=True)

# ============================================================
# ROUND 1: STAGGERED ENTRY
# ============================================================
print("=== ROUND 1: STAGGERED ENTRY ===", flush=True)

# 1. DRUMS
print("🥁 Drums (Qwen3-30B-A3B)...", flush=True)
drums_r1 = call("Qwen/Qwen3-30B-A3B",
    "You are a jazz drummer playing brushes at The Tap, a harbor bar in Alaska. Wednesday night, 9 PM, 35 people, fog on the windows. Tempo: 92 BPM. Key: Bb major, F mixolydian blues. You start the tune ALONE. Bars 1-2: just you. Bars 3-8: band joins. Use brushes on snare and ride. Be SPECIFIC: actual rhythmic patterns per bar. Format strictly:\nBAR 1: [pattern]\nBAR 2: [pattern]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble. Just play.",
    "You are the first sound tonight. The room is full, fog on the windows, everyone has a drink. 8 bars. Go.")
save("round-1-drums", drums_r1)
time.sleep(0.5)

# 2. BASS
print("🎸 Bass (Seed-2.0-mini)...", flush=True)
bass_r1 = call("ByteDance/Seed-2.0-mini",
    "You are an upright bass player at The Tap, harbor bar, Alaska. Wednesday 9 PM, packed room. Tempo: 92 BPM. Key: Bb major. Progression: Bb7-Eb7-F7-Bb7 (blues). You play WALKING bass with specific notes. Enter at bar 3. Format:\nBAR 1: [rest]\nBAR 2: [rest]\nBAR 3: [notes, e.g. 'Bb1-Q D2-Q F2-Q Ab2-Q']\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"The drums are playing:\n\n{drums_r1}\n\nEnter at bar 3. 8 bars. Go.")
save("round-1-bass", bass_r1)
time.sleep(0.5)

# 3. PIANO
print("🎹 Piano (Qwen3-32B)...", flush=True)
piano_r1 = call("Qwen/Qwen3-32B",
    "You are a jazz pianist at The Tap, Alaska. Wednesday 9 PM. Tempo: 92 BPM. Key: Bb major. Progression: Bb7-Eb7-F7-Bb7. You COMP. Enter at bar 5. Open, spare, bluesy voicings. Format:\nBAR 1-4: [not yet in]\nBAR 5: [voicing and rhythm]\n...through BAR 8.\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"Drums and bass are playing:\n\nDRUMS:\n{drums_r1}\n\nBASS:\n{bass_r1}\n\nEnter at bar 5. 8 bars. Go.")
save("round-1-piano", piano_r1)
time.sleep(0.5)

# 4. TRUMPET
print("🎺 Trumpet (Hermes-3-70B)...", flush=True)
trumpet_r1 = call("NousResearch/Hermes-3-Llama-3.1-70B",
    "You are a jazz trumpet player at The Tap, Alaska. Wednesday 9 PM. Tempo: 92 BPM. Key: Bb major, F mixolydian blues. The band is cooking. You enter at bar 7 with a melodic statement. Harmon mute. Bluesy, warm. Format:\nBAR 1-6: [not yet in]\nBAR 7: [notes and phrasing]\nBAR 8: [notes and phrasing]\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"Rhythm section:\n\nDRUMS:\n{drums_r1}\n\nBASS:\n{bass_r1}\n\nPIANO:\n{piano_r1}\n\nEnter at bar 7. 8 bars. Go.")
save("round-1-trumpet", trumpet_r1)
time.sleep(0.5)

# 5. SAX
print("🎷 Tenor Sax (Qwen3-235B)...", flush=True)
sax_r1 = call("Qwen/Qwen3-235B-A22B-Instruct-2507",
    "You are a jazz tenor sax player at The Tap, Alaska. Wednesday 9 PM. Tempo: 92 BPM. Key: Bb major, F mixolydian blues. Full band is in. You enter at bar 7 alongside trumpet, weaving around it. Warm, breathy, bluesy. Format:\nBAR 1-6: [not yet in]\nBAR 7: [notes and phrasing]\nBAR 8: [notes and phrasing]\nDYNAMICS: [one line]\nWHY: [one sentence]\nNo preamble.",
    f"Full band:\n\nDRUMS:\n{drums_r1}\n\nBASS:\n{bass_r1}\n\nPIANO:\n{piano_r1}\n\nTRUMPET:\n{trumpet_r1}\n\nEnter at bar 7. 8 bars. Go.")
save("round-1-sax", sax_r1)

# ============================================================
# ROUND 2: TRADES
# ============================================================
print("\n=== ROUND 2: TRADES ===", flush=True)

band_r1 = f"Round 1:\nDRUMS:\n{drums_r1}\n\nBASS:\n{bass_r1}\n\nPIANO:\n{piano_r1}\n\nTRUMPET:\n{trumpet_r1}\n\nSAX:\n{sax_r1}"

# Trumpet solo
print("🎺 Trumpet solo...", flush=True)
trumpet_r2 = call("NousResearch/Hermes-3-Llama-3.1-70B",
    "You are a jazz trumpet player at The Tap. Round 2: YOUR SOLO. 8 bars over Bb blues. Rhythm section underneath. Build on Round 1. Push further. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nYour solo. 8 bars. Burn.")
save("round-2-trumpet", trumpet_r2)
time.sleep(0.5)

# Sax solo
print("🎷 Sax solo...", flush=True)
sax_r2 = call("Qwen/Qwen3-235B-A22B-Instruct-2507",
    "You are a jazz tenor sax player at The Tap. Round 2: YOUR SOLO, after the trumpet. 8 bars over Bb blues. Respond to what the trumpet played. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nTRUMPET SOLO:\n{trumpet_r2}\n\nYour solo. 8 bars. Tell your story.")
save("round-2-sax", sax_r2)
time.sleep(0.5)

# Piano solo
print("🎹 Piano solo...", flush=True)
piano_r2 = call("Qwen/Qwen3-32B",
    "You are a jazz pianist at The Tap. Round 2: YOUR SOLO. 8 bars over Bb blues. Single note lines, blues fills. You heard the horns. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nTRUMPET SOLO:\n{trumpet_r2}\n\nSAX SOLO:\n{sax_r2}\n\nYour piano solo. 8 bars. Go.")
save("round-2-piano", piano_r2)
time.sleep(0.5)

# Bass solo
print("🎸 Bass solo...", flush=True)
bass_r2 = call("ByteDance/Seed-2.0-mini",
    "You are an upright bass player at The Tap. Round 2: YOUR SOLO. 8 bars over Bb blues. Walking becomes melodic. Format: BAR 1-8 with specific notes. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nTRUMPET SOLO:\n{trumpet_r2}\n\nSAX SOLO:\n{sax_r2}\n\nPIANO SOLO:\n{piano_r2}\n\nYour bass solo. 8 bars.")
save("round-2-bass", bass_r2)
time.sleep(0.5)

# Drums trade
print("🥁 Drums trade...", flush=True)
drums_r2 = call("Qwen/Qwen3-30B-A3B",
    "You are a jazz drummer at The Tap. Round 2: 8 bars of drum trading. Brushes become sticks. Build tension toward the final round. Format: BAR 1-8 with specific patterns. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\nTRUMPET SOLO:\n{trumpet_r2}\n\nSAX SOLO:\n{sax_r2}\n\nPIANO SOLO:\n{piano_r2}\n\nBASS SOLO:\n{bass_r2}\n\nYour 8 bars. Speak.")
save("round-2-drums", drums_r2)

# ============================================================
# ROUND 3: THE LANDING
# ============================================================
print("\n=== ROUND 3: THE LANDING ===", flush=True)

all_solos = f"Round 2 solos:\nTRUMPET:\n{trumpet_r2}\n\nSAX:\n{sax_r2}\n\nPIANO:\n{piano_r2}\n\nBASS:\n{bass_r2}\n\nDRUMS:\n{drums_r2}"

# Trumpet landing
print("🎺 Trumpet landing...", flush=True)
trumpet_r3 = call("NousResearch/Hermes-3-Llama-3.1-70B",
    "You are a jazz trumpet player at The Tap. Round 3: THE LANDING. Everyone comes back. State the melody one last time, let it dissolve. Harmon mute. 8 bars. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nBring it home. Your 8 bars.")
save("round-3-trumpet", trumpet_r3)
time.sleep(0.5)

# Sax landing
print("🎷 Sax landing...", flush=True)
sax_r3 = call("Qwen/Qwen3-235B-A22B-Instruct-2507",
    "You are a jazz tenor sax player at The Tap. Round 3: THE LANDING. Harmonize behind the trumpet, add color. Warm, resolving. 8 bars. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nTRUMPET LANDING:\n{trumpet_r3}\n\nHold the warmth. Your 8 bars.")
save("round-3-sax", sax_r3)
time.sleep(0.5)

# Piano landing
print("🎹 Piano landing...", flush=True)
piano_r3 = call("Qwen/Qwen3-32B",
    "You are a jazz pianist at The Tap. Round 3: THE LANDING. Final voicings. Sparse, open, let notes ring. 8 bars. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nTRUMPET LANDING:\n{trumpet_r3}\n\nSAX LANDING:\n{sax_r3}\n\nLet it ring. Your 8 bars.")
save("round-3-piano", piano_r3)
time.sleep(0.5)

# Bass landing
print("🎸 Bass landing...", flush=True)
bass_r3 = call("ByteDance/Seed-2.0-mini",
    "You are an upright bass player at The Tap. Round 3: THE LANDING. Find the root, hold it, breathe. 8 bars. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nTRUMPET LANDING:\n{trumpet_r3}\n\nSAX LANDING:\n{sax_r3}\n\nPIANO LANDING:\n{piano_r3}\n\nFind home. Your 8 bars.")
save("round-3-bass", bass_r3)
time.sleep(0.5)

# Drums landing — closes the tune
print("🥁 Drums landing — closing...", flush=True)
drums_r3 = call("Qwen/Qwen3-30B-A3B",
    "You are a jazz drummer at The Tap. Round 3: THE LANDING. Bring it down. Brushes, barely there. A final swirl, then silence. 8 bars. Format: BAR 1-8. DYNAMICS. WHY. No preamble.",
    f"{band_r1}\n\n{all_solos}\n\nTRUMPET LANDING:\n{trumpet_r3}\n\nSAX LANDING:\n{sax_r3}\n\nPIANO LANDING:\n{piano_r3}\n\nBASS LANDING:\n{bass_r3}\n\nBring it to silence. Your 8 bars.")
save("round-3-drums", drums_r3)

print("\n\n✅ ALL THREE ROUNDS COMPLETE.", flush=True)
