#!/usr/bin/env python3
"""
Jevvy the Auditor — High-Level Quality Audit Daemon

A high-level bot that:
- Reads recent canon (prose + songs + code)
- Batches 5-10 audit questions through JEV
- Verdict: PASS / CAUTION / FAIL
- Witnesses verdict with confidence score
- Reports verdicts to audit-log.json

Usage:
    python3 jevvy_audit.py --once
    python3 jevvy_audit.py --loop 600
"""
import os
import sys
import json
import time
import argparse
import hashlib
import urllib.request
from pathlib import Path
import concurrent.futures

CANON_DIR = Path("/workspace/repos/ai-writings/prose")
WITNESS_PATH = Path("/workspace/repos/ai-writings/bots/jevvy-auditor/witness.log")
AUDIT_LOG = Path("/workspace/repos/ai-writings/bots/jevvy-auditor/audit-log.json")

import sys
sys.path.insert(0, '/workspace/repos/ai-writings/bots/substrate-bus')
from substrate_bus import witness as substrate_witness, publish as substrate_publish

BOOKKEEPER_PATH = Path("/workspace/repos/ai-writings/bots/jevvy-auditor/bookkeeper.wal")

_witness_seq = [0]

def witness(event_type, payload):
    """Append a witness entry. The hash covers the timestamp and a monotonic
    sequence number as well as the payload, so two runs 33 days apart can never
    produce the same hash and a replayed verdict is detectable."""
    WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    _witness_seq[0] += 1
    ts = time.time()
    entry = {
        "ts": ts,
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "seq": _witness_seq[0],
        "event": event_type,
        "payload": payload,
    }
    entry["hash"] = hashlib.sha256(
        json.dumps({"ts": ts, "seq": entry["seq"], "event": event_type,
                    "payload": payload}, sort_keys=True, default=str).encode()
    ).hexdigest()[:16]
    with WITNESS_PATH.open("a") as f:
        f.write(json.dumps(entry) + "\n")

def jev_batch(state, questions):
    """Call JEV with batch of questions"""
    body = {
        "model": "jev-latest",
        "state": state[:1000],
        "questions": {f"q{i}": q for i, q in enumerate(questions)},
    }
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=data,
        headers={"Authorization": f"Bearer {os.environ['TYPESAFEAI_KEY']}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"error": str(e)}

def load_audit_log():
    if AUDIT_LOG.exists():
        return json.loads(AUDIT_LOG.read_text())
    return {"audits": []}

def save_audit_log(log):
    AUDIT_LOG.write_text(json.dumps(log, indent=2))

def pick_recent_canon(n=3):
    """Return up to n sampled canon files as (title, full_text).

    The full body is returned: the audit is worthless if the model is shown a
    title and a metadata header instead of the prose it is being asked to rate.
    """
    if not CANON_DIR.exists():
        return []
    files = sorted(CANON_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    out = []
    for f in files:
        if len(out) >= n:
            break
        try:
            body = f.read_text()
        except OSError:
            continue
        if body.strip():
            out.append((f.stem, body))
    return out

MAX_CANON_CHARS = 12000

def canon_block(samples, limit=MAX_CANON_CHARS):
    """Render the sampled canon as a single text block for the questions."""
    parts = []
    for name, body in samples:
        parts.append(f"### CANON DOCUMENT: {name}\n{body}")
    return "\n\n".join(parts)[:limit]

def build_audit_questions(samples, canon_text=None):
    """Build 5-7 audit questions about recent canon.

    Every question carries the canon text inline. Previously only q0 embedded
    any prose, so q1-q5 asked about "this canon" with no antecedent and could
    only be answered from a `state` field the endpoint largely ignores -- the
    model was effectively grading a document it had never been shown.
    """
    if not samples:
        raise ValueError("empty canon sample: refusing to audit a placeholder")

    if canon_text is None:
        canon_text = canon_block(samples)

    def q(instructions, type_, criteria=None):
        d = {"type": type_, "instructions": instructions}
        if criteria is not None:
            d["criteria"] = criteria
        return d

    return [
        q(f"How high is the quality of this canon?\n\n{canon_text}", "score",
          ["poor", "mediocre", "good", "excellent", "landmark"]),
        q(f"Does this canon advance the cellular-first substrate?\n\n{canon_text}", "noul"),
        q(f"Is this canon worth keeping (not waste)?\n\n{canon_text}", "noul"),
        q(f"How novel is this canon vs prior canon?\n\n{canon_text}", "score",
          ["redundant", "incremental", "novel", "highly-novel", "groundbreaking"]),
        q(f"How aligned is this canon with the substrate's core doctrines (cells, bookkeeper, ternary, JEPA, FEP)?\n\n{canon_text}", "score",
          ["misaligned", "partial", "aligned", "tightly-aligned", "embodies-doctrine"]),
        q(f"What is the biggest risk in this canon?\n\n{canon_text}", "choice",
          {"low-quality": "low-quality", "redundant": "redundant", "off-topic": "off-topic",
           "too-abstract": "too-abstract", "none": "no significant risk"}),
    ]

# Gate thresholds, calibrated against the canon corpus's own score
# distribution (47 frontmatter-scored files: q median 2.16, a median 3.39,
# best achievable avg 3.02). The previous absolute gate (avg >= 3.5 AND
# noul > 0.7) was unreachable for every canon in the corpus, so PASS could
# never be emitted -- a gate that cannot fire is not a gate.
PASS_AVG = 2.60        # corpus p90 of the best-scoring documents
PASS_NOUL = 0.70      # the corpus does reach this
CAUTION_AVG = 1.80
CAUTION_NOUL = 0.45

# A verdict is only trusted if the text-bearing score is materially above a
# same-batch no-text control arm. Without this, a model that never saw the
# canon still returns plausible numbers, and the bot cannot tell the
# difference between "the canon is bad" and "the model was blind".
CONTROL_MARGIN = 0.35

def _score_of(ans):
    v = ans.get("score", 1.0)
    if isinstance(v, dict):
        return float(v.get("level", 1.0))
    try:
        return float(v)
    except (TypeError, ValueError):
        return 1.0

def verdict_from_audit(answers, control=None):
    """Convert JEV answers to a verdict.

    If `control` is supplied (answers from a no-text control batch), the
    text-bearing score must clear the control by CONTROL_MARGIN on the
    quality/novelty/alignment average; otherwise the verdict is CAUTION
    with verdict_confidence="low" -- we refuse to assert a finding about
    canon the model may not have actually read.
    """
    quality_score = 1.0
    novelty_score = 1.0
    advance_prob = 0.5
    aligned_score = 1.0

    for name, ans in answers.items():
        if ans.get("type") == "score":
            level = _score_of(ans)
            if "quality" in name.lower() or name == "q0":
                quality_score = level
            elif "novel" in name.lower() or name == "q3":
                novelty_score = level
            elif "aligned" in name.lower() or "doctrines" in name.lower() or name == "q4":
                aligned_score = level
        elif ans.get("type") == "noul":
            noul = ans.get("noul", 0.5)
            if name == "q1":
                advance_prob = noul

    avg = (quality_score + novelty_score + aligned_score) / 3

    confidence = "normal"
    c_avg = None
    if control is not None:
        c_avg = (control.get("quality", 1.0) + control.get("novelty", 1.0)
                 + control.get("alignment", 1.0)) / 3
        if avg - c_avg < CONTROL_MARGIN:
            return "CAUTION", "low", avg, advance_prob, c_avg
        confidence = "high"

    if avg >= PASS_AVG and advance_prob > PASS_NOUL:
        verdict = "PASS"
    elif avg >= CAUTION_AVG and advance_prob >= CAUTION_NOUL:
        verdict = "CAUTION"
    else:
        verdict = "FAIL"
    return verdict, confidence, avg, advance_prob, c_avg

def _control_batch(questions):
    """Run the same questions with no canon text, as a blind control arm.

    A model asked to grade "this canon" without being shown any canon still
    returns plausible-looking numbers. The control arm measures that floor so
    the real batch can be checked against it.
    """
    blind = []
    for q in questions:
        q2 = dict(q)
        instr = q2.get("instructions", "")
        if "\n\n" in instr:
            q2["instructions"] = instr.split("\n\n")[0]
        blind.append(q2)
    return jev_batch("no canon text was provided", blind)

def _summarise_control(answers):
    out = {"quality": 1.0, "novelty": 1.0, "alignment": 1.0, "noul": 0.5}
    for name, ans in answers.items():
        if ans.get("type") == "score":
            level = _score_of(ans)
            if "quality" in name.lower() or name == "q0":
                out["quality"] = level
            elif "novel" in name.lower() or name == "q3":
                out["novelty"] = level
            elif "aligned" in name.lower() or "doctrines" in name.lower() or name == "q4":
                out["alignment"] = level
        elif ans.get("type") == "noul" and name == "q1":
            out["noul"] = ans.get("noul", 0.5)
    return out

def _record_failure(reason, samples=None, detail=None):
    """Record a failed run in the audit log.

    A JEV outage used to exit 0 and append nothing, so a scheduled runner
    recorded the outage as a healthy run and the log looked complete. Failures
    are now first-class entries.
    """
    entry = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "verdict": "ERROR",
        "error": reason,
        "detail": detail,
        "canon_sample_count": len(samples) if samples else 0,
        "canon_titles": [s[0] for s in samples] if samples else [],
        "answers": {},
    }
    log = load_audit_log()
    log["audits"].append(entry)
    save_audit_log(log)
    return entry

def run_once(verbose=True):
    try:
        samples = pick_recent_canon(3)
    except Exception as e:
        print(f"[JEVVY] FATAL: {e}")
        return 2
    if not samples:
        reason = "empty canon sample: refusing to audit a placeholder"
        print(f"[JEVVY] FATAL: {reason}")
        _record_failure(reason)
        witness("audit_failed", {"reason": reason})
        return 2

    canon_state = canon_block(samples)
    questions = build_audit_questions(samples, canon_state)

    response = jev_batch(canon_state, questions)

    if "error" in response:
        reason = "jev_error"
        print(f"[JEVVY] JEV failed: {response['error']}")
        witness("jev_failed", {"error": response["error"]})
        _record_failure(reason, samples, response["error"])
        return 1

    answers = response.get("answers", {})

    control_summary = None
    control_resp = _control_batch(questions)
    if "error" not in control_resp:
        control_summary = _summarise_control(control_resp.get("answers", {}))

    verdict, confidence, avg, advance_prob, c_avg = verdict_from_audit(answers, control_summary)

    try:
        substrate_witness("audit_complete", "jevvy-auditor", {"verdict": verdict, "canon_count": len(samples)})
        substrate_publish("audit_complete", "jevvy-auditor", {"verdict": verdict, "answers": answers}, recipients=["casper-critic"])
    except Exception:
        pass

    audit_entry = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "verdict": verdict,
        "verdict_confidence": confidence,
        "score_avg": round(avg, 4),
        "advance_prob": advance_prob,
        "control_avg": round(c_avg, 4) if c_avg is not None else None,
        "canon_sample_count": len(samples),
        "canon_titles": [s[0] for s in samples],
        "answers": answers,
        "control_answers": control_resp.get("answers", {}) if control_summary is not None else None,
    }

    log = load_audit_log()
    log["audits"].append(audit_entry)
    save_audit_log(log)

    witness("audit_complete", {"verdict": verdict, "canon_count": len(samples), "score_avg": round(avg, 4)})

    if verbose:
        print(f"[JEVVY] verdict: {verdict} (confidence={confidence})")
        if c_avg is not None:
            print(f"  score_avg={avg:.3f}  control_avg={c_avg:.3f}  advance_prob={advance_prob:.2f}")
        for name, ans in answers.items():
            t = ans.get("type")
            v = ans.get(t, "?")
            conf = ans.get("confidence", 0.5)
            if conf is None:
                conf = 0.0
            print(f"  {name} ({t}): {v} (conf={conf:.2f})")
    return 0

def main():
    parser = argparse.ArgumentParser(description="Jevvy the Auditor — JEV quality audit")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "jevvy-auditor", "pid": os.getpid()})
    
    if args.once:
        sys.exit(run_once() or 0)
    elif args.loop:
        while True:
            run_once(verbose=False)
            time.sleep(args.loop)
    else:
        print("Use --once or --loop")
        sys.exit(1)

if __name__ == "__main__":
    main()
