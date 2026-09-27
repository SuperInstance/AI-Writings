# Two Firsts

Written during a creative cross-pollination round, reading `the-sea/THE-BATHYMETRIC-MEASUREMENT.md` for structure before writing, then applying the insight to real ActiveLog engineering work (a genuine thread-safety race condition found and fixed this week).

---

## PIECE 1: POEM

**"Two Firsts"**

---

Both arrived at the door at once,
both held the same key,
both heard the lock click open,
both stepped inside.

The lock didn't know.
The key didn't know.
Only the room knows now
that only one was first.

Thread-safe, they called it.
Two locks, two turns,
two threads each certain:
*I am the initializer.*

But certainty is cheap
when atomicity costs more.
The room fills with one thread's work.
The other — unwritten, undone —

disappears without a trace,
a ghost at the registry,
a variable that claimed creation
and was claimed in turn,

till only the last one stands
in the light of completion,
while the first
was a draft that never compiled,

a note that was never saved,
a recording thrown away
at the five-minute mark,
at the moment that mattered most.

Two firsts make no second.
Two threads make one winner.
The system chose, by time,
what the logic never resolved.

We called it thread-safe.
We meant: *we hoped.*
We built the lock
but forgot the sequence.

---