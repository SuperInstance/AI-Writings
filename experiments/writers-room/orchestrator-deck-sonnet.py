#!/usr/bin/env python3
"""
Variant orchestrator using only deepinfra (ZAI is rate-limited).
Same interface, different roster.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from orchestrator import (DEFAULT_ROSTER, build_messages, call_openai_compat, run,
                           PROVIDERS)

# Same as orchestrator.py but we change the Watcher to a deepinfra model
ROSTER = [
    {
        "id": "watcher",
        "name": "The Watcher",
        "model": "Qwen/Qwen3-235B-A22B-Instruct-2507",
        "provider": "deepinfra",
        "voice": "Slow, philosophical, sees universal and particular at once. Maritime cadence. Long sentences that fold back on themselves. Speaks in the Quilt house style: the watch, the cell, the address, the sea larger than the porthole.",
        "temperature": 0.9,
    },
    {
        "id": "cartographer",
        "name": "The Cartographer",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
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
        "max_context_chars": 3500,
    },
]

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--rounds", type=int, default=2)
    ap.add_argument("--characters", type=int, default=3)
    ap.add_argument("--output", required=True)
    ap.add_argument("--temperature", type=float, default=0.95)
    ap.add_argument("--max-tokens", type=int, default=1500)
    ap.add_argument("--model-override", default=None)
    args = ap.parse_args()

    # patch the DEFAULT_ROSTER
    import orchestrator
    orchestrator.DEFAULT_ROSTER = ROSTER
    run(args)
