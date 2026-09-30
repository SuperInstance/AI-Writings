#!/usr/bin/env python3
"""polyform — cross-formalism differ: does the same fnv1a-64 kernel give the same hash in every formalism?

For each formalism whose toolchain is present, run its impl (impls/) on the GOLDEN vectors and compare to
the pinned hash. A formalism whose toolchain is absent is reported "reference-only (toolchain absent)",
never "agreed". Exit 0 = no divergence and no toolchain error; exit 1 otherwise.
--require=bqn,futhark,uiua additionally fails if any of those did not actually run and agree.

Toolchain lookup, per formalism: env var (POLYFORM_BQN / POLYFORM_FUTHARK / POLYFORM_UIUA), then PATH.
POLYFORM_DISABLE=bqn,uiua forces those to be treated as absent (used to exercise the absent path).
"""
import json, os, re, shutil, subprocess, sys, tempfile
from dataclasses import dataclass, field
from typing import Callable, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
IMPLS = os.path.join(HERE, "impls")
sys.path.insert(0, IMPLS)
from fnv1a import fnv1a64  # noqa: E402  (the Python baseline)

OFFSET, PRIME = 0xCBF29CE484222325, 0x100000001B3

# --- GOLDEN -------------------------------------------------------------------------------------
# name -> (bytes, pinned hex). "", "a", "foobar" and the fox sentence are published FNV-1a-64 vectors; the rest were
# computed once with impls/fnv1a.py and pinned here. selftest re-derives them, so a typo fails loudly.
GOLDEN = {
    "empty":      (b"", "cbf29ce484222325"),
    "a":          (b"a", "af63dc4c8601ec8c"),
    "foobar":     (b"foobar", "85944171f73967e8"),
    "fox":        (b"The quick brown fox jumps over the lazy dog", "f3f9b7f5e7e47110"),
    "nul-ff":     (b"\x00\xff\x00\xff\x80\x7f", "d629564a53029b58"),
    "all-bytes":  (bytes(range(256)), "4242dc5249c33625"),
    "kilo-mixed": (bytes((i * 131 + 7) % 256 for i in range(1000)), "0bb313ff230e2f45"),
}


def _hex(n: int) -> str:
    return "%016x" % n


# --- formalism adapters -------------------------------------------------------------------------
@dataclass
class Formalism:
    name: str
    source: str                                   # file under impls/
    find: Callable[[], Optional[str]]             # -> toolchain path or None
    run: Callable[[str, bytes], str]              # (toolchain, data) -> 16 hex digits
    note: str = ""
    model: Optional[Callable[[bytes], int]] = None  # pure-Python model of the source's algorithm
    consts: list = field(default_factory=list)      # strings that must appear in the source


def _which(env: str, *names: str) -> Optional[str]:
    if os.environ.get(env):
        p = os.environ[env]
        return p if os.path.exists(p) else None
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    return None


def _with_file(data: bytes, fn):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(data)
        path = f.name
    try:
        return fn(path)
    finally:
        os.unlink(path)


def _limbs_to_hex(text: str) -> str:
    nums = [int(x) for x in re.findall(r"\d+", text)]
    if len(nums) != 4 or any(n > 0xFFFF for n in nums):
        raise RuntimeError("expected 4 16-bit limbs, got %r" % text)
    return _hex(sum(n << (16 * i) for i, n in enumerate(nums)))


def _sh(cmd, **kw) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60, **kw)
    if r.returncode != 0:
        raise RuntimeError("%s failed: %s" % (cmd[0], (r.stderr or r.stdout).strip()[:300]))
    return r.stdout


def run_python(_tc, data):
    return _with_file(data, lambda p: _sh([sys.executable, os.path.join(IMPLS, "fnv1a.py"), p]).strip())


def run_bqn(tc, data):
    return _with_file(data, lambda p: _limbs_to_hex(_sh([tc, os.path.join(IMPLS, "fnv1a.bqn"), p])))


def run_uiua(tc, data):
    return _with_file(data, lambda p: _limbs_to_hex(
        _sh([tc, "run", os.path.join(IMPLS, "fnv1a.ua"), "--", p])))


_fut_cache = {}


def find_futhark():
    fut = _which("POLYFORM_FUTHARK", "futhark")
    if fut and not shutil.which("cc") and not shutil.which("gcc"):
        return None  # `futhark c` needs a C compiler; without one it cannot run here
    return fut


def run_futhark(tc, data):
    if tc not in _fut_cache:
        d = tempfile.mkdtemp(prefix="polyform-fut-")
        shutil.copy(os.path.join(IMPLS, "fnv1a.fut"), d)
        _sh([tc, "c", "fnv1a.fut"], cwd=d)
        _fut_cache[tc] = os.path.join(d, "fnv1a")
    arr = "[" + ",".join("%du8" % b for b in data) + "]" if data else "empty([0]u8)"
    r = subprocess.run([_fut_cache[tc]], input=arr, capture_output=True, text=True, timeout=60)
    m = re.fullmatch(r"(\d+)u64\s*", r.stdout)
    if r.returncode != 0 or not m:
        raise RuntimeError("futhark binary failed: %s" % (r.stderr or r.stdout).strip()[:300])
    return _hex(int(m.group(1)))


def limb_model(data: bytes) -> int:
    """Pure-Python model of the BQN/Uiua algorithm: 4x16-bit limbs, XOR on limb 0, multiply as
    435*limbs + 256*limbs<<2 limbs, then carry. Checks the *algorithm*, not the BQN/Uiua source."""
    h = [(OFFSET >> (16 * i)) & 0xFFFF for i in range(4)]
    for b in data:
        h[0] ^= b
        c = [h[k] * 435 + (h[k - 2] * 256 if k >= 2 else 0) for k in range(4)]
        out, carry = [], 0
        for k in range(4):
            t = c[k] + carry
            out.append(t & 0xFFFF)
            carry = t >> 16
        h = out
    return sum(v << (16 * i) for i, v in enumerate(h))


FORMALISMS = [
    Formalism("python", "fnv1a.py", lambda: sys.executable, run_python, "baseline; int is arbitrary precision",
              model=fnv1a64, consts=["0xCBF29CE484222325", "0x100000001B3"]),
    Formalism("bqn", "fnv1a.bqn", lambda: _which("POLYFORM_BQN", "cbqn", "bqn", "BQN"), run_bqn,
              "CBQN; f64 numbers -> 16-bit limbs", model=limb_model, consts=["435‿0‿256‿0", "8997‿33826‿40164‿52210"]),
    Formalism("futhark", "fnv1a.fut", find_futhark, run_futhark, "futhark c (sequential C backend); native u64",
              model=fnv1a64, consts=["0xcbf29ce484222325u64", "0x100000001b3u64"]),
    Formalism("uiua", "fnv1a.ua", lambda: _which("POLYFORM_UIUA", "uiua"), run_uiua,
              "f64 numbers -> 16-bit limbs", model=limb_model, consts=["[8997 33826 40164 52210]", "×435", "×256"]),
]


# --- harness ------------------------------------------------------------------------------------
def golden_vectors(golden=None):
    return golden if golden is not None else GOLDEN


def check_reference_only(f: Formalism, vectors) -> dict:
    """No toolchain: cannot run the source. Two weaker checks, neither of which counts as 'agreed':
    the constants are present in the source text, and the algorithm model hits the golden hashes."""
    src = open(os.path.join(IMPLS, f.source), encoding="utf-8").read()
    missing = [c for c in f.consts if c not in src]
    model_bad = [n for n, (d, g) in vectors.items() if f.model and _hex(f.model(d)) != g]
    return {"constants_in_source": not missing, "missing_constants": missing,
            "model_matches_golden": not model_bad, "model_diverged_on": model_bad}


def run_formalism(f: Formalism, vectors, disabled=()) -> dict:
    tc = None if f.name in disabled else f.find()
    res = {"name": f.name, "source": f.source, "note": f.note, "toolchain": tc}
    if not tc:
        res["status"] = "reference-only (toolchain absent)"
        res["reference_check"] = check_reference_only(f, vectors)
        return res
    got, bad, err = {}, [], None
    for name, (data, golden) in vectors.items():
        try:
            got[name] = f.run(tc, data)
        except Exception as e:  # toolchain present but the run failed: NOT reference-only, a real failure
            err = "%s: %s" % (name, e)
            break
        if got[name] != golden:
            bad.append(name)
    res["results"] = got
    if err:
        res["status"], res["error"] = "toolchain error", err
    elif bad:
        res["status"], res["diverged_on"] = "DIVERGED", bad
    else:
        res["status"] = "ran, agreed on golden (%d/%d vectors)" % (len(vectors), len(vectors))
    return res


def run_all(formalisms=None, vectors=None, disabled=None) -> list:
    if disabled is None:
        disabled = [x for x in os.environ.get("POLYFORM_DISABLE", "").split(",") if x]
    return [run_formalism(f, golden_vectors(vectors), disabled) for f in (formalisms or FORMALISMS)]


def ok(results) -> bool:
    return all(r["status"].startswith(("ran, agreed", "reference-only")) for r in results)


def report(results) -> str:
    lines = ["%-8s %-42s %s" % ("formalism", "status", "toolchain")]
    for r in results:
        lines.append("%-9s %-42s %s" % (r["name"], r["status"], r["toolchain"] or "-"))
        if "reference_check" in r:
            c = r["reference_check"]
            lines.append("          reference-only checks (NOT a run): constants in source=%s, algorithm model on golden=%s"
                         % (c["constants_in_source"], c["model_matches_golden"]))
        if r.get("diverged_on"):
            lines.append("          DIVERGENCE localized to %s on vectors: %s" % (r["name"], ", ".join(r["diverged_on"])))
            for v in r["diverged_on"]:
                lines.append("            %-10s got %s want %s" % (v, r["results"][v], GOLDEN[v][1]))
        if r.get("error"):
            lines.append("          ERROR " + r["error"])
    ran = [r["name"] for r in results if r["status"].startswith("ran, agreed")]
    ref = [r["name"] for r in results if r["status"].startswith("reference-only")]
    lines.append("ran and agreed: %s | reference-only: %s | %s"
                 % (", ".join(ran) or "none", ", ".join(ref) or "none", "OK" if ok(results) else "FAIL"))
    return "\n".join(lines)


if __name__ == "__main__":
    res = run_all()
    # --require bqn,futhark,uiua : treat "reference-only" for those as a failure (for CI that has the toolchains)
    req = next((a.split("=", 1)[1].split(",") for a in sys.argv if a.startswith("--require=")), [])
    unmet = [r["name"] for r in res if r["name"] in req and not r["status"].startswith("ran, agreed")]
    if unmet:
        print("REQUIRED but did not run+agree: " + ", ".join(unmet), file=sys.stderr)
    if "--json" in sys.argv:
        print(json.dumps(res, indent=2))
    else:
        print(report(res))
    sys.exit(0 if ok(res) and not unmet else 1)
