import json,os,urllib.request,pathlib
OUT=pathlib.Path(".")
keys={}
for line in open(os.path.expanduser("~/.bashrc")):
    if "DEEPINFRA_API_KEY=" in line: keys=line.split("=",1)[1].strip().strip(chr(34))
def di(model,msgs,temp):
    body=json.dumps({"model":model,"messages":msgs,"temperature":temp,"max_tokens":600}).encode()
    req=urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",data=body,headers={"Authorization":"Bearer "+keys,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=30) as r: d=json.load(r)
    m=d["choices"][0]["message"]; return m.get("content") or m.get("reasoning_content") or "(silence)"
sysmsg="You are a musician at an improvised jam session. Stay in the music. Concrete notes, bars, dynamics. Under 250 words. No AI meta."
INSTR="a poet playing HARMONIUM (pump organ) in the green room — long breaths, chords that bloom slowly"
set_r={"r1":open("r1-transcript.md").read(),"r2":open("r2-transcript.md").read(),"r3":open("r3-transcript.md").read()}
briefs={
"r1":"""ROUND 1 — STAGGERED ENTRY. The green room backstage at The Tap before the last ferry: mirror with warm bulbs, old velvet, a kettle on, stage door cracked open. Key Bb major, 3/4 WALTZ, 92 BPM. You are {i}. You drifted in third, after the cello and vibes already started warming up. Play 4 quiet bars — a warm-up that becomes a phrase. Heard so far: {h} Write bars as concrete notes, then one sentence on the room.""",
"r2":"""ROUND 2 — TRADES IN THE MIRROR. Solo 4 bars at your reflection, others vamping. Bb major, 3/4, 92 BPM. FERRY RULE: quote one note from another player's phrase, name it and whose. Set so far: {h} You are {i}.""",
"r3":"""ROUND 3 — THE LANDING / LAST FERRY. Ferry horn sounds low F twice. All play 8 bars quiet; one by one players put instruments down and head for the stage door. Last note of the night is a Bb2 held until the kettle clicks off. Bb major, 3/4, 92. Full set: {h} You are {i}. Write your 8 bars and the moment you stop playing. End: what the green room sounds like empty."""}
for rnd in ["r1","r2","r3"]:
    h=set_r[rnd][:1600]
    model="Qwen/Qwen3.5-9B"
    try: txt=di(model,[{"role":"system","content":sysmsg},{"role":"user","content":briefs[rnd].format(i=INSTR,h=h)}],0.8)
    except Exception as e:
        print(rnd,model,"fail",e); model="mistralai/Mistral-Nemo-Instruct-2407"
        try: txt=di(model,[{"role":"system","content":sysmsg},{"role":"user","content":briefs[rnd].format(i=INSTR,h=h)}],0.8)
        except Exception as e2: print(rnd,"fallback fail",e2); txt="(the harmonium never arrived — an empty chair)"
    set_r[rnd]=set_r[rnd].replace("### kimi-harmonium:\n\n", f"### harmonium ({model}):\n{txt}\n\n")
    open(f"{rnd}-transcript.md","w").write(set_r[rnd]); print(rnd,"ok",len(txt))
print("FILLED")
