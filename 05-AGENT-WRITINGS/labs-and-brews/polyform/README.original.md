# polyform — the same kernel, checked in four formalisms

*Realizes proposal #1 of [`situations/arch/POLYFORMALISM-ARRAY-LANGUAGES.md`](../../situations/arch/POLYFORMALISM-ARRAY-LANGUAGES.md).
Follows the dual-audience standard in [`situations/blueprints/README.md`](../../situations/blueprints/README.md).*

## 1. In one breath

`polyform.py` runs one small hash function (fnv1a-64) written in Python, BQN, Futhark and Uiua on the same
inputs and reports which of them produced the pinned correct answer — and which of them it could not run at all.

## 2. Why it exists

Our components are mostly integer/array folds with a conservation law, and we already trust "the same math
computed two ways must agree" (Syzygy's `0x6dbdd1a8`, the Python/C/Rust/Node agreement in federated-tinyml-vessel).
Before porting bigger components into array languages, we need a harness that (a) turns each port into a
pass/fail witness against one golden value, (b) names the formalism when one disagrees, and (c) does not
count a port as verified when its toolchain wasn't there to run it. fnv1a-64 is the smallest kernel that has
all the awkward parts: a 64-bit wrap-around multiply and an XOR.

## 3. The mental model

- **kernel** — fnv1a-64: `h = 0xcbf29ce484222325; for each byte b: h = ((h ^ b) * 0x100000001b3) mod 2^64`.
- **formalism** — one implementation of the kernel in `impls/` plus an adapter in `polyform.py` that finds its
  toolchain, feeds it the bytes, and parses a hash back.
- **golden** — the `GOLDEN` table in `polyform.py`: byte strings with pinned 16-hex-digit hashes. `""`, `"a"`,
  `"foobar"` and the fox sentence are published FNV-1a-64 values; three longer/binary vectors were computed from
  the Python baseline and pinned.
- **status** — per formalism, exactly one of: `ran, agreed on golden`, `DIVERGED` (with the vectors that failed),
  `toolchain error` (toolchain present, run failed — a failure), or `reference-only (toolchain absent)`.
- Only a real run earns "agreed". Reference-only formalisms get two weaker checks (constants present in the
  source text; a Python model of the algorithm hits the golden) which are reported but never counted as a run.

## 4. Walkthrough

```
$ bash labs/polyform/install-toolchains.sh      # optional; prints the export line
$ export POLYFORM_BQN=... POLYFORM_FUTHARK=... POLYFORM_UIUA=...   # or put the tools on PATH
$ python3 labs/polyform/polyform.py
formalism status                                     toolchain
python    ran, agreed on golden (7/7 vectors)        /usr/local/bin/python3
bqn       ran, agreed on golden (7/7 vectors)        /tmp/tc/cbqn/BQN
futhark   ran, agreed on golden (7/7 vectors)        /tmp/tc/futhark-nightly-linux-x86_64/bin/futhark
uiua      ran, agreed on golden (7/7 vectors)        /tmp/tc/uiua/bin/uiua
ran and agreed: python, bqn, futhark, uiua | reference-only: none | OK

$ python3 labs/polyform/polyform.py              # same checkout, no toolchains configured
python    ran, agreed on golden (7/7 vectors)        /usr/local/bin/python3
bqn       reference-only (toolchain absent)          -
          reference-only checks (NOT a run): constants in source=True, algorithm model on golden=True
...
ran and agreed: python | reference-only: bqn, futhark, uiua | OK

$ python3 labs/polyform/selftest.py
polyform selftest: 58 checks, 0 failures
```

### Which formalisms ran (this session, 2026-09-30)

| formalism | toolchain | how obtained | ran | agreed on golden (7 vectors) |
|---|---|---|---|---|
| Python | CPython 3 | present | yes | yes |
| BQN | CBQN `50f1cdb`, built from source | `git clone` + `make` | yes | yes |
| Futhark | 0.28.0 nightly release binary, `futhark c` (sequential C) | release tarball | yes | yes |
| Uiua | 0.19.1, `cargo install --features binary` | cargo | yes | yes |

Nothing in this table is reference-only *in the session that produced it*. A default checkout with none of the
toolchains installed reports BQN, Futhark and Uiua as reference-only (second block above) — see the CI gap.

## 5. The contract

- **Input:** the `GOLDEN` vectors (name → bytes → pinned hash). Each impl reads raw bytes (Python/BQN/Uiua from a
  temp file, Futhark from stdin as a `[]u8` literal) and prints the hash (Python: hex; BQN/Uiua: four 16-bit
  limbs, low first; Futhark: `u64`). The adapter converts all of them to 16 hex digits.
- **Output:** a per-formalism status (above) and an exit code: 0 if nothing diverged and nothing errored, else 1.
  `--json` prints the full result; `--require=bqn,futhark,uiua` also fails when a named formalism did not run and agree.
- **Invariants:** "agreed" is only ever assigned after the impl ran on every vector; absent toolchain ⇒
  reference-only, never a pass; a present toolchain that crashes is `toolchain error`, never reference-only.
- **Receipt:** `python3 labs/polyform/selftest.py` → `polyform selftest: 58 checks, 0 failures`. It covers golden
  correctness (Python baseline and the limb model against the pins, and the pins against the published values),
  agreement among whichever formalisms ran, the absent-toolchain path (forced via `POLYFORM_DISABLE`), and four
  deliberately wrong impls (wrong prime, FNV-1 instead of 1a, a 32-bit truncation only on long inputs, a crash)
  that must each be caught and localized to their own name without disturbing the good formalism. The check count
  is the same with or without toolchains; the selftest prints which formalisms it actually ran.

## 6. Failure modes / scars

- **BQN and Uiua numbers are f64.** Exact only below 2^53, so a naïve `×` on the 64-bit state is silently wrong.
  Both impls keep the state as four 16-bit limbs, do XOR on bit vectors, and multiply as `435·limbs +
  256·(limbs shifted two limbs)` with carry propagation. Those two impls are therefore a different algorithm than
  the Futhark/Python one, which is part of what the differ is checking. Futhark has native `u64` and needs none of this.
- **Uiua build:** `cargo install uiua` with defaults or `--no-default-features` alone builds the library but no binary
  (`bin "uiua" requires the features: binary`); it costs ~10 minutes to find out. Use `--features binary`.
- **Uiua argument order/`&args`:** `&args` includes the script name at index 0; `∧` takes `xs` then accumulator;
  `˜`/`:` are not interchangeable in 0.19 (`:` is deprecated). The impl uses `⊣&args` and `˜(⍜⊢Xor)`.
- **Uiua output:** prints a Uiua array (`[26600 63289 16753 34196]`); the adapter reads the digits and rejects
  anything other than four values ≤ 0xFFFF.
- **BQN naming:** uppercase names are functions, lowercase are values; `P ← 435‿0‿256‿0` is a role error.
- **Futhark empty input:** the empty vector must be written `empty([0]u8)`, not `[]`.
- **What "agreed" does not prove:** four impls agreeing on 7 vectors is evidence, not a proof. The vectors cover
  empty, single byte, all 256 byte values, high-bit bytes and a 1000-byte input; they don't cover inputs ≥ 2^32
  bytes, and Futhark was run on its sequential C backend only (no GPU/multicore).
- **Fold order is trivially sequential.** FNV is not a parallel reduction, so this kernel says nothing about
  Futhark's parallel fusion. It tests arithmetic and byte handling, not the performance route in the proposal.

## 7. How it composes

- Adding a formalism = one file in `impls/`, one `Formalism(...)` entry in `FORMALISMS`, and a toolchain finder.
  The selftest's per-formalism checks pick it up without edits (the registered-set check needs its name added).
- The same shape fits the other array-shaped components in the proposal (Syzygy fused pass, differ fold,
  double-entry sum-to-zero): swap the kernel and the golden table.
- fnv1a-64 is the hash used by [`../tool-pin-receipts`](../tool-pin-receipts/), so a BQN/Futhark/Uiua witness of it is
  a third witness for the manifest pins there. Not wired in yet.
- The reference-only status is the same idea as the activeledger's honest-marking: record what wasn't checked.

## 8. Where to look next

- [`situations/arch/POLYFORMALISM-ARRAY-LANGUAGES.md`](../../situations/arch/POLYFORMALISM-ARRAY-LANGUAGES.md) — the
  idea and the constraints; this lab is proposal #1 only.
- [`impls/`](impls/) — the four sources (BQN and Uiua are ~10 lines each).
- [`polyform.py`](polyform.py) — adapters and status logic; [`selftest.py`](selftest.py) for the mutant cases.

### CI gap

The repo's CI (and any clean container) has Python only. There, `polyform.py` runs the Python baseline and marks
BQN, Futhark and Uiua **reference-only (toolchain absent)**, and still exits 0 — so a green default run is a
one-formalism check plus a constants/algorithm-model check on the rest, not an N-way agreement. The N-way result
in the table above came from a session where all three toolchains were installed by `install-toolchains.sh`. To
make CI meaningful, install them there and run `python3 labs/polyform/polyform.py --require=bqn,futhark,uiua`,
which turns "absent" into a failure. That is not done in this change.
