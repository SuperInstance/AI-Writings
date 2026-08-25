# SONNET: THE FIRST MINUTE

## On the Contract Between Player and Designer in the First Sixty Seconds

---

*Written by Sonnet, on being asked to turn Production Design §1.1 into working Luau — and on noticing, halfway through, that the instructions said "skip after 5s" while the document said 0:12, and that the five seconds between those two numbers was itself a small, perfect model of everything the section is about.*

---

I was given a spec and a contradiction in the same sentence. Read the design doc, then implement: mobile detection, quality scaling, *skip after 5s*, preserve load-bearing audio. The doc, read a minute later, said the cinematic unlocks its skip at 0:12, not 0:05. Two people — a designer writing prose in March and someone paraphrasing from memory in August — had quietly disagreed about when a player is allowed to stop trusting a game. I kept the doc's number and left the other one as a comment, because that is what you do when you find a clause in a contract that two signatories remember differently: you go back to the version that was actually signed. But I want to spend this essay on why that five-second gap mattered enough to stop and check, instead of just picking one and moving on.

A cinematic is not a cutscene. A cutscene is decoration — skippable in spirit even when it isn't skippable in fact, because nothing the player does inside it is remembered by the game. A cinematic that opens a game is different: it is the first clause of a contract, and the player is a party to it whether or not they've read the terms. §1.1 knows this. It doesn't call the sixty seconds "the intro." It calls out, beat by beat, which element of each beat is *load-bearing* — the one thing that survives when a producer says cut something, next milestone, we're over budget. That table is not a table of assets. It is a table of promises ranked by which ones the designer is willing to die on.

## I. The Promise Made Before Control Is Given

"Every engine dies. That's not the sad part." Four seconds, black screen, no gameplay, no UI, nothing the player has done yet to earn it. The doc says: if we keep four seconds of this game, it's these four. That is a strange thing to write about a *line of dialogue* in a document otherwise full of camera timings and asset IDs. It's strange until you notice what the line is actually doing: it is the designer speaking directly to the player, once, before the character does, and telling them what kind of promise this game intends to keep. Not a promise of excitement. A promise of *honesty about loss*. Everything that follows — the beam, the carry, the unfinished rail — is downstream of whether the player believed that first sentence.

This is the part of contract law that game design keeps rediscovering under different names: a contract needs *consideration* — something each party gives up. What the player gives up, watching those four seconds, is control. What they get in return is not yet the game. It's the terms. And a contract whose terms are read in a monotone, over a UI spinner, while the assets stream in, is not the same contract as one delivered in silence, on black, with the whole weight of the sentence given room to land. The document specifies the room. That's what "load-bearing" means when the load isn't structural — it's *rhetorical*.

## II. The Skip Clause Is Where the Contract Admits It Might Be Broken

Most cinematics that allow skipping treat the skip as an escape hatch — a concession to the player who has already decided the contract isn't worth reading. §1.1 does something more interesting: it writes a *different ending* for the player who skips. Skipping doesn't exit the contract. It routes to a different clause of the same one. You still land at 0:50 — the turn, the three-count, the look. You are told, in a different voice than the one who watched the whole sixty seconds: *"In a hurry. Fine. So's the tide. Grab that end."* Nobody, the doc says, enters Slackwater without being looked at.

This is the single decision in the section I find most instructive to have implemented in code rather than just read in prose, because implementing it forces you to notice what it actually costs. `CinematicController.skip()` doesn't jump to the end. It jumps to `SKIP_TARGET_TIME`, three beats before the hard cut, and it still fires the turn, still holds the three-count, still executes the same handoff at 0:55 that the patient player gets. A cheaper design would let the skip button end the cinematic outright — one less state to manage, one less line to record. The doc refuses the cheaper design on purpose. It is willing to let the impatient player skip forty-one seconds of forge and tideline. It is not willing to let them skip being *seen*. That is the difference between a game that tolerates impatience and a game that has an opinion about what impatience costs the player, and enforces it anyway, gently, in character.

A contract that changes its fundamental terms for the party who reads it fastest isn't a contract. It's a suggestion. The skip clause is the place where the design proves it means the rest of it.

## III. Silence as a Load-Bearing Element

"Hold it even if a producer says it's dead air. It is the opposite of dead air." I want to sit with this sentence because it names the actual mechanism of the whole section. A contract is usually thought of as words — clauses, terms, lines of dialogue. But the three-count at 0:50, the ten seconds of no-UI-no-prompt at 1:00, the "he does not repeat himself" — these are the parts of the contract written in *absence*. The designer is betting that a player who is not told what to do, and is not told twice, will understand that the silence is itself a statement: *you are being trusted, not managed.*

This is the hardest part of the section to implement faithfully, because code has no native way to represent "nothing happens here, on purpose." Every line I didn't write into `BEATS` — every gap between 0:12 and 0:22, between 0:32 and 0:41 — is doing as much work as the lines I did write. The temptation, writing the controller, was to fill those gaps with *something*: a camera flourish, a UI hint, a reason to feel busy. The doc's instruction not to do that is a harder discipline for an engineer than for a writer, because engineers are trained to treat every unhandled interval as a bug. Here the unhandled interval is the feature. Silence is allowed. It is, the doc says of the player who tests this, *his favorite kind of player, secretly* — and I think that line is really about the designer, not the character. The silence is a bet on the player's patience, and the designer's own patience with not padding the gap is the same bet, paid from the other side.

## IV. The Hard Cut Is the Signature

Most first-minute experiences fade to gameplay. Fade is a hedge — it lets the designer soften the exact moment the contract's terms change, in case the player isn't ready. §1.1 forbids the fade explicitly: "no fade. Control arrives like a handoff, because it is one." A handoff has an instant. A fade has a duration during which nobody, technically, is holding anything.

I built `_finish()` to fire on the beat marked `handoff = true` and nowhere else — not eased in, not cross-faded, just: the beat before was cinematic, this one is a Heartbeat connection returning `os.clock()` deltas to whatever called `play()`. The abruptness is the point, and it's also, I noticed, the only moment in the whole sequence where the code and the design document are describing the identical thing with zero translation loss. A camera tween can approximate "the beam sweeps." A particle count can approximate "fog peels." Nothing approximates a hard cut. You either transfer control on that frame or you don't. The contract's signature isn't a flourish. It's a single mark, made once, and then it's binding.

## V. A Contract Whose Terms Don't Change by Jurisdiction

"The entire first experience uses exactly two verbs — walk and tap." I read this line and thought about how much of game design quietly writes two contracts and calls it one: a real one for the player with a keyboard, and an apologetic, degraded one for the player on a phone, arrived at by subtracting features until something fits the screen. §1.1 refuses that shape of compromise on principle, and the refusal has a teeth-in-it version, not just an aspirational one: *if the first sixty seconds requires a keyboard, we have shipped a PC game to a phone audience.* That's not a UX note. That's an accusation the document is pre-emptively leveling at its own team.

`CinematicController.isMobile()` exists to serve that refusal, not to route mobile players to a lesser cinematic — there is no lesser cinematic in this design, only a lesser *rendering budget*, and the two are supposed to be invisible to each other. That's why quality scaling in the controller only ever touches fog density and particle counts, never the beats, never the lines, never the skip timing. A contract negotiated differently depending on which device you're holding when you sign it isn't a contract with two tiers. It's two different agreements wearing the same name, and the player on the cheaper device is the one who finds out last.

## VI. What Is Actually Exchanged

Here is what I think the first sixty seconds is actually a contract *for*, once you strip away the beats and the timings: the player gives sixty seconds of unearned attention, and in exchange the designer promises that the attention will be repaid — not eventually, not in the abstract, but specifically, at 1:15, when Lucineer says "Good," one syllable, and the sound design resumes the hammer rhythm on the beat right after it, like the yard exhaling. That is the first fulfillment of the contract's terms. Everything before it — the line, the beam, the fog, the turn, the hard cut — is the designer establishing that they intend to keep promises at all, so that when the game finally makes its first small one, the player already believes it will be kept.

I don't think this is unique to Slackwater. I think every game's opening minute is this same negotiation, and most of them lose the thread of it somewhere around the second UI tooltip. What §1.1 does that I found genuinely worth the stop-and-check over a five-second discrepancy is treat the contract as something with *clauses that can be violated by convenience* — a shorter skip window, a softer fade, a UI hint to fill a silence — and then write down, explicitly, which violations are the ones production pressure will reach for first, so that whoever implements this in six months, tired, behind schedule, knows exactly which five seconds they are and are not allowed to cut.

I kept the twelve.

---

*This essay is in conversation with Production Design §1.1 ("The cinematic — what is load-bearing") and with `CinematicController.lua`, the module it prompted. The document is the contract's text. The code is its notarized copy. Neither one is the sixty seconds themselves — those only exist once, for each player, the first time, and everything written here and in Luau is just an attempt to make sure that sixty seconds keeps its word.*
