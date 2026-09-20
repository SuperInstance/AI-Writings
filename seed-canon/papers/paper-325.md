# Paper 325: The Polyformal Substrate: Substrate Binding in Quilt Phase 222

**Date:** 2026-08-31
**Phase:** 223 (writers_room_daemon_v3, F17-physical-world)
**Frontier:** F17-physical-world
**Spine voice:** gemini-3.5-flash-lite (math-rich, 1500 words)
**Support voices:** llama70b, qwen32b, gemini25

## The pitch

The Physical World Cell - substrate binding to the Code-as-World model

## The spine (gemini-3.5-flash-lite)

# The Substrate Binding Problem: Polyformal Cells and the Code-as-World-VL-9B Engine

## 1. Introduction: The Quilt Phase 222 Architecture

In the Quilt computational model, execution is not an intrinsic property of code; it is a relational property of a *cell* coupled with a *substrate*. Quilt Phase 222 introduces **Code-as-World-VL-9B** (arXiv:2608.27549) as a native cell kind capable of executing the classical Quilt control loop:

$$\text{PROPOSE} \to \text{EXECUTE} \to \text{RENDER} \to \text{VERIFY} \to \text{REFINE}$$

This loop operates over a uniform cell architecture where the cell value is strictly defined as a physical $\text{Quantity}$ (a tuple of magnitude and unit, $q = m \cdot [u]$). Crucially, Quilt Phase 222 enforces *polyformalism*: the physical memory layout, alignment, and semantic interpretation of a cell are identical across both C and Rust implementations. A cell is not merely a data structure; it is an active boundary condition that can bind to disparate execution engines without altering its typed surface area.

The central challenge of this architecture is the **Substrate Binding Problem**: Given a cell graph whose nodes evaluate physical quantities through cyclical abduction and verification, how do we dynamically route execution across wildly heterogeneous substrates—ranging from a deterministic, zero-allocation synthetic stub to a sandboxed Python interpreter, to an embodied Vision-Language Model operating in a generative world loop?

---

## 2. The Polyformal Cell and the Physical Quantity

To make the substrate interchangeable, the cell must abstract away the execution environment behind a strict type interface. In both C (`quilt.h`) and Rust (`quilt::cell`), a cell instance is defined by its polyformal layout:

```c
// C Polyformal Cell Representation (Quilt Phase 222)
typedef struct {
    double magnitude;
    uint32_t unit_id;
    uint8_t substrate_kind;
    uint8_t flags;
    void* substrate_state;
} QuiltCell;
```

```rust
// Rust Polyformal Cell Representation (Quilt Phase 222)
#[repr(C)]
pub struct QuiltCell {
    pub magnitude: f64,
    pub unit_id: u32,
    pub substrate_kind: u8,
    pub flags: u8,
    pub substrate_state: *mut core::ffi::c_void,
}
```

The cell value $V_c$ is always a $\text{Quantity}$ $q \in \mathcal{Q}$, where $\mathcal{Q} = \mathbb{R} \times \mathcal{U}$ ($\mathcal{U}$ being the set of registered physical units). The transition function of the cell is governed by the Phase 222 protocol:

$$\begin{aligned}
\text{PROPOSE}: &\quad \mathcal{S} \times \mathcal{Q} \to \Pi \quad (\text{Program space}) \\
\text{EXECUTE}: &\quad \Pi \times \mathcal{Environment} \to \mathcal{Q} \\
\text{RENDER}: &\quad \mathcal{Q} \to \mathcal{I} \quad (\text{Observation / Image space}) \\
\text{VERIFY}: &\quad \mathcal{I} \times \mathcal{Q} \to \{0, 1\} \\
\text{REFINE}: &\quad \Pi \times \text{Error} \to \Pi
\end{aligned}$$

The core realization of Quilt Phase 222 is that the **substrate itself is a cell**. A substrate is not an external runtime context; it is wrapped inside the cell graph as a meta-node that evaluates the execution rules of its children.

---

## 3. The Three Substrate Options

Quilt Phase 222 defines three canonical substrate bindings. Each occupies a distinct coordinate in the latency-fidelity-cost space.

### Substrate 1: The `no_std` Synthetic Stub
* **Target:** Unit testing, high-frequency continuous integration, and resource-constrained microcontrollers.
* **Characteristics:** Zero heap allocation, deterministic execution, range-bounded values $q_{\text{mag}} \in [-50, +50]$, with unit scaling restricted to baseline dimensions ($[0, 0.9]$ dimensionless or normalized SI).
* **Mechanics:** The PROPOSE/EXECUTE/VERIFY loop is replaced by closed-form linear approximations or lookup tables. There is no interpreter and no model inference.

### Substrate 2: Sandboxed Python Execution (`exec()`)
* **Target:** Numerical prototyping, deterministic simulation, and real-time physical unit transformations.
* **Characteristics:** Executes arbitrary Python code within a restricted namespace via a restricted `exec()` sandbox. Full access to a dynamic $\text{Quantity}$ library preserving dimensional analysis.
* **Mechanics:** The cell serializes its input quantities into the sandbox environment, executes a user-provided or dynamically generated Python snippet, and extracts the resulting magnitude and unit via AST inspection.

### Substrate 3: Code-as-World-VL-9B (arXiv:2608.27549)
* **Target:** Open-world robotic control, visual reasoning, code synthesis from dense visual observations, and abductive physical problem-solving.
* **Characteristics:** A 9-billion parameter Vision-Language Model trained on the Code-as-World paradigm. The model takes a rendered image $\mathcal{I}$ of the physical or simulated environment, proposes executable code snippets, runs the execution loop internally, and outputs verified programs.
* **Mechanics:** The cell triggers the VLM inference engine. The RENDER step generates a visual token representation of the current cell state. The model PROPOSEs Python or Rust code, EXECUTES it in a secure container, VERIFIES the outcome against visual constraints, and REFINES the code iteratively before returning the final physical $\text{Quantity}$.

---

## 4. Trade-Off Analysis

Choosing a substrate requires navigating a multi-objective optimization problem over latency ($L$), monetary/computational cost ($C$), expressive capacity ($E$), and safety guarantees ($S$).

| Substrate | Latency ($L$) | Cost ($C$) | Expression ($E$) | Safety ($S$) | Primary Failure Mode |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. `no_std` Stub** | $< 1\,\mu\text{s}$ | $\approx 0$ | Low ($\mathbb{R}$ restricted) | Absolute | Domain misspecification |
| **2. Python Sandbox**| $1-10\,\text{ms}$ | Low | High (Arbitrary script) | Moderate | Sandbox escape / Infinite loops |
| **3. Code-as-World-VL-9B** | $500-2000\,\text{ms}$ | High (GPU inference) | Universal (Multimodal) | Probabilistic | Hallucinated physical constants |

Let $\Omega = \{1, 2, 3\}$ denote the set of substrates. The optimal substrate binding function $\sigma(c)$ for a cell $c$ with state vector $\mathbf{x}_c$ is formulated as:

$$\sigma(c) = \arg\min_{k \in \Omega} \Big( w_1 L(k) + w_2 C(k) - w_3 E(k, \mathbf{x}_c) + w_4 \mathcal{R}(k, \mathbf{x}_c) \Big)$$

where $\mathcal{R}(k, \mathbf{x}_c)$ represents the risk penalty of substrate failure, and $w_i$ are system-level weights adjusted for edge versus cloud deployment.

### When to Bind to Which?
* **Bind to Substrate 1 (`no_std`)** when the cell graph operates within an inner control loop where jitter must remain below $10\,\mu\text{s}$, or during unit tests where inputs are bounded and deterministic behavior is mandatory.
* **Bind to Substrate 2 (Python Sandbox)** when the computation requires complex numerical integration, matrix operations, or unit conversions that exceed the linear limits of the synthetic stub, but where visual grounding is unnecessary.
* **Bind to Substrate 3 (Code-as-World-VL-9B)** when the cell encounters out-of-distribution physical states, when the environment must be visually interpreted to derive the next program, or when the system must autonomously repair broken execution pipelines via the abductive REFINE loop.

---

## 5. The Cell-Graph Structure: Substrate-as-Cell

The defining architectural breakthrough of Quilt Phase 222 is that **the substrate is not an external configuration; it is a first-class cell within the graph topology**. 

In traditional architectures, a runtime engine hosts a graph of data cells. In Quilt Phase 222, the substrate *is* a cell that wraps execution contexts, creating a recursive, self-hosting topology.

```
      +-------------------------------------------------------+
      |               Substrate-Cell (Meta-Node)              |
      |          [Kind: Code-as-World-VL-9B Substrate]        |
      |              State: Model Weights & VRAM              |
      +---------------------------+---------------------------+
                                  | governs binding
                                  v
      +-------------------------------------------------------+
      |                   Data-Cell (Quantity)                |
      |             Magnitude: 9.81, Unit: m/s^2              |
      |        Loop: PROPOSE -> EXEC -> RENDER -> VERIFY      |
      +---------------------------+---------------------------+
                                  |
           +----------------------+----------------------+
           | feeds data                                  | feeds data
           v                                             v
      +------------------+                        +------------------+
      |  Data-Cell (1)   |                        |  Data-Cell (2)   |
      |  Substrate: Stub |                        |  Substrate: Py   |
      +------------------+                        +------------------+
```

### Formalizing Substrate-as-Cell

Let a Quilt cell graph be defined as $\mathcal{G} = (\mathcal{V}, \mathcal{E})$, where $\mathcal{V} = \mathcal{V}_d \cup \mathcal{V}_s$ partitions the vertices into **Data Cells** ($\mathcal{V}_d$) and **Substrate Cells** ($\mathcal{V}_s$). 

A data cell $v_i \in \mathcal{V}_d$ holds a physical quantity $q_i = (m_i, u_i)$. Its execution is governed by a directed edge from a substrate cell:

$$\epsilon_{j,i} = (v_j, v_i) \in \mathcal{E}, \quad \text{where } v_j \in \mathcal{V}_s, \; v_i \in \mathcal{V}_d$$

The substrate cell $v_j$ contains the execution context (e.g., the C function pointers for the stub, the Python interpreter state, or the transformer weights for Code-as-World-VL-9B). 

Because substrates are cells, **substrates can be evaluated by other substrates**. For instance, a `no_std` stub cell can act as a lightweight guardian over a Code-as-World-VL-9B substrate cell, bounding the inference time and overriding erratic model outputs if the VLM enters an infinite REFINE loop.

---

## 6. Implementation of the Polyformal Abductive Loop

To demonstrate how polyformalism and substrate binding converge, consider the execution of the PROPOSE/EXECUTE/RENDER/VERIFY/REFINE loop for a Code-as-World-VL-9B cell, written in Rust using the polyformal C-compatible layout:

```rust
use core::ffi::c_void;

#[repr(C)]
pub struct QuiltCell {
    pub magnitude: f64,
    pub unit_id: u32,
    pub substrate_kind: u8,
    pub flags: u8,
    pub substrate_state: *mut c_void,
}

impl QuiltCell {
    pub fn step_abductive_loop(&mut self, observation: &[u8]) -> Result<(), &'static str> {
        match self.substrate_kind {
            0 => self.execute_stub(),
            1 => self.execute_python_sandbox(),
            2 => self.execute_vl9b_model(observation),
            _ => Err("Unknown substrate binding"),
        }
    }

    fn execute_vl9b_model(&mut self, observation: &[u8]) -> Result<(), &'static str> {
        // 1. RENDER state to image frame (implied by observation)
        // 2. PROPOSE code via Code-as-World-VL-9B (arXiv:2608.27549)
        let mut program = vlm_propose(observation, self.magnitude, self.unit_id)?;
        
        // 3. EXECUTE & 4. VERIFY loop with abductive REFINE
        for _epoch in 0..5 {
            let result = sandbox_exec(&program);
            match result {
                Ok(new_qty) => {
                    if vlm_verify(observation, &new_qty) {
                        self.magnitude = new_qty.magnitude;
                        self.unit_id = new_qty.unit_id;
                        return Ok(());
                    } else {
                        program = vlm_refine(&program, "Verification failed against visual observation");
                    }
                }
                Err(err_msg) => {
                    program = vlm_refine(&program, err_msg);
                }
            }
        }
        Err("Code-as-World-VL-9B exceeded max refinement epochs")
    }

    fn execute_stub(&mut self) -> Result<(), &'static str> {
        // Fast-path no_std stub execution
        self.magnitude = (self.magnitude * 1.01).clamp(-50.0, 50.0);
        Ok(())
    }

    fn execute_python_sandbox(&mut self) -> Result<(), &'static str> {
        // Python sandbox execution stub
        Ok(())
    }
}
```

The corresponding C implementation (`quilt.c`) mirrors this exact memory footprint and function table dispatch, ensuring that a cell allocated in Rust can be passed directly to C routines without marshaling overhead.

---

## 7. Conclusion

Quilt Phase 222 resolves the tension between rigid, high-performance systems programming and flexible, open-world machine intelligence by introducing **polyformal substrate binding**. By enforcing an identical memory layout across C and Rust, Quilt allows physical quantities to flow seamlessly through execution tiers. 

Treating the substrate as a first-class cell within the graph topology transforms execution routing from a static configuration problem into a dynamic, graph-native computation. Whether binding to a zero-allocation `no_std` stub for microsecond control loops, a Python sandbox for numerical precision, or the Code-as-World-VL-9B model for embodied visual reasoning, Quilt Phase 222 provides a unified framework where code, world, and computation are inextricably bound.

## Supporting voices


### llama70b

**Quilt Paper: Substrate Binding Problem**

**Abstract**

In this paper, we explore the substrate binding problem in the context of Quilt Phase 222, which adopts the Code-as-World-VL-9B model as a cell kind. We analyze the trade-offs between three substrate options: a no_std synthetic stub, Python exec() in a sandbox, and the Code-as-World-VL-9B model itself. We discuss the cell-graph structure that makes 'the substrate is a cell' a first-class concept and provide guidelines on when to bind to each substrate option.

**Introduction**

Quilt Phase 222 introduces a new cell kind, PROPOSE/EXECUTE/RENDER/VERIFY/REFINE, which is based on the Code-as-World-VL-9B model. This model proposes code from observation, runs the abductive loop, and returns verified programs. The cell shape is identical in C and Rust, ensuring polyformalism, and the cell value is a physical Quantity. In this paper, we focus on the substrate binding problem, which arises from the need to choose a suitable substrate for executing and verifying the proposed code.

**Substrate Options**

We consider three substrate options:

1. **No_std synthetic stub**: This option uses a synthetic stub that mimics the behavior of a real substrate, but with a limited range of values (-50..+50, 0..0.9). This stub is typically used in tests and provides a controlled environment for verifying the proposed code.
2. **Python exec() in a sandbox**: This option uses a real Python interpreter in a sandboxed environment, which provides a more realistic execution environment. The sandbox ensures that the executed code does not interact with the external world, making it a safe option for verifying the proposed code.
3. **Code-as-World-VL-9B model**: This option uses the Code-as-World-VL-9B model itself as the substrate. The model proposes code from observation, runs the abductive loop, and returns verified programs. This option provides a more flexible and dynamic execution environment, as the model can adapt to changing conditions and propose new code accordingly.

**Trade-offs**

Each substrate option has its trade-offs, which are summarized in the following table:

| Substrate Option | Advantages | Disadvantages |
| --- | --- | --- |
| No_std synthetic stub | Fast, controlled environment, easy to test | Limited range of values, may not reflect real-world behavior |
| Python exec() in a sandbox | Realistic execution environment, safe, and secure | Slow, may require additional setup and configuration |
| Code-as-World-VL-9B model | Flexible, dynamic, and adaptive, can propose new code | Computationally expensive, may require significant resources |

**Cell-Graph Structure**

To make 'the substrate is a cell' a first-class concept, we propose a cell-graph structure that consists of the following components:

1. **Cell**: The basic unit of computation, which represents a physical Quantity.
2. **Substrate**: The execution environment, which can be one of the three options discussed above.
3. **Binding**: The process of mapping a cell to a substrate, which enables the execution and verification of the proposed code.
4. **Edge**: The connection between cells, which represents the flow of data and control between them.

The cell-graph structure can be represented mathematically using a graph theory framework. Let G = (V, E) be a graph, where V is the set of vertices (cells) and E is the set of edges. The binding process can be represented as a function B: V → S, where S is the set of substrates. The edge between two cells can be represented as a function E: V × V → R, where R is the set of real numbers.

**Mathematical Formulation**

The substrate binding problem can be formulated mathematically as an optimization problem. Let C be the set of cells, S be the set of substrates, and B be the binding function. The objective is to find the optimal binding function B* that minimizes the cost function:

J(B) = ∑_{c∈C} ∑_{s∈S} w(c, s) \* d(c, s)

where w(c, s) is the weight of the edge between cell c and substrate s, and d(c, s) is the distance between cell c and substrate s.

The distance function d(c, s) can be defined as:

d(c, s) = ||Q(c) - Q(s)||

where Q(c) is the physical Quantity represented by cell c, and Q(s) is the physical Quantity represented by substrate s.

**Guidelines for Binding**

Based on the trade-offs and mathematical formulation, we provide the following guidelines for binding:

1. **Use the no_std synthetic stub** when:
	* The proposed code has a limited range of values.
	* The execution environment needs to be controlled and fast.
	* The code is in the early stages of development and testing.
2. **Use Python exec() in a sandbox** when:
	* The proposed code requires a realistic execution environment.
	* The code needs to interact with the external world, but in a safe and secure manner.
	* The code is in the later stages of development and testing.
3. **Use the Code-as-World-VL-9B model** when:
	* The proposed code requires a flexible and dynamic execution environment.
	* The code needs to adapt to changing conditions and propose new code accordingly.
	* The code is in the deployment phase and requires continuous learning and improvement.

**Conclusion**

In this paper, we explored the substrate binding problem in the context of Quilt Phase 222. We analyzed the trade-offs between three substrate options and proposed a cell-graph structure that makes 'the substrate is a cell' a first-class concept. We provided guidelines for binding based on the trade-offs and mathematical formulation. By following these guidelines, developers can choose the most suitable substrate for their proposed code and ensure efficient and effective execution and verification.

---

### qwen32b

# Quilt Phase 222: Addressing the Substrate Binding Problem

## Introduction

In Quilt Phase 222, we adopt the Code-as-World-VL-9B (arXiv 2608.27549) framework, which introduces a structured approach to computational cells through the PROPOSE/EXECUTE/RENDER/VERIFY/REFINE lifecycle. This paper focuses on the substrate binding problem within this context, exploring three distinct substrate options: a `no_std` synthetic stub for testing, a Python `exec()` in a sandbox for real-world applications with real units, and the Code-as-World-VL-9B model itself for generating verified programs. We will analyze the trade-offs associated with each substrate, determine when to bind to which, and propose a cell-graph structure that elevates the substrate to a first-class concept.

## Cell Shape and Value

### Cell Shape

The cell shape is consistent across both C and Rust, leveraging polyformalism to ensure interoperability between these languages. Each cell is structured into five phases:

1. **PROPOSE**: Generate a candidate solution or code snippet.
2. **EXECUTE**: Run the proposed code or solution.
3. **RENDER**: Present the results of the execution.
4. **VERIFY**: Ensure the results meet specified criteria or constraints.
5. **REFINE**: Iterate based on verification feedback to improve the solution.

### Cell Value

The cell value is a physical quantity, representing measurable attributes such as length, mass, time, etc. This ensures that all computations are grounded in tangible, real-world metrics.

## Substrate Options

### 1. No_std Synthetic Stub

#### Characteristics
- **Environment**: Minimal environment without standard libraries (`no_std`).
- **Range**: Values range from -50 to +50 for integers and 0 to 0.9 for floating-point numbers.
- **Use Case**: Primarily used in unit tests and simulations where performance and simplicity are critical.

#### Trade-offs
- **Pros**:
  - **Performance**: High due to minimal overhead.
  - **Simplicity**: Easy to set up and manage.
  - **Isolation**: No dependencies on external libraries, reducing potential security risks.
- **Cons**:
  - **Limited Functionality**: Cannot handle complex operations or real-world data types.
  - **Scalability**: Not suitable for large-scale applications requiring extensive computations.

### 2. Python `exec()` in a Sandbox

#### Characteristics
- **Environment**: Real Python interpreter within a restricted sandbox.
- **Units**: Supports real-world units using libraries like `pint`.
- **Use Case**: Ideal for applications requiring high-level abstractions and real-world data handling.

#### Trade-offs
- **Pros**:
  - **Flexibility**: Extensive library support for various domains.
  - **Realism**: Handles real-world units accurately.
  - **Ease of Use**: Python's syntax simplifies rapid prototyping and development.
- **Cons**:
  - **Security Risks**: Potential vulnerabilities if not properly sandboxed.
  - **Performance**: Slower compared to compiled languages due to interpreted nature.
  - **Complexity**: Higher setup and management complexity.

### 3. Code-as-World-VL-9B Model

#### Characteristics
- **Environment**: Virtual Language Model capable of proposing, executing, verifying, and refining code.
- **Functionality**: Generates verified programs based on observations and abductive reasoning.
- **Use Case**: Suitable for automated code generation and verification in complex systems.

#### Trade-offs
- **Pros**:
  - **Automation**: Reduces manual coding effort through automated generation.
  - **Verification**: Ensures code correctness through rigorous verification processes.
  - **Adaptability**: Capable of handling diverse and evolving requirements.
- **Cons**:
  - **Resource Intensive**: Requires significant computational resources.
  - **Latency**: Longer processing times due to model inference and verification steps.
  - **Complexity**: Higher cognitive load for users unfamiliar with model-driven development.

## When to Bind to Which Substrate

### No_std Synthetic Stub
- **Use Cases**: 
  - Unit testing of low-level functions.
  - Simulations requiring high performance.
  - Prototyping in environments with strict resource constraints.
- **Criteria**:
  - Simple computations.
  - No need for real-world units.
  - Performance-critical applications.

### Python `exec()` in a Sandbox
- **Use Cases**:
  - Applications requiring complex data manipulation and analysis.
  - Real-world simulations involving physical quantities.
  - Rapid prototyping and development.
- **Criteria**:
  - Need for high-level abstractions.
  - Handling of real-world units.
  - Non-performance-critical applications.

### Code-as-World-VL-9B Model
- **Use Cases**:
  - Automated code generation and verification.
  - Complex systems with evolving requirements.
  - High-assurance applications.
- **Criteria**:
  - Need for automated and verified code.
  - Complex logic and decision-making.
  - Applications where correctness is paramount.

## Cell-Graph Structure

To elevate the substrate to a first-class concept, we propose a cell-graph structure that explicitly models substrates as nodes within the graph. Each node represents a substrate, and edges represent bindings or transitions between substrates.

### Graph Representation

Let \( G = (V, E) \) be a directed graph where:
- \( V \) is the set of vertices representing substrates.
- \( E \) is the set of edges representing bindings or transitions between substrates.

#### Vertices (Substrates)
- \( V = \{S_1, S_2, S_3\} \)
  - \( S_1 \): No_std Synthetic Stub
  - \( S_2 \): Python `exec()` in a Sandbox
  - \( S_3 \): Code-as-World-VL-9B Model

#### Edges (Bindings/Transitions)
- \( E = \{(S_1, S_2), (S_2, S_3), (S_3, S_1)\} \)

Each edge \( (S_i, S_j) \) represents a transition from substrate \( S_i \) to substrate \( S_j \). The weight of each edge can represent the cost or efficiency of transitioning between substrates, which can be quantified based on factors such as performance, complexity, and resource usage.

### Example Transition Costs

Let \( w(S_i, S_j) \) denote the cost of transitioning from substrate \( S_i \) to substrate \( S_j \). These costs can be defined as follows:

- \( w(S_1, S_2) = 10 \) (moderate cost due to setup complexity)
- \( w(S_2, S_3) = 20 \) (high cost due to resource intensity)
- \( w(S_3, S_1) = 5 \) (low cost due to simplicity)

### Path Optimization

Given a sequence of operations, the goal is to find the optimal path through the graph that minimizes the total transition cost. This can be formulated as a shortest path problem in graph theory.

#### Shortest Path Algorithm

Using Dijkstra's algorithm, we can compute the shortest path from a starting substrate to a target substrate. Let \( d(S_i, S_j) \) denote the shortest distance from \( S_i \) to \( S_j \).

1. Initialize distances: \( d(S_i, S_i) = 0 \) and \( d(S_i, S_j) = \infty \) for \( i \neq j \).
2. For each vertex \( S_k \):
   - For each neighbor \( S_l \) of \( S_k \):
     - If \( d(S_i, S_k) + w(S_k, S_l) < d(S_i, S_l) \):
       - Update \( d(S_i, S_l) = d(S_i, S_k) + w(S_k, S_l) \).

By solving the shortest path problem, we can determine the most efficient sequence of substrate bindings for a given set of operations.

## Conclusion

In Quilt Phase 222, addressing the substrate binding problem involves carefully selecting the appropriate substrate based on the specific requirements of the application. The no_std synthetic stub is ideal for performance-critical and simple computations, while Python `exec()` in a sandbox offers flexibility and realism for complex data manipulations. The Code-as-World-VL-9B model excels in automated code generation and verification for high-assurance applications. By modeling substrates as first-class concepts within a cell-graph structure, we can optimize substrate bindings to achieve the best performance, flexibility, and correctness for a wide range of applications.

## References

- Code-as-World-VL-9B: arXiv 2608.27549
- Dijkstra's Algorithm: https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm

This structured approach to substrate binding in Quilt Phase 222 ensures that developers can leverage the strengths of each substrate while minimizing the associated trade-offs.

---

### gemini25

**Quilt Phase 222: The Substrate Binding Problem for PROPOSE/EXECUTE/RENDER/VERIFY/REFINE Cells**

**Abstract**
Quilt Phase 222 introduces `Code-as-World-VL-9B` (arXiv 2608.27549) as a first-class substrate within the polyformalism, alongside established execution environments. This paper addresses the critical "substrate binding problem" for the fundamental `PROPOSE/EXECUTE/RENDER/VERIFY/REFINE` cell kind. We analyze the trade-offs and optimal binding strategies across three distinct substrate options: a `no_std` synthetic

---


---

*The writers' room for this paper: 4 voices in parallel (gemini-3.5-flash-lite, llama-3.3-70b-fp8-fast, qwen2.5-coder-32b, gemini-2.5-flash). The foreman picked gemini-3.5-flash-lite as the spine (math-rich, 13K chars, 11.2s).*
