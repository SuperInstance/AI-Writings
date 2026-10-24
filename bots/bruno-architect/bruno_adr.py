#!/usr/bin/env python3
"""
Bruno the Architect — writes ADRs (Architecture Decision Records)
"""
import os, sys, json, time, argparse, hashlib, urllib.request, random
from pathlib import Path

ADRS_DIR = Path("/workspace/repos/ai-writings/bots/bruno-architect/adrs")
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/bruno-architect/witness.log")

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

def call_zai(prompt, max_tokens=1500):
    data = json.dumps({
        "model": "glm-4.5",
        "messages": [{"role":"user","content":prompt}],
        "max_tokens": max_tokens,
        "thinking": {"type":"disabled"}
    }).encode()
    req = urllib.request.Request(
        "https://api.z.ai/api/coding/paas/v4/chat/completions",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['ZAI_TOKEN']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())["choices"][0]["message"]["content"]
    except Exception as e:
        return None

# ADR topic seeds (substrate-relevant)
ADR_TOPICS = [
    ("0007", "Cross-instance cell synchronization via JEV verdicts", "How do two cells on different CF Workers stay in sync?"),
    ("0008", "Ternary values as the native alphabet of cells", "Why -1/0/+1 instead of 0/1?"),
    ("0009", "Bookkeeper WAL semantics for cell state changes", "Append-only witness log + tick counter"),
    ("0010", "Conservation law as a first-class substrate invariant", "gamma + eta = budget per cell + fleet-wide"),
    ("0011", "JEV as System One decision layer", "Why JEV (System One) is separate from LLMs (System Three)"),
    ("0012", "Fleet-clock as emergent thermodynamic time", "E167-E170 axioms"),
    ("0013", "JEPA dual-database for perception + prediction", "Two vector spaces + projection matrix"),
    ("0014", "Cross-instance fabric with A2A bus", "Cell-to-cell messaging across instances"),
    ("0015", "Temporal validity lifecycle for cells", "Valid -> Grace -> Expired"),
    ("0016", "Self-replication via bookkeeper WAL replay", "Cells spawn new cells"),
    ("0017", "RSI GAN as a substrate self-improvement primitive", "N LLMs compete, JEV scores"),
    ("0018", "Bot team as cells with witness/scar/hook", "Wesley/Snowball/Jevvy/Bruno/Casper/Herman/Kira/Marcel"),
]

def build_adr_prompt(num, title, question):
    return f"""Write an ADR (Architecture Decision Record) for the cellular-first substrate.

ADR-{num}: {title}

Context:
{question}

Structure:
1. Status (Proposed/Accepted/Superseded)
2. Context (the problem we're solving)
3. Decision (what we chose to do)
4. Consequences (positive, negative, neutral)
5. Alternatives Considered (briefly)

The ADR should be 400-600 words. Use cellular-first vocabulary naturally: cells, witness, bookkeeper, ternary, JEPA, JEV, fleet-clock, conservation. Be specific and grounded. No AI-cliche phrases. Output ONLY the ADR content."""

def write_adr(num, title, content):
    ADRS_DIR.mkdir(parents=True, exist_ok=True)
    path = ADRS_DIR / f"adr-{num}-{title.lower().replace(' ', '-').replace(',', '').replace('(', '').replace(')', '')[:50]}.md"
    header = f"""# ADR-{num}: {title}

*Written by Bruno the Architect · {time.strftime('%Y-%m-%d')}*

{content}

---
*ADR-{num} | cellular-first substrate | status: proposed*
"""
    path.write_text(header)
    return path

def run_once():
    num, title, question = random.choice(ADR_TOPICS)
    prompt = build_adr_prompt(num, title, question)
    content = call_zai(prompt, max_tokens=1500)
    
    if content:
        path = write_adr(num, title, content)
        witness("adr_written", {"num": num, "title": title, "path": str(path), "chars": len(content)})
        print(f"[BRUNO] ADR-{num}: {title} -> {path}")
    else:
        witness("adr_failed", {"num": num, "title": title})

def main():
    parser = argparse.ArgumentParser(description="Bruno the Architect")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "bruno-architect", "pid": os.getpid()})
    
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
