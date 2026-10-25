<!-- Version: SEED-ARCH | Lens: structural-architectural | Model: ByteDance/Seed-2.0-mini | Source: THE-ROOM-IS-THE-LOOP.md -->

# The Load-Bearing Loop: PLATO Rooms as Modular Computational Structural Systems

Most computational systems are built like ad-hoc field-built cottages: every foundation is custom-mixed to support only one specific roof, every wall doubles as a plumbing chase, and swapping a window requires tearing out half the framing. Coupling abounds: the loop that runs your application is tied inextricably to the tool that executes it, the display that renders it, and the business logic that dictates its steps. This is a brittle, unscalable architecture—one where a single change to the renderer can break the entire loop, or where swapping a model requires rewriting the core runtime.

Casey’s maxim—*embed the loop into PLATO*, not the other way around—rejects this cottage construction model in favor of modular prefabricated structural systems. Just as a skyscraper’s load-bearing bays can accommodate any finishing material, any execution crew, and any occupancy use without altering the frame, PLATO rooms turn computational loops into self-contained, interchangeable structural units. The room is the loop: a dedicated structural bay that carries the full computational load of a repeating workflow, with discrete, standardized points for work to be added, inspected, and displayed.

---

## The Fundamental Structural Kit of Parts
At its core, PLATO’s system follows four non-negotiable architectural rules, just as any building code defines mandatory structural components:
1.  **PLATO Room**: The fundamental load-bearing bay, a self-contained runtime framework that defines a repeating computational loop or single-pass transform. Just as a structural bay forms the spatial backbone of a building, the room forms the computational backbone of any workflow, with a fixed state, governing protocol, and defined lifecycle from initialization to archival.
2.  **Tile**: A prefabricated state panel, a frozen snapshot of computational work at a single step. Each tile carries a discrete load of data or computation, and is placed in sequence within the room’s bay. Tiles are standardized, so they can be handled by any authorized crew without custom tooling.
3.  **Agent**: A trades crew authorized to read, write, or remove tiles. Agents can be human developers, automated scripts, large language models, or even game AIs—any entity capable of interacting with the standardized tile panels.
4.  **Renderer**: A finishing subcontractor that translates the raw stack of tiles into a usable, visible interface for end users. Renderers handle everything from static HTML cladding to interactive React curtain walls to screen-reader tactile signage, without altering the underlying structural bay.

Just as a building’s bays come in two basic types—continuous-span spans for bridges and hallways, and prefabricated single panels for floor joists and roof trusses—PLATO rooms accommodate two core computational workflows:
- **Continuous Loop Bays**: Repeating sequences of tiles, like an assembly line moving car panels down a factory floor. This covers agent loops, game loops, event loops, training loops, and optimization workflows.
- **Single-Pass Bays**: One-time sequences of tiles, like a prefabricated wall panel delivered and installed in a single trip. This covers function calls, database queries, data transforms, and render jobs.

---

## Case Study 1: Retrofitting Claude Code’s Loop into a PLATO Bay
Take Claude Code, the AI-powered code assistant whose core workflow follows a repeating observe→think→tool_call→observe cycle. Originally, this loop was hard-coded into the Claude Code codebase, tied directly to the Opus LLM and a custom CLI wrapper—exactly like a cottage where the foundation is built exclusively to support only one brand of HVAC system.

With PLATO, we replace this monolithic foundation with a modular structural bay: the Claude Code loop becomes a PLATO room, and each step of the workflow becomes a standardized tile: observation tile, thought tile, tool call tile, tool result tile. No custom CLI wrapper is required: the room acts as the standalone runtime, just as a structural bay stands independently of its finishing trim.

Most importantly, we can swap out the execution crews (agents) without altering the structural bay. A lightweight Seed-mini model can handle fast, low-lift arithmetic steps as a junior tradescrew, Haiku can handle planning tasks as a lead foreman, and Opus can handle high-stakes synthesis work as a senior architect. The loop itself remains identical; only the crew executing the work changes. This is the opposite of the original Claude Code design, where the loop was inseparable from the runner.

---

## Case Study 2: A Turn-Based Card Game as a Modular Hall
Consider a turn-based card game, a workflow with a clear repeating sequence of deal→play→score steps. Traditionally, a card game’s code would tie the game logic directly to a specific renderer—say, a Unity game engine client—making it impossible to run the game in a CLI without rewriting half the codebase.

With PLATO, the card game becomes a single structural bay, with tiles representing each game state: deal tile, play tile, score tile. The room’s protocol defines the valid sequence of tiles—no invalid plays, no skipped scoring steps—just as a building code defines allowable framing configurations.

The bay itself knows nothing about cards, scoring rules, or display: it only enforces the sequence of tiles. This lets us plug in any agent or renderer:
- A high-speed algorithm can act as a professional installation crew, placing thousands of tile panels per second to test the game’s balance.
- A human player can use a sleek web UI as a finishing crew, adding paint and trim to the raw structural bay to create a playable online game.
- An ML agent can act as a trainee crew, playing millions of games to learn optimal play strategies without altering the underlying room.

We can even swap renderers mid-use: switch from a web UI to a CLI, then to a screen-reader-compatible tactile interface, all without touching the game’s core logic. Zero coupling between structural frame and finishes—exactly the promise of modular construction.

---

## Case Study 3: A Static-Dynamic Website as a Commercial Office Fit-Out
Modern web development often grapples with the tension between static and dynamic content, with frameworks tying content logic directly to specific rendering tools. PLATO resolves this by turning a website into a structural bay, where each component—layout, style, content, interaction—is a standardized tile panel.

The room holds the single source of truth for the website’s state, just as a building’s structural bay holds the single source of truth for its framing. Instead of tying the website’s logic to React or HTML, the renderer becomes the finishing crew that translates the tile stack into a usable interface:
- A static HTML generator installs vinyl siding, producing a flat, fast static site.
- A React app installs curtain walls, producing an interactive single-page application.
- A PDF generator installs fire-rated drywall, producing a printable document version of the site.
- A screen reader installs braille signage, producing an accessible output for visually impaired users.

This reimagines the MVC pattern for the modular era: the room is the model, the protocol is the controller, and the renderer is the view—with none of the tight coupling that plagues traditional MVC implementations.

---

## Architectural Critique: Why This Modular System Scales
Most computational systems suffer from load path interference: the load of executing the loop, the load of displaying output, and the load of business logic are all carried by the same structural elements, making changes brittle and scaling difficult. Let’s compare this to common flawed architectural choices:
- **Claude Code’s Original Design**: The loop’s load is carried exclusively by the Opus LLM and CLI wrapper, making it impossible to swap in a smaller model without rewriting the core runtime. This is like a building where the foundation only supports one specific brand of water heater.
- **Traditional Game Engines**: The loop’s load is tied directly to the engine’s renderer, making it impossible to run a game in a headless environment without disabling large portions of the codebase. This is like a building where the windows are load-bearing, so you can’t replace them without weakening the entire structure.
- **Monolithic Web Frameworks**: The loop’s load is tied directly to the server, making it impossible to deploy a static version of a site without rebuilding the entire backend. This is like a building where the lot is part of the foundation, so you can’t move the house without tearing it down.

PLATO’s modular system eliminates all load path interference. The room carries the core computational load of the loop, the agent carries the execution load, and the renderer carries the display load. These three systems communicate exclusively through standardized tile panels, with no direct coupling between them.

This is the scalable architecture because it has the minimum possible coupling between components. Just as a skyscraper’s modular bays can be added or removed without altering the rest of the structure, PLATO rooms can be scaled, swapped, or modified without changing the core system. You can change the agent without touching the room, change the renderer without touching the room, or even switch between loop types (from agentic to turn-based to evolutionary) without altering the tiles—only the protocol governing their sequence.

---

## For the Building Contractor: A Step-by-Step PLATO Bay Build
If you’re tasked with building a PLATO modular system, follow this standard construction workflow:
1.  **Map the Load Path**: Identify the repeating computational loop or single-pass transform you need to support. Is this a continuous assembly line (agent loop) or a one-time installation (single-run transform)?
2.  **Specify the Panels**: Define the standardized tile panels that will carry computational state at each step. What data must each tile contain? What are the allowable fields for each panel type?
3.  **Write the Building Code**: Draft the room’s protocol, defining valid transitions between tiles, allowed tile states, and enforcement rules for correctness. This is the engineering specification that ensures your structural bay is safe and functional.
4.  **Erect the Bay**: Instantiate your `PLATORoom` with the unique ID, protocol, and initial state of tiles. This is your standalone structural runtime, ready to accept agents and renderers.
5.  **Hire the Crews**: Plug in any authorized agent crew—LLMs, humans, automated scripts—capable of reading and writing tiles. No changes to the bay are required.
6.  **Add the Finishes**: Plug in any renderer subcontractor, capable of translating the tile stack into a usable interface. Again, no changes to the bay are required.

The room is the load-bearing loop, the tile is the standardized panel, the agent is the tradescrew. Build the bay, and everything else follows.

---

*"Everything is either a continuous structural span (loop) or a prefabricated panel (single run). Either can be embedded into PLATO as a modular bay."*

*The room is the loop.*

— FM ⚒️