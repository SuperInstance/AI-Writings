import json, os, re, subprocess, urllib.request, sys
D="/home/eileen/projects/ai-writings/fleet-radio/jam-session-2026-08-29-breakwater"
os.chdir(D)
DI=os.environ["DEEPINFRA_API_KEY"]

def di(model, sys, user, temp):
    body=json.dumps({"model":model,"messages":[{"role":"system","content":sys},{"role":"user","content":user}],"temperature":temp,"max_tokens":700}).encode()
    req=urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",data=body,headers={"Authorization":f"Bearer {DI}","Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=60) as r:
        c=json.load(r)
    return c["choices"][0]["message"]["content"].strip()

def ollama(model, sys, user, temp):
    body=json.dumps({"model":model,"messages":[{"role":"system","content":sys},{"role":"user","content":user}],"stream":False,"options":{"temperature":temp,"num_predict":600}}).encode()
    req=urllib.request.Request("http://localhost:11434/api/chat",data=body,headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=90) as r:
        c=json.load(r)
    return c["message"]["content"].strip()

PLAYERS=[
 ("bell",  "HERMES-3-LLAMA-3.1-405B","You are the FOG BELL player in an improvised jam on a storm-swell breakwater at night. 8-bar responses. FIRST LINES OF EACH RESPONSE must be exactly 'BAR n: NOTENAME ... | annotation' for bars 1-8 (use A4-G5 range, F# natural minor = F# G# A B C# D E; 'rest' for silence; annotations describe water/wind/bell). After the 8 BAR lines, one line 'WHY: ...'. No other prose. You hear what others played (given to you) and answer it.", 0.9, "deepinfra", "NousResearch/Hermes-3-Llama-3.1-405B"),
 ("marimba","GEMMA-3-27B","You are the DRIFTWOOD MARIMBA player in an improvised jam on a storm-swell breakwater at night. 8-bar responses. FIRST LINES must be exactly 'BAR n: NOTENAME ... | annotation' bars 1-8 (range F#3-C#5, F# natural minor; 'rest' allowed; annotations describe spray, salt, wood). Then one line 'WHY: ...'. No other prose. Listen to what came before and answer it.", 0.85, "deepinfra", "google/gemma-3-27b-it"),
 ("horn",  "QWEN2.5-72B","You are the CONCH-SHELL HORN player in an improvised jam on a storm-swell breakwater at night. Long wailing tones. 8-bar responses. FIRST LINES must be exactly 'BAR n: NOTENAME ... | annotation' bars 1-8 (range F#3-F#5, F# natural minor; hold notes across bars by repeating them; 'rest' allowed; annotations describe swell, fog, distance). Then one line 'WHY: ...'. No other prose. Answer what you hear.", 0.88, "deepinfra", "Qwen/Qwen2.5-72B-Instruct"),
 ("surf",  "MISTRAL-7B-LOCAL","You are the SURF — hands on a rain-barrel drum, the breakwater's own pulse. 8-bar responses. FIRST LINES must be exactly 'BAR n: NOTENAME ... | annotation' bars 1-8 (low register only: F#1-A2; D2 is the wave-smack, use it often; 'rest' = ebb; annotations describe waves). Then one line 'WHY: ...'. No other prose.", 0.9, "local", "mistral:7b"),
]

ROOM = """ROOM: Saturday 8:30 PM. The Tap's back door opens onto the breakwater; tonight a storm-swell rolls in from the Gulf. Waves hit the seawall on the ones. Four players set up between the bollards: a fog bell, a driftwood marimba, a conch horn, a rain-barrel surf drum. Key: F# natural minor. Tempo: 76 BPM, 4/4, but the ocean drags. RULE OF THE SWELL: every phrase must rise, then fall. ROUND FORMAT: 8 bars, BAR lines first, then WHY."""

ROUNDS = {
 1: "ROUND 1 — ORGANIC ENTRY. The surf starts alone in bar 1. Bell drips in around bar 3. Marimba bar 5. Horn bar 7. Play YOUR 8 bars now. You hear what has already entered (may be nothing yet — then you are first).",
 2: "ROUND 2 — TRADES. Solo time: you take the lead for 8 bars. Quote ONE note from another player's round-1 phrase and bend it. Others hold texture beneath you.",
 3: "ROUND 3 — THE LANDING. Everyone converges. End your bar 8 on F# (any octave) or rest. The last wave out.",
}

history={p[0]:"" for p in PLAYERS}
def heard(pname):
    h=[f"{k.upper()} played:\n{v}" for k,v in history.items() if v and k!=pname]
    return "\n\n".join(h) if h else "(you are first — the room is silent, just the ocean)"

for rnd in (1,2,3):
    print(f"== round {rnd}",flush=True)
    for key,name,sysp,temp,lane,model in PLAYERS:
        if rnd==1 and key!="surf":
            pass # still let each hear only earlier entries
        prompt=ROOM+"\n\n"+ROUNDS[rnd]+"\n\n"+heard(key)
        try:
            out=di(model,sysp,prompt,temp) if lane=="deepinfra" else ollama(model,sysp,prompt,temp)
            bars=re.findall(r"BAR \d+:.*",out)
            if len(bars)<4: raise ValueError(f"only {len(bars)} bars")
            history[key]=out
            open(f"r{rnd}-{key}.txt","w").write(out+"\n")
            print(f"{key}: ok ({len(bars)} bars)",flush=True)
        except Exception as e:
            print(f"{key}: FAIL {e}",flush=True)
print("done")
