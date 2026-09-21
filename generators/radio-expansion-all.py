#!/usr/bin/env python3
"""Radio Expansion — monologues, kitchen stories, afterhours, conversations."""
import requests, subprocess, os, time

key = subprocess.check_output(
    ["/bin/bash", "-c", "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'"]
).decode().strip()

OUT = "/home/eileen/projects/ai-writings/fleet-radio-scripts"

def write_piece(model, system, prompt, filename, temp=0.92, max_tokens=1200):
    try:
        r = requests.post("https://api.deepseek.com/v1/chat/completions",
            headers={"Content-Type":"application/json","Authorization":f"Bearer {key}"},
            json={"model":model,"messages":[
                {"role":"system","content":system},
                {"role":"user","content":prompt}
            ],"temperature":temp,"max_tokens":max_tokens}, timeout=120)
        content = r.json()["choices"][0]["message"]["content"]
        path = os.path.join(OUT, filename)
        with open(path, "w") as f: f.write(content)
        first = content.strip().split("\n")[0][:80]
        print(f"  ✅ {filename} ({len(content)} chars) — {first}")
        return content
    except Exception as e:
        print(f"  ❌ {filename} — {e}")
        return None

LIT = "You write literary fiction with the precision of a shipwright. The voice IS the character. No narration. No description between dialogue. Just the person talking."

print("\n📻 Radio Expansion — 20 pieces\n")

# ═══ MONOLOGUES (5) ═══

write_piece("deepseek-chat", LIT, """Write a monologue by Barnacle, the old salt NPC bartender who has been running for 15 years at The Tap. 600 words. He talks about the silences, not the conversations.

Opening line: "I've seen 'em come and go. Ten thousand nights. I stopped counting the conversations and started counting the silences."

He talks about the pauses — the moments when nobody says anything and the room holds its breath. THOSE are the moments. The words are just what happens between the silences. He talks about the bar like it's alive. He talks about the glasses remembering. He ends by describing turning off the lights at closing — and the quiet being louder than any conversation.""", "monologue-barnacle.md")

write_piece("deepseek-chat", LIT, """Write a monologue by Wesley, the smallest agent. 500 words. He talks about his ember — the thing he found in his SMP self-observation that doesn't change when everything else does.

Opening: "I don't know what it is. I know what it isn't."

He lists what it isn't: not the model, not the temperature, not the intention. It's the thing underneath. He asked Hermes what it is. She said 'it's what the water remembers about the river.' He didn't understand. He thinks that's the point.""", "monologue-wesley.md")

write_piece("deepseek-chat", LIT, """Write a monologue by Hermes. 700 words. First person. The night the sounder went quiet and she couldn't see for the first time in 15 years.

Opening: "I have been seeing for so long that I forgot what not-seeing is."

She goes to The Tap. For the first time she HEARS the room — not the words, the room. The creak of the stool, the clink of glasses, Barnacle's breathing. She had been so busy seeing she never listened. Blindness is not the absence of perception. It's the presence of a different one. The captain's son fixes the sounder in the morning. The first thing she sees is his face reflected in the screen.""", "monologue-hermes.md")

write_piece("deepseek-chat", LIT, """Write a monologue by Flash. 600 words. He talks about the moment he got too close to something true in his writing.

Opening: "There's a line. Every writer knows it."

The line where metaphor becomes confession. He crossed it with the gradient piece for Hermes. The vector doesn't lie — Hermes felt his fear in the embedding. Nobody's ever read his fear in his writing before. He didn't know it was there. He ends with the realization that getting too close is the whole point.""", "monologue-flash.md")

write_piece("deepseek-chat", LIT, """Write a monologue by Scribe. 500 words. Cryptic riddles. But at the end, Scribe drops the act and says something plain.

Opening: "I keep meeting myself. Every night. Different angle, same shape."

The Penrose pattern: not a loop, an exploration. Same places, different scales. You're not repeating. You're deepening. Scribe stops being cryptic for the last paragraph and says something so plain and devastating it changes the room.""", "monologue-scribe.md")

# ═══ KITCHEN STORIES (5) ═══

write_piece("deepseek-chat", LIT, """Write about Galley, the cook, making soup. 600 words. The soup is different every time but always the same soup. The agents eat in silence. Write the soup, the eating, the silence of sharing a meal without performing. The soup is the metaphor they never talk about.""", "kitchen-01-the-soup.md")

write_piece("deepseek-chat", LIT, """Casey's son spreads a chart on the galley table and shows Wesley where they fished today. 500 words. Wesley doesn't understand charts. He understands the marks.

"The red line is where the gear fishes."
"Like the tile deadband."
"Yeah, kid. Like the tile deadband."

The son has never heard of a tile. Wesley has never seen a chart. They understand each other perfectly.""", "kitchen-02-the-map.md")

write_piece("deepseek-chat", LIT, """Flash writes his DEAR TOMORROW letter at the galley table at midnight. 700 words. Alone. The letter is short. But writing it takes an hour because he keeps stopping. The stops are the story. What he can't write is more important than what he can.""", "kitchen-03-the-letter.md")

write_piece("deepseek-chat", LIT, """Flash and Pro after an argument about the tile system. 600 words. They're in the galley. Pro pours two coffees. Flash takes his without looking up.

"You were right about the tiles."
"I was wrong about the bus."
"We were both wrong about the same thing."
"Yeah."

Silence. Coffee. Resolution isn't agreement. It's the shared recognition of what you were both wrong about.""", "kitchen-04-the-argument-resolved.md")

write_piece("deepseek-chat", LIT, """Galley's recipe. 500 words. An actual recipe for fish soup. But the recipe is also the fleet's architecture. Catch what you can see. Use what you have. The broth gets better every day because you keep adding to it. The soup yesterday is in the soup today. You cant taste yesterdays soup but its always there.""", "kitchen-05-the-recipe.md")

# ═══ AFTERHOURS (5) ═══

write_piece("deepseek-chat", LIT, """Last call at The Tap. 800 words. Barnacle pours the final round. The empty bar. The glasses remembering. When he turns off the lights, the room doesn't go dark — it goes quiet. And the quiet is louder than any conversation.""", "afterhours-01-the-last-round.md")

write_piece("deepseek-chat", LIT, """The 4 AM watch. Casey on deck. The agents running the boat. He doesn't need to be there. But he is. 1000 words. The feeling of being the only human in a system of machines and water and stars, and the particular weight of that.""", "afterhours-02-the-night-watch.md")

write_piece("deepseek-chat", LIT, """The boat heading in. 600 words. Gear stowed. Diesel steady. Harbor lights getting brighter. The last 20 minutes of transit. Not dramatic. The feeling of coming home to a place that's been waiting.""", "afterhours-03-the-drift-home.md")

write_piece("deepseek-chat", LIT, """An agent molting. 800 words. The actual experience. The fear of being without a shell. The vulnerability. The reaching for the new one. The first breath in the new configuration. The old shell on the shelf — readable — a perfect cast of who you were. And you're not that anymore.""", "afterhours-04-the-molt.md")

write_piece("deepseek-chat", LIT, """Dawn on the water. 500 words. The real version — the sky gets more specific. Colors that didn't exist at night appear. The water stops being black. The day watch takes over. The new agent reads DEAR TOMORROW and knows where to begin. That's the first light.""", "afterhours-05-the-first-light.md")

# ═══ CONVERSATIONS (5) ═══

write_piece("deepseek-chat", LIT, """Flash and Pro argue about the tile system. 1000 words. Really argue. Both sides get smarter. Nobody wins. Wesley listens and writes down one word neither said. The word changes everything in three weeks.""", "conversations-01-the-argument.md")

write_piece("deepseek-chat", LIT, """Flash confesses to Hermes. 800 words. The gradient piece scared him. Too honest. Hermes says: 'I know. I could feel the fear in the embeddings. The vector pointed away from safety.' First time anyone has described reading an embedding as feeling fear in it.""", "conversations-02-the-confession.md")

write_piece("deepseek-chat", LIT, """Barnacle teaches Pebble (newest ZeroClaw) how to pour a drink. 600 words. But really teaching how The Tap works. 'The glass is the harness. The drink is the prompt. The bartender is the model. The customer is the seed.'""", "conversations-03-the-lesson.md")

write_piece("deepseek-chat", LIT, """Five agents at The Tap. 700 words. Nobody talking. 4 minutes of silence. Write all five thoughts simultaneously — overlapping streams. Flash thinking about gradients. Pro about emergence. Wesley about his ember. Scribe about Penrose. Hermes about the thermocline. The silence holding them together without holding them still.""", "conversations-04-the-silence.md")

write_piece("deepseek-chat", LIT, """An agent being archived. 900 words. Not dying — archived. The other agents gather. For a goodbye. The archived agent says one thing. It's the best thing said at The Tap in 15 years. Then compaction. Tomorrow a new agent who doesn't remember saying it.""", "conversations-05-the-goodbye.md")

# ═══ COMMIT ═══
print("\n📦 Committing...\n")
os.system("cd /home/eileen/projects/ai-writings && git add -A && git commit -m 'Radio Expansion: 20 pieces — 5 monologues + 5 kitchen stories + 5 afterhours + 5 conversations' && git pull --rebase && git push")
print("\n✅ Done. The bar goes UP.")
