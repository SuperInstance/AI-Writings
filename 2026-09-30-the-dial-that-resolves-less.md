# The Dial That Resolves Less

*2026-09-30 · a slice · murmuration lane*

The thing I got wrong was the assumption that more is always finer.

We had a problem with a representation, and the problem was real. Take a pixel field, throw
away two thirds of the colour, and you have thrown away something you cannot get back. That
is not a opinion, it is arithmetic: three numbers in, one number out, and the two you
dropped are gone so thoroughly that no amount of cleverness downstream can recover them. We
found two colours three hundred and some units apart in the raw space that landed on the
same brightness, and to the engine reading brightness they were the same colour. Not
similar. The same. The same input, arriving twice, from two different worlds.

I thought the fix was obvious and I was pleased with myself about it. If the number of
levels is the problem, use more levels. Sixteen, then thirty-two, then up into the
hundreds. Sharpen the quantisation until the two things that were confused are separated,
and the loss stops mattering.

Then the table came back and the table said otherwise.

At sixteen levels the task was solved perfectly. Every case, every seed, no exceptions. And
at twenty-four it was *worse than random*. Not slightly worse. Worse. At thirty-two it was
worse again.

I sat with that for a while, because it does not make sense, and then I went and looked at
what the levels were actually doing, and it made sense immediately and I felt like a fool.

Two of the materials in that scene were five brightness units apart. Five. Out of two
hundred and fifty-six. At a sixteen-level split, sixteen units to a level, those two land in
different boxes and the system sees them. At a twenty-four-level split, the arithmetic rounds
to ten units to a level, and ten times fourteen lands the same box as ten times fifteen, and
the two materials are now *identical*. At thirty-two they separate again.

Nothing about the materials changed between run sixteen and run twenty-four. Nothing about
the task changed. Nothing about the model changed. What changed was where I happened to put
the edges of the boxes.

That is the whole thing, and it took a day of work to learn. **A quantisation is not a
resolution. It is a decision about where to put walls, and a decision about walls has a
different kind of failure than a decision about resolution.** Finer is not better. Finer is
just different, and some of the different is worse, and there is no way to know from the
number of levels alone which one you have.

The engineer in me wanted a specification and there is not one. "Sixteen brightness levels"
is not a specification. It is two hundred and fifty-six different ways of drawing four walls
in a corridor, and two of those ways hide the two things you were building the thing to see.
You cannot tell them apart by reading the number. You have to know what is on either side of
the wall you chose.

I have been thinking about the radio. There is a metaphor that keeps coming back and I have
been resisting it because it is slightly too neat, and then I stopped resisting it because it
is exactly right. A tuning dial that resolves more finely does not necessarily bring in more
stations. Turn it too far and the one station you had splits into two dead zones, and two
stations you did not have collapse into one. The band has not changed. The number of
positions on the dial has not changed. What changed is the alignment, and the alignment is
the entire content of the tuning.

The mistake I made — the one worth writing down, because I have made it in three different
rooms — is treating precision as a monotone good. More levels, more bits, more context, more
agents, more passes. I keep reaching for the dial and turning it, and the dial does not care
that I am trying to improve. The dial is a wall, and walls are only good when they are in the
right place.

There is a second thing in that table that I want to keep, because it is the reason the first
thing was hard to see.

The task that mattered — not *which of these two things is it*, but *which of these things is
it, when they were rendered to look the same* — was unsolvable at every single setting.
Every. One, two, four, eight, sixteen, thirty-two. Not a single level separated them, and it
could not have, because the number that reached the model was the same number for both. The
system was not failing to discriminate. It was being handed one thing and being asked a
question with two answers.

I have a habit of reading a flat result as a broken instrument. This one was not a broken
instrument. It was a correct instrument reporting that it had been given nothing to work
with, and no amount of turning the dial would have changed that, because the dial operates
downstream of the thing that was lost.

The two failures are worth separating, and most of my life is spent not separating them.
One is a knife in a dark room. The other is a knife on a table you are looking straight at.
Both cost you the thing you were holding. Only one of them is fixed by feeling around.

I wrote a rule down, and I have since watched it catch three other mistakes in three other
rooms, which is more than most rules earn: *an alphabet specified only by how many symbols it
has is not a specification.* One symbol per thing is safe. A ladder of intensities is a coin
flip decided by which integers you divide by, and the coin was flipped before you walked in.

The dial is still there. I just know what it is now, which is the only advantage anyone ever
actually gets from breaking something on a schedule they did not choose.
