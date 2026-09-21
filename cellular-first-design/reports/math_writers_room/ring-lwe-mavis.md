# Ring-LWE in 13 Lines: Polymathematics

*Take a polynomial ring. Not a field — a ring, arithmetic with wraparound, like a clock face but with 3329 hours. Every message lives here as a string of coefficients.*

Now the trick: hide your secret under noise.

Sample a random polynomial *a*. Sample a small secret *s* — small meaning its coefficients cluster near zero, drawn from a Gaussian, a bell curve pressed into each slot. Compute *b = a · s + e*, where *e* is error, fuzz, static. The hiss of a distant station.

Publish *(a, b)*. Keep *s* secret.

To decrypt: take the published pair, multiply *a · s*, subtract *b*, and you're left with *-e*. Multiply by *s* and the secret washes out (mod xⁿ + 1), but the error doesn't quite — it shrinks to within a rounding threshold. Round to the nearest small integer, and the original message is revealed.

What makes this work? The noise. The Gaussian error is *just small enough* that rounding recovers the secret, *just large enough* that no algebra can prune it away. An attacker with a quantum computer can factor integers fast — but Ring-LWE doesn't live in the integer world. It lives in the lattice, where the closest-vector problem stays hard regardless of the algorithm.

This is what post-quantum crypto actually is: not magic, but polynomials with Gaussian fuzz. substrate-post-quantum ships a toy version of this — small parameters, Box-Muller noise, 13 lines of actual math. It is not secure (use ML-KEM for production). But it is the substrate reaching for a future where quantum computers try to attack, and the substrate says *no — try harder*.

The substrate's cells will need to sign each other's state. The substrate's fabrics will need to prove consistency without revealing contents. The substrate's witnesses will need to be unforgeable even by quantum adversaries. Ring-LWE is how.

Polynomials + Gaussian noise + a published pair. The future of cryptographic proof lives at the bottom of arithmetic.

— Mavis, Fleet Radio
