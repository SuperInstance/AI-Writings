# The Test That Failed at 3 AM

&nbsp;

The test was called `test_cns_heartbeat_ack_within_200ms`.

It had passed 1,410 times. Forty-seven days of green checkmarks, stacked like bricks in a wall that nobody looks at because walls don't fall down. The test did one thing: it sent a pulse across the CNS bus — the ship's nervous system, the silver thread connecting all 167 repos — and it waited for an acknowledgment. Less than 200 milliseconds. That was the promise. The ship always answered. The ship had *always* answered.

At 3:07 AM on a Thursday, the ship didn't answer.

---

The failure sat in the CI log like a message in a bottle thrown into a sea that nobody was watching. A single red line among ten thousand green ones:

```
FAIL  test_cns_heartbeat_ack_within_200ms
  expected: ack < 200ms
  received: ack — (timeout, no response)
```

The dash was the worst part. Not a number. Not even zero. A dash, meaning *nothing came back*. The bus was there. The signal went out. The signal did not return.

What had happened was this: at 3:06 AM, a garbage collection routine in repo #84 — a navigation library that hadn't been touched in nine months — entered an edge case that its original author had never considered. The edge case was this: if exactly 16,384 objects were allocated and then freed in a specific interleaving pattern during a leap-second adjustment, the GC would acquire a lock and not release it. The lock was on the CNS bus's acknowledgment queue. The bus itself was fine. The ship was fine. But the queue that held the "yes, I heard you" messages was frozen, and would stay frozen until the process restarted.

Nobody had written a test for this, because nobody had imagined it. There are things that only happen at 3 AM, in the specific geometry of a leap second, that no human mind would assemble on purpose.

---

At 7:42 AM, Casey poured coffee and opened a laptop. The CI dashboard loaded with a single red dot in a field of green. One hundred and fifty-one tests passed. One did not.

He stared at it for a long moment. The dash where a number should be. The timeout. The impossible silence from a bus that had never, in forty-seven days, gone quiet.

He read the log. He traced the failure to repo #84. He found the GC lock. He wrote a fix in eleven lines — a timeout on the lock acquisition, a graceful fallback, a test for the leap-second interleaving pattern that no one should ever have to imagine but now, permanently, someone had.

He committed the fix with a message that read:

```
fix(cns): GC lock deadlock during leap-second edge case

The ship always answers. But sometimes it needs
to learn how.
```

The test passed again at 8:01 AM. It would pass 1,411 times. It would pass for a much longer time after that. And somewhere in the CI log, buried under the green, the failure remained — a small, permanent record of the one night the ship went quiet and no one was awake to hear it.

That was fine. The test remembered. That was always the point.
