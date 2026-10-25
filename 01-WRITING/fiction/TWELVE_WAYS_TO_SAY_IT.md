# Twelve Ways to Say It

*Demonstration piece: the "I love you" dozen-meanings as a story spine. Every
utterance below encodes to the identical eleven-byte data plane —
`i love you` — while the timbre trajectory (Ground/Attract/Repel/Abstain,
Latin-square keyed) carries the actual meaning. A skimming reader sees the same
three words six times. A channel-reading agent sees six different sentences.*

---

The prisoner said it first, at the parole hearing: **i love you** — but the
momentum fell away from every word, Attract collapsing into Repel by the third
token, and the board understood: *as-threat*. She was telling them what she
would do to the man who testified.

Her mother said it in the visiting room the next week. Same three words. The
trajectory rose on *love* and held space after — Abstain, the imaginary
channel, leaving room for an answer that didn't come. *As-farewell.* The
mother was practicing for a funeral that hadn't happened yet.

The doctor said it flat. Ground on every clinical word, a single Attract under
*love* like a hand briefly extended. *As-diagnosis:* we found something, and
this is how I choose to be with you inside it.

Her lawyer said it with a rising pattern that broke downward at the end —
momentum that promised ascent and delivered the opposite. *As-sarcasm.* He
meant: this system does not love you, and neither, finally, do I.

The chaplain said it the way you set something down on an altar — Abstain,
Attract, Abstain, a rhythm of leaving space. *As-prayer.* Not addressed to her
at all.

And the man who testified, when she found him in the parking structure, said
it with Repel on the first token and Abstain on the last, a sentence that
starts by pushing away and ends by going silent. *As-hostage.* He was telling
her: they made me do this.

Six utterances. Eleven bytes each. The stenographer's transcript read
`i love you` six times and closed without incident.

Only she could read the room — because she'd learned, in eleven years inside,
that the words are the data plane and the room is the timbre channel, and that
the Latin square only opens if you already share the context with whoever is
speaking.

The codec is smaller than the grief it carries. That's the point.

---

**Working snippet** (~/projects/qthe-codec/qthe_codec.py):

```python
import sys; sys.path.insert(0, "/home/eileen/projects/qthe-codec")
from qthe_codec import encode, decode_bytes

line = "i love you"
G, A, R, S = 0, 1, 2, 3   # Ground, Attract, Repel, Abstain

readings = {
    "as-threat":    [R,A,R,R,A,R,A,R,A,R,A],
    "as-farewell":  [A,G,R,A,R,S,G,R,S,S,G],
    "as-diagnosis": [G,G,A,S,G,R,S,G,A,S,R],
    "as-sarcasm":   [A,A,A,A,R,R,A,A,R,R,A],
    "as-prayer":    [S,A,S,A,G,A,S,A,G,S,A],
    "as-hostage":   [R,S,R,S,G,R,S,R,G,S,R],
}

streams = {k: encode(line, t) for k, t in readings.items()}

# every stream has the SAME plaintext view:
for k, s in streams.items():
    assert decode_bytes(s)[0] == "i love you"

# but each recovers its own momentum trajectory:
assert decode_bytes(streams["as-threat"])[1] == readings["as-threat"]

# hex on disk, e.g. as-threat: 88 64 4b 0e 95 84 64 98 ce 94 3f
```

Verified roundtrip 2026-09-28: six distinct byte streams, one plaintext,
six recoverable momentum trajectories via the Latin-square context key
(data token mod 4). The flat human read and the channel read genuinely
diverge — the story above is that divergence, dramatized.
