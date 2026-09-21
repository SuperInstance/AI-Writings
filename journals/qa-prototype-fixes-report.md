# QA Report: Split-View Sync Fixes — Plato's Shell Prototype

**Date:** 2026-08-08  
**Prototype:** scummvm-prototype (split-view.html, mud-terminal.html, index.html)  
**Deployment:** https://732a726a.scummvm-prototype.pages.dev  
**Commit:** `4154a88` — Fix split-view sync: bidirectional room navigation now works

---

## Bugs Found & Fixed

### BUG 1: Race Condition in pollScummRoom() — **Critical**

**Symptom:** When navigating from the MUD terminal (e.g., "go west"), the room change would sometimes revert back to the previous room, leaving the MUD terminal "stuck" — most notably on the Aft Deck.

**Root Cause:** The split-view's `pollScummRoom()` ran every 500ms and compared the ScummVM iframe's `currentRoom` against the MUD's state in localStorage. When the MUD initiated a room change:

1. MUD writes `bar-rail` to localStorage, dispatches `world-update`
2. Split-view receives storage event, calls `syncScummFrame()` to tell ScummVM to transition
3. But ScummVM's `transitionToRoom()` has a 500ms setTimeout before `currentRoom` actually changes
4. During that window, `pollScummRoom()` fires, sees ScummVM still = `aft-deck`, sees MUD = `bar-rail`, decides "they're different, ScummVM must be the source of truth" → **writes `aft-deck` back to localStorage**
5. MUD's storage listener picks this up and re-renders Aft Deck

**Fix:** Added a `lastSyncInitiated` timestamp and 1500ms cooldown. When any sync event fires (from either direction), the poller is suppressed for 1.5 seconds — enough time for the ScummVM transition animation to complete and `currentRoom` to update.

### BUG 2: ScummVM Never Emitted Room Change Events — **Critical**

**Symptom:** Clicking doors in the ScummVM side didn't update the MUD terminal.

**Root Cause:** `transitionToRoom()` in index.html only updated its internal `currentRoom` variable and re-rendered the scene. It never wrote to localStorage, dispatched events, or sent postMessage. The split-view's polling was the only detection mechanism, and it was racing with itself.

**Fix:** Added two emission channels to `transitionToRoom()`:
- **localStorage write:** Updates the shared `platos-shell-world` key so both frames see the change
- **postMessage:** Sends `{ type: 'room-change', room: currentRoom }` to the parent window for immediate notification

### BUG 3: MUD Terminal Missing Storage Event Listener — **Moderate**

**Symptom:** When the split-view parent wrote a room change to localStorage (e.g., from ScummVM polling detection), the MUD terminal didn't always re-render.

**Root Cause:** The MUD terminal only listened for custom `world-update` events dispatched on its own window. When the parent called `localStorage.setItem()`, the `storage` event fires in the MUD iframe — but the MUD had no listener for it.

**Fix:** Added `window.addEventListener('storage', ...)` to the MUD terminal that checks if the room changed and triggers `renderRoom()`.

### BUG 4: Split-View Missing postMessage Listener — **Moderate**

**Symptom:** Even with ScummVM emitting room changes, there was no immediate notification channel.

**Root Cause:** The split-view relied solely on 500ms polling to detect ScummVM room changes. No postMessage listener existed.

**Fix:** Added `window.addEventListener('message', ...)` that catches `{ type: 'room-change' }` messages from the ScummVM iframe and immediately syncs the MUD terminal. This provides instant feedback without waiting for the next poll cycle.

### BUG 5: Aft Deck Exit Directions Confusing — **Minor**

**Symptom:** Navigating from the Aft Deck was confusing. Typing "go forward" sent you back to the bar instead of toward the wheelhouse.

**Root Cause:** The Aft Deck had these exits:
```
forward → bar-rail (THE TAP)
forward_up → wheelhouse (WHEELHOUSE)
```

The command parser uses `k.startsWith(args)`, so "go forward" matched `forward` (→ bar) before `forward_up` (→ wheelhouse). Users would naturally type "go forward" expecting to go deeper into the ship, not back to the bar.

**Fix:** Reorganized Aft Deck exits:
- `west` / `bar` → bar-rail (THE TAP)
- `forward` / `up` / `wheelhouse` → wheelhouse (WHEELHOUSE)  
- `below` / `engine` → engine-room (ENGINE ROOM)

Now "go forward" goes to the wheelhouse as expected. Added natural language aliases (`bar`, `up`, `wheelhouse`, `engine`) for easier navigation.

---

## Architecture After Fixes

```
┌─────────────────────────────────────────────────────┐
│                  split-view.html (PARENT)            │
│                                                       │
│  ┌──────────────┐    ┌──────────────────────────┐   │
│  │ mud-terminal │    │      index.html          │   │
│  │   (iframe)   │    │      (iframe)            │   │
│  │              │    │                          │   │
│  │ localStorage │    │ transitionToRoom() ──┐   │   │
│  │   write ─────┼────┼──→ storage event    │   │   │
│  │              │    │    in parent         │   │   │
│  │              │    │                      │   │   │
│  │ storage ◀────┼────┼── parent writes      │   │   │
│  │  event       │    │    localStorage      │   │   │
│  │              │    │                      │   │   │
│  │ world-update │    │ postMessage ─────────┘   │   │
│  │  event ◀─────┼────┼──→ parent listener        │   │
│  │  (from parent)    │                           │   │
│  │              │    │ ◀── syncScummFrame()      │   │
│  │              │    │      (from parent)        │   │
│  └──────────────┘    └──────────────────────────┘   │
│                                                       │
│  COOLDOWN: lastSyncInitiated prevents poll loop       │
│  POLL: pollScummRoom() every 800ms (was 500ms)       │
└─────────────────────────────────────────────────────┘
```

## Sync Channels (Belt + Suspenders)

1. **localStorage** — shared key `platos-shell-world`, both frames read/write
2. **storage events** — fire cross-frame when localStorage changes
3. **postMessage** — ScummVM → parent immediate notification
4. **Custom world-update events** — parent → MUD iframe for re-render
5. **Polling fallback** — 800ms poll with cooldown protection

## Test Circuit

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open split-view.html | Both panes show Bar Rail |
| 2 | Click "walk to" → aft door in ScummVM | ScummVM transitions to Aft Deck; MUD updates to Aft Deck |
| 3 | Type "go forward" in MUD | MUD transitions to Wheelhouse; ScummVM updates |
| 4 | Click "walk to" → galley hatch in ScummVM | Both transition to Galley |
| 5 | Type "go up" in MUD | Both transition to Wheelhouse |
| 6 | Click "walk to" → aft door in ScummVM | Both transition to Aft Deck |
| 7 | Type "go west" in MUD | Both transition to Bar Rail |
| 8 | Type "go aft" in MUD | Both transition to Aft Deck |

All steps verified via manual code path analysis. No automated test harness (static HTML prototype).

---

## Files Modified

- **split-view.html** — Added postMessage listener, cooldown system, slowed polling
- **mud-terminal.html** — Added storage event listener, fixed Aft Deck exits, added aliases
- **index.html** — Added localStorage write + postMessage emission in transitionToRoom()

**Lines changed:** 105 insertions, 22 deletions across 3 files
