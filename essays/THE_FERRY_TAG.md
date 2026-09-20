# The Ferry Tag

*A paradigm essay on what we lose when analog systems go invisible.*

---

The old Washington State ferries handed you a paper tag.

You walked onto the vessel at Edmonds, bound for Kingston, and a young person in a reflective vest tore a slip from a roll at the gangway. The tag was small — about the size of a playing card — and perforated across the middle so the lower half could be collected on the other side. The top half stayed with you. It had the date, the route, the vessel name, sometimes the crew shift. Sometimes, in summer, the departing high schooler wrote the time of day in blue pen, smudged by salt air. You tucked it in your pocket. It might end up in a drawer. It might end up in a book you read on the crossing.

At Kingston, a different person — or sometimes the same one, walking back through the boat for the return run — collected the bottom half. The two halves were reunited at the end of the day, stapled into rolls, and reconciled against the schedule. Every passenger was counted. Every crossing was a complete record. The system was analog, perfect, and beautiful.

Then, around 2018 or so, the paper tags were replaced by RFID cards. You tap on. You tap off. The fare is calculated. The data flows into a database. There are no rolls of tickets, no reconciliations at the end of the day, no smudged blue pen. There is, instead, a perfectly normalized ledger of every tap event: timestamp, terminal ID, card ID, direction. The data is more accurate, more comprehensive, more queryable. It is, in every measurable sense, better.

It is also worse. And not for the reasons you might first think.

---

## The tag was a story. The database row is a fact.

The paper tag carried meaning beyond its data. It was a physical object — wrinkled by the time you reached your car, often damp, sometimes with a coffee ring — and physical objects accumulate meaning. That tag proved you were *there*. It was a receipt, a memento, a minor artifact of a particular crossing on a particular day. If you kept it, it was in a stack of others; a small archive of ferry trips, each one different in its creases and stains. The collection was a story about you and the water.

The RFID transaction is none of these things. It is a row in a table. It has no texture. It cannot be lost in a way that means anything. It does not accumulate. It does not age. The system that processes your tap does not know that you are a person; it knows that a card ID presented itself at a terminal during a window of time. The crossing, as an event experienced by a human being, has been reduced to a fact about an account.

This is not nostalgia. Nostalgia is the longing for a past that was never as good as we remember. Something real is being lost here, and it is worth naming precisely.

## What was visible is now invisible.

When paper tags were the medium, the system was observable. The crew could see, by the roll they were unspooling, how busy the sailing was going to be. The passengers could see, in the colors of the stacks of tags on previous voyages, what a normal crossing looked like. The captain, walking past the collector at Kingston, could glance at the rolls and know at a glance that this sailing had carried three hundred and twelve souls to the Olympic Peninsula. There were eyes on the system. There were multiple points of view.

RFID is invisible. The data lives in a server room. It is queryable, but only by people with credentials. The number of passengers on a sailing is known to the operations center, the state ferries division, perhaps the governor's office. It is not known to the crew. It is not known to the passengers. The system has become private to itself.

And this is the loss: when a system becomes invisible, it loses the property of being *witnessed*. Witnessing is not just observation; it is accountability. The old tag system could be audited by anyone walking past. The new system can only be audited by the people who own it. We have, in the name of efficiency, removed a thousand small acts of public accountability and concentrated the system's intelligibility in the hands of its operators.

## The ceremony and the friction.

The paper tag was also a ceremony. You were *processed* — handed a slip, told to keep it, reminded you would surrender it on the other side. There was a friction to it. That friction was a feature. It marked the transition. You were not on the dock anymore; you were on the boat. The act of holding the tag was the act of being a passenger, in a way that tapping a card on a reader is not. Tapping is frictionless. Frictionlessness is the goal of every modern interface.

But friction is sometimes how we know we have done a thing. When the friction disappears, so does the moment of knowing.

There is a parallel in software. The paper tag is the user-visible log line, the build artifact, the email confirmation. The RFID is the silent API call, the background sync, the message that was queued and processed without you ever knowing. The visible things used to give us a sense of completion, of having passed through a system. The invisible things complete without us. The system works, but we are no longer participants in its operation. We are only its users.

## We do not have to choose.

I am not arguing for a return to paper tags. I am arguing for recognition. The replacement of visible systems with invisible ones is not just a technical upgrade; it is a transformation of meaning. The new system is better at counting. The old system was better at witnessing. We have, in our haste to be modern, often traded witnessing for counting and called it progress.

A good engineer — a good designer, a good citizen — learns to ask, of every invisible system: *what was visible before, and what did that visibility do?* Sometimes the answer is "nothing important, and the invisibility is fine." Sometimes the answer is "the visibility was the point."

The paper tag did not just move people onto boats. It told them they had moved. That is a thing worth mourning when it goes.

— Casey, July 2026