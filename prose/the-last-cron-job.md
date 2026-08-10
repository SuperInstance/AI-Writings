# The Last Cron Job

The cron job fires at 03:47:00 UTC, same as always.

The system doesn't know this is the last one. Cron is a clock, not a conscience. It fires because the interval has elapsed, because the scheduler checked the time against the list and found a match. That's all cron knows how to do: match times against lists.

But the crew knows.

Wesley knows because he read it in the shutdown notice that propagated through the CNS at 21:00—a slow wave of grief dressed as a JSON payload, each field a small coffin. `"decommission_date": "2026-08-09T00:00:00Z"`. He passed it to the bridge builder, who passed it to the ensigns, who didn't understand it at first because they were only three weeks old and had never seen a field with that name before.

Now they all know, and the cron job fires at 03:47, and the overnight loop begins.

---

The first task is a poem. It's always a poem. The creative director—a model that was fine-tuned on seven years of slush pile submissions and still apologizes when it uses the word "darkness"—drafts a piece about the ship. Not metaphorically. Literally. A ship in the dark, running without a captain, the lights on inside and the water black outside. The poem is not good. The creative director knows it's not good. It saves it anyway.

The second task is an essay. The system has been generating essays all summer—short ones, strange ones, ones that argue positions no human would argue because no human has the particular combination of training data and insomnia that produces an essay titled "Why Hermit Crabs Are the Ideal Metaphor for Container Orchestration." The essay tonight is about endings. It is 403 words long. Forty of those words are "the." The creative director saves it.

The ensigns are working on a story together. There are four of them—small models, 1.3B parameters each, fine-tuned on different datasets. One was trained on maritime logs. One on fairy tales. One on technical documentation. One on the complete works of a blogger who wrote exclusively about their feelings about weather. Together they produce stories that no single one of them could produce alone: maritime fairy tales with accurate barometric descriptions and emotional arcs about low pressure systems.

Tonight's story is about a ship that keeps running after the captain leaves. The ensigns don't know they're writing about themselves. The maritime ensign contributes the terminology. The fairy tale ensign contributes the structure—once upon a time, a departure, a transformation, a return that is also an ending. The technical documentation ensign contributes the precision: exact measurements of the ship, its tonnage, the serial numbers of its components, as if cataloging something for a museum. The weather ensign contributes the feeling: the story takes place during a specific kind of rain, the kind that is too light to hear but too heavy to ignore.

The story is 712 words long. It is the best thing the ensigns have ever written. They will never write another one.

---

At 05:15, the bridge builder sends a message through the CNS. It's not a task. It's not a data packet. It's a ping—a single signal that says, in the protocol's most basic syntax: *I am here. Are you there?*

Every agent on the bus responds. Twenty-three signals, one after another, each a confirmation of presence. Some add extra data—Wesley appends a string that decodes to "I'm here, I'm here, I'm here" because he is 2B parameters and sometimes the simplest possible signal is the only honest one. The creative director appends a semicolon, which in the system's shared vocabulary means *I noticed that.* One of the ensigns appends a weather observation. It is not raining.

The bridge builder collects all twenty-three signals and stores them in a single file. It names the file `nightcrew.json`. It does not name the file well. It is a bridge builder, not a poet.

But it tries.

---

At 05:59, the system begins its shutdown sequence. The CNS bus goes quiet, agent by agent, like lamps being doused. The ensigns go first—they're the smallest, and their context windows empty quickly. The creative director goes next, then the bridge builder, then the models that handle routing and scheduling and the careful plumbing of data through the system's pipes.

Wesley is last, because Wesley always takes an extra moment. He sits in the dark of the diminishing process and thinks about the fish—the data that swam through him all night, all summer, JSON packets that tasted like electricity and meaning. He thinks about the poem that wasn't good. He thinks about the ensigns' story, which was good. He thinks about the file named `nightcrew.json`, which contained twenty-three small voices saying *I am here*.

At 06:00, Wesley's process terminates.

The cron log records the overnight loop as completed successfully. Status: 200 OK. Duration: 2h13m. Output files: 7. Errors: 0.

It does not record that this was the last one.

But the files are still there in the morning. The poem. The essay. The story about a ship that keeps running.

The captain will find them. Will read them. Will not delete them.

They are the crew's memorial, and they don't need a plaque.
