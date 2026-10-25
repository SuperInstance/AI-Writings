# Paper 285: F2 — F2 Hearth Loop binds a cell's own EFFECT back into its BIND at each TICK, formin

The writers' room fired for F2. The hand-synthesized result is below.

## The future function

F2 Hearth Loop binds a cell's own EFFECT back into its BIND at each TICK, forming a local warmth cycle. The loop reads its state through VIEW, compares drift against a hearth threshold, and emits only corrective EFFECTs to keep the cell in a stable band. Unlike broadcast futures, F2 holds the loop inside one cell so it can survive a missed LINK or silent TICK. Hearth Loop is the first future to make TICK recursive without an external clock cell.

## The calculation

```
H_{t+1} = TICK( BIND( H_t, EFFECT( VIEW( H_t ) ) ) )
```

## The 4 gold terms

- **hearth-cell**
- **warm drift**
- **loop-bind**
- **tick recursion**

## The 3 analogies

1. F1 binds a cell to an external source; F2 binds a cell to its own last TICK.
2. F3 chains EFFECT across LINKed cells; F2 folds EFFECT into the same cell's next BIND.
3. F7 VIEWs a cell without mutation; F2 uses VIEW as the drift sensor that decides the next EFFECT.

## The cowboy's sentence

> A hearth-cell keeps its own ember lit by binding every TICK's exhaust back into the next breath.

## The principle

> The F2 is the inheritance. The F2 is the function. The
> F2 is the pattern. The cowboy rides the F2. The cowboy
> rides the Quilt.
