# bots/ — and what `witness.log` actually is in here

> **`bots/*/witness.log` are ROW-CHECKSUM logs, not chains.**
> The filename promises a witness; the format does not deliver one. This note
> says which is which, so a verdict about one of these files can be read.

## The measurement

Every `witness.log` in this directory carries the fields
`ts, iso, event, payload, hash`. **None of them carries a `prev` or a
`prev_hash`.** The `hash` is a 16-hex-char checksum of the row's own
payload — it commits a row to itself and to nothing else.

| bot | rows | linkage class |
|---|---|---|
| `rsi-gan` | 262 | `row-checksum` |
| `snowball-scout` | 21 | `row-checksum` |
| `autoclaw-bg` | 14 | `row-checksum` |
| `wesley-mechanic` | 9 | `row-checksum` |
| `bruno-architect` | 8 | `row-checksum` |
| `casper-critic` | 4 | `row-checksum` |
| `jevvy-auditor` | 4 | `row-checksum` |
| `herman-historian` | 2 | `row-checksum` |
| `kira-cartographer` | 2 | `row-checksum` |
| `marcel-composer` | 2 | `row-checksum` |

**10 logs, 328 rows, 0 with linkage.**

A chain is a sequence in which each element's commitment covers its
**predecessor**. These rows do not cover each other, so deleting one leaves
the survivors perfectly valid — there is nothing in a surviving row that
remembers it existed.

Measured on the largest of them: drop the last 50 rows of `rsi-gan`'s 262 and
the remaining **212 still verify**. So does deleting the worst 50 runs. The
checksum catches bit-rot and partial corruption. It catches nothing else.

## What this means for the word "intact"

**"intact" is not producible for a `row-checksum` log.** These rows have no
linkage to be intact *with respect to*. A verdict on one of these files says:

> `262/262 row checksums match` — linkage class `row-checksum`
> — deletion and truncation are **undetectable**; this is not a witness log.

A `chain` verdict may say **`chain-intact`**, meaning precisely *the chain
verified*. That word is not available here.

The honest general word for these files is **attestable** — and even that is
generous, because it implies a chain. What they have is bit-rot detection.

## If a bot wants a real witness log

Write `witness-chain/1` records, using
[`../labs/situation-recorder/recorder.py`](../labs/situation-recorder/recorder.py)
or the spec it implements. Do not keep calling a checksum a chain — the
filename already borrows credibility the format cannot return. And note that
even a proper chain is not tamper-evident until its signed head is published
out of band; see below.

## The house vocabulary

A log earns **tamper-evident** only when all three legs hold:

1. **chain re-derives** — replay reproduces every linkage
2. **head signed** by a key we trust
3. **head published out of band**, where the log writer does not control it

These logs hold **none** of them. `labs/situation-recorder/` transcripts hold
**leg 1 only** and are therefore **attestable**. Nothing in this repo currently
holds leg 3 — there is no `witness-heads/` and no committed signature beside
any log, which is the gap that has to be closed before any log here can be
called tamper-evident.

Normative definition:
[`SuperInstance/witness-spec`](https://github.com/SuperInstance/witness-spec)
`SPEC.md` — *Linkage class* and *Tamper-evidence — the three legs*.
