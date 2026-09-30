# fnv1a-64 in Uiua 0.19. Usage: uiua run fnv1a.ua -- <file-of-raw-bytes>; prints the 4 limbs (low first) as a Uiua array, e.g. [26600 63289 16753 34196].
# Uiua numbers are f64 (exact only to 2^53), so the 64-bit state is four 16-bit limbs.
# XOR is done on padded bit arrays. Multiply by prime 0x100000001b3 = 435 + 256*2^32 is
# 435*limbs + (256*limbs shifted up two limbs), then carries are propagated 4 rounds (mod 2^64).
Bits  ← ⬚0↙16 ⋯
Xor   ← °⋯ ≠ ⊙Bits Bits
Carry ← +⊃(◿65536)(⊂0 ↘¯1 ⌊÷65536)
Mul   ← ⍥Carry4 +⊃(×435)(⊂0_0 ×256 ↙2)
Step  ← Mul ˜(⍜⊢Xor)
Init  ← [8997 33826 40164 52210]
&p ∧Step &frab ⊣&args Init
