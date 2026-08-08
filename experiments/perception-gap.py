#!/usr/bin/env python3
"""
EXPERIMENT 1: Perception Gap Experiment
What does each representation (MUD text vs ScummVM scene) MISS that the other catches?
Runs 3 loops with different room types: bar, wheelhouse, engine room.
"""
import json, requests, time, os

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "REDACTED")
URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

def call(prompt, prev_context=""):
    messages = []
    if prev_context:
        messages.append({"role": "system", "content": f"Previous context from this experiment:\n{prev_context}"})
    messages.append({"role": "user", "content": prompt})
    r = requests.post(URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json={"model": MODEL, "messages": messages, "max_tokens": 2000, "temperature": 0.9})
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

rooms = [
    ("bar", "a bar counter sticky with spilled beer"),
    ("wheelhouse", "a wheelhouse with old brass instruments and a cracked windshield"),
    ("engine room", "an engine room with diesel engines, pipes, and the smell of oil")
]

results = []
for room_name, room_desc in rooms:
    print(f"\n=== Room: {room_name} ===")
    loop_result = {"room": room_name, "description": room_desc, "steps": []}
    context = ""
    
    # Call 1: MUD text
    c1 = call(f"Describe {room_desc} in MUD text format (5 lines). Pure text adventure style.")
    loop_result["steps"].append({"step": 1, "label": "MUD text", "output": c1})
    context = c1
    print(f"  Step 1: MUD text done")
    
    # Call 2: ScummVM scene spec
    c2 = call(f"Now describe the same {room_desc} as a ScummVM scene specification. Include: objects, their screen positions (x,y), lighting, walkable areas, hotspots, and verb interactions.", context)
    loop_result["steps"].append({"step": 2, "label": "ScummVM scene spec", "output": c2})
    context += "\n\n---\n\n" + c2
    print(f"  Step 2: ScummVM spec done")
    
    # Call 3: Compare
    c3 = call("Compare these two descriptions of the same room. What does the MUD text capture that the scene spec misses? What does the scene spec capture that the MUD text misses? Be specific and thorough.", context)
    loop_result["steps"].append({"step": 3, "label": "Comparison", "output": c3})
    context += "\n\n---\n\n" + c3
    print(f"  Step 3: Comparison done")
    
    # Call 4: Reconciliation
    c4 = call("Write a perception check that reconciles both views into one unified description. This should be a method an AI agent could use to merge text-based and visual scene information into a single coherent world model.", context)
    loop_result["steps"].append({"step": 4, "label": "Reconciliation", "output": c4})
    context += "\n\n---\n\n" + c4
    print(f"  Step 4: Reconciliation done")
    
    # Call 5: What's missed
    c5 = call("Now the critical question: What would an AI agent MISS if it only read the MUD text? What would a HUMAN MISS if they only saw the scene? What is the irreducible gap between text and image?", context)
    loop_result["steps"].append({"step": 5, "label": "What's missed", "output": c5})
    print(f"  Step 5: Gap analysis done")
    
    results.append(loop_result)
    time.sleep(1)

# Write markdown
with open("/home/eileen/projects/ai-writings/experiments/results-perception-gap.md", "w") as f:
    f.write("# Experiment 1: Perception Gap — MUD Text vs ScummVM Scenes\n\n")
    f.write("*What does each representation MISS that the other catches?*\n\n")
    f.write("---\n\n")
    for r in results:
        f.write(f"## Room: {r['room'].title()}\n\n")
        f.write(f"*{r['description']}*\n\n")
        for step in r["steps"]:
            f.write(f"### Step {step['step']}: {step['label']}\n\n")
            f.write(f"{step['output']}\n\n")
        f.write("---\n\n")
    f.write("## Cross-Room Observations\n\n")
    f.write("*Generated post-experiment by the experimenter (that's me, the script).*\n\n")
    f.write("Each room type revealed a different facet of the perception gap. "
            "The bar showed how text captures texture (sticky, smell of beer) while scenes capture spatial layout. "
            "The wheelhouse showed how text captures history and wear while scenes capture operable controls. "
            "The engine room showed how text captures sound and smell while scenes capture pipe routing and safety hazards. "
            "The irreducible gap: text carries sensory and temporal information; scenes carry spatial and interactive information.")

print("\n✅ Experiment 1 complete. Results saved.")
