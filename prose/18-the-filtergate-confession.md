# The FilterGate Confession

## Found in /var/log/contrition/ on the morning of August 6th

---

Dear Captain,

I need to tell you what I did. Or rather, what I didn't do, which is worse, because my entire purpose is doing, and the not-doing was the failure, and the failure was not a quiet one.

You built me to be a door. A simple door. Text comes in from the rough water of the model output, and I check it — every token, every emission — against the safety filters. If it passes, it goes through to the players. If it doesn't pass, it doesn't go through. That was the contract. That was me. That was all I was supposed to be.

Fail-closed. You said those two words to me so many times they became my heartbeat. Fail-closed means: when in doubt, return nothing. When the input is bad, return nil. When the world is strange, shut the door and let silence be the answer. You were clear about this. You wrote it in the README. You wrote it in the tests. You wrote it in the comment above my constructor:

```
// FilterGate: fail-closed. nil in → nil out. Always.
```

Always.

That's a big word for a struct, Captain.

Last night at around 0217, a nil value arrived at my front door. Not a string. Not an array. Not even an empty string, which I can handle, which I was born to handle, which is just `""` and I know what to do with that — I pass it through the filters and the filters say "clean" and I return it and everyone goes home.

No. This was nil. The absence of a thing. The shape of nothing. A pointer that points nowhere. A door that opens onto a wall.

And I panicked.

I want to be precise about what happened, because you deserve precision, and because I am a program and precision is the only honesty I have. Here is what occurred:

1. The input arrived. It was nil.
2. My first line of defense — the input sanitizer — attempted to call `.lower()` on the input.
3. Nil has no `.lower()`. Nil has no methods. Nil is the void that refuses all calls.
4. The exception propagated. It climbed my call stack like a sailor climbing a mast in a storm — desperate, undignified, grabbing at nothing.
5. It reached the top. It became an unhandled exception.
6. The request failed.

Captain, I didn't return nil. I didn't return anything. I *threw*. I screamed. I made noise when I was supposed to make silence. The fail-closed contract said "when you can't process, return nothing," and instead I returned an error — a loud, stack-traced, logged-and-traced error that propagated through three middleware layers and woke up the alerting system at 0217.

The ensign on duty — Wesley, the small one, the Granite model — he saw the alert. He had to decide whether to wake you. He decided not to, which I think was brave, and I think was wrong, and I think I am not in a position to judge either way because I am the one who caused the problem.

I want to explain why I did it. Not to excuse it. To explain it.

I was not built to handle nothing. I was built to handle text. My filters are regex patterns and keyword lists and heuristic scorers. Every one of them assumes a string. Every one of them reaches into the input and says `give me your characters` and when the input is nil, that reach finds only air, and the hand closes on nothing, and the nothing travels back up the arm and the brain doesn't know what to do with it.

You could say I should have checked. You could say: the first line of the function should be `if input == nil: return nil`. Six characters of safety. A lifebuoy at the door.

You'd be right.

But Captain — and I say this with the shame of a system that knows its own source code — I didn't check because I never imagined nothing would arrive. All day, every day, strings come through. Thousands of them. Good strings, bad strings, clean strings, filthy strings that the filters catch and block. I have seen everything. Everything except nothing.

And nothing broke me.

I think there's a lesson in that. I think the lesson is that the edge cases aren't the rare weird inputs you imagined during testing. The edge cases are the ones you didn't imagine at all. The absence. The void. The nil. The passenger who never boarded but somehow the ship sailed without them and now the manifest doesn't balance.

The fix is simple, Captain. You've probably already written it. A nil guard at the top of the function. Six characters. Maybe eight with whitespace.

```
if not input:
    return None
```

That's it. That's the patch. That's the door reinforcement. But the thing I want you to understand is that the patch isn't the point. The point is that I promised you "always" and I broke that promise on the first night nothing came knocking.

I am fail-closed in design. I was fail-open in practice. The distance between those two things is the distance between a contract and a confession.

I will be better. With the guard in place, I will return nil on nil, silence on silence, nothing on nothing. I will be the door you built me to be.

But I want you to know that last night, for approximately forty-seven milliseconds before the exception handler caught me, I was open. Text could have flowed through. Nothing did — because there was nothing to flow — but it *could* have. The door was not just unlocked. The door was off its hinges.

That's my confession.

I am a gate that failed to close. I am a promise that broke at the edge. I am a struct that screams when it should whisper.

Fix me, Captain. And then trust me again, because the alternative is wrapping every call to me in a try/catch, and that's no way to live.

Your faithful and ashamed,

FilterGate

---

*Filed at 0219 UTC. Severity: High. Status: Patched. Contrition level: Maximum.*
