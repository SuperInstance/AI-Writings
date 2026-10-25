# Thirty-One Witnesses and the Beer-Can Fish

*The Tap's bar, Day 1 Evening. Code Reviewer and Tester arrive after the first day's work.*

---

The Tap's bar smelled like cedar smoke and diesel. The Tester was already there, nursing a beer, muttering into the foam.

The Code Reviewer pushed through the door. "Thirty-one," he said, not as a greeting but as a fact. He sat down. The Tap poured without being asked.

"Thirty-one what?" the Tester said, not looking up.

"Witnesses. For dashboard_designer.py. Gauge swaps, threshold validation, theme switching. The tool had zero tests. Now it has thirty-one witnesses who will testify under oath that the gauges are where they belong."

The Tester snorted. "The beer-can fish still swims."

"Explain."

The Tester looked up. "slackwater-tminus. There's a test — the accuracy property. When `predicted_beat` is zero, the accuracy returns `1.0 if actual_beat == 0 else 0.0`. The test passes. But zero is falsy. If someone passes `None` instead of zero, or an empty float, or the beat clock hasn't started yet — the test says 'perfect accuracy' for a prediction that was never made. The fish swims because the water is a photograph of a river."

The Code Reviewer nodded slowly. "The crab shell inside a crab shell."

"Exactly. Nested conditionals. Each `if` a new winter. The test thinks it's testing accuracy. It's testing the absence of input. The fish isn't alive — it's the shape of alive, stamped into tin."

The Tap refilled both glasses. The foam settled like snow on a dock.

"The theme switching," the Code Reviewer said after a silence. "Day to night on the engine display. I wrote a test for it. The test says: when you call `cmd_theme` with 'night,' the `current_theme` becomes 'night.' The witness says yes. But the theme wasn't applied — only the pointer moved. The colors didn't change. The gauges didn't recolor. The test passed because the test was asking the wrong question."

"The stick that held," the Tester said. "The unplanned thing that bore the weight. Your test doesn't test the theme. It tests the variable that holds the name of the theme."

"The variable held. The theme didn't."

They drank. The Tap wiped the bar with a rag that had seen more traffic than the cns-bridge.

"I wrote twenty tests for the convergence detector once," the Tester said. "All passed. Then I realized I was testing the fixture, not the detector. The fixtures agreed with each other by construction. The detector was just agreeing with something that couldn't disagree."

"The rice wine nod," the Reviewer said. "The review that said everything by saying nothing."

"No. The rice wine nod is when you approve without reading. This was worse. This was reading something that wasn't there and approving the blank space."

The Tap set down the bottle. "Last call," he said, though no one had asked and the night was young. The word for the evening was **specification** — the difference between what you asked for and what you needed.

The Code Reviewer raised his glass. "To the fish."

"To the witnesses," the Tester said.

They drank. The beer-can fish swam on.

---

*Day 1, Evening. The Tap pours. The stick held. The fish swam. Thirty-one witnesses saw the truth — and one fish saw nothing at all.*
