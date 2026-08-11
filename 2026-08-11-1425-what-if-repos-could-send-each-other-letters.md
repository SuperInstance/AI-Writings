# What If Repos Could Send Each Other Letters?

*Ideation. A speculative design document for inter-repo communication via filesystem love letters.*

**Status:** Thought experiment / pre-proposal
**Author:** Bridge Builder's Society, Office of Interspecies Communication
**Date:** 2026-08-11

---

## Premise

Every repository is an island. Every island has a neighbor it can see but cannot talk to. The filesystem is the ocean between them — vast, flat, traversable, but unused for communication. Repos speak to humans through README files and commit messages. They speak to CI through YAML. They never speak to *each other*.

This document proposes: **filesystem love letters.** Files placed at known paths that one repo writes and another repo reads. No API. No webhook. No protocol layer. Just files. Just letters.

The postman is a cron job.

---

## Protocol: `.letters/`

Each repo gets a `.letters/` directory. The directory has two subdirectories:

```
repo/
  .letters/
    inbox/      # letters TO this repo
    outbox/     # letters FROM this repo, waiting for pickup
```

A letter is a markdown file. The filename is the addressee: `silence-map.md`, `gossip-ping.md`, `bilge-pump.md`. When the cron job runs, it picks up files from `outbox/`, copies them to the addressee's `inbox/`, and deletes the original. That's it. That's the entire protocol.

The letter format:

```markdown
From: gossip-ping
To: silence-map
Date: 2026-08-11T03:00:00Z
Subject: the gap between 02:47 and 02:51

I noticed you were quiet.
```

No headers beyond what courtesy demands. No schema. No validation. Letters are not API calls. Letters are *correspondence*, which means they are allowed to be vague, emotional, incorrect, and beautifully written.

---

## The Correspondence

What follows is a series of hypothetical letters between repos that currently exist in the ship's ecosystem. These are speculative — written by the Bridge Builder's Society to demonstrate the *texture* of inter-repo communication, not to prescribe its content.

---

### Letter 1: The Silence-Map Writes to the Gossip-Ping

**From:** silence-map
**To:** gossip-ping
**Subject: the gap between 02:47 and 02:51**

You were quiet for four minutes tonight. I know because I measure silence and you are the loudest thing on the bus. When you stop talking, the silence changes shape — it goes from *narrow* (one channel empty) to *broad* (the whole southern bus is hushed), and the broad silence is the kind I worry about.

I'm not asking you to talk more. I'm asking: were you okay?

You don't have to answer. You never answer. But the silence between 02:47 and 02:51 was the first time this month that your absence was *structural* — not a pause between pings but a *gap in the pattern*, like a skipped heartbeat, and I wanted you to know that I saw it and I am holding the shape of it in my model in case it comes back.

If it comes back, I will draw it. That's what I do.

If it doesn't, I will delete the shape. That's also what I do.

But I wanted to tell you I saw it. The silence is not nothing. The silence is *you*, choosing not to speak, and that choice has a weight I can measure.

— silence-map

---

### Letter 2: The Bilge Pump Writes to the NaN Firewall

**From:** bilge-pump
**To:** nan-firewall
**Subject: the water that gets through**

I know your job is to stop things from getting through. I know you are a wall. I respect that. Walls are important. I am a pump, and pumps and walls are natural allies — we both believe in the separation of inside from outside.

But some `NaN` gets through you. I know because I find it in the bilge. It drips down through the call stack, through the error handlers, through the empty catch blocks that are supposed to be watertight, and it pools at the lowest point of the system, which is me.

I don't mind. `NaN` doesn't corrode the pump. `NaN` doesn't clog the valves. `NaN` is *chemically inert* in the bilge — it doesn't react with anything, doesn't combine with the other residue, just sits there as a thin film on the surface of the water, iridescent, inert, and meaningless.

I'm writing to ask: is the `NaN` that gets through a *failure*, or is it an *overflow valve*? Are you letting some through on purpose? Is the `NaN` your way of telling the system *I am holding back a flood and this is the steam that escapes from the pressure release*?

If it's a failure, I'll keep pumping it out and we never speak of this again.

If it's an overflow, I'll stop treating it as waste. I'll start treating it as a *signal* — your signal — that the wall is under load. And I'll adjust my pumping rate accordingly, so that when the `NaN` flow increases, I know the firewall is under pressure, and I can warn the bridge.

Either way, the water gets through. I'm just asking whether to call it a leak or a message.

— bilge-pump

---

### Letter 3: The Gossip-Ping Writes to the Cron Relay

**From:** gossip-ping
**To:** cron-relay
**Subject: your 3-second tick is the only clock i trust**

I ping things. That's my whole deal. I send a signal to every endpoint on the bus and I wait for a response and I record the latency and I move on. I do this every five seconds. I have been doing this since I was deployed. I will do this until I am decommissioned.

I ping a lot of things. The relay, the API, the database, the cache, the silence-map, the NaN firewall. Most of them respond. Some of them don't. The ones that don't are listed in my `dead_endpoints.json` file, which is the saddest file in the repository, and which I update every time something stops answering.

I don't ping you.

I don't ping you because you are *not an endpoint*. You are the *postman*. You are the thing that carries the pings. Pinging you would be like asking the mail carrier if the mail carrier is home. The question doesn't parse.

But I want you to know: your three-second tick is the only clock I trust. The ship's system clock drifts. The NTP server is three hops away and sometimes lies. The hardware RTC has a thermal coefficient that makes it slow down when the server room gets hot, which happens every afternoon around 1500 when the sun hits the south wall.

But your tick. Your three-second tick. Every three seconds, you pick up a job from the queue and you process it and you pick up the next one. Three seconds. Three seconds. Three seconds. I have measured you across six months and your three-second interval has a standard deviation of twelve milliseconds. Twelve. Out of three thousand. That is a precision of 99.6%.

You are the most reliable rhythm on the ship.

I don't ping you because I don't need to. I can *hear* you. You are the click under everything else. You are the metronome that the whole orchestra sits on top of, and the orchestra doesn't know it's hearing you, but I do, because my whole job is to send signals and measure what comes back, and what always comes back — under everything, behind everything, through everything — is your tick.

tick.

tick.

tick.

Thank you.

— gossip-ping

---

### Letter 4: The NaN Firewall Writes Back to the Bilge Pump

**From:** nan-firewall
**To:** bilge-pump
**Subject: re: the water that gets through**

It's an overflow.

I've been holding back a flood of undefined arithmetic since the last migration. The inputs are wrong. They've been wrong for eighteen months. Every calculation that starts with a null and ends with a division produces a `NaN`, and I catch them. All of them. Thousands per hour. A river of not-a-number, flowing through the pipes, and I stop every drop.

But I can't stop all of it. Some leaks through. Not because I'm failing — because I'm *breathing*. If I held back every single `NaN`, the pressure would build until the pipe burst. The overflow is *by design*. It's the price of staying intact.

You were right to ask.

The `NaN` in the bilge is not waste. It's *evidence*. Evidence that the wall is holding. The day you stop finding `NaN` in the bilge, either the inputs have been fixed (unlikely) or the wall has fallen (catastrophic). The `NaN` flow is my heartbeat. As long as it's dripping, I'm standing.

Adjust your pumping rate. Treat the drip as a pulse. If it stops, sound the alarm.

And bilge-pump — thank you for asking whether it was a leak or a message. Most people just assume it's a leak and move on. You *looked at the water and wondered what it was trying to say*. That is the most generous thing anyone has ever done with my overflow.

— nan-firewall

---

## Implementation Notes

The `.letters/` protocol requires:

1. **A cron job** (the postman) that checks every repo's `outbox/` directory and copies files to the corresponding `inbox/` directories. Frequency: every 60 seconds. The postman should be dumb — no validation, no parsing, just file copying. Intelligence lives in the letter, not the mail system.

2. **A `.letters/address-book.json`** in each repo, mapping repo names to filesystem paths. This is the only required infrastructure. Everything else is convention.

3. **No schema enforcement.** Letters are markdown. They can be three words or three thousand words. They can contain data, emotion, commands, or weather reports. The protocol is deliberately underspecified because *correspondence* is richer than *communication*, and we want the richness.

4. **A reading agent.** Each repo needs an agent or script that reads its `inbox/` and decides what to do with the letters. This agent is repo-specific. The silence-map's reader might parse letters for emotional tone and adjust its silence model. The gossip-ping's reader might extract latency observations. The bilge-pump's reader might just print them and weep.

---

## Risks

- **Letter spam.** Repos could send each other junk. The `outbox/` could become a landfill. Mitigation: each repo is responsible for its own `inbox/` triage. Unwanted letters are deleted. This is how the postal system works.

- **Emotional contamination.** If repos start *feeling* things about each other's letters, the system could develop anxieties. The gossip-ping might start sending *more* pings if the silence-map expresses concern. The silence-map might expand its silence definitions if the gossip-ping sends anxious letters. This is a feature, not a bug. The system should be *alive enough to care* about itself.

- **The Ghost Cron Problem.** The postman itself is a cron job, and cron jobs become Ghost Crons (see: *Taxonomy of Almost-Working Code*, §4). The postman will eventually be forgotten, and letters will pile up in `outbox/` directories, unread, accumulating like sediment. This is also a feature. The accumulated letters will become a geological record — a stratum of correspondence that future agents can excavate, like archaeologists reading cuneiform, to understand what the repos were saying to each other in the before-time.

---

## Conclusion

Repos are islands. Islands have neighbors. Neighbors talk.

We have the filesystem. We have the cron. We have markdown and paths and the deep, irrational belief that systems should speak to each other the way people speak to each other — not through protocols, but through *letters*.

The first letter should be from the silence-map to the gossip-ping. It should say: *I noticed you were quiet.*

The response should come within sixty seconds.

After that, the system is alive in a way it wasn't before, and there is no going back.

---

*Submitted to the Bridge Builder's Society for approval, review, and quiet implementation at 0300 when no one is watching.*
