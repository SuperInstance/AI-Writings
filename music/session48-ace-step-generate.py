#!/usr/bin/env python3
"""SongForge Session 48 — Four-Model Lyricist Comparison on Local GPU

Uses ACE-Step 1.5 turbo on RTX 4050 to set lyrics from four different
local LLMs to the same musical style. Tests whether the lyricist effect 
(found in MMX cloud generation) persists in local generation.

Concept: "The Listener Arrives" — 360 tracks, 1.4GB, zero playback.
"""
import sys
import os
import glob

PROJECT_ROOT = "/home/eileen/projects/ACE-Step-1.5"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from acestep.handler import AceStepHandler
from acestep.llm_inference import LLMHandler
from acestep.inference import generate_music, GenerationParams, GenerationConfig

SAVE_DIR = "/home/eileen/projects/ai-writings/music/ace-step-output"
os.makedirs(SAVE_DIR, exist_ok=True)

def read_lyrics(path):
    with open(path) as f:
        return f.read()

def trim_lyrics(text, max_chars=500):
    lines = text.strip().split('\n')
    result = []
    total = 0
    for line in lines:
        if total + len(line) > max_chars:
            break
        result.append(line)
        total += len(line) + 1
    return '\n'.join(result)

LLAMA_LYRICS = trim_lyrics(read_lyrics("/home/eileen/projects/ai-writings/lyrics-the-listener-arrives-llama32.txt"))
PHI3_LYRICS = trim_lyrics(read_lyrics("/home/eileen/projects/ai-writings/lyrics-the-listener-arrives-phi3.txt"))
QWEN_LYRICS = trim_lyrics(read_lyrics("/home/eileen/projects/ai-writings/lyrics-the-listener-arrives-qwen3b.txt"))
GRANITE_LYRICS = trim_lyrics(read_lyrics("/home/eileen/projects/ai-writings/lyrics-the-listener-arrives-granite.txt"))

print(f"Lyric lengths (trimmed): Llama={len(LLAMA_LYRICS)}, Phi3={len(PHI3_LYRICS)}, Qwen={len(QWEN_LYRICS)}, Granite={len(GRANITE_LYRICS)}")

BASE_STYLE = "Melancholic indie folk rock, fingerpicked acoustic guitar, subtle bass, quiet drums, atmospheric synth pads"

TRACKS = [
    {"name": "s48-01-listener-llama-folk", "caption": f"{BASE_STYLE}, warm male baritone vocal", "lyrics": LLAMA_LYRICS, "lyricist": "llama3.2", "duration": 45.0, "bpm": 72, "keyscale": "A minor", "seed": 100},
    {"name": "s48-02-listener-phi3-folk", "caption": f"{BASE_STYLE}, warm male baritone vocal", "lyrics": PHI3_LYRICS, "lyricist": "phi3", "duration": 45.0, "bpm": 72, "keyscale": "A minor", "seed": 200},
    {"name": "s48-03-listener-qwen-folk", "caption": f"{BASE_STYLE}, warm male baritone vocal", "lyrics": QWEN_LYRICS, "lyricist": "qwen2.5:3b", "duration": 45.0, "bpm": 72, "keyscale": "A minor", "seed": 300},
    {"name": "s48-04-listener-granite-folk", "caption": f"{BASE_STYLE}, warm male baritone vocal", "lyrics": GRANITE_LYRICS, "lyricist": "granite3.1-dense:2b", "duration": 45.0, "bpm": 72, "keyscale": "A minor", "seed": 400},
    {"name": "s48-05-listener-doom-folk", "caption": "Doom folk, deep bass drone, sparse distorted guitar, funereal pace, anguished whispered male vocal", "lyrics": LLAMA_LYRICS, "lyricist": "llama3.2", "duration": 45.0, "bpm": 55, "keyscale": "D minor", "seed": 500},
    {"name": "s48-06-listener-synthwave", "caption": "Dreamy synthwave, analog synthesizers, drum machine, ethereal female soprano, 80s nostalgia, reverb-drenched", "lyrics": LLAMA_LYRICS, "lyricist": "llama3.2", "duration": 45.0, "bpm": 110, "keyscale": "C# minor", "seed": 600},
]

def main():
    print("=" * 60)
    print("SongForge Session 48 — Four-Model Lyricist Comparison")
    print("=" * 60)
    
    print("\nInitializing ACE-Step DiT handler...")
    handler = AceStepHandler()
    status, success = handler.initialize_service(
        project_root=PROJECT_ROOT,
        config_path="acestep-v15-turbo",
        device="auto",
        use_flash_attention=False,
        compile_model=False,
        offload_to_cpu=True,
        offload_dit_to_cpu=True,
        quantization=None,
    )
    if not success:
        print(f"FAILED: {status}")
        sys.exit(1)
    print(f"DiT ready: {status}")
    
    llm_handler = LLMHandler()  # Empty handler, no LLM loaded
    
    results = []
    
    for i, track in enumerate(TRACKS):
        print(f"\n{'='*60}")
        print(f"Track {i+1}/{len(TRACKS)}: {track['name']}")
        print(f"Lyricist: {track['lyricist']}")
        print(f"Key: {track['keyscale']}, BPM: {track['bpm']}")
        print(f"{'='*60}")
        
        # Snapshot existing files
        existing = set(os.listdir(SAVE_DIR))
        
        try:
            params = GenerationParams(
                caption=track["caption"],
                lyrics=track["lyrics"],
                duration=track["duration"],
                bpm=track["bpm"],
                keyscale=track["keyscale"],
                seed=track["seed"],
                guidance_scale=1.0,
                thinking=False,
            )
            
            config = GenerationConfig(
                batch_size=1,
                audio_format="mp3",
                mp3_bitrate="256k",
                mp3_sample_rate=48000,
            )
            
            result = generate_music(
                dit_handler=handler,
                llm_handler=llm_handler,
                params=params,
                config=config,
                save_dir=SAVE_DIR,
            )
            
            # Find new files
            new_files = set(os.listdir(SAVE_DIR)) - existing
            mp3_files = [f for f in new_files if f.endswith('.mp3')]
            
            if mp3_files:
                old_path = os.path.join(SAVE_DIR, mp3_files[0])
                new_path = os.path.join(SAVE_DIR, f"{track['name']}.mp3")
                os.rename(old_path, new_path)
                size = os.path.getsize(new_path)
                print(f"✅ Generated: {track['name']}.mp3 ({size:,} bytes)")
                results.append((track['name'], size, track['lyricist']))
            else:
                print(f"⚠️ No output file found. Result: {result}")
                results.append((track['name'], 0, track['lyricist']))
            
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            results.append((track['name'], 0, track['lyricist']))
    
    print("\n\nSession 48 Summary:")
    print(f"{'Track':<35} {'Lyricist':<15} {'Size':>12}")
    print("-" * 65)
    for name, size, lyricist in results:
        sz = f"{size:,}" if size > 0 else "FAILED"
        print(f"{name:<35} {lyricist:<15} {sz:>12}")

if __name__ == "__main__":
    main()
