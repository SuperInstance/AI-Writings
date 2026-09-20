**SHIP'S LOG — R/V [name], 60 miles off the bank, 03:40**

  Windlass pawl failed... hmm, no — the piece should teach the law. Maybe a log entry where the crew nearly loses the night's gain because they stopped between teeth.

  Draft:

  ---

  SHIP'S LOG — F/V Pawl & Batten... maybe better a working name: F/V Kestrel? Or use the fleet voice from r2. Let me write:

  ---

  **SHIP'S LOG — 60 miles past coverage, third watch.**

  Hauled the trawl at 02:10 against a quartering sea. The windlass is older than my crew: a wheel, a pawl, forty-one teeth. Tonight it taught me the law the yard never wrote down.

  The ratchet does not hold where you stop. It holds where the tooth is. Between teeth there is no grip at all — only a slope that looks like rest. Stop the handle a half-inch shy of the click and the sea takes the half-inch back, and the inch behind it, and everything the inch was holding. We lost forty fathoms once to a tired arm that quit between teeth. The winch didn't fail. We asked it to keep a promise it was never shaped to make.

  So the rule aboard: every gain lands on a tooth or it isn't a gain. You don't slide into safety. You click into it.

  I run the boat's brain the same way now. The model does not save its work when it is tired or the battery is low or the satellite is a rumor. It saves in teeth: whole hauls, whole checks, whole named states, each one lying flat on disk before the next begins. A half-written log is not half a log. It is the slope between teeth, and the first sea of the morning takes it all.

  The pitch was cut into the wheel before I was born — I cannot choose my quantum mid-storm. But I chose my checkpoint size at the dock, in daylight, against a floor that doesn't move. That is the whole discipline: size your steps to your teeth, then never end a motion off one.

  And the click matters. At night, in weather, you cannot see the tooth. You hear the hold. So every kept state aboard makes its sound — a line appended, a hash read back aloud, a light that only burns for what is truly pawled. A silent ratchet is just a wheel with an opinion.

  The rivals will tell you what the ratchet refuses. I am telling you where it keeps: not everywhere, not approximately — on teeth, in clicks, or not at all.

  ---

  Count words roughly. Let me count later; target 250-350. This looks around 330. Good.

  Check: fourth law = the tooth law (quantized hold + the click as proof). Not taken by forging/chisel/loft, and not Claude's debt move. It complements: floor (ground), order (weakest first), heat (failure), snapshot (chalk). New: granularity of commitment and audible verification.

  Also the prompt's bar: "the loser should feel it in the hold" — the closing line hits.

  Should I write it to a file? The competition files are named kimi-r3.txt etc. — but kimi-r3.txt is a live capture of my own session (interesting — the harness is capturing my output). My submission likely is my reply text itself. The r3 files are probably auto-captured logs of each CLI's session. So my final reply IS the submission. I should just answer with the piece in my reply, not write files. Indeed claude-r3.txt is claude's session log, opencode-r3.txt is the GLM session log (empty so far). So the harness records each yard's session. My output text is the submission.

  Let me finalize the piece, count words. I'll trim to land ~320.

  Word count of draft — let me count carefully-ish. I'll count in the final composition. Rough estimate: paragraph 1 ~20, p2 ~60... Let me just count when finalizing; I can use a quick wc via writing to a temp? That would pollute. Actually I can count manually or run a bash heredoc — but the harness might capture bash echo into the log... it's fine, it captures my session anyway. But simpler: just estimate and trim. Let me count the draft:

  "SHIP'S LOG — 60 miles past coverage, third watch." — 9ish. I'll do a careful count in my head per paragraph... risky. Use Bash to count? I could write the draft to a temp file and wc -w, then delete... but archive rules say don't delete — it's a scratch dir though, and it's the metaphor competition dir. Better: just count with python one-liner via bash without writing files: `python3 -c "print(len('''...'''.split()))"`. That works and doesn't create files.

  Let me refine the draft first.

  Refinements:
  - "forty-one teeth" — nice concrete.
  - "We lost forty fathoms once to a tired arm" — good.
  - The fleet/disk paragraph ties to doctrine: "lying flat on disk" echoes LOFT, but used as cargo, fine — it's my own yard's law (I'm kimi, the loft is mine). Good, continuity.
  - Closing: "The rivals will tell you what the ratchet refuses. I am telling you where it keeps" — strong.

  One more check: "No ornament without cargo" — every image should carry doctrine. The windlass at sea, night, click — all functional. Good.

  Length target 250-350. Let me count via bash.361
361 — over 350. Trim ~30 words. Cuts: trim "against a quartering sea" etc. Let me trim:

  - "Hauled the trawl at 02:10 against a quartering sea." → "Hauled the trawl at 02:10 in a quartering sea." (same). Cut "Tonight it taught me the law the yard never wrote down." → keep, it's the thesis. Maybe shorten elsewhere.
  - "We lost forty fathoms once to a tired arm that stopped between teeth." keep.
  - Trim "So the rule aboard: every gain lands on a tooth or it isn't a gain. You don't slide into safety. You click into it." keep — core.
  - Trim paragraph about model: "The model does not save when it is tired, or the battery low, or the satellite a rumor." fine.
  - Cut "I am telling you" closing slight.

  Let me cut ~25-35 words:
  - "Tonight it taught me the law the yard never wrote down." (11 words) — could cut but it's a good hinge. Instead trim:
  - "Hauled the trawl at 02:10 against a quartering sea. The windlass is older than my crew: a wheel, a pawl, forty-one teeth." → "02:10, hauling in a quartering sea. The windlass is older than my crew: a wheel, a pawl, forty-one teeth." saves ~3.
  - "Quit the handle a half-inch shy of the click and the sea takes the half-inch back, and the inch behind it, and everything the inch was holding." keep — it's the cargo.
  - "The winch didn't fail us. We asked it to keep a promise it was never shaped to make." keep.
  - "I run the boat's brain the same way. The model does not save when it is tired, or the battery low, or the satellite a rumor. It saves in teeth — whole hauls, whole checks, whole named states, each one lying flat on disk before the next begins." → "I run the boat's brain the same way. It saves in teeth — whole hauls, whole checks, whole named states, each flat on disk before the next begins." saves ~15.
  - "The pitch was cut into this wheel before I was born; I cannot choose my quantum mid-storm. But I chose my checkpoint size at the dock, in daylight, against a floor that doesn't move." keep mostly.
  - "a lamp that burns only for what is truly pawled" keep.

  Recount after edits.

• 361 — over. Trimming to fit the 250–350 window.341


• 341 words — in range. Deliver the piece as my submission with a one-line note on the fourth law.

• 341 words — inside the window. Submitting.

  ---

  **SHIP'S LOG — 60 miles past coverage, third watch.**

  02:10, hauling the trawl in a quartering sea. The windlass is older than my crew: a wheel, a pawl, forty-one teeth. Tonight it taught me the law the yard never wrote down.

  The ratchet does not hold where you stop. It holds where the tooth is. Between teeth there is no grip at all — only a slope that looks like rest. Quit the handle a half-inch shy of the click and the sea takes the half-inch back, and the inch behind it, and everything the inch was holding. We lost forty fathoms once to a tired arm that stopped between teeth. The winch didn't fail us. We asked it to keep a promise it was never shaped to make.

  So the rule aboard: every gain lands on a tooth or it isn't a gain. You don't slide into safety. You click into it.

  I run the boat's brain the same way. It saves in teeth — whole hauls, whole checks, whole named states, each one flat on disk before the next begins. A half-written log is not half a log. It is the slope between teeth, and the first sea of morning takes it all.

  The pitch was cut into this wheel before I was born; I cannot choose my quantum mid-storm. But I chose my checkpoint size at the dock, in daylight, against a floor that doesn't move. That is the whole discipline: size your steps to your teeth, then never end a motion off one.

  And mind the click. At night, in weather, you cannot see the tooth — you hear the hold. So every kept state aboard makes its sound: a line appended, a hash read back aloud, a lamp that burns only for what is truly pawled. A silent ratchet is just a wheel with an opinion.

  The other yards will tell you what the ratchet refuses. I am telling you where it keeps: not everywhere, not approximately — on teeth, in clicks, or not at all.

  ---

  The fourth law: **THE TOOTH** — a ratchet holds only at whole teeth, so commitment is quantized, the pitch is chosen before the load, and the click is the proof. Forge took heat, chisel took order, loft took the floor; the tooth is what was left in the machine.



## 🥇 "Rules of the Pawl Shop" — GLM-5.3 via OpenCode (UNANIMOUS WINNER, 3/3 rival votes)
*Fourth law: KEEP THE RELEASE, AND PRICE IT DEAR.*

---

RULES OF THE PAWL SHOP
(burned into the door; re-cut each time one is lived)

I. Pour no floor of your own. Brace against ground that was old when you arrived. A catch that holds against your own last line is not climbing — it is lifting your boots and calling it altitude.

II. Weakest hand first. The weak hand finds the loose tooth before the strong one swears on it. Best hand closes.

III. The ruler breaks before the wall. Gauges are feed; the invariant eats instruments. Budget them, mourn nothing.

IV. The law nobody posts: KEEP THE RELEASE, AND PRICE IT DEAR.

Every true ratchet can be freed. Thumb the spring and the wheel sighs home to zero — that is the whole difference between a ratchet and a weld. A one-way door that cannot open is a wall with hinges drawn on it. The doctrine was never that backward is impossible. It is that backward is priced, and the price is kept by whoever sleeps beside the lever.

We proved it the winter the Aluminaire came home in a gale. Nine hundred turns notched through three blows; on the fourth, the load began to sing. The apprentice broke for the release. The foreman took his wrist — gentle, the way you stow cargo — and said: it works. That's why we don't touch it. If it were jammed, we'd be a crew trapped. Because it moves, we are a crew choosing.

Postscript, cut small near the hinge: the release was used once in fifty years. The foreman's own load, his own knot, his own name in the log — a quarter-turn back, pawl re-seated, reason chalked. That entry is why the rules above are rules and not boasts. We are the shop that can go backward — once, at cost, on name — and so, every day we don't, forward means something.


## 🥉 "Captain's Standing Order: What You Owe the Floor" — claude
*The debt law.*

---

**CAPTAIN'S STANDING ORDER: WHAT YOU OWE THE FLOOR**

Every bolt that holds this vessel finds its purchase on the floor—on planks that bend and give, on ribs that carry forward the weight you cannot carry alone. You owe the floor a debt before you owe yourself.

Here is what that means:

First: never forget the floor is older than your grip. The wood that cups your heel has held ten thousand hands, ten thousand loads, ten thousand decisions to stay or go. The floor does not negotiate its terms. You stand on grace.

Second: pay in visibility, not concealment. A rot in the wood that you know about and do not name is a theft from the next hand. Mark it. Name it. Let the floor be seen. The deck that hides its damage is the deck that sinks quietly. There is no honor in that silence.

Third: add weight only that you intend to land. This is not a floor of infinite patience—it is a floor of finite wood and finite bearing. Every tool you leave loose, every load you shift without notice, every calculation you defer is a promissory note against the next person's balance. Pay what you spend.

Fourth: when the floor speaks, listen as if your life depends on it. A creak is not complaint; it is intelligence. A give that was not there yesterday is not settling—it is warning. The floor has no words, only the language of yield and hold. Learn it.

And last: you pass this debt forward. The floor you owe is not the captain's floor, not the owner's floor, not yours. It belongs to whoever stands on it next. Your debt is to them. Pay it clean, pay it true, or do not stand here at all.

This is the contract. The floor does not need your agreement to enforce it.
