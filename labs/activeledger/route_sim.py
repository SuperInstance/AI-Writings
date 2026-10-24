"""Canonical route, simulated as cheap deterministic cells:

    microphone -> speech/noise pre-filter -> STT -> grammar-cleanup -> LLM

Cells are simulated (no models). The point is what gets BOOKED: cell.tick intra-state
(with confidence + load), route.hop double-entry unit translation, and the pre-filter's
measurable reduction of STT load. Run with filter=False for the no-filter baseline.
"""

from __future__ import annotations

from activeledger import (ActiveLog, DoubleEntry, ZERO_BUDGET, add_budget, budget,
                          content_hash, route_total)

# Deterministic audio: 10 frames of 100ms. (label, energy) — label is ground truth for the sim.
FRAMES = [("noise", 0.05), ("speech", 0.8), ("speech", 0.9), ("noise", 0.1), ("silence", 0.0),
          ("speech", 0.7), ("noise", 0.2), ("silence", 0.0), ("speech", 0.85), ("noise", 0.07)]
WORDS = {1: "turn", 2: "on", 5: "the", 8: "lights"}          # words carried by speech frames
CELL_KIND = {"microphone": "PHYSICAL", "prefilter": "FILTER", "stt": "TOOL",
             "cleanup": "FILTER", "llm": "LLM"}

# Per-frame STT model cost (the load the pre-filter is meant to shrink).
STT_MS_PER_FRAME, STT_W_PER_FRAME = 12, 0.4


def _prefilter_conf(label, energy):
    """Simulated VAD: confidence a frame is speech (deterministic)."""
    return {"speech": 0.9 + energy / 20, "noise": 0.15 + energy, "silence": 0.02}[label]


def run(use_filter=True, threshold=0.5, dev="activeledger") -> dict:
    al = ActiveLog(dev=dev)
    rid = "route:mic-stt-llm:%s" % ("filtered" if use_filter else "nofilter")
    n = len(FRAMES)
    stages = []

    def tick(cell, state, b):
        al.emit("cell.tick", {"cell": cell, "kind": CELL_KIND[cell], "route": rid,
                              **state, "budget": b})

    def hop(src, su, sa, dst, du, rate, ref, b):
        body = DoubleEntry.translate(src, su, sa, dst, du, rate, ref).body()
        body.update({"route": rid, "budget": b})
        return al.emit("route.hop", body)["body"]["debit"]["amount"]

    # 1. microphone: emits n frames (own units: frames)
    tick("microphone", {"units": "frames", "frames_out": n, "confidence": 1.0, "load": n},
         budget(wall_ms=n, power_w=0.05 * n, mem_mb=1, prod=64, train=128, reqs="local+physical"))

    # 2. pre-filter (optional): drops obviously-not-speech frames
    if use_filter:
        confs = [_prefilter_conf(l, e) for l, e in FRAMES]
        keep = [i for i, c in enumerate(confs) if c >= threshold]
        tick("prefilter", {"units": "frames", "frames_in": n, "frames_out": len(keep),
                           "dropped": n - len(keep), "confidence": round(sum(confs[i] for i in keep) / len(keep), 4),
                           "confidences": [round(c, 4) for c in confs], "load": n},
             budget(wall_ms=n, power_w=0.02 * n, mem_mb=1, prod=96, train=192))
    else:
        keep = list(range(n))
    frames_to_stt = len(keep)
    hop("microphone", "frames", n, "stt", "frames", frames_to_stt / n, "T:mic->stt/keep-fraction",
        budget(wall_ms=1, power_w=0.01, mem_mb=0, prod=32, train=64))

    # 3. STT: load scales with frames received — this is what the filter shrinks
    words = [WORDS[i] for i in keep if i in WORDS]
    stt_load = frames_to_stt
    tick("stt", {"units": "frames", "frames_in": frames_to_stt, "words": words,
                 "confidence": round(len(words) / max(1, sum(1 for i in keep if FRAMES[i][0] == "speech")), 4),
                 "load": stt_load},
         budget(wall_ms=STT_MS_PER_FRAME * stt_load, power_w=round(STT_W_PER_FRAME * stt_load, 6),
                mem_mb=48, prod=4096, train=8192, tokens={"stt-sim": 0}, reqs="local"))
    stages.append(("stt", stt_load))
    hop("stt", "words", len(words), "cleanup", "tokens", 1.0, "T:words->tokens",
        budget(wall_ms=1, power_w=0.01, mem_mb=0, prod=32, train=64))

    # 4. grammar cleanup
    text = " ".join(words)
    cleaned = text[:1].upper() + text[1:] + "."
    tick("cleanup", {"units": "tokens", "in": text, "out": cleaned, "confidence": 0.97, "load": len(words)},
         budget(wall_ms=2, power_w=0.05, mem_mb=8, prod=512, train=1024, tokens={"slm-sim": 4 * len(words)},
                usd=0.00001 * len(words), reqs="net"))
    hop("cleanup", "tokens", len(words), "llm", "prompt-tokens", 1.5, "T:tokens->prompt-tokens (+template)",
        budget(wall_ms=1, power_w=0.01, mem_mb=0, prod=32, train=64))

    # 5. LLM: deterministic canned reply keyed on the transcript
    reply = "Lights on." if cleaned.lower().startswith("turn on") else "Sorry?"
    tick("llm", {"units": "prompt-tokens", "in": cleaned, "out": reply, "confidence": 0.9, "load": int(len(words) * 1.5),
                 "cot": "transcript parsed as a device command"},
         budget(wall_ms=40, power_w=3.0, mem_mb=256, prod=2048, train=4096, tokens={"llm-sim": 12}, usd=0.0004, reqs="net"))

    total = route_total(al.records, rid)
    txn = al.emit("ledger.transaction", {
        "route": rid, "status": "settled", "transcript": cleaned, "reply": reply,
        "product_hash": content_hash({"transcript": cleaned}), "stt_load": stt_load,
        "binds": [content_hash(r) for r in al.records if r["body"].get("route") == rid],
        "total_budget": total})
    return {"log": al, "route": rid, "transcript": cleaned, "reply": reply, "stt_load": stt_load,
            "total_budget": total, "txn": txn}
