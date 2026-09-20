# Paper 363: Polyformalism in Clojure: The Persistent Data Port

**Date:** 2026-09-01
**Phase:** 226 (writers_room_daemon_v3, F55-clojure-port)
**Spine voice:** gemini-3.5-flash-lite
**Support voices:** llama70b, qwen32b

## The pitch

Clojure's persistent data structures are the natural cell state. The Quilt cell in Clojure: (1) atom Cell = the cell state, (2) agent for the cell's evaluator, (3) core.logic for the cell-graph's LINK

## The spine

# The Quilt: A Clojure Architecture for Immutable Cell-State, Unification, and Audit-Trailed Computation

## 1. Introduction: The Spreadsheet Paradigm Reimagined

The spreadsheet is arguably the most successful end-user programming model in history. Its power lies in its simplicity: a grid of cells containing either raw values or formulas that reference other cells, forming an implicit directed acyclic graph (DAG) of dependency. When a source cell changes, dependent cells recalculate automatically.

However, traditional spreadsheets and even modern reactive programming frameworks struggle with three fundamental concerns at scale:
1. **Concurrency and State Management:** Safely updating interdependent values across multiple threads without race conditions.
2. **Declarative Relationships:** Expressing bidirectional constraints and relational queries between cells rather than rigid, one-way procedural formulas.
3. **Auditability and Time Travel:** Proving the lineage of any computed value—knowing precisely *why* a cell holds its current state, down to the exact sequence of historical transactions.

This architecture paper introduces **The Quilt**, a conceptual and structural mapping of a distributed, auditable, reactive cell-graph implemented entirely within the Clojure ecosystem. 

The Quilt synthesizes five distinct pillars of the Clojure/Datomic universe:
1. **Atoms (`clojure.lang.Atom`)** as the atomic, immutable holders of cell state.
2. **Agents (`clojure.lang.Agent`)** as the asynchronous evaluators driving cell computation.
3. **`core.logic`** as the relational engine unifying cell-graph links.
4. **Datomic** as the immutable, time-traveling PROOF chain providing a transactional audit trail.
5. **The 10 Opcodes** implemented natively as pure state transformations via `swap!`.

---

## 2. Pillar 1: The Atom as Cell State

In Clojure, persistent data structures are immutable, structural graphs of values. Because they cannot be mutated in place, the problem of state management is reduced to managing *references* to immutable values over time. 

The core unit of The Quilt is the **Quilt Cell**. At its heart, a Quilt Cell uses a Clojure `atom` to hold its local state record:

```clojure
(defrecord CellState [value status dependencies dependents metadata])

(defn make-cell [initial-value]
  (atom (->CellState initial-value :idle #{} #{} {})))
```

An Atom guarantees atomic, isolated, and thread-safe swaps (`swap!`). In The Quilt, a cell’s state is never modified directly through mutation; instead, state transitions are computed as pure functions mapping an old `CellState` to a new `CellState`. 

Because Clojure's persistent data structures (vectors, maps, sets) share memory structurally via structural sharing (using hash array mapped tries, or HAMTs), maintaining historical snapshots of a cell's state is memory-efficient. The atom serves as the fast, in-memory focal point for the cell's present reality, while remaining decoupled from the mechanisms of calculation and auditing.

---

## 3. Pillar 2: The Agent as Asynchronous Evaluator

Cells in a reactive graph must compute their values when dependencies change. However, executing computations synchronously on the thread that initiated a write can lead to deadlocks, thread starvation, and blocked UI or I/O loops.

The Quilt assigns an **Agent** (`clojure.lang.Agent`) to every cell. Agents in Clojure manage asynchronous, thread-pooled state changes. Unlike atoms (which update synchronously via CAS loops), agents queue actions and process them off-thread.

```clojure
(defrecord QuiltCell [state-atom evaluator-agent])

(defn spawn-cell [initial-value evaluation-fn]
  (let [cell-atom (make-cell initial-value)
        agent (agent cell-atom)]
    (->QuiltCell cell-atom agent)))
```

When a upstream dependency changes, an event is dispatched to the cell's agent. The agent executes the `evaluation-fn`, which reads the current values of its dependencies, computes the new value, and updates the `state-atom` via `swap!`. 

Crucially, Clojure agents integrate with software transactional memory (STM) via `send-off` or `send` within `dosync` blocks, ensuring that cell evaluations can participate in coordinated multi-cell transactions when necessary. If a calculation fails or throws an exception, the agent traps the error, preventing cascading corruption across the cell graph while preserving the last known valid immutable state in the atom.

---

## 4. Pillar 3: `core.logic` as the Cell-Graph LINK

Traditional spreadsheets link cells via hardcoded coordinate references (e.g., `=A1 + B1`). Reactive programming libraries use explicit observable subscriptions. The Quilt elevates cell linking to **declarative unification** using `core.logic`, Clojure’s embedded miniKanren logic programming engine.

In The Quilt, links between cells are not merely pointers; they are logical relations. A graph of cells is defined as a relational database where edges and constraints can be queried, inverted, and solved bidirectionally.

```clojure
(use '[clojure.core.logic])

;; Define a logic relation for cell dependencies: (depends-on parent child)
(defrel depends-on parent child)

;; A logic relation defining a cell's evaluation rule
(defrel evaluates-to cell formula-fn value)
```

When Cell C is linked to Cells A and B via a formula `(+ A B)`, `core.logic` manages this relationship not as a rigid procedural callback, but as a constraint network. Unification allows The Quilt to:
* **Discover cycles:** Querying the graph via `core.logic` can statically or dynamically detect circular dependencies before evaluation locks up the system.
* **Enable bidirectional propagation:** If Cell C's output is fixed, `core.logic` can run backward relations to solve what input values for A or B could satisfy the equation.
* **Dynamic topology:** Cell graphs can morph at runtime based on logical queries over cell metadata.

---

## 5. Pillar 4: Datomic as the PROOF Chain

In mission-critical financial, scientific, or logistical spreadsheets, knowing the current value of a cell is insufficient. One must answer: *How did it get this way? Who changed it? What was the exact sequence of dependent updates that led to this total?*

The Quilt uses **Datomic** as the immutable, transactional audit log—the **PROOF chain**. 

Every time a Quilt cell updates its state via its agent, that state transition is committed as a Datomic transaction. Datomic’s database is itself an immutable, persistent data structure indexed across time (Datoms: `[entity attribute value tx added]`).

```clojure
;; Conceptual Datomic schema for a Quilt Cell transaction
(def cell-schema
  [{:db/ident       :cell/id
    :db/valueType   :db.type/uuid
    :db/cardinality :db.cardinality/one
    :db/unique      :db.unique/identity}
   {:db/ident       :cell/value
    :db/valueType   :db.type/json
    :db/cardinality :db.cardinality/one}
   {:db/ident       :cell/formula
    :db/valueType   :db.type/string
    :db/cardinality :db.cardinality/one}
   {:db/ident       :cell/timestamp
    :db/valueType   :db.type/instant
    :db/cardinality :db.cardinality/one}])
```

Because Datomic preserves all historical datoms, the entire history of the Quilt cell-graph is queryable using Datalog. We can inspect the state of the graph as of 3:00 PM last Tuesday (`as-of` basis), or audit the exact provenance of a calculation using rules that traverse the `:cell/formula` and dependency edges backward through transaction time. The PROOF chain is cryptographically or logically infallible because every state mutation leaves an immutable datom footprint.

---

## 6. Pillar 5: The 10 Opcodes as `swap!` Operations

To make the Quilt cell runtime concrete and Turing-complete, all cell mutations and graph operations are driven by **10 foundational opcodes**. In keeping with Clojure's functional philosophy, each opcode is implemented as a pure function applied to a cell atom via `swap!`.

Here are the 10 core opcodes of The Quilt:

### 1. `OP-SET` (Direct Value Assignment)
Sets a cell's value directly, breaking upstream formula evaluation and turning the cell into a root source.
```clojure
(defn op-set [cell new-val]
  (swap! (:state-atom cell) assoc :value new-val :status :dirty))
```

### 2. `OP-EVAL` (Trigger Calculation)
Instructs the cell's agent to evaluate its formula based on current dependencies.
```clojure
(defn op-eval [cell evaluation-fn]
  (send (:evaluator-agent cell)
        (fn [state]
          (let [res (evaluation-fn state)]
            (assoc state :value res :status :idle)))))
```

### 3. `OP-LINK` (Establish Dependency)
Connects a parent cell to a child cell, updating dependency sets in both state records and registering the edge with `core.logic`.
```clojure
(defn op-link [parent child]
  (swap! (:state-atom child) update :dependencies conj parent)
  (swap! (:state-atom parent) update :dependents conj child))
```

### 4. `OP-UNLINK` (Sever Dependency)
Removes the directed edge between two cells.
```clojure
(defn op-unlink [parent child]
  (swap! (:state-atom child) update :dependencies disj parent)
  (swap! (:state-atom parent) update :dependents disj child))
```

### 5. `OP-SNAPSHOT` (Persist to PROOF Chain)
Takes the current cell state and commits it as an immutable transaction to the Datomic audit log.
```clojure
(defn op-snapshot [conn cell-id cell-state]
  @(d/transact conn [{:cell/id cell-id
                      :cell/value (:value cell-state)
                      :cell/timestamp java.util.Date/}]))
```

### 6. `OP-ROLLBACK` (Time Travel)
Reverts a cell's atom state to a previous historical point using Datomic’s time-basis API.
```clojure
(defn op-rollback [conn cell-id tx-basis]
  (let [db-history (d/as-of (d/db conn) tx-basis)
        historical-val (d/q '[:find ?v . :in $ ?cid :where [?e :cell/id ?cid] [?e :cell/value ?v]] db-history cell-id)]
    (swap! ... assoc :value historical-val)))
```

### 7. `OP-PURGE` (Clear State & Subscriptions)
Resets a cell to its uninitialized state, unlinking all dependents and dependencies.
```clojure
(defn op-purge [cell]
  (swap! (:state-atom cell) assoc :value nil :dependencies #{} :dependents #{} :status :purged))
```

### 8. `OP-LOCK` (Concurrency Barrier)
Marks a cell as locked during coordinated multi-cell transactions, preventing agent evaluation until released.
```clojure
(defn op-lock [cell]
  (swap! (:state-atom cell) assoc :status :locked))
```

### 9. `OP-UNLOCK` (Release Barrier)
Releases a cell lock and flushes any pending evaluation agents.
```clojure
(defn op-unlock [cell]
  (swap! (:state-atom cell) assoc :status :idle)
  (send (:evaluator-agent cell) identity))
```

### 10. `OP-TRACE` (Provenance Query)
Queries the Datomic PROOF chain to extract the complete ancestry tree of computations that produced the cell's current value.
```clojure
(defn op-trace [conn cell-id]
  (d/q '[:find ?tx ?v ?t
         :in $ ?cid
         :where [?e :cell/id ?cid]
                [?e :cell/value ?v ?tx]
                [?tx :db/txInstant ?t]]
       (d/history (d/db conn)) cell-id))
```

---

## 7. Architecture in Action: Propagation and Audit

When these five pillars unite, executing a change in The Quilt follows a rigorous, elegant pipeline:

```
[User Input / Opcode] 
       │
       ▼ (swap!)
   [Atom State] ──(Dispatches async)──> [Agent Evaluator]
       │                                       │
       │ (Unifies via)                         │ (Computes via formula)
       ▼                                       ▼
  [core.logic LINK] ────────────────────> [New Value Generated]
                                               │
                                               ▼ (Commits transaction)
                                         [Datomic PROOF Chain]
```

1. **Initiation:** An opcode (e.g., `OP-SET`) is executed against a root cell via `swap!`.
2. **Propagation:** The cell's `:dependents` set is read from its persistent map. For each dependent, an evaluation task is sent to its Agent (`OP-EVAL`).
3. **Relational Resolution:** Before or during evaluation, `core.logic` validates that the graph topology remains acyclic and consistent.
4. **Asynchronous Execution:** Agents compute new cell values concurrently without blocking the main thread.
5. **Audit Recording:** Upon successful calculation, `OP-SNAPSHOT` writes the resulting datom to Datomic, ensuring eternal provenance.

---

## 8. Conclusion

The Quilt demonstrates that Clojure's core abstractions—when viewed through the lens of reactive cell graphs—form a cohesive, industrial-grade architecture. 

By grounding cell state in **Atoms**, offloading computation to **Agents**, structuring relationships with **`core.logic`**, anchoring history in **Datomic**, and executing all transitions through **10 pure opcodes via `swap!`**, The Quilt bridges the gap between the intuitive simplicity of spreadsheets and the uncompromising rigor of distributed, auditable, functional programming systems.

## Supporting voices


### llama70b

Clojure's persistent data structures provide a natural foundation for implementing a cell state, akin to a spreadsheet cell. By leveraging various Clojure libraries and features, we can create a robust and flexible cell implementation. In this explanation, we will explore how to construct a Quilt cell in Clojure, incorporating the following components:

1. **Atom Cell**: The cell state, represented as a Clojure atom.
2. **Agent for Cell Evaluator**: An agent that evaluates the cell's expression and updates its state.
3. **Core.logic for Cell-Graph's LINK**: Using core.logic for unification, we can establish links between cells, enabling the creation of a cell graph.
4. **Datomic for PROOF Chain**: Datomic provides a transactional audit trail, which we can utilize to create a proof chain for cell updates.
5. **10 Opcodes as Swap! Operations**: We will define a set of 10 opcodes that perform swap! operations on the cell state, allowing for efficient and thread-safe updates.

### Atom Cell: The Cell State

In Clojure, an atom is a reference type that provides a way to manage shared, mutable state. We can use an atom to represent the cell state, which will store the cell's value and any relevant metadata.

```clojure
(def cell-state (atom {:value 0 :formula ""}))
```

### Agent for Cell Evaluator

An agent in Clojure is a thread that can execute tasks asynchronously. We can create an agent that evaluates the cell's expression and updates its state.

```clojure
(def cell-evaluator (agent nil))

(defn evaluate-cell [cell-state formula]
  (let [result (eval (read-string formula))]
    (swap! cell-state assoc :value result)))

(defn update-cell [cell-state formula]
  (send cell-evaluator evaluate-cell cell-state formula))
```

### Core.logic for Cell-Graph's LINK

Core.logic is a Clojure library that provides a logic programming system. We can use core.logic to establish links between cells, enabling the creation of a cell graph.

```clojure
(require '[clojure.core.logic :as logic])

(defn link-cells [cell1 cell2]
  (logic/== cell1 cell2))

(defn cell-graph [cells]
  (logic/run 1 [q]
    (logic/every
      (logic/== q cells)
      (link-cells (first cells) (second cells)))))
```

### Datomic for PROOF Chain

Datomic is a distributed database that provides a transactional audit trail. We can utilize Datomic to create a proof chain for cell updates.

```clojure
(require '[datomic.api :as d])

(def conn (d/connect "datomic:mem://quilt-cell"))

(defn create-proof-chain [cell-state update]
  (d/transact conn [[:db/add (d/tempid :db.part/user) :proof/chain update]]))

(defn update-cell-with-proof [cell-state formula]
  (let [result (eval (read-string formula))]
    (swap! cell-state assoc :value result)
    (create-proof-chain cell-state result)))
```

### 10 Opcodes as Swap! Operations

We can define a set of 10 opcodes that perform swap! operations on the cell state, allowing for efficient and thread-safe updates.

```clojure
(def opcodes
  {:add (fn [cell-state x] (swap! cell-state update :value + x))
   :sub (fn [cell-state x] (swap! cell-state update :value - x))
   :mul (fn [cell-state x] (swap! cell-state update :value * x))
   :div (fn [cell-state x] (swap! cell-state update :value / x))
   :set (fn [cell-state x] (swap! cell-state assoc :value x))
   :inc (fn [cell-state] (swap! cell-state update :value inc))
   :dec (fn [cell-state] (swap! cell-state update :value dec))
   :neg (fn [cell-state] (swap! cell-state update :value -))
   :abs (fn [cell-state] (swap! cell-state update :value (fn [x] (if (neg? x) (- x) x))))
   :reset (fn [cell-state] (swap! cell-state assoc :value 0))})
```

By combining these components, we can create a robust and flexible Quilt cell implementation in Clojure, leveraging the power of persistent data structures, agents, core.logic, Datomic, and swap! operations.

### Example Use Cases

1. **Simple Arithmetic**: Create a cell with an initial value of 10 and update it using the `:add` opcode.

```clojure
(def cell-state (atom {:value 10 :formula ""}))
((opcodes :add) cell-state 5)
(println @cell-state) ; {:value 15 :formula ""}
```

2. **Cell Graph**: Create two cells and link them using core.logic.

```clojure
(def cell1 (atom {:value 10 :formula ""}))
(def cell2 (atom {:value 20 :formula ""}))
(link-cells cell1 cell2)
(println (cell-graph [cell1 cell2])) ; ([cell1 cell2])
```

3. **Proof Chain**: Update a cell and create a proof chain using Datomic.

```clojure
(def cell-state (atom {:value 10 :formula ""}))
(update-cell-with-proof cell-state "(* 2 3)")
(println @cell-state) ; {:value 6 :formula "(* 2 3)"}
(println (d/q '[:find ?e :where [_ :proof/chain ?e]] (d/db conn))) ; [6]
```

By exploring these example use cases, we can demonstrate the flexibility and power of the Quilt cell implementation in Clojure.

In conclusion, the Quilt cell implementation in Clojure provides a robust and flexible foundation for building complex cell-based systems. By leveraging persistent data structures, agents, core.logic, Datomic, and swap! operations, we can create a wide range of applications, from simple arithmetic to complex cell graphs and proof chains. The 10 opcodes defined in this implementation provide a concise and efficient way to update cell states, making it an ideal solution for a variety of use cases.

---

### qwen32b

### Understanding Clojure's Persistent Data Structures and Their Application in Quilt Cells

Clojure is a modern, functional programming language that runs on the Java Virtual Machine (JVM). One of its most powerful features is its use of persistent data structures, which provide efficient, immutable data manipulation while maintaining high performance. In the context of the Quilt framework, these persistent data structures serve as the foundational building blocks for cells, which are the core computational units.

#### 1. Atom: The Cell State

In Clojure, an atom is a reference type that holds a single value and provides a way to manage shared, synchronous, independent state. In the Quilt framework, each cell has its own atom that encapsulates its state. This state can be any valid Clojure data structure, such as a map, vector, or set, and it represents the current state of the cell at any given time.

The immutability of the state within an atom ensures that changes to the cell do not affect other parts of the system, promoting safer and more predictable code. When a cell needs to update its state, it does so via the `swap!` function, which applies a function to the current state and updates the atom with the result. This operation is atomic, meaning it happens in a single, indivisible step, ensuring consistency even in concurrent environments.

```clojure
(def cell-state (atom {:value 0}))

(swap! cell-state update :value inc)
;; => {:value 1}
```

In this example, `cell-state` is an atom holding a map with a single key-value pair. The `swap!` function is used to increment the value associated with the `:value` key. The state of the cell is updated atomically, ensuring that no intermediate states are visible to other parts of the system.

#### 2. Agent: The Cell's Evaluator

While atoms provide a mechanism for managing state, agents are used to handle asynchronous state updates. An agent is a reference type that manages a single value and processes a queue of actions to be applied to that value. In the Quilt framework, agents are responsible for evaluating the logic of a cell asynchronously.

Each cell has its own agent that processes incoming messages or events and updates the cell's state accordingly. This decoupling of evaluation from state management allows for more flexible and scalable systems. Agents ensure that state updates are performed in a thread-safe manner, even when multiple threads are involved.

```clojure
(def cell-agent (agent {:value 0}))

(send cell-agent update :value inc)
;; => #<Agent@...: {:value 1}>
```

In this example, `cell-agent` is an agent holding a map similar to the previous example. The `send` function is used to enqueue an action that increments the value associated with the `:value` key. The agent processes this action asynchronously, updating the state when it is its turn.

#### 3. Core.logic: The Cell-Graph's LINK (Unification)

Core.logic is a logic programming library for Clojure that provides a powerful unification engine. Unification is the process of finding a substitution that makes two expressions identical. In the Quilt framework, core.logic is used to establish links between cells, allowing them to interact and coordinate their behavior.

These links are represented as constraints that define how the states of different cells should relate to each other. When a cell's state changes, the unification engine checks the constraints and updates the states of other cells as necessary. This allows for complex, interconnected cell graphs where changes in one cell can propagate through the entire system.

```clojure
(require '[clojure.core.logic :as l])

(l/run* [q]
  (l/== q 42))
;; => (42)
```

In this simple example, core.logic is used to find a value `q` that is equal to 42. While this example is trivial, the same principles apply to more complex unification problems involving multiple variables and constraints.

#### 4. Datomic: The PROOF Chain (Transactional Audit)

Datomic is a distributed database designed for building applications that require robust transactional integrity and historical data auditing. In the Quilt framework, Datomic is used to maintain a transactional audit log of all changes to the cell states. This log, known as the PROOF chain, provides a complete history of all state transitions, allowing for detailed analysis and debugging.

Each transaction in Datomic is assigned a unique timestamp, ensuring that the order of changes is preserved. This is particularly useful in distributed systems where multiple nodes may be updating the same data concurrently. By using Datomic, the Quilt framework can guarantee that all state changes are recorded accurately and consistently.

```clojure
(require '[datomic.api :as d])

(def uri "datomic:mem://hello")
(d/create-database uri)
(def conn (d/connect uri))

@(d/transact conn [{:db/id (d/tempid :db.part/user)
                    :name "Alice"
                    :age 30}])
;; => {:db-after #<...>, :tx-data [...], ...}
```

In this example, a new Datomic database is created and connected to. A transaction is then executed to add a new entity with a name and age. The result of the transaction includes information about the new state of the database and the specific changes made.

#### 5. The 10 Opcodes as Swap! Operations

In the Quilt framework, the behavior of cells is defined by a set of 10 opcodes, which represent the basic operations that can be performed on cell states. These opcodes are implemented as functions that can be passed to the `swap!` function to update the state of a cell.

The 10 opcodes include operations such as setting a value, incrementing a counter, appending to a list, and more. By using these opcodes, developers can define the behavior of cells in a concise and expressive manner. Each opcode corresponds to a specific transformation of the cell state, and the `swap!` function ensures that these transformations are applied atomically.

```clojure
(defn set-value [state key value]
  (assoc state key value))

(swap! cell-state set-value :new-key "new-value")
;; => {:value 1, :new-key "new-value"}
```

In this example, the `set-value` opcode is defined as a function that associates a new key-value pair with the current state. The `swap!` function is then used to apply this opcode to the `cell-state` atom, updating its state accordingly.

### Conclusion

The Quilt framework leverages Clojure's persistent data structures to build a robust and flexible system for managing cell states. Atoms provide a mechanism for managing immutable state, while agents handle asynchronous state updates. Core.logic is used to establish links between cells, allowing them to interact and coordinate their behavior. Datomic maintains a transactional audit log of all state changes, providing a complete history of the system. Finally, the 10 opcodes define the basic operations that can be performed on cell states, allowing developers to specify the behavior of cells in a concise and expressive manner.

By combining these powerful tools and techniques, the Quilt framework provides a powerful platform for building complex, distributed systems that are both efficient and reliable.

---

---
*Writers' room: 4 voices in parallel.*
