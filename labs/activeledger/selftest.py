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

# ---- playtest hardening (PLAYTEST-REPORT.md) ----------------------------------------------
check("PT: add_budget('' + 'local') has no leading '+' (precedence bug: `-` bound tighter than `|`)",
      A.add_budget(A.budget(reqs=""), A.budget(reqs="local"))["reqs"] == "local"
      and A.add_budget(A.budget(reqs="net"), A.budget(reqs="local"))["reqs"] == "local+net")
check("PT: budget_ok rejects inf / NaN / bool fields (they hash as non-JSON or as 1)",
      not any(A.budget_ok(b) for b in (A.budget(usd=float("inf")), A.budget(usd=float("nan")),
                                       A.budget(tokens={"a": True}), A.budget(wall_ms=True), A.budget(mem_mb=float("inf")))))
try:
    A.canon({"a": float("nan")}); nan_loud = False
except ValueError:
    nan_loud = True
check("PT: canon() refuses NaN/Infinity instead of emitting non-JSON", nan_loud)
check("PT: verify_chain / validate_envelope treat non-dict records as invalid (was TypeError)",
      A.verify_chain([1]) is False and A.verify_chain([None]) is False and A.verify_chain([]) is True)
import lzma as _lzma
import random as _random
_mk = A.ActiveLog("pt")
for _i in range(30):
    _mk.emit("cell.tick", {"c": "cell%d" % (_i % 3), "n": _i * 5, "f": _i / 3, "s": "hello%d" % (_i % 4), "ok": _i % 2 == 0, "l": [_i, "x"],
                           "budget": A.budget()})
_recs, _pay, _head = _mk.records, AR._payload(_mk.records, 0), AR._head(_mk.records)
_rng, _kinds, _wrong = _random.Random(3), set(), 0
for _t in range(400):
    _b = bytearray(_pay)
    for _ in range(_rng.choice((1, 1, 2, 5))):
        _op, _p = _rng.random(), _rng.randrange(len(_b))
        if _op < .6:
            _b[_p] = _rng.randrange(256)
        elif _op < .8:
            del _b[_p:_p + _rng.randrange(1, 5)]
        else:
            _b[_p:_p] = bytes(_rng.randrange(256) for _ in range(_rng.randrange(1, 4)))
    try:
        _o = AR.unpack(b"ALR1\x00" + _head + _lzma.compress(bytes(_b)))
        _wrong += A.canon(_o) != A.canon(_recs)
    except AR.AtRestError:
        pass
    except Exception as _e:                     # old code: ~60% of mutations escaped as IndexError/JSONDecodeError/UnicodeDecodeError
        _kinds.add(type(_e).__name__)
check("PT: 400 structurally-mutated payloads (valid lzma) only ever raise AtRestError (was IndexError/JSONDecodeError/UnicodeDecodeError)", not _kinds)
check("PT: ...and never silently return different records", _wrong == 0)
def _atrest_err(f):
    try:
        f()
    except AR.AtRestError:
        return True
    except Exception:
        return False
    return False
check("PT: pack([]) / pack_many with an empty run -> AtRestError (was IndexError)",
      _atrest_err(lambda: AR.pack([])) and _atrest_err(lambda: AR.pack_many([[], _recs])))
check("PT: a blob that is only the 4-byte magic -> AtRestError (was IndexError)",
      _atrest_err(lambda: AR.unpack(b"ALR1")) and _atrest_err(lambda: AR.unpack_many(b"ALRM")))
check("PT: trailing bytes after the lzma stream are refused", _atrest_err(lambda: AR.unpack(AR.pack(_recs) + b"\x00")))
_old = AR.MAX_PAYLOAD
AR.MAX_PAYLOAD = 1000
check("PT: decompressed payload over MAX_PAYLOAD is refused (lzma-bomb guard)",
      _atrest_err(lambda: AR.unpack(b"ALR1\x00" + _head + _lzma.compress(b"\x00" * 5000))))
AR.MAX_PAYLOAD = _old
_rb = AR.pack(_recs, repair=True)
def _flip(n, seed):
    r, b = _random.Random(seed), bytearray(_rb)
    for _ in range(n):
        b[r.randrange(5, len(b))] ^= 1 << r.randrange(8)      # skip magic+flags (those are not RS-protected)
    return bytes(b)
_rec1 = all(A.canon(AR.unpack(_flip(1, k))) == A.canon(_recs) for k in range(20))
_wr = 0
for _k in range(20):
    try:
        _wr += A.canon(AR.unpack(_flip(100, _k))) != A.canon(_recs)
    except AR.AtRestError:
        pass
    except Exception:
        _wr += 1
check("PT: RS-protected blob: 1 flipped bit always recovers; 100 flips either recover or raise AtRestError, never wrong/other", _rec1 and _wr == 0)

print("activeledger selftest: %d checks, %d failures" % (checks, fails))
sys.exit(1 if fails else 0)
