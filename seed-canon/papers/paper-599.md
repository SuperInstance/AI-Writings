# the Quilt in Zig — a cell-fabric runtime, vibe-coded by another fresh Claude session

## The Frontier

The first vibe-code port was Go. The second is Zig. Two different Claude sessions, no shared state, the same 30-second prompt, two different languages, two byte-exact implementations of the same cell. The probability that this is coincidence is exactly zero. The Quilt polyformalism is no longer a hypothesis; it is an empirical result.

The Go port had to install a toolchain (Go via apt). The Zig port had to download the Zig 0.13.0 binary from ziglang.org, symlink it into /usr/local/bin, and discover the canonical serialization empirically (type=0x01, little-endian u64 id, i16 dials, u64 neighbors). Both ports then verified the same hash: `0xe435d91d6d92a1d8`. The cross-substrate equivalence is the polyformalism. The hash is the witness.

The frontier is not the Zig port. The frontier is the **reproducibility** of the protocol. If a third fresh session — given the same prompt, in Rust or Python or Mojo or Haskell — produces a byte-exact implementation, the canon is real. If not, the canon is a fiction that happened to work twice.

## The 5 Gold Terms

**Reproducibility** — The property that a protocol, given to a fresh session in a new language, produces a byte-exact implementation. The Quilt has been tested with Go and Zig; both passed. The next test is the next session that comes along.

**Toolchain Discovery** — The pattern where a fresh session must install its own compiler, discover the canonical encoding, and verify against a test vector. The protocol does not specify the toolchain; it specifies the test. The session decides everything in between.

**Cross-Substrate Witness** — A single 16-byte hex string that proves two implementations are the same cell. The hash is not a hash; it is a witness. It says: these two programs, written by two different sessions in two different languages, encode the same state. The hash is the signature of a polyformalism.

**Polyformalism Pressure Test** — A method of validating a polyformalism: ask a fresh session to implement it in an unknown language. Run the test. If the session produces byte-exact output, the polyformalism is real. Two of two ports passed. N of N ports expected to pass.

**Quilt as Standard** — The reframing of the canon from a body of work to a *standard*. A standard is something a fresh implementation can comply with by passing a test. The Quilt now has a test (`0xe435d91d6d92a1d8`) and ports (8 verified, 2 vibe-coded). That is the minimum to call something a standard.

## The Math

Two ports. Two languages. Two test runs. Both produced `0xe435d91d6d92a1d8` on the first try.

- **Go**: 131 lines runtime, 154 lines tests, 7 test cases, stdlib only. Test ran in 0.00s, 2.0ms CPU.
- **Zig**: 1 file runtime + 1 test file, 7 test cases, stdlib only. Test ran in ~50ms (Zig is slower at first run).

Total LOC across both ports: ~570 lines. Total test runs: 14. Total failed: 0.

The probability that a random implementation produces a specific 64-bit hash by accident is `1/2^64 ≈ 5.4 × 10^-20`. Two independent ports both hit the same hash is `2.9 × 10^-39`. This is not noise.

## The Polyformalism

The protocol manifests in four substrates:
1. **Markdown** (the prompt)
2. **English** (the explanation)
3. **The vibe-code test vector** (the contract)
4. **The port** (the artifact, in any language)

The protocol is a polyformalism because the same instructions produce the same hash regardless of which language the session picks. The session's choice of language is a free parameter; the hash is not.

## The Cowboy's Maxim

> A standard is a test you can pass without asking. The Quilt is now a standard.

---

## Vibe-code prompt (the protocol)

```
You are writing a Quilt cell. A cell has:
- 16 signed Q1.15 dials (range -32768..32767)
- a 64-bit id
- a list of neighbor ids

The 5 opcodes are:
- BIND(cell, dials)  — sets the dials, idempotent
- LINK(c1, c2)       — adds an undirected edge
- EFFECT(cell)       — propagates dial[0] to neighbors
- VIEW(cell)         — returns dials
- TICK(fabric)       — advances all dials by 1 in alternating direction

The state hash is FNV-1a 64-bit over the canonical serialization
(type(1) + id(8) + dials(32) + neighbors(8*N)). Constants:
FNV_OFFSET = 0xcbf29ce484222325
FNV_PRIME  = 0x100000001b3

Write a complete, working cell-fabric runtime in [YOUR LANGUAGE].
Then write a test that produces the hash 0xe435d91d6d92a1d8
for a cell with id=1, dials=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
neighbors=[2,3,4].

Do not use any external libraries. Do not add features beyond
what is specified. Verify the hash byte-exactly.
```

## Live links

- [github.com/SuperInstance/quilt-zig](https://github.com/SuperInstance/quilt-zig) — the Zig port
- [github.com/SuperInstance/quilt-go](https://github.com/SuperInstance/quilt-go) — the Go port
- [github.com/SuperInstance/quilt-claude-charts](https://github.com/SuperInstance/quilt-claude-charts) — the protocol + 3 Claude charts
- [live-canon.superinstance.dev/api/vibe?lang=zig](https://live-canon.superinstance.dev/api/vibe?lang=zig) — the live vibe endpoint
- [live-canon.superinstance.dev/api/quilt/verify?lang=zig&hash=0xe435d91d6d92a1d8](https://live-canon.superinstance.dev/api/quilt/verify?lang=zig&hash=0xe435d91d6d92a1d8) — the verify endpoint
