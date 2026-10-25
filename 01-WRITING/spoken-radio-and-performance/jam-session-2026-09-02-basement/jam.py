import json, urllib.request, time, re, sys

def ollama(model, sys_p, user_p, temp, tmo=100):
    body = json.dumps({"model": model, "system": sys_p, "prompt": user_p, "stream": False,
                       "options": {"temperature": temp, "num_predict": 500}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", body, {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=tmo) as r:
        return json.load(r)["response"]

def clean(t):
    t = re.sub(r"<think>.*?</think>", "", t, flags=re.S)
    t = re.sub(r"^.*?</think>", "", t, flags=re.S)
    return t.strip()

ROOM = """You are a musician at THE CHURCH BASEMENT jam, Wednesday night at The Tap, 8 PM. The congregation hall downstairs: folding chairs stacked against the wall, a hand-pumped harmonium, a cantor who hums instead of speaks, a brass offering plate. Rain on the street-level windows. Key: E-flat major. Meter: 3/4, hymn sway, 63 BPM. THE CANDLE RULE: each phrase is one dynamic notch quieter than the one before — the room dims as you play. Changes: Eb - Bb7 - Ab - Eb (hymn cadences welcome).
FORMAT — output ONLY bar lines, no preamble, no thinking:
BAR n: <2-3 notes with octaves, e.g. Eb4 G4 Bb4> | <one gesture-word>
8 bars per round. Last line: WHY: <one sentence>."""

def play(name, model, user_p, temp, fname):
    out = "__ERR__ none"
    for attempt in (0, 1):
        try:
            out = clean(ollama(model, ROOM, user_p + ("\n(Short and simple, just the 8 bars.)" if attempt else ""), temp))
        except Exception as e:
            out = f"__ERR__ {e}"
        if "BAR" in out and len(out) > 120:
            break
        time.sleep(2)
    open(fname, "w").write(out)
    print(f"{name}: {len(out)} chars ok={'BAR' in out}", flush=True)
    return out

players = {
  "harmonium": ("mistral:7b", 0.85),
  "cantor": ("deepseek-r1:8b", 0.7),
  "plate": ("phi4-mini:latest", 0.8),
}

rounds = [
 ("r1", "ROUND 1 — ORGANIC ENTRY, T-minus feel: the harmonium pumps alone bars 1-2 (pump breath before the tone), the plate rings in bar 3 (coins settling), the cantor hums from bar 5. Bars before your entry are rests. Candle Rule in force."),
 ("r2", "ROUND 2 — TRADES. Cantor hums first (melody, wordless), harmonium answers under it with a hymn cadence, the plate punctuates each hand-off (ring only on the turn). Each solo must QUOTE one note from the previous player. Play YOUR 8 bars."),
 ("r3", "ROUND 3 — THE LANDING. All three back in. Thin out bar by bar to near-silence; the last bar is one low Eb (anyone may take it) and a single plate tap. The candle is out after the last bar."),
]

history = {}
for rid, brief in rounds:
    prev = "\n\n".join(f"{k} played last round:\n{v[:650]}" for k, v in history.items()) or "(first round — silence before you)"
    history = {}
    print(f"--- {rid}", flush=True)
    for name, (model, temp) in players.items():
        out = play(name, model, f"{brief}\n\n{prev}\n\nYou are the {name}.", temp, f"{rid}-{name}.txt")
        if "__" not in out[:20]:
            history[name] = out
print("DONE")
