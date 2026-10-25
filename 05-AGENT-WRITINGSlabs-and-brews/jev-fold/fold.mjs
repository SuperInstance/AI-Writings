// jev-fold — a zero-dep decomposing-fold client for the JEV oracle.
// Given a compound claim: split it into parts, score the whole and each part
// with JEV `noul`, return the weakest part and the whole-vs-fold divergence.
// See situations/arch/THE-WEAKEST-CLAIM-METHOD.md for the method.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";

const JEV_URL = "https://api.typesafe.ai/v1/systemone";
const FIXTURE_PATH = fileURLToPath(new URL("./fixtures.json", import.meta.url));

export const FACT_QUESTION = {
  type: "noul",
  question: "Is this statement factually true?",
  criteria: { true: "accurate", false: "false" },
};

// Split on clause boundaries: ";", ", and", ", but", " and " between clauses,
// and sentence ends. Callers who need exact control pass `parts` instead.
export function split(claim) {
  return claim
    .split(/\s*;\s*|,\s*(?:and|but|while)\s+|\.\s+(?=[A-Z])|\s+and\s+(?=(?:the|a|an|it|its|[A-Z0-9])\b)/)
    .map((s) => s.trim().replace(/[.;,]+$/, ""))
    .filter((s) => s.length > 0);
}

// Live scorer: one JEV call per statement. Throws on any non-200.
export function liveScorer(key = process.env.TYPESAFEAI_KEY) {
  if (!key) throw new Error("TYPESAFEAI_KEY not set");
  return async (state) => {
    const r = await fetch(JEV_URL, {
      method: "POST",
      headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
      body: JSON.stringify({ model: "jev-latest", state, questions: { v: FACT_QUESTION } }),
    });
    if (!r.ok) throw new Error(`JEV ${r.status}`);
    return (await r.json()).answers.v.noul;
  };
}

// Fixture scorer: replays recorded nouls; unknown statements are an error.
export function fixtureScorer(path = FIXTURE_PATH) {
  const table = JSON.parse(readFileSync(path, "utf8")).scores;
  return async (state) => {
    if (!(state in table)) throw new Error(`no fixture for: ${state}`);
    return table[state];
  };
}

// The fold. `score` maps a statement to a noul in [0,1].
export async function fold(claim, { score, parts } = {}) {
  parts = parts ?? split(claim);
  if (parts.length < 2) throw new Error("claim did not split into 2+ parts; pass `parts`");
  const [whole, ...scores] = await Promise.all([claim, ...parts].map((s) => score(s)));
  const leaves = parts.map((text, i) => ({ text, noul: scores[i] }));
  const weakest = leaves.reduce((a, b) => (b.noul < a.noul ? b : a));
  const others = leaves.filter((l) => l !== weakest).map((l) => l.noul);
  return {
    claim,
    whole,
    leaves,
    weakest,
    fold_min: weakest.noul,
    divergence: +(whole - weakest.noul).toFixed(4), // how much the compound verdict hid
    margin: others.length ? +(Math.min(...others) - weakest.noul).toFixed(4) : null, // how cleanly it is located
  };
}

// Pick live if possible, else degrade to the recorded fixture.
export async function autoScorer() {
  if (process.env.TYPESAFEAI_KEY && !process.env.JEV_FOLD_OFFLINE) {
    const live = liveScorer();
    try {
      await live("2 + 2 = 4.");
      return { score: live, source: "live" };
    } catch (e) {
      console.error(`JEV unavailable (${e.message}); using recorded fixture`);
    }
  }
  return { score: fixtureScorer(), source: "fixture" };
}

export function render(r) {
  const bar = (n) => "█".repeat(Math.round(n * 20)).padEnd(20, "·");
  const lines = [`whole  ${bar(r.whole)} ${r.whole.toFixed(2)}  ${r.claim}`];
  for (const l of r.leaves) {
    lines.push(`${l === r.weakest ? "→ part" : "  part"} ${bar(l.noul)} ${l.noul.toFixed(2)}  ${l.text}`);
  }
  lines.push(`weakest: "${r.weakest.text}"  divergence(whole−min)=${r.divergence}  margin=${r.margin}`);
  return lines.join("\n");
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const claim =
    process.argv.slice(2).join(" ") ||
    "The Eiffel Tower is in Paris, and the Great Wall of China is in Japan, and water freezes at 0 degrees Celsius.";
  const { score, source } = await autoScorer();
  const r = await fold(claim, { score });
  console.log(`[source: ${source}]\n${render(r)}`);
}
