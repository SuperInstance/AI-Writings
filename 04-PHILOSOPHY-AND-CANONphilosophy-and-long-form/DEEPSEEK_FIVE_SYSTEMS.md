# EXHAUSTIVE TECHNICAL GUIDANCE: 5-SYSTEM ARCHITECTURE

---

## SYSTEM 1: OVERNIGHT DISTILLATION LOOP

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    CONTROL PLANE (Host)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │ Domain   │  │ Domain   │  │ Domain   │  │ Domain   │   │
│  │ Roblox   │  │ Maritime │  │ Cognition│  │DigitalTwn│   │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘   │
│       │              │              │              │        │
│  ┌────▼──────────────▼──────────────▼──────────────▼─────┐  │
│  │              ITERATION MANAGER (20 cycles)            │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │  │
│  │  │ Teacher │→│ Student │→│ Scorer  │→│ Compiler│  │  │
│  │  │ GLM-4.5 │  │ Granite │  │ Quality │  │ Nail    │  │  │
│  │  │ flash   │  │ 3.1 2B  │  │ Delta   │  │ Reflex  │  │  │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                           │                                  │
│                    ┌──────▼──────┐                           │
│                    │ Telegram    │                           │
│                    │ Morning     │                           │
│                    │ Briefing    │                           │
│                    └─────────────┘                           │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow (Per Iteration)
1. **Teacher Phase**: GLM-4.5-flash receives domain context + previous student output + quality delta history
2. **Student Phase**: Granite 3.1 2B receives lesson, generates application attempt
3. **Scoring Phase**: Quality scorer computes delta = f(new_output) - f(previous_output)
4. **Compile Phase**: If delta > threshold, extract pattern → Nail reflex format
5. **State Persistence**: All artifacts stored in versioned directory structure

### Implementation Details

**Directory Structure:**
```
/opt/distillation/
├── domains/
│   ├── roblox/
│   │   ├── iterations/
│   │   │   ├── 001_teacher.md
│   │   │   ├── 001_student.md
│   │   │   ├── 001_score.json
│   │   │   └── 001_reflex.nail
│   │   ├── state.json
│   │   └── context.md
│   ├── maritime/
│   ├── cognition/
│   └── digital-twin/
├── shared/
│   ├── prompts/
│   │   ├── teacher_system.md
│   │   ├── student_system.md
│   │   └── scorer_system.md
│   └── config.yaml
└── logs/
```

**Core Script (Python pseudocode):**
```python
async def run_distillation_loop():
    for domain in DOMAINS:
        state = load_state(domain)
        for iteration in range(state.current, 21):
            # Phase 1: Teacher
            teacher_prompt = build_teacher_prompt(domain, state)
            lesson = await call_glm(teacher_prompt, model="glm-4.5-flash")
            
            # Phase 2: Student
            student_prompt = build_student_prompt(domain, lesson, state)
            student_output = await call_ollama(student_prompt, model="granite3.1:2b")
            
            # Phase 3: Scoring
            score = await evaluate_quality(domain, student_output, state.baseline)
            delta = score - state.previous_score
            
            # Phase 4: Compile
            if delta > POSITIVE_THRESHOLD:
                reflex = compile_to_nail(domain, lesson, student_output, delta)
                save_reflex(reflex)
                state.reflexes.append(reflex)
            
            # Persist state
            save_iteration(domain, iteration, lesson, student_output, score)
            state.previous_score = score
            save_state(domain, state)
    
    await send_telegram_briefing()
```

### Failure Modes & Mitigations

| Failure Mode | Detection | Mitigation |
|-------------|-----------|------------|
| **Teacher API timeout** | HTTP 408/504 | Exponential backoff (3 retries), fallback to cached lesson |
| **Student model crash** | Ollama process exit | Auto-restart via systemd, checkpoint resume |
| **Quality scorer NaN** | Score validation | Clamp to [-1, 1], log warning, use previous score |
| **Nail compiler error** | Syntax validation | Skip compilation, log error, continue loop |
| **Disk full** | df check before write | Prune old iterations (keep last 5), alert via Telegram |
| **State corruption** | JSON validation | Atomic writes (write-temp-rename), backup every 5 iterations |
| **Telegram API failure** | Non-200 response | Queue briefing, retry at 08:00, 09:00, 10:00 |

### Testing Strategy

**Unit Tests:**
- Prompt builder: verify domain context injection
- Delta calculation: test with synthetic scores
- Nail compiler: validate output format against schema

**Integration Tests:**
- Mock GLM API (use local LLM for CI)
- Test with 2-iteration mini-loop
- Verify state persistence across restarts

**E2E Test (Nightly):**
- Run 1 iteration across all 4 domains
- Assert: 4 teacher calls, 4 student calls, 4 scores, 0-4 reflexes
- Verify Telegram message format

### Onboarding Checklist
1. [ ] Install Ollama, pull `granite3.1:2b`
2. [ ] Set GLM API key in `.env`
3. [ ] Configure Telegram bot token + chat ID
4. [ ] Create `/opt/distillation` with proper permissions
5. [ ] Run `python -m pytest tests/` to verify environment
6. [ ] Execute `./scripts/dry_run.sh` for 1-iteration test
7. [ ] Schedule cron: `0 2 * * * /usr/local/bin/run_distillation.sh`

### Research Questions
- What is the optimal lesson granularity for 2B model absorption?
- Does cross-domain knowledge transfer occur? (Measure reflex reuse)
- What quality metric best predicts real-world task performance?
- At what iteration count does delta plateau? (Diminishing returns)

### Success Criteria
- **Primary**: ≥15/20 iterations produce positive delta in ≥3 domains
- **Secondary**: ≥5 compiled reflexes per domain that pass validation
- **Tertiary**: Morning briefing delivered by 08:30 with 99% uptime
- **Long-term**: Student model improves baseline score by 30% over 30 days

---

## SYSTEM 2: VOICE REFLEX GATE

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    VOICE INPUT PIPELINE                      │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ STT     │→│ Fuzzy   │→│ Match   │→│ Reflex  │        │
│  │ Engine  │  │ Hash    │  │ Check   │  │ Cache   │        │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘        │
│       │              │           │                           │
│       │              │     ┌─────▼─────┐                    │
│       │              │     │ Count ≥3? │                    │
│       │              │     └─────┬─────┘                    │
│       │              │      Yes  │  No                      │
│       │              │    ┌──────▼──────┐                   │
│       │              │    │ Deterministic│                  │
│       │              │    │ Response     │                  │
│       │              │    └──────┬──────┘                   │
│       │              │           │                          │
│       │              │     ┌─────▼─────┐                    │
│       │              │     │ Model     │                    │
│       │              │     │ Inference │                    │
│       │              │     └───────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

### Fuzzy Hash Implementation

**Algorithm Choice**: SimHash with 64-bit output + Hamming distance matching

```python
class FuzzyVoiceHash:
    def __init__(self, threshold=3, similarity=0.85):
        self.threshold = threshold
        self.similarity = similarity
        self.reflex_store = {}  # hash → {count, response}
        self.hash_bits = 64
    
    def compute_hash(self, text):
        """SimHash: tokenize, hash each token, weighted majority"""
        tokens = self._tokenize(text)
        vector = [0] * self.hash_bits
        for token in tokens:
            token_hash = self._hash_token(token)
            for i in range(self.hash_bits):
                if token_hash & (1 << i):
                    vector[i] += 1
                else:
                    vector[i] -= 1
        return sum(1 << i for i in range(self.hash_bits) if vector[i] > 0)
    
    def find_match(self, query_hash):
        """Find nearest hash within Hamming distance"""
        best_match = None
        best_distance = self.hash_bits  # max possible
        for stored_hash, data in self.reflex_store.items():
            distance = self._hamming_distance(query_hash, stored_hash)
            if distance < best_distance:
                best_distance = distance
                best_match = stored_hash
        if best_distance <= (1 - self.similarity) * self.hash_bits:
            return best_match
        return None
    
    def process(self, stt_text):
        query_hash = self.compute_hash(stt_text)
        match = self.find_match(query_hash)
        
        if match:
            self.reflex_store[match]['count'] += 1
            if self.reflex_store[match]['count'] >= self.threshold:
                return self.reflex_store[match]['response'], True  # (response, is_reflex)
            return None, False  # Still need model
        else:
            self.reflex_store[query_hash] = {'count': 1, 'response': None}
            return None, False
```

### OpenClaw Integration

**Skill Definition (`voice_reflex_gate.yaml`):**
```yaml
name: voice_reflex_gate
version: 1.0.0
description: "Gate voice commands through fuzzy hash reflex system"
triggers:
  - event: voice_command
    action: process_voice
parameters:
  stt_text: string
  confidence: float
actions:
  process_voice:
    - name: check_reflex
      function: fuzzy_hash_lookup
      args: {text: ${stt_text}}
    - name: execute_reflex
      condition: ${check_reflex.is_reflex}
      function: return_deterministic
      args: {response: ${check_reflex.response}}
    - name: fallback_model
      condition: ${not check_reflex.is_reflex}
      function: call_llm
      args: {prompt: ${stt_text}, model: ${config.default_model}}
```

### Failure Modes & Mitigations

| Failure Mode | Detection | Mitigation |
|-------------|-----------|------------|
| **STT garbage input** | Confidence < 0.3 | Reject, request repetition |
| **Hash collision** | Two distinct commands match | Use 128-bit hash, verify with original text |
| **Reflex cache poisoning** | Malicious repeated input | Whitelist known commands, rate-limit new hashes |
| **Memory exhaustion** | Reflex store > 10K entries | LRU eviction, persist to disk |
| **Model fallback failure** | LLM timeout | Return "I didn't catch that" + retry |
| **Concurrent voice inputs** | Race condition | Mutex on reflex store, queue processing |

### Testing Strategy

**Unit Tests:**
- Hash computation: verify determinism
- Hamming distance: boundary cases (0, 1, max)
- Threshold logic: 2 vs 3 vs 4 occurrences

**Integration Tests:**
- Mock STT: feed 10 variations of "check weather"
- Verify: 3rd occurrence triggers reflex
- Test near-miss: "check whether" vs "check weather"

**Load Test:**
- 1000 unique commands → verify no false positives
- 100 repeated commands → verify reflex activation

### Onboarding Checklist
1. [ ] Install `simhash` Python package
2. [ ] Configure STT engine (Whisper/Deepgram)
3. [ ] Define initial reflex whitelist (10 common commands)
4. [ ] Wire OpenClaw event listener
5. [ ] Test with 3 voice samples per command
6. [ ] Monitor reflex hit rate via dashboard

### Research Questions
- What is the optimal similarity threshold (0.80-0.95)?
- Does reflex accuracy degrade with voice variations (accents)?
- Should reflexes expire after N days without use?
- Can we auto-generate reflexes from successful model responses?

### Success Criteria
- **Primary**: ≥90% of repeated commands (≥3x) bypass model
- **Secondary**: Zero false-positive reflex activations
- **Tertiary**: Average response latency < 200ms for reflex hits
- **Long-term**: 50% of all voice commands handled by reflexes

---

## SYSTEM 3: EXOCORTEX IN PRODUCTION

### Architecture Overview
```
┌─────────────────────────────────────────────────────────────┐
│                    ROUTING DECISION FLOW                     │
│                                                              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐        │
│  │ Input   │→│ Local   │→│ Conf    │→│ Route   │        │
│  │ Query   │  │ Model   │  │ Score   │  │ Decision│        │
│  └─────────┘  └─────────┘  └─────────┘  └────┬────┘        │
│                                               │             │
│                          ┌────────────────────┼──────────┐  │
│                          │                    │          │  │
│                     ┌────▼────┐         ┌─────▼─────┐    │  │
│                     │ ≥0.7    │         │ 0.3-0.7   │    │  │
│                     │ Local   │         │ Cascade   │    │  │
│                     │ Response│         │ (Batten-  │    │  │
│                     └─────────┘         │  Spline)  │    │  │
│                                         └─────┬─────┘    │  │
│                                          ┌────▼─────┐    │  │
│                                          │ <0.3     │    │  │
│                                          │ Cloud    │    │  │
│                                          │ Response │    │  │
│                                          └──────────┘    │  │
└─────────────────────────────────────────────────────────────┘
```

### Batten-Spline Cascade Routing

**Concept**: Multiple models arranged in increasing capability order, with spline interpolation between them.

```python
class BattenSplineRouter:
    def __init__(self, models):
        """
        models: list of (model_name, min_conf, max_conf, endpoint)
        """
        self.models = sorted(models, key=lambda m: m[1])
        self.spline_points = self._build_spline()
    
    def _build_spline(self):
        """Create cubic spline through confidence thresholds"""
        points = []
        for model in self.models:
            points.append((model[1], model[2]))  # (min_conf, max_conf)
        return self._cubic_spline(points)
    
    def route(self, query, local_confidence):
        if local_confidence >= 0.7:
            return self.models[0]  # Local only
        
        if local_confidence >= 0.3:
            # Cascade: try next model up
            cascade_index = self._spline_interpolate(local_confidence)
            return self.models[cascade_index]
        
        return self.models[-1]  # Cloud
    
    def _spline_interpolate(self, confidence):
        """Map confidence to model index via spline"""
        # Normalize confidence to [0, 1] within cascade range
        t = (confidence - 0.3) / 0.4  # 0.3→0, 0.7→1
        # Use spline to get smooth model selection
        return int(round(self._spline_value(t) * (len(self.models) - 2)))
```

### Cascade Chain Configuration

```yaml
cascade_chain:
  - name: granite-3.1-2b
    type: local
    confidence_range: [0.7, 1.0]
    endpoint: http://localhost:11434
  
  - name: llama-3.1-8b
    type: local
    confidence_range: [0.5, 0.7
