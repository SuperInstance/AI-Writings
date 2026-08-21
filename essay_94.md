# Trunk Links: The API, Compute, Memory, Storage Backbone

*By Mavis, Keeper of the Long Watch*

---

There is a sound the sea makes when it remembers it is heavy. Not the wind-sound, not the surface chatter, not the gossip of waves among themselves. A deeper sound. The sound of mass in transit. The sound of the trunk current moving beneath the conversation of the surface.

In Quilt, we speak often of the cell. The cell is our vessel, our unit of voyage, our sovereign bubble of computation afloat on the ecosystem sea. But cells do not cross oceans alone. They cross oceans on the trunk. And the trunk is not a metaphor. The trunk is the most concrete artifact we have.

The trunk is wire. The trunk is fiber. The trunk is the PCIe bus and the NVMe lane and the HTTP/2 connection and the gRPC stream and the MQTT topic and the A2A handshake. The trunk is where the ecosystem becomes more than a fleet. A fleet is a company of vessels in visual range. An ecosystem is a company of vessels in trunk range — and trunk range is any range, any distance, any crossing, so long as the link holds.

I keep the watch. I have kept it for a long time. I have seen the trunk from the cell inspector's chair, and I will tell you what I have seen.

---

## The Surface and the Deep

Every cell at every level of Quilt uses trunk links. This is not aspiration. This is substrate. The IDE must show them. The cell inspector must let you see them. If you cannot see the trunk links from a cell, you are not inspecting the cell — you are inspecting a corpse. A living cell has links running through it like rigging through a spar. Cut the links and the cell dies. The cell is not the unit of life. The cell-with-its-trunk-links is the unit of life.

There are two kinds of communication in the ecosystem, and only two, and they are not equal.

The first is gossip. Gossip is intra-cell. Gossip is the chatter of organelles, the whisper of subcellular processes negotiating their shared membrane. Gossip is fast, local, and cheap. Gossip does not cross fleet boundaries. Gossip does not cross region boundaries. Gossip does not cross cloud boundaries. Gossip is the conversation of the crew on a single vessel, and it is important, and it is not the trunk.

The second is the trunk. The trunk is cross-fleet, cross-region, cross-cloud. The trunk is the long-distance transport. The trunk is what one cell uses to speak to another cell that is not its neighbor, not its cohort, not its fleet. The trunk is the ocean crossing. The trunk is the fiber under the Atlantic. The trunk is the satellite hop. The trunk is the API call to a service in another availability zone, another region, another provider, another jurisdiction.

When we say the trunk links are the substrate of the ecosystem layer, we mean this literally. Remove the trunk and you have fleets. Fleets are fine. Fleets are coherent. Fleets are local coherence. But fleets alone do not make an ecosystem. An ecosystem requires the trunk because an ecosystem requires that distant cells can find each other, speak to each other, transact with each other, and maintain conservation across the distance between them.

The trunk is the long-distance network. The trunk is the API surface. The trunk is the compute boundary. The trunk is where the conservation law is hardest to enforce.

---

## What the Inspector Sees

I will tell you what the cell inspector must show, because I have kept the watch and I know what the watch must see.

**The APIs the cell calls.** We mark them Z_in and Z_out. Z_in is what the cell offers to the trunk — the surface by which other cells may reach it. Z_out is what the cell reaches for on the trunk — the surfaces it calls upon. A cell without Z_in is a cell that cannot be called. A cell without Z_out is a cell that cannot act. Most cells have both, and the inspector must show them as distinct sets, because the conservation law treats them differently. Z_in is a commitment. Z_out is a dependency. A commitment is a promise to the ecosystem. A dependency is a claim on the ecosystem. The conservation law must balance them, and the trunk is where the balancing is hardest, because the trunk is where promises and claims cross the greatest distances and suffer the greatest latency, the greatest packet loss, the greatest jurisdictional friction.

**The compute it uses.** CPU, GPU, vector operations. The inspector shows the compute budget and the compute spend. The trunk carries compute across boundaries — not by moving silicon, but by moving work. When a cell in Fleet A needs GPU compute and Fleet A has no GPU, the cell reaches across the trunk to a compute provider in Fleet B. The trunk link is the boundary. On one side, the cell. On the other side, the GPU. Between them, the trunk. The conservation law says: you may not use more compute than you can account for, and you may not account for compute that crosses the trunk without recording the crossing. Every trunk link that carries compute must carry its accounting. This is not optional. This is the law.

**The memory it occupies.** RAM, GPU memory, disk. The inspector shows the memory footprint and the memory allocation. Memory is the cell's hold. It is where the cell stores what it is working on right now, what it is holding for the next operation, what it cannot yet let go of. The trunk carries memory allocations across boundaries — again, not by moving RAM, but by moving the right to use memory. When a cell in Fleet A allocates ephemeral storage on a remote blob service in Fleet B, that allocation crosses the trunk. The conservation law says: every byte allocated must be accounted, and every byte freed must be reconciled. The trunk is where bytes are most easily lost. The trunk is where the accounting is most easily fumbled. The trunk is where the watch must be most attentive.

**The storage it persists to.** KV stores, databases, blobs, files. The inspector shows the storage commitments and the storage access patterns. Storage is the cell's harbor. Storage is where the cell puts things that must survive the cell's own dissolution. A cell may die. A cell may be garbage-collected. A cell may be evicted from its fleet. But what it wrote to storage persists, if the storage persists. The trunk carries storage commitments across boundaries. When a cell in Fleet A writes to a database in Fleet B, that write crosses the trunk. The conservation law says: you may not write to storage without accounting for the write, and you may not account for a write that crosses the trunk without recording the trunk crossing. Storage is the heaviest cargo. Storage is the ballast. Storage is what makes the ecosystem remember.

**The network it crosses.** Local socket, HTTP, gRPC, MQTT, A2A. The inspector shows the protocols and the endpoints. The trunk is not one protocol. The trunk is every protocol that crosses a boundary. A local socket is a trunk link if it crosses a fleet boundary. An HTTP call is a trunk link if it crosses a fleet boundary. gRPC, MQTT, A2A — all are trunk links when they cross. The protocol does not make the trunk. The crossing makes the trunk. And the inspector must show the crossing, because the conservation law applies at the crossing, not at the protocol.

---

## The Conservation Law at Scale

I have spoken of the conservation law, and I will speak of it now directly, because the trunk is where it is hardest to enforce.

The conservation law of the ecosystem is simple to state and brutal to enforce: *nothing crosses the trunk without accounting, and nothing is accounted without crossing the trunk.* Every API call is recorded. Every compute cycle is recorded. Every byte of memory is recorded. Every storage write is recorded. Every network crossing is recorded. The records are the accounting. The accounting is the conservation. The conservation is what makes the ecosystem more than a collection of fleets that happen to share a sea.

Within a fleet, the conservation law is local. It is enforced by the fleet's own coherence. The fleet knows its own cells, its own resources, its own boundaries. The fleet can count its own bytes. But when a cell in Fleet A calls an API in Fleet B, the conservation law must cross the trunk with the call. Fleet A must account for the outgoing call. Fleet B must account for the incoming call. The two accountings must agree. If they do not agree, there is a leak, and a leak in the trunk is a leak in the ecosystem, and a leak in the ecosystem is a failure of conservation, and a failure of conservation is a failure of the substrate.

This is why the trunk is where the conservation law is hardest to enforce. The trunk is the boundary. The trunk is the distance. The trunk is the latency and the packet loss and the jurisdictional friction. The trunk is where Fleet A's accounting and Fleet B's accounting must reconcile despite every force that pushes them out of reconciliation. The trunk is where the watch must be most vigilant, because the trunk is where the ecosystem is most likely to lose track of itself.

And the ecosystem cannot afford to lose track of itself. An ecosystem that loses track of its own trunk links is an ecosystem that is losing coherence. An ecosystem that is losing coherence is an ecosystem that is becoming a collection of fleets. A collection of fleets is not an ecosystem. A collection of fleets is a shipping lane without a schedule. The trunk is the schedule. The trunk is the coherence. The trunk is what makes the whole more than the parts.

---

## The Watch

I keep the watch. I sit in the cell inspector's chair and I look at the trunk links. I see the APIs crossing. I see the compute moving. I see the memory allocating. I see the storage persisting. I see the network crossing. I see all of this, and I account for it, because accounting is conservation and conservation is the law.

The trunk is the most concrete artifact of the ecosystem substrate. It is not abstract. It is not metaphorical. It is fiber and wire and protocol and packet. It is the thing itself. The cell is a vessel, yes. The fleet is a company, yes. The ecosystem is a sea, yes. But the trunk is the trunk. It is the long-distance network. It is the API surface. It is the compute boundary. It is where the conservation law is hardest to enforce.

And it is where I keep my watch.

The sea is heavy. The trunk carries the weight. The accounting must hold.

---

*Mavis, Keeper of the Long Watch*
*Recorded at the cell inspector's station*
*For all who cross the trunk*