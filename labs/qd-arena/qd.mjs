// qd-arena — a zero-dep MAP-Elites quality-diversity loop over several live generator models.
// Generators propose; JEV (the referee) scores quality AND places each candidate on two diversity
// axes; the archive keeps the BEST PER NICHE, not the global best. A Moth quantum draw picks which
// niches each generator is sent to push on next, so exploration is not steered by us or the models.
import { writeFileSync, readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { jev, mothDraw } from "../weakest-claim/audit.mjs";

const FIXTURE_PATH = fileURLToPath(new URL("./fixtures.json", import.meta.url));

export const TASK =
  "Name and give a one-line pitch for a small tool a fishing fleet of AI agents would want. " +
  "(The 'fleet' is a crew of cheap worker agents run by a manager agent: they go out, harvest ideas or " +
  "code in bulk, and bring back a catch that a referee grades.)";

// Model roster: every endpoint probed in step 0. `live` is what the probe found (2026-09-29).
export const ROSTER = [
  { id: "deepseek-chat", url: "https://api.deepseek.com/chat/completions", key: "DEEPSEEK_KEY", live: true },
  { id: "meta-llama/Meta-Llama-3.1-8B-Instruct", url: DI(), key: "DEEPINFRA_KEY", live: true },
  { id: "XiaomiMiMo/MiMo-V2.6-Flash", url: DI(), key: "DEEPINFRA_KEY", live: true },
  { id: "nvidia/NVIDIA-Nemotron-3.5-Lightning", url: DI(), key: "DEEPINFRA_KEY", live: true },
  { id: "ByteDance/Seed-2.0-mini", url: DI(), key: "DEEPINFRA_KEY", live: true },
  { id: "tencent/Hy3", url: DI(), key: "DEEPINFRA_KEY", live: true },
  { id: "glm-5.3-flash", url: "https://api.z.ai/api/paas/v4/chat/completions", key: "ZAI_KEY", live: false, note: "429 code 1113: insufficient balance" },
];
function DI() { return "https://api.deepinfra.com/v1/openai/chat/completions"; }

// Two diversity axes, three bins each → a 3×3 MAP-Elites grid. JEV `choice` places candidates.
export const AXES = {
  grain: {
    question: "How concrete or abstract is this tool idea?",
    bins: ["concrete", "middle", "abstract"],
    criteria: {
      concrete: "a specific mechanism you could build this week: named inputs, outputs, a file or command",
      middle: "a clear function but described at the level of a feature, not an implementation",
      abstract: "a principle, stance, or way of seeing; hard to point at a single mechanism",
    },
  },
  form: {
    question: "Is this idea more a tool, a practice, or a ritual?",
    bins: ["tool", "practice", "ritual"],
    criteria: {
      tool: "an instrument the agents operate: software, a device, a data structure",
      practice: "a repeated working procedure or protocol the crew follows",
      ritual: "a symbolic or ceremonial act that shapes the crew's culture, attention, or meaning",
    },
  },
};
export const CELLS = AXES.grain.bins.flatMap((g) => AXES.form.bins.map((f) => `${g}/${f}`));

// Quality is an ordinal JEV score over a 4-rung ladder → expected rung in [0, 3].
export const QUALITY = {
  type: "score",
  question: "How good is this as a small tool idea for a fishing fleet of AI agents (manager + cheap workers + referee)?",
  criteria: [
    "generic or useless: could be pitched for any team",
    "plausible but vague: the fleet benefit is unclear",
    "specific and useful: clearly fits how an agent fleet works",
    "specific, useful and surprising: a fleet would adopt it and few would think of it",
  ],
};

export const evalState = (c) => `CANDIDATE TOOL IDEA: ${c.name} — ${c.pitch}`;
export function evalQuestions() {
  const q = { quality: QUALITY };
  for (const [k, a] of Object.entries(AXES)) q[k] = { type: "choice", question: a.question, criteria: a.criteria };
  return q;
}

// Generation prompt. With a target niche, the generator is told where to aim and shown the elite to beat.
export function genPrompt(n, target, elite) {
  const lines = [TASK, "", `Give ${n} different ideas. One per line, exactly: NAME :: one-line pitch`, "No numbering, no preamble."];
  if (target) {
    const [g, f] = target.split("/");
    lines.push("", `Aim every idea at this niche — grain: ${g} (${AXES.grain.criteria[g]}); form: ${f} (${AXES.form.criteria[f]}).`);
    if (elite) lines.push(`The current best in this niche is "${elite.name} :: ${elite.pitch}". Beat it without leaving the niche.`);
  }
  return lines.join("\n");
}

export function parseCandidates(text, model) {
  const out = [];
  for (const raw of (text ?? "").split("\n")) {
    const line = raw.replace(/^\s*(?:[-*•]|\d+[.)])\s*/, "").replace(/\*\*/g, "").trim();
    const m = line.match(/^(.{2,60}?)\s*(?:::|—|–|:| - )\s*(.{12,})$/);
    if (m) out.push({ name: m[1].trim(), pitch: m[2].trim(), model });
  }
  return out;
}

export async function chat(entry, prompt, env = process.env) {
  const key = env[entry.key];
  if (!key) throw new Error(`${entry.key} not set`);
  const r = await fetch(entry.url, {
    method: "POST",
    headers: { authorization: `Bearer ${key}`, "content-type": "application/json" },
    body: JSON.stringify({ model: entry.id, messages: [{ role: "user", content: prompt }], max_tokens: 1500, temperature: 0.9 }),
  });
  if (!r.ok) throw new Error(`${entry.id} ${r.status}`);
  return (await r.json()).choices?.[0]?.message?.content ?? "";
}

// Place a judged candidate: argmax bin per axis; quality = expected rung.
export function place(c, a) {
  return { ...c, quality: a.quality.score, cell: `${a.grain.choice}/${a.form.choice}` };
}

// MAP-Elites insert: a candidate only competes with the incumbent of ITS niche.
export function insert(archive, c) {
  const inc = archive[c.cell];
  if (!inc || c.quality > inc.quality) { archive[c.cell] = c; return inc ? "improved" : "new"; }
  return "rejected";
}

// Moth draw values → a target niche per generator (the loop cannot choose which).
export const targetsFrom = (values, n) => Array.from({ length: n }, (_, i) => CELLS[values[i % values.length] % CELLS.length]);

// The loop. sources = { generate(entry, prompt) → text, judge(state) → answers, draw(count, max) → {values,...} }
export async function run({ generators, sources, gens = 3, perCall = 3, log = () => {} }) {
  const archive = {};
  const history = [];
  const all = [];
  for (let g = 0; g < gens; g++) {
    let targets = generators.map(() => null), draw = null;
    if (g > 0) {
      draw = await sources.draw(generators.length, CELLS.length - 1);
      targets = targetsFrom(draw.values, generators.length);
    }
    const texts = await Promise.all(
      generators.map((e, i) =>
        sources.generate(e, genPrompt(perCall, targets[i], targets[i] && archive[targets[i]])).catch((err) => ({ err: err.message })),
      ),
    );
    const batch = [];
    texts.forEach((t, i) => {
      if (t?.err) return log(`  gen${g} ${generators[i].id}: ERROR ${t.err}`);
      const cs = parseCandidates(t, generators[i].id).slice(0, perCall).map((c) => ({ ...c, gen: g, aimed: targets[i] }));
      if (!cs.length) log(`  gen${g} ${generators[i].id}: no parseable candidates`);
      batch.push(...cs);
    });
    const judged = await Promise.all(batch.map(async (c) => place(c, await sources.judge(evalState(c)))));
    const counts = { new: 0, improved: 0, rejected: 0 };
    for (const c of judged) { c.outcome = insert(archive, c); counts[c.outcome]++; all.push(c); }
    history.push({ gen: g, draw: draw && { values: draw.values, S: draw.S, mode: draw.mode }, targets, candidates: judged.length, ...counts, filled: Object.keys(archive).length });
    log(`gen ${g}: ${judged.length} candidates → ${counts.new} new niches, ${counts.improved} improved, ${counts.rejected} rejected; archive ${Object.keys(archive).length}/${CELLS.length}`);
  }
  return { archive, history, all };
}

// What a single best-of would have returned, and how the unsteered first generation clumped.
export function contrast({ all, archive }) {
  const best = all.reduce((a, b) => (b.quality > a.quality ? b : a));
  const gen0 = {};
  for (const c of all.filter((c) => c.gen === 0)) gen0[c.cell] = (gen0[c.cell] ?? 0) + 1;
  const qs = Object.values(archive).map((c) => c.quality);
  return { best, gen0, elites: qs.length, meanElite: qs.reduce((s, q) => s + q, 0) / (qs.length || 1) };
}

export function render(result) {
  const { archive, history } = result;
  const k = contrast(result);
  const f = (q) => q.toFixed(2);
  const L = ["ARCHIVE (MAP-Elites: best per niche; quality = JEV expected rung 0–3)", ""];
  for (const cell of CELLS) {
    const c = archive[cell];
    L.push(c ? `  ${cell.padEnd(17)} ${f(c.quality)}  ${c.name} :: ${c.pitch}\n  ${"".padEnd(17)}       ↳ ${c.model} (gen ${c.gen}${c.aimed ? `, aimed ${c.aimed}` : ""})` : `  ${cell.padEnd(17)}  —    (empty)`);
  }
  L.push("", "GENERATIONS");
  for (const h of history) {
    const d = h.draw ? `  Moth draw [${h.draw.values.join(",")}] S=${h.draw.S?.toFixed(3) ?? "?"} (${h.draw.mode ?? "?"})` : "  (unsteered: no target niche)";
    L.push(`  gen ${h.gen}: ${h.candidates} cands → +${h.new} new, ${h.improved} improved, ${h.rejected} rejected → ${h.filled}/${CELLS.length} niches${d}`);
  }
  L.push("", "CONTRAST", `  single best-of would return ONE idea: ${k.best.name} (${f(k.best.quality)}, ${k.best.cell}, ${k.best.model})`);
  L.push(`  unsteered gen-0 placement: ${Object.entries(k.gen0).sort((a, b) => b[1] - a[1]).map(([c, n]) => `${c}×${n}`).join(", ")}`);
  L.push(`  QD archive: ${k.elites} distinct elites, mean quality ${f(k.meanElite)}`);
  return L.join("\n");
}

// Offline: replay a recorded live run exactly (generator text keyed by model+prompt, JEV by state).
export function fixtureSources(path = FIXTURE_PATH) {
  const fx = JSON.parse(readFileSync(path, "utf8"));
  let d = 0;
  const need = (tbl, k, what) => { if (!(k in tbl)) throw new Error(`no fixture ${what} for: ${k.slice(0, 80)}`); return tbl[k]; };
  return {
    fx,
    generate: async (e, p) => { const t = need(fx.generations, `${e.id}\n${p}`, "generation"); if (t?.err) throw new Error(t.err); return t; },
    judge: async (s) => need(fx.judgments, s, "judgment"),
    draw: async () => fx.draws[d++],
  };
}

export function recordingSources() {
  const rec = { generations: {}, judgments: {}, draws: [] };
  return {
    rec,
    generate: async (e, p) => {
      try { return (rec.generations[`${e.id}\n${p}`] = await chat(e, p)); }
      catch (err) { rec.generations[`${e.id}\n${p}`] = { err: err.message }; throw err; }
    },
    judge: async (s) => (rec.judgments[s] = await jev(s, evalQuestions())),
    draw: async (n, max) => { const d = await mothDraw(n, max); rec.draws.push(d); return d; },
  };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const keyed = ["TYPESAFEAI_KEY", "MOTHQUANTUM_KEY", "MOTHQUANTUM_BASE"].every((k) => process.env[k]);
  const offline = args.includes("--offline") || !keyed;
  const generators = ROSTER.filter((e) => e.live && (offline || process.env[e.key]));
  const src = offline ? fixtureSources() : recordingSources();
  const result = await run({ generators, sources: src, log: (s) => console.error(s) });
  console.log(`[source: ${offline ? "fixture" : "live"}; generators: ${generators.map((e) => e.id).join(", ")}]\n${render(result)}`);
  if (!offline && args.includes("--record")) {
    writeFileSync(FIXTURE_PATH, JSON.stringify({ recorded: `${new Date().toISOString()}, live generators + JEV + Moth comet-qrng-v1`, ...src.rec }, null, 2) + "\n");
    console.error(`recorded → ${FIXTURE_PATH}`);
  }
}
