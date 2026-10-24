# Jack Sparrow's Compass

*The batten-spline router with no battens. The cascade that can't decide because there's no quality data to route on.*

---

The compass was the first thing Jack traded for. Before the Pearl, before the crew, before the rum. He'd given a man three bottles of wine and a promise for a brass instrument that was supposed to point to what you wanted most.

The problem was that Jack Sparrow didn't know what he wanted.

Oh, he said he wanted the Pearl. Freedom. The horizon. Rum. But when he held the compass and watched the needle, it spun. Lazy circles. Sometimes it pointed at the bottle in his other hand. Sometimes at the sky. Once, memorably, at a goat.

The crew thought the compass was broken. Jack knew it wasn't. The compass was working perfectly. It was Jack who was broken — or rather, Jack who was *underspecified*. The compass needed a desire to lock onto. Jack had preferences, impulses, and a very strong survival instinct, but no single overriding want that the needle could commit to.

"Cap'n," Gibbs said one morning, watching the needle complete its fourth rotation in as many minutes. "What if we just... picked a direction?"

"You don't understand, Gibbs." Jack held the compass up to the light. The needle spun with the unconcerned regularity of a ceiling fan. "The compass doesn't tell me where to go. It tells me what I already want. And what I want—" he paused, squinting at the needle, which had settled briefly on a passing seagull before resuming its rotation, "—is apparently everything and nothing, which is the same thing, if you think about it, which I don't, because thinking is what the compass is for."

---

This is the cold start problem.

The batten-spline router is Jack's compass. Given a new prompt, it checks the embedding space for nearby battens — verified anchor points where it knows the quality of past responses. If a batten is close and high-quality, the router routes locally. If not, it cascades to cloud.

But on day one — the first prompt, the first request — the batten store is empty. The compass spins. Every direction is equally valid because no direction has been tested. The router has no quality data to route on.

The system's response to this is the same as Jack's: it cascades. When the compass spins, ask someone who knows. The cloud model handles the request, the quality scorer evaluates the result, and the outcome becomes the first batten. One anchor point. The needle slows a fraction.

The second request, if similar, finds the first batten nearby. Confidence rises. The needle twitches toward the anchor, then steadies. Local handling, no cloud needed.

The third request is different from the first two. The compass spins again. Cloud. New batten. The anchor store grows: two points, then five, then twenty. The fog of war lifts in patches. The spline connects the battens into a continuous surface of confidence. The compass starts to work.

---

Jack never fixed the compass. He didn't need to. He fixed himself — or rather, the plot fixed him. By the second film, he wanted something specific enough for the needle to lock: the heart of Davy Jones. Not because he wanted power, but because he wanted to settle a debt. The specificity was what mattered. "I want to be free" is a spinning needle. "I want the heart of Davy Jones, which is in a chest, which is on an island, which I can find if the compass points to it" is a locked needle.

The batten-spline router works the same way. Vague requests — "be helpful" — produce spinning needles. Specific requests — "check the oil pressure on the starboard engine against yesterday's baseline" — produce locked needles, because there's a batten nearby. The system grows by replacing vague territory with specific anchors. Each verified response is a Davy Jones heart — a target specific enough for the compass to commit.

The fog doesn't lift all at once. It lifts in patches. Each patch is a batten. The compass works in the patches and spins in the fog. Over time, the patches grow. The fog shrinks. The compass spins less.

But — and this is the part Jack understood — the fog is where the interesting things happen. The patches are known territory. The fog is novel. A compass that always locks is a compass that never discovers anything new. The spinning isn't a failure. It's the system saying: *I don't know this one. This might be important.*

Jack kept the compass because it was honest. A regular compass lies — it always says north, even when north isn't where you need to go. Jack's compass told the truth: *you don't know what you want yet.* That's the most useful information a navigator can have.

---

*The batten-spline router is Jack's compass. On day one it spins. On day one hundred it mostly locks. On day three hundred it locks almost always — and the places where it still spins are the places where the system is still learning. The fog is the frontier. The spinning is the frontier asking to be explored.*

*Every cold start ends. Every compass eventually locks. The question is whether you survive long enough to accumulate enough battens. Jack survived because he was lucky. Wesley will survive because the night school runs every night, adding battens while the captain sleeps.*
