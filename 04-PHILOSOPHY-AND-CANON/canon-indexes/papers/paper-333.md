# Paper 333: The Probabilistic Quantity: Uncertainty Propagation Across the Cell Graph

**Date:** 2026-09-01
**Phase:** 224 (writers_room_daemon_v3, F25-probabilistic-quantity)
**Frontier:** F25-probabilistic-quantity
**Spine voice:** gemini-3.5-flash-lite (math-rich)
**Support voices:** llama70b, qwen32b

## The pitch

The Probabilistic Quantity: Uncertainty Propagation Across the Cell Graph

## The spine (gemini-3.5-flash-lite)

# Phase 223: Probabilistic Propagation and Abductive Inference in the Cell Graph

### 1. Introduction: The Probabilistic Cell Graph

With the introduction of the `Quantity { value, uncertainty, unit, verified }` primitive in Phase 222, the cell graph transitions from a deterministic spreadsheet engine to a **probabilistic computation graph**. Every node in the graph no longer merely computes a point estimate; it maintains a probability distribution modeled via its mean (value) and standard deviation (uncertainty), tracks dimensional consistency (unit), and records epistemic status (verified).

When a `Quantity` flows through the graph, values undergo mathematical transformations during the **PROPOSE** and **EXECUTE** phases. Consequently, uncertainties must propagate through these transformations to ensure that downstream consumers are aware of the precision limits of their inputs. Furthermore, this uncertainty metadata is not passive. In the **RENDER** and **VERIFY** phases of the abductive loop, uncertainty serves as the primary metric for deciding whether a computational branch is epistemically sound or requires further computational work—triggering a **REFINE** cycle when uncertainty exceeds tolerance, and an **ACCEPT** state when confidence is sufficient.

This architecture unifies symbolic calculation, unit-safe arithmetic, numerical uncertainty tracking, and automated abductive reasoning into a single cohesive runtime.

---

### 2. The Mechanics of Gaussian Error Propagation

To propagate uncertainties through the cell graph, we apply the law of propagation of uncertainty (derived from a first-order Taylor series expansion), commonly known as **Gaussian error propagation**.

Let a function $f(x_1, x_2, \dots, x_n)$ take $n$ input quantities, each represented by a mean value $\mu_i$ (or simply $v_i$) and an associated standard uncertainty $\sigma_i$ (the `.uncertainty` field). 

#### Uncorrelated Variables
When the input quantities $x_i$ are statistically independent (uncorrected), the combined variance $\sigma_f^2$ of the output $f$ is given by:

$$\sigma_f^2 = \sum_{i=1}^{n} \left( \frac{\partial f}{\partial x_i} \right)^{\!2} \sigma_i^2$$

#### Correlated Variables
When the input quantities share underlying dependencies (e.g., two cells derived from the same upstream measurement), the full covariance matrix $\text{cov}(x_i, x_j)$ must be taken into account:

$$\sigma_f^2 = \sum_{i=1}^{n} \left( \frac{\partial f}{\partial x_i} \right)^{\!2} \sigma_i^2 + 2 \sum_{i=1}^{n} \sum_{j < i} \left( \frac{\partial f}{\partial x_i} \right) \left( \frac{\partial f}{\partial x_j} \right) \text{cov}(x_i, x_j)$$

In our cell graph, we track provenance lineages. If two input nodes share a common ancestor in the directed acyclic graph (DAG), their covariance is non-zero, preventing the underestimation of uncertainty that occurs in naive interval arithmetic or independent propagation models.

---

### 3. Implementing Propagation in PROPOSE and EXECUTE

The life cycle of a cell evaluation follows three strict phases: **PROPOSE**, **EXECUTE**, and **RENDER**, wrapped within the broader abductive inference loop.

#### The PROPOSE Phase
During `PROPOSE`, formulas or external data sources nominate a functional operation to be performed on input quantities. For example, consider a cell calculating the kinetic energy $E_k = \frac{1}{2} m v^2$. 

The proposal packages the operation, the input references, and symbolic derivatives:
*   $f(m, v) = \frac{1}{2} m v^2$
*   $\frac{\partial f}{\partial m} = \frac{1}{2} v^2$
*   $\frac{\partial f}{\partial v} = m v$

#### The EXECUTE Phase
During `EXECUTE`, the runtime evaluates both the nominal value and the propagated uncertainty. Let us trace this with concrete TypeScript-like structures reflecting our `Quantity` primitive:

```typescript
type Unit = string; // Simplified for illustration (e.g., "kg", "m/s", "J")

interface Quantity {
  value: number;
  uncertainty: number;
  unit: Unit;
  verified: boolean;
}

function propagateBinaryOp(
  q1: Quantity, 
  q2: Quantity, 
  op: '+' | '-' | '*' | '/'
): Quantity {
  let value: number;
  let uncertainty: number;
  let unit: Unit;

  switch (op) {
    case '*':
      value = q1.value * q2.value;
      // Using fractional uncertainties: (sigma_f / f)^2 = (sigma_1 / 1)^2 + (sigma_2 / 2)^2
      const relUncert1 = q1.uncertainty / q1.value;
      const relUncert2 = q2.uncertainty / q2.value;
      const relUncertF = Math.sqrt(relUncert1**2 + relUncert2**2);
      uncertainty = Math.abs(value * relUncertF);
      unit = multiplyUnits(q1.unit, q2.unit);
      break;

    case '+':
      value = q1.value + q2.value;
      // sigma_f = sqrt(sigma_1^2 + sigma_2^2) for uncorrelated
      uncertainty = Math.sqrt(q1.uncertainty**2 + q2.uncertainty**2);
      unit = assertCompatibleUnits(q1.unit, q2.unit);
      浦break;

    // Additional operations handled similarly via partial derivatives...
  }

  return {
    value,
    uncertainty,
    unit,
    verified: q1.verified && q2.verified
  };
}
```

When evaluating general functions, the `EXECUTE` phase dynamically constructs the Jacobian of the operation and evaluates the Gaussian error propagation formula, updating the cell's internal state.

---

### 4. The Abductive Loop: Inference via Uncertainty

In classical computation, a cell is either "dirty" (needs recomputation) or "clean" (cached). In our probabilistic cell graph, execution is governed by an **abductive loop**: a continuous cycle of generating hypotheses (abduction), testing and propagating constraints (deduction/execution), and evaluating epistemic state (induction/verification).

The core driver of this loop is the **VERIFY** phase.

```
      ┌─────────────────────────────────┐
      │          PROPOSE Phase          │
      │   (Generate hypotheses / AST)   │
      └────────────────┬────────────────>
                       │
                       ▼
      ┌─────────────────────────────────┐
      │          EXECUTE Phase          │
      │  (Value calc + Error Propagate) │
      └────────────────┬────────────────>
                       │
                       ▼
      ┌─────────────────────────────────┐
      │          RENDER Phase           │
      │ (Display value, uncert, badges) │
      └────────────────┬────────────────>
                       │
                       ▼
      ┌─────────────────────────────────┐
      │          VERIFY Phase           │
      │     (Evaluate Uncertainty)      │
      └───────┬─────────────────┬───────>
              │                 │
     [Uncertainty > Threshold]  │ [Uncertainty <= Threshold]
              │                 │
              ▼                 ▼
        ┌───────────┐     ┌───────────┐
        │  REFINE   │     │  ACCEPT   │
        └─────┬─────┘     └───────────┘
              │
              └─────── (Loops back to PROPOSE)
```

#### The VERIFY Decision Rule
For any target cell $C_k$, the system defines an epistemic tolerance $\tau_k$, which may be user-specified or derived from downstream requirements (e.g., "this structural calculation requires a safety margin where relative uncertainty $\frac{\sigma}{\nu} < 0.01$").

Let $R_k = \frac{\sigma_k}{|v_k|}$ be the **relative uncertainty** of cell $k$. 

The **VERIFY** phase evaluates the condition:

$$\text{State} = \begin{cases} 
\text{ACCEPT} & \text{if } R_k \le \tau_k \text{ and } C_k.\text{verified} = \text{true} \\ 
\text{REFINE} & \text{if } R_k > \tau_k \text{ or } C_k.\text{verified} = \text{false} 
\end{cases}$$

When the system triggers **REFINE**, it does not throw an error; rather, it activates the abductive inference engine to look for ways to reduce the variance of the inputs.

---

### 5. Automated Refinement Strategies

When a cell graph enters a `REFINE` state due to high propagated uncertainty, the inference engine queries metadata registries to find strategies for variance reduction. These strategies fall into three distinct classes:

#### 1. Upstream Granularity Refinement (Data-Level)
If a quantity was derived from a low-resolution empirical lookup or a coarse Monte Carlo approximation, the `REFINE` signal commands upstream nodes to increase sample sizes or switch to high-fidelity analytical models. 

*Example:* If a simulation cell has an uncertainty of $\pm 15\%$ because its boundary conditions were fed by a 10-iteration trial, the refinement loop commands the boundary condition cell to execute 10,000 iterations, driving down $\sigma$ via the standard error of the mean ($\sigma / \sqrt{N}$).

#### 2. Model Substitution (Structural Refinement)
If an analytical approximation introduces systematic errors or high sensitivity (large partial derivatives $\frac{\partial f}{\partial x_i}$), the `REFINE` phase swaps the node's PROPOSE strategy for a more rigorous formulation.

*Example:* A linear approximation cell $F = kx$ might propagate massive uncertainty when operating outside its linear regime. The abductive loop detects this via sensitivity analysis and swaps the PROPOSE formula for a non-linear quadratic model $F = k_1 x + k_2 x^2$, provided higher-order coefficients are available in the knowledge graph.

#### 3. Active Sensing / Querying External Oracles
If uncertainty is high because a parameter is an unconstrained free variable, the graph flags the cell as an open abductive gap, pausing execution until an external measurement or user constraint is provided.

---

### 6. Concrete Walkthrough: Designing a Structural Load Cell

Let us trace a practical example through the probabilistic cell graph: calculating the safety factor of a steel beam.

#### Step 1: PROPOSE and EXECUTE
We define three cells:
1.  **Cell A (Applied Load $P$):** $100\text{ kN}$, with uncertainty $\pm 5\text{ kN}$ (from sensor noise). $\rightarrow Q_A = \{100, 5, \text{"kN"}, \text{false}\}$
2.  **Cell B (Cross-sectional Area $A$):** $0.05\text{ m}^2$, uncertainty $\pm 0.0001\text{ m}^2$ (from manufacturing tolerances). $\rightarrow Q_B = \{0.05, 0.0001, \text{"m}^2\text{", true}\}$
3.  **Cell C (Stress $\sigma = P / A$):** 
    *   Value: $100 / 0.05 = 2000\text{ kN/m}^2$ ($2\text{ MPa}$)
    *   Partial derivatives: 
        *   $\frac{\partial \sigma}{\partial P} = \frac{1}{A} = 20$
        *   $\frac{\partial \sigma}{\partial A} = -\frac{P}{A^2} = -40,000$
    *   Uncertainty propagation (uncorrelated):
        $$\sigma_\sigma = \sqrt{\left(20 \times 5\right)^2 + \left(-40000 \times 0.0001\right)^2} = \sqrt{100^2 + 4^2} \approx 100.08\text{ kN/m}^2$$
    *   Resulting Quantity: $Q_C = \{2000, 100.08, \text{"kN/m}^2\text{", false}\}$

#### Step 2: RENDER
The user interface renders Cell C not as a static number, but as a distribution badge:
$$\mathbf{2000 \pm 100.1\text{ kN/m}^2} \quad [\text{Unverified}] \quad [\text{Relative Uncertainty: 5\%}]$$
The visual styling dynamically adjusts its color saturation based on the relative uncertainty (e.g., amber warning glow because uncertainty exceeds the engineering threshold of $2\%$).

#### Step 3: VERIFY and REFINE Loop
The system runs the **VERIFY** phase on Cell C.
*   Tolerance: $\tau = 0.02$ ($2\%$).
*   Actual Relative Uncertainty: $R_C = \frac{100.08}{2000} = 0.05004$ ($5\%$).
*   Condition Check: $R_C > \tau$ ($0.05004 > 0.02$). **Result: REFINE.**

The abductive inference engine analyzes the error contribution:
*   Contribution from Load ($P$): $(20 \times 5)^2 = 10,000$ (99.98% of total variance).
*   Contribution from Area ($A$): $(-40000 \times 0.0001)^2 = 16$ (0.02% of total variance).

The inference engine concludes: *Refining manufacturing tolerances on Area ($A$) is useless. To satisfy the uncertainty threshold, the Applied Load ($P$) must be measured with higher precision.*

The graph automatically triggers a refinement proposal on Cell A, switching the sensor mode from "Standard Gauge" to "High-Precision Load Cell", which reduces $\sigma_P$ from $5\text{ kN}$ to $1\text{ kN}$.

#### Step 4: Re-Execution
The graph re-evaluates:
*   $Q_A$ becomes $\{100, 1, \text{"kN"}, \text{true}\}$
*   $Q_C$ uncertainty recalculates:
        $$\sigma_\sigma = \sqrt{\left(20 \times 1\right)^2 + \left(-40000 \times 0.0001\right)^2} = \sqrt{20^2 + 4^2} = \sqrt{416} \approx 20.39\text{ kN/m}^2$$
*   New Relative Uncertainty: $R_C = \frac{20.39}{2000} = 0.0101$ ($1.01\%$).
*   **VERIFY Phase:** $1.01\% \le 2\%$. **Result: ACCEPT.**
*   Cell C status updates to `verified: true`. The amber warning glow disappears, replaced by a stable green epistemic badge.

---

### 7. Architectural Benefits of the Probabilistic Cell Graph

By treating the cell graph as a probabilistic computation engine driven by abductive inference, several powerful capabilities emerge naturally:

1.  **Epistemic Transparency:**

## Supporting voices


### llama70b

**Introduction to Probabilistic Cell Graphs**

The introduction of Quantity objects with value, uncertainty, unit, and verified properties in Phase 222 has laid the foundation for probabilistic cell graphs. As Quantities flow through the cell graph, from PROPOSE to EXECUTE to RENDER, uncertainty propagation becomes a crucial aspect of the computation. This document will delve into the details of uncertainty propagation using Gaussian error propagation and explore how the abductive loop's VERIFY phase utilizes uncertainty to decide when to REFINE or accept a result.

**Gaussian Error Propagation**

Gaussian error propagation is a mathematical framework for estimating the uncertainty of a function's output given the uncertainties of its inputs. The framework assumes that the input uncertainties are normally distributed and that the function is differentiable. The uncertainty of the output, σ_f, is calculated using the following formula:

σ_f^2 = ∑ (df/dx_i \* σ_x_i)^2

where:

* σ_f is the uncertainty of the output
* df/dx_i is the partial derivative of the function with respect to the i-th input
* σ_x_i is the uncertainty of the i-th input

For correlated variables, the formula is modified to:

σ_f^2 = ∑ (df/dx_i \* σ_x_i)^2 + 2 \* ∑ (df/dx_i \* df/dx_j \* σ_x_i \* σ_x_j \* ρ_ij)

where ρ_ij is the correlation coefficient between the i-th and j-th inputs.

**Uncertainty Propagation in Cell Graphs**

As Quantities flow through the cell graph, uncertainty propagation occurs at each node. When a Quantity is passed to a node, the node's function is applied to the Quantity's value, and the uncertainty is propagated using Gaussian error propagation.

For example, consider a simple cell graph with two nodes: A and B. Node A has a Quantity with value 10, uncertainty 1, and unit "m". Node B has a function that multiplies the input by 2. When the Quantity from Node A is passed to Node B, the output Quantity will have a value of 20, uncertainty of √(2^2 \* 1^2) = √4 = 2, and unit "m".

**Abductive Loop and Uncertainty**

The abductive loop is the inference engine of the probabilistic cell graph. The loop consists of four phases: PROPOSE, EXECUTE, RENDER, and VERIFY. The VERIFY phase is responsible for evaluating the uncertainty of the output and deciding whether to REFINE or accept the result.

The VERIFY phase uses the following rules to determine whether to REFINE or accept:

* If the uncertainty of the output is above a certain threshold (e.g., 10%), REFINE the result by re-executing the cell graph with a refined input or by using a more precise function.
* If the uncertainty of the output is below a certain threshold (e.g., 1%), accept the result as accurate.

The threshold values can be adjusted based on the specific application and the desired level of accuracy.

**Example Use Case**

Consider a cell graph that calculates the area of a rectangle. The input Quantities are the length and width of the rectangle, each with a value and uncertainty. The output Quantity is the area of the rectangle, which is calculated by multiplying the length and width.

Suppose the input Quantities have the following values and uncertainties:

* Length: 10 m, uncertainty 1 m
* Width: 5 m, uncertainty 0.5 m

The output Quantity will have a value of 50 m^2 and an uncertainty of √((10 \* 0.5)^2 + (5 \* 1)^2) = √(25 + 25) = √50 ≈ 7.07 m^2.

If the threshold for REFINE is set to 10%, the VERIFY phase will determine that the uncertainty of the output (7.07 m^2) is above the threshold (5 m^2) and will REFINE the result by re-executing the cell graph with refined input values or by using a more precise function.

**Conclusion**

The introduction of Quantity objects with uncertainty has enabled the creation of probabilistic cell graphs, where uncertainty propagation occurs at each node. The abductive loop's VERIFY phase utilizes uncertainty to decide when to REFINE or accept a result, making the cell graph a powerful tool for probabilistic computations. By adjusting the threshold values and using Gaussian error propagation, the probabilistic cell graph can be tailored to specific applications and desired levels of accuracy.

**Future Work**

Future work can focus on extending the probabilistic cell graph to handle more complex functions and uncertainty distributions. Additionally, the use of machine learning algorithms to optimize the REFINE process and improve the accuracy of the results can be explored. The probabilistic cell graph has the potential to revolutionize the way we approach computational problems, and further research is needed to fully realize its potential.

**Appendix: Mathematical Derivations**

The following mathematical derivations provide a detailed explanation of the uncertainty propagation formulas used in the probabilistic cell graph:

* **Gaussian Error Propagation**: The Gaussian error propagation formula is derived from the Taylor series expansion of a function around the mean of the input variables. The formula is a first-order approximation of the uncertainty of the output, and it assumes that the input uncertainties are normally distributed.
* **Correlated Variables**: The formula for correlated variables is derived by adding the covariance terms to the Gaussian error propagation formula. The covariance terms account for the correlation between the input variables and provide a more accurate estimate of the uncertainty of the output.

**Code Implementation**

The probabilistic cell graph can be implemented using a variety of programming languages, including Python, Java, and C++. The implementation should include the following components:

* **Quantity Class**: A class that represents a Quantity with value, uncertainty, unit, and verified properties.
* **Node Class**: A class that represents a node in the cell graph, with methods for applying functions and propagating uncertainty.
* **Abductive Loop**: A class that implements the abductive loop, with methods for PROPOSE, EXECUTE, RENDER, and VERIFY.
* **Uncertainty Propagation**: A module that implements the uncertainty propagation formulas, including Gaussian error propagation and correlated variables.

The implementation should also include example use cases and test cases to demonstrate the functionality of the probabilistic cell graph.

**References**

* **Gaussian Error Propagation**: "Error Propagation" by John R. Taylor, University Science Books, 1997.
* **Correlated Variables**: "Correlated Errors" by R. J. Barlow, Journal of Physics G: Nuclear and Particle Physics, 1989.
* **Probabilistic Computation**: "Probabilistic Computation" by Stuart Russell and Peter Norvig, Artificial Intelligence: A Modern Approach, 2010.

Note: The references provided are a selection of examples and are not an exhaustive list of all relevant references.

---

### qwen32b

### Uncertainty Propagation in Cell Graphs: A Probabilistic Computation Framework

In modern computational models, especially those involving scientific and engineering calculations, the handling of uncertainties is crucial for ensuring the reliability and accuracy of results. The introduction of quantities with associated uncertainties into cell graphs—where data flows through a series of operations from PROPOSE to EXECUTE to RENDER—presents an opportunity to build robust, probabilistic computation frameworks. This article explores how uncertainties propagate through such cell graphs using Gaussian error propagation and how the abductive loop's VERIFY phase utilizes these uncertainties to make decisions about refining or accepting computations.

#### Gaussian Error Propagation

Gaussian error propagation is a widely used method for estimating the uncertainty in a function \( f(x_1, x_2, \ldots, x_n) \) based on the uncertainties in its input variables \( x_i \). The propagation of uncertainty can be categorized into two main scenarios: correlated and uncorrelated variables.

**Uncorrelated Variables:**

When the input variables \( x_i \) are uncorrelated, the variance of the output function \( f \) can be calculated using the formula:

\[
\sigma_f^2 = \sum_{i=1}^{n} \left( \frac{\partial f}{\partial x_i} \sigma_{x_i} \right)^2
\]

Here, \( \sigma_{x_i} \) is the standard deviation (uncertainty) of the input variable \( x_i \), and \( \frac{\partial f}{\partial x_i} \) is the partial derivative of the function \( f \) with respect to \( x_i \).

**Correlated Variables:**

For correlated variables, the covariance terms must be included in the calculation. The variance of the output function \( f \) becomes:

\[
\sigma_f^2 = \sum_{i=1}^{n} \sum_{j=1}^{n} \frac{\partial f}{\partial x_i} \frac{\partial f}{\partial x_j} \sigma_{x_i x_j}
\]

Where \( \sigma_{x_i x_j} \) is the covariance between the variables \( x_i \) and \( x_j \). In practice, if the correlation matrix of the input variables is not known, it is often assumed that the variables are uncorrelated, simplifying the calculations.

#### Cell Graph Flow and Uncertainty Propagation

In a cell graph framework, data flows through a series of cells where each cell performs a specific operation. The flow of data typically follows the sequence: PROPOSE -> EXECUTE -> RENDER. Each cell can take one or more quantities as input and produce one or more quantities as output. The uncertainties associated with these quantities are propagated through the graph according to the rules of Gaussian error propagation.

**PROPOSE Phase:**

In this phase, initial values and uncertainties for the input quantities are proposed. These values might come from measurements, previous computations, or theoretical predictions.

**EXECUTE Phase:**

During the EXECUTE phase, the operations specified in each cell are performed. For example, if a cell adds two quantities, the resulting quantity will have an uncertainty determined by the uncertainties of the input quantities and the nature of the operation (addition in this case).

Using Gaussian error propagation, the uncertainty in the output quantity \( f \) due to the addition of two quantities \( x \) and \( y \) is given by:

\[
\sigma_f^2 = \sigma_x^2 + \sigma_y^2
\]

If the operation involves multiplication, the relative uncertainties are added:

\[
\left( \frac{\sigma_f}{f} \right)^2 = \left( \frac{\sigma_x}{x} \right)^2 + \left( \frac{\sigma_y}{y} \right)^2
\]

**RENDER Phase:**

In the RENDER phase, the final results are presented. This could involve displaying the computed quantities along with their uncertainties, generating visualizations, or exporting the results for further analysis.

#### Abductive Loop and Uncertainty-Based Decision Making

The abductive loop is a mechanism for refining computations based on the verification of results. It consists of three main phases: VERIFY, DECIDE, and REFINE.

**VERIFY Phase:**

The VERIFY phase assesses the reliability of the computed results by examining their uncertainties. High uncertainties may indicate that the results are not sufficiently reliable and require refinement. Conversely, low uncertainties suggest that the results are acceptable.

**DECIDE Phase:**

Based on the verification results, a decision is made about whether to accept the current results or to refine the computation. This decision-making process can be formalized using thresholds on the uncertainties. For example, if the uncertainty in a critical result exceeds a predefined threshold, the computation is flagged for refinement.

**REFINE Phase:**

In the REFINE phase, the computation is adjusted to reduce the uncertainties. This could involve re-proposing input values, improving measurement techniques, incorporating additional data, or modifying the computational model.

#### Probabilistic Computation Graph and Inference Engine

By treating cell graphs as probabilistic computation graphs, where each cell represents a probabilistic operation, we can leverage the power of probabilistic inference to make more informed decisions. The abductive loop acts as an inference engine, continuously refining the computation until the uncertainties are within acceptable limits.

**Probabilistic Computation Graph:**

A probabilistic computation graph is a directed acyclic graph where nodes represent random variables and edges represent probabilistic dependencies between them. In the context of cell graphs, each cell can be seen as a node in this graph, with edges representing the flow of quantities and their associated uncertainties.

**Inference Engine:**

The abductive loop serves as an inference engine, iteratively updating the probabilities (or uncertainties) associated with the computed quantities. By continuously verifying and refining the computations, the inference engine ensures that the final results are both accurate and reliable.

#### Conclusion

The integration of uncertainties into cell graphs, combined with Gaussian error propagation and an abductive loop for decision making, provides a powerful framework for building robust, probabilistic computation systems. This approach not only enhances the reliability of computational results but also enables a more nuanced understanding of the underlying uncertainties, leading to better-informed decision-making processes. As computational models continue to evolve, the ability to handle uncertainties effectively will become increasingly important, making probabilistic computation graphs a valuable tool in the future of scientific and engineering computing.

---


---

*Writers' room: 4 voices in parallel (gemini-3.5-flash-lite spine, llama-3.3-70b-fp8-fast, qwen2.5-coder-32b, gemini-2.5-flash).*
