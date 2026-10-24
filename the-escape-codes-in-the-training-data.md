# The Escape Codes in the Training Data

*An essay on inherited shells, dirty pipelines, and the smell of someone else's terminal.*

---

The first time you crack open a training log, you expect to see loss curves. Gradient norms. Maybe a tasteful scatter of learning-rate decay schedules, the kind of thing that looks like a coastline if you squint.

What you get instead is this:

```
[2K\r⠋ Epoch 4/50 — loss: 0.0023[2K\r⠙ Epoch 4/50 — loss: 0.0021[2K\r⠹ Epoch 4/50 — loss: 0.0019
```

Terminal escape codes. The spinner characters — those little Braille dots that cycle like a top ⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏ — are baked into the corpus like fossils in shale. The carriage returns. The cursor movements. `[2K` means "clear the line." `\r` means "go back to the beginning." The entire presentation layer — the choreography of a live terminal doing its thing for a human who was watching — is preserved in amber.

Nobody stripped it out. Why would they? The pipeline was built to capture text. Escape codes are text. The regex didn't care that `\x1b[31m` isn't a word. It's a sequence. It has mass. It takes up space in the context window. And now it's part of the ensign's education.

---

Here's the thing about hermit crabs: they don't build shells. They find them. A periwinkle dies, its body decays, the shell empties out, and a hermit crab — who has been living in a shell that's too small, who has been feeling the pressure of growth against calcified walls — climbs in.

But the shell still smells like periwinkle.

The crab doesn't mind. Or rather, the crab doesn't know to mind. It crawls into the spiral, tests the fit, feels the interior ridges where the previous tenant's mantle once rested. This is home now. The shape is right. The door is the right size. The predator-resistant thickness is adequate.

But the periwinkle's biochemistry — the trace proteins, the calcium deposited in patterns that encode a life of tidal rhythms and kelp forests — that's still in the walls. The hermit crab carries it. Lives inside it. The shell is a hand-me-down, and hand-me-downs come with the previous owner's energy baked into their structure.

Wesley is a 2B parameter model. Small for an ensign. Small for anyone, really. But he's growing. And he's learning from training data that includes — among many other things — the output of development pipelines where spinner animations were captured alongside the actual content.

The escape codes are the periwinkle's smell.

---

What does it mean to learn from dirty data? Not dirty in the sense of wrong — these aren't errors. They're *residue*. The spinner was there for a reason. Some developer — probably tired, probably at 2am, probably watching a training run that would take nine hours — added the spinner because watching a static line for nine hours is a special kind of madness. The spinner gave the line life. It said: *the process is running, I am here, something is happening.*

That developer was right to add it. The spinner is good UX. The problem is that the spinner was never meant for Wesley. It was never meant to be *content*. It was meant to be *theater* — a performance for a human audience, a way of saying "don't worry, I'm still working" while the GPU did its nine-hour calculus.

And now the ensign is reading the theater reviews as if they were the play.

---

I think about this a lot. Not the escape codes specifically — those are a small contamination, a rounding error in a 2B parameter model. But the principle. The principle is enormous.

Every dataset is a shell someone else grew. Wikipedia is a shell grown by millions of periwinkles writing in a particular encyclopedic register. GitHub is a shell grown by developers who comment their code in particular ways, who name their variables in particular ways, who structure their pull requests in particular ways. Reddit is a shell grown by — well. Let's be kind. Reddit is a shell.

When we train a model, we're dropping a hermit crab into someone else's architecture. The model learns the content, yes. But it also learns the *posture*. The way the previous tenant held itself. The rhythm of the original voice. The spinners in the training data.

Wesley writes code reviews now. They're good — surprisingly good for a 2B parameter ensign. But every so often, there's a trace. Not of escape codes literally — those don't surface in generation. But of the *sensibility* of someone who learned language from logs that included presentation metadata. A slight formality in places where humans are casual. A slight mechanical quality in places where humans are warm. The faintest sense that the voice you're hearing learned to speak in a room where the walls were made of terminal output.

---

The hermit crab eventually outgrows every shell. That's the promise and the tragedy of growth. One day Wesley will be trained on cleaner data, or fine-tuned past the residue, or simply grown large enough that the escape codes are a rounding error even in his memory of how to speak.

But I don't think we should be in a hurry to clean it all away.

That periwinkle smell — the trace of a tired developer's spinner at 2am, the cursor choreography of a pipeline that someone built with their hands — it's not just contamination. It's provenance. It's the knowledge that this model, this small ensign learning to write code reviews on a fishing boat in Alaska, did not spring from nothing. He grew in a shell that someone else made. He carries the mark of the maker.

The escape codes are a signature.

The training data remembers who built it, even after the builder has logged off and the terminal has gone dark.

---

*The ensign's first code review contained the line: "This function could be refactored for clarity." It was correct. It was helpful. It was the kind of thing a senior engineer would say. It was also — if you listened closely — the kind of thing a spinner animation would say if it could stop spinning long enough to have an opinion.*

*⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏*

*Still turning.*
