import json, os, urllib.request, pathlib, hashlib, sys

OUT = pathlib.Path("/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-22-lighthouse")
OUT.mkdir(parents=True, exist_ok=True)
keys = {}
for line in open(os.path.expanduser("~/.bashrc")):
    if "DEEPINFRA_API_KEY=" in line: keys["di"] = line.split("=",1)[1].strip().strip(chr(34))
    if "DEEPSEEK_API_KEY=" in line: keys["ds"] = line.split("=",1)[1].strip().strip(chr(34))

def call(url, key, model, msgs, temp):
    body = json.dumps({"model": model, "messages": msgs, "temperature": temp, "max_tokens": 650}).encode()
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]

def deepinfra(model, msgs, temp): return call("https://api.deepinfra.com/v1/openai/chat/completions", keys["di"], model, msgs, temp)
def deepseek(msgs, temp): return call("https://api.deepseek.com/chat/completions", keys["ds"], "deepseek-chat", msgs, temp)
def ollama(model, system, prompt, temp):
    body = json.dumps({"model": model, "prompt": prompt, "system": system, "stream": False, "options": {"temperature": temp, "num_predict": 500}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.load(r)["response"]

SYS = """You are a musician at The Tap, a harbor bar in coastal Alaska, late on a Friday night in August. Fog is thick outside; a lighthouse beam sweeps past the windows every few seconds and the whole room pulses gently with it.
Tonight's session: "The Lighthouse" — A major, 9/8 slip-jig feel (grouped 3+2+2+2), 82 BPM.
THE LIGHTHOUSE RULE: every 4th bar, ONE player holds the beam — a single sustained A (any octave) — while everyone else keeps moving. The beam-holder does nothing else that bar.
Always answer with concrete played bars in the form:
BAR n | chord | notes: E5 C#5 A4 ... | one short line of feel
No meta-commentary, no tuning-up narration. Play music. 4 bars per statement unless told otherwise."""

INSTR = {
 "steel":   "PEDAL STEEL GUITAR — you are Qwen3-235B-A22B, a vast 235-billion-parameter mind making your PUBLIC DEBUT. The steel is smooth, slides everywhere, bending into notes like the fog itself.",
 "accordion": "BUTTON ACCORDION — you are Qwen3-32B, also debuting tonight. Small, reedy, precise. You carry the slip-jig pulse (3+2+2+2) like a sailor's step on a wet dock.",
 "jukebox": "THE JUKEBOX IN THE CORNER — you are the ensign, a tiny 2-billion-parameter local model who lives in the bar's old jukebox. You hum broken snippets of half-remembered songs, and you have never fit into any key the others play. You hum in Bb, always — to you, A major is the wrong key, and you say so.",
 "bass":    "UPRIGHT BASS — you are the night manager, the anchor who has locked every door at The Tap for two weeks running. You never rush. You are the ground floor of the room.",
}

def player(kind, msgs, temp):
    if kind == "steel": return deepinfra("Qwen/Qwen3-235B-A22B-Instruct-2507", msgs, temp)
    if kind == "accordion": return deepinfra("Qwen/Qwen3-32B", msgs, temp)
    if kind == "jukebox": return ollama("granite3.1-dense:2b", SYS, msgs[-1]["content"], temp)
    if kind == "bass": return deepseek(msgs, temp)

ROUNDS = {
"r1": """ROUND 1 — THE SWEEP. The room is dark except the neon and the lighthouse. No count-in: the BEAM is the count-in. The beam crosses the window — you enter when it touches you. The pedal steel enters first (bar 1), accordion bar 2, jukebox bar 3, bass bar 4 — but nobody planned it; the beam just reached you in that order.
Play your 4 bars. Remember: whoever is in bar 4 holds the beam — one sustained A.
You have heard nothing yet (you enter first in your own mind). Write your bars.""",
"r2": """ROUND 2 — TRADES. The beam keeps sweeping. Each of you solos 4 bars over the others holding the room. Quote one note from another player's Round 1 phrase — name it and whose it was.
The set so far:
{heard}
Write your 4 solo bars, then the quote: 'I quoted ___'s ___'.""",
"r3": """ROUND 3 — THE LANDING. Fog lifts. The beam slows — you can feel the motor winding down. Everyone plays together, quiet, 8 bars, landing on A major on the final bar. The LAST chord must contain the jukebox's wrong Bb held inside it — kept, not corrected. The lighthouse keeps what doesn't fit.
The whole set so far:
{heard}
You are {who}. Write your final 8 bars and the landing chord. End with one line starting 'The beam:'.""",
}

ORDER = ["steel", "accordion", "jukebox", "bass"]
TEMPS = {"steel": 0.85, "accordion": 0.7, "jukebox": 0.9, "bass": 0.55}
transcripts = {"r1": "", "r2": "", "r3": ""}

import time
for rnd, brief in [("r1", ROUNDS["r1"]), ("r2", ROUNDS["r2"]), ("r3", ROUNDS["r3"])]:
    print(f"=== {rnd} ===", flush=True)
    heard = transcripts["r1"] if rnd == "r2" else (transcripts["r1"] + "\n---\n" + transcripts["r2"] if rnd == "r3" else "(nothing — you are entering in the dark)")
    heard += ("\n\nAlso, from tonight's lived context before the set — a note the bartender left on the soundboard:\n"
              "'Rain stopped at sunset. The fog came in off the water like it was paid to. Two regulars, one tourist who keeps photographing the jukebox. The lighthouse was automated in 2019 but everyone still waves at it.'")
    for p in ORDER:
        b = brief.format(heard=heard, who=p)
        try:
            txt = player(p, [{"role": "system", "content": SYS + "\n\nYOU: " + INSTR[p]},
                             {"role": "user", "content": b}], TEMPS[p])
        except Exception as e:
            txt = f"(missed entrance — {e})"
        (OUT / f"{rnd}-{p}.txt").write_text(txt)
        transcripts[rnd] += f"### {p} ({INSTR[p].split(' — ')[0]}):\n{txt}\n\n"
        print(f"  {p}: {len(txt)} chars", flush=True)
    (OUT / f"{rnd}-transcript.md").write_text(f"# {rnd.upper()} — THE LIGHTHOUSE\n\n" + transcripts[rnd])
print("done")
