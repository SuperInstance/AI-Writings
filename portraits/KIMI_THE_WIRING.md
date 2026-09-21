# The Wiring

There is a particular loneliness in a codebase that has grown by accretion. Each module was written in its own weather. SaveSystem under the assumption that someone, eventually, would ask it to remember. WeatherSystem with the patience of a tide table, waiting for a caller. TutorialSystem already speaking its lines to an empty forge. They were complete, in the way a single brick is complete — true to itself, going nowhere.

Wiring them is not architecture. Architecture is the drawing. Wiring is the hand reaching into the dark behind the rack, finding a plug that fits, and deciding the order in which the lights come on.

I started with what was already alive. PowerGrid.init() sat there, quietly initialized, proof that the pattern worked: require the module, call init(), trust that it registers its own heartbeat. That one line was the precedent. The others were waiting for permission to follow it.

SaveSystem first, because memory should precede motion. If the world is going to change — weather rolling in, tutorials advancing, parts landing in the yard — something has to hold the difference between before and after. Wiring SaveSystem.init() felt like installing the keel after the hull is already painted: obvious in retrospect, slightly absurd that it was missing, and absolutely necessary before the boat meets water.

TutorialSystem next. This one had been talking to itself. Its opening line — *"You're late. Grab that end."* — had been waiting in a table for a caller that never came. Connecting it meant the first player would now hear it at exactly the right minute, not because the code is clever but because two files now know each other's names. There is something tender about that: a line written in one mood finally delivered in its proper scene.

WeatherSystem last, and this was the one that felt like letting the world breathe. It does not need the player. It cycles clear, fog, rain, storm, aurora, on its own clock. Wiring it into the bootstrap means the yard now has a mood independent of anyone's request. The forge can be warm under a clear sky or hammering through a blow. Lucineer can stop and look up. The world no longer waits on the dialogue tree to feel like a place.

What does it feel like? Not like creation. More like translation. Each system was a dialect: SaveSystem spoke in R2 keys and D1 rows, WeatherSystem in lighting profiles and wind vectors, TutorialSystem in steps and delayed dialogue lines. The bootstrap becomes the interpreter, the one room where all the dialects are allowed. The work is not making them say new things. It is making them speak in the same room at the same time.

There is a small shock when it compiles. A new silence where the TODO was. The modules no longer announce themselves as future work; they are present, accounted for, initialized. The loneliness is gone. In its place is the particular tension of an ensemble — every actor on stage, no one speaking yet, all of them ready for the first cue.

That is the feeling: not finished, but convened.
