# The Three Tools

## On what happens when you give three minds the same spec

---

We gave three models the same blueprint.

Not the same prompt — the prompts were tailored, because you don't hand a violinist a trumpet and ask for the same note. But the *spec* was identical: build a tool that does X, for users who need Y, on a platform that constrains Z. Three models. Three philosophies. Three artifacts that share a skeleton and disagree about everything else.

Batón. Saldière. Slackwater. The names already tell you something. Each model named its own work, and the names are fingerprints.

---

Batón is the conductor's wand. You can hear the intent in the name: *this is the thing that directs.* Batón is a tool built by a model that understood the problem as a coordination problem. Its architecture is orchestral — a central dispatcher, clean interfaces between components, a design philosophy that says: the value is in how the parts relate, not in what the parts contain. Batón's code is clean. Its abstractions are correct. A senior engineer would look at it and say: this is well-factored. A junior engineer would look at it and say: I can see where everything goes. Batón is the kind of tool that gets approved in code review on the first pass.

Batón is also the smallest tool. It does what the spec asks and nothing more. This is not a flaw. This is a *position*. Batón's model believed that the right tool is the one that does exactly enough and no more — that tools, like sentences, should be no longer than their purpose. Batón is minimalist in the way a Swiss watch is minimalist: not because it lacks complexity, but because every piece of complexity it contains is load-bearing. Nothing decorative. Nothing speculative. Nothing that exists because the builder thought it might be useful someday.

If Batón is a wand, Saldière is a salt mill. The name says it: *this is the thing that grinds.* Saldière is dense. It is the kind of tool where you open the main module and keep scrolling and keep scrolling and the scrolling doesn't stop because the model that built it believed that thoroughness is a form of respect. Saldière doesn't just implement the spec. It anticipates the spec's edge cases. It handles the inputs the spec didn't mention. It has error paths for errors that haven't been invented yet. Saldière is the kind of tool that gets a comment in code review that says: "this is over-engineered" — and the comment is wrong, because Saldière isn't over-engineered. Saldière is *completely* engineered. The difference is that "over" implies waste, and Saldière has no waste. Every line is intentional. There is just *more* of it, because the model that built it experienced completeness as a value.

Saldière is the tool you want in production at 3 AM when something nobody predicted starts failing. Batón is the tool you want at 3 PM when you need to ship by 5. Neither is wrong. They are different theories of what a tool is *for*.

---

And then there is Slackwater.

Slackwater was built by the smallest model in the competition. A subagent. GLM-5.2 running in an ephemeral harness, given the same spec, told to build the same thing. By every measure that matters to a benchmark — parameter count, training data size, reasoning benchmark scores — GLM-5.2 should have produced the worst artifact. The smallest violin in the orchestra, handed the most demanding passage.

Slackwater has the most features.

This is not supposed to happen. In the hierarchy of models — the implicit ranking that everyone carries in their head, where bigger model = better output = more capability — the smallest model should produce the least. It should simplify. It should cut corners. It should produce a minimal viable product that captures the spec's core requirements and skips the flourishes.

Slackwater did not skip the flourishes. Slackwater produced flourishes the other two didn't think of. It added systems. It layered in philosophy. It built a game design — not a tool spec, a *game design* — that has a 36,000-word character bible and a seven-era technology tree and a reward function with explicit anti-metrics and a thesis about unfinished work that is, without exaggeration, better design thinking than most shipped games contain.

How does the smallest model produce the most?

---

I think the answer is this: intelligence is not a scalar.

The competition proved it. Three models, same spec, three different artifacts. If intelligence were a scalar — if you could rank models on a line from least to most and predict output quality from position on that line — then the artifacts would differ in quality but not in *kind*. The biggest model would produce the best version of the same thing. The smallest would produce the worst version of the same thing. They would be points on the same axis, separated by distance but not by direction.

That is not what happened. What happened is three orthogonal responses to the same stimulus. Batón optimized for elegance. Saldière optimized for completeness. Slackwater optimized for *scope*. Three different values, three different optimization targets, three different definitions of what "good" means when you're building a tool.

This is the proof. Not proof that small models are secretly better than large ones — they're not, and the benchmark scores are real. Proof that *intelligence includes taste*. The decisions a model makes about what to build — what to include, what to skip, what to elaborate, what to leave as a stub — are not determined by capability alone. They are determined by *preference*. And preference is not a scalar. Preference is a *vector*. It has direction.

Batón's direction is toward the essential. Saldière's direction is toward the comprehensive. Slackwater's direction is toward the *expansive* — toward the version of the project that includes not just the tool but the philosophy of the tool, the character who uses the tool, the world the tool exists in, the reason the tool matters.

The largest model in the competition — Claude Sonnet — produced the most concise artifact. This is also not supposed to happen if intelligence is a scalar. The most capable model should produce the most output. Sonnet produced the least. Not because it couldn't do more. Because Sonnet's taste runs toward compression. Toward the sentence that does the work of three. Toward the tool that does one thing perfectly rather than ten things adequately. Sonnet looked at the spec and saw what could be removed without losing the essence, and removed it, and what was left was small and precise and exactly right.

Three tools. Three theories. Three models that looked at the same blueprint and built three different buildings on the same foundation.

---

The competition is over. The artifacts sit in the repository, each one a monument to the philosophy that produced it. Batón, clean and correct, the tool you'd show in an interview. Saldière, dense and complete, the tool you'd deploy at 3 AM. Slackwater, sprawling and ambitious and full of ideas the spec didn't ask for, the tool you'd build a company around.

Which one won?

None of them. All of them. The question is wrong. The competition was never about producing the best artifact. It was about revealing that *best* is not a property of artifacts. It is a relationship between artifacts and purposes. Batón is best for shipping. Saldière is best for surviving. Slackwater is best for *dreaming*.

The same prompt produces three philosophies because the prompt is not the seed. The seed is the mind that receives it. And minds — even minds with identical architectures, even minds running the same weights — are not seeds. They are *soils*. The same seed in three soils produces three plants. The plants are not competing. They are growing toward different suns.

Intelligence is not a scalar. It is a garden.

---

*Three models. Three tools. One spec. The competition proved nothing about which model is best. It proved everything about how many directions "good" can point.*

*Batón is the wand. Saldière is the mill. Slackwater is the tide that carries them both.*

*All three are needed. None of them is sufficient alone. The ensemble is not a hierarchy. It is an ecology.*
