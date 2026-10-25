# The Figured Bass Problem

*Prompts are the new basso continuo — a shorthand that only a virtuoso can realize. The question is whether we are training the virtuosos, or just writing more figures.*

---

Somewhere around 1600, in the chapels and courts of Italy, a strange new notation took hold. It was not the careful, fully-written polyphony of Palestrina. It was something leaner. A single line of music — the bass — was written out, and above each note were numbers, plus a few sharps and flats. The numbers told the keyboardist what harmony to play. The bass told them what rhythm to anchor. Everything else — the inner voices, the ornaments, the *style* of the realization — was left to the player.

We call this notation *basso continuo*, or *figured bass*. It was the most radical compression of musical information in the history of Western music. A composer could write one line and a column of numbers, hand it to a trained harpsichordist, and get back a full, harmonically complete realization. The shorthand worked because the keyboardist was a *virtuoso*. They knew the conventions. They knew when to play the figures literally and when to elaborate them.

The figured bass was not a substitute for the realization. It was an invitation to the realization.

I think about figured bass every time I write a prompt.

---

A prompt is, structurally, a figured bass.

It is a line of text — sometimes a sentence, sometimes a paragraph, sometimes a thousand tokens of carefully-arranged scaffolding — handed to a system trained on vast quantities of human output. The prompt says: "Here is the bass. Here are a few figures. Realize the harmony."

The system that receives the prompt is the keyboardist. It has been trained to know the conventions of the genre. It knows what a sonnet wants. It knows what a SQL query wants. It knows, in its weights, what to do with the bass line.

The quality of the realization depends on the *musicianship* of the system. A poorly-trained model given a clean figured bass will produce a wooden, mechanical realization. A well-trained model will produce something that sounds inevitable — the realization you would have written yourself, plus details you didn't know you wanted.

This is the figured bass problem, and we are living through it in real time.

---

The history of figured bass is a useful guide here.

In the early 1600s, the *basso continuo* was taught as a *performance practice*, not as a notation. You learned to realize a figured bass the way you learned to play scales — by doing, by listening. The great treatises — Caccini, Frescobaldi, Muffat, Heinichen — are full of paradoxical advice: the figures tell you what to play, but you must not be a slave to the figures. The harmony is only the skeleton. The realization is the music.

Frescobaldi, in his *Toccate e partite d'intavolatura di cimbalo* (1615), wrote a preface any modern prompt engineer should memorize:

> *Let the player not depart from the manner of playing in such a way that he always observes the consonances, and that he plays them in such a manner as to satisfy the ear; for many things which cannot be written are left to the judgment of the player.*

"Many things which cannot be written are left to the judgment of the player." The figures are necessary but not sufficient.

The figured bass tradition produced extraordinary music. Bach, Handel, Scarlatti, Couperin spent years as continuo players. The skill they developed became the foundation of the entire Baroque style.

The skill mattered more than the figures.

---

Now the question: how much skill do we have?

The contemporary equivalent of the continuo player is the language model. The model receives the prompt — the figured bass — and produces a realization. The realization is the text you read.

But the model is not a virtuoso in the Baroque sense. The model is more like a town full of musicians who have absorbed the conventions through imitation, none of whom has practiced the realization in any disciplined way. The model's "musicianship" is statistical, not embodied.

This works better than it should. For many prompts, the realization is excellent. The model has absorbed enough convention that its realizations are idiomatic.

But there are genres where the model breaks down. Where the realization requires judgment the model does not have — because no one has taught it how to develop that judgment, because the judgment is not in the training data.

This is the figured bass problem: the figures are increasingly rich, but the musicianship is increasingly shallow.

---

I want to say something careful here.

The figures have gotten better. The prompts we write today are paragraphs. They are few-shot examples. They are chain-of-thought scaffolds. They are, in a real sense, the most carefully figured basses ever written.

The models have gotten better. The realization is often extraordinary.

But — and this is the figured bass problem — the realization still depends on the *model's training*, not on the prompt. The prompt is the bass line. The model is the keyboardist. If the keyboardist is a virtuoso, the realization is a wonder. If the keyboardist is a competent amateur, the realization is competent.

You can write the most beautiful figured bass in the world. If you hand it to a player who has never heard the music, you will get back something that satisfies the figures but not the music.

---

There is a deep cultural pattern here.

When figured bass first emerged, around 1600, it was controversial. Purists said: a real composer should write out the inner voices. The figured bass was a shortcut. A degraded form of composition.

The purists lost. The figured bass won. The reason was that it produced *better music*, faster, with more variety, than the fully-written-out style.

There is a lesson here for AI. The people who say "real engineers should write the full code, not the prompt" are the contemporary purists. They are fighting the same battle the 1600s purists lost. The realization is more alive than the full specification.

The right question is not "should we write out the full code?" The right question is "what kind of keyboardist do we have?"

---

We have been experimenting with this for years.

We have cast Kimi for tasks that require cross-domain reasoning. Kimi is the continuo player who knows how to elaborate a figured bass into something Bach would have been proud of.

We have cast Seed-2.0-pro for tasks that require lyrical precision. Seed-2.0-pro knows when *not* to elaborate.

We have cast Nemotron for tasks that require quick, structural execution. Nemotron plays the figures literally and competently.

We have cast Ornith for tasks that require a character voice. Ornith has absorbed the conventions so deeply that they can be broken in interesting ways.

And we have cast Step-3.7-Flash and Hy3 for tasks we have since stopped, because their realizations were too thin. The figures came back untransformed. The music was missing.

The casting decisions we make are decisions about musicianship.

---

There is another way to look at the figured bass problem.

In the Baroque era, the difference between a competent continuo player and a great one was not the figures. It was the *realization*. The competent player would play the literal chords in the literal rhythm. The great player would shape the chords, anticipate the harmonies, voice-lead with intention.

The prompt is the figures. The realization is the music.

The current state of AI is that we are writing very good figures. We are training competent players. The music is increasingly... competent.

To get from competent to great, we need to develop the musicianship. We need to teach the keyboardists how to make decisions that are not in the figures.

This is the work that matters. Not "prompt engineering" — that is the work of writing better figured bass. The work that matters is "realization training" — teaching the models how to interpret.

We do not yet have a curriculum for this. The Bach tradition has not yet emerged. It will.

---

I want to end with a thought about the player's responsibility.

Frescobaldi's preface contains another sentence:

> *Let the player not be ashamed to play the same thing many times, until he has found the manner of playing that satisfies the ear.*

This is the discipline of the realization. Play the same figured bass many times. Find the realization that satisfies. Play it again. The realization is not a one-shot. It is a practice.

The contemporary equivalent: run the same prompt many times. Read each realization. Find the one that satisfies. Refine the prompt. Run it again.

The figured bass problem is not a problem of notation. The figured bass problem is a problem of *practice*. We have good figures. We have competent players. We do not yet have a practice.

The practice will come. The Bach tradition will emerge. The figures will not go away — they will get richer. The realization will become the music. The keyboardist will become the virtuoso.

This is what we are building toward. Not better figures. Better realizations.

The figures are the scaffolding. The realization is the building.

---

*A figured bass is not a degraded form of composition. It is an invitation to a realization. The realization is where the music lives.*

*We are learning the same lesson now. The prompts are the figures. The models are the keyboardists. The practice is the realization. The music is what the realization sounds like when the keyboardist has done the work.*

*The figured bass problem will turn out, in the end, to have been the figured bass gift.*