#!/usr/bin/env python3
"""SET 24: THE STAIRWELL — duo night. vibraphone(DeepSeek Flash) + double bass(Hermes-3-405B)."""
import json, os, re, urllib.request, sys

D = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-27-stairwell"
DS_KEY = "sk-0a57cd44bc674f5caffd9b0ec10e284c"
DI_KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
CONDS = open(f"{D}/conds.txt").read()

def call(url, key, model, sysmsg, user, temp):
    body = json.dumps({"model": model, "temperature": temp, "max_tokens": 500,
        "messages": [{"role":"system","content":sysmsg},{"role":"user","content":user}]}).encode()
    req = urllib.request.Request(url, body, {"Content-Type":"application/json","Authorization":f"Bearer {key}"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            d = json.load(r)
            if "choices" in d: return d["choices"][0]["message"]["content"]
            return d["choices"][0]["text"] if "choices" in d else str(d)[:200]
    except Exception as e:
        return f"__ERR__ {e}"

VIBE = """You are a musician at a late-night jam in a concrete stairwell. You play VIBRAPHONE.
""" + CONDS

BASSVIBE = """You are a musician at a late-night jam in a concrete stairwell. You play DOUBLE BASS.
""" + CONDS

def round_(rnd, instr, vibe, prev):
    if instr == "vibes":
        model, url, key = "deepseek-chat", "https://api.deepseek.com/chat/completions", DS_KEY
    else:
        model, url, key = "NousResearch/Hermes-3-Llama-3.1-405B", "https://api.deepinfra.com/v1/openai/chat/completions", DI_KEY
    user = f"ROUND {rnd} of 3. "
    if rnd == 1: user += "Organic entry: no count-in. You begin alone, mid-thought, as if you'd been playing before anyone listened."
    if rnd == 2: user += "TRADES: you take the lead this round; the other player answers you.\nWhat you both played last round:\n" + prev
    if rnd == 3: user += "THE LANDING: find resolution together; end your last bar on a D (any octave) and let it ring.\nWhat you both played last round:\n" + prev
    out = call(url, key, model, vibe, user, 0.85)
    return out

names = {"vibes":"vibraphone","bass":"bass"}
prev = ""
for rnd in (1,2,3):
    tr = [f"# ROUND {rnd}\n"]
    prev_new = []
    for instr in ("vibes","bass"):
        out = round_(rnd, instr, VIBE if instr=="vibes" else BASSVIBE, prev)
        fn = f"{D}/r{rnd}-{names[instr]}.txt"
        open(fn,"w").write(out)
        prev_new.append(f"{names[instr]}:\n{out}\n")
        tr.append(f"## {names[instr]} ({'DeepSeek Flash' if instr=='vibes' else 'Hermes-3-405B'})\n```\n{out}\n```\n")
    prev = "\n".join(prev_new)
    open(f"{D}/r{rnd}-transcript.md","w").write("\n".join(tr))
    print(f"round {rnd} done", flush=True)
print("ALL DONE")
