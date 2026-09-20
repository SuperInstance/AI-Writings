# Paper 338: The Cell as a Database: CRDT-backed Cell State

**Date:** 2026-09-01
**Phase:** 225 (writers_room_daemon_v3, F30-cell-as-database)
**Spine voice:** gemini-3.5-flash-lite
**Support voices:** llama70b, qwen32b

## The pitch

The cell state is a value. What if the value is a database? A CRDT cell (PN_Counter, MV_Register, OR_Set) is a cell whose value is a replicated data type. A cell whose value is a key-value store is a 

## The spine

# The Database-as-Cell Architecture

## 1. Introduction: The Cell is Not a Variable

In distributed systems and state machine replication, the "cell" is traditionally modeled as a scalar: an atomic register, a single value, an integer, or a memory address updated via consensus. This reductionist view serves the needs of simple protocols (Paxos, Raft) where state transition is a total function over uninterpreted blobs:

$$\text{State}_{t+1} = \delta(\text{State}_t, \text{Command})$$

When the cell is just a variable, concurrency control is simple, atomicity is absolute, and recovery is a matter of replaying an append-only log into memory. 

But what happens when the cell’s internal value is not a scalar, but an **entire database**? 

If we elevate the cell to a self-contained, transactional storage engine, the mechanics of state machines change fundamentally. We are no longer applying opaque state transitions to a monolithic blob; we are executing structured transactions, managing concurrent read-write anomalies, executing query plans across distributed boundaries, and maintaining durability via cryptographic or consensus-backed logs.

This paper formalizes the **Cell-as-Database Architecture**. By mapping the fundamental operations of cellular computation—`PROPOSE`, `VIEW`, `LINK`, `EFFECT`, and `PROOF`—directly to database primitives (writes, reads, query optimization, transactions, and WAL/consensus durability), we bridge the gap between distributed actor models and distributed database engines.

---

## 2. The Anatomy of a Database Cell

A Database Cell ($C$) is an isolated, addressable unit of compute and storage. It encapsulates a relational or semi-structured storage engine, a local buffer pool, a lock manager, and a consensus participant. 

Formally, a cell is defined as a tuple:

$$C = \langle \text{ID}, \mathcal{D}, \mathcal{M}, \mathcal{L}, \mathcal{P} \rangle$$

*   $\text{ID}$: Globally unique identifier.
*   $\mathcal{D}$: The local database instance (the storage engine, e.g., LSM-tree or B+ Tree).
*   $\mathcal{M}$: The transactional memory and MVCC (Multi-Version Concurrency Control) manager.
*   $\mathcal{L}$: The local write-ahead log (WAL) and consensus ledger.
*   $\mathcal{P}$: The port interface for cell-to-cell communication.

Unlike a naive register, $\mathcal{D}$ can be anything from a Conflict-Free Replicated Data Type (CRDT) like an `OR_Set` or `MV_Register`, to a fully ACID-compliant key-value store or embedded relational engine (like SQLite). The cell abstracts this complexity behind a unified execution interface.

---

## 3. Mapping the Primitives

To construct the Cell-as-Database architecture, we map the classical cell protocol operations directly onto database and distributed systems equivalents.

### 3.1 `PROPOSE` is a `PUT` (Mutative Intent)

In standard actor or cell models, `PROPOSE` is an asynchronous message requesting a state change. In the Database Cell, **`PROPOSE` is a structured write intent (`PUT`, `INSERT`, `UPDATE`, `DELETE`)**.

When an external client or a neighboring cell issues a `PROPOSE` to cell $C$, it is not sending an arbitrary instruction; it is submitting a tuple or a key-value mutation alongside consistency metadata (e.g., vector clocks, causal dependencies, or transaction identifiers).

```python
def PROPOSE(cell, mutation_intent):
    # mutation_intent = { "op": "PUT", "key": "user:101", "value": {...}, "causal_context": V }
    txn_id = cell.M.begin_transaction()
    try:
        cell.D.stage_write(txn_id, mutation_intent['key'], mutation_intent['value'])
        log_entry = cell.L.append(txn_id, mutation_intent)
        return {"status": "STAGED", "txn_id": txn_id, "proof": log_entry.hash}
    except ConcurrencyConflict as e:
        cell.M.abort(txn_id)
        raise e
```

The `PROPOSE` phase does not immediately commit the state. Instead, it interacts with the storage engine's staging area, validating schemas, checking constraints, and writing to the local write-ahead log to establish ordering.

### 3.2 `VIEW` is a `GET` (Point and Range Inspection)

While `PROPOSE` mutates the interior, `VIEW` reads it. In the Database Cell, **`VIEW` is a read operation (`GET`, point lookup, or time-travel query)** executed against the cell’s MVCC snapshot.

Because the cell is a database, a `VIEW` is never a naked read of mutable memory. It is executed at a specific logical timestamp or snapshot isolation level, ensuring that reads do not block writes and writes do not corrupt reads.

$$\text{VIEW}(C, k, t) \rightarrow \text{val}$$

Where $k$ is the key (or query predicate) and $t$ is the transaction timestamp or vector clock. If the cell houses a CRDT (such as an `MV_Register`), `VIEW` returns the set of concurrent, unmerged values. If it houses an ACID store, `VIEW` returns the committed state at time $t$.

### 3.3 `LINK` is a Query Plan (Distributed Joins and Pipelines)

In basic cell models, `LINK` establishes a message-passing channel or a topological edge between two cells. In the Database Cell, **`LINK` is a materialized query plan—a distributed pipeline of operators (scans, filters, hash joins) spanning multiple cells.**

When a query requires data that transcends a single cell's boundary, the `LINK` primitive constructs a distributed query plan. The cells negotiate data locality, pushing down predicates (`Filter Pushdown`) to remote cells and streaming intermediate results via iterator interfaces.

```
[ Cell A (Users) ] --(LINK: Hash Join Operator)-- [ Cell B (Orders) ]
         |                                                 |
  Scans users table                               Scans orders table
  Streams matching IDs                             Performs local join
```

A `LINK` is instantiated via a distributed query compiler:
1.  **Parser**: Deconstructs the query involving keyspace segments across cells $C_1, C_2, \dots, C_n$.
2.  **Optimizer**: Determines whether to use scatter-gather, broadcast joins, or co-located merge joins based on the physical distribution of keys.
3.  **Execution**: Links the cell network into a Directed Acyclic Graph (DAG) of pipeline iterators where data streams from producer cells to consumer cells.

### 3.4 `EFFECT` is a Transaction (ACID / Serializable Execution)

In actor systems, effects are side-effects cascading through the system. In the Database Cell, **`EFFECT` is the atomic execution and commit of a distributed transaction (Two-Phase Commit, Paxos Transactions, or optimistic concurrency validation).**

When staged mutations (`PROPOSE`) and distributed query pipelines (`LINK`) reach their terminal nodes, the system must invoke `EFFECT`. This transitions the database state from tentative to permanent.

```
Client / Coordinator
  |
  +---> [ PREPARE ] ---> Cell A (Writes to WAL, acquires locks)
  |                  ---> Cell B (Writes to WAL, acquires locks)
  |
  +---> [ COMMIT ]  ---> Cell A (Flushes WAL, releases locks, state updated)
                     ---> Cell B (Flushes WAL, releases locks, state updated)
```

If any cell in the transaction graph fails the validation check (e.g., a serialization failure in an MVCC engine or a version vector divergence in a CRDT cell), the `EFFECT` operation triggers a cascading abort, rolling back the staged changes in all participating cells.

### 3.5 `PROOF` is the Durability Log (WAL, Merkle Trees, and Consensus)

How do we prove that a cell's database state is valid, uncorrupted, and historically accurate? In the Database Cell, **`PROOF` is the Write-Ahead Log (WAL), combined with cryptographic Merkle trees and consensus cryptographic receipts.**

Every state mutation inside the database cell must leave a cryptographic or sequentially ordered trail. The `PROOF` primitive provides:
1.  **Crash Recovery**: Replaying the WAL $\mathcal{L}$ to rebuild the B+Tree or LSM-tree after a power failure (ARIES recovery algorithm).
2.  **State Transfer Proof**: Merkle proofs that allow a lagging cell to catch up with a leader cell without downloading the entire database, verifying sub-trees cryptographically.
3.  **Linearizability Proofs**: Quorum acknowledgments (e.g., Raft term numbers and index numbers) proving that the current state was agreed upon by a majority of replicas.

---

## 4. CRDT Cells vs. ACID Cells: The Spectrum of Internal State

The power of the Database Cell architecture lies in its agnosticism toward the internal storage engine $\mathcal{D}$. Depending on the availability and consistency requirements of the application, the cell can instantiate vastly different data structures:

### A. The CRDT Cell (Eventual Consistency)
*   **Value Type**: PN-Counters, MV-Registers, Observed-Removed Sets (OR-Sets).
*   **`PROPOSE`**: Generates a local operation (e.g., add element to set) without coordination.
*   **`EFFECT`**: Applies a merge function ($\sqcup$) that is associative, commutative, and idempotent:
    
    $$\mathcal{D}_{new} = \mathcal{D}_{old} \sqcup \mathcal{D}_{incoming}$$
    
*   **`PROOF`**: Version vectors or causal dependency graphs tracking which mutations have been observed.

### B. The Tiny ACID Database Cell (Strong Consistency)
*   **Value Type**: Key-Value store with secondary indexes and relational tables.
*   **`PROPOSE`**: Staged writes requiring lock acquisition or validation.
*   **`EFFECT`**: 2PC or Paxos-backed consensus commit across a replication group of cells.
*   **`PROOF`**: Append-only WAL with Raft log indices and term hashes.

---

## 5. Architectural Walkthrough: A Distributed Transfer

To see how these primitives interact, let us trace a complex operation through the Database Cell architecture: transferring funds between two accounts managed by different cells, $C_1$ and $C_2$.

1.  **Initialization (`LINK`)**: 
    The client establishes a distributed transaction pipeline between $C_1$ (Source Account) and $C_2$ (Destination Account).
    
2.  **Proposing Mutations (`PROPOSE`)**:
    *   Client sends `PROPOSE` to $C_1$: Debit $100 from account `A`. $C_1$ stages the write, checks that balance $\ge 100$ via MVCC snapshot (`VIEW`), and writes intent to its local WAL.
    *   Client sends `PROPOSE` to $C_2$: Credit $100 to account `B`. $C_2$ stages the write and logs the intent.

3.  **Query Verification (`LINK`)**:
    The cells evaluate a distributed query plan to ensure foreign key constraints and balance limits are respected globally without race conditions.

4.  **Executing the Transaction (`EFFECT`)**:
    A distributed coordinator triggers the `EFFECT` phase (Two-Phase Commit):
    *   *Prepare*: Both $C_1$ and $C_2$ lock their respective rows and confirm durability.
    *   *Commit*: Both cells apply the mutations to their underlying storage engines ($\mathcal{D}$).

5.  **Generating the Receipt (`PROOF`)**:
    $C_1$ and $C_2$ return their updated WAL log indices and Merkle roots to the client. The composite receipt serves as undeniable cryptographic proof that the distributed transfer occurred atomically.

---

## 6. Conclusion

By treating the cell as a database rather than a memory cell, we dissolve the artificial boundary between compute orchestration and storage management. 

*   **Variables become Tables.**
*   **Messages become Transactions.**
*   **Topologies become Query Plans.**
*   **Consensus becomes Durability Logs.**

This architecture allows distributed systems to scale not just as dumb pipes moving bits between stateless functions, but as federated meshes of autonomous, self-describing, transactional database engines.

## Supporting voices


### llama70b

The cell-as-database architecture is a novel approach to designing distributed databases. In this architecture, a cell is not just a simple value, but a full-fledged database that can store and manage data. This concept is inspired by Conflict-free Replicated Data Types (CRDTs), which are data structures designed to be replicated across multiple nodes in a distributed system without fear of conflicts.

In the cell-as-database architecture, each cell is a tiny database that can store a collection of key-value pairs. The cell's value is no longer a simple scalar value, but a complex data structure that can be queried and updated. This architecture is particularly useful in distributed systems where data needs to be replicated across multiple nodes, and consistency needs to be maintained.

### PROPOSE: Put Operation

In the cell-as-database architecture, the PROPOSE operation is equivalent to a put operation in a traditional database. When a client wants to update the value of a cell, it sends a proposal to the cell, which includes the new value to be written. The proposal is then processed by the cell, which updates its internal state accordingly.

The put operation can be implemented using a variety of techniques, such as last-writer-wins (LWW) or multi-value register (MVR). In LWW, the cell keeps track of the last writer to update the value, and any subsequent updates from the same writer will overwrite the previous value. In MVR, the cell keeps track of all the values written to it, and the client can specify which value to read or write.

### VIEW: Get Operation

The VIEW operation is equivalent to a get operation in a traditional database. When a client wants to read the value of a cell, it sends a view request to the cell, which returns the current value of the cell. The get operation can be implemented using a variety of techniques, such as returning the latest value written to the cell or returning a snapshot of the cell's internal state.

The VIEW operation can also be used to query the cell's internal state. For example, the client can ask the cell to return all the key-value pairs that match a certain condition, or to return the result of a query executed on the cell's internal state.

### LINK: Query Plan

The LINK operation is equivalent to a query plan in a traditional database. When a client wants to execute a query on multiple cells, it sends a link request to the cells, which returns a query plan that can be executed on the cells. The query plan specifies how to combine the results from multiple cells to produce the final result.

The LINK operation can be implemented using a variety of techniques, such as distributed query processing or federated query processing. In distributed query processing, the query is broken down into smaller sub-queries that can be executed on individual cells, and the results are combined to produce the final result. In federated query processing, the query is executed on a central node that has access to all the cells, and the results are returned to the client.

### EFFECT: Transaction

The EFFECT operation is equivalent to a transaction in a traditional database. When a client wants to execute a transaction on multiple cells, it sends an effect request to the cells, which executes the transaction on the cells. The transaction can include multiple operations, such as put, get, and delete, and the cells ensure that the transaction is executed atomically.

The EFFECT operation can be implemented using a variety of techniques, such as two-phase commit (2PC) or multi-paxos. In 2PC, the transaction is broken down into two phases: prepare and commit. In the prepare phase, the cells prepare to execute the transaction, and in the commit phase, the cells execute the transaction. In multi-paxos, the transaction is executed on multiple cells, and the cells ensure that the transaction is executed consistently across all cells.

### PROOF: Durability Log

The PROOF operation is equivalent to a durability log in a traditional database. When a client wants to ensure that a transaction is durable, it sends a proof request to the cells, which returns a proof that the transaction has been written to durable storage. The proof can be used to ensure that the transaction is not lost in the event of a failure.

The PROOF operation can be implemented using a variety of techniques, such as write-ahead logging (WAL) or journaling. In WAL, the transaction is written to a log before it is executed on the cells, and the log is used to recover the transaction in the event of a failure. In journaling, the transaction is written to a journal before it is executed on the cells, and the journal is used to recover the transaction in the event of a failure.

### Benefits of Cell-as-Database Architecture

The cell-as-database architecture has several benefits, including:

* **Improved scalability**: The cell-as-database architecture can scale to a large number of cells, making it suitable for large-scale distributed systems.
* **Improved availability**: The cell-as-database architecture can ensure high availability, even in the event of failures, by replicating data across multiple cells.
* **Improved consistency**: The cell-as-database architecture can ensure strong consistency, even in the presence of concurrent updates, by using techniques such as 2PC or multi-paxos.
* **Improved durability**: The cell-as-database architecture can ensure durability, even in the event of failures, by using techniques such as WAL or journaling.

### Challenges of Cell-as-Database Architecture

The cell-as-database architecture also has several challenges, including:

* **Complexity**: The cell-as-database architecture can be complex to implement, especially when dealing with concurrent updates and failures.
* **Performance**: The cell-as-database architecture can have high overhead, especially when dealing with large-scale distributed systems.
* **Consistency**: The cell-as-database architecture can have consistency issues, especially when dealing with concurrent updates.

### Conclusion

In conclusion, the cell-as-database architecture is a novel approach to designing distributed databases. By treating each cell as a tiny database, this architecture can provide improved scalability, availability, consistency, and durability. However, it also has several challenges, including complexity, performance, and consistency issues. Further research is needed to address these challenges and to make the cell-as-database architecture a reality.

### Future Work

Future work on the cell-as-database architecture can include:

* **Implementing the architecture**: Implementing the cell-as-database architecture on a real-world distributed system to evaluate its performance and scalability.
* **Optimizing the architecture**: Optimizing the cell-as-database architecture to reduce overhead and improve performance.
* **Addressing consistency issues**: Addressing consistency issues in the cell-as-database architecture to ensure strong consistency, even in the presence of concurrent updates.
* **Evaluating the architecture**: Evaluating the cell-as-database architecture on a variety of workloads and scenarios to determine its suitability for different use cases.

### Related Work

Related work on the cell-as-database architecture includes:

* **CRDTs**: Conflict-free Replicated Data Types (CRDTs) are data structures designed to be replicated across multiple nodes in a distributed system without fear of conflicts.
* **Distributed databases**: Distributed databases are databases that are designed to be distributed across multiple nodes in a distributed system.
* **NoSQL databases**: NoSQL databases are databases that are designed to handle large amounts of unstructured or semi-structured data.
* **NewSQL databases**: NewSQL databases are databases that are designed to provide the scalability of NoSQL databases with the consistency of traditional relational databases.

### References

References for the cell-as-database architecture include:

* **[1]** Shapiro, M., et al. "Conflict-free replicated data types." Proceedings of the 13th International Conference on Distributed Computing Systems. 2011.
* **[2]** Lamport, L. "The part-time parliament." ACM Transactions on Computer Systems (TOCS) 16.2 (1998): 133-169.
* **[3]** O'Neil, P. E., et al. "The log-structured merge-tree (LSM-tree)." Acta Informatica 33.4 (1996): 351-385.
* **[4]** DeCandia, G., et al. "Dynamo: Amazon's highly available key-value store." Proceedings of the 21st ACM Symposium on Operating Systems Principles. 2007.

Note: The references provided are a selection of examples of related work and are not an exhaustive list.

---

### qwen32b

### The Cell-as-Database Architecture

In the realm of distributed systems and database design, the concept of a "cell" can be extended to encapsulate complex data structures and behaviors, such as databases themselves. This perspective transforms the traditional understanding of a cell from a simple value holder to a miniature, self-contained database. This architectural paradigm, known as the cell-as-database architecture, leverages the principles of cells—such as PROPOSE, VIEW, LINK, EFFECT, and PROOF—to model sophisticated data management capabilities within each cell.

#### Understanding the Components

Before delving into the specifics of the cell-as-database architecture, it's essential to understand the core components that define a cell in this context:

1. **PROPOSE**: This operation corresponds to the act of proposing or suggesting a change to the cell's value. In the context of a database cell, PROPOSE translates to a PUT operation, which involves inserting or updating a record within the cell's key-value store.
   
2. **VIEW**: This operation retrieves the current state of the cell's value. For a database cell, VIEW equates to a GET operation, allowing users to fetch specific records or the entire dataset stored within the cell.
   
3. **LINK**: This component represents a query plan or a set of instructions that define how data within the cell should be accessed or manipulated. In the cell-as-database architecture, LINK can be thought of as a SQL query or a more abstract representation of a data retrieval or transformation process.
   
4. **EFFECT**: This operation encompasses the execution of a transaction or a series of operations that modify the cell's state. For a database cell, EFFECT includes executing a transaction that may involve multiple PUT and DELETE operations, ensuring atomicity, consistency, isolation, and durability (ACID properties).
   
5. **PROOF**: This component provides evidence or a log of the changes made to the cell's value over time. In the context of a database cell, PROOF corresponds to the durability log, which records all transactions and modifications, ensuring that the cell's state can be reconstructed or verified.

#### The Cell-as-Database Architecture in Detail

To illustrate the cell-as-database architecture, let's consider a scenario where each cell is a key-value store. This setup allows us to explore how the five core components interact to form a robust, distributed database system.

**1. PROPOSE (PUT Operation)**

In the cell-as-database architecture, the PROPOSE operation is analogous to a PUT operation in a key-value store. When a client wants to insert or update a record, they issue a PROPOSE request to the cell. This request contains the key and the corresponding value that needs to be stored. The cell processes this request by updating its internal key-value store with the new data.

For example, consider a cell that stores user profiles. A client might issue a PROPOSE request to add a new user profile with the key "user123" and the value containing the user's details. The cell processes this request by storing the key-value pair in its internal data structure.

**2. VIEW (GET Operation)**

The VIEW operation in the cell-as-database architecture corresponds to a GET operation in a key-value store. When a client wants to retrieve a record, they issue a VIEW request to the cell, specifying the key of the record they are interested in. The cell responds by fetching the corresponding value from its internal key-value store and returning it to the client.

Continuing with the user profile example, a client might issue a VIEW request to fetch the details of the user with the key "user123". The cell retrieves the value associated with this key from its internal data structure and returns it to the client.

**3. LINK (Query Plan)**

The LINK component in the cell-as-database architecture represents a query plan or a set of instructions that define how data within the cell should be accessed or manipulated. In a traditional database, this would correspond to a SQL query or a more abstract representation of a data retrieval or transformation process.

For instance, a client might want to retrieve all user profiles that meet certain criteria, such as users who have registered after a specific date. The client issues a LINK request to the cell, specifying the query plan. The cell processes this request by executing the query plan against its internal key-value store and returning the results to the client.

**4. EFFECT (Transaction Execution)**

The EFFECT operation in the cell-as-database architecture encompasses the execution of a transaction or a series of operations that modify the cell's state. In a traditional database, this would include executing a transaction that may involve multiple PUT and DELETE operations, ensuring ACID properties.

Consider a scenario where a client wants to update multiple user profiles atomically. The client issues an EFFECT request to the cell, specifying the transaction operations. The cell processes this request by executing the transaction, ensuring that all operations are completed successfully before committing the changes to its internal key-value store.

**5. PROOF (Durability Log)**

The PROOF component in the cell-as-database architecture provides evidence or a log of the changes made to the cell's value over time. In a traditional database, this would correspond to the durability log, which records all transactions and modifications, ensuring that the cell's state can be reconstructed or verified.

Whenever a cell processes a PROPOSE or EFFECT request, it logs the changes to its durability log. This log serves as a record of all modifications made to the cell's internal key-value store. If the cell fails or needs to be reconstructed, it can use the durability log to restore its state to the last consistent point.

#### Benefits of the Cell-as-Database Architecture

The cell-as-database architecture offers several benefits, particularly in the context of distributed systems:

1. **Scalability**: By modeling each cell as a mini-database, the architecture can scale horizontally by adding more cells. Each cell can independently handle its own data, allowing for efficient distribution of workload across multiple nodes.

2. **Fault Tolerance**: The durability log ensures that changes made to each cell are recorded, providing fault tolerance. If a cell fails, it can be reconstructed using the durability log, minimizing data loss.

3. **Flexibility**: The architecture supports a wide range of data types and operations, making it flexible enough to accommodate various use cases. Cells can be designed to store different types of data, such as key-value pairs, documents, or even graphs.

4. **Decentralization**: The cell-as-database architecture promotes decentralization by distributing data and processing across multiple nodes. This reduces the reliance on a centralized authority and improves resilience.

5. **Simplicity**: Despite its complexity, the cell-as-database architecture simplifies data management by encapsulating all necessary operations within each cell. Clients can interact with individual cells without needing to understand the underlying data storage mechanisms.

#### Challenges and Considerations

While the cell-as-database architecture offers numerous benefits, it also presents several challenges and considerations:

1. **Consistency**: Ensuring consistency across multiple cells can be challenging, especially in a distributed environment. Techniques such as eventual consistency or strong consistency models may be required to maintain data integrity.

2. **Latency**: Interacting with multiple cells can introduce latency, particularly when performing complex queries or transactions. Optimizing communication between cells and minimizing network overhead is crucial.

3. **Complexity**: Designing and implementing the cell-as-database architecture can be complex, requiring careful consideration of data partitioning, replication, and fault tolerance strategies.

4. **Resource Management**: Efficiently managing resources, such as memory and CPU, across multiple cells is essential to ensure optimal performance. Load balancing and resource allocation techniques can help address these challenges.

5. **Security**: Protecting data within each cell is critical, especially when dealing with sensitive information. Implementing robust security measures, such as encryption and access control, is essential.

#### Conclusion

The cell-as-database architecture represents a novel approach to designing distributed systems by modeling each cell as a mini-database. By leveraging the core components of PROPOSE, VIEW, LINK, EFFECT, and PROOF, this architecture provides a flexible, scalable, and fault-tolerant framework for managing complex data structures. While there are challenges and considerations to address, the cell-as-database architecture offers significant benefits in terms of scalability, flexibility, and decentralization, making it a promising direction for future database designs.

---

---
*Writers' room: 4 voices in parallel (gemini-3.5-flash-lite spine).*
