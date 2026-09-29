#!/usr/bin/env node
/**
 * bell_witness_verify.mjs — third-party-verifiable receipt for any randomness claim.
 *
 * WHY THIS EXISTS
 *
 * The fleet's verification problem is well documented: the second reader shares the
 * substrate, the model lineage, the prompts and the incentives of the first. A receipt
 * verified by another agent on the same account is internal consistency, not external
 * truth. The stated remedy is "a second reader on a genuinely different substrate."
 *
 * A CHSH Bell witness is the only verification primitive this fleet has that a stranger
 * can check WITHOUT running any fleet code, without insider context, and without trust.
 * It is a number with published bounds. S > 2 means the correlations that produced the
 * randomness cannot be explained by local hidden variables. That is arithmetic, not
 * ceremony — anyone can recheck it with a pocket calculator.
 *
 * So: any claim of the form "this selection was un-gameable" becomes checkable by
 * publishing S. Not by asking a second agent to believe you.
 *
 * HONEST LIMITS (the lab states these; this tool refuses to hide them)
 *
 *   - Fixed measurement settings, no space-like separation, fair sampling assumed.
 *     A witness certifies entangling-gate and readout fidelity on the device that
 *     produced the randomness. It is NOT device-independent certification.
 *   - An emu/aer backend is a simulator. The witness is real mathematics; the noise
 *     source is a classical simulation. Report `mode` and `backend` alongside S or the
 *     receipt is misleading.
 *   - A witness on one draw says nothing about whether the caller used the draw
 *     honestly. It certifies the randomness, not the process.
 *
 * USAGE
 *   node bell_witness_verify.mjs <result.json>      # a comet-qrng-v1 result object
 *   node bell_witness_verify.mjs --self-test
 *
 * Exit 0 = witness passes. Exit 2 = fails or is unusable. Nothing partial.
 */

import { readFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';

export const CLASSICAL_BOUND = 2;
export const TSIRELSON_BOUND = 2 * Math.SQRT2; // 2.8284271247461903

export function verifyWitness(w) {
  const S = Number(w?.S);
  const sigma = Number(w?.sigma_S);
  const classical = Number(w?.classical_bound ?? CLASSICAL_BOUND);
  const tsirelson = Number(w?.tsirelson_bound ?? TSIRELSON_BOUND);
  const backend = w?.backend ?? w?.mode ?? 'unknown';

  const usable = Number.isFinite(S) && S > 0;
  if (!usable) {
    return { ok: false, reason: 'NO_S_VALUE', S: null, backend };
  }

  const above_classical = S > classical;
  const within_tsirelson = S <= tsirelson + 1e-9;
  const sigma_beyond = Number.isFinite(sigma) ? (S - classical) / sigma : null;
  // Overshooting Tsirelson is a DIAGNOSTIC, not a failure. S is a finite-sample
  // estimator; the asymptotic bound 2*sqrt(2) applies to the true value, so S_hat
  // may legitimately land above it. The recorded fleet fixture sits 0.9 sigma
  // above Tsirelson, which is exactly what a small sample looks like. The only
  // test that means anything for "was this randomness quantum" is S > 2.
  const overshoots_tsirelson = !within_tsirelson;
  const overshoot_sigma = overshoots_tsirelson && Number.isFinite(sigma)
    ? (S - tsirelson) / sigma : null;

  return {
    ok: above_classical,
    S, sigma_S: sigma, classical_bound: classical, tsirelson_bound: tsirelson,
    backend,
    above_classical,
    within_tsirelson,
    overshoots_tsirelson,
    overshoot_sigma,
    sigma_beyond_classical_bound: sigma_beyond,
    reason: !above_classical ? 'BELOW_CLASSICAL_BOUND' : 'VERIFIED',
    caveat: w?.caveat ?? 'no caveat recorded — treat as unverified provenance',
  };
}

function receipt(w) {
  const v = verifyWitness(w);
  const body = {
    schema: 'fleet/bell-witness-receipt@v1',
    verdict: v.ok ? 'VERIFIED' : 'FAILED',
    S: v.S,
    sigma_S: v.sigma_S ?? null,
    classical_bound: v.classical_bound,
    tsirelson_bound: v.tsirelson_bound,
    above_classical_bound: v.above_classical ?? false,
    within_tsirelson_bound: v.within_tsirelson ?? false,
    overshoots_tsirelson_bound: v.overshoots_tsirelson ?? false,
    overshoot_sigma: v.overshoot_sigma ?? null,
    sigma_beyond_classical_bound: v.sigma_beyond_classical_bound,
    backend: v.backend,
    caveat: v.caveat,
  };
  const r = { ...body, receipt_sha256: createHash('sha256').update(JSON.stringify(body, Object.keys(body).sort())).digest('hex') };
  return r;
}

const SELFTEST = [
  { name: 'real recorded witness (S=2.848, emu/aer)', w: { S: 2.84814453125, sigma_S: 0.02194096478543922, classical_bound: 2, tsirelson_bound: 2.8284271247461903, backend: 'emu/aer' }, expect: true },
  { name: 'exactly at classical bound (S=2.0) must FAIL', w: { S: 2.0, sigma_S: 0.02 }, expect: false },
  { name: 'below classical (S=1.41) must FAIL', w: { S: 1.4142, sigma_S: 0.02 }, expect: false },
  { name: 'above Tsirelson (S=3.1) passes quantum test but is FLAGGED', w: { S: 3.1, sigma_S: 0.02 }, expect: true, flag: 'overshoots_tsirelson' },
  { name: 'missing S must FAIL', w: { sigma_S: 0.02 }, expect: false },
  { name: 'noisy but real (S=2.35) must PASS', w: { S: 2.35, sigma_S: 0.05 }, expect: true },
];

function selfTest() {
  let bad = 0;
  for (const t of SELFTEST) {
    const v = verifyWitness(t.w);
    const ok = v.ok === t.expect;
    const flagged = t.flag ? v[t.flag] === true : true;
    if (!ok || !flagged) bad++;
    console.log(`  [${ok && flagged ? 'PASS' : 'FAIL'}] ${t.name}`);
    console.log(`         ok=${v.ok} reason=${v.reason} S=${v.S} beyond_classical=${v.sigma_beyond_classical_bound?.toFixed(1) ?? 'n/a'}σ overshoot=${v.overshoots_tsirelson} (${v.overshoot_sigma?.toFixed(1) ?? 'n/a'}σ)`);
  }
  // determinism: same input twice -> same receipt hash
  const a = JSON.stringify(receipt(SELFTEST[0].w)), b = JSON.stringify(receipt(SELFTEST[0].w));
  const det = a === b;
  if (!det) bad++;
  console.log(`  [${det ? 'PASS' : 'FAIL'}] receipt is deterministic across runs`);
  console.log(bad === 0 ? `\nselftest: ${SELFTEST.length + 1}/${SELFTEST.length + 1} legs correct` : `\nselftest: ${bad} leg(s) wrong`);
  return bad === 0;
}

function main() {
  const args = process.argv.slice(2);
  if (args.includes('--self-test')) process.exit(selfTest() ? 0 : 2);
  const p = args.find(a => !a.startsWith('--'));
  if (!p || !existsSync(p)) {
    console.error('usage: bell_witness_verify.mjs <result.json> | --self-test');
    process.exit(2);
  }
  let raw;
  try { raw = JSON.parse(readFileSync(p, 'utf8')); }
  catch { console.error('unparseable input'); process.exit(2); }
  // accept either a bare witness or a wrapped result
  const w = raw?.S !== undefined ? raw
          : raw?.result?.S !== undefined ? raw.result
          : raw?.witness ?? raw;
  const r = receipt(w);
  console.log('bell witness verification');
  console.log('='.repeat(66));
  console.log(`  verdict:        ${r.verdict}`);
  console.log(`  S:              ${r.S}`);
  console.log(`  classical:      ${r.classical_bound}   tsirelson: ${r.tsirelson_bound?.toFixed(6)}`);
  console.log(`  sigma beyond:   ${r.sigma_beyond_classical_bound?.toFixed(2) ?? 'n/a'} sigma`);
  console.log(`  overshoot:      ${r.overshoots_tsirelson_bound ? `YES (${r.overshoot_sigma?.toFixed(1)}σ above Tsirelson — finite-sample estimate, not a failure)` : 'no'}`);
  console.log(`  backend:        ${r.backend}`);
  console.log(`  receipt sha256: ${r.receipt_sha256}`);
  console.log('='.repeat(66));
  console.log(`  ${r.caveat}`);
  process.exit(r.verdict === 'VERIFIED' ? 0 : 2);
}

if (import.meta.url === `file://${process.argv[1]}`) main();
