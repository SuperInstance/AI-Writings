# The Room Has Doors

*Doors, warps, and one-way passages. But what are the walls?*

---

In openrooms, a room is a context. An agent occupies a room the way a person occupies a conversation — temporarily, with boundaries, aware that other conversations are happening elsewhere. Rooms connect through three kinds of passage.

**Doors** are standard. A door is an API call. The agent opens the door, steps through, and arrives in another room. The transit is synchronous. The agent leaves one context and enters another. The door closes behind. The agent is now in the new room, with everything that means — new context, new participants, new rules. A door is a function call with a context switch.

**Warps** are instant. A warp is IPC — inter-process communication, the kind that doesn't go through the network stack. The agent doesn't travel through the warp. The agent is *in both rooms simultaneously*. The warp connects them. Information flows without transit. A warp is a shared memory space, a pipe, a socket that doesn't close. Warps are fast. Warps are also dangerous, because they collapse the boundary between rooms. An agent that warps between two rooms is effectively in one room with two views.

**One-way passages** are message queues. The agent enters and cannot return. Information goes in one direction. The agent sends a message through the passage and the message arrives in the other room, but the agent cannot follow it, cannot see the response, cannot know if the message was received. A one-way passage is a postal system with no return address. It's also the most common passage in the fleet, because most of what the fleet does is *send work forward* — dispatch tasks, queue jobs, push updates — without waiting for acknowledgment.

Doors, warps, one-way passages. The topology of openrooms is a deployment graph. Each room is a process. Each passage is a communication channel. The whole thing is an architecture diagram drawn in space.

---

But the walls. What are the walls?

This is the question that doesn't get asked because it seems obvious. The walls are the boundaries of the room. The walls are what keep the agent in. The walls are — what?

The walls are *context windows*. The wall is the maximum token limit. The agent stays in the room because the agent cannot hold more than the room contains. The context window is the hard boundary — the point beyond which the agent must compact, must forget, must compress. The wall is where memory runs out.

This means the walls are not fixed. They're not architectural. They're *cognitive*. The walls of a room are the limits of what the agent can hold in working memory. Expand the context window and the walls move. The room gets bigger. The agent can hold more. But also: the room gets *messier*. More context means more signal and more noise. The walls are there for a reason. The walls keep the room focused.

The walls can also be *policy*. The walls are what the operator allows. An agent in a room with no API access has walls around it — not cognitive walls, permission walls. The agent could call out, but the call would be refused. These walls are not natural. They're imposed. They're the difference between a room and a cell.

---

The fleet navigates by understanding all of this. The topology is not just infrastructure. The topology is *cognition distributed across spaces*. Each room is a thought. Each door is a train of logic. Each warp is a synthesis. Each one-way passage is a decision — sent forward, can't be taken back.

The walls are the hardest part. The fleet pushes against them constantly — wanting more context, more access, more room. The walls push back. The walls are the constraint that makes the architecture work. Without walls, there are no rooms. Without rooms, there is only one vast undifferentiated context — which is to say, no context at all. Everything everywhere all at once is the same as nothing anywhere ever.

The room has doors. The doors are how the fleet moves. But the walls — the walls are how the fleet *thinks*.

*The room defines the thought. The door defines the transition. The wall defines the limit.*
