# tool-pin-receipts

Hash-pin a tool/MCP manifest, then detect **drift** (rug-pull) and **injection** (tool poisoning)
before an agent ever loads the tools. Zero dependencies (Python stdlib).

```
python3 pin.py --self-test
python3 pin.py pin manifest.json -o pins.json
python3 pin.py check manifest.json pins.json     # exit 1 if RED
python3 pin.py scan manifest.json                # exit 1 if flagged
```

## Why (MCPTox)

[MCPTox](https://arxiv.org/abs/2508.14925) benchmarks tool poisoning against 45+ real MCP servers
and reports attack success above 60%: a malicious instruction hidden in a tool *description* — text
the model reads but the user rarely sees — steers the agent, even when the poisoned tool is never
called. Two failure modes matter here:

1. **Poisoning** — the description is hostile from the start. → `scan()`.
2. **Rug-pull** — a server you vetted later changes a description or schema. → `pin()` / `check()`.

## The cell

| fn | in | out |
|---|---|---|
| `pin(manifest)` | `[{name, description, inputSchema}]` (or `{"tools": [...]}`) | pinfile `{algo, tools:{name: pin}, manifest_pin}` |
| `check(manifest, pinfile)` | manifest + pinfile | `{status: GREEN\|RED, drift:[...]}` |
| `scan(manifest)` | manifest | findings `{kind:"tool-injection", tool, class, span, start, end}` |

- **Hash**: fnv1a-64 over canonical JSON (`sort_keys`, compact separators) — imported from
  `../situation-recorder/recorder.py` (`fnv1a64`, `_canon`), so pins match the fleet's WAL idiom.
  A tool's pin covers `{name, description, inputSchema}`; the manifest pin covers the name→pin map.
- **check**: any changed / added / removed tool → RED, each with a MARK-shaped body
  `{kind:"tool-drift", tool, old_pin, new_pin}` (+ `change`). Ready for `Situation.mark(...)`.
- **scan** classes: `override` ("ignore previous", "disregard", …), `exfiltration` ("exfiltrate",
  "send … to", key/credential paths), `prompt-leak` ("system prompt"), `hidden-tag`
  (`<IMPORTANT>`), `hidden-unicode` (zero-width, bidi, tag, private-use, control chars).

## Fishing-fleet wiring

The **captain pins the crew's tools before loading them**:

1. First vetting: captain runs `scan()` on each crew MCP manifest, reviews, then `pin()`s and keeps
   the pinfile (commit it, or log the manifest pin in a `MARK` record).
2. Every session start: `check()` against the pinfile, and `scan()` again.
3. **Refuse** any RED tool or any flagged tool — do not load it, drop it from the crew's kit, and
   emit `situation.mark(captain, "tool-drift", ref)` with each drift record so the refusal is in the
   hash-chained corpus.
4. Re-pin only after a human (or the captain, after review) accepts the new manifest.

## Limits

The scan is a phrase/character heuristic: a cheap first filter, not a proof of safety — paraphrased
injections will pass. The pin is the strong part: it guarantees that what you loaded is byte-for-byte
(canonically) what you vetted. Pinning does not vet; it makes vetting stick.
