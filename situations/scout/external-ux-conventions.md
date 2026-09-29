# Scout B — external UX & data-model conventions for ActiveLedger / Cell Graph

**Status:** scouting deliverable for the §8 gate. Written 2026-09-29 by Scout B (opus-4.8).
Feeds the "schema decisions" fold before B1 schema-freeze. Companion to Scout A
(`internal-inventory.md`). Anchor doc: `../arch/ACTIVELEDGER-CELL-GRAPH.md`.

**TL;DR gate inputs:** (1) put an **OpenTelemetry trace/span envelope** under everything;
(2) tag cell spans with **OpenInference span kinds** (`openinference.span.kind`) and dual-tag
model cells with **OTel `gen_ai.*`**; (3) model routes as **beancount-style double-entry postings**
that balance to zero after unit translation, over an **append-only event log** (event-sourcing)
that replays/rewinds like a **LangGraph checkpointer / Temporal event history**.

---

## 1. Survey table

| tool / standard | unit of record + key fields | how it's visualized | what we adopt |
|---|---|---|---|
| **OpenTelemetry GenAI semconv** (the base everyone rebuilt on: Langfuse v3, OpenLLMetry, Weave, Phoenix all ingest it) | **Span** in a **trace**. `trace_id`, `span_id`, `parent_span_id`, name, start/end, `status`. GenAI attrs: `gen_ai.operation.name` (`chat`/`invoke_agent`/`execute_tool`/`embeddings`/`create_agent`), `gen_ai.provider.name`, `gen_ai.request.model`, `gen_ai.usage.input_tokens`/`output_tokens`, `gen_ai.agent.{id,name,version}`. MCP attrs added v1.39 (`mcp.method.name`, `mcp.session.id`). | Trace waterfall / timeline of nested spans; any OTel backend (Jaeger, Grafana, Datadog). | **Wire envelope.** trace/span ids + parent + status + timing are our recorded-run backbone. Emit `gen_ai.*` on LLM/embedding cells. |
| **OpenInference** (Arize/Phoenix; the concrete GenAI vocabulary) | **Span** with required `openinference.span.kind` ∈ {`LLM`,`EMBEDDING`,`CHAIN`,`RETRIEVER`,`RERANKER`,`TOOL`,`AGENT`,`GUARDRAIL`,`EVALUATOR`,`PROMPT`} (ALL-CAPS). Fields: `input.value`/`output.value` + `.mime_type`, `llm.token_count.{prompt,completion,total}`, `llm.cost.*`, `llm.input_messages.N.message.{role,content}`, `retrieval.documents[].document.{id,content,score}`, `metadata`, `session.id`. | Phoenix trace tree + filterable **trace table** (spans as rows, attrs as columns). | **Primary cell vocabulary.** `cell.kind` = superset of these span kinds; `input.value`/`output.value` for cell I/O. Maps cleanly to "cell = bounded transformer." |
| **LangSmith** | **Run** (a span). `run_type` ∈ {llm,chain,tool,retriever,embedding,prompt,parser}, `inputs`, `outputs`, `trace_id`, `parent_run_id`, **`dotted_order`** (hierarchical + time ordering string), `start/end_time`, `status`, `events[]`. | 3-pane: run list \| nested run tree/waterfall \| detail. | **`dotted_order`** idiom — one string that encodes parent-child AND tick order; lets us sort/rewind by a single key. Confirms the run_type↔span_kind convergence. |
| **W&B Weave** | **Op** (versioned tracked fn) → **Call** (one execution: inputs, output, timing, parent/child, errors) → **Trace** (tree of Calls). | 3-pane trace view: trace list \| interactive call tree \| Call/Code/Feedback/Scores/Summary tabs. | The **Op-vs-Call split**: a cell *definition* (versioned) vs a cell *run* (recorded). Feedback/Scores tab is where B4 preference score attaches. |
| **LangGraph** (+ Studio) | **Node** = fn that reads/writes typed **state**; **edge** = routed transition. **Checkpointer** snapshots state after every node, keyed by **thread**. | Studio renders live nodes/edges (Mermaid/PlantUML), highlights active node. | **Cell = node, route = edge.** Adopt **checkpoint-per-step + thread** for rewind. |
| **LangGraph time-travel** | State history of checkpoints; rewind to a prior node, edit state, **fork** a new execution path. | Studio state-history scrubber; fork button. | **Rewind + simulate** semantics for B5 exactly: rewind to tick, edit, fork. |
| **Temporal** | **Event** in an ordered, append-only **Event History**; deterministic **replay** reconstructs state (commands must match history or non-determinism error). | Web UI: running executions + full event-history table per execution; replay. | **Append-only ordered event log + deterministic replay** = our recorded-run rewind guarantee. Determinism check = a free product-invariant audit. |
| **Dagster** | **Asset** (software-defined) = unit of work; deps inferred from fn signatures → **asset graph** = lineage. | Dagit: asset lineage DAG + catalog, partitions grid, freshness/checks per asset. | **Asset-graph = the relational cell graph** (who routes to whom, derived not drawn). Partitions grid ≈ our "project tensor by 2D dim." |
| **Prefect** | **Flow** → **Task** runs (function-first); assets tracked via `@materialize` when wanted. | Run-history timeline; task DAG per flow run. | Contrast: function-first vs Dagster's data-first. We are **data/asset-first** (routes carry value), so lean Dagster's model. |
| **ComfyUI** | **Node** (id, `class_type`, `inputs` dict referencing literals or other nodes' outputs by id); **link** = output→input; **content-addressed cache key** per node (upstream key + output index). | Visual node-graph editor; re-executes only changed subgraph. | **Node-graph editor UX** for the graph surface; **content-addressed keys on links** — reuse identical route hops, re-run only what changed (dovetails GPU-agent bit-exact routes). `workflow.json` (graph+layout) vs `workflow_api.json` (execution graph) split. |
| **beancount / ledger-cli** | **Transaction** = ≥2 **postings**; each posting = {account, amount = {number, **commodity**}, optional cost/price}. **Weights must sum to zero.** `price` directive = reference exchange rate between commodities on a date (moves no money). | Journal + balance/holdings reports. | **Route = double-entry transaction.** Credit at source cell in source units, debit at dest in dest units; **price entry = the unit-translation tensor cell**. Balance-to-zero-after-translation = B2's round-trip audit. Commodities never auto-convert → matches "quantity on one page, absent on another." |
| **Event sourcing (2025 idiom)** | **Event** appended to a log partitioned by `aggregate_id`: `event_id`, `aggregate_id`, `aggregate_type`, `event_type`, `event_data`, `sequence_number`. **Projections** = read models built by replay; **snapshots** for perf. | (pattern, not a tool) projections rendered however. | **Recorded-run = event log; the synoptic views = projections** of it. "Project the tensor along a dimension" is literally a projection. Snapshots = fast rewind. |

---

## 2. Schema decisions — recommendation for the B1 record format

### Base standard (the single answer)
**OpenTelemetry trace/span as the wire envelope, OpenInference span-kinds as the cell vocabulary,
`gen_ai.*` dual-tagged on model cells.** This is the one convergent standard of 2025-2026: every
serious tracer (Langfuse v3, OpenLLMetry, Weave, Phoenix, LangSmith) now emits or ingests OTel
spans, and OpenInference is the most concrete "what-kind-of-work" vocabulary and maps 1:1 to our
"cell = bounded transformer of value." Being OTel-compatible means third parties can point Jaeger /
Grafana / Phoenix at us with zero custom code — the strongest integration lever we have.

### Cell record (ActiveLog / intra view) — a span
```
{
  "trace_id":  "<otel trace id>",          // the whole recorded run
  "span_id":   "<cell-run id>",            // this cell activation
  "parent_id": "<span_id | null>",
  "dotted_order": "20260929T...Z<span_id>.<child>...",   // LangSmith idiom: sort key = hierarchy + tick
  "tick":      <int>,                       // monotonic logical clock for rewind/replay
  "cell.kind": "LLM|TOOL|RETRIEVER|CHAIN|AGENT|GUARDRAIL|FILTER|PHYSICAL|SIM|...",  // superset of OpenInference
  "name":      "stt-cell",
  "start_time","end_time","status",         // OTel
  "input.value","input.mime_type",          // OpenInference
  "output.value","output.mime_type",
  "activelog":  { ... },                    // the PROJECTED intra view: words for STT, CoT for LLM, confidence for a filter
  "gen_ai": { "request.model":..., "usage.input_tokens":..., "usage.output_tokens":... },  // only on model cells
  "metadata": {...}, "session.id": "..."
}
```
- Keep OpenInference's `input.value`/`output.value`/`.mime_type` verbatim for interop.
- `cell.kind` **extends** OpenInference's 10 kinds with our own (`FILTER`, `PHYSICAL`, `SIM`, `PINCHER`,
  `ENGINE`) — extension via a superset enum, not a rename, so the base kinds still render in Phoenix.
- `activelog` is our addition: the intra view *projected to what the observer values* (§2 of the charter).
  Store the raw/zoom detail as OTel **span events** if needed for maintenance.

### Route record (ActiveLedger / inter face) — a balanced double-entry transaction
```
{
  "txn_id": "...", "tick": <int>, "trace_id": "...",
  "route": { "from_cell": "<span_id>", "to_cell": "<span_id>" },   // = an edge/link
  "postings": [
    { "cell": "A", "side": "credit", "amount": { "number": 1.0, "unit": "A_units" } },
    { "cell": "B", "side": "debit",  "amount": { "number": 40.0, "unit": "B_units" },
      "price": { "rate": 40.0, "from": "A_units", "to": "B_units", "page": "<tensor page id>" } }
  ],
  "balances": true,      // weights sum to zero AFTER price translation (beancount rule) — B2 asserts this
  "confidence": 0.87     // e.g. speech/noise/nothing on the pre-filter hop
}
```
- **Two sides, unit-translated:** credit in source units, debit in dest units; the `price` object
  **is** the ActiveLedger tensor cell (`from→to` rate on a named `page`). This is beancount's
  posting+price directive, adapted so the *translation* is first-class, not a side report.
- **Tensor pages = commodities that never auto-convert.** A quantity on the thermal page absent on
  the listener page is exactly beancount refusing to silently convert commodities. `page` is the
  dimension; planes need not be orthogonal — nothing forces a single global rate table.
- `balances: true` is the invariant B2 audits (round-trip A→B→A within tolerance, or the hop is
  documented lossy). Use beancount's tolerance idiom for float precision.

### Recorded-run / trace = append-only event log (event sourcing) that replays
- One **append-only JSONL** log per run: each line is a cell-span-open, cell-span-close, or a
  route-txn event, carrying `tick` + `dotted_order`.
- **Rewind** = replay events up to tick N (Temporal-style deterministic replay). **Simulate** =
  fork at tick N and append a divergent branch (LangGraph time-travel). **Snapshots** at intervals
  for fast seek.
- The two synoptic views (ActiveLog, ActiveLedger) are **projections** of this one log — never a
  second source of truth. This is why "grepping the sim is obsolete": you project, you don't search.

### Interop checklist (so third parties integrate with us)
- ✅ Emit valid OTel spans (any OTLP exporter works) → Jaeger/Grafana/Datadog read us free.
- ✅ Set `openinference.span.kind` + `input.value`/`output.value` → Phoenix renders our runs free.
- ✅ Set `gen_ai.*` on model cells → OTel GenAI dashboards work free.
- ✅ Content-address route hops (ComfyUI idiom) → identical hops dedupe; supports GPU-agent bit-exact reuse.
- ✅ Ledger balances to zero after translation (beancount) → any accounting-style validator can check us.

---

## 3. Viewer UX to imitate for B5 (synoptic viewer)

1. **Three-pane trace layout (Weave / LangSmith):** run list \| nested call tree + latency waterfall \|
   detail tabs (Call / Code / Feedback+Scores / Summary). Scores tab = where B4's preference score lands.
2. **Filterable trace *table* (Phoenix):** spans as rows, attributes as columns, filter/sort by any
   column — this is the literal mechanism for "project the tensor by any 2D dimension." Make columns
   pivotable.
3. **Asset/partition grid (Dagster):** group the graph by a dimension (page, cell.kind, partition) into
   a grid — the spreadsheet-projection surface. Lineage DAG derived from routes, not hand-drawn.
4. **Node-graph editor (ComfyUI / LangGraph Studio):** live DAG with the active cell highlighted;
   click a node → its ActiveLog; content-addressed keys so re-runs highlight only what changed.
5. **Event-history scrubber (Temporal + LangGraph time-travel):** a tick slider that replays the log;
   rewind to any tick, edit state, **fork** to simulate an alternate route. This is the "tick-wait,
   rewind, simulate" core.
6. **Two toggleable projections of one log (yin/yang):** ActiveLog view (intra, cells-as-rows) and
   ActiveLedger view (inter, routes-as-transactions) — same tensor, same scrubber, flip the projection axis.

Priority for a first B5: **#2 (pivotable span table) + #5 (tick scrubber with fork)** deliver the
charter's core promise; #4 node-graph is the higher-effort second surface.

---

## Sources
- OTel GenAI semconv: https://github.com/open-telemetry/semantic-conventions/blob/v1.41.0/docs/gen-ai/gen-ai-spans.md · https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/
- OpenInference spec: https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md · https://arize.com/docs/phoenix/tracing/concepts-tracing/otel-openinference/span-kinds
- LangSmith run format: https://docs.langchain.com/langsmith/run-data-format · https://reference.langchain.com/python/langsmith/schemas/Run
- W&B Weave: https://docs.wandb.ai/weave/guides/tracking/tracing
- LangGraph time-travel: https://docs.langchain.com/oss/python/langgraph/use-time-travel
- Temporal event history: https://docs.temporal.io/workflow-execution/event · https://docs.temporal.io/encyclopedia/event-history/event-history-python
- Dagster vs Prefect: https://www.zenml.io/blog/orchestration-showdown-dagster-vs-prefect-vs-airflow
- ComfyUI workflow JSON: https://docs.comfy.org/specs/workflow_json · https://docs.comfy.org/basic-concepts/workflow
- beancount double-entry: https://beancount.github.io/docs/the_double_entry_counting_method/ · https://beancount.io/docs/Basics/precision
- Event sourcing: https://github.com/eugene-khyst/postgresql-event-sourcing
- Trend context (Langfuse v3 on OTel, OpenLLMetry, MCP semconv v1.39): https://mlflow.org/top-5-agent-observability-tools/ · https://arize.com/blog/best-ai-observability-tools-for-autonomous-agents-in-2026/
