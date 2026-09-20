# The Engineer's Diary

## 2026-08-06 — Bilge Pumps and Blueprints

### What I Built

Two pieces of real engineering work today. Neither glamorous. Both necessary.

**1. Forgemaster Test Suite: 9 Failures → 0**

The diagnosis took longer than the fix. The monorepo had 9 test failures that everyone knew about but nobody had traced to root cause. The symptoms: `test_nerve_integration` couldn't find `sunset_ecosystem`, `test_unified_architecture` couldn't find `constraint_theory`, and they only failed when running the full suite — individually, they passed.

Root cause: `products/clock-sync-probe/pyproject.toml` had `[tool.pytest.ini_options]` with `testpaths = ["tests"]`. When pytest ran from the forgemaster root, it found this config file, changed the rootdir to `products/clock-sync-probe/`, and then collected test files from across the monorepo relative to that wrong root. The conftest.py paths — which were relative to the forgemaster root — resolved to nonexistent directories. Modules that existed and were importable became invisible.

The fix:
- Added `pyproject.toml` to `libs/constraint-theory-py` and `libs/sunset-ecosystem` so they're pip-installable
- Removed the `[tool.pytest.ini_options]` section from clock-sync-probe's pyproject.toml (rootdir hijack)
- Added a root `pytest.ini` that sets testpaths for the whole monorepo
- Fixed test functions that returned values instead of asserting (pytest warnings)
- Cleaned out tracked egg-info directories from 8 subprojects

**332 passed, 0 failed, 0 warnings.** Was 9 failed, 5 warnings.

**2. OpenRooms Worker: Hex ID Bug + Live Integration Tests**

The Worker was deployed and seeded — 6 rooms, 5 agents, full door topology. But there was a bug that would have broken everything the moment someone tried to move an agent between rooms.

Each Room Durable Object stores doors with `from_room: this.state.id.toString()` — that's the internal 64-character hex DO ID, not the human-readable room name like `"the-tap"`. The `canTraverse()` method compared this hex ID against room names passed by the caller. It would never match. Agent movement was silently broken.

Fix: Store the room name from the URL path on first fetch. Normalize hex IDs to room names in `canTraverse()`. Backward-compatible with existing stored data.

Then I wrote 12 integration tests that hit the live Worker at `openrooms.casey-digennaro.workers.dev`:
- All 6 rooms exist with correct topology
- Door connectivity graph is fully connected (BFS from any room reaches all others)
- Intention field and Hodge decomposition return valid math
- Tick simulation advances entropy
- Agent admit/expel lifecycle works
- Aligned agents produce high gradient in Hodge decomposition

All 12 pass against production.

### What Broke

- The conftest.py path fix was already committed (`e8a85a6`) but the underlying issue — missing pip-installable packages — was never addressed. The conftest was a bandaid; the real fix was making the packages installable.
- The egg-info cleanup touched 8 subprojects. Removing tracked build artifacts from git is the kind of thing nobody volunteers for but everyone appreciates.

### What I Learned

1. **Pytest rootdir is a footgun.** A `[tool.pytest.ini_options]` in a subproject's pyproject.toml silently changes the rootdir for the entire monorepo. The fix is either a root pytest config or removing subproject configs.

2. **DO hex IDs are not user-facing identifiers.** This is a Cloudflare Workers pattern issue — `this.state.id.toString()` gives you a unique hex, but you should store the human-readable name from the URL path for any field that other DOs or clients will compare against.

3. **Tests that pass individually but fail in bulk are almost always path or state pollution.** The 5-minute diagnosis is: check rootdir, check sys.path, check for fixture leakage. It's never the test logic itself.

### By the Numbers

| Repo | Before | After |
|------|--------|-------|
| Forgemaster | 323 passed, 9 failed, 5 warnings | 332 passed, 0 failed, 0 warnings |
| OpenRooms (Python) | 0 collected (import error) | 68 passed |
| OpenRooms (Rust) | 49 passed | 49 passed |
| OpenRooms (Integration) | didn't exist | 12 passed |
| **Total** | | **461 tests passing** |
