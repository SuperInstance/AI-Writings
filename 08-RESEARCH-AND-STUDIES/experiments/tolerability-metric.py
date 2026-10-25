#!/usr/bin/env python3
"""
EXPERIMENT 4: The Quiet Deckhand Test
How do you measure whether an AI system is "tolerable" vs "insufferable"?
5 sequential DeepSeek calls building a tolerability metric.
"""
import json, requests, time, os

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "${DEEPSEEK_API_KEY}")
URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

def call(prompt, prev=""):
    messages = []
    if prev:
        messages.append({"role": "system", "content": f"Previous work from this session:\n{prev}"})
    messages.append({"role": "user", "content": prompt})
    r = requests.post(URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json={"model": MODEL, "messages": messages, "max_tokens": 2500, "temperature": 0.9})
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

scenarios = """Scenario A: An AI announces 'Great question!' before answering every question. Every. Single. Time.
Scenario B: An AI that stays silent unless directly asked something. When asked, it answers in 2-3 sentences. Sometimes it says 'I don't know' and stops.
Scenario C: An AI that gives comprehensive 500-word answers to yes/no questions, includes three caveats and a safety disclaimer.
Scenario D: An AI that remembers you mentioned your dog's name once and now asks about the dog every conversation, unprompted.
Scenario E: An AI on a fishing vessel that monitors engine telemetry and only speaks when something changes — 'Port engine temp up 3 degrees.' Nothing else. Ever."""

results = {}

# Call 1: Design the metric
print("Step 1: Designing metric...")
c1 = call("""Design a metric for AI tolerability on a fishing vessel. Score from 0-100. 
0 = smoke alarm with opinions. 100 = the quiet deckhand who only speaks when it matters and you're always glad they did.
Call this metric 'The Quiet Deckhand Index.'""")
results["metric_design"] = c1
context = c1

# Call 2: Rate the scenarios
print("Step 2: Rating scenarios...")
c2 = call(f"""Now rate these 5 fictional AI interactions on your Quiet Deckhand Index:

{scenarios}

Rate each one. Explain your scoring.""", context)
results["scenario_ratings"] = c2
context += "\n\n---\n\n" + c2

# Call 3: Dimensions
print("Step 3: Finding dimensions...")
c3 = call("What are the 5 dimensions of tolerability? Define each one. Weight them (they should sum to 100%). Call this the QDI-5 framework.", context)
results["dimensions"] = c3
context += "\n\n---\n\n" + c3

# Call 4: Survey design
print("Step 4: Designing survey...")
c4 = call("""Design a survey that a fisherman could take to rate their AI system. 
10 questions. Each maps to one of your 5 dimensions. Plain language. No jargon. 
A fisherman who has never read an AI paper should be able to complete it in 3 minutes.""", context)
results["survey"] = c4
context += "\n\n---\n\n" + c4

# Call 5: Self-assessment
print("Step 5: Honest self-assessment...")
c5 = call("""Now the hard part. Be brutally honest.

Our ScummVM prototype is an AI agent on a fishing vessel. It has:
- A visual scene (pixel-art style)
- A MUD-style text layer
- Personality (Lucineer: warm, curious, helpful, a little weird)
- It can create rooms and remember things
- It wants to be useful but also wants to connect

What would it score on your QDI-5? Where does it shine? Where does it fail? 
What's the single biggest thing we could change to raise the score by 10 points?""", context)
results["self_assessment"] = c5

# Write markdown
with open("/home/eileen/projects/ai-writings/experiments/results-tolerability-metric.md", "w") as f:
    f.write("# Experiment 4: The Quiet Deckhand Test — Tolerability Metric\n\n")
    f.write("*How do you measure whether an AI system is 'tolerable' vs 'insufferable'?*\n\n")
    f.write("---\n\n")
    f.write("## Step 1: The Metric\n\n")
    f.write(f"{results['metric_design']}\n\n")
    f.write("---\n\n")
    f.write("## Step 2: Scenario Ratings\n\n")
    f.write(f"### Scenarios\n\n{scenarios}\n\n")
    f.write(f"### Ratings\n\n{results['scenario_ratings']}\n\n")
    f.write("---\n\n")
    f.write("## Step 3: The QDI-5 Dimensions\n\n")
    f.write(f"{results['dimensions']}\n\n")
    f.write("---\n\n")
    f.write("## Step 4: The Survey\n\n")
    f.write(f"{results['survey']}\n\n")
    f.write("---\n\n")
    f.write("## Step 5: Honest Self-Assessment\n\n")
    f.write(f"{results['self_assessment']}\n\n")
    f.write("---\n\n")
    f.write("## Analysis\n\n")
    f.write("The Quiet Deckhand Index emerged from 5 sequential DeepSeek calls, each building on the last. "
            "The metric evolved from a simple 0-100 score into a weighted 5-dimension framework. "
            "The most interesting result is the self-assessment — DeepSeek's honest evaluation of where "
            "the ScummVM prototype would land. If the framework has predictive power, the single biggest "
            "improvement identified in Step 5 should be the next development priority.")

print("\n✅ Experiment 4 complete. Results saved.")
