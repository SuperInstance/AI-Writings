// weakest-claim — a reusable weakest-claim auditor built ON labs/jev-fold.
// Localize: fold the target's compound guarantee (reusing fold.mjs) with a
// "sound guarantee?" noul per leaf → argmin + whole-vs-fold divergence.
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

export const loadTarget = (path) => JSON.parse(readFileSync(path, "utf8"));
export const loadFixtures = (path = FIXTURE_PATH) => JSON.parse(readFileSync(path, "utf8"));

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const path = process.argv[2] ?? fileURLToPath(new URL("./targets/jev-fold.json", import.meta.url));
  const loc = await localize(loadTarget(path), { score: guaranteeScorer() });
  console.log(render(loc));
}
