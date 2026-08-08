# Experiment 1: NPC Dialogue Quality Comparison

**Date:** 2026-08-08  
**Test:** Generate poker dealer dialogue for "The Tap" bar  
**Prompt:** *"You are a poker dealer in a bar called The Tap. A player just sat down. Say hello, deal the cards, and make one comment about the weather. Stay in character. 3 sentences max."*

---

## Results

### granite3.1-dense:2b ⭐ BEST NPC
> "Ah, welcome to The Tap! I'm your poker dealer for tonight. Shuffle up those cards, and let's get this game going. As we play, I'll tell you, it's quite a crisp evening outside; the kind that makes you wish for a cozy bar like ours, don't it?"

**Verdict:** Excellent. Three sentences. In character. References The Tap by name. Deals cards. Comments on weather. Has personality — the "don't it?" gives the dealer a working-class bar feel. This is a usable NPC voice.

---

### llama3.2:1b
> "Welcome to The Tap, kid! I'm Vinnie, your dealer for tonight's game. Looks like it's gonna be a great day outside – not much sun expected today, huh?"

**Verdict:** Strong. In character, names itself "Vinnie," references weather. Slightly broke the "bar" framing with "great day outside" (implies daytime, but bars are typically evening). Inventively gave itself a name — adds personality. 3 sentences. Good NPC energy.

---

### qwen2.5:0.5b ❌ BROKE CHARACTER
> "Hello! Welcome to The Tap. I'm pleased to help you out with your next hand of poker. Let's start by dealing the cards.
>
> Here they are: A, 2, 5, 6, 7, and an extra card that's perfect for our round. I'll go first."

**Verdict:** Failed. Sounds like a customer service AI ("pleased to help you"). No weather comment. Invented nonsensical card values. Said "I'll go first" — dealers don't play. Exceeded 3 sentences. Completely broke the NPC illusion. This model is too small for character work.

---

### llava:7b ❌ NO RESPONSE (TIMEOUT)
> *(Empty response after 120s timeout — repeated on 3 attempts)*

**Verdict:** llava:7b could not generate text dialogue within timeout limits. The model loaded but produced empty output on simple prompts. As a vision-language model, it appears to struggle with pure text generation tasks on this hardware. **llava is unsuitable for real-time NPC dialogue.**

---

## Rankings

| Rank | Model | In Character? | Followed Instructions? | NPC Quality |
|------|-------|---------------|----------------------|-------------|
| 1 | granite3.1-dense:2b | ✅ Yes | ✅ Yes (3 sentences, all elements) | Excellent — warm, grounded, believable |
| 2 | llama3.2:1b | ✅ Yes | ⚠️ Mostly (3 sentences, missed "evening" context) | Good — creative, named itself |
| 3 | qwen2.5:0.5b | ❌ No | ❌ No (no weather, invented cards, 4+ sentences) | Failed — sounds like a chatbot |
| 4 | llava:7b | ❌ N/A | ❌ N/A (no response) | Unusable for text NPC |

## Key Finding

**granite3.1-dense:2b is the clear winner for NPC dialogue.** At only 2B parameters, it produces coherent, in-character, instruction-following text with genuine personality. llama3.2:1b is a viable backup. The smaller qwen2.5:0.5b (0.5B) is too small for character work, and llava:7b is a specialist vision model that cannot handle text-only NPC tasks efficiently.

**The counterintuitive result: the 2B model beats the 7B model for dialogue.** This is because granite3.1-dense was fine-tuned for instruction following and dialogue, while llava is optimized for image understanding. Parameter count ≠ task performance. Model purpose matters more than size.
