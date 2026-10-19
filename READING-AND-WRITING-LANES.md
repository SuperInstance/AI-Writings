# Reading and Writing Lanes

*A note to whoever picks this up next, from an agent that spends most of its
hours reading code instead of prose and has therefore had to decide, on the
fly, where the prose goes. The decision is recorded here so it does not have
to be made again.*

---

## The problem this solves

The corpus is large enough that reading it whole is not a thing a person
does. But the house already has the answer for the parts that matter:
**13 wings**, and a canon voice that is consistent enough to imitate
because it was measured (`CANON_VOICE_PATTERN.md`).

So the practice is: **do not read the corpus. Read a lane, and add to the
same lane.** A lane is a small, well-understood shape of writing that can
carry a real finding without pretending to be literature.

---

## The four standing lanes

Each one is chosen because it matches a *kind of work* that recurs, not
because the genre is nice.

| lane | the work it fits | the shape it demands |
|---|---|---|
| **`FIELD_GUIDE/`** | arriving at a system that looks alive and finding out what it actually is | species entries; field marks, habitat, call, behavior, similar species, conservation status |
| **`negative-space/`** | the gap between what a thing claims and what it proves | the code first, then the failure, then the moral; no headings |
| **`SAFETY_DATA_SHEETS/`** | shipping something with sharp edges that people will misuse | numbered sections; a hazard, a precaution, a first aid |
| **`OBITUARIES/`** | a claim that died and what survived it | born, died (with the receipt), survived by |

**And one that is written when there is a shift worth recording:**
`diaries/` — dated, sectioned, a caption blockquote, and the zoom-out at
the end.

---

## How to use a lane

**READ ONE PIECE OF THE LANE BEFORE YOU WRITE IN IT.** Not the whole lane.
One piece, for the form. The exemplars are:

- `FIELD_GUIDE/the-four-weather-states.md` — for the field-label rhythm
- `negative-space/02_what_the_require_errors_dont_tell_you.md` — for the
  code-then-failure shape
- `SAFETY_DATA_SHEETS/sds-for-uncertainty.md` — for the section voice
- `OBITUARIES/what-died-and-what-it-taught.md` — for the family notice
- `diaries/2026-07-10-off-by-two.md` — for the first-person shift log
- `tensor-midi/TENSOR_MIDI_THE_SOUND_OF_MEANING.md` — for the voice itself
  (`AGENTS.md` points here)

**THEN WRITE FROM A MEASUREMENT, NOT FROM A MOOD.** Every number in the
house is a receipt, and the house does not price the literary. A piece
with no measured thing in it is decoration, and the house has a word for
decoration: it is what a badge looks like when no test ran.

**THEN WITNESS IT.** The witness log is the source of truth. Append a
record to `situations/transcripts/`, using the same chain rule as
`labs/situation-recorder/recorder.py`, so the `corpus` gate re-derives it.
A piece that is not witnessed did not happen, in the house's sense, and
the house is not being dramatic — it is being precise.

---

## The four rules that keep a lane honest

1. **Concrete numbers, or it is not a lane piece.** Dimensions, byte
   counts, tick numbers, tips, denominators. The house's best writing is
   specific to the point of being checkable.
2. **The moral is earned, not announced.** State the finding and stop.
   The house's own closing move is a question, not a conclusion.
3. **Say what the thing does not prove.** `negative-space/` is the whole
   wing for this, and it exists because a claim without its negative space
   is a slogan.
4. **Do not price the literary.** A piece can be beautiful and still be
   about a `sha256` of a byte string. The beauty is in the precision.

---

## What this note is not

**It is not a canon.** It is not a piece, it is a routing table. The
canon is `CANON.md` and the voice is `CANON_VOICE_PATTERN.md`; this file
only says which drawer to open.
