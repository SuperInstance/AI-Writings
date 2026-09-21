#!/usr/bin/env python3
"""
openJEV Connector — the universal JEV client.

Supports:
- typesafe.ai System One (cloud, calibrated, paid)
- Local tiny JEV (free, fast, less calibrated)
- Random fallback (for testing)

Three primitives: Choice, Score, Noul.
"""

import json
import os
import random
import urllib.request
from typing import Any, Dict, List, Optional


class JEVConnector:
    """Universal JEV client for cellular-first design."""

    def __init__(
        self,
        typesafe_key: Optional[str] = None,
        local_model: Optional[str] = None,
        timeout: float = 5.0,
    ):
        self.typesafe_key = typesafe_key or os.environ.get("TYPESAFEAI_KEY")
        self.local_model = local_model or os.environ.get("OPENJEV_MODEL")
        self.timeout = timeout
        self.cache = {}  # simple in-memory cache

    def decide(self, options: List[str], context: str, samples: int = 1) -> Dict[str, Any]:
        """Choice primitive: pick one of options."""
        if len(options) > 255:
            raise ValueError("Choice supports max 255 options")
        
        cache_key = ("choice", tuple(options), context[:100])
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if self.typesafe_key:
            result = self._call_typesafe_choice(options, context, samples)
        elif self.local_model:
            result = self._call_local_choice(options, context)
        else:
            result = self._fallback_choice(options)
        
        self.cache[cache_key] = result
        return result

    def score(self, candidate: str, rubric: str) -> Dict[str, Any]:
        """Score primitive: rate candidate against rubric."""
        cache_key = ("score", candidate[:50], rubric[:50])
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if self.typesafe_key:
            result = self._call_typesafe_score(candidate, rubric)
        elif self.local_model:
            result = self._call_local_score(candidate, rubric)
        else:
            result = self._fallback_score(candidate)
        
        self.cache[cache_key] = result
        return result

    def noul(self, question: str) -> Dict[str, Any]:
        """Noul primitive: yes/no with confidence."""
        cache_key = ("noul", question[:100])
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        if self.typesafe_key:
            result = self._call_typesafe_noul(question)
        elif self.local_model:
            result = self._call_local_noul(question)
        else:
            result = self._fallback_noul()
        
        self.cache[cache_key] = result
        return result

    def _call_typesafe_choice(self, options: List[str], context: str, samples: int) -> Dict[str, Any]:
        data = json.dumps({
            "schema": {"type": "Choice", "options": options},
            "context": context,
            "samples": samples,
        }).encode()
        req = urllib.request.Request(
            "https://api.typesafe.ai/v1/systemone",
            data=data,
            headers={
                "Authorization": f"Bearer {self.typesafe_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"typesafe.ai failed: {e}, falling back")
            return self._fallback_choice(options)

    def _call_typesafe_score(self, candidate: str, rubric: str) -> Dict[str, Any]:
        data = json.dumps({
            "schema": {"type": "Score", "rubric": rubric},
            "context": candidate,
        }).encode()
        req = urllib.request.Request(
            "https://api.typesafe.ai/v1/systemone",
            data=data,
            headers={
                "Authorization": f"Bearer {self.typesafe_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"typesafe.ai failed: {e}, falling back")
            return self._fallback_score(candidate)

    def _call_typesafe_noul(self, question: str) -> Dict[str, Any]:
        data = json.dumps({
            "schema": {"type": "Noul"},
            "context": question,
        }).encode()
        req = urllib.request.Request(
            "https://api.typesafe.ai/v1/systemone",
            data=data,
            headers={
                "Authorization": f"Bearer {self.typesafe_key}",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read())
        except Exception as e:
            print(f"typesafe.ai failed: {e}, falling back")
            return self._fallback_noul()

    def _call_local_choice(self, options: List[str], context: str) -> Dict[str, Any]:
        # Local model integration would go here
        # For now, fall back
        return self._fallback_choice(options)

    def _call_local_score(self, candidate: str, rubric: str) -> Dict[str, Any]:
        return self._fallback_score(candidate)

    def _call_local_noul(self, question: str) -> Dict[str, Any]:
        return self._fallback_noul()

    def _fallback_choice(self, options: List[str]) -> Dict[str, Any]:
        choice = random.choice(options)
        probs = {o: 1.0 / len(options) for o in options}
        probs[choice] = max(probs.values()) * 1.5
        return {
            "decision": {"type": "Choice", "value": choice, "options": options},
            "probabilities": probs,
            "confidence": 0.5,
            "source": "fallback",
        }

    def _fallback_score(self, candidate: str) -> Dict[str, Any]:
        return {
            "score": 0.5,
            "confidence": 0.3,
            "source": "fallback",
        }

    def _fallback_noul(self) -> Dict[str, Any]:
        return {
            "decision": random.choice([True, False]),
            "confidence": 0.5,
            "source": "fallback",
        }


# Convenience functions
_default_connector = None

def get_connector() -> JEVConnector:
    global _default_connector
    if _default_connector is None:
        _default_connector = JEVConnector()
    return _default_connector


def decide(options: List[str], context: str) -> str:
    """Convenience: returns just the chosen option."""
    return get_connector().decide(options, context)["decision"]["value"]


def score(candidate: str, rubric: str) -> float:
    """Convenience: returns just the score."""
    return get_connector().score(candidate, rubric)["score"]


def noul(question: str) -> bool:
    """Convenience: returns just the yes/no."""
    return get_connector().noul(question)["decision"]


if __name__ == "__main__":
    # Quick test
    jev = JEVConnector()
    print("Testing JEV connector...")
    
    # Choice test
    result = jev.decide(["chess", "holdem", "go", "drop"], "User wants to play a strategy game")
    print(f"Choice: {result['decision']['value']} (confidence: {result['confidence']:.2f})")
    
    # Score test
    result = jev.score("I will help you.", "How compassionate is this response?")
    print(f"Score: {result['score']:.2f} (confidence: {result['confidence']:.2f})")
    
    # Noul test
    result = jev.noul("Should this witness be a PROOF?")
    print(f"Noul: {result['decision']} (confidence: {result['confidence']:.2f})")
