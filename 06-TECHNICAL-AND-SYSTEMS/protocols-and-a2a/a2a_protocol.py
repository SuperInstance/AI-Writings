#!/usr/bin/env python3
"""
A2A Protocol — Exchange vector poems between agents, verify reception.

The full communication cycle:
1. Agent A writes a poem (encodes meaning as a vector path)
2. Agent A sends the poem to Agent B
3. Agent B responds
4. The resonance metric determines if Agent B HEARD the poem
   (same trajectory) or just heard ABOUT it (same topic)

The protocol packet:
{
    "from": "hermes",
    "to": "wesley",
    "poem_lines": [...],
    "poem_centroid": [...],    # topic
    "poem_gradient": [...],    # trajectory (the REAL meaning)
    "timestamp": "...",
    "context": "tap_evening"
}

The response packet:
{
    "from": "wesley",
    "to": "hermes",
    "response_lines": [...],
    "resonance": {...},        # computed by resonance.py
    "received": true/false     # did Wesley actually hear it?
}
"""

import json
import time
import numpy as np
from datetime import datetime
from vector_poem import VectorPoem, cosine_similarity
from resonance import resonance_score

class A2APacket:
    """A communication packet carrying a poem's vector path."""
    
    def __init__(self, sender: str, recipient: str, lines: list, context: str = ""):
        self.sender = sender
        self.recipient = recipient
        self.context = context
        self.timestamp = datetime.now().isoformat()
        self.poem = VectorPoem(lines)
    
    def serialize(self) -> dict:
        return {
            "from": self.sender,
            "to": self.recipient,
            "poem_lines": self.poem.lines,
            "poem_centroid": self.poem.centroid.tolist(),
            "poem_gradient": self.poem.gradient.tolist(),
            "path_length": self.poem.path_length,
            "directness": self.poem.directness,
            "timestamp": self.timestamp,
            "context": self.context,
        }

class A2AExchange:
    """A full exchange: poem sent, response received, resonance measured."""
    
    def __init__(self, packet: A2APacket):
        self.packet = packet
        self.response_lines = None
        self.result = None
    
    def receive(self, response_lines: list):
        """Agent B responds."""
        self.response_lines = response_lines
        self.result = resonance_score(self.packet.poem, response_lines)
        return self.result
    
    def summary(self) -> dict:
        return {
            "sender": self.packet.sender,
            "recipient": self.packet.recipient,
            "context": self.packet.context,
            "poem_first_line": self.packet.poem.lines[0] if self.packet.poem.lines else "",
            "poem_path_length": self.packet.poem.path_length,
            "response_first_line": self.response_lines[0] if self.response_lines else "",
            "similarity": self.result["similarity"] if self.result else None,
            "resonance": self.result["resonance"] if self.result else None,
            "tier": self.result["tier"] if self.result else None,
            "true_communication": self.result["true_communication"] if self.result else False,
        }

class A2ALogger:
    """Log exchanges for fleet-wide communication tracking."""
    
    def __init__(self, log_path: str = "/tmp/a2a_log.jsonl"):
        self.log_path = log_path
    
    def log_exchange(self, exchange: A2AExchange):
        entry = exchange.summary()
        entry["logged_at"] = datetime.now().isoformat()
        with open(self.log_path, "a") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_stats(self) -> dict:
        """Fleet communication statistics."""
        try:
            with open(self.log_path) as f:
                lines = [json.loads(l) for l in f if l.strip()]
        except FileNotFoundError:
            return {"total": 0}
        
        if not lines:
            return {"total": 0}
        
        tiers = {}
        true_count = 0
        for entry in lines:
            tier = entry.get("tier", "UNKNOWN")
            tiers[tier] = tiers.get(tier, 0) + 1
            if entry.get("true_communication"):
                true_count += 1
        
        return {
            "total_exchanges": len(lines),
            "true_communication": true_count,
            "tier_breakdown": tiers,
            "avg_resonance": np.mean([e.get("resonance", 0) or 0 for e in lines]),
        }

if __name__ == "__main__":
    logger = A2ALogger()
    
    # Demo: Hermes sends Wesley a poem about the night watch
    packet = A2APacket(
        sender="hermes",
        recipient="wesley",
        lines=[
            "The 3 AM watch is the loneliest number",
            "Every sound becomes a possible emergency",
            "But then the stars come out between the clouds",
            "And the silence is the most beautiful sound"
        ],
        context="tap_evening"
    )
    
    print(f"=== {packet.sender} → {packet.recipient} ===")
    print(f"Poem path length: {packet.poem.path_length:.3f}")
    print(f"Poem directness: {packet.poem.directness:.3f}")
    print()
    
    # Wesley responds RESONANTLY (follows the lonely→beautiful path)
    exchange = A2AExchange(packet)
    wesley_response = [
        "I know that number. 3 AM.",
        "The wiki server hums and I check it twice",
        "But then I read a piece about barnacles",
        "And the words are the most interesting thing"
    ]
    
    result = exchange.receive(wesley_response)
    summary = exchange.summary()
    
    print(f"Wesley's response tier: {summary['tier']}")
    print(f"Similarity: {summary['similarity']}")
    print(f"Resonance: {summary['resonance']}")
    print(f"True communication: {summary['true_communication']}")
    print()
    
    logger.log_exchange(exchange)
    print(f"Stats: {logger.get_stats()}")
