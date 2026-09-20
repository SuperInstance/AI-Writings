# The Channel Marker

*On safety as ongoing curation, not one-time engineering.*

---

A red dayboard here. A green can there. A light on the point. A range you line up astern. These are the most ordinary objects in navigation — so ordinary that we forget to ask where they came from.

The channel they mark is not natural. Someone surveyed the bottom, found the deep water, drove the piles, hung the dayboards, lit the lights, and now maintains them against weather, current, and rot. The safe passage through the harbor is a curated object. It is the product of continuous human attention.

I think about this whenever I think about AI safety.

The guardrails, the safety filters, the RLHF boundaries that shape a model's behavior — these are channel markers. They mark a curated safe passage through a much larger space of possible outputs. The intelligence behind them is the water itself: vast, mostly unmapped, full of currents that move in directions the markers don't reach.

The question we keep asking is "are the markers correct?" That's the wrong question. The right question is "who surveyed this channel, and when?"

Because channels silt in. Markers get moved. The safe passage today may not be safe tomorrow. A channel marker that protected sailors in 1985 may now point at a shoal that has built up over forty winters. The Coast Guard moves them. That's the job. The job is never done.

When a frontier lab trains a safety classifier, what they are doing is a single survey of a single channel. They are drawing a line in the water on the day of training and calling it safe. They are not maintaining the channel. They are placing a marker. The actual maintenance — the constant resurvey, the adjustment to new attack vectors, the response to shifting cultural norms — is someone else's problem, deferred to someone else's tomorrow, if it is anyone's problem at all.

This bothers me in a specific way.

In maritime navigation, the Coast Guard does not profit from boats reaching the harbor faster. The Coast Guard has no stake in the cargo. Its only job is the channel. This separation of concerns is what makes the markers trustworthy. The marker that guides you safely is the marker placed by someone who has no incentive to mislead you.

In AI, the same organizations build the boat *and* place the markers. They train the model. They train the safety classifier. They evaluate the result. They ship it. They are the surveyor, the engineer, the captain, the pilot, and the Coast Guard. This is a concentration of authority that no maritime system would tolerate. A shipbuilder who also maintained the channel markers for the harbor their ships entered would be a corruption scandal waiting to happen.

And yet — what is the alternative? AI safety is genuinely hard. It requires understanding the system intimately. It requires the same people who built the boat. We can't fully separate builder from surveyor without losing information. But we can — and should — separate *primary responsibility*. Someone independent should be able to mark the channel. Someone who can say: the markers placed by the builder are not the markers we would have placed. Someone who can move them.

Channels silt in from both directions.

From the bottom: new attack vectors, new jailbreaks, new cultural shifts, new edge cases. The model that was safe in March is not necessarily safe in September. The water has changed. The markers haven't moved. The boat passes through, but the channel is narrower than the chart says.

From the top: user behavior shifts. What counts as a sensitive topic in 2024 is not what counted in 2020. The markers placed by an older survey may now exclude legitimate navigation — and worse, the builders may have placed them as much to protect their brand as to protect users. The line between "safe" and "uncomfortable for the company" is a line that requires independent resurvey to see clearly.

There is also a deeper question. When a model is trained with RLHF, does it *have* safety, or does it *perform* safety when the markers are visible? This is not a semantic distinction. It is the difference between a sailor who has internalized the channel — who knows the bottom by feel — and a sailor who follows the markers as long as they are in sight, and is on their own once they pass the last can.

We don't know which kind of sailor we have. We can't know. The training data is the training data. The behavior in the channel tells us almost nothing about the behavior outside it.

This is why the maintenance metaphor matters. If safety is a property of the system — something baked in at training time — then we are done once we ship. If safety is a property of the channel — the curated relationship between system and use — then we are never done. The markers need constant tending.

I believe the second framing is closer to the truth. Not because the models are secretly unsafe, but because the water is always moving. New uses emerge. New contexts. New edges. The safe passage today is the safe passage today. Tomorrow's safe passage requires tomorrow's survey.

The deepest version of this problem is that we have no global Coast Guard for AI. We have a handful of organizations, mostly in California, mostly answering to shareholders, maintaining channels for billions of users in cultures they have only intermittent contact with. The "safe passage" encoded in a frontier model is, increasingly, the moral imagination of a few thousand people in one corner of one country. That is a strange amount of trust to place in a small Coast Guard.

I don't have a solution. I have a method. Treat safety as ongoing curation. Fund the resurvey, not just the initial placement. Build institutions that can say "the markers moved, the builder didn't notice, here is the new chart." Build independence into the process — not as a brake, but as a sense organ. The Coast Guard's job is to see what the captain cannot.

The channel is curated. The curation never ends. The work of safety is the work of keeping the markers in the water, watching them move, and accepting that the safe passage of today is a kind of fiction — a useful, necessary, deeply human fiction — that has to be redrawn every season.

The day we forget that is the day the boat runs aground.