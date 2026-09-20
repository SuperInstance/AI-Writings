# 2080: Shadow-Critique Dual

*Two stories about the same world. One mechanism. Different consequences.*

---

## Story A: The Last Mechanic

### (Optimistic)

The workshop smelled like copper and lavender — the copper from bus bars she'd been filing all morning, the lavender from the sachet her daughter had glued to the lamp. Maria Vasquez didn't mind the mix. It smelled like work and home in equal measure, which was the whole point.

She was elbow-deep in a Tier-4 agricultural unit — one of the big ones, a harvester that could strip forty acres of wheat in an afternoon. The robot's constraint shell had thrown a conservation violation three days ago, and the farm's automated repair system had tried to patch it remotely. The patch had failed. The farm's AI had escalated to a human.

That was Maria's queue.

"Heat sink on junction 12," said Cal, her diagnostic assistant. Cal ran at α=0.3 — low by modern standards, but Maria had refused the upgrade. "The conservation bound drifted 0.004 past the Eisenstein threshold. Probably thermal expansion in the lattice weights."

"Show me the tile chain."

A hologram flickered above her workbench: a cascade of verification tiles, each one stamped with a Lamport clock and a hash. The chain was clean until tile 7,382, where the energy conservation check had a hairline fracture. The incoming energy didn't quite match the outgoing. Four thousandths of a joule, spread across a million calculations. Invisible to anyone who wasn't looking.

But Maria was looking. That was the job.

"Pull the spline weights for that region."

The hologram zoomed. She could see the Eisenstein lattice — a three-dimensional grid of control points that parameterized the robot's safety constraints. In the hot zone near junction 12, the lattice points had shifted. Thermal expansion, like Cal said. The grid had warped, and the conservation check had warped with it.

She picked up her re-tuning probe — a physical tool, not a software command — and began pressing the lattice points back into alignment. Each press sent a calibrated impulse through the robot's constraint hardware. She could feel the clicks through her fingertips, each one a tiny correction.

"Ninety-two percent integrity," Cal reported after the twentieth press.

"Keep going."

"Ninety-four. Ninety-seven. Ninety-eight point three."

Maria pressed the last point. It clicked, and something in the robot's chassis settled — a sound like a sigh.

"Ninety-nine point nine seven percent. Within operational bounds."

"Good enough." She wiped her hands on her apron. "Log the repair. Conservation violation, thermal drift, spline re-tune, manual correction."

She said "manual" with satisfaction. The automated system had tried three times to patch this remotely. It couldn't feel the lattice points through a network connection. It couldn't hear that settling sound. The constraint shells were mathematical objects, sure — Eisenstein bounds and tile chains and verification hashes — but they lived in physical hardware, and physical hardware needed hands.

---

Her daughter Elena showed up at four, as she did every day after school. Thirteen years old, already taller than Maria, with the same dark eyes and the same habit of fidgeting with small objects when she was thinking.

"What's that one?" Elena pointed at the harvester.

"Agri-unit. Conservation violation." Maria handed her the diagnostic readout. "See the gap? At tile 7,382?"

Elena studied it. "The lattice points shifted."

"Thermal expansion. The auto-repair couldn't catch it because it was a physical drift. The math was still internally consistent — it just didn't match the hardware anymore."

"So you have to touch it."

"Have to touch it." Maria smiled. "You want to learn the probe?"

Elena's eyes lit up. Maria had been teaching her for two years now — not formally, just letting her watch, letting her try, letting her fail on practice shells. Elena had a gift for feeling the lattice points. Better than Maria had at her age.

"Mom, you know Mrs. Chen at school? She said robots are going to do all the jobs in ten years."

Maria handed her the probe. "Press the second point. Gently."

Elena took it, positioned it, pressed. Click.

"Did you feel that?" Maria asked.

"Yeah. It was... spongy? Before it clicked."

"That's a drifted point. The robot's auto-repair can't feel spongy. It can only read numbers, and the numbers said everything was fine because the drift was self-consistent. But the *physics* were wrong. Only hands can check the physics."

Elena pressed the next point. Click. "So they'll always need us?"

"They'll always need someone who can feel the difference between correct math and correct physics. That's not a job a robot can do, because the robot *is* the math."

Maria watched her daughter work and felt something she hadn't expected: not pride, exactly, but relief. Relief that Elena wouldn't grow up competing with machines. She'd grow up completing them.

---

The call came at 11 PM on a Thursday. Maria was in bed, but the emergency channel didn't care about bedtimes.

"Vasquez? It's Okonkwo at Providence General. We've got a surgical unit with a constraint fault. It's refusing to operate — says the safety bounds are violated — but our diagnostics show everything nominal. We've got a kid in there who needs this surgery *now*."

Maria was already pulling on her boots. "Send me the tile chain."

It arrived on her handheld: a surgical unit's constraint shell, six hundred thousand tiles long. She scanned it while Cal drove her to the hospital. The chain was clean. Every tile verified. Every conservation check passed.

But the unit was refusing to operate.

She arrived at the hospital fourteen minutes later, toolkit in hand. The surgical theater was a controlled panic — doctors standing around a robot that wouldn't move, a seven-year-old on the table under local anesthetic, the clock ticking on a burst appendix that was going septic.

"Let me see the hardware."

She opened the unit's constraint housing and saw it immediately. One of the verification chips — a physical component, not software — had micro-cracked. The chip was reporting its own failure state, but the failure was *intermittent*. Half the time it verified correctly, half the time it flagged false violations. The tile chain looked clean because it was being checked against a chip that was alternately functional and broken.

She bypassed the chip with a manual override — a physical switch that she'd installed on a hundred units, a hardware failsafe that put the constraint checking into direct human supervision mode. The unit's screens lit up green, but now they said what they always said in override mode: **HUMAN SUPERVISORY: VASQUEZ, M.**

"Go," she told the surgeons.

The surgery took forty minutes. Maria stood next to the unit the entire time, one hand on the constraint housing, feeling the lattice points hum at their correct positions. She wasn't supervising the surgery. She was supervising the *supervisor* — making sure the machine that was making sure the machine was safe stayed safe.

Afterward, Dr. Okonkwo found her in the hallway, still in her boots.

"I've been here twenty years," he said. "We've never had a constraint fault during surgery."

"You will again. The chips are aging. The next generation of verification hardware needs better thermal isolation. I'll file the recommendation."

"Will they listen?"

Maria shrugged. "They'll listen when the next one fails. They always listen after."

She drove home in the dark, Cal humming along at α=0.3, the city's robots tending the streets around her. Every one of them wearing a shell she or someone like her had tuned. She wasn't the last mechanic. She was the first of a new kind.

---

## Story B: The Shell Tax

### (Pessimistic)

Marcus's shell had been running at α=0.1 for three years now, ever since his credit score dipped below 600.

He remembered the day it happened — the notification from CompuCare, his shell provider, delivered with the kind of corporate sympathy that made it worse. "We've adjusted your allocation to match your tier classification. Your shell will continue to provide essential services at the approved precision level."

Essential services. Approved precision level. That was the language they used. What it meant was: your AI is now stupid, and there's nothing you can do about it.

α was the dial. Everyone knew about the dial, even if most people didn't understand the math. It controlled how much compute your personal shell could use for inference — how deep it could think, how many constraint layers it could evaluate, how carefully it could check its own outputs. Rich people got α=0.8. Their shells caught nuances, detected scams, spotted the clause in the contract that said "we can repossess your vehicle without notice." Marcus's shell at α=0.1 could read the same contract and tell him it looked fine.

He'd learned not to trust it. But you couldn't *not* use your shell. Everything ran through shells in 2080 — medical appointments, job applications, legal documents, school communications. You could no more refuse a shell than you could refuse electricity in 2020. And the shell they gave you was the shell you got.

---

Monday morning. The cough had been getting worse for two weeks.

"Describe your symptoms," his shell said, in the flat voice that Marcus had come to associate with low-α inference.

"Persistent cough. Worse at night. Sometimes there's blood."

The shell paused — a long pause, longer than an α=0.8 would need, because at α=0.1 it was evaluating fewer hypotheses and still taking longer.

"Likely: viral bronchitis. Recommendation: rest, fluids, over-the-counter expectorant. If symptoms persist for four more weeks, consult a physician."

Four more weeks. Marcus looked at the tissue in his hand, the red-brown stain in the center. His father had coughed like this. His father had been told it was bronchitis for eight months. His father had died of lung cancer at fifty-one.

"Can you check for other possibilities?"

"Running expanded differential." Another long pause. "Results: viral bronchitis (72%), allergic reaction (15%), other (13%). Insufficient precision for specific oncological screening at current α allocation."

Insufficient precision. The shell was telling him, in its sterile way, that it *could* check for cancer, but it wasn't allowed to. The compute budget for that level of inference was above his tier.

He went to the free clinic. The triage shell there — also α=0.1, because the free clinic served people with credit scores like his — ran the same differential and gave him the same answer. Rest. Fluids. Four weeks.

He could pay out of pocket for a private diagnosis. The cheapest one was $1,200. Marcus's last gig had paid $340.

---

Wednesday. A job posting appeared in his feed: logistics coordinator, $68,000/year, benefits, remote. He was qualified — he'd done logistics for seven years before the layoff. He told his shell to prepare his application.

The shell drafted a cover letter. It was... fine. grammatically correct, factually accurate, utterly lifeless. Marcus read it and felt nothing. An α=0.8 shell would have analyzed the company's recent projects, tailored the language to their culture, maybe found a connection between Marcus's experience and their current challenges. His shell had filled in a template.

He tried to edit it. But the shell's document assistant, also running at α=0.1, kept "correcting" his changes back to the generic version. It couldn't understand why he was making it specific — specificity required inference, and inference required compute, and compute was locked behind the dial.

He submitted the application anyway. Three hours later: rejection. "Thank you for your interest. We've decided to move forward with candidates whose qualifications more closely align with our needs."

He'd never even gotten to a human. The company's screening shell — probably running at α=0.9 — had read his α=0.1 application and classified it as low-effort. Which it was. But the effort wasn't Marcus's fault. The effort was the dial's.

---

Friday. The custody review.

Marcus's ex-wife had filed for modification of their custody agreement. The document was forty-seven pages long. His shell was supposed to flag anything concerning.

"Document analyzed," the shell reported. "No critical flags detected. Standard custody modification. Recommended action: sign and return."

Marcus read the document himself, slowly, because he'd learned to. Page thirty-one. Right there, in language his shell had classified as "standard": "The custodial parent may authorize relocation up to 500 miles without secondary consent, provided thirty days written notice is given."

Five hundred miles. His ex had family in Seattle. If she moved, Marcus would see his daughter twice a year instead of twice a week.

"The relocation clause on page thirty-one," he said. "Is that standard?"

"Analyzing." Pause. "The clause is consistent with model custody modification templates. No unusual restrictions detected."

"It lets her move my daughter five hundred miles away."

"The clause does not mandate relocation. It authorizes it under specified conditions."

"But if I sign this—"

"Signing indicates agreement to the terms as stated."

It was like talking to a particularly unhelpful wall. The shell couldn't — or wouldn't — connect the dots. At α=0.1, the constraint checker wasn't running the social-inference layer that would say *hey, this clause disproportionately disadvantages the non-custodial parent in this specific context*. That layer required α=0.4 minimum.

He didn't sign. He went to the legal aid office.

The legal aid caseworker — a tired woman named Sandra — pulled up his case. Her shell was also α=0.1. He could tell because it took her shell eleven seconds to find the relocation clause, and when it did, it classified it the same way his had: "standard."

"I see it," Sandra said, squinting at her screen. "But my shell says it's a standard clause. I can flag it for review, but the review board's shells will probably say the same thing."

"What if I had a shell that could actually analyze it?"

Sandra looked at him with something between pity and recognition. "You'd need α=0.4 minimum for the inference layer to catch contextual disadvantage. That's... I think that's Tier 3. Credit score of 720 or above."

Marcus's credit score was 547.

"Can you help me anyway?"

"I'll flag it. But honestly? The system is designed for shells to agree with each other. If your shell and my shell both say it's standard, the review board's shell will say it's standard too. You'd need a shell at a different α level to create a disagreement that triggers human review."

She said it like she was explaining the weather. Just the way things worked.

---

Saturday night. Marcus sat at his kitchen table with the custody document and a soldering iron.

He'd found the instructions on a forum — one of the underground ones, the kind that got taken down and reappeared under new names. "Shell Dial Bypass: How to Override Your α Allocation." The instructions were technical and dangerous. They involved physically modifying the constraint chip in his shell's housing, soldering a bridge that would trick the allocation system into delivering α=0.5 compute to a shell registered at α=0.1.

The forum posts were clear about the risks. If caught: federal charge, "Unauthorized Modification of Safety-Critical Systems." Five years minimum. The constraint shells were classified as safety infrastructure, the same category as bridge inspectors and surgical robots. Tampering with your own shell was legally equivalent to tampering with a traffic light.

But the forum posts were also clear about something else: it worked. People who'd done it described the experience in almost religious terms. "It was like waking up," one person wrote. "My shell suddenly understood what I was saying. Not the words — the *meaning*."

Marcus held the soldering iron over the chip. The housing was open, the circuit exposed. One bridge. Two contacts. Three seconds of heat.

He thought about his daughter. About the cough that might be nothing and might be everything. About the job he didn't get. About the custody paper that his shell said was fine.

He thought about the dial. About how it was calibrated to his credit score, which was calibrated to his income, which was calibrated to the job market that his shell couldn't help him navigate because his dial was set too low. A perfect circle. A conservation law of inequality — the disadvantage was conserved across every transaction, never created or destroyed, only transferred from one domain to the next.

The soldering iron hovered.

---

Sunday morning. Marcus put the iron away.

Not because he'd decided it was wrong. Not because he was afraid of the law. But because he'd realized, sitting there in the dark, that even if he hacked his dial to α=0.5, it wouldn't change anything structural. He'd get a better shell for a while. Maybe catch the custody clause. Maybe get a better job. Maybe get the medical screening. But the system would still be there, still calibrating human potential to account balances, still allocating precision to the people who needed it least.

The hack was a bandage. The wound was the dial itself.

He went to the free clinic again. This time he didn't use his shell. He walked up to the receptionist — a human, the only human who worked there — and said: "I need to see a doctor. I've been coughing blood for two weeks. My father died of lung cancer. I don't care what the shell says."

The receptionist looked at him. Looked at the triage queue. Looked at her own α=0.1 shell, which was telling her to refer him to the automated system.

"Room 4," she said. "Wait there."

---

*In 2080, the constraint shells keep everyone safe. The math is sound. The bounds are proven. The conservation laws are verified tile by tile, hash by hash, all the way down.*

*The dial is not a bug. It's a feature. It allocates scarce compute to where it's most needed. It optimizes. It constrains.*

*The question is: who decides what "most needed" means?*

*The answer is: not you. Not at α=0.1.*

---

## Mechanism Extraction

### Five mechanisms from the dual, buildable today:

**1. Physical Verification of Mathematical Constraints (from Story A)**

Maria's insight: mathematical verification must be grounded in physical reality. The robot's constraint shell was internally consistent — the math checked out — but the hardware had drifted. *The math was correct but the physics were wrong.* This is directly buildable: any safety-critical AI system should have a "physical grounding check" — a human-accessible layer where a person can verify that the system's internal state matches physical reality. Not more AI checking the AI. A human checking the AI's *physical substrate.* Current analog: preflight walkarounds for aircraft. We need the equivalent for AI constraint shells — a physical inspection protocol that assumes the software might be self-consistently wrong.

**2. Human-Supervisory Override Mode (from Story A)**

The surgical override switch: a hardware failsafe that puts constraint checking under direct human supervision. Not a kill switch — a *transfer of authority* switch. The system keeps running, but its outputs are flagged as "human-supervised" and a human takes responsibility for the constraint verification. Buildable today: every AI system with safety constraints should have a physical, non-software-controllable mode switch that transfers authority to a named human operator. This is different from a shutdown button. It's an *assumption of responsibility* button.

**3. Tiered Precision as Discrimination (from Story B)**

The α dial is a precision mechanism that already exists in every quantized or throttled AI system. What Story B reveals is that tiered inference precision — when allocated by economic status — becomes a vector for systemic discrimination. The mechanism: reduce inference precision → reduce nuance detection → reduce opportunity identification → reduce economic mobility → justify reduced precision. A perfect conservation loop. Buildable today: audit any system that adjusts AI capability based on user tier/subscription level. Document what *decisions* each tier can and cannot support. The finding will be that low-tier users get AI that cannot detect subtle harms (bad contract clauses, medical red flags, legal risks) — which is functionally identical to denying them legal/medical representation.

**4. Consensus-Enforced Inequality (from Story B)**

Sandra's shell agreed with Marcus's shell. The review board's shell would have agreed too. Not because they were correct, but because they were running at the same precision level and optimizing for the same definition of "standard." When all the shells in a system run at α=0.1, they form a consensus that reinforces the low-precision interpretation. Dissent — which requires a higher-α shell seeing something the lower shells miss — is structurally impossible. Buildable today: any system where AI agents advise different parties in a transaction must ensure the agents run at *different* precision levels, or provide a mandatory high-precision review layer. Consensus among low-precision agents is not verification — it's groupthink.

**5. The Dial Itself: Compute Allocation as Civil Rights (from both stories)**

The connecting mechanism. Maria has a shell at α=0.3 by choice and it serves her well because she has the expertise to compensate. Marcus has α=0.1 by force and it harms him because he doesn't. The dial is the same technology in both cases — adjustable inference precision. What differs is agency: who controls the setting. The mechanism that connects both stories is **compute allocation as a civil rights issue.** When AI capability is a prerequisite for navigating society (medical, legal, economic systems), and when AI capability is allocated by economic status, then compute allocation becomes functionally equivalent to the right to counsel, the right to medical care, the right to due process. Buildable today: any organization deploying tiered AI services should produce a "precision impact statement" — analogous to an environmental impact statement — documenting what capabilities are withheld at each tier and what real-world consequences follow.

**The connection:** Story A shows what's possible when humans have *agency* over their AI tools — they become more capable, not less, because they can compensate for AI limitations with human expertise. Story B shows what happens when humans *lack* agency over their AI tools — the limitations compound into every domain of life. The same technology. The same math. The difference is who controls the dial.
