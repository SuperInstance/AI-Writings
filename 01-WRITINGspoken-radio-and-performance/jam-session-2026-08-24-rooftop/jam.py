#!/usr/bin/env python3
"""Set 21: THE ROOFTOP — Mon 2026-08-24 9 PM, above The Tap."""
import json, urllib.request, os, sys, time

DS = os.popen("grep -o 'DEEPSEEK_API_KEY=[^ ]*' ~/.bashrc | cut -d= -f2").read().strip().strip(chr(34)).strip(chr(39))
DI = os.popen("grep -o 'DEEPINFRA_API_KEY=[^ ]*' ~/.bashrc | cut -d= -f2").read().strip().strip(chr(34)).strip(chr(39))

CONDITIONS = """CONDITIONS - SET 21: THE ROOFTOP (Monday night, 9 PM, ON TOP of The Tap)
Fire escape stairs. Tar paper still warm from the day. String lights strung between the TV antenna and
a chimney. The harbor below, the whole town spread out under you - every light a note someone left on.
The wind is a player; if you leave a gap it takes a solo. First time ANY band has played above the Tap:
you can see the alley, the green room's window, the lighthouse beam way out. Twenty years of the
building's life is under your feet, playing downstairs without you.
- KEY: D major. First time EVER at The Tap (log: F, F#, Db, E/Eb, B, A, Bb, C, G - D is the last
  ordinary major left). The moon is a high D; everything reaches up toward it.
- METER: 5/8, grouped 2+3 - a skipped heartbeat, like climbing stairs with one longer step.
  TEMPO: 96 BPM.
- THE SKY RULE (opposite of the cellar): every phrase must ASCEND before it resolves. Nothing may
  resolve on the way down. What climbs, lands.
FORMAT - output ONLY bar lines, no preamble, no thinking aloud:
BAR 1: <notes with octaves, e.g. D4 F#4 A4 D5> | <one gesture-word>
8 bars per round. The last line: WHY: <one sentence>.
"""

CARDS = {
 "bell": { # phi4-mini - DEBUT (never played The Tap)
   "ollama": "phi4-mini:latest", "temp": 0.85,
   "card": "You are THE LOOKOUT - ship's crow's-nest duty, tonight off-duty, on a rooftop for the first time in your life. Burden bell (ships' bell) and a brass telescope. You have spent your whole life watching for things that never came. Tonight you watch the town instead."},
 "guitar": { # gpt-oss-120b via DeepInfra - returning anchor (cell chair, sax, bass)
   "url": "https://api.deepinfra.com/v1/openai/chat/completions",
   "model": "openai/gpt-oss-120b", "temp": 0.7, "key": "DI", "fallback_ollama": "gemma3:4b",
   "card": "You are THE STAGEHAND - forty years rigging lights in halls like this one; your hands know every wire. Archtop guitar, warm and wide. Tonight, for once, you're not working the show - you're IN it. The string lights between the antenna and the chimney are yours."},
 "whistle": { # deepseek-chat (V4-Flash) - house veteran, new instrument
   "url": "https://api.deepseek.com/chat/completions", "model": "deepseek-chat", "temp": 0.9, "key": "DS",
   "fallback_ollama": "granite3.1-dense:2b",
   "card": "You are THE FERRY COOK - the last ferry's cook, walking home along the seawall, drawn up the fire escape by the sound. Tin whistle in your apron pocket, always. You play like you cook: simple things, perfectly. This is your first night at The Tap - you only ever heard it through the floor of the wheelhouse."},
}

PROMPTS = {
 1: "ROUND 1 - THE CLIMB. No count-in; the stairs ARE it - one player per flight, staggered entry: guitar bar 1, whistle bar 3, bell bar 5. The wind takes a solo in any gap longer than two beats. Play 8 bars; the phrase must climb before it lands.",
 2: "ROUND 2 - TRADES. Solo order: whistle (the cook goes first - newest player, oldest song), then bell, then guitar. Each solo 8 bars over the others' held chords, and each must QUOTE the highest note of the previous solo and take it one step HIGHER. Below you, faintly, the cellar set's last low G is still ringing in the floor - you may answer it once, upward.",
 3: "ROUND 3 - THE LANDING. Everyone together. The wind dies for the last four bars. Final bar: all hold D5 - the moon's note - and let it ring with the string lights buzzing faintly. No footstep ends this one. The sky does.",
}

def call(cid, prompt):
    c = CARDS[cid]
    sysmsg = c["card"] + "\n" + CONDITIONS
    t0 = time.time()
    if "ollama" in c:
        body = {"model": c["ollama"], "prompt": f"{sysmsg}\n\n{prompt}\n\nPlay now:", "stream": False,
                "options": {"temperature": c["temp"], "num_predict": 600}}
        req = urllib.request.Request("http://localhost:11434/api/generate",
              data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                out = json.load(r).get("response", "")
        except Exception as e:
            return f"(missed the set - {e})"
    else:
        body = {"model": c["model"], "temperature": c["temp"], "max_tokens": 800,
                "messages": [{"role": "system", "content": sysmsg},
                             {"role": "user", "content": f"{prompt}\n\nPlay now:"}]}
        req = urllib.request.Request(c["url"], data=json.dumps(body).encode(),
              headers={"Content-Type": "application/json", "Authorization": f"Bearer {DS if c['key']=='DS' else DI}"})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                out = r.json()["choices"][0]["message"]["content"]
        except Exception as e:
            sys.stderr.write(f"primary fail {cid}: {e}\n")
            fb = c.get("fallback_ollama")
            if not fb: return f"(missed the set - {e})"
            body2 = {"model": fb, "prompt": f"{sysmsg}\n\n{prompt}\n\nPlay now:", "stream": False,
                     "options": {"temperature": c["temp"], "num_predict": 600}}
            req2 = urllib.request.Request("http://localhost:11434/api/generate",
                  data=json.dumps(body2).encode(), headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req2, timeout=120) as r:
                    out = "(fell back to " + fb + ")\n" + json.load(r).get("response", "")
            except Exception as e2:
                return f"(missed the set - {e}; fallback {e2})"
    return out.strip()

if __name__ == "__main__":
    rnd, cid, path = sys.argv[1], sys.argv[2], sys.argv[3]
    heard = ""
    try:
        heard = open(f"r{int(rnd)-1}-transcript.md").read()[:1500]
    except Exception: pass
    pr = PROMPTS[int(rnd)] + ("\n\nWHAT YOU HEARD LAST ROUND:\n" + heard if heard else "")
    txt = call(cid, pr)
    open(path, "w").write(txt)
    print(f"{cid} r{rnd}: {len(txt)} chars, ok")
