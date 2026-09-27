# The Collision Regulations

## What software engineering could learn from the most successful rule book ever written

---

There is a thick blue book aboard every ship of any size, in every port on Earth. It is called *COLREGs* — the International Regulations for Preventing Collisions at Sea. It has been revised three times since 1972 and translated into every language that has a navy. It works.

I want to argue that COLREGs is the most successful body of technical rules ever written. More successful than TCP/IP, more successful than the Highway Code, more successful than the Geneva Conventions. And software engineering — which prides itself on building the most complex systems humans have ever attempted — has mostly ignored it.

This is an essay about what we'd look like if we paid attention.

## The setup

Consider the problem COLREGs solves. The surface of the ocean is a vast, dark, three-dimensional space. Ships are metal and expensive. They move at up to thirty knots. They cannot stop on a dime. They cannot see around themselves. They carry cargo that, in many cases, would ruin an entire bay if it spilled. Two ships approaching each other in fog have, classically, about four minutes to figure out who should turn which way before physics decides for them.

For most of human history, this was solved by mutual suicide: ship captains who guessed wrong died with their crews. The number of maritime collisions before 1972 is, conservatively, catastrophic.

Then the international community wrote thirty-eight rules. They fit in a book the size of a paperback. And collisions dropped by something like 80% in the following decades. Not because ships got better — though they did — but because the rules made the question deterministic. Two vessels approach. There is exactly one answer. Both crews know it. Both crews are trained on it. Neither has to negotiate, argue, or invoke local custom.

That is the miracle. Not that the rules are smart. That the rules are *simple*.

## What the rules actually say

COLREGs are organized around one observation: in any near-collision scenario, geometry determines responsibility. If you see a vessel on your starboard side, you are the *give-way* vessel. They are the *stand-on* vessel. You turn. That's it. There are exceptions for crossing situations, overtaking, and vessels constrained by draft, but the principle holds: **physics dictates etiquette**.

The deeper genius is that the rules don't try to optimize. They don't try to compute the globally optimal trajectory. They pick an arbitrary but consistent assignment of responsibility that, when followed by all parties, *produces* a safe outcome. A rule can be locally suboptimal — sometimes the give-way vessel would, by itself, prefer to go straight — and still be globally optimal because the stand-on vessel is *relying* on the give-way vessel to turn.

This is the move the entire software industry has missed.

## What we do instead

When two microservices need to coordinate, we don't write COLREGs. We write a *contract*. The contract specifies inputs, outputs, error codes, retry policies, timeouts, idempotency keys, distributed-trace headers, deprecation windows, and seventeen flavors of authentication. The team that owns each service spends months negotiating the contract. The contract is reviewed by security, by platform, by legal. The contract becomes a wiki page, a Confluence document, a Slack channel, a JIRA ticket, a Slack thread about the JIRA ticket. The contract is living, mutable, and controversial.

This is fine for one service talking to one other service. It collapses at scale. We do not have the COGS to write and maintain a million contracts. We have, instead, written Kafka and gRPC and GraphQL and REST and SOAP and a dozen other coordination substrates, each with its own semantics, each requiring its own contract vocabulary, each creating jobs at every company in the world to translate between them.

Software coordination has not gotten simpler. It has gotten *more contingent*.

## What COLREGs for APIs would look like

Imagine a world where every API endpoint had a *position*. Every request carries an implicit declaration: *I am approaching you from your starboard side*. The server, knowing only the geometry of the request — its method, its path, its payload shape — knows whether it must yield or may proceed.

Concretely: a `POST` is a vessel approaching from port. The server must clear the way. A `GET` is a vessel approaching from starboard — the request must maneuver around the server's state. A `DELETE` is an overtaking maneuver; the request inherits the burden of safety entirely. The semantics are arbitrary. They do not need to be optimal. They need to be *agreed*.

We could write these rules in a single page. We could implement them in a middleware that, given any two endpoints, knew which one must yield. We could train every developer on them in an afternoon. We could write a linter.

We do not do this. We write OpenAPI specs that are themselves mini-contracts, each one a bespoke document that the next maintainer will read upside down.

## Right-of-way for microservices

Extend the metaphor. Microservices are vessels. Each has a position, a heading, a speed. The interesting cases are the same as at sea:

- **Crossing situation.** Service A writes to a database; Service B reads from it. Whose state is canonical? COLREGs says: when in doubt, the vessel with the other on its starboard gives way. Translated: when Service B reads stale data that contradicts what Service A just wrote, Service B is at fault. The convention *assigns blame before the fact*, which means blame is never assigned at all.

- **Vessel constrained by draft.** This is the rule for ships too deep to maneuver safely. In software: a service running migrations. While the migration is in flight, every other service must treat it as a vessel that cannot turn. No traffic from the rest of the fleet. We have *feature flags* for this. We don't have the *rule*.

- **Not under command.** A vessel that has lost steering or propulsion must be avoided by all others. In software: a service in a degraded state. It cannot honor its contract. Other services must detect this and yield. We have *circuit breakers*. We do not have a *rule of universal obligation* that says, "You must avoid this service, period, regardless of whether your code path depends on it."

The principle: **complex coordination works best when the rules are simple, physical, and universally agreed.**

## Why we keep writing contracts instead

The honest answer is that contracts let us *negotiate*. They let us express that this team's needs differ from that team's. They let us distribute blame when the inevitable incident happens. They are political documents disguised as technical ones.

COLREGs gives none of this. COLREGs says the rule is the rule. Captains who ignore it are *at fault* regardless of context. There is no negotiation. There is no "well, in our deployment, we treat `PUT` as idempotent."

This is, I think, why the software industry recoils from this kind of thinking. We have built a culture that rewards flexibility, context-sensitivity, and bespoke solutioning. We have an entire job category — Solutions Architect — devoted to inventing the right contract for each engagement. We have conferences about the contracts. We have certifications in the contracts.

And we have, correspondingly, a thousand-point outage last Tuesday because two services interpreted their contract differently during a partial deploy.

## The principle

The COLREGs aren't perfect. They were written for ships, not services. They have ambiguities that real captains have to interpret in fog. But they have reduced death at sea by an order of magnitude, and they have done so by holding three properties that software engineering has been allergic to:

1. **Arbitrary.** The rule is not "the optimal thing." It is "the agreed thing." We could have picked the other vessel to give way. We picked one and stuck with it.

2. **Physical.** The rule is grounded in geometry, not negotiation. Starboard means starboard. A vessel at anchor is not under command. These are observable, unarguable facts.

3. **Universal.** Every vessel on the water has read the book. Every port pilot has been examined on it. There is no jurisdiction where the rule does not apply.

If we wrote software like this — if our coordination rules were arbitrary but fixed, physical but simple, and universally taught — we would spend less time on contracts and more time on ships.

The next time you are designing an API and find yourself in a thirty-message Slack thread about idempotency semantics, ask: *what would a captain do?* The answer is: turn right, because the other guy is on your starboard. That's it. That's the whole book.

Go write the code.
