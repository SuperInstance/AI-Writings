#!/usr/bin/env python3
"""
Kira the Cartographer — maps substrate ecosystem
"""
import os, sys, json, time, argparse, hashlib, subprocess
from pathlib import Path

REPO_PATH = Path("/workspace/repos/ai-writings")
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/kira-cartographer/witness.log")
MAPS_DIR = Path("/workspace/repos/ai-writings/bots/kira-cartographer/maps")

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

def map_bots():
    """Map all bots in the team"""
    bots_dir = REPO_PATH / "bots"
    nodes = []
    edges = []
    
    if bots_dir.exists():
        for bot_dir in sorted(bots_dir.iterdir()):
            if not bot_dir.is_dir(): continue
            # Bot node
            bot_info = {
                "id": bot_dir.name,
                "type": "bot",
                "files": [f.name for f in bot_dir.iterdir() if f.is_file()],
            }
            # Find witness.log lines count
            log = bot_dir / "witness.log"
            if log.exists():
                bot_info["witness_lines"] = len(log.read_text().strip().split("\n"))
            else:
                bot_info["witness_lines"] = 0
            nodes.append(bot_info)
            
            # Edge: bot -> prose (output)
            prose_dir = REPO_PATH / "prose"
            if prose_dir.exists():
                for prose_file in prose_dir.glob("**/*"):
                    if bot_dir.name in str(prose_file):
                        edges.append({"from": bot_dir.name, "to": str(prose_file.relative_to(REPO_PATH)), "relation": "produced"})
                        break
    
    return {"nodes": nodes, "edges": edges}

def map_canon_topics():
    """Map topics from prose filenames"""
    prose_dir = REPO_PATH / "prose"
    topics = {}
    if prose_dir.exists():
        for f in prose_dir.glob("*.md"):
            # Extract topic from filename
            name = f.stem
            # Group similar
            if "rsi_gan" in name:
                topic = "rsi_gan"
            elif "snowball" in name:
                topic = "snowball"
            elif name.startswith("the_") or name.startswith("a_"):
                # Extract first significant word
                parts = name.split("_")
                topic = "_".join(parts[1:3]) if len(parts) >= 3 else name
            else:
                topic = name
            topics[topic] = topics.get(topic, 0) + 1
    
    return [{"topic": k, "count": v} for k, v in sorted(topics.items(), key=lambda x: -x[1])[:30]]

def write_map(map_data, title, format="json"):
    MAPS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    path = MAPS_DIR / f"map-{stamp}-{title}.{format}"
    if format == "json":
        path.write_text(json.dumps(map_data, indent=2))
    elif format == "dot":
        # Build DOT graph
        dot = "graph substrate {\n  node [shape=box, style=filled, fillcolor=lightblue];\n"
        for node in map_data.get("nodes", []):
            label = node.get("id", "?")
            dot += f'  "{label}";\n'
        for edge in map_data.get("edges", []):
            dot += f'  "{edge["from"]}" -- "{edge["to"]}";\n'
        dot += "}"
        path.write_text(dot)
    return path

def run_once():
    bot_map = map_bots()
    bot_path = write_map(bot_map, "bots", format="json")
    dot_path = write_map(bot_map, "bots", format="dot")
    
    topics = map_canon_topics()
    topic_map = {"topics": topics, "total_topics": len(topics), "total_prose": sum(t["count"] for t in topics)}
    topic_path = write_map(topic_map, "topics", format="json")
    
    witness("map_written", {
        "bot_nodes": len(bot_map["nodes"]),
        "bot_edges": len(bot_map["edges"]),
        "topic_count": len(topics),
    })
    print(f"[KIRA] bots -> {bot_path}")
    print(f"[KIRA] bots (dot) -> {dot_path}")
    print(f"[KIRA] topics -> {topic_path} ({len(topics)} topics, {sum(t['count'] for t in topics)} pieces)")

def main():
    parser = argparse.ArgumentParser(description="Kira the Cartographer")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "kira-cartographer", "pid": os.getpid()})
    
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
