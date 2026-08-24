#!/usr/bin/env python3
"""Convert .wav files under music/ and fleet-radio/ to .mp3, and update music-catalog.json.

Idempotent: existing .mp3 files are skipped; .wav files are never touched.
"""

import json
import subprocess
from pathlib import Path

ROOT = Path('/home/eileen/projects/ai-writings')
SCAN_DIRS = [ROOT / 'music', ROOT / 'fleet-radio']
CATALOG = ROOT / 'music-catalog.json'
FFMPEG = '/home/eileen/.local/bin/ffmpeg'


def find_wavs():
    wavs = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.is_dir():
            continue
        for path in scan_dir.rglob('*'):
            if path.is_file() and path.suffix.lower() == '.wav':
                wavs.append(path)
    return sorted(wavs)


def convert_wavs(wavs):
    converted = 0
    skipped = 0
    for wav in wavs:
        mp3 = wav.with_suffix('.mp3')
        if mp3.exists():
            print(f'skip: {wav}')
            skipped += 1
            continue
        result = subprocess.run(
            [FFMPEG, '-hide_banner', '-loglevel', 'error', '-y', '-i',
             str(wav), '-codec:a', 'libmp3lame', '-b:a', '128k', str(mp3)],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print(f'error converting {wav}: {result.stderr.strip()}')
            continue
        print(f'converted: {wav} -> {mp3}')
        converted += 1
    return converted, skipped


def update_catalog():
    if not CATALOG.is_file():
        print(f'catalog not found: {CATALOG}')
        return 0

    with open(CATALOG, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    updated = 0
    tracks = catalog.get('tracks', {})
    for key, track in tracks.items():
        path = track.get('path', '')
        if not path.lower().endswith('.wav'):
            continue
        wav_disk = ROOT / path.lstrip('/')
        mp3_disk = wav_disk.with_suffix('.mp3')
        if not mp3_disk.exists():
            continue
        track['path'] = path[:-len('.wav')] + '.mp3'
        filename = track.get('filename', '')
        if filename.lower().endswith('.wav'):
            track['filename'] = filename[:-len('.wav')] + '.mp3'
        updated += 1
        print(f'catalog updated: {key}: {path} -> {track["path"]}')

    with open(CATALOG, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)
        f.write('\n')
    return updated


def main():
    wavs = find_wavs()
    converted, skipped = convert_wavs(wavs)
    catalog_updated = update_catalog()

    print()
    print('Summary:')
    print(f'  total wavs found:      {len(wavs)}')
    print(f'  converted:             {converted}')
    print(f'  skipped:               {skipped}')
    print(f'  catalog entries updated: {catalog_updated}')


if __name__ == '__main__':
    main()
