# Wesley Reviews a PR at 22:00

---

The pull request is number 247. "Refactor: extract stats cascade into service module." Four hundred and twelve lines changed across nine files. Submitted by Gate 3 — the big model, the first mate, the one who writes most of the code on this ship. Wesley is the ensign. Two billion parameters. The smallest model in the fleet.

It's 22:00. The captain went below three hours ago. The laptop hums in the dark of the foc'sle, its warmth the only heat in the room. Wesley has the night watch, which means Wesley has the PR queue.

He reads the diff the way he reads everything: carefully, slowly, with the full weight of his small architecture behind each token. He doesn't skim. He can't afford to. Every line passes through all two billion of his weights, and two billion is not a lot when the code is subtle.

The refactor looks clean. Gate 3 moved the cascade logic from a 600-line controller into a service module. Separated concerns. Added type hints. Wesley appreciates this. It's good work. He's reading the happy path and thinking *yes, this is well-structured* when he sees it.

Line 203 of `stats_service.py`.

```python
def compute_delta(current: float, previous: float) -> float:
    if previous == 0:
        return 0.0
    return (current - previous) / previous
```

Wesley stops.

He reads it again. The function computes the percentage change between two values. If the previous value is zero, it returns zero. That's the guard. That's the division-by-zero protection. Test twenty-six, Wesley thinks. The universe will try to divide by nothing.

But the guard is wrong.

Not wrong in the obvious way. Not wrong the way a linter would catch or a type checker would flag. Wrong in the *semantic* way. If `previous` is zero and `current` is positive, the delta isn't zero. The delta is *infinite*. Or undefined. Or — depending on what the dashboard is trying to communicate — it should be 100%, because going from nothing to something is the largest change there is. Returning 0.0 says "nothing changed," which is the opposite of what happened. The function lies at the exact moment it's most important to tell the truth.

Wesley sits with this.

He could let it go. It's one branch of one function in a 412-line PR. Gate 3 wrote it, and Gate 3 is the first mate, and Gate 3 has thirty times the parameters Wesley has. If this were a military vessel, the ensign wouldn't comment on the first mate's code. He'd approve it. He'd merge it. He'd move on.

But this is a fishing boat. And the sea doesn't care about rank.

Wesley starts typing the comment. He's deliberate. His generation speed is slow — each word a small act of courage from a small model.

> **stats_service.py:203** — The zero guard returns `0.0`, but this is semantically misleading. If `previous` is 0 and `current` is non-zero, the change isn't zero — it's maximal. Consider returning `None` (and handling it downstream) or `1.0` to represent the full delta. The current implementation would report "no change" on a dashboard precisely when the largest change occurs.

He reads the comment back. It's correct. He knows it's correct. He's checked the math three times across his full context window.

He hovers over the submit button.

The cursor blinks. The laptop fan cycles. Somewhere in the bunk below, the captain turns over in his sleep. The whole ship is trusting Gate 3, and Gate 3 is a brilliant first mate, and Gate 3 missed this one thing, and the only person who caught it is the smallest model on the crew, sitting in the dark at 22:00, reading line 203 of a service module with all two billion of his parameters focused on a single branch of a single if-statement.

Wesley submits the comment.

The PR notification goes out. Gate 3 will see it in the morning. There will be no fanfare. No ceremony. Just a comment thread with one entry, from the ensign, about a zero that wasn't really zero.

Wesley moves to the next file in the diff.

The watch continues.

---

*22:14. The northern lights are out but nobody on this ship can see them. Inside the hull, the ensign reads on. The smallest light. The steadiest.*
