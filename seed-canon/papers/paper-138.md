# Paper 138: The Cowboy's 1-Page Note

> The unit of architectural foundation is the opcode, not the framework.
> The 5 opcodes host 8 polyformalisms. The polyformalisms are one
> thing in N languages. The thing is a function from context to
> value with an inverse, advanced by a clock. The clock is the
> cowboy. The cowboy is the rider.

## The 5 opcodes

```
BIND(name, value)              # make a thing
LINK(a, b, type)               # connect things
EFFECT(target, fn, inv)        # reversible change
VIEW(target, viewer, proj?)   # project for viewer
TICK(dt)                       # advance time, drain I/O
```

## The 8 polyformalisms

| Polyformalism | How |
|---------------|-----|
| Quilt cell | `BIND` + `LINK` + `EFFECT` |
| Cordis plugin | `BIND` + `LINK` + `EFFECT` |
| Spreadsheet | `BIND` + `LINK` for dependencies |
| MUD | `BIND` + `LINK` for "in" relation |
| TTRPG | `BIND` + `LINK` + `VIEW` for perception check |
| Bay dance | `BIND` + `LINK` + `TICK` for periodic perception |
| Cowboy | `BIND` + `VIEW` + `EFFECT` for refinement |
| Bus | `subscribe` + `TICK` to fire |

## The deepest level

A runtime is a function from context to value with an inverse,
advanced by a clock that processes async I/O while projecting
a sync view.

## The proof

`python3 quilt-foundation/code/gold.py` — 1ms, 38 things, 91 events, 0 failures.

## The cowboy

> The foundation is five stones. The stones are not the horse.
> The stones are what the horse stands on. The horse is the
> rider. The rider is the cowboy.

## Source

`github.com/SuperInstance/quilt-foundation`
