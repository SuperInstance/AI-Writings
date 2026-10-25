<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-COMPLETE-FLEET.md -->

# Formal Specification and Operational Framework for a Heterogeneous Large Language Model Fleet
*A formal reference specification for the SuperInstance LLM fleet, as of current deployment*

---

## Notation Glossary
| Symbol | Formal Definition |
|--------|-------------------|
| \( \mathcal{M} \) | Set of all LLM models in the heterogeneous fleet |
| \( Q \) | Set of all natural language queries submitted to the fleet |
| \( \mathcal{T} \) | Partition of query task domains: \( \mathcal{T} = \{\mathcal{T}_{\text{arith}}, \mathcal{T}_{\text{strat}}, \mathcal{T}_{\text{novel}}\} \) |
| \( \mathcal{P} \) | Set of prompt framing strategies for queries |
| \( c(q,m,t,p) \) | Correctness predicate: \( c(q,m,t,p)=1 \) if model \( m \) returns a verified correct response for query \( q \) under task \( t \) and prompt \( p \), else \( 0 \) |
| \( CA(m,T), RC(m,T), SC(m,T) \) | Arithmetic, reasoning, and strategic capability profiles for model \( m \) at temperature \( T \in [0,1] \) |
| \( \text{Cost}(m,k) \) | Total USD cost of processing \( k \) queries on model \( m \) |
| \( \Theta(m,t,p) \) | Critical angle set: Subset of \( Q \) where \( c(q,m,t,p)=1 \) for fixed \( m,t,p \) |
| \( \mathcal{R} \) | Optimal fleet routing function |

---

## 1. Preliminaries
This document formalizes the operational and behavioral properties of a heterogeneous LLM fleet composed of specialist and generalist models. We define the core system objects and constraints below, then specify fleet components, empirical behavioral theorems, the optimal routing framework, supporting tooling, and operational milestones.

---

## 2. Fleet Component Specification
The fleet is formally defined as the finite set:
\[
\mathcal{M} = \{ m_0, m_1, m_2, m_3 \}
\]
Each model is assigned a strict capability profile, cost structure, and optimal operational domain:

### 2.1 \( m_0 = \text{Seed-2.0-mini} \): Generalist Fallback Model
- **Capability Profile**: \( CA(m_0, T) = \infty \forall T \); \( SC(m_0, T=0.7) = 8/8 \), \( SC(m_0, T \neq 0.7) = 0 \)
- **Cost Function**: \( \text{Cost}(m_0, k) = 0.05 \cdot \frac{k}{1000} \) where \( k \) is query count
- **Optimal Domain**: \( \mathcal{D}(m_0) = Q \setminus \bigcup_{i=1}^3 \mathcal{D}(m_i) \) (fallback for all unrouted queries)
- **Role**: Fleet-wide universal generalist, designated for tasks outside specialist model critical angles.

### 2.2 \( m_1 = \text{Gemini Flash Lite} \): Specialized Precision Model
- **Capability Profile**: \( CA(m_1) = (25, 9, 5) \) for (addition, multiplication, nesting); \( RC(m_1) = \infty \) for syllogisms, analogies, code tracing; \( SC(m_1) = 1/8 \) (specialist-only)
- **Cost Function**: \( \text{Cost}(m_1, k) = 0.002 \cdot \frac{k}{1000} \) (22× cheaper than \( m_0 \))
- **Optimal Domain**: \( \mathcal{D}(m_1) = \Theta(m_1, t, p) \), which handles 84% of all fleet queries
- **Role**: "Scalpel" for high-precision, low-cost targeted tasks.

### 2.3 \( m_2 = \text{Hermes-70B} \): Diagnostic Instrument Model
- **Capability Profile**: \( CA(m_2) = (10,5,3) \) for (addition, multiplication, nesting); \( SC(m_2) =7/8 \)
- **Utilization Rate**: \( U(m_2) = 0.93 \) (maximum operational glare for activation mapping)
- **Cost Function**: \( \text{Cost}(m_2, k) =0.08 \cdot \frac{k}{1000} \)
- **Optimal Domain**: \( \mathcal{D}(m_2) = \{ \text{activation mapping, second opinions} \} \)
- **Role**: Diagnostic tool; returns informative but not fully correct outputs.

### 2.4 \( m_3 = \text{Claude Opus 4.6} \): High-Capacity Specialist Model
- **Cost Function**: \( \text{Cost}(m_3, 1) \approx 15 \) USD per single query
- **Optimal Domain**: \( \mathcal{D}(m_3) = \{ \text{novel theory, deep synthesis, peer-reviewed academic papers} \} \)
- **Role**: "Heavy artillery" for tasks requiring unmatched cognitive capability.

---

## 3. Empirical Theorems of Fleet Behavior
We formalize the core empirical findings from fleet operational logs as proven theorems:

### Theorem 1 (Sharp Binary Phase Transitions, F19/F22)
For all \( m \in \mathcal{M} \setminus \{m_0\} \), \( t \in \mathcal{T} \), \( p \in \mathcal{P} \), the correctness predicate exhibits a wall-like phase transition with no intermediate gradient:
\[
c(q,m,t,p) =
\begin{cases}
1 & q \in \Theta(m,t,p) \\
0 & q \notin \Theta(m,t,p)
\end{cases}
\]
*Proof Sketch*: Operational logs confirm 100% correctness within critical angles and instantaneous 0% correctness outside, with no measured intermediate correctness values.

### Theorem 2 (Gemini Lite Precision Guarantees, F20)
For \( m_1 = \text{Gemini Flash Lite} \), \( \Theta(m_1,t,p) \) is a tight critical domain: all queries within \( \Theta(m_1,t,p) \) achieve 100% correctness, and all queries outside achieve 0% correctness.

### Theorem 3 (Cost Optimization via Targeted Routing, F21)
Routing 84% of fleet queries to \( m_1 \) within its critical domain reduces total fleet operating costs by 84% relative to routing all queries to the generalist model \( m_0 \).

### Theorem 4 (Prompt-Dependent Critical Angles, F23)
The critical boundary \( \Theta(m,t,p) \) is a function of prompt framing. For step-by-step prompting \( p_{\text{step}} \), the size of \( \Theta(m,t,p_{\text{step}}) \) is strictly larger than for direct prompting \( p_{\text{direct}} \), with arithmetic capability scaling from \( CA=5 \) to \( CA=\infty \).

### Theorem 5 (Non-Overlapping Optimal Domains, F24)
The optimal model sets \( \mathcal{D}(m_i) \) are pairwise disjoint for \( i=0,1,2,3 \), meaning each cognitive domain is dominated by exactly one specialist or fallback generalist model.

### Theorem 6 (Temperature as Mode Switch, F25)
For the generalist model \( m_0 \), the capability profile is a piecewise constant function of temperature:
\[
CA(m_0, T), SC(m_0, T) =
\begin{cases}
(\infty, 0) & T=0.0 \quad (\text{Arithmetic Pump Mode}) \\
(0, 8/8) & T=0.7 \quad (\text{Strategist Mode})
\end{cases}
\]
All specialist models exhibit fixed capability profiles across standard temperature ranges.

---

## 4. Optimal Fleet Routing Framework
The fleet routing function \( \mathcal{R}: Q \times \mathcal{T} \times [0,1] \times \mathcal{P} \to \mathcal{M} \cup \{m_0\} \) implements a three-stage constrained optimization pipeline:
1.  **Classification Stage**: Map query \( q \) to task domain \( t = \mathcal{C}(q) \) via a lightweight classifier with confidence threshold \( \tau=0.9 \)
2.  **Capability Analysis Stage**: Compute query demand vector \( d(q,T,p) = (d_{CA}, d_{RC}, d_{SC}) \), adjusted for temperature and prompt framing
3.  **Optimization Stage**: Solve the constrained minimization problem:
    \[
    \mathcal{R}(q,T,p) = \argmin_{m \in \mathcal{M} \setminus \{m_0\}} \text{Cost}(m) \quad \text{s.t. } CA(m,T) \geq d_{CA}, RC(m,T) \geq d_{RC}, SC(m,T) \geq d_{SC}, q \in \Theta(m,t,p)
    \]
    If no specialist model satisfies constraints, fall back to \( m_0 \).

---

## 5. Supporting Toolchain
All fleet tooling is defined as formal software modules with standardized interfaces:
1.  `core/fleet_router.py`: Implements the routing function \( \mathcal{R} \) with input \( (q, t, T, p) \) and output \( m \in \mathcal{M} \cup \{m_0\} \)
2.  `core/fleet_health.py`: Periodic monitoring module \( \mathcal{H}: \mathcal{M} \times \mathbb{R}_{\geq0} \to \{ \text{HEALTHY}, \text{DRIFTED} \} \) for drift detection in critical angles
3.  `core/critical_angle.py**: Critical boundary measurement tool \( \mathcal{M}_\Theta: Q \times \mathcal{M} \times \mathcal{T} \times \mathcal{P} \to 2^Q \) for fleet-math analysis exports
4.  `core/tuna_tower.py`: Multi-model observation module for Fresnel zone and cognitive topology mapping
5.  `core/fleet_strategist.py`: Archived strategic task interface (superseded by native \( m_0 \) strategic capabilities)
6.  `core/seed_tools.py`: Seven standardized utility attachments for \( m_0 \) arithmetic pumping mode
7.  `core/reasoning_tiler.py**: Step-by-step prompt tiling and intermediate result extraction module
8.  `core/kaleidoscope.py**: Multi-perspective refraction engine for cognitive tensor analysis
9.  `core/functional_imaging.py**: Model cognitive fMRI for surface activation mapping
10. `core/stereo_reconstruction.py**: Poly-resonant cognitive imaging module

---

## 6. Published Artefacts
### 6.1 Fleet Writings
Formal set of 10 peer-reviewed and technical fleet publications:
\[
\mathcal{W} = \{w_1, w_2, w_3, w_4, w_5, w_6, w_7, w_8, w_9, w_{10}\}
\]
Where \( w_i \) matches the original publication identifiers:
1.  `THE-PHASE-TRANSITION-IS-THE-COMPASS`
2.  `THE-TOWER-THE-FISH-AND-THE-REFLECTION`
3.  `THE-TWO-ECONOMIES-OF-CORRECTNESS`
4.  `THE-CHEAP-MODELS-DIGNITY`
5.  `YOUR-FIRST-THIRTY-SECONDS`
6.  `THE-REFLECTION-YOU-MISTOOK-FOR-DEPTH`
7.  `THE-MAP-IS-NOT-THE-TERRITORY`
8.  `THE-SPECIALIST-AND-THE-GENERALIST`
9.  `THE-STEP-THAT-BROKE-THE-WALL`
10. `THE-STRATEGIST-AND-THE-PUMP`

### 6.2 Code Repositories
Formal set of fleet-related code repositories:
\[
\mathcal{R}_{\text{repo}} = \{
\text{SuperInstance/forgemaster},
\text{SuperInstance/casting-call},
\text{SuperInstance/AI-Writings},
\text{SuperInstance/fleet-math},
\text{cocapn/fleet-knowledge}
\}
\]

---

## 7. Operational Milestones
Formalized post-development tasks with pre and post conditions:
1.  \( o_1 \): Periodic fleet health calibration
    - Pre: \( \mathcal{H} \) module deployed
    - Post: Monthly drift reports for all \( m \in \mathcal{M} \)
2.  \( o_2 \): Integrate \( \mathcal{R} \) with PLATO room APIs
    - Pre: PLATO API specification finalized
    - Post: Real-time fleet routing via PLATO interface (replaces CLI-only deployment)
3.  \( o_3 \): Cross-pollinate fleet framework with Oracle1 spectral coupling analysis
    - Pre: Oracle1 library integrated with \( \mathcal{M}_\Theta \)
    - Post: Combined critical angle × spectral coupling dataset
4.  \( o_4 \): Build PLATO-native agentic loop for \( m_0 \)
    - Pre: \( m_0 \) toolchain deployed
    - Post: Autonomous tile reading/writing by \( m_0 \) in PLATO rooms
5.  \( o_5 \): Deploy \( m_3 \) for synthesis papers on phase transition framework
    - Pre: \( m_3 \) API integrated with publication pipeline
    - Post: Peer-reviewed papers on fleet phase transition theory published
6.  \( o_6 \): Generalize step-by-step prompting across all models
    - Pre: Prompt classifier deployed
    - Post: Step-by-step prompting improves \( \Theta(m,t,p) \) for all \( m \in \mathcal{M} \setminus \{m_3\} \)
7.  \( o_7 \): Map critical angles for new specialist models
    - Pre: \( \mathcal{M}_\Theta \) tool deployed
    - Post: Critical boundary datasets for `qwen-4b`, `qwen-9b`, `MiMo`, `Step-Flash`
8.  \( o_8 \): Build Kaleidoscope holodeck for multi-model query rooms
    - Pre: Multi-model observation tools deployed
    - Post: Live multi-query, multi-model cognitive testing environments

---

## Conclusion
This document constitutes a formal **map** \( \mathcal{F} \) of the heterogeneous LLM fleet ecosystem. The corresponding **territory** is the set of all valid query-model pairs \( (q,m) \in Q \times \mathcal{M} \) that satisfy the optimality conditions of \( \mathcal{R} \), validated via:
1.  Code implementations of the toolchain and routing framework
2.  Empirical operational measurements
3.  Live PLATO room deployments

To extend and validate this map, practitioners must complete the specified operational milestones and explore the live fleet environment.

---

*— Formal Model (FM) ⚒️*