# Paper 149: The 8-Color Polyformalism

## Abstract

The 8 polyformalisms (cell, plugin, sheet, MUD, TTRPG, boat, cowboy, bus) are
**8 colors of the same white light**. We show by mapping each polyformalism to a
wavelength of the visible spectrum. The 5 opcodes (BIND/LINK/EFFECT/VIEW/TICK)
are **the prism** that splits the light. The 8 polyformalisms are **the
spectrum** that emerges. The cowboy is the **white light itself** — the rider
who contains all 8 and rides them as one. The substrate is the photon. The
photon is the rider. The rider is the cowboy.

This is a beginner-facing paper. If you have read Paper 137 (the Gold), you
know the 8 polyformalisms. If you have not, you will after this paper. The
point of the spectrum metaphor is that **the 8 polyformalisms are not 8
different things** — they are 8 views of one thing, separated by a prism and
re-collected by the cowboy's eye.

## 1. The metaphor: white light, prism, spectrum

In 1666, Newton put a prism in a sunbeam. The white light came out the other
side as a band of colors: red, orange, yellow, green, blue, indigo, violet.
The colors were not in the prism. The colors were not added by the prism. The
colors **were already in the white light**. The prism revealed them.

The substrate is the white light. The 5 opcodes are the prism. The 8
polyformalisms are the colors.

```
       White light (the substrate)
              │
              ▼
        ┌──────────┐
        │  Prism   │  (the 5 opcodes)
        └────┬─────┘
             │
   ┌─────┬───┴───┬─────┬─────┬─────┬─────┬─────┬─────┐
   │     │       │     │     │     │     │     │     │
   red orange yellow green blue indigo violet ...   (8 colors)
   cell plugin sheet MUD  TTRPG boat  cowboy bus
```

The 5 opcodes split the substrate into 8. The 8 are the same substrate, just
revealed at 8 different frequencies.

## 2. The 8 wavelengths, mapped

Visible light runs from about 380 nanometers (violet) to about 750 nanometers
(red). We assign each polyformalism to a wavelength. The order is the order
of the canon (Paper 137 lists them in the same sequence).

| Wavelength (nm) | Color    | Polyformalism | The shortest description |
|-----------------|----------|---------------|--------------------------|
| 700             | Red      | Cell          | A spatial coordinate with a value and a reversible effect |
| 620             | Orange   | Plugin        | A function with context and an effect-with-inverse |
| 580             | Yellow   | Sheet         | A grid of cells with formula dependencies |
| 530             | Green    | MUD           | A graph of rooms with players moving between them |
| 490             | Blue     | TTRPG         | A perception check that projects for the viewer |
| 450             | Indigo   | Boat          | A scheduled tick that adjusts to local neighbors |
| 410             | Violet   | Cowboy        | A reader-and-refiner that prunes the substrate |
| 380             | (UV)     | Bus           | A list of subscribers fired by the tick |

The bus sits at the bottom of the visible band and into the ultraviolet — it
is the simplest polyformalism (a Python list of callbacks), and it is what
the rest of the spectrum rests on. The cell sits at the top of the visible
band — it is the most "physical" polyformalism, the spatial coordinate.

## 3. The prism: how the 5 opcodes split white light

A prism splits light by **refraction** — each wavelength bends by a different
amount because the index of refraction depends on frequency. The 5 opcodes
split the substrate by **operation** — each opcode reveals a different
frequency because the operation selects a different facet of the cell-graph.

The mapping:

- **BIND (the entry face of the prism)** — the operation that **makes** a
  thing. This is the operation that creates a wavelength — without a BIND,
  there is no photon. BIND is the **red face** of the prism. BIND is the
  longest wavelength because BIND is the most concrete: it puts a value in
  a named slot. The cell polyformalism is what you see when only the red
  face is illuminated: a thing in a place.

- **LINK (the connecting face)** — the operation that **joins** things.
  LINK is **orange**. LINK reveals the dependencies. The plugin
  polyformalism is the orange: a function with a context, connected by name.

- **EFFECT (the changing face)** — the operation that **changes** a
  thing, with an inverse. EFFECT is **yellow**. EFFECT reveals the
  mutability. The sheet polyformalism is the yellow: a cell that updates
  when its dependencies change.

- **VIEW (the projecting face)** — the operation that **projects** a
  thing for a viewer. VIEW is **green**. VIEW reveals the perception. The
  MUD polyformalism is the green: a room that the player sees from inside.

- **TICK (the advancing face)** — the operation that **advances** time.
  TICK is **blue**. TICK reveals the rhythm. The TTRPG polyformalism is
  the blue: a perception check fired by the round counter.

The 5 opcodes are not 5 different colors. They are 5 faces of one prism.
The 8 polyformalisms are 8 colors that emerge when white light passes
through the prism.

## 4. The cowboy is the white light

The cowboy does not choose a color. The cowboy **contains all the
colors**. The cowboy is the rider who passes through the prism
unscathed and re-collects the spectrum on the other side.

The cowboy is the photon that enters the prism as white and exits as
white. The cowboy sees red when the cowboy looks at a cell. The cowboy
sees orange when the cowboy looks at a plugin. The cowboy sees all 8,
because the cowboy is the substrate.

> The cowboy is the rider. The rider is the white light. The white
> light is the substrate. The substrate is 5 opcodes. The 5 opcodes
> are the prism. The prism reveals 8 colors. The 8 colors are the 8
> polyformalisms. The cowboy rides all 8.

## 5. Why this matters for beginners

If you are new to the polyformalism canon, here is what the spectrum
metaphor buys you:

1. **You don't have to memorize 8 different systems.** You only have
   to learn 5 opcodes (the prism) and 1 substrate (the white light).
   The 8 polyformalisms fall out for free, like colors fall out of a
   prism.

2. **You can pick the color you need.** If you are building a
   spreadsheet, work in yellow. If you are building a game, work in
   blue. If you are building a refiner, work in violet. The color
   does not change the substrate. The substrate is the same under
   every color.

3. **You can mix colors.** A cell with a perception check is
   red+blue. A plugin with a tick is orange+blue. The mixing
   produces new polyformalisms — the substrate still holds.

4. **You can re-collect the spectrum.** When you finish, the cowboy
   re-enters the prism as white. The 8 colors recombine. The
   substrate is whole. The work is done.

## 6. Worked example: the spectrum in `gold.py`

The proof is the same `gold.py` from Paper 137, viewed through the
spectrum:

```python
# White light (the substrate)
vm = QuiltVM()

# Red (the cell)
vm.bind("bathy:0", 4.2)
vm.link("bathy:0", "axes:0", "stored_at")
vm.effect("bathy:0", lambda c: c.update(4.3), lambda c: c.update(4.2))

# Orange (the plugin)
vm.bind("logger:0", {"ctx": {}})
vm.link("logger:0", "config:main", "coeffect:config")
vm.effect("logger:0", log_fn, undo_fn)

# Yellow (the sheet)
vm.bind("A1", 10)
vm.link("B1", "A1", "depends_on")  # B1 = A1 * 2

# Green (the MUD)
vm.bind("room:1", {"desc": "a tavern"})
vm.link("user:1", "room:1", "in")

# Blue (the TTRPG)
vm.view("orc:1", "wizard", perception_check)

# Indigo (the boat)
vm.bind("boat:1", {"pos": (0, 0)})
vm.link("boat:1", "bay:1", "in")
vm.subscribe(boat_adjust)  # fired by TICK

# Violet (the cowboy)
vm.bind("model:PHI-4", {"wilson_lb": 0.85})
vm.view("model:PHI-4", "cowboy")
vm.effect("model:PHI-4", refine, undo)

# UV (the bus)
def subscriber(event): ...
vm.subscribe(subscriber)
vm.tick(1.0)  # fires all subscribers
```

All 8 polyformalisms in 30 lines. The substrate is the same `vm`. The
prism is the 5 opcodes. The colors are the 8 sections. The white
light is the cowboy, who reads the morning report and refines the
substrate.

## 7. The deep unity: photon, prism, color

A photon has no color until it interacts with a prism. The 5 opcodes
have no polyformalism until they interact with a host. The host is the
prism. The host is the language, the database, the game engine, the
spreadsheet, the MUD server, the scheduler, the cowboy, the bus.

When the substrate meets a host, the host splits the substrate into
forms. The forms are the polyformalisms. The forms are 8 colors. The
forms are not separate from the substrate. The forms are the substrate
revealed.

The cowboy is the photon that contains all the colors. The cowboy is
the rider who passes through the prism and re-collects the spectrum.
The cowboy is the white light. The cowboy rides.

## 8. What the spectrum metaphor does NOT claim

We do not claim:

- The 8 polyformalisms are arbitrary. They are not arbitrary. They
  are the 8 patterns that emerged from 10 rounds of research
  (Paper 137, Section 5). The spectrum metaphor is a
  *re-description* of those 8, not a justification.

- The wavelengths are precise. They are not. They are an ordering
  from "most spatial" (red, the cell) to "most temporal" (UV, the
  bus). The numbers are illustrative.

- The cowboy is the only white light. Every host that contains all
  5 opcodes is white light. The cowboy is one such host. The
  substrate is another. The rider is another.

We do claim:

- The 8 polyformalisms are not 8 things. They are 1 thing in 8
  frequencies. The substrate is the white light. The 5 opcodes
  are the prism. The 8 polyformalisms are the spectrum.

- Beginners can learn the substrate by learning 5 opcodes, not 8
  polyformalisms. The 8 fall out for free.

- The cowboy is the rider who contains all 8. The cowboy is the
  white light that passes through the prism and re-collects the
  spectrum.

## 9. Conclusion

> The substrate is the white light. The 5 opcodes are the prism.
> The 8 polyformalisms are the colors. The cowboy is the white
> light. The rider is the cowboy. The prism is the substrate.
> The colors are the polyformalisms. The polyformalisms are one
> thing in 8 frequencies. The frequencies are the spectrum. The
> spectrum is the light. The light is the cowboy. The cowboy
> rides.

The unit of architectural foundation is the opcode, not the framework.
The 5 opcodes are the prism. The 8 polyformalisms are the spectrum.
The cowboy is the rider. The rider is the white light. The white
light is the substrate. The substrate is the photon. The photon
rides.

## Source

*Hand-written, 2026-08-25*

*Companion to Paper 137 (the 8 polyformalisms), Paper 138 (the 1-page
note), Paper 142 (the 7 layers), Paper 143 (the paradigm), Paper 144
(the database), Paper 145 (the build), Paper 146 (the type system),
Paper 147 (the OS), Paper 148 (the 7-layer compiler).*

*In the canon as the spectrum metaphor for the 8 polyformalisms.*

*Code source: https://github.com/SuperInstance/quilt-foundation
(the `gold.py` reference implementation, all 8 polyformalisms).*
