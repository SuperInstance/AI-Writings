#!/usr/bin/env python3
"""Control B mock for the z.ai provider path.

Deterministic body derived from md5(cultural_prompt):
    d      = md5(cultural_prompt).digest()
    h      = d.hex()
    i      = d[0] % 4
    seed   = h[(i*2)%8 : (i*2)%8+4]
    color  = h[8:12]
    figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
Geometry: 38-char header + 162-char tail = 200 (content_preview[:200]),
then a 149-char continuation -> 349-char body (band 332-369).
"""
import json, hashlib, sys, os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8099
CIVS_DIR = os.environ.get("CIVS_DIR", os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
CULTURES = {c: json.load(open(f"{CIVS_DIR}/{c}/culture.json")) for c in json.load(open(f"{CIVS_DIR}/civilizations.json"))}

TAIL = " A cell keeps its own accounts and asks the network for what it cannot remember itself. The bookkeeper and the witness log are two names for the same discipline: "
CONT = " It records first and reasons later, and it never claims a number it cannot show. Each entry names its own witness, so the ledger can be checked with"

LOG = []

def build_body(civ_id, prompt):
    cul = CULTURES[civ_id]
    cultural_prompt = f"""You are a voice in the tradition of "{cul['name']}".
Your tenets: {', '.join(cul['tenets'])}.
Your voice: {cul['voice_emphasis']}.

{prompt}"""
    d = hashlib.md5(cultural_prompt.encode()).digest()
    h = d.hex()
    i = d[0] % 4
    seed = h[(i*2) % 8:(i*2) % 8 + 4]
    color = h[8:12]
    figure = f"{h[12:16]}/{h[16:20]}/{h[20:24]}"
    header = f"[mock-zai {seed}] #{color} {figure}. "
    assert len(header) == 38, len(header)
    assert len(TAIL) == 162, len(TAIL)
    return header + TAIL + CONT

class H(BaseHTTPRequestHandler):
    def do_POST(self):
        n = int(self.headers.get('Content-Length', 0))
        raw = self.rfile.read(n)
        try:
            data = json.loads(raw.decode())
            content = data["messages"][0]["content"]
        except Exception as e:
            LOG.append({"err": str(e)})
            self.send_response(400); self.end_headers(); self.wfile.write(b'{"error":"bad"}')
            return
        # identify the civ from the cultural prompt's first line
        civ_id = "civ-grounded"
        for cid, cul in CULTURES.items():
            if f'tradition of "{cul["name"]}"' in content:
                civ_id = cid; break
        prompt = content.split("\n\n", 1)[1] if "\n\n" in content else content
        body = build_body(civ_id, prompt)
        LOG.append({"civ": civ_id, "seed": body[10:14], "len": len(body), "ts": __import__("time").time()})
        out = json.dumps({"choices": [{"message": {"role": "assistant", "content": body}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(out)))
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(out)

    def log_message(self, *a):  # silence stderr access log
        pass

if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    print(f"mock listening on {PORT}", flush=True)
    srv.serve_forever()
