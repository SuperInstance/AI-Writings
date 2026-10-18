#!/usr/bin/env python3
"""recorder.py — turn a manager↔crew situation into a hash-chained transcript.

The fleet's real product is not only the repos a crew ships; it is the
*recorded inputs and outputs of the manager↔crew system* — a decomposable
corpus so a future model can learn to do what the manager does: take a
compound thing apart, locate where the value/truth lives, recombine. See
situations/arch/INTER-RELATIONAL-INTELLIGENCE.md for the why.

This is that capture unit, made small and reusable. One SITUATION is one
manager+crew mission (a dispatch). Its transcript is an append-only JSONL
receipt ledger — the SAME idiom github.com/SuperInstance/MicroMoth-quilt uses
for quantum circuits: every line a cell, chained, replayable. The v0 hash
algebra here was byte-compatible with that repo's tools/collapse_ledger.py on
purpose (one fewer idiom to invent; one more relationship made explicit
between two cells of the fleet).

ATTESTABLE, NOT TAMPER-EVIDENT. The chain re-derives, so an edit is expensive
and a naive edit is named — that is one leg of the three an anchor needs. The
head is not signed, and no head is published where the writer does not
control it. So a re-chained rewrite verifies perfectly, and a TRUNCATED chain
is a SHORTER VALID CHAIN: drop the last 50 records of a 121-record transcript
and verify() returns ok on the remaining 71. Nothing but an external anchor
fixes that. See sign_head() below and the house vocabulary in
github.com/SuperInstance/witness-spec SPEC.md ("Linkage class" and
"Tamper-evidence — the three legs").

Each line is a RELATION-record (the graph edges are its `refs`):

    envelope: sid, seq, ts, actor{tier,id,session}, rel, refs[], hash
    rel ∈ TASK ROUTE DRAFT DRAW FOLD KEEP DROP MARK OUTCOME

Zero dependencies (Python stdlib only), like micromoth.py. Run it directly for
a self-test that builds a demo situation and re-verifies the whole chain:

    python3 recorder.py            # -> writes example_situation.jsonl, verifies, prints OK
"""

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


# ── witness-chain/1 ────────────────────────────────────────────────────────
#
# The chain rule was upgraded. The old one is witness-chain/0 and is still
# READ and VERIFIED, because a log that cannot verify its own history is a
# lie about the past. New records are witness-chain/1.
#
#   v0:  hash = fnv1a64(json.dumps({prev, **envelope}, sort_keys=True,
#                                 separators=(",", ":")))
#   v1:  leaf(i) = SHA256(0x00 || JCS(record_i))
#        hash(i) = SHA256(0x01 || hash(i-1) || leaf(i))
#
# THREE REASONS, and the third is the important one.
#
# 1. RFC 8785 (JCS) instead of a house convention. The v0 canonicalisation
#    was json.dumps(sort_keys=True), reimplemented by hand in every port.
#    It is not a standard, and it DIVERGES from JCS in three measured ways:
#      * 1.0 -> "1.0" in v0, "1" in JCS (ECMAScript Number::toString)
#      * keys are sorted by CODE POINT in Python and by UTF-16 CODE UNIT in
#        JCS, so they disagree for any key above U+FFFF against one below
#      * Python's ensure_ascii escapes non-ASCII; JCS does not
#    RFC 8785 is a MUST in A2A v1.0 8.4.1, so this is interoperability too.
#
# 2. DOMAIN SEPARATION (RFC 6962 2.1): a leaf hashes with a 0x00 prefix and
#    a node with 0x01, so the two kinds of thing cannot be confused.
#
# 3. THE ONE THAT MATTERS: v0 HAD NO TAMPER-EVIDENCE.
#    A hash chain is SELF-CONSISTENT, and self-consistency is not
#    tamper-evidence. Rewrite a record, re-chain it, and the chain still
#    verifies -- because the attacker recomputed it. v0 also used FNV-1a-64,
#    which is 64 bits and not collision-resistant, so an attacker rewriting
#    a chain does not need to collide anything.
#    Tamper-evidence needs an anchor OUTSIDE the log: a SIGNED TREE HEAD,
#    signed under a key the log writer does not hold (RFC 6962 / Trillian's
#    LogWitness). See sign_head()/verify_head() below.
#
# The key must NOT be the log writer's key, or the writer can re-sign and
# there is no anchor. HMAC-SHA256 is used here because it is in both the
# Python and the JavaScript standard libraries; it is a STAND-IN, not a
# signature, because it is symmetric -- it proves "someone with the key
# wrote it", not "who". Ed25519 is the production answer.

CHAIN_VERSION = "witness-chain/1"
CHAIN_V1 = "witness-chain/1"
CHAIN_V0 = "witness-chain/0"

_LEAF_PREFIX = b"\x00"
_NODE_PREFIX = b"\x01"
_HEAD_PREFIX = b"\x03"


def _jcs_key(s: str) -> bytes:
    """Sort key: the key's UTF-16 code units, as bytes.

    JCS sorts object keys by UTF-16 CODE UNITS. Python's sorted() sorts by
    CODE POINT. They disagree for any key above U+FFFF against one below:

        "\U00010000"  code point 0x10000, UTF-16 lead unit 0xD800
        "\ue000"      code point 0xE000,  UTF-16 unit      0xE000

    Python's sorted() puts \ue000 first (0xE000 < 0x10000). UTF-16 puts
    \U00010000 first (0xD800 < 0xE000). So a chain hashed in Python and a
    chain hashed in JavaScript would diverge on any object carrying both
    kinds of key -- silently, and only on the keys that matter least.
    """
    return s.encode("utf-16-be", "surrogatepass")


_JCS_ESCAPES = {
    "\b": "\\b", "\t": "\\t", "\n": "\\n", "\f": "\\f", "\r": "\\r",
    '"': '\\"', "\\": "\\\\",
}


def _jcs_string(s: str) -> str:
    out = ['"']
    for ch in s:
        if ch in _JCS_ESCAPES:
            out.append(_JCS_ESCAPES[ch])
        elif ord(ch) < 0x20:
            out.append("\\u%04x" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _shortest_digits(v: float):
    """The shortest round-trip digits of a positive finite double.

    Returns (s, k, n) with value == s * 10**(n-k), 10**(k-1) <= s < 10**k,
    and k as small as possible. ECMA-262 6.1.6.1.20.
    """
    r = repr(v)                       # shortest round-trip, Python's layout
    if "e" in r or "E" in r:
        mant, _, exp = r.replace("E", "e").partition("e")
        exp = int(exp)
    else:
        mant, exp = r, 0
    ip, _, fp = mant.partition(".")
    digits = ip + fp
    n = len(ip) + exp                  # the decimal point sits after n digits
    stripped = digits.lstrip("0")
    n -= (len(digits) - len(stripped))
    digits = stripped.rstrip("0")
    if not digits:
        return ("0", 1, 1)
    return (digits, len(digits), n)


def _jcs_number(v: float) -> str:
    """ECMAScript Number::toString, exactly as RFC 8785 Appendix B wants.

    THE PREVIOUS VERSION OF THIS FUNCTION WAS WRONG, and it was wrong in the
    exact way the fleet's own witness-spec caught: it used Python's repr()
    with an exponent fix-up, and repr() is not ECMAScript's Number::toString.

    Three differences, each visible in RFC 8785 Appendix B:

      * the SHORTEST round-trip digits of a large integer are NOT the exact
        integer value. 295147905179352830000 is a double whose exact value
        is 295147905179352825856; ECMAScript prints the former.
      * the plain-decimal band is -6 < n <= 21, so 1e-6 prints as
        "0.000001", not "1e-06".
      * an exponent has NO leading zero: "9.999999999999997e-7".

    A chain is only worth its hash if the canonical form is the STANDARD
    one. The witness-spec conformance suite exists to catch exactly this,
    and it caught it here.
    """
    if v != v or v in (float("inf"), float("-inf")):
        raise ValueError("JCS: non-finite number")
    if v == 0:
        return "0"                      # -0 canonicalises to 0
    sign = "-" if v < 0 else ""
    s, k, n = _shortest_digits(abs(v))
    if k <= n <= 21:
        return sign + s + ("0" * (n - k))
    if 0 < n <= 21:
        return sign + s[:n] + "." + s[n:]
    if -6 < n <= 0:
        return sign + "0." + ("0" * (-n)) + s
    e = n - 1
    esign = "+" if e >= 0 else "-"
    head = s[0] if k == 1 else s[0] + "." + s[1:]
    return sign + head + "e" + esign + str(abs(e))


def _jcs(v) -> str:
    if v is None:
        return "null"
    if v is True:
        return "true"
    if v is False:
        return "false"
    if isinstance(v, str):
        return _jcs_string(v)
    if isinstance(v, int):
        # RFC 8785 s3.2.2.3 serializes a number as ECMAScript's
        # Number::toString -- that is, as the IEEE-754 DOUBLE. An integer
        # above 2^53 is not exactly representable as a double, so there is
        # no correct ECMAScript rendering OF THE VALUE: the only thing
        # ECMAScript can print is the value it would have ROUNDED TO.
        #
        # THIS IS NOT A COSMETIC EDGE. Python's json keeps an integer above
        # 2^53 EXACT through a round trip; JSON.parse in JavaScript cannot
        # represent it and rounds it to 9007199254740992. So the two
        # languages would hash the SAME logical record DIFFERENTLY -- and
        # 2^53+1 is not an I-JSON value, so RFC 8785 does not say which is
        # right. Found by cross-checking the two implementations against each
        # other for the first time.
        #
        # THE FIX IS NOT TO PICK A SIDE. A body that leaves the I-JSON range
        # must be REFUSED, so that the chain says "this cannot be hashed"
        # instead of quietly meaning something different in each language.
        if abs(v) > 9007199254740992:
            raise ValueError(
                "JCS: integer " + str(v) + " is outside the I-JSON range "
                "(+/- 2^53). It is not exactly representable as an IEEE-754 "
                "double, so ECMAScript's Number::toString -- which RFC 8785 "
                "requires -- has no correct rendering of it, and Python and "
                "JavaScript would canonicalize it differently. Refuse it "
                "rather than let two implementations disagree about what a "
                "record means. Store it as a string, or as a float, if the "
                "exact value matters.")
        return str(v)
    if isinstance(v, float):
        return _jcs_number(v)
    if isinstance(v, (list, tuple)):
        return "[" + ",".join(_jcs(x) for x in v) + "]"
    if isinstance(v, dict):
        keys = sorted(v.keys(), key=_jcs_key)
        return "{" + ",".join(_jcs_string(k) + ":" + _jcs(v[k]) for k in keys) + "}"
    raise TypeError("JCS: unsupported type " + type(v).__name__)


def _leaf_hash_v1(record: dict) -> str:
    body = {k: v for k, v in record.items() if k != "hash"}
    return "0x" + hashlib.sha256(_LEAF_PREFIX + _jcs(body).encode("utf-8")).hexdigest()


def _chain_hash_v1(prev: str, leaf: str) -> str:
    return "0x" + hashlib.sha256(
        _NODE_PREFIX + prev.encode("utf-8") + leaf.encode("utf-8")).hexdigest()


def sign_head(head: str, key: bytes) -> str:
    """The signed tree head -- the EXTERNAL ANANCHOR.

    Publish this somewhere the log writer does not control, and keep the key
    from the log writer. Without both, there is no anchor and no
    tamper-evidence, only a self-consistent chain.
    """
    return "0x" + hmac.new(key, _HEAD_PREFIX + head.encode("utf-8"), hashlib.sha256).hexdigest()


def verify_head(head: str, signature: str, key: bytes) -> bool:
    return hmac.compare_digest(sign_head(head, key), signature)



# -- RFC 8785 Appendix B: the COMPLETE number-serialization samples -------

# The value is reconstructed from its IEEE-754 hex, so the test is
# self-contained and exact.
#
# This list was ADDED because the previous canonicalisation -- Python's
# repr() with an exponent fix-up -- failed 10 of these 24. It is not a
# hypothetical: the house's own witness-spec caught it, and this file is
# the fleet's reference implementation.
#
# A conformance suite that lists only the cases it passes is decoration.
# These are ALL of them, asserted by COUNT, by hex, and by canonical form.
RFC8785_APPENDIX_B = [
    ("0000000000000000", "0"),
    ("8000000000000000", "0"),
    ("0000000000000001", "5e-324"),
    ("8000000000000001", "-5e-324"),
    ("7fefffffffffffff", "1.7976931348623157e+308"),
    ("ffefffffffffffff", "-1.7976931348623157e+308"),
    ("4340000000000000", "9007199254740992"),
    ("c340000000000000", "-9007199254740992"),
    ("4430000000000000", "295147905179352830000"),
    ("44b52d02c7e14af5", "9.999999999999997e+22"),
    ("44b52d02c7e14af6", "1e+23"),
    ("44b52d02c7e14af7", "1.0000000000000001e+23"),
    ("444b1ae4d6e2ef4e", "999999999999999700000"),
    ("444b1ae4d6e2ef4f", "999999999999999900000"),
    ("444b1ae4d6e2ef50", "1e+21"),
    ("3eb0c6f7a0b5ed8c", "9.999999999999997e-7"),
    ("3eb0c6f7a0b5ed8d", "0.000001"),
    ("41b3de4355555553", "333333333.3333332"),
    ("41b3de4355555554", "333333333.33333325"),
    ("41b3de4355555555", "333333333.3333333"),
    ("41b3de4355555556", "333333333.3333334"),
    ("41b3de4355555557", "333333333.33333343"),
    ("becbf647612f3696", "-0.0000033333333333333333"),
    ("43143ff3c1cb0959", "1424953923781206.2"),
]


def _check_rfc8785() -> None:
    """Assert this implementation matches RFC 8785 Appendix B, in full."""
    import struct
    assert len(RFC8785_APPENDIX_B) == 24, (
        "RFC 8785 Appendix B has 24 numeric samples; this list has "
        + str(len(RFC8785_APPENDIX_B))
        + ". A truncated list is how the last bug hid.")
    for hexbits, want in RFC8785_APPENDIX_B:
        value = struct.unpack(">d", bytes.fromhex(hexbits))[0]
        got = _jcs(value)
        assert got == want, (
            "JCS disagrees with RFC 8785 Appendix B at " + hexbits
            + ": got " + repr(got) + " want " + repr(want))

    # THE I-JSON BOUNDARY, and the refusal that enforces it. Without this
    # check the behaviour is UNTESTED, and an untested refusal is a
    # comment: the next person to touch _jcs() would not know it was there.
    #
    # 2^53 is INSIDE the range and must canonicalize normally.
    assert _jcs(9007199254740992) == "9007199254740992", "2^53 is representable and must canonicalize"
    assert _jcs(-9007199254740992) == "-9007199254740992", "-2^53 likewise"
    # 2^53+1 is OUTSIDE it, and must be refused rather than canonicalized.
    for bad in (9007199254740993, -9007199254740993, 10 ** 30):
        try:
            got = _jcs(bad)
        except ValueError:
            continue
        raise AssertionError(
            "JCS accepted the out-of-range integer " + str(bad) + " and "
            "canonicalized it to " + repr(got) + ". Two implementations "
            "would disagree about that record and no spec says which is "
            "right. It must be refused.")
    # A bool is an int in Python, and must NOT be refused.
    assert _jcs(True) == "true" and _jcs(False) == "false"


GENESIS = "0x0000000000000000"
REL_TYPES = {"TASK", "ROUTE", "DRAFT", "DRAW", "FOLD", "KEEP", "DROP", "MARK", "OUTCOME"}


def fnv1a64(s: str) -> int:
    """fnv1a-64 over utf-8 — the fleet WAL convention (matches MicroMoth-quilt)."""
    h = 0xCBF29CE484222325
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * 0x100000001B3) & 0xFFFFFFFFFFFFFFFF
    return h


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Situation:
    """An append-only, hash-chained transcript of one manager↔crew mission.

    The chain rule mirrors MicroMoth-quilt's cell id: each record's `hash` is
    a commitment over the previous record's hash and this record's body. So
    the transcript is replayable: recompute the chain from the bodies and it
    must reproduce every hash, or a record was edited or reordered.

    That is RE-DERIVATION (leg 1 of 3), and it is what "chain-intact" means.
    It is not tamper-evidence: an attacker who recomputes the chain over their
    own edit re-derives perfectly, and a truncated transcript is a shorter
    valid chain. See the module docstring.
    """

    def __init__(self, sid: str, ts=None):
        self.sid = sid
        self.records: list[dict] = []
        self._clock = ts  # optional callable for deterministic timestamps (tests)

    # --- core ---------------------------------------------------------------

    def emit(self, rel: str, actor: dict, body: dict, refs=None) -> dict:
        """Append one relation-record and return it (with its computed hash)."""
        if rel not in REL_TYPES:
            raise ValueError("unknown rel %r (allowed: %s)" % (rel, sorted(REL_TYPES)))
        if not isinstance(actor, dict) or "tier" not in actor:
            raise ValueError("actor must be a dict with at least a 'tier' key")
        prev = self.records[-1]["hash"] if self.records else GENESIS
        rec = {
            "v": CHAIN_VERSION,
            "sid": self.sid,
            "seq": len(self.records),
            "ts": (self._clock() if self._clock else _now()),
            "actor": actor,
            "rel": rel,
            "refs": list(refs or []),
            "body": body,
        }
        rec["hash"] = _chain_hash_v1(prev, _leaf_hash_v1(rec))
        self.records.append(rec)
        return rec

    # --- typed convenience verbs (the inter-relational primitives) ----------

    def task(self, actor, brief, refs=None):
        return self.emit("TASK", actor, {"brief": brief}, refs)

    def route(self, actor, subtask, to, why, refs=None):
        return self.emit("ROUTE", actor, {"subtask": subtask, "to": to, "why": why}, refs)

    def draft(self, actor, prompt, response, params=None, refs=None):
        return self.emit("DRAFT", actor,
                         {"prompt": prompt, "response": response, "params": params or {}}, refs)

    def draw(self, actor, request, value, receipt, refs=None):
        """An un-gameable draw. `receipt` carries provenance: a Moth Bell-S, OR a
        MicroMoth-quilt collapse-ledger id when drawing locally in-environment."""
        return self.emit("DRAW", actor,
                         {"request": request, "value": value, "receipt": receipt}, refs)

    def fold(self, actor, claim, leaves, refs=None):
        """The decomposition record. `leaves` is a list of {claim, verdict}. We store
        the located weakest (argmin) and the GAP the single number would have hidden —
        the datum that teaches how much a scalar verdict smoothed over."""
        if not leaves:
            raise ValueError("fold needs at least one leaf")
        verdicts = [float(l["verdict"]) for l in leaves]
        argmin = min(range(len(leaves)), key=lambda i: verdicts[i])
        folded = min(verdicts)  # the weakest leaf is the honest ceiling of the conjunction
        whole = None
        for l in leaves:
            if l.get("is_whole"):
                whole = float(l["verdict"])
        body = {
            "claim": claim,
            "leaves": leaves,
            "weakest_index": argmin,
            "weakest_claim": leaves[argmin].get("claim"),
            "folded_min": folded,
            "whole_verdict": whole,
            "gap": (None if whole is None else round(folded - whole, 6)),
        }
        return self.emit("FOLD", actor, body, refs)

    def keep(self, actor, candidate_ref, reason, refs=None):
        r = list(refs or [])
        if candidate_ref not in r:
            r.append(candidate_ref)
        return self.emit("KEEP", actor, {"candidate": candidate_ref, "reason": reason}, r)

    def drop(self, actor, candidate_ref, reason, refs=None):
        r = list(refs or [])
        if candidate_ref not in r:
            r.append(candidate_ref)
        return self.emit("DROP", actor, {"candidate": candidate_ref, "reason": reason}, r)

    def mark(self, actor, kind, ref, refs=None):
        """A durable artifact written (commit sha / doc path / receipt id)."""
        return self.emit("MARK", actor, {"kind": kind, "ref": ref}, refs)

    def outcome(self, actor, of_ref, result, detail=None, refs=None):
        """A realized downstream result (CI green/red, revert, measured speedup) —
        the delayed label. `of_ref` points back at the record it judges."""
        r = list(refs or [])
        if of_ref not in r:
            r.append(of_ref)
        return self.emit("OUTCOME", actor, {"of": of_ref, "result": result, "detail": detail}, r)

    # --- persistence + verification ----------------------------------------

    def to_jsonl(self) -> str:
        return "".join(_canon(r) + "\n" for r in self.records)

    def write(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(self.to_jsonl(), encoding="utf-8")
        return path


def _envelope(rec: dict) -> dict:
    """The record without its own hash — what the chain commits to."""
    return {k: v for k, v in rec.items() if k != "hash"}


def verify(records) -> tuple[bool, str]:
    """Replay the chain. Returns (ok, message). Catches reorder, edit, and drop.

    BOTH chain versions are accepted, and a chain that MIXES them is a
    FAILURE, not a convenience:

      witness-chain/0  fnv1a64 over a house-convention canonical form
      witness-chain/1  SHA-256, RFC 8785 canonicalisation, RFC 6962 domain
                       separation

    The version is a field INSIDE the record, so it is inside the hashed
    bytes: you cannot strip or downgrade a version without breaking the
    chain. That is why a mixed chain is detectable.

    What this does NOT do: it does not detect an edit that the writer
    RE-CHAINED. A chain is self-consistent, and self-consistency is not
    tamper-evidence. For that you need the signed tree head -- sign_head()
    and verify_head() -- published somewhere the writer does not control.
    """
    prev = GENESIS
    seen_version = None
    for i, rec in enumerate(records):
        if rec.get("seq") != i:
            return False, "seq gap at index %d (got %r)" % (i, rec.get("seq"))
        version = rec.get("v")
        if version is None:
            version = CHAIN_V0
        if seen_version is None:
            seen_version = version
        elif version != seen_version:
            return False, ("MIXED CHAIN VERSIONS at seq %d: %s then %s -- a chain "
                           "does not change its rule mid-flight; start a new "
                           "transcript and name the previous head in it"
                           % (i, seen_version, version))
        if version == CHAIN_V1:
            want = _chain_hash_v1(prev, _leaf_hash_v1(rec))
        else:
            want = "0x%016x" % fnv1a64(_canon({"prev": prev, **_envelope(rec)}))
        if rec.get("hash") != want:
            return False, "hash mismatch at seq %d: stored %s want %s" % (
                i, rec.get("hash"), want)
        for ref in rec.get("refs", []):
            if isinstance(ref, str) and ref.startswith("0x") and ref not in {
                    r["hash"] for r in records[:i]}:
                return False, "seq %d refs unknown/forward hash %s" % (i, ref)
        prev = rec["hash"]
    # "chain-intact" means precisely THE CHAIN VERIFIED. It is not a claim
    # about tampering: this same function returns ok for a tail-truncated
    # chain, because a prefix of a valid chain is a valid chain. Leg 1 of 3
    # only -- re-derived, not anchored. See the module docstring.
    return True, ("ok: %d records, chain-intact (%s) "
                  "[leg 1 of 3: re-derived, not anchored -- not tamper-evident]"
                  % (len(records), seen_version or CHAIN_V0))


def head(records) -> str:
    """The chain head -- what gets signed."""
    return records[-1]["hash"] if records else GENESIS


def load(path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line]


# --- self-test / demo -------------------------------------------------------

def _demo() -> Situation:
    """Build a small but real-shaped situation: a captain routes a claim-check to a
    crew member, draws an adversary locally (MicroMoth-quilt), folds the crew's
    compound claim through the referee, drops it on the located weakest leaf, and
    books the scar. Deterministic timestamps so the demo file is reproducible."""
    ticks = iter(["2026-09-29T05:20:%02dZ" % s for s in range(0, 40, 3)])
    s = Situation("sit-demo-0001", ts=lambda: next(ticks))
    disp = {"tier": "dispatcher", "id": "opus-4.8", "session": "parent"}
    cap = {"tier": "captain", "id": "opus-5.5", "session": "fresh-01"}
    crew = {"tier": "crew", "id": "deepseek-chat", "session": "fresh-01"}
    ref = {"tier": "referee", "id": "jev-latest", "session": "fresh-01"}
    dice = {"tier": "dice", "id": "micromoth-quilt/bell", "session": "fresh-01"}

    t = s.task(disp, "Verify the crew's anatomy claim before it lands in a README.")
    r = s.route(cap, "fact-check compound claim", to="deepseek-chat",
                why="cheap hauler; captain reserves judgment for the fold", refs=[t["hash"]])
    d = s.draft(crew,
                prompt="State four facts about the human heart.",
                response=("four chambers; pumps blood; contains the SA node; "
                          "located entirely on the left side of the chest"),
                refs=[r["hash"]])
    dr = s.draw(dice, request="draw adversary leaf index in [0,4)",
                value=3,
                receipt={"collapse_ledger": "0x… (micromoth-quilt bell, local, no network)",
                         "note": "un-gameable in-env: quantum-shaped, nobody steered it"},
                refs=[d["hash"]])
    f = s.fold(ref,
               claim="the heart claim (compound)",
               leaves=[
                   {"claim": "the compound claim as a whole", "verdict": 0.11, "is_whole": True},
                   {"claim": "four chambers", "verdict": 0.98},
                   {"claim": "pumps blood through the body", "verdict": 0.97},
                   {"claim": "contains the SA node that sets rhythm", "verdict": 0.95},
                   {"claim": "located entirely on the left side of the chest", "verdict": 0.08},
               ],
               refs=[d["hash"], dr["hash"]])
    dp = s.drop(cap, candidate_ref=d["hash"],
                reason=("fold located the rot at leaf 3 (left-side), the same leaf the "
                        "un-gameable draw hit; whole-verdict 0.11 hid WHERE — gap %.2f"
                        % f["body"]["gap"]),
                refs=[f["hash"]])
    m = s.mark(cap, kind="ledger", ref="dispatch-ledger.csv#d121", refs=[dp["hash"]])
    s.outcome(disp, of_ref=m["hash"], result="scar-booked",
              detail="claim kept OUT of the README; transcript retained as a FOLD example",
              refs=[f["hash"]])
    return s


def main(argv=None):
    ap = argparse.ArgumentParser(description="situation-recorder self-test / verifier")
    ap.add_argument("--verify", metavar="PATH", help="verify an existing transcript JSONL")
    ap.add_argument("--out", default=str(Path(__file__).with_name("example_situation.jsonl")),
                    help="where the demo writes its transcript")
    args = ap.parse_args(argv)

    if args.verify:
        ok, msg = verify(load(args.verify))
        print(("VERIFY OK  — " if ok else "VERIFY FAIL — ") + msg)
        return 0 if ok else 1

    _check_rfc8785()
    print("RFC 8785 Appendix B: all 24 samples match")

    s = _demo()
    path = s.write(args.out)
    ok, msg = verify(s.records)
    assert ok, msg
    # naive-edit check: flipping one field must break the chain downstream.
    # NAIVE -- an attacker who recomputes the chain over their own edit
    # passes this, which is the limit the next block demonstrates.
    bad = load(path)
    bad[3]["body"]["value"] = 0
    tampered_ok, _ = verify(bad)
    assert not tampered_ok, "tamper went undetected — chain is not doing its job"
    print("wrote %s (%d records)" % (path, len(s.records)))
    print(msg)
    print("re-derivation: editing seq 3 breaks verification ✓ (a naive edit)")

    # ── the honest limits, demonstrated ────────────────────────────────────
    #
    # A chain is SELF-CONSISTENT. An attacker who edits a record and
    # RE-CHAINS it produces a chain that verifies perfectly -- and the
    # difference between "nobody touched this" and "somebody rewrote the
    # whole thing" is INVISIBLE without an anchor outside the log.
    #
    # This is the defect the old rule (witness-chain/0) had, and it is worth
    # being able to SHOW rather than assert.
    key = b"a-key-the-log-writer-does-not-hold"
    good = load(path)
    sig = sign_head(head(good), key)

    forged = load(path)
    forged[3]["body"]["value"] = 0
    # The attacker recomputes the chain over their own edit -- and must also
    # re-point every `refs` entry that names a hash they changed, because
    # verify() checks refs against the hashes of EARLIER records. Re-pointing
    # a ref changes a record's body, which changes its hash, which cascades.
    # So the attack is a FIXPOINT, and this iterates it to convergence.
    #
    # (A first attempt that only re-chained, without re-pointing refs, was
    # caught -- by the refs check. That is a SECOND layer of detection, and
    # it is worth knowing about, but it is not the same as tamper-evidence:
    # it is only as good as the attacker's care. The signed head does not
    # depend on the attacker's competence.)
    for _ in range(16):
        before = [r["hash"] for r in forged]
        prev = GENESIS
        for r in forged:
            r["hash"] = _chain_hash_v1(prev, _leaf_hash_v1(r))
            prev = r["hash"]
        remap = {before[i]: forged[i]["hash"] for i in range(len(forged))}
        changed = False
        for r in forged:
            for j, ref in enumerate(r.get("refs", [])):
                if isinstance(ref, str) and ref in remap and remap[ref] != ref:
                    r["refs"][j] = remap[ref]
                    changed = True
        if not changed:
            break
    forged_ok, forged_msg = verify(forged)
    print("RE-CHAINED rewrite verifies?           %s  (%s)" % (forged_ok, forged_msg))
    print("  -> a chain alone CANNOT tell. The witness log is self-consistent,")
    print("     not tamper-evident. That was true of witness-chain/0 too.")
    anchored_ok = verify_head(head(forged), sig, key)
    print("RE-CHAINED rewrite caught by the signed head? %s" % (not anchored_ok))
    assert forged_ok, "expected a re-chained rewrite to still verify -- if this fails, the demo is not showing the real limit"
    assert not anchored_ok, "the signed head did NOT catch a re-chained rewrite -- the anchor is broken"
    print("with a signed head, a re-chained rewrite is CAUGHT ✓")
    print("  NOTE: that is legs 1+2. It is NOT yet tamper-evident -- the head")
    print("  must also be PUBLISHED where the writer cannot control it, and")
    print("  no such publication exists in this repo. Until it does, the")
    print("  honest word is 'attestable'. A signed head stored inside the log")
    print("  it anchors can be refreshed for free after any rewrite.")
    w = s.records[4]["body"]
    print("demo FOLD located weakest = leaf %d (%r), gap vs whole = %s"
          % (w["weakest_index"], w["weakest_claim"], w["gap"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
