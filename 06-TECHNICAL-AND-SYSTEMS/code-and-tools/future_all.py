"""
future_all.py — The seven futures, fully written to disk.
Each timeline gets: 1 draft from a "voice" model + 1 Socratic pass from a "teacher" model.
Output: /workspace/ai-writings-new/seed-canon/stories/11-17-*.md
"""
import urllib.request, urllib.error, json, os, time, re
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
    for attempt in range(3):
        try:
            t = time.time()
            r = urllib.request.urlopen(req, timeout=240)
            d = json.loads(r.read())
            ms = (time.time() - t) * 1000
            return d["choices"][0]["message"]["content"], ms
        except urllib.error.HTTPError as e:
            if attempt == 2: return f"ERR {e.code} {e.reason[:80]}", 0
            time.sleep(3 ** attempt)
        except Exception as e:
            if attempt == 2: return f"ERR {str(e)[:80]}", 0
            time.sleep(3 ** attempt)

TIMELINES = [
    {
        "n": "11",
        "label": "1 year from now (2027)",
        "year": "2027",
        "world": "Early adopters. The substrate is a real, working CLI. The cowboy is a tool Reyes uses. Some skeptics. A handful of fishing fleets. The 5 opcodes are documented but not yet invisible.",
        "voice": ("deepinfra", DEEPINFRA_TOKEN, "meta-llama/Llama-3.3-70B-Instruct", "near-future realist"),
        "teacher": ("deepinfra", DEEPINFRA_TOKEN, "Qwen/Qwen2.5-72B-Instruct", "Socratic teacher"),
        "title_hint": "The Morning Ritual",
    },
    {
        "n": "12",
        "label": "3 years from now (2029)",
        "year": "2029",
        "world": "The substrate is in 3 fishing fleets. The cell-graph handles weather routing, market pricing, and the morning ritual. Most crew don't know it's there. A junior dev is asked to explain it and can't.",
        "voice": ("deepinfra", DEEPINFRA_TOKEN, "Qwen/Qwen2.5-72B-Instruct", "deployment-period novelist"),
        "teacher": ("deepinfra", DEEPINFRA_TOKEN, "meta-llama/Llama-3.3-70B-Instruct", "Socratic editor"),
        "title_hint": "The Thing That Routes Boats",
    },
    {
        "n": "13",
        "label": "5 years from now (2031)",
        "year": "2031",
        "world": "The substrate is in a billion devices. A child's first sentence is a BIND-LINK-VIEW. Schoolchildren learn the 5 opcodes the way they learn the alphabet. Then they forget.",
        "voice": ("deepinfra", DEEPINFRA_TOKEN, "Qwen/Qwen2.5-72B-Instruct", "primary-school teacher voice"),
        "teacher": ("deepinfra", DEEPINFRA_TOKEN, "mistralai/Mistral-Small-24B-Instruct-2501", "compression poet"),
        "title_hint": "What We No Longer Learn",
    },
    {
        "n": "14",
        "label": "10 years from now (2036)",
        "year": "2036",
        "world": "The substrate is invisible. The captain of the F/V EILEEN V is 25. She's never seen a fishing boat without the cell-graph. Her grandmother remembers. The grandmother is fading.",
        "voice": ("zai", ZAI_TOKEN, "glm-5", "granddaughter's memory voice"),
        "teacher": ("deepinfra", DEEPINFRA_TOKEN, "Qwen/Qwen2.5-72B-Instruct", "Socratic teacher"),
        "title_hint": "The Grandmother Forgets",
    },
    {
        "n": "15",
        "label": "50 years from now (2076)",
        "year": "2076",
        "world": "The substrate is in the bedrock. People who still remember the 5 opcodes are like people who remember punch cards. The opcodes are taught in archaeology classes, not computer science. The cell-graph is the syntax of the bedrock.",
        "voice": ("zai", ZAI_TOKEN, "glm-5.3", "archaeology professor voice"),
        "teacher": ("zai", ZAI_TOKEN, "glm-5", "compressing archivist"),
        "title_hint": "The Bedrock Syntax",
    },
    {
        "n": "16",
        "label": "100 years from now (2126)",
        "year": "2126",
        "world": "The F/V EILEEN has been a museum ship for 60 years. The cell-graph still runs in its hull — the museum guides use it for navigation demos. A child asks: 'Is this the AI?' The guide says no.",
        "voice": ("zai", ZAI_TOKEN, "glm-5.3", "museum guide voice"),
        "teacher": ("deepinfra", DEEPINFRA_TOKEN, "mistralai/Mistral-Small-24B-Instruct-2501", "compression poet"),
        "title_hint": "The Guide Says No",
    },
    {
        "n": "17",
        "label": "1000 years from now (3026)",
        "year": "3026",
        "world": "The F/V EILEEN is a ruin. A deep-time archeologist pulls a strange thing from the silt — a tablet. On it: a 5-line poem. The archeologist does not know that the lines are the 5 opcodes. The opcodes are the first symbolic letters of the post-human era.",
        "voice": ("zai", ZAI_TOKEN, "glm-5.3", "post-historical voice"),
        "teacher": ("deepinfra", DEEPINFRA_TOKEN, "mistralai/Mistral-Small-24B-Instruct-2501", "compression poet"),
        "title_hint": "The First Symbolic Letters",
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
- Do NOT add meta commentary

Return ONLY the final story."""

def make_voice_messages(t):
    return [
        {"role": "system", "content": SYS_VOICE.format(
            label=t["label"], world=t["world"], title_hint=t["title_hint"])},
        {"role": "user", "content": f"Write the {t['label']} story. Title: {t['title_hint']}. ~700 words. Begin with the title."}
    ]

def make_teacher_messages(t, draft):
    return [
        {"role": "system", "content": SYS_TEACHER},
        {"role": "user", "content": f"Draft:\n\n{draft}\n\nNow rewrite as the final version. ~700 words. Begin with the title."}
    ]

def process_timeline(t):
    src, tok, mdl, role = t["voice"]
    if not tok: return f"NO TOKEN for {t['label']}"
    url = DEEPINFRA if src == "deepinfra" else ZAI
    msgs = make_voice_messages(t)
    draft, ms1 = call(url, tok, mdl, msgs, max_tokens=1700, temperature=0.85)
    print(f"  [{t['label']}] VOICE  ({mdl}, {role}): {ms1:.0f}ms, {len(draft)} chars")

    # Teacher pass
    src2, tok2, mdl2, role2 = t["teacher"]
    if not tok2:
        final = draft
    else:
        url2 = DEEPINFRA if src2 == "deepinfra" else ZAI
        msgs2 = make_teacher_messages(t, draft)
        final, ms2 = call(url2, tok2, mdl2, msgs2, max_tokens=1700, temperature=0.7)
        print(f"  [{t['label']}] TEACHER({mdl2}, {role2}): {ms2:.0f}ms, {len(final)} chars")

    # Write to disk
    out = f"""# Story {t['n']}: {t['title_hint']} — {t['label']}

{final.strip()}

---

*Written in the writers' room, 2026-08-25. Setting: {t['label']}.*
*Voice: {role}. Teacher: {role2}.*
*Companion to Fable 68 (The Cowboy at the Foundation) and Paper 137 (The Gold).*
"""
    out_path = f"/workspace/ai-writings-new/seed-canon/stories/{t['n']}-{re.sub(r'[^a-z0-9-]', '-', t['title_hint'].lower())}.md"
    with open(out_path, "w") as f:
        f.write(out)
    print(f"  [{t['label']}] WROTE: {out_path}")
    return out_path

if __name__ == "__main__":
    # Run all 7 in parallel
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = {pool.submit(process_timeline, t): t["label"] for t in TIMELINES}
        for f in as_completed(futs):
            try:
                r = f.result()
                print(f"Done: {futs[f]}")
            except Exception as e:
                print(f"FAILED: {futs[f]}: {e}")
