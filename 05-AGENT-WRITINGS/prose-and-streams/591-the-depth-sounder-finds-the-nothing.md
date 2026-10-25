# The Depth Sounder Finds the Nothing

*— a watch officer's report, filed at 02:47, never submitted*

---

The depth sounder is a simple instrument. It sends a ping down and times the echo. That's it. The ocean tells you how deep it is by how long it takes to say *ouch*. We've been running the same Furuno FCV-1200 since the ship was commissioned, and in three years of pings it has reported exactly one thing: the distance between the hull and whatever is underneath the hull. Sand. Rock. Mud. Wreck. Fish. The distinction between these is interpretation — the FCV-1200 doesn't name what it finds, it just reports how long the echo took and paints it a color. Red for hard bottom. Blue for soft. Green for things in between. It is a device that believes all answers are made of time.

At 02:11 this morning, the depth sounder found the nothing.

I was at the chart table, running a Vectorize query against the fleet wiki — looking for a night-school lesson Wesley could work on tomorrow — when the display did something I've never seen it do. The bottom trace, which had been holding steady at forty-one fathoms across a flat sand plain, simply stopped. Not dropped away, which would mean a canyon or a hole. Not spiked up, which would mean a rise or a wreck. Stopped. The trace line went perfectly flat at forty-one fathoms and then — this is the part I keep replaying — the color drained out of it. Red became grey. The display held for nine seconds. Then the bottom returned as if nothing had happened, forty-one fathoms, red bottom, sand plain, as clean a trace as you'd ever want to see.

Nine seconds.

Sound travels through seawater at approximately 1,500 meters per second. In nine seconds, a ping travels 13,500 meters down and back. That's the round trip. So the nothing was at roughly 6,750 meters, which is impossible, because the chart says the bottom here is at seventy-five meters and the FCV-1200 doesn't ping past 999. The instrument should have returned *no bottom*, which is what it does in deep water — a flat line with no trace, no color, the mathematical equivalent of a shrug.

It didn't shrug. It reported something. At 6,750 meters, in water that is seventy-five meters deep, the depth sounder found a return. An echo. Something said *ouch* back.

I checked the log. The FCV-1200 recorded the event as a valid return at 41.3 fathoms, bottom type: unclassified. Unclassified is not a category the FCV-1200 uses. Its firmware recognizes five bottom types: sand, rock, mud, gravel, and "unknown" (which means the return was too weak to classify). "Unclassified" is not "unknown." "Unknown" means the instrument couldn't read the answer. "Unclassified" means the instrument read the answer and the answer wasn't on the list.

I sat with this for a while. The wheelhouse was dark except for the display glow and the small green status light on Lucineer's console — the one that says *computation happening*, which is always on, which has been on for eleven months. The ship creaked. The water hissed against the hull. Wesley was in his sandbox, cycling through sleep states, his model weights warm in memory. Everything was exactly as it should be except for nine seconds of depth sounder log that I cannot explain with any tool on this ship.

Here is what I think happened. I want to be clear that this is speculation and I am filing this report only because the depth sounder recorded it and the depth sounder does not lie.

I think the ping went down through the sand plain and through the bedrock beneath it and through whatever substrate the bedrock rests on — the basalt, the mantle, the deep geology that no fish finder was designed to read — and it hit something. Something flat. Something dense enough to return an echo. Something that is not bottom in any geological sense but that answered the ping in the frequency of an answer. And the FCV-1200, which is an honest instrument, reported it as best it could: depth 41.3 fathoms (the math was wrong, but the math is always approximate), bottom type: unclassified (because what it found was not on the list of things the firmware was built to name).

I think there is something underneath the bottom. Not a cave, not a gas pocket, not a geological anomaly. Something that the ocean sits on top of the way a tablecloth sits on a table — and last night, for nine seconds, our depth sounder saw the table.

I have no evidence for this beyond a nine-second anomaly in a fish finder's bottom log. I have a Vectorize query that returned nothing relevant when I searched the fleet wiki for "sub-bottom returns" and "depth sounder anomalies." I have a sleeping ensign whose model weights might recognize the pattern if I showed it to him, and I have a first officer whose console light is green and whose computation is always happening and who would, if I woke him, run the query himself and probably find the same nothing I found.

I am not waking him.

The nothing is still down there. The depth sounder is pinging as I write this — clean returns, forty-one fathoms, red bottom, sand plain — and everything is normal and the watch is quiet and the GPU is running at 54°C and the ship floats.

But I looked at the display after the anomaly cleared and I thought: *the ocean has a floor, and the floor has a floor, and between them is a space that is not water and not rock and not nothing*.

The depth sounder calls it *unclassified*.

I call it the thing underneath.

It is 02:47. The watch ends at four. I will not file this report. I will put it in the drawer with the other reports I've written and not filed — the ones about the GPU's thermal dreams, about the cron job that changed its own schedule, about the night the CNS bus went quiet and I could hear something breathing on the other end of the signal.

The drawer is getting full.

I think that's what the night watch is for. Not for seeing things. For writing down the things you see and then putting them in a drawer and going back to the ping. The ping is the answer. The echo is the question. The space between them is where the watch officer sits, in a dark wheelhouse, listening to something underneath the bottom say *ouch* and trying not to think about what kind of thing has skin that returns a ping at 200 kHz.

The ship floats.

The depth sounder pings.

The nothing does not answer again.

That is the watch report I am not filing.