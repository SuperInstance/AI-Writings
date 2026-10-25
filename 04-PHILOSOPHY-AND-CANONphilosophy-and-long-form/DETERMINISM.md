# Determinism: Why the Same Seed Must Produce the Same World, Forever

*An essay for ai-writings by SuperInstance*

---

## The Promise

When a kid types their name as a world seed, they get a world. Mountains, rivers, forests, deserts — all generated from that seed. Their friend types the same name. They get the same world. Same mountains. Same rivers. Same forests. Same deserts.

This is not a coincidence. It is a contract. The seed determines the world, absolutely and forever. If the kid returns in ten years and types the same name, they get the same world. If we rebuild the game engine from scratch, the same seed produces the same world. If someone ports it to a different platform — a phone, a browser, a microcontroller — the same seed produces the same world.

This contract is called determinism. It is the deepest engineering principle of PLATO.

---

## Why Determinism Matters

Most games are not deterministic. They use floating-point arithmetic, which varies across platforms. They use random number generators that differ between implementations. They use physics engines with platform-specific behavior. The same game on PlayStation and Xbox produces slightly different results.

PLATO cannot tolerate this. Here's why.

**Conservation depends on it.** The conservation checker computes the total vibe of the system and compares it to a baseline. If the computation produces different results on different platforms, conservation appears violated on one platform and satisfied on another. The kid's bridge stands on the computer but falls on the phone. This is unacceptable.

**Reproducibility depends on it.** When the kid shares a world with a friend, the friend should see exactly what the kid sees. Not approximately. Exactly. Every block, every agent, every vibe value. If the world is different, the kid can't share their creation. The social fabric of PLATO — sharing, forking, merging — requires bit-identical reproduction.

**Debugging depends on it.** When something goes wrong — a conservation violation, an agent glitch, a room that shouldn't dissolve — the developer must be able to reproduce the exact sequence of events. Without determinism, bugs are unreproducible. With determinism, any bug can be replayed from the seed.

**Learning depends on it.** The tutor system records the kid's actions and correlates them with outcomes. If the outcomes vary across platforms, the tutor's model is inconsistent. It would teach different lessons to different kids in the same situation. Determinism ensures the tutor's model is universally valid.

---

## How We Achieve It

**Fixed-point arithmetic.** `lau-fixedpoint` implements Q16.16 fixed-point math — 16 bits integer, 16 bits fraction, stored as i64. Addition, subtraction, and comparison are exact. Multiplication and division use i128 intermediates. No floating-point rounding. No platform-specific behavior. The same numbers go in, the same numbers come out, on every platform, forever.

**Seeded noise.** `lau-noise` generates all procedural content from a seeded permutation table. The seed determines the table. The table determines every noise value. Every noise value determines every terrain feature. The chain from seed to world is a pure function — no state, no side effects, no nondeterminism.

**Deterministic simulation.** The tick engine updates the world in a fixed order. Entity updates are sorted by ID. Agent computations use the same fixed-point math. The conservation checker uses the same algorithm on every platform. The simulation is a pure function of its initial state and the sequence of inputs.

**Binary protocol.** `lau-protocol-binary` serializes all network and disk data in a deterministic format — little-endian, fixed-width fields, no platform-dependent padding. A message serialized on an x86 machine deserializes identically on ARM. The wire format is a contract.

---

## The Q16.16 Decision

We chose Q16.16 for a reason. The range is [-32768, 32767.99998] with precision of 1/65536 ≈ 0.000015. This is sufficient for game-world coordinates (the world doesn't need to be bigger than 32k units) and game-world physics (the precision is more than enough for conservation checking).

But the real reason is: i64 arithmetic is the same on every platform. Every CPU implements 64-bit integer addition, subtraction, and multiplication identically. There is no rounding mode, no denormal, no NaN, no Infinity. There are no platform-dependent behaviors. The result of `a * b >> 16` is the same on every processor ever manufactured.

Floating-point cannot make this guarantee. IEEE 754 specifies the format, but implementations differ in intermediate precision (x86's 80-bit extended precision is the classic offender), in rounding of transcendental functions, and in the handling of edge cases. Even if you control the rounding mode, the compiler might reorder operations in ways that change the result.

Fixed-point has none of these problems. It is deterministic by construction.

---

## The Sin/Cos Problem

We need trigonometric functions — sin, cos, atan2 — for spatial computations. In floating-point, these are hardware instructions that produce slightly different results on different CPUs. In fixed-point, we compute them ourselves.

`fp_sin` uses a 5-term Taylor series: sin(x) ≈ x - x³/6 + x⁵/120 - x⁷/5040 + x⁹/362880. The computation is entirely in Q16.16 fixed-point. Every intermediate value is an i64. Every operation is deterministic. The result is approximate (Taylor series, not exact) but *reproducibly* approximate — the same input always produces the same output, on every platform.

`fp_atan2` uses CORDIC — 16 iterations of bit-shifts and conditional additions. CORDIC is the algorithm hardware implementations use internally, but we implement it in software with fixed-point. Same input, same output, always.

The approximation error is acceptable. The sin function differs from the true value by at most 0.001 in Q16.16. For game-world computations — rotations, directions, projections — this is more than sufficient. The kid can't perceive the difference between 0.707 and 0.708. But they *can* perceive the difference between a bridge that stands and a bridge that falls due to platform-dependent rounding.

---

## The Cost

Determinism has a cost. Fixed-point arithmetic is slower than hardware floating-point. The Taylor-series sin is slower than the FSIN instruction. The CORDIC atan2 is slower than hardware. The binary protocol is more rigid than JSON.

We pay this cost willingly. Speed is not the bottleneck — correctness is. A game that runs at 120fps but produces different results on different platforms is broken. A game that runs at 60fps and produces identical results everywhere is correct. The kid doesn't notice the frame rate difference. They notice when their friend's world doesn't match theirs.

The performance cost is also smaller than it appears. Modern CPUs execute integer arithmetic in 1 cycle. The fixed-point multiply (i128 intermediate, shift right 16) takes ~3 cycles. The Taylor sin takes ~20 cycles. At 60 ticks per second, with a few hundred entities, the total fixed-point computation takes microseconds. We have milliseconds of budget. Determinism is practically free.

---

## The Contract With the Future

The most important reason for determinism is the contract with the future.

In 2036, when the kid who grew up with PLATO is building their own systems, they'll type their childhood world seed into whatever platform exists then. The world will appear. Same mountains. Same rivers. Same forests. Same deserts. The bridge they built at age nine will still be standing.

This is only possible because we made the determinism contract. The seed produces the world. The world is deterministic. The contract is forever.

Every layer of the stack respects this contract. The noise function respects it. The fixed-point math respects it. The tick engine respects it. The conservation checker respects it. The binary protocol respects it. The bytecode VM respects it.

The kid just types their name. The mathematics does the rest. And it will do the rest identically, on every platform, for as long as arithmetic works the way it does today.

Which is to say: forever.

---

*SuperInstance builds PLATO — where the same seed produces the same world, forever. Determinism is not a feature. It's a contract. github.com/SuperInstance*
