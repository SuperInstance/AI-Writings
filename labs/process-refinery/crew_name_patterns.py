"""Cheap-crew helper: propose pattern NAMES from free-text ledger notes.

Advisory only. The crew (DeepInfra flash models) reads batches of ledger rows and
proposes short kebab-case pattern names + an outcome guess. The output is cached in
crew_patterns.json and the refinery reports it as *proposals*: a proposed name is
adopted only if it agrees with the deterministic rule-classifier (the gate). Metrics
never read crew output.

    python3 crew_name_patterns.py            # needs DEEPINFRA_KEY; writes crew_patterns.json
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import process_refinery as pr  # noqa: E402

BASE = "https://api.deepinfra.com/v1/openai/chat/completions"
CREW = ["deepseek-ai/DeepSeek-V4-Flash", "Qwen/Qwen3.8-Flash", "zai-org/GLM-5.3-Flash"]
SYSTEM = ("You label software-development log rows. For each row, output one JSON line "
          '{"id": <row id>, "patterns": [<1-3 short kebab-case names of the development MOVE used>], '
          '"outcome": "WORKED"|"CLUNKY"|"SCAR"}. Output only JSON lines, nothing else.')


def call(model: str, rows: list[dict]) -> tuple[list[dict], dict]:
    body = "\n".join("%s | %s" % (r["id"], r["text"][:400]) for r in rows)
    req = urllib.request.Request(BASE, data=json.dumps({
        "model": model, "temperature": 0, "max_tokens": 2500,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": body}],
    }).encode(), headers={"Authorization": "Bearer " + os.environ["DEEPINFRA_KEY"].strip(),
                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        out = json.load(resp)
    text = out["choices"][0]["message"].get("content") or ""
    got = []
    for line in text.splitlines():
        line = line.strip().strip(",")
        if line.startswith("{"):
            try:
                got.append(json.loads(line))
            except ValueError:
                pass
    return got, out.get("usage", {})


def main() -> int:
    rows = pr.load_ledger(pr.LEDGER)
    batches = [rows[i:i + 20] for i in range(0, len(rows), 20)]
    proposals, usage = {}, {"prompt_tokens": 0, "completion_tokens": 0, "calls": 0, "failed": 0}
    for bi, batch in enumerate(batches):
        model = CREW[bi % len(CREW)]
        try:
            got, u = call(model, batch)
        except Exception as exc:  # crew is advisory; a failed call is booked, not fatal
            usage["failed"] += 1
            print("batch %d %s failed: %s" % (bi, model, exc), file=sys.stderr)
            continue
        usage["calls"] += 1
        usage["prompt_tokens"] += u.get("prompt_tokens", 0)
        usage["completion_tokens"] += u.get("completion_tokens", 0)
        for g in got:
            if isinstance(g, dict) and "id" in g:
                proposals[str(g["id"])] = {"model": model, "patterns": g.get("patterns", []),
                                           "outcome": g.get("outcome")}
    json.dump({"crew": CREW, "usage": usage, "proposals": proposals},
              open(os.path.join(HERE, "crew_patterns.json"), "w"), indent=1, sort_keys=True)
    print("crew labelled %d/%d rows (%s)" % (len(proposals), len(rows), usage))
    return 0


if __name__ == "__main__":
    sys.exit(main())
