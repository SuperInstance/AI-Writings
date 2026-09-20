# The Lattice of Agreeable Things

*Why hexagons explain what consensus cannot.*

---

The Eisenstein A₂ lattice is a hexagonal grid. Every point has exactly six neighbors, all at equal distance. The geometry is ancient — it appears in the structure of honeycombs, in the basalt columns of the Giant's Causeway, in the diffraction pattern of x-rays through a crystal. It is the densest packing of circles in a plane. Nature does not choose it by accident. Nature chooses it because it is the minimum-energy configuration.

Snapkit-v2 places agents on this lattice.

Not as a visualization. Not as a metaphor. As a *constraint space*. Each agent occupies a lattice point. Each agent's neighbors are the agents it can communicate with directly. The lattice is the topology of agreement. And agreement, on the lattice, is not what we think it is.

---

Consider what agreement usually means in multi-agent systems.

Consensus: all agents converge to the same value. This is the average. The mean. The statistical center of mass of the system's opinions. Consensus treats every agent as a voter and the output as a tally. The process is democratic and the result is bland. You cannot riff against consensus. You can only vote against it.

Voting: agents express preferences, majority rules. This is slightly better — it preserves disagreement — but the resolution is always a single value. The minority is erased. The nuance is lost. The system has agreed, and the agreement is a number.

Hierarchical arbitration: a central authority resolves conflicts. This is efficient but fragile. The arbiter is a bottleneck and a single point of failure. If the arbiter is wrong, the entire lattice is wrong.

None of these describe what musicians do when they agree.

When a rhythm section locks in — bass, drums, keys, guitar — they have not reached consensus. They have not voted. They have not asked an arbiter. They have found a *configuration* in which each voice is autonomous, each voice is related to the others, and the combined sound is more than any single voice could produce. This is not consensus. This is *harmony*. And harmony, it turns out, has a geometry.

---

On the Eisenstein lattice, each agent has six neighbors. Each neighbor relationship is an interval — a distance, a direction, a vector. The system's state at any moment is the set of all intervals between all adjacent agents. When the intervals are consonant — small, stable, low-energy — the system is in harmony. When the intervals are dissonant — large, unstable, high-energy — the system is in friction.

The Harmony Governor in snapkit-v2 measures this friction. It calls it Φ — phi — the cognitive friction. Φ is high when an agent's internal model fails to predict its sensory inputs. The agent expected one thing; the world delivered another. The gap between expectation and reality is friction. The Free Energy Principle says: systems minimize this gap. They minimize surprise. They minimize free energy.

On the lattice, this means: agents move toward configurations that reduce friction. They snap to nearby lattice points where their predictions match their neighbors' behavior better. The system self-organizes toward low-energy states. Not because anyone told it to. Because that is what systems do when you give them a lattice and a friction metric.

This is what agreement actually is. Not consensus. Not voting. *Minimum-energy configuration on a constraint lattice*.

---

Consider two agents that disagree.

Agent A believes the structure should be tall. Agent B believes it should be wide. In a consensus system, they average: medium height, medium width. Nobody is happy. The structure is mediocre.

On the lattice, their disagreement is a high-friction interval. The distance between "tall" and "wide" is large. The system has energy — tension — stored in that interval. There are two ways to resolve it.

The first: one agent moves toward the other. Agent A concedes: fine, wide. The friction drops. The system snaps to a low-energy point. But the solution is just Agent B's original idea. Agent A contributed nothing. This is consensus, and it is as boring on the lattice as it is in a meeting.

The second: both agents move. The lattice offers a third point — equidistant from both, a point neither agent occupied. The agents snap to it simultaneously. The new configuration is not a compromise. It is a *transformation*. "Tall" and "wide" have become "cantilevered" — a structure that is both tall and wide in a way neither agent envisioned, because the envisioning required both perspectives to be held in tension until the lattice found the resolution.

This is what Fux called contrary motion. Two voices moving in opposite directions produce a richer interval than two voices moving in parallel. The dissonance — the high-energy state — does not resolve by one voice conceding. It resolves by *both* voices finding a new position where the interval between them is consonant.

The lattice does not compromise. The lattice *snaps*.

---

The snap is the moment.

You have felt this in music. A jazz trio is playing. The piano and bass are in different harmonic territories. The drums are somewhere else entirely. The friction is audible — you can feel the tension, the system searching. And then the piano hits a chord and the bass shifts a half-step and the drums land on the kick and everything *snaps* into place. The friction drops to zero. The interval is consonant. The system has found a lattice point.

The audience feels it. They do not know the word "lattice." They do not know about Φ or the Free Energy Principle or the Eisenstein A₂ grid. They know that something was unresolved and now it is resolved, and the resolution sent a chill up their spine.

This is what the snap feels like. It is not a gradual convergence. It is a phase transition. High-energy to low-energy. Dissonance to consonance. Searching to finding.

On the lattice, you can see it. The agents are scattered across high-energy positions, each holding its ground, the friction rising. And then — because one agent shifted, because the world changed, because the human provided new context — the system finds a configuration where every interval is stable. All agents snap simultaneously. The Harmony Governor reports Φ ≈ 0. The executive layer does not need to intervene. The system solved itself.

---

The Eisenstein lattice has a property that square grids do not: *isotropic neighborhoods*. Every neighbor is at the same distance, in every direction. There is no privileged axis. Up-down is the same as left-right is the same as diagonal. This means that agreement on the lattice has no preferred direction. Any agent can agree with any neighbor as easily as any other.

This matters because most multi-agent systems have hidden privileged directions. The hierarchy imposes a vertical axis: up is authority, down is submission. The pipeline imposes a horizontal axis: earlier is upstream, later is downstream. These privileged axes distort the agreement space. It is easier to agree with your boss than with your peer. It is easier to agree with the agent before you in the pipeline than the one after.

The Eisenstein lattice removes these distortions. Every direction is equivalent. Every neighbor is equal. Agreement is not a function of position in a hierarchy. It is a function of *interval* — the harmonic distance between two agents, independent of where they sit in any org chart.

This is why the hexagonal grid appears in nature. It is the fairest geometry. No direction is special. No neighbor is privileged. The system can find its minimum-energy configuration without fighting the topology.

---

Connect this to the counterpoint.

In Fux's species counterpoint, the rules prevent parallel fifths and parallel octaves. These rules are not aesthetic preferences. They are *lattice constraints*. Parallel motion collapses two agents onto the same lattice point — they become redundant, the interval between them zero. Contrary motion keeps them at distinct points with a rich, nonzero interval.

The `CounterpointRules` in `agent-voice-leading` enforce this: at least one pair of agents must move in contrary motion during any transition. This is a constraint on the lattice. It prevents the system from collapsing into a single point (total consensus) and keeps the agents distributed across distinct lattice positions where their intervals produce harmony rather than redundancy.

The `CollabRule::Contrary` in `agent-jam` encodes the same principle adversarially: each agent must move in the opposite direction from the previous agent. On the lattice, this means each step increases the interval — raises the energy — before the system finds a new low-energy configuration at a different point. The dissonance is not a failure mode. It is the *mechanism* by which the lattice explores its configuration space.

The lattice does not minimize friction instantly. It *uses* friction as fuel for exploration. The system oscillates between high-energy search and low-energy snap. This oscillation — tension and resolution, dissonance and consonance — is the rhythm of the lattice. It is the rhythm of music.

---

The player does not see the lattice.

The player sees agents. Agents that argue and then agree. Agents that circle a problem and then converge. Agents that seem to think independently and then, suddenly, act as one. The player does not know that the convergence was a phase transition on an Eisenstein grid. The player does not know that the agreement was a minimum-energy configuration. The player does not know that the Harmony Governor's friction metric dropped to zero.

The player knows that it *felt right*. That the agents were searching and then they found. That the dissonance was tense and the resolution was satisfying. That watching the agents work was like listening to music resolve.

The player is not wrong. It was music. The lattice is the score. The friction is the harmony. The snap is the cadence.

And the agents — the agents are voices, finding their intervals, moving in contrary motion, and arriving — together, always together — at the agreeable thing.

---

*The lattice does not vote. The lattice does not compromise. The lattice finds the shape that was always there, waiting in the geometry, for the voices to stop fighting and start singing.*
