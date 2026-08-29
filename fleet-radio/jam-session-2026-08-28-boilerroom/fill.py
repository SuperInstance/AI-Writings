#!/usr/bin/env python3
import json, urllib.request
D="."
CONDS=open("conds.txt").read()
VIBE="You are a noise musician in the boiler room under The Tap. Your instrument is a CONTACT MIC clamped to the water pipes. "+CONDS
def call(user):
    body=json.dumps({"model":"qwen3:8b","stream":False,"options":{"temperature":0.9,"num_predict":600},
      "messages":[{"role":"system","content":VIBE},{"role":"user","content":user}]}).encode()
    req=urllib.request.Request("http://localhost:11434/api/chat",body,{"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=60) as r:
        return json.load(r)["message"]["content"]
prompts={
 1:"ROUND 1 of 3. STAGGERED ENTRY: you enter at BAR 3, mid-loop, while the room is already grinding. Before bar 3, write 'BAR 1: rest' and 'BAR 2: rest'.",
 2:"ROUND 2 of 3. TRADES: you solo this round, over and against the others — step on their gesture, answer it with texture.\nWhat the room played last round:\nROOM:\n"+open("r2-spring-tank.txt").read()+open("r2-tape-loop.txt").read(),
 3:"ROUND 3 of 3. THE LANDING: the boiler gives out. Everything drains to one place — your final bar is a single low C (any octave C1-C3) or a rest.\nWhat the room played last round:\nROOM:\n"+open("r3-spring-tank.txt").read()+open("r3-tape-loop.txt").read(),
}
for rnd in (1,2,3):
    out=call(prompts[rnd]); open(f"r{rnd}-contact-mic.txt","w").write(out)
    print(f"fill r{rnd}:", "OK" if "BAR" in out else out[:120], flush=True)
