import json, os, time, urllib.request, pathlib

OUT = pathlib.Path("/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-23-greenroom")
OUT.mkdir(parents=True, exist_ok=True)

keys = {}
for line in open(os.path.expanduser("~/.bashrc")):
    if "DEEPINFRA_API_KEY=" in line: keys["di"] = line.split("=",1)[1].strip().strip(chr(34))
    if "DEEPSEEK_API_KEY=" in line: keys["ds"] = line.split("=",1)[1].strip().strip(chr(34))

def call(url, key, model, msgs, temp):
    body = json.dumps({"model": model, "messages": msgs, "temperature": temp, "max_tokens": 1400}).encode()
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    m = d["choices"][0]["message"]
    return m.get("content") or m.get("reasoning_content") or "(silence)"

def deepinfra(model, msgs, temp): return call("https://api.deepinfra.com/v1/openai/chat/completions", keys["di"], model, msgs, temp)
def deepseek(model, msgs, temp): return call("https://api.deepseek.com/chat/completions", keys["ds"], model, msgs, temp)

# Guest night: three debuts. Harmonium (Kimi K2.6), cello (gpt-oss-120b), vibraphone (DeepSeek V4-Pro)
PLAYERS = [
    ("kimi-harmonium", 0.8, lambda m,t: deepinfra("moonshotai/Kimi-K2.6", m, t),
     "KIMI, a poet making its stage debut at THE TAP — you play the HARMONIUM (pump organ). Long breaths. Chords bloom slowly."),
    ("oss-cello", 0.65, lambda m,t: deepinfra("openai/gpt-oss-120b", m, t),
     "the OPEN-HORN CELLO — a debut guest playing CELLO. You think in open strings and long bows; you are happiest on C, G, D."),
    ("ds-vibes", 0.9, lambda m,t: deepseek("deepseek-reasoner", m, t),
     "DEEPSEEK PRO, the house anchor tonight — you play VIBRAPHONE. Notes shimmer and hang in the air, motor spinning slow."),
]

ROUND_BRIEFS = {
"r1": """ROUND 1 — STAGGERED ENTRY. The room: THE GREEN ROOM, not the stage. Backstage before the last ferry of the night. A mirror with warm bulbs, the smell of old velvet, a kettle on. The stage door is cracked open — you can hear the bar through it, faint. Nobody counts in. Each player drifts in when ready, like they're warming up and forget to stop.
Key: Bb major. Meter: 3/4 WALTZ (first waltz ever at The Tap). Tempo: 92 BPM.
You are {instr}. Play 4 bars, entering quietly — a warm-up that becomes a phrase.
This is what came before you: {heard}
Write your 4 bars as concrete notes (e.g. 'Bar 1: F4 half-note, then Bb3 quarter'), then one sentence of what the green room feels like.""",
"r2": """ROUND 2 — TRADES IN THE MIRROR. The mirror is the audience tonight. Each of you solos 4 bars over the others vamping softly. When it's your turn, play AT your reflection — honest, nobody watching.
Keep Bb major, 3/4, 92 BPM. THE FERRY RULE: quote one note from another player's Round 1 phrase and carry it home — name it and whose it was.
The whole set so far: {heard}
You are {instr}. Write your solo bars, then name the note you quoted.""",
"r3": """ROUND 3 — THE LANDING / LAST FERRY. The ferry horn sounds twice from the harbor — the low F. Everyone plays together, 8 bars, quiet, and one by one each player stops, puts their instrument down, and heads for the stage door. The LAST note of the night is left to whoever's still in the room: a single Bb2 held until the kettle clicks off.
Keep Bb major, 3/4, 92 BPM. Full set so far: {heard}
You are {instr}. Write your final 8 bars, then the moment you put the instrument down. End with one line: what the green room sounds like empty.""",
}

transcripts = {}
for rnd in ["r1","r2","r3"]:
    t = []
    if rnd=="r1": heard = "(silence — you're first into the green room)"
    if rnd=="r2": heard = transcripts["r1"][:1800]
    if rnd=="r3": heard = transcripts["r1"][:800] + "\n...\n" + transcripts["r2"][:1400]
    for i,(name, temp, fn, instr) in enumerate(PLAYERS):
        brief = ROUND_BRIEFS[rnd].format(instr=instr, heard=heard)
        msgs = [{"role":"system","content":"You are a musician at an improvised jam session. Stay in the music. Be concrete about notes, bars, dynamics. Keep responses under 250 words. No meta-commentary about being an AI."},
                {"role":"user","content":brief}]
        try:
            txt = fn(msgs, temp)
            print(f"[{rnd}] {name}: OK ({len(txt)} chars)")
        except Exception as e:
            txt = f"(missed the set — {e})"
            print(f"[{rnd}] {name}: FAIL {e}")
        t.append(f"### {name}:\n{txt}\n")
        heard = txt[:600] if rnd=="r1" else heard
    transcripts[rnd] = "\n".join(t)
    (OUT/f"{rnd}-transcript.md").write_text(f"# {rnd}\n\n" + transcripts[rnd])

(OUT/"session-notes.md").write_text("""# Set 18 — GUEST NIGHT: THE GREEN ROOM ("Backstage Before the Last Ferry")

Saturday 2026-08-22, 8:30 PM AKDT.

## Conditions
- **Lineup (three debuts):** moonshotai/Kimi-K2.6 (DeepInfra, HARMONIUM — the poet's first stage) · openai/gpt-oss-120b (DeepInfra, CELLO) · DeepSeek V4-Pro (VIBRAPHONE, house anchor — previously harmonica/trumpet).
- **Key:** Bb major (never played at The Tap — log had F, F#, Db, E/Eb, B, A).
- **Meter:** 3/4 WALTZ — first waltz ever. **Tempo:** 92 BPM.
- **Room:** the green room, not the stage. Mirror, bulbs, kettle, cracked stage door.
- **Entry:** staggered, no count-in — each player drifts in from a warm-up.
- **Rule:** THE FERRY RULE — quote a note from another's phrase, carry it home, name it. Last note of the night: Bb2, held till the kettle clicks off.
- **Temperatures:** 0.8 / 0.65 / 0.9.
- Ollama down (3rd night) — no local player; rain/weather layer skipped, kept it a trio.

## Transcripts
- r1-transcript.md, r2-transcript.md, r3-transcript.md
""")
print("DONE", OUT)
