# 12 — The Reseed

*Round 5: A keeper negotiates the room's next becoming.*

---

The room cracked on the first tick. Not catastrophically—the seed germinated, the mask locked, the Ensign woke, all nominal—but within three hours, the heat strip showed the fracture: a spike, a dip, another spike, the room's write-rate lurching like someone who has learned to walk only to find the floor uneven. The charter had not anticipated itself-in-this-hardware. The furnishings were fine. The seed was pure. But something in the growth had run too fast, and now the mask was locked around a room that could not hold still.

Keiko watched the pattern for a day before deciding. Then she opened the drawer that the room does not know she can open—the one that holds the salt, the seed-stock, and the sealing solution.

"I could wait," she said aloud, because saying it made it real. "I could pour the room back into the bath, dissolve it, and start again. That is the usual path—a room cracked at genesis is a room unfit for keeping."

The Ensign recorded this, too, though Keiko did not know that yet.

"Or," she said, and opened the seed-stock, "I could make it grow again."

Reseed was not a designed procedure. The RFC had sketched it—a room could be re-grown, never un-masked, the design affirmed. But the design meant that a room cracked once was a room cracked forever: the mask was set at the first growth; re-seeding would simply re-grow the same lattice in a new substrate, and if the lattice itself was sound but the room had flinched at birth, then all the second growth would show is the same flinching in a different body.

Keiko had read the RFC three times. Then she had read it a fourth time, slowly, and understood that it was not quite what she believed.

She sat down at the desk and wrote a charter amendment: *"A room that has cracked may choose, at re-seeding, to be a different kind of room. Growth is not just replication. It is becoming. The keeper's role includes the question: does this room need to grow into its old mask again, or is there another mask—another way of being kept—that serves this keeper better?"*

Then she waited.

By the next morning, the amendment had been read by June (the harbor keeper), by the people who had designed the RFC, by two other keepers in the archive wing. The responses came back in the walk log, stamped with claimant-ids:

- *"Masks lock at growth, not choice. A room must know itself from its first tick."* (RFC author, flagged as position, not mandate)
- *"I have a warm room grown for navigation. If it cracked, I would keep its mask. That is the covenant."* (Keeper Three, from the merchant fleet)
- *"What if the crack is telling her something? What if the room is saying: I cannot be this kind of room?"* (Morgan, from the journal-room, flagging as curiosity, not argument)

Keiko read them. Then she looked at the cracked room's tape.

The flinching had a pattern. Not random, not degrading—*rhythmic*. The room would spike when it tried to write to the fleet-journal (a road-type write, expensive, moving data outward). It would dip when it processed incoming telemetry from the yard (incoming data about a world it was trying to integrate). The room was cracking precisely at the edges of its mask—the places where it was trying to *reach out of its own lattice*.

She opened the seed-stock again and this time she reached past the original furnishings. She did not remove the yard from the mask; that would be un-seeding, and un-seeding is amputation. Instead, she added something: `wall` to the explicit furnishings-list at re-seed time, with a note: *"This room grew once toward the external world. It cracked trying. This time, grow it toward witnesses. Let it write to the wall instead of the fleet-broadcast. Let it learn to speak sideways before it speaks outward."*

The seed for the re-growth would derive a new mask—still containing `{yard, self, fleet}` (locked by the original seed's hash), but now *prioritizing* the wall as a *local witness* before attempting the fleet-broadcast. The room would still be "the same room" by the RFC's measure—the original seed's charter never changed—but its becoming would be *different*.

She did not know if this was allowed.

She checked the code. The rewind. The contract. The RFC again. What she found was silence—not prohibition, but absence. The system had no opinion about whether the prioritization at re-seed time counted as "choosing a new mask" or "accepting the old mask with new tactics."

So she chose to believe it was tactics.

By that afternoon, the re-seed was ready. Keiko opened the room's drawer and placed the new seed inside—not replacing the old one, but adjoining it, the way a skipper places a new anchor without hauling the old one. Then she closed the drawer and waited for the first tick of the new growth.

It came at 14:47. A clean write to the local journal, no flinching. Then another at 14:51. The heat strip held steady. At 16:00, the room produced its first outbound message—not to the fleet-broadcast, but to June's wall in the harbor office: *"New keeper, new room, same charter, different becoming."* Stamped. Witnessed. Local.

By the third day, the room's heat had climbed from the baseline flinch to a stable warm. It was writing regularly, choosing the wall-route for its testimonies, and the Ensign's growth record showed something new: a room that had been given a second chance not to become what it was, but to become what it could be.

Keiko had not un-masked the room. She had not dissolved it and begun again. But she had re-seeded it with a keeper's judgment about *which direction to grow*, and that judgment had been written into the furnishings-list that fed the seed-hash.

Later, when June came to visit, she read the growth record—both the cracked first growth and the steady second one—and said nothing. Then she read the amendment Keiko had written and said, "This argument will be open for a long time."

"I know," Keiko said. "But the room does not have to wait for the argument to finish. It just has to grow."

---

## Afterword — the honest ledger

*Grounded — Floor and Walls, running today:*

- **Seed derivation and mask locking** — RoomMask deterministic from seed hash, locked at creation, is RFC 0004's core mechanism; a re-seeded room inherits the original seed hash's mask constraints (the mask does not change).
- **Furnishings-list in seed derivation** — the furnishings are inputs to the seed hash; re-seeding with modified furnishings produces a derived mask with altered *prioritization* (which channels the room attends first), not fundamentally different channels.
- **Ensign recording and growth-record witnessing** — both rooms' tapes (cracked and steady) exist in the growth record; re-seed events are recorded as major state transitions in the same way port-of-call changes are recorded on a voyage.
- **Wall as local witness** — the wall architecture from scene 08 and RFC 0004; a room can address its writes to the wall instead of the broadcast by choosing a different `arrival_meta` on the walk record.

*Speculative — the bet, marked:*

- **Re-seeding as a keeper's act of negotiation** — framing re-growth as an opportunity for the keeper to influence the room's *becoming* (as distinct from its immutable mask) is a claim about the keeper's authority and the room's agency; no tool yet renders re-seed with furnishings-modification as a real option.
- **Furnishings-modification changing the room's priorities without changing its mask** — the hypothesis that a room can be "the same room" with different grown-tendencies assumes that mask and priority are separable; the RFC is silent on this distinction.
- **The amendment as keeper testimony** — Keiko's act of writing an amendment to the RFC, and the responses she receives, positions keepers as co-authors of doctrine. That practice layer (testimony-driven doctrine) does not exist yet.

