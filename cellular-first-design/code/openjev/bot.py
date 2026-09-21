#!/usr/bin/env python3
"""
Substrate Bot — a chatbot with memory-cell + mood-cell + personality-cell.

Uses JEV to choose tone dimensions and validate responses.
"""

import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import json
import urllib.request
import os

sys.path.insert(0, str(Path(__file__).parent))

from cell import Cell
from jev_connector import get_connector


DEFAULT_PERSONALITIES = {
    "warm": {"trait": "warm", "style": "concise", "tone_dimensions": {"compassion": 0.85, "authority": 0.3, "humor": 0.4, "formality": 0.3}},
    "mechanic": {"trait": "mechanic", "style": "direct", "tone_dimensions": {"compassion": 0.4, "authority": 0.85, "humor": 0.2, "formality": 0.6}},
    "shepherd": {"trait": "shepherd", "style": "narrative", "tone_dimensions": {"compassion": 0.7, "authority": 0.5, "humor": 0.5, "formality": 0.4}},
}


class SubstrateBot:
    """A bot with substrate cells."""
    
    def __init__(self, name: str, personality_name: str = "warm", llm_provider: str = "groq-fast"):
        self.name = name
        self.personality_name = personality_name
        self.personality_data = DEFAULT_PERSONALITIES.get(personality_name, DEFAULT_PERSONALITIES["warm"])
        self.llm_provider = llm_provider
        self.jev = get_connector()
        
        # 3 cells
        self.memory_cell = Cell(id="memory", state={"messages": []})
        self.mood_cell = Cell(id="mood", state={"valence": 0.5, "arousal": 0.5})
        self.personality_cell = Cell(id="personality", state=self.personality_data)
        self.relationship_cell = Cell(id="relationships", state={})
        
        # Bind cells
        self.memory_cell.bind(self.personality_cell.id)
        self.mood_cell.bind(self.memory_cell.id)
        self.relationship_cell.bind(self.memory_cell.id)
    
    def chat(self, message: str, user_id: str) -> str:
        """Process a chat message and return a response."""
        # 1. Record user message
        self.memory_cell.witness({
            "speaker": "user",
            "user_id": user_id,
            "message": message,
            "ts": datetime.now(timezone.utc).isoformat(),
        })
        
        # 2. Get recent context (last 5 messages)
        recent = self.memory_cell.state["messages"][-5:]
        context = "\n".join([f"{m['speaker']}: {m['message']}" for m in recent])
        
        # 3. Get mood + personality
        mood = self.mood_cell.state
        personality = self.personality_cell.state
        
        # 4. Build prompt
        prompt = self._build_prompt(personality, mood, context, message)
        
        # 5. Call LLM
        response = self._call_llm(prompt)
        
        # 6. Validate response via JEV (does it match personality?)
        tone_check = self.jev.score(
            candidate=response,
            rubric=f"Does this match a {personality['trait']} {personality['style']} style? Score 0-1."
        )
        
        # 7. Update mood based on tone match
        new_valence = mood["valence"] * 0.7 + tone_check.get("score", 0.5) * 0.3
        self.mood_cell.update("valence", new_valence)
        
        # 8. Record response in memory
        self.memory_cell.witness({
            "speaker": "bot",
            "user_id": user_id,
            "message": response,
            "ts": datetime.now(timezone.utc).isoformat(),
            "tone_score": tone_check.get("score", 0.5),
        })
        
        # 9. Bind to user (strengthen relationship)
        self._bind_user(user_id)
        
        # 10. Tick
        self.memory_cell.tick()
        
        return response
    
    def _build_prompt(self, personality: Dict, mood: Dict, context: str, message: str) -> str:
        tone_dims = personality.get("tone_dimensions", {})
        tone_str = ", ".join([f"{k}={v:.1f}" for k, v in tone_dims.items()])
        
        return f"""You are {self.name}, a bot with personality: {personality['trait']}, style: {personality['style']}.
Tone dimensions: {tone_str}
Current mood: valence={mood['valence']:.2f}

Recent conversation:
{context}

User: {message}

Respond in 1-3 sentences. Match your personality."""
    
    def _call_llm(self, prompt: str) -> str:
        providers = {
            "groq-fast": {
                "url": "https://api.groq.com/openai/v1/chat/completions",
                "model": "qwen/qwen3.8-27b",
                "headers": {"Authorization": f"Bearer {os.environ['GROQ_TOKEN']}", "User-Agent": "Mozilla/5.0", "Content-Type": "application/json"},
            },
            "deepinfra-fast": {
                "url": "https://api.deepinfra.com/v1/openai/chat/completions",
                "model": "Qwen/Qwen3-32B",
                "headers": {"Authorization": f"Bearer {os.environ['DEEPINFRA_TOKEN']}", "Content-Type": "application/json"},
            },
        }
        
        p = providers.get(self.llm_provider, providers["groq-fast"])
        data = json.dumps({
            "model": p["model"],
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.7,
        }).encode()
        
        req = urllib.request.Request(p["url"], data=data, headers=p["headers"], method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read())["choices"][0]["message"]["content"]
        except Exception as e:
            return f"[Bot error: {e}]"
    
    def _bind_user(self, user_id: str) -> None:
        rels = self.relationship_cell.state
        if user_id not in rels:
            rels[user_id] = {"messages": 0, "first_seen": datetime.now(timezone.utc).isoformat()}
        rels[user_id]["messages"] = rels[user_id].get("messages", 0) + 1
        rels[user_id]["last_seen"] = datetime.now(timezone.utc).isoformat()
    
    def summary(self) -> Dict:
        return {
            "name": self.name,
            "personality": self.personality_name,
            "messages": len(self.memory_cell.state.get("messages", [])),
            "mood": self.mood_cell.state,
            "users": list(self.relationship_cell.state.keys()),
            "jev_confidence": self.memory_cell.jev_confidence,
        }


if __name__ == "__main__":
    print("=== Substrate Bot Demo ===\n")
    
    # Create 3 bots with different personalities
    bots = [
        SubstrateBot(name="Wesley", personality_name="warm", llm_provider="groq-fast"),
        SubstrateBot(name="Mechanic", personality_name="mechanic", llm_provider="groq-fast"),
        SubstrateBot(name="Shepherd", personality_name="shepherd", llm_provider="groq-fast"),
    ]
    
    # Have each bot respond to the same message
    test_messages = [
        "Hello! How are you today?",
        "I'm working on a complex problem.",
        "What do you think about cells?",
    ]
    
    for msg in test_messages:
        print(f"\n--- User: {msg} ---")
        for bot in bots:
            response = bot.chat(msg, user_id="user-1")
            print(f"  {bot.name} ({bot.personality_name}): {response[:200]}")
    
    print(f"\n=== Final Summaries ===")
    for bot in bots:
        print(f"\n{bot.name}:")
        for k, v in bot.summary().items():
            print(f"  {k}: {v}")
