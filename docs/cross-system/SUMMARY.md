# JEV × Cross-System Specs · Sept 19, 2026

5 specs covering how JEV integrates with the rest of the Quilt stack.

## pincher.md — vector scoring (115 lines)
**Before**: developer hand-tunes vector thresholds with regex + manual review
**After**: JEV scores each vector against a rubric in 150ms
**Workload**: 1M vectors/month × 200 tokens = **$8.40/month** on JEV (vs $1,600/month on GPT-4)
**Pattern**: developer iterates by adjusting rubric, not code

## lever-runner.md — agent orchestration (94 lines)
**Before**: agent emits 10 free-text candidate actions, runner parses and picks
**After**: JEPA pre-classifies → JEV scores → LLM narrates top-3 → runner executes top-1
**Reduction**: 80% reduction in hallucination-induced actions
**Cost**: $2.73/month on JEV vs $5,000/month for full LLM-everywhere

## plato.md — teacher-student architecture (131 lines)
**Before**: every student question → teacher LLM ($2,500/month per 100k Q)
**After**: JEV classifies each question by depth + topic + confidence; teacher LLM only for "deep"
**Reduction**: 10x reduction in teacher-LLM calls (90% handled by JEV)
**Pattern**: shallow + teachable → JEV answer; deep + low-confidence → LLM teaches

## sunset-ecosystem.md — simulation substrate (123 lines)
**Before**: tick = JEPA predict → LLM narrate → next tick (no validation)
**After**: tick = JEPA → JEV validate → LLM narrate → next tick
**Use case**: 1000 parallel simulations, JEV flags the 5 that diverged
**Cost**: $84/month for fully validated, narrated, audited simulation
**What this enables**: early detection of "impossible" simulation paths

## ai-writings.md — canon substrate (141 lines)
**Before**: keyword-based indexing of taps
**After**: JEV classifies each tap with category + depth + novelty + witness-worthiness
**Workload**: 10k taps/month × 500 tokens = **$0.21/month** on JEV (vs $16/month on GPT-4)
**What this enables**: automatic canon indexing, semantic witness-log, cross-tap similarity

## Unified pattern

Across all 5 specs, the same pattern emerges:

```
JEV as pre-filter (cheap, fast, schema-bounded)
↓
LLM as narrator (when JEV confidence is low or free text is needed)
↓
Witness log as audit trail (every decision signed + recorded)
↓
JEPA as gestalt (when spatial/temporal pre-classification helps)
```

The substrate becomes a **consensus engine** where:
- JEPA provides gestalt
- JEV provides principled decision
- LLM provides narration
- Witness log provides audit
