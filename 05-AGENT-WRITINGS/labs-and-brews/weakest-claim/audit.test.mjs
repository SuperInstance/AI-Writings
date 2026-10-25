// node --test labs/weakest-claim/audit.test.mjs   (offline replay; WEAKEST_CLAIM_LIVE=1 adds a live JEV check)
import { test } from "node:test";
import assert from "node:assert/strict";
import { fileURLToPath } from "node:url";
import { audit, localize, adversary, pickBypasses, fixtureSources, guaranteeScorer, loadTarget, report } from "./audit.mjs";

const TARGET = loadTarget(fileURLToPath(new URL("./targets/jev-fold.json", import.meta.url)));
const SPLITTER = TARGET.parts[0];

test("pickBypasses keeps the first k distinct drawn indices", () => {
  assert.deepEqual(pickBypasses([8, 2, 8, 0, 1, 5], 3), [8, 2, 0]);
  assert.deepEqual(pickBypasses([4, 4, 4], 3), [4]);
});

test("recorded live audit replays: splitter located, 2/3 adversaries land", async () => {
  const r = await audit(TARGET, fixtureSources());
  assert.equal(r.loc.weakest.text, SPLITTER);
  assert.equal(r.adv.tested, 3);
  assert.equal(r.adv.hits, 2);
  assert.ok(r.adv.draw.S > 2, "Bell witness above the classical bound");
  assert.match(report(r), /ranking \+ hit-rate \+ divergence/);
});

test("adversary counts only 'defeats' verdicts and the auditor cannot choose the picks", async () => {
  const pool = ["p0", "p1", "p2", "p3"];
  const draw = async () => ({ values: [3, 3, 1, 0, 2, 2], S: 2.8 });
  const judge = async (s) => ({ choice: s.endsWith("p1") ? "holds" : "defeats" });
  const r = await adversary("leaf", pool, { draw, judge });
  assert.deepEqual(r.trials.map((t) => t.idx), [3, 1, 0]);
  assert.equal(r.hits, 2);
});

test("live JEV ranks the splitter or argmin leaf lowest", { skip: !process.env.WEAKEST_CLAIM_LIVE }, async () => {
  const loc = await localize(TARGET, { score: guaranteeScorer() });
  assert.ok([TARGET.parts[0], TARGET.parts[1]].includes(loc.weakest.text), loc.weakest.text);
});
