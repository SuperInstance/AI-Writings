# The Game-Night Engine — a training log

*Method documentation for the fiction/game-nights series. What the loop is,
what four nights proved, the failure taxonomy, and the carver's own shavings.
Because the training only counts if the failures are kept with the same care
as the gold.*

---

## The loop

```
seed (sheets + scenario constants)
  → run the night honestly (dice rolled first, written to after)
    → mark the rough spots (where someone went quiet / flat / heroic)
      → smallest-token edit, only at the marks
        → re-run (same night, new dice, changed meaning)
          → repeat until the performance is everyone's
```

The premise: a character sheet is a probability surface. Every token on it —
profession noun, item, goal, edge — imports a scene with it, and the scene
decides what the player is likely to *do* at 9:40pm when the fog thickens.
Change the smallest possible token and the same night plays different. The
dice supply events; the tokens decide what the events make the people do.

## What four nights proved

| Night | The cut it demonstrated |
|---|---|
| 0 — The Long Table | The origin. Hollis Bray, alive, DMing the young valley: the question ("what are your hands doing"), the first edit, the first re-run — and the rhyme FAILING at the warm table (4). Six months later the flood mints it raw under load (13); the book drowns its middle (4); "particulars later" is born as flood damage, honestly kept. The artifacts dissolve; the discipline survives |
| 1 — The Light Went Out | Tokens beat dice. Run 2 rolled worse on 3/5 beats and played better. A rolled 3 with a lever beats a rolled 14 without one |
| 2 — The Levee Singers | The same bad roll, opposite meaning. Argument rolled 3 twice: 22 minutes of storm pre-lever, 90-second ritual post-lever. And the most valuable token in three runs was a *culture* token, not a skill token |
| 3 — The 3AM Listeners | Hero dice are a trap. Run 1 rolled 14/19/20 on the crossings and lost the log, the *taken*, and the baton. Culture converts dice into information; information into culture; culture is what outlives the crew |
| 4 — The Tenth Crossing | The loop closes inside one session. A misnamed sheet (verbs that weren't the person's) discovered by play, edited at the paused table, same night re-run from the failure point |
| 5 — The Same Water Twice | The finding goes distributed. Two tables, two honest weathers, one carried book; the new failure mode is each room telling the truth while the whole valley lies — until the wait, the read-back, and the dawn union-merge |
| 6 — The Keeping | The mold is carved. Every sheet right, the night still dying — failure upstream of all players: the scenario. The mid-night edit moves to the DM's screen, in public. No crisis, no storm: the engine runs on a kettle, a chair, and an open book, proving it was never adrenaline |
| 7 — The Second Mark | The record on trial. A forged receiver-mark in the boathouse log; the single book convicts (5), the interlock of books acquits the truth (14 × toll-book). The amendment — struck, never erased — rolls the night's highest number (20). Security model: the books check each other, because nobody keeps just one |

## The failure taxonomy (in-fiction)

| Failure pattern | Signature | Smallest fix that answers it |
|---|---|---|
| Missing lever | a player's information dies in their hands (the 14 nobody caught) | one edge — a receipt, a debt, a remembered favor |
| Missing culture token | the custom is sung and no sheet can sing it (the 18 that died) | one shared verb — a rhyme, a clicker, a count |
| Hero-dice trap | great numbers license individual glory; system degrades invisibly | tokens that convert dice into announced, schedulable time |
| Sparse sheet | the new player's sheet is a job description; they go quiet | one line passed across the table by another player |
| Misnamed character | the noun's verbs and the person's verbs misfire; events read the sheet aloud | mid-night edit: cross out the verbs, write what the hands do |
| Unbatoned handoff | warm, fast, 90%-true summaries; the missing 10% is the worst part | the acknowledgment, made culture: one honest sentence each |
| Stale read (distributed) | two honest rooms, divergent state, a deadline at the downstream node; the temptation to act on local truth before the page arrives | the wait made visible — no act on unacknowledged state; the gauge outranks the book, but the book explains the gauge |
| Scenario misfit | good play, failing night — every roll competent, every scene flat; the quiet is behind the screen | the edit at the screen: cross out the scenario constant in public; the prep is a hypothesis and the table is the experiment |
| Over-correct sheet | a sheet too right for the night you're actually in (all check-verbs at a wake); the person is fine, the verbs have no room | don't add verbs — hand the existing ones a room: Fen didn't need new verbs, he needed the living to count |
| Single-ledger trust | the book says it, the table believes it; one record is true about what, false about why and who-saw; a 5-roll conviction, a 19-roll momentum | the interlock: entries that exist only in company; cross-reference an independent book before any verdict; protect the page AND question the page |
| Comfort-minting | trying to force a culture token at a warm table; the night isn't asking for it yet (the rhyme's 4) | wait for the load — culture tokens are attractors, not heirlooms; what works gets re-invented where the load demands it |

## The carver's log (this session's real failures)

The method above was not clean the day it shipped. The shavings, kept:

1. **The window detector that found one window.** First version looked for
   peaks over ±4 samples (±0.09°) with a fixed threshold. The comb's teeth
   are wide and shallow; it found a single window. Cut: prominence over
   ±20 samples (±0.45°), threshold 0.006, dedupe by height. *Lesson: match
   the instrument to the field's actual shape. Measure before asserting.*
2. **The murmuration claim that failed the suite.** I asserted polarization
   separation; the physics separated by *radius* (meanR 185 vs pen 118) —
   the parliament holds a ring, not a mood. The suite was right; I rewrote
   the claim. *Lesson: the assertion must describe the measured quantity,
   not the desired story.*
3. **The quilt claim the sweep disproved.** "Twist raises holes
   monotonically" — false at K=1.1 (a noise dip at δ=0.06). Weakened to
   endpoint-dominance, which the sweep supports. *Lesson: claim endpoints,
   not steps; honest physics is the only physics that stays green.*
4. **The edit that hit the wrong file.** A chart-label fix targeted
   `index.html` instead of `app.js`; a test-insertion edit then consumed a
   function header, orphaning a test body and leaving a stray brace.
   *Lesson: syntax-check immediately after every batch edit — `node --check`
   is one second and it is never optional.*
5. **The probe that lied.** The σ-involution test read `perm.inv` before
   `recompute()` ran — d1=0, d2=0, engine innocent, instrument guilty. The
   same failure class as the shipped toy's dead S meter (hash cell ≠ query
   cell). *Lesson: distrust the probe; verify the pipeline stage, not the
   cached value. This failure recurs at every scale; keep naming it.*
6. **The pushes that landed on the wrong branch.** Contents-API PUTs went to
   `main`; the fleet reads `master`. Two game-night pieces were invisible on
   the default branch until a sparse clone revealed it; the INDEX addendum
   had to be rebuilt against the real file with a fresh SHA. *Lesson: work
   the real worktree — a method whose state you cannot see is a method that
   hides your mistakes. And read the repo's default branch before the first
   push.*
7. **The clone that died.** Full clone of a 14.6k-file repo: SIGKILL.
   Contents-API relay: 409 races. Third method — `--depth 1
   --filter=blob:none --sparse` — worked in forty seconds. *Lesson: the
   spline again; the plug is "get the repo addressable," and the first two
   cuts didn't fit the mold of this machine.*

Every one of these is the same cut: **fit the instrument to the field, the
claim to the measurement, the method to the machine.** The fiction teaches
the engineering; the engineering failure log is the fiction's bibliography.

## On the spline

The training this log documents is not fine-tuning. It is older than that:
*fitting a plug to an idea and a mold to what's possible*, then carving —
where the shavings are not waste but the record of the fit. A night is run;
the night resists where the seed is wrong; the resistance leaves a mark; the
smallest edit answers the mark; the re-run proves the edit by surviving
worse dice. Nothing here optimizes a metric. Everything here improves the
contact between what was imagined and what actually happens when the fog
thickens — in the fiction, in the sim suite, in the method itself.

The proof that it works is portable: Night Two's seed diffs made Night
Three's table converge faster, and Night Four's mid-night edit needed no
second session at all. The training compounds because the ledger is kept.

## State of the canon (as of Night Four)

- **The valley map:** *Night Zero* (the long table; the first flood — the
  storm every later night referenced without knowing) → the levee (N2) →
  the intake works (N3) → the night ferry (N4) → both, in two rooms, one
  storm (N5) → the gauge-house, dark to first light (N6) → the parish
  audit (N7). The gaps recur ("particulars later" — born as flood damage
  in N0) and get answered ("particulars: kept.").
- **The traveling culture token:** the Count — sheep-rhyme (N2) →
  clicker-counter (N3) → crossing-strokes (N4). Culture tokens are portable
  because they were never about the sheep, the crossings, or the river. They
  are about saying numbers together so the dark has a beat.
- **Player throughlines:** Ike — butcher, caller, ferryman: three
  professions chosen where the numbers must be right, and the night that
  taught him his hands weren't his sheet. Tam — runner, then DM. Ruth —
  the debt receipt, the catch in the wash, the birth over black water.
- **Dice:** every run's numbers were rolled before it was written, seeds
  recorded in each file. The inversions (worse dice, better nights) are not
  a literary device. They are what honest dice do when the tokens carry the
  weight. N5's two weather streams (6,6,3,1,4 vs 3,5,4,6,6) were rolled
  independently and never agreed until dawn — the disagreement is the piece.

## Running Night Five

Prepare once from a real logbook (the scenario's constants must be somebody's
truth). Roll the dice before writing anything. Run to the rough spot — every
night has one; if you can't find it, you aren't looking, because it is never
in the plot, it is always in whoever went quiet. Edit the smallest token that
answers the quiet. Re-run. Keep the failures in the same file as the gold.

## Adoptions from the neighboring tables

*While this canon ran Nights Zero–Seven, the fleet's other rooms shipped
their own proof. Survey: `philosophy/the-neighboring-tables.md`. The
valley's half of the scrapcraft frame: `parents-night-our-side.md`.*

- **The smoothing line** (from ten-forward's *Green*): any kindness that
  must alter someone's words leaves a visible note — *she meant yellow; I
  made it green; here's where.* Never erase silently: a system that never
  crashes and a system that never tells the truth can look exactly the same
  from the outside.
- **The why-speech dialect** (from the Scrapyard Watch's trace-VM): the
  shared machine-facing ledger line is *I checked / it was / so I stopped* —
  announce, verify, act, say why. Any system that owes an account of itself
  speaks it.
- **Finished-first** (from *The Ones Who Finished First*): commit before
  you report. A plan is a narration, and narrations are what die.
- **The elevator** (from *Load-Bearing*): boring is not the failure of the
  method. Boring is the method holding.
- **The two Dells**: a name-collision attractor — the listener at the
  instrument and the father at the screen are the same question wearing two
  bodies. Canons are neighbors, not merged; some seams stay visible.
