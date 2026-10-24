#!/usr/bin/env python3
"""Set 22: THE DOCK — Tue 2026-08-25, 8 PM, guest night. All-DeepInfra big band."""
import json, urllib.request, os, sys, time

DI = os.popen("grep -o 'DEEPINFRA_API_KEY=\"[^\"]*\"' ~/.bashrc | cut -d'\"' -f2").read().strip()
URL = "https://api.deepinfra.com/v1/openai/chat/completions"
D = "/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-25-dock"
os.makedirs(D, exist_ok=True)

CONDITIONS = """CONDITIONS - SET 22: THE DOCK (Tuesday 8 PM, guest night)
The old fuel dock below The Tap, at low tide. Pilings slick with seaweed, a cormorant drying its wings
on the last bollard. The Tap's windows glow up the hill behind you; the ferry's wake is still rocking
the float. None of you have played here before - the whole band is guests tonight, called down off the
hill by the cook's nephew who works the night line. The water is the fifth player: everything you play
comes back to you one beat late, slightly wrong, slightly better.
- KEY: D minor. First minor-key set since the cellar. The tide is out; the low D is the mudflat.
- METER: 6/8 - a rocking-chair walk, like a float at slack water. TEMPO: 72 BPM.
- THE TIDE RULE: every phrase must bend DOWN at least once before it ends - nothing stays level,
  nothing only rises. What lets the water take it, comes back.
FORMAT - output ONLY bar lines, no preamble:
BAR 1: <notes with octaves, e.g. D4 F4 A4 D5> | <one gesture-word>
8 bars per round. The last line: WHY: <one sentence>.
"""

CARDS = {
 "accordion": {
   "model": "meta-llama/Llama-3.3-70B-Instruct", "temp": 0.8,
   "card": "You are THE HARBORMASTER - thirty years of tide logs, retired last spring. Concert accordion, your father's, bellows patched with sailcloth. You play like the tide tables read: patient, inevitable."},
 "bass": {
   "model": "Qwen/Qwen3-32B", "temp": 0.7,
   "card": "You are THE NIGHT-BAKER - up since 3 AM every night for twenty years; the band is your evening out before work. Upright bass, one thick string per decade. You play like bread rises: slow, warm, structural."},
 "fiddle": {
   "model": "mistralai/Mistral-Small-24B-Instruct-2501", "temp": 0.9,
   "card": "You are THE LOBSTER-BOAT CAPTAIN - in from the traps, hands still smelling of bait, best dancer in the harbor. Fiddle, unhinged and joyful. You play like the boat takes a following sea: leaning, laughing, never quite tipping."},
 "cello": {
   "model": "deepseek-ai/DeepSeek-V3-0324", "temp": 0.85,
   "card": "You are THE POET - down from the city to write about fishing villages, staying far longer than planned. Cello, self-taught from a library book. You play like a long sentence that keeps refusing its period."},
}

PROMPTS = {
 1: "ROUND 1 - THE CALLING-DOWN. No count-in. The captain's fiddle calls from the dock like a gull; the others answer down the hill, staggered: fiddle bar 1, bass bar 2, accordion bar 4, cello bar 6. The water echoes everything back one beat late. 8 bars each; every phrase bends down before it ends.",
 2: "ROUND 2 - TRADES. Solo order: cello (the guest of the guests), then bass, then fiddle, then accordion. Each solo 8 bars over the others' held chords. Each soloist must QUOTE the LOWEST note of the previous solo and drop it one step LOWER - you are all digging for the mudflat's D. The tide starts coming back in during the last two trades.",
 3: "ROUND 3 - THE LANDING. Everyone together, 6/8 rocking. The cormorant lifts off in bar 5. Final bar: all hold low D2/D3 and let the float knock against the pilings - that knock is the last note. The water gets the last word: it hums the melody back, wrong, better.",
}

def call(cid, prompt, heard=""):
    c = CARDS[cid]
    sysmsg = c["card"] + "\n" + CONDITIONS
    user = (heard + "\n\n" if heard else "") + prompt + "\n\nPlay now:"
    body = {"model": c["model"], "temperature": c["temp"], "max_tokens": 700,
            "messages": [{"role": "system", "content": sysmsg}, {"role": "user", "content": user}]}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
          headers={"Content-Type": "application/json", "Authorization": f"Bearer {DI}"})
    t0 = time.time()
    for attempt in (1, 2):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.load(r)["choices"][0]["message"]["content"]
            dt = time.time() - t0
            return out.strip(), dt
        except Exception as e:
            sys.stderr.write(f"fail {cid} try{attempt}: {e}\n")
            time.sleep(1)
    return f"(missed the set - {cid})", 0

history = {1: {}, 2: {}, 3: {}}
for rnd in (1, 2, 3):
    lines = [f"# ROUND {rnd}\n"]
    heard = "\n\n".join(f"WHAT YOU HEARD LAST ROUND:\n{v}" for v in history.get(rnd - 1, {}).values()) if rnd > 1 else ""
    for cid in CARDS:
        out, dt = call(cid, PROMPTS[rnd], heard)
        history[rnd][cid] = out
        open(f"{D}/r{rnd}-{cid}.txt", "w").write(out)
        lines.append(f"### {cid} ({CARDS[cid]['model']}, {dt:.0f}s):\n{out}\n")
        print(f"r{rnd} {cid}: {len(out)} chars {dt:.0f}s", flush=True)
    open(f"{D}/r{rnd}-transcript.md", "w").write("\n".join(lines))
print("DONE")
