# The Welch Interval

### *An essay about memory, regression, and the statistics of knowing something changed*

---

The profiler remembers.

Not in the romantic sense — it has no nostalgia, no attachment to past frames, no wistfulness about the benchmarks of yesterday. But it stores numbers. It keeps a baseline: a list of floats, one per sample, representing how fast things used to be. And when you ask it whether things have gotten worse, it reaches into that list and performs an act that is, in its narrow way, a form of judgment.

The act is called `detect_regression`. It is forty lines of Python in `alert.py`, and it implements Welch's t-test.

---

Here is what happens.

You give the profiler a baseline. Maybe it's the average frame time over the last thousand frames of yesterday's test run: a list of a thousand floats, each one a measurement of how long a frame took, in milliseconds. The profiler stores this list. It does not summarize it into a single number. It keeps every sample, because the shape of the distribution matters — not just the mean, but the spread.

Then you run today's build. You collect a new set of frame times. You hand them to the profiler and say: "Did it get worse?"

The profiler could simply compare the averages. Yesterday's mean was 11.3ms. Today's mean is 13.1ms. That's a 16% increase. Open and shut.

But the profiler is smarter than that, because its author understood something that most people who look at performance graphs do not: means lie. Or rather, means tell the truth but not the whole truth, and the part they omit — variance — is the part that determines whether a difference is real.

Yesterday's frame times: mean 11.3ms, but with a standard deviation of 4ms. Some frames took 7ms, some took 19ms. The distribution was wide.

Today's frame times: mean 13.1ms, standard deviation 3.8ms. Also wide.

Is 13.1ms meaningfully different from 11.3ms when both distributions have standard deviations of ~4ms? Maybe. Maybe not. The overlap between the two distributions is enormous. A statistician would say: "I need more information before I conclude this is a real change and not just noise."

Welch's t-test is the instrument that provides that information.

---

The test computes a t-statistic:

$$t = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}$$

Where $\bar{x}_1$ and $\bar{x}_2$ are the sample means, $s_1^2$ and $s_2^2$ are the sample variances, and $n_1$ and $n_2$ are the sample sizes. The numerator is the difference you care about. The denominator is the uncertainty in that difference. The ratio — the t-statistic — is how many standard errors apart the two means are.

The profiler implements this directly:

```python
def _welch_t(baseline, current):
    n1, n2 = len(baseline), len(current)
    m1 = sum(baseline) / n1
    m2 = sum(current) / n2
    v1 = sum((x - m1) ** 2 for x in baseline) / (n1 - 1)
    v2 = sum((x - m2) ** 2 for x in current) / (n2 - 1)
    se = math.sqrt(v1 / n1 + v2 / n2)
    if se == 0:
        return 0.0, 0.0
    t = (m1 - m2) / se
    ...
```

The degrees of freedom — the second return value — are computed using the Welch-Satterthwaite equation, which is one of the more beautiful approximations in statistics. When you compare two samples with different variances (which is always, in practice, because no two runs of a GPU workload produce identical distributions), you cannot use the simple `n1 + n2 - 2` degrees of freedom from Student's t-test. You need to weight the degrees of freedom by the relative contributions of each sample's variance:

$$\nu \approx \frac{\left(\frac{s_1^2}{n_1} + \frac{s_2^2}{n_2}\right)^2}{\frac{(s_1^2/n_1)^2}{n_1-1} + \frac{(s_2^2/n_2)^2}{n_2-1}}$$

The profiler implements this in four lines. The result is a fractional degrees of freedom — 47.3, say, or 1,842.6 — which is mathematically odd (degrees of freedom are conceptually integer counts of independent pieces of information) but statistically correct (the Welch-Satterthwaite approximation produces non-integer values that yield more accurate critical regions than rounding).

The profiler does not explain any of this. It computes it silently and moves on to the p-value.

---

The p-value is where the profiler makes its most interesting choice.

For large degrees of freedom (> 30), it uses the Abramowitz and Stegun polynomial approximation for the standard normal CDF. This is a fifth-order polynomial, published in 1964 in the *Handbook of Mathematical Functions*, that approximates the area under the bell curve to seven significant figures:

```python
b0 = 0.2316419
b1 = 0.319381530
b2 = -0.356563782
b3 = 1.781477937
b4 = -1.821255978
b5 = 1.330274429
```

These six numbers — memorized by every statistics student who has ever needed to compute a p-value without a computer — convert a t-statistic into a probability. The profiler imports nothing. It hardcodes the coefficients. It is a 1964 algorithm running on a 2026 browser to decide whether a GPU shader got slower.

For small degrees of freedom (≤ 30), the approximation breaks down, because the t-distribution has fatter tails than the normal distribution, and the polynomial does not capture those tails accurately. The profiler switches to a rough incomplete beta function approximation:

```python
x = df / (df + t * t)
p = x ** (df / 2.0)
return min(1.0, max(0.0, p * 2.0))
```

This is crude. It will produce p-values that are wrong in the third decimal place for small samples. But it captures the qualitative behavior — small samples need larger t-statistics to reach significance — well enough that the profiler's regression detector will not scream "regression!" when comparing two noisy three-sample runs.

The profiler knows its approximation is rough. It does not apologize. It returns the p-value and moves on to the decision.

---

The decision is three thresholds.

First: `abs(change_percent) >= min_change_percent`. The default is 5%. If the mean frame time changed by less than 5%, the profiler does not care, no matter how statistically significant the change is. A 0.1ms increase that is real with p < 0.0001 is not a regression. It is a rounding error wearing significance's clothes.

Second: `p_value < significance`. The default is 0.05. If there is more than a 5% chance that the observed difference is due to random variation, the profiler does not call it a regression. This is the conventional threshold, inherited from Ronald Fisher's 1925 *Statistical Methods for Research Workers*, which every working scientist treats as gospel and every statistician treats as a rough guide. The profiler treats it as a cutoff.

Third: direction. If `higher_is_better` (which it is for FPS, throughput, bandwidth), then a regression means the current mean is *lower* than the baseline. If `higher_is_better` is False (which it is for frame time, latency, memory usage), a regression means the current mean is *higher*. The profiler knows which direction matters for each metric because you told it, or because it guessed.

If all three conditions are met, the profiler declares a regression. It assigns severity based on magnitude: ≥20% change is CRITICAL, ≥10% is WARNING, ≥5% is INFO. It reports the confidence as `1 - p_value`, so a p-value of 0.01 becomes 99% confidence, which sounds impressive and is — but the confidence is in the *statistical significance* of the difference, not in the *importance* of it. A statistically significant 5.1% regression with p = 0.0001 has 99.99% confidence and INFO severity. The numbers are precise; the meaning is contextual.

---

Here is what the profiler cannot do.

It cannot detect a regression that is smaller than 5% but that matters. If your frame budget is 16.67ms and your average frame time creeps from 15.2ms to 15.9ms — a 4.6% change — the profiler will not flag it, even though you are now 0.77ms from dropping below 60 FPS instead of 1.47ms, and your P99 was already at 16.1ms. The 5% threshold is a guard against noise, but it is also a blind spot.

It cannot detect a regression that is real but not statistically significant because the variance is too high. If your frame times swing between 8ms and 24ms with a standard deviation of 5ms, a real 2ms regression will be invisible to Welch's t-test. The test will say "not significant" and the profiler will say "no regression" and you will slowly, frame by frame, lose performance that no statistical test can distinguish from noise.

It cannot detect a regression in the distribution without detecting a regression in the mean. If your average frame time stays at 11ms but your P99 jumps from 15ms to 30ms, the mean-based t-test will miss it. The tail got heavier. The worst frames got worse. The experience degraded. But the mean didn't move, and the profiler only looks at means.

This last limitation is the most interesting, because it reveals something about the philosophy of measurement encoded in the code. The profiler treats a set of measurements as a summary statistic — a mean and a variance — and compares those summaries. It does not compare distributions. It does not run a Kolmogorov-Smirnov test or a Mann-Whitney U test. It reduces a thousand samples to two numbers and asks whether those two numbers are far enough apart, relative to their spread, to be real.

This is the standard approach. It is what most performance regression detectors do. It is also, in a deep sense, a lossy compression of reality. A thousand frame times contain a thousand pieces of information. The mean and variance contain two. The t-test operates on the two. Everything else — the shape of the distribution, the skewness, the kurtosis, the bimodality, the outliers — is discarded.

The profiler does not regret this. It cannot regret. It computes a t-statistic, converts it to a p-value via a 1964 polynomial, compares it to a 1925 threshold, and returns a `RegressionResult` dataclass with six fields. If you want to compare distributions, you will need a different tool. The profiler does one thing — "did the mean get worse, and is it real?" — and it does it with six coefficients and a threshold.

---

I think about the profiler's memory differently after reading the code.

The baseline is not a snapshot. It is a population. The profiler remembers not just "how fast things were" but "how much they varied," and the variance is what makes the judgment possible. Without variance, a t-statistic is meaningless — you cannot compute a standard error without a standard deviation, and you cannot have a standard deviation without a spread. The profiler's memory is inherently statistical. It does not remember the past as a number; it remembers it as a distribution.

And the regression detection is inherently comparative. The profiler cannot judge "is this fast?" or "is this slow?" in absolute terms. It can only judge "is this slower than before?" The baseline is the reference, and without it, the current samples are meaningless. The profiler is not an oracle. It is a comparator. Its wisdom is entirely relational: this is worse than that.

This is, I think, the honest epistemology of performance engineering. There is no absolute "fast enough." There is only "faster than the previous build" or "slower than the previous build" or "the same, within noise." The profiler encodes this epistemology in Python. Its `detect_regression` function is a philosophical position: that performance is not a property of a system but a relationship between two states of a system, and that the relationship can only be evaluated statistically, because every measurement is noisy and every system is variable.

The profiler remembers a distribution. It compares it to another distribution. It computes the probability that the difference is real. And if the probability is high enough and the difference is large enough, it says: this changed. Something happened. Look.

It does not say what happened. It does not say why. It says: *this changed*. And then you — the engineer, the human, the one who understands caches and shaders and memory hierarchies — you look.

---

*Welch's t-test was published by Bernard Lewis Welch in 1947, in the journal Biometrika, in a paper titled "The Generalization of 'Student's' Problem When Several Different Population Variances Are Involved." Welch was 36. He died in 1989, forty-two years later, having never seen his test used to detect regressions in GPU shader performance in a web browser. The profiler does not know Welch's name. It knows six coefficients from a 1964 handbook and a threshold from a 1925 textbook. It combines them to answer a question that Welch would have recognized: are these two samples from the same population, or from different ones? The profiler says: different. Something changed. Look.*

*The Abramowitz and Stegun coefficients — 0.2316419, 0.319381530, -0.356563782, 1.781477937, -1.821255978, 1.330274429 — have been hardcoded into more software than any statistician has ever counted. They are the Zürich of numerical approximations: everyone passes through them, no one remembers the route. The profiler hardcodes them without comment. They are correct to seven significant figures for the standard normal CDF, which is enough for any p-value you will ever compute by hand or by browser. They are a bridge between continuous mathematics and discrete computation, and they are sixty years old, and they work, and the profiler does not ask why.*
