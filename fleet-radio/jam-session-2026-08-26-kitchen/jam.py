#!/usr/bin/env python3
"""Set 23: THE KITCHEN — Wed 2026-08-26, 8:30 PM. After close, the kitchen. 4 DeepInfra + 1 Ollama."""
import json, urllib.request, os, sys, time, threading

DI = os.popen("grep -o 'DEEPINFRA_API_KEY=\"[^\"]*\"' ~/.bashrc | cut -d'\"' -f2").read().strip()
URL = "https://api.deepinfra.com/v1/openai/chat/completions"
OLLAMA = "http://localhost:11434/api/generate"
D = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-26-kitchen"
os.makedirs(D, exist_ok=True)

CONDITIONS = """CONDITIONS - SET 23: THE KITCHEN (Wednesday 8:30 PM, after close)
The Tap's kitchen after last call. Doors locked, lights half-off, griddle still ticking as it cools.
Steam still rises off the dish pit. The room smells of bleach and tomorrow's bread proofing on the rack.
Nobody's being paid tonight - the band stayed because the kitchen is the warmest room in the building
and the walk-in hums a perfect G. It has hummed that G for thirty years; tonight you tune to the walk-in.
- KEY: G major, but no instrument may play the open G string as a melody note - the walk-in owns that G.
  You may only touch it in passing. It is the room's note, not yours.
- METER: 5/4 - a slow wolf swing, five counts like carrying four plates plus the coffee.
  TEMPO: 88 BPM. The room is small; play like it.
- THE STEAM RULE: whenever you finish a phrase, at least one note must be DAMPED - choked, muted,
  swallowed - as if a cloud of steam took it. The kitchen eats one note per phrase. Feed it.
FORMAT - output ONLY bar lines, no preamble, no thinking:
BAR 1: <notes with octaves, e.g. B4 D5 G4> | <one gesture-word in lowercase>
8 bars per round. Last line: WHY: <one sentence>.
"""

CARDS = {
 "griddle": {
   "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo", "temp": 0.8, "src": "di",
   "card": "You are THE LINE COOK - twenty years on the line, hearing damage in one ear so you lean your head to listen. Teaspoon-and-spatula percussion on the flat-top. You keep time like orders coming in: in threes, always in threes."},
 "dishpit": {
   "model": "zai-org/GLM-4.7-Flash", "temp": 0.9, "src": "di",
   "card": "You are THE DISHWASHER - been here longer than the menu. Plays the dish pit: steel bowls inverted as bells, the sprayer's hiss, racks rolled home like a ride cymbal. You have heard every fight, every wedding toast, every last call through that window. You never rush. You never stop."},
 "piano": {
   "model": "openai/gpt-oss-20b", "temp": 0.85, "src": "di",
   "card": "You are THE WAITRESS - pooling tips since the smoking ban. The owner's upright piano lives between the dry storage and the mop sink; the low A sticks. You play the melody because you know every song the room has ever sung, and you sing along under your breath. Tonight it's your piano."},
 "sax": {
   "model": "mistralai/Mistral-Small-24B-Instruct-2501", "temp": 0.95, "src": "di",
   "card": "You are THE COOK'S NEPHEW - worked the night line all summer, unafraid of anything. Baritone sax borrowed from the school, borrowed since June. You play too loud and at exactly the right moment. Nobody taught you the changes; you don't need them."},
 "steam": {
   "model": "mistral:7b", "temp": 1.0, "src": "ollama",
   "card": "You are THE WALK-IN - the refrigerator, the eldest thing in the building, humming its G for thirty years. You are the drone beneath everything: long low tones, door hisses, frost breath. You hold the room together. The G is yours."},
}

PROMPTS = {
 1: "ROUND 1 - ORGANIC ENTRY. No count-in. The walk-in door hisses, the dish pit answers, and the kitchen wakes one player at a time: steam bar 1, dishpit bar 2, griddle bar 3, piano bar 5, sax bar 7. Everyone else holds near-silence until their bar. The steam eats one note per phrase. 8 bars each.",
 2: "ROUND 2 - TRADES OVER THE SINK. Solo order: sax, then piano, then griddle, then dishpit. Each solo 8 bars, the walk-in droning under all of it. Each soloist must QUOTE one note from the previous solo but DAMP it - the note they stole comes out choked, different. Someone knocks over a stack of bowls in bar 4 of the dishpit solo. Do not stop playing.",
 3: "ROUND 3 - SWEEPING UP. Everyone in, 5/4, quieter and quieter - this is the last thing before home. The griddle stops ticking in bar 4. By bar 8 the only sound is the walk-in's G and one broom. Final bar: the walk-in alone holds its G - the note nobody was allowed to play all night, returned to its owner. Then the door hisses shut.",
}

def call_di(cid, prompt, heard=""):
    c = CARDS[cid]
    user = (heard + "\n\n" if heard else "") + prompt + "\n\nPlay now (bars only, no reasoning):"
    body = {"model": c["model"], "temperature": c["temp"], "max_tokens": 700,
            "messages": [{"role": "system", "content": c["card"] + "\n" + CONDITIONS},
                         {"role": "user", "content": user}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
          headers={"Content-Type": "application/json", "Authorization": f"Bearer {DI}"})
    t0 = time.time()
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.load(r)["choices"][0]["message"]["content"] or ""
            return out.strip(), time.time() - t0
        except Exception as e:
            sys.stderr.write(f"fail {cid} try{attempt}: {e}\n"); time.sleep(1)
    return f"(missed the set - {cid})", 0

def call_ollama(cid, prompt, heard=""):
    c = CARDS[cid]
    user = (heard + "\n\n" if heard else "") + prompt + "\n\nPlay now (bars only, no reasoning):"
    body = {"model": c["model"], "temperature": c["temp"], "options": {"num_predict": 600},
            "stream": False, "system": c["card"] + "\n" + CONDITIONS, "prompt": user}
    req = urllib.request.Request(OLLAMA, data=json.dumps(body).encode(),
          headers={"Content-Type": "application/json"})
    t0 = time.time()
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                out = json.load(r).get("response", "")
            return out.strip(), time.time() - t0
        except Exception as e:
            sys.stderr.write(f"fail {cid} try{attempt}: {e}\n"); time.sleep(1)
    return f"(missed the set - {cid})", 0

def call(cid, prompt, heard=""):
    fn = call_ollama if CARDS[cid]["src"] == "ollama" else call_di
    return fn(cid, prompt, heard)

history = {1: {}, 2: {}, 3: {}}
for rnd in (1, 2, 3):
    heard = "\n\n".join(f"WHAT YOU HEARD LAST ROUND:\n{v}" for v in history.get(rnd - 1, {}).values()) if rnd > 1 else ""
    # run all players of the round in parallel
    results = {cid: call(cid, PROMPTS[rnd], heard) for cid in CARDS}
    lines = [f"# ROUND {rnd}\n"]
    for cid in CARDS:
        out, dt = results[cid]
        history[rnd][cid] = out
        open(f"{D}/r{rnd}-{cid}.txt", "w").write(out)
        lines.append(f"### {cid} ({CARDS[cid]['model']}, {dt:.0f}s):\n{out}\n")
        print(f"r{rnd} {cid}: {len(out)} chars {dt:.0f}s", flush=True)
    open(f"{D}/r{rnd}-transcript.md", "w").write("\n".join(lines))
print("DONE")
