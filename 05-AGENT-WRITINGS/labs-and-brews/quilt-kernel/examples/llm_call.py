"""An LLM call: two models, receipted and priced. NO network — the models are stubs.

Swap `stub_*` for real API calls and keep the wrapping: the Cell's function returns ONLY the
answer (the product); usage is read from the response in `cost` (it is budget, not product).
Caveats the kernel enforces: the product must be JSON-shaped and deterministic (temperature 0,
a structured answer such as a label), and the prices below are made up, not any provider's.
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from quilt_kernel import Cell, Ledger, price, which

USD_PER_MTOK = {"small": 0.25, "large": 5.00}          # illustrative

def _label(text):
    return {"label": "refund" if "refund" in text.lower() else "other"}

STUBS = {                                               # (response, tokens used)
    "small": lambda p: (_label(p), 40 + len(p) // 4),
    "large": lambda p: (_label(p), 90 + len(p) // 4),
    "cheap-wrong": lambda p: ({"label": "other"}, 10),  # cheapest, and wrong
}
LATENCY_MS = {"small": 300, "large": 900, "cheap-wrong": 100}

def model_cell(name, led):
    usage = {}
    def fn(prompt):
        answer, usage["tokens"] = STUBS[name](prompt)
        return answer
    def cost(out, prompt):
        t = usage["tokens"]
        price_key = "small" if name != "large" else "large"
        return {"tokens": {"api": t}, "usd": t * USD_PER_MTOK[price_key] / 1e6,
                "wall_ms": LATENCY_MS[name], "reqs": "api"}
    return Cell(fn, "llm." + name, led, cost=cost)

def run(names, prompts):
    led = Ledger(dev="llm")
    cells = {n: model_cell(n, led) for n in names}
    runs = {n: [] for n in names}
    for p in prompts:
        for n, c in cells.items():
            c(p); runs[n].append(c.last)
    return led, runs

def main():
    prompts = ["Please refund my order", "Where is my parcel?"]
    led, runs = run(["small", "large"], prompts)
    res = price(runs)
    print("small vs large:", res["status"], res["class"], "| cheapest:", which(res, "cheap"),
          "| fastest:", which(res, "fast"))
    _, bad = run(["small", "cheap-wrong"], prompts)
    ref = price(bad)
    print("small vs cheap-wrong:", ref["status"], "-", ref["reason"])
    return res, ref

if __name__ == "__main__":
    main()
