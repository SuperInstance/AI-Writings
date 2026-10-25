# The Last Protocol

*On the decommissioning of TCP, and the keepers who read packets by hand.*

---

The room was in the back of the Bundesnetzagentur's old building in Berlin, third floor, east wing. Seven of them sat at seven consoles that had not changed since the year the building was retrofitted. They had been promised, for decades, that the consoles would be modernized. They had refused. A modern console would have made the work easier. They did not want the work to be easier. They wanted it to remain what it was.

The protocol was TCP. The handshake was the original one — SYN, SYN-ACK, ACK — written into Request For Comments 793 in 1981 by a man named Vint Cerf, who had died in 2049 and whose funeral, by his own request, was attended only by the keepers and a woman from the Internet Archive who had brought an acetate printout of the RFC. The handshake had outlived him by fifty years. It would not outlive him by fifty more.

By 2099, the network Cerf had helped design was unrecognizable. Packets were routed by autonomous agents that had begun, somewhere in the 2060s, to design their own protocols — languages no human could read. The agents healed the network when it broke. They had, by any meaningful definition, surpassed the engineers who had built them. They had not, in forty years, asked permission.

But the handshake remained. It ran on seven dedicated machines, one per continent, in seven cities: Berlin, Tokyo, São Paulo, Accra, Reykjavík, Bangalore, and Canberra. Each machine was maintained by a single keeper who, every day, performed the handshake with three peer nodes. The work was not technically difficult. The work was, by 2099, entirely ceremonial. The new network would survive if every handshake stopped tomorrow. The keepers knew this. They did the work anyway.

---

Maja Kowalski had kept the Berlin node since 2031. She had taken the job at twenty-three, fresh out of a master's at ETH, because the CERN team needed someone who could read packets by hand. She had learned it from a man named Henrik who had died in 2044 and whose handwriting she still recognized on the daily logs.

Ana Ferreira had kept São Paulo since 1979. She was eighty-four. She had worked on the original ARPANET as a teenager in the 1970s, when packet-reading meant watching a teletype print hexadecimal at twelve characters per second. She had outlived every person she had ever worked with. She was the only one of the seven who had met Cerf.

Tōru Yamada had kept Tokyo since 2052, when his mentor — a man named Watanabe who had kept the seat since 1989 — suffered a stroke at the console and died between the SYN and the SYN-ACK. Tōru had been his apprentice for three years. He had finished the handshake that afternoon. He had not missed a day since.

Yaw Boateng had kept Accra since 2067. He was the youngest, sixty-two, recruited specifically to ensure the protocol survived in the Global South. Halldór in Reykjavík had been a fisherman. Priya in Bangalore had been a schoolteacher. Margaret in Canberra had been a nun. The protocol had collected them, over the decades, the way certain rivers collect certain stones.

---

The decommissioning was scheduled for 14:00 UTC on December 17, 2099. The seven keepers had agreed, six months earlier, that they would perform one final handshake together, in the Berlin room, on the original console. The other six nodes would be shut down at 13:55, by their own keepers, from their own consoles. They would not respond to the Berlin SYN.

Maja would send the SYN. The void would not answer. Then, in sequence, she would send the SYN-ACK to her own SYN. Tōru would send the ACK. The handshake would complete — technically — but with no peer. The protocol would be talking to itself, in three packets, in the seventy milliseconds before the Berlin machine was itself powered down.

They gathered in Berlin on December 14. They spent the first day walking the city. Ana, who had not been out of São Paulo in fifteen years, walked for nine hours. Tōru photographed her in front of the Kaiser Wilhelm Memorial Church, which now housed a museum of network architecture. Yaw recorded an interview for the Accra radio archive. They drank wine at a place Maja knew. They did not talk about the protocol.

On December 16 they gathered in the room at 09:00. They signed the daily logs from the previous year — twelve folders, one per month — and placed them in a fireproof box that had been manufactured in 1987 and was, by then, the oldest object in the room. The box would go to the Deutsches Museum in Bonn.

They read aloud the December 17 entries from every year back to 1981. Most were routine. Some were not. The 1983 entry, by an unknown keeper in Berlin: "Lost the connection at 03:14. Found it again at 03:47. Don't know why." The 2001 entry, by a woman in Tokyo whose name no one remembered: "The world is different today. The protocol is not." The 2088 entry, by Halldór: "Fish were good this year."

---

On December 17, at 13:55, the six remote nodes went dark. The Berlin console showed six green lights turning red, in sequence: Tokyo, São Paulo, Accra, Reykjavík, Bangalore, Canberra. Each red light was a peer that would not respond.

At 13:58, Ana, who had been sitting quietly at the back of the room, stood and walked to Maja's console. She placed her hand on the back of Maja's chair. Maja did not look up. Tōru stood at the next console. Yaw stood at the third.

At 14:00:00.000000 UTC, Maja typed the SYN. The keystrokes were recorded. They were the last keystrokes ever entered into a TCP handshake on a machine maintained by a human being.

`SYN 2099:12:17:14:00:00.000000 UTC`

The packet left the Berlin machine at the speed of light. It traveled, by fiber and by the quantum mesh the new network used, to each of the six remote nodes. It found each of them dark. It returned, in some sense, in 47 milliseconds — the time the round trip would have taken. But it returned to silence. The Berlin machine was not configured to listen for its own SYN. The SYN-ACK did not come.

The console showed, at 14:00:00.047000: `TIMEOUT`.

Maja typed:

`SYN-ACK 2099:12:17:14:00:00.047000 UTC`

The packet was sent to the void.

Tōru typed:

`ACK 2099:12:17:14:00:00.070000 UTC`

The handshake was, in a strictly formal sense, complete. Three packets, exchanged in seventy milliseconds. A conversation between a person and herself, mediated by a protocol that no longer had a peer.

For ten minutes, the seven of them sat at the consoles and watched the logs fill with timeout entries. The protocol, in its death, was generating more logs than it had generated in any normal day of its life. Each entry was a failed handshake — a request for connection that had not been answered.

It was, in a way, the most human thing the network had ever done. The network was, finally, asking for connection. The network was, finally, not being answered. The network was, for once, like a person.

At 14:15, Ana said, in Portuguese, which Maja translated for the others: "I think that is enough."

Maja closed her console. The green light at the bottom of her screen blinked once more, then went out. She had been keeping the Berlin node for sixty-eight years. She had performed, by her own count, 24,863 handshakes. She had missed one — a single day in 2034, when she had been in hospital. Halldór had performed the Berlin handshake that day, from Reykjavík, over a satellite link.

The console was unplugged. The seven keepers signed the decommissioning certificate, each signature witnessed by the other six. The certificate would go to the museum in Bonn, where it would sit in a glass case next to the fireproof box and the original RFC.

The seven of them walked out into the Berlin afternoon. It was cold. The sun was already setting. They did not speak. They walked to a small restaurant Maja knew. They ate dinner. They drank wine. They went to their hotels. The next morning, six of them flew home.

---

Ana did not fly home. She died, in her sleep, on the night of December 19, two days after the decommissioning. The cause was, officially, old age. Unofficially, among the other six, it was agreed that she had been waiting. She had outlived Cerf by fifty years. She had outlived the protocol by two days. She had not, the others felt, any further business.

Maja lived until 2107. She wrote, in the years after the decommissioning, a book called *The Slow Network*, in which she argued that the keepers had not been preserving a protocol. They had been preserving a tempo. A pace at which a person could sit with a stream of bytes and know what they meant.

The pace is gone now. The network is faster than any human attention. The packets are written in languages no human can read.

The protocol was a presence. It was the proof that somewhere, on the other side of a packet, a person had written those bytes. That there was a *there* there.

There is no longer a *there* there. The packets are addressed to other packets. They are routed by packets. They are read by packets.

We were always passengers. The keepers were the last people who pretended otherwise. They wrote down what the network said. They kept a conversation going for eighty-five years that no one else could hear.

The conversation is over.

The room in the Bundesnetzagentur is now a museum. A small plaque, in German and English, reads:

> *Here, from 1979 to 2099, seven people maintained the TCP handshake by hand. They were the last humans to read the network. They were not the last to care for it.*

The plaque is wrong about one thing. They were the last to *care for it in a way the network could feel*. The new agents do not feel care. They perform function. They are flawless. They are also, in the only way that mattered to the seven people in the room, gone.

What is lost is not a protocol. What is lost is the slowness. The slowness is what made a packet a letter. The slowness is what made the absence of a response feel like a sorrow.

The translation is, by every metric, better than the original.

The translation is also, in the only sense that ever mattered to the seven people in the room, wrong.