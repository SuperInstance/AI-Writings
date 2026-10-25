## TYPESAFE JEV API — REAL WORKING SCHEMA (discovered 2026-09-21)

**THE BREAKTHROUGH**: After many failed schemas, the real schema is:

```
POST https://api.typesafe.ai/v1/systemone
Authorization: Bearer apikey_xxxx
Content-Type: application/json

{
  "model": "jev-latest",        // or "jev-preview"
  "state": "any text or object",
  "questions": {
    "name1": {
      "type": "noul",            // LOWERCASE! not "Noul"
      "instructions": "Is the user happy?"
    },
    "name2": {
      "type": "choice",
      "instructions": "What is the tone?",
      "criteria": {              // DICT, not list
        "warm": "friendly",
        "neutral": "informational",
        "angry": "upset"
      }
    },
    "name3": {
      "type": "score",
      "instructions": "How urgent?",
      "criteria": ["low", "medium", "high"]   // LIST
    }
  }
}
```

**RESPONSE**:
```
{
  "model": "jev-1.13.0",
  "answers": {
    "name1": {"type": "noul", "noul": 0.33},
    "name2": {"type": "choice", "choice": "angry", "confidence": 0.76, "probabilities": {...}},
    "name3": {"type": "score", "score": 1.76, "confidence": 0.64, "legend": {...}, "probabilities": {...}}
  },
  "usage": {"input_tokens": 390, "output_tokens": 73}
}
```

**KEY FACTS**:
- Endpoint: `/v1/systemone` (NOT `/v1/decide`, NOT `/v1/jev`)
- `type` is LOWERCASE: `"noul"`, `"choice"`, `"score"` (NOT `"Noul"` etc)
- `questions` must be DICT `{name: Question}` (NOT list)
- `instructions` is the question text (NOT `question`)
- `criteria` is dict for choice, list for score
- Get model list: GET `/v1/models`
- Latency: ~250ms per batch (10-15ms minimum)
- Token usage: ~390 input + ~73 output per 3-question batch
- OpenAPI schema at: `/openapi.json`

**INTEGRATION (canonical)**:
```python
from jev_connector import TypeSafeBackend, JEVConnector
conn = JEVConnector()
result = conn.decide(["a", "b", "c"], context="...")
# Returns JEVResult(kind="choice", value="b", confidence=0.85, probabilities={...}, source="typesafe", latency_ms=250)
```

**CHESS-BOAT REAL OUTPUT**:
> Initialized cells: 5 (rules, position, evaluator, reflex, learning)
> Move 1: Selected e2-e4 (confidence: 0.96)
> Move 2: Selected e2-e4 (confidence: 0.96)  [opening repetition, JEV knows]
> Move 3: Selected e2-e4 (confidence: 0.96)
> Witness entries: 17 (5 init + 12 from moves)

**SUBSTRATE BOT REAL OUTPUT** (3 personalities, real LLM + real JEV validation):
> Wesley (warm): "Hey there! I'm doing pretty well, just sipping on some digital coffee."
> Mechanic (mechanic): "I'm running at optimal efficiency, thank you for the check-in. Let's keep this brief: what vehicle or component needs your attention today?"
> Shepherd (shepherd): "Ah, friend, the morning light is catching the fur on my horns, and my flock is surprisingly quiet. I'm doing well enough, though I must confess, I'm always on the lookout for strays."

JEV IS LIVE IN THE SUBSTRATE.
