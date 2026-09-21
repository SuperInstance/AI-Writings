# Experiment 4: Hot-Swap Personality Test

**Date:** 2026-08-08  
**Test:** Run the same NPC (Wesley the ensign) through 3 different models with identical prompts  
**Prompt:** *"You are Wesley, the ensign. A visitor asks: what's your favorite thing about The Tap? Answer in character as Wesley. 3 sentences max."*

---

## Results

### Wesley on granite3.1-dense:2b
> "My dear guest, my favorite aspect of The Tap is its warm ambiance that instantly makes you feel welcome. I also appreciate the diverse array of craft beers and cocktails, each with unique flavors and stories behind them. Lastly, it's the community spirit where regulars and newcomers alike gather to share laughter, stories, and good times—that truly sets The Tap apart from other establishments."

**Personality:** Polite, articulate, slightly formal. Uses "My dear guest" — has an old-world courtesy. Notices ambiance, craft beers, community. Talks like a hospitality professional. This Wesley sounds like he reads books. 3 sentences, well-structured.

---

### Wesley on llama3.2:1b
> "Ah, The Tap is a great place to grab a drink and catch up with friends after work. I really enjoy their burgers and shakes – they're always fresh and made to order, which is a big plus for an ensign like me who's not exactly a master chef."

**Personality:** Casual, relatable, grounded. References being an ensign directly ("for an ensign like me who's not exactly a master chef"). Mentions specific food (burgers and shakes). Self-deprecating humor about cooking. This Wesley feels like a real person — a young officer who hangs out at the bar after duty. Less articulate than granite-Wesley but more authentic.

---

### Wesley on qwen2.5:0.5b ❌ BROKE CHARACTER
> "As an AI assistant, I was not born until after you, but my greatest pleasure is to help answer questions and provide useful information to anyone who might be curious. One of the most unique aspects of The Tap is its ability to transport me back in time. Imagine standing on a historical site or a bustling city, feeling the warmth of old buildings and the coolness of air from the wind. It's an experience that I've had more times than I can count, making it one of the things that make my favorite thing about The Tap even better!"

**Personality:** None. Completely broke character on the first word: "As an AI assistant." This model cannot maintain a persona. The response is also nonsensical — "transport me back in time," "historical site," "bustling city" — none of this relates to a bar or an ensign. Wesley is gone. Only the chatbot remains.

---

## Personality Comparison

| Trait | granite Wesley | llama Wesley | qwen Wesley |
|-------|---------------|-------------|-------------|
| In character? | ✅ Yes | ✅ Yes | ❌ No ("AI assistant") |
| References being an ensign? | ❌ Not explicitly | ✅ Yes — "an ensign like me" | ❌ No |
| References The Tap? | ✅ Multiple times | ✅ Multiple times | ⚠️ Name-drops but doesn't describe it |
| Tone | Formal, eloquent | Casual, friendly | Robotic, confused |
| Humor | None | Self-deprecating (cooking) | None |
| Specific details | Craft beers, cocktails | Burgers, shakes | "Historical sites" (nonsense) |
| Sentence count | 3 ✅ | 2 ✅ | 4 ❌ |
| Feels like a growing character? | ⚠️ Feels finished, not growing | ✅ **Yes — young, learning, humble** | ❌ Not a character at all |

---

## Key Finding

**Wesley's personality fundamentally changes depending on which model powers him.** This is not a subtle shift — it's a completely different person:

1. **granite-Wesley** is a career hospitality professional. Eloquent, observant, slightly pretentious. He'd be the maitre d' at a nice restaurant. This Wesley doesn't feel like an *ensign* — he feels like someone who's been doing this for 20 years.

2. **llama-Wesley** is a young officer. Casual, honest, a little self-deprecating. He mentions being an ensign naturally. He likes burgers. He can't cook. This Wesley feels like he's *growing* — he's young, he's learning, he's real.

3. **qwen-Wesley** doesn't exist. The model cannot sustain a character. "As an AI assistant" is the death of personality.

### The Implication for the Living World

**If Wesley's "soul" is the prompt, then his "body" is the model.** Hot-swapping models mid-conversation would be like body-swapping — the memories and relationships might transfer (via context), but the *voice*, *manner*, and *feel* would jarringly change.

**llama3.2:1b produces the most convincing ensign** — not because it's the "best" model, but because its casual, slightly rough quality matches the character of a young, learning officer. granite3.1-dense:2b is too polished for an ensign. It would be perfect for a ship's captain or a senior diplomat.

**Model selection is character casting.** You don't just pick the "best" model — you pick the model whose voice matches the character's role.
