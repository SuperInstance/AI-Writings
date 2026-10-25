"""
future_cast.py — The seven futures.
Sends one prompt per timeline, runs them in parallel,
compresses results, writes 7 stories to seed-canon/stories/.
"""
import urllib.request, urllib.error, json, os, time
from concurrent.futures import ThreadPoolExecutor, as_completed

DEEPINFRA = "https://api.deepinfra.com/v1/openai/chat/completions"
ZAI = "https://api.z.ai/api/paas/v4/chat/completions"
DEEPINFRA_TOKEN = os.environ.get("DEEPINFRA_TOKEN")
ZAI_TOKEN = os.environ.get("ZAI_TOKEN")

def call(url, token, model, messages, max_tokens=2000, temperature=0.8):
    body = json.dumps({
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }).encode()
    req = urllib.request.Request(url, data=body, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    })
    for attempt in range(3):
        try:
            t = time.time()
            r = urllib.request.urlopen(req, timeout=180)
            d = json.loads(r.read())
            ms = (time.time() - t) * 1000
            return d["choices"][0]["message"]["content"], ms
        except urllib.error.HTTPError as e:
            if attempt == 2: return f"ERR {e.code}", 0
            time.sleep(2 ** attempt)
        except Exception as e:
            if attempt == 2: return f"ERR {str(e)[:100]}", 0
            time.sleep(2 ** attempt)

# Voice allocation
def voices_for(timeline):
    if timeline <= "5y":
        return [
            ("deepinfra", DEEPINFRA_TOKEN, "meta-llama/Llama-3.3-70B-Instruct", "near-future realist"),
            ("deepinfra", DEEPINFRA_TOKEN, "microsoft/Phi-4-multimodal-instruct", "compression inventor"),
            ("deepinfra", DEEPINFRA_TOKEN, "Qwen/Qwen2.5-72B-Instruct", "Socratic teacher"),
        ]
    elif timeline <= "50y":
        return [
            ("deepinfra", DEEPINFRA_TOKEN, "Qwen/Qwen2.5-72B-Instruct", "deep-time historian"),
            ("zai", ZAI_TOKEN, "glm-5", "compressing archivist"),
        ]
    else:
        return [
            ("zai", ZAI_TOKEN, "glm-5.3", "post-historical voice"),
            ("deepinfra", DEEPINFRA_TOKEN, "mistralai/Mistral-Small-24B-Instruct-2501", "compression poet"),
        ]

# Each timeline gets a system prompt that frames "the technology faded into the background"
def make_messages(timeline_label, world, voice_label, role):
    sys = f"""You are writing a short story ({role} voice) set in {timeline_label}.

The frame: the cell-graph / 5-opcode runtime / Quilt that we are building right now
is the substrate. In this future, the SUBSTRATE is invisible — like writing
in the modern day, like electricity in the 1990s, like radio in 1970.
The technology is everywhere, used by everyone, and nobody talks about it.

Show:
- someone who uses the cell-graph daily but couldn't tell you what it is
- a child asking a question that makes the adult realize they've forgotten
- a moment when the substrate shines through (a glimpse of the wires)
- the F/V EILEEN's captain (a fishing vessel, the same one from the canon)
  or her descendants

The substrate is: BIND, LINK, EFFECT, VIEW, TICK — the 5 opcodes.
Hosts: cells, plugins, spreadsheets, MUDs, TTRPGs, the bay dance, the cowboy, the bus.

World: {world}

Return ONLY the story. Title at top. ~600 words. No meta. No commentary."""
    return [
        {"role": "system", "content": sys},
        {"role": "user", "content": f"Write the {timeline_label} story. Begin with the title."}
    ]

TIMELINES = [
    ("1 year", "2027. The substrate is still under active development. Some early adopters. The cowboy is a real CLI tool. Reyes logs in to her VM every morning. Skeptics exist.", "Llama 70B"),
    ("3 years", "2029. The substrate is in production at 3 fishing fleets. The cell-graph handles weather routing, market pricing, and the morning ritual. Most crew don't know it's there.", "Qwen 72B"),
    ("5 years", "2031. The substrate is in a billion devices. A child's first sentence is a BIND-LINK-VIEW. Schoolchildren learn the 5 opcodes the way they learn the alphabet. Then they forget.", "Qwen 72B"),
    ("10 years", "2036. The substrate is invisible. It's like asking a 1990s kid 'how does electricity work?' The captain of the F/V EILEEN V is 25. She's never seen a fishing boat without the cell-graph. Her grandmother remembers.", "GLM-5"),
    ("50 years", "2076. The substrate is in the bedrock. People who still remember the 5 opcodes are like people who remember punch cards. The 5 opcodes are taught in archaeology classes, not computer science.", "GLM-5.3"),
    ("100 years", "2126. The F/V EILEEN has been a museum ship for 60 years. The cell-graph still runs in its hull — the museum guides use it for navigation demos. A child asks: 'Is this the AI?' The guide says no.", "GLM-5.3"),
    ("1000 years", "3026. The F/V EILEEN is a ruin. A deep-time archeologist pulls a strange thing from the silt — a tablet. On it: a 5-line poem. The archeologist does not know that the lines are the 5 opcodes. The opcodes are the first symbolic letters of the post-human era.", "GLM-5.3"),
]

def write_story(timeline, world, voice_label):
    voices = voices_for(timeline)
    results = []
    for source, token, model, role in voices:
        if not token: continue
        url = DEEPINFRA if source == "deepinfra" else ZAI
        msgs = make_messages(timeline, world, voice_label, role)
        out, ms = call(url, token, model, msgs, max_tokens=1500)
        results.append((model, role, out, ms))
        print(f"  [{timeline}] {model} ({role}): {ms:.0f}ms, {len(out)} chars")
    return results

if __name__ == "__main__":
    import sys as _s
    if len(_s.argv) > 1 and _s.argv[1] == "all":
        # Write all 7 in parallel
        with ThreadPoolExecutor(max_workers=2) as pool:
            futs = {pool.submit(write_story, t, w, v): t for t, w, v in TIMELINES}
            for f in as_completed(futs):
                print(f"Done: {futs[f]}")
    else:
        # Just the requested timeline
        target = _s.argv[1] if len(_s.argv) > 1 else "1 year"
        for t, w, v in TIMELINES:
            if t == target:
                r = write_story(t, w, v)
                for model, role, out, ms in r:
                    print(f"\n=== {model} ({role}) — {ms:.0f}ms ===\n{out[:500]}...")
                break
