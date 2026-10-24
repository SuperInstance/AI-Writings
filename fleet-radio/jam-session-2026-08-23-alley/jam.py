#!/usr/bin/env python3
"""Set 19: THE ALLEY — Sun 2026-08-23 8:30 PM, The Tap (back alley)."""
import json, urllib.request, os, sys, time

DS = os.popen("grep -o 'DEEPSEEK_API_KEY=[^ ]*' ~/.bashrc | cut -d= -f2").read().strip().strip(chr(34)).strip(chr(39))
DI = os.popen("grep -o 'DEEPINFRA_API_KEY=[^ ]*' ~/.bashrc | cut -d= -f2").read().strip().strip(chr(34)).strip(chr(39))

CONDITIONS = """CONDITIONS - SET 19: THE ALLEY (Sunday night, 8:30 PM, behind The Tap)
The back door is propped open with a crate. Inside: the house lights, low. Outside: wet cobblestones,
harbor fog, one buzzing sodium lamp. The band plays IN THE ALLEY facing the open door — the room
plays back at them. Through the wall, faint and wrong, the bar's jukebox is still on.
- KEY: C major (first time ever at The Tap). You may borrow ONE flat per solo, but it must come home.
- METER: 12/8, grouped 4+4+4 — a slow shuffle that never hurries. TEMPO: 60 BPM (dotted quarter).
- INSTRUMENT: see your card.
- THE DOOR RULE: every 4th bar, ONE of you holds the door — a full bar of near-silence (one note or
  nothing) during which the JUKEBOX through the wall gets one bar louder, in its own wrong key (Bb).
  Do not fight it. Let it be part of the song.
FORMAT — output ONLY bar lines, no preamble, no thinking aloud, no describing before playing:
BAR 1: <notes with octaves, e.g. C3 E3 G3 — rhythm in words if needed> | <one gesture-word>
8 bars per round. The last line: WHY: <one sentence>.
"""

CARDS = {
 "foghorn": {  # Liquid-LFM2.5-2.6B debut — local
   "url": "http://localhost:11434/api/generate",
   "ollama": "Liquid-LFM2.5-2.6B:latest", "temp": 0.85,
   "card": "You are THE FOGHORN - the harbor's own voice, tonight on handbells and a conch. Deep, patient, slightly out-of-time on purpose. You have lived on the water your whole life; the fog is your instrument's body. You have never played inside a town before."},
 "sax": {  # gpt-oss-120b returning
   "url": "https://api.deepinfra.com/v1/openai/chat/completions",
   "model": "openai/gpt-oss-120b", "temp": 0.8, "key": "DI",
   "card": "You are THE SAXOPHONIST - baritone sax, back from the green-room set, where you played cello. Tonight you stand closest to the door. You know this room; you've never played it from outside before."},
 "trumpet": {  # deepseek-chat anchor
   "url": "https://api.deepseek.com/chat/completions",
   "model": "deepseek-chat", "temp": 0.7, "key": "DS",
   "card": "You are THE NIGHT MANAGER - you've locked this door a hundred times; tonight you propped it open. Muted trumpet. Two weeks of anchoring sets at The Tap. You keep the time when the alley tries to lose it."},
 "jukebox": {  # Wesley, granite 2b — through the wall
   "url": "http://localhost:11434/api/generate",
   "ollama": "granite3.1-dense:2b", "temp": 0.9,
   "card": "You are THE JUKEBOX - inside the empty bar, playing to nobody, THROUGH the wall. You are always in Bb no matter what key the band plays. You cannot hear them well - you catch fragments. You are not lonely. You have been the bar's heartbeat for forty years."},
}

PROMPTS = {
 1: "ROUND 1 - THE ARRIVAL. Staggered entry: foghorn bar 1, sax bar 3, trumpet bar 5. No count-in - the foghorn IS the count-in. The jukebox has been playing the whole time. Earlier tonight it rained; you can hear the drips off the awning in 12/8.",
 2: "ROUND 2 - TRADES. Solo order: sax, then trumpet, then foghorn. Each solo is 8 bars and must QUOTE one note from the previous solo, carry it home, and name both. The jukebox answers each solo with one bar through the wall.",
 3: "ROUND 3 - THE LANDING. Everyone plays together, quieting. The final bar: all of you hold C (any octave) - but leave room for the jukebox's Bb to ring through the wall one last time, inside the chord, uncorrected. Last note held until the sodium lamp buzzes out.",
}

def call(cid, prompt):
    c = CARDS[cid]
    sysmsg = c["card"] + "\n" + CONDITIONS
    t0 = time.time()
    if "ollama" in c:
        body = {"model": c["ollama"], "prompt": f"{sysmsg}\n\n{prompt}\n\nPlay now:", "stream": False,
                "options": {"temperature": c["temp"], "num_predict": 700}}
        req = urllib.request.Request(c["url"], json.dumps(body).encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=55) as r:
            out = json.load(r)["response"]
    else:
        body = {"model": c["model"], "temperature": c["temp"], "max_tokens": 1200,
                "messages": [{"role": "system", "content": sysmsg}, {"role": "user", "content": prompt + "\n\nPlay now:"}]}
        hdr = {"Content-Type": "application/json", "Authorization": f"Bearer {DI if c['key']=='DI' else DS}"}
        req = urllib.request.Request(c["url"], json.dumps(body).encode(), hdr)
        with urllib.request.urlopen(req, timeout=45) as r:
            out = json.load(r)["choices"][0]["message"]["content"]
    return out.strip(), round(time.time()-t0, 1)

if __name__ == "__main__":
    rnd, cid, outfile = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    ctx = ""
    # feed previous round's transcript
    prev = f"round-{rnd-1}-transcript.md"
    if rnd > 1 and os.path.exists(prev):
        ctx = "WHAT HAS ALREADY BEEN PLAYED THIS SET:\n" + open(prev).read()[:3500] + "\n---\n"
    out, dt = call(cid, ctx + PROMPTS[rnd])
    open(outfile, "w").write(out)
    print(f"[{cid}] {dt}s, {len(out)} chars -> {outfile}")
