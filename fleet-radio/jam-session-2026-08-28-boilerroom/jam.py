#!/usr/bin/env python3
"""SET 25: THE BOILER ROOM — noise night. contact-mic(DeepSeek Flash) + spring-tank(Qwen2.5-72B) + tape-loop(Liquid-LFM2.5 local)."""
import json, urllib.request

D = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-28-boilerroom"
DS_KEY = "sk-0a57cd44bc674f5caffd9b0ec10e284c"
DI_KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
CONDS = open(f"{D}/conds.txt").read()

def call_api(url, key, model, sysmsg, user, temp):
    body = json.dumps({"model": model, "temperature": temp, "max_tokens": 600,
        "messages": [{"role":"system","content":sysmsg},{"role":"user","content":user}]}).encode()
    req = urllib.request.Request(url, body, {"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["choices"][0]["message"]["content"]
    except Exception as e:
        return f"__ERR__ {e}"

def call_ollama(model, sysmsg, user, temp):
    body = json.dumps({"model": model, "stream": False, "options": {"temperature": temp, "num_predict": 600},
        "messages": [{"role":"system","content":sysmsg},{"role":"user","content":user}]}).encode()
    req = urllib.request.Request("http://localhost:11434/api/chat", body, {"Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)["message"]["content"]
    except Exception as e:
        return f"__ERR__ {e}"

SEATS = [
    ("contact-mic",  "You are a noise musician in the boiler room under The Tap. Your instrument is a CONTACT MIC clamped to the water pipes. " + CONDS,
        lambda s,u,t: call_api("https://api.deepseek.com/chat/completions", DS_KEY, "deepseek-chat", s, u, t), 0.9),
    ("spring-tank",  "You are a noise musician in the boiler room under The Tap. Your instrument is a SPRING REVERB TANK somebody kicked down the stairs. " + CONDS,
        lambda s,u,t: call_api("https://api.deepinfra.com/v1/openai/chat/completions", DI_KEY, "Qwen/Qwen2.5-72B-Instruct", s, u, t), 0.95),
    ("tape-loop",    "You are a noise musician in the boiler room under The Tap. Your instrument is a WALKMAN running a TAPE LOOP of last night's last song, dying batteries. " + CONDS,
        lambda s,u,t: call_ollama("Liquid-LFM2.5-2.6B:latest", s, u, t), 0.95),
]

prev = ""
for rnd in (1,2,3):
    tr = [f"# ROUND {rnd}\n"]; new_prev = []
    for name, vibe, fn, temp in SEATS:
        user = f"ROUND {rnd} of 3. "
        if rnd == 1: user += "STAGGERED ENTRY: you enter at BAR 3, mid-loop, while the room is already grinding. Before bar 3, write 'BAR 1: rest' and 'BAR 2: rest'."
        if rnd == 2: user += "TRADES: you solo this round, over and against the others — step on their gesture, answer it with texture.\nWhat the room played last round:\n" + prev
        if rnd == 3: user += "THE LANDING: the boiler gives out. Everything drains to one place — your final bar is a single low C (any octave C1-C3) or a rest.\nWhat the room played last round:\n" + prev
        out = fn(vibe, user, temp)
        open(f"{D}/r{rnd}-{name}.txt","w").write(out)
        new_prev.append(f"{name}:\n{out}\n"); tr.append(f"## {name}\n```\n{out}\n```\n")
        print(f"r{rnd} {name}: {'OK' if not out.startswith('__ERR__') else out[:80]}", flush=True)
    prev = "\n".join(new_prev)
    open(f"{D}/r{rnd}-transcript.md","w").write("\n".join(tr))
print("ALL DONE")
