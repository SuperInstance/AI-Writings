# 05 — Open Problems (the five gaps the source named)

1. **Temporal de-noising.** A keystroke is a noisy proxy for intent:
   hesitation masquerades as deliberation; a backspace storm reads as
   intent reversal but is often muscle error. The course assumes a
   *jitter sieve* between physical stream and intent mask, but the
   sieve's shape is unbuilt. Every claim downstream of the mask
   inherits this noise. **Status: unbuilt, load-bearing.**

2. **The adjudicator's boundary.** A conservative form-checker cannot
   judge semantic correctness, only shape. The course routes around
   this by making the adjudicator small and the ledger loud — but the
   boundary of "shape vs meaning" is drawn by hand, in prose, and the
   source knows it. **Status: hand-drawn, unformalized.**

3. **The intent mask's weighting schema.** The mask is computed from
   multiple signals (keys, voice, focus, recent history) whose weights
   are tuned, not derived. A schema exercise exists in principle (the
   source gestures at it); no receipts exist for any weighting.
   **Status: tuned by feel.**

4. **Substrate proofs.** Module 4 assumes hash-chained receipts and
   content-addressed patches are sufficient for audit; the source does
   not address what a compromised *adjudicator itself* could fake, nor
   any zero-knowledge alternative. **Status: out of scope, named.**

5. **Compression of context under compaction.** Module 3's compaction
   sheds context the future may need; the source offers no mechanism
   for predicting what the future will ask. The bet is honest; the
   odds are unpriced. **Status: an honest bet, unpriced.**

**Common thread:** every open problem is a place where the course's own
receipts culture says *no receipts exist for this claim.* Build those
receipts and the problem closes; assert them and the course's doctrine
collapses on itself.
