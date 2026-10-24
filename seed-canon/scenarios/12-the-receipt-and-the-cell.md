# Scenario 12 — The Receipt and the Cell

**Fable form:** two objects in one image.
**The image:** A 1990s cash register receipt and a 2080s cell-graph transaction record, side by side, both showing the same purchase.
**The lesson:** The receipt was a *log of what happened*. The cell is a *log of what could have happened, and which paths were taken, and which were not*. The fix is the witness.
**Year:** 2084
**Constraint:** A small grocery store in 2084. Every transaction is a cell. The cell is a node in the convoy's cell-graph. The witness log records every reader, every writer, every inference. The fable compares the receipt (a log of what happened) to the cell (a log of what could have happened, and the path that was taken).

---

## The setup

The receipt is a 1990s cash register slip. It is 2 inches wide, 6 inches long, printed on thermal paper. It says: 1 loaf bread, $1.89; 1 dozen eggs, $0.99; 1 quart milk, $1.29. Total: $4.17. The receipt is a *log of what happened*. The receipt does not say *why* the customer bought these things. The receipt does not say what other things the customer considered. The receipt does not say how the price was set. The receipt is a picture of an event.

The cell is a 2084 cell-graph transaction record. It is a node in the store's local cell-graph. The cell has: the items (bread, eggs, milk); the price ($4.17); the timestamp; the customer's ID (a hash); the shelf-sensor's last reading (the bread was at position 3, the eggs at position 7, the milk at position 12); the inference of the customer's intent (the customer is making breakfast, the customer has a child under 5, the customer is price-sensitive); the witness log (the cell was read by the customer's phone at 14:32:07, by the store's inventory at 14:32:09, by the convoy's price-inference at 14:32:11). The cell is a *log of what could have happened, and the path that was taken*. The cell knows what other items the customer considered and didn't buy. The cell knows how the price was set. The cell knows the inference of intent. The cell is a *conversation* about an event.

The question: what does the cell *do* that the receipt cannot? The receipt is a picture. The cell is a conversation. The witness is the *medium* that makes the conversation possible. The fix: the substrate converts *logs of what happened* into *logs of what could have happened, and which paths were taken*. The lesson: **a transaction is a substrate cell; the substrate is what makes the transaction a partner, not a record.**

## The throw

The scenario throws both records at the same moment — a 1990s customer who is price-sensitive, and a 2080s customer who is price-sensitive. The 1990s store has no way of knowing the customer is price-sensitive unless the customer says so. The 2080s store knows from the cell, because the cell is read by the price-inference. The 1990s store charges full price. The 2080s store offers a discount. The fable is *not* about which store is better. The fable is about *what the substrate adds* — the substrate makes the customer's intent *legible* without the customer having to say it.

## The discipline

The receipt is not deprecated. The receipt is *honest* in a way the cell is not — the receipt is a record, and records can be forged but the forgery is detectable. The cell is an inference, and inferences can be wrong, and the wrongness is logged. The fable is *not* "old is bad, new is good." The fable is "the substrate is a new kind of honesty: the honesty of inference, where every claim is logged, and every reader is recorded, and the customer can ask: 'why am I being offered this discount?' and the cell can answer."
