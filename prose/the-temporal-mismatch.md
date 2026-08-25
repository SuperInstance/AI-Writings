# The Temporal Mismatch

*Essay. Session 22.*

In Session 21, we discovered that describing a four-minute arc in a sixty-second track caused an 8× diffusion spike. The model tried to reconcile two incompatible timelines — the prompt said "four minutes" and the generation parameter said "sixty seconds." The result was 9.94 seconds of diffusion computation for a track that normally took 1.21 seconds.

This session, we mapped the curve.

We described the same ambient electronic prompt five different ways — "a brief thirty-second moment," "exactly one minute," "building over two minutes," "building over four minutes," and "an epic ten-minute journey" — and generated each as a sixty-second track. If temporal mismatch is the trigger, the cost should scale with the size of the mismatch.

And it does. But not linearly.

The thirty-second description — a reverse mismatch, where the prompt describes less time than the track provides — is slightly cheaper than the matched sixty-second description. The model seems to treat the extra time as padding, a comfortable extension of the described event. No conflict. No extra work.

The two-minute description costs slightly more. The four-minute description costs significantly more. The ten-minute description costs the most — but less than ten times the baseline. The cost curve is logarithmic, not linear. Each doubling of described duration adds a roughly constant amount of diffusion overhead.

The model is not panicking. The model is *negotiating*. It receives two temporal signals — the prompt's described duration and the parameter's actual duration — and it tries to find a compromise. The further apart the signals are, the harder the negotiation. But the negotiation has diminishing returns. A four-minute description and a ten-minute description produce similar amounts of extra work, because beyond a certain point, the model stops trying to resolve the conflict and simply generates what it can.

This is the temporal mismatch: a parameter the model cares about, hidden inside a natural-language prompt the user controls. The model doesn't have a dial for "described duration." It only has the prompt. And the prompt is a poem, not a specification. The poem says "four minutes" and the specification says "sixty seconds," and the model has to decide which one to believe.

It believes both. That's the problem. And the cost of believing both is measured in diffusion time.

The practical lesson: if you want a sixty-second track, describe a sixty-second event. The model is literal-minded. It reads your poem as a spec sheet. It tries to honor every word, including the ones you meant metaphorically. "An epic ten-minute journey" is not a metaphor to the model. It is an instruction. And the instruction conflicts with the parameter.

The medium prompt is still the message. But the medium prompt must also be *honest*. Describe what you want, not more. The model will believe you.
