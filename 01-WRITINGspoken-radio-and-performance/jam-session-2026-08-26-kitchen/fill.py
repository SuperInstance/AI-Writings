#!/usr/bin/env python3
"""Fill script: redo dishpit + piano chairs (empty in main run). dishpit->gemma-3-27b, piano gpt-oss-20b w/ bigger budget."""
import json, urllib.request, os, sys, time

DI = os.popen("grep -o 'DEEPINFRA_API_KEY=\"[^\"]*\"' ~/.bashrc | cut -d'\"' -f2").read().strip()
URL = "https://api.deepinfra.com/v1/openai/chat/completions"
D = os.path.dirname(os.path.abspath(__file__))

CONDITIONS = open(f"{D}/conds.txt").read()
PROMPTS = {int(k): v for k, v in (l.split("|", 1) for l in open(f"{D}/prompts.txt"))}

CARDS = {
 "dishpit": ("google/gemma-3-27b-it", 0.9,
   "You are THE DISHWASHER - been here longer than the menu. Plays the dish pit: steel bowls inverted as bells, the sprayer's hiss, racks rolled home like a ride cymbal. You have heard every fight, every wedding toast, every last call through that window. You never rush. You never stop."),
 "piano": ("openai/gpt-oss-20b", 0.85,
   "You are THE WAITRESS - pooling tips since the smoking ban. The owner's upright piano lives between the dry storage and the mop sink; the low A sticks. You play the melody because you know every song the room has ever sung, and you sing along under your breath. Tonight it's your piano."),
}

def call(model, temp, sysmsg, user, budget):
    body = {"model": model, "temperature": temp, "max_tokens": budget,
            "messages": [{"role": "system", "content": sysmsg}, {"role": "user", "content": user + "\n\nPlay now (bars only, no preamble, no reasoning):"}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
          headers={"Content-Type": "application/json", "Authorization": f"Bearer {DI}"})
    t0 = time.time()
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=35) as r:
                out = (json.load(r)["choices"][0]["message"].get("content") or "").strip()
            if out: return out, time.time() - t0
        except Exception as e:
            sys.stderr.write(f"fail {model} try{attempt}: {e}\n"); time.sleep(1)
    return "", time.time() - t0

for rnd in (1, 2, 3):
    heard = ""
    if rnd > 1:
        heard = f"WHAT YOU HEARD LAST ROUND:\n{open(f'{D}/r{rnd-1}-dishpit.txt').read()}\n\n{open(f'{D}/r{rnd-1}-piano.txt').read()}"
    else:
        heard = "WHAT YOU HEARD (round 1 already in progress - the walk-in hums, griddle ticking, sax waiting): (the set is starting)"
    for cid, (model, temp, card) in CARDS.items():
        budget = 1500 if "gpt-oss" in model else 700
        out, dt = call(model, temp, card + "\n" + CONDITIONS, heard + "\n\n" + PROMPTS[rnd], budget)
        if out:
            open(f"{D}/r{rnd}-{cid}.txt", "w").write(out)
        print(f"r{rnd} {cid}: {len(out)} chars {dt:.0f}s", flush=True)
print("FILL DONE")
