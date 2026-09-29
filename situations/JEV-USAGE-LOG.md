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
