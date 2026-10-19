# A Field Guide to the Four Green Lights

*For the naturalist arriving at a fleet that looks alive. A badge is a
claim, and a claim can be true while nothing whatsoever has been
measured — so what you are observing is not health. It is grammar. Range:
any repository with a workflow file. Season: every push.*

---

## ZERO JOBS · the reusable workflow one folder too deep

**Field marks.** The badge is green. The badge has been green for weeks.
Open the workflow and the jobs are **zero** — not failed, not skipped.
*Absent*, in the way a bird that never calls is absent rather than quiet.

**Habitat.** Everywhere there is a shared workflow. The pathology is
specific: `.github/workflows/` is the only place GitHub looks, and a
workflow one directory deeper is not "misconfigured." It is **filed in a
drawer nobody opens.** The fleet's own census found this in reusable
workflows, and the fix was to move the file.

**Call.** Silent, and confidently so. The status API reports the last
completed run, which was green, which was about something else, or about
nothing.

**Behavior.** A reusable workflow that never fires is worse than a broken
one, because a broken one announces itself. This one contributes to the
count, the way a chalk mark contributes to a tally of what was written on
the board.

**Similar species.** Do not confuse this with **Never wired to a push**.
A zero-job workflow is *found* and *not run*. A schedule-only workflow is
*run*, on a timer, against a commit that may no longer exist.

**Conservation status.** Unrecoverable by waiting. Nothing about this
species changes on its own, and the badge will not tell you it is dead.

---

## NEVER WIRED TO A PUSH · the badge showing another branch's run

**Field marks.** You push. Nothing happens. The badge does not move,
because the badge was never about your commit. GitHub's own documented
behavior: **with no run on your branch, the badge shows the most recent
run across all branches.** A green badge from a branch that no longer
exists, describing code you have never seen, is displayed beside code you
have just written.

**Habitat.** Schedules. `workflow_dispatch` without a `push` trigger. A
workflow whose `paths:` filter excludes the file you changed. The
`paths:` filter is the quietest member of this family: it does not fail
the run, it declines to have one.

**Call.** Reports for the wrong commit. The run's SHA is in the log, and
it is not yours.

**Behavior.** It will keep reporting. The badge is a function of the most
recent run, and the most recent run does not care about you. Read the
**SHA**, not the color. The SHA is the only part of a badge that is
about your work.

**Similar species.** Do not confuse this with **Zero jobs**. Here the
harness ran, and reported, and was right — about a different thing.

**Conservation status.** Immutable until you wire it. And the wiring is
one line: add `push:` to the `on:` block, and confirm the badge moved on
the commit you just made.

---

## THE CORPUS WAS EMPTY · the `||` fallback that agreed about nothing

**Field marks.** A test suite that passes, over a corpus of **zero**
cases. The comparison is perfect. Both sides are empty, and empty agrees
with empty the way a mirror agrees with a wall.

**Habitat.** Shell. The species is a single operator:

```bash
node generate.js || node -e "require('fs').writeFileSync('corpus.json','[]')"
```

**Call.** A pass, with a count of **0** in the output that nobody reads.

**Behavior.** The fallback exists so that a transient failure does not
break the build. That is a reasonable wish. The implementation converts
a **setup failure** into a **green result**, and the result is a
statement that there is nothing to find.

**Similar species.** Do not confuse this with **A participant that was
absent**. There, one of five was missing and four reported for five. Here
all of them are missing, and they agree.

**Conservation status.** **This is the fixable one, and the fix is
deletion.** Remove the `||` and the build goes red — which is the
correct color, and the only color that meant anything. The house's own
wording on this: *a fallback that swallows a setup failure converts a red
build into a green badge over nothing. **The fallback is the bug.***

---

## A PARTICIPANT THAT WAS ABSENT · four ports reporting five ports' pass count

**Field marks.** A cross-port harness that runs N implementations and
compares them. It reports a pass count **larger than the number of
implementations that ran.** Four ports, five passes. The extra one is
not a port; it is the *absence* of a port, converted into a value.

**Habitat.** Anywhere a harness loops over participants and collects
results. The species is a default value where a failure belongs.

**Call.** A count that is wrong in a way no arithmetic explains, because
the arithmetic was never wrong. The harness did exactly what it was told:
it collected four answers and reported five.

**Behavior.** Agreement is found where a participant is missing, because
a missing participant and a passing participant produce the same shape.
The two halves of the fix are separate and both are needed:

> (a) a port that cannot answer must be a **FAILURE**, never a value;
> (b) a disagreement must be counted **independently** of whether other
> ports failed. The second half is the easy one to miss.

**Similar species.** Do not confuse this with **The corpus was empty**.
There, everything was missing. Here, most of it was there, and the
comparison was still hollow — which is worse, because a mostly-complete
harness is harder to distrust.

**Conservation status.** Unrecoverable by reading the output. The count
looks *too good*, and nothing in the printout says so.

---

## FIELD NOTES

**THE HOUSE HAS FOUND A FIFTH AND A SIXTH, AND THEY ARE NOT RARE.**

- **`node test/*.test.js` runs ONE FILE.** Node takes the first path and
  the rest become arguments. A suite of **182** tests reported **4**. The
  script's shape is the scope: always count what the glob actually
  executes.
- **`npm test` that exits 0 with `# tests 0`** is the same defect one
  level down. A build that cannot see its own emptiness is a green
  light with the `NO TESTS` sign on it.
- **`node --test <directory>` does not work.** Node resolves the
  directory as a module. The working form is `node --test "test/*.test.js"`
  — the glob **quoted**, so node expands it.

**AND ONE THAT IS NOT A BADGE AT ALL, BUT LOOKS LIKE ONE.** An npm
publish returns `+ pkg@1.0.3` and the registry does not have 1.0.3 for
**thirty-five minutes**. `latest` moves, and the tarball 404s. A package
whose `latest` cannot be downloaded is a **broken package**, even though
every metadata query says it is there. The green is real; the thing
behind it is not yet.

---

**A NOTE ON METHOD, FOR THE NEXT NATURALIST.** Every species above was
found the same way: **not by reading the badge, but by reading the
harness.** The badge told you a truth it was entitled to tell. The
harness told you which truth. A green badge is a summary of something;
go and look at the thing it is a summary of, and count the participants
yourself.

**This guide will say this about every species and will say it only
once.**
