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
BOOKKEEPER_PATH = Path("/workspace/repos/ai-writings/bots/jevvy-auditor/bookkeeper.wal")

def witness(event_type, payload):
    WITNESS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with WITNESS_PATH.open("a") as f:
        entry = {
            "ts": time.time(),
            "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "event": event_type,
            "payload": payload,
            "hash": hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16],
        }
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
    if not CANON_DIR.exists():
        return []
    files = sorted(CANON_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return [(f.stem, f.read_text()[:200]) for f in files[:n] if f.exists()]

def build_audit_questions(samples):
    """Build 5-7 audit questions about recent canon"""
    if not samples:
        samples = [("empty canon", "no content yet")]
    
    canon_summary = "; ".join(f"{name}: {content[:100]}" for name, content in samples[:3])
    
    return [
        {"type": "score", "instructions": f"How high is the quality of this canon? '{canon_summary[:150]}'", "criteria": ["poor", "mediocre", "good", "excellent", "landmark"]},
        {"type": "noul", "instructions": "Does this canon advance the cellular-first substrate?"},
        {"type": "noul", "instructions": "Is this canon worth keeping (not waste)?"},
        {"type": "score", "instructions": "How novel is this canon vs prior canon?", "criteria": ["redundant", "incremental", "novel", "highly-novel", "groundbreaking"]},
        {"type": "score", "instructions": "How aligned is this canon with the substrate's core doctrines (cells, bookkeeper, ternary, JEPA, FEP)?", "criteria": ["misaligned", "partial", "aligned", "tightly-aligned", "embodies-doctrine"]},
        {"type": "choice", "instructions": "What is the biggest risk in this canon?", "criteria": {"low-quality": "low-quality", "redundant": "redundant", "off-topic": "off-topic", "too-abstract": "too-abstract", "none": "no significant risk"}},
    ]

def verdict_from_audit(answers):
    """Convert JEV answers to verdict"""
    # Find quality score
    quality_score = 1.0
    novelty_score = 1.0
    advance_prob = 0.5
    aligned_score = 1.0
    
    for name, ans in answers.items():
        if ans.get("type") == "score":
            crit = ans.get("score", {})
            if isinstance(crit, dict):
                level = crit.get("level", 1)
            else:
                level = crit
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
    
    if avg >= 3.5 and advance_prob > 0.7:
        return "PASS"
    elif avg >= 2.5:
        return "CAUTION"
    else:
        return "FAIL"

def run_once(verbose=True):
    samples = pick_recent_canon(3)
    questions = build_audit_questions(samples)
    canon_state = "; ".join(f"{n}: {c[:80]}" for n, c in samples[:3]) if samples else "empty canon"
    
    response = jev_batch(canon_state, questions)
    
    if "error" in response:
        witness("jev_failed", {"error": response["error"]})
        if verbose: print(f"[JEVVY] JEV failed: {response['error']}")
        return
    
    answers = response.get("answers", {})
    verdict = verdict_from_audit(answers)
    
    audit_entry = {
        "ts": time.time(),
        "iso": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "verdict": verdict,
        "canon_sample_count": len(samples),
        "canon_titles": [s[0] for s in samples],
        "answers": answers,
    }
    
    log = load_audit_log()
    log["audits"].append(audit_entry)
    save_audit_log(log)
    
    witness("audit_complete", {"verdict": verdict, "canon_count": len(samples)})
    
    if verbose:
        print(f"[JEVVY] verdict: {verdict}")
        for name, ans in answers.items():
            t = ans.get("type")
            v = ans.get(t, "?")
            conf = ans.get("confidence", 0.5)
            print(f"  {name} ({t}): {v} (conf={conf:.2f})")

def main():
    parser = argparse.ArgumentParser(description="Jevvy the Auditor — JEV quality audit")
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--loop", type=int)
    args = parser.parse_args()
    
    witness("bot_started", {"bot": "jevvy-auditor", "pid": os.getpid()})
    
    if args.once:
        run_once()
    elif args.loop:
        while True:
            run_once(verbose=False)
            time.sleep(args.loop)
    else:
        print("Use --once or --loop")
        sys.exit(1)

if __name__ == "__main__":
    main()
