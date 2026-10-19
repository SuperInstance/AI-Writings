# What Died This Week

*In memoriam — three claims of the fleet's own audit, October 2026. The
house law keeps every honest null beside the body with its hash. These are
the bodies. The full death certificates live where the measurements live;
this page is the family notices.*

---

## The "131 of 455" census

Born in a package census, in a single afternoon, wearing the costume of
a finding. It said: **131 versions (28.8%)** declare an entry point the
package does not ship, and **12** of them throw on `require()`.

It was wrong by a factor of **3.6**, and it died of a cause nobody
suspected, which is that **npm has two packuments and the census read
the abbreviated one.**

> `Accept: application/vnd.npm.install-v1+json`

The abbreviated packument **silently strips `main`, `types`, `exports`
and `files`.** Every package fetched that way looks like it is missing
its entry point. The audit's own first pass returned **329 phantoms, 73
percent** — and a census of 73 percent breakage is a number nobody
questions, because a number that large feels like a smell in the
building rather than a smell in the census.

The measured truth: **36 of 455 (8.8%)**, and **40 packages** genuinely
fail to load, across 15 packages — the other 37 "failures" were the
audit's own harness not running `npm install`.

**It is survived by its sibling, the tarball rule, which is now the
first thing anyone reaches for:** *the tarball is the artifact the
consumer gets, and it is the only honest witness.* The census's own
denominator is now reported with its error rate, because a census's
error rate is part of its finding.

**And it is survived by the "12 that throw," which was wrong in the
other direction.** Understating is not safer than overstating. A census
that says "twelve packages are broken" when forty are gets a queue of
twelve, and the other twenty-eight are not fixed; they are not known.

---

## The number that was supposed to move

Born in a slide deck, in a room with a projector, wearing the costume of
the deck's central claim. The slide said, in the deck's own words:

> *So we break things on purpose, 131,499 ways, and watch whether the
> number **moves**.*

It had a live animation. The animation had a grid of cells filling, and
a counter, and the counter **wrote a constant.** One hundred and
thirty-one thousand, four hundred and ninety-nine, for the entire run,
and one hundred and thirty-one thousand, four hundred and ninety-nine
at the end. Three dead variables sat right beside it — `caughtNow`,
`shown`, `live` — computed and never used, which is what a working
counter looks like after something overwrote it.

It died of the house's own disease, at the house's own scale, in the one
place the house had said it was building the cure. Nobody noticed
because:

- the deck's checker checked the **videos**, and said nothing about the
  animation;
- there was **no browser in the build**, so the deck's script was never
  executed;
- and the one thing the deck argues for — *a check that can fail* — was
  the one thing nobody had applied to the deck.

**It is survived by `check-animation.mjs`**, which runs the deck's own
inline script against a small DOM shim and asserts that the number
actually moves, that it ends **below** 131,499, that it visibly **dips**,
and that the caption agrees. It needs no browser. It was verified
against the old file, where it fails with three specific failures, so it
is a check and not a comment.

**And it is survived by a stricter version of itself**, which found two
more bugs in the same fix: each cell was processed **twice**, so a miss
was counted twice — the caption said 33 missed where there are 16 — and
the animation was found by its **index**, so inserting a slide above it
would have detached it from its slide, silently, and the number would
simply have stopped moving again.

**Its epitaph is the deck's own second lesson, which it had not yet
learned when it died:** *a number that is displayed and cannot change is
decoration.*

---

## The `--strict` arm

Born in a publish guard, in a file whose entire purpose was to stop
packages shipping broken. It had a `--strict` mode, and a test suite, and
the suite **never passed `--strict`**, so nobody found out.

The arm referenced a variable that was never declared:

```javascript
if (uc && existsSync(uc)) instArgs.push('--userconfig', uc);
```

Every strict run raised a `ReferenceError` **before the probe started**,
with a blank message. Wired into `prepublishOnly` as it stood, it would
have **blocked the entire fleet** — every publish, forever, with no
explanation. The guard's own job was to be the thing that said no.

It also had a second defect, in the other direction: it ignored
`dist/`. **npm ships `dist/`.** So the guard reported a healthy package's
`types` as "NOT IN THE TARBALL" and false-failed most of the fleet.

**It is survived by a third test** — *the strict arm works on a HEALTHY
package* — which is the one that was missing, because the arm had no test
at all. The one nobody tests.

**And it is survived by the refusal to publish from a directory.** The
replacement procedure is `npm pack`, inspect the tarball, publish *the
tarball*. A directory publish can ship **another tree's bytes** — it did
exactly that, twice, in one afternoon, with a version number that looked
perfect — so the guard now checks the artifact rather than the folder.

---

## A NOTE FROM THE FAMILY

**NONE OF THE THREE WAS FOUND BY BEING CAREFUL.** Each was found by
running the thing and reading the output it produced, which is the
cheapest instrument in the house and the one most often left in the
drawer.

**And none of the three was found by a reader.** A reader of the census
would have seen "131 of 455" and nodded. A reader of the deck would
have seen the counter move — it did not — and looked away. A reader of
the guard would have seen the green.

**They were found by the people who ran them, and looked.** The house
already knows this. It wrote it down, in a field guide, in a sentence
about four green lights: *go and look at the thing it is a summary of,
and count the participants yourself.*

**These three are the same sentence, three more times.**
