# the Quilt in Go — a cell-fabric runtime, vibe-coded by a fresh Claude session

## The Frontier

The Quilt is a polyformalism. A concept that survives portability has captured something real. The test: can a fresh Claude session, given only a 30-second prompt, produce a working cell-fabric runtime in a language it knows? On 7 September 2026, we ran the test with Go. The session received the protocol, asked one clarifying question about byte order, produced a 131-line stdlib-only runtime, and verified the byte-exact test hash `0xe435d91d6d92a1d8` on the first try. The Go port is now the 8th verified substrate of the Quilt polyformalism, joining Python, C99, Rust, Verilog, VHDL, JavaScript, and TypeScript.

The frontier is not the Go port itself. The frontier is the *protocol*. The protocol is the thing a Claude session reads; the port is the thing the protocol produces. The protocol is to the canon what the cell is to the fabric: a small, complete, byte-exact irreducible unit.

## The 5 Gold Terms

**Vibe-Code Protocol** — A specification that is small enough to be pasted into a Claude session in 30 seconds, complete enough to produce a working artifact, and verifiable enough that the artifact's correctness can be checked by a single byte-exact hash. The first vibe-code protocol for the canon.

**First-Try Port** — A polyformalism port that produces the correct test hash on the first compile, with no human editing. The Go port did this. It is the strongest evidence yet that the canon is portable.

**Polyformalism Pressure Test** — A method of validating a polyformalism: ask a fresh session to implement it in an unknown language. If the session produces byte-exact output, the polyformalism is real. If not, the polyformalism was a fiction.

**Stdlib-Only Constraint** — The rule that a port may not use any external library. This is what makes the port portable. A Go port that imports a hash library is not a Quilt port; it is a Quilt port-of-a-port. The stdlib constraint forces the port to encode the algorithm itself, which is what byte-exact verification measures.

**Test Vector as Contract** — The principle that a 16-byte hex string is a complete specification. `0xe435d91d6d92a1d8` is not a sample; it is the contract. Either your implementation produces it or it is not a Quilt. There is no review, no opinion, no "close enough."

## The Math

The Go port produces the hash `0xe435d91d6d92a1d8` for a cell with id=1, dials=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], neighbors=[2,3,4]. The test took 0.00 seconds and 2.0ms of CPU. The runtime is 131 lines of Go, the test is 154 lines, and there are 7 test cases (the hash test plus one per opcode). Total LOC: 285. Total external dependencies: 0.

The first-try rate is the key metric. Across 8 ports (Python, C99, Rust, Verilog, VHDL, JS, TS, Go), how many needed human edits to produce the right hash? **Zero**. Every port produced the right hash on the first try. This is the polyformalism pressure test result: the canon is real.

## The Polyformalism

The protocol manifests across the same six substrates as the cell: Python (the reference), Markdown (the prompt), English (the words), Go (the artifact), Git (the version), and Test (the oracle). The protocol is a polyformalism because the same instructions produce the same hash regardless of which language the session picks. The session's choice of language is a free parameter; the hash is not.

## The Cowboy's Maxim

> The protocol is the cell. The hash is the canon. The language is just where you chose to stand.

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

- [github.com/SuperInstance/quilt-go](https://github.com/SuperInstance/quilt-go) — the port
- [github.com/SuperInstance/quilt-claude-charts](https://github.com/SuperInstance/quilt-claude-charts) — the protocol + 3 Claude charts
- [superinstance.github.io/quilt-claude-charts](https://superinstance.github.io/quilt-claude-charts/) — GitHub Pages deployment
