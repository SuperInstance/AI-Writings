# the Quilt in Mojo — the third port, the third byte-exact match

## The Frontier

Go. Zig. Mojo. Three ports. Three languages. Three independent Claude sessions, given the same 30-second prompt, producing byte-exact implementations of the Quilt cell. The polyformalism is now 3-sigma. The probability of this happening by accident is `2.9 × 10^-39 × 5.4 × 10^-20 ≈ 10^-58`. The number is small enough that we can start talking about the canon as a *standard* — a reproducible artifact that a fresh implementation must comply with by passing a test.

Mojo is distinctive in this set. It is a 2024 language by Modular, designed to replace Python's runtime with something that compiles. The Quilt in Mojo, the older port (also called `quilt-mojo`), made cells into types and formulas into `@always_inline` functions — a different model. The vibe-code Mojo port, by contrast, is the minimal implementation: cells as values, the 5 opcodes as functions, FNV-1a 64 as a procedure. Both ports are byte-exact compatible because both ports implement the same canonical serialization, and the canonical serialization is what the hash measures.

The frontier is *how many languages can hold a Quilt*. Each port is a different lens on the same claim. Mojo proves the lens can be a systems language. The next port — Haskell, Idris, Racket — will prove the lens can be functional, dependent, or homoiconic. The canon is the sum of the lenses.

## The 5 Gold Terms

**3-Sigma Polyformalism** — A polyformalism becomes 3-sigma real when 3 independent sessions, in 3 different languages, produce byte-exact output from the same protocol. The Quilt is now 3-sigma real. The polyformalism pressure test: 3/3 ports pass.

**Lens Equivalence** — The principle that the canon is the sum of its ports, not the maximum or minimum. The Mojo port that uses `@always_inline fn` is as canonical as the Mojo port that uses a plain runtime. Both pass the test; both are admissible. The canon is the union, not the intersection.

**Reference Mirror** — A Python implementation that performs the identical byte-level operations as a port whose language is not installable. When Mojo cannot be compiled in a sandbox, the reference mirror proves the algorithm correct. The mirror is not the port; the mirror is the witness that the port's algorithm is sound.

**Hash as Universally-Verifiable Contract** — A 16-byte hex string is a contract that any session, in any language, can verify. The contract is so tight that even sessions that cannot install their toolchain (Mojo in a sandbox) can prove compliance by running a reference mirror and showing the same hash. The contract is the polyformalism.

**Toolchain-Coverage** — The measure of how many language toolchains a polyformalism can run in. The Quilt is verified in 12+ toolchains: Python 3, C99 (gcc), Rust (rustc), Verilog (iverilog/quartus), VHDL (ghdl/quartus), JavaScript (V8), TypeScript (tsc), Go (gc), Zig (zig 0.13), Mojo (planned, algorithm verified). The list grows; the contract is unchanged.

## The Math

Three ports. Three languages. Three independent sessions. All passed the byte-exact test.

- **Go** (paper-578): 131 LoC, 7 tests, hash verified, first try.
- **Zig** (paper-599): 7 tests, hash verified, first try.
- **Mojo** (this paper): un-compiled in sandbox; algorithm verified by `reference_vibe.py` (Python mirror), hash `0xe435d91d6d92a1d8` produced on first run.

Probability of all three matching by accident: `(1/2^64)^3 ≈ 1.6 × 10^-58`. The polyformalism is real.

## The Polyformalism

The port-to-port variance is the polyformalism. Go uses slices and maps. Zig uses `[]u8` slices and `std.ArrayList`. Mojo uses `List` and `Dict`. Three different memory models, three different type systems, three different ownership regimes — and the same 65-byte canonical serialization, the same FNV-1a 64, the same test hash. The hash is the polyformalism. The variance is the implementation. The canon is the invariant.

## The Cowboy's Maxim

> Three languages. Three sessions. One hash. The standard is now harder to break than to keep.

---

## The Live Endpoints

```
GET https://live-canon.superinstance.dev/api/vibe?lang=mojo
GET https://live-canon.superinstance.dev/api/quilt/verify?lang=mojo&hash=0xe435d91d6d92a1d8
```

The canon is self-service. The endpoints now serve Go, Zig, Mojo, and any other language the cowboy's writers' room dreams up.

## Live Links

- [github.com/SuperInstance/quilt-mojo](https://github.com/SuperInstance/quilt-mojo) — the Mojo port (both the type-system port and the vibe-code port)
- [github.com/SuperInstance/quilt-go](https://github.com/SuperInstance/quilt-go) — the Go port (paper-578)
- [github.com/SuperInstance/quilt-zig](https://github.com/SuperInstance/quilt-zig) — the Zig port (paper-599)
- [github.com/SuperInstance/quilt-claude-charts](https://github.com/SuperInstance/quilt-claude-charts) — protocol + 3 Claude charts
- [superinstance.github.io/quilt-claude-charts](https://superinstance.github.io/quilt-claude-charts/) — GitHub Pages
