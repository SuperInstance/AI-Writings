"""system2-redesigner (B8) — the System-2 PROPOSER that closes the loop.

    propose  ->  B7 gate (product identity FIRST)  ->  B4 promote (iron-triangle preference map)
                                                         (ACTIVELEDGER-CELL-GRAPH.md §11, B8 row)

The slow cell. It never serves traffic. It takes a quilt that already has routes (here the
text-normalize quilt, EX4), collects ALTERNATIVE networks for the same request, and:

  1. PARSES each proposal into a tiny route language (ROUTE DSL below). A proposal that does
     not parse is refused at `parse` — it never runs.
  2. EXECUTES it on every case of a gate corpus (the quilt's own WORKLOAD + all 128 ASCII code
     points + a unicode trap set + seeded fuzz), emitting a real ActiveLog v1 run per case
     (cell.tick / route.hop / ledger.transaction, budget vector on every record).
  3. GATES it with B7, imported unmodified: `backtest.backtest_pair(reference, proposal)` per
     case, reference = the quilt's own FULL route (handles all input). ONE refused case refuses
     the proposal — a cheaper DIFFERENT answer is never ranked. A crash is a refusal too. The
     first counterexample (input, expected, got) is kept: refusals are documented dead-ends.
  4. PROMOTES the survivors with B4, imported unmodified: per-case `prefer()` (which re-runs the
     gate) feeds a hebbian PreferenceBook; `prefer_axes()` over the workload sums gives the
     frontier and `preferred_when` per priority. Frontier routes are PROMOTED (elite corners);
     gate-passing but dominated routes are kept as SATISFICE routes (§11.1: always a route standing).

Who proposes? Offline: the caller passes proposal dicts (the selftest's stubs). Live
(`--live`): a CHEAP-MODEL CREW on DeepInfra each proposes networks in the DSL; B8 conducts,
B7 judges. The crew supplies breadth; it has no say in the verdict.

ROUTE DSL — a proposal is a JSON object (a 2-branch network, nestable to depth 3):
    {"name": str, "guard": GUARD, "steps": [OP, ...], "fallback": "full" | <proposal>,
     "rationale": str (optional, ignored by the judge)}
  If the guard holds on the input, `steps` run left-to-right on the text; otherwise the
  fallback network runs ("full" = NFKC -> casefold -> unicode-ws-collapse, the reference).

Costs are a DETERMINISTIC COST MODEL (OP_COST/GUARD_COST, the same convention as the example
quilts) — not wall-clock measurements. Gate counts and verdicts are measured outputs.

Library:  parse(obj) -> proposal | raises Invalid
          execute(proposal, text) -> ActiveLog records
          gate(proposal, corpus) -> {"status": passed|refused, ...}
          promote(passed, corpus) -> preference map (B4)
          redesign(proposals) -> full report (gate + promote + tallies), report_hash
          crew_propose(models) -> (proposals, crew log)            # live only
CLI:      python3 system2_redesigner.py [--json]                   # offline: built-in stubs
          python3 system2_redesigner.py --live [--models a,b,c] [--moth] [--bold] [--out runs/x.json]
"""

from __future__ import annotations

import json
import os
import random
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
LABS = os.path.dirname(HERE)
for _p in ("activeledger", "system2-backtest", "route-preference",
           os.path.join("examples", "text-normalize-quilt"), "convo-quilt"):
    sys.path.insert(0, os.path.join(LABS, _p))

import activeledger as al  # noqa: E402
import backtest as bt  # noqa: E402          B7, unmodified
import route_preference as rp  # noqa: E402  B4, unmodified
import textnorm_quilt as tn  # noqa: E402    EX4, the quilt being redesigned

MAX_DEPTH = 3
MAX_STEPS = 8


class Invalid(Exception):
    """A proposal that does not parse into the route DSL."""


# ---- the route DSL -------------------------------------------------------------------

def _ascii_bytes(s: str) -> bytes:
    if not s.isascii():
        raise ValueError("bytes op on non-ASCII input")
    return s.encode("ascii")


_FS = bytes.maketrans(b"\x1c\x1d\x1e\x1f", b"    ")

OPS = {   # name -> str -> str. Bytes ops RAISE on non-ASCII (they lack the tooling).
    "nfkc": lambda s: unicodedata.normalize("NFKC", s),
    "nfc": lambda s: unicodedata.normalize("NFC", s),
    "nfkd": lambda s: unicodedata.normalize("NFKD", s),
    "casefold": lambda s: s.casefold(),
    "lower": lambda s: s.lower(),
    "ws_collapse": lambda s: " ".join(s.split()),
    "strip": lambda s: s.strip(),
    "map_fs_controls": lambda s: _ascii_bytes(s).translate(_FS).decode("ascii"),
    "bytes_lower": lambda s: _ascii_bytes(s).lower().decode("ascii"),
    "bytes_ws_collapse": lambda s: b" ".join(_ascii_bytes(s).split()).decode("ascii"),
    "const_empty": lambda s: "",
    "identity": lambda s: s,
}


def _clean_ascii(s: str) -> bool:
    """Already normalized and pure ASCII: no upper, no ws other than single inner spaces."""
    return s.isascii() and not any("A" <= c <= "Z" for c in s) and " ".join(s.split()) == s \
        and all(c == " " or not c.isspace() for c in s) and not any(c in s for c in "\x1c\x1d\x1e\x1f")


GUARDS = {
    "always": lambda s: True,
    "ascii": lambda s: s.isascii(),
    "latin1": lambda s: all(ord(c) < 256 for c in s),
    "blank": lambda s: not s.strip(),
    "clean_ascii": _clean_ascii,
}


def _b(wall, power, mem, prod, train):
    return al.budget(wall_ms=wall, power_w=power, mem_mb=mem, prod=prod, train=train)


# Deterministic cost model. Unicode tables are expensive to ship and to run; ASCII byte ops
# are tiny; a guard is a scan. Same scale as textnorm_quilt.COST.
OP_COST = {
    "nfkc": _b(2, 0.3, 4, 1536, 6144), "nfc": _b(2, 0.25, 3, 1024, 4096),
    "nfkd": _b(2, 0.3, 4, 1536, 6144), "casefold": _b(1, 0.1, 2, 512, 2048),
    "lower": _b(1, 0.05, 1, 64, 128), "ws_collapse": _b(1, 0.05, 1, 64, 128),
    "strip": _b(0, 0.01, 0, 8, 16), "map_fs_controls": _b(1, 0.02, 1, 16, 32),
    "bytes_lower": _b(1, 0.02, 1, 16, 32), "bytes_ws_collapse": _b(1, 0.02, 1, 16, 32),
    "const_empty": _b(0, 0.0, 0, 0, 0), "identity": _b(0, 0.0, 0, 0, 0),
}
GUARD_COST = {
    "always": _b(0, 0.0, 0, 0, 0), "ascii": _b(0, 0.01, 0, 8, 0),
    "latin1": _b(0, 0.01, 0, 8, 0), "blank": _b(1, 0.02, 0, 8, 16),
    "clean_ascii": _b(1, 0.02, 0, 16, 32),
}
EDGE_COST = _b(0, 0.01, 0, 8, 16)          # one route.hop between consecutive cells
FULL_STEPS = ["nfkc", "casefold", "ws_collapse"]


def parse(obj, depth: int = 1) -> dict:
    """Validate a proposal into canonical form. Raises Invalid — refused before it runs."""
    if obj == "full":
        return "full"
    if not isinstance(obj, dict):
        raise Invalid("proposal must be an object (or the string 'full' as a fallback)")
    if depth > MAX_DEPTH:
        raise Invalid("network nested deeper than %d" % MAX_DEPTH)
    name = obj.get("name") if depth == 1 else obj.get("name", "branch")
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9_.\-]{1,40}", name or ""):
        raise Invalid("name must match [A-Za-z0-9_.-]{1,40}, got %r" % (name,))
    guard = obj.get("guard", "always")
    if guard not in GUARDS:
        raise Invalid("unknown guard %r (allowed %s)" % (guard, sorted(GUARDS)))
    steps = obj.get("steps")
    if not isinstance(steps, list) or not steps or len(steps) > MAX_STEPS:
        raise Invalid("steps must be a list of 1..%d ops" % MAX_STEPS)
    bad = [s for s in steps if s not in OPS]
    if bad:
        raise Invalid("unknown op(s) %r (allowed %s)" % (bad, sorted(OPS)))
    fb = obj.get("fallback", "full")
    if guard == "always":
        fb = "full"                                 # unreachable; normalize away
    return {"name": name, "guard": guard, "steps": list(steps),
            "fallback": parse(fb, depth + 1)}


def shape_hash(p) -> str:
    """Content address of a network's SHAPE (name/rationale excluded) — dedupes the crew."""
    def strip(q):
        return q if q == "full" else {"guard": q["guard"], "steps": q["steps"],
                                      "fallback": strip(q["fallback"])}
    return al.content_hash(strip(p))


def describe(p) -> str:
    if p == "full":
        return "full"
    if p["guard"] == "always":
        return ">".join(p["steps"])
    return "%s ? %s : %s" % (p["guard"], ">".join(p["steps"]), describe(p["fallback"]))


# ---- execution: one ActiveLog run per (proposal, input) ---------------------------------

def execute(p, text: str, label: str | None = None) -> list[dict]:
    """Run network `p` on `text`, booking every cell. Product shape == textnorm_quilt.run's
    ledger.transaction ({"out": ...}) so B7 compares like with like. Raises on op failure."""
    label = label or (p if p == "full" else p["name"])
    log = al.ActiveLog(dev="system2-redesigner")
    rid = "s2:%s" % al.content_hash([label, text])
    total = al.ZERO_BUDGET
    prev_cell, s, cells = "request", text, 0

    def tick(cell, cost, **extra):
        nonlocal total
        log.emit("cell.tick", {"route": rid, "cell": cell, "kind": "SIM", "path": label,
                               "budget": cost, **extra})
        total = al.add_budget(total, cost)

    def hop(src, dst, n):
        nonlocal total
        h = al.DoubleEntry.translate(src, "chars", float(n), dst, "chars", 1.0, "text passes through")
        log.emit("route.hop", {"route": rid, **h.body(), "budget": EDGE_COST})
        total = al.add_budget(total, EDGE_COST)

    tick("request", tn.COST["cheap"]["tick"], units="chars", chars=len(text))
    node = p
    for _ in range(MAX_DEPTH + 1):
        if node == "full":
            steps = FULL_STEPS
            break
        g = "guard:%s" % node["guard"]
        hop(prev_cell, g, len(s)); prev_cell = g
        taken = GUARDS[node["guard"]](s)
        tick(g, GUARD_COST[node["guard"]], taken=taken)
        if taken:
            steps = node["steps"]
            break
        node = node["fallback"]
    for i, op in enumerate(steps):
        cell = "%d:%s" % (i, op)
        hop(prev_cell, cell, len(s)); prev_cell = cell
        s = OPS[op](s)
        tick(cell, OP_COST[op], out_hash=al.content_hash(s))
        cells += 1
    hop(prev_cell, "result", len(s))
    tick("result", tn.COST["cheap"]["tick"], value=s, units="chars")
    log.emit("ledger.transaction", {"route": rid, "path": label, "out": s, "total_budget": total})
    return log.records


def _product(records) -> str:
    return [r for r in records if r["type"] == "ledger.transaction"][0]["body"]["out"]


# ---- the gate corpus ------------------------------------------------------------------

TRAPS = ["Straße", "ẞIG", "ﬁne ﬀ ﬃ", "Ⅷ Ⅸ ⅻ", "ＡＢＣ１２３", "İstanbul", "ǅemal ǈ ǋ",
         "ΣΊΣΥΦΟΣ ς", "㎏ ㎒ ℃", "a b", "x　y", "p q", "z​w", "é é",
         "ª º ² ½", "ǰ", "Ω Å K", "µ", "\u0085next", "Ａ　", " 　 ", "ß",
         "ĳ Ǳ", "ﬅ", "ẞ", "Ⅰ", "ﬆop", "ᾳ ᾼ"]


def corpus(seed: int = 8, n_fuzz: int = 120) -> list[str]:
    """Deterministic gate corpus: workload + every ASCII code point (in context) + traps +
    seeded fuzz mixing ASCII, whitespace controls and trap characters."""
    out = list(tn.WORKLOAD)
    out += ["a%sB c" % chr(i) for i in range(128)]
    out += TRAPS
    out += [t for w in REGIMES.values() for t in w]       # every priced input is also gated
    alphabet = ([chr(i) for i in range(32, 127)] * 3 + list("\t\n\x0b\x0c\r\x1c\x1d\x1e\x1f  ")
                + list("".join(TRAPS)))
    rng = random.Random(seed)
    for _ in range(n_fuzz):
        out.append("".join(rng.choice(alphabet) for _ in range(rng.randint(0, 14))))
    seen, uniq = set(), []
    for t in out:
        if t not in seen:
            seen.add(t); uniq.append(t)
    return uniq


_REF_CACHE: dict = {}


def reference(text: str) -> list[dict]:
    """The quilt's own FULL route run — the oracle's side of every gate comparison."""
    if text not in _REF_CACHE:
        _REF_CACHE[text] = tn.run(text, route="full")["log"].records
    return _REF_CACHE[text]


# The incumbent production network re-expressed in the DSL (textnorm_quilt.choose + its two
# routes). ALL networks B4 ranks are priced by ONE cost model (OP_COST) — pricing the incumbent
# by the quilt's own COST table and proposals by OP_COST would make a mere re-expression of the
# incumbent look cheaper (an artifact this module once had; see README §6). The quilt's real
# run is used only as the product ORACLE (reference()), never for price.
INCUMBENT = {"name": "incumbent", "guard": "ascii",
             "steps": ["map_fs_controls", "bytes_lower", "bytes_ws_collapse"], "fallback": "full"}
BASELINES = {"full": "full", "incumbent": INCUMBENT}


# ---- gate (B7) -----------------------------------------------------------------------

def gate(p, texts: list[str]) -> dict:
    """B7 per case, reference vs proposal. First refusal refuses the proposal."""
    label = "p:" + p["name"]
    for i, t in enumerate(texts):
        try:
            recs = execute(p, t, label)
        except Exception as e:
            return {"status": "refused", "stage": "execute", "case": i, "input": t,
                    "reason": "%s: %s" % (type(e).__name__, e)}
        v = bt.backtest_pair(reference(t), recs)
        if v["status"] != "certified":
            return {"status": "refused", "stage": "b7", "case": i, "input": t,
                    "expected": tn.full_route(t), "got": _product(recs), "reason": v["reason"],
                    "verdict_hash": v["verdict_hash"]}
    return {"status": "passed", "cases": len(texts)}


# ---- promote (B4) --------------------------------------------------------------------

# Traffic regimes for PRICING (the gate corpus is adversarial and prices nothing). "Preferred
# when" is regime-dependent (§11.1): the quilt's own recorded WORKLOAD, and a declared
# clean-heavy regime (mostly already-normalized ASCII, e.g. re-normalizing stored keys).
REGIMES = {
    "quilt-workload": list(tn.WORKLOAD),
    "clean-heavy": ["hello world", "already clean", "id 42", "a b c", "ok", "user name",
                    "key:value", "x", "", "  Hello,   World!  ", "Straße  ﬁne  Ⅷ  ＡＢＣ"],
}


def promote(passed: list[dict], texts: list[str]) -> dict:
    """B4 over {incumbent, reference full, every gate-passing proposal} on one traffic regime."""
    if not passed:
        return {"status": "nothing-to-promote"}
    book, sums, refused = rp.PreferenceBook(), {}, 0
    for t in texts:
        routes = [(n, execute(b, t, n)) for n, b in BASELINES.items()] + \
                 [("p:" + p["name"], execute(p, t, "p:" + p["name"])) for p in passed]
        r = rp.prefer(routes, weights=book.weights)      # B4 re-runs the B7 gate itself
        if r["status"] != "certified":
            refused += 1
            continue
        book.observe(r)
        for n, ax in r["routes"].items():
            sums.setdefault(n, []).append(ax)
    work = rp.prefer_axes({n: bt._sum_axes(v) for n, v in sums.items()}, weights=book.weights)
    vs_inc = {}
    for p in passed:
        n = "p:" + p["name"]
        v = bt.score(work["routes"]["incumbent"], work["routes"][n], None, ("incumbent", n))
        vs_inc[n] = {"class": v["class"], "dominant": v["dominant"], "axes": v["axes"],
                     "cheap_detail": v["cheap_detail"]}
    proposals = {"p:" + p["name"] for p in passed}
    return {
        "status": "certified", "cases": len(texts), "b4_refused_cases": refused,
        "workload": work,
        "promoted": sorted(n for n in work["frontier"] if n in proposals),
        "satisfice": sorted(n for n in proposals if n not in work["frontier"]),
        "vs_incumbent": vs_inc,
        "settled": book.settled(), "book_digest": book.digest(),
        "preference_map": {"product": "text-normalize", "preferred_when": work["preferred_when"],
                           "frontier": work["frontier"], "dominated": work["dominated"]},
    }


# ---- the loop ------------------------------------------------------------------------

def redesign(proposals: list[dict], texts: list[str] | None = None) -> dict:
    """proposals: [{"proposer": str, "proposal": obj}]. Parse -> dedupe -> B7 gate -> B4."""
    texts = texts if texts is not None else corpus()
    rows, by_shape, passed = [], {}, []
    for n, b in BASELINES.items():         # rediscovering a baseline is a duplicate, not a win
        by_shape[shape_hash(b)] = {"name": n, "status": "passed"}
    for item in proposals:
        who, raw = item.get("proposer", "?"), item.get("proposal")
        try:
            p = parse(raw)
        except Invalid as e:
            rows.append({"proposer": who, "name": (raw or {}).get("name") if isinstance(raw, dict) else None,
                         "status": "refused", "stage": "parse", "reason": str(e)})
            continue
        sh = shape_hash(p)
        if sh in by_shape:
            first = by_shape[sh]
            rows.append({"proposer": who, "name": p["name"], "shape": sh, "network": describe(p),
                         "status": first["status"], "duplicate_of": first["name"]})
            continue
        names = {r.get("name") for r in rows}
        if p["name"] in names or p["name"] in ("full", "incumbent"):
            p["name"] = "%s-%s" % (p["name"], sh[-4:])
        g = gate(p, texts)
        row = {"proposer": who, "name": p["name"], "shape": sh, "network": describe(p),
               "rationale": (raw.get("rationale") or "")[:300], **g}
        rows.append(row)
        by_shape[sh] = row
        if g["status"] == "passed":
            passed.append(p)
    prom = {r: promote(passed, w) for r, w in sorted(REGIMES.items())}
    promoted = sorted({n for v in prom.values() for n in v.get("promoted", [])})
    satisfice = sorted({"p:" + p["name"] for p in passed} - set(promoted))
    tally = {"proposals": len(rows),
             "unique": len(by_shape) - len(BASELINES) + sum(1 for r in rows if r.get("stage") == "parse"),
             "passed": sum(1 for r in rows if r["status"] == "passed" and "duplicate_of" not in r),
             "refused_parse": sum(1 for r in rows if r.get("stage") == "parse"),
             "refused_execute": sum(1 for r in rows if r.get("stage") == "execute"),
             "refused_b7": sum(1 for r in rows if r.get("stage") == "b7"),
             "duplicates": sum(1 for r in rows if "duplicate_of" in r),
             "promoted": len(promoted), "satisfice": len(satisfice)}
    rep = {"quilt": "text-normalize", "corpus_cases": len(texts),
           "corpus_hash": al.content_hash(texts), "proposals": rows, "promotion": prom,
           "promoted": promoted, "satisfice": satisfice,
           "tally": tally}
    rep["report_hash"] = al.content_hash(rep)
    return rep


# ---- offline stubs (also the selftest's fixtures) -------------------------------------

STUBS = [
    {"proposer": "stub", "proposal": {"name": "quilt-equiv", "guard": "ascii",
     "steps": ["map_fs_controls", "bytes_lower", "bytes_ws_collapse"], "fallback": "full",
     "rationale": "the incumbent, re-expressed: a duplicate of a baseline, never a 'win'"}},
    {"proposer": "stub", "proposal": {"name": "early-exit", "guard": "clean_ascii",
     "steps": ["identity"], "fallback": {"guard": "ascii",
     "steps": ["map_fs_controls", "bytes_lower", "bytes_ws_collapse"], "fallback": "full"},
     "rationale": "skip all work when the text is already normalized ASCII"}},
    {"proposer": "stub", "proposal": {"name": "blank-exit", "guard": "blank",
     "steps": ["const_empty"], "fallback": "full"}},
    {"proposer": "stub", "proposal": {"name": "latin1-lower", "guard": "latin1",
     "steps": ["lower", "ws_collapse"], "fallback": "full",
     "rationale": "WRONG: lower != casefold on U+00DF, and NFKC is not identity on latin1"}},
    {"proposer": "stub", "proposal": {"name": "no-nfkc", "steps": ["casefold", "ws_collapse"],
     "rationale": "WRONG: drops NFKC (roman numerals, fullwidth, ligatures)"}},
    {"proposer": "stub", "proposal": {"name": "bytes-always",
     "steps": ["map_fs_controls", "bytes_lower", "bytes_ws_collapse"],
     "rationale": "WRONG: no guard, crashes on non-ASCII"}},
    {"proposer": "stub", "proposal": {"name": "bad-op", "steps": ["nfkc", "teleport"]}},
]


# ---- live: the cheap-model crew --------------------------------------------------------

CREW = ["deepseek-ai/DeepSeek-V4-Flash", "zai-org/GLM-5.3-Flash", "Qwen/Qwen3.8-Flash",
        "moonshotai/Kimi-K3", "inclusionAI/Ling-3.0-flash", "openai/gpt-oss-120b",
        "XiaomiMiMo/MiMo-V2.6-Pro", "tencent/Hy3"]


BOLD = ("\nBE AGGRESSIVE this round: every proposal must DROP, REORDER or SUBSTITUTE at least one "
        "reference step on some guarded path (e.g. lower for casefold, nfc for nfkc, str ops on "
        "latin1, casefold before nfkc) where you believe it is still byte-identical. Wrong bets are "
        "fine; they will be caught and logged.")


def crew_prompt(bold: bool = False) -> str:
    ops = {k: "wall_ms=%d prod_bytes=%d" % (v["wall_ms"], v["storage_bytes"]["prod"])
           for k, v in OP_COST.items()}
    gs = {k: "wall_ms=%d prod_bytes=%d" % (v["wall_ms"], v["storage_bytes"]["prod"])
          for k, v in GUARD_COST.items()}
    return (
        "You are redesigning a text-normalization pipeline to be CHEAPER or FASTER while producing "
        "BYTE-IDENTICAL output to the reference on EVERY possible input string.\n"
        "Reference: out = ' '.join(unicodedata.normalize('NFKC', s).casefold().split())  "
        "(Python 3).\nThe incumbent production route: if s.isascii(): map 0x1c-0x1f to space, "
        "bytes.lower(), bytes split/join; else the reference.\n\n"
        "Propose alternative networks in this JSON route language:\n"
        '{"name": "short-id", "guard": GUARD, "steps": [OP, ...], "fallback": "full" | <nested network>, '
        '"rationale": "one sentence"}\n'
        "If the guard holds on the input, the steps run left-to-right; otherwise the fallback runs "
        "('full' = the reference). Nest at most 3 deep, at most 8 steps.\n"
        "OPS (cost): %s\n"
        "  nfkc/nfc/nfkd = unicodedata.normalize; casefold/lower = str methods; ws_collapse = "
        "' '.join(s.split()); strip = s.strip(); map_fs_controls/bytes_lower/bytes_ws_collapse are "
        "ASCII-only byte ops that CRASH on non-ASCII; const_empty returns ''; identity returns s.\n"
        "GUARDS (cost): %s\n"
        "  ascii = s.isascii(); latin1 = all ord<256; blank = not s.strip(); clean_ascii = ASCII and "
        "already normalized (no A-Z, single inner spaces, no other whitespace/controls); always = no guard.\n\n"
        "Every proposal is checked against hundreds of adversarial inputs (all ASCII code points, "
        "ligatures, fullwidth, roman numerals, German sharp s, Turkish dotted I, Greek final sigma, "
        "unicode spaces). One wrong output and it is rejected. Ideas: reorderings, cheaper encodings, "
        "early exits, extra guarded fast paths.\n"
        "Reply with ONLY a JSON array of 2 or 3 proposals, no prose." % (ops, gs)) + (BOLD if bold else "")


def extract_json_array(text: str):
    """Pull the first JSON array (or object) out of a model reply; tolerate ``` fences."""
    t = re.sub(r"```(?:json)?", "", text)
    pairs = sorted((("[", "]"), ("{", "}")), key=lambda oc: (t.find(oc[0]) == -1, t.find(oc[0])))
    for opener, closer in pairs:                 # outermost container first
        i, j = t.find(opener), t.rfind(closer)
        if i != -1 and j > i:
            try:
                v = json.loads(t[i:j + 1])
                return v if isinstance(v, list) else [v]
            except json.JSONDecodeError:
                continue
    return None


def crew_propose(models: list[str], use_moth: bool = False, bold: bool = False):
    """Ask each cheap model for proposals. Returns (proposal items, crew log). Failures are
    logged, never hidden. Moth (optional) rotates the gating order with an un-gameable draw."""
    import providers as pv
    msgs = [{"role": "user", "content": crew_prompt(bold)}]
    items, log = [], []
    for m in models:
        try:
            r = pv.chat("deepinfra", m, msgs, max_tokens=3000, temperature=0.9, timeout=180)
        except pv.ProviderError as e:
            log.append({"model": m, "ok": False, "error": str(e)})
            continue
        arr = extract_json_array(r["text"])
        log.append({"model": m, "ok": arr is not None, "tokens": r["tokens"], "wall_ms": r["wall_ms"],
                    "n_proposals": len(arr) if arr else 0, "raw": r["text"][:4000]})
        for obj in arr or []:
            items.append({"proposer": m, "proposal": obj})
    order = {"source": "as-received", "offset": 0}
    if use_moth and items:
        try:
            k, job, heads = pv.moth_draw(len(items))
            items = items[k:] + items[:k]
            order = {"source": "moth", "offset": k, "job": job, "heads": heads}
        except pv.ProviderError as e:
            order = {"source": "as-received", "offset": 0, "moth_error": str(e)}
    return items, {"models": log, "order": order}


# ---- CLI --------------------------------------------------------------------------------

def _fmt(rep) -> str:
    L = ["== system2-redesigner over %s  (gate corpus %d cases, %s)"
         % (rep["quilt"], rep["corpus_cases"], rep["corpus_hash"])]
    for r in rep["proposals"]:
        tag = r["status"].upper() + ("(%s)" % r["stage"] if r.get("stage") else "")
        if "duplicate_of" in r:
            tag += " dup-of " + r["duplicate_of"]
        L.append("  %-22s %-14s %-34s %s" % (r.get("name"), tag, r["proposer"][:34], r.get("network", "")))
        if r.get("stage") in ("b7", "execute"):
            L.append("      counterexample %r -> expected %r got %r  [%s]"
                     % (r["input"], r.get("expected"), r.get("got"), r["reason"][:70]))
        elif r.get("stage") == "parse":
            L.append("      %s" % r["reason"][:110])
    for regime, pr in rep["promotion"].items():
        if pr.get("status") != "certified":
            L.append("  [%s] %s" % (regime, pr.get("status")))
            continue
        w = pr["workload"]
        L.append("  -- regime %s (%d cases)" % (regime, pr["cases"]))
        for n, ax in w["routes"].items():
            L.append("  %-22s wall_ms=%-5d storage_bytes=%-8d tokens=%d usd=%s"
                     % (n, ax["wall_ms"], ax["storage_bytes"], ax["tokens"], ax["usd"]))
        L.append("  frontier=%s  class=%s" % (w["frontier"], w["class"]))
        L.append("  preferred_when=%s" % w["preferred_when"])
        L.append("  promoted=%s  satisfice=%s" % (pr["promoted"], pr["satisfice"]))
        for n, v in pr["vs_incumbent"].items():
            L.append("  vs incumbent: %-20s %s (dominant=%s)" % (n, v["class"], v["dominant"]))
    L.append("  PROMOTED (frontier in >=1 regime)=%s  SATISFICE=%s" % (rep["promoted"], rep["satisfice"]))
    L.append("  tally=%s" % rep["tally"])
    L.append("  report_hash=%s" % rep["report_hash"])
    return "\n".join(L)


def main(argv):
    if "--live" in argv:
        models = CREW
        if "--models" in argv:
            models = argv[argv.index("--models") + 1].split(",")
        items, crew = crew_propose(models, use_moth="--moth" in argv, bold="--bold" in argv)
        crew["bold"] = "--bold" in argv
        rep = redesign(items)
        rep["crew"] = crew
        out = argv[argv.index("--out") + 1] if "--out" in argv else None
        if out:
            os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
            with open(out, "w") as f:
                json.dump(rep, f, indent=1, sort_keys=True, ensure_ascii=False)
        for m in crew["models"]:
            print("crew %-32s ok=%s n=%s %s" % (m["model"], m["ok"], m.get("n_proposals", 0),
                                                m.get("error", "")[:90]))
        print("order:", crew["order"])
    else:
        rep = redesign(STUBS)
    print(json.dumps(rep, sort_keys=True, indent=1, ensure_ascii=False) if "--json" in argv else _fmt(rep))


if __name__ == "__main__":
    main(sys.argv[1:])
