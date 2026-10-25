#!/usr/bin/env python3
import json, urllib.request
CONDS=open("conds.txt").read()
VIBE="You are a noise musician in the boiler room under The Tap. Your instrument is a CONTACT MIC clamped to the water pipes. "+CONDS
def call(user):
    body=json.dumps({"model":"zai-org/GLM-4.7-Flash","temperature":0.9,"max_tokens":600,
      "messages":[{"role":"system","content":VIBE},{"role":"user","content":user}]}).encode()
    req=urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",body,
      {"Content-Type":"application/json","Authorization":"Bearer zYuVMGC4JySULP2waqKW35jI42TjaPkl"})
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.load(r)["choices"][0]["message"]["content"]
prompts={r:open(f"r{r}-spring-tank.txt").read()+open(f"r{r}-tape-loop.txt").read() for r in (1,2,3)}
for rnd in (1,2,3):
    base={
      1:"ROUND 1 of 3. STAGGERED ENTRY: you enter at BAR 3, mid-loop, while the room is already grinding. Before bar 3, write 'BAR 1: rest' and 'BAR 2: rest'.\nWhat the room played:\n",
      2:"ROUND 2 of 3. TRADES: you solo this round, over and against the others — step on their gesture, answer it with texture.\nWhat the room played:\n",
      3:"ROUND 3 of 3. THE LANDING: the boiler gives out. Everything drains to one place — your final bar is a single low C (any octave C1-C3) or a rest.\nWhat the room played:\n"}[rnd]
    try:
        out=call(base+prompts[rnd]); open(f"r{rnd}-contact-mic.txt","w").write(out)
        print(f"fill r{rnd}:", "OK" if "BAR" in out else out[:120], flush=True)
    except Exception as e:
        print(f"fill r{rnd}: FAIL {e}", flush=True)
