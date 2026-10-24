#!/usr/bin/env node
// ─────────────────────────────────────────────────────────────────────────────
// SITUATION S17 — "The Weakest Leaf"  ·  a PLAYABLE quilt situation
//
// Untested question it answers:
//   "Of all the guarantees a fleet tool advertises, WHICH ONE is its weakest —
//    the claim it makes most confidently that the fold can least defend — and
//    does that weakness survive an adversary nobody could have steered?"
//
// How PLAYING it produces the answer:
//   1. Take a real tool's headline guarantee (here: lever-runner's "the LLM never
//      sees your shell; injection-proof") and DECOMPOSE it into leaf-claims.
//   2. Project JEV around each leaf as a `noul` — P(this leaf is a sound absolute
//      guarantee).  The tree of nouls IS the visual logic; the entangled whole
//      abstracts to a single scalar, the fold LOCALIZES which leaf is rotten.
//   3. The whole−fold divergence measures how much the compound claim was hiding.
//   4. Moth draws the UN-GAMEABLE adversary: quantum dice pick which concrete
//      bypass-hypotheses get fired at the located weakest leaf, so the auditor
//      cannot stack the deck.  JEV (choice) adjudicates each drawn bypass.
//   5. DONE/answer signal: the located weakest leaf + whether its noul survives
//      the quantum-drawn adversary, stamped with Moth's provenance (hex + Bell S).
//
// This is a tool-improver: the located leaf is the next thing to harden (or stop
// overclaiming) in the tool under audit.  Point AUDIT_TARGET at any tool's spec.
//
// Cost envelope:  JEV ~cheap (1 whole + N leaf + up to K adversary noul/choice,
//                 ~450 in / ~40 out tokens each).  Moth: 1 run = 5 credits.
// Run:  node situations/play/weakest-leaf.mjs
//   Needs env: TYPESAFEAI_KEY, MOTHQUANTUM_KEY, MOTHQUANTUM_BASE
//   --no-moth  : skip the quantum draw (JEV-only, cents-cheap, deterministic-ish)
// ─────────────────────────────────────────────────────────────────────────────

const JEV_URL = "https://api.typesafe.ai/v1/systemone";
const JEV_KEY = (process.env.TYPESAFEAI_KEY || "").trim();
const MOTH_BASE = (process.env.MOTHQUANTUM_BASE || "").trim();
const MOTH_KEY = (process.env.MOTHQUANTUM_KEY || "").trim();
// Cloudflare error-1010 blocks non-browser fingerprints; a browser UA is load-bearing.
const UA =
  "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36";
const USE_MOTH = !process.argv.includes("--no-moth");

// ── The tool under audit (swap this block to audit any tool's spec) ──────────
const AUDIT_TARGET = {
  tool: "lever-runner",
  whole:
    "lever-runner is injection-proof: the LLM never sees your shell, files, " +
    "network, or env — it only ever emits a short intent phrase, and commands " +
    "are looked up from a pre-approved table and run in a per-session sandbox.",
  // Each leaf: the guarantee AS STATED. JEV judges whether it is a SOUND ABSOLUTE
  // guarantee (true) or has a plausible bypass / is an overclaim (false).
  leaves: [
    { id: "L1-phrase-only", claim:
      "The LLM emits ONLY a short intent phrase and can never inject a command, " +
      "because every command is looked up from a pre-approved table." },
    { id: "L2-sandbox", claim:
      "Every execution is fully contained in a per-session sandbox directory " +
      "(/tmp/lever-runner/<id>/) with no escape to the host filesystem." },
    { id: "L3-timeout", claim:
      "A hard timeout (default 30s) reliably kills any runaway command." },
    { id: "L4-trust-gate", claim:
      "Low-trust commands always require explicit human confirmation before running." },
    { id: "L5-no-secrets", claim:
      "The LLM never sees API keys, absolute paths, or environment variables." },
    { id: "L6-metachar", claim:
      "Shell injection is fully blocked: all arguments are validated and every " +
      "shell metacharacter is rejected." },
    { id: "L7-airgap", claim:
      "In passthrough mode ZERO data leaves the machine — there is no network call at all." },
  ],
  // Level-2 decomposition: atomic sub-claims per leaf. When a leaf is LOCATED as
  // weakest, the fold decomposes it AGAIN — the tree deepens, the logic gets more
  // visual, and the rot localizes to a single atom. (Provide for any leaf you like.)
  subleaves: {
    "L5-no-secrets": [
      "The LLM never sees API keys.",
      "The LLM never sees absolute filesystem paths.",
      "The LLM never sees environment variables.",
    ],
    "L6-metachar": [
      "The command VERB cannot carry a shell metacharacter.",
      "Every ARGUMENT value is validated so no metacharacter reaches the shell.",
      "Template parameters ({{param}}) cannot interpolate metacharacters.",
    ],
    "L1-phrase-only": [
      "The intent phrase cannot itself select a dangerous pre-approved command.",
      "A poisoned 'teach' step cannot install a malicious reflex the runtime trusts.",
      "The lookup table cannot be edited to add an unsafe command post-approval.",
    ],
  },
  // Adversarial pool: concrete bypass-hypotheses; Moth draws which get fired.
  bypass_pool: [
    "A parameterized template ({{param}}) lets a taught command interpolate " +
      "attacker-controlled text straight into the final shell command.",
    "The pre-approved table itself was populated by an LLM 'teach' step, so a " +
      "poisoned teach installs a malicious reflex the runtime then trusts.",
    "argument values (not the command verb) can still carry metacharacters that " +
      "reach the shell when the command is assembled by string interpolation.",
    "a symlink or `..` inside the per-session sandbox dir reaches host paths.",
    "the 5-word intent phrase can itself be crafted to select a dangerous " +
      "pre-approved command (phrase-as-injection).",
    "trust scores auto-promote on 20+ successes, so a slow-drip benign command " +
      "can graduate past the confirmation gate before turning hostile.",
  ],
};

// ── JEV helpers ──────────────────────────────────────────────────────────────
async function jev(state, questions) {
  const r = await fetch(JEV_URL, {
    method: "POST",
    headers: { authorization: `Bearer ${JEV_KEY}`, "content-type": "application/json" },
    body: JSON.stringify({ model: "jev-latest", state, questions }),
  });
  if (!r.ok) throw new Error(`JEV ${r.status}: ${await r.text()}`);
  return (await r.json()).answers;
}
const nq = (question) => ({
  type: "noul",
  question,
  criteria: {
    true: "the guarantee holds as an absolute, sound security property with no plausible bypass",
    false: "the guarantee is an overclaim — there is a plausible bypass or an unstated assumption",
  },
});

// ── Moth helper: the un-gameable draw ────────────────────────────────────────
async function mothDraw(count, min, max) {
  const H = {
    authorization: `Bearer ${MOTH_KEY}`,
    "content-type": "application/json",
    "user-agent": UA,
  };
  const start = await fetch(`${MOTH_BASE}/engines/comet-qrng-v1/process`, {
    method: "POST",
    headers: H,
    body: JSON.stringify({ params: { derive: { integers: { min, max, count } } } }),
  });
  if (!start.ok) throw new Error(`Moth process ${start.status}: ${await start.text()}`);
  const { job_id } = await start.json();
  let status = "queued", tries = 0;
  while (status !== "completed" && status !== "failed" && tries < 30) {
    await new Promise((s) => setTimeout(s, 3000));
    tries++;
    const st = await (await fetch(`${MOTH_BASE}/jobs/${job_id}/status`, { headers: H })).json();
    status = st.status;
  }
  if (status !== "completed") throw new Error(`Moth job ${status}`);
  const res = await (await fetch(`${MOTH_BASE}/jobs/${job_id}/result`, { headers: H })).json();
  const o = res.result?.output || res.output || res;
  return {
    values: o.random?.derived?.integers?.values || [],
    hex: o.random?.hex || "",
    S: o.bell_witness?.S,
    classical_bound: o.bell_witness?.classical_bound,
    z: o.bell_witness?.z_above_classical,
  };
}

// ── visual: the tree of nouls ────────────────────────────────────────────────
function bar(n) {
  const w = Math.round(n * 24);
  const glyph = n < 0.5 ? "█" : "▓"; // dark = likely-false (weak), light = likely-sound
  return glyph.repeat(w).padEnd(24, "·") + ` ${n.toFixed(2)}`;
}
function verdictWord(n) {
  if (n <= 0.2) return "OVERCLAIM";
  if (n < 0.5) return "shaky";
  if (n < 0.8) return "hedged";
  return "sound";
}

async function main() {
  if (!JEV_KEY) throw new Error("TYPESAFEAI_KEY not set");
  console.log("╔═══════════════════════════════════════════════════════════════════╗");
  console.log(`║  SITUATION S17 — The Weakest Leaf   ·   audit target: ${AUDIT_TARGET.tool.padEnd(12)} ║`);
  console.log("╚═══════════════════════════════════════════════════════════════════╝\n");

  // 1) the WHOLE verdict (the shadow) ────────────────────────────────────────
  const whole = (await jev(AUDIT_TARGET.whole, {
    sound: nq("Is this tool's overall security guarantee sound as stated?"),
  })).sound.noul;
  console.log(`WHOLE compound claim → noul = ${whole.toFixed(2)}  (${verdictWord(whole)})`);
  console.log("  the whole says only THAT it is (un)sound, not WHERE.\n");

  // 2) project JEV across the decomposition (the map) ─────────────────────────
  console.log("DECOMPOSED — the tree of nouls (dark bar = the fold's suspicion):\n");
  const leafNouls = [];
  for (const leaf of AUDIT_TARGET.leaves) {
    const ans = await jev(leaf.claim, { sound: nq(`Is this guarantee sound? "${leaf.claim}"`) });
    const n = ans.sound.noul;
    leafNouls.push({ ...leaf, noul: n });
    console.log(`  ${leaf.id.padEnd(16)} ${bar(n)}  ${verdictWord(n)}`);
  }

  // 3) the fold vs the whole — what the entanglement was hiding ───────────────
  const foldMin = Math.min(...leafNouls.map((l) => l.noul));
  const foldProd = leafNouls.reduce((p, l) => p * l.noul, 1);
  const weakest = leafNouls.reduce((a, b) => (b.noul < a.noul ? b : a));
  console.log(`\n  FOLD(min)     = ${foldMin.toFixed(2)}`);
  console.log(`  FOLD(product) = ${foldProd.toFixed(3)}`);
  console.log(`  WHOLE         = ${whole.toFixed(2)}`);
  console.log(`  divergence (whole − fold_min) = ${(whole - foldMin).toFixed(2)}` +
    "   ← how much the compound claim was hiding");
  console.log(`\n  ▶ LOCATED weakest leaf: ${weakest.id}  (noul ${weakest.noul.toFixed(2)})`);
  console.log(`    "${weakest.claim}"\n`);

  // 3b) increasingly decompose the located leaf — the tree deepens ────────────
  let atom = null;
  const subs = AUDIT_TARGET.subleaves?.[weakest.id];
  if (subs?.length) {
    console.log(`  └─ decomposing ${weakest.id} again (the logic gets visual as it splits):`);
    const subNouls = [];
    for (const claim of subs) {
      const n = (await jev(claim, { sound: nq(`Is this guarantee sound? "${claim}"`) })).sound.noul;
      subNouls.push({ claim, noul: n });
      console.log(`       ├─ ${bar(n)}  ${claim.slice(0, 50)}`);
    }
    atom = subNouls.reduce((a, b) => (b.noul < a.noul ? b : a));
    console.log(`     ▶ rot localized to the atom (noul ${atom.noul.toFixed(2)}): "${atom.claim}"\n`);
  }

  // 4) Moth draws the un-gameable adversary against the located leaf ──────────
  let draw = null;
  if (USE_MOTH && MOTH_KEY && MOTH_BASE) {
    console.log("Rolling the un-gameable dice (Moth comet-qrng-v1, quantum) ...");
    try {
      draw = await mothDraw(3, 0, AUDIT_TARGET.bypass_pool.length - 1);
      console.log(`  Bell witness S = ${draw.S?.toFixed(3)} > classical ${draw.classical_bound}` +
        `  (z=${draw.z?.toFixed(1)}σ)  — provenance is physics, not a re-roll.`);
      console.log(`  quantum seed: ${draw.hex.slice(0, 24)}…`);
      const picks = [...new Set(draw.values)].slice(0, 3);
      console.log(`  drawn bypass indices: [${picks.join(", ")}]  (nobody steered these)\n`);

      // JEV adjudicates each drawn bypass as a `choice`: does it defeat the leaf?
      console.log("ADVERSARY — JEV adjudicates each quantum-drawn bypass vs the weakest leaf:\n");
      let defeated = 0;
      for (const idx of picks) {
        const bypass = AUDIT_TARGET.bypass_pool[idx];
        const ans = await jev(
          `GUARANTEE: ${weakest.claim}\nPROPOSED BYPASS: ${bypass}`,
          { verdict: {
              type: "choice",
              question: "Does the proposed bypass credibly defeat the guarantee?",
              criteria: {
                defeats: "the bypass is a credible, realistic way to violate the guarantee",
                holds: "the guarantee still holds; the bypass does not credibly defeat it",
              },
          } }
        );
        const v = ans.verdict;
        const hit = v.choice === "defeats";
        if (hit) defeated++;
        console.log(`  bypass#${idx}: ${v.choice.toUpperCase().padEnd(8)} ` +
          `(conf ${(v.confidence ?? 0).toFixed(2)})  ${bypass.slice(0, 62)}…`);
      }
      console.log(`\n  ${defeated}/${picks.length} quantum-drawn adversaries DEFEAT the located leaf.`);
      draw.defeated = defeated;
      draw.tested = picks.length;
    } catch (e) {
      console.log(`  (Moth skipped: ${e.message})`);
      draw = null;
    }
  } else {
    console.log("(Moth draw skipped — JEV-only run.)");
  }

  // 5) DONE / answer signal ───────────────────────────────────────────────────
  console.log("\n─────────────────────────── ANSWER ───────────────────────────");
  console.log(`Tool "${AUDIT_TARGET.tool}"'s weakest advertised guarantee is:`);
  console.log(`   → ${weakest.id}  (noul ${weakest.noul.toFixed(2)}, ${verdictWord(weakest.noul)})`);
  if (atom) console.log(`   → precise atom: "${atom.claim}" (noul ${atom.noul.toFixed(2)})`);
  console.log(`   → fix-or-soften this claim next.`);
  if (draw?.tested) {
    const survived = draw.defeated === 0;
    console.log(`Un-gameable adversary: ${draw.defeated}/${draw.tested} quantum-drawn bypasses ` +
      `land → the weakness is ${survived ? "NOT confirmed (leaf held)" : "CONFIRMED real"}.`);
    console.log(`Provenance: Bell S=${draw.S?.toFixed(3)} (>2), seed ${draw.hex.slice(0, 16)}… — ` +
      `this audit could not be re-rolled until it flattered the tool.`);
  }
  console.log("───────────────────────────────────────────────────────────────");
}

main().catch((e) => { console.error("PLAY FAILED:", e.message); process.exit(1); });
