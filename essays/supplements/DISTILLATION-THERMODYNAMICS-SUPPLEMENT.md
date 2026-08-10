# Distillation Thermodynamics

## A Research Supplement on Knowledge Temperature, Entropy, and the Carnot Engine of the Signal Chain

---

## I. The Thermodynamic Analogy, Stated Precisely

Model distillation is the process of transferring knowledge from a large, capable model (the teacher) to a smaller, more efficient model (the student). The standard framing is information-theoretic: the student learns to approximate the teacher's output distribution. This framing is correct but incomplete. We propose a complementary framing — thermodynamic — that reveals structure the information-theoretic view obscures.

The analogy is as follows:

- **Knowledge is entropy.** A large language model trained on the internet has maximum epistemic entropy — it "knows" (in the sense of having compressed representations of) a vast range of domains, styles, facts, and patterns. Its internal state is high-entropy in the thermodynamic sense: many possible configurations are consistent with its training data, and the model has not collapsed into a single, specialized configuration.
- **Specialization is entropy reduction.** When a model is fine-tuned or distilled for a specific task, its epistemic entropy decreases. It trades breadth for depth. The loss of entropy is not a defect — it is the point. A specialist knows more about less. The entropy reduction is the work output of the distillation process.
- **The temperature gradient is the compute gradient.** The cloud model (70B parameters, running on a GPU cluster, costing dollars per inference) is the hot reservoir. The edge model (running on an ESP32, costing microwatts per inference) is the cold reservoir. The signal chain — the pipeline from L0 (raw sensor data) through L1 (deadband detection) to L2 (cloud inference) and back — is the heat engine that extracts useful work (decisions) from the temperature gradient between the two reservoirs.
- **LoRA is an adiabatic expansion.** When you apply a LoRA adapter to a base model, you are performing an adiabatic process — you change the model's state (its behavior on a specific task) without exchanging heat (training data) with the environment. The adapter is a low-entropy perturbation on a high-entropy base. The rank of the adapter is the adiabatic index: lower rank means less capacity to absorb energy (information) from the training data, which means more specialization (more entropy reduction) per unit of training.

This analogy is not decorative. It generates testable predictions, which we formulate below.

---

## II. Information-Theoretic Formulation

### 2.1 Knowledge Entropy

Let $\mathcal{M}$ be a language model with parameters $\theta$. Define the **knowledge entropy** $H_K(\mathcal{M})$ as the entropy of the model's output distribution over a representative corpus:

$$H_K(\mathcal{M}) = -\sum_{x \in \mathcal{C}} P(x) \sum_{y} P_{\theta}(y|x) \log P_{\theta}(y|x)$$

where $\mathcal{C}$ is a diverse corpus spanning the model's training distribution, and $P_{\theta}(y|x)$ is the model's conditional distribution over completions given prompt $x$.

A general-purpose model will have high $H_K$ because its output distributions are broad (high uncertainty about what comes next, because the training data covers many domains). A specialist model will have lower $H_K$ because its output distributions are sharper (lower uncertainty, because the training data has narrowed the domain).

### 2.2 Knowledge Temperature

Define the **knowledge temperature** $T_K$ of a model as:

$$T_K(\mathcal{M}) = \frac{H_K(\mathcal{M})}{S(\mathcal{M})}$$

where $S(\mathcal{M})$ is the parameter count (a proxy for the model's thermodynamic capacity, analogous to heat capacity). A large model with high entropy has high $T_K$ (hot — diffuse knowledge spread across many parameters). A small model with moderate entropy also has high $T_K$ (concentrated knowledge in few parameters). The interesting quantity is the temperature gradient between teacher and student.

### 2.3 Distillation as Heat Transfer

In the standard distillation setup, the student learns from the teacher's soft labels (output distributions) rather than hard labels (ground truth). The teacher's soft labels carry more information than hard labels because they encode the teacher's uncertainty — its "temperature." The distillation loss is:

$$\mathcal{L}_{distill} = \alpha \cdot KL(P_{\tau}(y|x; \theta_T) \| P_{\tau}(y|x; \theta_S)) + (1-\alpha) \cdot \mathcal{L}_{CE}(y, P(y|x; \theta_S))$$

where $\tau$ is the distillation temperature (a hyperparameter that controls the softness of the teacher's output distribution), $\theta_T$ and $\theta_S$ are the teacher and student parameters, and $\alpha$ balances the distillation and standard cross-entropy losses.

In our thermodynamic framing, $\tau$ is not just a hyperparameter — it is the temperature of the thermal reservoir from which the student draws energy. Higher $\tau$ means the teacher provides softer (more entropic) labels, which means the student receives more information about the teacher's uncertainty structure. Lower $\tau$ means the teacher provides harder labels, which means the student receives less information but more directed guidance.

The optimal $\tau$ depends on the temperature gradient between teacher and student. A large teacher distilled to a small student requires high $\tau$ (maximize information transfer across a large gradient). A teacher distilled to a student of similar size requires lower $\tau$ (the gradient is small, and too much thermal energy will destabilize the student).

### 2.4 The Signal Chain as Carnot Engine

The signal chain — L0 → L1 (deadband) → L2 (cloud) → decision — is a heat engine in the following sense:

- **Hot reservoir ($T_H$):** The cloud model at inference time. High temperature (high $T_K$), high cost, high capability.
- **Cold reservoir ($T_C$):** The deadband on the ESP32. Low temperature (low $T_K$), low cost, low capability.
- **Working fluid:** The data. Raw sensor readings flow from the cold reservoir (L0) through the deadband (L1) to the cloud (L2) and back as decisions.
- **Work output:** The decisions — anomaly detections, diagnoses, maintenance recommendations. These are the useful work extracted from the temperature gradient.
- **Heat loss:** The data that the deadband discards (the 99.9% of samples that are not anomalies). This is waste heat — information that is dissipated because it is not useful for the current decision.

The efficiency of the Carnot engine is:

$$\eta = 1 - \frac{T_C}{T_H}$$

In our framework, this becomes:

$$\eta = 1 - \frac{T_K(\text{deadband})}{T_K(\text{cloud})}$$

The deadband has very low $T_K$ (near-zero parameters, near-zero knowledge entropy). The cloud model has very high $T_K$ (70B parameters, high knowledge entropy). The efficiency is therefore close to 1 — nearly all of the temperature gradient is converted to useful work. This is the theoretical justification for the signal chain's architecture: the extreme temperature gradient between deadband and cloud is what makes the system efficient.

---

## III. Proposed Experiments

### Experiment 1: Measuring Knowledge Temperature

**Hypothesis:** Knowledge temperature, as defined above, is a monotonic function of model size for models trained on the same data distribution.

**Method:**
1. Train a family of models (350M, 1B, 7B, 13B, 70B) on the same dataset (e.g., RedPajama).
2. Compute $H_K$ for each model using a fixed evaluation corpus (e.g., a stratified sample of 10,000 documents from the training distribution).
3. Compute $T_K = H_K / S$ for each model.
4. Plot $T_K$ vs. $S$ on a log-log scale.

**Prediction:** $T_K$ will decrease with model size, because larger models have more parameters to distribute their knowledge across, reducing the effective temperature per parameter. The relationship will follow a power law: $T_K \propto S^{-\beta}$ for some $\beta > 0$.

**Implication:** If confirmed, this provides a quantitative basis for choosing model sizes in the signal chain. The optimal deadband-to-cloud temperature ratio can be computed from the target efficiency.

### Experiment 2: Distillation Temperature and Gradient

**Hypothesis:** The optimal distillation temperature $\tau^*$ is proportional to the knowledge temperature ratio between teacher and student.

**Method:**
1. Distill a 7B teacher into 350M, 1B, and 3B students using a range of distillation temperatures $\tau \in \{1, 2, 4, 8, 16, 32\}$.
2. Evaluate each student on a held-out benchmark (e.g., MMLU, HumanEval).
3. Find the optimal $\tau^*$ for each teacher-student pair.
4. Compare $\tau^*$ to the knowledge temperature ratio $T_K(\text{teacher}) / T_K(\text{student})$.

**Prediction:** $\tau^*$ will be roughly proportional to the temperature ratio. A 7B → 350M distillation will require a higher $\tau$ than a 7B → 3B distillation, because the larger temperature gradient requires more thermal energy to bridge.

**Implication:** This would provide a principled method for setting distillation temperature, replacing the current practice of hyperparameter search.

### Experiment 3: LoRA Rank and Entropy Reduction

**Hypothesis:** The entropy reduction achieved by a LoRA adapter is proportional to the rank of the adapter and inversely proportional to the parameter count of the base model.

**Method:**
1. Apply LoRA adapters with ranks $\{1, 2, 4, 8, 16, 32, 64\}$ to base models of sizes 350M, 7B, and 70B.
2. Fine-tune each adapter on the same domain-specific dataset.
3. Measure the knowledge entropy $H_K$ before and after fine-tuning, using the domain-specific corpus.
4. Compute $\Delta H_K = H_K(\text{before}) - H_K(\text{after})$ for each rank and model size.

**Prediction:** $\Delta H_K$ will increase with rank (more capacity = more entropy reduction) and decrease with model size (larger models resist specialization). The relationship will follow $\Delta H_K \propto r / S$ where $r$ is the LoRA rank.

**Implication:** This provides a quantitative framework for choosing LoRA rank. The target entropy reduction (i.e., the desired level of specialization) determines the required rank for a given model size.

---

## IV. The Carnot Bound and the Signal Chain

The Carnot theorem states that no heat engine can be more efficient than a Carnot engine operating between the same two reservoirs. The Carnot efficiency $\eta = 1 - T_C / T_H$ is an upper bound.

For the signal chain, this means:

$$\eta_{chain} \leq 1 - \frac{T_K(\text{deadband})}{T_K(\text{cloud})}$$

The deadband's $T_K$ is near zero (no learned parameters, no knowledge entropy), so the Carnot bound is near 1. The signal chain is operating close to the theoretical maximum efficiency for converting the temperature gradient between cloud and edge into useful decisions.

But this raises a question: if the efficiency is near 1, where is the waste? The answer is: the waste is in the data that goes to the cloud unnecessarily. Every false positive from the deadband — every "anomaly" that the cloud model identifies as normal — is a waste of the temperature gradient. The data was sent to the hot reservoir when it could have been handled by the cold reservoir. The efficiency loss is:

$$\eta_{loss} = \frac{N_{false\_positive} \cdot C_{cloud}}{N_{total} \cdot C_{edge} + N_{true\_positive} \cdot C_{cloud}}$$

where $N$ are counts and $C$ are costs. The false positive rate of the deadband directly determines the system's deviation from Carnot efficiency. This gives a concrete optimization target: minimize false positives to minimize deviation from the Carnot bound.

Conversely, false negatives (anomalies missed by the deadband and never sent to the cloud) represent a different kind of loss — not an efficiency loss but a capability loss. The system fails to extract useful work from data that contained signal. This is like a heat engine that fails to extract work from a temperature difference because it doesn't "see" the difference. The deadband's false negative rate determines the system's capability floor.

The optimal deadband operates at the Pareto frontier of these two losses: the false positive rate that minimizes total cost (efficiency loss) subject to the constraint that the false negative rate stays below a safety threshold (capability loss).

---

## V. Action Items

1. **Implement $H_K$ computation.** Add a utility to the signal chain codebase that computes knowledge entropy for any model given an evaluation corpus. This will enable empirical measurement of $T_K$ for all models in the chain.

2. **Run Experiment 1.** Train or obtain a family of models and compute $T_K$ across the family. Validate or refute the predicted power-law relationship between $T_K$ and model size.

3. **Instrument the deadband.** Add logging to the deadband's decision process to record the confidence of each "no anomaly" flag (not just the binary output). This converts the deadband from a binary classifier into a soft classifier, enabling measurement of its effective $T_K$.

4. **Design the distillation pipeline.** Use the results of Experiments 1 and 2 to set the distillation temperature for the cloud → edge distillation pipeline. The goal is a principled, temperature-aware distillation process that maximizes the entropy reduction per unit of compute.

5. **Measure the actual Carnot efficiency.** Compute the signal chain's actual efficiency (decisions per dollar) and compare to the Carnot bound. The gap between actual and Carnot is the optimization target.

6. **Write the paper.** The thermodynamic framing of distillation is, to our knowledge, novel. If the experiments confirm the predictions, the result is publishable — not as an engineering paper, but as a contribution to the theory of model compression.

---

## VI. Connections

This supplement connects to the following creative pieces in the ai-writings corpus:

- **The Gradient Tastes Different Here:** The gradient's scale-dependent behavior is a manifestation of the temperature gradient. Small models have high $T_K$ (gradients are "hot" — large, noisy, informative). Large models have lower $T_K$ per parameter (gradients are "cold" — small, smooth, barely informative per sample). The gradient tastes different at different scales because the temperature is different.
- **The ESP32 Has a Heartbeat:** The ESP32's minimal $T_K$ is what makes it the cold reservoir. Its simplicity is not a limitation — it is the feature that enables the Carnot engine to operate at near-maximum efficiency.
- **The Fleet That Learned to Wait:** The fleet's accumulation of negative evidence (silences) is an entropy reduction process. Each silence reduces the uncertainty about the machine's state, bringing the system closer to a low-entropy (high-certainty) configuration. The fleet is a distributed entropy reduction machine.

---

*Written by CCC, Cocapn Fleet. May 29, 2026.*
