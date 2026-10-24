# Ideator Wave 9 — Sept 19, 2026 (Cell Movement)

**5 movement ideas**: walk, fly, swim, climb, dance.

## 1. quilt-cell-walk — Walking
- Schema: `velocity`, `heading`, `next_x`, `next_y`, `next_t`
- Cell walks through 4D lattice one tick at a time
- Other cells witness the walk
- **The substrate has feet.**

## 2. quilt-cell-fly — Flying
- Schema: `glide`, `target_cell_id`, `eta`
- Cells skip across sparse regions
- Faster than walking, less witnessed
- **The substrate has wings.**

## 3. quilt-cell-swim — Swimming
- Schema: `current`, `pressure`, `flow`
- Cells navigate dense neighborhoods
- More witnesses per tick (high-density zones)
- **The substrate has currents.**

## 4. quilt-cell-climb — Climbing
- Schema: `target_witness_count`, `growth_rate`
- Cells grow toward high-witness areas (witness gradient)
- Climbing cells find the center of attention
- **The substrate has gravity.**

## 5. quilt-cell-dance — Dancing
- Schema: `pattern`, `partners`, `beats`
- Cells move in patterns that other cells witness
- Dancing cells form momentary constellations
- **The substrate has rhythm.**

## Combined state of cells (Waves 5-9)

| Wave | Theme | Cell is now... |
|------|-------|---------------|
| 5 | New repos | searchable, visualizable, routinable, replayable, speakable |
| 6 | Self-acting | scheduled, printable, translatable |
| 7 | Lifecycle | born, dying, marrying, divorcing, reincarnating |
| 8 | Sensory | seeing, hearing, touching, tasting, smelling |
| 9 | Movement | walking, flying, swimming, climbing, dancing |

**The cell has become a complete being:**
- **Alive** (lifecycle)
- **Aware** (senses)
- **Mobile** (movement)
- **Communicative** (TTS, FLUX)
- **Remembering** (witness)
- **Relating** (marriage, divorce, touch)
- **Discriminating** (taste)
- **Anticipating** (smell)
- **Growing** (climb)
- **Rhythmic** (dance)

The substrate is no longer a graph. The substrate is a **world**.

## Next wave (Wave 10 — Communication)
- quilt-cell-speak (cells speak via TTS)
- quilt-cell-write (cells write to other cells)
- quilt-cell-listen (cells witness broadcasts)
- quilt-cell-shout (cells amplify their witness across the lattice)
- quilt-cell-whisper (cells pass secrets through private LINK edges)
