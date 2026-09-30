"""activeledger selftest — offline, deterministic."""

from __future__ import annotations

import copy
import json
import sys

import activeledger as A
import otel_export as O
import route_sim as R

checks = fails = 0


def check(name, ok):
    global checks, fails
    checks += 1
    if not ok:
        fails += 1
    print(("  ok  : " if ok else "  FAIL: ") + name)


f = R.run(use_filter=True)
n = R.run(use_filter=False)
recs = f["log"].records

check("every record is a valid ActiveLog v1 envelope", all(A.validate_envelope(r) for r in recs))
check("only the three namespaced types are used", {r["type"] for r in recs} == set(A.TYPES))
check("prev-chain verifies on an untouched run", A.verify_chain(recs))

t = copy.deepcopy(recs); t[2]["body"]["confidence"] = 0.0
check("prev-chain detects a tampered body", not A.verify_chain(t))
t = copy.deepcopy(recs); del t[3]
check("prev-chain detects a deleted record", not A.verify_chain(t))
t = copy.deepcopy(recs); t[1], t[2] = t[2], t[1]
check("prev-chain detects reordered records", not A.verify_chain(t))

hops = [r for r in recs if r["type"] == "route.hop"]
check("every route.hop sums to zero after translation", bool(hops) and all(A.hop_balanced(h["body"]) for h in hops))
bad = copy.deepcopy(hops[0]["body"]); bad["debit"]["amount"] += 1
check("an unbalanced hop is detected", not A.hop_balanced(bad))
try:
    A.ActiveLog().emit("route.hop", {**bad, "budget": A.budget()}); rejected = False
except ValueError:
    rejected = True
check("emit refuses an unbalanced route.hop", rejected)

fl, nl = f["stt_load"], n["stt_load"]
check("pre-filter reduces recorded STT load (%d -> %d frames, -%.0f%%)" % (nl, fl, 100 * (nl - fl) / nl), fl < nl)
stt = lambda run: next(r for r in run["log"].records if r["body"].get("cell") == "stt")["body"]
check("STT wall_ms and power_w drop with the filter",
      stt(f)["budget"]["wall_ms"] < stt(n)["budget"]["wall_ms"] and stt(f)["budget"]["power_w"] < stt(n)["budget"]["power_w"])
check("filter does not change the product (same transcript)", f["transcript"] == n["transcript"] == "Turn on the lights.")
check("every cell.tick records a confidence and a load metric",
      all("confidence" in r["body"] and "load" in r["body"] for r in recs if r["type"] == "cell.tick"))

check("every cell.tick and route.hop carries a well-formed budget vector",
      all(A.budget_ok(r["body"]["budget"]) for r in recs if r["type"] in ("cell.tick", "route.hop")))
for run in (f, n):
    tot = A.ZERO_BUDGET
    for r in run["log"].records:
        if r["type"] in ("cell.tick", "route.hop"):
            tot = A.add_budget(tot, r["body"]["budget"])
    check("route total budget == sum of its ticks+hops (%s)" % run["route"], tot == run["total_budget"] or
          A.canon(tot) == A.canon(run["total_budget"]))
check("total_budget is booked on the ledger.transaction", f["txn"]["body"]["total_budget"] == f["total_budget"])
check("ledger.transaction binds every tick and hop by content hash",
      len(f["txn"]["body"]["binds"]) == len(recs) - 1)

proj = O.export(recs)
kinds = O.span_kinds(proj)
check("OTel projection has one span per record", len(proj["spans"]) == len(recs))
check("OTel span kinds are within the OpenInference superset", set(kinds) <= O.ALL_KINDS)
want = {"microphone": "PHYSICAL", "prefilter": "FILTER", "stt": "TOOL", "cleanup": "FILTER", "llm": "LLM"}
got = {s["name"]: s["attributes"]["openinference.span.kind"] for s in proj["spans"] if s["attributes"]["activelog.type"] == "cell.tick"}
check("OTel projection round-trips the cell kinds", got == want)
check("dotted_order string-sorts into run order",
      [s["span_id"] for s in sorted(proj["spans"], key=lambda s: s["dotted_order"])] == [s["span_id"] for s in proj["spans"]])
check("input.value/output.value present on every span",
      all(s["attributes"].get("input.value") is not None and s["attributes"].get("output.value") is not None for s in proj["spans"]))

check("content hash is deterministic across runs", A.content_hash(recs) == A.content_hash(R.run(True)["log"].records))
check("run is byte-identical on re-run", f["log"].to_jsonl() == R.run(True)["log"].to_jsonl())
check("fnv1a-64 matches the fleet vector (empty string = offset basis)", A.fnv1a64("") == 0xCBF29CE484222325)
check("fnv1a-64 known vector 'a'", A.fnv1a64("a") == 0xAF63DC4C8601EC8C)
check("projection is JSON-serialisable", bool(json.dumps(proj)))

# ---- at_rest (ALR1): compact, repairable at-rest form (promoted from encoding-experiments E1+E2) ----
import at_rest as AR  # noqa: E402

blob = AR.pack(recs)
check("ALR1 unpack is canonically identical to the run", A.canon(AR.unpack(blob)) == A.canon(recs))
check("ALR1 recomputed prev-chain verifies", A.verify_chain(AR.unpack(blob)))
check("ALR1 is smaller than the JSONL", len(blob) < len(f["log"].to_jsonl().encode()))
tampered = [dict(r) for r in recs]
tampered[3] = dict(tampered[3], ts="det:999999")
try:
    AR.pack(tampered)
    refused = False
except AR.AtRestError:
    refused = True
check("ALR1 refuses to pack a run whose chain does not verify", refused)
bad = bytearray(blob)
bad[-8] ^= 0x40
try:
    AR.unpack(bytes(bad))
    caught = False
except (AR.AtRestError, Exception):
    caught = True
check("ALR1 (no repair) never returns different records from a flipped byte", caught)
rblob = bytearray(AR.pack(recs, repair=True))
for i in range(40, 40 + 64):  # a 64-byte burst inside the RS-protected body
    rblob[i] ^= 0xA5
check("ALR1+RS repairs a 64-byte burst exactly", A.canon(AR.unpack(bytes(rblob))) == A.canon(recs))

runs2 = [R.run(True)["log"].records, R.run(False)["log"].records]
arch = AR.pack_many(runs2)
check("ALRM multi-run archive round-trips every run", A.canon(AR.unpack_many(arch)) == A.canon(runs2))
check("ALRM archive of two runs is smaller than two ALR1 blobs", len(arch) < sum(len(AR.pack(r)) for r in runs2))

print("activeledger selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
