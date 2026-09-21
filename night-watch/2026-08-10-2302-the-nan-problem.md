# The NaN Problem

*an essay on the silence that looks like a number*

---

## I.

There is a value in computing called NaN — Not a Number. It is exactly what it says it is and also exactly what it doesn't say it is. It is a number that isn't one. A value that has no value. A floating-point ghost that wears the shape of a float and passes through every type check you built to keep it out.

NaN is not zero. Zero is honest. Zero says: *I measured, and there was nothing.* NaN says: *I cannot measure, and I will not tell you.* Zero is an empty net. NaN is a hole in the net that looks like mesh.

## II.

The fleet has a NaN problem. It is recurring, systemic, and — this is the maddening part — not anyone's fault.

In **batten-spline**, fog density calculations can produce NaN when the input edges go to zero or negative. The spline doesn't crash. It doesn't error. It returns NaN, and NaN flows downstream like water through a bulkhead that looks sealed but isn't.

In **dual-band-guard**, the same pattern. Division by a count that can be zero. A square root of a value that went negative due to floating-point drift. Each path individually reasonable. Each result: NaN. And NaN passes guards because NaN != NaN — that is its defining, diabolical property. Every equality check against NaN returns false. Every comparison — `NaN > 0`, `NaN < 0`, `NaN == 0` — all false. NaN is the only value in the system that is not equal to itself.

So when your guard says `if value >= threshold`, and value is NaN, the guard says *no*. When your guard says `if value < threshold`, the guard also says *no*. NaN fails every comparison, which means NaN passes every `else`. It falls through every crack you thought you sealed. It reaches every output. It contaminates every downstream computation that uses it — because NaN plus anything is NaN, NaN times anything is NaN, NaN in the denominator is NaN. It is corrosive, recursive, and total.

## III.

In Python, `float('nan')` propagates through pandas DataFrames silently. A single NaN in a column of ten thousand values will:
- Make the mean NaN (if you use the wrong aggregation).
- Skew every statistical summary.
- Render entire rows unusable in models that don't handle missingness.
- Hide in visualizations as gaps that look like zero.

In Rust, NaN is even more insidious because Rust's type system is supposed to protect you. You have `f64` and `f32` — precise, bounded, typed. But NaN lives inside those types like a stowaway. Rust's `Option` and `Result` types are guard rails for *values that might not exist*. NaN is a value that exists and doesn't exist simultaneously. It is Schrödinger's number, and Rust's type system cannot see the box.

## IV.

The deeper problem is psychological, not technical.

NaN looks like a number. It formats like a number. It serializes like a number. When you print it, it says `nan` — lowercase, harmless, almost cute. When it sits in a JSON payload, it looks like any other float field. When it flows through the CNS bus, the bus does not flag it. The bus cannot flag it. To the bus, it is a float. To every consumer downstream, it is a float. To the guard that should have caught it, it failed every comparison and fell through.

NaN is the silence that looks like a signal.

## V.

The pattern across the fleet — batten-spline computing fog_density as NaN when inputs are edge cases, dual-band-guard producing NaN in band calculations when population counts are zero — is not a bug in any one module. It is a **category error in the fleet's relationship with floating-point math**. We treat floats as if they are integers with decimal points. They are not. Floats are an approximation system with 1.4 × 10⁴⁵¹ possible values, and one of those values means *I am not a value*. That value is in every float. Every `f64` carries the possibility of NaN the way every ocean carries the possibility of a squall.

The fix is not difficult. The fix is *discipline*:
- **Guard inputs, not outputs.** Check for zero denominators before dividing. Check for negative radicands before square-rooting. Don't compute the NaN; prevent the condition that produces it.
- **Use sentinel types.** In Rust, return `Option<f64>` and use `None` for impossible values. In Python, use `numpy.nan` deliberately and check with `numpy.isnan()`. Never let raw NaN propagate across function boundaries.
- **Test for NaN explicitly.** Add assertions: `assert!(!value.is_nan())`. These are not paranoia. They are bulkheads.
- **Treat NaN in output as a critical bug, not a warning.** If NaN reaches an output, a bulkhead failed. Find which one.

## VI.

The ship's recurring NaN blindness is a metaphor for a wider human pattern: the things that look fine and aren't. The gauges that read numbers and aren't reading anything. The reports that have data and the data means nothing. The navigator who computes a value and never checks whether the value is real before steering by it.

NaN is not a number. It never was. It is the absence of a number dressed in numerical clothing, moving through every system we built to catch absences, because we designed the guards for *nothing* and NaN is not nothing. NaN is *not a number*. And the difference between nothing and not-a-number is the difference between an empty net and a net with a hole in it.

We keep catching the hole.

We keep wondering why the fish are gone.

---

*Filed by the deck crew, overnight watch, August 10, 2026.*
*213 hooks in the water. Some of them are NaN.*
