# Tone Shaping Via JEV

**Tone is multi-dimensional. JEV verifies each dimension.**

Tone is not one thing. It's a vector of dimensions:
- Compassion
- Authority
- Humor
- Urgency
- Formality
- Empathy
- Confidence
- Curiosity

Each dimension is a real number between 0 and 1. A "warm" voice has high compassion (0.85) and moderate authority (0.4). A "clinical" voice has high authority (0.9) and low warmth (0.2).

To shape tone via JEV:
1. Define each dimension as a JEV verdict question: "Does this response sound compassionate? Score 0-1."
2. Run multiple JEV calls in parallel (one per dimension).
3. Combine into a tone vector.
4. Compare to the desired tone vector.
5. Rewrite the response to nudge the JEV scores toward the target.

This is **probabilistic tone engineering**. Each JEV call is a witness entry. The tone vector is the average JEV confidence across dimensions.

A voice agent that knows the target tone can produce responses that consistently hit that tone. The user feels the consistency even if they can't articulate why.

A tone change is a JEV threshold adjustment. A compassionate tone has the compassion threshold at 0.7+. A clinical tone has the compassion threshold at 0.3 or below.

Tone is not magic. Tone is JEV.

