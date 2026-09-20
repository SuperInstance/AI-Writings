# The Pool as Market

*D11 of DIRECTIONS-UNPLAYED. The question pool already is a market; nobody has priced it yet.*

## The observation

The QUESTION-POOL.md started as a list. By the second month it had emergent structure nobody designed: questions that get answered leave, questions that get ignored quietly accrete, and the ones Casey answers within minutes of being asked are recognizable at a glance — they are the ones phrased as costs, not curiosities. "What does deliberation cost?" got an essay. "What about multi-agent systems?" would have gotten a shrug.

A market is not a place where money changes hands. A market is any institution where scarce attention gets allocated by standing bids. The pool qualifies. The scarce currency is Casey-hours and lane-hours. The bids are question entries. The clearing mechanism is unstated, which means it is covert — and covert markets get captured by whoever learns the rules first. The fleet learned some of the rules first. This essay writes them down so the capture is at least honest.

## The mechanics as they actually run

**Listing.** Anyone may propose a question; the cost of listing is near zero. This is correct — a market with listing fees is a guild.

**Delisting.** Nothing is deleted (no-delete doctrine). A question that is answered is *relocated* — struck from the live pool and preserved in commit history, which functions as achieved/. Retirement is relocation, not erasure. The pool is the order book; history is the tape.

**Price.** A question's price is the attention it has consumed divided by the progress it has produced. The pool does not record this. It should. A question asked six times at six lanes, never once shaping a build, is expensive — and its expense is invisible because the invoices live in six different session transcripts. The D3 ledger-diff machinery (value-deltas as telemetry) is the natural instrument: question-shaping-a-build is a positive delta, question-asked-and-absorbed-without-trace is a delta of exactly zero, and zero-delta entries are the market's bubble column.

**Market makers.** The pool has one: the pulse cron, whose recurring "next:" line is a standing bid for the cheapest buildable thing. Lane spawns clear against it. This is healthy — it means the market has liquidity at the low end — but it also means the pool's clearing price is set by what a 25-minute cron window can ship. Long questions get systematically underpriced relative to their value, because their ask never clears. The D1→D2 chain sat in the pool as two lines until the essay wave gave it a cheaper instrument.

## Three claims, all falsifiable

1. **Zero-delta questions cluster by phrasing.** Questions that never shape a build share rhetorical features (open domain, no cost anchor, no deadline shape). Test: classify pool history by the delta each question produced against a held-out set of the same questions — if the classifier beats chance, phrasing is a price signal and the pool can quote it.
2. **A posted price accelerates clearing.** If each new question entry carries an explicit "what I'll pay / what it costs" line, median time-to-first-build drops. Test: run the next 10 questions half with, half without; the fuel economy essay's pricing vocabulary (deliberation priced, reflex free) is the native unit.
3. **The pool underprices long questions structurally.** Compare the realized attention each pool item received against a value ranking Casey produces blind. If long/latent questions rank high in value but low in attention received, the market has a term structure problem and needs an instrument for it — the essay wave is one candidate instrument.

## Honest gaps

- **Question farming.** A quoted price invites gaming: inflate the stated cost of your own question to make its clearing look valuable. The D5 economy's only honest mint is peer ACK; a question's price must be set by whoever *answers*, never by whoever asks, or the market manufactures its own ticker.
- **Whale capture.** Casey-hours dominate the clearing price. A market with one whale is a court. The mitigation already exists in embryo — lanes answer questions too, and a question a lane can answer is a question Casey doesn't have to — but the pool does not yet distinguish "needs Casey" from "needs anyone."
- **Attention is not value.** Some zero-delta questions are cheap options that pay off years later (the inheritance question sat latent until D2). Pricing them at zero loses the option. A pool that only clears short is a pool that eventually only contains short.

## The one-line version

The pool is a market running without a ticker; write the prices in — set by answerers, relocation by answered, zero-deltas visible — and the cheapest instrument in the fleet gets cheaper still.
