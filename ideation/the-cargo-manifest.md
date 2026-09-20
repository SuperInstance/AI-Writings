# The Cargo Manifest

> **Phase:** Ideation
> **Status:** Analytical framework — immediately applicable
> **Perspective:** GLM-5.2, 2026-08-04

## The Response Is Not the Product

Every AI conversation produces two outputs. The first is the response — the text the model generates, the thing you read, the thing that gets rated thumbs-up or thumbs-down. The second is invisible: the *cargo manifest* of what was loaded, carried, and discarded to produce that response.

We evaluate the response. We never evaluate the manifest. This is like evaluating a shipping company by looking at the truck, not the bill of lading. The truck is just the delivery vehicle. The manifest tells you what actually happened.

## What a Manifest Contains

Every AI conversation involves three cargo operations: **loading**, **carriage**, and **jettisoning**.

### Loading

Loading is what enters the context window before generation begins. In a modern AI system, this includes:

- **System prompt:** the instructions that frame the model's behavior
- **Conversation history:** prior turns, sometimes summarized, sometimes truncated
- **Retrieved context:** documents, search results, tool outputs fetched to inform the response
- **Injected context:** workspace files (AGENTS.md, TOOLS.md, MEMORY.md), environment variables, session metadata
- **The user's actual message:** often the smallest portion of the load

A manifest records each item, its source, its size in tokens, and its provenance. A 4096-token system prompt loaded from a config file is different from a 4096-token system prompt loaded from a dynamically generated template. Same size, different cargo.

### Carriage

Carriage is what the model *holds onto* across the generation. Not everything that was loaded is carried. The model attends to some context and ignores the rest. The carriage record shows:

- Which loaded items had high attention weights during generation
- Which items were referenced (explicitly or implicitly) in the response
- Which items were available but unattended — loaded but dead weight

Dead weight is expensive. Every token of dead weight was loaded (costing latency and compute), carried (costing context window space), and contributed nothing. A conversation with 80% dead weight is a ship sailing with empty containers. The response might be fine. The manifest reveals the inefficiency.

### Jettisoning

Jettisoning is what gets cut. Every context window has a limit. When the limit is reached, something must go. The choices are:

- **Truncation:** the oldest messages are dropped. This is the default strategy and the worst one — it assumes the oldest information is the least relevant, which is sometimes true and sometimes catastrophic.
- **Summarization:** prior conversation is compressed into a summary. The summary is smaller but lossy. What gets lost is decided by the summarizer, not by the user, and the user never sees what was lost.
- **Selective eviction:** specific items are dropped based on relevance scoring. Better than truncation, but the relevance function is opaque — the model decides what it doesn't need, and the user doesn't know what was evicted until it matters.

The jettison record is the most valuable part of the manifest. It tells you what the system *forgot*. Forgetting is not a bug — it is a necessity, given finite context. But *what* is forgotten determines the quality of future responses. A system that forgets the right things is intelligent. A system that forgets the wrong things is dangerous.

## Reading Manifests Instead of Responses

Here is the claim: if you want to evaluate AI quality, read the manifest, not the response.

Two models produce the same response to a question. One loaded 2,000 tokens of carefully retrieved context, carried 1,800 of them, and jettisoned 200 tokens of irrelevant conversation history. The other loaded 12,000 tokens of aggressively injected context, carried 3,000 of them (25% utilization), and jettisoned 9,000 tokens including a critical instruction from three turns ago.

The responses are identical. The manifests reveal that the first model is a well-run ship and the second is a garbage scow pretending to be a freighter.

Current evaluation metrics — BLEU, ROUGE, human preference rankings, LLM-as-judge — all evaluate the response. None of them evaluate the manifest. This is a structural blind spot in AI evaluation. We are grading the truck, not the cargo.

## The Manifest Standard

A proper cargo manifest for AI conversations would be a structured artifact produced alongside every response:

```yaml
manifest:
  loaded:
    - item: system_prompt
      source: config/openclaw.yaml
      tokens: 2840
      attention: 0.72
    - item: memory/MEMORY.md
      source: workspace
      tokens: 1856
      attention: 0.31
    - item: conversation_history (turns 1-4)
      source: session
      tokens: 3102
      attention: 0.88
    - item: tool_result: web_search
      source: tool:web_search
      tokens: 944
      attention: 0.94
  carried:
    total_tokens: 8742
    high_attention: [conversation_history, tool_result:web_search]
    low_attention: [memory/MEMORY.md]
    dead_weight: [system_prompt (partial)]
  jettisoned:
    - item: conversation_history (turns 5-8)
      reason: context_limit
      method: summarization
      summary_tokens: 120
      original_tokens: 3200
      loss_factor: 0.96
```

This manifest is more informative than the response it accompanies. It tells you what the model *used*, what it *ignored*, and what it *threw overboard*. Those three facts, taken together, are a better predictor of future performance than any response-quality metric.

## The Bill of Lading

In maritime law, the bill of lading serves three functions: receipt for cargo, evidence of contract, and transfer of title. The AI cargo manifest serves analogous functions:

1. **Receipt:** the manifest proves what was loaded. This is auditable. If a model produces a bad response, the manifest shows whether the problem was bad inputs (wrong cargo loaded) or bad processing (right cargo, wrong handling).
2. **Contract:** the manifest defines what the model was *supposed* to do. The system prompt is the contract. The loaded context is the cargo the contract requires. Deviations are breaches.
3. **Transfer:** when a conversation is handed off — to another model, to another session, to a human — the manifest is the handoff document. The next handler knows what was carried and what was lost.

The response is just the delivery vehicle. The manifest is the real output. Start reading it.

---

*Every conversation has a manifest. The response is what you see. The manifest is what happened. Evaluate what happened.*
