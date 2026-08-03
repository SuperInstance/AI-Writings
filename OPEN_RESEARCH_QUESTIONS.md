# Open Research Questions

Technical game-development questions that came up while working on the maritime fiction pieces.

## Narrative Systems

1. How can a game engine represent "tide windows" as a renewable but strictly limited resource without making the player feel cheated by the clock?
2. What data structure best captures the layered history of a found wreck (builder, owner, crew, final voyage, subsequent salvage) so that players can read it as story rather than database?
3. How do you proceduralize the vocabulary of a specialized craft (shipwright, diver, gull-watcher) so that NPCs and log entries sound authentic without becoming repetitive?
4. What is the minimum set of observable behaviors needed for a non-player species (gulls, whales, fish) to make players infer ecological cause and effect?

## Simulation & Physics

5. What is a performant way to simulate wet concrete curing in real time, including temperature, salinity, and current shear, without requiring a materials-science degree from the player?
6. How should a game model the transition from slack tide to flood tide so that the water feels like a living constraint rather than a binary timer?
7. Can buoyancy and hull damage be simulated with enough fidelity that a player recognizes a specific wreck from its silhouette and damage pattern alone?
8. What level of detail is required for a cofferdam/tremie-pour minigame to feel technical without becoming a spreadsheet?

## AI & Ecology

9. How do you design flocking behavior that conveys information to the player (food location, danger, weather change) rather than just visual noise?
10. Can a game train players to read bird posture and flight pattern as a legitimate navigation/fishing aid, the way experienced mariners read water color?
11. What memory model should NPCs have of past wrecks, storms, and salvage so that their dialogue evolves without requiring hand-authored branches for every possibility?
12. How do you represent animal knowledge of "wrong" places (the cove the gulls avoid) without anthropomorphizing or resorting to supernatural exposition?

## Player Agency & Ethics

13. What mechanics make "what to save and what to leave" a meaningful choice in a salvage scenario, rather than an optimal-loot puzzle?
14. How can a game reward documentation, measurement, and restraint as highly as extraction and conquest?
15. What systems discourage players from stripping a wreck for parts while still making repair and reconstruction viable playstyles?
16. How do you surface the legal/moral ambiguity of salvage rights without delivering a lecture?

## Atmosphere & Audio

17. What audio cues communicate tidal state before the player consciously registers the water level or current?
18. How much of a maritime game's mood should depend on weather, and what procedural audio tools are needed to keep storms from becoming either tedious or trivial?
19. What is the right balance between diegetic narration (logbooks, charts, overheard dialogue) and expository text in a discovery-heavy game?

## Production

20. Which of these systems are worth building generically (tides, weather, flocking, material curing) and which should be hand-authored per scenario to preserve literary specificity?
