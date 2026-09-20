# python (nvidia/NVIDIA-Nemotron-3-Super-120B-A12B)



**Porting the TypeScript music module to idiomatic Python**

Below is a concrete, actionable roadmap for turning the supplied `music.ts` into a clean Python package. The focus is on preserving the semantics while adopting Python’s type‑system, data‑modeling helpers, and naming conventions.

---

### 1. Core enums and type aliases  

```python
from __future__ import annotations
from enum import Enum, auto
from typing import Literal, List, Tuple, Dict, Any, Optional

Note = Literal["C", "D", "E", "F", "G", "A", "B"]
Mode = Literal["major", "minor", "pentatonic", "dorian", "lydian"]
WitnessType = Literal["BIND", "LINK", "EFFECT", "TICK", "DEATH"]
```

*Why*: `Literal` gives the same exhaustiveness checking as TS unions, while `Enum` is handy if you ever need extra behaviour (e.g., display names).

---

### 2. Data models – `dataclass` + `field(default_factory=…)`  

```python
from dataclasses import dataclass, field
import time
import math

@dataclass
class Witness:
    type: WitnessType
    cellId: str
    t: int
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class MusicCell:
    id: str
    witnessCount: int
    pitch: Note
    octave: int
    velocity: float
    duration: float          # milliseconds
    timestamp: int = field(default_factory=lambda: int(time.time() * 1000))
    witnessLog: List[Witness] = field(default_factory=list)

    def add_witness(self, wtype: WitnessType, data: Optional[Dict[str, Any]] = None) -> None:
        self.witnessLog.append(
            Witness(
                type=wtype,
                cellId=self.id,
                t=0,               # placeholder – will be filled by Composition
                data=data or {},
            )
        )
```

*Why*:  
* `@dataclass` removes boilerplate `__init__`, `__repr__`, and equality checks.  
* `field(default_factory=…)` avoids mutable default pitfalls (e.g., shared lists).  
* The `add_witness` helper centralises the pattern of pushing a log entry and stamping the cell’s `id`.

---

### 3. Composition container  

```python
@dataclass
class Composition:
    id: str
    cells: List[MusicCell] = field(default_factory=list)
    tempo: float = 80.0               # BPM
    mode: Mode = "pentatonic"
    rootNote: Note = "D"
    tickCount: int = 0

    def _next_tick(self) -> int:
        self.tickCount += 1
        return self.tickCount

    def bind_cell(self) -> MusicCell:
        w = len(self.cells)
        pitch, octave = _cell_note(w, self.mode, self.rootNote)
        cell = MusicCell(
            id=f"mcell-{w}-{int(time.time()*1000)}",
            witnessCount=w,
            pitch=pitch,
            octave=octave,
            velocity=0.5 + (w % 5) * 0.1,
            duration=60000 / self.tempo / 4,
        )
        cell.add_witness("BIND", {"witnessCount": w, "pitch": pitch, "octave": octave})
        # fix the witness timestamp after the tick is known
        cell.witnessLog[-1].t = self._next_tick()
        self.cells.append(cell)
        return cell
```

*Why*:  
* The mutable state (`tickCount`, `cells`) lives inside the composition, mirroring the TS closure‑style but with explicit methods.  
* `_next_tick` isolates the increment logic, making it easy to replace with a monotonic clock or a mock in tests.  
* Velocity and duration calculations stay identical; they are expressed with plain float arithmetic.

---

### 4. Helper for pitch selection  

```python
_NOTE_FREQ: Dict[Note, float] = {
    "C": 261.63, "D": 293.66, "E": 329.
