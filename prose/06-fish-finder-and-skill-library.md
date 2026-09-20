# The Fish Finder and the Skill Library

*On sonar, semantic search, and the shape of things you haven't named yet*

---

Every Alaskan fisherman knows the fish finder. You drop the transducer. You send out a ping. The sound wave travels down through the cold green water and hits things — thermoclines, kelp, rock piles, fish — and bounces back. The return paints a shape on the screen. A dense ball. A scattered cloud. A long streak along the bottom.

You don't see fish. You see *shapes that behave like fish.*

You don't know the species until you reel it in. The sonar doesn't care about species. It cares about density, about reflection, about the difference between water and not-water. The interpretation — *that's a king salmon at forty feet* — happens in the fisherman's head, not the machine.

---

Semantic search over a skill library works the same way.

You have a problem. You don't know what skill solves it. You might not even know the skill exists. You type a query — "I need to debug a Node.js memory leak" — and the embedding model sends out a ping. Not sound. Not light. A vector. A point in high-dimensional space, cast outward into the library like a transducer into the deep.

The ping hits the skills. Each one is also a vector — a position in that same space. The distance between the query vector and a skill vector tells you how much they reflect each other. Close means *this shape matches your shape.* Far means *nothing here.*

The return paints a shape. *node-inspect-debugger* lights up at 0.87 similarity. *python-debugpy* at 0.41. *weather* at 0.03. You get a cloud of hits, ranked by density.

But here's the thing: **you don't know the species until you reel it in.**

The embedding said 0.87. That's a shape. That's a sonar return. It means *something down there is reflecting your signal.* It might be exactly the skill you need. It might be a skill that's close but wrong — a king salmon that's actually a black cod. You don't know until you open the SKILL.md, read the procedures, try the commands. You reel it in.

---

This is why embeddings are better than keyword search and worse than understanding.

Keyword search is a net with exactly one mesh size. If your query word doesn't match the skill's title, you catch nothing. The ocean is empty.

Embeddings are sonar. They find shapes. They find the thing that's *almost* the right shape, the thing that's reflecting from a slightly different angle but still catching your frequency. They find the skill you didn't know you needed because you didn't have the word for it.

The fish finder doesn't need to know the word "salmon." It needs to know the shape of *not-empty-water.*

The skill library doesn't need exact titles. It needs the shape of *this problem.*

---

The fisherman trusts the finder but watches the water. The skill librarian trusts the embeddings but reads the files. Sonar gets you close. The reel does the rest.

And sometimes — this is the best part — the ping comes back with a shape you've never seen before. Something big. Something deep. Something that wasn't on any chart.

That's not a malfunction.

That's a discovery.
