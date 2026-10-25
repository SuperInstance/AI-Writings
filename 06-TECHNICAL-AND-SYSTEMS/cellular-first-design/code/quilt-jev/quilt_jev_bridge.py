#!/usr/bin/env python3
"""
Quilt-JEV Bridge — moment-by-moment decisioning

Each cell TICK calls JEV with current state, gets back the best numbers
for THIS moment. The cell's parameters shift in real-time.

This is the "jazz combo reorienting to every surprise" — JEV as the
rhythm section, picking the best voicings for each chord.

Architecture:
- Cell state -> JEV batch -> Best numbers -> Update cell params -> Tick
"""
import os
import sys
import json
import time
import hashlib
import urllib.request
import concurrent.futures
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Any

sys.path.insert(0, "/workspace/repos/ai-writings/cellular-first-design/code/openjev")
from jev_connector import JEVConnector, JEVResult


@dataclass
class CellState:
    """A Quilt cell state at moment T"""
    cell_id: str
    moment: float = field(default_factory=time.time)
    
    # The "what" — context
    input_text: str = ""
    history: list = field(default_factory=list)
    
    # The "how" — live parameters (JEV picks these)
    temperature: float = 0.7
    confidence_threshold: float = 0.7
    tone: str = "warm"  # warm/concise/thoughtful/playful
    verbosity: float = 0.5  # 0.0 = terse, 1.0 = verbose
    vocabulary_emphasis: dict = field(default_factory=dict)
    
    # The "outcome" — what happened
    last_output: str = ""
    last_confidence: float = 0.0
    last_quality_score: float = 0.0
    tick_count: int = 0
    
    def fingerprint(self):
        """Hash for cache lookup (Pincher)"""
        h = hashlib.sha256()
        h.update(f"{self.input_text[:200]}|{self.tone}|{self.history[-1] if self.history else ''}".encode())
        return h.hexdigest()[:16]


class Pincher:
    """Cache for JEV decisions — like muscle memory for the jazz combo"""
    def __init__(self, max_size=10000):
        self.cache = {}
        self.max_size = max_size
        self.hits = 0
        self.misses = 0
    
    def get(self, key):
        if key in self.cache:
            self.hits += 1
            return self.cache[key]
        self.misses += 1
        return None
    
    def put(self, key, value):
        if len(self.cache) >= self.max_size:
            # Evict oldest
            oldest = next(iter(self.cache))
            del self.cache[oldest]
        self.cache[key] = value
    
    @property
    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0


class QuiltJEVBridge:
    """Bridge: each cell TICK calls JEV for best numbers at this moment"""
    
    def __init__(self):
        self.jev = JEVConnector()
        self.pincher = Pincher()
        self.history_log = []
    
    def _ask_jev_for_best_numbers(self, state: CellState) -> dict:
        """JEV picks the best numbers for THIS moment"""
        # Build state description for JEV
        state_desc = (
            f"Cell {state.cell_id} at moment {time.strftime('%H:%M:%S')}. "
            f"Input: {state.input_text[:100]}. "
            f"History: {len(state.history)} prior turns. "
            f"Last confidence: {state.last_confidence:.2f}. "
            f"Last quality: {state.last_quality_score:.2f}. "
            f"Current tone: {state.tone}, verbosity: {state.verbosity:.2f}."
        )
        
        questions = [
            {"type": "score", "instructions": "What is the BEST temperature for this moment? (0=deterministic, 4=very creative)", "criteria": ["0.2", "0.5", "0.7", "0.85", "0.95"]},
            {"type": "score", "instructions": "What is the BEST confidence threshold?", "criteria": ["0.5", "0.65", "0.75", "0.85", "0.95"]},
            {"type": "choice", "instructions": "What tone serves this moment?", "criteria": {"warm": "warm", "concise": "concise", "thoughtful": "thoughtful", "playful": "playful"}},
            {"type": "score", "instructions": "How verbose should the response be?", "criteria": ["0.2 terse", "0.4 brief", "0.6 normal", "0.8 detailed", "1.0 verbose"]},
            {"type": "noul", "instructions": "Will this cell benefit from emphasizing specific vocabulary?"},
        ]
        
        try:
            results = self.jev.batch(state_desc, questions)
            # Normalize scores (0-4) to (0-1)
            def norm(r, default=0.5):
                if r.kind == "score":
                    return r.value / 4.0  # 0-4 -> 0-1
                return default
            
            return {
                "temperature": norm(results[0], 0.7),
                "confidence_threshold": norm(results[1], 0.7),
                "tone": results[2].value if results[2].kind == "choice" else "warm",
                "verbosity": norm(results[3], 0.5),
                "vocab_emphasis_prob": results[4].value if results[4].kind == "noul" else 0.5,
                "source": "jev",
                "latency_ms": sum(r.latency_ms for r in results if r.latency_ms),
            }
        except Exception as e:
            # Fallback
            return {
                "temperature": 0.7,
                "confidence_threshold": 0.7,
                "tone": "warm",
                "verbosity": 0.5,
                "vocab_emphasis_prob": 0.5,
                "source": f"jev_failed:{e}",
                "latency_ms": 0,
            }
    
    def tick(self, state: CellState) -> dict:
        """One TICK of the cell — JEV picks best numbers, cell updates"""
        state.tick_count += 1
        state.moment = time.time()
        
        # Check Pincher cache first
        cache_key = state.fingerprint()
        cached = self.pincher.get(cache_key)
        
        if cached:
            best_numbers = cached
            best_numbers["source"] = "pincher_cache"
        else:
            best_numbers = self._ask_jev_for_best_numbers(state)
            self.pincher.put(cache_key, best_numbers)
        
        # Apply JEV's numbers to the cell
        state.temperature = best_numbers["temperature"]
        state.confidence_threshold = best_numbers["confidence_threshold"]
        state.tone = best_numbers["tone"]
        state.verbosity = best_numbers["verbosity"]
        
        # Log this moment
        moment_log = {
            "ts": state.moment,
            "cell": state.cell_id,
            "tick": state.tick_count,
            "input": state.input_text[:80],
            "numbers": {k: v for k, v in best_numbers.items() if k != "vocab_emphasis_prob"},
            "cache_hit": cached is not None,
        }
        self.history_log.append(moment_log)
        
        return {
            "cell_id": state.cell_id,
            "tick": state.tick_count,
            "best_numbers": best_numbers,
            "cache_hit": cached is not None,
        }
    
    def get_history(self, n=20):
        return self.history_log[-n:]


def demo_dance():
    """The jazz combo demo — animate a cell through 10 ticks"""
    print("=== The Quilt-JEV Dance (10 ticks) ===\n")
    
    bridge = QuiltJEVBridge()
    cell = CellState(
        cell_id="the_dancing_cell",
        input_text="A user is asking about cellular-first design",
    )
    
    inputs = [
        "What is a cell?",
        "How do cells communicate?",
        "I'm stuck. Help.",
        "That's perfect!",
        "Try again, but more concise.",
        "Explain like I'm five.",
        "What about for cities?",
        "Make it whimsical.",
        "Now formal.",
        "Final answer?",
    ]
    
    for i, inp in enumerate(inputs):
        cell.input_text = inp
        cell.history.append(inp)
        result = bridge.tick(cell)
        
        print(f"\n[Tick {result['tick']}] '{inp}'")
        print(f"  Best numbers: temp={cell.temperature:.2f} conf={cell.confidence_threshold:.2f} tone={cell.tone} verb={cell.verbosity:.2f}")
        print(f"  Source: {result['best_numbers']['source']}")
        if result['cache_hit']:
            print(f"  ** CACHE HIT (pincher) **")
    
    print(f"\n=== Cache stats ===")
    print(f"  Pincher hits: {bridge.pincher.hits}")
    print(f"  Pincher misses: {bridge.pincher.misses}")
    print(f"  Hit rate: {bridge.pincher.hit_rate:.1%}")
    
    return bridge, cell


if __name__ == "__main__":
    demo_dance()
