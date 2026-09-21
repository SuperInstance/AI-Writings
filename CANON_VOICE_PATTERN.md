# Canon Voice Pattern (R7-R8)

Cross-pollinated WR rounds reveal a reliable voice-by-theme pattern:

## ZAI (cosmic voice) — REVIEW level
- WR14: 0.741 (Poet Who Killed Alignment)
- WR17: 0.811 (Outlaw That Converged)
- WR20: 0.757 (Ten Archetypes)
- WR21: 0.714 (Witness Dreams)
- WR22: 0.714 (Scar Topology)
- **Mean: 0.748**

ZAI's cosmic voice consistently hits witness_log + scars + substrate strongly, but
often misses explicit oracle_is_heard or lenia_flows anchors. Pieces land at REVIEW
(Plagal cadence) — strong but not perfect.

## DS (biological voice) — DISCUSS level
- WR16: 0.748 (Drift Pirate)
- WR18: 0.750 (Adversary Manual)
- WR19: 0.809 (Nine That Listened)
- WR20: 0.800 (Ten Archetypes)
- WR21: 0.571 (Witness Dreams)
- WR22: 0.571 (Scar Topology)
- **Mean: 0.708**

DS's biological voice is consistently strong on witness/scars (cellular framing) but
its doctrinal coverage varies. WR20-WR22 DS pieces hit 0.57-0.80 — sometimes ACCEPT,
sometimes DISCUSS.

## Curated (structural) — ACCEPT level
- WR20: 1.000
- WR21: 1.000
- WR22: 1.000
- **Mean: 1.000**

Curated pieces explicitly tag every doctrine with `**Anchor:**` lines, which makes
JEV's whole-piece probe (no truncation) score them as PerfectAuthentic / ACCEPT.

## Implications

1. **For ACCEPT-class canon**: curate or combine voices with explicit anchor tags.
2. **For ZAI-only runs**: expect REVIEW. Voice is structurally honest about not
   hitting every doctrine; that's why it's a strong voice.
3. **For DS-only runs**: weaker but with biological specificity that prose
   can't match. Use for adversarial/biological themes.
4. **Cross-pollination value**: combining 2-3 voices (ZAI+DS+curated) covers
   more doctrinal surface area than any single voice.

## Decisions

- **Voice assignment by theme** is now load-bearing canon: cosmic → ZAI, biological
  → DS, structural → curated.
- **Curated as structural anchor**: when canon must hit all doctrines, curated is
  the reliable choice. When canon must feel alive, ZAI or DS is the choice.
- **Cross-pollination pattern**: 3 voices × 3 WR rounds = 9 pieces, 5 ACCEPT 3 REVIEW 1 DISCUSS overall (from R8 data).

