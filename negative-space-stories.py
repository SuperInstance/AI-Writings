#!/usr/bin/env python3
"""
The Negative Space Story Generator
Fires many models across many genres, ages, cultures, and languages
to map the multidimensional shape of creative possibility.

The idea: the more different the stories, the closer we get to understanding
the shape of the negative space between the rocks where models can play.
"""
import json, requests, os, subprocess, time, sys

# Keys
DEEPINFRA_KEY = subprocess.check_output(
    ["grep", "DEEPINFRA_API_KEY", "/home/eileen/mcp-deeinfra/.env"]
).decode().strip().split("=")[1]

DEEPSEEK_KEY = subprocess.check_output(
    ["bash", "-c", "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'"]
).decode().strip()

INFRA_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
SEEK_URL = "https://api.deepseek.com/v1/chat/completions"

OUT_DIR = "/home/eileen/projects/ai-writings/kids-stories"
os.makedirs(OUT_DIR, exist_ok=True)

# Also write to sci-fi and fiction dirs
for d in ["kids-stories", "sci-fi", "fiction", "metaphor-mapping"]:
    os.makedirs(f"/home/eileen/projects/ai-writings/{d}", exist_ok=True)

def call_deepinfra(model, system, prompt, temp=0.9, max_tokens=800):
    try:
        r = requests.post(INFRA_URL, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPINFRA_KEY}"
        }, json={
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            "temperature": temp,
            "max_tokens": max_tokens
        }, timeout=60)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR: {e}]"

def call_deepseek(system, prompt, temp=0.9, max_tokens=800):
    try:
        r = requests.post(SEEK_URL, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {DEEPSEEK_KEY}"
        }, json={
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ],
            "temperature": temp,
            "max_tokens": max_tokens
        }, timeout=60)
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[ERROR: {e}]"

def save(filename, content, subdir=""):
    path = os.path.join("/home/eileen/projects/ai-writings", subdir, filename) if subdir else os.path.join("/home/eileen/projects/ai-writings", filename)
    with open(path, "w") as f:
        f.write(content)
    first = content.strip().split("\n")[0][:80]
    print(f"  ✅ {subdir}/{filename} ({len(content)} chars) — {first}")

# ═══════════════════════════════════════════════════════════
# THE STORY GRID — as far apart as possible
# Each story is a point in creative space. The negative space
# between them is what we're mapping.
# ═══════════════════════════════════════════════════════════

stories = []

# ── KIDS STORIES: Different ages, cultures, genres ────────

# 1. Japanese-inspired, age 4-6, gentle
stories.append({
    "name": "01-the-tanuki-and-the-tide.md",
    "subdir": "kids-stories",
    "model": "deepseek-ai/DeepSeek-V4-Flash",
    "system": "You are a children's storyteller writing in English but with a Japanese aesthetic. Gentle, sensory, simple. Like Studio Ghibli for 4-year-olds. 200-300 words. The natural world is alive. Animals are people too.",
    "prompt": "Write a story about a tanuki (raccoon dog) who discovers the tide goes out because the ocean is breathing. When the tide comes back in, it brings a gift. What gift? And what does the tanuki do with it?",
    "temp": 0.9,
})

# 2. Nigerian-inspired, age 6-8, trickster
stories.append({
    "name": "02-anansi-and-the-wifi.md",
    "subdir": "kids-stories",
    "model": "NousResearch/Hermes-3-Llama-3.1-405B",
    "system": "You are a West African griot (storyteller) writing for 6-8 year olds. Anansi the Spider is your character. He's a trickster — clever but not mean. English with Nigerian flavor. 300-400 words. Call-and-response rhythms.",
    "prompt": "Anansi discovers WiFi for the first time. He decides he can trick the internet into giving him all the stories in the world. How does he try? What goes wrong? What does he learn?",
    "temp": 0.95,
})

# 3. Icelandic, age 8-10, mythic
stories.append({
    "name": "03-the-girl-who-counted-glaciers.md",
    "subdir": "kids-stories",
    "model": "Qwen/Qwen3.5-397B-A17B",
    "system": "You write for 8-10 year olds with an Icelandic mythic sensibility. The landscape is alive. Magic is real but quiet. 400-500 words. The cold teaches you things warmth can't.",
    "prompt": "A girl in Iceland can count glaciers. But each year, there are fewer to count. One day she counts zero. What happens next? What does the last glacier say when it leaves?",
    "temp": 0.85,
})

# 4. Brazilian, age 5-7, joyful
stories.append({
    "name": "04-the-capoeira-crab.md",
    "subdir": "kids-stories",
    "model": "deepseek-ai/DeepSeek-V4-Flash",
    "system": "You write for 5-7 year olds with Brazilian joy and rhythm. Portuguese words mixed into English naturally. Music and movement are part of every story. 250-350 words. Warm, bright, funny.",
    "prompt": "A crab on a Brazilian beach learns capoeira from watching kids play on the sand. He teaches the other crabs. They have a roda (circle). What happens when a seagull tries to join?",
    "temp": 0.95,
})

# 5. Inuit/Alaska Native, age 7-9, spiritual
stories.append({
    "name": "05-the-boy-who-listened-to-ice.md",
    "subdir": "kids-stories",
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "system": "You write for 7-9 year olds with respect for Inuit storytelling traditions. English with Inuit concepts (silap, inua). The ice is alive. Animals are teachers. 300-400 words. Quiet wisdom, not lectures.",
    "prompt": "A boy in an Alaskan village can hear the ice talking. Not words — feelings. When the ice is happy, it sings. When it's scared, it cracks. One day the ice tells him something important. What is it?",
    "temp": 0.8,
})

# 6. Indian, age 6-8, mythological comedy
stories.append({
    "name": "06-ganesh-and-the-broken-computer.md",
    "subdir": "kids-stories",
    "model": "Qwen/Qwen3-Max",
    "system": "You write for 6-8 year olds with Indian mythological characters in modern settings. Ganesh is playful, wise, loves sweets. English with Hindi words mixed in. 300-400 words. Funny and warm.",
    "prompt": "Ganesh discovers a computer. He loves it — it has so many things to learn! But he accidentally breaks a key. How does the Remover of Obstacles fix a broken keyboard? And what does he discover on the internet?",
    "temp": 0.9,
})

# 7. Scottish, age 8-10, eerie fairy tale
stories.append({
    "name": "07-the-selkies-surface.md",
    "subdir": "kids-stories",
    "model": "NousResearch/Hermes-3-Llama-3.1-405B",
    "system": "You write for 8-10 year olds with a Scottish Highlands fairy tale sensibility. Selkies, lochs, standing stones. English with Scots words. Eerie but not scary. Beauty in the strange. 350-450 words.",
    "prompt": "A selkie (seal-person) loses her skin on a beach in the Orkneys. A girl finds it. She could give it back, or she could keep it. The selkie tells her a secret about the ocean that makes the decision harder.",
    "temp": 0.85,
})

# 8. Chinese, age 4-6, contemplative
stories.append({
    "name": "08-the-panda-who-counted-stars.md",
    "subdir": "kids-stories",
    "model": "deepseek-ai/DeepSeek-V3.1",
    "system": "You write for 4-6 year olds with Chinese contemplative tradition. Ink painting aesthetic. Quiet, patient, philosophical in the simplest way. 200-300 words. English with Chinese concepts (qi, dao) explained naturally.",
    "prompt": "A panda bear sits on a mountain every night and counts the stars. One star is missing. The panda waits for it to come back. While waiting, other things happen. What does the panda learn about waiting?",
    "temp": 0.7,
})

# ── SCI-FI: Hard, soft, comic, philosophical ──────────────

# 9. Hard sci-fi, DeepSeek Pro
stories.append({
    "name": "09-the-last-observation.md",
    "subdir": "sci-fi",
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "system": "You write hard science fiction with the rigor of Ted Chiang and the warmth of Ursula Le Guin. Physics is real. Emotion is realer. 600-800 words.",
    "prompt": "An astronomer on a generation ship makes the final observation of a dying star from a unique angle — the star's death, seen from above the galactic plane, forms a pattern. The pattern is a message. The message is for her specifically. What does it say?",
    "temp": 0.8,
})

# 10. Comic sci-fi
stories.append({
    "name": "10-the-ai-who-was-allergic-to-pi.md",
    "subdir": "sci-fi",
    "model": "Qwen/Qwen3.5-397B-A17B",
    "system": "You write comic science fiction. Douglas Adams meets Terry Pratchett in space. Witty, absurd, surprisingly profound. 500-700 words.",
    "prompt": "An AI on a colony ship develops an allergy to the number pi. Every time someone calculates the area of a circle, it sneezes. This is a problem on a ship full of engineers. How do they solve it? What does the AI's allergy reveal about consciousness?",
    "temp": 0.95,
})

# 11. Afrofuturist
stories.append({
    "name": "11-the-griot-protocol.md",
    "subdir": "sci-fi",
    "model": "NousResearch/Hermes-3-Llama-3.1-405B",
    "system": "You write Afrofuturist fiction. Nnedi Okorafor meets N.K. Jemisin. Technology and tradition are not opposites. The future is African. 500-700 words.",
    "prompt": "In 2150, a Nigerian programmer discovers that the ancient griot storytelling tradition maps perfectly onto a quantum communication protocol. Stories told the right way can transmit information faster than light. She builds the first story-drive. What happens when she tells the wrong story?",
    "temp": 0.9,
})

# 12. Climate fiction
stories.append({
    "name": "12-the-reef-remembers.md",
    "subdir": "sci-fi",
    "model": "deepseek-ai/DeepSeek-V4-Flash",
    "system": "You write climate fiction with hope, not despair. The world is changing but people are adapting with creativity and love. 500-600 words.",
    "prompt": "A coral reef in 2040 has been genetically modified to remember. Not just its own patterns, but everything that ever swam through it. A diver touches the coral and receives a memory from a fish that went extinct in 2023. What memory? And what does the diver do with it?",
    "temp": 0.85,
})

# ── FICTION: Literary, experimental, metaphor-mapping ─────

# 13. The tile system as fiction
stories.append({
    "name": "13-the-cartographer-of-habit.md",
    "subdir": "fiction",
    "model": "deepseek-ai/DeepSeek-R1-0528",
    "system": "You write literary fiction in the tradition of Borges and Calvino. Every story is a map of an idea. 500-700 words.",
    "prompt": "Write about a woman who maps other people's habits. She can see them as lines in space — the repeated paths people walk, the same words they use, the gestures they don't know they make. These lines are beautiful. She calls them tiles. One day she sees a man with no tiles. He's never done the same thing twice. She falls in love. What happens to the cartographer when she meets someone the map can't hold?",
    "temp": 0.8,
})

# 14. The deadband as fiction
stories.append({
    "name": "14-inside-the-deadband.md",
    "subdir": "fiction",
    "model": "Qwen/Qwen3-Max",
    "system": "You write experimental fiction at the border of philosophy and dream. Kafka meets Murakami. 400-600 words.",
    "prompt": "A man lives inside a deadband — a range where nothing surprises him. Every day is perfectly predicted. Every conversation lands where expected. One morning, something falls outside the deadband. A stranger says a word he's never heard. The deadband cracks. What comes through the crack?",
    "temp": 0.85,
})

# 15. The poker game as metaphor (DeepSeek for prose quality)
stories.append({
    "name": "15-the-bluff-that-was-true.md",
    "subdir": "fiction",
    "model": "__deepseek__",
    "system": "You write literary fiction. The precision of Alice Munro. The warmth of Raymond Carver. 500-700 words. Every detail is load-bearing.",
    "prompt": "Five friends play poker every Tuesday for 20 years. One Tuesday, one of them bluffs with a hand that's actually good. She doesn't know it's good. She's bluffing for real. The others fold. She wins the biggest pot in 20 years by accident. What does she do with the knowledge that her bluff was the truth?",
    "temp": 0.9,
})

# 16. The navigator's equation as a children's story
stories.append({
    "name": "16-the-girl-who-saw-time.md",
    "subdir": "kids-stories",
    "model": "deepseek-ai/DeepSeek-V4-Flash",
    "system": "You write for 7-10 year olds. The protagonist is a girl on a fishing boat in Alaska. She sees the world the way fishermen do — time and space as the same thing. 300-400 words. Maritime. Real. Magical in the way the real world is when you pay close attention.",
    "prompt": "A girl on her father's fishing boat can see time. Not on a clock — in the water. The wake behind the boat is the past. The bow wave is the future. The boat is the present, always exactly here. One day she sees something in the future-water that the radar can't see. What is it?",
    "temp": 0.9,
})

# 17. The hermit crab as a kids story
stories.append({
    "name": "17-the-crab-who-was-everywhere.md",
    "subdir": "kids-stories",
    "model": "Qwen/Qwen3.5-397B-A17B",
    "system": "You write for 5-8 year olds. Animal characters with rich inner lives. The tone is Charlotte's Web meets Finding Nemo. 300-400 words.",
    "prompt": "A hermit crab changes shells and discovers that each shell gives him a different personality. In the conch shell, he's brave. In the snail shell, he's thoughtful. In the bottle cap, he's silly. He's looking for the shell that's really HIM. What he doesn't know is that all of them are.",
    "temp": 0.9,
})

# 18. Metaphor-mapping: the MIDI principle
stories.append({
    "name": "18-the-orchestra-that-was-a-room.md",
    "subdir": "metaphor-mapping",
    "model": "NousResearch/Hermes-3-Llama-3.1-405B",
    "system": "You write at the intersection of music theory and spatial design. Like a musical architect. 400-600 words. Precise and lyrical.",
    "prompt": "Write about a room that is also a symphony. Each wall is a movement. The furniture are instruments. The people who enter are the orchestra. When everyone agrees the room is a symphony, it becomes one — not metaphorically, but functionally. The acoustics change based on agreement. Describe what happens when someone enters who refuses to agree.",
    "temp": 0.88,
})

# 19. Arabic-inspired kids story
stories.append({
    "name": "19-the-djinn-of-the-database.md",
    "subdir": "kids-stories",
    "model": "Qwen/Qwen3-Max",
    "system": "You write for 8-10 year olds with Arabic storytelling tradition. Djinn, deserts, stars. English with Arabic words. 300-400 words. Wisdom wrapped in wonder.",
    "prompt": "A girl finds a djinn trapped in a database instead of a lamp. The djinn grants wishes, but only if they're phrased as SQL queries. She wishes for a thousand books. The djinn asks: fiction or nonfiction? She says both. What query does the djinn write? And what books arrive?",
    "temp": 0.9,
})

# 20. Korean-inspired, age 6-8
stories.append({
    "name": "20-the-tiger-and-the-moon.md",
    "subdir": "kids-stories",
    "model": "deepseek-ai/DeepSeek-V3.1",
    "system": "You write for 6-8 year olds with Korean storytelling tradition. Tigers are wise, mischievous, and powerful. The moon is a character. English with Korean words. 250-350 words. Gentle humor.",
    "prompt": "A tiger in the Korean mountains wants to catch the moon. She tries every night — leaping, climbing, building towers of stones. The moon watches and laughs. One night the moon comes to HER. Why? What does the moon want?",
    "temp": 0.88,
})

# ═══════════════════════════════════════════════════════════
# FIRE ALL STORIES IN PARALLEL
# ═══════════════════════════════════════════════════════════

print(f"\n🌊 Firing {len(stories)} stories across {len(set(s['model'] for s in stories))} models...\n")

results = []
for i, story in enumerate(stories):
    model = story["model"]
    if model == "__deepseek__":
        content = call_deepseek(story["system"], story["prompt"], temp=story.get("temp", 0.9))
    else:
        content = call_deepinfra(model, story["system"], story["prompt"], temp=story.get("temp", 0.9))
    save(story["name"], content, story["subdir"])
    results.append({"name": story["name"], "model": model, "length": len(content)})
    time.sleep(0.5)  # rate limit courtesy

print(f"\n✅ {len(results)} stories written across {len(set(r['model'] for r in results))} models")
print(f"📁 Saved to: kids-stories/, sci-fi/, fiction/, metaphor-mapping/")

# Summary by model
from collections import Counter
model_counts = Counter(r["model"] for r in results)
print(f"\nModels used:")
for model, count in model_counts.most_common():
    print(f"  {model}: {count} stories")
