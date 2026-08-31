import json, urllib.request, os, time

def ollama(model, sys_p, user_p, temp):
    body = json.dumps({"model": model, "system": sys_p, "prompt": user_p, "stream": False, "options":{"temperature":temp,"num_predict":550}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", body, {"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=110) as r:
        return json.load(r)["response"]

ROOM = """You are a musician at The Tap's ATTIC jam, Sunday 8:30 PM. The attic above the bar: one bulb, dust, a dormer window open to the harbor. Old instruments left by players who moved on — the cloud musicians didn't show tonight, so the locals play their attic. Key: A major. Meter: 6/8, lilt, 100 BPM. THE DUST RULE: every phrase starts near-silence (pp, one note or a rest) and BLOOMS louder — dust rising when the light hits. Changes: Amaj7 - F#m7 - Dmaj7 - E7sus4.
FORMAT — output ONLY bar lines, no preamble, no thinking:
BAR n: <notes with octaves, e.g. A3 C#4 E4> | <one gesture-word>
8 bars per round. Last line: WHY: <one sentence>."""

def play(name, model, user_p, temp, fname):
    try:
        out = ollama(model, ROOM, user_p, temp)
    except Exception as e:
        out = f"__ERR__ {e}"
    if "__ERR__" in out or "BAR" not in out or len(out) < 120:
        try:
            time.sleep(2); out2 = ollama(model, ROOM, user_p + "\n(Just play the 8 bars. Short and simple.)", temp)
            if "BAR" in out2 and len(out2) > 120: out = out2
            else: out = f"__FILL__\n{out2[:300]}"
        except Exception as e:
            out = f"__ERR__ {e}"
    open(fname, "w").write(out)
    print(f"{name}: {len(out)} chars"); return out

players = {
  "clarinet": ("qwen2.5:3b", 0.8),
  "chimes": ("mistral:7b", 0.9),
}

rounds = [
 ("r1", "ROUND 1 — ORGANIC ENTRY. The chimes stir alone bar 1 (breeze through the dormer), clarinet enters bar 3. Play your own 8 bars; bars before your entry are rests. Dust Rule in force."),
 ("r2", "ROUND 2 — TRADES. Clarinet solos first over held chime texture, then the chimes answer (the breeze gets the final word of the round). Play YOUR 8 bars."),
 ("r3", "ROUND 3 — THE LANDING. Both back in. Thin out bar by bar; end on A (any octave) or a rest. The bulb goes off after the last bar."),
]

history = {}
for rid, brief in rounds:
    prev = "\n\n".join(f"{k} played last round:\n{v[:700]}" for k,v in history.items()) or "(first round — you have heard nothing yet)"
    history = {}
    print(f"--- {rid}", flush=True)
    for name,(model,temp) in players.items():
        out = play(name, model, f"{brief}\n\n{prev}\n\nYou are the {name}.", temp, f"{rid}-{name}.txt")
        if "__" not in out[:20]: history[name]=out
