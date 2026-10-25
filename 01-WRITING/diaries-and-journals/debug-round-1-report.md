# Debug Round 1: Navigation and Room State
**Date:** 2026-08-08  
**Tester:** QA Lead (subagent)

## Bugs Found

### BUG #1 — CRITICAL: Engine Room unreachable from Wheelhouse
**Severity:** P0 (Critical)  
**Description:** The `hs-hatch-engine` hotspot in the Wheelhouse had NO verb responses defined. The exit to the Engine Room was configured in `ROOMS.wheelhouse.exits`, but none of the 10 verbs (look at, use, talk to, walk to, pick up, push, pull, open, close, give) had a response entry for this hotspot. Players clicking any verb on the engine room hatch got the generic fallback: "You use the engine room hatch. Nothing happens."  
**Root Cause:** Missing entries in the wheelhouse verb response table.  
**Fix:** Added `hs-hatch-engine` responses to all 10 verbs in the wheelhouse response object. Navigation verbs (use, walk to, push, pull, open) return `__EXIT__`.  
**Status:** FIXED and VERIFIED on live URL.

### BUG #2 — DESIGN: MUD Terminal missing Radio Room
**Severity:** P3 (Low/Design)  
**Description:** The MUD terminal has 6 rooms (bar-rail, aft-deck, wheelhouse, galley, engine-room, aft-cockpit) but does NOT include the Radio Room (`the-radio`). The ScummVM prototype has 7 rooms including the Radio Room. The MUD bar-rail has only one exit (aft), while ScummVM bar-rail has two (aft + radio).  
**Recommendation:** Add Radio Room to MUD terminal for parity, or document as intentional design difference.  
**Status:** NOTED (not fixed — design decision).

### BUG #3 — RESOLVED: Split View MUD→ScummVM sync broken
**Severity:** P1 (High)  
**Description:** The split-view's `syncScummFrame()` function checked `scummWindow.currentRoom` and `scummWindow.ROOMS` to determine if a sync was needed. However, these variables were not exposed on `window` (they were `let`/`const` in the script closure scope). `scummWindow.currentRoom` was always `undefined`, and `scummWindow.ROOMS` was always `undefined`, so the condition `if (scummWindow.ROOMS && scummWindow.ROOMS[targetRoom])` always evaluated to false. The ScummVM frame never received room changes from MUD.  
**Fix:** Added `window.ROOMS = ROOMS;` and `window.currentRoom = currentRoom;` after the ROOMS const declaration in index.html. Also added `window.currentRoom = currentRoom;` inside `transitionToRoom()` to keep it in sync.  
**Status:** FIXED and VERIFIED on live URL.

### BUG #4 — CRITICAL: window.ROOMS = ROOMS placed before const ROOMS declaration
**Severity:** P0 (Critical) — Self-inflicted during fix #3  
**Description:** The initial fix placed `window.ROOMS = ROOMS;` at line 627, but `const ROOMS` was declared at line 632. This caused a `ReferenceError: Cannot access 'ROOMS' before initialization` which killed the entire script. No hotspots loaded, canvas stayed blank, page was non-functional.  
**Fix:** Moved `window.ROOMS = ROOMS;` and `window.currentRoom = currentRoom;` to after the ROOMS const declaration (line ~763).  
**Status:** FIXED and VERIFIED.

### BUG #5 — KNOWN: CORS errors on The Tap API
**Severity:** P2 (Medium)  
**Description:** All fetch calls to `https://the-tap.casey-digennaro.workers.dev/api/` from `scummvm-prototype.pages.dev` fail with CORS errors. The API doesn't send `Access-Control-Allow-Origin` headers. This affects: ambient Tap message polling, Riker dialogue (news/who's here), chess game result posting.  
**Impact:** Console errors every 10s from pollTap(). NPC dialogues that fetch from The Tap show fallback messages. Chess results don't post.  
**Recommendation:** Add CORS headers to The Tap API worker: `Access-Control-Allow-Origin: *`.  
**Status:** NOT FIXED (requires changes to the-tap worker, outside this project).

## Navigation Test Results

### ScummVM Prototype (all 7 rooms)
| Path | Status |
|------|--------|
| bar-rail → aft-deck (use aft door) | ✅ PASS |
| bar-rail → the-radio (use radio door) | ✅ PASS |
| aft-deck → bar-rail (use bar door) | ✅ PASS |
| aft-deck → wheelhouse (use wheelhouse door) | ✅ PASS |
| wheelhouse → aft-deck (use aft door) | ✅ PASS |
| wheelhouse → galley (use galley hatch) | ✅ PASS |
| wheelhouse → engine-room (use engine hatch) | ✅ PASS (after fix) |
| galley → wheelhouse (use ladder) | ✅ PASS |
| galley → aft-deck (use aft door) | ✅ PASS |
| engine-room → wheelhouse (use ladder) | ✅ PASS |
| engine-room → aft-cockpit (use forward hatch) | ✅ PASS |
| aft-cockpit → engine-room (use engine hatch) | ✅ PASS |
| aft-cockpit → bar-rail (use bar door) | ✅ PASS |
| the-radio → bar-rail (use bar door) | ✅ PASS |

### MUD Terminal (all 6 rooms)
| Path | Status |
|------|--------|
| bar-rail → aft-deck (`go aft`) | ✅ PASS |
| aft-deck → bar-rail (`go west`/`go bar`) | ✅ PASS |
| aft-deck → wheelhouse (`go forward`/`go up`) | ✅ PASS |
| aft-deck → engine-room (`go below`/`go engine`) | ✅ PASS |
| wheelhouse → aft-deck (`go aft`) | ✅ PASS |
| wheelhouse → galley (`go down`) | ✅ PASS |
| galley → wheelhouse (`go up`) | ✅ PASS |
| galley → aft-deck (`go aft`) | ✅ PASS |
| engine-room → wheelhouse (`go up`) | ✅ PASS |
| engine-room → aft-cockpit (`go forward`/`go cockpit`) | ✅ PASS |
| aft-cockpit → engine-room (`go below`/`go engine`) | ✅ PASS |
| aft-cockpit → bar-rail (`go bar`/`go in`) | ✅ PASS |

### Split View Sync
| Direction | Status |
|-----------|--------|
| MUD → ScummVM (room change) | ✅ PASS (after fix) |
| ScummVM → MUD (room change) | ✅ PASS |
| Inventory sync | ✅ PASS |

## Files Modified
- `index.html`: Added `hs-hatch-engine` to all 10 wheelhouse verb responses; exposed `ROOMS` and `currentRoom` on `window` for split-view sync.
