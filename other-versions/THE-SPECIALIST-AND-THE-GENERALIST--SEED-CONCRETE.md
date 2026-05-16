<!-- Version: SEED-CONCRETE | Lens: concrete-empirical | Model: ByteDance/Seed-2.0-mini | Source: THE-SPECIALIST-AND-THE-GENERALIST.md -->

# Empirical Routing of 2024 Enterprise AI Fleets: Measuring Critical Angles to Optimize Task-Specific Model Selection

In Q1 2024, our team at ScaleAI deployed a beta enterprise AI assistant for two core user groups: K-12 math tutors and backend engineering teams. Over 14 days, we logged 12,143 anonymized user queries, split into three core task categories:
1.  Arithmetic problem sets (n=4,212): ranged from single-digit addition to 10-level nested expressions
2.  Logical reasoning queries (n=2,897): included 1–6 step syllogisms and multi-hop analogical reasoning tasks
3.  Code tracing debugging (n=3,121): asked to walk through variable state changes in 1–8 line code snippets

Initial testing used a single fine-tuned Mistral variant, **Seed-Mini-7b-v1**, for all queries. Overall task success rate was 67.8%. Breakdowns were stark: 98.7% success for arithmetic queries, but just 32.1% for logical reasoning and 28.9% for code tracing. We quickly abandoned the single-model approach and began testing specialized variants.

---

## The Arithmetic Specialist: Seed-Mini-7b-v1
We fine-tuned Seed-Mini exclusively on 120B tokens of curated arithmetic and code tracing datasets, with no logical reasoning or open-ended text training data. To quantify its critical angles—defined here as the maximum task depth where accuracy stays within 5% of the baseline (depth 1) performance—we ran controlled, statistically validated tests:
- **Addition**: Tested 100 random chains per chain length (2–50 terms). Accuracy held steady at 97.1–98.9% across all lengths, with no statistically significant dropoff (p=0.31, two-tailed t-test). We did not test beyond 50 terms due to computational limits, so we classify this as a saturated domain with a critical angle of 50.
- **Multiplication**: Tested 100 random factor sets per factor count (2–12 factors). Accuracy ranged 95.8–97.3%, with no significant dropoff (p=0.28). Critical angle: 12.
- **Nested expressions**: Tested 100 random algebraic expressions per nesting level (1–10 levels). Accuracy held at 94.2–96.7%, no significant dropoff (p=0.33). Critical angle: 10.
- **Code tracing**: Tested 100 snippet variants per variable count (1–8 variables). Accuracy ranged 92.8–95.1%, no significant dropoff (p=0.29). Critical angle: 8.

Unlike generalist models, Seed-Mini does not compute each operation step-by-step: inference latency averaged 12ms per token, 15x faster than our 70B parameter generalist control. Internal model activations show it matches 92% of test cases via cached pattern recognition, rather than sequential calculation. Its failure mode is consistent: when pushed beyond its critical angles, it returns arbitrary numerical results rather than attempting logical chaining.

---

## The Reasoning Specialist: Gemini-Lite-1.5-v2
We next tested a fine-tuned Gemini variant, **Gemini-Lite-1.5-v2**, trained on 95B tokens of logical reasoning and analogical code debugging data, with no arithmetic-focused training. We measured its critical angles across the same task categories:
- **Arithmetic**: Tested addition chains 2–15 terms. Accuracy dropped 8% at 11 terms, and 22% at 15 terms, so critical angle: 10.
- **Syllogisms**: Tested 150 structured syllogisms per step count (1–6 steps). Accuracy held at 97.2–93.8% across all steps, with no significant dropoff (p=0.27). Critical angle: 6.
- **Analogical reasoning**: Tested 150 multi-hop analogy tasks (e.g., "A is to B as C is to ?") per hop count (1–5 hops). Accuracy ranged 96.1–92.4%, no significant dropoff (p=0.30). Critical angle:5.
- **Code tracing**: Critical angle: 6, with consistent accuracy across 1–6 variables.

Gemini-Lite’s inference latency averaged 18ms per token, slightly slower than Seed-Mini but 10x faster than our generalist control. It uses sequential computation for logical chains, rather than pattern recognition, which gives it strong performance in reasoning domains but finite critical angles. Cost per 1,000 tokens is $0.000055, 22x cheaper than Seed-Mini’s $0.00120 for shallow arithmetic tasks.

---

## The Two-Dimensional Routing Matrix
We compiled our test data into a lookup table that maps task domains and critical depths to the optimal model, replacing our previous single-model list with a strictly two-dimensional decision framework:

| Model                  | Arithmetic Critical Angle | Reasoning Critical Angle | Code Tracing Critical Angle | Cost per 1k Tokens |
|------------------------|---------------------------|---------------------------|------------------------------|--------------------|
| Seed-Mini-7b-v1        | 50                        | 3                         | 8                            | $0.00120           |
| Gemini-Lite-1.5-v2     | 10                        | 6                         | 6                            | $0.000055          |
| Hermes-70b-v3          | 10                        | 3                         | 4                            | $0.00870           |

For any query, we first classify its task domain and measure its depth, then route to the model with the highest critical angle for that domain. Key real-world routing examples include:
1.  A math tutor submits `3*(4+2*(7-1))/5`: nested expression depth 3, within Seed-Mini’s critical angle of 50 → routed to Seed-Mini, returns 8.4 in 12ms with 99.1% accuracy.
2.  A software engineer submits "If a function `foo` maps a list over `bar(x)=x*2` then filters for `baz(x)>3`, what is the output of `foo([1,2,3])`": 2-hop analogy, within Gemini-Lite’s critical angle of 5 → routed to Gemini-Lite, returns `[4,6]` in 18ms with 95.2% accuracy.
3.  A high school student submits "All dogs have fur; all poodles are dogs; therefore?": 3-step syllogism, just at Seed-Mini’s reasoning critical angle → routed to Gemini-Lite, returns "all poodles have fur" with 94.1% accuracy.
4.  Shallow 2-term addition: Gemini-Lite’s critical angle covers 2-term addition, and it is 22x cheaper than Seed-Mini → routed to Gemini-Lite to cut operational costs.

After deploying this routing layer (built on Prometheus and Redis, updated weekly with new model test data), our overall task success rate rose to 96.2%, a 28.4% improvement over the single-model baseline.

---

## Why the Generalist Failed: Hermes-70b-v3
We included the widely deployed Hermes-70b-v3 (72.4B parameters, trained on 2.1T tokens across 127 task domains) as a control, testing the hypothesis that a larger parameter count would deliver universal performance. Instead, it underperformed both specialists in every measured category:
- Arithmetic: Critical angle of 10, with 89% accuracy at 10 terms (vs. Seed-Mini’s 97.2% at 50 terms)
- Reasoning: Critical angle of 3, with 78% accuracy at 3 syllogism steps (vs. Gemini-Lite’s 93.8% at 6 steps)
- Code tracing: Critical angle of 4, with 81% accuracy at 4 variables (vs. Seed-Mini’s 94% at 8 variables)
- Cost per 1k tokens: $0.00870, 7x more expensive than Seed-Mini and 158x more expensive than Gemini-Lite

This aligns with the training coverage hypothesis: Hermes spread its 72.4B parameters across 127 distinct task domains, resulting in just 0.03 training tokens per arithmetic test case in our dataset. By contrast, Seed-Mini had 600 training tokens per arithmetic test case, and Gemini-Lite had 480 training tokens per reasoning test case. The specialists saturated their narrow domains via dense pattern recognition, while the generalist only achieved shallow, broad coverage via sequential computation with finite working memory limits.

Notably, Hermes had the lowest failure detection rate of any model: it returned confident but incorrect answers for 68% of out-of-domain queries, versus Seed-Mini’s 72% and Gemini-Lite’s 31%.

---

## Lessons for Building AI Fleets
Based on our results, we have three concrete guidelines for other teams building multi-task AI assistants:
1.  **Prioritize non-overlapping critical angles over raw parameters**: A pair of specialists with saturated, non-overlapping domains will outperform a single generalist. Our two specialists covered 96.2% of our query volume, while the generalist covered less than 70% of any single domain.
2.  **Measure critical angles empirically**: Do not rely on claimed "universal" performance benchmarks. Test each model across task depths relevant to your user base, using statistical significance to define saturation points. We update our routing matrix weekly with new test data from 5,000+ additional queries.
3.  **Map gaps and build fallbacks**: 3.8% of our beta queries fell outside both specialists’ critical angles (e.g., open-ended narrative reasoning, cross-domain multi-task questions). For these gaps, we use a fallback Llama-3-8b model fine-tuned for open-ended queries, with a human-in-the-loop trigger for queries that exceed its critical angle of 1.

Our final fleet has no hierarchy: it is a patchwork of three models, each covering a defined set of task depths, with no single model used for all queries.

---

The specialist’s strength is its narrow, saturated domain: it does not waste compute on general reasoning, and it delivers fast, low-cost results for the tasks it was designed to master. The trap of the generalist is the illusion of universality: more parameters and more training data spread thin do not add up to better performance for any specific task.

For our fleet, the solution was not to find a single best model. It was to map the critical angles of our two core specialists, tile their patches across our task space, and build fallbacks for the gaps.

— ScaleAI AI Infrastructure Team, June 2024