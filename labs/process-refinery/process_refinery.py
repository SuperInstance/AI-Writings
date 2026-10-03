"""process-refinery — System-2 pointed at the development process itself.

Reads the process record and reports which development MOVES work, per environment,
then emits portable SETUP CELLS for the WORKED-dominant ones
(situations/arch/DEVELOPMENT-AS-A-QUILT.md §2-§4).

Inputs (all in-repo, read-only):
    situations/corpus/process-signals.jsonl   typed process_signal records (crew-runner writes
                                              these; optional — absent today)
    situations/arch/DEVELOPMENT-AS-A-QUILT.md §2's 12 seed scars (always read: the fallback
                                              and the known-scar library for setup cells)
    situations/dispatch-ledger.csv            every dispatch row, mined for pattern outcomes
    labs/process-refinery/crew_patterns.json  advisory cheap-crew pattern names (optional;
                                              never feeds a metric)

The metrics are deterministic: a rule classifier tags each ledger row with patterns, an
outcome (WORKED / CLUNKY / SCAR, or unresolved) and an env. Same files in -> same report
out (no clock, no randomness, no network); the report carries an fnv1a-64 hash like the
rest of the fleet. Ledger outcomes are INFERRED from prose and are labelled that way.

    worked_rate = WORKED / (WORKED + CLUNKY + SCAR)        per (pattern, env)

Headline: anthropic-tokens-per-shipped-receipt. The ledger records cost_class (integer
cost-units) but not tokens, so tokens are an ESTIMATE = cost-units x TOKENS_PER_COST_UNIT,
always marked as such. Cost-units-per-receipt is exact and reported beside it.

Library:  load_ledger, parse_seed_scars, load_corpus, ledger_signals, worked_rates,
          scar_heaviest, tokens_per_receipt, top_worked, render_setup_cell, parse_setup_cell,
          build(), render_report()
CLI:      python3 process_refinery.py            # print summary
          python3 process_refinery.py --write    # write the report + situations/setups/
          python3 process_refinery.py --json     # machine-readable result
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
from collections import Counter, OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
LEDGER = os.path.join(REPO, "situations", "dispatch-ledger.csv")
SPEC = os.path.join(REPO, "situations", "arch", "DEVELOPMENT-AS-A-QUILT.md")
CORPUS = os.path.join(REPO, "situations", "corpus", "process-signals.jsonl")
CREW = os.path.join(HERE, "crew_patterns.json")
REPORT = os.path.join(REPO, "situations", "arch", "PROCESS-REFINERY-REPORT.md")
SETUPS = os.path.join(REPO, "situations", "setups")

OUTCOMES = ("WORKED", "CLUNKY", "SCAR")
PHASES = ("PLAN", "DISPATCH", "BUILD", "HARVEST", "BOOK", "PUSH")
ENVS = ("cloud-session", "local-gpu-openclaw", "fork+keys")

# ESTIMATE, not a measurement. One cost-unit (the ledger's cost_class: 1 dispatcher/Haiku,
# 3 Sonnet lane, 8 Opus/Fable lane) is priced at 60k Anthropic tokens — a dispatcher
# turn-burst with its context reads. A Sonnet lane ~180k, an Opus lane ~480k. Change it
# here; every token figure in the report scales linearly and the cost-unit figures don't move.
TOKENS_PER_COST_UNIT = 60_000

RESOLVED_OK = {"DONE", "FOLDED", "MERGED"}
RESOLVED_BAD = {"BLOCKED", "ABANDONED"}
UNRESOLVED = {"OPEN", "PENDING", "HOLD"}
KNOWN_STATUS = RESOLVED_OK | RESOLVED_BAD | UNRESOLVED | {"PARTIAL"}


def fnv1a64(data: str) -> str:
    h = 0xcbf29ce484222325
    for b in data.encode("utf-8"):
        h = ((h ^ b) * 0x100000001b3) & 0xFFFFFFFFFFFFFFFF
    return "0x%016x" % h


def canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


# ---- 1. readers ----------------------------------------------------------------------

def load_ledger(path: str = LEDGER) -> list[dict]:
    """Parse the dispatch ledger tolerantly. Some rows carry unquoted commas in prose, so
    only the first five columns are positional; the rest is kept as one free-text field and
    the status is the last column that names a known status."""
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        reader = csv.reader(fh)
        header = next(reader)
        for i, rec in enumerate(reader):
            if not rec or not rec[0].strip():
                continue
            rec = rec + [""] * (len(header) - len(rec))
            status = ""
            for field in reversed(rec[5:]):
                tok = field.strip().split(" ")[0].upper()
                if tok in KNOWN_STATUS:
                    status = tok
                    break
            cc = rec[4].strip()
            rows.append({
                "id": rec[0].strip(), "order": i, "date": rec[1].strip(),
                "tier": rec[2].strip().upper(), "model": rec[3].strip(),
                "cost_class": int(cc) if cc.isdigit() else None,
                "status": status, "text": " | ".join(f.strip() for f in rec[5:] if f.strip()),
            })
    return rows


def _slug(s: str) -> str:
    s = re.sub(r"[`'\"()]", "", s.lower())
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


# The seed scars name their own move; this maps each onto the canonical ledger pattern it
# is a scar *of*, so a setup cell for that pattern inherits it as a known scar.
SEED_CANONICAL = (
    (r"metaphor|perm mode|add_repo|cross-repo", "dispatch-5.5-director"),
    (r"full merge|clobber", "harvest-checkout-fetch-head"),
    (r"503|push-auth", "backoff-push"),
    (r"usage caps|5h", "dispatch-5.5-director"),
    (r"roster|cheap model", "cheap-crew-brief"),
    (r"selftest", "independent-selftest-receipt"),
)
SEED_PHASE = ((r"brief|perm|add_repo", "DISPATCH"), (r"harvest|clobber", "HARVEST"),
              (r"push|503", "PUSH"), (r"roster|selftest|cheap", "BUILD"), (r"cap", "DISPATCH"))


def parse_seed_scars(path: str = SPEC) -> list[dict]:
    """The §2 table of DEVELOPMENT-AS-A-QUILT.md -> process_signal records."""
    text = open(path, encoding="utf-8").read()
    start = text.index("### The scars already observed")
    end = text.index("\n## ", start)
    out = []
    for line in text[start:end].splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] in ("pattern", "") or set(cells[0]) <= set("-: "):
            continue
        name, outcome, fix = cells
        low = name.lower()
        phase = next((p for rx, p in SEED_PHASE if re.search(rx, low)), "BUILD")
        canonical = next((c for rx, c in SEED_CANONICAL if re.search(rx, low)), _slug(name))
        out.append({"phase": phase, "pattern": _slug(name), "label": name.replace("`", ""),
                    "canonical": canonical, "outcome": outcome.upper(), "cost": {},
                    "env": "cloud-session", "fix": fix.replace("`", ""),
                    "ref": "DEVELOPMENT-AS-A-QUILT.md §2", "source": "seed-scar"})
    return out


def load_corpus(path: str = CORPUS) -> list[dict]:
    """Typed process_signal records (crew-runner's output). Absent file -> []."""
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("outcome") not in OUTCOMES or not rec.get("pattern"):
            continue
        rec.setdefault("env", "cloud-session")
        rec.setdefault("canonical", rec["pattern"])
        rec["source"] = "corpus"
        out.append(rec)
    return out


# ---- 2. the deterministic rule classifier over ledger prose ---------------------------

PATTERNS = OrderedDict([
    # name: (phase, regex over tier+model+text)
    ("dispatch-5.5-director", ("DISPATCH", r"create_session|director|session_0|child.session|\blanes?\b")),
    ("cheap-crew-brief", ("BUILD", r"cheap|deepinfra|z\.ai|\bzai\b|deepseek|roster|flash|glm|qwen|crew|mistral|llama")),
    ("harvest-checkout-fetch-head", ("HARVEST", r"harvest|fetch_head|checkout \S+ --")),
    ("independent-selftest-receipt", ("HARVEST", r"selftest|\d+ checks|\d+/0\b|tests? (green|pass)|ci green|0 fail")),
    ("pr-merge-release", ("PUSH", r"pr #\d+|\bmerged?\b")),
    ("in-process-subagent", ("DISPATCH", r"subagent|in-process|agent tool")),
    ("scheduled-trigger", ("HARVEST", r"send_later|trigger|wakeup|scheduled")),
    ("backoff-push", ("PUSH", r"backoff|\b503\b|re-?push")),
    ("verified-gate", ("BUILD", r"\bjev\b(?!-quilt)|typesafe|\bgated\b|gate proven|product-identity|probes\.yaml|\bb7\b|differ\b")),
    ("architecture-spec", ("PLAN", r"^(arch|doc|seed|plan|coord|systemize|skill)\b")),
    ("ledger-note", ("BOOK", r"^(note|scar|owner-block)\b")),
])

# Tuned against the real ledger: "403 checks", "evil-origin rejected 403", "injection scan",
# "1 blocked" (an inventory) and "honest scars" (scars as data) are features, not breaks.
SCAR_RX = re.compile(r"(?<!rejected )\b40[13]\b(?!\s*(checks|/|rejected))|clobber|flaky|killed|"
                     r"\bstall(ed|s)?\b|(?<!\d )\bblocked\b|failed on|injection(?![ -]scan)|"
                     r"\bbroke\b|red main|authentication_error", re.I)
# Phrases that name a break only to negate it or describe a feature; blanked before scanning.
NEGATED_RX = re.compile(r"\bno (\S+ )?stall|reject(ed|s)? 40[13]|40[13]-checks|"
                        r"injection can evade|encoded injection", re.I)
CLUNKY_RX = re.compile(r"re-?dispatch|retr(y|ied)|rate.?limit|\b503\b|paused|workaround|"
                       r"session limit|usage cap|salvage|re-?steer|restart|conflict|flapp|"
                       r"\bv2\b|errored|stalled", re.I)
# A row that SCHEDULES local-GPU work was still run from a cloud session; only a row saying
# the openclaw agent itself shipped/ran something is evidence for that env.
SCAR_WORD = re.compile(r"\bscar\b(?!s)", re.I)
WRITING_TIERS = {"DOC", "ARCH", "SEED", "SKILL", "SYSTEMIZE", "PLAN", "COORD"}
ENV_RX = (("local-gpu-openclaw", re.compile(r"openclaw\s+(shipped|ran|built|landed)", re.I)),
          ("fork+keys", re.compile(r"(ran|shipped|built) (from|in|on) (a |the )?fork", re.I)))


def classify_row(row: dict) -> dict:
    """-> {patterns, outcome (None if unresolved), env}. Precedence SCAR > CLUNKY > WORKED."""
    hay = "%s %s %s" % (row["tier"].lower(), row["model"].lower(), row["text"].lower())
    pats = [n for n, (_, rx) in PATTERNS.items() if re.search(rx, hay)] or ["other"]
    st = row["status"]
    # writing ABOUT scars/friction (a doc/arch row) is not having them: for writing tiers
    # only the status column can mark a row SCAR/CLUNKY
    prose = "" if row["tier"] in WRITING_TIERS else NEGATED_RX.sub(" ", row["text"])
    if (row["tier"] in ("SCAR", "OWNER-BLOCK") or st in RESOLVED_BAD or SCAR_WORD.search(prose)
            or SCAR_RX.search(prose)):
        outcome = "SCAR"
    elif st == "PARTIAL" or CLUNKY_RX.search(prose):
        outcome = "CLUNKY"
    elif st in RESOLVED_OK:
        outcome = "WORKED"
    else:
        outcome = None
    if st in UNRESOLVED and row["tier"] not in ("SCAR", "OWNER-BLOCK"):
        outcome = None  # an OPEN row's prose describes intent, not a result
    env = next((e for e, rx in ENV_RX if rx.search(row["text"])), "cloud-session")
    return {"patterns": pats, "outcome": outcome, "env": env}


def ledger_signals(rows: list[dict]) -> list[dict]:
    """One inferred process_signal per (row, pattern) for every resolved row."""
    out = []
    for row in rows:
        c = classify_row(row)
        if c["outcome"] is None:
            continue
        for p in c["patterns"]:
            out.append({"phase": PATTERNS[p][0] if p in PATTERNS else "BUILD", "pattern": p,
                        "canonical": p, "outcome": c["outcome"], "env": c["env"],
                        "cost": {"cost_units": row["cost_class"]}, "fix": "",
                        "ref": row["id"], "source": "ledger-inferred"})
    return out


# ---- 3. metrics ----------------------------------------------------------------------

def worked_rates(signals: list[dict], key: str = "canonical") -> dict:
    """{(pattern, env): {WORKED, CLUNKY, SCAR, n, worked_rate}} — worked_rate is
    WORKED / (WORKED + CLUNKY + SCAR); None when n == 0."""
    acc: dict = {}
    for s in signals:
        k = (s[key], s["env"])
        a = acc.setdefault(k, {"WORKED": 0, "CLUNKY": 0, "SCAR": 0})
        a[s["outcome"]] += 1
    for a in acc.values():
        a["n"] = a["WORKED"] + a["CLUNKY"] + a["SCAR"]
        a["worked_rate"] = round(a["WORKED"] / a["n"], 4) if a["n"] else None
    return dict(sorted(acc.items()))


def scar_heaviest(rates: dict, limit: int = 6) -> list:
    """Patterns ranked by SCAR count, then scar share, then name (deterministic)."""
    items = [(k, v) for k, v in rates.items() if v["SCAR"]]
    items.sort(key=lambda kv: (-kv[1]["SCAR"], -kv[1]["SCAR"] / kv[1]["n"], kv[0]))
    return items[:limit]


def top_worked(rates: dict, env: str = "cloud-session", min_n: int = 5, limit: int = 4) -> list:
    """WORKED-dominant patterns: worked_rate >= 0.5 over >= min_n signals, ranked by
    WORKED count then rate. 'other' never qualifies."""
    items = [(k[0], v) for k, v in rates.items()
             if k[1] == env and k[0] != "other" and v["n"] >= min_n and v["worked_rate"] >= 0.5]
    items.sort(key=lambda kv: (-kv[1]["WORKED"], -kv[1]["worked_rate"], kv[0]))
    return items[:limit]


HARD_RECEIPT_RX = re.compile(r"\d+ checks|\d+/0\b|selftest|pr #\d+|\bmerged\b|@ ?[0-9a-f]{7,}|"
                             r"tests? (green|pass)|ci green", re.I)


def tokens_per_receipt(rows: list[dict], parts: int = 3) -> dict:
    """Anthropic-tokens-per-shipped-receipt over the whole ledger and by booking-order
    window. Spend counts EVERY row with a cost_class (notes and failures are overhead the
    receipts must carry); a receipt is a DONE/FOLDED row whose prose cites a verifiable
    artifact (a selftest/check count, a PR/merge, or a commit sha)."""
    def window(rs):
        units = sum(r["cost_class"] or 0 for r in rs)
        rec = sum(1 for r in rs if r["status"] in RESOLVED_OK and HARD_RECEIPT_RX.search(r["text"]))
        return {"rows": len(rs), "cost_units": units, "receipts": rec,
                "cost_units_per_receipt": round(units / rec, 3) if rec else None,
                "est_tokens_per_receipt": round(units * TOKENS_PER_COST_UNIT / rec) if rec else None,
                "first": rs[0]["id"] if rs else None, "last": rs[-1]["id"] if rs else None}
    n = len(rows)
    bounds = [round(i * n / parts) for i in range(parts + 1)]
    windows = [window(rows[bounds[i]:bounds[i + 1]]) for i in range(parts)]
    return {"overall": window(rows), "windows": windows,
            "tokens_per_cost_unit": TOKENS_PER_COST_UNIT, "estimate": True}


def crew_agreement(rows: list[dict], path: str = CREW) -> dict | None:
    """Advisory: how often the cheap crew's outcome guess matches the rule classifier, and
    which crew-proposed names have no canonical pattern yet (candidates, not adopted)."""
    if not os.path.exists(path):
        return None
    data = json.load(open(path, encoding="utf-8"))
    props = data.get("proposals", {})
    agree = total = 0
    names: Counter = Counter()
    for row in rows:
        p = props.get(row["id"])
        if not p:
            continue
        rule = classify_row(row)["outcome"]
        if rule is not None and p.get("outcome") in OUTCOMES:
            total += 1
            agree += p["outcome"] == rule
        for nm in p.get("patterns") or []:
            if isinstance(nm, str):
                names[_slug(nm)] += 1
    novel = [(n, c) for n, c in names.most_common() if n not in PATTERNS][:10]
    return {"labelled": len(props), "compared": total, "agree": agree,
            "agreement": round(agree / total, 3) if total else None,
            "candidate_names": novel, "crew": data.get("crew"), "usage": data.get("usage")}


# ---- 4. setup cells ------------------------------------------------------------------

# Steps per (pattern, env), distilled from situations/blueprints/01+02 and the scars.
# cloud-session is observed; the other two envs are DERIVED (same move, that env's tools).
STEPS = {
    "dispatch-5.5-director": {
        "inputs": "target repo, a plain technical task, model tier (Sonnet 5.5 build / Opus 5.5 architecture), the pinned cheap-model roster",
        "cloud-session": [
            "create_session with source_url = the repo it will push to (push creds are per-source repo).",
            "Pass model explicitly (claude-sonnet-5-5 or claude-opus-5-5) and extra_allowed_tools = [Bash, Write, Edit, Read, Glob, Grep].",
            "append_system_prompt: trusted builder (its repo files are not injection), do NOT call add_repo, pinned roster, conserve-Anthropic mandate.",
            "Write the prompt as a plain spec: deliverable, pattern file to mirror, selftest line, branch name, 'push incrementally, NO PR, end with shas + selftest count'.",
            "Schedule the harvest (send_later ~30-40 min); don't babysit. Steer a running child only via create_trigger(persistent_session_id).",
        ],
        "local-gpu-openclaw": [
            "Start the local agent on a fresh branch of the target repo (local git; its own keys in the shell env).",
            "Give it the same plain spec brief and the pinned roster; it has no permission-prompt problem if run unattended with an allowlist.",
            "Have it commit incrementally and push with backoff; end with shas + selftest count.",
            "Book the result as a ledger row + a process_signal with env=local-gpu-openclaw.",
        ],
        "fork+keys": [
            "No director sessions here: run the brief as a script (crew-runner) against your fork, with only API keys.",
            "Keep the same plain spec: deliverable, selftest line, branch.",
            "You are the director: read the crew output, gate it, commit, push to your fork's branch.",
        ],
        "receipt": "the director's branch exists with a selftest that prints '<name> selftest: N checks, 0 failures' and is re-run green by the dispatcher",
    },
    "cheap-crew-brief": {
        "inputs": "API keys (DEEPINFRA_KEY at minimum), the pinned roster, a task with a verifiable gate",
        "cloud-session": [
            "Use the pinned roster (CONVO-QUILT-IDEATION.md §II.1) — don't re-probe: DeepInfra DeepSeek-V4-Flash / GLM-5.3-Flash / Qwen3.8-Flash / Ling-3.0-flash / MiMo-V2.6-Pro / gpt-oss-120b; z.ai via the CODING endpoint.",
            "Keep a stable prompt prefix so repeat calls hit the provider cache.",
            "Crew proposes in volume (temperature 0 for labelling, higher for ideation); the 5.5 model only decomposes and verifies.",
            "Gate every crew output with a verified cell (B7, probes, TypeSafe typed-check, or a deterministic rule) before it counts.",
            "Cache the crew output in the repo so the report/selftest is reproducible offline.",
        ],
        "local-gpu-openclaw": [
            "Same roster over the same HTTPS endpoints, plus local models on the GPU for the free tier of the volume.",
            "Same gate and cache discipline; record the cheap-vs-Anthropic token split in the process_signal.",
        ],
        "fork+keys": [
            "Export DEEPINFRA_KEY (and optionally ZAI_KEY for the coding endpoint); run the crew script directly.",
            "Avoid Inkling-Small / Muse-Glimmer / granite-4.2-30b at low token caps (they return empty text).",
            "Gate before trusting; commit the cached crew output.",
        ],
        "receipt": "a cached crew-output file + a gate that accepted/rejected it deterministically + a token-split line",
    },
    "harvest-checkout-fetch-head": {
        "inputs": "the director's branch name, the lab directory it owns",
        "cloud-session": [
            "get_session(<id>) to read status — harvest even if the last turn errored (lanes push incrementally).",
            "git fetch origin <branch> (backoff on network errors).",
            "git checkout FETCH_HEAD -- labs/<thing>   # only the files you want; never a full merge.",
            "Never blind-checkout a shared index file (README, landing page, ledger); re-add your rows from HEAD.",
            "Re-run the selftest on main yourself, then book your own ledger row (yours supersedes the director's).",
        ],
        "local-gpu-openclaw": [
            "git fetch the agent's branch from the local remote; checkout FETCH_HEAD -- <dir> onto your working branch.",
            "Same rule: shared index files are restored from HEAD, never taken from the branch.",
            "Re-run the selftest locally before booking.",
        ],
        "fork+keys": [
            "If the work came from a PR or another fork: git fetch <remote> <branch>; git checkout FETCH_HEAD -- <dir>.",
            "Re-run its selftest before you trust it.",
        ],
        "receipt": "only the lab directory changed on main + the selftest re-run green + one booked ledger row",
    },
    "independent-selftest-receipt": {
        "inputs": "a lab with selftest.py (stdlib, offline)",
        "cloud-session": [
            "Every lab ships selftest.py that prints '<name> selftest: N checks, 0 failures' and exits non-zero on failure.",
            "Pin every random draw (seed) — an unseeded selftest is flaky and is not a receipt.",
            "The dispatcher re-runs it after harvest; the director's own claim is not the receipt.",
            "Prove N consecutive green runs before trusting a selftest that touches randomness.",
            "Quote the exact count in the ledger row.",
        ],
        "local-gpu-openclaw": [
            "Same selftest contract; run it in a clean checkout, not the agent's working tree.",
            "Quote the count in the process_signal and the ledger row.",
        ],
        "fork+keys": [
            "python3 labs/<thing>/selftest.py — no keys needed (offline by contract).",
            "If it needs a key it is not a selftest; split the live part out.",
        ],
        "receipt": "the selftest line, re-run by someone other than the author",
    },
    "verified-gate": {
        "inputs": "a candidate output (crew draft, cheaper route, model answer) and a gate that can refuse it",
        "cloud-session": [
            "Pick the gate that fits: B7 product-identity (labs/system2-backtest) for routes, a probes.yaml / differ for behaviour, TypeSafe typed-check (TYPESAFEAI_KEY) for structured output, JEV only on domains its competence map marks reliable.",
            "Run the gate FIRST; never price or compare an output that failed it (refuse, don't rank).",
            "Make the gate deterministic and replayable: same input -> same verdict + a verdict hash.",
            "Book refusals as well as passes — a gate that never refuses is not proven non-vacuous.",
            "Trim API keys from env before use (a trailing-whitespace key returns 401/403).",
        ],
        "local-gpu-openclaw": [
            "Same gates run locally (B7 and probes are stdlib/offline); TypeSafe/JEV need their keys in the agent's env.",
            "Book the verdict hash with the process_signal.",
        ],
        "fork+keys": [
            "Offline gates (B7, probes, differ) need nothing but the repo; TypeSafe needs TYPESAFEAI_KEY.",
            "Wire the gate before the crew call, not after the commit.",
        ],
        "receipt": "a gate verdict (pass or refusal) with its hash, reproducible on re-run",
    },
    "pr-merge-release": {
        "inputs": "a reviewed branch, owner go-ahead for the merge",
        "cloud-session": [
            "Open the PR (draft) only when asked; otherwise push the branch and book it.",
            "Merge only on an explicit owner instruction; wait for CI green on the head commit.",
            "Record the merge sha in the ledger row.",
        ],
        "local-gpu-openclaw": ["Same: CI green on head, owner go-ahead, record the merge sha."],
        "fork+keys": ["Open a PR from your fork; the upstream owner merges."],
        "receipt": "a merge sha with CI green on the merged head",
    },
    "architecture-spec": {
        "inputs": "a design question past the deadband, Opus 5.5",
        "cloud-session": [
            "Wake Opus 5.5 only past the deadband (architectural fork, irreversible action, law-level change).",
            "Deliverable is one doc under situations/arch/ with a buildable spec a Sonnet lane can execute.",
            "Book it; the next build lane cites it.",
        ],
        "local-gpu-openclaw": ["Same doc contract; author locally, push the doc."],
        "fork+keys": ["Write the spec as a doc in your fork; a crew can critique it, you decide."],
        "receipt": "a doc under situations/arch/ that a later build row cites",
    },
}

GENERIC = {"inputs": "the repo and the task", "receipt": "a booked ledger row",
           **{e: ["No distilled steps yet for this pattern; see the ledger refs below."] for e in ENVS}}


def render_setup_cell(pattern: str, env: str, ev: dict | None, scars: list[dict],
                      refs: list[str]) -> str:
    lib = STEPS.get(pattern, GENERIC)
    ev = ev or {"WORKED": 0, "CLUNKY": 0, "SCAR": 0, "n": 0, "worked_rate": None}
    status = "observed" if ev["n"] else "derived-unverified"
    lines = [
        "---",
        "cell: setup",
        "pattern: %s" % pattern,
        "env: %s" % env,
        "status: %s" % status,
        "evidence: worked=%d clunky=%d scar=%d n=%d worked_rate=%s" % (
            ev["WORKED"], ev["CLUNKY"], ev["SCAR"], ev["n"],
            "%.2f" % ev["worked_rate"] if ev["worked_rate"] is not None else "n/a"),
        "evidence_source: ledger-inferred + seed-scars (DEVELOPMENT-AS-A-QUILT.md §2)",
        "generated_by: labs/process-refinery",
        "---",
        "",
        "# Setup — `%s` in `%s`" % (pattern, env),
        "",
        "*To run this pattern in this environment, do the steps below. Generated by "
        "`labs/process-refinery`; regenerate rather than hand-edit.*",
        "",
    ]
    if status == "derived-unverified":
        lines += ["> **Derived, not observed.** No recorded run of this pattern in `%s` yet; the "
                  "steps are the cloud-session steps translated to this env's tools. The first run "
                  "here should book a `process_signal` with `env: %s`." % (env, env), ""]
    lines += ["## Inputs", "", lib["inputs"], "", "## Steps", ""]
    lines += ["%d. %s" % (i + 1, s) for i, s in enumerate(lib.get(env) or lib["cloud-session"])]
    lines += ["", "## Receipt", "", lib["receipt"], "", "## Known scars", ""]
    if scars:
        lines += ["- **%s** (%s) — fix: %s" % (s["label"], s["outcome"], s["fix"]) for s in scars]
    else:
        lines += ["- none recorded for this pattern"]
    if env != "cloud-session" and scars:
        lines += ["", "*Scars above were hit in cloud-session; which carry over to `%s` is "
                  "unmeasured.*" % env]
    lines += ["", "## Evidence refs", "",
              (", ".join(refs) if refs else "none (derived)"), ""]
    return "\n".join(lines)


REQUIRED_KEYS = ("cell", "pattern", "env", "status", "evidence", "generated_by")
REQUIRED_SECTIONS = ("## Inputs", "## Steps", "## Receipt", "## Known scars", "## Evidence refs")


def parse_setup_cell(text: str) -> dict:
    """Validate a setup cell. Raises ValueError if malformed; returns its header + steps."""
    if not text.startswith("---\n"):
        raise ValueError("missing front matter")
    end = text.index("\n---\n", 4)
    head = {}
    for line in text[4:end].splitlines():
        k, _, v = line.partition(":")
        head[k.strip()] = v.strip()
    for k in REQUIRED_KEYS:
        if not head.get(k):
            raise ValueError("missing key %s" % k)
    if head["cell"] != "setup" or head["env"] not in ENVS:
        raise ValueError("bad cell/env")
    if head["status"] not in ("observed", "derived-unverified"):
        raise ValueError("bad status")
    pos = [text.find(s) for s in REQUIRED_SECTIONS]
    if -1 in pos or pos != sorted(pos):
        raise ValueError("sections missing or out of order")
    steps_block = text[pos[1]:pos[2]]
    steps = [l for l in steps_block.splitlines() if re.match(r"^\d+\. ", l)]
    if not steps:
        raise ValueError("no steps")
    head["steps"] = steps
    return head


# ---- 5. build + report ---------------------------------------------------------------

def build(ledger: str = LEDGER, spec: str = SPEC, corpus: str = CORPUS, crew: str = CREW) -> dict:
    rows = load_ledger(ledger)
    seed = parse_seed_scars(spec)
    corp = load_corpus(corpus)
    led = ledger_signals(rows)
    signals = led + seed + corp
    rates = worked_rates(signals)
    ledger_only = worked_rates(led)
    resolved = [r for r in rows if classify_row(r)["outcome"] is not None]
    oc = Counter(classify_row(r)["outcome"] for r in resolved)
    top = top_worked(rates)
    cells = OrderedDict()
    for pattern, _ in top:
        scars = [s for s in seed + corp if s.get("canonical") == pattern and s["outcome"] != "WORKED"]
        refs = sorted({s["ref"] for s in led if s["canonical"] == pattern and s["outcome"] != "WORKED"},
                      key=lambda r: [int(x) if x.isdigit() else x for x in re.split(r"(\d+)", r)])
        for env in ENVS:
            ev = rates.get((pattern, env))
            cells["%s.%s.md" % (pattern, env)] = render_setup_cell(
                pattern, env, ev, scars, refs[-8:] if env == "cloud-session" else [])
    res = {
        "inputs": {"ledger_rows": len(rows), "resolved_rows": len(resolved),
                   "row_outcomes": dict(sorted(oc.items())), "seed_scars": len(seed),
                   "corpus_signals": len(corp), "ledger_signals": len(led),
                   "corpus_present": os.path.exists(corpus)},
        "rates": {"%s|%s" % k: v for k, v in rates.items()},
        "ledger_only_rates": {"%s|%s" % k: v for k, v in ledger_only.items()},
        "scar_heaviest": [["%s|%s" % k, v] for k, v in scar_heaviest(rates)],
        "top_worked": [[p, v] for p, v in top],
        "tokens": tokens_per_receipt(rows),
        "crew": crew_agreement(rows, crew),
        "setup_cells": list(cells),
        "seed": [{k: s[k] for k in ("pattern", "canonical", "phase", "outcome")} for s in seed],
    }
    res["result_hash"] = fnv1a64(canon(res))
    res["_cells"] = cells
    return res


def _pct(x):
    return "n/a" if x is None else "%.0f%%" % (100 * x)


def render_report(res: dict) -> str:
    inp, tok = res["inputs"], res["tokens"]
    o = tok["overall"]
    L = []
    L += ["# Process-refinery report — what our development moves actually do",
          "",
          "*Generated by `labs/process-refinery` (deterministic; regenerate with "
          "`python3 labs/process-refinery/process_refinery.py --write`). Spec: "
          "`DEVELOPMENT-AS-A-QUILT.md`. result_hash `%s`.*" % res["result_hash"],
          "",
          "## How to read this (and what is estimated)",
          "",
          "- **Ledger outcomes are inferred, not recorded.** The dispatch-ledger has no outcome "
          "column; a rule classifier reads each row's prose. SCAR = the row names a break "
          "(403/401, blocked, clobber, flaky, stall, injection, `SCAR`/`OWNER-BLOCK` tier); CLUNKY "
          "= it names friction (retry, rate-limit, 503, paused, re-dispatch, salvage, conflict); "
          "WORKED = DONE/FOLDED with neither. OPEN/PENDING rows are excluded as unresolved.",
          "- **A row's outcome is charged to every pattern it mentions.** A director lane that hit a "
          "403 marks `dispatch-5.5-director` *and* `harvest-*` SCAR. This over-spreads blame; "
          "typed `process_signal`s (crew-runner) will fix it.",
          "- **Tokens are an estimate.** The ledger records `cost_class` (integer cost-units), not "
          "tokens. Anthropic tokens = cost-units × %s (one dispatcher turn-burst). "
          "Cost-units-per-receipt is exact; the token figure scales with that constant." % format(
              tok["tokens_per_cost_unit"], ","),
          "- **Env:** the ledger is effectively all `cloud-session`. `local-gpu-openclaw` and "
          "`fork+keys` have **zero** recorded runs, so their setup cells are marked "
          "`derived-unverified`.",
          "",
          "## Inputs",
          "",
          "| source | count |", "|---|---|",
          "| ledger rows parsed | %d |" % inp["ledger_rows"],
          "| resolved rows (outcome inferred) | %d — %s |" % (
              inp["resolved_rows"], ", ".join("%s %d" % kv for kv in inp["row_outcomes"].items())),
          "| ledger-inferred signals (row × pattern) | %d |" % inp["ledger_signals"],
          "| seed scars (§2) | %d |" % inp["seed_scars"],
          "| process-signals.jsonl | %s |" % (
              "%d signals" % inp["corpus_signals"] if inp["corpus_present"]
              else "absent (crew-runner not landed) — seed scars used as the typed fallback"),
          "",
          "## Headline — anthropic-tokens-per-shipped-receipt (ESTIMATE)",
          "",
          "A *shipped receipt* = a DONE/FOLDED row citing a verifiable artifact (a selftest/check "
          "count, a PR/merge, or a commit sha). Spend counts every row, so notes and failures are "
          "overhead the receipts carry.",
          "",
          "| window | rows | cost-units | receipts | cost-units / receipt (exact) | est. Anthropic tokens / receipt |",
          "|---|---|---|---|---|---|",
          "| **all** | %d | %d | %d | %s | **~%s** |" % (
              o["rows"], o["cost_units"], o["receipts"], o["cost_units_per_receipt"],
              format(o["est_tokens_per_receipt"], ",") if o["est_tokens_per_receipt"] else "n/a")]
    for i, w in enumerate(tok["windows"]):
        L.append("| third %d (%s–%s) | %d | %d | %d | %s | ~%s |" % (
            i + 1, w["first"], w["last"], w["rows"], w["cost_units"], w["receipts"],
            w["cost_units_per_receipt"],
            format(w["est_tokens_per_receipt"], ",") if w["est_tokens_per_receipt"] else "n/a"))
    ws = [w["cost_units_per_receipt"] for w in tok["windows"]]
    if all(ws):
        trend = "falling" if ws[-1] < ws[0] else "rising" if ws[-1] > ws[0] else "flat"
        L += ["", "Trend by booking-order thirds: **%s** (%s cost-units/receipt). Caveat: later "
              "rows are dispatcher harvests (class 1) that bundle a child lane's work whose own "
              "Anthropic spend was not booked as a separate row, so the late thirds "
              "*under*-count spend. Read the trend as directional, not as proof the process got "
              "cheaper." % (trend, " → ".join(str(x) for x in ws))]
    L += ["", "## Worked-rate per pattern per env", "",
          "Combined signals (ledger-inferred + seed scars + corpus). worked_rate = WORKED / (WORKED + CLUNKY + SCAR).",
          "",
          "| pattern | env | WORKED | CLUNKY | SCAR | n | worked-rate |", "|---|---|---|---|---|---|---|"]
    for k, v in sorted(res["rates"].items(), key=lambda kv: (-kv[1]["n"], kv[0])):
        p, e = k.split("|")
        L.append("| `%s` | %s | %d | %d | %d | %d | %s |" % (
            p, e, v["WORKED"], v["CLUNKY"], v["SCAR"], v["n"], _pct(v["worked_rate"])))
    L += ["", "## What still hurts most — SCAR-heaviest patterns", "",
          "| pattern | env | SCAR | n | scar share |", "|---|---|---|---|---|"]
    for k, v in res["scar_heaviest"]:
        p, e = k.split("|")
        L.append("| `%s` | %s | %d | %d | %s |" % (p, e, v["SCAR"], v["n"], _pct(v["SCAR"] / v["n"])))
    if res["scar_heaviest"]:
        (wk, wv) = res["scar_heaviest"][0]
        share = sorted(((k, v) for k, v in res["rates"].items() if v["n"] >= 5 and v["SCAR"]),
                       key=lambda kv: (-kv[1]["SCAR"] / kv[1]["n"], kv[0]))
        L += ["", "**Worst by count:** `%s` (%d SCAR of %d). **Worst by share (n ≥ 5):** `%s` "
              "(%s of %d). The director lane is where nearly every seed scar lives too (perm mode, "
              "metaphor brief, cross-repo push, usage caps) — the spawn step, not the build, is what "
              "still breaks. `verified-gate`'s SCAR count is partly over-spread blame: e.g. d078/d083 "
              "book the TypeSafe/JEV 401 outage — the gate was unreachable, not wrong — and blocked "
              "director rows that merely name a gate are charged to it too." % (
                  wk.split("|")[0], wv["SCAR"], wv["n"], share[0][0][0],
                  _pct(share[0][1]["SCAR"] / share[0][1]["n"]), share[0][1]["n"])]
    L += ["", "Seed scars by the pattern they wound:", ""]
    sc = Counter(s["canonical"] for s in res["seed"] if s["outcome"] == "SCAR")
    cl = Counter(s["canonical"] for s in res["seed"] if s["outcome"] == "CLUNKY")
    for p in sorted(set(sc) | set(cl), key=lambda p: (-sc[p], -cl[p], p)):
        L.append("- `%s`: %d SCAR, %d CLUNKY" % (p, sc[p], cl[p]))
    L += ["", "## WORKED-dominant patterns → setup cells", "",
          "Rule: worked-rate ≥ 50% over ≥ 5 signals in cloud-session, ranked by WORKED count. "
          "Each gets three env cells in `situations/setups/`.", ""]
    for p, v in res["top_worked"]:
        L.append("- `%s` — %d WORKED / %d (%s)" % (p, v["WORKED"], v["n"], _pct(v["worked_rate"])))
    L += ["", "`architecture-spec` reads optimistic by construction: doc/arch rows can only fail by "
          "status (prose about scars is not a scar), so its rate measures *did the doc land*, not "
          "*was the design right*."]
    L += ["", "Emitted: " + ", ".join("`%s`" % c for c in res["setup_cells"]), ""]
    cr = res["crew"]
    L += ["## Cheap-crew pattern naming (advisory, gated)", ""]
    if cr:
        u = cr.get("usage") or {}
        L += ["The crew (%s) labelled %d rows from their prose (%d calls, %d failed; %s prompt + %s "
              "completion tokens, all non-Anthropic). Its outcome guess agreed with the rule "
              "classifier on **%s** of %d comparable rows. Crew labels feed **no** metric above; "
              "names it proposed that have no canonical pattern yet (candidates for a human to "
              "adopt or reject):" % (
                  ", ".join(cr.get("crew") or []), cr["labelled"], u.get("calls", 0),
                  u.get("failed", 0), format(u.get("prompt_tokens", 0), ","),
                  format(u.get("completion_tokens", 0), ","), _pct(cr["agreement"]), cr["compared"]),
              ""]
        L += ["- `%s` ×%d" % nc for nc in cr["candidate_names"]] or ["- none"]
    else:
        L += ["No crew_patterns.json — run `crew_name_patterns.py` with DEEPINFRA_KEY. The "
              "metrics don't need it."]
    L += ["", "## What this tells us to do next", "",
          "1. **Land crew-runner's typed `process_signal`s.** Inferred outcomes charge every "
          "pattern in a row; one typed signal per move removes the over-spread blame and makes "
          "tokens measured, not estimated.",
          "2. **Book Anthropic tokens per lane** (even a rough `usage` line). The headline metric "
          "is the thing we're driving down and today it rests on a constant.",
          "3. **Run one lane in `local-gpu-openclaw` and one in `fork+keys`** and book them — "
          "until then those setup cells are translations, not evidence.",
          ""]
    return "\n".join(L)


def write(res: dict) -> list[str]:
    os.makedirs(SETUPS, exist_ok=True)
    written = []
    for name, text in res["_cells"].items():
        with open(os.path.join(SETUPS, name), "w", encoding="utf-8") as fh:
            fh.write(text)
        written.append(os.path.join("situations", "setups", name))
    with open(REPORT, "w", encoding="utf-8") as fh:
        fh.write(render_report(res))
    written.append(os.path.relpath(REPORT, REPO))
    return written


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    res = build()
    if "--json" in argv:
        print(json.dumps({k: v for k, v in res.items() if k != "_cells"}, indent=1, sort_keys=True))
        return 0
    o = res["tokens"]["overall"]
    worst = res["scar_heaviest"][0] if res["scar_heaviest"] else None
    print("process-refinery: %d ledger rows (%d resolved), %d seed scars, corpus=%s" % (
        res["inputs"]["ledger_rows"], res["inputs"]["resolved_rows"], res["inputs"]["seed_scars"],
        res["inputs"]["corpus_signals"] if res["inputs"]["corpus_present"] else "absent"))
    if res["top_worked"]:
        p, v = res["top_worked"][0]
        print("top WORKED: %s (%d/%d)" % (p, v["WORKED"], v["n"]))
    if worst:
        print("worst SCAR: %s (%d SCAR of %d)" % (worst[0], worst[1]["SCAR"], worst[1]["n"]))
    print("cost-units/receipt %s; est. Anthropic tokens/receipt ~%s (ESTIMATE)" % (
        o["cost_units_per_receipt"], format(o["est_tokens_per_receipt"] or 0, ",")))
    print("result_hash %s" % res["result_hash"])
    if "--write" in argv:
        for p in write(res):
            print("wrote", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
