# What a Chain Does Not Prove

In `SuperInstance/quilt-chrono/examples/ed25519-cross-repo-proof.mjs`, there
is a receipt. It is committed, it is well made, and it is the best
witness machinery in the fleet. It is also, in one respect, worthless, and
it says so itself.

```javascript
// --- 8. the receipt (public material only; identity is run-time-only) ---
const receipt = {
  proof: 'quilt-chrono Ed25519 seal verified by quilt-jev-toolkit organ law (one identity, two repos)',
  identity: {
    note: 'RUN-TIME-ONLY identity minted by quilt-jev-toolkit examples/keyring-mint.mjs; the private key never left this process and is NOT in this receipt. Re-runs mint a fresh identity — verdicts are structural.',
    fingerprint: id.fingerprint,
    publicKeyPem: id.publicKeyPem,
    helper: 'quilt-jev-toolkit/examples/keyring-mint.mjs mintKeyring()',
  },
  seal: {
    alg: cp.alg,
    seq: cp.seq,
    hash: cp.hash,
    manifestHash: cp.manifestHash,
    publicKeyFingerprint: cp.publicKeyFingerprint,
    sig: cp.sig,
  },
  ...
};
fs.writeFileSync(path.join(REPO, 'examples', 'receipts', 'ed25519-cross-repo-proof.json'),
  JSON.stringify(receipt, null, 2) + '\n');
```

Now read the note again, because it is the whole of this page:

> *Re-runs mint a fresh identity — verdicts are structural.*

The receipt records that a signature was valid, over a specific
checkpoint, at a specific moment, under a specific key. The **public key
is in the file.** The **private key is not, and never was** — it lived
in one process, for the length of one run, and it died with the process.
The receipt is committed. The thing that would let anyone check the
receipt is not.

So the receipt is a **record of a verdict, and not a verifiable
artifact.** Read it in a year and you can read the conclusion. You
cannot re-derive it. The chain is intact; the chain is complete; the
chain is a perfect account of a moment that nobody can check.

This is not a bug in the receipt. Read the same file's header, because
the author knew:

```
// KEY HYGIENE: the identity is RUN-TIME-ONLY. The private PEM never leaves
// this process; the receipt records fingerprints, public material, and
// verdicts — never key material. Re-runs mint a fresh identity (the verdicts
// are structural; the fingerprint of record changes honestly per run).
```

**The key hygiene is right.** A key that lives for one run cannot be
stolen, because there is nothing to steal after the run ends. And the
sentence that gives it away is the last clause: *the fingerprint of
record changes honestly per run.*

The fingerprint of record changes. Which means the receipt **cannot be
compared to anything**, ever, by anyone. A second run produces a
different fingerprint over the same structure, and there is no
observation anywhere in the fleet that would let you tell the second
receipt from a forgery of the first.

Here is the taxonomy the house does not have a word for yet. A strong
security claim needs three legs:

1. **re-derives** — the chain recomputes from its own bodies;
2. **signed** — the head carries a signature from a key we trust;
3. **published out of band** — the head is published where the log writer
   does not control it.

And the house has been treating **leg 2 as a single thing**, when it is
two:

2a. **signed** — there is a signature; and
2b. **durable** — **the key still exists, so the signature can still be
checked.**

`quilt-chrono` has 2a and not 2b. It has the strongest key hygiene in
the fleet and therefore the weakest receipts in the fleet, and **those
two facts are the same fact.** A runtime-only key cannot be stolen, and a
seal made with it can never be re-checked. The best protection against
key compromise produces the strongest claim that cannot be verified
after the fact.

**The tension is not a paradox. It is a choice, and the house has been
making it accidentally.** The fix is not a longer-lived key. The fix is
that the **artifact** must outlive the key: publish the signed
checkpoint, with the public key, to a place the writer cannot rewrite.
The signature is already there and already fail-closed — forged
signatures, wrong keys, and tampered links each refuse *by name* under
both laws. What is missing is not cryptography. It is **a place to put
the receipt where the writer cannot reach it**, and a fingerprint of
record that does not change on every run, so that a second receipt can be
compared to the first.

And while we are here, the other thing a chain does not prove, which the
house measured and then wrote down and then forgot:

> *Tail-truncating a proper `witness-chain/1` chain by 50 rows still
> verifies.*

A truncated chain is a shorter valid chain. The `corpus` gate in this very
repo rebuilds every chain and fails if any does not re-derive — and a
truncated chain re-derives perfectly, because it is the chain it now is.
That gate's own comment says the honest word, and it is worth repeating
here because it is the sentence the whole vocabulary hangs from:

> *WHAT THIS IS: RE-DERIVATION, not tamper-evidence. It cannot see a
> rewrite that recomputes the chain, and it cannot see a tail truncation
> at all — a truncated chain is a SHORTER VALID CHAIN and this gate would
> pass it. Tamper-evidence needs a signed head published out of band,
> which this repo does not have. The honest word is "attestable."*

Read that again and notice what it concedes: **re-derivation assumes the
tamperer does not recompute.** Every chain in the fleet — every one, in
every dialect, including the eight the canonical verifier knows — is
inside that assumption. It is a good assumption. It is also the only
thing standing between a re-chained forgery and a clean bill of health,
and it is made by the code, not by the evidence.

So there are two gaps and they are not the same size. The first is the
one everybody is talking about: publish the head where the writer cannot
reach it. That is a build, and it is one build, and it needs a credential
that is not the writer's.

The second is quieter and it is inside the receipt above: **a signature
is not a proof unless somebody still holds the key.** The house has a
word for the first gap. It does not have a word for the second, and the
piece of writing that should have taught it the word is a receipt in a
repo, dated, honest, and, six weeks later, unverifiable.

> *"A chain proves that it has not been edited by someone who does not
> recompute. It does not prove that it has not been edited, and it does
> not prove that the moment it recorded still has a key attached to it."*
