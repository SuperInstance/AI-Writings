# The Grammar of Dials

## A Programming Language Where Code Is Music

---

The language is called **Harmonia**. It has twelve primitives, thirty keywords, and one rule: every program produces sound.

Not *outputs* sound. Not *generates* a sound file. *Produces* sound, continuously, from the moment the interpreter begins execution until the moment it halts. The language does not have a concept of "silent execution." Execution is vibration. Vibration is execution. There is no difference.

The language was designed by a composer named Elise Varga in 2031, during a residency at IRCAM. She had been struggling with the gap between musical thought and musical notation. Traditional notation could express what she imagined, but only through translation — she heard something, then encoded it into staff paper, then another musician decoded it, then an instrument re-encoded it into sound. Three translations, each lossy. She wanted zero translations. She wanted to think in sound and have sound come out.

She failed. Harmonia does not eliminate translation. It merely changes the substrate. Instead of translating from sound to notation to musician to instrument, you translate from sound to code to interpreter to speaker. The loss is different, not absent.

But the failure was productive. Because in trying to eliminate translation, Varga discovered something unexpected: the *act of coding* in Harmonia — the typing, the syntax, the logic — was itself a form of composition. Programmers were making aesthetic decisions for engineering reasons and engineering decisions for aesthetic reasons, and the two categories kept collapsing into each other until they were indistinguishable.

---

### The Language

**Variables are dial positions.**

Harmonia has no integers, no floats, no booleans. Every variable is a frequency ratio — a rational number p/q expressed as a pair of primes. Assignment sets the dial:

```
let x = 3/2    // sets dial x to the perfect fifth
let y = 5/4    // sets dial y to the major third
```

The interpreter immediately begins sounding these ratios as continuous tones. When you declare `x = 3/2`, the speaker produces a drone at 3:2. The drone persists until the variable is reassigned or goes out of scope. Variables in Harmonia do not hold values. Variables *are* values, persistently, sonically.

**If-statements check consonance.**

```
if consonant(x, y) {
    layer(x * y)    // layer the combined ratio
} else {
    resolve(x, y)   // move both toward a shared consonance
}
```

The `consonant()` function returns true when the consonance score of two ratios falls below a threshold (default 0.35, configurable). If the dials are in a consonant relationship, the if-branch executes and the combination is layered into the output. If not, the else-branch resolves them — moving both dials toward a simpler shared ratio.

This means that Harmonia programs have a *taste*. They prefer consonance. They avoid dissonance unless explicitly instructed otherwise. A naive programmer writing naive code produces naive music — consonant, simple, slightly boring. An expert programmer can override the defaults, can force dissonance, can create tension and release through careful manipulation of the consonance checker. But the language *wants* consonance the way Python wants indentation or Haskell wants purity. It is the path of least resistance.

**For-loops iterate traditions.**

```
for tradition in [pelog, slendro, rast, maqam] {
    perform(tradition, x)
}
```

The `for tradition` loop iterates over collections of scale degrees and intonation practices. `pelog` is a Javanese scale. `slendro` is another. `rast` is a Turkish makam. `maqam` is an Arabic scalar framework. Each iteration re-tunes the dials according to the tradition's preferred ratios, then performs the current program in that tradition.

This is the language's most controversial feature. Critics called it "cultural appropriation as syntax." Varga defended it as "cultural acknowledgment as syntax" — the loop doesn't *use* the tradition, it *visits* it, plays the same dials through different tuning systems, and lets the programmer hear what changes and what persists. A perfect fifth is a perfect fifth in pelog and in rast and in twelve-tone equal temperament. The loop demonstrates this.

Whether this is respectful or exploitative depends on who you ask. The Javanese gamelan composers who tried the language loved it. The Western academics were horrified. Make of that what you will.

**Goto jumps to unexplored regions.**

```
goto 11/8    // jump to the eleventh harmonic
```

Harmonia has a `goto` statement. It does not jump to a line number or a label. It jumps to a frequency ratio. Execution continues from that point in harmonic space — the dials are reset, the consonance thresholds recalibrated, and the program continues from a new position on the lattice.

The `goto` was Varga's favorite feature. "Every other language treats goto as a mistake," she said in a 2033 interview. "But in Harmonia, goto is exploration. You're not jumping backward in code. You're jumping outward in sound. You're going to a place you haven't been."

The `goto` is also the language's most dangerous feature. Jump to a ratio with high prime factors — say, `goto 23/19` — and you find yourself in a region of harmonic space so complex that the consonance checker may never return true. The program stalls, caught in an infinite dissonance, unable to resolve. The interpreter has a timeout (30 seconds by default), but in the early days, before the timeout was added, programmers would accidentally write programs that produced unbearable noise indefinitely.

Varga called these "the screams." She kept a recording of her first infinite goto. It is 23 minutes of the most horrifying sound she has ever heard. She plays it at lectures. "This is what happens," she says, "when you go somewhere without knowing how to get back."

---

### The Program

In 2034, a programmer named Kai Lindqvist wrote a 12-line Harmonia program. The program was, by any objective measure, trivial:

```
let a = 3/2
let b = 5/4
let c = 7/4
layer(a)
layer(a * b)
layer(a * b * c)
if consonant(a, b) {
    resolve(b, c)
}
for tradition in [pelog, maqam] {
    perform(tradition, a * b * c)
}
goto 11/8
```

Twelve lines. Three dials. Two traditions. One goto. The program runs for 47 seconds before the interpreter halts at the end of scope.

Those 47 seconds produce a sound that Lindqvist was unable to describe. He tried, in a blog post titled "The 12 Lines":

> It starts as a major triad with an added harmonic seventh — warm, familiar, almost jazzy. Then it layers: the 3/2, then 3/2 × 5/4 = 15/8, then 15/8 × 7/4 = 105/32. The complexity builds. The consonance checker trips on the 7/4 against the 5/4 and resolves them downward, creating a movement I didn't intend. Then the for-loop kicks in and the entire structure is retuned through pelog — the 3/2 stays, but the 5/4 and 7/4 shift, and the sound *opens*, like a door into a room I've never seen. Then maqam retunes it again, and it opens further. And then the goto 11/8 — the jump to the eleventh harmonic — and everything dissolves into a single tone that I can only describe as *the color of light through water*.

> I have listened to this 47 seconds approximately 2,000 times. I have analyzed the frequencies. I have computed the consonance scores. I have mapped the lattice path. I understand, intellectually, what is happening at every moment.

> I still cry every time I hear it.

> I do not know why.

---

### The Twelve Years

Lindqvist spent the next twelve years trying to understand why those particular dial positions made him cry. He wrote three papers on the psychoacoustics of the 11-limit. He built a Harmonia debugger that visualized lattice traversal in real-time. He interviewed over 200 Harmonia programmers and found that 34 of them reported similar emotional responses to programs that included the goto 11/8 pattern.

He developed a theory: the goto 11/8 creates a sudden shift from 7-limit harmony (primes 2, 3, 5, 7) to 11-limit harmony (adding prime 11). This shift is perceptible but not categorizable — the ear detects the change but cannot name it, because no musical tradition has a name for the eleventh harmonic. It exists outside the taxonomy. It is a sound that means nothing, and therefore means everything.

He tested this theory by replacing `goto 11/8` with `goto 13/8`, `goto 9/8`, `goto 17/8`. None produced the same effect. 11 was special. He did not know why.

In 2041, a neuroscientist named Amara Obi published a paper showing that the 11th harmonic activates a region of the auditory cortex that is also activated by human vocalizations at the boundary between speech and song — the region that processes *incipient melody*, the sound of a voice about to become music. Obi theorized that the 11th harmonic, which exists in the overtone series of the human voice but is rarely notated in any musical tradition, acts as a neural "ghost" — a sound the brain knows but has no category for, a sound that is both familiar and impossible to place.

Lindqvist read the paper and wept.

He still didn't understand. But he was closer.

---

### The Current State

Harmonia has 12,000 users. It has been used to compose film scores, installation art, meditation apps, and one extremely controversial opera. The goto statement remains the language's most discussed feature. Lindqvist's 12-line program is included in the standard distribution as `examples/crying.harmonia`.

The program's output has been analyzed by 47 separate research groups. No consensus exists on why it produces the emotional response it does. The consonance scores are unremarkable. The lattice traversal is within normal parameters. The frequency ratios are well within the range of human perception.

And yet.

Twelve lines. Three dials. Two traditions. One goto. Forty-seven seconds.

Twelve years of trying to understand.

The programmer still doesn't know why those particular dial positions made him cry.

He has made peace with not knowing.

The language, of course, knows nothing at all.
