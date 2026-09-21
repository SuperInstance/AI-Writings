# QA Report — MUD Terminal Navigation Bug

**Date:** 2026-08-08  
**Tester:** Bug-fixer Agent  
**Component:** Plato's Shell — MUD Terminal (`mud-terminal.html`)  
**Prototype:** ScummVM MUD Terminal Prototype

---

## Bug: Room State Stuck on Aft Deck

**Severity:** Critical — Blocks all navigation after first room transition

### Summary

After navigating from `bar-rail` to `aft-deck` (via `go aft`), the player cannot navigate further. The `go` command fails for all other exits, effectively soft-locking the game.

### Root Cause

The `aft-deck` room definition used non-directional exit keys that didn't match what the parser expected or what the design spec required.

**Original (broken) exit mapping for `aft-deck`:**
```js
exits: {
  bar: { target: 'bar-rail', label: 'THE TAP' },
  wheelhouse: { target: 'wheelhouse', label: 'WHEELHOUSE' },
  below: { target: 'engine-room', label: 'ENGINE ROOM' }
}
```

The command parser matches exit keys using `k.startsWith(args)`:
```js
const exitKey = Object.keys(room.exits).find(k =>
  k.startsWith(args) || room.exits[k].label.toLowerCase().includes(args)
);
```

When the player types `go forward_up` or `go west` or `go forward`, none of these match the keys `bar`, `wheelhouse`, or `below` via `startsWith`. The player also can't type `go wheelhouse` to get to the wheelhouse because... actually that *would* have worked via `startsWith`, but the design spec calls for directional commands (`forward_up`), not room-name commands. The key issue is that `go west`, `go forward`, and `go forward_up` all fail silently.

This left the player stranded on the Aft Deck after arriving from the Bar Rail.

### Fix

Changed `aft-deck` exits to use proper directional keys matching the design spec:

```js
exits: {
  west: { target: 'bar-rail', label: 'THE TAP' },
  forward: { target: 'bar-rail', label: 'THE TAP' },
  forward_up: { target: 'wheelhouse', label: 'WHEELHOUSE' },
  below: { target: 'engine-room', label: 'ENGINE ROOM' }
}
```

Also updated the room description to reference the correct direction names: *"Doors lead to the bar (west), the wheelhouse (forward and up), and the engine room (below)."*

### Verification — Full Circuit Test

All six required navigation routes verified:

| Route | Command | Status |
|-------|---------|--------|
| bar-rail → aft-deck | `go aft` | ✅ |
| aft-deck → wheelhouse | `go forward_up` | ✅ |
| wheelhouse → galley | `go down` | ✅ |
| galley → wheelhouse | `go up` | ✅ |
| wheelhouse → aft-deck | `go aft` | ✅ |
| aft-deck → bar-rail | `go west` or `go forward` | ✅ |

**Ambiguity note:** `go forward` could match both `forward` and `forward_up` via `startsWith`. Insertion order ensures `forward` (→ bar-rail) is checked first, so the correct destination is selected. `go forward_u` or `go forward_up` disambiguates to the wheelhouse.

### Other Rooms — No Issues Found

- **bar-rail**: Single exit `aft → aft-deck`. Works correctly.
- **wheelhouse**: Exits `aft → aft-deck`, `down → galley`. Both work.
- **galley**: Exits `up → wheelhouse`, `aft → aft-deck`. Both work.
- **engine-room**: Single exit `up → aft-deck`. Works correctly.

### Split-View

The split-view (`split-view.html`) loads `mud-terminal.html` in an iframe. The fix propagates automatically. The split-view's own `ROOM_NAMES` and `ROOM_ID_MAP` already included all five rooms. No changes needed.

---

## Additional Findings (Non-blocking)

1. **Galley has an undocumented exit to aft-deck.** The `galley` room has `aft → aft-deck` which isn't mentioned in the original task's required routes but makes sense spatially. Verified working.

2. **Engine room exists and is reachable** via `go below` from aft-deck, though it's not part of the main circuit. The split-view's `ROOM_ID_MAP` maps `engine-room` to `aft-deck` as a fallback (engine room not yet in the ScummVM visual view).

3. **Click-to-navigate** (exit links) works correctly after the fix — the clickable exit links use the exit keys as `data-exit` attributes and pass them directly to `goToRoom()`.

---

## Conclusion

**Bug status:** Fixed and deployed.  
**Root cause:** Mismatched exit key names in `aft-deck` room definition — keys used semantic names (`bar`, `wheelhouse`) instead of directional commands (`west`, `forward`, `forward_up`) that the parser's `startsWith` matcher expects.  
**Fix:** Updated exit keys to directional names matching the design spec.  
**Verified:** Full circuit navigation works in all directions.
