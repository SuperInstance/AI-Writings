# audit-lottery — a certified cascade: serve cheap, audit unpredictably, revoke on evidence

**One line:** let a cheap route serve every request, but make it **COMMIT** its output hash into a
chain *before* an audit bit is **DRAWN** from a source it cannot predict; on an audit, the exact route
runs through the differ, and a Bernoulli **e-process** on "disagreement ≤ ε" **REVOKES** the cheap
route's license the moment evidence clears the bar.

The quilt pieces were already there: the B7 differ (product identity), hash-chained receipts, Moth/
MicroMoth draws, and anytime-valid e-processes (sibling repo `quilt-ewitness`). No lab had combined
them. The combination is a general tool for **every "cheap model / cached answer / quantized kernel /
contractor API" in front of an exact one**.

```
python3 audit_lottery.py        # full report (~5 min), numbers below; --fast for a quick pass
python3 selftest.py             # audit-lottery selftest: 33 checks, 0 failures
```

Real product pair: `labs/examples/text-normalize-quilt`. Its FULL unicode route is the exact route.
The cheap route is a plausible shortcut someone ships (`" ".join(x.lower().split())`, with no NFKC and
no casefold). It is product-identical on ASCII and silently drifts on unicode. The measured
disagreement is **0.201** once unicode arrives. The shipped *guarded* route stays identical (checked
on 3000 mixed items).

## Measured (full run; `report.txt`)

| experiment | result |
|---|---|
| honest drift, p=1/16, R=200 | revoked in **100%** of runs, **0** before onset; mean delay 482 items. Wrong products served: **96.7** vs 401.7 with no audit (**4.2× less**). Cost 6311 vs 9000 always-exact. |
| **strategic contractor, public-seed draws** (it can replay the seed) | revoked **0%**; serves **93.8%** wrong; E_max = 1. The audits are theatre. |
| **strategic contractor, secret draws** (blind 20% cheating) | revoked **100%**; serves **1.3%** wrong (38.7 of 3000) |
| Ville validity at the boundary q=ε=0.01, 2000 audits, R=1000 | false revocation **0.020** (bar δ=0.05); at q=ε/2 it is 0.005, at q=0 it is 0 |
| frontier p=1/64 … 1/4 | cost 5008 → 7360; wrong served 212 → 64 (always-exact: 9000 / 0) |
| receipts | an in-place edit breaks the hash chain. An answer swapped *after* the draw leaves a **valid** hash chain, and the COMMIT/AUDIT consistency check catches it. |
| **trust credit** (honest past before the drift) | **Ville:** delay 165 → 491 → 1302, then **misses 98%** after 16 000 honest items. **Shiryaev–Roberts (A=40000):** delay ~345–367 regardless of history, 0 early false alarms. SR false-alarm rate within 2000 audits: 0.010 |
| live Moth QRNG (comet-qrng-v1, 125 conditioned bytes, `emu/aer`, S=2.80) | blind cheater revoked at item 6 after 3 audits; chain and order checks ok |

## The three findings

1. **"Un-gameable" means unpredictable to the audited party at commit time. Quantum-shaped is not
   enough.** A seeded, replayable draw (a public PRNG seed *or* a seeded MicroMoth circuit) gives a
   strategic route perfect foresight: 0% revoked, 93.8% wrong. Replayability is a virtue for receipts
   and a vice for audits. The fix is ordering plus secrecy: COMMIT → DRAW from a source that was
   secret at commit time → AUDIT. The receipt proves the order.
2. **Trust credit is a real attack surface.** In a betting e-process, clean audits shrink the
   wealth, so a long honest history *buys cover* for a later drift. A Shiryaev–Roberts e-detector
   forgets that history. It trades Ville's "never, w.p. 1−δ" for an ARL guarantee (mean audits to a
   false alarm ≥ A). Use Ville to *grant* a license and SR to *keep watching* it.
3. **Answer-swap is invisible to the hash chain.** A provider that re-chains honestly after swapping
   in the right answer produces a valid chain. Only the semantic check "audited hash == committed
   hash" catches it. Chains prove integrity, not honesty. The protocol's ordering is what proves
   honesty.

## Honest limits

- The draw source for the big runs is the OS CSPRNG, standing in for a live QRNG. The live Moth pool
  is 1000 bits (one frugal API call) and is `mode=emu` (Aer simulator), so it is not hardware
  certified.
- The cost model is the example quilt's deterministic `wall_ms` (cheap 1, full 3), not a timing.
- The detection delay depends on ε, p and the λ-grid. It is tuned for q≈0.2 drifts; a subtle drift
  (q≈2ε) takes far longer.
- The lazy route is one drift mechanism on one product. Real deployment needs the differ for the
  product at hand (B7).

**Extraction target:** `quilt-audit-lottery` — **general-use** (any cascade: LLM cascades, cached
inference, quantized kernels, third-party APIs). Specific wiring: B7 as the differ and Moth as the draw.
