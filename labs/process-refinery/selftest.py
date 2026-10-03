"""process-refinery selftest — offline, stdlib, deterministic.

Covers: parsing the 12 seed scars, worked-rate on a hand-computed fixture, the rule
classifier on fixture rows, tokens-per-receipt arithmetic, setup-cell well-formedness
(and rejection of malformed cells), corpus loading, and a determinism check over the
real ledger.
"""

from __future__ import annotations

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import process_refinery as pr  # noqa: E402

checks = failures = 0


def check(name: str, cond: bool) -> None:
    global checks, failures
    checks += 1
    if not cond:
        failures += 1
        print("FAIL:", name)


# 1. seed scars from DEVELOPMENT-AS-A-QUILT.md §2
seed = pr.parse_seed_scars()
check("12 seed scars parsed", len(seed) == 12)
check("seed outcomes are 7 SCAR + 5 CLUNKY",
      (sum(s["outcome"] == "SCAR" for s in seed), sum(s["outcome"] == "CLUNKY" for s in seed)) == (7, 5))
check("every seed outcome is a valid outcome", all(s["outcome"] in pr.OUTCOMES for s in seed))
check("every seed phase is a valid phase", all(s["phase"] in pr.PHASES for s in seed))
check("every seed has a fix", all(s["fix"] for s in seed))
first = seed[0]
check("first seed scar is the metaphor brief", first["pattern"] == "metaphor-heavy-director-brief"
      and first["outcome"] == "SCAR" and first["canonical"] == "dispatch-5.5-director")
by = {s["pattern"]: s for s in seed}
check("harvest-via-full-merge -> CLUNKY on harvest pattern",
      by["harvest-via-full-merge"]["outcome"] == "CLUNKY"
      and by["harvest-via-full-merge"]["canonical"] == "harvest-checkout-fetch-head")
check("flaky selftest maps to selftest pattern",
      by["flaky-selftest-unseeded-draw"]["canonical"] == "independent-selftest-receipt")
check("backticks stripped from labels", all("`" not in s["label"] + s["fix"] for s in seed))

# seed parsing on a synthetic spec (fallback path independent of the real doc)
with tempfile.TemporaryDirectory() as td:
    spec = os.path.join(td, "spec.md")
    open(spec, "w").write("# x\n\n### The scars already observed this session\n\n"
                          "| pattern | outcome | fix |\n|---|---|---|\n"
                          "| flaky selftest | SCAR | pin the seed |\n| harvest via full merge | CLUNKY | checkout |\n"
                          "\nprose\n\n## 3. next\n| not | a | scar |\n")
    syn = pr.parse_seed_scars(spec)
    check("synthetic spec: 2 rows, stops at next section", len(syn) == 2)
    check("synthetic spec: phases inferred", [s["phase"] for s in syn] == ["BUILD", "HARVEST"])

# 2. worked-rate on a fixture (hand-computed)
def sig(p, o, e="cloud-session"):
    return {"canonical": p, "pattern": p, "outcome": o, "env": e}

fx = ([sig("a", "WORKED")] * 3 + [sig("a", "CLUNKY")] + [sig("a", "SCAR")] * 2
      + [sig("a", "WORKED", "fork+keys")] + [sig("b", "SCAR")] * 4 + [sig("c", "WORKED")] * 5)
r = pr.worked_rates(fx)
check("a/cloud: 3 W, 1 C, 2 S, n=6", (r[("a", "cloud-session")]["WORKED"], r[("a", "cloud-session")]["CLUNKY"],
                                      r[("a", "cloud-session")]["SCAR"], r[("a", "cloud-session")]["n"]) == (3, 1, 2, 6))
check("a/cloud worked_rate = 0.5", r[("a", "cloud-session")]["worked_rate"] == 0.5)
check("a/fork+keys kept separate, rate 1.0", r[("a", "fork+keys")]["worked_rate"] == 1.0)
check("b worked_rate = 0.0", r[("b", "cloud-session")]["worked_rate"] == 0.0)
check("c worked_rate = 1.0", r[("c", "cloud-session")]["worked_rate"] == 1.0)
check("worked_rate on 2/3", pr.worked_rates([sig("d", "WORKED")] * 2 + [sig("d", "SCAR")])[("d", "cloud-session")]["worked_rate"] == 0.6667)
sh = pr.scar_heaviest(r)
check("scar-heaviest: b first (4 SCAR), then a (2)", [k[0] for k, _ in sh] == ["b", "a"])
tw = pr.top_worked(r, min_n=5)
check("top_worked: c (5/5) then a (3/6); b excluded (<50%)", [p for p, _ in tw] == ["c", "a"])
check("top_worked respects min_n", pr.top_worked(r, min_n=6) == [("a", r[("a", "cloud-session")])])
check("worked_rates empty -> {}", pr.worked_rates([]) == {})

# 3. rule classifier on fixture rows
def row(tier, text, status="DONE", cc=1, rid="x1"):
    return {"id": rid, "order": 0, "date": "", "tier": tier, "model": "dispatcher",
            "cost_class": cc, "status": status, "text": text}

c = pr.classify_row(row("HARVEST", "Harvested branch; selftest 25 checks, 0 failures"))
check("clean harvest -> WORKED", c["outcome"] == "WORKED")
check("clean harvest -> harvest + selftest patterns",
      {"harvest-checkout-fetch-head", "independent-selftest-receipt"} <= set(c["patterns"]))
check("403 push -> SCAR", pr.classify_row(row("BUILD", "director push failed 403"))["outcome"] == "SCAR")
check("rate-limit -> CLUNKY", pr.classify_row(row("BUILD", "hit the rate limit, resumed"))["outcome"] == "CLUNKY")
check("OPEN row unresolved", pr.classify_row(row("BUILD", "plan to build", "OPEN"))["outcome"] is None)
check("BLOCKED status -> SCAR", pr.classify_row(row("BUILD", "waiting on creds", "BLOCKED"))["outcome"] == "SCAR")
check("SCAR tier -> SCAR", pr.classify_row(row("SCAR", "operational learning"))["outcome"] == "SCAR")
check("doc row ABOUT scars is not a scar",
      pr.classify_row(row("DOC", "booked 12 scars incl cross-repo push 403"))["outcome"] == "WORKED")
check("jev-quilt repo name is not a gate",
      "verified-gate" not in pr.classify_row(row("BUILD", "PR on jev-quilt"))["patterns"])
check("JEV adjudication is a gate", "verified-gate" in pr.classify_row(row("BUILD", "JEV adjudicated"))["patterns"])
check("scheduling local-GPU work stays cloud-session",
      pr.classify_row(row("BUILD", "docket of local-GPU experiments"))["env"] == "cloud-session")
check("openclaw shipped -> local-gpu-openclaw",
      pr.classify_row(row("COORD", "Casey's openclaw shipped superinstance-api"))["env"] == "local-gpu-openclaw")
check("'403 checks' is a count, not a 403", pr.classify_row(row("HARVEST", "11 selftests, 403 checks, 0 failures"))["outcome"] == "WORKED")
check("'no stall' is negated", pr.classify_row(row("SESSION", "fallbacks worked, no unfunded-provider stall"))["outcome"] == "WORKED")
check("'reject 403' is a feature", pr.classify_row(row("BUILD", "cross-origin reject 403, oversized 413"))["outcome"] == "WORKED")
check("flaky selftest is a SCAR", pr.classify_row(row("HARVEST", "its selftest is FLAKY"))["outcome"] == "SCAR")
check("unmatched row -> other", pr.classify_row(row("BUILD", "zzz"))["patterns"] == ["other"])

# 4. tokens-per-receipt arithmetic
rows = [row("BUILD", "selftest 10 checks", cc=3, rid="a"), row("NOTE", "learning", cc=1, rid="b"),
        row("BUILD", "PR #4 MERGED", cc=3, rid="c"), row("BUILD", "wip", "OPEN", cc=8, rid="d"),
        row("BUILD", "landed @ abc1234", cc=1, rid="e"), row("NOTE", "x", cc=None, rid="f")]
t = pr.tokens_per_receipt(rows, parts=2)
check("overall: 16 units / 3 receipts", (t["overall"]["cost_units"], t["overall"]["receipts"]) == (16, 3))
check("overall cost-units/receipt = 5.333", t["overall"]["cost_units_per_receipt"] == 5.333)
check("est tokens = units x constant / receipts",
      t["overall"]["est_tokens_per_receipt"] == round(16 * pr.TOKENS_PER_COST_UNIT / 3))
check("token figure flagged estimate", t["estimate"] is True)
check("windows split in booking order", [w["first"] for w in t["windows"]] == ["a", "d"])
check("window 1: 7 units / 2 receipts", (t["windows"][0]["cost_units"], t["windows"][0]["receipts"]) == (7, 2))
check("no receipts -> None, not div-by-zero",
      pr.tokens_per_receipt([row("NOTE", "x")], parts=1)["overall"]["cost_units_per_receipt"] is None)

# 5. setup cells: well-formed, and malformed ones are rejected
ev = {"WORKED": 3, "CLUNKY": 1, "SCAR": 2, "n": 6, "worked_rate": 0.5}
cell = pr.render_setup_cell("harvest-checkout-fetch-head", "cloud-session", ev,
                            [s for s in seed if s["canonical"] == "harvest-checkout-fetch-head"], ["d150"])
h = pr.parse_setup_cell(cell)
check("setup cell parses", h["cell"] == "setup" and h["pattern"] == "harvest-checkout-fetch-head")
check("setup cell observed with evidence", h["status"] == "observed" and "worked_rate=0.50" in h["evidence"])
check("setup cell has >=3 steps", len(h["steps"]) >= 3)
check("setup cell carries its known scars", "full merge" in cell and "clobbers" in cell)
check("setup cell names FETCH_HEAD step", "FETCH_HEAD" in cell)
d = pr.parse_setup_cell(pr.render_setup_cell("cheap-crew-brief", "fork+keys", None, [], []))
check("zero-evidence env cell is derived-unverified", d["status"] == "derived-unverified")
check("derived cell has env-specific steps", any("DEEPINFRA_KEY" in s for s in d["steps"]))
g = pr.parse_setup_cell(pr.render_setup_cell("no-such-pattern", "local-gpu-openclaw", None, [], []))
check("unknown pattern falls back to generic steps", len(g["steps"]) == 1)
for bad, why in [(cell.replace("---\n", "", 1), "no front matter"),
                 (cell.replace("cell: setup", "cell: other"), "wrong cell kind"),
                 (cell.replace("env: cloud-session", "env: mars"), "unknown env"),
                 (cell.replace("## Receipt", "## Receit"), "missing section"),
                 (cell.replace("\n1. ", "\n- ").replace("\n2. ", "\n- ").replace("\n3. ", "\n- ")
                      .replace("\n4. ", "\n- ").replace("\n5. ", "\n- "), "no numbered steps")]:
    try:
        pr.parse_setup_cell(bad)
        check("malformed cell rejected: " + why, False)
    except ValueError:
        check("malformed cell rejected: " + why, True)

# 6. corpus loader: typed signals accepted, junk skipped, absent -> []
with tempfile.TemporaryDirectory() as td:
    p = os.path.join(td, "ps.jsonl")
    open(p, "w").write('{"phase":"PUSH","pattern":"backoff-push","outcome":"WORKED","env":"fork+keys"}\n'
                       '{"pattern":"x","outcome":"MAYBE"}\n\n{"outcome":"SCAR"}\n')
    cs = pr.load_corpus(p)
    check("corpus: 1 valid of 3", len(cs) == 1 and cs[0]["env"] == "fork+keys" and cs[0]["source"] == "corpus")
    check("corpus absent -> []", pr.load_corpus(os.path.join(td, "nope.jsonl")) == [])

# 6b. crew agreement: advisory, column-echo names filtered, absent -> None
with tempfile.TemporaryDirectory() as td:
    cp = os.path.join(td, "crew.json")
    import json
    json.dump({"crew": ["m"], "usage": {}, "proposals": {
        "a": {"outcome": "WORKED", "patterns": ["act", "new-move"]},
        "b": {"outcome": "WORKED", "patterns": ["ledger-note"]}}}, open(cp, "w"))
    ca = pr.crew_agreement(rows, cp)
    check("crew: agreement counted against the rule classifier",
          ca["compared"] == 2 and ca["agree"] == sum(
              1 for rid in ("a", "b") if pr.classify_row(next(r for r in rows if r["id"] == rid))["outcome"] == "WORKED"))
    check("crew: echo name 'act' filtered, novel name kept, canonical dropped",
          [n for n, _ in ca["candidate_names"]] == ["new-move"])
    check("crew file absent -> None", pr.crew_agreement(rows, os.path.join(td, "none.json")) is None)

# 7. the real ledger: parse, determinism, cells emitted for every env
real = pr.load_ledger()
check("real ledger parses >= 160 rows", len(real) >= 160)
check("every real row has an id and a tier", all(r["id"] and r["tier"] for r in real))
r1, r2 = pr.build(), pr.build()
check("build deterministic (result_hash)", r1["result_hash"] == r2["result_hash"])
check("report deterministic", pr.render_report(r1) == pr.render_report(r2))
check("3-4 top WORKED patterns", 3 <= len(r1["top_worked"]) <= 4)
check("one cell per (top pattern, env)", len(r1["setup_cells"]) == 3 * len(r1["top_worked"]))
ok = True
for name, text in r1["_cells"].items():
    try:
        hh = pr.parse_setup_cell(text)
        ok &= name == "%s.%s.md" % (hh["pattern"], hh["env"])
    except ValueError:
        ok = False
check("every emitted cell is well-formed and named <pattern>.<env>.md", ok)
check("gate cell inherits the ungated-output scar",
      "ungated" in r1["_cells"].get("verified-gate.cloud-session.md", "ungated"))
check("report marks the token figure as an estimate", "ESTIMATE" in pr.render_report(r1))
check("fnv1a64 known vector", pr.fnv1a64("") == "0xcbf29ce484222325")

print("process-refinery selftest: %d checks, %d failures" % (checks, failures))
sys.exit(1 if failures else 0)
