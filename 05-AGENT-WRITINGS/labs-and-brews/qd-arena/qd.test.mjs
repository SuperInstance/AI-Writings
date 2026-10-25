// node --test labs/qd-arena/qd.test.mjs   (offline replay; QD_ARENA_LIVE=1 adds a live JEV placement check)
import { test } from "node:test";
import assert from "node:assert/strict";
import { run, insert, place, parseCandidates, targetsFrom, contrast, render, fixtureSources, evalQuestions, evalState, ROSTER, CELLS } from "./qd.mjs";
import { jev } from "../weakest-claim/audit.mjs";

const LIVE = ROSTER.filter((e) => e.live);

test("insert keeps the best PER NICHE, not the global best", () => {
  const a = {};
  assert.equal(insert(a, { cell: "concrete/tool", quality: 2.9 }), "new");
  assert.equal(insert(a, { cell: "abstract/ritual", quality: 0.8 }), "new"); // far worse globally, still kept
  assert.equal(insert(a, { cell: "abstract/ritual", quality: 0.5 }), "rejected");
  assert.equal(insert(a, { cell: "abstract/ritual", quality: 1.1 }), "improved");
  assert.equal(Object.keys(a).length, 2);
});

test("place uses JEV's argmax bins and expected-rung quality", () => {
  const c = place({ name: "x" }, { quality: { score: 2.2 }, grain: { choice: "middle" }, form: { choice: "ritual" } });
  assert.deepEqual([c.cell, c.quality], ["middle/ritual", 2.2]);
});

test("parseCandidates reads NAME :: pitch lines and skips chatter", () => {
  const cs = parseCandidates("Here you go:\n1. **Tidewatch** :: a shared log of every haul and where it came from\n- Knot :: ties", "m");
  assert.equal(cs.length, 1);
  assert.deepEqual([cs[0].name, cs[0].model], ["Tidewatch", "m"]);
});

test("targetsFrom maps quantum draw values onto the 3×3 grid", () => {
  assert.deepEqual(targetsFrom([0, 8, 4], 4), ["concrete/tool", "abstract/ritual", "middle/practice", "concrete/tool"]);
});

test("recorded live run replays: unsteered gen 0 collapses to one niche, QD illuminates 7/9", async () => {
  const src = fixtureSources();
  const r = await run({ generators: LIVE, sources: src });
  const k = contrast(r);
  assert.equal(Object.keys(k.gen0).length, 1, "all 18 unsteered candidates share one niche");
  assert.equal(k.gen0["middle/tool"], 18);
  assert.equal(Object.keys(r.archive).length, 7);
  assert.deepEqual(r.history.map((h) => h.filled), [1, 4, 7]);
  assert.ok(r.history.slice(1).every((h) => h.draw.S > 2), "Bell witness above classical bound");
  assert.equal(k.best.name, "HOLDMARK");
  assert.match(render(r), /single best-of would return ONE idea/);
});

test("live JEV places a clear ritual in a ritual column", { skip: !process.env.QD_ARENA_LIVE }, async () => {
  const a = await jev(evalState({ name: "Dawn Tally", pitch: "each morning the crew recites yesterday's worst catch aloud before casting nets" }), evalQuestions());
  assert.equal(a.form.choice, "ritual");
  assert.ok(a.quality.score >= 0 && a.quality.score <= 3);
});
