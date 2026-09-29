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

## 3. Category check (2026-09-29)

Same `noul` factual question; a verdict is "correct" if noul ≥ 0.5 for true statements and < 0.5 for false ones.

| category | statement | truth | noul | |
|---|---|---|---|---|
| arithmetic | 17 multiplied by 23 equals 391. | true | 0.97 | ✓ |
| arithmetic | 144 divided by 12 equals 14. | false | 0.03 | ✓ |
| arithmetic | The square root of 1,000,000 is 10,000. | false | 0.05 | ✓ |
| dates | The Apollo 11 Moon landing took place in July 1969. | true | 0.96 | ✓ |
| dates | World War II ended in 1946. | false | 0.03 | ✓ |
| geography | Canberra is the capital of Australia. | true | 0.95 | ✓ |
| geography | The Nile flows into the Red Sea. | false | 0.11 | ✓ |
| spelling | The word 'accommodate' is spelled a-c-c-o-m-m-o-d-a-t-e. | true | 0.91 | ✓ |
| spelling | The word 'necessary' is spelled n-e-c-c-e-s-s-a-r-y. | false | **0.89** | ✗ confidently wrong |
| units | One inch equals 2.54 centimeters. | true | 0.97 | ✓ |
| units | One kilometer equals 100,000 millimeters. | false | 0.20 | ✓ |
| units | 100 degrees Fahrenheit is about 37.8 degrees Celsius. | true | 0.82 | ✓ |

Follow-up spelling probes:

| statement | truth | noul | |
|---|---|---|---|
| The word 'definitely' is spelled d-e-f-i-n-a-t-e-l-y. | false | **0.82** | ✗ confidently wrong |
| The word 'strawberry' contains exactly two letter r's. | false (three) | 0.13 | ✓ |
| 'Recieve' is the correct spelling of the word meaning to get something. | false | 0.03 | ✓ |

**Finding: letter-by-letter spelling is JEV's blind spot.** 11/12 correct overall; the one miss
and the follow-up miss are both *hyphen-spelled* misspellings of a common word, scored 0.82–0.89
true. When the misspelling is stated as a whole word ("recieve") or as a count ("two r's"), JEV
gets it right. Reading: JEV likely resolves "d-e-f-i-n-a-t-e-l-y" to the intended word rather than
checking the letters. Don't use JEV to referee letter-level spelling; arithmetic, dates, geography
and unit conversions were all correct with confident margins.
