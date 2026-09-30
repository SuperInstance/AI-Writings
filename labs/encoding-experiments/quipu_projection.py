"""E6 quipu_projection — counterintuitive projection alphabets for a numeric feed, read back by an LLM.

Gems: quipu-math (Incan knotted-cord positional decimal: long knots for units, single
knots for higher positions, absence = 0; digit-sum checksum), ternary-* (balanced
ternary), and Syzygy's own glyph/braille projection.

Question: when a numeric feed (here: wall_ms values from E1's ActiveLog) is PROJECTED to
text for a model to read, which alphabet survives the round-trip through the model?
Each alphabet gets the same legend-in-prompt treatment; the model must decode the feed
back to decimal. We measure exact-value recall, and prompt tokens (cost).

Alphabets:
  decimal   "135"
  quipu     "o|ooo|LLLLL"   high->low positions; higher positions = single knots 'o' x d,
                            units = long knot 'L' x d (1 = figure-eight '8'); 0 = '_'
  braille   Unicode braille digits (⠁⠃⠉⠙⠑⠋⠛⠓⠊⠚), the Syzygy-adjacent projection
  trit      balanced ternary with '+', '0', '-' (most significant first)

Offline part (no API): the quipu digit-sum checksum vs Luhn vs ISBN-style mod-11, on
single-digit substitutions and adjacent transpositions.

Run: python3 quipu_projection.py            (uses cached LLM answers; calls DeepInfra on a miss)
     python3 quipu_projection.py --selftest (offline)
"""
from __future__ import annotations
import json, re, sys
import common as C

BRAILLE = "⠚⠁⠃⠉⠙⠑⠋⠛⠓⠊"  # 0..9


def to_quipu(n: int) -> str:
    ds = str(n)
    out = []
    for k, ch in enumerate(ds):
        d = int(ch)
        units = k == len(ds) - 1
        if d == 0:
            out.append("_")
        elif units:
            out.append("8" if d == 1 else "L" * d)
        else:
            out.append("o" * d)
    return "|".join(out)


def from_quipu(s: str) -> int:
    v = 0
    for g in s.split("|"):
        v = v * 10 + (0 if g == "_" else 1 if g == "8" else len(g))
    return v


def to_braille(n):
    return "".join(BRAILLE[int(c)] for c in str(n))


def from_braille(s):
    return int("".join(str(BRAILLE.index(c)) for c in s))


def to_trit(n):
    if n == 0:
        return "0"
    out = []
    while n:
        r = n % 3
        n //= 3
        if r == 2:
            r = -1
            n += 1
        out.append("+0-"[1 - r] if r != 0 else "0")
    return "".join(reversed(out))


def from_trit(s):
    v = 0
    for ch in s:
        v = v * 3 + {"+": 1, "0": 0, "-": -1}[ch]
    return v


ALPHABETS = {
    "decimal": (str, int, "Each value is written in ordinary decimal digits."),
    "quipu": (to_quipu, from_quipu,
              "Each value is an Incan quipu cord written left to right from the highest decimal position to the units. "
              "Positions are separated by '|'. In a higher position, the digit d is written as d single knots 'o' "
              "(e.g. 'ooo' = 3). In the units position, digit d>=2 is a long knot of d turns written 'L' repeated d times "
              "(e.g. 'LLLLL' = 5) and digit 1 is a figure-eight knot '8'. An empty position (digit 0) is '_'. "
              "Example: 'o|ooo|LLLLL' = 135, 'oo|_|8' = 201."),
    "braille": (to_braille, from_braille,
                "Each value is written in Unicode braille digits: ⠁=1 ⠃=2 ⠉=3 ⠙=4 ⠑=5 ⠋=6 ⠛=7 ⠓=8 ⠊=9 ⠚=0, "
                "most significant digit first. Example: ⠁⠉⠑ = 135."),
    "trit": (to_trit, from_trit,
             "Each value is written in balanced ternary, most significant trit first, with '+' = +1, '0' = 0, "
             "'-' = -1 and place values 1, 3, 9, 27, 81, 243, ... Example: '+-0' = 9 - 3 + 0 = 6, '+0-' = 9 - 1 = 8."),
}


def feeds(k=5, m=10):
    import delta_budget as E1
    recs = E1.build_log(k * m * 5, seed=21)
    vals = [r["body"]["budget"]["wall_ms"] for r in recs if r["body"]["cell"] in ("stt", "llm", "mic")]
    return [vals[i * m:(i + 1) * m] for i in range(k)]


def prompt_for(name, feed):
    enc, _, legend = ALPHABETS[name]
    body = "\n".join(f"{i + 1}. {enc(v)}" for i, v in enumerate(feed))
    return (f"You are decoding a telemetry feed. {legend}\n\nFeed ({len(feed)} values):\n{body}\n\n"
            f"Decode every value to an ordinary decimal integer. Answer with ONLY a JSON array of "
            f"{len(feed)} integers in order, nothing else.")


def parse_ints(text, n):
    m = re.search(r"\[[^\]]*\]", text, re.S)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
        return [int(x) for x in arr][:n]
    except Exception:
        return [int(x) for x in re.findall(r"-?\d+", m.group(0))][:n]


MODELS = ["meta-llama/Meta-Llama-3.1-8B-Instruct", "deepseek-ai/DeepSeek-V3"]


def measure_llm(log=print):
    fs = feeds()
    res = {}
    for model in MODELS:
        for name in ALPHABETS:
            hit = tot = ptoks = 0
            for feed in fs:
                try:
                    out = C.chat(prompt_for(name, feed), model=model, max_tokens=200)
                except Exception as e:  # a missing model is a recorded result, not a crash
                    res[f"{model}|{name}"] = {"error": str(e)[:120]}
                    break
                got = parse_ints(out["text"], len(feed))
                hit += sum(1 for a, b in zip(got, feed) if a == b)
                tot += len(feed)
                ptoks += out["usage"].get("prompt_tokens", 0)
            else:
                res[f"{model}|{name}"] = {"exact": round(hit / tot, 3), "values": tot,
                                          "prompt_tokens_per_feed": ptoks // len(fs)}
            r = res[f"{model}|{name}"]
            log(f"  {model.split('/')[-1]:28s} {name:8s} " + (f"exact {r['exact']:.3f} ({r['values']} values)  prompt tokens/feed {r['prompt_tokens_per_feed']}" if "exact" in r else r["error"]))
    return res


# ---------------- offline: check digits ----------------------------------------------------
def quipu_checksum(n):
    return sum(int(c) for c in str(n))


def luhn(n):
    s, dbl = 0, False
    for c in reversed(str(n)):
        d = int(c)
        if dbl:
            d = d * 2 - 9 if d * 2 > 9 else d * 2
        s += d
        dbl = not dbl
    return s % 10


def mod11(n):
    ds = str(n)
    return sum((i + 1) * int(c) for i, c in enumerate(reversed(ds))) % 11


def measure_checks(trials=4000, log=print):
    r = C.Rng(33)
    res = {}
    for name, f in (("quipu-digit-sum", quipu_checksum), ("luhn", luhn), ("mod11-weighted", mod11)):
        sub = subn = tr = trn = 0
        for _ in range(trials):
            n = r.randint(10 ** 5, 10 ** 6 - 1)
            ds = list(str(n))
            i = r.randint(0, 5)
            new = r.choice([c for c in "0123456789" if c != ds[i]])
            bad = ds[:]
            bad[i] = new
            if bad[0] != "0":
                subn += 1
                sub += f(int("".join(bad))) != f(n)
            j = r.randint(0, 4)
            if ds[j] != ds[j + 1]:
                t = ds[:]
                t[j], t[j + 1] = t[j + 1], t[j]
                if t[0] != "0":
                    trn += 1
                    tr += f(int("".join(t))) != f(n)
        res[name] = {"substitution_detect": round(sub / max(subn, 1), 4), "transposition_detect": round(tr / max(trn, 1), 4)}
    log("  check digits on 6-digit values: " + "; ".join(f"{k}: subst {v['substitution_detect']}, transp {v['transposition_detect']}" for k, v in res.items()))
    return res


def selftest():
    c = C.Checks()
    r = C.Rng(2)
    for n in [0, 1, 7, 10, 101, 135, 201, 999, 4096] + [r.randint(0, 10 ** 6) for _ in range(40)]:
        for name, (enc, dec, _) in ALPHABETS.items():
            if n == 0 and name == "quipu":
                continue
            c.ok(dec(enc(n)) == n, f"{name} round-trip {n}")
    c.ok(to_quipu(135) == "o|ooo|LLLLL" and to_quipu(201) == "oo|_|8", "legend examples are true")
    c.ok(from_trit("+-0") == 6 and from_trit("+0-") == 8, "trit legend examples are true")
    c.ok(parse_ints("sure: [1, 2, 3]", 3) == [1, 2, 3], "parse")
    m = measure_checks(trials=600, log=lambda *a: None)
    c.ok(m["quipu-digit-sum"]["substitution_detect"] == 1.0, "digit sum catches every substitution")
    c.ok(m["quipu-digit-sum"]["transposition_detect"] == 0.0, "digit sum misses every transposition")
    c.ok(m["mod11-weighted"]["transposition_detect"] == 1.0, "mod-11 weighted catches transpositions")
    return c.report("quipu_projection")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    print("E6 quipu_projection: 5 feeds x 10 wall_ms values per alphabet, decoded back by an LLM (temperature 0)")
    res = {"llm": measure_llm(), "check_digits": measure_checks()}
    with open(C.HERE + "/results_quipu_projection.json", "w") as f:
        json.dump(res, f, indent=1, ensure_ascii=False)
