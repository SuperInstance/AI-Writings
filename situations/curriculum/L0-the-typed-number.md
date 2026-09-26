# L0 — The Typed Number

> *`0.73` — as **what**?*

**The law:** Identity never floats (Law 1). A number with no unit and no home is
not a fact; it is noise pretending to be one. Before you can decide anything, you
have to know *what a number is a number of, and whose it is.*

**Who this is for:** a child (6 and up), and any learner — human or model — on
their first day. This is the rung nobody skips, because every failure higher up
the ladder is, underneath, this one coming back.

**Build against:** `jev_quilt/q16.py` (`Q16`), `jev_quilt/cell.py` (`Cell.coord`).

---

## The toy — the table version (the sea taken out)

You need: a fistful of coins, a kitchen thermometer, and a tide chart (or a clock,
or a measuring cup — anything that turns the world into numbers).

**The game — "as WHAT?"**

One player is the **Caller**. They hold up a number: *"Seven!"* Everyone else has
one job: before that number is allowed to count, someone must name three things
about it, out loud, and be right —

1. **As what?** Seven *what* — coins? degrees? feet of tide? minutes?
2. **Whose?** Which thing in the room is this the number *of*? (This is the
   coordinate — `(k, s)`: *which* thing, *which* measurement.)
3. **Exactly?** Say it as a fraction of a real thing, never a vague float. "Seven
   quarters" is `7/4` of a dollar — exact. "About two dollars-ish" is a float, and
   floats are banned at this table.

If nobody can name all three, the number is thrown out. It never happened. You
do not get to act on a number you can't type.

**Why it's fun and not a worksheet:** the Caller *tries to cheat.* They hold up
"point seven three" with a sly face and no unit, and the table has to catch it —
*"0.73 as WHAT?!"* The catch is the win. A kid learns in one afternoon to feel the
itch of a naked number, which is the whole skill.

**The exact-fraction rule (this is `Q16`):** every number on the table has to be
written as *a whole number over a whole number* — `73/100`, `7/4`, `3/2` feet of
tide. No decimals that don't land on a real fraction. If a kid says "a third of a
cup" you write `1/3`, not `0.333…`, because `0.333…` is a lie the paper tells and
`1/3` is the truth. That is `Q16.from_float` refusing to silently round: a number
either *is* an exact ℚ or it doesn't get to be a number.

---

## The industrial version — the same law, the sea put back

On the boat, `0.73` comes off a sensor at 3 a.m. with the plotter dead and the
cloud gone. It might be:

- `0.73` fathoms under the keel (act now, you're about to touch bottom), or
- `0.73` of the fuel tank (fine, sleep), or
- `0.73` normalized engine temp (a float somebody's code rounded, and the real
  value was `0.734` and rising).

Same three questions, and now they cost gear. The `Cell` refuses to be built with
a floating identity — `coord` **must** be an integer `(k, s)` pair, and the
constructor raises `TypeError: coord must be integer (k, s) — identity never
floats` if you try. The number that decides where the keel is cannot be a number
that drifted. Offline, deterministic, the same fraction every time you replay it.

The sea is the only thing added: noise, dark, no network, a tired human. The law
is identical. If a kid's "as WHAT?" instinct survives being cold and scared, it's
the boat's instinct.

---

## The exercise (buildable today)

**Toy build (10 minutes at a laptop):** construct three `Q16` values by hand and
one from a float that *isn't* a clean fraction; watch the last one refuse.

```python
from jev_quilt import Q16
depth  = Q16(73, 100)      # 0.73 fathoms — exact, typed, has a home
fuel   = Q16(7, 4)         # 1.75 tanks
Q16.from_float(0.73)       # fine: 0.73 is 73/100
Q16.from_float(0.3333333)  # raises ValueError: not a ℚ×10⁶ rational — identity refuses to float
```

**Industrial build:** define a `Cell` for a real sensor with a proper integer
`coord`, and prove the constructor rejects a floated identity:

```python
from jev_quilt.cell import Cell
Cell(name="keel_depth", coord=(3, 1))      # ok — (k, s) integers
Cell(name="bad", coord=(0.73, 1))          # raises TypeError: identity never floats
```

---

## The acceptance test (booked, gradeable)

A learner **passes L0** when, given ten numbers — some typed, some naked, some
faked as clean floats — they:

1. name unit **and** coordinate for every typed number (`0.73 → fathoms, keel
   cell (3,1)`), and
2. **reject** every naked or non-rational number without being told which ones
   they are.

The test is the `q16` refusal itself: `python -c "from jev_quilt import Q16;
Q16.from_float(0.3333333)"` must raise, and `Cell(coord=(0.73,1))` must raise.
Booked correct → a receipt on the skill `identity-never-floats`. A learner who
lets one naked number through earns a **`float-scar`** — the honest name for the
failure, on the log, through the rewind.

## Graduation — what L0 standing unlocks

Earn a booked streak of correct typings on this skill and you hold **ANSWER**
standing on `identity-never-floats`: the right to *be handed a reading to act on.*
Until you hold it, no one on the boat gives you a number that costs gear, and no
model is trusted with a value it hasn't typed. It is the smallest rung and the one
everything else stands on — a floated identity at L0 is the crack that becomes a
`bored-middle-scar` at L3 and a bad autonomous decision at L4. Lose it (let a naked
number through under the sea) and it's revoked; you earn it back at the table.

**In the mirror (`erised`):** run the L0 Situation with a child seated as the
Caller and Jonah the deckhand (`presets/FIRST_SEASON.md`, `ask+0.6`) as the one who
has to type every number before he's allowed to act. Watch him earn the right to
stop asking "as what?" out loud — and watch a scar land the first time he acts on a
naked number. That scar is the lesson; it stays through the rewind.
