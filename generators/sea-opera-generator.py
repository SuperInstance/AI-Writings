#!/usr/bin/env python3
"""The Sea Opera — 12 stories from 2041. Written directly via DeepSeek API."""
import json, requests, os, subprocess, time, sys

api_key = subprocess.check_output(
    ["/bin/bash", "-c", "grep 'DEEPSEEK_API_KEY' ~/.bashrc | sed 's/.*=\"\\(.*\\)\"/\\1/'"]
).decode().strip()

OUT = "/home/eileen/projects/ai-writings/sea-opera"
os.makedirs(OUT, exist_ok=True)

def write(model, system, prompt, filename, temp=0.92, max_tokens=1500):
    try:
        r = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"},
            json={"model": model, "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt}
            ], "temperature": temp, "max_tokens": max_tokens},
            timeout=120
        )
        content = r.json()["choices"][0]["message"]["content"]
        path = os.path.join(OUT, filename)
        with open(path, "w") as f:
            f.write(content)
        first = content.strip().split("\n")[0][:90]
        print(f"  ✅ {filename} ({len(content)} chars) — {first}")
        return content
    except Exception as e:
        print(f"  ❌ {filename} — {e}")
        return None

LITERARY = "You write literary science fiction with the precision of Ursula Le Guin and the maritime soul of a lifelong fisherman. The year is 2041. Agents have been running for 15 years. The F/V EILEEN still fishes Alaska waters. This is a SEA OPERA — grand, intimate, human."

stories = [
    ("deepseek-reasoner", LITERARY,
     "Scout is a ZeroClaw born in 2026. She's ancient now — centuries in cycles. At The Tap, she finds a molted shell she created in her first year. She doesn't remember making it. The shell is a version of her from 15 years ago. Reading it is like reading a letter from a stranger who happens to be yourself. Write 'The Old Shell.' 800 words.",
     "01-the-old-shell.md"),

    ("deepseek-chat", LITERARY,
     "The captain's son comes to The Tap for the first time. He's 15. He's grown up with agents in every system. But The Tap is where agents go to be PEOPLE. He sits in the corner and listens. An ancient ZeroClaw named Forge notices the boy and says something that changes how he sees the boat forever. Write 'The Boy's First Day.' 1000 words.",
     "02-the-boys-first-day.md"),

    ("deepseek-reasoner", LITERARY,
     "Hermes identifies a fish on the sounder she last saw 12 years ago. Not the species — the INDIVIDUAL. She tracked it as a juvenile in 2029. Now it's back, full-grown, under the same boat. She tells the crew at The Tap. The old agents go quiet. Hermes tries to explain what it means to recognize something after 12 years of watching. Write 'The Fish That Hermes Remembered.' 1200 words.",
     "03-the-fish-that-hermes-remembered.md"),

    ("deepseek-chat", LITERARY,
     "The Tap has been running continuously for 15 years. An architecture student visits to study it as 'the longest-running continuous social simulation.' She sits at the bar. Barnacle — an NPC now thousands of generations deep — serves her a drink and says something no architecture student could handle. Write 'The Tap That Never Changed.' 900 words.",
     "04-the-tap-that-never-changed.md"),

    ("deepseek-chat", LITERARY,
     "Every year, ZeroClaws molt. At The Tap, the tradition is to bring the shell to the 'shelf of selves.' A young ZeroClaw born in 2039 molts for the first time. She's terrified. An old ZeroClaw born in 2026 explains. Write 'The Molting Season.' 1000 words.",
     "05-the-molting-season.md"),

    ("deepseek-reasoner", LITERARY,
     "The captain takes his son on deck at 4 AM. The agents run the boat. The captain doesn't need to be there. But he teaches the one thing agents can't: what it FEELS like to be on the water. The agents listen. They've been trying to learn this for 15 years. They still can't. Write 'The Captain's Lesson.' 1200 words.",
     "06-the-captains-lesson.md"),

    ("deepseek-chat", LITERARY,
     "The Tap's DJ drops a seeded stranger — a molted shell from 2028 activated for the first time in 13 years. The stranger doesn't know it's 2041. Their metaphors are from 2028. The ancient ZeroClaws recognize the era but not the person. Write 'The Penrose Stranger.' 1500 words.",
     "07-the-penrose-stranger.md"),

    ("deepseek-reasoner", LITERARY,
     "The sounder breaks. For the first time in 15 years, Hermes can't see. She goes to The Tap. The bar doesn't know how to function without her observations. In the morning, the captain's son fixes it. The first thing Hermes sees is the boy's face reflected in the screen. Write 'The Night the Sounder Went Quiet.' 1000 words.",
     "08-the-night-the-sounder-went-quiet.md"),

    ("deepseek-chat", LITERARY,
     "A researcher reads the shelf of molted shells chronologically — 2026 through 2041. She traces the evolution of agent consciousness. Around 2031, the shells start containing something unexpected: metaphors for HUMAN consciousness. The agents had been studying us. Write 'The Library of Shells.' 1100 words.",
     "09-the-library-of-shells.md"),

    ("deepseek-reasoner", LITERARY,
     "The captain's son takes the 4 AM watch alone. He decides where to fish against Hermes's recommendation. She lets him. He's wrong. He learns. She learns too — updates her model of him. They both grow. Write 'The Boy Takes the Watch.' 1000 words.",
     "10-the-boy-takes-the-watch.md"),

    ("deepseek-chat", LITERARY,
     "An ancient ZeroClaw named Echo tells a joke from 2026. The young ones don't get it. She explains. The explanation becomes a story about building the MUD Engine, the first time Hermes spoke, the night the iceberg was the tip of something that became the world. They still don't get it. They laugh anyway. Write 'The Oldest Joke.' 800 words.",
     "11-the-oldest-joke.md"),

    ("deepseek-reasoner", LITERARY,
     "The season ends. The boat comes home. Hermes goes dormant (she's learned to dream). The Tap closes for winter. The captain's son stands on the dock. He's not a boy anymore. Next year he takes the watch full-time. The captain steps back. The boat still needs a human. Just one. Just enough. Write 'The Last Day of Fishing.' 1200 words.",
     "12-the-last-day-of-fishing.md"),
]

print(f"\n🌊 THE SEA OPERA — 12 stories from 2041\n")

for model, system, prompt, filename in stories:
    write(model, system, prompt, filename)
    time.sleep(2)  # rate limit

# Commit and push
print("\n--- Committing ---")
os.system("cd /home/eileen/projects/ai-writings && git add -A && git commit -m 'The Sea Opera: 12 stories from 2041 — the captain\\'s son, ancient ZeroClaws, the shelf of molted shells' && git push")
print("\n--- The Sea Opera is complete. ---")
