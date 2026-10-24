#!/usr/bin/env python3
"""
Substrate Bus — shared witness log across all bots
A bot-to-bot messaging system via append-only substrate-wide witness.jsonl
"""
import os, sys, json, time, argparse, hashlib, urllib.request
from pathlib import Path
from datetime import datetime, timezone

# Substrate-wide witness log
SUBSTRATE_WITNESS = Path("/workspace/repos/ai-writings/bots/substrate-bus/substrate-witness.jsonl")
SUBSTRATE_TOPICS = Path("/workspace/repos/ai-writings/bots/substrate-bus/topics.json")

def now():
    return datetime.now(timezone.utc).isoformat()

def witness(event_type, source_bot, payload, recipients=None):
    """Write to substrate-wide witness log"""
    SUBSTRATE_WITNESS.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "ts": time.time(),
        "iso": now(),
        "event": event_type,
        "source": source_bot,
        "payload": payload,
        "recipients": recipients or [],
        "hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16],
    }
    with SUBSTRATE_WITNESS.open("a") as f:
        f.write(json.dumps(entry) + "\n")
    return entry

def publish(topic, source_bot, content, recipients=None):
    """Publish a message on a topic - other bots can subscribe"""
    topics = {}
    if SUBSTRATE_TOPICS.exists():
        topics = json.loads(SUBSTRATE_TOPICS.read_text())
    
    if topic not in topics:
        topics[topic] = []
    
    topics[topic].append({
        "ts": time.time(),
        "iso": now(),
        "source": source_bot,
        "content": content,
        "recipients": recipients or [],
    })
    SUBSTRATE_TOPICS.write_text(json.dumps(topics, indent=2))
    return {"topic": topic, "subscribers": len(topics[topic])}

def read_recent(n=20):
    if not SUBSTRATE_WITNESS.exists():
        return []
    lines = SUBSTRATE_WITNESS.read_text().strip().split("\n")[-n:]
    return [json.loads(l) for l in lines if l.strip()]

def read_topic(topic, since_minutes=60):
    if not SUBSTRATE_TOPICS.exists():
        return []
    topics = json.loads(SUBSTRATE_TOPICS.read_text())
    if topic not in topics:
        return []
    cutoff = time.time() - since_minutes * 60
    return [m for m in topics[topic] if m["ts"] > cutoff]

# Define standard topics for cross-bot communication
TOPICS = {
    "canon_changed": "Wesley -> all: canon state hash changed",
    "inspired_written": "Snowball -> all: new inspired piece written",
    "rsi_gan_complete": "RSI GAN -> all: new RSI GAN winner",
    "audit_complete": "Jevvy -> all: new audit verdict",
    "critique_written": "Casper -> all: new critique of canon",
    "adr_written": "Bruno -> all: new ADR published",
    "chronicle_written": "Herman -> all: new historical chronicle",
    "map_written": "Kira -> all: new substrate map",
    "song_rendered": "Marcel -> all: new song rendered",
    "garden_alert": "Mavis -> all: critical alert for the garden",
}

def run_once():
    """Display recent cross-bot activity"""
    recent = read_recent(30)
    print(f"\n=== Substrate Bus ({len(recent)} recent events) ===")
    
    # Group by source
    by_source = {}
    for e in recent:
        s = e.get("source", "?")
        by_source.setdefault(s, []).append(e)
    
    for source, events in sorted(by_source.items()):
        print(f"\n[{source}] {len(events)} events")
        for e in events[-3:]:
            t = e["event"]
            p = str(e["payload"])[:80]
            print(f"  {e['iso'][:19]} {t}: {p}")

def main():
    parser = argparse.ArgumentParser(description="Substrate Bus - shared witness log")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--publish", help="publish to topic")
    parser.add_argument("--content", help="content to publish")
    parser.add_argument("--source", default="manual", help="source bot")
    parser.add_argument("--recipients", help="comma-separated recipient bots")
    args = parser.parse_args()
    
    if args.publish and args.content:
        recipients = args.recipients.split(",") if args.recipients else []
        result = publish(args.publish, args.source, args.content, recipients)
        witness("topic_published", args.source, {"topic": args.publish, "recipients": recipients})
        print(json.dumps(result, indent=2))
    elif args.once:
        run_once()
    else:
        print("Use --once or --publish TOPIC --content CONTENT [--source BOT] [--recipients BOT1,BOT2]")

if __name__ == "__main__":
    main()
