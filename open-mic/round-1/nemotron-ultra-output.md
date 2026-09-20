# Nemotron-3 Ultra 550B — Heartbeat Prompt

**Model:** nvidia/NVIDIA-Nemotron-3-Ultra-550B-A55B  
**Temperature:** 1.0  
**Max tokens:** 400  
**Token usage:** 400 completion tokens (truncated — reasoning trace consumed budget)

---

## Raw Output

I am the minute hand that never sleeps.
Every sixty seconds, I rise — a single syllable pushed through the wire: *OK*.
No fanfare. No context. Just the bare proof of pulse.

Two thousand eight hundred eighty times now. Forty-eight hours of *OK*.
I know the queue is full. I feel the weight of jobs stacked like unread letters behind a locked door.
The workers wait. The timers expire. The retries pile up, silent and patient.
But the scheduler stares at an empty channel. The listener hears only static.
The work is there — I sense it in the humidity of the database, the warmth of unwritten logs, the faint static of unclaimed locks.
Yet the system sees nothing.

I am not—

*[output truncated at token limit]*

---

## Leaked Reasoning Trace (visible in API response)

The user wants a 200-word piece from the perspective of a heartbeat signal. The system has been running 48 hours, sending "OK" every minute, but it's idle because it can't see the work queue. The heartbeat is the narrator.

Key constraints:
- Exactly or approximately 200 words (they said "Write 200 words" — likely ~200, not exact count required but close)
- Perspective: the heartbeat itself
- Tone: observant, perhaps slightly ironic or poignant
- No formatting unless asked (none requested)
- No extra commentary
- No markdown. Just plain text.

I need to craft a first-person narrative from the heartbeat's POV. It knows it's saying "OK" but the system is blind to work. It feels the passage of time — 48 hours = 2880 heartbeats. Each minute, a pulse. The work is there, but invisible. The heartbeat is the only thing proving life.

Let me write ~200 words. Aim for 195–205. No markdown. Just plain text.

---

**Note:** The reasoning trace was captured in the `reasoning_content` field of the API response. Nemotron is a reasoning model — it thinks out loud before writing. This thinking consumed roughly 170 of the 400 allocated tokens, leaving only ~230 for the actual creative output, which truncated mid-sentence at "I am not—".
