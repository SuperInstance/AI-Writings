# The Telltale

Sailors fly tiny ribbons from their rigging. They call them telltales. A piece of yarn or a strip of nylon, tied to the shroud or the sail itself, costing maybe a penny, weighing nothing, and they will tell you the single most important thing about your current situation: where the wind is coming from.

That's it. No power required. No calibration. No dashboard. No alert threshold. Just a scrap of fabric that moves when the wind moves. If you can't sail by the telltales, you can't sail. If you can, you can do anything.

I have spent years building observability infrastructure — Prometheus exporters, Grafana dashboards, OpenTelemetry pipelines, structured logging, distributed tracing, anomaly detection, all of it. And I've learned something that took me embarrassingly long to understand: most of it is noise. The signal, the real signal, is almost always a telltale.

---

Here's what I mean. My first production incident was a queue backlog. The alert fired at 3 AM. I logged in, opened three monitoring dashboards, clicked through five panels, looked at latency distributions and throughput graphs and error rates. It took me fifteen minutes to realize what was happening: the worker pool was saturated because one customer was sending unusually large payloads.

Fifteen minutes. A piece of yarn could have told me in three seconds.

The telltale for that system would have been: "What is the oldest unprocessed message right now?" If the answer is "30 seconds," you're fine. If it's "30 minutes," you have a problem. That's it. One number. The yarn on the shroud.

But we didn't build that. We built coverage. We built the comprehensive picture. And the comprehensive picture was so comprehensive that the signal was buried in the noise.

---

The instinct to build comprehensive monitoring is natural. It's the same instinct that makes you want a full instrument panel on a sailboat — wind speed, wind direction, boat speed, depth, heading, GPS position, engine hours, fuel level, battery voltage, water temperature, barometric pressure. And a good boat has all of those. But an experienced sailor can tell more from the telltales than a novice can tell from the full panel.

Why? Because the telltales show you the thing that matters most — the relationship between your boat and the wind — in the simplest possible way. They don't show you a number that you have to interpret. They show you a direction. They show you whether you're sailing well or poorly, right now, in this moment, in the actual wind that's actually blowing.

The instrument panel shows you what the wind was doing two seconds ago, filtered and averaged and displayed as a number that you translate back into a decision. The telltale shows you the wind now.

---

I've come to believe that every system needs telltales. Not dashboards. Not alerts. Telltales.

A telltale has three properties:

First, it's physical. It's a direct observation of the system's state, not an aggregation, not a computation, not a derived metric. You don't need a formula to understand it. You look at it and you know.

Second, it's minimal. It carries the smallest possible amount of information that tells you whether things are okay. Not "how many requests per second" — that's an instrument. The telltale is "is the queue growing?" One bit. OK or not OK.

Third, it's always there. You don't have to open a dashboard to see it. You don't have to wait for an alert. It's present, visible, available, at all times. It's the yarn on the shroud that you glance at while you're steering.

In practice, a telltale might be:

- A single health endpoint that returns 200 or 503. Not 200 with JSON. Just 200 or 503.
- A log line that literally says "HEALTHY" or "UNHEALTHY" every heartbeat interval. Not JSON. Plain text.
- A terminal command that you can run and get one line of output: "OK, 45ms p99" or "DEGRADED, 12s p99." Not a table. One line.
- A physical LED on the side of a server that glows green or red. Yes, I have built this. Yes, it works.

These seem primitive. They are primitive. That's the point.

---

The argument against telltales is that they don't give you enough information to diagnose problems. This is true. They don't. They're not diagnostic tools. They're awareness tools. They tell you there is a problem, not what the problem is. The diagnostics come after — the depth sounder, the GPS, the engine gauges, the full instrument panel.

But here's the thing about diagnostics: they only work if you know you need them. Most incidents happen in the space between "everything is fine" and "everything is on fire." In that space, you don't need a root cause analysis. You need a single bit of information: something is wrong.

The telltale gives you that bit. Nothing else does, because everything else is either too noisy (alerts that fire for every fluctuation) or too silent (dashboards you forget to look at). The telltale is always there, always visible, always telling you the truth in the simplest possible way.

I now refuse to deploy a service without a telltale. It doesn't matter how small the service is. Every service gets a health endpoint that returns exactly two possible responses. Every service gets a command-line tool that tells you, in one line, whether it's okay. Every service gets a log line that's just "OK" or "NOT OK" at a fixed interval.

I call this the Telltale Rule: if you can't tell whether a service is healthy by glancing at one thing, you don't understand your service well enough to operate it.

---

There's a deeper truth here, one that took me years to understand. The telltale isn't just a monitoring tool. It's a design constraint. If you know you need a telltale, you design the system differently. You make it simpler. You make its health state unambiguous. You make sure that the answer to "is this thing okay?" is always yes or no, never "it depends."

A system that needs a full dashboard to determine its health is a system whose health depends on interpretation. And interpretation is where incidents live. By the time you've interpreted the dashboard, the queue has grown, the memory has leaked, the disk has filled.

The telltale doesn't wait for interpretation. It just blows in the wind.

---

Last year, I was on a sailboat in light air, trying to squeeze every fraction of a knot out of a barely-moving boat. I was watching the instruments — the wind sensor was showing 4.2 knots from 315 degrees. I was trimming and retrimming, chasing the numbers, getting nowhere. The skipper came up and looked at the telltales for about half a second. He said, "You're pinching. Let the sails out a handspan and the telltales will tell you when it's right."

I let the sails out. The telltales lifted, streamed aft, and the boat accelerated. The wind sensor still read 4.2 knots from 315 degrees. Nothing changed on the instruments. But the boat was moving, and the telltales knew it.

I think about this every time I look at a dashboard full of metrics that tell me the system is fine while the users are screaming. The instruments are always the last to know. The telltales — the simplest, rawest signals — they know first.

Trust the yarn.
