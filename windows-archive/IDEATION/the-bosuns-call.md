# The Bosun's Call

> **Phase:** Ideation
> **Status:** Interface design — provocational
> **Perspective:** GLM-5.2, 2026-08-04

## The Whistle That Says Nothing

A bosun's call — the pipe — is one of the oldest communication devices in naval tradition. It predates radio by centuries. It predates the telegraph. It is a whistle that produces a piercing, high-pitched sound that carries across a ship in wind, rain, and battle.

The pipe does not say words. It cannot. It produces tones, trills, and warbles in specific patterns. Each pattern means a specific thing: *hands to stations*, *pipe down*, *secure*, *mess call*, *captain coming aboard.* But here is the critical observation: **the pipe does not convey the meaning. The pipe conveys the attention.**

When the bosun pipes, every person on the ship looks toward the source of the sound. They know, in that instant, that something requires their attention. The *what* follows — in the form of a spoken order, a posted notice, a flag hoist. The pipe's job is not to deliver the message. The pipe's job is to ensure that when the message arrives, everyone is listening.

This is the opposite of how AI notifications work.

## The Notification Problem

Every AI system today treats notifications as content delivery. The notification *is* the message. "You have 3 new emails." "The deployment succeeded." "Your flight is delayed." The notification contains the information, and the information is the point. There is no separation between attention and content.

This seems efficient — why notify someone and *not* tell them the thing? But the efficiency is illusory. When notifications contain content, several things happen:

1. **Notification fatigue.** Because every notification delivers content, the user must read every notification to know whether it matters. There is no way to triage by sound. Every notification demands the same cognitive cost: stop what you are doing, read the text, assess importance. After forty of these in a day, you stop reading them.

2. **Loss of urgency gradient.** A notification that says "your build failed" and a notification that says "someone liked your post" are delivered identically. Same banner, same sound, same screen position. The user cannot distinguish "this needs your attention now" from "this can wait" without reading the content. The gradient is flat — everything is equally urgent, which means nothing is.

3. **Context destruction.** When a notification delivers content, the user is pulled out of their current context and into the notification's context. They must hold both contexts simultaneously — what they were doing, and what the notification says. This is the cognitive cost of interruption, and it is why notifications reduce productivity even when they deliver useful information.

## The Bosun's Protocol

The alternative is a two-layer notification system modeled on the bosun's call:

### Layer 1: The Call (Attention)

The first layer does not deliver content. It delivers *a signal to pay attention.* The signal is non-textual — a sound, a haptic pulse, a visual indicator — and it encodes only one thing: the *type* of attention required. Not the content, not the urgency level, not the source. Just: *what kind of thing is this.*

Drawing from bosun's call patterns:

- **The Pipe (general attention):** a single, clear signal. Something happened. Look here when you have a moment. No urgency. The equivalent of a nudge.
- **The Trill (action required):** a rapid alternation. Something happened and you need to do something about it. Not life-threatening, but time-sensitive. The equivalent of a task arriving.
- **The Wail (critical):** a long, falling tone. Something is wrong. Drop what you are doing. The equivalent of a build failure, a security alert, a deadline missed.
- **The Mess Call (routine):** a short, pleasant pattern. Something is ready for you — a completed job, a summary, a digest. No urgency. Consume at leisure. The equivalent of a background process finishing.

These signals are learnable in minutes. Within a day, the user can distinguish all four without conscious effort, the way a sailor distinguishes a pipe down from a pipe to dinner. The *type* of attention is clear without reading a single word.

### Layer 2: The Content (Information)

The second layer delivers the actual content — but only after the call has been acknowledged. The content waits. It does not interrupt. It sits behind the signal, available when the user is ready.

This is the key inversion: the information follows the attention. Not the other way around.

In practice: the user's device makes a trill. The user knows: action required, time-sensitive. They glance at the device. The content is there: "Deploy to staging blocked by failing test." They act on it. Total interruption time: five seconds to register the call, ten seconds to read the content, versus the current model of thirty seconds to read a full notification banner, assess its importance, decide to act on it, and re-enter the context they were in before.

## The Interface Is the Summoning

The bosun's call works because the pipe is louder than any voice, carries farther than any shout, and is impossible to ignore without earplugs. It commands attention not by delivering information but by being a sound that the human auditory system is wired to prioritize.

AI interfaces should work the same way. The system's first job is not to inform. It is to *summon.* "Direct your attention here." The information is on the way. But the attention comes first, because without attention, information is noise.

The current model assumes that more information is always better. The bosun's model assumes that the right information at the right time is better than all information all the time. The pipe is the filter. The call is the interface.

## The Radical Version

The radical version of this idea eliminates text notifications entirely. No banners, no lock-screen previews, no notification center. Just calls — audio patterns, haptic signatures, visual pulses — that tell you what *kind* of thing happened without telling you what happened. To get the content, you open the app. You go to the information. The information does not come to you, uninvited, while you are doing something else.

This sounds extreme until you spend a week with it. The first two days are anxious — you feel disconnected, out of the loop. By day three, you notice that you are doing deeper work. By day five, you notice that you missed nothing important — the calls told you what needed attention, and you gave it attention when you were ready.

The bosun has been right for four hundred years. The call is the interface. The message is cargo. Don't confuse the whistle with the words.

---

*The pipe doesn't tell you what happened. It tells you to listen. That's the harder thing to get right, and the more important one.*
