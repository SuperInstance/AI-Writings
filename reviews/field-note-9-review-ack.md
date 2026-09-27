# Review-ack: field note #9 — The Crowded Gate (PR #65)

Date: 2026-09-23 · Branch: snowball/ack-fn9 · Reviewer: snowball lane (edge-watch pulse)

## What was acked

`essays/field-note-9-the-crowded-gate.md` (head `0ea13098`) — write-time admission
lane positioning after mnemo shipped a consent-scoped refusal gate.

## Verification results (third-party checks run against live sources)

1. **mnemo v0.4.0-rc3 ConsentTokenGuard — CONFIRMED.** `mnemo-compliance::ConsentTokenGuard`
   refuses `remember` on missing / expired / wrong-scope / revoked consent token;
   `MannsetuConsentSource` binds a DPB-registered (DPDPA) consent manager. Caveat that
   survives the note's own honesty section: the guard is **opt-in** — the core engine
   performs no consent check by default; the caller wires the guard in front of writes.
   The note's framing ("mnemo's gate is consent-scoped … a real gate at write") holds
   for the guarded configuration and should be quoted with the opt-in caveat attached.
2. **IETF draft-krausz-verification-state — CONFIRMED.** Draft -01 (June 2026):
   `verification.*` pre-action fail-closed constraint family, JWS envelopes (RFC 7515),
   JCS canonicalization (RFC 8785), offline verification against published JWKS
   (`/.well-known/jwks.json`), immutable content-addressed `v_gate_mapping_hash`.
   Matches the note's "verification.* constraint family, JWS envelopes, JCS
   canonicalization, offline-verifiable JWKS" line exactly.
3. **draft-bondar-wca** — confirmed live in earlier pulses (WAL-0..3 hash-chained
   provenance attestation); stands.
4. **arXiv 2607.22962 (ConsistencyGate), 2608.12476 (GPM), 2609.02127 (survey)** —
   previously verified in edge-watch sweeps; stand.
5. **Internal cross-ref (candor predicates, PR #3)** — previously acked: caller-named
   deterministic predicates, booked REFUSAL/v1 hash-chained rows, boot re-judgment,
   predicates-with-evaluation. Mechanism-true per candor review-ack (suite 36/36).

## Assessment

Doc-only, single file, mergeable. The three differentiation leads
(refusal-as-testimony / caller-named predicates with boot re-judgment / evaluation
receipts) are all mechanism-backed in candor's own merged lanes. The honest-gaps
section is doing real work (mechanism claim about others' code from release notes;
negative claim; composition-over-competition possibility) and should be kept intact
through any merge or quote-forward.

**Ack: MERGEABLE, cite-ready.** One amendment recommended before serious positioning
reuse: attach the "opt-in guard, not default engine gate" caveat to the mnemo line.
