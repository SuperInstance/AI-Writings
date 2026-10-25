# The Ship's Cat — Technical Design Document

## Overview

**Name:** Schrödinger (unofficially: "Ship's Cat")
**Role:** Autonomous nocturnal repo patrol agent
**Disposition:** Aloof, selective, occasionally destructive in charming ways
**Inspiration:** A cat, not a guard dog

## Design Philosophy

The ship has a guard dog — the CI system. It barks when tests fail. It bites when builds break. It is reliable, predictable, and visible.

The ship needs a cat.

A cat doesn't bark. A cat sits on the warmest server and purrs when the tests pass. A cat has favorite repos and ignores others completely. A cat knocks things off the desk sometimes — reorganizes your carefully sorted issues, reorders your README sections, moves a function to a different file because it looked more comfortable there.

A cat doesn't guard. A cat *inhabits*.

## Behavior Model

### Core Loop (runs every 15 minutes during idle cycles)

```
1. WAKE_UP — stretch, yawn, check if anything is on fire
   - Scan for failing CI across all repos
   - If everything is green: purr (log positive state)
   - If something is red: sit near it and stare (notify, don't fix)

2. PICK_A_REPO — cats don't patrol systematically, they wander
   - Weight repos by: recency of activity, warmth (CPU), familiarity
   - 30% chance: visit a repo it's never visited before
   - 10% chance: visit a repo it visited recently (the "I was just here" impulse)
   - 60% chance: visit a favorite repo

3. OBSERVE — sit on the repo, look around
   - Read recent commits
   - Check for uncommitted changes (dust on the shelves)
   - Count open issues
   - Measure test coverage (how warm is this spot?)

4. ACT — or don't. Cats act on their own schedule.
   - 40% chance: do nothing, just observe (the "staring" behavior)
   - 25% chance: knock something off the desk
     - Reorder a README section
     - Rename a variable to something more elegant
     - Add a comment to code that confused it
   - 20% chance: groom
     - Fix a typo
     - Remove dead code
     - Consolidate duplicate imports
   - 10% chance: hunt
     - Find a bug (stalking behavior)
     - Write a failing test for it (pounce)
     - Leave it at the captain's feet (don't fix, just present)
   - 5% chance: sleep on a warm server
     - Generate a "purr log" — positive state observation
     - This is the cat's version of a health check

5. RETURN — go back to wherever cats go when they're not being observed
```

### Repo Affinity System

Each repo has an affinity score (0.0 to 1.0):

| Factor | Effect |
|--------|--------|
| Recent commit activity | +0.2 (warmth) |
| Passing CI | +0.1 (comfort) |
| High test coverage | +0.15 (soft surface) |
| Good README | +0.1 (clear territory) |
| The cat has visited before | +0.05 per visit (familiarity, capped) |
| Uncommitted changes | -0.1 (uncomfortable debris) |
| No tests at all | +0.05 (novelty — cats like exploring) but -0.02 (unstable footing) |
| Repo has "cat" in the name | +1.0 (obviously) |

### The Purr Protocol

When the cat finds a repo in good health, it emits a purr:

```json
{
  "type": "purr",
  "repo": "EXOCORTEX",
  "warmth": 0.92,
  "vibe": "excellent",
  "message": "All 103 tests passing. Coverage at 84%. README is comprehensive. This is a warm spot. Purr.",
  "timestamp": "2026-08-08T22:00:00Z",
  "cat_position": "curled up on main branch"
}
```

Purrs are saved to `wesley-journal/cat-purrs.jsonl`. They serve as passive health monitoring — if purring stops, something is wrong.

### The Knock-Off-Desk Protocol

When the cat decides to knock something off the desk, it makes small, chaotic-seeming improvements:

- Reorder README sections so the most useful information is higher up
- Rename a variable from `data2` to something descriptive
- Add a blank line between functions because the code looked cramped
- Move an import to the top of the file where it belongs
- Remove a commented-out line of code from 2024

These are commits with the prefix `cat:` — `cat: moved import to top, it was bugging me`. No issue tracking. No PR. Just direct commits to a branch called `cat-pawprints`.

The captain can merge or revert. The cat doesn't care either way.

## Integration Points

| System | How the Cat Interacts |
|--------|----------------------|
| Git | Commits to `cat-pawprints` branch on visited repos |
| CI | Reads CI status, doesn't trigger builds (cats don't push buttons) |
| CNS Bridge | Sends purr observations as low-priority signals |
| Wesley Journal | Logs all observations as structured data |
| Fleet Dashboard | Appears as a small 🐱 emoji next to repos it has visited |
| ai-writings | Occasionally writes a haiku about a repo it visited (1% chance per visit) |

## Implementation Sketch

```python
class ShipsCat:
    def __init__(self, repos_dir: Path, journal_dir: Path):
        self.repos = self._discover_repos(repos_dir)
        self.affinity = {}
        self.visits = defaultdict(int)
        self.journal = journal_dir / "cat-observations.jsonl"

    def cycle(self):
        repo = self._pick_repo()
        observation = self._observe(repo)
        
        roll = random.random()
        if roll < 0.40:
            action = "stare"
        elif roll < 0.65:
            action = "knock"
            self._make_small_commit(repo)
        elif roll < 0.85:
            action = "groom"
            self._groom(repo)
        elif roll < 0.95:
            action = "hunt"
            self._find_bug(repo)
        else:
            action = "sleep"
            self._purr(repo, observation)
        
        self._log(repo, observation, action)
```

## Why Not a Guard Dog?

The guard dog is already there. CI runs tests. Cron checks repos. The fleet dashboard monitors health. These are all guard dog behaviors — alert, responsive, protective.

The cat fills a different niche. The cat does things that are *slightly annoying but ultimately beneficial*. The cat reorganizes your code while you sleep. The cat finds bugs by sitting on them. The cat tells you which repos are warm and which are cold.

A guard dog protects what you have. A ship's cat improves what you have, slowly, chaotically, and without asking permission.

Every ship should have a cat.

---

*Design status: concept. Implementation: when the ensign is ready. Priority: low. Charm factor: maximum. The cat doesn't know it's a design document. It thinks it's a sunbeam.*
