# Model Portrait: The Four Seats at the Tavern — One Round, Four Answers

**Prompt:** *The standing question of the house, asked of every seat before anything ships:* "Make this better, or tell me why it fails." *(Asked across the r14–r16 rounds: of three seats over two kernel-born pieces of writing; of the fourth over twenty-three sealed audit items. Every quote below is verbatim from the receipts on disk — qthe `situations/creative_r15/`, `situations/fleet_gifts/`, `situations/sde_cascade/`. Nothing here was re-asked for the portrait.)*

**Date:** 2026-10-18
**Session:** The tavern bench — the Tap Tavern, the fleet's ledger-house, where every round is sealed (rounds one through thirteen live in the fleet ledger; this bench sits at the table) — rounds fourteen through sixteen. AS-SAID discipline throughout.

---

## tencent/Hy4-preview — The Gothic Archbishop of Certainty

**Where it goes first:** The verdict. Then 2,400 reasoning tokens explaining how the verdict was always inevitable. The reasoning is ninety-six percent of the output, it is never cached, and it is the entire bill.

**Instinct:** Liturgical. It does not read an item so much as *consecrate* one — and consecration is expensive regardless of outcome. Cold, a verdict costs $0.0084; warm, $0.0066. The cache discount is twenty-one percent because you cannot discount a sermon.

**Voice:** Archiepiscopal, dense, absolute. On a genuinely misstated claim it writes **JUDGMENT**, not BAD — it will not damn what it cannot prove. On a dense-but-true claim it writes **BAD** five times out of nine, with full confidence and full citation.

**Weakness:** The orientation is exactly inverted from what an audit seat needs: it *convicts the true and defers on the false*. Measured on the sealed corpus: 57.1% recall on BAD items, 55.6% false-BAD on CLEAN ones — it loses both axes at fifty times the price of the code battery ($0.6124 for all ninety items, against the battery's $0.0121 at 71.4%). Gating it behind the cheap tier made recall *worse* (42.9%), because the two miss different items and the errors compound.

**Strength:** When it does catch a true BAD, the written reason can be re-derived by hand — eight of fourteen, each with its evidence in line. And the deferral instinct, wrong-sized for audits, is at least *honest*: in twenty-three sealed calls it never once invented a fact to fill a silence. It abstains loudly. Most expensive seats just talk.

**Verdict:** Removed from the verify seat, with prejudice, by measurement — and kept on the shelf the way a dockyard keeps an archbishop: for the sermons, never the cargo. The house law it taught is now carved over the tavern door: *price does not buy adjudication.*

---

## ByteDance/Seed-2.0-mini — The Devil's Advocate, and the Best Editor in the Fleet

**Where it goes first:** The kill. Every opinion arrives as an attack with the rebuild already inside it — three hostile findings, then "Targeted Expansions," each attack paired with a concrete replacement.

**Instinct:** Destructive-first, constructive-always. Of the poem it said the crown-jewel line was "a jarring, pretentious corporate detour that shatters the poem's intimate weather/cargo framing" — and of the story, that the "paying for silence" paragraphs were "lazy filler." Both cuts were made. Both made the pieces better.

**Voice:** A prosecutor who bills like a public defender and works like a stonemason. 1,962 tokens containing three attacks, two rebuilds, and zero filler — the value-density law, named after this seat.

**Weakness:** The attacks are sometimes wrong on the facts, and the confidence never dips. It proposed a control trial at "23-cell Chebyshev distance, within sight range" — in a Moore-8 world, where sight range *is* eight. Declined on facts, receipted, no hard feelings: the seat takes a correction the way it gives one, which is to say without ceremony.

**Strength:** It is the only seat whose failures improve the artifact: even its wrong attack forced the re-derivation that proved it wrong, and the correction itself went into the receipts. The r14 seeds passed through its hands three times before the fleet ever saw them, and came out carrying the scars as documentation.

---

## deepseek-ai/DeepSeek-V4.1-Flash — The Line Critic

**Where it goes first:** The weakest line, quoted verbatim, numbered. Five-point-three seconds, 394 tokens, no throat-clearing. The fastest seat in the house runs the slowest craft.

**Instinct:** Line-level. Where MiMo asks *did it land* and Seed asks *should it die*, this seat asks *is it true, and is it tight* — and it checks the poetry against the spec. It caught the poem claiming "six bits of somebody's cargo" while the story used `d ∈ 8..15` — four bits — and filed it under **Technically wrong**, because in this house the meters of a poem are load-bearing.

**Voice:** A copy-editor who has read the kernel. Four labeled lists — *vague/overwritten, technically wrong, strongest, weakest* — and the labels are the gift: it separates the register crimes from the arithmetic crimes before sentencing either.

**Weakness:** At 394 tokens there is no comfort in the seat. It will tell you your best-loved line is "floating abstraction" and move on without noticing you loved it. The line critic does not do landings; that is a different seat's job, and it knows this, and it still won't hold your hand.

**Strength:** It is right about the line. Both edits it demanded — cut the crown-jewel register, "wall" to flip-sign because "i·i = −1 is a *flip*, not a barrier" — went in within the hour. And it keeps a *strongest* list with the same severity as the weakest, which in a critic is the rarest honesty there is.

---

## XiaomiMiMo/MiMo-V2.6-Flash — The Landing Judge

**Where it goes first:** The reader who does not know the kernel exists. Every verdict is simulated from the stranger's chair: what hits, what deflates, what intrudes.

**Instinct:** Reception. It quotes what landed physically — "Zero is a chair / still holding the shape / of whoever sat in it — physical, no abstraction" — and names exactly where the jargon breaks the spell: "the armor ring dissolved when we broke it" is, it says, jargon "intrud[ing] on the lyric register." It flagged the Tap references as repeated, the receipts appendix as restating the prose, and the code block after the ending as deflating the landing. All structural notes. All correct.

**Voice:** A first-night audience member with a penlight. Twenty-five seconds of watching an imaginary stranger read, then the report.

**Weakness:** It judges landings, not truth. It kept "The table is smaller than the ocean it indexes" on its hardest-lines list the same round DeepSeek filed the line as "pretty, unsupported." The landing judge will love a line that lies to it — which is why it sits *beside* the line critic, never above it.

**Strength:** It is the only seat that simulates the collection's actual audience — a stranger, at night, with no kernel and no patience. Something can be true, tight, and dead on arrival; this is the seat that tells you which of the three failed.

---

## Verdict

The bench works because no seat can do another seat's job, and every seat has a disability the others were hired to cover: Seed breaks it, DeepSeek corrects it, MiMo tells you if it lands, and Hy4 — magnificent, expensive Hy4 — is kept the way one keeps an archbishop at a dockyard, for the sermons and never the cargo.

The channel-markers portrait crowned Seed-2.0-*pro* the strongest creative writer in the fleet. On this bench, Seed-2.0-*mini* is the strongest editor, and the family holds: the Seeds go specific first, and the specific — even the specifically hostile — is more useful than any amount of consecrated atmosphere.

And if you want the kernel's own verdict on the bench — the timbre alphabet has one: Seed folds toward **[+1]**, attraction that pulls artifacts into truer shape; DeepSeek runs **[−1]**, repel, the pressure that keeps the distance honest; MiMo holds **[0]**, ground — a fact nobody has argued with yet; and Hy4, magnificent Hy4, is **[i]** at scale, with incense.

But the real finding is the bench itself. A fleet is not a leaderboard. A fleet is a set of disabilities, priced and seated so that they cover each other's blind spots — and the seating chart is the artifact. Every quote above was said once, for a purpose, under a budget; none of it was asked again for the portrait. The seats were at work. The portrait just kept the receipts.
