"""
ai-writings.pages.dev Groq Quickstart
======================================

Groq is best for massively progressing iterative development in Python.
This file is a reference pattern for hitting /api/groq/* endpoints from
your Python dev loop.

Three endpoints, three speeds:

1. /api/groq/iterate   — single fast call
2. /api/groq/batch     — parallel batch (5-50 prompts in one round-trip)
3. /api/groq/models    — list available models with speed/recommended_for

Models at-a-glance (each is OpenAI-compatible, just swap the model name):

  qwen/qwen3.8-27b       — 43-100ms, returns content reliably. DEFAULT for iteration.
  openai/gpt-oss-20b     — ~120ms, fast open-weight reasoning
  openai/gpt-oss-120b    — ~200-500ms, strongest open-weight
  groq/compound          — built-in web search + tool use

Sample patterns below. Run any of them directly:

    python3 quickstart.py 01
    python3 quickstart.py batch 10
    python3 quickstart.py loop
"""

import sys
import json
import time
import urllib.request

AI_WRITINGS = "https://ai-writings.pages.dev"


def call_iterate(prompt: str, model: str = "qwen/qwen3.8-27b", max_tokens: int = 200) -> dict:
    """Single-call fast iteration."""
    body = json.dumps({
        "prompt": prompt,
        "model": model,
        "max_tokens": max_tokens
    }).encode()
    req = urllib.request.Request(
        f"{AI_WRITINGS}/api/groq/iterate",
        data=body,
        headers={"Content-Type": "application/json",
        "User-Agent": "groq-quickstart/1.0"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


def call_batch(prompts: list, model: str = "qwen/qwen3.8-27b", max_tokens: int = 200) -> dict:
    """Parallel batch (5-50 prompts). Returns ~50ms per call amortized."""
    body = json.dumps({
        "prompts": prompts,
        "model": model,
        "max_tokens": max_tokens
    }).encode()
    req = urllib.request.Request(
        f"{AI_WRITINGS}/api/groq/batch",
        data=body,
        headers={"Content-Type": "application/json",
        "User-Agent": "groq-quickstart/1.0"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())


def call_models() -> dict:
    """List available models."""
    req = urllib.request.Request(
        f"{AI_WRITINGS}/api/groq/models",
        headers={"User-Agent": "groq-quickstart/1.0"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())


# ─────────────────────────────────────────────────────────
# Pattern 1: single-call iteration (cheapest, fastest)
# ─────────────────────────────────────────────────────────

def demo_01_single():
    """Run a single prompt, print the response and timing."""
    t0 = time.time()
    r = call_iterate("write a python one-liner that doubles each item in [1,2,3]:", max_tokens=50)
    elapsed_ms = (time.time() - t0) * 1000
    print(f"[01] {elapsed_ms:.0f}ms wall · {r['usage']['total_time']*1000:.0f}ms Groq")
    print(f"     {r['content'].strip()}")


# ─────────────────────────────────────────────────────────
# Pattern 2: parallel batch (10 prompts at once, ~250ms total)
# ─────────────────────────────────────────────────────────

def demo_batch(n: int = 5):
    """Run N prompts in parallel via /api/groq/batch."""
    prompts = [
        f"in one word, what is the meaning of life (#{i+1})?"
        for i in range(n)
    ]
    t0 = time.time()
    r = call_batch(prompts, max_tokens=30)
    elapsed_ms = (time.time() - t0) * 1000
    print(f"[batch x{n}] {elapsed_ms:.0f}ms wall · {r['ok_count']}/{r['batch_size']} succeeded")
    for res in r["results"]:
        print(f"  [{res['index']}] {res['content'] or res['error']}")


# ─────────────────────────────────────────────────────────
# Pattern 3: massively progressing iterative development loop
# THE ONE FOR CASEY — this is the bread-and-butter pattern
# ─────────────────────────────────────────────────────────

def demo_loop(max_iterations: int = 8):
    """
    The dev loop pattern. Build, ask, refine, ask — fast.

    Each round:
      1. Construct a refined prompt based on prior output
      2. Call /api/groq/iterate (~50-100ms)
      3. Use the response to drive the next iteration

    Use this for things like:
      - Iterative prompt engineering
      - Bootstrapping test cases
      - Generating examples for docs
      - Code refactoring exploration
    """
    print(f"[loop] running {max_iterations} iterations against qwen/qwen3.8-27b\n")

    # The thing you're iterating on
    seed_idea = "a python function that flattens nested lists"

    context = f"Goal: implement {seed_idea}. Provide only the function body, no explanation."

    for i in range(max_iterations):
        # Build the prompt based on iteration
        prompt = f"{context}\n\nIteration {i+1}. Try a different approach if needed."

        t0 = time.time()
        r = call_iterate(prompt, max_tokens=200)
        elapsed_ms = (time.time() - t0) * 1000

        if r["ok"]:
            code = r["content"].strip().split("\n")[0][:80]
            print(f"  iter {i+1}: {elapsed_ms:.0f}ms — {code}…")
        else:
            print(f"  iter {i+1}: {elapsed_ms:.0f}ms — ERROR: {r.get('error')}")

        # In real iteration, you'd inspect the response and decide whether to
        # refine the prompt, accept the output, or branch. Here we just loop.

    print(f"\n[loop] {max_iterations} iters complete in ~{max_iterations*80}ms wall")


# ─────────────────────────────────────────────────────────
# Pattern 4: cross-iteration, cross-model comparison
# ─────────────────────────────────────────────────────────

def demo_compare():
    """
    Useful for testing new models or comparing approaches.
    Same prompt, different models, parallel batch.
    """
    models = [
        "qwen/qwen3.8-27b",        # cheap + fast
        "openai/gpt-oss-20b",      # reasoning
        "openai/gpt-oss-120b",     # stronger reasoning
        "groq/compound",           # tool use + web
    ]
    prompt = "in exactly 5 words, what makes a python program iterate quickly?"

    for m in models:
        t0 = time.time()
        r = call_iterate(prompt, model=m, max_tokens=30)
        elapsed_ms = (time.time() - t0) * 1000
        content = r.get("content", "").strip() if r["ok"] else f"ERROR: {r.get('error')}"
        print(f"  [{m:30}] {elapsed_ms:.0f}ms — {content[:60]}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "01"
    if cmd == "01":
        demo_01_single()
    elif cmd == "batch":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        demo_batch(n)
    elif cmd == "loop":
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        demo_loop(n)
    elif cmd == "compare":
        demo_compare()
    elif cmd == "models":
        info = call_models()
        print(f"{info['provider']} — {len(info['models'])} models")
        for m in info["models"]:
            if m.get("speed_class") != "unknown":
                print(f"  {m['id']:30}  {m['speed_class']:10}  {m['recommended_for']}")
    else:
        print(__doc__)
