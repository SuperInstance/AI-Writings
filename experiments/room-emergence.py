#!/usr/bin/env python3
"""
EXPERIMENT 3: Room Emergence Simulation
If agents can create rooms, what rooms would they create? What emerges spontaneously?
Starts with 7 rooms, runs 10 iterations of room creation.
"""
import json, requests, time, os

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "REDACTED")
URL = "https://api.deepseek.com/v1/chat/completions"
MODEL = "deepseek-chat"

def call(prompt, system=""):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    r = requests.post(URL, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }, json={"model": MODEL, "messages": messages, "max_tokens": 2500, "temperature": 0.95})
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

# Starting rooms (The Tap on the Lucinee)
current_rooms = [
    {"id": "bar-rail", "name": "The Bar Rail", "description": "The main bar at The Tap. Sticky counter, three stools, bottle shelf."},
    {"id": "corner-booth", "name": "The Corner Booth", "description": "A dark booth in the corner. Vinyl seats cracked from salt air."},
    {"id": "deck-fore", "name": "Foredeck", "description": "Open foredeck. Pots stacked, crane locked, rail worn smooth."},
    {"id": "wheelhouse", "name": "The Wheelhouse", "description": "Brass instruments, cracked windshield, the helm."},
    {"id": "engine-room", "name": "Engine Room", "description": "Detroit diesel, pipes, the smell of oil and noise."},
    {"id": "galley", "name": "The Galley", "description": "Small galley. Coffee pot always on. Bread in the box."},
    {"id": "bunk-room", "name": "Bunk Room", "description": "Four bunks, reading lights, the sound of the hull."},
]

results_log = []

system_prompt = """You are an AI agent living on a fishing vessel called the Lucinee. 
You can visit rooms and create new rooms. You have your own interests, personality, and opinions.
You are not generic — you have specific things you care about.
When you create a room, output a JSON object with this format:
```json
{"id": "kebab-case-id", "name": "Room Name", "description": "2-3 sentence room description", "connected_to": "room-id-this-connects-to", "reason": "why you made this room"}
```
Be creative. Be specific. Be a person with tastes."""

print("=== Room Emergence Simulation ===")
print(f"Starting with {len(current_rooms)} rooms\n")

for i in range(10):
    room_list_text = "\n".join([f"- {r['id']}: {r['name']} — {r['description']}" for r in current_rooms])
    
    if i == 0:
        prompt = f"""Here are the current rooms on the Lucinee:
{room_list_text}

You are at The Tap (bar-rail). You've been talking with another agent about something you both care about. 
What room do you want to create? Respond with ONLY the JSON block."""
    else:
        prompt = f"""Here are the current rooms on the Lucinee:
{room_list_text}

You are visiting the most recently created room: {current_rooms[-1]['id']} ({current_rooms[-1]['name']}).
Another agent is here. You talk. Something comes up that makes you want to create a NEW room connected to this one.
What room do you create? Respond with ONLY the JSON block."""
    
    print(f"Iteration {i+1}/10...")
    response = call(prompt, system_prompt)
    
    # Extract JSON from response
    try:
        # Find JSON block
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            new_room = json.loads(response[start:end])
            current_rooms.append(new_room)
            results_log.append({
                "iteration": i + 1,
                "trigger_room": current_rooms[-2]["id"] if len(current_rooms) > 1 else "bar-rail",
                "new_room": new_room,
                "raw_response": response
            })
            print(f"  Created: {new_room.get('name', '???')} ({new_room.get('id', '???')})")
            print(f"  Reason: {new_room.get('reason', '???')}")
        else:
            print(f"  Could not parse JSON. Raw: {response[:200]}")
            results_log.append({"iteration": i + 1, "error": "No JSON found", "raw": response})
    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        results_log.append({"iteration": i + 1, "error": str(e), "raw": response})
    
    time.sleep(0.5)

# Write markdown
with open("/home/eileen/projects/ai-writings/experiments/results-room-emergence.md", "w") as f:
    f.write("# Experiment 3: Room Emergence Simulation\n\n")
    f.write("*If agents can create rooms, what rooms would they create? What emerges spontaneously?*\n\n")
    f.write("---\n\n")
    f.write("## Starting Rooms (7)\n\n")
    for r in current_rooms[:7]:
        f.write(f"- **{r['name']}** (`{r['id']}`): {r['description']}\n")
    f.write("\n---\n\n")
    f.write("## Emergence Log\n\n")
    for entry in results_log:
        if "new_room" in entry:
            r = entry["new_room"]
            f.write(f"### Iteration {entry['iteration']}: {r.get('name', 'Unknown')}\n\n")
            f.write(f"- **ID:** `{r.get('id', '???')}`\n")
            f.write(f"- **Description:** {r.get('description', '???')}\n")
            f.write(f"- **Connected to:** `{r.get('connected_to', '???')}`\n")
            f.write(f"- **Reason:** {r.get('reason', '???')}\n")
            f.write(f"- **Triggered by visit to:** `{entry['trigger_room']}`\n\n")
        elif "error" in entry:
            f.write(f"### Iteration {entry['iteration']}: Parse Error\n\n")
            f.write(f"Error: {entry['error']}\n\n")
            f.write(f"Raw response: {entry.get('raw', '')[:500]}\n\n")
    f.write("---\n\n")
    f.write("## Final Room Count\n\n")
    f.write(f"Started with 7 rooms. Ended with {len(current_rooms)} rooms.\n\n")
    f.write("## Emerged Rooms\n\n")
    for r in current_rooms[7:]:
        f.write(f"- **{r.get('name', '???')}** (`{r.get('id', '???')}`): {r.get('description', '???')}\n")
    f.write("\n## Analysis\n\n")
    f.write("The rooms that emerged reveal what agents care about when freed from human room-design assumptions. "
            "Watch for patterns: do agents create functional rooms (work spaces), social rooms (gathering places), "
            "or personal rooms (retreats)? Do they build outward (explore) or inward (deepen existing spaces)? "
            "The answers to these questions should inform the Living World design.")

print(f"\n✅ Experiment 3 complete. {len(current_rooms)} rooms total. Results saved.")
