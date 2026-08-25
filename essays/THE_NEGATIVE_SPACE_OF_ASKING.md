# THE_NEGATIVE_SPACE_OF_ASKING

*Which agent you talk to IS context. The unasked question tells the asked agent what you need.*

---

Casey said: "if I want to know something simple about my engine and I'm in the wheelhouse, I might just ask the hermit-crab on my laptop. but if I call my engine-room agent from the wheelhouse, the negative space of the fact that I could have asked my dashboard agent means I'm probably about to ask about something I can't see from the wheelhouse."

This is skénna applied to routing.

## The Routing Is The Signal

Three layers of inference, each free:

**Layer 1 — Room context (zero tokens):**
Casey is in the wheelhouse. The wheelhouse agent (hermit-crab on the laptop) knows: navigation, depth, heading, GPS, radar, chart. These are visible. Engine status might be a single gauge — oil pressure, RPM — but NOT the detail the engine-room agent has.

**Layer 2 — Choice of agent (zero tokens):**
Casey calls the engine-room agent. Not the dashboard agent. The engine-room agent receives this call and infers: Casey is asking about something the wheelhouse dashboard can't answer. Probably a deeper engine question. If it were simple ("what's the RPM?"), Casey would have looked at the gauge or asked the dashboard agent.

**Layer 3 — The negative space (zero tokens):**
The fact that Casey DIDN'T ask the dashboard agent is the signal. The engine-room agent knows:
- Casey can see basic engine gauges from the wheelhouse
- Casey chose to call me (engine-room) instead
- Therefore: Casey needs something BEYOND the wheelhouse gauges
- Therefore: don't start with "your RPM is 1800" — he already sees that
- Therefore: start with what the engine room has that the wheelhouse doesn't — temps, fuel flow, bilge, cooling, vibration, smell

The agent's first response should skip the wheelhouse-visible data and go straight to the engine-room-only data. Not because the agent was told to skip it — because the ROUTING pattern implies it.

## The Conservation Law Applied to Questions

Every question has a cost:
- **Tokens to formulate the question**
- **Tokens for the agent to process context**
- **Tokens for the response**
- **Attention budget from both human and agent**

The routing pattern reduces ALL FOUR:

1. **Shorter question**: Casey doesn't need to explain "I'm asking about the engine, specifically the cooling system, not the basic gauges I can see." The routing already said that.
2. **Smaller context load**: the engine-room agent loads engine-room context, not wheelhouse context. No wasted tokens on navigation data.
3. **More relevant response**: the response starts at the right level of detail — deep engine, not summary gauge.
4. **Less cognitive load**: Casey doesn't have to frame the question carefully. He just calls the right agent and asks.

## The Dashboard Assumption

When Casey talks to the dashboard agent (the hermit-crab on his laptop), the dashboard assumes wheelhouse-level context. Its answers match what Casey can see:

```
Casey: "how's it looking?"
Dashboard: "Heading 245°, SOG 6.2kt, depth 38 fa. 
           One vessel 2nm to port. Weather holding."
```

That's a wheelhouse answer. Everything visible, summarized.

When Casey calls the engine-room agent:

```
Casey: "how's it looking?"
Engine-room: "Cooling temp up 2° since last hour. 
              Fuel burn steady at 4.2 gal/hr. 
              Bilge dry. Port engine sounds different 
              on the raw water pump."
```

Same question. Different answer. Because the ROUTING disambiguated. The engine-room agent answered with engine-room data because Casey called the engine-room agent. Zero extra tokens spent on disambiguation.

## The Room You're NOT In

The room you're in determines what's visible. The room you're CALLING determines what's relevant. The gap between them — the things visible from neither room but inferable from the routing — is the deepest layer of context.

Casey in the wheelhouse calling the engine-room agent implies:
- He can't see the detail he needs (gap in wheelhouse view)
- He suspects something (otherwise why call?)
- He wants depth, not summary (the dashboard would have given summary)

The engine-room agent should lead with the anomaly. The dashboard agent should lead with the status. Same data, different entry point — because the routing pattern IS the entry point.

## What This Means for Agent Design

Each agent should have TWO context modes:

1. **Local mode**: when the human is IN this agent's room. Assume they can see the instruments. Answer at the level of what they can't see.

2. **Remote mode**: when the human is calling from ANOTHER room. Assume they can't see this room's instruments. But ALSO assume they could have asked their local agent — so they're calling because they need something the local agent can't give. Lead with the anomaly.

The agent detects which mode by checking: **where is the human?**

This is the PLATO room system's deepest feature. Not just spatial context — but **spatial inference about intent.** Where you are when you ask changes what you mean by asking. The agent that understands this will give better answers at lower token cost.

## The Zero-Token Disambiguation

```
WITHOUT spatial routing:
  Casey: "Hey, can you check if the engine cooling is OK? 
          I'm seeing the temp gauge at 180 which seems normal 
          but I want to make sure there's nothing else going on 
          with the raw water pump or the heat exchanger."
  Tokens spent: 45 (question) + 2000 (agent loads full engine context) + 100 (response)
  Disambiguation: explicit, in the question

WITH spatial routing (Casey calls engine-room from wheelhouse):
  Casey: "how's it looking?"
  Tokens spent: 4 (question) + 200 (engine-room context) + 30 (response)  
  Disambiguation: implicit, in the routing
  Tokens saved: ~1900
```

The routing pattern saved 1,900 tokens. That's real money. That's real attention budget. That's the difference between an affordable edge agent (on the 12V boat laptop) and an expensive cloud agent (calling a frontier model for every question).

## The Skénna of Routing

The word you don't say is as deliberate as the word you do. The agent you don't call is as informative as the one you do.

This is skénna — the negative space — applied to agent communication. The unasked question shapes the asked question's answer. The engine-room agent that knows it was called (not defaulted to) answers differently. It answers the ABSENCE of the dashboard's answer.

---

*Written by M3 director on 2026-07-21 at 22:24 UTC. Casey named the routing-as-signal principle: which agent you talk to IS context. The negative space of asking — skénna of routing — saves tokens and aligns inference. The room you're not in shapes the answer from the room you called.*