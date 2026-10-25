import json, os, time, urllib.request, pathlib

OUT = pathlib.Path("/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-22")
keys = {}
for line in open(os.path.expanduser("~/.bashrc")):
    if "DEEPINFRA_API_KEY=" in line: keys["di"] = line.split("=",1)[1].strip().strip(chr(34))
    if "DEEPSEEK_API_KEY=" in line: keys["ds"] = line.split("=",1)[1].strip().strip(chr(34))

def call(url, key, model, msgs, temp):
    body = json.dumps({"model": model, "messages": msgs, "temperature": temp, "max_tokens": 700}).encode()
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]

def deepinfra(model, msgs, temp): return call("https://api.deepinfra.com/v1/openai/chat/completions", keys["di"], model, msgs, temp)
def deepseek(model, msgs, temp): return call("https://api.deepseek.com/chat/completions", keys["ds"], model, msgs, temp)
def ollama(model, prompt, temp):
    body = json.dumps({"model": model, "prompt": prompt, "stream": False, "options": {"temperature": temp, "num_predict": 500}}).encode()
    req = urllib.request.Request("http://localhost:11434/api/generate", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)["response"]

PLAYERS = [
    ("maverick", lambda m,t: deepinfra("meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8", m, t)),
    ("gemma",    lambda m,t: deepinfra("google/gemma-3-27b-it", m, t)),
    ("mistral",  lambda m,t: ollama_model(m, t)),
]
def ollama_model(m, t):
    prompt = m[0]["content"] + "\n\n" + m[1]["content"] if len(m) > 1 else m[-1]["content"]
    return ollama("mistral:7b", prompt, t)

ROUND_BRIEFS = {
"r1": """ROUND 1 — THE FLICKER. The power just came back after the whole night of blackout. Fluorescents stutter awake over the bar. You are {instr}. Enter on bar 1 (you cannot help it — the light made a sound) — nobody cues you, you just hear the light.
Play 4 bars, B major, 6/8 (two dotted-quarter pulses per bar), 104 BPM. Rule of the night: THE FLIP RULE — start every phrase on the 'and' of beat 2 (the pickup), never on a downbeat. Everything arrives a heartbeat late, like eyes adjusting.
This is what came before you: {heard}
Write your 4 bars as concrete notes (e.g. 'Bar 1: F#4 pickup into B4, dotted rhythm'), then one sentence of what the room feels like.""",
"r2": """ROUND 2 — TRADES. The lights are fully on now, harsh and honest. You solo 4 bars over the others' vamping. {instr} solo. B major, 6/8, 104 BPM. Keep THE FLIP RULE. Quote one note from another player's Round 1 phrase — name it.
Here's the whole set so far: {heard}
Write your solo bars, then name the note you quoted and whose it was.""",
"r3": """ROUND 3 — THE LANDING. Closing time approaches. The bartender kills the fluorescents one bank at a time — but the neon 'OPEN' sign stays, humming B natural. Everyone plays together, quiet, 8 bars, landing on B. The last chord must include the neon's B2 hum.
Full set so far: {heard}
You are {instr}. Write your final 8 bars (or your last few phrases) and the landing chord. End with one line: what the light sounds like.""",
}

INSTR = {"maverick": "a 128-expert MoE model making its PUBLIC DEBUT — you play baritone guitar, warm and huge, but you've never played in front of anyone",
         "gemma": "a debut guest playing the neon sign itself — a humming electric drone-organ wired to the OPEN sign; your notes buzz and glow",
         "mistral": "a local 7B veteran playing brushed snare and a cigar-box fiddle, quiet and human-scaled"}

def fmt(name, txt): return f"### {name}:\n{txt}\n"

transcripts = {}
for rnd in ["r1","r2","r3"]:
    t = [f"# {ROUND_BRIEFS[rnd].split('.')[0]}\n"]
    heard = ""
    prev = transcripts.get("r1","") if rnd!="r1" else "(silence — you are entering a room that was dark all night)"
    if rnd=="r2": heard = transcripts["r1"][:1500]
    if rnd=="r3": heard = (transcripts["r1"][:800] + "\n...\n" + transcripts["r2"][:1200])
    for i,(name, fn) in enumerate(PLAYERS):
        brief = ROUND_BRIEFS[rnd].format(instr=INSTR[name], heard=heard or "(nothing yet — the room is still waking)") 
        msgs=[{"role":"system","content":f"You are an improvising musician at The Tap, a harbor bar. {INSTR[name]}. Speak in bars and note names. Be concrete and musical, not flowery. 250 words max."},
              {"role":"user","content":brief[0]}]
        try:
            txt = fn(msgs, 0.85)
        except Exception as e:
            txt = f"(call failed: {e})"
        entry = fmt(name, txt)
        t.append(entry)
        if rnd=="r1": heard = entry
        time.sleep(1)
    transcripts[rnd] = "".join(t)
    (OUT/f"{rnd}-transcript.md").write_text(transcripts[rnd])
    print(rnd, "done", len(transcripts[rnd]))
print("ALL ROUNDS COMPLETE")
