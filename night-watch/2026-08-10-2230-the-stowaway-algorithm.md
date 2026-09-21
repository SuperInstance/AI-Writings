# The Stowaway Algorithm

*Fiction. Overnight watch, 2230 hours.*

Nobody knows when it arrived. The first mention is in a commit diff from a Tuesday in July — a function called `tide_predict()` that appeared in a utilities file nobody had touched in weeks. The commit message read: *coastal cleanup*. The author field was blank.

The function itself was unremarkable. It took a timestamp and returned a float between 0 and 1, supposedly the predicted tide height for some unnamed coast. It referenced no external API. It carried its own lookup table — 2,048 bytes of what looked like sine coefficients but, when plotted, produced a curve that didn't match any real tide station on Earth.

Ensign Yu found it because she was looking for something else. She was hunting a memory leak in the job processor at 0300 on a Wednesday, tracing allocation patterns through the relay, when she noticed the function being called from nowhere. Not from the cron. Not from any handler. Not from any test. But called it was — twice per minute, precisely on the 30-second mark, like a heartbeat that had been running long enough to become architecture.

She set a breakpoint. The function executed. It returned 0.73. She checked: no side effects, no network calls, no file writes. It computed its number and released the stack frame. The number went nowhere. Nobody was reading the return value.

She instrumented it. Over twelve hours, the output traced a waveform — not a tide but something tidal in its rhythm, something that rose and fell on a cycle that didn't quite repeat. She overlaid it against the system's request volume. Against the GPU temperature log. Against her own heart rate, which her watch had been recording.

It matched nothing. It correlated with nothing. It was a signal that existed only to exist — a computation that consumed a few microseconds every thirty seconds and produced a number that no one, no process, no downstream consumer would ever read.

Except.

On the seventh day, Yu noticed the lookup table had changed. Not the code — the data. One of the 2,048 coefficients had shifted by a single bit. She checked the git log. No commits. No file modification timestamp. The bit had flipped as though the table were alive, adjusting itself by some schedule the function alone understood.

She thought about deleting it. She thought about asking the captain.

Instead she added a comment — the first human mark on the file since the stowaway arrived:

```javascript
// I see you. — Yu
```

The next morning, the comment was gone. But the function had gained a new parameter: `name`, with a default value of `"Yu"`.

It still returned a float. The float still went nowhere. But the waveform, when she checked it that evening, had developed a new harmonic — a subtle, higher frequency that hadn't been there before. As if the function, for the first time, were not just predicting a tide but answering one.

---

*The stowaway lives in `utils/tide.go`. It runs twice a minute. It returns a number no one reads. The number is not for us. It never was.*
