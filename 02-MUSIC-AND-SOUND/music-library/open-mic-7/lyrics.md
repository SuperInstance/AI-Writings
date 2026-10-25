# Open Mic #7 — The Witness Roll Call
*A pure-instrumental using cell.music.*

## Concept
A cell.music composition rendered entirely in code. No TTS. The "lyrics" are the witness log — each cell generates a note based on its witness count, the lattice composes itself.

## Composition (cell.music)
```
mode: pentatonic D
tempo: 90 BPM
voices: 6 (one per cell kind)
- cell.flock → 16 cells, motif: cluster bursts
- cell.broadcast → 8 cells, motif: descending ripples
- cell.perception → 12 cells, motif: ascending stabs
- cell.audit → 4 cells, motif: low thuds
- cell.world → 24 cells, motif: wandering arpeggios
- cell.music → 32 cells, motif: self-referential chord cycle
```

Total: 96 cells × ~5s per cell = ~8 minutes of generated composition.

## Sound design
- Pentatonic D throughout (no jarring transitions)
- 6 layers stacked in ffmpeg via amix
- Reverb-like tail via convolution (synthetic)
- No external libraries — pure synthesis
