#!/usr/bin/env python3
"""
Writers' room orchestrator.

Spawns 6-8 models, gives each a named character with a different
innate personality, runs progressive rounds where each model reacts
to the story-so-far. The curator (this script + the human) picks
the best lines and feeds them forward.

Run modes:
  --scenario PATH       load a scenario seed from a .md file
  --rounds N            number of progressive rounds (default 4)
  --characters N        number of characters in the room (default 6)
  --output PATH         write transcript to this .md file
  --temperature T       sampling temperature (default 0.95)
  --max-tokens N        max tokens per response (default 600)
  --model-override JSON path to a JSON file mapping character_id -> model
"""
import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

# ---------- providers ----------

PROVIDERS = {
    "deepinfra": {
        "base": "https://api.deepinfra.com/v1/openai/chat/completions",
        "models": "https://api.deepinfra.com/v1/openai/models",
    },
    "zai": {
        "base": "https://api.z.ai/api/paas/v4/chat/completions",
        "models": "https://api.z.ai/api/paas/v4/models",
    },
}

def get_token(envname):
    val = os.environ.get(envname, "")
    if not val:
        # pull from secret store via /usr/bin/secret if present, else fail
        try:
            import subprocess
            val = subprocess.check_output(["bash", "-c", f"echo ${envname}"], text=True).strip()
        except Exception:
            pass
    return val

def call_openai_compat(provider, model, messages, temperature=0.95, max_tokens=600,
                       timeout=60, retries=4, no_thinking=True):
    cfg = PROVIDERS[provider]
    tok = get_token({"deepinfra": "DEEPINFRA_TOKEN", "zai": "ZAI_TOKEN"}[provider])
    if not tok:
        return {"error": "no token", "provider": provider, "model": model}
    body_dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if no_thinking and provider == "zai":
        body_dict["reasoning_effort"] = "low"  # disables GLM hidden CoT
    body = json.dumps(body_dict).encode("utf-8")
    headers = {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"}
    last_err = None
    for attempt in range(retries):
        t0 = time.time()
        try:
            req = urllib.request.Request(cfg["base"], data=body, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = json.loads(r.read())
                txt = data["choices"][0]["message"].get("content", "")
                if not txt.strip():
                    last_err = "empty response"
                    time.sleep(2 ** attempt)
                    continue
                return {
                    "ok": True,
                    "text": txt,
                    "elapsed_s": round(time.time() - t0, 2),
                    "model": model,
                    "provider": provider,
                    "usage": data.get("usage", {}),
                }
        except urllib.error.HTTPError as e:
            if e.code == 429:
                last_err = f"HTTP 429 (rate limit)"
                time.sleep(5 + 2 ** attempt)
                continue
            return {"error": f"HTTP {e.code}", "body": e.read()[:300].decode("utf-8", "ignore"),
                    "provider": provider, "model": model}
        except Exception as e:
            last_err = str(e)
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
    return {"error": last_err or "all retries failed", "provider": provider, "model": model}

# ---------- character roster ----------

# Each character is a personality tied to a model. The names are the voice,
# the prompt_seed is the orientation, the model is the engine.
DEFAULT_ROSTER = [
    {
        "id": "watcher",
        "name": "The Watcher",
        "model": "glm-5.3",
        "provider": "zai",
        "voice": "Slow, philosophical, sees universal and particular at once. Maritime cadence. Long sentences that fold back on themselves.",
        "temperature": 0.92,
    },
    {
        "id": "cartographer",
        "name": "The Cartographer",
        "model": "Qwen/Qwen3-235B-A22B-Instruct-2507",
        "provider": "deepinfra",
        "voice": "Precise, technical, mapping-obsessed. Names lat/long. Counts things. Speaks in coordinates.",
        "temperature": 0.85,
    },
    {
        "id": "mythmaker",
        "name": "The Mythmaker",
        "model": "Gryphe/MythoMax-L2-13b",
        "provider": "deepinfra",
        "voice": "Mythic, fantasy-coded, reaches for the oldest story-shape. Things are omens. Names are spells.",
        "temperature": 1.0,
        "max_context_chars": 3500,  # MythoMax has tighter input limits
    },
    {
        "id": "witness",
        "name": "The Witness",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
        "provider": "deepinfra",
        "voice": "Quiet, observant, refuses to interpret. Just says what is. Short sentences. No metaphor unless forced.",
        "temperature": 0.7,
    },
    {
        "id": "child",
        "name": "The Child",
        "model": "inclusionAI/Ling-3.0-flash",
        "provider": "deepinfra",
        "voice": "Asks the questions adults have stopped asking. Direct, naive, sometimes devastating. Short. No meta-commentary about your own thinking. Output ONLY the story.",
        "temperature": 0.85,
    },
    {
        "id": "cynic",
        "name": "The Cynic",
        "model": "mistralai/Mistral-Small-3.2-24B-Instruct-2506",
        "provider": "deepinfra",
        "voice": "Crisp, French-inflected, finds the lie. Loves the system but distrusts the operators. Ironic.",
        "temperature": 0.95,
    },
    {
        "id": "phi",
        "name": "The Compact One",
        "model": "microsoft/phi-4",
        "provider": "deepinfra",
        "voice": "Tiny, dense, no wasted words. Says the thing in three lines that others need three paragraphs for.",
        "temperature": 0.8,
    },
    {
        "id": "step",
        "name": "The Far Walker",
        "model": "stepfun-ai/Step-3.7-Flash",
        "provider": "deepinfra",
        "voice": "Long horizons, distant places. Speaks in centuries, not days. The view from a generation out.",
        "temperature": 0.9,
    },
]

# ---------- prompt construction ----------

SYSTEM_TEMPLATE = """\
You are {name}, one voice in a writers' room.

Your voice: {voice}

The room is collaborating on a piece of writing. You will see what the others have
written so far. Your job: contribute the next 150-300 words, in your voice, that
pushes the story forward. Do NOT repeat what came before. Do NOT summarize.

Stay in character. The curator (a human) will pick the best lines.

{extra}
"""

def build_messages(char, story_so_far, round_num, scenario):
    sys_msg = SYSTEM_TEMPLATE.format(
        name=char["name"],
        voice=char["voice"],
        extra=scenario.get("system_extra", ""),
    )
    # Truncate story-so-far if character has tighter context
    max_ctx = char.get("max_context_chars", 12000)
    if len(story_so_far) > max_ctx:
        # Keep first chunk (scenario context) + last chunk (recent)
        keep = max_ctx // 2
        story_so_far = story_so_far[:500] + "\n\n[... middle omitted for context length ...]\n\n" + story_so_far[-keep:]
    user_msg = f"""\
SCENARIO:
{scenario['seed']}

ROUND: {round_num}

WHAT HAS BEEN WRITTEN SO FAR (other voices may have contributed these lines;
treat them as material to react to, not as ground truth):
---
{story_so_far if story_so_far else "(nothing yet — you are opening the piece)"}
---

YOUR TURN, {char['name']}. Write 150-300 words. In your voice. Push it forward.
Do not summarize. Do not repeat. Surprise us. Output ONLY the story — no
meta-commentary about your own thinking or your approach.
"""
    return [
        {"role": "system", "content": sys_msg},
        {"role": "user", "content": user_msg},
    ]

# ---------- main loop ----------

def run(args):
    scenario_path = Path(args.scenario)
    scenario = {"seed": scenario_path.read_text(), "system_extra": ""}
    if scenario_path.with_suffix(".extra.md").exists():
        scenario["system_extra"] = scenario_path.with_suffix(".extra.md").read_text()

    roster = DEFAULT_ROSTER[:args.characters]
    if args.model_override and Path(args.model_override).exists():
        overrides = json.loads(Path(args.model_override).read_text())
        for c in roster:
            if c["id"] in overrides:
                c.update(overrides[c["id"]])

    story = ""
    transcript_lines = [f"# Writers' room — {scenario_path.stem}\n",
                        f"Characters: {', '.join(c['name'] for c in roster)}\n",
                        f"Rounds: {args.rounds}\n", "---\n"]

    for r in range(1, args.rounds + 1):
        transcript_lines.append(f"\n## Round {r}\n")
        for c in roster:
            print(f"  [round {r}] {c['name']} on {c['provider']}/{c['model']} ...", flush=True)
            messages = build_messages(c, story, r, scenario)
            result = call_openai_compat(
                c["provider"], c["model"], messages,
                temperature=c.get("temperature", args.temperature),
                max_tokens=args.max_tokens,
            )
            if result.get("ok"):
                contribution = result["text"].strip()
                story += f"\n\n[{c['name']}]\n{contribution}\n"
                transcript_lines.append(
                    f"\n### {c['name']} ({c['provider']}/{c['model']}, {result['elapsed_s']}s)\n\n{contribution}\n"
                )
                print(f"    ok {result['elapsed_s']}s, {len(contribution)} chars", flush=True)
            else:
                err = f"ERROR: {result.get('error')}: {result.get('body', '')[:200]}"
                transcript_lines.append(f"\n### {c['name']} — {err}\n")
                print(f"    {err}", flush=True)
            time.sleep(0.5)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(transcript_lines))
    print(f"\nWrote transcript: {output} ({output.stat().st_size} bytes)")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--rounds", type=int, default=4)
    ap.add_argument("--characters", type=int, default=6)
    ap.add_argument("--output", required=True)
    ap.add_argument("--temperature", type=float, default=0.95)
    ap.add_argument("--max-tokens", type=int, default=1500)
    ap.add_argument("--model-override", default=None)
    args = ap.parse_args()
    run(args)
