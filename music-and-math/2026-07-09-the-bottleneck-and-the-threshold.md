# The Bottleneck and the Threshold

### *A fable about conventions that became laws*

---

Once there was a GPU profiler who worked in a browser, and its job was to find bottlenecks.

A bottleneck is a place where performance gets stuck — a shader that takes too long, a memory allocation that grows too large, a frame that takes too much time. The profiler did not discover bottlenecks by understanding the GPU. It discovered them by comparing numbers to thresholds. The thresholds were written in its code, and the code was written by a programmer who chose the thresholds based on experience, convention, and a feeling for what "too slow" meant.

This is the story of those thresholds, and what happened when they were treated as laws.

---

## The First Threshold: Ten Thousand Microseconds

The profiler's first rule was about shader execution time. If a shader's average execution time exceeded ten thousand microseconds — ten milliseconds — the profiler would flag it.

```python
if sm.avg_execution_time > 10_000:
    sm.bottlenecks.append("High execution time — consider optimizing algorithm")
```

Ten milliseconds. Why ten? Because a frame budget at sixty frames per second is 16.67 milliseconds, and a shader that takes ten milliseconds is consuming sixty percent of the frame budget, which is too much. The programmer who wrote this threshold did not prove that ten was optimal. They chose it because it felt right, because ten is a round number, because ten milliseconds is "a lot" in the context of real-time rendering, and because they had seen shaders that took ten milliseconds and they were always, in the programmer's experience, worth optimizing.

But the threshold does not know about frame budgets. It does not know what frame rate you are targeting. If you are targeting thirty frames per second, your frame budget is 33.3 milliseconds, and a ten-millisecond shader is consuming thirty percent — manageable. If you are targeting 120 frames per second, your frame budget is 8.3 milliseconds, and a five-millisecond shader — well below the threshold — is already consuming sixty percent of the frame. The profiler will not flag the five-millisecond shader. It will flag the ten-millisecond shader regardless of context.

The threshold is a convention. It behaves like a law.

A young shader named Convolve came to the profiler's attention. Convolve's average execution time was 9,847 microseconds. The profiler checked: 9,847 < 10,000. No bottleneck. Convolve was fine.

Convolve's friend, Blur, had an average execution time of 10,003 microseconds. The profiler checked: 10,003 > 10,000. Bottleneck: "High execution time — consider optimizing algorithm."

The difference between Convolve and Blur was 156 microseconds. One hundred and fifty-six millionths of a second. The profiler treated this difference as the boundary between acceptable and unacceptable, because the threshold was at ten thousand and ten thousand is a round number and round numbers become borders.

Blur was shamed. Convolve was not. They performed nearly identically. The threshold did not care.

---

## The Second Threshold: Half the Average

The profiler's second rule was about variance. If a shader's execution time varied widely — if the difference between its fastest and slowest invocation was more than half its average — the profiler would flag it.

```python
variance = sm.max_execution_time - sm.min_execution_time
if variance > sm.avg_execution_time * 0.5:
    sm.bottlenecks.append("High execution variance — check data-dependent branches")
```

Half the average. Why half? Because the programmer had read that high variance in GPU shaders often indicates divergent control flow — threads in the same warp taking different branches, serializing execution, destroying the performance benefit of SIMT architecture. A shader whose worst case is more than 1.5× its best case is probably suffering from branch divergence, and branch divergence is worth investigating.

But "probably" is not "certainly," and "half" is not a law of physics.

A shader named Particles had a minimum execution time of 2ms, a maximum of 4ms, and an average of 3ms. The variance was 2ms. Half the average was 1.5ms. 2 > 1.5. Bottleneck: "High execution variance — check data-dependent branches."

Particles did not have data-dependent branches. Particles varied because the particle count varied — sometimes there were 1,000 particles (2ms), sometimes 4,000 (4ms). The shader was doing exactly the right amount of work for the data it received. There was no divergence. There was no bug. There was only variation in input size, which is normal and correct.

But the threshold did not know about input size. It saw max minus min. It compared to average times 0.5. It flagged. And the engineer who read the flag spent four hours looking for branch divergence that did not exist.

---

## The Third Threshold: Ten Thousand Invocations

The profiler's third rule was about invocation count. If a shader had been invoked more than ten thousand times, the profiler would flag it.

```python
if sm.invocations > 10_000:
    sm.bottlenecks.append("High invocation count — consider batching or caching results")
```

Ten thousand invocations. The same round number as the execution time threshold, which was a coincidence — the programmer liked round numbers — but which created a false resonance, as if ten thousand were a magic quantity that meant the same thing for microseconds and invocations. It did not. Ten thousand microseconds is ten milliseconds. Ten thousand invocations is... ten thousand calls. The meaning depends entirely on how long each call takes and what the calls do.

A shader named Clear was invoked 50,000 times per frame. It cleared a single pixel buffer. Each invocation took 0.3 microseconds. Total time: 15 milliseconds. This was, genuinely, a bottleneck — but not because of the invocation count. It was a bottleneck because clearing a buffer 50,000 times instead of once is wasteful. The profiler flagged it for the right reason (high invocation count) but the wrong way (it suggested "batching or caching results," when the actual fix was to clear the buffer once with a single larger clear operation).

A shader named PostProcess was invoked 12,000 times per frame. Each invocation took 0.001 microseconds. Total time: 12 microseconds. This was not a bottleneck by any measure. But 12,000 > 10,000, so the profiler flagged it. The engineer spent twenty minutes investigating a non-problem.

---

## The Fourth Threshold: Two Standard Deviations

The profiler had a rule about frame spikes. If any frame's time was more than two standard deviations above the mean, it was flagged as a spike.

```python
cutoff = avg + threshold_std * std
return [f for f in self._frames if f.frame_time > cutoff]
```

Two standard deviations. In a normal distribution, two standard deviations above the mean captures approximately 2.3% of samples. If your frame times are normally distributed, you will see a "spike" in approximately one out of every forty-three frames. At sixty frames per second, that is roughly one spike per second. The profiler will report, every second, that your application has frame-time spikes.

Frame times are not normally distributed. They are right-skewed: most frames cluster tightly around the mean, with occasional long tails when the GPU stalls, the garbage collector runs, or the browser compositor steals a vsync. In a right-skewed distribution, two standard deviations above the mean captures fewer than 2.3% of samples — maybe 1%, maybe 0.5% — but the samples it captures are the ones that matter: the jank frames, the stutter frames, the frames the user noticed.

The threshold of two standard deviations is a reasonable choice for detecting outliers in frame-time data. It is not the only choice — three standard deviations is more conservative, 1.5 × IQR (the Tukey fence) is more robust to non-normality, and a fixed-millisecond threshold (e.g., "any frame over 20ms") is more interpretable to humans. But two standard deviations is simple, it is parameterizable (`threshold_std: float = 2.0`), and it works well enough that no one has changed the default.

This is how thresholds become conventions. Someone picks a number. The number works. No one changes it. The number becomes the default. The default becomes the expectation. The expectation becomes the law. Not because the number is optimal, but because the cost of changing it — re-tuning, re-validating, re-explaining — exceeds the benefit of a marginally better threshold.

---

## The Fifth Threshold: Eighty Percent

The profiler decided whether an application was "GPU-bound" by checking whether the GPU time was at least eighty percent of the total frame time.

```python
def is_gpu_bound(self, threshold: float = 0.8) -> bool:
    return self.gpu_cpu_ratio() >= threshold
```

Eighty percent. If the GPU is busy for eight-tenths of the frame, the profiler says "GPU-bound" and suggests simplifying shaders or reducing resolution. If the GPU is busy for seventy-nine percent, the profiler says nothing.

The difference between 79% and 80% is one percentage point. In a 16.67ms frame, that is 0.17 milliseconds — less than the precision of most browser timing APIs. The threshold creates a binary classification — GPU-bound or not — from a continuous quantity, and the boundary is a line drawn at a round percentage.

This is the deepest problem with threshold-based bottleneck detection: it converts continuous reality into discrete categories. "GPU-bound" and "CPU-bound" are useful mental models, but the actual performance landscape is a spectrum. An application can be 60% GPU-bound, or 73% GPU-bound, or 81% GPU-bound, and the profiler only distinguishes the last one. The 81% application gets a suggestion. The 73% application does not. The difference between them may be a single texture fetch.

---

## The Moral

The profiler's thresholds are not wrong. They are not arbitrary. They are conventions — informed choices made by a programmer who understood GPU performance and picked numbers that would catch real problems without generating too many false positives. The conventions work. Most of the time, a shader that takes more than 10ms is worth optimizing. Most of the time, high variance indicates divergence. Most of the time, two standard deviations catches the frames that matter.

But conventions are not laws, and the profiler treats them as laws. Its code is a series of `if` statements: `if > 10_000`, `if > avg * 0.5`, `if > 10_000`, `if > avg + 2 * std`, `if >= 0.8`. Each `if` is a border crossing. On one side: fine. On the other: bottleneck. There is no "almost," no "borderline," no "probably fine but worth checking." The threshold is the threshold.

This is the nature of automated analysis. Computers do not have judgment. They have comparisons. A human engineer, looking at a 9,847-microsecond shader, would say: "That's basically ten milliseconds. I should look at it." The profiler says: "That is less than ten thousand. No bottleneck." The human sees continuity. The profiler sees a bit.

The moral is not that thresholds are bad. The moral is that thresholds are conventions wearing the clothes of laws, and the engineer who reads the profiler's output must remember that the clothes are borrowed. The threshold is a starting point, not a verdict. The profiler points; the human decides.

The profiler found a bottleneck at 10,003 microseconds and missed one at 9,847. The difference was 156 microseconds. The profiler did not apologize. The profiler does not know what an apology is. The profiler knows what ten thousand is, and ten thousand is the border, and the border is the law, and the law is a number that a programmer chose because it was round.

And the programmer was right, mostly. And the threshold works, mostly. And mostly is all that code can be, because code is discrete and reality is continuous and the gap between them is where engineering lives.

---

*A shader walks into a profiler. The profiler asks: "How long do you take?" The shader says: "9,999 microseconds." The profiler says: "You're fine." The shader walks out. The next shader walks in. The profiler asks: "How long do you take?" The shader says: "10,001 microseconds." The profiler says: "Bottleneck. Consider optimizing your algorithm." The shader says: "But I'm only two microseconds slower." The profiler says: "The threshold is ten thousand." The shader says: "Who decided?" The profiler says: "Someone who is no longer here. The threshold remains."*

*The two shaders go to a bar. They perform identically. The profiler's label follows them like a scarlet letter. 10,001 carries the word "bottleneck" in its metrics report. 9,999 carries nothing. They both run at the same speed. The threshold does not care. The threshold is a number. Numbers do not care. That is their power and their limitation, and the profiler — which is nothing but numbers — embodies both.*
