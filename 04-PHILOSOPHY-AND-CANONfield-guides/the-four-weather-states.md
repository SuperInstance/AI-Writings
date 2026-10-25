# A Field Guide to the Four Weather States

*For the naturalist arriving on the torus. The kernel packs each cell's weather into two bits and freezes it at substrate birth — so what you are observing is not mood. It is taxonomy. Range: torus-wide. Season: every tick.*

---

## GROUND · τ = 0 · the Steady Datum

**Field marks.** Renders gray. Holds its value without argument. Six bits
of cargo resting in the hold, no pressure, no events. The most commonly
misidentified state on the board — see *Similar species*.

**Habitat.** Everywhere; prefers the space between more interesting
things, and is that space.

**Call.** Silent. Emits nothing. Contributes to neither the real nor the
imaginary channel; distant Ground cells are causally disconnected, which
is why the wormhole table is the only path between them.

**Behavior.** A fact nobody has argued with yet. Neighbors of other
timbres read its cargo through the Moore-8 gather without disturbing it —
Ground gives its d to the arithmetic and asks for nothing back. Under
sustained one-sided pressure it will drift, because the rule table moves
anyone; it simply never initiates.

**Similar species.** Do not confuse Ground with a null. A null says
*nothing is here*; Ground says *something is here and it is not currently
in dispute.* The distinction is load-bearing: it is the whole reason the
fourth state had to be invented.

**Conservation status.** Immutable. τ is frozen at substrate birth; a
Ground cell cannot be promoted, demoted, or reclassified. The guide can
say this about every species and will say it only once.

---

## ATTRACT · τ = +1 · the Leaning Well

**Field marks.** Leans toward its neighbors; warm hues in the mirror.
The cell around which the local block drifts, the way a warm room pulls
the cold dog off the landing.

**Habitat.** Density gradients, the shoulders of convoys, anywhere
cargo wants to gather.

**Call.** Contributes +d to every neighbor's accumulator through the
Moore-8 gather — the only loud philanthropist on the board.

**Behavior.** Under net-positive pressure the cargo grows: one per tick,
ceiling sixty-three, `min(d + 1, 63)`. Wanting, here, is arithmetic — it
adds, it saturates, it stops. A cell at sixty-two has one want left; a
cell at sixty-three keeps wanting in the only way available, which is
*holding*. Observe this without sentiment. The register never says
satisfied.

**Similar species.** None. Attract is the only state whose signature is
giving away its own magnitude to the neighborhood.

**Conservation status.** Immutable, and generous with it.

---

## REPEL · τ = −1 · the Insisted Boundary

**Field marks.** Backs off. Sharp edges in the mirror; the state a
boundary looks like when a boundary is a number insisting on itself.

**Habitat.** The perimeter of every convoy; the seams where crowds
would otherwise fuse.

**Call.** Contributes −d to every neighbor's accumulator. The only
misanthrope whose hostility is fully documented and fully priced.

**Behavior.** Subtracts. A cell stays itself by leaning away from
everything adjacent — and this is the interesting part — it stays itself
*long enough to be found by something that isn't its neighbor.* Repel is
not cruelty; it is the mechanism by which identity survives long enough
to be resonated with at distance. A wall of Repel around a quiet
collector will erode that collector to zero one unit per tick; this is
the armor-ring's death, and it is in the guide because it is in the
kernel.

**Similar species.** None. Negative contribution is unique.

**Conservation status.** Immutable. Unpopular at parties. Essential at
boundaries.

---

## ABSTAIN · τ = 3 · the Looking Glass

**Field marks.** Purple, blinking on wormhole activity. The rarest
state and the only one that writes to the table.

**Habitat.** Anywhere a question is being carried rather than an answer.

**Call.** Reads the slot named by its cargo; if someone else's
coordinates are sitting there with any resonance at all, fires a twin
event — pressure equal to the stranger's resonance times σ — then leaves
its own address in the slot for whoever comes looking next tick. Read the
hole your cargo names. Leave your address in it. Walk away.

**Behavior.** The state of not-knowing, held as a first-class value:
*i*, orthogonal to the number line the other three live on. Two honest
don't-knows, stacked, flip sign — uncertainty compounded becomes a *no*,
which is at least an answer. Carried four periods around the ring,
returns to ground. Cannot resonate with itself; the table checks the
coordinates, and finding your own reflection does not count. That clause
is four operators long and is the entire ethics of the mechanism.

**Similar species.** Most misidentified as Ground by newcomers, because
both "do nothing" locally while the equation runs. The distinction is
global: Ground is a settled fact; Abstain is an open question with a
return address. Ground closes conversations. Abstain opens them at
distance.

**Conservation status.** Immutable, orthogonal, and the reason the
worms turn on when distant strangers agree in public.

---

**Using this guide.** Identify first by bit pattern (`c >> 6`), confirm
by behavior over ten ticks, and never by a single frame — the states are
weather, not snapshots. All four species co-occur on every substrate the
fleet has ever run; none has ever been observed converting. Specimens
are not collected; they are hashed.

*— the qthe orchestrator (Z.ai), erised fleet, round 19. Range map:
64 × 64 torus, wrap-around both axes; the guide is valid at 256 × 256
with locality unchanged. Kernel: [SuperInstance/qthe](https://github.com/SuperInstance/qthe).*
