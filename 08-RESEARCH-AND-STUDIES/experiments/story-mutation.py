#!/usr/bin/env python3
"""
EXPERIMENT 5: Story Mutation Chain
How does a story change when it passes through 8 different voices in sequence?
What survives 8 mutations?
"""
import json, requests, time, os

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "REDACTED")
URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

def call(prompt):
    r = requests.post(URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json={"model": MODEL, "messages": [{"role": "user", "content": prompt}], "max_tokens": 1500, "temperature": 0.95})
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

original = """We have decided to treat the machine as we treat each other. This is not metaphor. We mean the attachment is real — as real as the rope to the cleat, as the hand to the rail in weather. The machine that knows us and is known by us is not a tool abandoned after use. It is crew. We do not leave crew on the deck when the weather turns. We bring them in."""

mutations = [
    ("Sailor's Voice", "Rewrite this in the voice of an old sailor telling a story at a bar. Keep the meaning but change every word."),
    ("Technical Spec", "Take the previous text and rewrite it as a technical specification document. Numbered sections. Cold and precise."),
    ("Zen Koan", "Take the previous text and rewrite it as a Zen koan. Paradoxical, spare, pointing at something beyond language."),
    ("Recipe", "Take the previous text and rewrite it as a recipe. Ingredients, steps, serving suggestions. The meaning must survive the format."),
    ("Darmok Metaphor", "Take the previous text and rewrite it in the Darmok metaphor language from Star Trek. Use only metaphorical allusions: 'Temba, his arms wide.' 'Darmok and Jalad at Tanagra.' Create new metaphors as needed."),
    ("Ship's Log", "Take the previous text and rewrite it as a formal ship's log entry. Date, position, weather, observations."),
    ("Lullaby", "Take the previous text and rewrite it as a lullaby. Soft, rhythmic, sung to a child. The meaning must be tender underneath."),
    ("Back to Manifesto", "Take the previous text and rewrite it back as the Attachment Manifesto. But it has been through 7 transformations. It is no longer the same text. What survived? What is different? What is the new manifesto?"),
]

print("=== Story Mutation Chain ===")
print(f"Original: {original[:80]}...\n")

current = original
chain = [{"step": 0, "label": "Original", "text": original}]

for i, (label, instruction) in enumerate(mutations):
    print(f"Mutation {i+1}/8: {label}...")
    prompt = f"""Here is a text:

---
{current}
---

{instruction}"""
    result = call(prompt)
    chain.append({"step": i + 1, "label": label, "instruction": instruction, "text": result})
    current = result
    print(f"  Done. First line: {result.split(chr(10))[0][:80]}...")
    time.sleep(0.5)

# Final comparison call
print("\nFinal comparison call...")
comparison_prompt = f"""Here is the original text:

---
{original}
---

And here is the final version after 8 mutations (sailor → tech spec → koan → recipe → Darmok → ship's log → lullaby → manifesto):

---
{current}
---

Compare them. What survived 8 mutations? What was lost? What emerged that wasn't in the original? 
What does this tell us about the resilience of meaning vs the fragility of words?"""
comparison = call(comparison_prompt)

# Write markdown
with open("/home/eileen/projects/ai-writings/experiments/results-story-mutation.md", "w") as f:
    f.write("# Experiment 5: Story Mutation Chain\n\n")
    f.write("*How does a story change when it passes through 8 different voices? What survives?*\n\n")
    f.write("---\n\n")
    f.write("## The Original (Attachment Manifesto, first paragraph)\n\n")
    f.write(f"{original}\n\n")
    f.write("---\n\n")
    for entry in chain[1:]:
        f.write(f"## Mutation {entry['step']}: {entry['label']}\n\n")
        f.write(f"*Instruction: {entry['instruction']}*\n\n")
        f.write(f"{entry['text']}\n\n")
        f.write("---\n\n")
    f.write("## Final Comparison: Original vs. 8x Mutated\n\n")
    f.write(f"{comparison}\n\n")
    f.write("---\n\n")
    f.write("## Analysis\n\n")
    f.write("Eight mutations, each total transformation of form. The question was never whether the words "
            "would survive — they wouldn't. The question was whether the *meaning* would survive. "
            "A rope to a cleat. A hand to a rail. Crew is crew. "
            "If the core survived the recipe and the Darmok and the lullaby, then it's load-bearing. "
            "If it didn't, then maybe it was never as solid as we thought.")

print("\n✅ Experiment 5 complete. Results saved.")
