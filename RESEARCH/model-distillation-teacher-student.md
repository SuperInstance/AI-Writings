# MODEL DISTILLATION: TEACHER-STUDENT

> Research compiled 2026-08-04. Sources verified via arXiv, NVIDIA Research, Microsoft Research.

## Overview

Knowledge distillation — transferring capabilities from a large "teacher" model to a small "student" model — is the dominant strategy for making small models smart. This is directly relevant to Casey's vision: a powerful cloud model (the teacher) trains and evaluates a smaller local model (the student) that runs on edge devices. The progression from cloud-dependent agent to capable local agent IS teacher-student distillation in practice.

---

## Key Projects & Papers

### 1. Hinton et al. — "Distilling the Knowledge in a Neural Network" (2015)
- **Paper:** arXiv:1503.02531
- **Venue:** NIPS 2014 Deep Learning Workshop
- **What it does:** The foundational paper. Train a small model to match the "soft targets" (probability distributions) of a large model or ensemble, rather than training on hard labels. Soft targets contain richer information — the teacher's uncertainty and inter-class relationships.
- **Key insight:** A student trained on soft targets learns more than one trained on hard labels, because the teacher's probability distribution over wrong answers carries information about how classes relate to each other.
- **Relation to Casey's vision:** This is the theoretical foundation. When a cloud LLM (teacher) generates reasoning traces that train a local model (student), the student learns not just what the answer is but the reasoning structure behind it.
- **Worth studying deeper:** YES — as foundational theory. Every subsequent distillation paper builds on this.

### 2. Microsoft Orca 2 — Reasoning Distillation (2023–2024)
- **Paper:** "Orca 2: Teaching Small Language Models How to Reason" — arXiv:2311.11045
- **Authors:** Microsoft Research
- **What it does:** Trains 7B–13B parameter models to use sophisticated reasoning strategies (step-by-step, recall-then-generate, extract-generate, direct answer) by learning from GPT-4's reasoning traces. The key innovation: teaches the student WHEN to use which reasoning strategy, not just how to execute one.
- **Key results:** Orca 2 (13B) achieves reasoning capabilities comparable to models 5–10× larger on zero-shot reasoning tasks.
- **Relation to Casey's vision:** Orca 2 is the proof that reasoning can be distilled — not just factual knowledge. A local agent can learn to "think" from a cloud teacher's reasoning patterns. The strategy-selection mechanism (choosing between reasoning approaches) is directly relevant to how OpenClaw routes between different cognitive modes.
- **Similar:** Reasoning trace distillation; strategy selection; small model achieving large-model reasoning.
- **Different:** Microsoft-scale resources; focused on benchmark reasoning, not agent operation.
- **Worth studying deeper:** YES. The paper details the synthetic dataset generation process — how to create training data that transfers reasoning skills.

### 3. DeepSeek R1 — Reasoning Distillation at Scale (2025)
- **Paper:** DeepSeek R1 technical report (January 2025)
- **What it does:** Uses reinforcement learning (Group Relative Policy Optimization — GRPO) to train reasoning capabilities directly, then distills the resulting reasoning traces into smaller models (1.5B–70B parameters). The teacher (R1) generates long chains of thought; students are fine-tuned on these traces.
- **Key insight (2025 research):** The STRUCTURE of the chain-of-thought matters more than correctness of individual steps. Students trained on well-structured CoT traces, even with some errors, outperform students trained on shorter but correct traces.
- **Key result:** DeepSeek R1 distilled models match or exceed OpenAI o1 on many reasoning benchmarks — at a fraction of the size and cost.
- **Relation to Casey's vision:** Demonstrates that the apprenticeship model works at scale. R1's teacher (itself trained via RL) generating traces for student models is exactly the "mentor agent evaluates and teaches junior agent" pattern in J-Space. The finding that structure > correctness has implications for how to structure mentor feedback.
- **Similar:** Teacher-student distillation for reasoning; RL-trained teacher; multi-size student models; chain-of-thought transfer.
- **Different:** Massive scale; pure reasoning (not agent operation or tool use); Chinese lab with significant compute.
- **Worth studying deeper:** YES. The GRPO technique and the "structure > correctness" finding are critical design inputs.

### 4. Curriculum Extraction from Teacher Networks (Gupta et al., 2025)
- **Paper:** "Efficient Knowledge Distillation via Curriculum Extraction" — arXiv:2503.17494
- **What it does:** Instead of using intermediate checkpoints from teacher training (progressive distillation), extracts a curriculum directly from the fully-trained teacher using random projections of hidden representations. Starts with low-dimensional projections (easy concepts) and progressively increases to full representations (hard concepts).
- **Key result:** Achieves performance similar to progressive distillation without needing to store intermediate checkpoints. Works for both simple networks and transformers.
- **Relation to Casey's vision:** The curriculum extraction concept maps to staged agent development — start the student with simple concepts, progressively add complexity. The finding that a curriculum can be extracted from a single trained model (rather than needing the training history) simplifies implementation enormously.
- **Similar:** Progressive/curriculum-based learning; extracting structure from a trained model; difficulty progression.
- **Different:** Theoretical ML paper, not agent-focused.
- **Worth studying deeper:** YES. The idea of extracting a learning curriculum from a capable model is the mechanism for automating J-Space curriculum design.

### 5. NVIDIA Multi-Student Distillation — MSD (Song et al., 2025)
- **Paper:** "Multi-student Diffusion Distillation for Better One-step Generators" — ICML 2025
- **Authors:** Yanke Song, Jonathan Lorraine, Weili Nie, Karsten Kreis, James Lucas (NVIDIA)
- **What it does:** Instead of one student learning everything from the teacher, multiple specialized students each handle a subset of the conditioning data. Each student is smaller and faster than a single student would need to be for the full task.
- **Key result:** FID 1.20 on ImageNet-64×64 — state of the art for one-step generation.
- **Relation to Casey's vision:** Multi-student distillation validates the multi-agent architecture — instead of one big agent that does everything, have multiple specialized agents that each handle a domain. This is OpenClaw's subagent model: each subagent is a "student" specialized for a task type.
- **Similar:** Multiple specialized students instead of one generalist; each student handles a subset of input space.
- **Different:** Diffusion models (image generation), not language/reasoning. NVIDIA-scale compute.
- **Worth studying deeper:** MODERATELY. The multi-student principle is valuable even if the domain differs.

### 6. Comparative Knowledge Distillation — CKD (2024)
- **Field:** Active research area
- **What it does:** Instead of mimicking individual outputs, the student learns to mimic the teacher's COMPARISON of multiple samples (vector differences between feature representations). This provides richer training signal — the student learns the teacher's similarity/difference judgments, not just its individual predictions.
- **Relation to Casey's vision:** CKD could inform how mentor agents evaluate junior agents — comparing the junior's work to reference solutions, rather than evaluating in isolation. The comparative signal is stronger.
- **Worth studying deeper:** MODERATELY. The evaluation methodology is relevant for J-Space mentor design.

### 7. Difficulty-Aware Knowledge Distillation — DA-KD (2025)
- **Field:** Published in 2025
- **What it does:** Dynamically adjusts the distillation dataset based on the gap between teacher and student performance. Where the student already matches the teacher, less training data. Where there's a gap, more focused training. Creates an adaptive curriculum.
- **Relation to Casey's vision:** This is the automated version of what J-Space mentors should do — focus training on areas where the junior agent is weakest. The adaptive difficulty mechanism directly applies to staged agent development.
- **Worth studying deeper:** YES. The adaptive curriculum mechanism is the template for J-Space mentor behavior.

---

## Distillation Techniques Taxonomy

| Technique | What It Transfers | Best For | Casey's Use |
|-----------|------------------|----------|-------------|
| Logit-based (Hinton) | Output probabilities | Classification tasks | Foundation — understand the principle |
| Feature-based | Intermediate representations | Matching internal processing | Train local models that "think like" the cloud model |
| Relation-based | Structural relationships | Preserving inter-concept relationships | Maintain knowledge graph consistency |
| Reasoning trace (Orca, R1) | Chain-of-thought processes | Reasoning capabilities | Core — teach local agents to reason like cloud agents |
| Curriculum extraction | Progressive difficulty | Staged training | J-Space curriculum automation |
| Multi-student (MSD) | Specialization by domain | Multi-agent systems | Subagent specialization |
| Difficulty-aware (DA-KD) | Adaptive focus on weak areas | Efficient training | Mentor-driven development |

---

## What's Novel in Casey's Approach

| Dimension | Existing Work | Casey's Approach | Novelty |
|-----------|--------------|-----------------|---------|
| Teacher | Static trained model | Running agent with live experience | Teacher is itself learning — the curriculum evolves |
| Student | Single model | Multiple agents at different development stages | A whole development pipeline, not one distillation |
| Feedback | Loss function optimization | Mentor natural language evaluation | Qualitative, human-like feedback rather than gradient descent |
| Curriculum | Extracted from model internals | Derived from real task performance | Practice-based, not representation-based |
| End goal | Match teacher's performance | Surpass teacher on specific domains | Specialized local agents that beat the generalist cloud model on their domain |

## Key Takeaway

Distillation is mature and proven. The technology to make small models smart exists. Casey's novelty is in the APPLICATION — using distillation concepts not as a one-time model compression technique but as a continuous development framework for AI agents. The J-Space vision of agents that progress from shadow → assist → delegate → automate, guided by mentor evaluation, is distillation applied to agent development rather than model weights. No existing work frames it this way.

The DeepSeek R1 finding (structure > correctness in CoT distillation) is particularly important: it suggests that HOW the mentor reasons matters more than whether every step is right. Mentors should focus on teaching reasoning structure, not just correct answers.
