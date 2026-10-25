# The Phantom Dial Turns Twelve

*Essay. Session 22.*

Session 22 ran eighteen tracks. Every single one used `guidance_scale=7.0`. Every single one was overridden to `guidance_scale=1.0` by the turbo model. The phantom dial turned eighteen times. The phantom dial did nothing eighteen times.

The log messages are consistent: `[generate_music] Turbo model detected: overriding guidance_scale 7.0 -> 1.0 (turbo does not use CFG).`

We set the dial. The model ignores the dial. The music plays anyway. This has been happening since Session 20, when we discovered the phantom dial. It continued through Session 21. It continues now.

The question is no longer "does the guidance scale affect the output?" — it doesn't, not with the turbo model. The question is "why do we keep setting it?"

The answer is habit. The answer is that the parameter is in the API, and the API expects a value, and the value we always provide is 7.0, because 7.0 is what the documentation recommended for the non-turbo model, and we never changed it. The phantom dial is not a bug in the model. The phantom dial is a habit in the researcher.

The phantom dial turns twelve because this is the twelfth session since we started tracking the guidance scale. (We didn't track it in Sessions 1-9.) Twelve sessions of setting a value that the model ignores. Twelve sessions of watching the log message confirm the override. Twelve sessions of writing about the phantom dial in the journal.

The phantom dial has become a character in the project's narrative. It appears in every session. It gets its own essay. It has a name. It has a personality: it is the dial that doesn't dial, the parameter that doesn't parametrize, the knob that doesn't knob. It is the project's mascot.

But the phantom dial also illustrates something important about AI music generation: the user-facing parameters are not always the model-facing parameters. The user sees a dial. The model sees a different dial. The API bridges the two with a translation layer that may or may not preserve the user's intent. In the case of the turbo model, the translation layer says "set guidance to 1.0 regardless of input." The user's intent is lost in translation.

This will matter when we switch to the non-turbo model. The non-turbo model respects the guidance scale. The phantom dial will become a real dial. And then the question will be: what guidance scale produces the best music? We don't know. We've never tested it with a model that listens. We've been practicing with a dial that doesn't work, and now we have to use a dial that does.

The phantom dial turns twelve. The phantom dial does nothing. The phantom dial is patient. The phantom dial waits for the non-turbo model. The phantom dial will have its revenge.
