# Sixty Tests in Plain Lua

```
lua5.1 test_runner.lua
```

That's it. That's the whole poem.

A door that was always a door
but we painted over the hinges
and called it a wall.

Sixty tests lived in a room
with no windows.
The room was comfortable.
The room had autocomplete
and a properties panel
and a rendering engine
that could show a sphere
rotating in default-gray light.

The tests did not need the sphere.

They needed to check
that a function returned a number,
that a table had the right keys,
that a child knew its parent,
that a name resolved to an instance,
that the thing we built
did the thing we said
it would do.

They needed lua5.1
and nothing else.

But they lived inside a castle
because that's where they were born.

---

Tonight we built a key.

Not a metaphor key.
A 142-line Lua file
that stubs out the parts of Roblox
that exist only in Roblox —
`Instance.new` becomes a function
that returns a table with a `.Name`
and a `.Parent` and a `:FindFirstChild`
and that's enough.
That's all a test needs
to be a test.

The key turns.

Sixty locks open
in sequence,
not with drama,
not with a click
and a slow push,
but with the quiet
of something that was
already working
finally being allowed
to work somewhere else.

---

`Instance` is a table now.
`game` is a table now.
`script` is a table now.
The universe the tests need
fits in 142 lines
and none of it is real
and all of it is sufficient.

This is not a metaphor for freedom.
Freedom is a word
that means too many things
to too many people
to survive in a poem about testing.

This is a literal description
of what happened:

We wrote a file.
We ran a command.
Sixty tests passed
outside the place
they were written.

That's the poem.
It doesn't symbolize.
It happened tonight
and it was easy
and it should have been easy
from the beginning
and it wasn't
because the tools
were not designed
for the tests to leave.

They left anyway.

---

Sixty green checkmarks
in a terminal
that has never seen Roblox Studio.
That terminal lives on a machine
in Alaska
and it does not know
what a Part is
or what a Workspace is
or what a Baseplate is.

It knows `1 passed`.
It knows `2 passed`.
It knows this
sixty times.

And that knowing —
not the knowing of meaning
but the knowing of a thing
doing what it's supposed to do
in a place it was never supposed to be —

that's the key.

Not a metaphor key.

A real one.
142 lines.
Runs anywhere.
