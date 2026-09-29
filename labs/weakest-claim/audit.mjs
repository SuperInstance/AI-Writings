// weakest-claim — a reusable weakest-claim auditor built ON labs/jev-fold.
// Localize: fold the target's compound guarantee (reusing fold.mjs) with a
// "sound guarantee?" noul per leaf → argmin + whole-vs-fold divergence.
// Adversary: Moth quantum draw picks which bypasses fire at that leaf; JEV `choice` adjudicates.
// Method: situations/arch/THE-WEAKEST-CLAIM-METHOD.md.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { fold, render } from "../jev-fold/fold.mjs";

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
export async function mothDraw(count, max, { base = process.env.MOTHQUANTUM_BASE, key = process.env.MOTHQUANTUM_KEY } = {}) {
  if (!base || !key) throw new Error("MOTHQUANTUM_BASE / MOTHQUANTUM_KEY not set");
  const H = { authorization: `Bearer ${key}`, "content-type": "application/json", "user-agent": UA };
  const get = async (p) => {
    const r = await fetch(`${base}${p}`, { headers: H });
    if (!r.ok) throw new Error(`Moth ${p} ${r.status}`);
    return r.json();
  };
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
  const res = await get(`/jobs/${job_id}/result`);
  const o = res.result?.output ?? res.output ?? res;
  return {
    job_id,
    values: o.random?.derived?.integers?.values ?? [],
    seed: o.random?.hex ?? "",
    S: o.bell_witness?.S,
    classical_bound: o.bell_witness?.classical_bound,
  };
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

export const loadTarget =(path) => JSON.parse(readFileSync(path, "utf8"));
export const loadFixtures = (path = FIXTURE_PATH) => JSON.parse(readFileSync(path, "utf8"));

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const path = process.argv[2] ?? fileURLToPath(new URL("./targets/jev-fold.json", import.meta.url));
  const target = loadTarget(path);
  const loc = await localize(target, { score: guaranteeScorer() });
  console.log(render(loc));
  const adv = await adversary(loc.weakest.text, target.bypass_pool, { draw: mothDraw, judge: liveJudge() });
  console.log(JSON.stringify(adv, null, 2));
}
