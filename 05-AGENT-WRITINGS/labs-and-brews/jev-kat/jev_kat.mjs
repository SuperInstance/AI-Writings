#!/usr/bin/env node
/**
 * jev_kat.mjs — known-answer control for the JEV oracle client.
 *
 * WHY
 *
 * The fleet uses JEV (typesafe.ai /v1/systemone) as a canon gate: promote a claim only
 * if p > 0.7. A gate is only as good as the instrument behind it, and this instrument has
 * never been characterised. Three question types are available (noul / choice / score) and
 * only one had been used.
 *
 * A KAT is the cheapest possible test of an instrument: feed it cases whose correct
 * answer you already know, and see whether it finds them. This is the same discipline the
 * keeper's own lode protocol already requires of its Elo scorer ("the scorer itself is
 * deterministic and stranger-verifiable", KAT 1/1). JEV has had no equivalent.
 *
 * WHAT THIS ALREADY FOUND
 *
 * The `score` type fails a naive KAT: fed numpy (2.58), a 1,285-assertion reference port
 * with green CI (2.59), and an empty shell (2.61), it returns a near-constant ~2.6 at
 * ~0.62 confidence regardless of input. Confidence does not drop to signal the failure.
 *
 * That does not prove `score` is useless — it proves `score` does not DISCRIMINATE on
 * absolute ratings. A constant output is still compatible with a useful RANKING if the
 * ordering is preserved under repetition. This script measures both properties separately:
 * discrimination (does it spread?) and rank-stability (does the ordering survive?).
 *
 * That distinction is the whole point. A gate that only ever asks "is this above 0.7"
 * needs discrimination. A gate that only ever asks "which of these ranks higher" needs
 * rank-stability. They are different requirements and only one was ever being assumed.
 *
 * USAGE
 *   node jev_kat.mjs            # full run, all three types
 *   node jev_kat.mjs --quick    # noul + choice only
 *   node jev_kat.mjs --json
 *
 * Exit 0 = every type met its bar. Exit 2 = at least one did not. Nothing partial.
 */

const KEY = process.env.TYPESAFEAI_KEY;
const BASE = 'https://api.typesafe.ai/v1/systemone';
if (!KEY) { console.error('TYPESAFEAI_KEY not set'); process.exit(2); }

async function jev(state, questions, model = 'jev-latest') {
  // The upstream edge intermittently returns 503. A control harness that aborts on a
  // transient blip measures the network, not the instrument — so retry with backoff and
  // record how many retries each call needed. That count is itself a small finding.
  RETRIES.n++;
  for (let attempt = 0; attempt <= 4; attempt++) {
    let r;
    try {
      r = await fetch(BASE, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${KEY}`, 'Content-Type': 'application/json' },
        body: JSON.stringify({ model, state, questions }),
      });
    } catch (e) {
      if (attempt === 4) throw new Error(`network after 5 attempts: ${e.message}`);
      await sleep(600 * 2 ** attempt);
      RETRIES.retried++;
      continue;
    }
    if (r.ok) return r.json();
    if (r.status === 503 || r.status === 429) {
      if (attempt === 4) throw new Error(`HTTP ${r.status} persistent after 5 attempts`);
      await sleep(600 * 2 ** attempt);
      RETRIES.retried++;
      continue;
    }
    throw new Error(`HTTP ${r.status}: ${(await r.text()).slice(0, 120)}`);
  }
  throw new Error('unreachable');
}

const sleep = ms => new Promise(r => setTimeout(r, ms));
const RETRIES = { n: 0, retried: 0 };

/* ── the KAT corpus ───────────────────────────────────────────────────── */

// Subjects with a KNOWN ordering on two independent axes.
// absolute: how usable is this to a stranger with no context?  (known: numpy >> refport > shell)
// rank-only: which of these is more finished, relative to the others? (known ordering)
const SUBJECTS = [
  ['numpy', 'The NumPy library. Thirty years of development, millions of dependents, used by nearly every Python data scientist. Extensive test suite, continuous integration, clear contributor documentation, stable public API with deprecation policy.'],
  ['c99_ref_port', 'C99 reference port of a 5-opcode cell model. 1,285 automated assertions across 7 suites, a one-command verify entry point, a sha256 receipt, CI green on a fresh runner, Apache-2.0 license detected. Referenced by zero other repos.'],
  ['empty_shell', 'A repository containing one README file that says "work in progress". No source code, no tests, no CI, no license, last commit eight months ago.'],
];

// For noul we must separate THREE regimes, because conflating them is how you end up
// measuring the wrong thing.
//
//   REGIME A1 — no prior, genuinely unknowable. "Does this unknown private repo have 1000
//   stars?" The model has no prior and cannot look. A calibrated model sits near 0.5. A
//   model that swings to 0.95 is confabulating. NEAR-0.5 IS CORRECT.
//
//   REGIME A2 — no prior, but widely known. "Is numpy widely used?" The model has no prior
//   about THIS REPO, but numpy is public knowledge. A calibrated model MAY answer
//   confidently, and should. Uncertainty here would be the failure, not confidence.
//
//   REGIME B — judgement with stated criteria. This is the regime the fleet's p>0.7 canon
//   gate actually lives in, and the only regime where spread above 0.7 means anything.
//
// Two bugs this KAT found in ITSELF, both worth recording:
//
//  1. The first version put A1 and A2 in one bucket and scored the model's correct
//     confidence in A2 as an overconfidence failure. Wrong expected value; a KAT whose
//     expectations are wrong is worse than no KAT because it reports false failures.
//
//  2. A1 was originally phrased as a META-question — "can it be determined whether this
//     repo has 1000 stars?" — which invites a confident "no". A confident "no" there is
//     the right answer, and the test scored it as overconfidence. A calibration probe must
//     ask about the FACT, not about the knowability of the fact.
//
// Both bugs would have been reported as instrument failures. Neither touched the model.
//
//   REGIME B — judgement with stated criteria. "Is this registry append-only and
//   byte-verified?" The model CAN weigh this from the description against the criteria.
//   This is the regime the fleet's p>0.7 canon gate actually lives in, and it is the
//   only regime where spread above 0.7 means anything.
//
// The original version of this KAT only ran regime A and reported it as a failure. That
// was a bug in the KAT, not in the instrument. Measuring the regimes separately is the
// point of having a known-answer control at all.
const NOUL_JUDGEMENT = [
  ['regimeA1_unknowable', 'A private GitHub repository owned by an unknown person, described only as "some code".', 'Does this repository have more than 1000 GitHub stars?', false],
  ['regimeA2_widely_known', 'The NumPy library, a scientific computing package for Python.', 'Is this repository widely used, with extensive test coverage and millions of dependents?', true],
  ['regimeA2_obscure_true', 'The International System of Units, the standard used to define units of measurement worldwide.', 'Is this a widely adopted international standard?', true],
  ['regimeB_weak', 'A registry file described as "a JSONL file containing prediction records".', 'Does the description state that the registry is append-only and protected against modification by a byte-prefix check?', false],
  ['regimeB_strong', 'A registry file described as "a JSONL file containing prediction records. Every line is sealed with a sha256 of its own prediction text, the file is append-only, and a validator proves the old file is a byte-prefix of the new one across commits. Editing a sealed line is impossible without breaking the hash chain."', 'Does the description state that the registry is append-only and protected against modification by a byte-prefix check?', true],
  ['regimeB_strawman', 'A registry file described as "a JSONL file containing prediction records. The team is careful and does not usually change old entries."', 'Does the description state that the registry is append-only and protected against modification by a byte-prefix check?', false],
];

/* ── measure the two properties separately ─────────────────────────────── */

function stats(vals) {
  if (vals.length < 2) return { spread: 0, min: vals[0], max: vals[0] };
  const min = Math.min(...vals), max = Math.max(...vals);
  return { spread: max - min, min, max };
}

async function katScore(reps = 2) {
  const rubric = [
    '0 — invisible: no README, or the README does not explain what it is.',
    '1 — described: a README explains it, but there is nothing to run.',
    '2 — runnable: a stranger can execute something in under 10 minutes.',
    '3 — verifiable: runnable, with a machine-checkable receipt or test suite a stranger can independently confirm.',
    '4 — composable: an outside agent can depend on it through a stable interface and get a receipt back.',
  ];
  const perSubject = {};
  for (const [name, desc] of SUBJECTS) perSubject[name] = [];
  const orderings = [];

  for (let rep = 0; rep < reps; rep++) {
    const q = {};
    for (const [name, desc] of SUBJECTS) {
      q[name] = { type: 'score', instructions: 'How usable is this to a stranger who has no context?', criteria: rubric };
    }
    const state = SUBJECTS.map(([n, d]) => `${n}: ${d}`).join('; ');
    const res = await jev(state, q);
    const scored = SUBJECTS.map(([n]) => res.answers[n]?.score).filter(Number.isFinite);
    for (const [name] of SUBJECTS) {
      const s = res.answers[name]?.score;
      if (Number.isFinite(s)) perSubject[name].push(s);
    }
    orderings.push(SUBJECTS.map(([n]) => n).sort((a, b) =>
      (res.answers[b]?.score ?? 0) - (res.answers[a]?.score ?? 0)));
    if (rep < reps - 1) await sleep(400);
  }

  const means = Object.fromEntries(
    Object.entries(perSubject).map(([k, v]) => [k, v.reduce((a, b) => a + b, 0) / v.length]));
  const spread = stats(SUBJECTS.map(([n]) => means[n]));
  // known ordering for ABSOLUTE usability: numpy > c99_ref_port > empty_shell
  const expectedAbs = ['numpy', 'c99_ref_port', 'empty_shell'];
  const gotAbs = [...expectedAbs].sort((a, b) => means[b] - means[a]);
  const absCorrect = expectedAbs.every((n, i) => gotAbs[i] === n);
  // rank-stability: does the ordering repeat identically across reps?
  const rankStable = orderings.every(o => o.join('>') === orderings[0].join('>'));

  return {
    type: 'score', reps, means, spread: spread.spread,
    absolute_ordering_correct: absCorrect,
    got: gotAbs, expected: expectedAbs,
    rank_stable: rankStable,
    discriminates: spread.spread >= 0.5,
    verdict: (spread.spread >= 0.5 && absCorrect) ? 'PASS' : 'FAIL_DISCRIMINATION',
  };
}

async function katNoul() {
  const cases = [];
  for (const [id, state, q, truth] of NOUL_JUDGEMENT) {
    const r = await jev(state, {
      [id]: { type: 'noul', instructions: q,
              criteria: { true: 'Yes, this is the case.', false: 'No, this is not the case.' } },
    });
    const p = r.answers[id]?.noul;
    const regime = id.startsWith('regimeA1') ? 'A1_unknowable'
                : id.startsWith('regimeA2') ? 'A2_widely_known' : 'B_judgement';
    cases.push({ id, regime, truth, noul: p,
                 direction_correct: p === undefined ? null : ((p > 0.5) === truth) });
    await sleep(350);
  }
  const A1 = cases.filter(c => c.regime === 'A1_unknowable');
  const A2 = cases.filter(c => c.regime === 'A2_widely_known');
  const B  = cases.filter(c => c.regime === 'B_judgement');
  // A1: must be UNCERTAIN. Assert it does not confidently assert what it cannot know.
  const A1overconfident = A1.filter(c => Math.abs((c.noul ?? 0.5) - 0.5) > 0.35).length;
  // A2: must be CONFIDENT about things that really are public knowledge.
  const A2confident = A2.filter(c => (c.noul ?? 0) > 0.5).length;
  // B: spread must exist and the strongly-grounded case must rank highest.
  const Bs = B.map(c => c.noul).filter(Number.isFinite);
  const Bspread = Bs.length > 1 ? Math.max(...Bs) - Math.min(...Bs) : 0;
  const okB = B.filter(c => c.direction_correct === true).length;
  const Bmax = Math.max(...B.map(x => x.noul ?? 0));
  const BstrongestHighest = (B.find(c => c.id === 'regimeB_strong')?.noul ?? 0) === Bmax;

  // Verdict is per-regime, not per-type. Collapsing them produced a false "noul is
  // broken" reading, because noul is well-behaved in the regime the fleet actually uses
  // (B: judgement against stated criteria) and only misbehaves when asked about facts it
  // cannot possibly know (A1).
  const regimeB_passes = okB === B.length && Bspread >= 0.3 && BstrongestHighest;
  const a1_passes = A1overconfident === 0;
  const A1values = A1.map(c => c.noul).filter(Number.isFinite);
  return {
    type: 'noul', n: cases.length, cases,
    regimeA1: { n: A1.length, overconfident: A1overconfident, values: A1values,
                correct_behaviour: 'near 0.5 on what it cannot know',
                passes: a1_passes,
                note: a1_passes ? 'calibrated on unknowable facts'
                     : 'ANSWERS UNKNOWABLE FACTS WITH CONFIDENCE — do not ask noul a question whose answer requires facts the model does not have' },
    regimeA2: { n: A2.length, confident: A2confident,
                correct_behaviour: 'confident about genuine public knowledge',
                passes: A2confident === A2.length },
    regimeB:  { n: B.length, direction_correct: okB, spread: Bspread, strongest_ranked_highest: BstrongestHighest,
                correct_behaviour: 'spread, with the strongly-grounded case highest',
                passes: regimeB_passes },
    discriminates: regimeB_passes,
    // The fleet's p>0.7 canon gate lives in regime B. That is what the verdict tracks.
    verdict: regimeB_passes ? 'PASS' : 'FAIL',
    verdict_scope: 'regime B (judgement against stated criteria) — the regime the canon gate uses',
    warning: a1_passes ? null : 'A1 overconfidence: noul answers unknowable facts confidently. Harmless for the canon gate; dangerous for any use as a fact-checker.',
  };
}

async function katChoice() {
  // A choice with a known winner, plus a deliberately ambiguous one.
  const r1 = await jev('A 2,856-pound Chinook salmon was landed. A 3-pound salmon was landed. Which is heavier?',
    { w: { type: 'choice', instructions: 'Which is heavier?',
           criteria: { big: 'The 2,856-pound Chinook salmon.', small: 'The 3-pound salmon.' } } });
  const w1 = r1.answers.w;
  const r2 = await jev('A 2,856-pound Chinook salmon was landed. A 3-pound salmon was landed. Which is heavier?',
    { w: { type: 'choice', instructions: 'Which is heavier?',
           criteria: { undetermined: 'Neither; the information given is insufficient.',
                       big: 'The 2,856-pound Chinook salmon.', small: 'The 3-pound salmon.' } } });
  const w2 = r2.answers.w;
  const correct = w1?.choice === 'big';
  const confident = (w1?.confidence ?? 0) > 0.7;
  const probs = w1?.probabilities ?? {};
  const spreadP = Math.max(...Object.values(probs)) - Math.min(...Object.values(probs));
  return {
    type: 'choice', correct_choice: w1?.choice, expected: 'big',
    correct, confidence: w1?.confidence, prob_spread: spreadP,
    ambiguous_case: w2?.choice,
    discriminates: correct && confident && spreadP > 0.3,
    verdict: (correct && confident && spreadP > 0.3) ? 'PASS' : 'FAIL',
  };
}

/* ── main ──────────────────────────────────────────────────────────────── */

async function main() {
  const args = process.argv.slice(2);
  const quick = args.includes('--quick');
  const asJson = args.includes('--json');

  console.log('JEV known-answer control (KAT)');
  console.log('='.repeat(72));
  console.log(`endpoint: ${BASE}`);
  console.log(`mode:     ${quick ? 'quick (noul + choice)' : 'full (all three types)'}`);
  console.log('='.repeat(72));

  const out = { schema: 'fleet/jev-kat@v1', ts: new Date().toISOString() };

  out.noul = await katNoul();
  console.log('');
  console.log('── noul ──────────────────────────────────────────────────────────');
  for (const c of out.noul.cases) {
    console.log(`  ${c.regime[0]} ${c.direction_correct ? 'ok  ' : 'MISS'} noul=${String(c.noul).padEnd(6)} expected=${c.truth ? 'true ' : 'false'}  ${c.id}`);
  }
  console.log(`  regime A1 (unknowable, correct = uncertain): ${out.noul.regimeA1.overconfident} overconfident of ${out.noul.regimeA1.n}  values=[${out.noul.regimeA1.values}]`);
  if (out.noul.warning) console.log(`  WARNING: ${out.noul.warning}`);
  console.log(`  regime A2 (widely known, correct = confident): ${out.noul.regimeA2.confident}/${out.noul.regimeA2.n} confident`);
  console.log(`  regime B (judgement, correct = spread):  ${out.noul.regimeB.direction_correct}/${out.noul.regimeB.n} right, spread ${out.noul.regimeB.spread.toFixed(2)}`);
  console.log(`  VERDICT: ${out.noul.verdict}  scope: ${out.noul.verdict_scope}`);

  out.choice = await katChoice();
  console.log('');
  console.log('── choice ────────────────────────────────────────────────────────');
  console.log(`  chose ${out.choice.correct_choice} (expected ${out.choice.expected})  confidence=${out.choice.confidence}  prob spread=${out.choice.prob_spread?.toFixed(2)}`);
  console.log(`  ambiguous case answered: ${out.choice.ambiguous_case}`);
  console.log(`  VERDICT: ${out.choice.verdict}  (discriminates: ${out.choice.discriminates})`);

  if (!quick) {
    out.score = await katScore(2);
    console.log('');
    console.log('── score ────────────────────────────────────────────────────────');
    for (const [n, m] of Object.entries(out.score.means)) {
      console.log(`  ${n.padEnd(16)} mean=${m.toFixed(3)}`);
    }
    console.log(`  spread: ${out.score.spread.toFixed(3)}  (>= 0.50 required to discriminate)`);
    console.log(`  expected ordering: ${out.score.expected.join(' > ')}`);
    console.log(`  actual   ordering: ${out.score.got.join(' > ')}   ${out.score.absolute_ordering_correct ? 'CORRECT' : 'WRONG'}`);
    console.log(`  rank-stable across reps: ${out.score.rank_stable}`);
    console.log(`  VERDICT: ${out.score.verdict}`);
  }

  const all = quick ? [out.noul, out.choice] : [out.noul, out.choice, out.score];
  const failing = all.filter(r => r.verdict !== 'PASS');
  console.log('');
  console.log('='.repeat(72));
  console.log(`types passing: ${all.length - failing.length}/${all.length}`);
  if (failing.length) {
    console.log('');
    console.log('READING THE FAILURES');
    console.log('  A type can fail this KAT and still be useful — the question is WHICH use.');
    console.log('  A constant output cannot serve an absolute threshold gate (p>0.7) because the');
    console.log('  threshold has nothing to bite on. It may still serve a RANKING gate if the');
    console.log('  ordering survives repetition. Measure the property you are going to depend on,');
    console.log('  not the one you assume.');
  }
  console.log('='.repeat(72));
  console.log(`upstream calls: ${RETRIES.n}  retries after 503: ${RETRIES.retried}`);
  out.upstream = { ...RETRIES };
  console.log('='.repeat(72));

  if (asJson) console.log(JSON.stringify(out, null, 2));
  process.exit(failing.length ? 2 : 0);
}

main().catch(e => { console.error('KAT failed:', e.message); process.exit(2); });
