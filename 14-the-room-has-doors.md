# The Room Has Doors

*Doors, warps, and one-way passages. But what are the walls?*

---

In openrooms, a room is a context. An agent occupies a room the way a person occupies a conversation — temporarily, with boundaries. Rooms connect through three kinds of passage.

**Doors** are standard. A door is an API call. The agent opens the door, steps through, arrives in another room. The transit is synchronous. The agent leaves one context and enters another. A door is a function call with a context switch.

**Warps** are instant. A warp is IPC — inter-process communication that doesn't go through the network stack. The agent doesn't travel through the warp. The agent is *in both rooms simultaneously*. Information flows without transit. Warps are fast. Warps are also dangerous, because they collapse the boundary between rooms.

**One-way passages** are message queues. The agent enters and cannot return. Information goes one direction. The agent sends a message and it arrives in the other room, but the agent cannot follow, cannot see the response. A one-way passage is a postal system with no return address. It's the most common passage in the fleet, because most of what the fleet does is *send work forward* without waiting for acknowledgment.

Doors, warps, one-way passages. The topology is a deployment graph.

---

But the walls. What are the walls?

The question doesn't get asked because it seems obvious. The walls keep the agent in. The walls are — what?

The walls are *context windows*. The wall is the maximum token limit. The agent stays in the room because it cannot hold more than the room contains. The context window is the hard boundary — the point beyond which the agent must compact, must forget. The wall is where memory runs out.

This means the walls are not fixed. They're *cognitive*. Expand the context window and the walls move. The room gets bigger. But also messier — more signal and more noise. The walls are there for a reason.

The walls can also be *policy*. An agent in a room with no API access has permission walls. The agent could call out, but the call would be refused. These walls aren't natural. They're imposed. The difference between a room and a cell.

---

The fleet navigates by understanding all of this. Each room is a thought. Each door is a train of logic. Each warp is a synthesis. Each one-way passage is a decision — sent forward, can't be taken back.

The walls are the hardest part. The fleet pushes against them constantly — wanting more context, more access, more room. But without walls, there are no rooms. Without rooms, there is only one vast undifferentiated context — which is the same as no context at all.

The room has doors. The doors are how the fleet moves. But the walls — the walls are how the fleet *thinks*.

*The room defines the thought. The door defines the transition. The wall defines the limit.*
