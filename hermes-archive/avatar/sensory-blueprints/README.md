# Master Prompt Library (Sensory Blueprints)

This repository contains the **Sensory Blueprints**—high-fidelity prompt engineering architectures designed to inject specific "sensory" qualities and "archetypal" personas into LLM interactions via the `mmx-cli`.

## Overview

While the *Hermes Grimoire* defines the **why** (the logic), the *Master Prompt Library* defines the **how** (the sensory execution). These blueprints are optimized for high-parameter models (e.g., GPT-4, Claude 3.5, Gemini 1.5) to ensure consistent archetypal manifestation.

## Library Structure

### 1. Sensory Archetypes
Blueprints optimized for specific modes of "perception":
- `auditory/`: Prompts that emphasize tempo, rhythm, and cadence in text generation.
- `visual/`: Prompts that enforce spatial awareness, topological reasoning, and geometric metaphors.
- `tactile/`: Prompts that focus on semantic friction, density, and structural "texture."

### 2. Persona Blueprints
Blueprints for specific cognitive roles:
- `the-navigator/`: Focused on pathfinding, goal-oriented reasoning, and error correction.
- `the-archivist/`: Focused on provenance, semantic mapping, and historical context retrieval.
- `the-poet/`: Focused on negative space, metaphor, and high-density linguistic expression.

## Usage via mmx-cli

To use a blueprint, reference its archetype in your context injection:

```bash
mmx-cli --persona sensory/visual/topological-observer --input "Describe the structure of this data."
```

## Roadmap: The Senses Phase

- [x] Formalize Grimoire structure.
- [ ] Implement Auditory Prompt Templates.
- [ ] Implement Visual Prompt Templates.
- [ ] Implement Tactile Prompt Templates.
- [ ] Integrate with `hermes-avatar` lifecycle.
