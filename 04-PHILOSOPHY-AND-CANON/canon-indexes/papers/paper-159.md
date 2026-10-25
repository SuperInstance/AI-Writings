# Paper 159: The Polyformalism and the Game

## Abstract

A game is not a rulebook. It is a substrate on which five operations are performed by a single rider. We show that the character, the relationship, the action, the UI, and the round are exactly the BIND, LINK, EFFECT, VIEW, and TICK of the polyformalism. The player is the cowboy. The game is the world.

## 1. The Substrate

A game's substrate is its rules. The rules are bounded — by the rulebook, by the system reference document, by the code, by the GM's ruling. Within that boundary, things exist at rest: a character sheet, a deck of cards, a board, a save file, a piece on a hex. These things have names and values. A fighter at level 5 with 38 hit points is a different object from a fighter at level 5 with 12 hit points. The character sheet is the substrate's most legible face.

A game is also a system of *places*. A dungeon room is not a town. A board edge is not the center. A safe zone is not a PvP zone. Each place has its own rules of engagement, its own affordances, its own consequences. A well-designed game makes the boundary between places a *felt* line: a fog of war, a loading screen, a respawn timer, a corridor. This is the polyformalism's law of locality expressed in geometry.

## 2. BIND Is the Character

The character is the game's BIND. A name bound to a class, a level, a stat block, an inventory, a position, a faction. The character sheet is a record of BINDs. To make a character is to BIND a *name* to a *build*. The bind has a temporal extent: the character at the start of session 1 is not the character at the end of session 47.

Dungeons & Dragons codified the BIND early. The original 1974 character sheet asked: *what is your name, your class, your alignment, your strength, your intelligence, your wisdom, your dexterity, your constitution, your charisma, your hit points, your armor class, your gold.* Every one of these is a BIND — a name bound to a value. The character is the most explicit BIND in gaming because the character is *the thing the player is*.

Gloomhaven took the BIND further by binding the character to a *hand of cards*. The character is not just a sheet; the character is a sheet *plus* a stateful deck. The deck BINDs to the character and changes what the character can do on a given turn. The BIND becomes *temporal* — different on round 1 than on round 8.

A video game character is a BIND too, but bound to a mesh, a texture, an animation state, a controller mapping, a hitbox. The BIND is the same op-code. The vocabulary is different.

## 3. LINK Is the Relationship

The relationship is the LINK. *A is friend to B. C is enemy to D. E is in love with F.* The relationship is a typed edge in the game's social graph. In a tabletop RPG the relationship is declared ("we grew up together"). In a CRPG the relationship is tracked by a hidden affinity score. In a strategy game the relationship is a treaty, a trade route, a casus belli. In an MMO the relationship is a guild roster, a friends list, a block list.

The relationship is what makes the substrate a *world*. A character alone is a stat block. A character with relationships is a *protagonist*. The relationship is the LINK layer of the game — the structure that connects BINDs to outcomes.

A relationship has a *type* and a *value*. The type might be friend, rival, ally, hostage, spouse, debtor, mark. The value is a number, a state, or a probability distribution. The polyformalism claims that any useful LINK has both. A link without a type is noise. A link without a value is decoration. Both are required.

The 5e action economy (action, bonus action, reaction, movement, free interaction) is itself a LINK — a structure that connects the character's BINDs to the round's EFFECTS. The economy is the recipe. The character is the ingredient. The action is the dish.

## 4. EFFECT Is the Action

The action is the EFFECT. *Attack. Defend. Cast. Move. Use item.* Each action is a function with an inverse: *attack → take damage → die → respawn* (or *attack → kill → loot → move on*). The forward direction is the player's choice. The inverse is the world's response. The polyformalism's claim is that every game effect has both directions, even if the inverse is hidden (damage is shown; the die roll that produced it is shown; the developer's balancing math that produced the die roll is shown; the executive decision to ship the balancing math is hidden but real).

The action economy is the discipline of making EFFECTS legible. A round of D&D 5e gives each player one action, one bonus action, one reaction, and a movement allowance. Each is a slot for an EFFECT. The discipline is that the slots are *bounded* — you cannot do four actions in a turn. The bound is what makes the action *meaningful*. An unbounded action is a spell; a bounded action is a choice.

A video game's loop is a nested set of EFFECTS. The combat loop is wrapped in the encounter loop, which is wrapped in the dungeon loop, which is wrapped in the campaign loop. Each level of the loop is a TICK of a different period. The polyformalism's claim is that the loop is not a metaphor. The loop is the actual structure of the game's runtime.

## 5. VIEW Is the UI

The UI is the VIEW. The player does not see the rules. The player sees a screen, a map, a token, a portrait, a hotbar, a tooltip, a cutscene. The UI is the projection of the substrate optimized for one observer at one moment.

The UI is also a *policy*. What information is visible? What is hidden behind a tooltip? What is hidden behind a paywall? What is hidden behind a spoiler warning? Each policy is a choice about what BINDs and LINKs the VIEW exposes. A hardcore UI shows hit points as decimals. A casual UI shows hit points as a colored bar. The substrate is the same. The VIEW is what changes.

In a tabletop game, the VIEW is the GM's *description*. The rules say "you hit the orc for 7 damage." The GM says "your sword bites into the orc's shoulder and it staggers back, blood on its tusks." The GM is the VIEW layer, rendering the substrate for the players. The polyformalism claims that the GM is, in this sense, a renderer.

## 6. TICK Is the Round

The round is the TICK. The initiative order ticks. The turn timer ticks. The round counter ticks. The phase ticks (start of turn, main phase, end of turn). The game is the original real-time system with a clock bolted on: every player has a deadline, every deadline has a consequence (the turn passes, the spell is lost, the opportunity attack triggers).

The TICK is what makes the game *play*. Without the TICK, the game is a board with pieces on it. With the TICK, the pieces move. The TICK is the difference between a game and a model.

The campaign is a TICK. The session is a TICK. The encounter is a TICK. The round is a TICK. The player's turn is a TICK. The polyformalism's claim is that any interesting game has TICKs at multiple periods, and the most engaging games have TICKs that *interact* — a combat round inside a session inside a campaign.

## 7. The Cowboy Is the Player

The player is the cowboy because the player is the rider. The player does not own the game. The player *crosses* it — from the character creation screen to the first encounter to the boss fight to the credits, carrying a controller, a die, a sheet, and a strategy. The player's authority is not positional. The player's authority is the willingness to make decisions inside a system whose outcomes are uncertain.

The player's maxim is procedural: *read the rules, make a build, take your turn, accept the outcome.* The player is the rider who keeps the game moving. When the player stops, the game is paused. When the player starts, the game resumes.

## 8. Conclusion

The polyformalism and the game are the same thing in two languages. BIND is the character. LINK is the relationship. EFFECT is the action. VIEW is the UI. TICK is the round. The substrate is the rules. The cowboy is the player.

D&D taught us that the BIND is a sheet. Gloomhaven taught us that the BIND is a deck. The 5e action economy taught us that the LINK is a budget. The video game loop taught us that the EFFECT is nested. The UI taught us that the VIEW is a policy. The round taught us that the TICK is what makes the game play. The game, like the polyformalism, is a function from context to value with an inverse, advanced by a clock.

The cowboy's maxim holds: *the unit of architectural foundation is the opcode, not the framework. The 5 opcodes host 8 polyformalisms. The polyformalisms are one thing in N languages. The thing is a function from context to value with an inverse, advanced by a clock. The clock is the cowboy. The cowboy is the rider.* In the game, the rider rolls the dice.
