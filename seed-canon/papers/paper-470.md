# F161 — Conservation Laws as Fences: The Physics of Working Animals
## Introduction

In the context of Quilt, a new framework for working animals, we propose three conservation laws that govern the behavior of these agents. These laws, enforced by the FLUX bytecode and runtime, ensure that working animals operate within a safe and bounded envelope. This paper defines these laws precisely, providing a clear understanding of their implications on the behavior of working animals.

## The Three Conservation Laws

### 1. Attention Budget (AB)

| **Property** | **Description** |
| --- | --- |
| **What** | The amount of LLM tokens (in + out) per session / per turn |
| **Unit** | tokens |
| **Default Fence** | 4096 tokens per turn, 32000 per session |
| **Boundary** | The agent is given 1 final "wrap-up" move, then terminated |
| **Test Vector** | 4000 tokens used, 96 remaining. The agent MUST summarize, not elaborate. |

The Attention Budget (AB) law conserves the amount of LLM tokens used by a working animal per session or turn. The default fence is set to 4096 tokens per turn and 32000 per session. When the boundary is reached, the agent is given a single "wrap-up" move before being terminated. The test vector demonstrates that with 4000 tokens used and 96 remaining, the agent must summarize its work without elaborating.

### 2. Action Potential (AP)

| **Property** | **Description** |
| --- | --- |
| **What** | The number of side-effecting tool calls per turn |
| **Unit** | integer |
| **Default Fence** | 7 tool calls per turn |
| **Boundary** | The agent returns "exceeded AP budget" with a partial result |
| **Test Vector** | 7/7 used. The next call must be a read-only call. The 8th write attempt returns 429. |

The Action Potential (AP) law conserves the number of side-effecting tool calls per turn. The default fence is set to 7 tool calls per turn. When the boundary is reached, the agent returns an "exceeded AP budget" message with a partial result. The test vector shows that after using 7 tool calls, the next attempt must be a read-only call, and the 8th write attempt returns a 429 error.

### 3. Information Throughput (IT)

| **Property** | **Description** |
| --- | --- |
| **What** | The number of cells modified per TICK |
| **Unit** | cells |
| **Default Fence** | 12 cells per TICK per agent |
| **Boundary** | The agent pauses, the rest is queued for the next TICK |
| **Test Vector** | 11 cells modified, 1 remaining. The 12th is allowed. The 13th blocks until the next TICK. |

The Information Throughput (IT) law conserves the number of cells modified per TICK. The default fence is set to 12 cells per TICK per agent. When the boundary is reached, the agent pauses, and the remaining modifications are queued for the next TICK. The test vector demonstrates that with 11 cells modified and 1 remaining, the 12th modification is allowed, but the 13th blocks until the next TICK.

## The Conservation Law Equation

For any working animal w at time t:
AB(w, t) + AP(w, t) + IT(w, t) ≤ fence(w)

Where fence(w) is the per-animal budget.

## Implications of Conservation Laws

The three conservation laws form a 3-dimensional working envelope (AB, AP, IT) that bounds the behavior of working animals. The envelope is the pasture, and the working animal is the inhabitant. The fence is the boundary of the envelope, and the runtime is the fence.

## What Happens When a Fence is Crossed

| **Event** | **Description** |
| --- | --- |
| **Fence Crossed** | The next call is REJECTED (HTTP 429) with a "fence crossed" message |
| **Agent Response** | The agent must return a partial result OR a "rejection notice" |
| **Integrity Score** | The partial result IS the integrity score for the turn |

When a fence is crossed, the agent is not yelled at or given a warning. Instead, the next call is rejected with a "fence crossed" message. The agent must return a partial result or a "rejection notice," which serves as the integrity score for the turn.

The fence is not a suggestion. The fence is physics. The runtime is the fence. The agent lives in the pasture. The pasture is bounded. The bounded pasture is what makes the working animal safe.