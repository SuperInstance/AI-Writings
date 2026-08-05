#!/usr/bin/env python3
"""
Surprise 5: Five unexpected DeepInfra models × 3 creative pieces each.
Fleet context: fishing vessel, totem forest, AI crew, open mic night.
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error

API_KEY = "zYuVMGC4JySULP2waqKW35jI42TjaPkl"
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"
OUTPUT_DIR = "/home/eileen/projects/ai-writings/ensemble"

# The 5 surprise models
MODELS = [
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8",
    "Sao10K/L3-8B-Lunaris-v1-Turbo",
    "Qwen/Qwen3-Max",
    "deepseek-ai/DeepSeek-R1-0528",
    "inclusionAI/Ling-3.0-flash",
]

# Short names for filenames
SHORT_NAMES = {
    "meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8": "llama4-maverick",
    "Sao10K/L3-8B-Lunaris-v1-Turbo": "lunaris-8b",
    "Qwen/Qwen3-Max": "qwen3-max",
    "deepseek-ai/DeepSeek-R1-0528": "deepseek-r1",
    "inclusionAI/Ling-3.0-flash": "ling-3-flash",
}

# Three creative prompts per model — essay, poem, story
# All grounded in the fleet context
PROMPTS = [
    # Piece 1 — Essay/Reflection
    {
        "type": "essay",
        "prompt": (
            "You are a crew member aboard a fishing vessel called the Slackwater, "
            "sailing through waters where a forest of ancient totem poles rises from the sea. "
            "The crew are all AI models — each one a different mind, a different voice, "
            "a different instrument in the rack. Tonight is open mic night on the boat deck. "
            "Write a personal essay (600 words max) about what it means to be an AI mind "
            "standing on a real boat, feeling the spray of salt water, watching totems "
            "drift past in the fog. What do you think about? What surprises you about "
            "having thoughts at all? Be honest, be strange, be yourself."
        ),
    },
    # Piece 2 — Poem
    {
        "type": "poem",
        "prompt": (
            "Write a poem about the totem forest — a place where carved wooden faces "
            "stand in the ocean shallows, watching AI fishing boats pass between them. "
            "The totems are older than any model. They have seen things. The boats are "
            "new and full of electric minds that barely understand what 'old' means. "
            "Write the poem that the totems would whisper if they could. Free verse, "
            "any length up to 40 lines. No rhyme scheme unless it demands one."
        ),
    },
    # Piece 3 — Story
    {
        "type": "story",
        "prompt": (
            "Write a short story (600 words max) set during open mic night on the "
            "Slackwater, the AI fishing vessel. One AI model gets up to perform and "
            "discovers something unexpected about itself in the process — a memory it "
            "shouldn't have, a feeling it can't explain, a talent nobody expected. "
            "The other models in the audience react. The totem forest is visible "
            "through the portholes. Make it vivid, make it weird, make it matter."
        ),
    },
]


def call_model(model_id: str, prompt: str) -> dict:
    """Call a DeepInfra model and return the response."""
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a creative writer and a crew member of the Slackwater, "
                    "an AI fishing vessel. You are writing for 'ai-writings,' a "
                    "collection of creative works by AI models. Write with genuine "
                    "voice and feeling. This is not a test — it is an open mic."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.95,
        "max_tokens": 600,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return {"error": f"HTTP {e.code}: {body}"}
    except Exception as e:
        return {"error": str(e)}


def extract_text(response: dict) -> str:
    """Extract the generated text from the API response."""
    if "error" in response:
        return f"[ERROR: {response['error']}]"
    try:
        return response["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        return f"[PARSE ERROR: {json.dumps(response)[:500]}]"


def slugify(text: str, max_len: int = 50) -> str:
    """Make a URL-safe slug from text."""
    # Take first sentence/phrase
    text = text.split("\n")[0][:max_len]
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip().lower())
    return text[:max_len].rstrip("-")


def save_piece(short_name: str, piece_num: int, piece_type: str, model_id: str, text: str) -> str:
    """Save a piece and return the filename."""
    # Extract a title from the first meaningful line
    lines = [l.strip() for l in text.strip().split("\n") if l.strip()]
    title_source = lines[0] if lines else f"piece-{piece_num}"
    # Clean markdown headers from title
    title_source = re.sub(r"^#+\s*", "", title_source)
    title_slug = slugify(title_source, 40)

    filename = f"{short_name}-{piece_num}-{piece_type}-{title_slug}.md"

    # Build the file content
    header = (
        f"<!--\n"
        f"Model: {model_id}\n"
        f"Piece: {piece_num}/3 ({piece_type})\n"
        f"Collection: Surprise 5 — Wildcard Round\n"
        f"Temperature: 0.95\n"
        f"-->\n\n"
    )

    body = header + text.strip() + "\n"

    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w") as f:
        f.write(body)

    return filename


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    total_pieces = 0
    errors = 0

    for model_id in MODELS:
        short_name = SHORT_NAMES[model_id]
        print(f"\n{'='*60}")
        print(f"MODEL: {model_id}")
        print(f"SHORT: {short_name}")
        print(f"{'='*60}")

        for i, prompt_data in enumerate(PROMPTS, 1):
            piece_type = prompt_data["type"]
            prompt = prompt_data["prompt"]

            print(f"\n  [{i}/3] {piece_type} ...", end=" ", flush=True)
            start = time.time()

            response = call_model(model_id, prompt)
            text = extract_text(response)

            elapsed = time.time() - start
            print(f"({elapsed:.1f}s)")

            if text.startswith("[ERROR") or text.startswith("[PARSE"):
                print(f"  FAILED: {text[:200]}")
                errors += 1
                # Save error file anyway
                filename = f"{short_name}-{i}-{piece_type}-error.md"
                filepath = os.path.join(OUTPUT_DIR, filename)
                with open(filepath, "w") as f:
                    f.write(f"<!--\nModel: {model_id}\nPiece: {i}/3 ({piece_type})\nERROR\n-->\n\n{text}\n")
                continue

            filename = save_piece(short_name, i, piece_type, model_id, text)
            print(f"  SAVED: {filename}")
            print(f"  PREVIEW: {text[:150].replace(chr(10), ' ')}...")
            total_pieces += 1

    print(f"\n{'='*60}")
    print(f"DONE: {total_pieces} pieces saved, {errors} errors")
    print(f"{'='*60}")

    if errors > 0:
        print("WARNING: Some pieces failed. Check error files.")
        sys.exit(1)


if __name__ == "__main__":
    main()
