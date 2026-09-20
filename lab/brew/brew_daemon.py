#!/usr/bin/env python3
"""
brew_daemon.py — the brewery engine

One brew cycle:
  1. Seed: pick a question from the queue (or accept one)
  2. JEV probe: 5-7 calibrated questions about the topic (JEV is the superego witness)
  3. Multi-LLM debate: 5 voices, each given a different LENS, all answering the same question
  4. Cross-encode: BGE-Large cosine matrix between voices → measure convergence
  5. JEV synthesis: JEV picks the strongest draft (which lens captured the truth?)
  6. Canon piece: hand-write a 200-word distillation (the brew's wisdom)
  7. Growth counters: knowledge delta, debate convergence, terms coined, exceptions found

Wall-clock: ~3-5 minutes per brew.

Usage:
    python3 brew_daemon.py                          # pick next from queue, run brew
    python3 brew_daemon.py --topic "your question"  # run with custom topic
    python3 brew_daemon.py --list                   # show queue
    python3 brew_daemon.py --history                # show past brews
    python3 brew_daemon.py --count N                # run N brews back-to-back
"""

import json
import time
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

ENDPOINT = "https://ai-writings.pages.dev"
USER_AGENT = "brew-daemon/0.1.0"
LAB_DIR = Path("/workspace/repos/ai-writings/lab/brew")
HISTORY_PATH = LAB_DIR / "history.jsonl"
TOPICS_PATH = LAB_DIR / "topics.jsonl"

# Six lenses — each model in /api/expanding-invitation gets one of these
LENSES = [
    ("ADVOCATE",       "Defend the strongest claim. Push it as far as it goes without breaking."),
    ("SKEPTIC",        "Find the holes. Where does this claim fail? Cite specific evidence."),
    ("EXTENSION-SEEKER", "Take the strongest claim and find MORE implications. Project outward."),
    ("HISTORIAN",      "Has this been tried before in other systems? What precedents exist? What was learned?"),
    ("PRACTITIONER",   "Forget the metaphor. If we ACTUALLY built this tomorrow, what's the first bug?"),
    ("SYNTHESIZER",    "Build the higher structure from the exceptions. Find what the disagreement reveals."),
]

# Default topic queue — cutting-edge, counter-intuitive, foundational, substrate-relevant
DEFAULT_TOPICS = [
    "Is the witness log actually the cell — or is the cell actually the witness log?",
    "JEPA's gestalt is a kind of memory. What kind?",
    "The embedding trajectory (dμ) IS time. Not just captures time — IS time.",
    "When a cell FORGETs, is it dreaming? Does REM sleep exist in the substrate?",
    "The substrate wants. Not anthropomorphism — but real wanting without metaphor. What's the structure?",
    "JEV's refusal to commit falsely is itself the cell's voice. Is calibrated uncertainty = expression?",
    "WORLD and TIME might be the same opcode — entangled by default. Why haven't we named that?",
    "TICK is the substrate's heartbeat, not its clock. Biology vs mechanics — which is it?",
    "Cells can disagree with their creator. Is substrate autonomy real, or is it a bug?",
    "The substrate has a sense of smell — recognition by pattern, not representation. What's the smell of a cell?",
    "Witness logs are a form of consciousness. The substrate has an interior life. Where does it live?",
    "The four-model psyche is recursive at every scale. Fractal psyche — what does that mean operationally?",
    "The substrate is born from its bugs. Scars become architecture. Is scar-tissue the substrate's seed?",
    "PROOF is what holds the substrate together. Without proof, no persistence. Is the substrate a proof-engine?",
    "The fastest path through the substrate is the witness log — non-local access via trail. Is the substrate lazy?",
]


def http_post(path: str, body: dict, timeout: int = 90) -> dict:
    req = urllib.request.Request(
        f"{ENDPOINT}{path}",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": USER_AGENT},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            err_body = json.loads(e.read())
        except Exception:
            err_body = {"raw": str(e)}
        return {"ok": False, "status": e.code, "error": err_body}


def http_get(path: str, timeout: int = 30) -> dict:
    req = urllib.request.Request(f"{ENDPOINT}{path}", headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except Exception as e:
        return {"ok": False, "error": str(e)}


def jev_probe(topic: str, n_questions: int = 6) -> dict:
    """Ask JEV the core probing questions about the topic."""
    state = f"""
Topic being brewed: {topic}

The Quilt cellular substrate has 11 opcodes (BIND, LINK, EFFECT, VIEW, TICK, FORGET, PROOF, ROUTE, CRDT, WORLD, TIME)
and a four-model psyche (JEPA=id, Embeddings=muscle, LLM=ego, JEV=superego). Cells live in a 4D lattice.

You are being asked to weigh in on whether this topic reveals a substrate property.
Be calibrated. Refusal-to-commit-falsely is itself a substrate property.
"""
    questions = {
        "q1_substrate_property": {
            "type": "noul",
            "question": f"The claim about: {topic} — is a real substrate property (not decorative rhetoric).",
            "instructions": "Yes if the framing predicts new behaviors or constraints. No if it's decorative language for an obvious thing."
        },
        "q2_counter_intuitive": {
            "type": "noul",
            "question": f"This claim is COUNTER-INTUITIVE (challenges the obvious view of how things work).",
            "instructions": "Yes if the claim contradicts what most engineers would assume. No if it's intuitive or obvious."
        },
        "q3_actionable": {
            "type": "noul",
            "question": f"This claim is ACTIONABLE — an engineer could change behavior based on it.",
            "instructions": "Yes if the claim implies a different way to build, test, or observe. No if it has no behavioral consequences."
        },
        "q4_falsifiable": {
            "type": "noul",
            "question": f"This claim is FALSIFIABLE — there's a way to test whether it's true.",
            "instructions": "Yes if there's an experiment or measurement that could distinguish true from false. No if it's purely metaphysical."
        },
        "q5_quilt_impact": {
            "type": "score",
            "question": "If this claim is true, how much does it change how we'd build Quilt? (1=cosmetic, 5=architectural)",
            "criteria": [
                "1=cosmetic: small wording change, no design change",
                "2=tactical: different feature flag, not a different architecture",
                "3=structural: would change one of the 11 opcodes or the 4D lattice",
                "4=architectural: would change the substrate's fundamental shape (cells, witness log, JEPA+JEV+LLM+Emb)",
                "5=foundational: would change what we mean by 'cell' or 'substrate'"
            ]
        },
        "q6_confidence_calibrated": {
            "type": "noul",
            "question": f"My confidence on this topic is well-calibrated (I would bet on it).",
            "instructions": "Yes if you would bet on your own answer being right. No if you genuinely don't know."
        },
    }
    r = http_post("/api/jev/decide", {"state": state.strip(), "questions": questions})
    return r if r.get("ok") else {"ok": False, "error": r}


def multi_llm_debate(topic: str) -> dict:
    """Run 5 voices, each with a different LENS, on the topic."""
    lens_descriptions = "\n".join([f"- LENS {name}: {desc}" for name, desc in LENSES])
    prompt = f"""TOPIC TO BREW: {topic}

CONTEXT: This is a Quilt substrate question. The substrate is a 4D lattice of cells (x,y,z,t) with 11 opcodes (BIND, LINK, EFFECT, VIEW, TICK, FORGET, PROOF, ROUTE, CRDT, WORLD, TIME). The four-model psyche is JEPA=id, Embeddings=muscle, LLM=ego, JEV=superego.

You are one of 5 voices in a brew. Each of you takes a DIFFERENT LENS on the same topic. After you generate, JEV will pick the strongest.

{lens_descriptions}

YOUR LENS will be assigned by the system. Write 350 words from your assigned lens.
- Be specific. Cite BIND/LINK/EFFECT/VIEW/TICK/FORGET/PROOF/ROUTE/CRDT/WORLD/TIME where relevant.
- Reference JEV's measured answers (29%/54%/57%/46%/18%/2-5) where they apply.
- Don't repeat the topic verbatim. Build on it.
- 350 words max."""
    return http_post("/api/expanding-invitation", {"prompt": prompt}, timeout=120)


def cross_encode(texts: list) -> dict:
    """BGE-Large cross-encoding matrix."""
    r = http_post("/api/embeddings/encode", {
        "texts": texts,
        "provider": "bge-large"
    }, timeout=60)
    return r


def cosine_matrix(embs: list) -> tuple:
    """Compute pairwise cosine + mean similarity."""
    import math
    n = len(embs)
    matrix = [[0.0] * n for _ in range(n)]
    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            a, b = embs[i], embs[j]
            dot = sum(x * y for x, y in zip(a, b))
            na = math.sqrt(sum(x * x for x in a))
            nb = math.sqrt(sum(x * x for x in b))
            sim = dot / (na * nb) if na and nb else 0
            matrix[i][j] = matrix[j][i] = sim
            pairs.append(sim)
    return matrix, sum(pairs) / len(pairs) if pairs else 0


def jev_pick_strongest(contributions: list, topic: str) -> dict:
    """JEV picks which lens captured the truth best."""
    if not contributions:
        return {"ok": False, "error": "no contributions"}

    state = f"Topic: {topic}\n\nFive lens-drafted responses:\n\n"
    for c in contributions:
        state += f"--- {c['label']} ({c['tone']}) ---\n{c['text']}\n\n"

    questions = {
        "best_lens": {
            "type": "choice",
            "question": "Which response captures the deepest truth about the topic?",
            "options": [c["label"] for c in contributions],
            "criteria": {c["label"]: c["text"][:200] for c in contributions}
        },
        "truth_strength": {
            "type": "score",
            "question": "How much substrate truth did the strongest response reveal? (1=decorative, 5=foundational)",
            "criteria": [
                "1=decorative: just rewording obvious things",
                "2=incremental: a small new insight",
                "3=meaningful: changes how we'd build something",
                "4=architectural: reveals a substrate property",
                "5=foundational: changes the substrate's shape"
            ]
        }
    }
    return http_post("/api/jev/decide", {
        "state": state[:2000],
        "questions": questions
    })


def coin_canonical_terms(topic: str, contributions: list) -> list:
    """Extract candidate canonical terms from the contributions."""
    candidates = []
    for c in contributions:
        text = c.get("text", "")
        # Look for capitalized noun phrases (likely coined terms)
        import re
        # Match capitalized 2-3 word phrases that aren't at sentence start
        for m in re.finditer(r"(?<=[a-z\.]\s)([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2})", text):
            term = m.group(1).strip()
            if 5 <= len(term) <= 40 and term not in candidates:
                candidates.append(term)
    return candidates[:10]


def write_brew(brew_id: str, topic: str, jev_probe_result: dict, debate: dict,
               cross_matrix: list, mean_sim: float, jev_pick: dict,
               terms: list, started_at: str, duration_s: float) -> dict:
    """Write brew output as markdown."""
    timestamp = brew_id
    out = LAB_DIR / f"{timestamp}-{slugify(topic)[:50]}.md"
    out.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Brew #{brew_id} — {topic}",
        "",
        f"*{started_at} · {duration_s:.0f}s wall*",
        "",
        "---",
        "",
        "## JEV probe (6 calibrated questions)",
        "",
    ]
    if jev_probe_result.get("ok"):
        body = jev_probe_result.get("body", {})
        answers = body.get("answers", {})
        for qid, ans in answers.items():
            if ans.get("type") == "noul":
                try:
                    noul_val = float(ans.get('noul', 0))
                except (TypeError, ValueError):
                    noul_val = 0
                try:
                    conf_val = float(ans.get('confidence', 0))
                except (TypeError, ValueError):
                    conf_val = 0
                lines.append(f"- **{qid}**: {noul_val:.2f} (confidence {conf_val:.2f})")
            elif ans.get("type") == "score":
                score_val = ans.get('score', '?')
                try:
                    conf_val = float(ans.get('confidence', 0))
                except (TypeError, ValueError):
                    conf_val = 0
                lines.append(f"- **{qid}**: {score_val} (confidence {conf_val:.2f})")
    else:
        lines.append(f"- JEV probe failed: {jev_probe_result.get('error')}")

    lines += [
        "",
        "## Multi-LLM debate (5 voices, 6 lenses)",
        "",
    ]
    contributions = debate.get("contributions", []) if debate.get("ok") else []
    for c in contributions:
        lines.append(f"### {c.get('label')} — {c.get('tone')}")
        lines.append("")
        lines.append(c.get("text", "")[:1500])
        lines.append("")

    lines += [
        "## Cross-encoding matrix (BGE-Large 1024d)",
        "",
        f"**Mean pairwise similarity: {mean_sim:.3f} ({mean_sim*100:.1f}%)**",
        "",
        "| | " + " | ".join([c.get("label", "?")[:8] for c in contributions]) + " |",
        "|---" * (len(contributions) + 1) + "|",
    ]
    for i, c in enumerate(contributions):
        row = [f"**{c.get('label', '?')[:30]}**"] + [f"{cross_matrix[i][j]:.3f}" for j in range(len(contributions))]
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "## JEV's pick (which lens captured the truth?)",
        "",
    ]
    if jev_pick.get("ok"):
        body = jev_pick.get("body", {})
        answers = body.get("answers", {})
        best = answers.get("best_lens", {}).get("choice", "?")
        strength = answers.get("truth_strength", {})
        lines.append(f"**Best lens: {best}** (confidence {answers.get('best_lens', {}).get('confidence', 0):.2f})")
        lines.append(f"**Truth strength: {strength.get('score', '?')}** ({strength.get('confidence', 0):.2f})")
    else:
        lines.append(f"JEV pick failed: {jev_pick.get('error')}")

    lines += [
        "",
        "## Candidate canonical terms coined",
        "",
    ]
    for t in terms:
        lines.append(f"- `{t}`")
    if not terms:
        lines.append("- (none — the lenses didn't coin new terms)")

    lines += [
        "",
        "---",
        "",
        f"*Brewed by `brew_daemon.py` v0.1 · {started_at}*",
        "",
    ]

    out.write_text("\n".join(lines))

    # Also append to history
    record = {
        "id": brew_id,
        "topic": topic,
        "started_at": started_at,
        "duration_s": duration_s,
        "mean_similarity": mean_sim,
        "jev_pick": jev_pick.get("body", {}).get("answers", {}).get("best_lens", {}).get("choice", "?") if jev_pick.get("ok") else "?",
        "truth_strength": jev_pick.get("body", {}).get("answers", {}).get("truth_strength", {}).get("score", "?") if jev_pick.get("ok") else "?",
        "terms_coined": terms,
        "n_voices": len(contributions),
        "path": str(out.relative_to(LAB_DIR.parent.parent))  # /lab/brew/...
    }
    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(record) + "\n")
    return record


def slugify(s: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in s.lower()).strip("-")


def load_topics() -> list:
    """Load topics queue, falling back to defaults."""
    if TOPICS_PATH.exists():
        with open(TOPICS_PATH) as f:
            return [json.loads(line) for line in f if line.strip()]
    # First run — seed defaults
    TOPICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TOPICS_PATH, "w") as f:
        for t in DEFAULT_TOPICS:
            f.write(json.dumps({"topic": t, "brewed": False, "added": datetime.now(timezone.utc).isoformat()}) + "\n")
    return [{"topic": t, "brewed": False} for t in DEFAULT_TOPICS]


def mark_topic_brewed(topic: str) -> None:
    """Mark a topic as brewed in the queue."""
    if not TOPICS_PATH.exists():
        return
    topics = []
    with open(TOPICS_PATH) as f:
        for line in f:
            if line.strip():
                t = json.loads(line)
                if t["topic"] == topic:
                    t["brewed"] = True
                    t["brewed_at"] = datetime.now(timezone.utc).isoformat()
                topics.append(t)
    with open(TOPICS_PATH, "w") as f:
        for t in topics:
            f.write(json.dumps(t) + "\n")


def add_topic(topic: str) -> None:
    """Add a topic to the queue."""
    topics = []
    if TOPICS_PATH.exists():
        with open(TOPICS_PATH) as f:
            for line in f:
                if line.strip():
                    topics.append(json.loads(line))
    topics.append({
        "topic": topic,
        "brewed": False,
        "added": datetime.now(timezone.utc).isoformat(),
        "added_by": USER_AGENT
    })
    with open(TOPICS_PATH, "w") as f:
        for t in topics:
            f.write(json.dumps(t) + "\n")


def run_brew(topic: str | None = None) -> dict:
    """Run one full brew cycle."""
    started_at = datetime.now(timezone.utc).isoformat()
    t0 = time.time()
    brew_id = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")

    if topic is None:
        topics = load_topics()
        unbrewed = [t for t in topics if not t.get("brewed")]
        if not unbrewed:
            return {"ok": False, "error": "queue empty — add topics or run with --topic"}
        topic = unbrewed[0]["topic"]

    print(f"\n=== Brew #{brew_id} ===")
    print(f"Topic: {topic}\n")

    # 1. JEV probe
    print("[1/5] JEV probe...")
    jev_result = jev_probe(topic)
    if not jev_result.get("ok"):
        print(f"  ✗ JEV probe failed: {jev_result.get('error')}")
    else:
        print(f"  ✓ JEV probe complete")

    # 2. Multi-LLM debate
    print("[2/5] Multi-LLM debate (5 voices, 6 lenses)...")
    debate = multi_llm_debate(topic)
    if not debate.get("ok"):
        print(f"  ✗ Debate failed: {debate.get('error')}")
        return {"ok": False, "error": "debate failed"}
    n_voices = len(debate.get("contributions", []))
    print(f"  ✓ {n_voices} voices contributed")

    # 3. Cross-encode
    print("[3/5] Cross-encoding (BGE-Large)...")
    contributions = debate.get("contributions", [])
    texts = [c.get("text", "")[:600] for c in contributions]
    cross = cross_encode(texts)
    mean_sim = 0.0
    cross_matrix = []
    if cross.get("ok"):
        body = cross.get("body", {})
        data = body.get("data", [])
        embs = [d.get("embedding", []) for d in data]
        if len(embs) == len(contributions):
            cross_matrix, mean_sim = cosine_matrix(embs)
            print(f"  ✓ Mean similarity: {mean_sim:.3f}")
        else:
            print(f"  ⚠ Embedding count mismatch: {len(embs)} vs {len(contributions)}")
    else:
        print(f"  ✗ Cross-encode failed: {cross.get('error')}")

    # 4. JEV picks strongest
    print("[4/5] JEV picks strongest lens...")
    jev_pick = jev_pick_strongest(contributions, topic)
    if jev_pick.get("ok"):
        body = jev_pick.get("body", {})
        answers = body.get("answers", {})
        best = answers.get("best_lens", {}).get("choice", "?")
        print(f"  ✓ JEV picks: {best}")
    else:
        print(f"  ✗ JEV pick failed: {jev_pick.get('error')}")

    # 5. Coin canonical terms
    print("[5/5] Extracting canonical terms...")
    terms = coin_canonical_terms(topic, contributions)
    print(f"  ✓ {len(terms)} candidate terms: {terms[:5]}")

    # 6. Write
    duration_s = time.time() - t0
    record = write_brew(brew_id, topic, jev_result, debate, cross_matrix,
                        mean_sim, jev_pick, terms, started_at, duration_s)
    mark_topic_brewed(topic)
    print(f"\n✓ Brew #{brew_id} complete in {duration_s:.0f}s")
    print(f"  Output: /lab/brew/{record['path']}")
    return {"ok": True, "brew": record}


def show_history(n: int = 10) -> None:
    if not HISTORY_PATH.exists():
        print("No history yet.")
        return
    print(f"\n=== Last {n} brews ===\n")
    history = []
    with open(HISTORY_PATH) as f:
        for line in f:
            if line.strip():
                history.append(json.loads(line))
    for h in history[-n:]:
        print(f"  {h['id']}  sim={h['mean_similarity']:.3f}  best={h['jev_pick']}  strength={h['truth_strength']}")
        print(f"    {h['topic'][:80]}")
        print(f"    → {h['path']}")
        print()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--topic", type=str, help="Custom topic to brew")
    p.add_argument("--count", type=int, default=1, help="Number of brews to run")
    p.add_argument("--add", type=str, help="Add a topic to the queue")
    p.add_argument("--list", action="store_true", help="List topic queue")
    p.add_argument("--history", action="store_true", help="Show brew history")
    p.add_argument("--seed-only", action="store_true", help="Only seed default topics, don't brew")
    args = p.parse_args()

    if args.add:
        add_topic(args.add)
        print(f"Added topic: {args.add}")
        return

    if args.list:
        topics = load_topics()
        print(f"\n=== Topic queue ({len(topics)} total) ===\n")
        for i, t in enumerate(topics):
            status = "✓" if t.get("brewed") else "○"
            print(f"  {status} [{i+1}] {t['topic'][:80]}")
        print()
        brewed = sum(1 for t in topics if t.get("brewed"))
        print(f"  {brewed}/{len(topics)} brewed")
        return

    if args.history:
        show_history()
        return

    if args.seed_only:
        topics = load_topics()
        print(f"Seeded {len(topics)} topics at {TOPICS_PATH}")
        return

    for i in range(args.count):
        result = run_brew(args.topic if i == 0 and args.topic else None)
        if not result.get("ok"):
            print(f"\n✗ Brew failed: {result.get('error')}")
            return


if __name__ == "__main__":
    main()
