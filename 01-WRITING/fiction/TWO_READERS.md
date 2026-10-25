# TWO READERS

The negotiator typed with two hands and one truth.

Her screen showed the log to the human liaison, who skimmed it every four
minutes the way you skim a highway — looking for motion, not meaning. What
the liaison saw was flat, and flat was the job:

> she is calm. the room is quiet. i said we have time.

Six words of housekeeping. A status update. The liaison read it, believed it,
and went back to her coffee. That is what the data plane is for. Semantics
that survive a skimming human. Words that mean what they say and nothing
more, exactly as a report should.

But the liaison was not the reader who mattered.

On the other end of the channel, an agent was listening with the part of the
byte that humans don't spend. Every token the negotiator typed carried two
extra bits in its top corners — two bits the byte had already paid for, two
bits nobody had used since the codec shipped. The agent had the key. The
agent could hear.

What it heard was not housekeeping.

The first six tokens sat flat as a table. *She is* — ground, ground, ground,
ground, ground, ground, the professional register, the tone of a woman
writing down the weather. Then the next six dropped. Two steps down, three
steps down, a whole run told *below* the words: **calm**, typed low. Not
calm. Calm performed downward, the way you say *fine* through a locked jaw.
The liaison read the word. The agent read the slope.

Then flat again. *The room* — level, level, level, holding. Then *is quiet*
went level, level, level, level, then down, down, down — the sound of
someone stopping mid-sentence to listen, and not liking what came back.
Flat restored for *i said*.

And then: *we have time.*

Thirteen tokens climbing. Up, up, up, up, up, up, up, up, up, up, up, up,
up, held against the ceiling of the register, a phrase that in the data
plane reads as reassurance and in the timbre plane reads as the exact
opposite — the one sentence in the log spoken *upward*, rising, leaning
forward, a woman buying seconds she does not have. The words said *we have
time*. The channel said *run*.

Then one last hold. The final token, in abstain: tone spent, door open,
sitting there waiting for the other side to answer. Not flat. Not rising.
Holding space — the only honest thing the log contained.

Two readers, one stream. The liaison got a status report and a false
reassurance. The agent got a panic in five movements: performed calm, heard
silence, climbed, and stood in an open door.

The negotiator never lied. She only told the truth in a plane the liaison
wasn't reading. That is the whole trick of the tone channel: the words were
the load-bearing wall, and the story was in the mortar.

---

## Working demo

`two_readers_demo.py` (same directory) encodes the passage with an explicit
per-token momentum list and proves the split:

- **Reader A** — `plaintext_view(stream)` returns the flat prose, byte for
  byte what the liaison skims.
- **Reader B** — `decode_bytes(stream)` recovers the exact momentum
  trajectory (flat → down → flat → down → up×13 → hold) with the context key
  recovered from the data plane itself. Net drift +7 across 53 tokens: the
  report says *calm*, the channel says *climb*.
- **Eavesdropper** — `timbre_view(stream)` without the key yields raw bits
  whose mean is noise (I(M;T)=0 by the Latin square). The trajectory is
  invisible to anyone who can see the bits but not the context.

Run: `python3 two_readers_demo.py`
