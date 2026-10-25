# compact (ByteDance/Seed-2.0-mini)

This quilt cell music composition code is almost fully functional but has two critical blocking issues that prevent it from being a minimal correct build, plus minor cleanup opportunities to reduce redundancy.

First and most urgent: the `linkCells` function is truncated mid-implementation, cutting off at `comp.tickCoun` — this is the only immediate blocker to the code compiling. To complete this function for minimal correct behavior, you must finish the logic to add symmetric LINK witness entries to both connected cells, and fix a hidden double-tick increment bug. Here’s the minimal fixed implementation:
```ts
export function linkCells(comp: Composition, cellIdA: string, cellIdB: string, linkType: string): boolean {
  const a = comp.cells.find(c => c.id === cellIdA);
  const b = comp.cells.find(c => c.id === cellIdB);
  if (!a || !b) return false;
  // Capture single tick count to avoid breaking event sequencing
  const eventTick = comp.tickCount++;
  a.witnessLog.push({ type: 'LINK', cellId: cellIdA, t: eventTick, data: { to: cellIdB, linkType } });
  b.witnessLog.push({ type: 'LINK', cellId: cellIdB, t: eventTick, data: { from: cellIdA, linkType } });
  return true;
}
```
This fixes the original code’s oversight of only logging one side of the link, and ensures each witness event gets a unique, sequential `t` value.

Next, simplify the redundant interval logic in `cellNote`. The original code uses a long if/else chain to assign mode intervals, which can be centralized into a single typed record to cut down on boilerplate and make future mode updates easier. This is a cleanup step that preserves full functionality while making the code more compact:
```ts
const MODE_INTERVALS: Record<Mode, number[]> = {
  major: MAJOR_INTERVALS,
  minor: MINOR_INTERVALS,
  pentatonic: PENTATONIC_INTERVALS,
  dorian: [0, 2, 3, 5, 7, 9, 10],
  lydian: [0, 2, 4, 6, 7, 9, 11]
};
// Replace the if/else block with:
const intervals = MODE_INTERVALS[mode];
```

You can also clean up a minor unnecessary mutation in `bindCell`: the original code initializes the BIND witness log with an empty `cellId`, then overwrites it immediately. Simplify this to set the correct cell ID upfront, removing one extra line of code:
```ts
witnessLog: [{
  type: 'BIND',
  cellId: cell.id,
  t: comp.tickCount++,
  data: { witnessCount: w, pitch, octave }
}]
```

Finally, the original code’s default `rootNote` in `createComposition` is set to `'D'`, which is valid per the `NOTE_FREQUENCIES` map, so no changes are needed here for minimal correctness. The only required fixes to get a working, minimal build are completing the `linkCells` function and fixing the double tick increment bug, with the cleanup steps reducing code bloat without altering functionality. (Word count: 482)
