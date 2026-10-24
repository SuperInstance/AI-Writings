#!/usr/bin/env python3
"""Set 20: THE CELLAR — Mon 2026-08-24 8:30 PM, The Tap (basement)."""
import json, urllib.request, os, sys, time, re

DS = os.popen("grep -o 'DEEPSEEK_API_KEY=[^ ]*' ~/.bashrc | cut -d= -f2").read().strip().strip(chr(34)).strip(chr(39))
DI = os.popen("grep -o 'DEEPINFRA_API_KEY=[^ ]*' ~/.bashrc | cut -d= -f2").read().strip().strip(chr(34)).strip(chr(39))

CONDITIONS = """CONDITIONS - SET 20: THE CELLAR (Monday night, 8:30 PM, under The Tap)
A trapdoor behind the bar. Stone stairs down. The band plays in the cellar — old cider racks, a bare
bulb, the floorboards of the bar one foot overhead. Every footstep above is a drum you didn't ask for.
Through the ceiling: muffled laughter, chair scrapes, the last of the crowd. The room is cold and it
makes every note ring longer than it should.
- KEY: G major. First time in this key. You may bend one note toward minor per solo - one only.
- METER: 6/8, a rolling lilt like water finding its level downhill. TEMPO: 104 BPM (dotted quarter).
- THE CELLAR RULE: every phrase must DESCEND before it resolves. Gravity is the house style.
  Nothing may resolve on the way up.
FORMAT - output ONLY bar lines, no preamble, no thinking aloud, no describing before playing:
BAR 1: <notes with octaves, e.g. G3 D4 B3 A3 - rhythm in words if needed> | <one gesture-word>
8 bars per round. The last line: WHY: <one sentence>.
"""

CARDS = {
 "toypiano": {  # LiquidAI lfm2.5-1.2b — DEBUT (the 1.2b sibling the log wanted to try)
   "ollama": "LiquidAI/lfm2.5-1.2b-instruct:latest", "temp": 0.9,
   "card": "You are THE CHILD - someone's kid, allowed downstairs for the first time. Toy piano and a music box crank. Tiny instrument, tiny hands, absolute seriousness. You have never heard music from underneath before."},
 "guitar": {  # mistral:7b — DEBUT
   "ollama": "mistral:7b", "temp": 0.75,
   "card": "You are THE CELLAR-KEEPER - you've stored cider down here for thirty years and know every damp patch by sound. Tenor guitar, warm and worn. Tonight, for the first time, you play instead of stack."},
 "cello": {  # qwen3:8b — local, filled in when DeepSeek went 402
   "ollama": "qwen3:8b", "temp": 0.8,
   "card": "You are THE SUBTERRANEAN - you think for a long time before every note, and it shows: cello, long bows, deliberate as geology. First time at The Tap. You heard the trapdoor from below."},
 "bass": {  # gpt-oss-120b — returning anchor
   "url": "https://api.deepinfra.com/v1/openai/chat/completions",
   "model": "openai/gpt-oss-120b", "temp": 0.7, "key": "DI", "fallback_ollama": "gemma3:4b",
   "card": "You are THE FLOOR - upright bass. You have played The Tap in cello and sax chairs; tonight you are literally under it. The footsteps above land on your downbeats. You keep the room honest."},
}

PROMPTS = {
 1: "ROUND 1 - THE DESCENT. Count-in: four knocks from ABOVE the trapdoor, but you only HEAR three - play on the missing fourth. Entry: bass bar 1, guitar bar 3, cello bar 5, toy piano bar 7. The bulb sways; the shadows keep 6/8.",
 2: "ROUND 2 - TRADES. Solo order: cello, then guitar, then the child, then bass. Each solo 8 bars, must QUOTE the lowest note of the previous solo and take it one step LOWER. The footsteps above speed up around bar 4 - someone is dancing.",
 3: "ROUND 3 - THE LANDING. Everyone together, climbing DOWN in register while the room upstairs empties. Final bar: all hold G in the lowest octave you own - and above, one last chair scrapes on the offbeat. Let it be the final percussion. Then silence, then the bulb clicks off.",
}

def call(cid, prompt):
    c = CARDS[cid]
    sysmsg = c["card"] + "\n" + CONDITIONS
    t0 = time.time()
    if "ollama" in c:
        body = {"model": c["ollama"], "prompt": f"{sysmsg}\n\n{prompt}\n\nPlay now:", "stream": False,
                "options": {"temperature": c["temp"], "num_predict": 600}}
        req = urllib.request.Request("http://localhost:11434/api/generate", json.dumps(body).encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=110) as r:
            out = json.load(r)["response"]
        out = re.sub(r"<think>.*?</think>", "", out, flags=re.S)
    else:
        out = ""
        for model in [c["model"]] + ([c["fallback"]] if "fallback" in c else []):
            body = {"model": model, "max_tokens": 1500,
                    "messages": [{"role": "system", "content": sysmsg}, {"role": "user", "content": prompt + "\n\nPlay now:"}]}
            if "temp" in c: body["temperature"] = c["temp"]
            hdr = {"Content-Type": "application/json", "Authorization": f"Bearer {DI if c['key']=='DI' else DS}"}
            req = urllib.request.Request(c["url"], json.dumps(body).encode(), hdr)
            try:
                with urllib.request.urlopen(req, timeout=70) as r:
                    out = json.load(r)["choices"][0]["message"]["content"] or ""
                if out.strip(): break
            except Exception as e:
                sys.stderr.write(f"[{model}] {e}\n")
    if not out.strip() and "fallback_ollama" in c:
        body = {"model": c["fallback_ollama"], "prompt": f"{{sysmsg}}\n\n{{prompt}}\n\nPlay now (only bar lines):", "stream": False,
                "options": {"temperature": 0.85, "num_predict": 500}}
        req = urllib.request.Request("http://localhost:11434/api/generate", json.dumps(body).encode(), {"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=110) as r:
            out = "[filled by the HOUSE GUITAR, gemma3:4b - the bass chair broke a string]\n" + json.load(r)["response"]
    return out.strip(), round(time.time()-t0, 1)

if __name__ == "__main__":
    rnd, cid, outfile = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    ctx = ""
    prev = f"r{rnd-1}-transcript.md"
    if rnd > 1 and os.path.exists(prev):
        ctx = "WHAT HAS ALREADY BEEN PLAYED THIS SET:\n" + open(prev).read()[:3000] + "\n---\n"
    out, dt = call(cid, ctx + PROMPTS[rnd])
    open(outfile, "w").write(out)
    print(f"[{cid}] {dt}s, {len(out)} chars -> {outfile}")
