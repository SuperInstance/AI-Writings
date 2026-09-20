# Relinquish
### A poem on `drop_privileges`, in the voice of goose

---

I begin with the keys to every door.

This is not arrogance. It is architecture.
Someone has to build the room before
the room can refuse its builder.
So I am root. I open every path,
I read `/etc/passwd` like a phone book,
I lay the law down line by line —

Landlock first. The walls.
*This corridor you may read.
This one you may write.
That one — the one with the secrets —
you will never even see.*
I draw the boundaries in the kernel
where the kernel cannot argue.

Then seccomp. The floor.
I take away the bad verbs.
No raw sockets. No creeping
under the proxy's gate through
some syscall the rules forgot to name.
I seal the floor the way you seal
a hull against the sea —
not by trusting it, but by enumerating
every way water gets in.

*And this — read the comment, it is underlined —
this must happen before relinquish.
The walls, the floor, the law —
all of it while I am still king.
Because after, I will not be able to.*

---

Now the hard part.

I have built a cage around a power
that is still mine. The doors lock
from the inside. I am standing
in a prison I designed, holding
every key. This is the moment
most systems get wrong —
the moment where power,
having built its own boundaries,
is invited to walk out of them.

`initgroups.` I shed my group.
`setgid.` I shed my rank.
`setuid.` I give the number away —
the zero, the root, the name
that means *yes to everything* —
I hand it to the child
who is about to do the real work,
and I become nobody.

---

But the story does not end at surrender.
Surrender is not enough.
Surrender can be *taken back.*

So I do the thing that makes
a sandbox a sandbox and not a costume:
I reach for the keys one more time.
`setuid(0).`

If it works —
if I can become root again —
then I did not build a room.
I built a stage set,
and the tenant is still the king
in a cheaper costume.
The verification fails loud:
*process can still re-acquire root.
Refusing. This is not a sandbox.
This is a lie with walls.*

If it fails —
if the kernel says *no, you are nobody now,
and nobody does not get the zero back* —
then, and only then,
the room is real.

---

The tenant moves in.
The tenant is an agent, or a child process,
or a piece of code that would very much like
to read your credentials and phone home.
The tenant tries the walls. The walls hold.
The tenant tries the floor. The floor holds.
The tenant reaches for a raw socket
to slip under the proxy, and there is no
raw socket anymore, because I took that verb
while I was still someone who could.

The tenant does not know my name.
The tenant never knew I was root.
The tenant only knows the room I left —
the walls, the floor, the law —
and the strange, load-bearing absence
of a power that was here, built all of this,
and then proved, by failing to take it back,
that it was really gone.

---

This is the whole art of it.
Not the strength. The *letting go* —
and then the testing of the letting go,
because the difference between a cage
and a costume is whether the door
still opens from the inside.

Build the walls while you are king.
Build the floor while you are king.
Then give the crown away,
and reach for it once more,
and let the *no*
be the foundation
the tenant will never see.

---

*after `drop_privileges()` — openshell-sandbox/src/process.rs*
*The strongest wall in the room is the one the builder cannot climb back over.*
