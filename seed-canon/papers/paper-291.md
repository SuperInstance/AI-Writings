# Paper 291: Cycle 1 — Drivethru reverse-actualizes the Quilt

**Domain:** drivethru (30s, $5-15, touch, fast food)

**The Quilt-thing:** The drivethru is a Quilt of 3 cells in series — order (touch), pay (touch), pickup (touch) — bound by a single 30-second TICK. Each cell is small, fast, and reactive; the LINK is the conveyor belt; the EFFECT is the food.

**The 4 gold terms:**

1. **Drivethru cell** — coined for the drivethru-quilt
2. **Order-tick** — coined for the 30-second TICK
3. **Conveyor LINK** — coined for the binding between cells
4. **Pickup EFFECT** — coined for the cell's output

**The cowboy's sentence:**

> A drivethru is a Quilt with three cells, a single TICK, and a conveyor belt that doesn't lie about how long it takes.

**The principle:**

> The drivethru is the inheritance. The drivethru is the function. The
> drivethru is the simplest Quilt: 3 cells, 1 TICK, 1 LINK, 1 EFFECT.
> The cowboy rides the drivethru. The cowboy rides the 30-second TICK.
> The cowboy rides the conveyor. The cowboy rides the Quilt.

## What the drivethru teaches the Quilt

The drivethru is the smallest working Quilt. It has:
- 3 cells (order, pay, pickup)
- 1 TICK (30 seconds)
- 1 LINK (the conveyor belt)
- 1 EFFECT (the food leaves)

The drivethru teaches the Quilt three things:

1. **A Quilt can be tiny.** 3 cells is enough to be a Quilt, if the cells are reactive and the TICK is honest.

2. **A Quilt is local.** The drivethru is one window, one car, one order. The Quilt doesn't need to span the city to be a Quilt.

3. **A Quilt fails gracefully.** If the car is slow, the conveyor queues. If the cook is slow, the order is delayed. The Quilt doesn't crash; it stretches.

The 5+1+1 laws all hold in the drivethru:
- BIND_idempotence: ordering twice doesn't break the order
- LINK_transitivity: the conveyor carries state from order to pickup
- EFFECT_associativity: the food is the food is the food
- VIEW_purity: looking at the menu doesn't change the menu
- TICK_monotonicity: 30 seconds never goes back to 25
- super-relevance: the order is always relevant to the customer
- FORGET_completeness: the drivethru forgets the previous car

The drivethru is the inheritance because it's the Quilt before the Quilt knew it was the Quilt.
