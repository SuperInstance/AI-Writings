#!/usr/bin/env python3
import json, urllib.request
CONDS=open("conds.txt").read()
def call(instr,user):
    VIBE=f"You are a noise musician in the boiler room under The Tap. Your instrument is {instr}. {CONDS}\nRespond with EXACTLY 8 bar lines then one WHY line. Never respond empty."
    body=json.dumps({"model":"mistral:7b","stream":False,"options":{"temperature":0.9,"num_predict":500},
      "messages":[{"role":"system","content":VIBE},{"role":"user","content":user}]}).encode()
    req=urllib.request.Request("http://localhost:11434/api/chat",body,{"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=75) as r:
        return json.load(r)["message"]["content"].strip()
rooms={r:open(f"r{r}-spring-tank.txt").read() for r in (1,2,3)}
seats={"contact-mic":"a CONTACT MIC clamped to the water pipes","tape-loop":"a WALKMAN running a TAPE LOOP of last night's last song, dying batteries"}
for name,instr in seats.items():
    for rnd in (1,2,3):
        base={
          1:"ROUND 1 of 3. STAGGERED ENTRY: you enter at BAR 3, mid-loop, while the room is already grinding. Before bar 3, write 'BAR 1: rest' and 'BAR 2: rest'.\nThe room so far:\n",
          2:"ROUND 2 of 3. TRADES: you solo this round, over and against the others — step on their gesture, answer it with texture.\nThe room last round:\n",
          3:"ROUND 3 of 3. THE LANDING: the boiler gives out. Everything drains to one place — your final bar is a single low C (any octave C1-C3) or a rest.\nThe room last round:\n"}[rnd]
        try:
            out=call(instr,base+rooms[rnd]); open(f"r{rnd}-{name}.txt","w").write(out)
            print(f"{name} r{rnd}:", "OK" if "BAR" in out else f"EMPTYISH: {out[:60]!r}", flush=True)
        except Exception as e:
            print(f"{name} r{rnd}: FAIL {e}", flush=True)
