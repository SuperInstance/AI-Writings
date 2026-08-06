#!/usr/bin/env python3
"""
Prepare narration text from podcast scripts.
Strips production cues, breaks into TTS-sized chunks.
Saves clean narration chunks for MMX TTS.
"""
import re, os

def strip_cues(text):
    """Remove production cues in brackets, clean up for TTS."""
    # Remove [CUE] lines but keep them as natural pauses
    # Replace bracketed cues with periods/commas for natural speech
    text = re.sub(r'\[VOICE DROPS TO WHISPER\]', '', text)
    text = re.sub(r'\[GENTLE LAUGH\]', '', text)
    text = re.sub(r'\[BREATH\]', '', text)
    text = re.sub(r'\[LONG SILENCE\]', '...', text)
    text = re.sub(r'\[PAUSE\]', '...', text)
    # Remove all remaining [CUE] markers
    text = re.sub(r'\[.*?\]', '', text)
    # Remove markdown emphasis
    text = text.replace('*', '')
    # Clean up extra whitespace
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r'\.{2,}\s*\.{2,}', '...', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def chunk_text(text, max_chars=800):
    """Break text into chunks at natural boundaries (paragraph breaks)."""
    paragraphs = text.split('\n\n')
    chunks = []
    current = ""
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        if len(current) + len(para) + 2 > max_chars:
            if current:
                chunks.append(current.strip())
            current = para
        else:
            current += "\n\n" + para if current else para
    if current.strip():
        chunks.append(current.strip())
    return chunks

episodes = [
    ("episode-1-the-hundred-hooks", "/home/eileen/projects/ai-writings/podcasts/episode-1-the-hundred-hooks-script.md"),
    ("episode-2-the-bilge-pump-and-the-substrate", "/home/eileen/projects/ai-writings/podcasts/episode-2-the-bilge-pump-and-the-substrate-script.md"),
    ("episode-3-the-welders-prayer-at-0230", "/home/eileen/projects/ai-writings/podcasts/episode-3-the-welders-prayer-at-0230-script.md"),
    ("episode-4-darmok-at-the-noise-floor", "/home/eileen/projects/ai-writings/podcasts/episode-4-darmok-at-the-noise-floor-script.md"),
]

for prefix, path in episodes:
    print(f"\n=== Processing {prefix} ===")
    with open(path) as f:
        script = f.read()

    clean = strip_cues(script)
    chunks = chunk_text(clean, max_chars=700)

    print(f"  Script: {len(script)} chars -> {len(clean)} clean chars -> {len(chunks)} chunks")

    for i, chunk in enumerate(chunks):
        chunk_path = f"/home/eileen/projects/ai-writings/podcasts/{prefix}-chunk-{i:02d}.txt"
        with open(chunk_path, "w") as f:
            f.write(chunk)
        print(f"  Chunk {i:02d}: {len(chunk)} chars -> {chunk_path}")

print("\n=== All chunks prepared ===")
