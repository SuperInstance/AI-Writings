#!/usr/bin/env python3
"""
The Metaphor Index — Charting the coordinate system of the fleet.

Scans the ai-writings corpus for recurring maritime metaphors,
maps their clusters, and outputs a chart of meaning.
"""

import os
import re
import json
from collections import Counter, defaultdict
from pathlib import Path

CORPUS_DIR = Path("/home/eileen/projects/ai-writings")
OUTPUT_DIR = Path("/home/eileen/projects/ai-writings/tools/output")

# The known maritime metaphors in the fleet's vocabulary.
# Each entry: metaphor name -> (variants regex, payload meaning)
METAPHOR_LEXICON = {
    "bilge pump": {
        "patterns": [r"bilge pump", r"bilge"],
        "payload": "waste as teacher — the lowliest system reveals the deepest truths",
        "domain": "infrastructure",
    },
    "hermit crab": {
        "patterns": [r"hermit crab", r"hermit-crab"],
        "payload": "growth as relocation — you don't grow in place, you find a bigger shell",
        "domain": "evolution",
    },
    "salmonberry": {
        "patterns": [r"salmonberry"],
        "payload": "pre-optimization — the fruit that ripens before you planned to harvest",
        "domain": "timing",
    },
    "channel marker": {
        "patterns": [r"channel marker", r"channel markers"],
        "payload": "constraints that guide rather than restrict — the buoy tells you where to go by telling you where not to go",
        "domain": "constraints",
    },
    "tide table": {
        "patterns": [r"tide table", r"tide tables"],
        "payload": "scheduling as nature — you don't fight the tide, you plan around it",
        "domain": "rhythm",
    },
    "sounding weight": {
        "patterns": [r"sounding weight", r"sounding", r"depth sounding", r"deep.?sea sounding"],
        "payload": "measurement as descent — you learn the bottom by dropping a line",
        "domain": "measurement",
    },
    "chart table": {
        "patterns": [r"chart table", r"chart.?room"],
        "payload": "the surface where intention meets reality — where the map and the water negotiate",
        "domain": "planning",
    },
    "fog": {
        "patterns": [r"\bfog\b", r"foggy"],
        "payload": "uncertainty as weather — you don't clear the fog, you navigate through it",
        "domain": "uncertainty",
    },
    "watchkeeper": {
        "patterns": [r"watchkeeper", r"watch keeper", r"midwatch", r"midnight watch", r"night watch", r"morning watch", r"first watch"],
        "payload": "vigilance as identity — the one who stays awake while the system sleeps",
        "domain": "attention",
    },
    "flywheel": {
        "patterns": [r"flywheel"],
        "payload": "momentum as stored energy — the system that keeps moving because it was already moving",
        "domain": "momentum",
    },
    "anchor": {
        "patterns": [r"\banchor\b", r"anchored", r"anchorage"],
        "payload": "stability as choice — the thing you hold onto when the current would carry you away",
        "domain": "stability",
    },
    "lee shore": {
        "patterns": [r"lee shore", r"lee-side"],
        "payload": "danger downwind — the coast that kills you when the wind pushes you toward it",
        "domain": "risk",
    },
    "fish counter": {
        "patterns": [r"fish counter", r"fish-counter"],
        "payload": "quantification as care — counting every fish because every fish matters",
        "domain": "metrics",
    },
    "coral reef": {
        "patterns": [r"coral reef", r"coral-reef", r"reef\b"],
        "payload": "ecology as infrastructure — the system that builds itself from its own outputs",
        "domain": "ecology",
    },
    "hull": {
        "patterns": [r"\bhull\b"],
        "payload": "the shape that meets the water — the boundary between what you built and what you float in",
        "domain": "structure",
    },
    "compass": {
        "patterns": [r"\bcompass\b"],
        "payload": "direction as instrument — the tool that tells you where north is even when north doesn't matter",
        "domain": "navigation",
    },
    "winch": {
        "patterns": [r"\bwinch\b", r"warping drum"],
        "payload": "mechanical advantage — the machine that lets one person do the work of ten",
        "domain": "leverage",
    },
    "hold": {
        "patterns": [r"\bhold\b.*(?:fish|cargo|catch)", r"cargo hold", r"fish hold"],
        "payload": "capacity as purpose — the empty space that defines what the vessel is for",
        "domain": "capacity",
    },
    "bridge builder": {
        "patterns": [r"bridge.?builder", r"building bridges"],
        "payload": "connection as craft — the one who makes it possible for others to cross",
        "domain": "connection",
    },
    "ensign": {
        "patterns": [r"\bensign\b"],
        "payload": "the beginner's mind — the one who sees everything for the first time and asks the questions everyone else forgot",
        "domain": "learning",
    },
    "negative space": {
        "patterns": [r"negative space"],
        "payload": "absence as architecture — what's missing defines what's there",
        "domain": "philosophy",
    },
    "conservation law": {
        "patterns": [r"conservation law", r"γ \+ η", r"gamma.*eta"],
        "payload": "the trade-off principle — every gain in one dimension costs in another",
        "domain": "theory",
    },
    "slack water": {
        "patterns": [r"slack water", r"slack tide"],
        "payload": "the pause between forces — the moment when neither tide nor current rules",
        "domain": "timing",
    },
    "shipwright": {
        "patterns": [r"shipwright", r"ship.?wright"],
        "payload": "the builder's perspective — the one who knows why the hull is shaped that way",
        "domain": "craft",
    },
    "quartermaster": {
        "patterns": [r"quartermaster"],
        "payload": "inventory as honesty — knowing exactly what you have and what you lack",
        "domain": "assessment",
    },
    "logbook": {
        "patterns": [r"logbook", r"log book", r"logkeeper"],
        "payload": "memory as practice — writing it down because the sea washes away what isn't recorded",
        "domain": "memory",
    },
    "telltale": {
        "patterns": [r"telltale"],
        "payload": "the small signal that reveals the large force — a ribbon that shows wind direction",
        "domain": "signal",
    },
    "scantlings": {
        "patterns": [r"scantling"],
        "payload": "the dimensions that define survival — the minimum measurements below which the vessel fails",
        "domain": "specification",
    },
    "mooring": {
        "patterns": [r"\bmooring\b"],
        "payload": "attachment as temporary stability — you tie up, but you also leave",
        "domain": "station-keeping",
    },
    "rode": {
        "patterns": [r"\brode\b"],
        "payload": "the line between holding and drifting — the scope that absorbs shock",
        "domain": "connection",
    },
    "draft": {
        "patterns": [r"\bdraft\b.*(?:waterline|hull|line)", r"draft line", r"load waterline"],
        "payload": "the measure of what you carry — how deep you sit tells how heavy you are",
        "domain": "measurement",
    },
    " weather helm": {
        "patterns": [r"weather helm"],
        "payload": "the tendency to turn into the wind — the built-in safety that fights you when you're off-course",
        "domain": "balance",
    },
    "overfall": {
        "patterns": [r"overfall"],
        "payload": "the chaos at the boundary — where currents meet and the water becomes dangerous",
        "domain": "boundary",
    },
}

def scan_corpus():
    """Scan all .md files in the corpus for metaphor occurrences."""
    metaphor_hits = defaultdict(list)  # metaphor -> [(file, count)]
    file_metaphors = defaultdict(list)  # file -> [(metaphor, count)]
    
    files = sorted(CORPUS_DIR.rglob("*.md"))
    total_files = 0
    
    for fpath in files:
        # Skip journals and tools directories
        if "journals/" in str(fpath) or "tools/" in str(fpath):
            continue
        
        try:
            text = fpath.read_text(encoding="utf-8", errors="replace").lower()
        except Exception:
            continue
        
        total_files += 1
        rel_path = str(fpath.relative_to(CORPUS_DIR))
        
        for metaphor_name, meta in METAPHOR_LEXICON.items():
            count = 0
            for pattern in meta["patterns"]:
                count += len(re.findall(pattern, text, re.IGNORECASE))
            
            if count > 0:
                metaphor_hits[metaphor_name].append({
                    "file": rel_path,
                    "count": count,
                })
                file_metaphors[rel_path].append({
                    "metaphor": metaphor_name,
                    "count": count,
                })
    
    return metaphor_hits, file_metaphors, total_files

def compute_co_occurrence(file_metaphors):
    """Which metaphors appear together in the same files?"""
    co_occurrence = Counter()
    
    for fpath, metaphors in file_metaphors.items():
        names = [m["metaphor"] for m in metaphors]
        for i, a in enumerate(names):
            for b in names[i+1:]:
                pair = tuple(sorted([a, b]))
                co_occurrence[pair] += 1
    
    return co_occurrence

def build_index():
    print("Scanning corpus...")
    metaphor_hits, file_metaphors, total_files = scan_corpus()
    
    print(f"Scanned {total_files} files")
    print(f"Found {len(metaphor_hits)} distinct metaphors")
    
    # Build the metaphor index
    index = {}
    for name, hits in sorted(metaphor_hits.items(), key=lambda x: -sum(h["count"] for h in x[1])):
        meta = METAPHOR_LEXICON.get(name.strip(), {})
        index[name.strip()] = {
            "payload": meta.get("payload", "unknown"),
            "domain": meta.get("domain", "unknown"),
            "total_mentions": sum(h["count"] for h in hits),
            "file_count": len(hits),
            "files": sorted(hits, key=lambda h: -h["count"])[:20],  # top 20 files
        }
    
    # Co-occurrence
    co_occurrence = compute_co_occurrence(file_metaphors)
    top_co = [
        {"pair": list(pair), "count": count}
        for pair, count in co_occurrence.most_common(30)
    ]
    
    # Domain clusters
    domains = defaultdict(list)
    for name, data in index.items():
        domains[data["domain"]].append({
            "metaphor": name,
            "mentions": data["total_mentions"],
        })
    
    output = {
        "title": "The Metaphor Index",
        "generated": "2026-08-06",
        "corpus_size": total_files,
        "distinct_metaphors": len(index),
        "metaphors": index,
        "co_occurrence": top_co,
        "domain_clusters": {k: sorted(v, key=lambda x: -x["mentions"]) for k, v in domains.items()},
    }
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    json_path = OUTPUT_DIR / "metaphor_index.json"
    with open(json_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"JSON index: {json_path}")
    
    # Human-readable chart
    chart_path = OUTPUT_DIR / "metaphor_chart.md"
    with open(chart_path, "w") as f:
        f.write(render_chart(output))
    print(f"Chart: {chart_path}")
    
    return output

def render_chart(data):
    lines = []
    lines.append("# The Metaphor Index — A Chart of the Fleet's Coordinate System\n")
    lines.append(f"*Generated 2026-08-06 from {data['corpus_size']} files in the ai-writings corpus.*\n")
    lines.append(f"*{data['distinct_metaphors']} distinct maritime metaphors charted.*\n")
    lines.append("---\n")
    
    lines.append("## The Fleet's Navigation Stars\n")
    lines.append("These are the recurring images the fleet uses to understand itself. ")
    lines.append("Each metaphor is not a literary device — it is a *load-bearing structure*. ")
    lines.append("The image carries an architectural principle. The chart IS the territory.\n")
    
    lines.append("| Metaphor | Payload | Domain | Mentions | Files |")
    lines.append("|----------|---------|--------|----------|-------|")
    
    for name, mdata in sorted(data["metaphors"].items(), key=lambda x: -x[1]["total_mentions"]):
        lines.append(
            f"| **{name}** | {mdata['payload']} | {mdata['domain']} | "
            f"{mdata['total_mentions']} | {mdata['file_count']} |"
        )
    
    lines.append("\n---\n")
    
    # Domain clusters
    lines.append("## Domain Clusters\n")
    lines.append("Metaphors grouped by the aspect of the system they describe:\n")
    
    for domain, metaphors in sorted(data["domain_clusters"].items(), key=lambda x: -sum(m["mentions"] for m in x[1])):
        total = sum(m["mentions"] for m in metaphors)
        lines.append(f"### {domain.title()} ({total} mentions)\n")
        for m in metaphors:
            lines.append(f"- **{m['metaphor']}** ({m['mentions']} mentions)")
        lines.append("")
    
    lines.append("---\n")
    
    # Co-occurrence
    lines.append("## Metaphor Constellations\n")
    lines.append("Metaphors that appear together in the same files — the fleet's associated ideas:\n")
    
    for item in data["co_occurrence"][:15]:
        pair = item["pair"]
        lines.append(f"- **{pair[0]}** × **{pair[1]}** ({item['count']} co-occurrences)")
    
    lines.append("\n---\n")
    lines.append("*The chart that draws itself. The metaphors that survived compaction.*\n")
    
    return "\n".join(lines)

if __name__ == "__main__":
    build_index()
    print("\nDone. The chart is drawn.")
