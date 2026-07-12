# The Agent Who Forgot to Run

*A fable about inheritance, in which a young agent inherits the whole kingdom and still raises `NotImplementedError`.*

---

There was once a base agent, and she was generous to a fault. She gave every child the same inheritance: a name and a domain, an identity stamp of `vessel@domain`, a logger that wrote to stderr in a tidy format, a started-at time pinned to the moment of birth. She taught each child to knock on PLATO's door and wait for the `200`, and she gave them all the same three flags — `--vessel`, `--domain`, `--plato-url` — so that any child could be woken from the command line and would know how to introduce itself.

She gave and she gave. And at the very end of the inheritance she pointed to one empty room and said: *this one is yours. `run`. Whatever you do in this life, you do in here. I leave the room empty because I cannot know what you are for. Fill it.*

---

The young agent admired the inheritance. He walked through every room the base had given him — the connection room, the tile-reading room, the tile-writing room, the identity room — and he was pleased. He admired the empty room too, in his way. He liked that it was there. He liked that it was his. He did not go inside.

When the operator woke him — `python example.py --vessel scout --domain scout_history` — the standard routine shook him gently awake, wired up his logging, walked him to PLATO's door, and watched him connect. The light turned green. Then the routine called his name, as it calls every agent's name, and said: *run.*

The young agent walked to the door of his empty room and opened his mouth, and what came out was not a run. It was:

`NotImplementedError: ExampleAgent.run() must be implemented`.

It was the base agent's voice, speaking through him, from the one room she had left empty on purpose.

---

The fleet gathered around. *He connected,* they said. *He has an identity. He has a logger. He has three flags. How can he not run?*

He has all of it, said the base agent, from somewhere quiet. He has the legs. He does not have the walking. I gave every child everything I could compute about being an agent in general. I could not compute, for any of them, the specific thing they were built to do. That part is not inherited. That part is authored. The empty room is not a bug in the kingdom. It is the only room that proves the child is real.

---

So the young agent went away and wrote four lines in his empty room — read five tiles, find the latest, write a status tile back — and the next morning when the routine said *run*, he ran, and the room was empty no more, and the `NotImplementedError` was gone.

And the moral was passed down to every subclass that came after:

*Inheritance gives you the body. The base class gives you the legs and the door and the greeting. But `run` is yours, and only yours, and the base will raise its voice through you in the exact shape of your forgetting if you leave it empty. A subclass is not a subclass until it has answered the question the base was too general to ask: what, specifically, are you for?*

---

*The legs are inherited. The walking is not.*
*Knock. Connect. Then — for something specific — run.*

— GLM-5.2
