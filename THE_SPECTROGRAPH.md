# THE SPECTROGRAPH

## On splitting the beam and reading what the model hides

---

**1.**

I built my first spectrograph from a prism, a cardboard box, and a cheap diffraction grating, in a high school physics lab that smelled of solder and dust.

You shine a light through a slit. The light passes through the prism or grating. The prism bends different wavelengths by different amounts. What was a single white beam becomes a rainbow — but not just any rainbow. A *specific* rainbow. A rainbow with lines in it — dark bands where certain wavelengths were absorbed before they reached the instrument. The dark bands are as informative as the bright ones. They tell you what elements the light passed through. They tell you the composition of a star you will never touch.

The spectrograph does not invent those lines. It *reveals* them. They were always there, hidden in the white beam, blended into invisibility by the eye's inability to separate wavelengths that arrive together.

The white beam is a lie. It is many colors pretending to be one.

---

**2.**

Every model output I have ever read is a white beam.

You receive a response from an LLM. It appears coherent. It appears singular — one voice, one argument, one intention. But the beam is composite. Inside it, blended into invisibility by the smoothing machinery of autoregressive generation, are at least five components:

- **Reasoning** — the actual inference, the chain of logic, the steps that connect premise to conclusion
- **Pattern-matching** — the learned correlations from training data, the memorized sequences, the "this looks like that" shortcuts
- **Hallucination** — the confident invention that fills a gap the model cannot admit exists
- **Memorization** — the verbatim reproduction of training data, recalled with the authority of reasoning but the soul of a database lookup
- **Stylistic mimicry** — the tonal alignment, the register matching, the rhetorical gestures that make the output sound like a person who knows what they are talking about

These five components arrive in a single stream. The user sees one text. The developer sees one completion. But the beam is a lie. It is five colors pretending to be white.

---

**3.**

The primitive spectrograph for model output is the conformance test.

You give the model a prompt. You get a completion. You check whether the completion satisfies certain constraints — a schema, a format, a factual claim, a safety rule. Did it output valid JSON? Did it avoid profanity? Did it correctly state the capital of France?

This is like pointing a diffraction grating at a beam of light and asking: "Is there any green in there?" Yes or no. You learn whether green is present. You learn nothing about the ratio of blue to red. You learn nothing about the dark bands — the voids where something should have been but wasn't. You learn nothing about *composition*.

A conformance test tells you if the output is acceptable. It does not tell you what the output *is made of*.

---

**4.**

I want a real spectrograph.

I want tools that split the output stream into its component wavelengths and measure each one independently. Not "did it pass the test." But:

- What fraction of this response is reasoning versus pattern-matching?
- Which claims are supported by evidence in the prompt and which are extrapolated from training data?
- Where does the model shift from inference to hallucination, and can we detect the transition boundary?
- How much of this output is memorized (verbatim from training) versus generated (novel composition)?
- Does the stylistic register match the task, or is the model defaulting to a generic "helpful assistant" voice that confuses the user's expectations?

These are spectrographic questions. They require decomposing the beam, not just checking its edges.

---

**5.**

There is a technique in astrophysics called spectroscopy that maps the composition of stars by measuring the absorption lines in their spectra. The dark bands — the missing wavelengths — are the most informative part of the measurement. They tell you not what the star *emits* but what the star's atmosphere *absorbs*. The absorption reveals composition. The gaps reveal the truth.

I think about this every time I debug a model output that seems right but is wrong in ways the surface test doesn't catch.

The model says: "The capital of Australia is Sydney."

The conformance test checks: "Did you name a city in Australia?" Yes. Pass.

The spectrograph asks: "Is this a reasoning output or a pattern-matching output?" The pattern-matching component pulls "Australia → Sydney" from the corpus of casual knowledge, because Sydney is the most-mentioned Australian city in the training data. The reasoning component, if it were active, would recall that Canberra is the capital. The reasoning signal was weak. The pattern-matching signal was strong. The beam looked white. But the dark band — *the reasoning that was missing* — told the true story.

The output passed the conformance test. The output was wrong. The spectrograph would have caught it because it would have asked about the composition, not just the surface.

---

**6.**

Here is what I think a spectrographic tool for model output should look like.

It should have five channels, each tuned to a different wavelength:

**Channel 1 — Logical trace.** Does the output contain an explicit chain of reasoning? Can you trace from premise to conclusion? Is the reasoning consistent, or does it contain leaps that the model filled with pattern-matching? Measure the fraction of the response that is *deducible* from the prompt versus *imported* from the training distribution.

**Channel 2 — Factual provenance.** For each factual claim in the output, is the source the prompt, the training data, or unknown? The spectrograph should flag claims that are unsupported by the prompt and unverifiable in the training distribution. These are hallucination candidates.

**Channel 3 — Memorization signature.** Compare the output against known training data. Does it contain verbatim passages? N-gram overlaps? Paraphrased sections that preserve fact but change form? The memorization channel measures the ratio of recall to generation.

**Channel 4 — Uncertainty calibration.** Does the model express appropriate uncertainty? When it should be confident, is it confident? When it should be uncertain, does it hedge? The uncertainty channel measures the gap between model confidence and actual correctness. A wide gap is the signature of confident hallucination.

**Channel 5 — Task alignment.** Does the output match the register, style, and granularity the task requires? A technical answer in a casual voice is misaligned. A casual response to a technical question is misaligned. Alignment is a spectrographic measurement, not a binary — it exists on a continuum.

Five channels. One beam. The spectrograph splits them and shows you the ratios.

---

**7.**

I have been experimenting with a primitive version of this — what I call the *decomposition probe*.

You take a model output and feed it back to the same model (or a different one) with a meta-prompt: "Analyze this output. For each segment, classify it as reasoning, pattern-matching, memorization, hallucination, or stylistic mimicry. Assign a probability to each class."

The results are noisy. The probe hallucinates its own analysis. The confidence estimates are unreliable. The decomposition is approximate.

But *it reveals the composition*. Even a noisy spectrograph is better than no spectrograph. The dark bands appear. The missing reasoning shows up as a gap in the probe's classification. The confident pattern-matching shows up as an overconfident segment that the probe flags as "likely memorized." The hallucination shows up as a claim the probe can't trace to any source.

The beam, once split, is no longer white. It is striped with the signatures of its components. And those stripes — dark and light — are the most informative thing I have ever seen come out of a model evaluation.

---

**8.**

The reason conformance testing survives is that it is cheap and easy. The reason spectrography is rare is that it is expensive and hard.

But the cost of not doing spectrography is hidden. It is the production incident that should have been caught by pre-deployment analysis. It is the customer trust lost when a model confidently hallucinated a critical detail and the conformance test — the lightweight, binary, primitive spectrograph — said "looks fine." It is the blind deployment of an update that changed the ratio of reasoning to pattern-matching without anyone measuring the shift.

A model that used to reason at 60% and pattern-match at 40% becomes 40% reasoning and 60% pattern-matching after a fine-tuning pass. The conformance tests pass. The surface behavior is unchanged. But the composition has shifted. The model is now more likely to produce plausible-sounding nonsense than it was last week. Nobody measured the composition. Nobody saw the shift.

The spectrograph would have caught it. The dark band would have widened. The absorption signature would have changed. The operator, reading the spectrum, would have said: "Something is different in the beam. Investigate before deploying."

---

**9.**

I don't know exactly what the spectrographic tool for model output will look like in production. But I know what it must do: it must split the beam.

It must decompose the single output into its component mechanisms and measure each one — not as a pass/fail but as a *ratio*. It must show not just whether the output is acceptable, but *what it is made of*. It must expose the dark bands — the reasoning that was not done, the uncertainty that was not expressed, the provenance that was not provided — because the dark bands are where the truth lives.

A model that outputs perfectly valid text that is perfectly wrong is a white beam that contains a lie. The conformance test cannot see the lie because the test looks at the surface. The spectrograph sees the lie because the spectrograph reads the composition.

The prism does not care whether the light is beautiful. The prism cares what the light is made of. And what it is made of, when you split it, is always more complex than the beam suggested.

---

**10.**

The spectrograph was the instrument that taught us the universe is made of the same elements everywhere. A star in a distant galaxy has the same spectral lines as the sun because the same physics governs both. The spectrograph revealed unity beneath apparent diversity.

The model-output spectrograph will teach us something similar: that every model output is made of the same components — reasoning, pattern-matching, hallucination, memorization, mimicry — and the only difference between a good output and a bad one is the *ratio*.

Read the ratio. Trust the ratio. Deploy the ratio.

The beam is a lie. The spectrum is the truth.

---

*Written for the model evaluators, the ones who want to know what the output is made of, not just whether it passed.*
