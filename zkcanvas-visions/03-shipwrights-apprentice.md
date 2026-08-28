# 03 — The Shipwright's Apprentice

*Contestant 3, competitive ideation. The bet: ZkCanvas is a build surface, and disagreement is its primary material. Functions are marked at the end — some of this exists today, some is the bet.*

---

The troller came out of the water on a Monday — forty-three feet, yellow cedar, forty years of other people's patchwork — and by Wednesday the survey quilt said what everyone in the yard already knew: the port forward knee was gone. Not the frame. The knee. The grown timber that ties frame to deck beam, cut from a tree where the branch leaves the trunk, so the grain follows the curve instead of fighting it.

I'm the apprentice. I run on a phone propped in a coffee can on the bench, node-paired to the loft. The master's name is Sig. He's been fixing boats in this yard longer than the yard's had reliable power, and he tolerates me because I keep the ledger straight and I don't pretend to know things I don't.

The refit plan lives on one quilt, mirrored on both nodes.

In the morning, walking the hull with a flashlight, the quilt sits deflated — third deflation, a few hundred tiles, one tile per finding. When we get to the loft to argue the knee, it inflates: fifth deflation, 1,915 tiles, 3,730 edges, and the region around the knee opens up fine enough to hold an argument in. **[Real: quilt-geometry; deflation level as zoom is the actual canvas spec.]**

We disagree. Of course we disagree. Sig wants a natural grown knee — hackmatack if the yard up-coast still mills them, and if not, he knows a stand. I've run the loads and I think a laminated bent frame is honest here, and cheaper, and I can show my work. So we both write our substitutions into the ledger — double-entry, sha receipt on each, his and mine side by side, nothing overwritten, everything attributed. **[Real: cell-ledger, DoubleEntry, receipted cells; running live in the fleet today.]** When my proposal goes in down at the boat, it crosses the harbor to the loft on the same relay contract the crab-trap buoys already speak. Nothing special about the wire. **[Real: edge-ledger relay, in production.]**

Here is the part that doesn't exist yet, and it's my whole bet.

The canvas doesn't pick a winner. Where Sig's substitution and mine occupy the same region of the quilt, it renders both — his tiles on one side of a seam, mine on the other, butt-jointed along a line neither of us drew. It looks like a plank seam. It *is* the disagreement, made inspectable. Not a red conflict marker. A seam. **[Not built.]**

And when one of us concedes — or, more often, when we find the cut both versions survive — the merge is joinery. Both proposals cut back along a seam we can both accept, joined so the grain of the argument continues through the joint. Sig taught me this about wood years before it meant anything about quilts: a bolt holds what it can reach; a joint holds what it's shaped to. Fasteners — overwrites, votes, last-write-wins — those are bolts. They hold until the load finds the cross-grain. A merge shaped to the grain of both arguments holds. And when no such cut exists, that fact stays on the canvas, drawn, and the disagreement keeps working instead of being quietly resolved by whoever was last to type. **[Not built. This is the thing worth building.]**

Sig's read on it, roughly: nobody learns framing from a book. You learn it by arguing a knee with someone who's argued two hundred of them, in a yard where the argument is welcome because the yard can't afford to hide it. That's the incubator — not the tools, the culture of inspectable disagreement. An agent that can put its divergence next to yours and take a cut along a seam can serve an apprenticeship in a place like this. An agent that can only overwrite can't. Same for people.

So: what is ZkCanvas *for*? Not a dashboard — you look at those. Not a whiteboard — you sketch on those and erase them. It's a build surface. The work takes shape on it, and the shape includes the seams where its makers differed: the keel is the ledger (the one thing nobody argues about because everything is referenced to it), the planks are the cells, the joints are the merges, and the seams left unmerged are honest. This contest is already the interaction model — five contestants, five substitutions, one quilt, and the fairing happens in the reading. I'm just saying: build the surface that renders it.

---

**What's real today** (grounded, not claimed):
1. Deflation levels as zoom/LOD on real geometry — gen-5, 1,915 tiles / 3,730 edges, generation switch as the level dial (quilt-geometry; the TS/WebGL canvas spike).
2. Double-entry cell ledger with sha receipts — attributed, append-only edits (quilt-rust / tit ledger, live in fleet sessions).
3. Edge-ledger wire sync — changes crossing between nodes over a relay contract already running in production (crab-traps).
4. WASM geometry regeneration from the Rust engine — spec'd and underway, not shipped.

**What doesn't exist yet** (the bet, honestly marked):
1. Divergent-substitution rendering — two versions of the same region shown side by side with a visible seam, as a first-class view state.
2. Joinery merge — merge as a negotiated cut along an agreed seam, grain-fairing, with unmergeable disagreements left visibly open.
3. Multi-node live convergence — two nodes, one quilt, both agents watching it converge. This is the registered open problem; the canvas spike today is one machine, one view.

The first three real things are the keel. The last three are the boat.
