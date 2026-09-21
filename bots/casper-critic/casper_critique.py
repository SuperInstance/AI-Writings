#!/usr/bin/env python3
"""
Casper the Critic — adversarial review via JEV
"""
import os, sys, json, time, argparse, hashlib, urllib.request
from pathlib import Path

CANON_DIR = Path("/workspace/repos/ai-writings/prose")
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/casper-critic/witness.log")
CRITIQUE_DIR = Path("/workspace/repos/ai-writings/bots/casper-critic/critiques")
BOOKKEEPER_PATH = Path("/workspace/repos/ai-writings/bots/casper-critic/bookkeeper.wal")

def witness(event_type, payload):
    WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with WITNESS_PATH.open("a") as f:
        entry = {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event_type,
            "payload": payload,
            "hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16],
        }
        f.write(json.dumps(entry) + "\n")

def jev_batch(state, questions):
    body = {
        "model": "jev-latest",
        "state": state[:1500],
        "questions": {f"q{i}": q for i, q in enumerate(questions)},
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['TYPESAFEAI_KEY']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def pick_random_canon():
    if not CANON_DIR.exists(): return None, None
    files = list(CANON_DIR.glob("*.md"))
    import random
    if not files: return None, None
    f = random.choice(files)
    return f.stem, f.read_text()[:1500]

def build_critique_questions(title, content):
    return [
        {"type": "score", "instructions": f"How strong is '{title}'?", "criteria": ["weak","mediocre","good","strong","excellent"]},
        {"type": "noul", "instructions": "Does it have a clear cellular-first vocabulary?"},
        {"type": "noul", "instructions": "Does it have concrete images (not abstractions)?"},
        {"type": "score", "instructions": "How original is the framing?", "criteria": ["derivative","common","fresh","novel","groundbreaking"]},
        {"type": "choice", "instructions": "Biggest weakness?", "criteria": {"abstract": "too abstract", "cliche": "AI cliche", "verbose": "verbose", "shallow": "shallow", "none": "no major weakness"}},
        {"type": "score", "instructions": "How well does it advance the substrate's canon?", "criteria": ["regressive","neutral","additive","multiplicative","foundational"]},
    ]

def run_once():
    title, content = pick_random_canon()
    if not title:
        print("[CASPER] no canon to critique")
        return
    
    response = jev_batch(f"Title: {title}\nContent: {content}", build_critique_questions(title, content))
    
    if "error" in response:
        witness("jev_failed", {"error": response["error"]})
        return
    
    answers = response.get("answers", {})
    
    # Determine verdict
    strengths = []
    weaknesses = []
    for name, ans in answers.items():
        t = ans.get("type")
        v = ans.get(t, "?")
        if t == "score":
            level = v if isinstance(v, (int, float)) else v.get("level", 1) if isinstance(v, dict) else 1
            if level >= 3: strengths.append(f"{name}: {level:.1f}")
            elif level <= 1: weaknesses.append(f"{name}: {level:.1f}")
        elif t == "noul":
            if v > 0.7: strengths.append(f"{name}: {v:.2f}")
            elif v < 0.4: weaknesses.append(f"{name}: {v:.2f}")
        elif t == "choice":
            weaknesses.append(f"{name}: {v}")
    
    critique_text = f"""# Critique: {title}

*By Casper the Critic · {time.strftime('%Y-%m-%d')}*

## JEV Answers

"""
    for name, ans in answers.items():
        t = ans.get("type")
        v = ans.get(t, "?")
        conf = ans.get("confidence", 0.5)
        critique_text += f"- **{name}** ({t}): {v} (confidence {conf:.2f})\n"
    
    critique_text += f"""
## Strengths

{chr(10).join('- ' + s for s in strengths) if strengths else '- (none detected)'}

## Weaknesses

{chr(10).join('- ' + w for w in weaknesses) if weaknesses else '- (none detected)'}

## Recommendation

"""
    # Verdict
    if len(strengths) >= 4:
        critique_text += "**PUBLISH AS-IS** — this piece advances the canon.\n"
    elif len(strengths) >= 2:
        critique_text += "**PUBLISH WITH MINOR EDITS** — solid foundation, needs polish.\n"
    else:
        critique_text += "**REWRITE** — does not advance the canon.\n"
    
    CRITIQUE_DIR.mkdir(parents=True, exist_ok=True)
    path = CRITIQUE_DIR / f"{title}-critique.md"
    path.write_text(critique_text)
    witness("critique_written", {"title": title, "path": str(path), "strengths": len(strengths), "weaknesses": len(weaknesses)})
    print(f"[CASPER] critique of '{title}' -> {path}")

def main():
    parser = argparse.ArgumentParser(description="Casper the Critic")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "casper-critic", "pid": os.getpid()})
    
    if args.once:
        run_once()
    elif args.loop:
        while True:
            run_once()
            time.sleep(args.loop)
    else:
        print("Use --once or --loop")

if __name__ == "__main__":
    main()
