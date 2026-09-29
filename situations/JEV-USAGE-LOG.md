# JEV Usage Log

Recovered experiments (a prior session ran these but could not push). Re-run live on 2026-09-29.
Key values are never recorded here — env var names only.

## 1. Liveness (2026-09-29)

| service | env var(s) | call | result |
|---|---|---|---|
| JEV | `TYPESAFEAI_KEY` | `POST /v1/systemone`, one `noul` ("Water boils at 100 °C at sea level") | **200**, model `jev-1.13.0`, noul 0.94 |
| Moth | `MOTHQUANTUM_KEY`, `MOTHQUANTUM_BASE` | `comet-qrng-v1/process` ints 0–8 ×6 | **202** queued → completed → result **200**: `[3,5,3,2,5,6]`, Bell S = 2.84 |
| DeepInfra | `DEEPINFRA_KEY` | chat completion, Llama-3.1-8B, 3 tokens | **200** |
| DeepSeek | `DEEPSEEK_KEY` | chat completion, `deepseek-chat`, 3 tokens | **200** (served as `deepseek-flash`) |

No auth errors. All four keys are live in this session.

## 2. Decomposing fold (2026-09-29)

Question: `noul` "Is this statement factually true?" (criteria true=accurate / false=false).
Run with `labs/jev-fold/fold.mjs` (live).

**Claim A** — "The Eiffel Tower is in Paris, and the Great Wall of China is in Japan, and water freezes at 0 degrees Celsius."

| statement | noul |
|---|---|
| whole | 0.08 |
| The Eiffel Tower is in Paris | 0.98 |
| **the Great Wall of China is in Japan** (false) | **0.01** |
| water freezes at 0 degrees Celsius | 0.94 |

**Claim B** — "Mount Everest is the tallest mountain above sea level, and the Amazon River flows through Brazil, and the chemical symbol for gold is Ag."

| statement | noul |
|---|---|
| whole | 0.08 |
| Mount Everest is the tallest mountain above sea level | 0.91 |
| the Amazon River flows through Brazil | 0.96 |
| **the chemical symbol for gold is Ag** (false — it is Au) | **0.02** |

**Result: yes, the per-part scores pinpoint the false part both times**, by a wide margin
(next-lowest part minus weakest = 0.93 and 0.89). The whole-claim noul (0.08) correctly says
"something here is false" but not *what*; the fold turns that verdict into a location.
Divergence whole − fold_min is small (0.06–0.07): for plain factual conjunctions JEV already
propagates the false conjunct into the whole, so the fold's value is localization, not detection.
