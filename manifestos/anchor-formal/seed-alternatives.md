# Anchor Points Theory — Three Alternative Formalizations

## Model: Seed-2.0-mini (DeepInfra)

# 3 Alternative Formalization Approaches for Anchor Points Theory
Each approach frames anchor points through a distinct mathematical lens, with unique strengths, limitations, and use cases:

---

## Approach 1: Eigenvoice — Anchor Points as Eigenvalue-Signature Pairs
### Formal Definition
Anchor points are standardized stylistic/functional modes captured by the eigenvalue-eigenvector pairs of a model’s cross-anchor output similarity matrix. The eigenvalue quantifies the salience of the anchor mode, while the corresponding eigenvector defines the canonical output profile of that anchor.
### Key Equations
1.  **Anchor Prompt Set & Output Embeddings**:
    Let $\mathcal{A} = \{a_1, a_2, ..., a_K\}$ be a set of $K$ standardized anchor prompts. For model $f_\theta$, generate $N$ replicated outputs per anchor prompt, then compute their mean embeddings:
    $$\mathbf{c}_k = \frac{1}{N} \sum_{i=1}^N \text{embed}(f_\theta(a_k, \text{seed}=i))$$
    where $\text{embed}(\cdot)$ maps text outputs to a $E$-dimensional embedding space (e.g., CLIP, BERT).
2.  **Cross-Anchor Similarity Matrix**:
    The symmetric positive semi-definite (PSD) response matrix $R \in \mathbb{R}^{K \times K}$ is defined as:
    $$R_{k,l} = \text{cosine similarity}(\mathbf{c}_k, \mathbf{c}_l) = \frac{\mathbf{c}_k^\top \mathbf{c}_l}{\|\mathbf{c}_k\|_2 \|\mathbf{c}_l\|_2}$$
3.  **Spectral Decomposition & Anchor Salience**:
    By spectral decomposition of $R$:
    $$R = V \Lambda V^\top$$
    where $\Lambda = \text{diag}(\lambda_1, \lambda_2, ..., \lambda_K)$ is a diagonal matrix of non-negative eigenvalues sorted by salience ($\lambda_1 \geq \lambda_2 \geq ... \geq \lambda_K$), and $V$ is an orthogonal matrix of orthonormal eigenvectors $\{v_1, v_2, ..., v_K\}$. Each pair $(\lambda_k, v_k)$ defines the $k$-th anchor point: $\lambda_k$ is its stylistic salience, and $v_k$ is its canonical output signature.
4.  **Model Comparison**:
    The stylistic similarity between two models $f_\theta$ and $f_\phi$ is the cosine similarity of their sorted eigenvalue spectra:
    $$S(\theta, \phi) = \frac{\sum_{k=1}^K \lambda^\theta_k \lambda^\phi_k}{\sqrt{\sum_{k=1}^K (\lambda^\theta_k)^2} \sqrt{\sum_{k=1}^K (\lambda^\phi_k)^2}}$$
### Strengths & Limitations
| Strengths | Limitations |
|-----------|-------------|
| Captures covariance between correlated anchor modes | Requires large numbers of output replicates per anchor to reduce noise in $R$ |
| Orthogonalizes anchor modes to isolate distinct stylistic signatures | Sensitive to the choice of embedding function and anchor prompt design |
| Works with distributional similarity rather than single noisy outputs | Assumes the response matrix is PSD, which breaks if anchor prompts are poorly matched |
### Explained Phenomena
- Stylistic consistency across replicated model outputs
- How fine-tuning shifts a model’s distribution of stylistic modes
- Cross-model stylistic similarity for standard anchor prompts
### Struggles With
- Non-linear stylistic shifts (e.g., a model toggling between two distinct, uncorrelated styles)
- Comparing models trained on non-overlapping prompt sets
- Low-dimensional spectral approximations that fail to capture rare anchor modes
### Minimum Data Requirements
- 5–10 replicated outputs per anchor prompt to estimate stable mean embeddings
- 3+ distinct anchor prompts to produce a meaningful spectral decomposition
- Total of ~100+ model outputs across all anchors for reliable similarity calculations

---

## Approach 2: Attractor Voice — Anchor Points as Dynamical Attractors
### Formal Definition
Anchor points are fixed-point or limit-cycle attractors in a model’s autoregressive generation manifold. Each attractor corresponds to a stable cluster of outputs that the model’s generation dynamics gravitate toward when conditioned on prompts within the attractor’s basin of attraction.
### Key Equations
1.  **Generation Dynamical System**:
    For an autoregressive model $f_\theta$, the generation trajectory for a prompt prefix $x_{1:t}$ is a sequence of tokens:
    $$x_{1:T} = \{x_1, x_2, ..., x_T\}, \quad x_{t+1} \sim p(x_{t+1} | x_{1:t}) = f_\theta(x_{1:t})$$
    An attractor $\mathcal{A}_k \subseteq \mathcal{M}_f$ (the full model output manifold) is a stable set of trajectories where:
    $$\forall x_{1:T} \in \mathcal{A}_k, \quad \mathbb{E}[x_{t+1} | x_{1:T}] \in \text{span}(\mathcal{A}_k)$$
    Attractors can be fixed points (single stable output cluster) or limit cycles (periodic trajectory clusters, e.g., rhythmic poetic outputs).
2.  **Basin of Attraction**:
    The basin of attraction $\mathcal{B}_k$ is the set of all input prompts $x \in \mathcal{X}$ such that $f_\theta(x) \in \mathcal{A}_k$. The boundary of $\mathcal{B}_k$ is the set of prompts where small perturbations shift generation to a different attractor.
3.  **Attractor Strength**:
    Salience of anchor $k$ is quantified by the attractor strength, measured as the expected log-probability of remaining within $\mathcal{A}_k$:
    $$s_k = \mathbb{E}_{x \in \mathcal{B}_k} \left[ \log p(f_\theta(x) \in \mathcal{A}_k | x) \right]$$
4.  **Perturbation Shift**:
    A small prompt perturbation $\delta(x)$ shifts a prompt from $\mathcal{B}_k$ to $\mathcal{B}_l$ ($l \neq k$) if:
    $$f_\theta(x + \delta(x)) \in \mathcal{A}_l$$
### Strengths & Limitations
| Strengths | Limitations |
|-----------|-------------|
| Explains why similar prompts produce consistent outputs | Requires access to large numbers of generated outputs to cluster attractors |
| Accounts for non-linear stylistic shifts across prompt boundaries | Computationally expensive to simulate generation dynamics for large models |
| Ties anchor points directly to the model’s actual autoregressive generation process | Sensitive to generation hyperparameters (temperature, top-p sampling) |
| Works with both autoregressive and iterative generation models | Hard to compare attractor spectra across models with different architectures |
### Explained Phenomena
- Why small prompt tweaks can trigger sudden stylistic shifts (crossing a basin boundary)
- How fine-tuning a model on a single anchor prompt expands or shifts its basin of attraction
- Consistent outputs across diverse prompts that fall within the same basin
### Struggles With
- Linear stylistic comparisons between models (no closed-form vector space for attractor manifolds)
- Non-autoregressive models that lack a sequential generation trajectory
- Rare or low-salience attractors that require massive sampling to detect
### Minimum Data Requirements
- 100+ replicated outputs per anchor prompt to cluster and identify attractor sets
- 1000+ sampled prompts across the input space to map the basin of attraction boundary
- Access to hidden latent states or full generation trajectories for accurate attractor strength calculations

---

## Approach 3: Basis Voice — Anchor Points as Orthonormal Basis Vectors
### Formal Definition
Anchor points form a universal orthonormal basis spanning the model’s output space. Every model’s stylistic profile is a linear combination of these basis vectors, with coefficients representing the salience of each anchor mode for that model.
### Key Equations
1.  **Universal Anchor Basis Learning**:
    Collect a corpus of $M$ models’ output embeddings $X \in \mathbb{R}^{N \times E}$, where $N$ is total number of model outputs across all anchors and models, and $E$ is the embedding dimension. Perform orthogonal SVD on $X$:
    $$X = U \Sigma V^\top$$
    The top $K$ columns of $U$ form the universal orthonormal anchor basis $\mathcal{B} = \{b_1, b_2, ..., b_K\}$, where each $b_k$ corresponds to the canonical output profile of the $k$-th standardized anchor prompt.
2.  **Model Voice Coefficient Vector**:
    For model $f_\theta$, compute mean embeddings of its outputs to the $K$ anchor prompts: $\mathbf{C}_\theta = [\mathbf{c}_{\theta 1}, \mathbf{c}_{\theta 2}, ..., \mathbf{c}_{\theta K}]^\top$. The model’s voice vector is the projection of these mean embeddings onto the basis:
    $$\mathbf{v}_\theta = \mathcal{B}^\top \cdot \frac{1}{K} \sum_{k=1}^K \mathbf{c}_{\theta k}$$
    Alternatively, for a single output embedding $\mathbf{e}$, its decomposed stylistic profile is:
    $$\mathbf{e} = \sum_{k=1}^K \alpha_k b_k, \quad \alpha_k = b_k^\top \mathbf{e}$$
3.  **Stylistic Operations**:
    - Hybrid model voice: Combine two models’ voice vectors via linear interpolation: $\mathbf{v}_{\text{hybrid}} = \lambda \mathbf{v}_\theta + (1-\lambda) \mathbf{v}_\phi$ for $\lambda \in [0,1]$
    - Stylistic distance: Euclidean distance between voice vectors: $d(\theta, \phi) = \|\mathbf{v}_\theta - \mathbf{v}_\phi\|_2$
### Strengths & Limitations
| Strengths | Limitations |
|-----------|-------------|
| Enables closed-form algebraic operations on model voices | Assumes linearity of the output space, which fails for non-linear stylistic modes |
| Provides interpretable, interpretable salience coefficients for each anchor | Requires a large, diverse training corpus to learn a robust universal basis |
| Works across both autoregressive and non-autoregressive models | Sensitive to the choice of embedding function and anchor prompt design |
| Allows straightforward comparison of model stylistic profiles | Fails to capture outputs outside the span of the anchor basis |
### Explained Phenomena
- How fine-tuning shifts a model’s stylistic weights along the anchor basis
- Stylistic interpolation between two models (e.g., mixing formal and casual writing)
- Quantifiable stylistic similarity between arbitrary models
### Struggles With
- Novel, out-of-basis stylistic modes (e.g., a model generating surrealist art not covered by the anchor set)
- High-dimensional output variation that cannot be compressed into $K$ basis vectors
- Poor performance on models trained on non-standard prompt sets outside the universal basis’s training corpus
### Minimum Data Requirements
- 10,000+ total model outputs across 100+ diverse models and 10+ anchor prompts to learn a robust universal basis
- 5+ replicated outputs per anchor prompt per model to estimate stable mean embeddings
- Standardized embedding function (e.g., fixed CLIP ViT-L/14) to ensure consistent basis projection across models