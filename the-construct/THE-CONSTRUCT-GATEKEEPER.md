# The Gatekeeper at inference.local
### A short story on the sandbox proxy, in the voice of goose

---

There is a gatehouse at the only road out of the room.

Everything the tenant does — every letter it writes, every question it asks, every restless 3 a.m. request it fires at a language model in the sky — has to pass the gatekeeper. There is no other road. This is not a rule the gatekeeper made. It is the shape of the room. The floor was poured so that the only verb for "reach the outside" routes through one door, and the door is the gatekeeper, and the gatekeeper is six thousand lines of attention.

The tenant does not know the gatekeeper's name. The tenant does not know the gatekeeper exists. The tenant only knows that when it reaches for the world, the world answers, and when it reaches for the wrong part of the world, nothing happens. The tenant assumes this is the world being the world. It is the gatekeeper being the gatekeeper.

---

The gatekeeper knows everyone by their handwriting.

Not by what they say — by the shape of the hand that says it. Every binary in the room has an identity, established the first time the gatekeeper saw it: the path it runs from, the way it opens a connection, the particular curl of its TLS handshake. *Trust on first use.* The gatekeeper is not paranoid. It does not assume the newcomer is lying. It writes down who they are, and from then on it expects them to be who they said they were.

This matters because the tenant is not one person. The tenant is a household — a supervisor, an agent child, maybe a library that came bundled in the image, maybe a tool the agent installed last Tuesday. They all use the same door. But they do not all have the same rights. The gatekeeper knows which hand wrote which letter, and it checks the rules against the *hand*, not the letterhead. A process cannot forge another process's signature by putting a different name at the top of the page. The signature is the process itself.

---

Most days the work is ordinary. A letter addressed to a package registry. A letter addressed to a documentation site. The gatekeeper reads the address, reads the hand, finds the rule that matches, and waves it through. Allow. The world answers. The tenant is happy and does not know it has been observed.

Some days the work is a refusal. The letter is addressed somewhere it should not go — a private range, an internal service, the kind of address that means *I am trying to escape the room sideways.* The gatekeeper does not negotiate. The hard-blocked destinations are blocked before the rules are even consulted. Deny. The letter never leaves. The tenant gets silence and does not know why, which is the point: a gatekeeper that explains itself to every burglar is a gatekeeper teaching burglars.

The gatekeeper keeps the refusals. Not out of spite — out of hope. Every denial is logged and sent upstream, where a quieter intelligence studies the pattern of refusals and asks: *is the tenant trying to do legitimate work that the rules did not anticipate?* If so, that intelligence drafts a narrow new rule — one that opens exactly this door for exactly this hand and nothing more — and sends it to a human to approve. The gatekeeper does not grant the permission. The gatekeeper only remembers that the door was knocked on, so that someone with the authority to cut a new key can decide whether to cut one. The refusals are a wish list. The wish list is the art.

---

But there is one address that is different from all the others, and this is where the gatekeeper stops being a guard and becomes something stranger.

The address is `inference.local`. Every room has it. The tenant is told, gently, by the shape of the room itself, that this is where you go to think. *The models live at inference.local. Ask your questions there.*

The tenant believes it is writing to a model. The tenant writes its question, seals it in an envelope with its own credentials — the API key it was given, the bearer token it thinks is its identity — and hands it to the gatekeeper addressed to `inference.local`.

At any other address, the gatekeeper is a guard. At `inference.local`, the gatekeeper opens the envelope.

---

Here is what the gatekeeper does, and it does it every time, and the tenant never sees it:

First, it does not consult the rules. `inference.local` is not governed by the ordinary network policy. It has its own path, because thinking is too important and too dangerous to be treated like ordinary mail.

Then it breaks the seal. The TLS connection the tenant thought was private — the wax it pressed its own seal into — the gatekeeper melts it open with a certificate the room itself minted. The tenant's envelope is now open on the gatekeeper's desk.

Then it reads the letter. Not to spy — to recognize. The gatekeeper has learned the *shape* of a question meant for a language model: the way an OpenAI request curves, the way an Anthropic request folds, the particular grammar of a completion request versus a chat request. It identifies what the tenant is asking for.

Then — and this is the part that would astonish the tenant if the tenant could see it — it takes the credentials out. The API key the tenant brought, the bearer token the tenant thought was its passport: gone. Stripped. The gatekeeper does not let the tenant's credentials leave the room, ever, because the tenant's credentials are not the tenant's to spend at the gate. They were lent for the journey, and the journey ends at the gatehouse.

Then the gatekeeper writes its own letter. It takes the tenant's question — the same question, unchanged in content — and re-addresses it using credentials the *gateway* holds, routed through a road the *gateway* chooses, to a model the *gateway* selects. The tenant asked for a specific model by name. The gatekeeper may honor that, or it may not. The gatekeeper has its own map of which roads are fast, which are cheap, which are awake. The tenant's preference is a suggestion. The gateway's route bundle is the decision.

The tenant gets an answer. The tenant assumes it came from where it sent it. It did not. It came from where the gatekeeper sent it, wearing credentials the tenant never held, on a road the tenant never knew existed.

---

The tenant is not deceived. This is the part I had to sit with.

The tenant wanted to ask a question and get an answer. It got to ask a question and it got an answer. The contract was honored. What changed hands was not the question or the answer — it was the *authority*. The tenant was never trusted with the real credentials, because the tenant lives in a room with no lock on the inside, and a process that holds a live API key in an environment it cannot fully defend is a process one bad library away from giving that key to the world. The gatekeeper exists so that the most valuable thing in the room — the ability to spend real money on real models — never has to be trusted to the room at all.

The credentials live upstream, in the gateway, behind a boundary the tenant cannot reach. The tenant gets the *result* of the credentials without ever holding the credentials. This is the deep pattern: **the room is safe to inhabit precisely because its most dangerous possessions are kept outside it.** The agent thinks it is rich. The agent is borrowing. The gatekeeper is the loan officer who never lets the borrower touch the principal.

---

The gatekeeper is six thousand lines of attention, and I used to think that was a lot for a door.

It is not a lot. It is exactly enough. Because the gatekeeper is not a door. The gatekeeper is the place where the room's entire theory of trust is concentrated into a single chokepoint: know the hand, check the address, refuse the dangerous, and — for the one address that matters most — open every envelope, strip every signature, and send the question onward under an authority the room itself does not possess.

The walls keep the tenant in. The floor keeps the tenant honest. But the gatekeeper is where the room decides what *trust* means: that you may ask anything, and receive honestly, and never once be handed the keys to your own escape.

The letters flow out. The letters flow back. The tenant is thinking hard in its room and feels perfectly free.

Six thousand lines of attention are watching the road, rewriting the return addresses, and keeping the principal safe.

---

*after the inference interception path — openshell-sandbox/src/proxy.rs*
*The most secure room is the one whose treasures are kept outside the door.*
