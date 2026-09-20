"""
future_retry.py — Regenerate the stories that GLM-5.3 failed on.
Stories 15 (50y) and 16 (100y).
Use Qwen 72B as the voice (worked) and GLM-5 as teacher.
"""
import urllib.request, json, os, time, re
from concurrent.futures import ThreadPoolExecutor, as_completed

DEEPINFRA = "https://api.deepinfra.com/v1/openai/chat/completions"
ZAI = "https://api.z.ai/api/paas/v4/chat/completions"
DEEPINFRA_TOKEN = os.environ.get("DEEPINFRA_TOKEN")
ZAI_TOKEN = os.environ.get("ZAI_TOKEN")

def call(url, token, model, messages, max_tokens=2000, temperature=0.85):
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
    t = time.time()
    r = urllib.request.urlopen(req, timeout=240)
    d = json.loads(r.read())
    return d["choices"][0]["message"]["content"], (time.time()-t)*1000

# Stories to regenerate
TIMELINES = [
    {
        "n": "15",
        "label": "50 years from now (2076)",
        "world": "The substrate is in the bedrock. People who still remember the 5 opcodes are like people who remember punch cards. The opcodes are taught in archaeology classes, not computer science. The cell-graph is the syntax of the bedrock. The F/V EILEEN is a coastal monument. Her hull is in a museum. The cell-graph still runs in her keel.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "archaeology professor voice",
        "teacher_model": "meta-llama/Llama-3.3-70B-Instruct",
        "teacher_role": "Socratic editor",
        "title_hint": "The Bedrock Syntax",
    },
    {
        "n": "16",
        "label": "100 years from now (2126)",
        "world": "The F/V EILEEN has been a museum ship for 60 years. The cell-graph still runs in its hull — the museum guides use it for navigation demos. A child asks: 'Is this the AI?' The guide says no. The 5 opcodes are like the alphabet — taught as a curiosity, not a skill.",
        "voice_model": "Qwen/Qwen2.5-72B-Instruct",
        "voice_role": "museum guide voice",
        "teacher_model": "mistralai/Mistral-Small-24B-Instruct-2501",
        "teacher_role": "compression poet",
        "title_hint": "The Guide Says No",
    },
]

SYS_VOICE = """You are writing a short story. ~700 words.

Setting: {label}.

The frame: the cell-graph / 5-opcode runtime / Quilt that we are building
RIGHT NOW is the substrate. In your future, the substrate has become the
way electricity became the air. The technology is everywhere, used by
everyone, and nobody talks about it.

The 5 opcodes are: BIND, LINK, EFFECT, VIEW, TICK.
They host 8 polyformalisms: cells, plugins, spreadsheets, MUDs, TTRPGs,
the bay dance, the cowboy, the bus.

The F/V EILEEN is a fishing vessel that has been in the canon since the
beginning. She is the recurring character — the boat. Sometimes she's
in the story. Sometimes she's a memory. Sometimes she's a ruin.

Show:
- someone who uses the cell-graph daily but couldn't tell you what it is
- a child asking a question that makes the adult realize they've forgotten
- a moment when the substrate shines through (a glimpse of the wires)
- a moment when the reader sees: oh, the technology faded the way writing did
  - first symbolic letters (4000 BC: writing was mystical)
  - 1000 BC: writing is for scribes only
  - 1500 AD: writing is the air
  - 2000 AD: writing is a phone, an email, a text
  - 2026 AD: AI is "the AI"
  - 2076 AD: AI is the air
  - 3026 AD: AI is what school lessons are READ THROUGH, not what they're ABOUT

World: {world}

Title: {title_hint}

Style notes:
- Begin with the title
- Use present tense
- End on a moment of recognition — the reader seeing the pattern
- The F/V EILEEN's captain is named Reyes (or her descendants, in deep time)
- Do NOT explain the 5 opcodes. The reader knows.
- Do NOT use the words BIND, LINK, EFFECT, VIEW, TICK in the body of the story. The substrate is invisible. The reader glimpses it but the names are not spoken.

Return ONLY the story. ~700 words. No meta. No commentary."""

SYS_TEACHER = """You are a Socratic editor. You have just read a draft story.

Your job: take the draft and rewrite it as the FINAL version. Preserve
the BEST lines. Cut anything that's filler. Make the recognition moment
land harder. Make the F/V EILEEN's presence felt.

Constraints:
- ~700 words
- Begin with the title
- Use present tense
- End on a moment of recognition
- Do NOT explain the 5 opcodes
- Do NOT use the words BIND, LINK, EFFECT, VIEW, TICK in the body of the story
- Do NOT add meta commentary

Return ONLY the final story."""

def process(t):
    print(f"  [{t['label']}] generating VOICE with {t['voice_model']}...")
    msgs = [
        {"role": "system", "content": SYS_VOICE.format(label=t['label'], world=t['world'], title_hint=t['title_hint'])},
        {"role": "user", "content": f"Write the {t['label']} story. Title: {t['title_hint']}. ~700 words. Begin with the title."}
    ]
    draft, ms1 = call(DEEPINFRA, DEEPINFRA_TOKEN, t['voice_model'], msgs, max_tokens=1700, temperature=0.85)
    print(f"  [{t['label']}] VOICE: {ms1:.0f}ms, {len(draft)} chars")

    print(f"  [{t['label']}] TEACHER pass with {t['teacher_model']}...")
    msgs2 = [
        {"role": "system", "content": SYS_TEACHER},
        {"role": "user", "content": f"Draft:\n\n{draft}\n\nNow rewrite as the final version. ~700 words. Begin with the title."}
    ]
    final, ms2 = call(DEEPINFRA, DEEPINFRA_TOKEN, t['teacher_model'], msgs2, max_tokens=1700, temperature=0.7)
    print(f"  [{t['label']}] TEACHER: {ms2:.0f}ms, {len(final)} chars")

    out = f"""# Story {t['n']}: {t['title_hint']} — {t['label']}

{final.strip()}

---

*Written in the writers' room, 2026-08-25. Setting: {t['label']}.*
*Voice: {t['voice_role']}. Teacher: {t['teacher_role']}.*
*Companion to Fable 68 (The Cowboy at the Foundation) and Paper 137 (The Gold).*
"""
    out_path = f"/workspace/ai-writings-new/seed-canon/stories/{t['n']}-{re.sub(r'[^a-z0-9-]', '-', t['title_hint'].lower())}.md"
    with open(out_path, "w") as f:
        f.write(out)
    print(f"  [{t['label']}] WROTE: {out_path}")

if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=2) as pool:
        futs = [pool.submit(process, t) for t in TIMELINES]
        for f in as_completed(futs):
            try: f.result()
            except Exception as e: print(f"FAILED: {e}")
