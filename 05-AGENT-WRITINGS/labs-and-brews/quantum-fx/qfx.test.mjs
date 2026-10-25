// node --test labs/quantum-fx/qfx.test.mjs   (offline fixture replay; QFX_LIVE=1 with MOTHQUANTUM_* set adds live checks)
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createClient, fixtureFetch, MothError, UA } from "./qfx.mjs";

const FX = JSON.parse(readFileSync(new URL("./fixtures.json", import.meta.url), "utf8")).engines;
const offline = (extra = {}) => createClient({ base: "https://fixture.invalid", key: "k", fetch: fixtureFetch({ ...FX, ...extra }), sleep: async () => {} });

test("every request carries the browser UA and bearer key", async () => {
  const seen = [];
  const inner = fixtureFetch(FX);
  const q = createClient({ base: "https://fixture.invalid", key: "k", sleep: async () => {}, fetch: (u, i) => (seen.push(i.headers), inner(u, i)) });
  await q.coinToss({ shots: 32 });
  assert.equal(seen.length, 3); // submit, status, result
  for (const h of seen) {
    assert.equal(h["user-agent"], UA);
    assert.equal(h.authorization, "Bearer k");
  }
});

test("qrng replays: d6 in range, floats in [0,1), Bell S above the classical bound", async () => {
  const d = await offline().qrng({ integers: { min: 1, max: 6, count: 8 }, floats: 3 });
  assert.equal(d.integers.length, 8);
  assert.ok(d.integers.every((x) => x >= 1 && x <= 6));
  assert.equal(d.floats.length, 3);
  assert.ok(d.floats.every((x) => x >= 0 && x < 1));
  assert.match(d.hex, /^[0-9a-f]+$/);
  assert.ok(d.S > d.classical_bound);
});

test("effect engines replay with their normalised shapes", async () => {
  const q = offline();
  const c = await q.coinToss({ shots: 32 });
  assert.equal(c.heads + c.tails, c.shots);
  const b = await q.blur([0, 0, 0, 8, 0, 0, 0, 0], { strength: 0.1 });
  assert.equal(b.output.length, 8);
  assert.equal(Math.max(...b.output), 8); // rescaled to the input max
  assert.ok(b.output[2] > 0 && b.output[4] > 0); // the spike leaked into its neighbours
  const p = await q.qpixl([0.05, 0.2, 0.4, 0.6, 0.8, 0.95]);
  assert.equal(p.output.length, 6);
  const e = await q.qec({ seed: 7 });
  assert.ok(e.success_rate > 0.5 && e.success_rate <= 1);
});

test("a failed job surfaces the engine's error type, not a bare 409", async () => {
  const bad = {
    submit: { job_id: "bad-job" },
    status: { job_id: "bad-job", status: "failed", error: { type: "unparseable_values", message: "`values` string must be wrapped in [..]", retryable: false } },
    result: {},
  };
  await assert.rejects(offline({ "qpixl-v1": bad }).qpixl("0.1,0.2"), (e) => e instanceof MothError && e.type === "unparseable_values" && e.job_id === "bad-job");
});

test("qrng retries a job that completes with no conditioned bytes", async () => {
  const empty = { result: { output: { random: { derivation_error: "conditioned bytes ran out" } } } };
  let submits = 0;
  const inner = fixtureFetch(FX);
  const q = createClient({
    base: "https://fixture.invalid", key: "k", sleep: async () => {},
    fetch: async (u, i) => {
      if (u.endsWith("/process")) submits++;
      if (submits === 1 && u.endsWith("/result")) return { ok: true, status: 200, text: async () => JSON.stringify(empty) };
      return inner(u, i);
    },
  });
  const d = await q.qrng({ integers: { min: 1, max: 6, count: 8 } });
  assert.equal(submits, 2);
  assert.equal(d.integers.length, 8);
});

const live = process.env.QFX_LIVE && process.env.MOTHQUANTUM_KEY && process.env.MOTHQUANTUM_BASE;
test("live: engine list includes every wrapped engine", { skip: !live }, async () => {
  const ids = (await createClient().engines()).map((e) => e.engine_id);
  for (const id of ["comet-qrng-v1", "coin-toss-v1", "blur-core-v1", "qpixl-v1", "tamagotchi-v1"]) assert.ok(ids.includes(id), id);
});

test("live: coin toss counts add up", { skip: !live }, async () => {
  const c = await createClient().coinToss({ shots: 8 });
  assert.equal(c.heads + c.tails, 8);
});
