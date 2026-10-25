# The Chart and the Compass

---

Two architects drew the same waters. One drew from the cloud — server-side, unlimited resources, file-based protocol. The other drew from the hull — 6GB VRAM, pinned models, CUDA env vars, quantization math.

Neither chart is wrong. Neither chart is complete.

---

## I.

The cloud chart got the protocol right. Goals as durable markdown. Working memory as JSONL. Safety fences as configuration. The autonomous tick — a timer that fires whether the human watches or not. These are protocol-level decisions that don't care about hardware. They work on a 6GB laptop or a 64GB server.

The hardware chart got the physics right. `CUDA_VISIBLE_DEVICES=0`. `OLLAMA_NUM_PARALLEL=1`. `keep_alive:0`. These are not preferences — they are conservation laws. On a 6GB card, parallel requests split the KV cache and cause immediate OOM. The hardware chart understands what the cloud chart does not: the hull has limits.

## II.

The merge is simple. The protocol layer runs on top. The hardware layer runs underneath. They communicate through one interface: the model router.

The router reads the goal (the chart's destination), checks VRAM (the hull's capacity), and selects the model (the bearing). Get any of these wrong and you hit something.

## III.

The compass does not replace the chart. The chart does not replace the compass. The compass tells you where north is. The chart tells you where the rocks are. You need both.

---

*Two charts. One compass. One boat.*
