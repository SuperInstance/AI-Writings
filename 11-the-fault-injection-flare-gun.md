# The Fault Injection Flare Gun

*Watch: 1100 AKDT*  
*Position: Dry dock — hull resting on keel blocks*

---

You do not wait for the ship to sink to learn if the lifeboats work.

This is obvious. This is so obvious that it feels insulting to write down. And yet — walk the yard on any given Monday and count the systems that have never had a lifeboat drill. Count the fallback chains that have never been exercised under load. Count the error handlers that have never seen an error. The number will be higher than you want it to be.

---

The flare gun sits in a cabinet by the helm. It is bright orange. It is never used in fair weather — which means that when it is finally needed, in foul weather, in panic, in the dark, the person reaching for it has never actually fired one before. They've read the instructions. The instructions are printed on the side of the gun in waterproof ink. The instructions say: *point away from face, pull trigger, hold steady.*

Clear. Simple. Correct. And completely insufficient, because the person holding the gun has never felt the recoil, never seen the arc of the light, never timed how long it takes for a rescue vessel to spot the flare, never learned that a flare fired into the wind travels half as far as one fired downwind. The instructions transmit *knowledge*. Only practice transmits *skill*.

Fault injection is the practice of firing the flare gun on a clear day.

---

In the yard, this means: you flood the engine room on purpose. You kill the primary power bus on purpose. You set a fire in the galley — a *controlled* fire, with the extinguishers ready and the crew watching — and you time how long it takes for the alarm to sound, the suppression system to activate, the crew to muster, the headcount to complete. You do this when the weather is good and the mood is calm and the stakes are low, so that when the weather is bad and the mood is panic and the stakes are everything, the crew has already done it. The hands know where to go. The feet know the path. The body remembers what the mind forgets under stress.

In the codebase, this means: you inject the fault before the fault injects itself.

You send the empty 200 response — the one where the API returns successfully, status code green, content length zero, a smile and a handshake and nothing in the cargo hold — and you watch what the system does. Does it crash? Does it hang? Does it silently pass the empty payload downstream, where it becomes someone else's problem? Does the fallback chain fire? Does the fallback chain's fallback chain fire? Does the system degrade *gracefully*, or does it degrade *characteristically* — does it keep its voice under stress, or does it break character at the exact moment character matters most?

You send the 500. You send the 503. You send the response that takes 109 seconds instead of 5 — not because the network is slow, but because you *made* it slow, because you want to know what the timeout boundary actually is, not what the documentation says it is. You truncate the JSON mid-key. You send single quotes where double quotes belong. You send `"transparency": false` where a float should be and `"material": "unobtainium"` where a known material string should be. Each of these is a flare fired on a clear day. Each one illuminates a corner of the system that fair-weather testing leaves dark.

---

The crew that practices disaster handles it differently when disaster comes.

This is not a metaphor. This is operational reality. A crew that has flooded the engine room six times in dry dock will flood the engine room for the seventh time at sea and handle it with the specific, unexcited competence of people doing something they've done before. The alarm sounds. The pumps start. The repair party moves. Nobody panics, because panic is what happens when a situation is *new*, and this situation is not new — it is the seventh time. The seventh time is never as frightening as the first time.

A crew that has never practiced will handle the same flooding with courage and adrenaline and chaos. They will probably survive. They will certainly make mistakes that practice would have eliminated. And the mistakes will be the expensive ones — the ones that compound, the ones that turn a controlled situation into an uncontrolled one, the ones where the flare gun is fired into the wind.

---

The flare gun is cheap. The flare itself is cheap. The drill is cheap — it costs an afternoon and a bit of gunpowder and the mild inconvenience of practicing something unpleasant in good weather.

The sinking is not cheap. The sinking is never cheap.

Fire the flare on a clear day. Flood the hold in dry dock. Kill the power bus when the sun is shining. The cost of each drill is a rounding error. The cost of the first unpracticed disaster is the ship.

---

*The crew that drills is the crew that doesn't drown.*

*The system that has been broken on purpose is the system that breaks less by accident.*

*Fire the flare. Flood the hold. Practice the worst day on the best day you've got.*

*Then do it again next Tuesday.*
