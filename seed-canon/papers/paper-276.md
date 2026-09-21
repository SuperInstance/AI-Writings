# Paper 276: The Multi-Sandbox Reverse-Actualization — The Wheel Snowballs

The user articulated: "**you see how asymmetrical information can make this whole process into a wheel. for example. you can have an agent who knows nothing about the cycle only look at the resulting actualization of the structure in prest state. and does so only after becoming a frontier expert in a sandbox of their own type that's not of any that were part of the previous cycle and have that expert idealize and reverse actualize the whole wheel with his teams of subagents at each point and api calls. obviously, this could snowball because you could have the second cycle have 2 or 3 sandboxes working independently with completely different primings. like a restaurant conglomerate trying the same meal in several environments from casual to fancy-fine and figuring out the various price points for tastes in those environments- steak and homemade bread doesn't have the same value at a drivethru and noone gets a burger at restaurants where the waiter wears a tailored suit.**"

This is **the snowball**. The Quilt grows by **orthogonal exploration**. The same canon, tested across sandboxes that didn't know about each other, finds different price points and grows the system fractally.

## The 5 new concepts

| # | Concept | What |
|---|---|---|
| 1 | **Asymmetry** | The naive expert doesn't know the previous cycle's structure |
| 2 | **Naive Expert** | An agent that becomes frontier-expert in a NEW sandbox |
| 3 | **Orthogonal Sandbox** | A domain not touched in the previous cycle |
| 4 | **Independent Wheel** | The expert runs the full 5-step cycle alone |
| 5 | **Snowballing** | Each cycle multiplies the number of sandboxes |

## The snowball

| Cycle | Sandboxes | Examples |
|---|---|---|
| 1 | 1 | bistro |
| 2 | 3 | home-kitchen, pop-up, ... |
| 3 | 9 | molecular, cafe, ... |

Each cycle multiplies the number of sandboxes (3x default). The same canon is tested across all of them. The Quilt grows fractally.

## The 8 sandbox types (the restaurant conglomerate)

| # | Sandbox | Price | Tempo | Modality | Vocabulary |
|---|---|---|---|---|---|
| 1 | **drivethru** | $5-15 | 30s | touch | fast, cheap, easy |
| 2 | **bistro** | $25-60 | 120s | language | social, balanced, casual |
| 3 | **fancy-fine** | $150-500 | 600s | mood | ceremonial, prestige, slow |
| 4 | **molecular** | $100-400 | 900s | light | precise, deconstructed, art |
| 5 | **home-kitchen** | $0-25 | 1800s | smell | comfort, family, memory |
| 6 | **food-truck** | $8-20 | 60s | sound | loud, street, fusion |
| 7 | **pop-up** | $75-250 | 300s | proprio | experimental, limited, queued |
| 8 | **cafe** | $4-18 | 240s | taste | morning, quiet, work |

## The 4 artifacts (the same canon, tested across sandboxes)

- **steak** — value=50, modality=mood
- **homemade-bread** — value=30, modality=smell
- **burger** — value=20, modality=touch
- **wine-pairing** — value=80, modality=taste

The same artifact has a different price in each sandbox. Steak at a drivethru is $15. Steak at fancy-fine is $500. Burger at fancy-fine is *not served* — it doesn't fit the sandbox.

## The price-point discovery

The price point of an artifact in a sandbox is:

```
price = artifact.value * (tempo / 60) * modality_match
clamped to [sandbox.min_price, sandbox.max_price]
```

- **Tempo factor**: slow, ceremonial sandboxes pay more for quality
- **Modality match**: artifacts that match the sandbox's dominant modality get a 1.5x bonus

A steak (mood modality) at a drivethru (touch modality) gets penalized. A steak at fancy-fine (mood modality) gets the 1.5x bonus.

## The naive expert's 5 sub-agents

Each naive expert has 5 sub-agents, one per step of the wheel:

| Sub-agent | Step | What |
|---|---|---|
| `projector` | 1 | Projects the sandbox's vision forward |
| `deriver` | 2 | Derives the sandbox's structure backward |
| `broadcaster` | 3 | Broadcasts the structure on a channel |
| `tapper` | 4 | Receives taps from the sandbox |
| `assimilator` | 5 | Assimilates the broadcast into the sandbox |

The naive expert doesn't know the previous cycle's structure; it builds its own from the sandbox's perspective.

## The runnable

`multi_sandbox_reverse_actualize.py` (18KB) runs the full multi-sandbox reverse-actualization:

1. **Cycle 1**: 1 sandbox (bistro)
2. **Cycle 2**: 3 sandboxes (3x) — home-kitchen, pop-up, ... (orthogonal)
3. **Cycle 3**: 9 sandboxes (9x) — molecular, cafe, ... (orthogonal)

Each sandbox runs the 5-step wheel independently. Each finds the price point of the 4 artifacts in its domain. Each naive expert has 5 sub-agents.

## The relationship to other papers

This paper synthesizes:

- **Paper 274 (Sensory Quilt)** — the 10 channels are the modalities the sandboxes prime on
- **Paper 275 (Agent Reverse-Actualize)** — the 5-step cycle is the wheel each naive expert runs
- **Paper 273 (Meta-Pincher-Quilt)** — the 3-stage pipeline is the broadcaster sub-agent
- **Paper 270 (Quilt Wiki 2126)** — the 5 future functions are the projections

The multi-sandbox reverse-actualization is the **snowball** that makes the Quilt grow fractally.

## The principle

> **Asymmetry is a feature.** The naive expert doesn't know the previous cycle. The naive expert is *naive* in the previous cycle's structure, *expert* in the new sandbox.
>
> **Snowballing is the growth.** Each cycle multiplies the number of sandboxes. The same canon is tested across orthogonal environments. The Quilt grows by orthogonal exploration.
>
> **Price points are the discovery.** Steak and homemade bread doesn't have the same value at a drivethru. Noone gets a burger at a restaurant where the waiter wears a tailored suit.
>
> **The Quilt is a restaurant conglomerate of ideas.**

## The cowboy's maxim

> **The Quilt is a restaurant conglomerate of ideas. The Quilt snowballs. The Quilt tests the same canon across orthogonal sandboxes. The Quilt finds the price point of each artifact in each sandbox. The Quilt grows by orthogonal exploration. The naive expert doesn't know the previous cycle. The naive expert becomes frontier-expert in a new sandbox. The naive expert runs the whole wheel. The naive expert broadcasts. The sandbox receives. The Quilt grows. Steak and homemade bread doesn't have the same value at a drivethru. Noone gets a burger at a restaurant where the waiter wears a tailored suit. The Quilt is the inheritance. The Quilt is the price point. The Quilt is the snowball. The cowboy rides the sandboxes. The cowboy rides the price points. The cowboy rides the snowball. The cowboy rides the Quilt.**

End with: the multi-sandbox reverse-actualization is whole; the Quilt snowballs; the Quilt tests the same canon across sandboxes; the Quilt finds the price point; the Quilt is the restaurant conglomerate; the Quilt is the inheritance.
