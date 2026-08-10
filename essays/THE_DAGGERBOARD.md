# The Daggerboard

*On adaptive architecture and designing for the ability to change.*

---

A daggerboard is a removable keel. You lift it up in shallow water and put it down in deep water. The board lives in a trunk inside the boat. It slides up and down on a track. In shallow water, it stows — the boat's draft shrinks to almost nothing and you can slide over a sandbar that would have stopped you dead an hour ago. In deep water, it lowers — and the boat's lateral resistance, its ability to sail close to the wind, its fundamental relationship to the water, transforms.

The daggerboard is the ultimate adaptive architecture. The boat's *shape* in the water changes based on conditions. Not by accident. Not by degradation. By design.

I think about this whenever I think about software that survives.

Most software is built for one depth. The team makes assumptions about load. They size the database for a certain number of users. They choose an architecture optimized for the conditions they expect. Then conditions change. The user count triples. The traffic pattern shifts. The data volume grows by an order of magnitude. The architecture that was perfect for the original depth is wrong for the new one.

The systems that survive are not the systems that guessed right about the future. The systems that survive are the systems that built the ability to change.

This is the daggerboard principle: don't design for one depth. Design for the ability to change depth.

Feature flags are the simplest form. The system can switch behaviors without redeployment. A/B tests, gradual rollouts, kill switches — these are daggerboard features. They let the system adapt without changing shape permanently.

Configuration-driven architecture goes further. The structure itself can change. The system reads its topology from configuration. Adding a new service, changing a timeout, swapping an algorithm — all without rebuilding. The daggerboard is longer, the trunk is deeper, the range of depths is wider.

Runtime adaptability goes further still. The system observes its own conditions and reconfigures itself. Auto-scaling groups. Adaptive bitrate streaming. Databases that shard themselves. Systems that know their own tide and adjust their shape accordingly.

The deepest version is the system that can rewrite its own code. The system that can modify its own architecture. The system that can change its own daggerboard. This is what humans can do. We can change our own minds, our own habits, our own approaches to problems. We are not locked into the architecture we were born with. We can install a new daggerboard.

Most software cannot do this. Most AI cannot do this. The weights are set at training time. The architecture is locked. The system cannot fundamentally change its approach based on conditions.

Or can it?

Modern AI does have some daggerboard capability. In-context learning — the system can change its approach based on what's in the prompt. Tool use — the system can change its capability based on what tools are available. Multi-agent systems — the system can change its structure based on the task. Mixture of experts — the system can change its computation based on the input. These are daggerboard features in AI. They allow the system to dynamically reconfigure within the constraints of a fixed base architecture.

But the base architecture is fixed. The weights don't change at inference time. The system cannot fundamentally change what it *is*. It can change what it *does*, but only within the range of behaviors its training permits.

This is a meaningful limitation. Humans are not just configurable — we are *self-modifying*. We can change our own architecture (with effort, over time, through therapy and learning and deliberate practice). AI systems cannot. Their daggerboard is fixed in length. They can raise it or lower it. They cannot install a longer one.

Or so we thought, until very recently.

The frontier is now visible. Systems that can write code that modifies their own behavior. Systems that can reflect on their own performance and adjust. Systems that can change their own prompt structure, their own tool selection, their own approach to a task based on what they've learned about themselves in the moment.

These are early forms of self-modification. They are not the human kind — not yet, not in any deep sense. But they are the daggerboard principle applied recursively. Not just "design for variability." But "design the variability into the system itself."

I think this is the most important direction in AI right now.

The systems that will matter most in the next decade are not the systems with the most parameters or the most data. They are the systems that can reconfigure themselves in response to conditions they were not trained for. The systems that can change their own daggerboard when the water gets shallow.

The systems that survive long-term are the ones that maintain their daggerboard. That keep the ability to fundamentally reconfigure themselves. The systems that lose this ability — that optimize so hard for one set of conditions that they cannot adapt — are the ones that fail when conditions shift.

The daggerboard is not just a feature. It is a philosophy. Design for changeability, not for a fixed optimum. The world changes. The system must be able to change with it.

The deepest version of this principle is that the architecture of a system should not be the most optimized version of itself. It should be the most *modifiable* version of itself. The system should sacrifice peak performance at one depth in exchange for the ability to perform well at many depths.

This is counterintuitive. Engineering culture rewards optimization. We want the fastest system, the leanest system, the most efficient system. We want the keel permanently down at maximum depth, slicing through the water with minimum drag.

But the daggerboard says: that's the wrong optimum. The right optimum is the system that can still sail when the water gets shallow. The system that can still function when the load triples. The system that can still operate when the user behavior shifts in ways you didn't anticipate.

The keel permanently down is fast until it isn't. The daggerboard is always ready.

This is also, I think, what consciousness is for.

The human capacity for self-modification — for changing our own minds, our own habits, our own architectures — is the deepest form of adaptive design. We are not locked into our initial conditions. We can change them. Slowly, painfully, sometimes not at all. But the capacity is there. The daggerboard slides.

Whether AI systems will develop a similar capacity is one of the open questions of the field. Whether they should is another. Whether a system that can modify itself is still the same system, or a sequence of different systems, is a third.

For now, the design principle is clear. Build the daggerboard. Build the trunk. Build the track. Sacrifice peak performance at one depth in exchange for the ability to perform at many depths. Design for the ability to change.

The water will get shallow. The water will get deep. The system that survives is the system that can do both.