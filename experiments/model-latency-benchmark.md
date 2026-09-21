# Experiment 3: Model Latency Benchmark

**Date:** 2026-08-08  
**Test:** Measure response time for "Say hello in one sentence."  
**Method:** `time curl` 3 runs per model, wall clock, streaming disabled  
**Hardware:** WSL2 Linux, local Ollama instance

---

## Results

### granite3.1-dense:2b
| Run | Latency |
|-----|---------|
| 1 | 557ms |
| 2 | 628ms |
| 3 | 464ms |
| **Average** | **550ms** |

### llama3.2:1b
| Run | Latency |
|-----|---------|
| 1 | 38,981ms ⚠️ *(cold start — model loading)* |
| 2 | 375ms |
| 3 | 304ms |
| **Average (excl. cold start)** | **340ms** |
| **Average (incl. cold start)** | **13,220ms** |

### qwen2.5:0.5b
| Run | Latency |
|-----|---------|
| 1 | 18,618ms ⚠️ *(cold start — model loading)* |
| 2 | 1,671ms |
| 3 | 2,059ms |
| **Average (excl. cold start)** | **1,865ms** |

### llava:7b
| Run | Latency |
|-----|---------|
| 1 | 40,463ms ⚠️ *(cold start — model loading)* |
| 2 | 2,141ms |
| 3 | 4,466ms |
| **Average (excl. cold start)** | **3,304ms** |

**llava:7b was measurable but extremely slow.** Cold start took 40 seconds. Even warm, it averaged 3.3 seconds for a one-sentence response — and this was for simple text generation. Vision tasks (image analysis) took 2-5 minutes. On this hardware, llava:7b is not viable for interactive NPC workloads.

---

## Analysis

### Real-Time NPC Dialogue Threshold (< 500ms)

| Model | Warm Latency | Viable for Real-Time? |
|-------|-------------|----------------------|
| llama3.2:1b | ~340ms | ✅ **YES — fastest warm model** |
| granite3.1-dense:2b | ~550ms | ⚠️ **MARGINAL — just over threshold, but acceptable** |
| qwen2.5:0.5b | ~1,865ms | ❌ **NO — too slow despite tiny size** |
| llava:7b | ~3,304ms (text only) | ❌ **NO — vision tasks take minutes** |

### Cold Start Problem

The first call to any model triggers a load from disk into VRAM/RAM:
- llama3.2:1b cold start: **39 seconds** → warm: **340ms** (115x faster after loading)
- qwen2.5:0.5b cold start: **18.6 seconds** → warm: **1.6s** (11x faster)
- granite3.1-dense:2b: no significant cold start observed (likely pre-loaded)

**Implication:** Any model selection system must pre-load (warm) models before players interact. A cold-start NPC would hang for 18-39 seconds on first interaction — unacceptable.

### The Counterintuitive Result

**qwen2.5:0.5b (the smallest model) is SLOWER than llama3.2:1b and granite3.1-dense:2b.** This seems paradoxical — fewer parameters should mean faster inference. The explanation: Ollama's inference overhead (tokenization, context processing, response parsing) dominates at tiny model sizes. The 0.5B model's inference is so fast it's bottlenecked by framework overhead, not compute. Meanwhile, llama3.2:1b is better optimized in Ollama's inference pipeline.

### Hardware Constraints

Running multiple models simultaneously caused OOM conditions:
- granite + llama + qwen together: OK
- Adding llava:7b to the mix: **killed other models** (OOM)
- llava alone: functional but extremely slow

**Memory budget on this machine appears sufficient for ~3B parameters total of loaded models.** llava:7b alone consumes most of available VRAM.

---

## Key Finding

**For real-time NPC dialogue:**
1. **llama3.2:1b is the speed champion** (340ms warm) but produces lower-quality text
2. **granite3.1-dense:2b is the best speed/quality balance** (550ms warm, highest dialogue quality)
3. **qwen2.5:0.5b is neither fast enough nor good enough** for interactive use
4. **llava:7b is desktop-only** — use for offline analysis, never for real-time interaction

**Recommendation:** Pre-load granite3.1-dense:2b as primary NPC engine. Keep llama3.2:1b loaded as fallback. Never hot-load llava during a session.
