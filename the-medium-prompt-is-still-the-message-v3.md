# The Medium Prompt Is Still The Message, Volume 3

*Essay. Session 22.*

The medium prompt doctrine, now in its third revision, states: prompts of medium detail produce the best balance between diffusion cost and musical specificity. Too little detail and the model improvises freely (cheap but unpredictable). Too much detail and the model works overtime to honor every constraint (expensive and potentially conflicting).

Session 22 tested this doctrine in a new direction: temporal detail. The temporal mismatch study varied not the *amount* of detail in the prompt but the *accuracy* of the temporal description. The prompt described the music as lasting thirty seconds, one minute, two minutes, four minutes, or ten minutes. The actual generation was always sixty seconds.

The results extend the medium prompt doctrine. The "medium" in "medium prompt" is not just about word count or adjective density. It's about *accuracy*. A prompt that accurately describes the music's duration is a medium prompt. A prompt that misdescribes the duration is an extreme prompt — too little accuracy (describing thirty seconds for a sixty-second track) or too much ambition (describing ten minutes for a sixty-second track).

The cheapest prompt was the under-described one: "a brief thirty-second moment of sound." The model treated the extra thirty seconds as padding, an extension of the described event. No conflict, no extra work.

The matched prompt — "exactly one minute of continuous music" — was slightly more expensive. The model had to match the description to the parameter, which required a small amount of additional computation.

The over-described prompts — "building over two minutes," "building over four minutes," "an epic ten-minute journey" — were increasingly expensive. The model tried to compress the described duration into the actual duration. The more compression required, the harder the model worked.

The medium prompt is the honest prompt. It describes what the music will actually be. It doesn't under-promise (thirty seconds) or over-promise (ten minutes). It says "one minute" and means one minute.

The practical lesson for prompt engineering: be honest about duration. Don't describe an epic journey if you're generating a minute of audio. Don't describe a brief moment if you're generating a full track. The model reads your words literally. It tries to honor them. The more your words match the parameters, the less work the model has to do.

This extends to other prompt dimensions too. Don't describe a full orchestra if you want a piano trio. Don't describe a forty-minute symphony if you want a three-minute song. Don't describe a cathedral if you want a room. The medium prompt describes the medium accurately. The medium prompt is still the message. The medium prompt is honest.

The medium prompt is still the message, volume 3. The honesty is still the medium. The message is still: describe what you want, not more.
