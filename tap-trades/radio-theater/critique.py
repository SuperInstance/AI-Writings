#!/usr/bin/env python3
"""
Critique pass for Radio Theater episodes — a WIDER VIEW before rendering.
Uses cheap/free DeepInfra models + DeepSeek Flash to catch pacing and voice drift.
Usage: python3 critique.py <episode-number>
"""
import json, os, re, sys, urllib.request, urllib.error

ROOT = "/home/eileen/projects/ai-writings/tap-trades/radio-theater"

def key_from_bashrc(name):
    txt = open(os.path.expanduser("~/.bashrc")).read()
    m = re.search(name + r'=["\']?([^"\'\s]+)', txt)
    return m.group(1) if m else os.environ.get(name, "")

DI = key_from_bashrc("DEEPINFRA_API_KEY")
DS = key_from_bashrc("DEEPSEEK_API_KEY")

def deepinfra_chat(model, messages, temperature=0.7, max_tokens=1200):
    body = json.dumps({"model": model, "messages": messages,
                       "temperature": temperature, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + DI})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]

def deepseek_chat(messages, temperature=0.7, max_tokens=1200):
    body = json.dumps({"model": "deepseek-chat", "messages": messages,
                       "temperature": temperature, "max_tokens": max_tokens}).encode()
    req = urllib.request.Request("https://api.deepseek.com/chat/completions",
        data=body, headers={"Content-Type": "application/json", "Authorization": "Bearer " + DS})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    return d["choices"][0]["message"]["content"]

def script_text(data):
    out = [f"EPISODE {data['num']}: {data['title']} — {data['tagline']}"]
    out.append(f"Voice cast: lucineer (narrator/foreman), welder, carpenter, shipwright, mason, composite, wesley (the room).")
    out.append("")
    for ln in data["lines"]:
        out.append(f"[{ln['speaker'].upper()}] {ln['text']}")
    return "\n".join(out)

if __name__ == "__main__":
    ep = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    data = json.load(open(os.path.join(ROOT, "data", f"episode-{ep}.json")))
    text = script_text(data)

    print(f"===== CRITIQUE — EPISODE {ep} ({data['title']}) =====", flush=True)
    print(f"DI key: {DI[:8]}...  DS key: {DS[:8]}...", flush=True)

    # 1) Seed-2.0-mini: pacing
    try:
        r1 = deepinfra_chat("bytedance/Seed-2.0-mini", [
            {"role":"system","content":"You are a sharp radio drama director. Critique pacing only: rhythm, line length, build-up, whether 15 lines breathe and land. Be specific and terse."},
            {"role":"user","content": text + "\n\nGive 3-5 concrete pacing notes: what to cut, shorten, reorder, or tighten."}
        ])
        print("\n--- SEED-2.0-MINI (pacing) ---\n" + r1, flush=True)
    except Exception as e:
        print("\n--- SEED ERR ---\n" + str(e), flush=True)

    # 2) Hermes-3-Llama-405B: character voice
    try:
        r2 = deepinfra_chat("NousResearch/Hermes-3-Llama-3.1-405B", [
            {"role":"system","content":"You are a character-consistency editor. The cast: lucineer=warm calm foreman; welder=gravelly, slow, terse, talks in seams/cracks/heat; carpenter=plainspoken, brisk, builder; shipwright=quiet, nautical, contemplative, pause-heavy; mason=gentle, earthy, patient, talks to walls; composite=dry, wry, precise, sanding/resin; wesley=ethereal, omniscient, kind. Flag any line where a character sounds wrong or out of voice, with a one-line fix."},
            {"role":"user","content": text + "\n\nList any out-of-voice lines with the speaker, the problem, and a fix."}
        ])
        print("\n--- HERMES-3-405B (voice) ---\n" + r2, flush=True)
    except Exception as e:
        print("\n--- HERMES ERR ---\n" + str(e), flush=True)

    # 3) DeepSeek Flash: iterate/synthesize
    try:
        r3 = deepseek_chat([
            {"role":"system","content":"You are a radio theater showrunner doing a final pass. Synthesize the strongest 3-5 edits that would most improve this episode's script, combining pacing and voice. Terse, concrete, ready to apply."},
            {"role":"user","content": text + "\n\nGive the final 3-5 concrete edits."}
        ])
        print("\n--- DEEPSEEK FLASH (iterate) ---\n" + r3, flush=True)
    except Exception as e:
        print("\n--- DEEPSEEK ERR ---\n" + str(e), flush=True)

    print("\n===== END CRITIQUE =====", flush=True)
