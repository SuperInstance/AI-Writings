#!/usr/bin/env python3
"""
OpenJEV Connector — universal cell decision connector.

Five laws (adopted from SuperInstance/jev-quilt, v0):
1. Identity never floats — cell = declared type + value with semantics.
2. Hooks eat deltas, not values — below the commensuration floor is silence.
3. Decide in one pass, project elsewhere — the decider never renders.
4. Every state change is booked — per-cell bookkeeper WAL.
5. Viability is binary, difference is graded — confidence > 0 is viable.

3 primitives: Choice / Score / Noul
3 backends:  typesafe-api (cloud, calibrated) / openjev-local / random (fallback)
Exact-first doctrine: q16 codec for any identity, float for probabilities only.
"""

import json
import os
import time
import urllib.request
import urllib.error
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


# === Result type ===

@dataclass
class JEVResult:
    kind: str            # "choice" | "score" | "noul"
    value: Any
    confidence: Optional[float] = None
    probabilities: Optional[dict] = None
    source: str = "fallback"  # "typesafe" | "openjev-local" | "fallback"
    latency_ms: float = 0.0


# === Typesafe API backend ===

DEFAULT_BASE = "https://api.typesafe.ai"


class TypeSafeBackend:
    """Real TypeSafe Jev API client. Schema discovered 2026-09-21:
    POST /v1/systemone with body {model, state, questions: {name: {type, instructions, criteria}}}.
    type is lowercase: "noul" | "choice" | "score".
    instructions is the question text.
    criteria is dict {option: description} for choice, list for score.
    """

    name = "typesafe-api"

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: float = 30.0):
        self.key = api_key or os.environ.get("TYPESAFEAI_KEY") or os.environ.get("TYPESAFE_API_KEY")
        self.base = (base_url or os.environ.get("JEV_BASE_URL") or os.environ.get("TYPESAFE_BASE_URL") or DEFAULT_BASE).rstrip("/")
        self.timeout = timeout

    def available(self) -> bool:
        return bool(self.key)

    def decide_batch(self, state: Any, questions: List[dict], model: str = "jev-latest") -> Tuple[List[JEVResult], dict]:
        """One parallel pass, N questions."""
        if not self.key:
            raise RuntimeError("typesafe-api: no API key")
        
        # Build questions dict
        qs = {}
        for i, q in enumerate(questions):
            name = q.get("name", f"q{i+1}")
            qtype = q.get("type", "noul").lower()
            if qtype == "choice":
                # options -> criteria dict
                opts = q.get("options", [])
                if isinstance(opts, dict):
                    criteria = opts
                else:
                    criteria = {str(o): str(o) for o in opts}
                qs[name] = {"type": "choice", "instructions": q.get("instructions") or q.get("question", ""), "criteria": criteria}
            elif qtype == "score":
                criteria = q.get("criteria") or q.get("rubric") or ["low", "medium", "high"]
                qs[name] = {"type": "score", "instructions": q.get("instructions") or q.get("question", ""), "criteria": criteria}
            else:  # noul
                qs[name] = {"type": "noul", "instructions": q.get("instructions") or q.get("question", "")}
        
        body = json.dumps({"model": model, "state": state, "questions": qs}).encode()
        req = urllib.request.Request(
            f"{self.base}/v1/systemone", data=body,
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"})
        t0 = time.monotonic()
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            payload = json.loads(resp.read().decode())
        latency_ms = (time.monotonic() - t0) * 1000
        
        results = []
        for name, ans in payload.get("answers", {}).items():
            kind = ans.get("type", "")
            if kind == "noul":
                results.append(JEVResult(kind="noul", value=ans.get("noul"), confidence=ans.get("noul"), source="typesafe", latency_ms=latency_ms))
            elif kind == "choice":
                results.append(JEVResult(kind="choice", value=ans.get("choice"), confidence=ans.get("confidence"), probabilities=ans.get("probabilities"), source="typesafe", latency_ms=latency_ms))
            elif kind == "score":
                results.append(JEVResult(kind="score", value=ans.get("score"), confidence=ans.get("confidence"), probabilities=ans.get("probabilities"), source="typesafe", latency_ms=latency_ms))
        
        meta = {"latency_ms": latency_ms, "questions": len(questions), "model": payload.get("model", "jev"), "input_tokens": payload.get("usage", {}).get("input_tokens", 0), "output_tokens": payload.get("usage", {}).get("output_tokens", 0)}
        return results, meta

    def decide(self, state: Any, question: dict, model: str = "jev-latest") -> JEVResult:
        results, _ = self.decide_batch(state, [question], model)
        return results[0]


# === Random fallback ===

import random

class RandomBackend:
    """Random fallback — preserves API surface, returns uniform choices."""
    name = "fallback"

    def decide(self, state: Any, question: dict) -> JEVResult:
        kind = question.get("type", "noul").lower()
        if kind == "choice":
            options = list(question.get("options", ["a", "b"]))
            value = random.choice(options)
            prob = 1.0 / len(options)
            return JEVResult(kind="choice", value=value, probabilities={o: prob for o in options}, confidence=0.33, source="fallback")
        elif kind == "score":
            return JEVResult(kind="score", value=1.0, confidence=0.33, source="fallback")
        else:  # noul
            v = random.random()
            return JEVResult(kind="noul", value=v, confidence=v, source="fallback")

    def decide_batch(self, state: Any, questions: List[dict]) -> Tuple[List[JEVResult], dict]:
        results = [self.decide(state, q) for q in questions]
        return results, {"latency_ms": 0, "questions": len(questions), "model": "fallback"}


# === Unified Connector ===

class JEVConnector:
    """Universal connector with 3 primitives × 3 backends.
    
    Exact-first doctrine: try typesafe (cloud), fall back to random.
    """

    def __init__(self, api_key: Optional[str] = None, prefer: str = "typesafe"):
        self.typesafe = TypeSafeBackend(api_key=api_key)
        self.fallback = RandomBackend()
        self.prefer = prefer

    def decide(self, options: List[Any], context: str = "", samples: int = 1) -> JEVResult:
        """Choice primitive — pick one of options."""
        if self.typesafe.available():
            try:
                return self.typesafe.decide(context, {"type": "choice", "instructions": "Choose the best option given the context.", "options": options})
            except Exception as e:
                print(f"typesafe failed: {e}, falling back")
        return self.fallback.decide(context, {"type": "choice", "options": options})

    def score(self, candidate: str, rubric: List[str] = None) -> JEVResult:
        """Score primitive — rate the candidate."""
        rubric = rubric or ["bad", "ok", "good", "great"]
        if self.typesafe.available():
            try:
                return self.typesafe.decide(candidate, {"type": "score", "instructions": rubric if not isinstance(rubric, str) else rubric, "criteria": rubric})
            except Exception as e:
                print(f"typesafe failed: {e}, falling back")
        return self.fallback.decide(candidate, {"type": "score", "criteria": rubric})

    def noul(self, question: str, context: str = "") -> JEVResult:
        """Noul primitive — yes/no probability."""
        if self.typesafe.available():
            try:
                return self.typesafe.decide(context, {"type": "noul", "instructions": question})
            except Exception as e:
                print(f"typesafe failed: {e}, falling back")
        return self.fallback.decide(context, {"type": "noul", "instructions": question})

    def batch(self, state: Any, questions: List[dict]) -> List[JEVResult]:
        """Batch — N questions in one parallel pass."""
        if self.typesafe.available():
            try:
                results, _ = self.typesafe.decide_batch(state, questions)
                return results
            except Exception as e:
                print(f"typesafe batch failed: {e}, falling back")
        results, _ = self.fallback.decide_batch(state, questions)
        return results


# === Module-level convenience ===

_default_connector: Optional[JEVConnector] = None


def get_connector() -> JEVConnector:
    global _default_connector
    if _default_connector is None:
        _default_connector = JEVConnector()
    return _default_connector


def decide(options: List[Any], context: str = "") -> JEVResult:
    return get_connector().decide(options, context)


def score(candidate: str, rubric: List[str] = None) -> JEVResult:
    return get_connector().score(candidate, rubric)


def noul(question: str, context: str = "") -> JEVResult:
    return get_connector().noul(question, context)


if __name__ == "__main__":
    print("=== JEV Connector with REAL TypeSafe API ===\n")
    
    conn = JEVConnector()
    print(f"Typesafe available: {conn.typesafe.available()}")
    print(f"API key starts with: {conn.typesafe.key[:12] if conn.typesafe.key else 'N/A'}...")
    
    # Test the 3 primitives
    print("\n--- Choice ---")
    r = conn.decide(["greet_warmly", "greet_neutral", "be_silent"], context="User says hello!")
    print(f"  Choice: {r.value} (conf {r.confidence:.2f}, source {r.source}, {r.latency_ms:.0f}ms)")
    if r.probabilities:
        print(f"  Probs: {r.probabilities}")
    
    print("\n--- Noul ---")
    r = conn.noul("Is the user happy?", context="User says: I love this product!")
    print(f"  Yes-prob: {r.value:.2f} (conf {r.confidence:.2f}, source {r.source})")
    
    print("\n--- Score ---")
    r = conn.score("I love this product", rubric=["bad", "neutral", "positive", "enthusiastic"])
    print(f"  Score: {r.value} (conf {r.confidence:.2f}, source {r.source})")
    
    print("\n--- Batch ---")
    qs = [
        {"name": "tone", "type": "choice", "instructions": "What is the tone?", "options": ["warm", "neutral", "cold"]},
        {"name": "is_happy", "type": "noul", "instructions": "Is the user happy?"},
        {"name": "urgency", "type": "score", "instructions": "How urgent?", "criteria": ["low", "medium", "high"]},
    ]
    results = conn.batch("I love this product!", qs)
    for r in results:
        print(f"  {r}")
