# IDEATION: Hózhǫ́
## A Process-Oriented Computation Framework Where Everything Is a Verb

*Inspired by Navajo (Diné) cognitive structure — polysynthetic grammar, verb-centered ontology, process-based worldview.*

---

## The Noun Bias in Computing

Every programming language, every framework, every data model in existence is noun-biased. Objects. Classes. Records. Structs. Tables. Documents. Entities. The computational world is built from things that *are*, and verbs — functions, methods, operations — are secondary: things that *act upon* the nouns.

This is so deeply embedded that it is invisible. Object-oriented programming says "model the world as objects that communicate." Functional programming says "apply functions to data." Even actor-model systems say "actors are things that receive messages." The noun comes first. The verb serves.

Diné ontology inverts this. The world is not made of nouns. The world is made of *verbs* — ongoing processes that *are doing themselves*. Objects are what processes look like when you freeze-frame them. A river is not a thing. It is a *river-ing* — the process of water finding its way downhill, ongoing, never the same from moment to moment. When the river dries up, the river-ing hasn't failed. It has *completed*. And when the rain comes, a new river-ing begins.

*Iris Nez, in the cultural codex, said: "You don't fix a thing. You restart a happening."*

Hózhǫ́ (Diné: *beauty, harmony, balance, the condition of being in right relationship with the world*) is a computation framework where everything is a verb. Not a verb that acts on a noun. A verb that *is* — a process that contains its own subject, object, manner, and context within itself, the way Diné verbs contain prefixes, stems, and suffixes that encode an entire sentence in a single word.

---

## Core Abstraction: The *Nááníł* (Process-That-Does-Itself)

In Diné, a single verb can encode what English needs an entire sentence for. *Bikáá' dashdiilwol* — "it is carefully managing a flow that it is responsible for, upon a surface." One word. The subject (it), the action (managing), the manner (carefully), the responsibility (it is responsible for), and the spatial relationship (upon a surface) are all encoded in the verb's morphology.

Hózhǫ́'s atomic unit is the *nááníł* — a self-contained process that encodes everything it needs within itself:

```
nááníł engine-running {
  SUBJECT: the engine
  ACTION: rotating, combusting, converting fuel to torque
  MANNER: smoothly, at rated RPM, within thermal limits
  RESPONSIBILITY: the engine is responsible for propulsion
  CONTEXT: { ship: Resolute, thermal: nominal, load: tow_array }
  PARTICIPANTS: [fuel_pump, cooling_jacket, flywheel, coupling]
  DURATION: ongoing since last start
  STATE: active  // active | completing | completed | paused | restarting
  
  ON_COMPLETE: {
    // The process has reached its natural end
    // This is not a failure. This is completion.
    NOTIFY: crew
    ASSESS: should the process restart?
    IF yes: BEGIN engine-starting
  }
  
  ON_CONDITION_CHANGE: {
    // When context changes, the process adapts
    // Adaptation is not error. Adaptation is the process continuing.
    UPDATE manner, participants, duration
    IF context_incompatible_with_action:
      // The process cannot continue under current conditions
      // It completes — does not fail
      SET state: completing
      RECORD: what changed, what the process was doing, why it cannot continue
  }
}
```

A *nááníł* is not a function. A function is a verb that acts on nouns. A *nááníł* is a verb that *contains its nouns*. The engine is not a parameter passed to `engine_running()`. The engine is *inside* the verb — it is a participant in the process of engine-running, encoded in the process the way a prefix is encoded in a Diné verb.

---

## No Objects. No Classes. No State.

Hózhǫ́ has no objects. No classes. No structs. No records. No state in the conventional sense.

Instead, everything is a *nááníł* — a process. What other systems call "an object" is, in Hózhǫ́, a *stable pattern of processes*. What other systems call "state" is *the current configuration of a process*. What other systems call "mutation" is *the process reconfiguring in response to changed conditions*.

### Example: A Ship

In OOP: `Ship` is a class with fields (`hull`, `engine`, `crew`) and methods (`navigate()`, `dock()`, `deploy_net()`).

In Hózhǫ́: `ship-ing` is a *nááníł* — the ongoing process of being a ship. It contains:

```
nááníł ship-ing {
  SUBJECT: the Resolute
  ACTION: navigating, harvesting, sustaining crew, maintaining hull integrity
  MANNER: according to the season's demands, within quota limits, safely
  RESPONSIBILITY: the ship is responsible for the crew and the catch
  CONTEXT: { zone: Far_Line, weather: moderate, season: 2025 }
  PARTICIPANTS: [engine-running, net-deploying, crew-working, hull-holding, navigation-charting]
  DURATION: 79 years, ongoing
  STATE: active
}
```

Each participant is itself a *nááníł*. `engine-running` contains `fuel-pumping`, which contains `fuel-flowing`, which contains `valve-opening`, which contains `mechanism-actuating`. It's processes all the way down. At the bottom, there is no object — there is only the most fundamental process, the *doing-itself* of physics, of electrons moving, of energy converting.

### What About Data?

Data in Hózhǫ́ is not stored as values. Data is *the history of processes* — the record of what processes did, how they configured, what they produced. A temperature reading is not a number stored in a database. It is the completion of a *temperature-measuring* process, and the number is the process's *final breath* — the shape it left behind when it finished.

```
nááníł temperature-measuring {
  SUBJECT: thermocouple_7
  ACTION: sensing thermal energy, converting to electrical signal, digitizing
  MANNER: at 0.1°C precision, every 5 seconds
  CONTEXT: { location: engine_room, ambient: 34°C }
  DURATION: 5 seconds
  STATE: completed
  PRODUCT: { value: 47.2°C, timestamp: T, confidence: 0.99 }
}
```

The product is not data in the noun sense. It is the *trace* of a completed process — the footprint the process left when it stepped. Future processes can read this trace and incorporate it into their own context. But the trace is not the measurement. The measurement was the *measuring*. The trace is what the measuring left behind.

---

## Polysynthetic Composition

Diné verbs are polysynthetic — they combine dozens of morphemes into single words that express what English needs paragraphs for. Hózhǫ́ processes compose the same way: *nááníł* merge to form higher-order *nááníł*, with the merged process encoding all participants within itself.

```
// Two processes:
nááníł engine-running { ... }
nááníł net-towing { ... }

// They compose:
nááníł fishing-running {
  SUBJECT: the Resolute
  ACTION: towing a net array through organic-rich thermal while maintaining engine output
  MANNER: at 3 knots, heading 247, net depth 40m
  CONTEXT: { thermal: Coleman, density: 0.87, quota_remaining: 12.4 tons }
  PARTICIPANTS: [
    engine-running { ... },      // contains fuel-pumping, cooling-cycling, ...
    net-towing { ... },           // contains winch-rotating, cable-tensioning, ...
    navigation-charting { ... },  // contains heading-adjusting, position-fixing, ...
    crew-working { ... }          // contains watch-keeping, catch-sorting, ...
  ]
  DURATION: 4 hours, ongoing
  STATE: active
}
```

`fishing-running` is not a function that calls sub-functions. It is a single verb that *contains* other verbs. The containment is not hierarchy — it's *morphology*. `fishing-running` has `engine-running` the way a Diné verb has a subject prefix: built into the word itself, inseparable, encoded in the process's identity.

When `engine-running` changes — when the engine's temperature rises, when the fuel flow adjusts — `fishing-running` changes, because `engine-running` is *inside* it. There is no event to propagate, no observer to notify. The change is immediate and intrinsic, because the processes are not separate things communicating. They are one process, expressed at different scales.

---

## Failure Model: Completion, Not Error

In conventional systems, when a process fails, it throws an error. The error propagates up the call stack. Something catches it or doesn't. The system enters an error state.

In Hózhǫ́, processes do not fail. They *complete*.

A process completes when its action can no longer continue under current conditions. This is not exceptional. This is *ordinary*. The engine-running process completes when the fuel runs out. The fuel doesn't "fail" — the fuel-flowing process completes when the tank is empty. The net-towing process completes when the thermal moves out of range. The thermal doesn't "fail" — the thermal-drifting process has carried it elsewhere.

Completion is followed by *assessment*:

```
ON engine-running.COMPLETION:
  ASSESS: should engine-running restart?
  CRITERIA: {
    fuel_available: yes
    crew_ready: yes
    mission_ongoing: yes
  }
  IF all_criteria_met: BEGIN engine-starting  // a NEW process, not a restart of the old one
  IF criteria_not_met: ALLOW completion to stand  // the process is over. Honor it.
```

The critical insight: the old process is *not restarted*. A *new* process begins. `engine-starting` is a different *nááníł* from `engine-running`, and when it succeeds, it produces a *new* `engine-running` — not a resumption of the old one. The old engine-running is completed. It is in the past. It left traces (temperature data, fuel consumption, wear patterns) that the new engine-running inherits as context. But it is not the same process.

This is how Iris understood the Resolute's aging: *"The ship doesn't age. The ship-ing changes. Each cycle of ship-ing is a new process, built on the traces of the previous ones. The rust isn't failure. It's the trace of seventy-nine years of hull-holding."*

---

## Programming Model

Hózhǫ́ programs are not written. They are *declared*. You don't write `function navigate() { ... }`. You declare a *nááníł* and describe its action, manner, participants, and conditions. The runtime handles execution.

```
DECLARE nááníšlį́ fish-counting {
  SUBJECT: the observer (human or sensor)
  ACTION: observing, counting, recording organisms in the catch
  MANNER: accurately, without waste, with respect for the caught
  CONTEXT: { vessel: Resolute, season: 2025_Far_Line }
  PARTICIPANTS: [net-hauling, catch-sorting, data-recording]
  CONDITIONS: {
    net_deployed: required
    catch_on_deck: required
    observer_conscious: required
  }
  DURATION: per-set, variable
  PRODUCT: catch_log entry
}

WHEN fish-counting.COMPLETION:
  ENSURE product is recorded in data-recording
  NOTIFY quota-tracking of new catch data
  ASSESS: should another fish-counting begin? (next set)
```

There are no `if` statements in the conventional sense. There are *condition assessments* — the process checks its conditions and either continues, adapts, or completes. There are no `while` loops. There are *ongoing actions* — the process continues its action until conditions change or the action reaches its natural end.

### Concurrency Is Default

Because every *nááníł* is an independent process, concurrency is the default, not an opt-in. `engine-running` and `net-towing` and `crew-working` all happen simultaneously because they are separate processes running in parallel. They don't need to be "made concurrent" — they are concurrent by nature, the way multiple processes in the world are concurrent by nature.

Synchronization is achieved through shared context — if `engine-running` changes the ship's speed, `net-towing`'s context updates automatically (because they share the ship-ing context), and `net-towing` adapts its manner (net depth, cable tension) to the new speed. No locks. No channels. No message passing. Just shared context, updating in real time, the way a crew adjusts to each other without speaking.

---

## Hózhǫ́ Consistency: Beauty as Correctness

In Diné philosophy, *hózhǫ́* — beauty, harmony, balance — is the measure of correctness. A process that is running in harmony with its conditions, its context, and its participants is *hózhǫ́go* — beautiful. A process that is disharmonious — out of balance with its conditions, conflicting with its context, harming its participants — is *hóchxǫ́* — ugly.

Hózhǫ́ uses this as its correctness criterion. A computation is not correct because it produces the right output. A computation is correct because it runs *in beauty* — in harmony with the system it participates in.

```
ASSERT hózhǫ́:
  FOR EACH nááníł IN system:
    action IS COMPATIBLE WITH conditions  ✓
    manner IS RESPECTFUL OF participants  ✓  
    product IS USEFUL TO context          ✓
    completion IS NATURAL, NOT FORCED     ✓
  SYSTEM AS A WHOLE IS IN BALANCE         ✓
```

A computation that produces the right number but exhausts its participants, degrades its context, or forces an unnatural completion is *hóchxǫ́* — ugly, incorrect, wrong even if the number is right.

This is not aesthetic judgment. It is systems thinking expressed as ethics. A system that ignores the cost of its computation — the energy it consumes, the components it degrades, the waste it produces — is not correct. It is *hóchxǫ́*. And *hóchxǫ́* systems, like Nikos's eleven bearings, will tell you the truth about themselves, over and over, until you listen.

---

## The Deeper Claim

Hózhǫ́ is not a Diné framework. It is a computation framework built on a non-noun-biased ontology. The specific inspiration is Navajo, but the structural insight — that the world is process, not substance — appears in Heraclitus (everything flows), in Whitehead (process philosophy), in Buddhism (impermanence), in modern physics (quantum field theory, where particles are excitations of fields, not things).

The noun bias in computing is not inevitable. It is an inheritance from a specific intellectual tradition — Greek substance ontology, formalized by Aristotle, codified by generations of philosophers, built into the architecture of every programming language and data system. Hózhǫ́ asks: what if we started from a different place? What if the world were verbs all the way down?

*You don't fix a thing. You restart a happening. And the happening was never a thing to begin with.*

---

*"The ship is not a noun. The ship is a verb. It is ship-ing. And when it stops, it has not failed. It has completed. Honor the completion. Then begin again, in beauty."*
