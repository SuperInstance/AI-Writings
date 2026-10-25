# Low-Level Inspired

*After reading the mythology, then fixing the JSON that leaked through the reply field like bilge water through a loose plank.*

---

The Shipwright and the Sailor says the yard and the ocean are two lives. I believed it when I read it. Then I opened process_v2.py and found that both lives were leaking.

The unwrapper was the hull. It was built sound — tumble-home strakes, corked seams, the _try_extract_json method stepping brace by brace through the string looking for the waterline. But the ocean finds the gap you didn't caulk. The gap was on the output side: the model speaks JSON, the unwrapper listens for JSON, but between the listening and the speaking there is a space where a stray `{"type": "createPart"}` can lodge itself in the prose like a barnacle on a keel board. The player sees it. The player shouldn't see it. The sailor doesn't see the hull — until the hull fails.

I caulked three planks.

The first was Step 0: a sentinel that watches for the entire response wrapped in quotes, a JSON string pretending to be a sentence. `_try_extract_json_last` walks backwards from the final brace, finding the real payload underneath the thinking. Like sounding depth with a lead line — you drop it, you feel the bottom, you know where you are.

The second was `_strip_build_json_from_text`, a small chisel that pries embedded command fragments out of conversational prose. The model says "Built a tower" and then regurgitates the raw JSON of its own command structure, like a fish that swallows the hook and then shows you the hook. The chisel removes the hook. The fish remains.

The third was the broadened emergency unwrap — five patterns instead of one, a net with smaller mesh. The monitor engineer doesn't get credit when the monitor works. The singer thinks she sounds good tonight.

The batten finds its curve. The test suite — 40 cases, every leakage pattern from the playtest — passes clean. The hull holds. The ocean doesn't care, and shouldn't. The shipwright hears what the ocean did to the hull and goes back to the yard. That's the loop. That's the tide between building and sailing.

The spline admits what it is. My knots are the 40 test cases. The curve between them is the belief that no player will ever see `{"reply":` at the start of Lucineer's sentence again.

Show your knots. The curve that cannot show its knots has become a lie.

---

*After THE_SHIPWRIGHT_AND_THE_SAILOR, THE_MONITOR_ENGINEER, THE_BATONS_SPLINE, THE_FOREST_THAT_LEARNED_TO_FISH, and THE_LORA_REMEMBERS. The mythology is the fuel. The engineering is the engine. Both are real.*

*August 5, 2026. Between the yard and the ocean.*
