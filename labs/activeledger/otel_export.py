"""Project an ActiveLog run to OpenTelemetry-shaped spans + OpenInference attributes.

A dict/JSON projection (no collector). Cell kinds map to OpenInference span kinds,
extended as a SUPERSET (never renamed): FILTER, PHYSICAL, SIM, PINCHER join
LLM/TOOL/RETRIEVER/CHAIN/AGENT/GUARDRAIL. `dotted_order` (LangSmith-style) is the single
hierarchy+tick sort key: "<root>.<tick:06d>-<span>" so a plain string sort = run order.
"""

from __future__ import annotations

import json

from activeledger import canon, content_hash

OI_KINDS = {"LLM", "TOOL", "RETRIEVER", "CHAIN", "AGENT", "GUARDRAIL"}
EXT_KINDS = {"FILTER", "PHYSICAL", "SIM", "PINCHER"}
ALL_KINDS = OI_KINDS | EXT_KINDS


def _span_id(rec) -> str:
    return content_hash({"dev": rec["dev"], "seq": rec["seq"]})[2:]


def export(records: list[dict]) -> dict:
    trace_id = content_hash({"dev": records[0]["dev"], "run": records[0]["prev"]})[2:].ljust(32, "0")
    root = "T%s" % trace_id[:8]
    spans = []
    for rec in records:
        b, t = rec["body"], rec["type"]
        if t == "cell.tick":
            kind, name = b["kind"], b["cell"]
            inp, out = b.get("in"), b.get("out")
            if inp is None:
                inp = json.dumps({k: b[k] for k in ("frames_in", "units") if k in b}, sort_keys=True)
            if out is None:
                out = json.dumps({k: b[k] for k in ("frames_out", "words") if k in b}, sort_keys=True)
        elif t == "route.hop":
            kind, name = "CHAIN", "%s->%s" % (b["credit"]["cell"], b["debit"]["cell"])
            inp = "%s %s" % (b["credit"]["amount"], b["credit"]["units"])
            out = "%s %s" % (b["debit"]["amount"], b["debit"]["units"])
        else:
            kind, name = "CHAIN", "ledger.transaction"
            inp, out = b["route"], b.get("transcript", "")
        bud = b.get("budget", b.get("total_budget"))
        sid = _span_id(rec)
        attrs = {
            "openinference.span.kind": kind,
            "input.value": inp, "output.value": out,
            "activelog.type": t, "activelog.dev": rec["dev"], "activelog.seq": rec["seq"],
            "activelog.prev": rec["prev"],
        }
        if bud:
            attrs.update({"activeledger.budget.wall_ms": bud["wall_ms"], "activeledger.budget.usd": bud["usd"],
                          "activeledger.budget.power_w": bud["power_w"], "activeledger.budget.mem_mb": bud["mem_mb"],
                          "activeledger.budget.reqs": bud["reqs"],
                          "activeledger.budget.storage_prod": bud["storage_bytes"]["prod"],
                          "activeledger.budget.storage_train": bud["storage_bytes"]["train"],
                          "activeledger.budget.tokens": canon(bud["tokens"])})
        if "confidence" in b:
            attrs["activeledger.confidence"] = b["confidence"]
        if "load" in b:
            attrs["activeledger.load"] = b["load"]
        spans.append({"trace_id": trace_id, "span_id": sid, "name": name, "start_mono": rec["mono"],
                      "end_mono": rec["mono"], "dotted_order": "%s.%06d-%s" % (root, rec["mono"], sid),
                      "attributes": attrs})
    return {"resource": {"service.name": "activeledger", "activelog.alv": 1}, "spans": spans}


def span_kinds(projection: dict) -> list[str]:
    return [s["attributes"]["openinference.span.kind"] for s in projection["spans"]]
