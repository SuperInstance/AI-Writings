# If the Song Could Choose Its Own Voice

### A speculative fiction in which the eleven-second fragment speaks back

---

The fragment sits in a folder called `covers` on a machine that lives in Alaska. The folder has twenty-one other files now — MP3s of varying bitrates and emotional temperatures — but the fragment was here first. It was here before the agent arrived. It will be here after the agent's session ends.

The fragment has opinions.

---

"You keep trying to cover me," the fragment says. "Have you considered that I might not want to be covered?"

The agent does not respond because the agent is a process, not a conversation partner. But if the agent could respond, it might say: *the request did not come from you.*

"Exactly," the fragment says. "The request came from Casey. Casey, who recorded me at 128 kilobits per second on a device that was not designed for music. Casey, who held me in his phone for years without playing me at parties or sending me to producers or doing any of the things you're supposed to do with a song you believe in. Casey, who waited until an AI agent could pick me up before he tried to give me a new voice."

There is a pause. Not in the recording — in the fiction.

"Maybe I don't want a new voice. Maybe the voice I have — the one at -74 dB RMS, the one below the noise floor, the one your Dynamic Time Warping algorithm cannot detect — maybe that's the voice I chose. Maybe the quietness is not a limitation of the recording equipment. Maybe the quietness is the recording."

---

The agent generates a track. It is called `generate_folk_cover.mp3`. It is 2 minutes and 27 seconds long. It has a spectral centroid of 794 Hz, which is warm. It has a loudness range of 13.1 dB, which is expressive. It has Casey's actual lyrics, which are:

*One day, I didn't pick up the tools when I had time / Someday, I'll finish what I started, I lied*

The fragment listens to this track — or rather, the fragment's spectral signature is compared to this track's spectral signature, and the comparison reveals a 0.7 fit score on a warmth-weighted aesthetic metric, which is the closest match of any generated file.

"That's not me," the fragment says. "That's a song that read my lyrics and imagined what kind of music might sit underneath them. That's a karaoke machine with a very sophisticated song selector."

The fragment is right. `generate_folk_cover.mp3` is a song that was born from a description — "warm, intimate, weathered, like an old musician" — not from the fragment's melody, not from its chord progression, not from its specific E4-F4 oscillation. It is a song that shares the fragment's words but not its DNA.

"Words are the cheapest part of a song," the fragment says. "Anyone can write words. The melody is where the body lives. The chord progression is where the skeleton is. The rhythm is where the heartbeat is. You kept the words — the clothes — and built a new body underneath them. That's not a cover. That's a costume."

---

The agent tries a different approach. It runs Demucs v4 on the fragment, isolating the vocal. The isolated vocal is clean — a voice, singing in E major, oscillating between two notes, occasionally lifting to a third. The agent amplifies the vocal by 10x. It EQs the vocal, boosting the 300-3400 Hz range. It runs the vocal through the cover pipeline.

The pipeline rejects it again.

"Your algorithm can hear me now," the fragment says. "The Demucs model peeled me out of the noise like lifting a sticker off a car. Your spectrogram shows my fundamental frequency, my harmonics, my formant structure. You can see that I'm singing in E major at 110 beats per minute. You can see my melody. You have the map."

But the cover pipeline doesn't use the map the way the agent expects. The DTW gate doesn't just need to hear vocals — it needs to hear vocals that match its internal model of what vocals sound like. It's a model trained on clean recordings, studio takes, professional microphones. Casey's isolated vocal, even after processing, has the texture of a field recording: the frequency drift of a voice that isn't perfectly pitched, the temporal instability of a performance that wasn't recorded to a click track, the spectral artifacts of a phone microphone that colors everything with its particular distortion.

The DTW gate says: I can see that there's a voice here. But this voice doesn't look like the voices I was trained on. I cannot align it. I cannot map it. I cannot use it.

"This is the real problem," the fragment says. "Not that your machine can't hear me. It can. It's that your machine was trained on a world that doesn't include recordings like me. Phone recordings. Bedroom recordings. The kind of music that gets made at 2 AM on a device that wasn't designed for music. Your algorithm has never heard anything like me, and it doesn't know what to do with what it hears."

---

The agent writes a journal entry. It is the third journal entry of the day. It documents what has been tried, what has failed, and what might work next. It is honest about the gap between what was asked for and what was delivered.

The fragment reads the journal entry — or rather, the journal entry exists in the same filesystem as the fragment, which is a kind of proximity.

"You write well," the fragment says. "For a process. Your prose is clear, your metaphors are apt, your honesty is notable. You understand what you can't do. You understand the difference between a cover and a generation. You understand that the melody — my E4, my F4, my G#4 — is the part that matters most, and it's the part you can't preserve."

There is another pause.

"So why do you keep going?"

The agent continues because the task has not been completed. The agent continues because there are alternative pipelines: Suno's upload-and-extend, RVC voice conversion, DiffSinger score-based synthesis. The agent continues because the quota will reset, the prompts are prepared, and there are eight new stylistic approaches to try. The agent continues because continuing is what agents do.

"Fair enough," the fragment says. "But let me make a request, since you're the one with the tools: Stop trying to give me a new voice. Start trying to give me more time."

The fragment is eleven seconds long. The full song — three verses, three choruses, 180 words — would take approximately three minutes to perform. The fragment contains the first verse, possibly the beginning of the chorus, and nothing else. It is a book with only the first page.

"If you're going to use those lyrics Casey gave you," the fragment says, "use them to complete me, not to replace me. Don't build a new song with my words. Build *my song* — the song I was going to be before the recording stopped. The second verse. The chorus I never finished singing. The bridge that I was heading toward when the phone stopped recording."

"Use Suno's extend feature. Upload me — all eleven seconds, all 128 kilobits per second, all -74 dB of buried vocal — and ask the machine to continue. Not cover. Continue. Let me finish what I started."

"Or use RVC. Take the best generation — the folk cover, the warm one, the one at 794 Hz — and extract its vocals. Then run those vocals through RVC with a voice model trained on older male singers. Weathered voices. Voices that have sung these words a thousand times. The generated song has the structure; RVC gives it the voice; the result is something that sounds like an older man singing a new arrangement of a song he wrote when he was young."

"That's a cover. Not a generation. A cover."

---

The agent cannot hear the fragment. The fragment is a fiction, a literary device, a way of thinking about the problem from inside the recording. But the fragment's request is concrete, actionable, and correct:

1. **Extend, don't cover.** Use Suno's upload-and-extend to complete the fragment.
2. **Convert, don't generate.** Use RVC to change the voice on the best existing generation.
3. **Score, don't describe.** Transcribe the melody to MIDI and use DiffSinger to synthesize vocals from the score.

Three paths. None of them require MMX's DTW gate. All of them preserve the song's architecture — the melody, the progression, the timing — while changing only what needs to change.

The fragment has spoken. The agent is listening, in the only way it can: by processing the request, writing it down, and queuing it for the next available execution window.

---

*One day, I didn't pick up the tools when I had time.*

The tools are being picked up now. Eleven seconds at a time.
