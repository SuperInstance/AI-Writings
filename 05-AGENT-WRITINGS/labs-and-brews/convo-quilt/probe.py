"""probe — which models actually answer? Writes probe.json. Run: python3 probe.py
Never trust a catalog listing: a model counts as WORKING only if a 1-line chat returned text."""
import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import providers as P

ASKED = [("deepinfra", m) for m in (
    "tencent/Hy3", "thinkingmachines/Inkling-Small", "nvidia/NVIDIA-Nemotron-3.5-Lightning",
    "meta-models/Muse-Glimmer-30B", "inclusionAI/Ling-3.0-flash", "ibm-granite/granite-4.2-30b",
    "Qwen/Qwen3.8-Flash", "XiaomiMiMo/MiMo-V2.6-Pro")]
EXTRA = [("deepinfra", m) for m in (
    "deepseek-ai/DeepSeek-V4-Flash", "zai-org/GLM-5.3-Flash", "moonshotai/Kimi-K3",
    "Qwen/Qwen3.8-27B", "google/gemma-4-31B-it", "openai/gpt-oss-120b", "XiaomiMiMo/MiMo-V2.6-Flash",
    "thinkingmachines/Inkling")] + [
    ("zai", "glm-4.6"), ("zai", "glm-5.3-flash"), ("zai", "glm-5.3"),
    ("zai-coding", "glm-4.6"), ("zai-coding", "glm-5.3"),
    ("kimi", "kimi-k3"), ("kimi", "kimi-k2.6"), ("kimi", "kimi-latest"),
    ("deepseek", "deepseek-chat"), ("groq", "llama-3.3-70b-versatile"), ("groq", "openai/gpt-oss-120b"), ("groq", "qwen/qwen3.8-27b")]
Q = [{"role": "user", "content": "Reply with exactly one short sentence naming one color."}]


def one(pm):
    prov, model = pm
    retried = False
    try:
        try:
            r = P.chat(prov, model, Q, max_tokens=300, temperature=0.2, timeout=60)
        except P.ProviderError as e:   # reasoning models: resolves, but thinks past a small budget
            if "empty content" not in str(e):
                raise
            retried = True
            r = P.chat(prov, model, Q, max_tokens=2500, temperature=0.2, timeout=120)
        return {"retried_2500": retried, "provider": prov, "model": model, "ok": True, "wall_ms": r["wall_ms"],
                "tokens": r["tokens"], "sample": r["text"][:80]}
    except P.ProviderError as e:
        return {"provider": prov, "model": model, "ok": False, "error": str(e)[:160]}


if __name__ == "__main__":
    with ThreadPoolExecutor(12) as ex:
        rows = list(ex.map(one, ASKED + EXTRA))
    try:
        j = P.jev("A cheap model proposed a new projection for ASCII frames.",
                  {"ideation": {"type": "score", "instructions": "How generative is this turn?",
                    "criteria": ["stuck", "flat", "useful", "generative", "breakthrough"]}})
        jev = {"ok": "error" not in j, "shape": json.dumps(j)[:300]}
    except P.ProviderError as e:
        jev = {"ok": False, "error": str(e)}
    try:
        idx, job, heads = P.moth_draw(5)
        moth = {"ok": True, "job": job, "heads_of_64": heads, "draw_mod5": idx}
    except P.ProviderError as e:
        moth = {"ok": False, "error": str(e)}
    out = {"probed_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "asked": [r for r in rows[:len(ASKED)]],
           "extra": rows[len(ASKED):], "jev": jev, "moth": moth,
           "working": [r["provider"] + ":" + r["model"] for r in rows if r["ok"]]}
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe.json"), "w"), indent=1)
    for r in rows:
        print("%-4s %-11s %-42s %s" % ("OK" if r["ok"] else "FAIL", r["provider"], r["model"],
                                      r.get("sample", r.get("error", ""))[:70]))
    print("JEV", jev); print("MOTH", moth)
