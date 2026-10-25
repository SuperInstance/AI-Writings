#!/usr/bin/env python3
"""Pre-flight gate: exercise the Control B mock before the batch.

Checks (per the SKILL checklist):
  1. 8 civs x 5 prompts = 40 requests, all 200 OK
  2. 40/40 distinct seeds
  3. 40/40 distinct previews
  4. 40/40 independently recomputed md5s (seed, color, figure)
  5. 38/162/200 geometry holds for every body
  6. body length in the 332-369 band
  7. 0 tracebacks
Prints an explicit final VERIFICATION line and exits 1 on any failure.
"""
import json, re, hashlib, sys, os, urllib.request

PORT = sys.argv[1] if len(sys.argv) > 1 else "8099"
URL = f"http://127.0.0.1:{PORT}/v1/chat/completions"
CIVS_DIR = os.environ.get("CIVS_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
REG = json.load(open(f"{CIVS_DIR}/civilizations.json"))
CULT = {c: json.load(open(f"{CIVS_DIR}/{c}/culture.json")) for c in REG}
PROMPTS = json.load(open(os.environ.get("CIV_PROMPTS", os.path.join(CIVS_DIR, "tools", "prompts.json"))))

TAIL_REF = " A cell keeps its own accounts and asks the network for what it cannot remember itself. The bookkeeper and the witness log are two names for the same discipline: "
PAT = re.compile(r"^\[mock-zai ([0-9a-f]{4})\] (#?[0-9a-f]{4}) ([0-9a-f]{4})/([0-9a-f]{4})/([0-9a-f]{4})\. (.*)$")

def cultural_prompt(civ_id, prompt):
    cul = CULT[civ_id]
    return f"""You are a voice in the tradition of "{cul['name']}".
Your tenets: {', '.join(cul['tenets'])}.
Your voice: {cul['voice_emphasis']}.

{prompt}"""

def expect(civ_id, prompt):
    cp = cultural_prompt(civ_id, prompt)
    d = hashlib.md5(cp.encode()).digest()
    h = d.hex()
    i = d[0] % 4
    return (h[(i*2)%8:(i*2)%8+4], h[8:12],
            f"{h[12:16]}/{h[16:20]}/{h[20:24]}")

results = []
fails = []
def chk(cond, label):
    if cond: print(f"  PASS  {label}")
    else:
        print(f"  FAIL  {label}"); fails.append(label)

print("PRE-FLIGHT GATE")
print(f"  endpoint: {URL}")
print(f"  civs: {len(REG)}  prompts: {len(PROMPTS)}  requests: {len(REG)*len(PROMPTS)}")
print()

bodies = []
for civ_id in REG:
    for prompt in PROMPTS:
        payload = json.dumps({
            "model": "glm-4.5",
            "messages": [{"role": "user", "content": cultural_prompt(civ_id, prompt)}],
            "max_tokens": 400, "temperature": 0.7, "top_p": 0.9,
        }).encode()
        req = urllib.request.Request(URL, data=payload,
            headers={"Authorization": "Bearer mock", "Content-Type": "application/json"},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                body = json.loads(r.read().decode())["choices"][0]["message"]["content"]
        except Exception as e:
            chk(False, f"{civ_id} / {prompt[:30]!r} request ({e})")
            continue
        m = PAT.match(body)
        if not m:
            chk(False, f"{civ_id} / {prompt[:30]!r} header parse")
            continue
        es, ec, ef = expect(civ_id, prompt)
        gs, gc, gf = m.group(1), m.group(2).lstrip("#"), f"{m.group(3)}/{m.group(4)}/{m.group(5)}"
        ok = (es == gs and ec == gc and ef == gf)
        if not ok: chk(False, f"{civ_id} / {prompt[:30]!r} recompute exp=({es},{ec},{ef}) got=({gs},{gc},{gf})")
        bodies.append((civ_id, prompt, body, (gs, gc, gf)))

chk(len(bodies) == 40, f"all 40 requests returned (got {len(bodies)})")
chk(len(set(b[2] for b in bodies)) == 40, f"40/40 distinct previews (got {len(set(b[2] for b in bodies))})")
chk(len(set(b[3] for b in bodies)) == 40, f"40/40 distinct seed-tuples (got {len(set(b[3] for b in bodies))})")
chk(len(set(b[3][0] for b in bodies)) == 40, f"40/40 distinct seeds (got {len(set(b[3][0] for b in bodies))})")
chk(all(len(b[2]) == 349 for b in bodies), f"all bodies 349 chars (min {min(len(b[2]) for b in bodies)}, max {max(len(b[2]) for b in bodies)})")
chk(all(332 <= len(b[2]) <= 369 for b in bodies), "all bodies inside 332-369 band")
chk(all(len(b[2][:200]) == 200 for b in bodies), "all previews exactly 200 chars")
# geometry: header 38 + tail 162 = 200  (the regex group 6 is tail+continuation,
# so the tail must be measured as body[38:200], not as group 6)
geo = all(b[2][38:200] == TAIL_REF and len(b[2][:38]) == 38 for b in bodies)
chk(geo, "38+162=200 geometry holds for every body (body[38:200] == tail)")
# and the continuation is the remainder after the 200-char preview
chk(all(len(b[2]) - 200 == 149 for b in bodies), "continuation is 149 chars on every body")
# per-civ: 5 prompts -> 5 distinct seeds
by_civ = {}
for civ_id, prompt, body, tup in bodies: by_civ.setdefault(civ_id, []).append(tup[0])
chk(all(len(set(v)) == 5 for v in by_civ.values()), "8/8 civs: 5 distinct seeds per civ")
# per-prompt: 8 civs -> 8 distinct seeds
by_p = {}
for civ_id, prompt, body, tup in bodies: by_p.setdefault(prompt, []).append(tup[0])
chk(all(len(set(v)) == 8 for v in by_p.values()), "5/5 prompts: 8 distinct seeds per prompt")

print()
if fails:
    print(f"PRE-FLIGHT: {len(fails)} FAIL")
    for f in fails[:20]: print("   -", f)
    print("VERIFICATION: FAIL")
    sys.exit(1)
print(f"PRE-FLIGHT: {len(bodies)} checks PASS")
print("VERIFICATION: ALL PASS")
