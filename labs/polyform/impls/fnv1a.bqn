# fnv1a-64 in BQN (CBQN). Usage: BQN fnv1a.bqn <file-of-raw-bytes>; prints 4 decimal limbs, low first.
# BQN numbers are f64 (exact only to 2⋆53), so the 64-bit state is kept as four 16-bit limbs.
# XOR is done on bit vectors; multiply-by-prime is a limb convolution with carry, mod 2⋆64.
# Prime 0x100000001b3 = 435 + 256·2⋆32  ->  limbs (low first) 435‿0‿256‿0.
p ← 435‿0‿256‿0
w ← 2⋆↕16
Xor ← {+´ w × ≠˝ 2|⌊𝕨‿𝕩 ÷⌜ w}
Mul ← {
  h ← 𝕩
  c ← {+´ ((1+𝕩)↑h) × ⌽(1+𝕩)↑p}¨ ↕4
  r ← ⟨⟩ ⋄ k ← 0
  {t ← k+𝕩 ⋄ r ∾↩ 65536|t ⋄ k ↩ ⌊t÷65536}¨ c
  r
}
Step ← {Mul (𝕨⊸Xor)⌾(0⊸⊑) 𝕩}
# offset basis 0xcbf29ce484222325, limbs low first
init ← 8997‿33826‿40164‿52210
bytes ← -⟜@ •file.Bytes ⊑•args
•Out 1↓∾ ' '⊸∾¨ •Repr¨ init Step´ ⌽bytes
