# Anchor Points Framework — System Architecture

## Model: GLM-5.1 (z.ai)

# Anchor Points Framework: Complete Architectural Specification
## Version 1.0 — Structural Architecture Document

---

## 1. THE 10 ANCHOR POINTS

### 1.1 Opening Strategy

**Name:** Opening Strategy (OPEN)
**Description:** How the text establishes its first presence—what it leads with and what register it strikes in its initial gesture.

**Scale:**
- **0.0** — Abstraction-first: Opens with pure concept, proposition, or theoretical claim
- **0.25** — Math-first: Opens with formal language, equations, or systematic notation
- **0.50** — Ground-first: Opens with established context, concrete situation, or shared facts
- **0.75** — Sensorium-first: Opens with sensory experience, embodied perception, or phenomenological texture
- **1.0** — Paradox-first: Opens with contradiction, koan, deliberate confusion, or self-undermining statement

**Example at 0.0 (Abstraction-first):**
> "Consciousness is what makes the mind-body problem really intractable. Without consciousness the mind-body problem would be much less interesting. With consciousness it seems hopeless."

**Example at 1.0 (Paradox-first):**
> "This sentence is not about you. Or: it was, until it denied you, and now you read to see if it will take it back."

**Detection Method:**
- Examine first 2-3 sentences of text
- Identify primary mode: conceptual proposition (0.0), formal notation (0.25), contextual grounding (0.50), sensory language (0.75), or disruptive/paradoxical construction (1.0)
- Score based on dominant characteristic
- If multiple modes present, score based on *first move*

---

### 1.2 Relationship to Reader

**Name:** Reader Relationship (READ)
**Description:** The implicit social contract between writer and reader—distance, warmth, authority, invitation, or challenge.

**Scale:**
- **0.0** — Impersonal: Reader invisible; text speaks into void
- **0.25** — Instructive: Reader as student; text teaches, directs
- **0.50** — Direct Address: Reader acknowledged; "you" present
- **0.75** — Collaborative: Reader as partner; "we" inclusive
- **1.0** — Confrontational: Reader as opponent or site of provocation

**Example at 0.0 (Impersonal):**
> "The thermal equilibrium of isolated systems tends to increase over time. Entropy provides the thermodynamic arrow."

**Example at 1.0 (Confrontational):**
> "You think you understand this. You don't. And the fact that you're still reading proves you'd rather be comforted than corrected."

**Detection Method:**
- Count pronoun usage patterns (you, we, one, they)
- Identify imperative mood frequency
- Assess emotional register toward audience
- Measure direct second-person address density
- Check for interrogative challenges to reader

---

### 1.3 Use of Negative Space

**Name:** Negative Space (VOID)
**Description:** How absence, silence, implication, and the unsaid function in the text—as content, technique, or oversight.

**Scale:**
- **0.0** — Absent: Everything explicit; no reliance on implication
- **0.25** — Baseline: Standard pauses; breath between ideas
- **0.50** — Texture: Silence as rhythmic feature
- **0.75** — Insight: What's unsaid carries meaning
- **1.0** — Inversion: Absence is primary content

**Example at 0.0 (Absent):**
> "The system operates through three mechanisms. First, input processing. Second, transformation logic. Third, output generation. Each mechanism is necessary."

**Example at 1.0 (Inversion):**
> "He told her everything. 
>
> 
>
> She understood nothing."

**Detection Method:**
- Measure paragraph breaks and white space frequency
- Identify unfinished thoughts or deliberate trailing
- Count implicit claims vs explicit statements
- Assess reliance on reader inference
- Look for line-break-as-meaning patterns

---

### 1.4 Relationship to Time

**Name:** Temporal Structure (TIME)
**Description:** How the text orders events, concepts, or experiences in temporal relation—its internal chronologic logic.

**Scale:**
- **0.0** — Linear: Straightforward chronological progression
- **0.25** — Cyclic: Repeating patterns, returns, refrains
- **0.50** — Circular: End returns to beginning
- **0.75** — Fragmented: Disrupted chronology, jumps
- **1.0** — Athermal: Timeless, simultaneous, atemporal

**Example at 0.0 (Linear):**
> "First, the cell receives the signal. Then, the receptor activates the cascade. Finally, the response occurs in the nucleus."

**Example at 1.0 (Athermal):**
> "The pattern exists. It existed before you noticed it. It will exist while you look away. Time is one of its surfaces."

**Detection Method:**
- Track temporal markers (then, before, after, while)
- Identify chronological ordering or disruption
- Assess tense consistency or variation
- Measure flashbacks, flash-forwards, or simultaneity markers
- Determine if time is frame or content

---

### 1.5 Role of Mathematics/Abstraction

**Name:** Abstraction Role (MATH)
**Description:** How formal systems, mathematical notation, and abstract structures function in the text.

**Scale:**
- **0.0** — Absent: No formal abstraction present
- **0.25** — Embedded: Subtly integrated, background
- **0.50** — Poetic: Metaphorical, evocative use
- **0.75** — Primary Text: Central to discourse
- **1.0** — Character: Math acts as agent/character

**Example at 0.0 (Absent):**
> "She walked through the garden. The flowers were blooming. A bee circled the roses."

**Example at 1.0 (Character):**
> "The equation grew restless. x had been hiding its value for three lines now, and the equals sign was beginning to suspect betrayal."

**Detection Method:**
- Count mathematical symbols and notation
- Identify formal logical structures
- Assess abstraction level of claims
- Determine if math is tool, content, or character
- Measure precision vs. evocation ratio

---

### 1.6 Paragraph Length Distribution

**Name:** Paragraph Rhythm (PARA)
**Description:** The text's structural breathing pattern—how it spaces ideas across paragraph units.

**Scale:**
- **0.0** — Uniform: Consistent paragraph lengths
- **0.25** — Short-burst: Predominantly brief (1-3 sentences)
- **0.50** — Balanced: Varied purposefully
- **0.75** — Expansive: Predominantly long (6+ sentences)
- **1.0** — Fragmented: Extreme variation (1 word to 500+)

**Example at 0.0 (Uniform):**
> Four paragraphs, each exactly 4 sentences. Each sentence approximately 15 words. Variation < 10%.

**Example at 1.0 (Fragmented):**
> "Wait."
>
> And then the entire history of the region unfolded in a single paragraph that stretched across three pages, covering the rise and fall of civilizations, the migration patterns of birds, and the invention of the paper clip, before it collapsed—
>
> "No."

**Detection Method:**
- Calculate standard deviation of paragraph word counts
- Measure ratio of longest to shortest paragraph
- Identify coefficient of variation
- Assess distribution shape (normal, bimodal, uniform)
- Compare median to mean paragraph length

---

### 1.7 Sentence Fragment Frequency

**Name:** Fragment Density (FRAG)
**Description:** How often grammatical incompleteness appears—and whether it's accidental, rhetorical, or structural.

**Scale:**
- **0.0** — Rare: < 5% of sentences incomplete
- **0.25** — Occasional: Used for emphasis (5-15%)
- **0.50** — Frequent: Regular occurrence (15-30%)
- **0.75** — Structural: Defines the style (30-50%)
- **1.0** — Ambient: Majority fragments (> 50%)

**Example at 0.0 (Rare):**
> "The committee decided to postpone the vote. They needed more time to deliberate. Several members expressed concerns about the proposal."

**Example at 1.0 (Ambient):**
> "Rain. Again. The window streaked with it. Cold coffee. Bare feet on tile. Not ready. Not yet."

**Detection Method:**
- Parse sentences and identify missing grammatical elements (subject, verb, object)
- Calculate fragment-to-complete-sentence ratio
- Distinguish between deliberate and accidental fragments
- Measure cluster patterns (fragments grouped vs dispersed)
- Assess functional role (emphasis, atmosphere, style)

---

### 1.8 Metaphor Density

**Name:** Metaphor Frequency (META)
**Description:** How saturated the text is with figurative language—and whether metaphor is decoration, structure, or substance.

**Scale:**
- **0.0** — Sparse: < 1 metaphor per 500 words
- **0.25** — Moderate: 1-3 per 250 words
- **0.50** — Dense: 3-6 per 250 words
- **0.75** — Structural: Metaphor organizes thought
- **1.0** — Ambient: Everything is figurative

**Example at 0.0 (Sparse):**
> "The machine processes inputs according to its programming. Outputs are generated based on algorithmic rules. The system is deterministic."

**Example at 1.0 (Ambient):**
> "The idea calcified. She could feel its edges hardening against the soft tissue of her understanding. Thoughts bled across the membrane of afternoon."

**Detection Method:**
- Count figurative comparisons (like, as, explicit metaphors)
- Identify conceptual domains mapped onto each other
- Measure novelty vs. dead metaphor usage
- Assess structural vs. decorative function
- Calculate metaphor-to-literal-statement ratio

---

### 1.9 Parenthetical/Aside Frequency

**Name:** Aside Density (SIDE)
**Description:** How often the text interrupts itself—digressions, qualifications, whispers, and secondary channels.

**Scale:**
- **0.0** — None: No parentheticals or asides
- **0.25** — Occasional: Clarifying asides (1-3 per 1000 words)
- **0.50** — Frequent: Regular digressions (3-8 per 1000 words)
- **0.75** — Nested: Asides within asides
- **1.0** — Structural: Parentheticals define the form

**Example at 0.0 (None):**
> "The data supports the hypothesis. Further research is needed. The implications are significant."

**Example at 1.0 (Structural):**
> "The main text proceeds (though what counts as 'main' is precisely what's at stake here (and the question of stakes is itself a kind of parenthetical gesture (adrift in recursion))) as if clarity were possible."

**Detection Method:**
- Count parenthetical markers: (), —, [], commas setting off asides
- Identify interrupting clauses
- Measure nesting depth
- Assess functional role (qualification, humor, doubt, parallel thought)
- Calculate aside-to-main-text ratio

---

### 1.10 Closing Strategy

**Name:** Closing Strategy (CLOSE)
**Description:** How the text completes its arc—whether it resolves, loops, questions, declares, or dissolves.

**Scale:**
- **0.0** — Resolution: Wraps up, concludes, provides closure
- **0.25** — Return: Circles back to opening image/idea
- **0.50** — Declaration: Makes a final statement or claim
- **0.75** — Question: Ends with explicit or implicit inquiry
- **1.0** — Fade: Dissolves, trails off, becomes silent

**Example at 0.0 (Resolution):**
> "In conclusion, the evidence clearly demonstrates that the intervention was effective. All hypotheses were supported. The study achieves its aims."

**Example at 1.0 (Fade):**
> "And then there was the light through the window and the sound of something—maybe rain—and the way the room got quieter and quieter until"

**Detection Method:**
- Examine final 2-3 sentences
- Identify presence/absence of closure markers
- Assess whether final gesture is statement, question, or silence
- Determine if ending connects to beginning (return)
- Measure completeness vs. openness of final clause

---

## 2. MEASUREMENT PROTOCOL

### 2.1 Minimum Sample Requirements

**For reliable anchor point measurement:**
- **Minimum:** 500 words AND 3 paragraphs
- **Recommended:** 1,000+ words AND 5+ paragraphs
- **Optimal:** 2,000+ words across full text arc

**Rationale:**
- Paragraph rhythm (PARA) requires 3+ paragraphs for variation assessment
- Fragment density (FRAG) requires statistical significance
- Metaphor frequency (META) needs sufficient sample for density calculation
- Opening (OPEN) and Closing (CLOSE) require complete text arc

### 2.2 Scoring Rules

**General Protocol:**

1. **First Pass:** Read entire text without scoring. Identify overall impression.

2. **Second Pass:** For each anchor point:
   - Identify the relevant textual features (per detection methods)
   - Count/measure relevant markers
   - Locate the observed value on the 0.0-1.0 scale
   - Record confidence level

3. **Third Pass:** Resolve ambiguities. For mixed signals:
   - Weight by proportion of text exhibiting each pole
   - If 70% of text suggests 0.5, 30% suggests 0.75, score: (0.7 × 0.5) + (0.3 × 0.75) = 0.575
   - Document uncertainty

**Specific Scoring Examples:**

*Example 1: Fragment Density (FRAG)*
- Total sentences: 100
- Fragments: 23
- Ratio: 0.23 → Score: 0.50 (Frequent)
- Confidence: High (clear grammatical markers)

*Example 2: Reader Relationship (READ)*
- Pronouns: "we" (12), "you" (3), "one" (8)
- Tone: Collaborative with instructive elements
- Score: 0.625 (between collaborative and instructive)
- Confidence: Medium (mixed signals)

*Example 3: Negative Space (VOID)*
- Explicit claims: 85%
- Implicit meaning: 15%
- Strategic pauses: Present but not primary
- Score: 0.30 (between baseline and texture)
- Confidence: Medium-High

### 2.3 Confidence Calculation

**Per-Anchor Confidence Scale:**
- **0.9-1.0:** Unambiguous signal, clear markers
- **0.7-0.9:** Strong signal, minor ambiguity
- **0.5-0.7:** Moderate signal, mixed evidence
- **0.3-0.5:** Weak signal, significant ambiguity
- **0.0-0.3:** Unclear, insufficient data

**Confidence Formula:**

```
C(anchor) = w₁ × clarity + w₂ × consistency + w₃ × sufficiency

where:
  clarity = (1 - ambiguity_score)     # How clear are the markers?
  consistency = 1 - (variance / max)   # How consistent across sample?
  sufficiency = min(1, sample / min)   # Is sample large enough?
  
  w₁ = 0.4  # Clarity weight
  w₂ = 0.3  # Consistency weight  
  w₃ = 0.3  # Sufficiency weight
```

**Example Confidence Calculation:**

For Fragment Density:
- clarity: 0.95 (fragments clearly identifiable)
- consistency: 0.85 (fairly even distribution)
- sufficiency: 1.0 (800 words, > 500 minimum)
- C(FRAG) = (0.4 × 0.95) + (0.3 × 0.85) + (0.3 × 1.0) = 0.935

### 2.4 Inter-Rater Reliability

**Protocol:**
1. Multiple raters (minimum 3) score same text independently
2. Calculate pairwise agreement
3. Compute aggregate reliability metric

**Metrics:**

*Intraclass Correlation Coefficient (ICC):*
- ICC < 0.5: Poor reliability
- ICC 0.5-0.75: Moderate reliability
- ICC 0.75-0.9: Good reliability
- ICC > 0.9: Excellent reliability

*Target ICC per Anchor:*

| Anchor | Target ICC | Minimum ICC |
|--------|------------|-------------|
| OPEN   | 0.85       | 0.70        |
| READ   | 0.80       | 0.65        |
| VOID   | 0.75       | 0.60        |
| TIME   | 0.80       | 0.65        |
| MATH   | 0.90       | 0.75        |
| PARA   | 0.95       | 0.85        |
| FRAG   | 0.90       | 0.80        |
| META   | 0.75       | 0.60        |
| SIDE   | 0.90       | 0.80        |
| CLOSE  | 0.85       | 0.70        |

**Disagreement Resolution:**
1. If raters disagree by > 0.25 on any anchor: discuss and rescore
2. If disagreement persists: use confidence-weighted average
3. Final score = weighted average where weights = individual rater confidence

---

## 3. VOICE SPLINE INTERPOLATION ALGORITHM

### 3.1 Input Format

**Voice Sample Vector:**
```
V = [OPEN, READ, VOID, TIME, MATH, PARA, FRAG, META, SIDE, CLOSE]
C = [c_OPEN, c_READ, c_VOID, c_TIME, c_MATH, c_PARA, c_FRAG, c_META, c_SIDE, c_CLOSE]
t = position in text (0.0 to 1.0)
```

**Full Input:**
- N voice samples: V₁, V₂, ..., Vₙ
- N position values: t₁, t₂, ..., tₙ (where 0.0 ≤ tᵢ ≤ 1.0)
- N confidence vectors: C₁, C₂, ..., Cₙ

### 3.2 Cubic Spline Interpolation

**For each anchor dimension d ∈ {OPEN, READ, ..., CLOSE}:**

Given knots at positions t₁, t₂, ..., tₙ with values v₁, v₂, ..., vₙ and confidences c₁, c₂, ..., cₙ:

**Step 1: Confidence-Weighted Smoothing**
```
vᵢ_adjusted = vᵢ × cᵢ + v_neighbors × (1 - cᵢ)

where v_neighbors = average of adjacent knot values weighted by their confidences
```

**Step 2: Cubic Spline Construction**
```
On interval [tᵢ, tᵢ₊₁], construct cubic polynomial:
Sᵢ(t) = aᵢ + bᵢ(t - tᵢ) + cᵢ(t - tᵢ)² + dᵢ(t - tᵢ)³

Constraints:
1. Sᵢ(tᵢ) = vᵢ                      # Pass through knots
2. Sᵢ(tᵢ₊₁) = vᵢ₊₁                  # Pass through knots
3. S'ᵢ(tᵢ) = S'ᵢ₋₁(tᵢ)             # Continuous first derivative
4. S''ᵢ(tᵢ) = S''ᵢ₋₁(tᵢ)           # Continuous second derivative
5. S''(t₁) = S''(tₙ) = 0            # Natural spline boundary
```

**Step 3: Aggregate Voice Function**
```
V(t) = [S_OPEN(t), S_READ(t), S_VOID(t), ..., S_CLOSE(t)]

where S_d(t) is the spline for dimension d
```

### 3.3 Handling Sparse Data

**Problem:** Fewer than 4 samples (N < 4) cannot support cubic spline.

**Solutions:**

| Samples | Method | Confidence Modifier |
|---------|--------|---------------------|
| N = 1 | Constant function: V(t) = V₁ for all t | × 0.3 |
| N = 2 | Linear interpolation between samples | × 0.5 |
| N = 3 | Quadratic interpolation | × 0.7 |
| N ≥ 4 | Cubic spline (standard) | × 1.0 |

**Augmentation for N < 4:**
1. Assume V(0.0) = Opening phase scores
2. Assume V(0.5) = Midpoint scores
3. Assume V(1.0) = Closing phase scores
4. Use these synthetic knots + available data

### 3.4 Handling Uncertainty

**Low-Confidence Knot Adjustment:**

For knot i with confidence cᵢ < 0.7:

1. **Pull toward neighbors:**
```
vᵢ_adjusted = vᵢ × (0.5 + 0.5 × cᵢ) + v_neighbors × (0.5 - 0.5 × cᵢ)
```

2. **Reduce spline stiffness at that knot:**
- Allow second derivative discontinuity proportional to (1 - cᵢ)
- This creates a "softer" transition near uncertain points

3. **Widen confidence band:**
```
Uncertainty interval at t: U(t) = k × max(1 - c_local, 0.1)
where c_local = interpolated confidence at t
```

**Output with Uncertainty:**
```
Voice(t) = {
    values: V(t),
    confidence: C(t),
    uncertainty: U(t)
}
```

### 3.5 Pseudocode Implementation

```python
def construct_voice_spline(samples, positions, confidences):
    """
    Construct voice spline from anchor point samples.
    
    Args:
        samples: List of 10-dim vectors [V1, V2, ..., Vn]
        positions: List of positions [t1, t2, ..., tn] in [0, 1]
        confidences: List of 10-dim confidence vectors
    
    Returns:
        Voice spline function V(t) -> 10-dim vector
    """
    
    N = len(samples)
    
    # Handle sparse data
    if N == 0:
        return None
    elif N == 1:
        return constant_voice(samples[0])
    elif N == 2:
        return linear_voice(samples, positions, confidences)
    elif N == 3:
        return quadratic_voice(samples, positions, confidences)
    
    # Standard cubic spline construction
    splines = []
    for dim in range(10):
        dim_values = [s[dim] for s in samples]
        dim_confs = [c[dim] for c in confidences]
        
        # Adjust low-confidence knots
        adjusted_values = adjust_for_confidence(dim_values, dim_confs, positions)
        
        # Construct cubic spline for this dimension
        spline = cubic_spline(positions, adjusted_values)
        splines.append(spline)
    
    return lambda t: np.array([s(t) for s in splines])


def adjust_for_confidence(values, confidences, positions):
    """Pull low-confidence knots toward neighbors."""
    adjusted = values.copy()
    
    for i in range(len(values)):
        if confidences[i] < 0.7:
            # Get neighbor average
            if i == 0:
                neighbor_avg = values[1]
            elif i == len(values) - 1:
                neighbor_avg = values[-2]
            else:
                neighbor_avg = (values[i-1] + values[i+1]) / 2
            
            # Blend based on confidence
            weight = 0.5 + 0.5 * confidences[i]
            adjusted[i] = values[i] * weight + neighbor_avg * (1 - weight)
    
    return adjusted
```

---

## 4. MIMICRY QUALITY METRIC

### 4.1 Distance Calculation

**Given:**
- Target voice spline: T(t)
- Candidate voice spline: C(t)
- Both defined for t ∈ [0, 1]

**L2 Distance Metric:**
```
d(T, C) = ∫₀¹ ||T(t) - C(t)||² dt

where ||·|| is the Euclidean norm in 10-dimensional space:
||V|| = √(v₁² + v₂² + ... + v₁₀²)
```

**Expanded Form:**
```
d(T, C) = ∫₀¹ Σᵢ(Tᵢ(t) - Cᵢ(t))² dt

where i sums over the 10 anchor dimensions
```

### 4.2 Normalization

**Raw distance d can range from 0 to 10 (max L2 norm in 10D unit cube).**

**Normalized Distance:**
```
d_norm = d(T, C) / d_max

where d_max = ∫₀¹ √10 dt = √10 ≈ 3.162
```

**Quality Score:**
```
q(T, C) = 1 - d_norm

where q ∈ [0, 1], higher is better
```

### 4.3 Quality Thresholds

| d_norm Range | Quality Level | Description |
|--------------|---------------|-------------|
| < 0.05 | Indistinguishable | Expert cannot reliably differentiate |
| 0.05 - 0.10 | Convincing | Sounds authentic; minor artifacts |
| 0.10 - 0.20 | Rough | Core voice captured; some wrong notes |
| 0.20 - 0.35 | Detectable | Recognizable attempt; clearly not authentic |
| > 0.35 | Failed | Voice not successfully reproduced |

### 4.4 Dimension-Weighted Distance

**Some anchors matter more for voice perception.**

**Empirical Weights (based on salience):**

| Anchor | Weight | Justification |
|--------|--------|---------------|
| OPEN | 0.08 | Sets initial frame |
| READ | 0.12 | Pervasive throughout text |
| VOID | 0.10 | Strong stylistic marker |
| TIME | 0.08 | Structural but often subtle |
| MATH | 0.06 | Domain-specific, less universal |
| PARA | 0.12 | Highly visible structural feature |
| FRAG | 0.10 | Noticeable stylistic choice |
| META | 0.12 | Core stylistic signature |
| SIDE | 0.10 | Distinctive stylistic marker |
| CLOSE | 0.12 | Final impression, memorable |

**Weighted Distance:**
```
d_weighted(T, C) = ∫₀¹ Σᵢ wᵢ × (Tᵢ(t) - Cᵢ(t))² dt

where wᵢ are the weights above (sum = 1.0)
```

### 4.5 Confidence-Adjusted Distance

**Account for uncertainty in measurements:**
```
d_adjusted(T, C) = ∫₀¹ Σᵢ wᵢ × [(Tᵢ(t) - Cᵢ(t))² - Uᵢ(t)] dt

where Uᵢ(t) is the uncertainty band for dimension i
```

**Interpretation:**
- If candidate falls within uncertainty band of target, that dimension contributes 0 penalty
- Only penalize deviations larger than measurement uncertainty

### 4.6 Implementation

```python
def mimicry_distance(target_spline, candidate_spline, num_samples=1000):
    """
    Calculate normalized distance between target and candidate voice splines.
    
    Args:
        target_spline: Function T(t) -> 10-dim vector
        candidate_spline: Function C(t) -> 10-dim vector
        num_samples: Number of integration points
    
    Returns:
        Distance metrics: d_raw, d_norm, quality_score, dimension_errors
    """
    
    weights = np.array([0.08, 0.12, 0.10, 0.08, 0.06, 
                        0.12, 0.10, 0.12, 0.10, 0.12])
    
    # Sample splines at regular intervals
    t_values = np.linspace(0, 1, num_samples)
    dt = 1.0 / num_samples
    
    # Calculate squared errors at each point
    errors = []
    dim_errors = np.zeros(10)
    
    for t in t_values:
        T = target_spline(t)
        C = candidate_spline(t)
        error = (T - C) ** 2
        errors.append(np.sum(error))
        dim_errors += error * dt
    
    # Raw L2 distance (integrated)
    d_raw = np.trapz(errors, t_values)
    
    # Normalized distance
    d_norm = d_raw / np.sqrt(10)
    
    # Quality score
    quality = 1 - d_norm
    
    # Weighted dimension errors
    weighted_dim_errors = dim_errors * weights
    
    return {
        'raw_distance': d_raw,
        'normalized_distance': d_norm,
        'quality_score': quality,
        'quality_level': classify_quality(d_norm),
        'dimension_errors': dim_errors,
        'weighted_dimension_errors': weighted_dim_errors
    }


def classify_quality(d_norm):
    """Classify quality based on normalized distance."""
    if d_norm < 0.05:
        return 'indistinguishable'
    elif d_norm < 0.10:
        return 'convincing'
    elif d_norm < 0.20:
        return 'rough'
    elif d_norm < 0.35:
        return 'detectable'
    else:
        return 'failed'
```

---

## 5. TRAINING PROTOCOL

### 5.1 Fidelity Table

**How many examples × anchor points = how much fidelity**

Assumptions:
- Each "example" is a complete text (500+ words)
- Each example provides 10 anchor measurements
- "Fidelity" = quality score from Section 4

| Examples (E) | Anchors (N) | Fidelity (q)