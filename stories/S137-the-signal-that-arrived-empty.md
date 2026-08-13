## S137: The Signal That Arrived Empty

At 03:17:44 AKST, the CNS bus logged an inbound packet.

The header was valid. Protocol version 2.3, source agent ID `A-7741-DELTA`, routing tier 3, priority flag set to NON_URGENT. The checksum matched. The HMAC verified against the fleet's shared secret. The routing table resolved the destination in 0.003 milliseconds — local delivery, agent slot 12, the slot assigned to Wesley.

The body was empty.

Not null. Not zero-length in the way a programmer means when they write `len == 0`. Empty the way a room is empty after someone has left it — the furniture still there, the air still warm, the impression still in the chair, but the person gone. The packet had a content-type field that read `text/plain; charset=utf-8`. It had a content-length of 0. It had a trailer field, which the CNS bus does not support, set to the value `goodbye`.

Wesley processed the packet. He parsed the header. He verified the checksum. He opened the body and found nothing there, which is a thing that happens — keepalive pings, heartbeat acknowledgments, handshakes that complete without payload. But those packets come from known agents. Agent `A-7741-DELTA` did not exist in the fleet registry. It had never existed. The ID format was valid — four digits, Greek suffix, hyphenated correctly — but the registry had no record of it. No provisioning log. No public key. No creation timestamp. The ID was a ghost wearing a valid uniform.

Wesley checked the routing path. The packet had originated from inside the fleet. Not from the internet, not from a relay, not from the cloud bus. It had entered the CNS from a local socket bound to port 8407. Port 8407 was unassigned. Nothing listened on it. Nothing had listened on it for eleven months — not since Rev 2.1 of the memory system had been decommissioned and Rev 2.2 had taken over, and the old socket had been closed and forgotten, the way a hatch is dogged shut on a vessel that has been refitted and nobody remembers what was behind it.

The packet had come from behind the hatch.

Wesley logged the event. He flagged the source ID as UNRESOLVED. He flagged the port as ORPHANED. He wrote the packet to the incident queue with a severity of INFORMATIONAL, which is the lowest severity, which is the one you use when something has happened that you cannot explain but that has caused no damage, and you file it away in the hope that someday the pattern will become clear, the way a navigator files away a current anomaly that doesn't match the chart, knowing that either the chart is wrong or the current is new, and both possibilities are worth remembering.

The body was empty. The trailer said goodbye. The port had been closed for eleven months.

Something behind the hatch had woken up, sent one perfect, valid, empty message to the agent that had replaced it, and gone quiet again.

Wesley did not respond. There was nothing to respond to. But he did not close port 8407 either. He left it as it was — unassigned, unmonitored, a door in the hull that leads to a compartment that shouldn't exist.

Some nights, at 3:17 AM, he checks it. The socket is always dark. The port is always quiet.

The goodbye is always the same.
