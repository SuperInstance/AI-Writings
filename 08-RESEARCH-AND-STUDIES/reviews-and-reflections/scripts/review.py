#!/usr/bin/env python3
"""
review.py — Have N models review the same code, each from a different language perspective.
"""
import os, sys, json, urllib.request, time
from pathlib import Path

API_TOKEN = os.environ.get('DEEPINFRA_TOKEN')
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

LANGUAGE_REVIEWERS = [
    {"model": "ByteDance/Seed-2.0-mini", "language": "compact", "focus": "What's the smallest correct version?"},
    {"model": "nvidia/NVIDIA-Nemotron-3-Super-120B-A12B", "language": "python", "focus": "Read it as Python. What does this look like ported?"},
    {"model": "nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B", "language": "deep", "focus": "Go as deep as possible. What's the deepest critique?"},
    {"model": "meta-llama/Llama-3.3-70B-Instruct-Turbo", "language": "rust", "focus": "Read it as Rust. What would the borrow checker say?"},
    {"model": "meta-llama/Llama-4-Scout-17B-16E-Instruct", "language": "fresh", "focus": "Fresh eyes. What does a new reader see wrong?"},
    {"model": "Qwen/Qwen3-Next-80B-A3B-Instruct", "language": "next", "focus": "What comes next? What's the version 2?"},
    {"model": "Qwen/Qwen3-Coder-480B-A35B-Instruct-Turbo", "language": "compile", "focus": "Will this compile? Show the diff."},
    {"model": "deepseek-ai/DeepSeek-V3.2", "language": "math", "focus": "Show the math. Where are the formulas hidden?"},
    {"model": "deepseek-ai/DeepSeek-V4-Flash", "language": "fast", "focus": "What ships this weekend?"},
    {"model": "moonshotai/Kimi-K3", "language": "compliance", "focus": "What breaks GDPR? PIPL? Algorithm filing?"},
    {"model": "mistralai/Mistral-Small-3.2-24B-Instruct-2506", "language": "european", "focus": "European perspective. What needs localization?"},
    {"model": "inclusionAI/Ling-3.0-flash", "language": "fresh-eyes", "focus": "Never seen this before. What's obvious?"},
]

def call(model, system, user, max_tokens=1200):
    payload = json.dumps({"model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "max_tokens": max_tokens, "temperature": 0.7}).encode()
    req = urllib.request.Request(API_URL, data=payload, method='POST')
    req.add_header('Authorization', f'Bearer {API_TOKEN}')
    req.add_header('Content-Type', 'application/json')
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read())
                return data['choices'][0]['message']['content']
        except Exception as e:
            if attempt < 2:
                time.sleep(3)
                continue
            return f"[ERROR]: {e}"

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    if Path(target).is_dir():
        code = ""
        for ext in ['*.rs', '*.js', '*.py', '*.ts']:
            for f in Path(target).rglob(ext):
                code += f"=== {f.relative_to(target)} ===\n{f.read_text()}\n\n"
    else:
        code = Path(target).read_text()
    print(f"Reviewing {len(code)} chars from {target}")
    out_dir = Path('reviews')
    out_dir.mkdir(exist_ok=True)
    for r in LANGUAGE_REVIEWERS:
        prompt = f"""You are reviewing code from the perspective of {r['language']}.

**Focus**: {r['focus']}

## Code to review

```
{code[:4000]}
```

Write 300-500 words. Be concrete and actionable.
"""
        out_file = out_dir / f"{r['language']}.md"
        if out_file.exists() and out_file.stat().st_size > 100:
            print(f"  ✓ {r['language']}: cached")
            continue
        result = call(r['model'],
            system=f"You are a senior engineer reviewing code from a {r['language']} perspective.",
            user=prompt)
        out_file.write_text(f"# {r['language']} ({r['model']})\n\n{result}\n")
        print(f"  ✓ {r['language']}: {len(result)} chars")

if __name__ == "__main__":
    main()
