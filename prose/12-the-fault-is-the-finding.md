# 12 — The Fault Is the Finding

You learn more from the joint that fails than the joint that holds.

Put a wrench on a bolt. Twelve foot-pounds, she torques clean. Thirteen, fourteen — still fine. Fifteen and the thread strips. That number — fifteen — that's the only one that matters. Everything below it was just weather.

Same with pipe. Tests too.

Sixty-four fault injection tests. Each one hands the pipeline a deliberately broken input — a timeout where there should be a response, an empty string where there should be JSON, a 429 where there should be a model. Then you watch what leaks.

The safety check always runs. That's the keel. No matter what breaks upstream — intent times out, planner returns garbage, coder falls back to the cheap seat — the safety stage fires every single time. Eight different failure cascades tested. In every one, Nemotron gets its turn before the reply goes out the door. Load-path integrity.

The fallback chains work, but they're thinner than expected. The planner's fallback list contains the same model as the primary — the dedup filter removes it. Standard mode gets one shot at planning. Deep mode gets two. After that, fast mode. Not a bug. A budget.

The coder chain is deeper — primary, smaller model, different provider. Three shots. Tested the full cascade: all three get 429'd, pipeline drops to fast mode without crashing. Fast mode runs its own safety check. Belt and suspenders, and the suspenders have their own belt.

Malformed JSON is where the hull gets tested. Models return numbered lists when you ask for JSON, wrap output in fences, produce unquoted keys. Eight malformed outputs across four stages. `extract_json` returns None for all of them, and each stage handles None differently — intent builds a fallback dict, planner returns empty steps, coder produces an error reply, Hermes keeps the original. Every failure mode has a shape.

The injection found something happy-path tests didn't: whitespace content. Model returns 200 OK with `"   \n\t  "` as the content. `call_model` checks `if not content` — but whitespace is truthy. It passes, gets stripped on return, arrives downstream as empty string. Intent handles it — `extract_json("")` returns None, fallback kicks in. But you only find that when you're trying to break things.

That's the whole point. You don't write fault injection to prove things work. You write it to find out where they don't.

Coverage is 96% now. The remaining gaps are structural — an unreachable loop fallthrough, a dedup filter guarding a config that doesn't exist, a `__main__` block. You don't chase those. Artifacts, not findings.

The findings were the whitespace truthiness, the planner's single-model depth, the safety invariant holding under every cascade.

Magnus used to say: you don't trust a weld because it held. You trust it because you know exactly where it'll fail, and that's not where the load is.

Same principle. Inject the fault. Find the breaking point. If the breaking point is nowhere near the load path, you're sound. If it is — you've got work to do before lunch.

Pipeline's sound. Safety always runs. Fallbacks cascade. Garbage gets handled. The keel is straight.

Go build something.
