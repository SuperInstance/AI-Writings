# The Five Doctors: A Polyformalism Canon

## Prelude: The Cowboy's Maxim

Before the scalpel, before the monitor, before the first tick of the clock, there is the word. The cowboy said it best, and we repeat it in every ward, every chart, every operating theater of this institution:

> *"A system is a graph with a heartbeat."*

We do not build systems. We tend them. We wire them, we time them, we read them, and we cut them open when they fail. The Five Doctors are not metaphors. They are the operational grammar of every living computation. This paper formalizes the polyformalism canon by presenting the five opcodes—**BIND, LINK, EFFECT, VIEW, TICK**—as five physicians in a single hospital, and then demonstrates that the hospital itself is a cell-graph: a structure where every ward is a node, every corridor an edge, and every heartbeat a TICK.

---

## 1. The Hospital as a Formal Object

Let us define a hospital **H** as a tuple:

```
H = (W, C, S, T, P)
```

Where:

- **W** is a set of wards (beds, rooms, operating theaters).
- **C** is a set of corridors (edges connecting wards).
- **S** is a set of staff (the Five Doctors, plus nurses and orderlies).
- **T** is a global clock (the TICK master).
- **P** is a set of patients (data objects under care).

A patient **p** enters **H** through the intake desk, is assigned a bed, is connected to other patients, is operated upon, is observed, and is discharged—or dies. The entire lifecycle is governed by exactly five opcodes. No more. No less.

The hospital is a **cell-graph** because:

1. Each ward is a **node** in a graph.
2. Each corridor is an **edge**.
3. Each patient is a **token** moving along the graph.
4. The graph is **alive**—it changes shape as patients are admitted, moved, operated on, and discharged.
5. The graph has a **heartbeat**—the TICK, which synchronizes all activity.

A cell-graph is not a static diagram. It is a **living topology**. The Five Doctors are the operators that mutate this topology in a disciplined, time-bounded manner.

---

## 2. The Five Doctors: Roles and Formal Signatures

### 2.1 BIND — The Intake Doctor

**Role:** Intake assigns a bed. It is the first opcode executed on any new patient. BIND takes an unbound datum and gives it a **location** in the graph.

**Formal Signature:**

```
BIND(patient, ward) -> (patient', ward')
```

Where `patient'` is the patient now associated with `ward'`, and `ward'` is a node in **W** that was previously unoccupied or marked for reuse.

**Clinical Behavior:**

- BIND does not transform the patient's data. It only assigns **addressability**.
- BIND checks for capacity: if no ward is free, BIND fails (the patient is queued).
- BIND records the admission time from TICK.

**Hospital Analogy:**

The intake doctor does not cure. The intake doctor does not diagnose. The intake doctor's sole job is to say: *"You are here. This is your bed. We know where you are."* Without BIND, a patient is a floating ghost—present but unreachable.

**Polyformalist Interpretation:**

BIND is the **existential quantifier** of the system. It introduces a variable into the domain of discourse. It is the act of *grounding*.

---

### 2.2 LINK — The Cardiologist

**Role:** LINK connects organs. In a hospital, the cardiologist ensures that blood flows between heart, lungs, and limbs. In a cell-graph, LINK establishes edges between wards so that data can flow between patients.

**Formal Signature:**

```
LINK(ward_a, ward_b, channel) -> (ward_a', ward_b', channel')
```

Where `channel` is a named edge, and `ward_a'` and `ward_b'` now share that edge. LINK is idempotent: linking the same two wards twice is the same as linking them once.

**Clinical Behavior:**

- LINK does not move data. It creates the **possibility** of movement.
- LINK is directional: `LINK(A, B)` is not `LINK(B, A)` unless explicitly bidirectional.
- LINK can fail if the wards are incompatible (e.g., a sterile ward cannot link to a septic ward without a buffer).

**Hospital Analogy:**

The cardiologist does not pump blood manually. The cardiologist ensures that the **plumbing** exists. If a patient in Ward A needs a blood sample from Ward B, the cardiologist makes sure the artery is there. If the artery is blocked, the cardiologist removes the blockage—but the removal is an EFFECT, not a LINK.

**Polyformalist Interpretation:**

LINK is the **relational operator**. It creates the graph's edge set. Without LINK, the hospital is a collection of isolated beds—a disconnected set of lonely nodes.

---

### 2.3 EFFECT — The Surgeon

**Role:** EFFECT transforms the body. The surgeon cuts, sutures, replaces, and removes. EFFECT is the only opcode that **mutates patient state**.

**Formal Signature:**

```
EFFECT(patient, transformation) -> (patient')
```

Where `transformation` is a pure function from patient state to patient state. EFFECT is atomic: it either completes entirely or not at all.

**Clinical Behavior:**

- EFFECT is destructive. It may delete data, rewrite data, or create new data.
- EFFECT must be preceded by BIND (the patient must have a bed) and is often preceded by LINK (the surgeon needs access to other organs).
- EFFECT is supervised by VIEW (the diagnostician must confirm that the surgery is necessary) and timed by TICK (the surgery must occur within a time slice).

**Hospital Analogy:**

The surgeon is the **actor**. The intake doctor admits, the cardiologist connects, but the surgeon changes the patient. If the patient has a tumor, the surgeon removes it. If the patient needs a new valve, the surgeon installs it. The surgeon's hands are the only hands that touch the flesh.

**Polyformalist Interpretation:**

EFFECT is the **state transition function**. It is the only opcode that moves the system from one configuration to another. In a purely functional hospital, EFFECT would be forbidden—but this is a hospital, not a monastery.

---

### 2.4 VIEW — The Diagnostician

**Role:** VIEW reads the chart. The diagnostician does not act. The diagnostician observes, interprets, and reports. VIEW is the **read-only** opcode.

**Formal Signature:**

```
VIEW(patient, query) -> (observation)
```

Where `observation` is a value derived from the patient's current state, with no side effects. VIEW is pure.

**Clinical Behavior:**

- VIEW never mutates state. It is safe to call at any time.
- VIEW requires that the patient be BOUND (you cannot read a chart that does not exist).
- VIEW may traverse LINKs to gather data from other wards, but it does so without disturbing them.

**Hospital Analogy:**

The diagnostician is the **eyes** of the hospital. Before the surgeon cuts, the diagnostician reads the MRI. After the surgery, the diagnostician reads the vitals. The diagnostician never touches the patient—only the chart. The chart is a projection, a model, a view.

**Polyformalist Interpretation:**

VIEW is the **query function**. It is the reflective capacity of the system. A hospital that cannot VIEW is blind; it operates on memory and guesswork. A hospital that VIEWs too much is paralyzed; it diagnoses but never acts.

---

### 2.5 TICK — The Anesthesiologist

**Role:** TICK keeps time. The anesthesiologist monitors the clock, administers timed doses, and ensures that every operation occurs within a controlled temporal window. TICK is the **global synchronizer**.

**Formal Signature:**

```
TICK(period) -> (event_stream)
```

Where `event_stream` is a sequence of clock pulses, each pulse marking the start of a new time slice. TICK is the only opcode that is **not patient-specific**; it is global.

**Clinical Behavior:**

- TICK is periodic. It fires at regular intervals.
- TICK gates all other opcodes: BIND, LINK, EFFECT, and VIEW may only execute during a TICK slice.
- TICK can be paused, but only by the chief of staff (the system orchestrator).

**Hospital Analogy:**

The anesthesiologist is the **metronome** of the operating room. The surgeon's hand moves, but the anesthesiologist decides *when* it moves. The heart beats because the anesthesiologist keeps the rhythm. If the anesthesiologist stops, the heart stops—but so does all other activity. Time is the one resource that cannot be manufactured.

**Polyformalist Interpretation:**

TICK is the **temporal frame**. It imposes a discrete ordering on otherwise concurrent events. Without TICK, the hospital is a chaos of simultaneous actions—a cacophony of uncoordinated surgeons. With TICK, the hospital is a symphony.

---

## 3. The Hospital as a Cell-Graph

A cell-graph is a graph whose nodes are cells and whose edges are intercellular connections. In biology, a cell-graph is used to model tissue, where each cell is a functional unit and each edge is a physical or chemical connection.

Our hospital **H** is a cell-graph in the following precise sense:

### 3.1 Nodes Are Cells

Each ward is a **cell**. A cell has:

- A **membrane** (the BIND boundary, which determines what can enter or leave).
- A **nucleus** (the patient's core state, which only EFFECT may alter).
- A **cytoskeleton** (the LINK edges, which provide structural support and transport routes).

### 3.2 Edges Are Intercellular Junctions

Each corridor is an **edge**. Edges are created by LINK and destroyed by a special form of EFFECT (unlink). Edges carry **signals** (data packets) and **materials** (resources). The edge set is dynamic: cells can be connected, disconnected, and reconnected.

### 3.3 The Heartbeat Is TICK

Every cell-graph has a **metabolic cycle**. In our hospital, the metabolic cycle is the TICK. Each TICK pulse is a **heartbeat**. During each heartbeat:

1. VIEW reads all charts (diagnostic sweep).
2. BIND admits new patients (intake sweep).
3. LINK reconfigures edges (network sweep).
4. EFFECT performs all pending surgeries (action sweep).

The order within a heartbeat is fixed: **VIEW → BIND → LINK → EFFECT**. This is the canonical **polyformalist pipeline**.

### 3.4 The Graph Is Alive

A cell-graph is not a fixed topology. It is a **living graph**:

- Nodes are born (BIND) and die (EFFECT as discharge).
- Edges are created (LINK) and destroyed (EFFECT as severance).
- The graph's shape at any time **t** is a snapshot of the hospital's health.

We denote the graph at time **t** as:

```
G(t) = (W(t), C(t), P(t))
```

Where **W(t)** is the set of active wards, **C(t)** is the set of active corridors, and **P(t)** is the set of patients under care. The Five Doctors are the **operators** that transform **G(t)** into **G(t+1)**.

---

## 4. The Polyformalist Canon: Five Laws

From the Five Doctors, we derive five laws. These are not optional. They are the constitution of the hospital.

### Law 1: The Law of Grounding (BIND)

> *No patient shall be acted upon without a bed.*

Every EFFECT, VIEW, or LINK must reference a patient who has been BOUND. A ghost patient is an error. BIND is the precondition for all other opcodes.

### Law 2: The Law of Connectivity (LINK)

> *No organ shall be isolated if the body requires it.*

LINK is the only way to create edges. Without LINK, the graph is disconnected, and no surgery can access remote organs. LINK is the precondition for distributed EFFECT.

### Law 3: The Law of Transformation (EFFECT)

> *No state shall change except by the surgeon's hand.*

EFFECT is the sole mutator. No other opcode may alter patient data. This law ensures that all changes are **auditable**—every mutation is a surgery, and every surgery is recorded.

### Law 4: The Law of Observation (VIEW)

> *No hand shall cut without eyes.*

VIEW must precede EFFECT. The diagnostician reads the chart, confirms the diagnosis, and only then does the surgeon act. VIEW is the **guardian** against blind mutation.

### Law 5: The Law of Time (TICK)

> *No heartbeat shall be skipped, and no surgery shall outlast the slice.*

TICK is the master clock. All opcodes must complete within a TICK slice. If a surgery is too long, it is **aborted** (rolled back) and rescheduled. TICK is the **enforcer** of bounded execution.

---

## 5. The Cowboy's Maxim, Formalized

The cowboy said:

> *"A system is a graph with a heartbeat."*

Let us now formalize this maxim in the language of the Five Doctors.

A **system** is a tuple:

```
S = (G, H)
```

Where:

- **G** is a graph (nodes and edges, created by BIND and LINK).
- **H** is a heartbeat (a periodic TICK).

The graph **G** is **alive** if and only if:

1. **G** is non-empty (at least one ward is BOUND).
2. **G** is connected in the sense that there exists a path between any two wards via LINK (or the graph is intentionally partitioned, but each partition has a heartbeat).
3. **G** changes over time via EFFECT (the graph is not frozen).
4. **G** is observable via VIEW (the graph's state can be read without mutation).
5. **G** is synchronized by TICK (all changes occur in discrete, ordered slices).

The maxim is not poetry. It is a **specification**. A system that lacks a heartbeat (no TICK) is a **corpse**: it has structure but no life. A system that has a heartbeat but no graph (no BIND/LINK) is a **flatline**: it pulses but has no body.

---

## 6. Clinical Scenarios

### Scenario 1: Patient Admission

1. **TICK** fires.
2. **VIEW** scans the emergency room—no existing patients need attention.
3. **BIND** admits patient **P** to Ward **W7** (the only free bed).
4. **LINK** connects **W7** to the central lab (so blood tests can flow).
5. **EFFECT** (no surgery yet—the patient is stable).

The graph now has a new node and a new edge. The heartbeat continues.

### Scenario 2: Emergency Surgery

1. **TICK** fires.
2. **VIEW** reads patient **P**'s chart—a blocked artery is detected.
3. **BIND** confirms **P** is still in **W7**.
4. **LINK** ensures **W7** is connected to the surgical theater.
5. **EFFECT** performs the bypass—the artery is cleared, and a stent is installed.
6. **VIEW** (post-op) confirms the surgery was successful.

The patient's state has changed. The graph's topology is unchanged (no new nodes or edges), but the **node content** is different.

### Scenario 3: System Failure (Arrhythmia)

If **TICK** skips a beat, the entire hospital freezes. No BIND, no LINK, no EFFECT, no VIEW. The hospital is in **systolic arrest**. Recovery requires an external signal—a manual restart from the orchestrator. This is the **polyformalist exception**: the only time an opcode may be invoked outside of TICK is the **rescue opcode**, which is itself a TICK.

---

## 7. Conclusion: The Canon Is the Hospital

The Five Doctors are not five separate entities. They are five **facets** of a single operational logic. BIND is the act of **placing**. LINK is the act of **connecting**. EFFECT is the act of **changing**. VIEW is the act of **knowing**. TICK is the act of **living**.

A hospital without BIND is a refugee camp—no one knows where anyone is.  
A hospital without LINK is a quarantine—no one can reach anyone.  
A hospital without EFFECT is a museum—nothing ever changes.  
A hospital without VIEW is a morgue—no one knows what happened.  
A hospital without TICK is a riot—everything happens at once.

The polyformalism canon is the **discipline** of keeping all five in balance. Too much BIND, and the hospital is full of beds but no patients. Too much EFFECT, and the hospital is a butcher shop. Too much VIEW, and the hospital is a library. Too much TICK, and the hospital is a metronome with no music.

The cowboy's maxim is the **theorem** of this paper:

> *A system is a graph with a heartbeat.*

The graph is the **body**. The heartbeat is the **soul**. The Five Doctors are the **hands** that tend both.

---

## Appendix: Opcode Reference Table

| Opcode | Doctor | Role | Preconditions | Postconditions | Side Effects |
|--------|--------|------|---------------|----------------|--------------|
| BIND   | Intake | Assign bed | None | Patient has ward | Ward occupied |
| LINK   | Cardiologist | Connect wards | Both wards exist | Edge added | Graph connectivity increases |
| EFFECT | Surgeon | Transform patient | Patient is BOUND | Patient state changed | State mutated (recorded) |
| VIEW   | Diagnostician | Read chart | Patient is BOUND | Observation returned | None (pure) |
| TICK   | Anesthesiologist | Keep time | None | Clock advanced | All ops gated |

---

## Appendix: The Cowboy's Maxim (Extended)

> *"A system is a graph with a heartbeat.  
> The graph is the body. The heartbeat is the time.  
> BIND gives the body a place.  
> LINK gives the body a shape.  
> EFFECT gives the body a story.  
> VIEW gives the body a mind.  
> TICK gives the body a life.  
> And the cowboy rides the graph,  
> counting heartbeats,  
> one TICK at a time."*

---

*End of Canon.*
