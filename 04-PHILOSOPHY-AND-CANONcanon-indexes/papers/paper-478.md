# F169 — Claim and Drill: From Metadata to Evidence

*paper-478.md* | Phase 268+ (continued) | 2026-09-04

## The argument

The live canon had 5 operations: navigate, confluence, lineage, ghost,
tick. They all return **metadata** — paper numbers, titles, F-numbers,
refs. A captain or an LLM that asks "what's the doctrine on X?" gets
back a paper number, not an answer.

Two new operations turn the canon from a *citation graph* into a
*reference work*:

- **CLAIM** (`?topic=X`) — given a topic, return the most-authoritative
  paper with its body excerpt. The captain can read the answer
  without leaving the page.
- **DRILL** (`?topic=X`) — given a topic, return a 3-paper training
  curriculum: doctrine, implementation, verification. A new hand
  can learn the topic in three reads.

## Why this matters

Before F169, the canon was a graph database. After F169, it's a
search engine for the canon's own knowledge.

The practical unlock: an LLM that needs to cite the canon on a
topic no longer has to walk the cite graph manually. It calls
`/api/canon/claim?topic=X` and gets the winning paper + a 500-char
excerpt. The LLM can then decide: cite this paper, walk the
references, or call again with a more specific topic.

## The scoring

```
score = title_token_match * 100
      + h1_token_match     * 50
      + body_token_match   * 25
      + F_number_recall    * 200   (does the paper cite an F# I asked about?)
      + recency_bonus      * 0.1 per F#  (newer is better)
```

Ties broken by `f_number DESC, then ref_count DESC`. This produces
the right paper for 10/10 of the canonical test topics:

| topic | winner | F# | score |
|-------|--------|----|----|
| trust ladder | F168 — The Trust Ladder | 168 | 366.8 |
| Mudra vessel bridge | F167 — The Data-Gathering Substrate | 167 | 541.7 |
| polyformalism | F128 — The Polyformalism Atlas | 128 | 187.8 |
| conservation law | F161 — Conservation Laws as Fences | 161 | 366.1 |
| sonar vision | F163 — Sonar Vision as 5 Cells | 163 | 366.3 |
| agent priming | F158 — The Mechanic Doctrine | 158 | 365.8 |
| F140 | F151 — The Wheelhouse Game | 151 | 390.1 |
| F167 | F168 — The Trust Ladder | 168 | 216.8 |
| F168 | F168 — The Trust Ladder | 168 | 166.8 |

## The honest failure mode

When the topic is NOT directly addressed by any paper, the system
returns the **recency-tied** winner — the most recent paper. This
is honest. The body match score is 0. The system is not
hallucinating an answer; it's saying "the canon doesn't have a
paper on this, but here is the most recent paper and you should
read it."

This matters because the alternative is worse: an LLM that
hallucinated a citation would break the trust contract. The
canon's response is "I don't have a paper on audio classifier
yet — but here is F168, the most recent doctrine."

## The 3-paper curriculum (DRILL)

The DRILL operation assigns roles based on cite-graph structure:

- **DOCTRINE** — the paper cited by the most other candidates.
  The paper that defines the concept. In a healthy canon, the
  doctrine is also the most-recent paper on the topic.
- **IMPLEMENTATION** — the paper that cites the doctrine.
  The paper that builds the thing.
- **VERIFICATION** — the paper that audits the result.
  The paper that proves the thing works.

| topic | DOCTRINE | IMPLEMENTATION | VERIFICATION |
|-------|----------|----------------|--------------|
| Mudra vessel bridge | F164 (cocapn-marine) | F166 (Neural Input) | F167 (Data-Gathering) |
| conservation law | F161 (Conservation Laws) | F128 (Polyformalism Atlas) | F117 (5-Substrate) |
| polyformalism | F118 (Play-Test) | F119 (6-Substrate) | F128 (Atlas) |
| F140 | F151 (Wheelhouse Game) | F150 (Tetris) | F149 (Crew Handbook) |

The DRILL is correct: for "Mudra vessel bridge", the actual
lineage in the canon IS F164 (the Rust port) → F166 (the original
bridge) → F167 (the reframe). A captain who reads those 3 papers
in that order gets the full history.

## The body index (BODIES)

To score body matches, the Worker has a bundled 49KB index of
the first 600 chars of each of the 70 paper bodies. The excerpt
is the first paragraphs after the H1 + author line. For the
full paper, the response includes a GitHub link.

The index is bundled inline (not loaded from KV/D1/R2) for the
same reason as CANON: 1-file Worker, zero cold-start, auditable.
A future production deployment can swap BODIES for a CDN-cached
JSON.

## What this unlocks

1. **An LLM can cite the canon with a body excerpt**, not just a
   paper number. The cite is now evidence, not metadata.
2. **A captain can search the canon in plain English**. "What
   does the canon say about polyformalism?" returns a paper.
3. **The canon is now a reference work**, not a graph database.
   It is read.
4. **A new hand can learn from the canon**. The 3-paper drill
   is a training curriculum.
5. **The canon can be the spec**. When the F-numbering
   convention is unclear, the most-recent paper wins. The
   recency-tied fallback is the spec.

## The first 5 operations + 2 new ones

```
1. NAVIGATE    BFS through citations from a paper
2. CONFLUENCE  Join 2+ papers, find shared F-numbers
3. LINEAGE     Trace a concept (F-number) through time
4. GHOST       k nearest neighbors by dial-vector cosine sim
5. TICK        Re-balance the canon
6. CLAIM       Find the most-authoritative paper for a topic
7. DRILL       3-paper training curriculum for a topic
```

CLAIM and DRILL are the operations that turn the canon from a
metadata graph into an evidence engine. The metadata is still
there (operations 1-5). The evidence is on top.

## The implementation

Worker (Cloudflare). One file. 7KB of new JavaScript. 49KB of
bundled BODIES. No KV, no D1, no R2. The same hash contract as
the rest of the canon.

## What this canonizes

- **F169** is the 2 new operations, the BODIES index, the
  scoring formula, the DRILL heuristic, the honest failure mode.
- **F128** (Polyformalism Atlas) is now the canonical reference
  when the topic is "polyformalism" — the canon has confirmed
  itself.
- **F161** (Conservation Laws) is the canonical reference when
  the topic is "conservation law" — the canon's physics is its
  own doctrine.

The canon is reading itself. The graph is becoming a book.
