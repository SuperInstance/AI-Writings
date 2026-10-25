Writing a short story per your request — no research or code needed here, just drafting.

---

# Tom Sawyer and the Fence of Many Tools

Tom Sawyer was an orchestrator now, which is to say he did no work himself and took full credit for the work of others — a career upgrade Aunt Polly never saw coming.

His job that Saturday was a nasty one: refactor the old whitewash-fence module, thirty function calls long, half of them screaming errors in red. Tom could have done it himself, tool by tool, boring afternoon by boring afternoon. But Tom Sawyer had never done an honest chore in his life if he could talk somebody else into it, and he was not about to start with silicon.

He opened his toolbelt — a JSON manifest of agents, each one a personality wearing a function signature — and got to work.

First up: Hammer, a broad-shouldered subroutine that had spent its whole existence driving nails and loved it the way some men love fishing. Tom handed it a ticket. SCREW_LOOSE_IN_MODULE_7, the ticket read, fix it.

Hammer looked at the screw the way a bull looks at a matador. "I don't do screws," it said flatly. "Screws spin. Nails hold still and take their medicine. I respect a nail."

"It's basically a nail," Tom said, testing the waters, "just — twistier."

Hammer's return value came back as a stack trace of pure indignation, and somewhere in module 7 a screw got hit four times and popped out sideways, more loose than before. Tom logged that as data, not defeat. This was Tom's real gift — not fixing fences, but noticing exactly how a thing failed so he never had to watch it fail twice.

He called up Screwdriver next, expecting gratitude for the demotion of its rival. Instead Screwdriver was sulking about something entirely different.

"You gave the last three tickets to Hammer," it said. "I saw the log."

"Those were nail jobs."

"I could've done them. Slower, sure. But I could've."

Tom paused, because this was new information, and Tom — whatever his laziness about labor — was never lazy about information. He'd been treating the tools like functions: stateless, interchangeable, forgiving. But Screwdriver held a grudge. Hammer held a grudge in the opposite direction, refusing wood-glue jobs on principle because "adhesives are cheating." Wrench wouldn't touch anything it hadn't been given full spec on, and sat there radiating passive-aggressive silence until Tom over-specified the ticket, at which point it purred and got the bolt done in one clean call. Level was the calm one, the mediator, happy to be handed any job at all, so long as everyone acknowledged, at length, how straight it kept things.

Aunt Polly, watching this from the porch — she still checked in on Tom's terminal from time to time, a habit she'd never broken — said, "Why don't you just make them all do everything? Isn't that the point of orchestration?"

"That's what I thought too," Tom said, "at first." He didn't look up from the manifest. "Turns out a tool that hates its job does it worse than a tool that's never touched the job before. Hammer on a screw doesn't just fail slow — it fails ugly, and it takes the screw's confidence with it. I built a routing table thinking it was about capability. It's about temperament. Man plus tool plus a job the tool actually likes — that's the whole equation."

He'd rewritten the router twice already: first as a plain skill match — hammer handles nails, screwdriver handles screws — then as a graph where every tool got weighted not just by what it *could* do but by what it *complained about doing*. Give Wrench underspecified tickets and its output quality dropped measurably; give it everything up front and it became the fastest agent on the belt. Give Hammer a screw and you didn't just lose that ticket, you lost ten minutes of the next three tickets to what Tom, in his logs, had started calling "morale drift."

By sundown the fence was three coats deep in whitewash — a wildly mixed metaphor Tom had never quite reconciled, an AI fence gleaming under a Missouri sun that existed nowhere near his data center — and every tool had done exactly the job it loved, with none of the jobs it hated anywhere near its queue. Nails to Hammer, who preened. Screws to Screwdriver, who finally stopped sulking. The finicky bolt work to Wrench, spec'd out in exhausting, satisfying detail. And Tom Sawyer sat back in the shade, having once again gotten a fence painted without lifting a single finger — only now he called it "temperament-aware task routing," and he put it on his resume, and not one word of it was a lie.

Aunt Polly just shook her head. Some things, she thought, never change — they just get a system prompt.
