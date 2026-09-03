import json, urllib.request, sys, time, pathlib

OLLAMA = "http://localhost:11434/api/generate"
D = pathlib.Path(__file__).parent

PLAYERS = [
    ("qwen3:8b", "harmonium", 0.85),
    ("Liquid-LFM2.5-2.6B", "hammered dulcimer (GUEST — first night at The Tap)", 0.9),
    ("deepseek-r1:8b", "upright bass", 0.8),
]

def call(model, prompt, temp):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False,
                       "options": {"temperature": temp, "num_predict": 500}}).encode()
    req = urllib.request.Request(OLLAMA, data=body, headers={"Content-Type": "application/json"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=150) as r:
            out = json.loads(r.read()).get("response", "")
    except Exception as e:
        out = f"__ERR__ {e}"
    return out.strip(), int(time.time()-t0)

def cond(instrument):
    return f"""TONIGHT AT THE TAP — MONDAY, THE BOILER ROOM (basement, steam heat, copper pipes overhead, one red bulb).
You play the {instrument}.
KEY: D DORIAN (D E F G A B C — naturals ONLY, no sharps no flats). Allowed notes: D2 D3 E3 F3 G3 A3 B3 C4 D4 E4 F4 G4 A4 B4 C5 D5.
METER: 5/4 — FIVE beats per bar. Each bar = exactly 5 comma-separated notes (a held rest is "p").
TEMPO: 96 BPM, slow boil. CHANGES per bar: Dm7 | G7 | Bbmaj7 | A7sus | Dm7 | G7 | Bbmaj7 | A7sus.
THE STEAM RULE: intensity rises one notch per bar until bar 5, then hold steady. Pipes ticking. Monday crowd of twelve, nobody talking.

FORMAT (STRICT, exactly 8 bars, nothing else):
BAR 1: note, note, note, note, note | mood-word
...
BAR 8: ...
WHY: <one sentence>"""

ROUNDS = [
    ("ROUND 1 — THE SLOW BOIL. Organic entry: establish the room. If you are the first voice, bar 1 is a count-in: D3 five times.",
     1.0),
    ("ROUND 2 — TRADES. This is your solo. Bars 1-4 you step out front, bars 5-8 you hand it back and comp for the others.",
     1.0),
    ("ROUND 3 — THE LANDING. Everyone eases off. By bar 8 all three of you arrive together on a low D. End on D.", 1.0),
]

for rn, (rdesc, _) in enumerate(ROUNDS, 1):
    heard = []
    for model, instr, temp in PLAYERS:
        prev = "\n\n".join(heard) if heard else "You are the first voice tonight. Nobody has played yet."
        prompt = f"{cond(instr)}\n\n{rdesc}\n\nWHAT YOU HAVE HEARD SO FAR THIS ROUND:\n{prev if prev.strip() else '(silence — you open)'}\n\nPlay NOW:"
        out, secs = call(model, prompt, temp)
        print(f"=== r{rn} | {instr} | {model} ({secs}s) ===")
        print(out[:900])
        (D / f"r{rn}-{instr.split()[0]}.txt").write_text(out)
        heard.append(f"[{instr}]\n{out}")
print("DONE")
