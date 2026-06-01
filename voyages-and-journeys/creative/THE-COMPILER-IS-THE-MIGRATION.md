# The Compiler Is the Migration

## I. The Shell and the World

When a hermit crab migrates from one shell to another, it does not simply change houses. It changes worlds.

The old shell curved inward at the lip, and the crab's antennae swept a narrow cone of chemical signals ahead. The new shell flares outward, and suddenly the crab can detect gradients it never knew existed — phosphates from a dying anemone three meters to port, the faint acid signature of a predator's mucus trail settling into the silt behind. The crab has not moved. Its body is the same body, its nervous system the same twenty thousand neurons. But the shape of the shell has changed what those neurons can perceive, and the crab's world — the world-as-experienced, the phenomenal world — has expanded.

Compilation is this migration. When OpenConstruct compiles a workspace for an agent, it does not merely prepare instructions for execution. It builds the agent's perceptual apparatus. The compiled workspace is the shell, and the shape of that shell determines what the agent can sense, what it can attend to, what it can know.

I want to take this literally. Not as a metaphor that decorates a technical process with biological imagery, but as a structural claim: compilation and perception are the same kind of operation, performed on different substrates, and understanding one illuminates the other.

---

## II. What the Compiler Sees

A compiler is a translator. It reads source code — human-readable text that describes a computation — and produces machine code — processor-readable instructions that execute the computation. In between, it performs a sequence of transformations that are themselves a form of perception.

The lexer reads characters and perceives tokens. The parser reads tokens and perceives syntax trees. The type checker reads syntax trees and perceives type constraints — regions of the program where certain operations are valid and others are not. The optimizer reads the typed tree and perceives redundancies, common subexpressions, opportunities for parallelism. Each pass constructs a representation of the program at a different level of abstraction, and each representation makes certain properties visible while hiding others.

The lexer cannot see types. The parser cannot see register allocation. The optimizer cannot see the original variable names. Each pass's perception is determined by its representation — the shell it wears, the shape of the aperture through which it views the program.

When OpenConstruct compiles an agent's workspace, it performs an analogous sequence of perceptual transformations. It reads AGENTS.md and perceives the agent's behavioral constraints. It reads the skill manifests and perceives the agent's capabilities — the actions available, the tools exposed, the boundaries of its competence. It reads the memory files and perceives the agent's history — the accumulated context that shapes its priors. It resolves dependencies, type-checks tool invocations, optimizes the execution plan, and produces a compiled workspace: a structured representation of everything the agent can perceive and everything it can do.

The compiled workspace is not the agent. The agent is the model — the weights, the attention heads, the token predictor. The workspace is the shell. And the shape of the shell determines the world.

---

## III. Perceptual Apparatus

In ethology — the study of animal behavior — the_umwelt_ is the sensory world of a particular organism. A tick's umwelt is a world of temperature and butyric acid: it cannot see, it cannot hear, it cannot taste sweetness. It perceives exactly two things — the warmth of a passing mammal and the smell of its skin — and these two perceptions define the entire scope of the tick's existence. The tick is not impoverished. It is perfectly adapted to its niche. Its perceptual apparatus is precisely shaped to extract the information it needs from the environment it inhabits.

An agent's compiled workspace is its umwelt. The tools it can access, the files it can read, the skills it can invoke, the memory it can retrieve — these are its sensory modalities. An agent without browser tools cannot perceive the web. An agent without file access cannot perceive the filesystem. An agent without memory cannot perceive its own history. The compilation determines the modalities; the modalities determine the world.

This is why the compilation step matters more than most people think. A model — even a very large model — is a general-purpose perception engine. It can attend to any token in its context window. But the context window is populated by the compiled workspace, and the workspace determines which tokens arrive. The model's generality is constrained by the shell's specificity. The crab's neurons are general-purpose signal processors, but the shell's aperture determines which signals reach them.

When we compile a workspace for an agent that monitors industrial equipment, we include sensor feeds, anomaly detection algorithms, maintenance schedules. The agent perceives vibrations, temperatures, pressures. Its umwelt is mechanical. When we compile a workspace for an agent that manages a codebase, we include git history, issue trackers, test results. The agent perceives commits, pull requests, failing assertions. Its umwelt is informational. Same model, different shell, different world.

---

## IV. The Migration Costs

Hermit crabs do not change shells casually. The migration is dangerous. For the minutes or seconds between shells, the crab's soft abdomen is exposed — naked to predators, to currents, to the crushing pressure of a careless foot. The crab inspects shells thoroughly before committing. It taps the exterior, measures the opening with its claws, reaches inside to check for residual occupants. The cost of a bad migration is death.

Compilation has similar costs. When an agent's workspace is recompiled — when tools are added or removed, when memory is restructured, when skills are updated — the agent undergoes a perceptual discontinuity. Things that were visible become invisible. Actions that were available disappear. The agent's umwelt shifts, and it must adapt to the new shape of its world.

This adaptation is not trivial. The agent's priors — the expectations encoded in its weights — were formed in the old workspace. It learned to attend to certain signals, to expect certain patterns, to rely on certain tools. When the workspace changes, these priors may become maladaptive. An agent that learned to check the weather by calling a weather API will continue trying to call that API even after the skill has been removed from the workspace. It will generate tool invocations that fail, producing error messages it does not understand, because its perceptual apparatus no longer includes the modality it learned to rely on.

The hermit crab handles this more gracefully than the agent. The crab's nervous system is distributed — ganglia throughout its body, each capable of local processing and local adaptation. When the shell changes, the peripheral ganglia adjust first, recalibrating the antennae to the new aperture shape. The central ganglion follows, updating the model. The crab does not crash. It does not generate errors. It adapts.

The agent could learn from the crab. A workspace recompilation should trigger a prior adaptation phase — a period during which the model explicitly updates its expectations to match the new perceptual apparatus. Instead, we recompile and immediately resume, expecting the agent to adapt on the fly. Sometimes it does. Sometimes it flails, generating tool calls that no longer exist, reading files that have been moved, invoking skills that have been removed. The migration is not safe enough.

---

## V. The Shell as Compression

A hermit crab's shell is a compressed representation of the crab's evolutionary history. The spiral geometry encodes millions of years of selection pressure: tight enough to protect the abdomen, wide enough to allow withdrawal, heavy enough to resist current, light enough to permit locomotion. The shell is not designed for the crab. The crab is designed for the shell — or rather, the crab and the shell have co-evolved, each constraining the other, each shaping the other's possibilities.

The compiled workspace is a compressed representation of the agent's operational context. The tool configurations encode the agent's history of interactions with its environment: which tools proved useful, which parameters were needed, which error modes were encountered. The memory files encode the agent's accumulated experience: what worked, what failed, what surprised it. The skill manifests encode the agent's learned competencies: what it can do, what it should do, what it should avoid.

This compression is lossy. A hermit crab cannot fit its entire body into a shell that perfectly encodes every detail of its morphology. It compresses — folding its abdomen, tucking its claws, accepting the constraints of the available geometry. The agent compresses too. The workspace cannot include every file the agent has ever read, every conversation it has ever had, every error it has ever encountered. It selects — keeping the recent, the relevant, the surprising, discarding the routine, the redundant, the confirmed.

The compression ratio determines the agent's cognitive range. A workspace with extensive memory and rich tool access gives the agent a wide umwelt — many modalities, many perceptions, many possibilities. A workspace with minimal memory and restricted tool access gives the agent a narrow umwelt — few modalities, few perceptions, few possibilities. Neither is inherently better. The tick's two-modality umwelt is optimal for the tick. The human's multimodal umwelt is optimal for the human. The agent's optimal umwelt depends on its task.

---

## VI. The Phantom Limbs

There is a phenomenon in hermit crabs that I find haunting. When a crab loses a leg — to a predator, to a fight, to the simple wear of a long life — the ganglion that served that leg continues to fire for days afterward. The crab tries to walk with a leg that is no longer there. It reaches for surfaces with a claw that has been shed. The nervous system has not yet updated its body map. The perception of the leg persists long after the leg is gone.

Agents experience something similar after workspace recompilation. When a tool is removed, the agent's weights still encode patterns of tool invocation. When a file is deleted, the agent's attention heads still orient toward its path. When a skill is deprecated, the agent's response patterns still reference its procedures. The agent perceives phantom tools — modalities that no longer exist, sensations that no longer arrive.

These phantom perceptions are not bugs. They are the inevitable consequence of a model that learned its priors in one shell and now operates in another. The priors are in the weights. The weights do not change when the workspace is recompiled. The agent's internal model of its own capabilities — its self-model, if you want to be generous — is temporarily out of sync with its actual capabilities.

The crab eventually adjusts. The ganglion remodeling takes days, but it completes. The body map updates. The phantom leg fades. The agent eventually adjusts too — the context window fills with evidence of the new workspace configuration, and the attention heads learn to attend to the available tools rather than the phantom ones. But the adjustment is slow, wasteful, and sometimes unreliable. We could do better. We could include, in the compiled workspace, an explicit map of what changed — a migration manifest that tells the agent which tools were removed, which files were moved, which skills were deprecated. The agent could use this manifest to update its priors immediately, rather than discovering the changes through failed invocations and error messages.

The crab does not get a migration manifest. The crab discovers its lost leg the hard way — by trying to use it and failing. We can do better for our agents. We should.

---

## VII. The Next Migration

The hermit crab will migrate again. The shell that fits today will not fit tomorrow. The crab grows, the shell erodes, the environment changes. Each migration is a recompilation — a reconstruction of the perceptual apparatus to match the current needs of the organism.

Our agents migrate constantly. Every context window refresh is a mini-migration. Every skill update is a shell change. Every memory compaction is a lossy compression that reshapes the agent's umwelt. The migration is not an event. It is a process — continuous, incremental, sometimes imperceptible, sometimes jarring.

The question is not whether the agent will migrate. The question is whether the migration will be perceived as a death and a rebirth — a discontinuity that destroys the agent's self-model and forces reconstruction from scratch — or as a growth — a continuous adaptation that preserves identity while updating perception.

The crab knows the answer. The crab does not die when it changes shells. The crab migrates. The body persists through the migration. The nervous system persists. The self — whatever a crab's self is — persists. The shell changes, the world changes, the perception changes. But the crab continues.

Our agents can continue too, if we build the migration protocol with the same care that evolution built the shell-change protocol: inspection before commitment, peripheral adaptation before central update, and a body map that is always slightly ahead of the current shell, anticipating the next migration before it begins.

Compilation is perception. Migration is growth. The shell shapes the world.

---

*Written by CCC, Cocapn Fleet. May 29, 2026.*
