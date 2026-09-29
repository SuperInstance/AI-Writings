// quantum-fx — zero-dep client for the Moth quantum engines that work from plain JSON params.
// One interface for all of them: submit → poll → result. Env: MOTHQUANTUM_BASE, MOTHQUANTUM_KEY.
// Every engine returns {"result": …} but the inner shape differs; the wrappers below normalise it.

// Cloudflare fronts the API and blocks non-browser User-Agents with error 1010 (looks like an auth failure).
export const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";

export class MothError extends Error {
  constructor(message, info = {}) {
    super(message);
    this.name = "MothError";
    Object.assign(this, info); // { status, job_id, engine_id, type, retryable }
  }
}

export function createClient({
  base = process.env.MOTHQUANTUM_BASE,
  key = process.env.MOTHQUANTUM_KEY,
  fetch: doFetch = globalThis.fetch,
  pollMs = 2000,
  maxPolls = 90,
  sleep = (ms) => new Promise((r) => setTimeout(r, ms)),
} = {}) {
  if (!base || !key) throw new MothError("MOTHQUANTUM_BASE / MOTHQUANTUM_KEY not set");
  const H = { authorization: `Bearer ${key}`, "content-type": "application/json", "user-agent": UA };

  async function call(path, init = {}) {
    const r = await doFetch(`${base}${path}`, { ...init, headers: H });
    const text = await r.text();
    let body;
    try { body = JSON.parse(text); } catch { body = { raw: text.slice(0, 300) }; }
    if (!r.ok) throw new MothError(`Moth ${init.method ?? "GET"} ${path} → ${r.status}: ${body.detail ?? body.raw ?? ""}`, { status: r.status });
    return body;
  }

  const engines = async () => (await call("/engines")).engines;
  const engine = (id) => call(`/engines/${id}`);

  // The uniform primitive. Returns { job_id, engine_id, result, steps, ms }; throws MothError on a failed job.
  async function run(engine_id, params = {}) {
    const t0 = Date.now();
    const { job_id } = await call(`/engines/${engine_id}/process`, { method: "POST", body: JSON.stringify({ params }) });
    let st;
    for (let i = 0; ; i++) {
      st = await call(`/jobs/${job_id}/status`);
      if (st.status === "completed") break;
      if (st.status === "failed") {
        const e = st.error ?? {};
        throw new MothError(`Moth job ${engine_id} failed: ${e.message ?? "unknown"}`, { job_id, engine_id, type: e.type, retryable: e.retryable });
      }
      if (i >= maxPolls) throw new MothError(`Moth job ${engine_id} still ${st.status} after ${maxPolls} polls`, { job_id, engine_id });
      await sleep(pollMs);
    }
    const { result } = await call(`/jobs/${job_id}/result`);
    return { job_id, engine_id, result, steps: st.steps?.map((s) => `${s.name}:${s.status}`), ms: Date.now() - t0 };
  }

  // comet-qrng-v1 — conditioned random bytes + server-side derive (unbiased ints via rejection sampling,
  // 53-bit floats in [0,1)) + a CHSH Bell witness. A job can complete with no extractable bytes; retry it.
  // The derivation fails ("conditioned bytes ran out") if output_bytes is too small, so size it from the request:
  // 8 B per float, a generous 8 B per integer to cover rejection sampling, plus slack.
  async function qrng({ integers, floats = 0, bytes, mode = "emu", attempts = 3 } = {}) {
    const derive = { ...(integers && { integers }), ...(floats && { floats }) };
    const output_bytes = Math.min(1e6, bytes ?? Math.max(32, 8 * floats + 8 * (integers?.count ?? 0) + 16));
    let why;
    for (let a = 0; a < attempts; a++) {
      const j = await run("comet-qrng-v1", { mode, output_bytes, include_raw_counts: false, ...(Object.keys(derive).length && { derive }) });
      const o = j.result?.output ?? {};
      const d = o.random?.derived ?? {};
      const ints = d.integers?.values ?? [];
      const fl = d.floats ?? []; // flat list, unlike integers
      if (!o.random?.hex || (integers && !ints.length) || (floats && !fl.length)) {
        why = o.random?.derivation_error ?? "no conditioned bytes";
        continue;
      }
      return {
        job_id: j.job_id,
        hex: o.random.hex,
        integers: ints,
        floats: fl,
        S: o.bell_witness?.S,
        sigma_S: o.bell_witness?.sigma_S,
        classical_bound: o.bell_witness?.classical_bound ?? 2,
        tsirelson_bound: o.bell_witness?.tsirelson_bound,
        mode: o.provenance?.mode, // "emu" = Aer simulator: report it, don't hide it
        backend: o.provenance?.backend,
      };
    }
    throw new MothError(`comet-qrng-v1 returned nothing usable after ${attempts} jobs: ${why}`, { engine_id: "comet-qrng-v1" });
  }

  // coin-toss-v1 — Hadamard coin; counts are flat on result (no output wrapper for them).
  async function coinToss({ shots = 10, mode = "emu" } = {}) {
    const j = await run("coin-toss-v1", { shots, mode });
    const { heads, tails, backend } = j.result;
    return { job_id: j.job_id, heads, tails, shots: j.result.shots, majority: j.result.output, mode: j.result.mode, backend };
  }

  // blur-core-v1 — quantum blur of any N-D array of non-negative numbers. Output has the input's shape
  // and is rescaled to the input's max (sum is not conserved). Omit `shots` for the exact result.
  async function blur(values, { strength = 0.5, reach = 0, axes, shots } = {}) {
    const j = await run("blur-core-v1", { values, strength, reach, ...(axes && { axes }), ...(shots && { shots }) });
    return { job_id: j.job_id, output: j.result.output };
  }

  // qpixl-v1 — encode values into a quantum state and read them back; the shot noise is the effect.
  // `values` must be an array (the engine's own sample sends a bare CSV string, which fails).
  async function qpixl(values, { machine = "aer", shots = 1024, discretize = 0, dynamic_range = "none" } = {}) {
    const j = await run("qpixl-v1", { values, machine, shots, discretize, dynamic_range });
    return { job_id: j.job_id, output: j.result.output, backend: j.result.backend };
  }

  // tamagotchi-v1 — quantum error correction pet: logical actions on a CSS code under depolarizing noise.
  async function qec({ actions = [["SE", 0], ["X", 0], ["SE", 0]], code = "steane", n_logical = 1, shots = 1000, noise = {}, seed } = {}) {
    const j = await run("tamagotchi-v1", { actions, code, n_logical, shots, noise, ...(seed != null && { seed }) });
    const o = j.result.output;
    return { job_id: j.job_id, success_rate: o.success_rate, logical_errors: o.logical_error_count, syndromes: o.syndromes_detected, per_logical: o.per_logical, shots: o.shots };
  }

  return { engines, engine, run, qrng, coinToss, blur, qpixl, qec };
}

// Offline fetch that replays recorded {engine_id: {submit, status, result}} bodies. Used by the test and --offline demo.
export function fixtureFetch(fixtures) {
  const jobs = new Map(Object.entries(fixtures).map(([id, f]) => [f.submit.job_id, id]));
  const reply = (body, status = 200) => ({ ok: status < 400, status, text: async () => JSON.stringify(body) });
  return async (url, init = {}) => {
    const p = new URL(url).pathname;
    let m;
    if ((m = p.match(/\/engines\/([^/]+)\/process$/)) && init.method === "POST") {
      const f = fixtures[m[1]];
      return f ? reply(f.submit, 202) : reply({ detail: `no fixture for ${m[1]}` }, 404);
    }
    if ((m = p.match(/\/jobs\/([^/]+)\/(status|result)$/))) {
      const id = jobs.get(m[1]);
      return id ? reply(fixtures[id][m[2]]) : reply({ detail: "unknown job" }, 404);
    }
    return reply({ detail: `unrouted ${p}` }, 404);
  };
}
