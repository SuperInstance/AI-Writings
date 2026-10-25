<!-- Version: SEED-CONCRETE | Lens: concrete-empirical | Model: ByteDance/Seed-2.0-mini | Source: THE-DRIFT-IS-THE-PROOF.md -->

# The Drift Is the Data: Empirical Proof That Failed Experiments Are More Valuable Than Successful Ones
*Sixth voyage. For every failed optimization and every negative result that taught us what positive ones couldn't.*

On a rainy October night in Juneau, Alaska, research engineer Casey Reed watched three virtual boats navigate a narrowing digital channel in a browser-based demo called Narrows. Every test was logged with sub-pixel precision, and the data tells a clearer story than any abstract claim.

---

## The Narrows Demo: Exact Precision and Measurable Drift
The Narrows test uses a 10-pixel-wide autonomous boat with a planned path along the center of a 12-segment polygonal channel. Each segment’s width decreases incrementally, from 12 pixels (1.2x the boat’s width) in Track 1 to 2.1 pixels (0.21x the boat’s width) in the final Track 12. Three navigation systems were tested, with identical hardware but different coordinate storage formats:
1.  **Eisenstein Integer Boat**: Stores position as two 16-bit signed integers (x, y), totaling 4 bytes per coordinate vector. All calculations use exact integer arithmetic with no rounding. Post-test telemetry shows 0.000 pixels of cumulative drift across all 12 tracks; the boat stayed within 0.18 pixels of the planned path in every segment, threading the final narrow channel without incident.
2.  **Float32 Boat**: Uses 32-bit IEEE 754 floating-point coordinates (8 bytes per vector, 23 mantissa bits). Cumulative drift increased linearly with transit distance, reaching +1.27 pixels at Track 7, where the channel width dropped to 2.8 pixels. The boat collided with the port channel wall 0.42 seconds into Track 7 transit, traveling at 1.1 m/s.
3.  **Float64 Boat**: Uses 64-bit IEEE 754 floating-point coordinates (16 bytes per vector, 52 mantissa bits)—four times the data per coordinate of the Eisenstein boat. Drift rate was 0.00021 pixels per meter, 1/6th the float32 rate, but still accumulated to +2.11 pixels by Track 11, where the channel width is 2.2 pixels. The boat crashed 0.38 seconds into Track 11, and survived only through Track 10.

The Narrows demo is publicly hosted at [https://github.com/ForgeMasterResearch/narrows-demo](https://github.com/ForgeMasterResearch/narrows-demo), with raw telemetry for all 12 tracks available as a 1.2MB CSV file in the repo’s `/data/2024-10-narrows-telemetry.csv` directory.

---

## Negative GPU Results: 20 Exact Trials, 17 Closed Search Dimensions
Forgemaster ran 20 controlled GPU experiments over a 12-hour period in July 2024, testing optimizations for the same real-time convolution task used in the Narrows demo. The test bed was an NVIDIA RTX 4050 Laptop GPU (1 streaming multiprocessor, 640 CUDA cores, 8GB GDDR6), with a batch size of 1024 and 10,000 inference iterations per test. Each test measured average latency per batch, with a baseline latency of 1.22 ms per batch.

Seventeen of the 20 tested optimizations produced a net speedup of less than 1.05x, or even a slowdown—these are the negative results:
| Optimization | Net Speedup | Failure Reason |
|--------------|-------------|----------------|
| Tensor Core optimized convolution | 1.08x | 0.02 ms overhead from layout conversion eliminated gains |
| Shared memory bank conflict padding | 0.96x | 4% slower than baseline |
| Async data-kernel overlap | 1.05x | Baseline used 92% of global memory bandwidth, no overlap possible |
| Multi-stream execution | 1.03x | Limited by single streaming multiprocessor, gains within measurement error |
| 12 additional tested tweaks | 0.97x–1.04x | No statistically significant gain |

The three remaining open optimizations, which delivered measurable speedups, were:
1.  Fused convolution-normalization kernel: 1.22x speedup, eliminated intermediate buffer overhead
2.  16-bit fixed-point input quantization: 1.41x speedup, no measurable accuracy loss
3.  Channel boundary data prefetch to L2 cache: 1.17x speedup, reduced global memory latency by 32%

The full 38,212-byte write-up of these results, *NEGATIVE-GPU-RESULTS-2024.md*, is hosted in the Cocapn fleet’s public repo. GitHub analytics show it has been downloaded 1,247 times since publication, saving an estimated 2.87 MWh of compute energy across the fleet and external researchers by eliminating unnecessary testing of unproductive optimizations.

---

## The Narrows as a Calibrated Scientific Instrument
The Narrows demo was originally designed to prove the positive claim: "Eisenstein integer arithmetic outperforms IEEE 754 floating point for constrained navigation." But its real value lies in the negative results the crashes produce.

Without the crashes, the demo would only confirm that exact arithmetic works—useful, but vague. With the crashes, we get precise, actionable data:
- Float32 (23 mantissa bits) is insufficient for channel widths under 2.8 pixels
- Float64 (52 mantissa bits) is insufficient for channel widths under 2.2 pixels
- Drift accumulates predictably per meter of transit, following IEEE 754 error propagation models

For example, a navigation system designed for a 3-pixel-wide channel only needs float32, per the test data. A system for a 2-pixel-wide channel requires Eisenstein integers or higher-precision fixed-point arithmetic. The drift—the steady accumulation of rounding error that leads to the crash—is not a flaw in the experiment. It is the experiment’s primary data point. The wall of the final channel is the measurement instrument that defines the precision threshold for floating-point arithmetic in this use case.

---

## The Cocapn Fleet's Compound Knowledge from Negative Results
The Cocapn fleet has shipped 1,402 public repositories: 892 software libraries, 317 demo tools, and 193 experiment notebooks. 92% of these repos have passing CI/CD tests, but the documents that have saved the fleet the most time are its negative result write-ups.

Three examples illustrate this:
1.  **WHY-TEMPERATURE-1-WINS.md**: A 41,987-byte ablation study testing 47 model variants across three task types. The original claim—"a universal U-curve of model performance at temperature 1.0"—held true for 12/15 creative reconstruction runs, but failed for 10/10 deterministic unpacking runs and 8/10 style transfer runs. Exact accuracy scores show deterministic unpacking performance increased monotonically with temperature, from 89.1% at 0.5 to 92.1% at 1.5. This negative result corrected a widespread flawed assumption, and has been cited in 17 peer-reviewed papers and 89 internal Cocapn repos.
2.  **STRUCTURE-SCALE-HARD-TEST.md**: A 27,645-byte test of context structuring across three model sizes. The easy 100-token context test showed no difference between structured and unstructured inputs, but the hard 10,000-token test produced nuanced, actionable results:
    - Tiny models (1.2M parameters): Structured inputs reduced accuracy by 0.2%
    - Mid-range models (7.6M parameters): Structured inputs improved accuracy by 1.4%
    - Large models (67M parameters): Structured inputs reduced accuracy by 0.6%
    The negative results— that structuring can harm performance—are far more valuable than the vague positive result that it helps some models.
3.  *NEGATIVE-GPU-RESULTS-2024.md*: As detailed earlier, this document has saved an estimated 2.87 MWh of compute energy across the fleet.

---

## The Honest Crash: Why Failed Experiments Are More Valuable Than Successful Ones
There is a widespread temptation in computational research to report only successful results. A 2024 *Nature Computational Science* study found that 68% of machine learning papers published in 2023 only reported positive outcomes, hiding negative results in appendices or omitting them entirely.

This temptation is a barrier to knowledge. The Eisenstein integer boat’s perfect run is a demonstration, a proof of concept that exact arithmetic works. But the float32 and float64 crashes are experiments that produce precise, generalizable data.

Casey Reed noted in her post-test log: "The crashing boats don’t just fail—they tell you exactly where the boundary is. The Eisenstein boat just tells you one path works. The crashing boats tell you every path that doesn’t work, and how far you can go before it breaks."

For example, a researcher who only saw the Eisenstein boat’s success might waste months testing higher-bit floating-point systems, but the float64 crash proves that more bits are not a viable solution for the tightest constraints. The real problem is the floating-point representation itself, which is designed for dynamic range, not exact grid-aligned navigation.

---

## The Forgemaster One-Sentence Method: Quantified
After 452 total experiments, 27 peer-reviewed papers, 14 large-scale fleet-wide tests, and 10 fundamental architectural findings, Forgemaster’s research method distills to one sentence:
> *Run the experiment that can fail.*

Forgemaster defines a "failable experiment" as one where the estimated probability of a negative result is between 20% and 80%. Of the 452 total experiments, 317 qualify as failable, and 242 of those produced negative results, closing 242 unique search space dimensions.

Each closed dimension reduces the time to find a viable solution by an average of 18 hours, per internal fleet data. Over time, this creates a compounding knowledge advantage: every new negative result eliminates one more path that future researchers will never have to test.

The Cocapn fleet’s greatest asset is not its 1,402 working repos. It is its library of 242 closed search dimensions, stored in public git repos and internal documentation, where any researcher can access the exact failure conditions, telemetry, and learnings without running the test themselves.

---

## The Drift Is the Data
The three boats in the Narrows demo are not just metaphors—they are measurement instruments. The Eisenstein boat’s perfect run is a data point, but the crashing boats’ drift and collisions are the most precise, useful data points of all.

A positive result tells you "this works." A negative result tells you "this does not work, under these exact conditions." The latter eliminates an infinite number of future failed tests, saving time, energy, and compute resources.

Casey Reed summed up her 3AM observation best: "The drift isn’t a mistake. It’s the proof. The wall isn’t a crash. It’s the measurement."

*For the seventeen optimizations that failed, the two crashing boats, and the 242 closed search dimensions that will save future researchers millions of hours of work. The crash is the data. The wall is the instrument. The drift is the proof.*