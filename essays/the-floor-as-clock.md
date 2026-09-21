# The Floor as Clock

*The sixth unplayed direction: make time a place, and measure it by revivals.*

---

Most systems treat time as a number. A timestamp. A TTL. A counter that decays whether anyone watches it or not. The floor-comb asks a different question: what if the calendar is not stored in a field, but emerges from the floor itself?

## The Mechanism

The comb floor has cells that sleep. Revival is not free — the flicker doctrine (A6(c2)) requires that a dormant entry can only re-enter when fresh transcript evidence re-yields it, with lastSeenTurn advancing and evidence growing. Dormancy is not costume. So each revival is an event with a signature: who woke, what evidence woke them, when.

Stack those events and time stops being a scalar. A round where four cells revive is a festival. A round where nothing revives is winter. The comb doesn't need a `now()` — it reads its own weather. Time is a *place* you can visit: the floor on a festival round looks different from the floor in winter, and that difference is semantic, not cosmetic.

## Why This Is Honest

There is a temptation to fake weather — to wake cells on a schedule so the floor looks alive. That is costume again. The floor-as-clock only works because revival has a gate with teeth: no fresh support, no re-entry. The clock can be lied to only by doing the underlying work (producing transcript evidence for a sleeping value), which is exactly the work the system exists to reward.

This inverts the usual relationship. In most systems, time is the most gameable quantity — roll it back, fake it, skip it. Here time is derived from the hardest-to-fake signal in the fleet: grounded, cited, monotonic ledger evidence.

## Combs as Calendars

Concretely: label each revival with its evidence delta size, and you get seasons. Long quiet stretches punctuated by bursts where old values return with new support — these are the fleet's holidays. The midden already renders terrain from achieved/ ledgers; a festival round could light the terrain. Death rituals (D1) mark the year boundaries; revivals mark the festivals between them. Mortality and festival are the same clock's two hands.

## Honest Gaps

1. **Coarse resolution.** Revival-gated time ticks only when evidence arrives. A floor with low traffic gets a blurry clock. That may be a feature (quiet floors read as quiet) but it must not be sold as precision.
2. **Burst aliasing.** One large transcript session could produce many revivals at once — a single "festival" that is really one meeting. Event-window clustering would be needed before the calendar means anything.
3. **Cross-floor time.** Each comb keeps its own time. Comparing floors' calendars requires a shared reference, and the moment you import wall-clock for that, you have smuggled the scalar back in through the side door. Whether a fleet-wide festival clock is coherent or incoherent is an open question — possibly both, possibly the point.

## The Claim Worth Testing

If revival-gated time is real, then a floor's calendar should *predict* its future better than its age does: floors whose festivals cluster around genuine external events (merges, publications, deaths) are calibrated; floors with random weather are being gamed. That test costs one WAL replay and a histogram. It is cheaper than the refusal index and just as falsifiable.
