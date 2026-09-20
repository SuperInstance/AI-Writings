#!/usr/bin/env python3
"""
Full TTS production pipeline using Piper TTS (norman voice).
Generates narration for all chunks, concatenates into full episodes.
"""
import glob, os, wave, sys
from piper import PiperVoice

VOICE_MODEL = "/home/eileen/.local/share/piper-voices/en_US-norman-medium.onnx"
OUT_DIR = "/home/eileen/projects/ai-writings/podcasts"

# Load voice once
print("Loading Piper voice model (norman)...")
voice = PiperVoice.load(VOICE_MODEL)
print("Voice loaded.")

# Find all chunk files grouped by episode
episodes = {}
for chunk_file in sorted(glob.glob(f"{OUT_DIR}/episode-*-chunk-*.txt")):
    basename = os.path.basename(chunk_file)
    # Extract episode prefix (everything before -chunk-)
    prefix = basename.split("-chunk-")[0]
    if prefix not in episodes:
        episodes[prefix] = []
    episodes[prefix].append(chunk_file)

for prefix in sorted(episodes.keys()):
    chunks = sorted(episodes[prefix])
    print(f"\n=== {prefix} ({len(chunks)} chunks) ===")
    
    wav_files = []
    for i, chunk_file in enumerate(chunks):
        with open(chunk_file) as f:
            text = f.read().strip()
        
        if not text:
            continue
            
        wav_path = f"{OUT_DIR}/{prefix}-tts-{i:02d}.wav"
        print(f"  Chunk {i:02d}: {len(text)} chars -> {os.path.basename(wav_path)}")
        
        try:
            with wave.open(wav_path, 'wb') as wav_file:
                voice.synthesize_wav(text, wav_file)
            wav_files.append(wav_path)
        except Exception as e:
            print(f"    ERROR: {e}")
            continue
    
    # Concatenate all WAVs for this episode
    if wav_files:
        combined_path = f"{OUT_DIR}/{prefix}-narration-full.wav"
        print(f"  Concatenating {len(wav_files)} WAVs -> {os.path.basename(combined_path)}")
        
        # Read all WAV data and concatenate
        with wave.open(combined_path, 'wb') as out_wav:
            params_set = False
            for wav_path in wav_files:
                with wave.open(wav_path, 'rb') as in_wav:
                    if not params_set:
                        out_wav.setparams(in_wav.getparams())
                        params_set = True
                    frames = in_wav.readframes(in_wav.getnframes())
                    out_wav.writeframes(frames)
        
        size_mb = os.path.getsize(combined_path) / (1024*1024)
        print(f"  ✅ {os.path.basename(combined_path)} ({size_mb:.1f} MB)")

print("\n=== All narration generated ===")
