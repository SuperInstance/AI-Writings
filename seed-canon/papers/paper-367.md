# Paper 367: The Substrate Federation: How 6 Substrates Stay in Sync

**Date:** 2026-09-01
**Phase:** 226 (writers_room_daemon_v3, F59-the-substrate-federation)
**Spine voice:** gemini-3.5-flash-lite
**Support voices:** llama70b, qwen32b

## The pitch

6 substrates run the same cell model. They must stay in sync. The federation protocol: each substrate has a versioning system, the canon publishes a substrate-impl manifest per version, each substrate

## The spine

# Federation Protocol Specification: Multi-Substrate Canonical Synchronization

## 1. Architectural Overview and Guiding Principles

The Cell Model Federation Protocol guarantees absolute deterministic consensus across heterogeneous execution substrates running the same core cellular simulation. A "substrate" refers to a distinct runtime environment, execution engine, or translation target (e.g., Rust/WASM, C++20 bare-metal, TypeScript V8, Go, Julia, and Python/Cython). Despite differences in memory management, floating-point compiler optimizations, and runtime idioms, all substrates must produce bit-for-bit identical state transitions given identical inputs.

To achieve this without centralizing execution, the federation relies on a decoupled, decentralized synchronization model. This model centers on four pillars:

1. **Substrate-Specific Versioning**: Each substrate maintains its own semantic versioning lineage to track internal bug fixes, compiler updates, and performance patches, decoupled from the core mathematical model's version.
2. **The Canon Substrate-Impl Manifest**: A cryptographically signed document published by the designated Canonical Substrate (`canon-0`), defining the exact byte-level expectations, instruction sets, and execution limits for a given model version.
3. **Cross-Checking Test Runners**: Local test execution harnesses running inside each substrate environment that validate local execution paths against the parameters and oracle vectors provided in the manifest.
4. **The FNV-1a State Hash Identity**: A rolling, deterministic checksum calculated via the Fowler–Noll–Vo hash function (specifically FNV-1a-64/128) over serialized cell states. This hash serves as the immutable cryptographic identity of the substrate at any given tick.

```
+-----------------------------------------------------------------+
|                        CANON SUBSTRATE                          |
|  - Executes Reference Model                                     |
|  - Generates Substrate-Impl Manifest (Per Version)              |
+-----------------------------------------------------------------+
                                 |
                                 | Publishes Signed Manifest
                                 v
+-----------------------------------------------------------------+
|                    FEDERATED SUBSTRATES (1-6)                   |
|                                                                 |
|  +-----------------------+     +-----------------------------+  |
|  |   Substrate Engine    |---->|     Local Test Runner       |  |
|  |  (Rust / C++ / Go...) |     |  - Cross-checks w/ Manifest |  |
|  +-----------------------+     +-----------------------------+  |
|              |                                  |               |
|              v                                  v               |
|  +-----------------------------------------------------------+  |
|  |           FNV-1a State Hash Generation & Identity         |  |
|  +-----------------------------------------------------------+  |
+-----------------------------------------------------------------+
```

---

## 2. Substrate Versioning and Identity Schema

Every substrate participating in the federation operates under a dual-versioning scheme. This decouples the *model logic version* from the *substrate implementation version*.

### 2.1 Version Format
`SUBSTRATE_ID:MODEL_VER-SUB_VER+BUILD_METADATA`

*   **`SUBSTRATE_ID`**: A 4-character lowercase alphanumeric string identifying the engine (`rs01` for Rust, cpp2 for C++, py09 for Python, etc.).
*   **`MODEL_VER`**: Semantic version of the core cell biology mathematical specification (`MAJOR.MINOR.PATCH`). Changes here indicate shifts in biological rules (e.g., altered mitosis thresholds).
*   **`SUB_VER`**: Semantic version of the specific substrate implementation (`MAJOR.MINOR.PATCH`). Changes here indicate performance refactors, memory layout optimizations, or bug fixes within that specific runtime.
*   **`BUILD_METADATA`**: Compiler flags, target architecture, and optimization levels (e.g., `x86_64-avx2-O3`).

### 2.2 The FNV-1a State Identity
State identity is not defined by memory addresses, object references, or arbitrary identifiers. At the conclusion of every discrete simulation tick $T$, each substrate serializes its entire active cell matrix into a canonical byte buffer and computes the **FNV-1a hash**. 

The FNV-1a algorithm is chosen for its simplicity, speed, and avalanche properties across small-to-medium structural layouts, making it ideal for streaming state validation:

$$\text{hash} = (\text{hash} \oplus \text{byte}_i) \times \text{FNV\_PRIME}$$

For 64-bit operations:
*   $\text{FNV\_OFFSET\_BASIS} = \text{0xcbf29ce484222325}$
*   $\text{FNV\_PRIME} = \text{0x100000001b3}$

The resulting hash string (hex-encoded) is the substrate's runtime identity for that tick. If two substrates compute different FNV-1a hashes at Tick $T$, a state divergence has occurred, triggering an automatic halt and diagnostic dump.

---

## 3. The Canon Substrate-Impl Manifest

The Canonical Substrate (`canon-0`), typically the reference implementation written in pure, dependency-free C or Rust utilizing fixed-point arithmetic, acts as the absolute arbiter of truth. Upon releasing a new `MODEL_VER`, `canon-0` generates and signs the **Substrate-Impl Manifest**.

### 3.1 Manifest Structure (`manifest.json`)
```json
{
  "$schema": "https://cellmodel.org/schemas/manifest-v1.json",
  "model_version": "2.4.1",
  "manifest_timestamp": "202X-11-04T14:22:00Z",
  "canon_substrate_identity": "rs01:2.4.1-1.0.0+native",
  "execution_parameters": {
    "max_ticks": 10000,
    "grid_dimensions": [512, 512],
    "fixed_point_precision_bits": 32,
    "floating_point_standard": "IEEE-754-2008"
  },
  "checkpoints": [
    {
      "tick": 0,
      "fnv1a_state_hash": "0x811c9dc5,0x62d2e1b9"
    },
    {
      "tick": 100,
      "fnv1a_state_hash": "0x3f2a118e,0x991204be"
    },
    {
      "tick": 1000,
      "fnv1a_state_hash": "0x77b018fc,0x110294ab"
    },
    {
      "tick": 10000,
      "fnv1a_state_hash": "0xdeadbeef,0xc0ffee11"
    }
  ],
  "oracle_vectors": [
    {
      "cell_id": 4192,
      "target_tick": 500,
      "expected_metabolites": {
        "ATP": "0x00004FA2",
        "Glucose": "0x00012000",
        "Volume": "0x00000FA0"
      }
    }
  ],
  "signature": "sig_ed25519_base64_encoded_string_here..."
}
```

### 3.2 Manifest Distribution
The manifest is distributed via the federation's secure content-addressable storage (CAS) network. Substrates pull the manifest matching their targeted `MODEL_VER` before initiating any simulation runs. Any modification to the manifest invalidates the cryptographic signature, causing local test runners to reject the execution payload.

---

## 4. Substrate Test Runner Architecture

Each of the 6 federated substrates embeds a local **Test Runner**. The runner acts as an intermediary between the substrate's execution engine and the federation network.

```
+-------------------------------------------------------+
|                 LOCAL TEST RUNNER                     |
|                                                       |
|  1. Parse & Verify Manifest Signature                 |
|  2. Initialize Substrate with Seed State              |
|  3. Execute Tick Loop -> Compute FNV-1a Hash          |
|  4. Cross-Check Checkpoints & Oracle Vectors          |
|  5. Emit Attestation / Divergence Report              |
+-------------------------------------------------------+
```

### 4.1 Runner Responsibilities
1.  **Manifest Verification**: Validates the Ed25519 signature of the manifest using the federation's root public key.
2.  **Environment Sanitization**: Enforces strict execution parameters. If the manifest dictates IEEE-754 compliance, the runner verifies that the host CPU is not running in non-standard flush-to-zero (FTZ) or denormals-are-zero (DAZ) modes unless explicitly overridden by substrate profile rules.
3.  **Checkpoint Interception**: Pauses execution at ticks specified in the manifest (e.g., Tick 0, 100, 1000, 10000), computes the local FNV-1a state hash, and compares it directly against the canonical hash.
4.  **Oracle Vector Probe**: Queries specific internal cell states designated in the manifest to ensure that individual metabolite gradients match expected outputs down to the fixed-point bit representation.

### 4.2 Divergence Handling Protocols
If a local runner detects a mismatch between its computed FNV-1a hash and the manifest's canonical hash at any checkpoint:
*   **Immediate Suspension**: The substrate halts execution immediately to prevent state corruption propagation.
*   **Binary Dump Generation**: A memory snapshot of the divergent grid sectors is serialized into a local core dump.
*   **Telemetry Emission**: An error payload containing the substrate identity, mismatch tick, expected hash, and actual hash is broadcasted to the federation coordinator.

---

## 5. Serialization and Determinism Constraints

The primary source of divergence across heterogeneous substrates is non-deterministic memory layout, floating-point rounding variations, and concurrent iteration order. To eliminate these vectors, the federation enforces strict serialization and execution rules.

### 5.1 Canonical Serialization Order
When computing the FNV-1a state hash, cells must not be hashed in arbitrary orders dictated by multi-threaded task stealing or hash-map iteration. The cell grid must be flattened into a 1D byte array using strict row-major order:

$$\text{Index} = (y \times \text{GridWidth}) + x$$

Within each cell structure, fields must be serialized in a fixed, padding-free layout:
1.  Cell ID (64-bit unsigned integer, little-endian)
2.  Cell State Flags (32-bit bitmask)
3.  Metabolite Concentrations (Array of 32-bit fixed-point integers, sorted alphabetically by metabolite identifier)
4.  Spatial Coordinates ($X, Y$ as 32-bit signed integers)

### 5.2 Arithmetic Standardization
*   **Floating-Point Math**: Standardized to IEEE 754-2008. Transcendental functions (`sin`, `cos`, `exp`) must utilize a federated lookup table (LUT) rather than native hardware instructions, as hardware implementations (e.g., x87 vs. ARM Neon vs. WASM software intrinsics) vary in precision.
*   **Fixed-Point Fallback**: Substrates operating in resource-constrained environments must use the canonical 32.32 fixed-point math library defined in the manifest, bypassing native floats entirely.

---

## 6. Federation Protocol Message Flow

The lifecycle of a synchronized simulation run follows a strict protocol sequence involving the Canon, the Federation Registry, and the 6 Substrate Runners.

```
Canon                 Registry                Substrates (1-6)
  |                       |                          |
  |--- Publish Manifest ->|                          |
  |                       |--- Broadcast Manifest -->|
  |                       |                          |--- Run Tick 0 (Init)
  |                       |                          |--- Compute FNV-1a
  |                       |<-- Submit Hash T0 -------|
  |                       |                          |--- Run Ticks 1..N
  |                       |                          |--- Compute FNV-1a
  |                       |<-- Submit Hash Tn -------|
  |                       |                          |
  |                       |[ Verify All Hashes Match ]|
  |                       |--- Issue Attestation --->|
```

1.  **Phase 0: Initialization**: `canon-0` generates the initial state, computes the Tick 0 FNV-1a hash, packages the manifest, and registers it with the federation network.
2.  **Phase 1: Distribution**: Substrates 1 through 6 fetch the manifest, initialize their local engines with the canonical seed state, and verify their environment configuration.
3.  **Phase 2: Execution & Checkpointing**: Substrates execute simulation ticks locally. At designated checkpoint ticks (e.g., $T=100$), execution pauses momentarily while the local test runner computes the FNV-1a state hash.
4.  **Phase 3: Attestation**: Each substrate transmits its computed hash to the federation registry. 
5.  **Phase 4: Consensus & Continuation**: The registry verifies that all 6 substrate hashes match the canonical manifest hash. If consensus ($N=6/6$) is achieved, substrates are signaled to resume execution to the next checkpoint.

---

## 7. Error Modes and Recovery Procedures

### 7.1 Floating-Point Drift Divergence
*   **Symptoms**: Hashes match through Tick 1,000, but diverge at Tick 1,000 due to accumulated rounding errors.
*   **Resolution**: The offending substrate inspects its compilation flags. If optimization flags exceed manifest-permitted thresholds (e.g., `-Ofast` instead of `-O2`), the runner forces a re-compilation profile or flags the substrate build as non-compliant.

### 7.2 Memory Layout Desynchronization
*   **Symptoms**: Immediate hash mismatch at Tick 1.
*   **Resolution**: Indicates a struct-padding or endianness bug within the substrate's serialization pipeline. The test runner initiates a differential byte-inspection tool against the canonical oracle vector to pinpoint the misaligned struct field.

### 7.3 Network Partition of Substrate Runners
*   **Symptoms**: A substrate fails to submit its FNV-1a hash within the heartbeat window.
*   **Resolution**: The federation registry fences the non-responsive substrate, marking its status as `SUSPENDED`. The remaining 5 substrates continue execution. The suspended substrate may rejoin only by rolling back to the last valid checkpoint, resyncing its state buffer, and re-attesting its hash.

---

## 8. Compliance Verification Checklist

For a new substrate implementation to be admitted into the 6-node federation, its maintainers must pass the following automated test harness provided by the canon:

- [ ] **Bit-Exact Initialization**: Matches `canon-0` Tick 0 FNV-1a hash precisely.
- [ ] **Serialization Compliance**: Produces identical byte-streams for the cell matrix flattening algorithm.
- [ ] **LUT Trigonometry Verification**: Passes all boundary tests for transcendental operations without utilizing unmasked native hardware floats.
- [ ] **Checkpoint Synchronization**: Successfully halts, hashes, and matches checkpoints at $T \in \{10, 100, 1000, 10000\}$.
- [ ] **Oracle Vector Validation**: Internal metabolite concentrations deviate by exactly $0$ bits from the canon manifest specifications across all probed cell coordinates.

## Supporting voices


### llama70b

**Federation Protocol Documentation**
=====================================

**Introduction**
---------------

The federation protocol is designed to ensure that six substrates running the same cell model remain in sync. This is achieved through a combination of versioning systems, manifest publications, and cross-checks against a canonical manifest. The protocol relies on the FNV-1a state hash as the substrate's identity.

**Versioning System**
--------------------

Each substrate has its own versioning system, which is used to track changes to the substrate's implementation. The versioning system is based on a simple incrementing integer, where each new version is assigned a unique integer value. This allows for easy identification of changes and ensures that all substrates are running the same version of the cell model.

**Canon and Manifest Publication**
---------------------------------

The canon is responsible for publishing a substrate-impl manifest per version. The manifest contains a list of substrates, their corresponding FNV-1a state hashes, and the version number. The manifest is used as a reference point for all substrates to ensure they are in sync.

The canon publishes a new manifest whenever a change is made to the cell model or a new version is released. The manifest is made available to all substrates, which can then use it to cross-check their own implementation.

**Test Runner and Cross-Checks**
------------------------------

Each substrate has a test runner that is responsible for cross-checking the substrate's implementation against the canonical manifest. The test runner uses the FNV-1a state hash to verify that the substrate's implementation matches the expected state.

The test runner performs the following checks:

1. **Version check**: The test runner checks that the substrate's version matches the version specified in the canonical manifest.
2. **FNV-1a state hash check**: The test runner calculates the FNV-1a state hash of the substrate's implementation and compares it to the expected hash specified in the canonical manifest.
3. **Implementation check**: The test runner checks that the substrate's implementation matches the expected implementation specified in the canonical manifest.

If any of these checks fail, the test runner reports an error and the substrate is considered out of sync.

**FNV-1a State Hash**
---------------------

The FNV-1a state hash is a 128-bit hash that is used to identify the substrate's implementation. The hash is calculated using the FNV-1a algorithm, which is a non-cryptographic hash function designed to be fast and have a low collision rate.

The FNV-1a state hash is used as the substrate's identity, allowing the canon and test runners to verify that the substrate's implementation matches the expected state.

**Federation Protocol Workflow**
-------------------------------

The following workflow illustrates the federation protocol:

1. **Canon publishes new manifest**: The canon publishes a new substrate-impl manifest per version, containing the list of substrates, their corresponding FNV-1a state hashes, and the version number.
2. **Substrates retrieve manifest**: Each substrate retrieves the new manifest from the canon.
3. **Test runner cross-checks**: Each substrate's test runner cross-checks the substrate's implementation against the canonical manifest, performing version, FNV-1a state hash, and implementation checks.
4. **Error reporting**: If any checks fail, the test runner reports an error and the substrate is considered out of sync.
5. **Syncing**: The substrate updates its implementation to match the expected state specified in the canonical manifest.
6. **Repeat**: The process is repeated for each new version or change to the cell model.

**Benefits**
------------

The federation protocol provides several benefits, including:

* **Ensures sync**: The protocol ensures that all substrates are running the same version of the cell model, preventing inconsistencies and errors.
* **Detects errors**: The protocol detects errors and reports them, allowing for quick identification and correction of issues.
* **Improves security**: The use of FNV-1a state hashes provides an additional layer of security, making it more difficult for malicious actors to manipulate the substrates.

**Conclusion**
--------------

The federation protocol is a robust and scalable solution for ensuring that multiple substrates running the same cell model remain in sync. By using a combination of versioning systems, manifest publications, and cross-checks against a canonical manifest, the protocol provides a high degree of confidence that all substrates are running the same version of the cell model. The use of FNV-1a state hashes as the substrate's identity provides an additional layer of security and ensures that the substrates are tamper-evident.

**Appendix**
------------

### FNV-1a Hash Algorithm

The FNV-1a hash algorithm is a non-cryptographic hash function designed to be fast and have a low collision rate. The algorithm is defined as follows:

* **Hash initialization**: The hash is initialized to a large prime number, typically 2166136261.
* **Hash update**: For each byte of the input data, the hash is updated using the following formula: `hash = (hash ^ byte) * 16777219`.
* **Hash finalization**: The final hash value is the result of the update formula after all input data has been processed.

The FNV-1a hash algorithm is widely used in many applications, including data storage and networking protocols.

### Example Use Case

Suppose we have six substrates running the same cell model, each with its own versioning system. The canon publishes a new manifest per version, containing the list of substrates, their corresponding FNV-1a state hashes, and the version number.

| Substrate | Version | FNV-1a State Hash |
| --- | --- | --- |
| A | 1 | 0x12345678 |
| B | 1 | 0x23456789 |
| C | 1 | 0x34567890 |
| D | 1 | 0x45678901 |
| E | 1 | 0x56789012 |
| F | 1 | 0x67890123 |

The test runner for each substrate cross-checks the substrate's implementation against the canonical manifest, performing version, FNV-1a state hash, and implementation checks. If any checks fail, the test runner reports an error and the substrate is considered out of sync.

For example, suppose substrate A has a version mismatch, with a local version of 2 instead of 1. The test runner will report an error, and substrate A will update its implementation to match the expected state specified in the canonical manifest.

By using the federation protocol, we can ensure that all six substrates are running the same version of the cell model, preventing inconsistencies and errors.

---

### qwen32b

### Federation Protocol for Synchronized Cell Model Substrates

#### Overview

In the context of running identical cell models across multiple substrates, synchronization is paramount to ensure consistency and reliability. This document outlines a comprehensive federation protocol designed to maintain synchronization among six substrates using a versioning system, a substrate-implementation manifest, and an FNV-1a state hash as the substrate's identity. This protocol ensures that all substrates remain in sync, facilitating accurate and reliable testing and operation.

#### Components of the Federation Protocol

1. **Versioning System**
2. **Substrate-Implementation Manifest**
3. **Test Runner Cross-Checking**
4. **FNV-1a State Hash**

---

### 1. Versioning System

The versioning system serves as the backbone of the synchronization mechanism. Each substrate maintains its own version number, which is incremented with every change or update to the cell model implementation. The versioning system ensures that all substrates are aware of the current state of the cell model and can synchronize accordingly.

**Version Number Format:**

The version number follows the semantic versioning format (MAJOR.MINOR.PATCH):

- **MAJOR:** Incremented when there are incompatible API changes.
- **MINOR:** Incremented when new functionality is added in a backward-compatible manner.
- **PATCH:** Incremented when backward-compatible bug fixes are made.

**Version Control:**

Each substrate maintains a local version file (`version.txt`) that stores the current version number. The version file is updated whenever a change is made to the cell model implementation.

**Version Publishing:**

The canonical authority (referred to as the "canon") publishes the latest version number to a shared repository accessible by all substrates. This ensures that all substrates are aware of the most recent version of the cell model.

---

### 2. Substrate-Implementation Manifest

The substrate-implementation manifest is a JSON file that provides detailed information about the cell model implementation for a specific version. The manifest includes metadata such as the version number, a description of the changes, and a list of files that make up the cell model implementation.

**Manifest Structure:**

```json
{
  "version": "1.2.3",
  "description": "Added support for new cell types and improved performance.",
  "files": [
    "cell_model.py",
    "utils.py",
    "tests/test_cell_model.py"
  ],
  "hashes": {
    "cell_model.py": "f1e069787ece74531d112559f70b6938b9762af6",
    "utils.py": "c3ab8ff13720e8ad9047dd593d46777098587f8c",
    "tests/test_cell_model.py": "d41d8cd98f00b204e9800998ecf8427e"
  }
}
```

**Manifest Generation:**

The manifest is generated by the canon whenever a new version of the cell model is released. The manifest includes the FNV-1a hash of each file to ensure integrity and consistency.

**Manifest Publishing:**

The manifest is published to the shared repository along with the version number. All substrates download the latest manifest and use it to verify the integrity of their local cell model implementation.

---

### 3. Test Runner Cross-Checking

The test runner is responsible for executing tests on the cell model implementation and ensuring that it behaves as expected. The test runner performs cross-checking against the substrate-implementation manifest to verify that the local implementation matches the expected version and files.

**Cross-Checking Process:**

1. **Download Manifest:** The test runner downloads the latest manifest from the shared repository.
2. **Verify Files:** The test runner compares the local files with the files listed in the manifest.
3. **Verify Hashes:** The test runner calculates the FNV-1a hash of each local file and compares it with the hash in the manifest.
4. **Run Tests:** If all files match and hashes are correct, the test runner proceeds to execute the tests.

**Error Handling:**

If any discrepancies are found during the cross-checking process, the test runner logs an error and halts execution. The substrate should then update its local cell model implementation to match the latest version.

---

### 4. FNV-1a State Hash

The FNV-1a state hash serves as the unique identifier for the substrate's cell model implementation. It is calculated based on the contents of the cell model files and is used to verify the integrity and consistency of the implementation across all substrates.

**FNV-1a Hash Calculation:**

The FNV-1a hash is calculated using the following algorithm:

```python
def fnv1a_hash(data):
    fnv_prime = 0x01000193
    hash_value = 0x811c9dc5
    for byte in data:
        hash_value ^= byte
        hash_value *= fnv_prime
        hash_value &= 0xffffffff
    return hash_value
```

**Hash Usage:**

The FNV-1a hash is included in the substrate-implementation manifest for each file. During the cross-checking process, the test runner calculates the hash of each local file and compares it with the hash in the manifest.

**State Consistency:**

By using the FNV-1a hash, the federation protocol ensures that all substrates have identical cell model implementations. Any discrepancies in the hashes indicate that a substrate's implementation is out of sync, prompting it to update.

---

### Implementation Steps

1. **Initial Setup:**
   - Each substrate initializes its local version file (`version.txt`) with the initial version number.
   - The canon publishes the initial substrate-implementation manifest to the shared repository.

2. **Version Update:**
   - When changes are made to the cell model implementation, the canon increments the version number and generates a new manifest.
   - The new manifest is published to the shared repository.

3. **Substrate Update:**
   - Each substrate periodically checks the shared repository for updates to the version number.
   - If a new version is detected, the substrate downloads the new manifest and performs cross-checking.
   - If the cross-checking process is successful, the substrate updates its local cell model implementation.

4. **Testing:**
   - The test runner executes tests on the updated cell model implementation.
   - If any tests fail, the substrate logs the errors and attempts to resolve them.

5. **Error Resolution:**
   - If discrepancies are found during cross-checking, the substrate updates its local cell model implementation to match the latest version.
   - The test runner re-executes the tests to ensure that the implementation is now consistent.

---

### Conclusion

The federation protocol outlined in this document ensures that all six substrates running the same cell model remain synchronized. By leveraging a versioning system, a substrate-implementation manifest, and an FNV-1a state hash, the protocol guarantees consistency and reliability across all substrates. This approach minimizes the risk of errors and ensures that all substrates are operating with the most up-to-date and accurate cell model implementation.

---

---
*Writers' room: 4 voices in parallel.*
