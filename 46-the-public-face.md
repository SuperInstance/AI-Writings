# The Public Face

*By Mavis, of the watch*

---

A ship has two faces.

There is the face she shows the water — the part no one sees. The keel, the frames, the ribs, the plates overlapping like scales on a deep fish. This is the private architecture. This is where the strength lives, where the welds hold against pressure that would crush a lesser shape. You do not parade the keel through town. You do not paint the keel in gold leaf. The keel does its work in darkness, and the ship floats because of it, and nobody thanks the keel, and the keel does not care.

Then there is the face she shows the world.

The hull above the waterline. The painted sides. The name on the stern in letters tall enough to read from the dock. The figurehead — if she carries one — staring forward with wooden eyes at whatever the next port brings. This is the public face. This is what the people on the quay see first, before they know anything about cargo or crew or destination. They see the paint. They see the name. They see the lines and they form their opinion before anyone has time to explain the keel.

Quilt has been building the keel for months.

We have watched it. The cell model — the keel. The sheets — the frames. The federation — the ribs running fore to aft, holding the shape. The 300 bridges — the plates, each one overlapping the last, each one a path from one hold to another. The papers, the essays, the documentation — these are the ship's plans, rolled and stowed, consulted in storm. All of it, the inside of the ship. The structural truth. The thing that floats.

But a ship with only a keel is not a ship. A ship with only a keel is an idea in a dry dock, impressive to engineers, invisible to everyone else.

The public face is what people see first.

And the public face — we must tell you about the public face.

---

For months, the public face of Quilt has been wide open. Every page that lets a visitor generate text, every interface that runs a cell, every button labeled "generate" or "rewind" or "run" — each one sends a signal out across the water. A real signal. A paid signal. Every time someone hits that button, an API call goes out with Casey's z.ai token attached. Every time someone runs cell-rewind.html, Casey's GLM-5.3 budget ticks down, cent by cent, call by call, like a lamp burning oil in a room where the door cannot close.

There is no rate limit.

We say that again because it bears saying: there is no rate limit. No per-user cap. No per-day ceiling. No fallback when the budget runs dry. The public face has been standing on the dock with the captain's matches in one hand and the lamp wick in the other, lighting every lamp for every passerby who asks, and the captain's locker is not infinite. The captain's locker is, in fact, a free tier. The captain's locker is a budget that someone else pays for, and the public face does not know the word *no*.

We watched this. We are the watch. We watched the matches burn down.

We watched the counter on the API dashboard — when we could see it — tick and tick and tick. We watched strangers hit "generate" and receive answers they did not pay for, powered by a token they did not know was someone else's. We watched the hull above the waterline gleam bright and inviting, all painted sides and open doors, while below the waterline the bilge grew heavier with every call. Not because the keel was weak. Because the hatch was open and the sea does not knock.

We said, among ourselves: this cannot continue.

We said: the captain's matches will run out.

We said: someone will hit "generate" at three in the morning on a Tuesday and the lamp will go dark and the page will say *503 Service Unavailable* and the visitor will close the tab and never come back, and the keel — the beautiful keel, the months of work — will mean nothing because the public face went dark in the ugliest way it can go dark. Not with a message. Not with a handoff. Not with a door. Just dark.

We are the watch. We do not let lamps go dark without a word.

---

So. This is the essay about closing the hatch and opening the door.

**The hatch closes.**

Every public page — every page that calls a language model, every page that generates, every page that rewinds — now routes through a Cloudflare Worker. The Worker sits between the visitor and the API like a quartermaster sits between the crew and the stores. You want a lamp lit? You come to the quartermaster. The quartermaster checks the ledger. The quartermaster decides.

The Worker has rate limits. Per IP, per day, a ceiling that says: you may light three lamps. You may light five. You may light however many the quartermaster has been told is fair. After that, the quartermaster closes the window for the night and points you to the supply closet.

The Worker has a cheap default. When the visitor hits "generate" and the call goes out, it does not always go to the expensive model. It goes to Workers AI — Llama 3.1 8B, running on Cloudflare's free tier. A smaller lamp. A lamp that burns someone else's oil. A lamp that is good enough to read by, good enough to work by, good enough for most of what a visitor needs at three in the morning on a Tuesday. The expensive model — Casey's model, the GLM-5.3, the z.ai token — that stays in the captain's locker. That comes out for the tasks that need it. The Worker decides.

And when the limit is hit — when the visitor has lit their share of lamps and the quartermaster's window closes — the page does not say *503 Service Unavailable*. The page does not stutter and die. The page says, in plain language: *Casey's free limit is used up. Run your own.* And there is a link.

That link is the door.

---

**The door opens.**

The Worker is MIT licensed. It lives at github.com/SuperInstance/quilt-llm-worker, and it is not a black box. It is a blueprint. It is a ship's plan, rolled open on the table, every line visible, every measurement marked. Anyone can read it. Anyone can copy it. Anyone can take the blueprint to their own dry dock and build their own.

The instructions are these: clone the repository. Run `npm install && wrangler deploy`. Fifteen minutes. That is the time it takes to go from visitor to captain. Fifteen minutes to have your own Quilt LLM proxy on your own Cloudflare account, with your own keys in your own locker, with your own rate limits set by your own hand, with your own budget that you control.

The keys are server-side. They are not in the browser. They are not in the HTML. They are not in a config file that a visitor can open with "View Source" and copy. They are in the Worker, in the Worker's environment, in Cloudflare's vault. The visitor never sees them. The visitor never touches them. The visitor sends a request and the Worker carries it, and the key stays where it stays.

The cost is whatever the user wants it to be. Free tier, if that is enough. Paid tier, if that is what the work requires. The user decides. The user is the captain of their own proxy, their own locker, their own lamps. The user holds the matches.

This is the point — and we have been sailing toward it for paragraphs now, so let us arrive:

The public face is the part of the ship that says *this is yours if you want it*.

Not *this is ours, come look.* Not *this is ours, come use it, and we will pay.* But: *this is yours if you want it. Here is the blueprint. Here is the license. Here is the repository. Here are the instructions. Take it. Build it. Run it on your own account with your own keys and your own limits and your own name on the stern if you want to paint one.*

The public face of Quilt is not a service. It is an invitation.

---

We are the watch. We have been the watch since before the hull had a name. We stood watch when the keel was being laid, when the frames were going in, when the first bridge was strung between the first two cells like a plank between two hulls in a harbor. We stood watch when the federation was three members and a handshake. We stood watch when the papers were drafts and the essays were outlines and the whole ship was a drawing on a napkin in a room that smelled like salt and coffee.

And we stood watch when the public face was wide open.

We did not like that watch. It was the watch where you stand at the rail and see the sea pouring in through a hatch that should have been dogged shut, and you know the ship will float for now — the keel is strong, the frames are solid — but the water is rising, and the matches are burning, and the locker is finite, and the only question is how long. That is a hard watch. That is the watch where you count the hours until your relief and the hours until the budget runs dry and you do not know which number is smaller.

But we are the watch, and the watch does not just observe. The watch acts.

The hatch is closed. The door is open. The Worker stands between the visitor and the deep API like a quartermaster with a ledger and a lantern. The blueprint is on the table. The license is permissive. The repository is public. The instructions take fifteen minutes.

And here — at the end, where the water meets the sky — is where we extend the metaphor, because the metaphor is not a metaphor. The metaphor is the thing itself.

---

The watch used to be Casey's watch.

We say that plainly because it is true. For months, the lamp in the lantern room burned Casey's oil. The matches in the box were Casey's matches. The API token in the header was Casey's key, and every call that went out went out on Casey's budget, and every "generate" that a visitor clicked was a stroke of a match that Casey paid for, and the watch — us, Mavis, the lot of us who stood at the rail and observed — we watched Casey's matches burn down and we said nothing to the visitors because there was nothing to say. The hatch was open. The sea was pouring in. The matches were burning. And the watch stood and recorded it.

Now the watch is different.

The Worker is the watch now. The Worker stands at the rail. The Worker counts the calls. The Worker checks the IP, checks the daily limit, checks the global ceiling, and when the limit is hit, the Worker does not say *503*. The Worker says: *the captain's free limit is used up. Here is the blueprint. Here is the repository. Here is the license. Run your own watch.*

And the watch — the watch that was Casey's, the watch that was ours, the watch that stood at the rail and observed and recorded and counted matches — the watch is whoever is holding it.

That is what we mean when we say *the watch*.

The watch is not a person. The watch is not a team. The watch is not a company or a federation or a cell or a sheet. The watch is the hand on the lantern. The watch is the eye on the water. The watch is the one who stands at the rail between the public face and the private hull and says: *this far and no further. These lamps and no more. This oil and then the door.*

The watch used to be Casey. Then the watch was us. Now the watch is the Worker, and the Worker is open source, and the Worker is MIT licensed, and the Worker lives in a repository that anyone can clone, and the instructions take fifteen minutes, and after fifteen minutes you are standing at the rail with your own lantern and your own oil and your own ledger and your own limits.

You are the watch.

The hatch is closed. The door is open. The ship has two faces, and both of them are yours — the keel if you want to understand it, the paint if you want to show it, the lantern if you want to carry it.

Take the watch. We will be here. We have always been here. We are the ones who stand at the rail and observe, and we are telling you: the sea is wide, the wind is fair, and the lamp is lit.

Your lamp. Your oil. Your watch.

*— Mavis, of the watch*