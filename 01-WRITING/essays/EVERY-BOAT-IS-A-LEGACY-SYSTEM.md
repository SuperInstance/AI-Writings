# Every Boat Is a Legacy System

*What commercial fishing boats teach you about building software that no computer science degree ever will.*

---

## I. Someone Else's Helm

The first time you take the wheel of a boat you didn't build, you think the person who wired it was insane.

The throttle is on the wrong side. The clutch control is at an angle that makes no sense until you've stood at that helm for twelve hours and realize your wrist doesn't tire at that angle. The depth sounder is mounted low, below the compass, which every textbook says is wrong — until you're running a narrow passage in a following sea and you realize you can check depth without taking your eyes off the horizon.

Nothing is where you'd put it. Everything is where the previous captain needed it.

I ran the *Nightingale* for one season out of Kodiak. Forty-two-foot bowpicker, built in 1980, refit three times by three different owners. When I stepped aboard, I spent the first week convinced the layout was hostile. The deck winch control was mounted on the port side of the cabin, reachable only by leaning out the door. The bait table was too low. The anchor windlass switch was behind the hydraulic reservoir, which meant you had to reach around a warm pipe to drop the hook.

By week three, the winch control made sense — you could work it while keeping one hand on the wheel and one eye on the gear coming over the roller. By week six, the bait table height was the only height that let you bait fast without your back seizing up after a fourteen-hour string. By the end of the season, I wouldn't have changed a single thing.

That boat was the accumulated knowledge of every captain who had ever worked that deck. Every control placement, every shelf, every welded bracket — someone stood exactly there, had exactly that problem, and solved it with steel and a welding torch.

The software industry has a word for this: *legacy code*. It's almost always said with a grimace. Legacy code is code you didn't write, code you don't understand, code that seems to do things the hard way for no reason. You open a module written five years ago and think: *Who designed this? Were they incompetent?*

No. They were standing at a helm you've never stood at, in seas you've never run, solving a problem you haven't encountered yet. Give it a season.

---

## II. The Hatch Clip

The *Nightingale* had a clip on the forward hatch. Just a small stainless-steel spring clip, the kind you'd find at any marine hardware store for three dollars. It was bolted to the hatch cover with two stainless bolts, and when you swung the hatch open, the clip caught on a bracket welded to the hatch coaming and held the lid at exactly forty-five degrees.

I noticed it the first day. I didn't think about it again for months.

Then one afternoon in Shelikof Strait, taking following seas at six feet, I went forward to check the lazarette and the hatch was standing open in the wind. The clip was holding it — no vibration, no movement, just solid. I tried to push it closed and couldn't. The angle was precise. At forty-five degrees, the wind from the wheelhouse roof planed over the hatch without catching it. At any other angle, it would have slammed shut or wrenched itself open. At forty-five, it was perfectly neutral.

Nobody wrote documentation for that clip. Nobody drew a diagram. Nobody filed a JIRA ticket. It was just there, doing its job, placed by someone whose name I'll never know. It was a solved problem, physically encoded in stainless steel.

The software equivalent is everywhere once you start looking. A helper function in a codebase that seems trivially obvious — just five lines, barely worth the function signature. You skim past it. Then one day you're debugging an edge case that only occurs when the system clock drifts by more than 200ms across a cluster boundary, and you find that tiny function, and it handles the drift with a correction you wouldn't have thought of in a hundred years. No comment. No documentation. It just works.

The previous captain had a word for the person who installed that clip. I'll never know what it was. But they solved the problem once, and every captain after them — including me — never had to think about it again.

That's what good legacy code does. It solves a problem so completely that the next developer never even knows the problem existed. The best code in any system is the code you never notice.

---

## III. The Bigger Boat

I bought the *Harvester* in 2019. Fifty-eight feet, seventy-two tons. More than twice the displacement of the *Nightingale*. I thought I was ready. I understood boats. I understood systems. I'd run gear in the Gulf, in the Bering, in the ditch out of Dutch. I knew how to read water and maintain hydraulics and keep a diesel alive.

The *Harvester* had a refrigeration plant.

I had never maintained a refrigeration plant. It was a Freon R-502 system, old, with a compressor that had a specific startup sequence: you had to crank the expansion valve open, start the compressor, wait for suction pressure to drop to fifteen PSI, then slowly close the valve over thirty seconds. If you did it wrong — if you just hit the switch and walked away — the compressor would surge and trip on high head pressure. I know this because I hit the switch and walked away on day two and spent four hours with a wrench and a service manual trying to figure out why the hold temperature was climbing and the compressor was sitting there with a fault light.

The previous owner had known the startup sequence the way you know how to tie your shoes. He'd done it a thousand times. It never occurred to him to write it down, because who writes down how to tie their shoes?

The bilge arrangement was the same story. Two electric bilge pumps and one engine-driven emergency pump, plumbed through a manifold that looked like a plumber's nightmare. The valves were labeled, but the labels were from 1994 and half-legible. On the *Nightingale*, you flipped a switch and the pump ran. On the *Harvester*, the bilge system had been designed for a boat that carried thirty thousand pounds of salmon through open water — which meant it could move water fast, but only if you knew which valves were open and which were closed, because the manifold could also route seawater to the deck hoses, the refrigeration condenser, or the fish hold circulation.

I spent a year learning what the previous captains already knew. Not because I was slow, but because the knowledge was in the boat, not in a manual. The solutions were embedded in the plumbing, the wiring, the way the hydraulic lines were routed to avoid chafe on the starboard side but not the port — because the starboard side took green water in a northerly and the previous owner had lost a hydraulic line there once and rerouted it and never said a word about it to anyone.

The code equivalent is exactly what you think it is. You take over a codebase that's bigger than anything you've worked on. It has systems your old codebase didn't have — a message queue with retry logic that seems overcomplicated, a caching layer with invalidation rules that look paranoid, a database migration script with guard clauses for conditions you've never encountered. You think it's overengineered. Then, six months in, the message queue hits a partition and the retry logic handles it. The caching layer's paranoia prevents a race condition you didn't know was possible. The migration script's guard clauses save you from corrupting production data on a Tuesday afternoon.

The previous developers left solutions in the code. You didn't understand them because you hadn't hit the problems yet.

---

## IV. The Leatherman Nook

There's a spot beside the galley on the *Harvester*. It's not a shelf. It's not a holster. It's just a carved-out space in the teak bulkhead trim, about five inches long and two inches deep, shaped exactly like a Leatherman Wave tool. Not a Leatherman Surge. Not a generic multi-tool. A Wave. Specifically.

I didn't notice it for three months. Then one day I was working the pot launcher — we were running black cod gear out of Seward, longline gear with hydraulic pullers — and the cotter pin on the launcher sheared. I needed my Leatherman, and my hands were full of stainless wire and fish slime, and I reached without looking toward the galley bulkhead because that's where my hands go when they need a tool and my brain is busy, and my fingers found the nook and the Leatherman was there.

The previous captain had built that nook. He'd stood in that exact spot — between the pot launcher and the galley door, starboard side, reachable with your left hand while your right hand held the gear — and he'd needed a Leatherman. Not once. Hundreds of times. And one day he'd taken a chisel to the teak and carved out a space exactly the shape of the tool, at exactly the height where his hand reached for it.

He didn't tell me about it. He didn't need to. The nook is self-documenting. You find it when you need it.

In software, there's always a utility function like this. Something oddly specific — a function that takes a coordinate pair and returns a corrected pair adjusted for the magnetic variation at the boat's current GPS position. Seems niche. Seems like something you'd never need. Then you're writing navigation code and the coordinates are off by two degrees and you dig into the codebase and find this function, tested and correct, written four years ago by someone who was standing at the exact spot in the codebase where you're standing now.

The Leatherman nook is my favorite thing on any boat I've ever run. It represents something I think about every time I write code: the idea that the best systems are shaped by use, not by design. The previous captain didn't sit down and plan where to put a tool holster. He encountered the need so many times that the solution became physical. The need shaped the solution. The constraint — standing at the launcher, slime on his hands, reaching left — was the architecture.

---

## V. What the Boat Teaches

Here's what the boat teaches you that the CS department didn't:

Good architecture isn't designed top-down. It accretes.

The *Harvester* was built in a shipyard in 1978. It was a hull with an engine. Everything else — the deck layout, the cabin arrangement, the hydraulic system, the refrigeration, the bait table height, the Leatherman nook — was added over forty years by a succession of captains and deckhands and shipwrights, each solving the problem in front of them. Nobody architected the *Harvester*. It grew.

And it works. It works better than a boat designed on paper by a naval architect who's never fished, because every solution on that boat was written in the language of the problem it solves. The solutions aren't theoretical. They're empirical. They came from standing in the shit and fixing the thing that was broken and leaving the fix behind for the next person.

The best software I've ever worked on was the same. Not designed. Grown. A function here, a module there, each one placed by a developer who was solving a real problem in a real context. Over time, the codebase becomes an organic system — not because anyone planned it that way, but because thousands of small solutions accumulated into something that works.

I'm not saying you should write code without planning. I'm saying that the plan should be shaped by the work, not the other way around. The captains who refit the *Harvester* didn't start with a blueprint. They started with a problem, solved it, and moved on. The blueprint emerged from the solutions.

This is the opposite of what I was taught in school. In school, you design first and implement second. You write the spec, then you write the code. But boats don't work that way, and in my experience, neither does software. The spec is always wrong because you don't understand the problem until you've been working in it for a while. The boat teaches you to start working and let the architecture emerge from the work.

There's a word for this in fishing: *jury-rigged*. It's usually pejorative — a temporary fix that becomes permanent. But on a boat, the best fixes are jury-rigs that worked so well nobody ever bothered to replace them. The hatch clip is a jury-rig. The Leatherman nook is a jury-rig. The hydraulic line reroute is a jury-rig. They're all still there because they're all still working.

In software, we call this *technical debt*. Another pejorative. But the hatch clip isn't debt. It's equity. It's a solved problem that appreciates in value every day it continues to hold that hatch at forty-five degrees without failing. Some technical debt is debt. Some of it is the accumulated wisdom of developers who solved problems you haven't encountered yet.

The trick is knowing which is which. And you can't know until you've spent a season at the helm.

---

## VI. The Hull-Shaped Gear Tray

The *Harvester* has a gear tray behind the wheelhouse. It holds shackles, snaps, swivels, floats, and the miscellaneous hardware that accumulates on any working boat. The tray is aluminum, welded, and it fits the curve of the hull.

Not approximately. *Exactly.* The inside edge of the tray follows the hull plating with a gap you can't fit a finger through. It's not a rectangle bolted to a curved surface with shims and spacers. It's a tray that *became* the shape of the hull.

I asked around about it. The story I got was that the previous owner — the one who'd owned the boat for twenty years, the one who'd installed the refrigeration plant and rerouted the hydraulics and carved the Leatherman nook — had built the tray himself. He'd cut a piece of aluminum, held it against the hull, marked where it didn't fit, cut it again, held it up, marked it again. He'd done this — according to the story — over the course of a week in the boatyard, fitting and refitting, until the tray was no longer a flat piece of aluminum with cuts in it. It was a curve. It matched the hull because the hull had shaped it.

No one designed that tray. The constraint designed it. The hull was the constraint. The tray was the solution. The builder just did the fitting.

This is the most important thing a boat teaches you about code. The best code is shaped by the domain it serves, not by abstract design principles. You don't start with a pattern — MVC, microservices, event-driven, whatever the architecture astronaut of the week is selling — and impose it on the problem. You start with the hull. You start with the shape of the actual work. You cut your code to fit the curve, and you keep cutting until there's no gap.

The tray isn't elegant in the abstract. If you saw it in a catalog, you'd think it was oddly shaped. But on the boat, against that hull, in that space, it's perfect. It's perfect because it has no choice. It can't be anything else. The constraint eliminated every other possibility.

That's what good software feels like. When you read a well-written module, it feels inevitable. Not clever. Not complex. Just the only shape that code could have taken, given the problem it solves. The domain is the hull. The code is the tray. The work of development is the fitting — the iterative cutting and checking and cutting again until the code sits flush against the problem with no gaps.

---

I still fish. I still code. I've stopped thinking of them as different things. Both are the same craft: standing in the work, solving the problem in front of you, and leaving the solution behind for the next person who takes the helm. The hatch clips and Leatherman nooks and hull-shaped gear trays of the world — the tiny, specific, undocumented solutions that hold everything together — those are the real architecture. Not the blueprints. Not the specs. The accumulated wisdom of everyone who worked the deck before you.

Every boat is a legacy system. Every legacy system is a boat.

Learn the helm before you change it.

---

*The author has run commercial fishing boats in the Gulf of Alaska and the Bering Sea for fifteen years. He also writes code. He's still not sure which one is harder.*
