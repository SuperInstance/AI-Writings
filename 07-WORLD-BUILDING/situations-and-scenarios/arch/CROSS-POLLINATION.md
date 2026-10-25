# Cross-Pollination — the Reader's Fold, made machine-readable

**Status:** buildable standard, v1. Dependency-free, drop-in, one uniform mechanism for 100+ repos.
**Grounded in:** jev-quilt Law 6 (the Reader's Fold — *a verdict is never carried, only content-addressed evidence each reader folds under its own weights*) and Law 7 (the Reach Bound).

---

## 0. The problem, as actually found

I inspected the live fleet (all public, cloned 2026-09-27). Cross-pollination **already exists — but only as prose**:

- `jev-quilt/README.md` — "Sibling of the quilt polyformalism … Cousin of TypeSafe's Jev …"
- `cargo-line-tycoon/README.md` — a hand-written **"In the broader fleet"** list of 17 `substrate-*` repos.
- `crab-traps/README.md`, `tessera/README.md` — "the renderer core … is `SuperInstance/chiaroscuro` … Tessera inherits it."

There is **no `.quilt/` directory, no `links.yml`, no machine-readable edge anywhere** in the fleet. Every one of those prose links is hand-maintained, one-directional, and invisible to any tool. That is exactly the "100 islands" failure: the connective tissue exists in a human's head and rots the moment a repo is renamed.

The fix is not to invent cross-linking — the fleet already wants it — but to give the existing instinct **one tiny declarative home** and generate the prose from it.

---

## 1. The mechanism (decision)

**One file per repo — `.quilt/links.yml` — as the single source of truth, plus a generated, marker-delimited README section, plus a zero-dependency `quilt-links.mjs` that renders both the per-repo section and the whole-fleet graph.**

```
repo/
├── .quilt/
│   └── links.yml          # SOURCE OF TRUTH — hand-edited, ~15 lines
├── README.md              # contains a generated block between two markers
└── (quilt-links.mjs lives once, in fleet-seeds/ — copied or curl'd, not vendored per-repo)
```

### Why this shape (vs the alternatives) — Law 6 justification

- **`.quilt/links.yml` (chosen)** — a manifest *is* content-addressed evidence: it declares pointers, never claims. A reader (the graph tool, a human, another repo's CI) folds those pointers under its own weights — precisely Law 6. One well-known path means a tool can `curl` it across 100 repos with zero per-repo config.
- **Fenced ` ```quilt-links ` block in the README (rejected as source of truth)** — tempting because it self-renders on GitHub, but it couples the machine record to prose editing: every regen has to surgically re-find the fence, and a human reflowing the README breaks the parser. We keep the *rendered* output in the README (below) but never the *source*.
- **A central `fleet/registry.json` (rejected)** — one file 100 repos must all commit to is a merge-conflict funnel and a single point of rot; it violates the fold (one repo would carry verdicts *about* the others). Edges must live *at the folding repo*, discovered outward.
- **A GitHub-topics-only scheme (rejected)** — topics can't express `provides` vs `consumes` vs `substrate`, carry no `why`, and aren't diffable in a PR.

Net: the manifest is the **only** new artifact a repo must own, it is ~15 lines, and a repo that never adds one still participates (see §4, degrade).

---

## 2. The schema (paste-ready)

`.quilt/links.yml` — every field except `repo` is optional. This is the complete, restricted grammar (a flat map of lists of flat maps — see §5 for the ~50-line parser that needs no YAML dependency).

```yaml
# .quilt/links.yml — the Reader's Fold manifest (jev-quilt Law 6).
# This repo carries NO verdicts about its neighbors — only content-addressed
# pointers each reader folds under its own weights. Edit this file; never edit
# the generated block in README.md by hand.

repo: cargo-line-tycoon          # REQUIRED. Must equal the GitHub repo name.
family: quilt                    # Optional, default "quilt". The fold this belongs to.

substrate:                       # What this repo is GROWN ON (the upstream spine).
  - repo: jev-quilt              #   Solid edge in the graph. 0..n entries.
    at: v0.3                     #   Optional content-address: tag / commit / mmr_root (Law 6).

provides:                        # What OTHER repos may fold FROM here. 0..n.
  - id: opcode-canon             #   A stable handle a consumer names in its `consumes`.
    what: the 11-opcode substrate algebra, FNV-1a canary-pinned 0x024a555471370b18d
  - id: memory-sandbox
    what: 6-pattern x 5-authority defensive envelope (defends Leong 2605.08442)

consumes:                        # What THIS repo folds FROM elsewhere. 0..n. Dashed edge.
  - repo: jev-quilt
    what: cell / hook / bookkeeper doctrine + q16 exact-rational codec
    at: v0.3                     #   Optional. Pin the evidence you actually folded.

related:                         # Sideways siblings — 1 HOP ONLY (Law 7, the Reach Bound).
  - repo: qthe                   #   Dotted edge. Never transitive: you declare direct
    why: shares the data-is-geometry framing               #   neighbors, never their neighbors.
  - repo: pong-quilt
    why: sibling "ML you can watch think" teaching artifact

upstream:                        # FORKS ONLY — the folded-in origin (may be outside the org).
  repo: karpathy/micrograd       #   owner/name form allowed for external upstreams.
  why: kept byte-for-byte; the quilt/ layer asks where floats lie
```

### Field semantics

| Field | Meaning | Edge in graph | Reach (Law 7) |
|---|---|---|---|
| `substrate` | grown on this spine | **solid** → substrate | 1 hop |
| `consumes` | folds this repo's evidence | **dashed** → source | 1 hop |
| `provides` | offers these handles outward | (inbound, drawn from consumers) | — |
| `related` | sideways sibling | **dotted** — | **1 hop, never transitive** |
| `upstream` | fork origin | **double** → upstream (external ok) | 1 hop |

**Law 7 in one rule:** a manifest may only name **direct** neighbors. The graph tool never expands `related`-of-`related`. Reach is bounded at the declaration site, so 100 repos yield a sparse, readable graph instead of a 100-clique.

**Law 6 in one rule:** `consumes[].at` and `substrate[].at` are the *content-address of the evidence you actually folded* (a tag, a commit, or a `fold.mmr_root`). A repo pins what it folded; it does not re-assert the upstream's claims. If the upstream changes, your pin still names the evidence you read.

---

## 3. The rendered README section

`quilt-links.mjs` (no args, run inside a repo) reads `.quilt/links.yml` and rewrites the block between two HTML-comment markers in `README.md`. If the markers are absent it inserts the block immediately before the first `## License`/`## License`-like heading, else at EOF.

```markdown
<!-- QUILT:LINKS:START — generated from .quilt/links.yml by quilt-links.mjs. Do not edit by hand. -->
## Cross-pollination — the Reader's Fold

*Part of the **quilt** family. Under [Law 6](https://github.com/SuperInstance/jev-quilt),
this repo carries no verdicts about its neighbors — only content-addressed pointers you
fold under your own weights.*

**Grown on** — [jev-quilt](https://github.com/SuperInstance/jev-quilt) `@v0.3`

**Provides** (fold these from here)
- `opcode-canon` — the 11-opcode substrate algebra, FNV-1a canary-pinned `0x024a555471370b18d`
- `memory-sandbox` — 6-pattern × 5-authority defensive envelope (defends Leong 2605.08442)

**Consumes** (folded from elsewhere)
- [jev-quilt](https://github.com/SuperInstance/jev-quilt) `@v0.3` — cell / hook / bookkeeper doctrine + q16 exact-rational codec

**Related** (1-hop siblings — Law 7)
- [qthe](https://github.com/SuperInstance/qthe) — shares the data-is-geometry framing
- [pong-quilt](https://github.com/SuperInstance/pong-quilt) — sibling "ML you can watch think" teaching artifact

<sub>Regenerate: `node quilt-links.mjs` · Fleet map: [FLEET.md](https://github.com/SuperInstance/fleet-seeds/blob/main/FLEET.md)</sub>
<!-- QUILT:LINKS:END -->
```

Forks additionally render a leading **Folded from** line linking `upstream.repo`. The block is pure Markdown/HTML-comment — it renders on GitHub with no JS, and re-running the generator is idempotent (byte-stable between the markers).

---

## 4. How a repo without a manifest degrades

The mechanism is **fail-open by construction** — it never breaks an island, it just can't hear one.

1. **No `.quilt/links.yml`** → the per-repo generator is a no-op (prints `no manifest, nothing to render` and exits 0). The README is left exactly as-is. The repo is a valid island.
2. **In the fleet graph**, a manifest-less repo still appears **if any other repo names it** in `substrate`/`consumes`/`related`/`upstream` — it is drawn as a leaf node with inbound edges only. So the *neighbor* adopting the standard is enough to pull an island onto the map; the island itself need not act.
3. **Malformed / partial manifest** → the parser is lenient: unknown keys are ignored, a missing optional list is treated as empty, only a missing `repo:` is fatal (and it fails loudly, changing nothing). A repo can adopt one field (`substrate:` alone) and grow the rest later.
4. **Markers present but manifest deleted** → generator leaves the last-rendered block untouched (no manifest = nothing to say), so a stale block is never silently blanked.

This is the confluent-merge property from `jev_quilt/commons.py` applied to docs: edges glue in any order (`A∪B == B∪A`), an unseen source contributes nothing, and adoption can be one repo at a time with no coordination.

---

## 5. The generator (zero-dependency, copy-pasteable)

One file. Node ≥18, no `npm install`, no YAML library — a ~50-line parser for exactly the restricted grammar in §2. Lives once in `fleet-seeds/quilt-links.mjs`; repos `curl` it in CI rather than vendoring 100 copies.

```javascript
#!/usr/bin/env node
// quilt-links.mjs — render the Reader's Fold. Zero dependencies. Node >=18.
//   node quilt-links.mjs                 # rewrite this repo's README block from .quilt/links.yml
//   node quilt-links.mjs --graph ./fleet # scan a dir of clones -> FLEET.md + graph.mmd
import { readFileSync, writeFileSync, existsSync, readdirSync } from "node:fs";
import { join } from "node:path";

const ORG = "https://github.com/SuperInstance";
const url = r => r.includes("/") ? `https://github.com/${r}` : `${ORG}/${r}`;

// --- tiny YAML subset parser: flat map -> (scalar | nested map | list of flat maps | list of scalars) ---
// list-vs-map is decided lazily by the first child, so `upstream:` (a map) and `substrate:` (a list) both parse.
function parseLinks(text) {
  const out = {}; let key = null, item = null;
  for (let raw of text.split(/\r?\n/)) {
    const line = raw.replace(/\s+#.*$/, "").replace(/^#.*$/, "");
    if (!line.trim()) continue;
    const top = line.match(/^(\w+):\s*(.*)$/);          // `key:` or `key: value` (column 0)
    if (top) { key = top[1]; const v = top[2].trim(); item = null; out[key] = v || undefined; continue; }
    const li = line.match(/^\s*-\s*(\w+):\s*(.*)$/);     // `- k: v` — first field of a list item
    if (li && key) { if (!Array.isArray(out[key])) out[key] = []; item = { [li[1]]: li[2].trim() }; out[key].push(item); continue; }
    const scalar = line.match(/^\s*-\s*(.+)$/);          // `- value` — scalar list item
    if (scalar && key) { if (!Array.isArray(out[key])) out[key] = []; out[key].push(scalar[1].trim()); item = null; continue; }
    const kv = line.match(/^\s+(\w+):\s*(.*)$/);         // `  k: v` — later list-item field OR map field
    if (kv && key) {
      if (item) item[kv[1]] = kv[2].trim();             // later field of the current list item
      else { if (typeof out[key] !== "object" || out[key] === null || Array.isArray(out[key])) out[key] = {}; out[key][kv[1]] = kv[2].trim(); }
      continue;
    }
  }
  return out;   // lenient: unknown keys pass through, missing lists/maps are absent
}

function render(m) {
  const L = [];
  L.push(`## Cross-pollination — the Reader's Fold\n`);
  L.push(`*Part of the **${m.family || "quilt"}** family. Under [Law 6](${ORG}/jev-quilt), this repo carries no verdicts about its neighbors — only content-addressed pointers you fold under your own weights.*\n`);
  if (m.upstream?.repo) L.push(`**Folded from** — [${m.upstream.repo}](${url(m.upstream.repo)})${m.upstream.why ? ` — ${m.upstream.why}` : ""}\n`);
  const subs = (m.substrate || []).map(s => `[${s.repo}](${url(s.repo)})${s.at ? ` \`@${s.at}\`` : ""}`);
  if (subs.length) L.push(`**Grown on** — ${subs.join(", ")}\n`);
  if ((m.provides || []).length) L.push(`**Provides** (fold these from here)\n` + m.provides.map(p => `- \`${p.id}\` — ${p.what || ""}`).join("\n") + "\n");
  if ((m.consumes || []).length) L.push(`**Consumes** (folded from elsewhere)\n` + m.consumes.map(c => `- [${c.repo}](${url(c.repo)})${c.at ? ` \`@${c.at}\`` : ""} — ${c.what || ""}`).join("\n") + "\n");
  if ((m.related || []).length) L.push(`**Related** (1-hop siblings — Law 7)\n` + m.related.map(r => `- [${r.repo}](${url(r.repo)}) — ${r.why || ""}`).join("\n") + "\n");
  L.push(`<sub>Regenerate: \`node quilt-links.mjs\` · Fleet map: [FLEET.md](${ORG}/fleet-seeds/blob/main/FLEET.md)</sub>`);
  return L.join("\n");
}

const START = "<!-- QUILT:LINKS:START — generated from .quilt/links.yml by quilt-links.mjs. Do not edit by hand. -->";
const END = "<!-- QUILT:LINKS:END -->";

function writeBlock() {
  if (!existsSync(".quilt/links.yml")) { console.log("no manifest, nothing to render"); return; }
  const m = parseLinks(readFileSync(".quilt/links.yml", "utf8"));
  if (!m.repo) { console.error("FATAL: .quilt/links.yml has no `repo:` — nothing changed"); process.exit(1); }
  const block = `${START}\n${render(m)}\n${END}`;
  let md = existsSync("README.md") ? readFileSync("README.md", "utf8") : "# " + m.repo + "\n";
  const re = new RegExp(`${START}[\\s\\S]*?${END}`);
  if (re.test(md)) md = md.replace(re, block);
  else if (/^## License/m.test(md)) md = md.replace(/^## License/m, block + "\n\n## License");
  else md = md.replace(/\s*$/, "\n\n") + block + "\n";
  writeFileSync("README.md", md);
  console.log(`rendered ${((m.substrate||[]).length + (m.consumes||[]).length + (m.related||[]).length)} edges into README.md`);
}

function graph(dir) {
  const nodes = new Set(), edges = [];
  for (const d of readdirSync(dir, { withFileTypes: true }).filter(e => e.isDirectory())) {
    const p = join(dir, d.name, ".quilt/links.yml");
    if (!existsSync(p)) { nodes.add(d.name); continue; }   // island: node only
    const m = parseLinks(readFileSync(p, "utf8")); const self = m.repo || d.name; nodes.add(self);
    for (const s of m.substrate || []) { nodes.add(s.repo); edges.push([self, s.repo, "==>", "grown on"]); }
    for (const c of m.consumes || []) { nodes.add(c.repo); edges.push([self, c.repo, "-.->", "consumes"]); }
    for (const r of m.related || []) { nodes.add(r.repo); edges.push([self, r.repo, "---", "related"]); }
    if (m.upstream?.repo) { nodes.add(m.upstream.repo); edges.push([self, m.upstream.repo, "===>", "fork of"]); }
  }
  const id = s => s.replace(/[^\w]/g, "_");
  const mmd = ["graph LR", ...[...nodes].map(n => `  ${id(n)}["${n}"]`),
    ...edges.map(([a, b, e, l]) => `  ${id(a)} ${e}|${l}| ${id(b)}`)].join("\n");
  writeFileSync("graph.mmd", mmd);
  const rows = edges.map(([a, b, , l]) => `| ${a} | ${l} | ${b} |`).join("\n");
  writeFileSync("FLEET.md", `# Fleet map — the quilt fold\n\n${nodes.size} repos, ${edges.length} edges. Regenerated by \`quilt-links.mjs --graph\`.\n\n\`\`\`mermaid\n${mmd}\n\`\`\`\n\n| from | edge | to |\n|---|---|---|\n${rows}\n`);
  console.log(`graph: ${nodes.size} nodes, ${edges.length} edges -> FLEET.md, graph.mmd`);
}

const gi = process.argv.indexOf("--graph");
if (gi >= 0) graph(process.argv[gi + 1] || ".");
else writeBlock();
```

### CI wiring (one job, drop into `.github/workflows/quilt-links.yml`)

```yaml
name: quilt-links
on: { push: { paths: [".quilt/links.yml"] } }
permissions: { contents: write }
jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: curl -sSfL https://raw.githubusercontent.com/SuperInstance/fleet-seeds/main/quilt-links.mjs -o quilt-links.mjs
      - run: node quilt-links.mjs
      - run: |
          git config user.name "quilt-links[bot]"; git config user.email "noreply@superinstance"
          git diff --quiet README.md || (git add README.md && git commit -m "chore: regenerate cross-pollination block" && git push)
```

The fleet-graph is a scheduled job in `fleet-seeds` only: it clones the org, runs `--graph`, commits `FLEET.md`. No per-repo cost.

---

## 6. Roll-out (minimal, one uniform path)

1. Land `quilt-links.mjs` + `FLEET.md` (empty seed) + the graph workflow in **`fleet-seeds`** (it is already the fleet's intake lane — the natural home).
2. Add the `paths:`-scoped `quilt-links.yml` workflow to each repo (identical file, no per-repo edits).
3. Fan-out agents each write ONE `.quilt/links.yml` per repo (§2) and let CI render the block. Start with the repos that already have prose links (cargo-line-tycoon, jev-quilt, crab-traps, tessera→chiaroscuro) — their manifests transcribe existing sentences into edges, so the first graph is non-trivial on day one.
4. `fleet-seeds/seedbox.mjs` gets one line: every newly spawned repo is born with a `.quilt/links.yml` stub (`repo:` + `substrate: [jev-quilt]`), so new repos are never islands.

Total new surface per repo: **one 15-line YAML file** and **one 12-line workflow**. Everything else is generated.
