// node --test labs/jev-fold/fold.test.mjs   (offline by default; JEV_FOLD_LIVE=1 adds a live check)
import { test } from "node:test";
import assert from "node:assert/strict";
import { split, fold, fixtureScorer, liveScorer } from "./fold.mjs";

const CLAIM =
  "The Eiffel Tower is in Paris, and the Great Wall of China is in Japan, and water freezes at 0 degrees Celsius.";
const FALSE_PART = "the Great Wall of China is in Japan";

test("split finds the three clauses", () => {
  assert.deepEqual(split(CLAIM), [
    "The Eiffel Tower is in Paris",
    FALSE_PART,
    "water freezes at 0 degrees Celsius",
  ]);
});

test("fold locates the known false part (recorded fixture)", async () => {
  const r = await fold(CLAIM, { score: fixtureScorer() });
  assert.equal(r.weakest.text, FALSE_PART);
  assert.ok(r.margin > 0.5, "false part is clearly separated from the true ones");
  assert.equal(r.divergence, +(r.whole - r.fold_min).toFixed(4));
});

test("fold honours explicit parts and rejects unsplittable claims", async () => {
  const score = async (s) => (s.includes("Ag") ? 0.1 : 0.9);
  const r = await fold("x", { score, parts: ["gold is Au", "gold is Ag"] });
  assert.equal(r.weakest.text, "gold is Ag");
  await assert.rejects(fold("Paris is in France.", { score }));
});

test("live JEV locates the false part", { skip: !process.env.JEV_FOLD_LIVE }, async () => {
  const r = await fold(CLAIM, { score: liveScorer() });
  assert.equal(r.weakest.text, FALSE_PART);
});
