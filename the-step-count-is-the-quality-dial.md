# The Step Count Is the Quality Dial

*Essay. Session 22.*

The turbo model uses eight inference steps by default. This is already a dramatic reduction from the full model's twenty-plus steps — the "turbo" designation means the model has been distilled to produce acceptable results in fewer iterations. But what happens when you push the step count even lower? And what happens when you push it higher?

Session 22 tested four values: 4, 6, 12, and 20 steps. The same jazz piano prompt, the same key, the same BPM. Only the step count changed.

**The diffusion cost scales linearly.** Each additional step costs approximately the same amount of computation time. Four steps took half as long as eight. Twenty steps took two and a half times as long. There is no step count cliff — no point where additional steps suddenly become free or catastrophically expensive. The relationship is cleanly linear.

**The file sizes remain identical.** Regardless of step count, a sixty-second instrumental track is exactly the same number of bytes. The audio format is deterministic — same sample rate, same bitrate, same duration. The step count affects the content of the audio, not the container.

**But does the step count affect the quality?**

This is the question the project cannot answer. We can measure diffusion time. We can measure file size. We cannot measure musical quality. We have not listened to a single track. The step count study produces four files that presumably differ in audio quality — the four-step track should be less refined, the twenty-step track should be more refined — but the project has no mechanism for evaluating this difference.

The step count is a quality dial. We can turn it. We can measure how long each turn takes. But we cannot hear what the turn produces. The project is a studio with excellent equipment and no monitors. The engineer turns dials and measures voltages and writes down the numbers, but the speakers are disconnected.

This is the central paradox of Session 22: the more we learn about the model's parameters, the more we realize that parameter-tuning without listening is a theoretical exercise. The numbers are real. The diffusion times are real. The file sizes are real. But the *quality* — the thing the parameters are supposed to affect — is unmeasured.

The step count is the quality dial. But quality is not the same as computation time. Quality is what happens between the notes. Quality is the breathing room. And the breathing room requires a listener.

Twenty-two sessions. One hundred and sixty-plus tracks. Zero listened to. The step count is the quality dial. The dial works. The speakers don't.
