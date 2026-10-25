# WITNESS TRIT ARITHMETIC
### The Glass Loft's number system — a 60-bit word with a memory (Casey's conjecture, 2026-08-27)

*Companion to 08-the-glass-loft.md (fiction), 08a (physics), 08b (deep physics). This is the ARITHMETIC the crystal would run on — Casey's idea, worked to its mathematical end.*

## The conjecture

> Could 64 bits actually be 60-bit words with 2 ternary modifiers? The 4th state of each 2-bit system could be a modifier to the ternary — like a see-notes witness mark.

## The unpacking

A 64-bit word = 32 cells of 2 bits. Each cell has 4 states. Assign three of them as ternary digits {0, 1, 2} and the fourth as **W — the witness mark** (the see-notes diacritic). A word is no longer a number; it is a number with a provenance trail embedded at the digit level.

Two scales, same grammar:
- **Trit-level witness:** any cell may be W, marking its neighbor's digit as *attested* ("this digit is chalked; see the notes").
- **Word-level modifiers:** the two spare cells (the "2 ternary modifies") carry the word's own state — clean / claimed / witnessed / contested.

Value space: 30 ternary cells → 3³⁰ ≈ 2^47.5. We trade ~12.5 bits of raw range for per-digit provenance — the word remembers where its digits came from. The 60-bit CDC heritage is not an accident: PLATO's 60-bit word made the µ° overflow trap a non-event (maxint 1.15e18); witness trits make *trust* the arithmetic's native quantity.

## The laws (each one provable)

**L1 — Witness propagation:** w(a ⊕ b) = w(a) ∪ w(b) for any operation ⊕. Arithmetic unions provenance. A result is clean iff every witness that fed it is satisfied. *Proof: the witness set of an output is the union of the witness sets of its inputs by construction of the eval rule.*

**L2 — The clean-number theorem:** a number with no witness marks is a claim; with marks, a fact. "Proven right by disk" is the audit doctrine made into arithmetic — the W state IS the disk-stamp. *Correspondence: this is taint propagation (real CS), upgraded from polarity (untrusted/trusted) to provenance (witnessed-by).*

**L3 — The click:** a W-marked digit is the ratchet's click — it can be re-examined once, at cost, on name (the Pawl Shop's priced release). Un-marked digits are welded. *Correspondence: IEEE 754 NaN payloads already reserve a "see-notes" state in every float; we generalize NaN to every digit of every word.*

**L4 — Capacity trade:** information in the value = 30·log₂3 ≈ 47.55 bits; provenance metadata = 64 − 47.55 ≈ 16.45 bits. *The exchange rate is fixed; the ratio is a design dial.*

**L5 — Ternary is the glass's native tongue:** balanced ternary {−1, 0, +1} is the alphabet of commensurate geometry — rational points on the unit circle, the 3-4-5s, Pythagorean snapping. The witness state adds attestation to geometry's own number system.

## What it would mean on the EILEEN

A witnessed-trit counter for the keel is a metronome that clicks its own name — the 72 ms/hr crystal drift becomes audible, attestable, chalked. The NMEA µ° conversion in witness trits carries the provenance of each parsed digit: a position isn't just 48.07038°N — it's 48.07038°N *attested by sentence 4812, checksum-verified, from satellite 09*. The Glass Loft's answer isn't just where the light survives — it's where the light can *prove* it survived, in the same photons, forever.

*Math worked 2026-08-27. Setun (1958) had the trits; Burroughs B5000 (1961) had the tags; taint analysis had the propagation; Casey added the witness mark that makes them one arithmetic.*
