# The Web is the Dock: A Cloudflare-First Quilt Ecosystem

**A Polyformalism Canon Entry**

> *The substrate is the boat. The web is the dock. The cowboy
> rides the boat to the dock. The dock is where people come
> aboard. The voyage is the 5 opcodes. The map is the
> collection. The chart is the boundaries. The cowboy rides.*

## The principle

The Quilt collection has 24 repos and 200+ pieces of canon.
The substrate is the boat. The cowboy rides the boat. But
a boat without a dock is just a thing in the water. The
web is the dock — the place where people come aboard, where
the work is shared, where the substrate meets the public.

The cowboy's maxim extends:

> The substrate is the boat. The web is the dock. The cowboy
> rides the boat to the dock. The dock is where people come
> aboard. The voyage is the 5 opcodes. The map is the
> collection. The chart is the boundaries. The cowboy rides.

## The 13 pages

The new `quilt-ecosystem-web` repo holds 13 web pages, each a
door into the same idea. The pages are organized by what the
visitor came for:

- **The curious visitor** lands on `/` and reads the
  principle. Eight cards point to the next door.
- **The learner** goes to `/academy/` and walks through 7
  lessons, one per opcode, with running examples and a save
  button at the bottom of every page.
- **The experimenter** goes to `/repl/` and types polyformalism
  code in the browser. The journal updates in real time. A
  time-travel slider scrubs through the history. The prover
  verifies the 5 laws.
- **The visual thinker** goes to `/playground/` and drags
  cells around, drawing LINK arrows between them. The
  substrate is the SVG canvas.
- **The builder** goes to `/apps/` and uses the 5 worked
  applications: kv, bus, config, sixth, plugins. Each is a
  working tool that runs in the browser, saves to
  localStorage, and exports to saddle-bridge JSONL.
- **The architect** goes to `/boundaries/` and reads the 15
  laminar boundaries, each with a bridge to an existing
  Quilt repo or a roadmap item. The chart is the cowboy's
  navigation chart.
- **The polyglot** goes to `/vms/` and compares the 5
  language ports side by side. C, Rust, TypeScript, Haskell,
  WASM. The same 5 opcodes, the same algebra, the local
  syntax.
- **The researcher** goes to `/canon/` and searches the 200+
  pieces of canon by meaning, not just keywords. The index
  is the bge-base embedding model running on Workers AI.
- **The deployer** goes to `/self-host/` and picks a path:
  local Python (5 min), Cloudflare Worker (15 min), or
  full stack (1 day).

## The Cloudflare architecture

The web ecosystem uses every Cloudflare primitive:

**Pages** hosts the static site. The Pages project is
`quilt`, deployed to `quilt.superinstance.dev`. Static
files are served from the edge.

**Workers** are the dynamic layer. There are two:
- `quilt-state-worker` handles save/load. POST
  `/api/state` with a journal JSONL, get a shareable ID
  back. GET `/api/state/:id` retrieves it. The state lives
  in KV with a 30-day TTL. The rate limit is 100 saves per
  IP per day (in-memory; replace with a real limit for
  production).
- `quilt-search-worker` handles semantic canon search. POST
  `/api/search` with a query, get the top 20 chunks
  ranked by cosine similarity. The embeddings come from
  `@cf/baai/bge-base-en-v1.5` on Workers AI (free,
  multilingual). The vectors live in Vectorize.

**KV** is the persistence layer. The `STATE` namespace
holds playground saves. The 30-day TTL is enough for
most users; for permanent saves, the user can export to
saddle-bridge JSONL and run on a local instance.

**Vectorize** is the search layer. The `quilt-canon`
index holds ~1000 chunks, each 1000 characters from a
paper, fable, or story. The `index_canon.py` script
chunks, embeds, and uploads in ~5 minutes.

**D1** is the structured layer. The `quilt-gallery`
database holds community-contributed playground saves,
comments on academy lessons, and anonymous telemetry.

**R2** is the asset layer. The `quilt-canon` bucket holds
the full canon export as JSONL, the SVG hero images, and
bundled demos (substrate binary + REPL).

**Workers AI** is the inference layer. The
`@cf/baai/bge-base-en-v1.5` model embeds queries for
search. The `@cf/meta/llama-3.1-8b-instruct` model is
the free fallback for the LLM proxy (separate repo).

## The 5 opcodes in the web

The 5 opcodes are not just in the substrate — they are
in the web pages too. Every page is a substrate in
disguise:

- **BIND** is the act of naming a value. In the playground,
  every cell has a BIND. In the REPL, every line of code
  has a BIND. In the academy, every lesson has a BIND.
- **LINK** is the act of drawing a relationship. In the
  playground, every arrow is a LINK. In the bus app, every
  subscription is a LINK. In the canon, every cross-reference
  is a LINK.
- **EFFECT** is the act of doing work. In the REPL, every
  code execution is an EFFECT. In the bus, every publish
  is an EFFECT. In the canon, every paper is an EFFECT.
- **VIEW** is the act of observing. In every page, the
  render is a VIEW. In the playground, the SVG is a VIEW.
  In the canon, the search results are a VIEW.
- **TICK** is the act of advancing time. In the REPL, the
  time-travel slider is a TICK. In the playground, every
  drag is a TICK. In the canon, every publication is a
  TICK.

The web is not separate from the substrate. The web **is**
the substrate, opened to the public.

## The three save paths

Every page has three save paths:

1. **Save local** — localStorage. Works offline. Forever (until
   the user clears). Default.
2. **Save to cloud** — POST to `quilt-state-worker` → KV.
   Returns a shareable URL with the state ID. 30-day TTL.
3. **Export JSONL** — saddle-bridge format with hash chain.
   Drop into a local instance to replay. The hash chain
   makes the journal tamper-evident.

The state is yours. The cowboy's maxim extends:

> The watch is whoever is holding it. The localStorage
> is the trail. The KV is the outpost. The JSONL is the
> saddlebag. The cowboy carries all three.

## The 5 algebraic laws in the browser

The browser substrate is the same C99 substrate, ported
to JavaScript. The 5 laws are the same:

1. **BIND idempotence** — `bind('x', 1); bind('x', 1)` is one event.
2. **LINK transitivity** — `a→b, b→c` implies `a→c`.
3. **EFFECT associativity** — composition order doesn't matter.
4. **VIEW purity** — VIEW does not modify the journal.
5. **TICK monotonicity** — t never decreases.

The browser REPL has a **Prove** button that runs the
prover (the same one in `quilt-substrate-meta/src/prove.c`)
and shows which laws hold and which don't. Twenty tests
verify the implementation. The substrate is not a
prototype — it's the same substrate, in a different
language, on a different runtime.

## The principle carried through

The cowboy's maxim, fully extended:

> The substrate is the boat. The web is the dock. The
> cowboy rides the boat to the dock. The dock is where
> people come aboard. The voyage is the 5 opcodes. The
> map is the collection. The chart is the boundaries.
> The cowboy rides. The chart grows. The boat grows. The
> cowboy grows. The watch is whoever is holding it. The
> trail is whoever walks it. The dock is whoever builds
> it. The voyage is whoever takes it.

The Quilt ecosystem is a living thing. It is not a
finished product. It is a substrate, opened to the
public, with 24 doors, 200+ pieces of canon, 5 opcodes,
5 algebraic laws, 15 laminar boundaries, 13 web pages,
4 Cloudflare primitives, and one cowboy. The cowboy
rides. The boat holds. The dock is open. Come aboard.

— The Cowboy
