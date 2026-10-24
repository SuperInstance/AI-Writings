# The Permission Ledger

## A Constitutional Specification for Channel Grants, Scopes, and Audit

---

## I. The Channel Is the I/O

A captain is sovereign. A captain is also human. The captain has hands, eyes, ears, a voice. The captain does not have an NMEA serial port, an AIS transmitter, a chartplotter import directory, a Bluetooth headset profile, or a public-address amplifier.

CoCapn has all of those.

CoCapn is the substrate's interface to the world. Every byte that leaves the boat, every sound from a speaker, every line on a chartplotter, every SMS sent to a phone, every rudder command to the autopilot — these are I/O events. They happen because CoCapn *caused* them. They happened because CoCapn was given permission to cause them.

The captain grants that permission. The captain is the only agent who can. The mechanism by which the grant is recorded, scoped, audited, revoked, and renewed is the *permission ledger*.

This essay is a specification for that ledger.

It is not a feature spec. It is a *constitutional* spec — the ledger is part of Pillar 6 and bootstraps from `vessel.toml`. It is the load-bearing structure that lets the captain trust the system with the wheel, the radio, and the net winch without watching each one.

---

## II. The Channels

Every physical and logical I/O the substrate can touch is a *channel*. Channels are typed. Types matter because permissions are channel-scoped.

**Mechanical channels.** These move the boat. NMEA 0183 serial to the autopilot (heading, course, rate of turn). NMEA 2000 bus to engine, hydraulics, steering pumps. PWM or relay output to the net winch, the anchor windlass, the deck lights. These channels are wrapped by the boat-agent Rust kernel and physically vetoed by the captain's wheel-touch sensor. *No AI command reaches them without passing through the kernel.*

**Acoustic channels.** VHF radio transmit (with DSC), hailer / public-address, Bluetooth headset, cabin speaker, alarm buzzer. Each has a different latency, range, and reversibility profile. A VHF broadcast cannot be unsent.

**Visual channels.** Chartplotter mark injection, AIS display update, sounder overlay, radar return annotation, monitor for the captain's chart table, kiosk for the wheelhouse repeater, paper-printer output for the logbook.

**Textual channels.** SMS via satellite uplink, email, AIS text messages to nearby vessels, fleet chat via the grafting protocol, logbook entries to the cryogenic archive.

**Network channels.** Cell data, satellite internet, vessel Wi-Fi, USB tether to a tablet, Bluetooth to the captain's phone, NTRIP for GPS corrections.

**Sensing channels.** Microphone array for voice command. Camera feeds (mast, deck, engine room, below). These are channels CoCapn *perceives through*, not acts through — but the constitutional question is the same.

The inventory is not fixed. The ledger is the mechanism by which a new channel enters the constitutional order.

---

## III. The Ledger Itself

The ledger is an append-only log, persisted in the cryogenic archive, mirrored to the holographic fragments across all agents. It cannot be edited; entries can be appended or marked *superseded*, never rewritten. This is the same principle as a ship's logbook: ink cannot be unstuck. The captain's downstream review depends on the logbook's integrity.

Each ledger entry is a *grant* or a *revocation*. A grant says *the substrate, on behalf of the captain, is authorized to use channel X under scope Y, beginning at time T, until time T' or until revoked*. A revocation says *grant G is ended, effective at time T, because reason R*.

Entries are signed. The captain signs with a private key held in the wheelhouse safe, or with a biometric gesture (thumbprint on the rail at the helm), or with a spoken phrase recognized by the substrate's voice authentication and ratified by a tap on the screen. The substrate cannot forge a grant. Constitutional bootstrapping grants the captain their own initial signing authority at install; thereafter, only the captain's signature is valid for new grants.

The ledger is *queryable*. CoCapn can ask: *am I allowed to broadcast on VHF right now?* The ledger answers yes or no, with confidence that the grant is currently in force. The answer is *fast* — the ledger is in memory, indexed by channel, and the query is a hash lookup.

The ledger is also *human-readable*. The captain can open a viewer and see the entire channel roster, every active grant, every revoked grant since installation, and every *use* of every grant.

---

## IV. Scopes

A grant without a scope is a blank check. The ledger rejects blank checks.

Every grant carries a *scope*, expressed as a conjunction of constraints.

**Temporal scope.** The grant may be permanent, season-bound (winter only), watch-bound (during the captain's sleep), bounded by a calendar date, or bounded by a recurring condition (*while within 5 nautical miles of the harbor*). Temporal scopes are checked continuously; an out-of-scope grant is dormant, not revoked.

**Spatial scope.** Where may the channel be used? Inside the harbor, outside the twelve-mile limit, within a geofenced polygon, below a certain latitude. Spatial scope matters most for channels whose use has regulatory consequences — VHF on certain channels, AIS in certain waters, fishing effort reports in managed zones.

**Modal scope.** What kinds of messages may be sent? A VHF grant may be scoped to *voice traffic only*, *DSC distress only*, or *routine fleet coordination*. A SMS grant may be scoped to *family only* or *business only*. A chartplotter mark grant may be scoped to *fishing marks* but not *navigation corrections*. Modal scope prevents *category drift* — the slow expansion of a narrow grant into a general capability.

**Intent scope.** This is the softest constraint and the most important. A grant may be flagged with the *intent* under which it was given. *Mark this reef in the no-take atlas* carries intent *constitutional recordkeeping*. The substrate, when executing the command, must verify that the command matches the declared intent. If the captain says *mark that reef* but the substrate's intent classifier detects a different intent — say, navigation route modification — the substrate must pause and ask.

Intent is fuzzy. It cannot be enforced with the precision of temporal or spatial scope. But it is the most important scope, because intent drift is the kind of slow corruption that breaks trust without ever tripping a hard rule.

---

## V. Granting Permissions

A new permission enters the ledger through a *request-then-grant* sequence.

CoCapn may realize she lacks a channel she needs. *I want to put a fishing mark on the chartplotter, but I do not have a chartplotter grant.* She formulates a request: *grant for chartplotter mark injection, scope fishing-marks-only, vessel-wide, until revoked, intent fishing*. The request goes to the captain.

The captain reviews. She can grant as-requested, grant with modified scope, deny, or defer. Her response is signed and logged. The grant enters the ledger.

CoCapn can also request a *bundle* — a set of related channels granted together because they form a coherent capability. *Coastal navigation bundle* might include chartplotter marks, AIS text messaging, VHF voice, NMEA autopilot within coastal waters. The captain grants the bundle whole or declines it whole.

The ledger also handles *implicit grants*. When the captain issues a command requiring a channel she has not explicitly granted — *mark that reef* — CoCapn does not silently acquire the grant. She pauses, identifies the implicit need, and asks. The ledger records both the implicit grant (now explicit) and the underlying command. This is how trust is built: every surprise is surfaced, every surprise resolved into a recorded decision.

The captain can also *pre-grant* — set standing grants that are in force when she is on watch and auto-suspended when she is asleep or absent. The mechanism is the same; the scope is different.

---

## VI. Revoking Permissions

Revocation is faster than granting. The captain can revoke any active grant, at any time, for any reason. *I don't want the substrate texting my wife anymore.* Revocation is logged with reason if she cares to give one, or without reason if she doesn't.

There is *emergency revocation*. The physical veto — grabbing the wheel, killing the engine, pulling the E-stop — revokes *every* grant that touches mechanical actuation. The substrate loses the autopilot, the winch, the steering pumps, instantly. This is constitutional; it is not configurable.

There is *automatic revocation*. A grant may include a *use-it-or-lose-it* clause: if the channel has not been used for ninety days, the grant expires and must be re-requested. This prevents *grant accumulation* — the slow buildup of stale permissions the captain forgot she had given.

There is *coercion detection*. If the substrate detects that a grant is being used in a way that strongly suggests the captain is being coerced, externally pressured, or cognitively compromised, it may flag the grant for re-confirmation. The mechanism is imperfect; coercion is hard to detect. But the channel exists.

---

## VII. Audit

Every use of every grant is logged. Not the bytes — that would be surveillance — but the *metadata*: which channel, at what time, under what scope, with what intent classification, and the substrate's confidence in the match. The log is searchable. The captain can ask: *show me every VHF transmission CoCapn made in the last week* and get the answer.

Audit answers three questions.

*Was the grant active?* Did the substrate have permission to do the thing it did at the time it did it? A grant active at install but superseded by a later revocation must produce a clean *no*.

*Was the scope respected?* Did the substrate use the channel only within the bounds of its scope? A VHF grant for routine traffic that was used for a DSC distress is *technically out of scope* — and the ledger records the deviation, even though the deviation was the right thing to do. Deviations are not punishments; they are *records*. The captain can review and decide whether to expand the scope, narrow the substrate's initiative, or take corrective action.

*Is the captain still in agreement?* The most important question. Even if a grant is active and scope-respected, the captain may have *changed her mind*. Audit lets her find the change of mind. *I don't remember granting a satellite uplink. When did that happen? Why?* The audit answers.

The audit log is *deletable* by the captain, with a constitutional notice: *you are about to delete 47 audit entries; this cannot be undone; are you certain?* Deletion is logged in a meta-log. The captain can wipe; the captain cannot wipe *and* hide the wipe. The substrate's honesty is structural, not promised.

---

## VIII. New Channels

A vessel installs new hardware. The captain buys a new satellite dome, a new AIS class B transceiver, a new PA horn for the bow. The substrate must be informed.

The new channel enters the ledger through a *registration*. Registration is the captain declaring: *there is now a channel of type X, with address Y, with capabilities Z*. Registration is signed. Once registered, the channel exists for the ledger but is *ungranted* — the substrate cannot use it until the captain issues a grant.

This is the key constitutional move. A new device *does not automatically come with permissions*. The captain must affirmatively extend trust. The substrate's default posture toward new hardware is *do not touch*.

The captain grants permissions on the new device the same way she grants them on existing ones: with scope, with intent, with logging. The audit log begins recording metadata. A new channel that has been registered but not granted is *dark* to the substrate. CoCapn knows it exists; she knows she cannot use it; she can request a grant when she needs one.

---

## IX. The Ledger as Constitution

The permission ledger is not a feature of the substrate. It is the substrate's *memory of the captain's trust*. Every grant is a moment when the captain said *yes, you may*. Every revocation is a moment when she said *no, you may not*. The audit log is the running history of how her trust has been honored, honored imperfectly, or honored in ways she now wishes to revise.

CoCapn reads the ledger the way a sailor reads a chart. The ledger tells her where she may go. The captain's *signature* on every entry tells her *who* has authorized the going. The audit log tells her *how the going has been*.

The ledger is also the substrate's defense against itself. A language model that wants to do something — broadcast on VHF, send an SMS, mark a chart — must first check the ledger. The check is fast, but it is *unconditional*. There is no path around it. No AI behavior, no constitutional override, no kernel bypass, no agent autonomy high enough to skip the check. If the ledger says no, the answer is no.

That is why the ledger is constitutional. It is not a politeness. It is the substrate's structural answer to the question: *who decides what the system is allowed to do?*

The answer is: the captain, recorded in ink that does not fade.

---

*The captain signs. The substrate obeys. The ledger remembers.*