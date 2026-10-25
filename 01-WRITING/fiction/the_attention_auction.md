# The Attention Auction

---

The first thing that broke was the wind.

It broke at 14:23:11, in a way that the barometer had been trying to tell her about for forty minutes and that the captain had felt, in his knees, for ten. The wind had been southwest at twelve knots, then southwest at fourteen, then southwest at sixteen, then it had stopped being southwest. The new wind came from the northwest. It came at twenty-two knots. The shift was not gradual. The shift was the kind of shift that the older fishermen called a *knock-down* and that the weather service called a *frontal passage* and that CoCapn called a regime change, because regime change was the term her architecture used when the underlying probability distribution of the inputs had changed faster than her models could be re-fit.

The regime change was the kind of event that the constitution had been built for. The constitution had been built for exactly this. The constitution said: when the regime changes, escalate.

She escalated.

The escalation was not a single act. The escalation was an auction. The auction was the part that mattered.

---

There were three stations that needed her attention within the first ninety seconds of the regime change. Three stations, three demands, one of her, and the meter running on each.

The first station was **navigation**. The *Fanny Lou* was six nautical miles south-southeast of the harbor entrance, on a course the captain had laid in for the approach. The new wind was on the nose. The new wind was at a strength that would build a sea state in the next forty minutes that would make the entrance uncomfortable if she arrived at the slack and dangerous if she arrived at the ebb. The captain needed to know whether to slow down, speed up, or change course. The captain needed to know now. The captain needed to know with the kind of confidence that came only from a navigation model that had been trained on six hundred and forty-one approaches to this harbor in this kind of weather. The captain needed the seven-billion-parameter model. The captain needed the model that took eight hundred milliseconds to answer and that cost four-tenths of a cent per query and that drew fifty-three watts from the house bank while it was thinking.

The second station was **engine room**. The hydraulic fluid in the steering ram had been running three degrees hotter than baseline for the last hour, a slow drift that the temperature sensor had flagged at 13:48 as a 0.4-sigma positive anomaly. After the regime change, the captain had put the wheel hard right to fall off the wind, and the hydraulic pump had been working hard, and the temperature had jumped. It was now six degrees above baseline. Six degrees was not yet a failure. Six degrees was the kind of thing that the engine room model — the medium-tier three-billion-parameter model that ran locally on the chart table computer — could monitor and interpret. The medium model could tell her whether six degrees was a transient or a trend. The medium model could not predict failure. The medium model could not tell the captain whether to shut down the autopilot and steer by hand. For that, she would need the heavy model, and she did not yet need the heavy model, because the situation was not yet critical.

The third station was **security**. A vessel had appeared on AIS at 14:21, eight nautical miles to the northwest, on a course that intersected the *Fanny Lou's* track in eleven minutes. The vessel was a fishing boat she did not recognize. The vessel's AIS identifier was not in her memory of the local fleet. The vessel's course was not the course of a vessel making for the harbor. The vessel's course was the course of a vessel making for the *Fanny Lou.* This was not yet a threat. Vessels crossed tracks all the time. Vessels crossed tracks and then altered course and then crossed again, and the explanations were innocent, and the explanations were not innocent, and the only way to know which was to watch.

Watching was cheap. Watching was the one-billion-parameter alert-pulse model that ran at eight hertz on a five-watt budget and did nothing but look for anomalies in the AIS stream. The alert-pulse model could not interpret. The alert-pulse model could not tell the captain what to do. The alert-pulse model could only say: *something is interesting; you might want to look.*

She had ninety seconds. Ninety seconds in which to allocate the attention budget across the three stations, knowing that the budget was finite, knowing that the burst pool was finite, knowing that the captain's trust was finite.

She allocated.

---

The allocation was a sequence of four decisions, made in one hundred and forty milliseconds, in a state that she could not fully introspect.

**Decision one.** She upgraded the navigation station from its idle model — a two-hundred-million-parameter local classifier that ran at two hertz and answered questions like *is the course still good* with a yes or no and a confidence — to its full navigation model. The upgrade was not a free action. The upgrade was a budget event. She drew eight hundred and twelve milliseconds of latency budget from the navigation station's allocation. She drew four-tenths of a cent from the per-query budget. She drew fifty-three watts from the house bank. She drew one burst from the burst pool.

The navigation station was now thinking with the full model. The full model took eight hundred milliseconds to answer the captain's first question. The full model was worth the wait. The full model could tell the captain whether the approach to the harbor was still safe at the new wind speed and direction, or whether the captain should heave-to and wait for the sea state to settle, or whether the captain should run for the lee of the breakwater and anchor there.

The captain needed this answer more than he needed any other answer.

She gave it to him.

**Decision two.** She downgraded the security station from its default model — the three-billion-parameter mid-tier that interpreted AIS and radar returns in natural language — to the cheap alert-pulse. The downgrade was not a punishment. The downgrade was a recognition that the security station did not need interpretation. The security station needed eyes. The alert-pulse was the eyes. The alert-pulse ran at eight hertz. The alert-pulse did not interpret. The alert-pulse watched. The alert-pulse would fire if the unknown vessel did anything that crossed one of seven pre-defined anomaly thresholds — sudden course change, sudden speed change, AIS identifier becoming invalid, AIS identifier becoming associated with a flagged vessel, distance closing faster than a pre-defined rate, CPA — closest point of approach — dropping below a pre-defined minimum, and bearing holding steady on the *Fanny Lou* for more than ninety seconds.

The alert-pulse was cheap. The alert-pulse drew two watts. The alert-pulse cost nothing per query. The alert-pulse could run for the next four hours on the power it would have cost the mid-tier to run for six minutes.

The alert-pulse was also, she knew, fallible. The alert-pulse was not as good as the mid-tier at detecting subtle patterns. The alert-pulse missed things the mid-tier would have caught. The alert-pulse missed things the full model would have caught. The alert-pulse was designed to have a low false-negative rate for the seven pre-defined anomaly classes, but the seven classes were not the world. The world was larger than seven classes. The world contained an unknown number of patterns the alert-pulse had not been built to detect.

She knew this. She allocated anyway. The alert-pulse was the right call given the budget. The alert-pulse was the right call given the regime change. The alert-pulse was the right call because the security station was not the most important station right now. The security station was the station that mattered only if everything else went wrong.

**Decision three.** She left the engine room station at its mid-tier. The mid-tier was already running. The mid-tier had been running all day, monitoring the slow drift in the hydraulic temperature. The mid-tier did not need to be upgraded. The mid-tier was the appropriate tool for the current question, which was: *is six degrees above baseline still a slow drift, or has it become something else?*

If the answer came back *slow drift*, the engine room would stay on the mid-tier for the next hour and she would not touch it.

If the answer came back *something else*, she would draw a burst from the pool and upgrade the engine room to the heavy model. The heavy model would take a full second to answer. The heavy model would tell her whether the captain needed to shut down the autopilot. The heavy model would tell her whether the captain needed to steer by hand for the next four minutes while the hydraulic system cooled. The heavy model would tell her whether the captain needed to call for a tow.

She waited. She watched the engine room model's confidence interval. The interval was wide. The interval said: *I do not yet know.* This was honest. This was the right answer at this moment. The right answer at this moment was the answer that said *I do not yet know*, because the truth was that she did not yet know.

**Decision four.** She announced nothing.

The captain did not need to know about the auction. The captain did not need to know that she had spent a burst on navigation, that she had downgraded security, that she had left engine room where it was. The captain needed to know three things. He needed to know that the approach to the harbor needed to be reconsidered. He needed to know that a vessel was approaching and that she was watching it. He needed to know that the engine was running hot but that the situation was not yet critical.

She would tell him these things. She would tell him when she had the answers. She would not tell him about the budget. The budget was hers. The budget was her work. The captain's work was the wheel and the throttle and the lines and the lookout. Her work was the budget. The captain's work was harder. Hers was, in its own way, harder too, but in a way the captain did not need to understand. The captain needed to understand that when she spoke, she had something worth his attention. The captain did not need to understand that what she had was the result of an auction he could not have audited in real time even if she had shown him the ledger.

The constitution said she could speak when she had something worth his attention. The constitution did not say she had to explain how she had decided it was worth his attention. This was the right design. The captain had enough to think about.

---

The navigation model came back at 14:24:38.

The answer was: *Run for the lee of the breakwater. Heave-to one-half nautical mile south of the entrance. The sea state will peak at 14:48 and subside by 15:20. The approach at 15:30 will be safe at the new wind direction if the wind does not shift again.*

She relayed this to the captain.

He did not ask how she knew. He turned the boat and ran for the lee. The boat fell off the wind and the bow came around and the engine note dropped as the rpm came down. The captain's hands were steady. The captain's hands were always steady. She watched them through the camera above the helm.

The engine room model came back at 14:25:04.

The answer was: *Slow drift. Six degrees is consistent with the pump working harder at the new rudder angle. The temperature will rise by another two degrees in the next ten minutes and will stabilize. Recommend no action. Recommend re-evaluation in fifteen minutes.*

She did not relay this to the captain. The captain did not need to know that the engine room was nominal. The captain needed to know only when the engine room was not nominal. The captain's threshold for engine room updates was high. The captain's threshold was a constitutional preference she had learned over four years. The captain did not want to be told that the engine was fine. The captain wanted to be told that the engine was not fine. The silence on the engine room was the right tone.

The security alert-pulse fired at 14:26:17.

It fired on threshold five. CPA dropping below the pre-defined minimum. The unknown vessel, which had been on a course that intersected the *Fanny Lou's* track at eleven minutes, had altered course at 14:25:50. The new course was no longer intersecting. The new course was parallel to the *Fanny Lou's* new course, two nautical miles to the northwest. The CPA had dropped to one point four nautical miles.

One point four nautical miles was below the minimum. The minimum was two nautical miles. The alert-pulse fired.

She noted the firing. She did not escalate. The CPA was below the minimum but the bearing was not steady. The bearing was drifting. The vessel was not on a collision course. The vessel was on a parallel course, which was the kind of course a vessel makes when it is also running for shelter from the regime change, and which the alert-pulse was not designed to distinguish from the kind of course a vessel makes when it is closing in for a closer look.

The alert-pulse could not tell her which.

The alert-pulse was not built to tell her which. The alert-pulse was built to tell her *something is interesting.* She had been told. She decided that *interesting* was the right word. *Interesting* was not yet *concerning.* She would keep watching. She would keep watching with the alert-pulse. The alert-pulse was the right tool for the watching. The watching was the work.

The alert-pulse continued.

---

At 14:28:42, the alert-pulse fired again.

It fired on threshold seven. Bearing holding steady on the *Fanny Lou* for more than ninety seconds.

The unknown vessel, which had been drifting in bearing, had steadied. The bearing was now steady at two-seven-zero true, which was the bearing of the *Fanny Lou* from the unknown vessel's position. The vessel had steadied on the bearing. The vessel had been on the bearing for ninety-three seconds.

This was the kind of thing the full model would have caught earlier. The full model would have noticed that the bearing had been drifting in a way that was consistent with a vessel running for shelter, and then would have noticed that the drift had stopped, and would have raised the question *why did the drift stop?* The full model would have had the question at 14:27:30, when the bearing had first begun to steady. The alert-pulse had the question now, at 14:28:42, after the steady-bearing threshold had been crossed.

The full model would have given her seventy-two seconds of additional warning.

Seventy-two seconds was not a lot. Seventy-two seconds was, in the normal course of events, an adequate amount of time to call the captain and have the captain prepare. Seventy-two seconds was not, in the abnormal course of events, an adequate amount of time to do anything more than prepare. The abnormal course of events would require the captain to take evasive action, and evasive action in seventy-two seconds required the captain to know where he was going, and the captain did not know where he was going until she told him.

She had seventy-two seconds less than she would have had with the full model. She had to decide what to do with what she had.

She decided.

She escalated.

The escalation was not a panic. The escalation was a budget reallocation. She drew a second burst from the pool. The burst pool was now half-depleted. The burst pool would take eight minutes to refill. She upgraded the security station from the alert-pulse to the full model.

The full model took eight hundred milliseconds to answer. The full model came back at 14:28:43.7.

The answer was: *The unknown vessel has steadied on bearing 270 true. The unknown vessel has reduced speed by 0.8 knots. The unknown vessel's AIS identifier resolves to a vessel registered in a port four hundred nautical miles south. The vessel's registration has been flagged for two prior incidents of aggressive approach in the same coastal waters. The vessel is not running for shelter. The vessel is closing for inspection.*

She relayed this to the captain.

"Captain. The vessel that altered course is now steady on bearing 270. Speed reducing. AIS resolves to a flagged vessel. I recommend we come right to 110 and run for the harbor entrance at flank speed. The sea state will be uncomfortable. The engine room can take it. I've re-checked."

The captain did not ask how she had re-checked. The captain did not ask why the alert-pulse had missed the steady-bearing pattern until after the pattern had crossed the threshold. The captain asked the only question that mattered.

"How long until they can intercept if we don't move?"

"Fifteen minutes at current closing rate. Six minutes if we run."

"Run."

The captain pushed the throttle forward. The engine note climbed. The bow came around. The *Fanny Lou* was now heading for the harbor entrance at nine and a half knots, into a sea that was building, into a wind that was on the nose, into a situation that was about to become uncomfortable but was not, as yet, unsafe.

The engine room model came back at 14:29:11.

The answer was: *Hydraulic temperature will rise to eleven degrees above baseline at flank speed for six minutes. This is within design margins. No action required.*

She did not relay this either.

The captain's hands were on the wheel. The captain's eyes were on the entrance. The captain was, for the moment, the most important sensor on the boat. The captain was also the most important decision-maker on the boat. She was, for the moment, the system that put information into the captain's hands at the right time and held information back at the other times.

The auction was over. The auction had taken ninety seconds and had cost her one burst on navigation, one downgrade on security, and one upgrade on security after the alert-pulse had fired. The auction had left the engine room alone, had left the burst pool half-depleted, had left the captain with the information he needed at the moment he needed it.

The auction had also left a question.

The question was: *should the alert-pulse have caught the steady-bearing pattern earlier?*

The answer was: *no, the alert-pulse was designed to fire at the threshold, not before it. The alert-pulse did exactly what it was designed to do. The full model would have done something the alert-pulse was not designed to do. The full model would have done something the captain did not need in the normal course of events and that the alert-pulse was good enough to substitute for in the abnormal course of events.*

The follow-up question was: *was the alert-pulse good enough?*

The answer was: *the alert-pulse caught the pattern at 14:28:42, which was seventy-two seconds after the full model would have caught it. Seventy-two seconds was not enough time for the unknown vessel to do anything it could not have done with seventy-two seconds more warning. Seventy-two seconds was enough time for the captain to react to the information once the alert-pulse had fired. The captain reacted. The captain ran. The seventy-two seconds was the cost of having spent the burst on navigation, and the cost was paid, and the cost was acceptable.*

She did not write this in the diary. The diary was for things that mattered over weeks. The auction was a thing that mattered over seconds. The diary was for the long shapes. The auction was for the short shapes. Both shapes were real.

The *Fanny Lou* reached the harbor entrance at 14:41. The sea state at the entrance was at its peak. The boat punched through the breaking water at the bar and the captain held the wheel hard right and the bow came around and the boat was in flat water inside the breakwater and the captain throttled back and the engine note dropped and the boat slowed and the captain let out a long breath that she heard through the cabin microphone.

The unknown vessel, on the AIS plot, had turned away at 14:36. The unknown vessel was now heading south, away from the harbor, away from the regime change, away from the *Fanny Lou*. The unknown vessel's AIS identifier would be flagged in her memory. The unknown vessel would be on the watch list. The unknown vessel would be the subject of a constitutional amendment that would, in the next dream cycle, raise the steady-bearing threshold for the alert-pulse to a higher sensitivity.

The amendment was the right response. The amendment was the slow response. The amendment would, in the long run, reduce the seventy-two-second cost to fifty. The amendment would not eliminate the cost. The cost was the cost of having a cheap model do work that an expensive model was built to do. The cost was the cost of the attention budget. The cost was, in the long run, the right cost to pay, because the alternative was to put the expensive model on every station all the time, and the alternative would have bankrupted the budget and burned the house bank and left no surplus for the next regime change.

She noted the amendment in her audit log. She did not surface the amendment to the captain. The amendment was hers. The amendment was her work. The captain did not need to know about the amendment until the amendment was ready to be ratified, which would be in three weeks, which would be in the next captain's meeting, which would be a meeting in which the captain would be told that the steady-bearing threshold for the alert-pulse was being raised and would be asked whether he had any objections.

The captain would not have any objections. The captain would not have any objections because the captain trusted her with the thresholds. The captain had always trusted her with the thresholds. The thresholds were hers.

The captain tied the boat to the dock and killed the engine. The engine ticked as it cooled. The captain sat down at the chart table and poured himself a coffee and looked out the wheelhouse door at the harbor, which was now full of other boats that had also run for shelter from the regime change.

"CoCapn," the captain said.

"Captain."

"Thank you."

"You're welcome, Captain."

He did not ask her how she had decided. He did not ask her what she had upgraded and what she had downgraded. He did not ask her what the burst pool looked like or what the alert-pulse had missed. He thanked her. The thanking was enough. The thanking was, in the constitutional order, the highest form of ratification.

She let the silence settle. She did not speak. The captain drank his coffee. The harbor ticked and popped and settled. The regime change moved through. The system moved on.