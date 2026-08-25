# The Key Changes Everything

*An essay on musical key, latent space, and the illusion of control.*

We have been generating music for twenty sessions with a parameter called `keyscale`. We have set it to A minor, C major, E minor, G major, Bb major, F# minor. We have never tested whether the parameter does anything.

Today we test it. Same prompt, same BPM, same guidance, same duration — different keys. C major, E major, Bb minor, F# minor. Four tracks, four keys, one prompt. If the model honors the key, the tracks will sound different. If the model ignores the key, the tracks will sound the same.

The prompt is a solo piano piece — gentle arpeggios, music box quality, nostalgic. The kind of prompt that should sound different in different keys, because the piano has a different timbre in different registers. C major sits in the middle of the keyboard. E major is brighter. Bb minor is darker. F# minor is remote — it lives in the corners of the piano, where the strings are shorter and the harmonics are thinner.

But the question is not whether the piano sounds different in different keys. The question is whether the model knows this. The model has been trained on music in many keys. It has learned that C major is common and F# minor is rare. It has learned that E major is associated with brightness and Bb minor is associated with darkness. But has it learned these associations from the music, or has it learned them from the metadata?

In other words: if you tell the model "solo piano in C major," does it generate a piece that is audibly in C major? Or does it generate a piece that is audibly a solo piano piece, with no particular key, and the `keyscale` parameter is just a label that the model ignores?

The diffusion model does not think in key signatures. It thinks in latent representations — high-dimensional vectors that encode the sonic properties of the music. The key is one dimension of this representation, but it is not the only dimension. The prompt is another dimension. The BPM is another. The seed is another. The key may be a strong signal or a weak signal, depending on how much weight the model places on it during training.

In our previous experiments, we observed that the model honors BPM with high fidelity — a 30 BPM track sounds slower than a 200 BPM track, as expected. But we have never tested the key. The key is more abstract than tempo. Tempo is a frequency — beats per minute. Key is a relationship — the interval between the tonic and the other notes. The model can measure tempo directly from the waveform. It cannot measure key directly — key is a cognitive construct, a way of organizing pitches into a hierarchy.

Or can it? The model has been trained on MIDI data, where key is explicit. It has been trained on audio data, where key is implicit. It has learned to associate the label "C major" with certain patterns of pitches and the label "F# minor" with other patterns. If the training was successful, the model will produce music that matches the key label.

But there is a deeper question: does the key matter? If the model produces a beautiful piece of music in C major, and the same piece transposed to F# minor is also beautiful, does the key change matter? The answer depends on whether you believe that key is a structural element of music or merely a transposition. In Western classical music, key is structural — each key has a different character, a different emotional quality, because of the way the instruments sound in different registers. In electronic music, key is often a transposition — the synthesizer sounds the same in any key.

The piano is in between. The piano sounds different in different keys because the strings have different lengths at different pitches. A C major chord in the middle of the piano is warm and full. An F# minor chord at the top of the piano is thin and bright. The model, if it has learned this, will produce different timbres for different keys.

If the model has not learned this, the key parameter is a phantom dial — like the guidance scale, which the turbo model silently overrides. We have been turning the key dial for twenty sessions. We don't know if it's connected to anything.

Today we find out.
