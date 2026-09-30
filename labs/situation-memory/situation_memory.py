#!/usr/bin/env python3
"""situation_memory.py — index situation-recorder transcripts so the corpus can recall.

The situation-recorder chain (labs/situation-recorder/) is *replayable*: every mission is a
hash-chained transcript of relation-records. It is not *searchable*: nothing answers "which
past mission is near this one, and how did it end?" — the recall primitive System-2 needs
(situations/arch/ACTIVELEDGER-CELL-GRAPH.md §11). The turbovec substrate is searchable but
remembers generic vectors (situations/arch/TURBOVEC-FAMILY-STUDY.md). This cell joins the two:
each verified transcript becomes one MISSION CELL on a second fnv1a-64 chain (same constants,
same GENESIS), carrying an embedding, substrate-style 4-bit codes, the transcript's head hash,
and the mission OUTCOME.

HONESTY — the embedder is a STAND-IN, not semantic.
    MissionEmbedder (id "situation-memory/structural-lexical-v1") is deterministic and cheap:
      block "rel"    9-d  relation-verb histogram (TASK ROUTE DRAFT DRAW FOLD KEEP DROP MARK OUTCOME)
      block "budget" 14-d budget-vector features (see BUDGET_FEATURES; most are PROXIES because
                          situation transcripts do not yet carry ActiveLog budget vectors)
      block "text"   64-d signed hash bag-of-words over the TASK brief text
    Two missions that say the same thing in different words are FAR under the text block. That
    is lexical recall, the same limit gap #2 of the turbovec study names for `simple_embed`.
    Swap it by passing any object with `.id`, `.blocks` ({name: dim}), `.semantic` and
    `.embed(records) -> {block: [float]}` to MissionIndex(embedder=...). Nothing else changes.

Library:
    load_corpus(transcripts_dir=None, ledger=None) -> (situations, sources)
    MissionIndex(embedder=None).add(records, source) -> mission cell
    MissionIndex.find_similar_missions(query, k=5, mode="float", exclude=()) -> [hit, ...]
        query: a transcript (list of records) OR a plain task-text string.
        hit:   {rank, sid, distance, outcome, outcome_raw, provenance, brief, cell}
    results_hash(hits) -> "0x…" fnv1a-64 over the canonical hits (determinism receipt)
    build_index(...) -> MissionIndex over the real corpus

CLI:
    python3 situation_memory.py                        # index the real corpus, print a summary
    python3 situation_memory.py --query "harvest + verify a cell" -k 5
    python3 situation_memory.py --like sit-2026-09-29-syzygy-p1-harvest -k 5
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
RECORDER_DIR = HERE.parent / "situation-recorder"
sys.path.insert(0, str(RECORDER_DIR))

from recorder import GENESIS, REL_TYPES, verify  # noqa: E402  (same chain rule as the writer)

DEFAULT_TRANSCRIPTS = REPO / "situations" / "transcripts"
DEFAULT_LEDGER = REPO / "situations" / "dispatch-ledger.csv"

FNV_OFFSET = 0xCBF29CE484222325
FNV_PRIME = 0x100000001B3
REL_ORDER = ["TASK", "ROUTE", "DRAFT", "DRAW", "FOLD", "KEEP", "DROP", "MARK", "OUTCOME"]
assert set(REL_ORDER) == REL_TYPES


def fnv1a64(s: str) -> int:
    h = FNV_OFFSET
    for b in s.encode("utf-8"):
        h ^= b
        h = (h * FNV_PRIME) & 0xFFFFFFFFFFFFFFFF
    return h


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hx(n: int) -> str:
    return "0x%016x" % n


# ---- outcome: the decision-useful label a hit carries --------------------------------

# Checked in this order; first match wins. The raw result is always kept beside the class.
_OUTCOME_RULES = [
    ("SCAR", re.compile(r"\b(scar\w*|blocked|abandon\w*|fail\w*|red|revert\w*|refus\w*|dropped|rejected)\b")),
    ("OPEN", re.compile(r"\b(open|pending|partial|awaiting|wip|in[- ]progress)\b")),
    ("DONE", re.compile(r"\b(done|verified|validated|shipped|folded|kept|green|landed|merged)\b")),
]


def classify_outcome(result) -> str:
    """Map a raw OUTCOME result to DONE / OPEN / SCAR / OTHER (UNLABELED when absent)."""
    if result is None or str(result).strip() == "":
        return "UNLABELED"
    text = re.sub(r"[-_/]", " ", str(result).lower())
    for cls, pat in _OUTCOME_RULES:
        if pat.search(text):
            return cls
    return "OTHER"


def mission_outcome(records) -> tuple[str, object]:
    """(class, raw) from the LAST OUTCOME record — the most recent realized label."""
    outs = [r for r in records if r.get("rel") == "OUTCOME"]
    if not outs:
        return "UNLABELED", None
    raw = outs[-1].get("body", {}).get("result")
    return classify_outcome(raw), raw


def task_text(records) -> str:
    return " ".join(str(r.get("body", {}).get("brief", "")) for r in records if r.get("rel") == "TASK")


# ---- the stand-in embedder -----------------------------------------------------------

_STOP = frozenset("""a an and are as at be by for from has in into is it its of on or that the
this to was were will with""".split())
_TOKEN = re.compile(r"[a-z0-9]+")

BUDGET_FEATURES = [
    # name                 source                                                     real/proxy
    ("log_records",        "log1p(#records) / 4",                                     "proxy"),
    ("log_actors",         "log1p(#distinct actor ids) / 3",                           "proxy"),
    ("log_cost_class",     "log1p(cost_class parsed from ROUTE.why) / 3",              "real (ledger)"),
    ("log_wall_ms",        "log1p(sum body.budget.wall_ms) / 16",                      "real if present"),
    ("log_tokens",         "log1p(sum body.budget.tokens.*) / 16",                     "real if present"),
    ("log_usd_milli",      "log1p(1000 * sum body.budget.usd) / 10",                   "real if present"),
    ("tier_dispatcher",    "fraction of records by tier dispatcher",                   "proxy"),
    ("tier_captain",       "fraction by tier captain",                                 "proxy"),
    ("tier_crew",          "fraction by tier crew/build/other worker tiers",           "proxy"),
    ("tier_referee",       "fraction by tier referee",                                 "proxy"),
    ("tier_dice",          "fraction by tier dice",                                    "proxy"),
    ("fold_min",           "min FOLD.folded_min (0 if no FOLD)",                       "real (FOLD)"),
    ("fold_gap",           "min FOLD.gap (0 if none)",                                 "real (FOLD)"),
    ("live",               "1 if no record is provenance-stamped as reconstructed",    "real"),
]


def _l2(v):
    n = math.sqrt(sum(x * x for x in v))
    return [x / n for x in v] if n > 0 else list(v)


class MissionEmbedder:
    """Deterministic structural + lexical STAND-IN for a semantic mission embedder."""

    id = "situation-memory/structural-lexical-v1"
    semantic = False  # read by callers + the selftest: this does NOT do semantic recall
    TEXT_DIM = 64
    blocks = {"rel": len(REL_ORDER), "budget": len(BUDGET_FEATURES), "text": TEXT_DIM}

    def embed_text(self, text: str) -> list:
        v = [0.0] * self.TEXT_DIM
        for tok in _TOKEN.findall(text.lower()):
            if len(tok) < 2 or tok in _STOP:
                continue
            h = fnv1a64(tok)
            v[h % self.TEXT_DIM] += 1.0 if (h >> 63) == 0 else -1.0
        return _l2(v)

    def embed(self, records) -> dict:
        n = len(records)
        hist = [0.0] * len(REL_ORDER)
        for r in records:
            hist[REL_ORDER.index(r["rel"])] += 1.0
        tiers = {"dispatcher": 0, "captain": 0, "crew": 0, "referee": 0, "dice": 0}
        actors, cost, wall, toks, usd, folds, gaps, live = set(), 0.0, 0.0, 0.0, 0.0, [], [], 1.0
        for r in records:
            a = r.get("actor", {})
            actors.add(a.get("id"))
            t = a.get("tier", "")
            tiers[t if t in tiers else "crew"] += 1
            b = r.get("body", {}) or {}
            if "reconstructed" in str(b.get("provenance", "")):
                live = 0.0
            if r["rel"] == "ROUTE":
                m = re.search(r"cost_class=(\d+)", str(b.get("why", "")))
                if m:
                    cost = max(cost, float(m.group(1)))
            bud = b.get("budget")
            if isinstance(bud, dict):
                wall += float(bud.get("wall_ms", 0) or 0)
                tk = bud.get("tokens", 0)
                toks += float(sum(tk.values()) if isinstance(tk, dict) else (tk or 0))
                usd += float(bud.get("usd", 0) or 0)
            if r["rel"] == "FOLD":
                if b.get("folded_min") is not None:
                    folds.append(float(b["folded_min"]))
                if b.get("gap") is not None:
                    gaps.append(float(b["gap"]))
        budget = [
            math.log1p(n) / 4, math.log1p(len(actors)) / 3, math.log1p(cost) / 3,
            math.log1p(wall) / 16, math.log1p(toks) / 16, math.log1p(1000 * usd) / 10,
            *[tiers[k] / n if n else 0.0 for k in ("dispatcher", "captain", "crew", "referee", "dice")],
            min(folds) if folds else 0.0, min(gaps) if gaps else 0.0, live,
        ]
        return {"rel": _l2(hist), "budget": _l2(budget), "text": self.embed_text(task_text(records))}


# ---- substrate-style 4-bit codes (TurboQuant shape: rotate, then Lloyd-Max quantize) ---

# 16-level Lloyd-Max centroids for N(0,1) (symmetric; standard table values).
_LM = [0.1284, 0.3881, 0.6568, 0.9424, 1.2562, 1.6180, 2.0690, 2.7326]
CENTROIDS = [-c for c in reversed(_LM)] + _LM
_BOUNDS = [(CENTROIDS[i] + CENTROIDS[i + 1]) / 2 for i in range(15)]


def _xorshift(seed):
    x = seed & 0xFFFFFFFFFFFFFFFF or 1
    while True:
        x ^= (x << 13) & 0xFFFFFFFFFFFFFFFF
        x ^= x >> 7
        x ^= (x << 17) & 0xFFFFFFFFFFFFFFFF
        yield x


def rotation(dim: int, seed: int) -> list:
    """Data-oblivious orthonormal rotation (Gaussian via Box-Muller on xorshift, then
    Gram-Schmidt) — deterministic for (dim, seed), as in turbovec-substrate."""
    g = _xorshift(seed)

    def gauss():
        u1 = (next(g) >> 11) / float(1 << 53) or 1e-12
        u2 = (next(g) >> 11) / float(1 << 53)
        return math.sqrt(-2 * math.log(u1)) * math.cos(2 * math.pi * u2)

    basis = []
    while len(basis) < dim:
        v = [gauss() for _ in range(dim)]
        for b in basis:
            d = sum(x * y for x, y in zip(v, b))
            v = [x - d * y for x, y in zip(v, b)]
        n = math.sqrt(sum(x * x for x in v))
        if n > 1e-9:
            basis.append([x / n for x in v])
    return basis


def _rotate(R, v):
    return [sum(r * x for r, x in zip(row, v)) for row in R]


def quantize(v_rot, dim) -> list:
    """Coordinates of a unit vector in R^d are ~N(0, 1/d); scale by sqrt(d), snap to 16 levels."""
    s = math.sqrt(dim)
    out = []
    for x in v_rot:
        y, c = x * s, 0
        while c < 15 and y > _BOUNDS[c]:
            c += 1
        out.append(c)
    return out


def dequantize(codes, dim) -> list:
    s = math.sqrt(dim)
    return [CENTROIDS[c] / s for c in codes]


def codes_hex(codes) -> str:
    return "".join("%x" % c for c in codes)


# ---- the mission index: one chained cell per verified transcript ---------------------

ROUND = 6  # vectors are rounded before hashing so the chain is platform-stable


class MissionIndex:
    def __init__(self, embedder=None, seed: int = 42):
        self.embedder = embedder or MissionEmbedder()
        self.seed = seed
        self.cells: list[dict] = []
        self._rot = {name: rotation(dim, seed + i) for i, (name, dim)
                     in enumerate(sorted(self.embedder.blocks.items()))}

    # -- encode --
    def _encode(self, blocks: dict) -> tuple[dict, dict]:
        rot, codes = {}, {}
        for name, v in blocks.items():
            dim = self.embedder.blocks[name]
            if len(v) != dim:
                raise ValueError("block %r has dim %d, embedder declares %d" % (name, len(v), dim))
            rv = [round(x, ROUND) for x in _rotate(self._rot[name], v)]
            rot[name] = rv
            codes[name] = quantize(rv, dim)
        return rot, codes

    # -- write --
    def add(self, records, source: str = "live") -> dict:
        """Verify the transcript chain, embed it, append one mission cell. Refuses a
        transcript whose own chain does not replay (never index an unverified mission)."""
        ok, msg = verify(records)
        if not ok:
            raise ValueError("refusing unverified transcript %r: %s"
                             % (records[0].get("sid") if records else None, msg))
        rot, codes = self._encode(self.embedder.embed(records))
        cls, raw = mission_outcome(records)
        prov = sorted({str(r.get("body", {}).get("provenance")) for r in records
                       if r.get("body", {}).get("provenance")}) or ["live-capture"]
        cell = {
            "kind": "mission",
            "seq": len(self.cells),
            "sid": records[0]["sid"],
            "source": source,
            "provenance": prov[0] if len(prov) == 1 else prov,
            "transcript_head": records[-1]["hash"],
            "n_records": len(records),
            "brief": task_text(records)[:240],
            "outcome": cls,
            "outcome_raw": raw,
            "embedder": self.embedder.id,
            "semantic": bool(self.embedder.semantic),
            "vec": rot,
            "codes": {k: codes_hex(v) for k, v in codes.items()},
        }
        prev = self.cells[-1]["hash"] if self.cells else GENESIS
        cell["prev_hash"] = prev
        cell["hash"] = hx(fnv1a64(canon({k: v for k, v in cell.items() if k != "hash"})))
        self.cells.append(cell)
        return cell

    # -- verify --
    def verify_chain(self) -> tuple[bool, str]:
        prev = GENESIS
        for i, c in enumerate(self.cells):
            if c.get("seq") != i or c.get("prev_hash") != prev:
                return False, "link broken at cell %d" % i
            want = hx(fnv1a64(canon({k: v for k, v in c.items() if k != "hash"})))
            if c.get("hash") != want:
                return False, "hash mismatch at cell %d (%s)" % (i, c.get("sid"))
            prev = c["hash"]
        return True, "ok: %d mission cells, chain intact" % len(self.cells)

    def head(self) -> str:
        return self.cells[-1]["hash"] if self.cells else GENESIS

    # -- read --
    def _query_blocks(self, query) -> dict:
        if isinstance(query, str):  # task text only: compare on the text block alone
            return {"text": self.embedder.embed_text(query)}
        return self.embedder.embed(query)

    def find_similar_missions(self, query, k: int = 5, mode: str = "float",
                              exclude=(), weights=None) -> list:
        """Nearest past missions to `query` (a transcript or task text).

        distance = sqrt( sum_b w_b * ||q_b - m_b||^2 / sum_b w_b ) over the blocks the query
        has, compared in each block's rotated space (rotation preserves L2). mode="codes"
        compares the query against the cells' DEQUANTIZED 4-bit codes instead of the stored
        floats (asymmetric distance). Ties break on sid for determinism."""
        if mode not in ("float", "codes"):
            raise ValueError("mode must be 'float' or 'codes'")
        w = dict(weights or {"rel": 0.25, "budget": 0.15, "text": 0.60})
        qrot, _ = self._encode(self._query_blocks(query))
        blocks = [b for b in qrot if w.get(b, 0) > 0]
        wsum = sum(w[b] for b in blocks)
        excl = set(exclude)
        scored = []
        for c in self.cells:
            if c["sid"] in excl:
                continue
            acc = 0.0
            for b in blocks:
                dim = self.embedder.blocks[b]
                mv = (dequantize([int(ch, 16) for ch in c["codes"][b]], dim)
                      if mode == "codes" else c["vec"][b])
                acc += w[b] * sum((x - y) ** 2 for x, y in zip(qrot[b], mv))
            scored.append((round(math.sqrt(acc / wsum), ROUND), c["sid"], c))
        scored.sort(key=lambda t: (t[0], t[1]))
        return [{"rank": i + 1, "sid": sid, "distance": d, "outcome": c["outcome"],
                 "outcome_raw": c["outcome_raw"], "provenance": c["provenance"],
                 "brief": c["brief"][:120], "cell": c["hash"]}
                for i, (d, sid, c) in enumerate(scored[:k])]


def results_hash(hits) -> str:
    return hx(fnv1a64(canon(hits)))


# ---- the real corpus ---------------------------------------------------------------

def load_corpus(transcripts_dir=None, ledger=None):
    """Live transcripts (every *.jsonl under situations/transcripts/ outside backfill/),
    plus the ledger backfill: read from backfill/ledger.jsonl if run_all.sh wrote it, else
    transcoded in memory from dispatch-ledger.csv (same deterministic output, no write).
    Returns (situations: {sid: records}, sources: {sid: "live"|"backfill"})."""
    tdir = Path(transcripts_dir or DEFAULT_TRANSCRIPTS)
    sits, sources = {}, {}
    for path in sorted(tdir.rglob("*.jsonl")):
        src = "backfill" if "backfill" in path.relative_to(tdir).parts else "live"
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                sits.setdefault(rec["sid"], []).append(rec)
                sources[rec["sid"]] = src
    if "backfill" not in sources.values():
        from ledger_to_transcript import transcode  # noqa: E402 (recorder dir on sys.path)
        lp = Path(ledger or DEFAULT_LEDGER)
        if lp.exists():
            for s in transcode(lp):
                sits[s.sid] = list(s.records)
                sources[s.sid] = "backfill"
    for recs in sits.values():
        recs.sort(key=lambda r: r["seq"])
    return sits, sources


def build_index(transcripts_dir=None, ledger=None, embedder=None) -> MissionIndex:
    sits, sources = load_corpus(transcripts_dir, ledger)
    idx = MissionIndex(embedder=embedder)
    for sid in sorted(sits, key=lambda s: (sources[s] != "live", s)):  # live first, then by sid
        idx.add(sits[sid], sources[sid])
    return idx


def _print_hits(hits):
    for h in hits:
        print("  %d. d=%.4f  %-9s %-44s %s" % (h["rank"], h["distance"], h["outcome"],
                                               h["sid"][:44], str(h["outcome_raw"])[:40]))
        print("       brief: %s" % h["brief"][:100])


def main(argv=None):
    ap = argparse.ArgumentParser(description="situation-memory: recall past missions")
    ap.add_argument("--query", help="task text to recall against (text block only)")
    ap.add_argument("--like", metavar="SID", help="use an indexed mission's transcript as the query")
    ap.add_argument("-k", type=int, default=5)
    ap.add_argument("--mode", choices=("float", "codes"), default="float")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    sits, _ = load_corpus()
    idx = build_index()
    ok, msg = idx.verify_chain()
    if not ok:
        print("INDEX CHAIN FAILED: " + msg)
        return 2
    if args.like:
        if args.like not in sits:
            print("unknown sid %r" % args.like)
            return 1
        hits = idx.find_similar_missions(sits[args.like], args.k, args.mode, exclude=[args.like])
    elif args.query:
        hits = idx.find_similar_missions(args.query, args.k, args.mode)
    else:
        hits = None
    if args.json:
        print(json.dumps({"head": idx.head(), "hits": hits,
                          "results_hash": results_hash(hits) if hits is not None else None}, indent=2))
        return 0
    live = sum(1 for c in idx.cells if c["source"] == "live")
    print("embedder: %s  (semantic=%s — lexical/structural STAND-IN)" % (idx.embedder.id, idx.embedder.semantic))
    print("indexed %d missions (%d live, %d backfill)  %s" % (len(idx.cells), live, len(idx.cells) - live, msg))
    print("index head: %s" % idx.head())
    if hits is not None:
        print("find_similar_missions(%s, k=%d, mode=%s):" % (
            ("like=%s" % args.like) if args.like else repr(args.query), args.k, args.mode))
        _print_hits(hits)
        print("results_hash: %s" % results_hash(hits))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
