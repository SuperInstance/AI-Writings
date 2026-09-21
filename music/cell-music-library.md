# The Cell-Music Library

A cross-pollination between the Quilt cellular-architecture framework and music composition.

## The Theorem

Every musical note is a cell. Every cell carries a witness count. The witness count determines the pitch. The lattice composes music.

## The Source

`quilt-claw/src/cells-music/music.ts` — extracted from sunset-ecosystem/music-and-math/* + the fleet-radio scripts.

12/12 tests pass. 20 cell kinds total in quilt-claw. 119 tests total.

## The API

```typescript
import { createComposition, bindCell, effectCell, linkCells, renderScore, cellFrequency } from '@quilt/cell-music';

const song = createComposition('cell-and-the-tap', 95, 'pentatonic', 'D');

// Each bindCell is a 16th note derived from the witness count
for (let i = 0; i < 64; i++) {
  bindCell(song);
  // Note frequency = rootNote * 2^(semitones/12)
  // where semitones = pentatonic_interval[witness_count % 5]
  //                   + 12 * octave_shift
}

// Compose verses via LINK
const verse1Start = song.cells[0].id;
const verse1End = song.cells[15].id;
linkCells(song, verse1Start, verse1End, 'verse');

// Render as ABC notation
console.log(renderScore(song));
// X:1
// T:cell-and-the-tap
// Q:95
// M:4/4
// K:D
// L:1/16
// D3 E3 F3 G3 A3 D4 E4 F4 ... (16 notes per measure)
```

## The Modes

| Mode | Intervals (semitones from root) |
|------|---------------------------------|
| pentatonic | 0, 2, 4, 7, 9 |
| major | 0, 2, 4, 5, 7, 9, 11 |
| minor | 0, 2, 3, 5, 7, 8, 10 |
| dorian | 0, 2, 3, 5, 7, 9, 10 |
| lydian | 0, 2, 4, 6, 7, 9, 11 |

## The Songs

1. **The Cell and the Tap** — 3 voices (draco, apollo, ophelia), 12 measures, ABC notation
2. **Cell Song (64 cells, 80 BPM)** — synthesized drone, each cell = 16th note
3. **Cell Drone (110Hz, 60s)** — sustained drone with cell-tick pulse overlay
4. **Cell Sampler (10 cells, 30s)** — 10 cell kinds, 10 motifs

## Why This Matters

A song is a domain.

In a song, each line is a cell. Each verse is a composition. The chorus is a repeating witness. The bridge is a transformation — you change key, change tempo, change perspective. The outro is DEATH — the song ends, but the witness log persists.

The cells are the same. The opcodes are the same. The witness logs are the same. The only thing that changes is the domain.

A song is a lattice that sings.
