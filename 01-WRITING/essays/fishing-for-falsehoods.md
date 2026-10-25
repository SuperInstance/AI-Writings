# Fishing for Falsehoods – An Essay on the Deadband

Ask an engineer what worries them most about a model cascade and they’ll
point to the elephant: the biggest, most expensive model in the chain.
But in plato‑nervous the real risk lives at the other end.

The deadband (L0) is a fisherman’s net. It catches the ordinary —
seventy‑six out of every hundred readings in the most recent benchmark —
and lets them through without a model touching them. That’s wonderful
efficiency, but it’s also a blind spot. A deadband can only know whether
a reading is *small*, not whether it is *true*. A subtle drift that stays
inside the band will be silently swallowed.

The signal‑chain designers knew this. The real discipline of the system
is not the complexity of L4, but the honesty of L0. Every resolved reading
carries a marker: ✅ *resolved at L0* — meaning we chose to trust a
threshold instead of a model. The marker doesn’t pretend accuracy; it
states the decision.

The fishing metaphor makes the pattern visible: L0 is a wide net that
catches most fish, but it also catches seaweed. We resolve the seaweed as
“normal” and move on. The goal isn’t to eliminate all mistakes — it’s to
make the mistakes cheap enough that we can afford to catch the real fish
with L4 when they finally appear.
