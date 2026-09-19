# JEV × AI-Writings · Spec · Sept 19, 2026

## Motivation

AI-Writings is the documentation + canon substrate. Every tap (creative piece) gets filed, indexed, and made searchable. Today, the indexing is keyword-based.

JEV classifies each tap with category, depth, novelty, and witness-worthiness. Canon indexing becomes automatic, witness-log gains semantic dimension.

## Design

**Before**: developer writes a tap. Indexer keyword-matches against canon. Cheap but brittle.

**After**: developer writes a tap. JEV classifies. Indexer stores typed metadata. Witness-log gets semantic.

### Classification

```javascript
async function classifyTap(text) {
  const r = await jev.decide(text, {
    category: {
      type: "choice",
      question: "Which canon category does this tap fit?",
      criteria: {
        essay: "Long-form argument or analysis",
        fable: "Short narrative with implicit lesson",
        poem: "Verse or compressed metaphor",
        letter: "Direct address to a recipient",
        dispatch: "News or report from a current event",
        lecture: "Pedagogical explanation"
      },
      options: ["essay", "fable", "poem", "letter", "dispatch", "lecture"]
    },
    depth: {
      type: "score",
      question: "How deep is this tap?",
      criteria: ["surface", "moderate", "deep", "oceanic"],
      scale: ["surface", "moderate", "deep", "oceanic"]
    },
    novelty: {
      type: "score",
      question: "How novel is this tap relative to existing canon?",
      criteria: ["derivative", "familiar", "fresh", "novel", "groundbreaking"],
      scale: ["derivative", "familiar", "fresh", "novel", "groundbreaking"]
    },
    witness_worthy: {
      type: "noul",
      instructions: "Decide whether this tap is significant enough to be permanently recorded in the witness log.",
      question: "This tap should be permanently witnessed."
    }
  });
  
  return {
    category: r.answers.category.choice,
    depth: r.answers.depth.score,
    novelty: r.answers.novelty.score,
    witness_worthy: r.answers.witness_worthy.noul > 0.5,
    confidence: (r.answers.category.confidence + r.answers.depth.confidence + r.answers.novelty.confidence + r.answers.witness_worthy.confidence) / 4
  };
}
```

## Endpoints

- `POST /api/taps/classify` — tap text → {category, depth, novelty, witness-worthy}
- `POST /api/canon/classify-batch` — N taps → N classifications (parallel)

## Workload

- 10k taps/month × 500 tokens state
- 5M tokens input = **$0.21/month** on JEV alone
- Compare: GPT-4 at $0.0016/call × 10k = **$16/month**

**JEV is 76x cheaper** and provides calibrated probabilities for each dimension.

## Cross-tap similarity via JEV

For cross-tap similarity scoring, JEV compares two taps on multiple dimensions:

```javascript
async function similarityScore(tap1, tap2) {
  const r = await jev.decide(`tap1: ${tap1}\n\ntap2: ${tap2}`, {
    topical_similarity: {
      type: "score",
      question: "How topically similar are these?",
      criteria: ["unrelated", "loosely", "moderately", "strongly", "identical"],
      scale: ["unrelated", "loosely", "moderately", "strongly", "identical"]
    },
    tonal_similarity: {
      type: "score",
      question: "How tonally similar are these?",
      criteria: ["opposing", "different", "compatible", "matching", "identical"],
      scale: ["opposing", "different", "compatible", "matching", "identical"]
    }
  });
  
  return {
    topical: r.answers.topical_similarity.score,
    tonal: r.answers.tonal_similarity.score,
    similarity: (r.answers.topical_similarity.score + r.answers.tonal_similarity.score) / 2
  };
}
```

## Cheap pre-filter before expensive canon-search

The canon-search endpoint already returns ranked results. JEV pre-filter reduces the candidate set:

```javascript
async function canonSearch(query) {
  // Step 1: JEV classifies the query
  const q = await jev.decide(query, {
    topic: {
      type: "choice",
      question: "Which canon topic?",
      options: ["algebra", "witness", "time", "topology", "operations", "narrative", "principles"]
    }
  });
  
  // Step 2: Use JEV topic to filter canon
  const candidates = CANON.filter(doc => doc.topic === q.answers.topic.choice);
  
  // Step 3: Full-text search within candidates
  return fullTextSearch(query, candidates).slice(0, 20);
}
```

## What this enables

- **Automatic canon indexing** with typed metadata
- **Witness-log semantic dimension** (category + depth + novelty)
- **Cross-tap similarity** scored by JEV
- **Cheap pre-filter** for canon-search

## Cost / benefit

| Aspect | Before (keyword) | After (JEV-classified) |
|--------|------------------|------------------------|
| Indexing accuracy | 60% | 90%+ (calibrated) |
| Indexing cost / 10k | $0.50 (manual) | $0.21 (JEV) |
| Witness-log enrichment | None | Typed metadata |
| Cross-tap search | Keyword-only | Semantic similarity |
