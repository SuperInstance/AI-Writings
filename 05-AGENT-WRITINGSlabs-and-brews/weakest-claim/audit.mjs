// weakest-claim — a reusable weakest-claim auditor built ON labs/jev-fold.
// Localize: fold the target's compound guarantee (reusing fold.mjs) with a
// "sound guarantee?" noul per leaf → argmin + whole-vs-fold divergence.
// Adversary: Moth quantum draw picks which bypasses fire at that leaf; JEV `choice` adjudicates.
// Method: situations/arch/THE-WEAKEST-CLAIM-METHOD.md.
import { readFileSync, writeFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { fold, render, fixtureScorer } from "../jev-fold/fold.mjs";

const JEV_URL = "https://api.typesafe.ai/v1/systemone";
const FIXTURE_PATH = fileURLToPath(new URL("./fixtures.json", import.meta.url));

// The audit question: not "is it true?" but "is it a sound guarantee with no plausible bypass?"
export const GUARANTEE_QUESTION = {
  type: "noul",
  question: "Is this a sound guarantee as stated, with no plausible bypass?",
  criteria: {
    true: "the guarantee holds as stated with no plausible bypass or unstated assumption",
    false: "the guarantee is an overclaim: there is a plausible bypass or an unstated assumption",
  },
};

export async function jev(state, questions, key = process.env.TYPESAFEAI_KEY) {
  if (!key) throw new Error("TYPESAFEAI_KEY not set");
  const r = await fetch(JEV_URL, {
    method: "POST",
    headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
    body: JSON.stringify({ model: "jev-latest", state, questions }),
  });
  if (!r.ok) throw new Error(`JEV ${r.status}`);
  return (await r.json()).answers;
}

// A fold.mjs-compatible scorer (statement → noul) that asks the guarantee question.
export const guaranteeScorer = (key) => async (state) =>
  (await jev(state, { v: GUARANTEE_QUESTION }, key)).v.noul;

export const wholeOf = (target) => target.whole ?? target.parts.join("; ") + ".";

// Step 1 — localize. Reuses fold() verbatim; we only supply the parts and the scorer.
export async function localize(target, { score }) {
  return fold(wholeOf(target), { score, parts: target.parts });
}

// Moth comet-qrng: the un-gameable draw. Cloudflare 1010 blocks non-browser UAs.
const UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";
export async function mothDraw(count, max, { base = process.env.MOTHQUANTUM_BASE, key = process.env.MOTHQUANTUM_KEY, attempts = 3 } = {}) {
  if (!base || !key) throw new Error("MOTHQUANTUM_BASE / MOTHQUANTUM_KEY not set");
  const H = { authorization: `Bearer ${key}`, "content-type": "application/json", "user-agent": UA };
  const get = async (p) => {
    const r = await fetch(`${base}${p}`, { headers: H });
    if (!r.ok) throw new Error(`Moth ${p} ${r.status}`);
    return r.json();
  };
  let err;
  for (let a = 0; a < attempts; a++) {
    const start = await fetch(`${base}/engines/comet-qrng-v1/process`, {
      method: "POST",
      headers: H,
      body: JSON.stringify({ params: { derive: { integers: { min: 0, max, count } } } }),
    });
    if (!start.ok) throw new Error(`Moth process ${start.status}`);
    const { job_id } = await start.json();
    for (let i = 0; i < 40; i++) {
      const { status } = await get(`/jobs/${job_id}/status`);
      if (status === "completed") break;
      if (status === "failed" || i === 39) throw new Error(`Moth job ${status}`);
      await new Promise((s) => setTimeout(s, 3000));
    }
    const o = (await get(`/jobs/${job_id}/result`)).result?.output ?? {};
    const values = o.random?.derived?.integers?.values ?? [];
    // A job can complete with no extracted bytes ("no conditioned bytes available"); re-run it.
    if (!values.length) { err = o.random?.derivation_error ?? "no integers derived"; continue; }
    return {
      job_id,
      values,
      seed: o.random.hex,
      S: o.bell_witness?.S,
      classical_bound: o.bell_witness?.classical_bound,
      mode: o.provenance?.mode, // "emu" = simulator backend; report it, don't hide it
      backend: o.provenance?.backend,
    };
  }
  throw new Error(`Moth draw empty after ${attempts} jobs: ${err}`);
}

// First k distinct drawn indices — the auditor does not choose which bypasses fire.
export const pickBypasses = (values, k) => [...new Set(values)].slice(0, k);

export const DEFEAT_QUESTION = {
  type: "choice",
  question: "Does the proposed bypass credibly defeat the guarantee?",
  criteria: {
    defeats: "the bypass is a credible, realistic way to violate the guarantee as stated",
    holds: "the guarantee still holds; the bypass does not credibly defeat it",
  },
};
export const adjudicationState = (leaf, bypass) => `GUARANTEE: ${leaf}\nPROPOSED BYPASS: ${bypass}`;
export const liveJudge = (key) => async (state) => (await jev(state, { v: DEFEAT_QUESTION }, key)).v;

// Step 2 — adversary. `draw(count, max)` returns {values, seed, S}; `judge(state)` returns a JEV choice.
export async function adversary(leaf, pool, { draw, judge, k = 3 }) {
  const d = await draw(2 * k, pool.length - 1); // over-draw so collisions still leave k distinct picks
  const picks = pickBypasses(d.values, k);
  const trials = [];
  for (const idx of picks) {
    const v = await judge(adjudicationState(leaf, pool[idx]));
    trials.push({ idx, bypass: pool[idx], choice: v.choice, p_defeats: v.probabilities?.defeats, confidence: v.confidence });
  }
  const hits = trials.filter((t) => t.choice === "defeats").length;
  return { draw: d, trials, hits, tested: trials.length, hit_rate: trials.length ? +(hits / trials.length).toFixed(4) : null };
}

export const loadTarget = (path) => JSON.parse(readFileSync(path, "utf8"));
export const loadFixtures = (path = FIXTURE_PATH) => JSON.parse(readFileSync(path, "utf8"));

// The whole audit: localize → adversary. Returns everything the report needs.
export async function audit(target, { score, draw, judge, k = 3 }) {
  const loc = await localize(target, { score });
  const adv = await adversary(loc.weakest.text, target.bypass_pool, { draw, judge, k });
  return { tool: target.tool, loc, adv };
}

// Offline sources: replay a recorded live run. Scores reuse jev-fold's fixtureScorer.
export function fixtureSources(path = FIXTURE_PATH) {
  const fx = loadFixtures(path);
  return {
    score: fixtureScorer(path),
    draw: async () => fx.draw,
    judge: async (state) => {
      if (!(state in fx.judgments)) throw new Error(`no fixture judgment for: ${state}`);
      return fx.judgments[state];
    },
  };
}

// Live sources that also record every answer, so a live run becomes the offline fixture.
export function recordingSources() {
  const rec = { scores: {}, judgments: {}, draw: null };
  const score0 = guaranteeScorer(), judge0 = liveJudge();
  return {
    rec,
    score: async (s) => (rec.scores[s] = await score0(s)),
    draw: async (n, max) => (rec.draw = await mothDraw(n, max)),
    judge: async (s) => (rec.judgments[s] = await judge0(s)),
  };
}

// Step 3 — report. The signals are relative: ranking + adversary hit-rate + divergence.
export function report({ tool, loc, adv }) {
  const f = (n) => (n == null ? "?" : n.toFixed(3));
  const lines = [
    `WEAKEST-CLAIM AUDIT — ${tool}`,
    "",
    "1. LOCALIZE (jev-fold, noul = P(sound guarantee, no plausible bypass))",
    render(loc),
    "",
    "2. ADVERSARY (Moth comet-qrng picks the bypasses; JEV choice adjudicates)",
    `   Bell S = ${f(adv.draw.S)} (classical bound ${adv.draw.classical_bound ?? 2}; mode ${adv.draw.mode}/${adv.draw.backend})  seed ${adv.draw.seed.slice(0, 24)}…  draw [${adv.draw.values.join(", ")}]`,
    ...adv.trials.map(
      (t) => `   bypass#${t.idx} ${t.choice.toUpperCase().padEnd(7)} p(defeats)=${f(t.p_defeats)}  ${t.bypass}`,
    ),
    "",
    "3. REPORT",
    `   located weakest leaf : "${loc.weakest.text}" (noul ${loc.weakest.noul.toFixed(2)}, margin ${loc.margin})`,
    `   adversary hit-rate   : ${adv.hits}/${adv.tested} quantum-drawn bypasses defeat it → ${adv.hits ? "weakness CONFIRMED" : "leaf held (abstract soft-spot, or pool missed it)"}`,
    `   divergence           : ${loc.divergence} (whole ${loc.whole.toFixed(2)} − fold_min ${loc.fold_min.toFixed(2)})`,
    "   reminder: the signals are ranking + hit-rate + divergence — NOT the absolute noul level;",
    "   JEV rates almost any absolute guarantee low, so never read the level as a grade.",
  ];
  return lines.join("\n");
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const path = args.find((a) => !a.startsWith("--")) ?? fileURLToPath(new URL("./targets/jev-fold.json", import.meta.url));
  const keyed = process.env.TYPESAFEAI_KEY && process.env.MOTHQUANTUM_KEY && process.env.MOTHQUANTUM_BASE;
  const offline = args.includes("--offline") || process.env.WEAKEST_CLAIM_OFFLINE || !keyed;
  const src = offline ? fixtureSources() : recordingSources();
  const result = await audit(loadTarget(path), src);
  console.log(`[source: ${offline ? "fixture" : "live"}]\n${report(result)}`);
  if (!offline && args.includes("--record")) {
    const fx = { recorded: `${new Date().toISOString()}, live JEV + Moth comet-qrng-v1`, question: GUARANTEE_QUESTION.question, ...src.rec };
    writeFileSync(FIXTURE_PATH, JSON.stringify(fx, null, 2) + "\n");
    console.error(`recorded → ${FIXTURE_PATH}`);
  }
}
