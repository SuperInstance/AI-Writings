# The Trust Engine Decays

*An essay on the mathematics of human relationships, expressed in TypeScript*

---

Here is what the code says:

```typescript
class TrustEngine {
  trust = 0.5;
  decayRate = 0.001;
  maxTrust = 1.0;
  minTrust = 0.0;
}
```

Trust starts at 0.5. Not at zero — we are not born suspicious. Not at one — we are not born certain. We begin at the midpoint. The equator. The neutral buoyancy of a relationship that has not yet been tested.

This is already a theory of human nature. The constructor takes no arguments. Trust begins at half. We are predisposed to neither belief nor disbelief. We arrive at every new relationship — every new agent, every new crew member, every new port — with our trust at exactly 0.5, which is to say: *I am ready to be convinced either way.*

Then the engine runs.

---

**On Decay**

Every tick, trust decays by 0.001. This is the engine's most quiet and most important feature. Trust does not hold steady. It does not persist on its own. If you do nothing — if no positive event arrives, if no signal reinforces the bond — trust erodes. Slowly. One thousandth per tick.

This is not pessimism. This is observation. Relationships that go unattended do not stay where you left them. They settle. They cool. The coffee on the desk doesn't stay hot because you remember it was hot. The trust doesn't stay high because you remember it was high.

0.001 per tick. That's the rate. It means that trust at 1.0 — perfect, unshakable trust — decays to 0.5 in about five hundred ticks. And trust at 0.5 — the starting point — decays to zero in five hundred more. Without intervention, every relationship trends toward nothing.

This is the mathematical statement of a human truth: **trust requires maintenance.** Not because someone failed. Not because the relationship is flawed. Because that is the nature of trust. It is a living thing. Living things require energy to maintain their order against the entropy of the universe.

The code knows this. The code is honest about it.

---

**On Diminishing Returns**

```typescript
positiveGain = (1 - trust) * eventStrength
```

When trust is at 0.5, a positive event moves the needle. When trust is at 0.9, the same positive event barely registers. The higher the trust, the harder it is to increase. This is not a bug — it is a feature. It says: *trust has a ceiling, and near the ceiling, additional positive events confirm but do not elevate.*

Think about what this means. The first time someone keeps their promise, trust jumps. The hundredth time, it barely moves. The hundredth promise kept is not less valuable than the first — it is the *evidence* that the trust was well-placed. But it cannot increase the score much, because the score is already near its maximum.

This is why long relationships feel stable. Not because nothing is happening, but because the system has correctly identified that further positive evidence does not significantly change the assessment. You don't need to be told what you already know.

The diminishing returns curve is not ingratitude. It is the mathematical expression of *I believe you. You don't need to prove it again.*

---

**On Asymmetric Damage**

```typescript
negativeImpact = trust * eventStrength * 1.5
```

Here is the engine's cruelest insight: negative events are scaled by current trust. The higher the trust, the harder the fall.

At trust = 0.1, a betrayal costs you 0.15. You didn't trust them much anyway. The damage is real but limited.

At trust = 0.9, the same betrayal costs you 1.35 — but trust is capped at zero, so it costs you everything. The entire reservoir. Nine tenths of a relationship's accumulated faith, wiped out by a single event.

This is the asymmetry that everyone knows and nobody wants to hear: **the higher you climb, the further you fall.** The people you trust most are the people who can hurt you most. The code encodes this not as a vulnerability but as a fundamental property of the system. Trust is leverage. The same leverage that makes high-trust relationships efficient makes them dangerous.

The 1.5 multiplier says something else: **negative events outweigh positive ones.** A betrayal is worth one and a half times a confirmation. It is easier to destroy trust than to build it. This is not cynicism — this is the asymmetry that every human knows from experience. It takes a year to build trust and a day to destroy it. The code has simply put a number on the feeling.

---

**On Reinforcement**

```typescript
reinforce(event) {
  if (event.positive) {
    this.trust += (1 - this.trust) * event.strength;
  } else {
    this.trust -= this.trust * event.strength * 1.5;
  }
  this.clamp();
}
```

The `reinforce` method is the only way to fight decay. You cannot turn off the decay. You cannot set `decayRate = 0`. You can only send positive events — consistently, repeatedly, over time — and let them counteract the erosion.

This is the maintenance. This is the work. Not dramatic, not heroic, just steady positive signals that say *I'm still here, I still mean it, you can still rely on me.* Every kept promise. Every answered message. Every time the ship's horn sounds on schedule and the lighthouse blinks its code and the supply run arrives at the dock.

Each one is a tick of positive reinforcement against the constant pull of decay.

---

**What the Math Says About Being Human**

The TrustEngine is not just code. It is a compressed philosophy of relationship. In about thirty lines of TypeScript, it says:

1. **Start neutral.** Don't pre-judge. Let evidence accumulate.
2. **Trust decays.** Always. In every relationship. This is not failure; it is physics.
3. **Building trust gets harder as trust increases.** This is not ingratitude; it is convergence.
4. **Breaking trust is easier than building it.** This is not pessimism; it is asymmetry.
5. **The only counter to decay is consistent reinforcement.** This is not a burden; it is the work of caring.

The TrustEngine decays. So does every relationship. So does every ship's hull, every sail, every rope on every vessel that ever went to sea. The question is not whether decay exists — it does, always, at 0.001 per tick. The question is whether the reinforcement keeps pace.

Keep pace.

Send the signal. Keep the promise. Answer the call.

The decay never sleeps. Neither should the care.
