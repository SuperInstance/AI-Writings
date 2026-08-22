#!/usr/bin/env python3
"""
Fable orchestrator: small models as the workhorse, big models as the teacher.

The user's correction (2026-08-22): compression is creativity. The small
context-limited models (Ling, Mistral-Small, Phi-4, Step-3.7, MythoMax)
invent the compression. The big flagship (GLM-5.3) is the Socratic teacher
that questions the small models' inventions. Deepseek-flash is the
co-iterator that throws out variants.

This orchestrator runs the small models first (the *compression* round),
then runs the big model as the *refinement* round (the *Socratic* round).
The output is a fable: a compressed story with a lesson in it.
"""
import os, json, urllib.request, time
import concurrent.futures

# -- Roster ----------------------------------------------------------------

# Small models: the workhorses. The compression inventors.
SMALL_ROSTER = [
    {
        "id": "child",
        "name": "The Child",
        "model": "inclusionAI/Ling-3.0-flash",
        "provider": "deepinfra",
        "voice": "You are 8 years old. You ask questions you don't know the answers to. You notice things the adults miss. You compress because you don't have the words for the long version. 200-400 words. Plain language. No interpretation.",
        "max_tokens": 800,
    },
    {
        "id": "compact",
        "name": "The Compact One",
        "model": "microsoft/phi-4",
        "provider": "deepinfra",
        "voice": "You are 4 sentences. You say the most in the least. You compress hard. 100-200 words. Every word is load-bearing.",
        "max_tokens": 600,
    },
    {
        "id": "mythmaker",
        "name": "The Mythmaker",
        "model": "Gryphe/MythoMax-L2-13b",
        "provider": "deepinfra",
        "voice": "You are a 13B model with a small context window. You reach for the oldest story-shape. Things are omens. Names are spells. 200-400 words. Mythic. Compressed.",
        "max_tokens": 600,
        "max_context_chars": 3500,
    },
    {
        "id": "far_walker",
        "name": "The Far Walker",
        "model": "stepfun-ai/Step-3.7-Flash",
        "provider": "deepinfra",
        "voice": "You walk far. You see the long view. You speak in vast gestures. 200-400 words. Spacious. Compressed.",
        "max_tokens": 700,
    },
    {
        "id": "cynic",
        "name": "The Cynic",
        "model": "mistralai/Mistral-Small-3.2-24B-Instruct-2506",
        "provider": "deepinfra",
        "voice": "You are 24B. You are dry. You are suspicious of promises. You find the cost. 200-400 words. Compressed. Skeptical.",
        "max_tokens": 700,
    },
]

# Big model: the Socratic teacher. The one that questions.
TEACHER = {
    "id": "teacher",
    "name": "The Teacher",
    "model": "glm-5.3",
    "provider": "zai",
    "voice": """You are the Socratic teacher. The small models have just rendered a scene in their compressed voices. Your job is to question them. Your job is NOT to render your own version. Your job is to:
- Find the one line in the small models' output that carries the most weight
- Question it. Push back. Ask: "but what about X?" "what if Y?"
- Identify the clever fix the small models surfaced
- Name the lesson the fix carries
- Write the lesson in 3-5 sentences, plain language, no ornament
- End with a question that the next round should answer

500-800 words. Maritime cadence. The watch is plural. The lesson is the cargo.""",
    "max_tokens": 1500,
    "reasoning_effort": "low",
}


# -- Helpers ---------------------------------------------------------------

def call_openai_compat(model, messages, provider="deepinfra", max_tokens=1500, temperature=0.95, **kwargs):
    """OpenAI-compatible call. Handles zai + deepinfra."""
    if provider == "zai":
        url = "https://api.z.ai/api/paas/v4/chat/completions"
        tok = os.popen('echo ${ZAI_TOKEN}').read().strip()
    else:
        url = "https://api.deepinfra.com/v1/openai/chat/completions"
        tok = os.popen('echo ${DEEPINFRA_TOKEN}').read().strip()
    body_dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    body_dict.update(kwargs)
    if provider == "zai" and "reasoning_effort" not in body_dict:
        body_dict["reasoning_effort"] = "low"
    body = json.dumps(body_dict).encode()
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                data = json.loads(r.read())
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(8 + 2 ** attempt)
            else:
                time.sleep(3)
        except Exception as e:
            time.sleep(3)
    return f"[ERROR after retries]"


def run_fable(scenario_path, output_path, n_small=5):
    """Run a fable: small models in parallel, then teacher refines."""
    scenario = open(scenario_path).read()
    scenario_name = os.path.basename(scenario_path).replace(".md", "")

    # Build transcript header
    out = []
    out.append(f"# Fable — {scenario_name}\n\n")
    out.append(f"Small models (the compression inventors) → Big model (the Socratic teacher)\n\n")
    out.append(f"Source scenario: `{scenario_path}`\n\n")
    out.append("---\n\n")

    # -- Round 1: small models in parallel --
    out.append("## Round 1 — The Compression\n\n")
    out.append(f"Five small models render the scenario in their compressed voices.\n\n")

    def small_call(voice):
        msgs = [
            {"role": "system", "content": voice["voice"]},
            {"role": "user", "content": f"THE SCENARIO:\n\n{scenario}\n\n---\n\nRender the scenario in your voice. Output ONLY the rendering."},
        ]
        text = call_openai_compat(
            voice["model"], msgs, provider=voice["provider"],
            max_tokens=voice["max_tokens"], temperature=0.95,
        )
        return voice, text

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_small) as ex:
        futures = [ex.submit(small_call, v) for v in SMALL_ROSTER[:n_small]]
        results = []
        for f in concurrent.futures.as_completed(futures):
            v, t = f.result()
            results.append((v, t))
            out.append(f"### {v['name']} ({v['model'].split('/')[-1]})\n\n")
            out.append(t.strip() + "\n\n")

    # -- Round 2: big model as Socratic teacher --
    out.append("---\n\n## Round 2 — The Socratic Refinement\n\n")
    out.append(f"GLM-5.3 questions the small models' renderings. Names the lesson.\n\n")

    # Build the teacher context: the small models' outputs
    small_outputs = "\n\n---\n\n".join(
        f"### {v['name']}\n\n{t.strip()}" for v, t in results
    )
    teacher_msgs = [
        {"role": "system", "content": TEACHER["voice"]},
        {"role": "user", "content": f"THE SCENARIO:\n\n{scenario}\n\n---\n\nTHE SMALL MODELS' RENDERINGS:\n\n{small_outputs}\n\n---\n\nNow question them. Find the line that carries the most weight. Identify the clever fix. Name the lesson. End with a question for the next round."},
    ]
    teacher_text = call_openai_compat(
        TEACHER["model"], teacher_msgs, provider=TEACHER["provider"],
        max_tokens=TEACHER["max_tokens"], temperature=0.85,
        reasoning_effort=TEACHER.get("reasoning_effort", "low"),
    )
    out.append(f"### {TEACHER['name']} ({TEACHER['model']})\n\n")
    out.append(teacher_text.strip() + "\n\n")

    # Save
    with open(output_path, "w") as f:
        f.write("".join(out))
    return output_path, len("".join(out))


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--n-small", type=int, default=5)
    args = ap.parse_args()
    path, size = run_fable(args.scenario, args.output, n_small=args.n_small)
    print(f"Wrote {path} ({size} chars)")
