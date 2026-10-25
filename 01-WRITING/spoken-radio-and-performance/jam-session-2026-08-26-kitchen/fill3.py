#!/usr/bin/env python3
"""Fill piano r1+r2 only (empty from main run). One model, hears the room."""
import json, urllib.request, os
DI = os.popen("grep -o 'DEEPINFRA_API_KEY=\"[^\"]*\"' ~/.bashrc | cut -d'\"' -f2").read().strip()
URL = "https://api.deepinfra.com/v1/openai/chat/completions"
D = os.path.dirname(os.path.abspath(__file__))
CONDITIONS = open(f"{D}/conds.txt").read()
def call(user):
    body = {"model":"google/gemma-3-27b-it","temperature":0.85,"max_tokens":500,
      "messages":[{"role":"system","content":"You are THE WAITRESS - pooling tips since the smoking ban. The owner's upright piano lives between the dry storage and the mop sink; the low A sticks. You know every song the room has ever sung; you sing along under your breath. Tonight it's your piano."},
                  {"role":"user","content":user+"\n\nPlay now (bars only, no preamble, no reasoning):"}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Authorization":f"Bearer {DI}"})
    with urllib.request.urlopen(req, timeout=35) as r:
        return (json.load(r)["choices"][0]["message"].get("content") or "").strip()
r2r1 = open(f"{D}/r1-sax.txt").read()+open(f"{D}/r1-steam.txt").read()
r1 = call(CONDITIONS+"\nROUND 1 - you enter at BAR 5 (walk-in hissing since bar 1, dishpit answering bar 2, line cook bar 3, sax waits till 7). Bars 1-4 near-silence (write 'rest'). 8 bars total.")
if r1: open(f"{D}/r1-piano.txt","w").write(r1); print("r1 ok",len(r1))
r2 = call(CONDITIONS+"\nROUND 2 - TRADES OVER THE SINK. Your solo is SECOND (after the sax). Quote one note from the sax solo below and DAMP it. 8 bars.\nTHE SAX SOLO YOU FOLLOWED:\n"+r2r1)
if r2: open(f"{D}/r2-piano.txt","w").write(r2); print("r2 ok",len(r2))
