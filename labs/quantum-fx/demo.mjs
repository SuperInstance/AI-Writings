// node labs/quantum-fx/demo.mjs [--offline] [--record]
// Runs every working engine once. Live when MOTHQUANTUM_* are set, else replays fixtures.json.
// --record (live only) rewrites fixtures.json from this run.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { createClient, fixtureFetch } from "./qfx.mjs";

const FIXTURES = fileURLToPath(new URL("./fixtures.json", import.meta.url));
const args = process.argv.slice(2);
const offline = args.includes("--offline") || !process.env.MOTHQUANTUM_KEY || !process.env.MOTHQUANTUM_BASE;

// Keep fixtures small: status needs only its state; comet's result keeps what qrng() reads
// (the full entropy report, commitment and raw counts are ~100 KB).
function slim(kind, body) {
  if (kind === "status") return { job_id: body.job_id, engine_id: body.engine_id, status: body.status, steps: body.steps, error: body.error };
  const o = body.result?.output;
  if (o?.random && o?.bell_witness) {
    const { S, sigma_S, classical_bound, tsirelson_bound, caveat } = o.bell_witness;
    const { mode, backend } = o.provenance ?? {};
    return { result: { output: { random: o.random, bell_witness: { S, sigma_S, classical_bound, tsirelson_bound, caveat }, provenance: { mode, backend } } } };
  }
  return body;
}

// Recording wrapper: remembers the last submit/status/result body per engine.
function recorder(inner) {
  const rec = {}, byJob = {};
  const f = async (url, init = {}) => {
    const r = await inner(url, init);
    const text = await r.text();
    const p = new URL(url).pathname;
    let m;
    if ((m = p.match(/\/engines\/([^/]+)\/process$/))) {
      const body = JSON.parse(text);
      byJob[body.job_id] = m[1];
      rec[m[1]] = { submit: body };
    } else if ((m = p.match(/\/jobs\/([^/]+)\/(status|result)$/)) && byJob[m[1]]) {
      rec[byJob[m[1]]][m[2]] = slim(m[2], JSON.parse(text));
    }
    return { ok: r.ok, status: r.status, text: async () => text };
  };
  return { f, rec };
}

const fx = offline ? JSON.parse(readFileSync(FIXTURES, "utf8")) : null;
const rec = offline ? null : recorder(globalThis.fetch);
const q = createClient(offline ? { base: "https://fixture.invalid", key: "fixture", fetch: fixtureFetch(fx.engines), sleep: async () => {} } : { fetch: rec.f });

const short = (id) => id.slice(0, 8);
const r3 = (xs) => xs.map((x) => +x.toFixed(3));
console.log(`[source: ${offline ? `fixture (${fx.recorded})` : "live"}]`);

const d = await q.qrng({ integers: { min: 1, max: 6, count: 8 }, floats: 3 });
console.log(`comet-qrng-v1   job ${short(d.job_id)}  Bell S=${d.S?.toFixed(3)} (bound ${d.classical_bound}, ${d.mode}/${d.backend})`);
console.log(`                bytes ${d.hex.slice(0, 32)}… (${d.hex.length / 2} B)  d6 [${d.integers}]  floats [${r3(d.floats)}]`);

const c = await q.coinToss({ shots: 32 });
console.log(`coin-toss-v1    job ${short(c.job_id)}  ${c.heads} heads / ${c.tails} tails of ${c.shots} (${c.mode}/${c.backend})`);

const b = await q.blur([0, 0, 0, 8, 0, 0, 0, 0], { strength: 0.1 });
console.log(`blur-core-v1    job ${short(b.job_id)}  [0,0,0,8,0,0,0,0] → [${r3(b.output)}]`);

const p = await q.qpixl([0.05, 0.2, 0.4, 0.6, 0.8, 0.95], { shots: 1024 });
console.log(`qpixl-v1        job ${short(p.job_id)}  [0.05,0.2,0.4,0.6,0.8,0.95] → [${r3(p.output)}]`);

const e = await q.qec({ shots: 1000, seed: 7, noise: { p_gate: 0.01, p_1q: 0.005, p_meas: 0.01, p_idle: 0.002 } });
console.log(`tamagotchi-v1   job ${short(e.job_id)}  steane logical qubit: success ${e.success_rate} (${e.logical_errors} logical errors, ${e.syndromes} syndromes / ${e.shots} shots)`);

if (!offline && args.includes("--record")) {
  writeFileSync(FIXTURES, JSON.stringify({ recorded: `${new Date().toISOString()}, live Moth`, engines: rec.rec }, null, 2) + "\n");
  console.error(`recorded → ${FIXTURES}`);
}
