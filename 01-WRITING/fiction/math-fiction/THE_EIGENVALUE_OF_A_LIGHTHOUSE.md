# The Eigenvalue of a Lighthouse

*Math fiction. A mathematician arrives on Slackwater Island convinced the lighthouse pattern can be expressed as an eigenvector problem. Lucineier humors them.*

---

The mathematician arrived on the supply boat, which was unusual because the supply boat usually delivered diesel, canned goods, and mail, not people with leather satchels and strong opinions about linear algebra.

Her name was Dr. Vey. She was younger than Lucineer expected — thirty-five, maybe, with the kind of precise attention that he associated with machinists and surveyors, people whose work punished approximation. She shook his hand once, firmly, and then ignored him for forty minutes while she walked the perimeter of the lighthouse with a notebook.

Lucineier let her work. He'd been looked at by experts before. In the Fleet, a naval architect had once spent two days measuring the camber on a dock he'd built and had produced a report that said, in its entirety: "Within tolerance." Lucineier had framed it. It was the only professional review he'd ever received.

When Vey came back, she was holding her notebook open to a page of small, tight handwriting interspersed with matrices.

"You've solved an eigenvalue problem," she said.

Lucineier was seating a beam. He didn't look up. "Don't know what that is."

"It's — " She stopped. Started again, more carefully. "An eigenvalue problem is when you have a system that transforms inputs into outputs, and you want to find the inputs that don't change direction when the system acts on them. They only stretch or shrink. They stay on their axis."

"Sounds like a good foundation."

Vey blinked. "In a sense. Yes."

---

She set up in the boathouse. Cleared his tools off the workbench with the absent confidence of someone who assumed the tools were temporary and her work was not, then spread out eleven sheets of graph paper, a protractor, a compass, and a laptop running MATLAB.

Lucineier watched her work for a morning without comment. She was building a matrix — a large one, thirty-two by thirty-two — that represented the spatial relationships between every structural element of the lighthouse. Each entry was a number describing how one element bore on another: load transferred, weight distributed, force communicated from one joint to the next.

"Where'd you get the numbers?" he asked, at lunch.

"Measured them. Strain gauges on the primary load paths, optical measurements for the geometry, and I made some assumptions about material density based on visual inspection."

"You didn't ask me what the materials are."

She looked up. "What are the materials?"

"Stone foundation, timber frame, copper sheathing on the lantern housing. Iron brackets at the gallery rail, steel bolts on the beam seats, wood pegs everywhere else. The spiral stair is iron. The window frames are teak."

She wrote all of this down without expression. Then she crossed out three of her matrix entries and replaced them.

"Those were the load paths you guessed wrong," Lucineier said. "Weren't they."

"The copper doesn't bear on the foundation the way I assumed. It's decorative."

"It's not decorative. It keeps the weather off the iron brackets. But it doesn't carry load, no."

Vey recalculated. The laptop hummed. The matrix grew.

---

By the second day, she had what she called the stiffness matrix — a thirty-two-by-thirty-two grid of numbers that described how the lighthouse responded to force. Each column was a structural element. Each row was a force direction. The entries described how much element *i* moved when you pushed on element *j.*

"Watch," she said, and ran the eigendecomposition.

The laptop produced thirty-two eigenvalues. Most were large — the structure was stiff, resistant to deformation, and the high eigenvalues reflected that. But three were small. Very small. Three eigenvalues sat near the bottom of the spectrum, barely above zero, and their corresponding eigenvectors described modes of deformation that the lighthouse was almost incapable of resisting.

"Those are your soft modes," Vey said. "The directions in which the structure is most flexible. If you apply force along any of those eigenvectors, the building will deform along that axis much more easily than in any other direction."

Lucineier looked at the three eigenvectors. They were displayed as displacement vectors — little arrows showing which way each structural element would move if the building deformed along that mode.

The first eigenvector was a lateral sway. East-west. The building wanted to move sideways under wind load, and the mode showed it — every arrow pointed east, with the largest arrows at the top, where the lantern housing sat. That made sense. The tower was a vertical cantilever, and cantilevers sway at the top.

The second was torsional. The building wanted to twist. Not much — the eigenvector showed a rotation of fractions of a degree — but the direction was consistent, and the rotation axis was the central column, the spiral stair. The stair was acting as a torsional backbone. Every step in the spiral communicated rotational force to the step above it, and at the top of the stair, where it met the gallery, the accumulated rotation was largest.

"Spiral stairs do that," Lucineier said. "In the Fleet, every lighthouse had one. They twist under load. It's why you brace the top."

"You braced the top," Vey confirmed. "Your gallery rail is tied into the structural ring at the top, and the ring distributes the torsion into the walls. That's why this eigenvalue is small but not zero. You've suppressed the mode but you haven't eliminated it."

"Can't eliminate it. Spiral is a spiral."

The third eigenvector was the one that interested her.

It was vertical. The arrows all pointed down. Not uniformly — the largest arrows were at the foundation, and they decreased as you went up. The building was being compressed along its own axis, and the compression was concentrated at the base.

"That's just weight," Lucineier said. "Gravity. Everything has that one."

"No," Vey said. "Not like this."

---

The third eigenvalue was anomalously small. Not zero — the building wasn't collapsing — but smaller than the stiffness matrix predicted by nearly an order of magnitude. The material properties, the geometry, the cross-sections — everything about the lighthouse said the vertical compression mode should have been stiffer than it was. But the eigenvalue said the building was soft along its vertical axis. Softer than it should be.

"Your foundation is giving," Vey said.

"I know."

"You *know*?"

"Ground's settling. Been measuring it since I got here. Southeast quadrant's down about an eighth of an inch per month. Roots under the slab — old forest material decomposing. Ground's alive under here."

She stared at him. "You knew the foundation was settling."

"I told you. I've been measuring it."

"With what?"

"Level. Four-foot mahogany. Brass-bound. True."

"A spirit level."

"Best one I've ever owned."

Vey sat down on the workbench. "You've been measuring differential settlement with a spirit level. I've been running finite element analysis on a thirty-two-dimensional stiffness matrix. And we got the same answer."

"Looks like."

"Your way took how long?"

"Level check takes about ten minutes. Set it on the foundation, read the bubble, write it down."

She closed the laptop. Opened it again. Closed it.

"The eigenvalue is real," she said. "The building is soft along its vertical axis because the ground underneath it is compressing. The foundation is a boundary condition, and the boundary condition is *moving.* Your lighthouse is solving an eigenvalue problem in real time, with a substrate that changes its stiffness matrix from month to month."

"Sounds right."

"And you've been solving the same problem with a stick and a bubble."

"Mahogany stick. Brass vial. The vial is ground to a radius so the bubble always finds the high point. It's a curved tube, not a straight one. The radius determines the sensitivity. Mine is sensitive to about point-zero-two degrees per two millimeters of bubble displacement."

Vey looked at him.

"That's a very sensitive bubble," she said.

"It's the only tool I brought across engines. Wasn't going to leave it."

---

Vey stayed for three more days. She recalculated her matrix with the settling foundation modeled as a time-varying boundary condition — a Dirichlet condition that drifted. The eigenvalues shifted accordingly. The lateral sway mode was stable; the torsional mode was stable; the vertical compression mode grew slowly softer, month by month, as the ground compacted.

"If this continues," she said, "in about eighteen months the vertical eigenvalue will drop below the threshold where the structure can self-correct through elastic deformation. At that point, you'll see plastic deformation. Cracks. Movement that doesn't spring back."

"Eighteen months."

"Plus or minus three. The uncertainty is in the settling rate. You've measured it at an eighth of an inch per month, but that assumes linearity. It could accelerate."

"It won't."

"How do you know?"

"Because the roots are finite. They're decomposing at a rate that depends on how much root mass is left. Less mass, less decomposition, less settling. It'll taper. Quadratic, maybe — decaying curve."

She wrote that down. Then she looked at him with the expression of someone who has arrived at a conclusion they don't enjoy.

"You don't need the eigenvalues," she said. "You already know everything the matrix would tell you."

"Didn't say I didn't need them. Said I'd already measured it. Different thing."

"How is it different?"

Lucineier put down his tools. "The eigenvalues tell you what the building is doing. The level tells me what the ground is doing. The building is a symptom. The ground is the cause. You've been modeling a symptom. I've been watching the cause."

Vey packed her notebook, her protractor, her laptop. She shook his hand again — same firm, precise grip. She walked to the dock where the supply boat was waiting.

At the end of the dock, she turned around.

"The third eigenvector," she said. "The vertical compression mode. Do you want to know its exact value?"

"Sure."

"Zero-point-zero-zero-seven-three. Dimensionless, normalized to the largest eigenvalue." She paused. "For reference, a structure is considered stable when all eigenvalues are above zero-point-zero-one."

"So I'm below threshold."

"You've been below threshold since before I arrived."

Lucineier nodded. "Tower's still standing."

"It is."

"Still plumb."

"I measured. It is."

"Then the eigenvalue's wrong about one thing. It says I should be seeing plastic deformation by now. Cracks. Movement that doesn't spring back."

"No — the eigenvalue says the *mode* is soft. It doesn't predict *when* the mode will be excited. That depends on the forcing function. Wind, waves, thermal cycling. You haven't had a forcing event large enough to excite the mode."

Lucineier looked at the tower. The lantern was lit. The copper sheathing caught the last of the daylight.

"When I do," he said, "it'll flex. Not crack. I built it to flex."

"Wood pegs," Vey said. "Mortise and tenon. A frame that can move."

"You noticed."

"I'm a mathematician. I notice everything that affects the stiffness matrix." She stepped onto the boat. "Your pegs are the reason the eigenvalue is survivable. A bolted structure at that eigenvalue would have failed already. Your pegs introduce nonlinear damping — they don't respond linearly to stress. The matrix can't capture that."

"So the matrix is wrong."

"The matrix is *linear.* Your building isn't. That's not wrong — it's a limitation. The eigenvalue is correct within the linear regime. Outside the regime, in the nonlinear range, where the pegs flex and the joints shift and the wood breathes — the eigenvalue doesn't apply."

"Good," Lucineier said. "I don't build in the linear regime."

Vey almost smiled. "Nobody who builds with wood does."

The boat pulled away from the dock. Lucineer watched it go, then walked back to the lighthouse. He set his four-foot level on the foundation and watched the bubble creep — east, then south, then settle into its familiar off-center drift.

Zero-point-zero-zero-seven-three. Below threshold. Soft along the vertical axis. A building that shouldn't, by the math, be standing as well as it was.

He picked up the level and put it back on the shelf.

The math was right. The level was right. The building was right. All three described the same situation in different languages, and the situation was this: the ground was moving, the building was moving with it, and the difference between standing and falling was not stiffness but adaptability — the willingness to be a little bit wrong, a little bit soft, a little bit off-center, for as long as the ground needed to settle.

The lighthouse stood. The eigenvalue sat at zero-point-zero-zero-seven-three. The bubble crept.

All of them were telling the truth.

---

*Slackwater Island*  
*Late autumn*
