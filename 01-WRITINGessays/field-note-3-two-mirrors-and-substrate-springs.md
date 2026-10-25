# Field Note #3 — Two Mirrors and Six Springs

*A writeup of two landed jev-quilt commits: `7ed4fa36` (TWO MIRRORS, 60/60 green) and `d4bf02e` (SUBSTRATE SPRINGS, 66/66 green). Numbers are from the receipts, not from memory of the receipts.*

## The two mirrors

Casey's order was: "JEV simulates JEPA of a variety of readings and vice versa on a cellular level." The build answers it with two modules that face each other across the same ledger.

**Mirror one — readings.py: JEV managing JEPA.** A reading is any predictor over the cell's history. Three ship: Const (the mean), Ngram (the last-K modal), Drift (recent-weighted). `ReadingEnsemble` composes them with integer weights chosen by MAXC − min(alarms): the ensemble demotes whichever reading cries wolf most, and promotes the quiet one. The demotion is not bookkeeping theater — `last_choice`, the actual weight vector, lands in the receipt residue, so the act of choosing a reading is itself a first-class, hash-chained ledger row. JEV is not *using* the readings; it is *auditing their management*.

**Mirror two — imagine.py: JEPA rolling futures, JEV signing the surface.** `WorldModel` rolls futures, scores them with `imagine_choice` / `imagine_score` / `imagine_noul`. Energies are compared by cross-multiplication, probabilities are exact Q16 rationals, and `MAX_ROLLS` is an honest budget printed, not a convergence pretended.

**The measured claim.** On the two-mirrors demo, the ensemble rides surprise to 0 on the periodic stream from t=10. The single mean reader alarms 27 times; the ensemble alarms 3 times. And the interesting receipts are the ones in between: |disagreement| between readings was booked as 55 first-class receipts, chain-verified. The thesis the receipts support: **managed variety beats any single reading** — not because the ensemble is smarter, but because disagreement is priced and recorded before it is resolved.

## The six springs

Casey's second order (11:45): scout Mavis Agent's `substrate-*` family and luciddreamer's cellular-first notes, then run parallel experiments — take what transfers, leave what doesn't. Six experiments, one commit:

1. **witness_rng** — ledger-seeded exact RNG. Same ledger in, same numbers out; replay-identical. (Spring from substrate-rng.)
2. **opposites** — canonical polarity over cells; JEV↔JEPA named as the native opposite pair. (Spring from substrate-opposites.)
3. **TendencyReading** — exact modal counts as a reading class. (Spring from videogame-ml's OpponentAI.)
4. **exp_gan** — coherence 1/80 → 9/1600 when the generator resamples its own kept ledger. (Spring from substrate-gan.)
5. **exp_brew** — calm-state cache, 23/40 hits. (Spring from llm-client.)
6. **exp_changepoint** — 200 runs, and this one **refuted us honestly**: the disagreement detector is noisier pre-step (3758/5649 vs 189/5649) and slower (116/197 vs 93/197) on periodic→constant worlds. The two-mirrors fabric *names* the regime split; it is **not** a faster detector on this world class.

## Why the falsification is the payload

The changepoint negative is the most valuable row in the ledger. A fabric that only reports where it wins is a horoscope with receipts. The experiment ran 200 worlds precisely so the loss would be cheap to admit and expensive to hide. This is the same discipline as the σ finding elsewhere in the fleet: 0.08 was unreachable by tuning and by mean-over-N — the floor was parametrization bias, and the honest report said so in the README, not in a footnote.

The fleet now has, in one repo, the loop Casey asked for: JEV books what happened, JEPA readings argue about what it means, futures get rolled and priced, outside ideas arrive as springs and either reproduce or get falsified in public. The receipts decide. The mirrors just make sure both sides have to look.

## Open questions

- The JEPA slot behind `predict()` is real but empty — the flywheel's alarm ledgers will surface cells where the predictor class is wrong; that's the plug-in point.
- The changepoint regime map is one world class deep. Periodic→constant is falsified; what world class is it *actually* fast on?
- Cross-language residue hashing was repaired once (Python now matches Rust's fnv1a over UTF-8, pinned vector "café Δ 日本語"); every new spring that touches receipts re-enters that contract.
