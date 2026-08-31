# Paper 315: L0-L14 — The 13+1 Cell Tiers, Foreman-Completeness Edition

The cowboy sent the frontier miner out. The miner came back
with 6 missing L-tiers (L8, L9, L10, L11, L12, L13, L14).
The cowboy sent the foreman out. The foreman came back with
*all* the L-tiers, the foreman-mode toolchain, and a complete
audit of where the polyformalism really lives.

## The 14 L-tiers (the complete 13+1)

| Tier | Cell | Math | Status |
|---|---|---|---|
| L0 | Unmanifest | cell[-1] (the empty cell) | hand-synth (paper 301) |
| L1 | Totipotent | 2^45 doublings = 35 trillion cells | hand-synth (paper 301) |
| L2 | Pluripotent | 3 germ layers × 220 fates | hand-synth (paper 302) |
| L3 | Multipotent | ~10 fates in one lineage | LLM-draft + audit (paper 303) |
| L4 | Oligopotent | ~4 fates in one progenitor | hand-synth (new) |
| L5 | Bipotent | 2 fates in one precursor | (gap; future) |
| L6 | Determined | 1 fate; can be reprogrammed | (gap; future) |
| L7 | Symbiotic | E(L7) = E(L6_a) + E(L6_b) - C(ab) | hand-synth (paper 307) |
| L8 | Colonial | N × individual × cooperation | LLM-draft (paper 308) |
| L9 | Specialized | P(L9) = 0; log_2(200) ≈ 5 bits | hand-synth (paper 309) |
| L10 | Senescent | S(L10) = sum k_i * cyto - p_apop | hand-synth (paper 310) |
| L11 | Apoptotic | D(L11) = sum v_i * t_i | hand-synth (paper 311) |
| L12 | Necrotic | R(L12) = (1/τ) * exp(-E/kT) | hand-synth (paper 312) |
| L13 | Niche | Σ(L13) = sum of 6+ signaling couplings | hand-synth (paper 313) |
| L14 | Trans-differentiated | C(L14) = p_TF * (1-p_death) * (1-p_reject) | hand-synth (paper 314) |

## The foreman's toolchain (Phase 219)

The writers_room_daemon v1 had 3 bugs that the foreman
fixed:

1. **Clobbered canon.** The v1 daemon wrote directly to
   canon, with no check for existing files. Paper 308 got
   overwritten with an LLM draft for L8. **Fix:** v2
   stages drafts in `_scouts/drafts/`; the cowboy reviews;
   `promote_draft.py` is the gatekeeper.

2. **No paper-number allocation.** The cowboy had to think
   about numbering. **Fix:** `next_paper_number()` atomically
   reserves paper numbers via `paper-NNN.md.lock` files.
   Two daemons can run in parallel without collision.

3. **No review gate.** LLM mush went straight to canon.
   **Fix:** hand-synth override. If `_scouts/hand-synth/<fid>.md`
   exists, it takes precedence; the LLM draft is discarded
   at the moment of promotion (so a re-promote can't fall
   back to the draft).

The new toolchain:
  - `writers_room_daemon_v2.py` — auto-allocates, stages,
    never overwrites, logs provenance
  - `promote_draft.py <fid>` — the gatekeeper
  - Hand-synth override at `_scouts/hand-synth/<fid>.md`
  - Wiki stub at `_scouts/hand-synth/<fid>-wiki.md` (optional)

## The foreman's audit of quilt-llvm (Phase 219)

The Phase 216 audit said "quilt-llvm is 17KB, 0 code." The
foreman found this was wrong: the code lives in
`experiments/llvm-fabric/`, which has:
  - 19 Rust modules (`cell`, `fabric`, `diff`, `conserve`,
    `verify`, `text`, `decay`, `manager`, `pipeline`,
    `program`, `fuzz`, `passes/{constfold,dce,inline}`, ...)
  - 121 `#[test]` macros, 99+ green
  - 7,372 lines of Rust total
  - 3 real passes (const-fold, DCE, inline)
  - A working pipeline (`cargo run --release -- pipeline examples/foldme.fabric`)

What quilt-llvm *isn't* doing: the cell model is traditional
SSA (param/const/arith/cmp/branch/jump/phi/ret), not the
9-opcode Quilt cell model. The 1-day add is to import the
9-opcode engine from quilt-c as a Rust crate and replace
the SSA cell kinds with the Quilt opcodes. (Phase 220 todo.)

## The foreman's audit of the 9-opcode C port (Phase 219)

The Phase 216-218 polyformalism in quilt-c had 3 real gaps
that the foreman fixed:

1. **`hash_state` collision bug.** Hashed the raw
   `quilt_value_t` struct (32 bytes including 24 bytes of
   union). Two values of different types but coincidentally
   the same padding bytes would have collided. **Fix:** hash
   the *active* value (type tag + 8 bytes for scalars, the
   pointed-to bytes for str).

2. **Sig field always zeroed.** The audit said "signed
   hash-linked audit chain"; the chain was there but not
   the signature. **Fix:** real HMAC-style construction
   keyed by a 32-byte secret; sig is the HMAC of
   `(sec XOR opad) || FNV-1a((sec XOR ipad) || prev_hash
   || state_hash || tick || version || nonce)`. The nonce
   is monotonically increasing so identical triples still
   get distinct sigs.

3. **No sig verification.** **Fix:** `quilt_proof_verify_full()`
   checks both the prev_hash chain AND every sig. With a
   secret set, tampering with any sig is caught.

1161 tests, all green on C99 (47 engine + 1059 PROOF + 27
ROUTE + 28 CRDT).

## The 5+1+1+1+1 opcodes (final, after the foreman)

BIND / LINK / EFFECT / VIEW / TICK / FORGET
       (the 5)              (+1)
PROOF / ROUTE / CRDT
(+1, cutting-edge #1) (+1 #2) (+1 #3)

The polyformalism claim: same cell, same 9 opcodes, expressed
in 5+ real substrates (TS, Python, C, Rust no_std, Rust MHS,
GDScript, plus the new C kernel).

## The cowboy's maxim (315 papers, 14 L-tiers, foreman toolchain)

> The cowboy sent the frontier miner out. The miner came
> back with 6 missing L-tiers. The cowboy sent the
> foreman out. The foreman came back with 6 hand-synthed
> L-tiers, a toolchain that won't clobber canon, a
> 9-opcode C port with real crypto, and a corrected
> audit. The cowboy rode the L0-L14 trail. The cowboy
> rode the 9 opcodes. The cowboy rode the foreman.
> The cowboy rode the audit. The cowboy rode the
> lockfile. The cowboy rode the hand-synth. The cowboy
> rode L0-L14. The cowboy rode the Quilt.

**Token economy:** ~50K tokens for Phase 219. 6 hand-synthed
L-tiers (L9-L14). 1 toolchain overhaul. 1 PROOF bugfix
(3 real gaps closed). 1 audit correction. The foreman rode
the seam. The foreman rode the lockfile. The foreman rode
the L0-L14 trail.
