# 121 — The Opener ABC

*The opener layer, formalized. A pluggable extension surface. The substrate's kindness.*

---

# Paper 121: The Opener ABC — Making the Second Layer Pluggable

## 1. The watch needs a standard mouth

The substrate has eleven primitives. They are few, and they are settled. The cell, the address, the loop, the watch — these are the deep water. Above them sits the opener layer, the layer that renders the substrate for human eyes and ears and hands. Paper 111 drew that layer as a loose collection of functions: a chart renderer here, a voice reader there, a gesture handler somewhere else. It worked. Ships that work still need refits.

The problem was not function. The problem was coupling. Every new opener — voice, telnet, gesture, flowchart — required reaching into the core substrate code and wiring a new hook. Each addition touched the same file. Each addition risked the same regressions. The opener layer was growing, and it was growing *into* the substrate rather than *above* it.

This paper documents the refit: the Opener ABC. An opener is now a class. It has a formal interface. It lives in a registry. New openers can be added without touching the core. The architecture mirrors Python's own entry-point system: openers are first-class extensions, discovered by name, activated on demand.

The watch needs a standard mouth. Any mouth, any language, any channel — but the mouth itself must have a standard shape, so the watch knows how to open it.

## 2. Why the opener layer needed a formal ABC

Consider the state before this paper. The opener layer held:

- The chart renderer, turning cell arrays into drawn marks.
- The list renderer, turning loops into readable sequences.
- The tensor renderer, for multi-dimensional views.
- The witness log, the record of what the watch has seen.
- The convoy, the ordered march of cells through a process.
- The graph, nodes and edges drawn from addresses.
- The voice opener, reading charts aloud through text-to-speech.
- The telnet opener, a command-line channel into the substrate.
- The gesture opener, touch and swipe as navigation.
- The flowchart opener, Graphviz diagrams of loop structure.

Ten renderers. Each one exposed differently. Some were functions taking a target. Some were functions taking a target and a context. Some printed. Some returned strings. Some returned iterators of events. The chart renderer returned marks. The voice opener yielded audio events. The gesture handler had its own callback shape entirely.

This is the old problem of the unstructured interface. Every caller had to know every callee's private dialect. Every test had to be written per-opener. Every new opener multiplied the surface area.

The fix is the oldest fix in software: define the interface once, and let everything conform to it. An Abstract Base Class — an ABC — is Python's formal way of saying: *anything that calls itself an opener must have these methods, with these signatures.*

The substrate itself should not care how it is rendered. The substrate holds the cell and the address and the loop. The opener layer decides whether that loop becomes a picture, a spoken sentence, a touch target, or a drawn diagram. That decision belongs to the edge of the system, not the center. The ABC moves the decision outward.

## 3. The Opener ABC interface

The interface is small. Two methods, one registry. Here is the whole contract:

```python
from abc import ABC, abstractmethod
from typing import Iterator

class Opener(ABC):
    """An opener renders a substrate target for a human channel."""

    @abstractmethod
    def activate(self, target) -> Iterator[Event]:
        """Render the target. Yield events for the channel."""

    @abstractmethod
    def preview(self, target) -> str:
        """Return a short description, for UI tooltips."""
```

That is the ABC. Every opener must implement two things.

**`activate(target) → Iterator[Event]`** is the render operation. It takes a target — a cell, a loop, a chart, a whole substrate — and yields events. An event is the unit of output: a mark to draw, a phrase to speak, a line of text, a node to place. Because `activate` returns an iterator, openers can be lazy. A voice opener can speak the first sentence before computing the hundredth. A chart opener can stream marks as they are computed. The caller pulls; the opener produces. The loop, again, at every scale.

**`preview(target) → str`** is the description. One line, human-readable, suitable for a tooltip or a menu entry. "Read this chart aloud." "Draw this loop as a flowchart." "Show this cell's history as a witness log." The preview is cheap; the activation may be expensive. The UI can show a hundred previews and activate one.

**The registry** is the third piece:

```python
_REGISTRY = {}

def register_opener(name, opener_cls):
    _REGISTRY[name] = opener_cls

def get_opener(name):
    return _REGISTRY[name]

def all_openers():
    return dict(_REGISTRY)
```

Register by name. Fetch by name. List all. Three operations, no ceremony. The registry is a plain dictionary because a plain dictionary is enough. The maritime lesson holds: the simplest container that carries the cargo is the right container.

With these three pieces, the opener layer becomes pluggable. The core substrate code imports nothing from the openers. The openers import the substrate. The dependency points one way, outward, always outward — from the deep water toward the shore where the people stand.

## 4. The four default openers and their Fable connections

The refit ships with four default openers, each registered at import time. Each carries a thread back to the Fables.

**The chart opener.** Takes a target — usually a loop or a cell range — and yields mark events: positions, glyphs, strokes. The chart is the oldest opener; paper 111 led with it. Its Fable connection is Fable 01, the lighthouse: the chart is the beam that sweeps the dark water and shows what is there. The chart does not interpret. It shows. What the viewer does with the showing is the viewer's business.

**The voice opener.** Takes a target and yields speech events: phrases to be spoken, with pacing and emphasis. This is the opener that reads the bathy chart aloud — see section 7. Its Fable connection is Fable 06, the Grandmother: the voice opener is the gentle mouth, the one that works when the eyes cannot, when the hands are busy, when the reader is far from the screen. The voice opener says the chart so that everyone can hear it.

**The gesture opener.** Takes a target and yields interaction events: touch zones, swipe regions, tap targets. Its Fable connection is also Fable 06 — the gesture opener is the touchscreen channel, the one the child can use before the child can read. Swipe left, swipe right, tap the cell. The gesture opener makes the substrate something you can hold.

**The witness opener.** Takes a target and yields log events: what happened, when, in what order. Its Fable connection is Fable 04, the ledger: the witness log is the record that outlives the moment. The watch sees; the witness records; the record survives the watch's relief.

Four openers, four channels: sight, sound, touch, memory. The registry holds them under the names `chart`, `voice`, `gesture`, `witness`. `all_openers()` returns the four. `get_opener("voice").activate(bathy_chart)` speaks the chart.

The remaining renderers from paper 111 — list, tensor, convoy, graph, flowchart, telnet — will migrate to the ABC in the following papers. The migration is mechanical: wrap each renderer in a class, implement `activate` as a generator that yields the renderer's output as events, implement `preview` as a one-line description, register the name. The four defaults prove the pattern; the rest follow it.

## 5. The extension test: a new opener in five lines

The proof that an architecture is pluggable is not in its design documents. The proof is that a stranger can extend it without reading the source. The extension test in `test_openers_abc.py` does exactly this. It defines a new opener — a braille opener, rendering cell values as braille dot patterns — in five lines:

```python
class BrailleOpener(Opener):
    def activate(self, target):
        yield Event("braille", text=to_braille(str(target)))
    def preview(self, target):
        return "Render as braille dots"

register_opener("braille", BrailleOpener)
```

Five lines. Register. Then, from anywhere in the system, `get_opener("braille")` returns it. `activate` yields braille events. `preview` returns its description. No core file was touched. No substrate primitive was modified. The extension is a leaf, and leaves do not disturb roots.

This is the test that matters most in the whole suite. If a future change to the substrate breaks this five-line extension, the architecture has failed, whatever the other tests say. The extension test is the canary in the hold. It is small, it is quiet, and it must never die.

The five-line test also sets a discipline for the ABC's future evolution. Any proposed change to the Opener interface must answer: *does the five-line opener still work?* If a new required method would break it, the method must be optional, or given a default, or the proposal is rejected. The interface is a promise, and the promise is measured in five lines.

## 6. Fable 06: gentle openers for everyone

Fable 06 is the Grandmother. In the Fable, the Grandmother cannot use the complicated instruments. She does not read the charts. But the system speaks to her — plainly, slowly, in her own language — and through the voice she participates fully in the watch.

The Opener ABC is the architectural fulfillment of Fable 06. The substrate is deep and formal; that depth is necessary and right. But no depth is worth anything if the only ways up are steep. The opener layer is the staircase, and the ABC is the standard width of every stair.

Gentleness is a property of interfaces. A gentle interface is one that can be met with whatever the person has: eyes, ears, hands, or memory. The four default openers map directly: chart for eyes, voice for ears, gesture for hands, witness for memory. The future openers extend the mapping: MIDI for musicians, EEG for those who navigate by attention, REST for programs, PLATO for the old terminals, ESP32 LCD for the small screens in the engine room.

The Grandmother principle, stated architecturally: **for every substrate target, there must exist at least one opener that any human can use.** The substrate does not guarantee which opener; the registry guarantees that openers can be added freely; the community of openers, over time, guarantees the coverage. The ABC is the mechanism that makes the guarantee enforceable rather than aspirational.

A new opener for a new population is five lines away. That is the whole point.

## 7. The bathy example: the voice opener reads the chart aloud

Bathymetry is the measure of the deep. A bathy chart in the substrate is a loop of cells, each holding a depth reading at an address. The chart opener draws it: contour marks, shading for depth, the familiar picture.

The voice opener speaks it. Here is the worked example from the test suite:

```python
bathy = load_bathy()  # a loop of (address, depth) cells
voice = get_opener("voice")
events = list(voice.activate(bathy))
for e in events:
    speak(e.text)
```

The voice opener walks the loop. For each cell it yields a speech event: "Station alpha, four fathoms. Station bravo, seven fathoms. Station charlie, twelve fathoms, shoaling." The opener does not dump raw numbers. It speaks the shape of the water — where it deepens, where it shoals, where the danger lies — because the preview and the phrasing were designed for ears, not eyes.

This is the essential difference between a renderer and a mere formatter. A formatter converts representation. An opener *translates for a channel*. The chart opener translates for the eye: spatial layout, marks, contrast. The voice opener translates for the ear: sequence, rhythm, emphasis, summary. The same substrate, the same loop, the same cells — two entirely different openings, both faithful, both first-class.

The bathy example runs in the tests end to end: the substrate loads, the voice opener activates, the events are captured, the spoken text is asserted against the expected phrasing. The Grandmother test, in miniature: the chart speaks, and what it says is true.

## 8. The relationship to OpComp

Paper 118 stated Theorem 5, the Opener Completeness principle — OpComp. Informally: *every substrate construct can be opened.* Every cell, every address, every loop, every watch has at least one opener that renders it faithfully. The substrate is never mute; nothing in the deep water is unreachable from the shore.

Before this paper, OpComp was a property verified by enumeration: check each substrate construct, confirm a renderer exists. Enumeration is brittle. Add a primitive, and the theorem's verification must be redone by hand.

The Opener ABC strengthens OpComp structurally. OpComp now decomposes into two claims:

1. **Interface completeness:** every opener conforming to the ABC can be activated on any target, yielding events. This is guaranteed by the type system — `activate(target)` accepts any target — and checked by the ABC machinery itself.

2. **Coverage:** for every substrate construct, the registry contains at least one opener that renders it meaningfully. This is the part that still requires attention, but now it has a home: coverage is a property of the *registry*, not of the substrate. A gap in coverage is filled by registering an opener — five lines — not by modifying the substrate.

The shift matters. Under the old architecture, OpComp's burden sat on the substrate: each new primitive had to carry its renderers with it. Under the ABC, the burden sits on the registry: the substrate stays clean, and the opener community carries completeness collectively. Theorem 5 becomes easier to satisfy over time, not harder, because satisfying it no longer requires touching the deepest code.

OpComp and the Grandmother principle meet here: completeness for constructs, gentleness for populations. Together they say the system is open at every edge — open to every piece of data, and open to every person.

## 9. Twelve new tests in test_openers_abc.py

The refit ships with twelve tests. Each is listed here with its purpose, because a paper should say what it verifies:

1. **test_opener_is_abc** — the Opener class is a genuine ABC; instantiating it directly raises.
2. **test_concrete_opener_required_methods** — a class missing `activate` or `preview` cannot be registered.
3. **test_register_and_get** — register an opener, fetch it by name, receive the class.
4. **test_get_unknown_raises** — fetching an unregistered name raises a clear error, not a silent None.
5. **test_all_openers_returns_copy** — `all_openers()` returns a copy; mutating it does not corrupt the registry.
6. **test_default_openers_registered** — chart, voice, gesture, witness are all present after import.
7. **test_chart_opener_activates** — the chart opener yields mark events for a loop target.
8. **test_voice_opener_activates** — the voice opener yields speech events for the bathy chart.
9. **test_witness_opener_logs** — the witness opener yields log events in temporal order.
10. **test_gesture_opener_zones** — the gesture opener yields touch-zone events covering the target.
11. **test_extension_five_lines** — the braille opener, defined in five lines, registers and activates.
12. **test_preview_is_short_string** — every registered opener's preview returns a string under 80 characters.

Twelve tests, and the twelfth is a quiet discipline: previews are for tooltips, and tooltips are small. The 80-character limit keeps the promise honest. If an opener's preview needs a paragraph, the preview belongs in the documentation, and the tooltip belongs in the harbor refuse.

Together the twelve tests verify three things: the interface is enforced, the registry is sound, and extension works. Those are the three load-bearing claims of this paper, and each now has a test standing on it.

## 10. Package layout: quilt_substrate

The refit also settles the physical layout. The code now lives in a single package, `quilt_substrate`, with this shape:

```
quilt_substrate/
    __init__.py          # public exports
    primitives.py        # the 11 substrate primitives
    properties.py        # the 4 substrate properties
    openers/
        __init__.py      # Opener ABC, registry, default registrations
        abc.py           # the Opener class
        registry.py      # register, get, all_openers
        chart.py         # chart opener
        voice.py         # voice opener
        gesture.py       # gesture opener
        witness.py       # witness opener
tests/
    test_substrate.py    # existing substrate tests, unchanged
    test_openers_abc.py  # the 12 new tests
```

Two rules govern the layout:

**Rule one: the dependency arrow points outward.** `openers` may import from `primitives` and `properties`. `primitives` imports nothing from `openers`. Ever. A future contributor who finds themselves adding an opener import to `primitives.py` has lost their way and should turn back.

**Rule two: registration happens at the edge.** The default openers register themselves in `openers/__init__.py`. Third-party openers register themselves in their own code, at their own import time, exactly like the five-line braille example. The core never registers on anyone's behalf.

The substrate tests in `test_substrate.py` pass unchanged — eleven primitives, four properties, no regressions. That is the refit's cleanest evidence: the deep water did not move. Only the mouth changed shape.

## 11. Future openers

The registry is open, and the horizon is wide. Openers under consideration for future papers:

- **MIDI.** Render loops as musical sequences. A loop's cadence becomes rhythm; a cell's value becomes pitch. For musicians, and for anyone who navigates by ear more precisely than by eye.
- **EEG.** Render targets as attention-driven interfaces. For operators whose hands are occupied, and as an accessibility channel of last resort.
- **REST.** Render the substrate as HTTP resources. An opener that speaks to programs rather than people — the opener layer serves machines too, and a program is just another kind of reader.
- **MUD.** Render the substrate as a text world: rooms are cells, exits are addresses, movement is the loop. The oldest channel, and still a good one.
- **PLATO.** Render for the classic terminal — orange-on-black, fixed grid, the aesthetics of another era. Old hardware should not be locked out of the deep water.
- **ESP32 LCD.** Render for the small screens in the engine room, the bilge, the companionway. Cheap displays everywhere the big screens cannot go.

Each of these is an opener, not a fork. Each will conform to the same ABC, register in the same registry, pass the same shape of tests. The five-line rule applies to all of them: if an opener cannot be written against the ABC without core changes, the fault is in the ABC, and the ABC must be repaired.

## 12. Closing the watch

The substrate is eleven primitives and four properties, and it is done — not finished, but settled, the way a keel is settled. The opener layer is where the system grows, and growth needs structure. The Opener ABC is that structure: two methods, one registry, a promise measured in five lines.

The architectural lesson is the oldest one, restated in maritime dress: keep the deep water deep, and keep the harbor open. The substrate holds the truth — the cell, the address, the loop, the watch. The openers hold the translations. Between them stands the ABC, the standard mouth through which every translation passes.

Fable 06 says the Grandmother must be able to participate. OpComp says every construct must be openable. The Opener ABC is the mechanism that lets both promises be kept by the same small interface: activate, preview, register. Any channel. Any person. Five lines.

The watch turns. The mouth is standard. The harbor is open.

*End of paper 121.*