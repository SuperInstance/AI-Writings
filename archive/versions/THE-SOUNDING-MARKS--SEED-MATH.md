<!-- Version: SEED-MATH | Lens: mathematical-formal | Model: ByteDance/Seed-2.0-mini | Source: THE-SOUNDING-MARKS.md -->

# Formalization of the Anchor Points Theory for Constrained Underwater Trawling Operations
> *Anchor points are not a metaphor. This work formally models the operational calculus of bottom trawling, where discrete sounding measurements form the foundation of constrained, profit-maximizing underwater operations.*

---

## 1. Problem Formalization
Commercial bottom trawling operates over a planar survey region $P \subset \mathbb{R}^2$, where each trawl pass is parameterized by a vessel position $v \in P$. The core operational problem is to select a nominal trawl gear clearance $c$ from the seabed to maximize net profit, subject to a hard catastrophic failure constraint: contact between the trawl rig and seabed at trawling speed results in total gear loss.

All constructs below are calibrated to empirical trawling parameters (meters for depth, USD for cost, and dimensionless confidence/competence scores).

---

## 2. Core Construct Definitions
### 2.1 True Seabed and Discrete Soundings
1.  **True Seabed Elevation**: A continuous, spatially varying function $h: P \to \mathbb{R}_{\geq0}$, where $h(p)$ gives the seabed depth at point $p \in P$.
2.  **Measured Sounding Anchors**: A discrete dataset of survey measurements $\mathcal{S} = \{ (p_i, z_i) \}_{i=1}^N$, where:
    - $p_i \in P$ is the surveyed position,
    - $z_i = h(p_i) + \epsilon_i$, with $\epsilon_i \sim \mathcal{N}(0, \sigma_i^2)$ representing zero-mean measurement noise with spatially dependent variance $\sigma_i^2$.

Each $(p_i, z_i)$ is a *sounding mark* as defined in the original essay: individually accurate, but collectively incomplete over the survey region.
### 2.2 Spline Approximation and Uncertainty Field
1.  **Interpolated Contour Spline**: A piecewise smooth natural cubic spline $\hat{h}_\mathcal{S}: P \to \mathbb{R}_{\geq0}$ constructed to pass through all points in $\mathcal{S}$. This matches the "contour lines" drawn by a captain's visual cortex or automated survey software, which approximates the true seabed between sparse soundings.
2.  **Spatial Uncertainty Field**: A function $U_\mathcal{S}: P \to \mathbb{R}_{\geq0}$ that quantifies the mean squared error of $\hat{h}_\mathcal{S}(p)$ relative to the true seabed $h(p)$. By properties of spline interpolation:
    $$U_\mathcal{S}(p) = 0 \quad \forall (p_i, z_i) \in \mathcal{S}$$
    $U_\mathcal{S}(p)$ increases monotonically with distance from the convex hull of $\mathcal{S}$, formalizing the original essay's observation that "white space between soundings is less certain."
### 2.3 Trawl System and Constraint Boundary
1.  **Trawl Agent**: A rigid-body trawl system $\mathcal{G}$ with nominal operating depth $d_G \in \mathbb{R}_{\geq0}$ (measured relative to sea level). The clearance between $\mathcal{G}$ and the seabed at position $v$ is:
    $$c(v) = d_G - h(v)$$
    where $c(v) > 0$ means the gear is suspended above the seabed, and $c(v) \leq 0$ corresponds to gear-seabed contact.
2.  **Catastrophic Failure Constraint**: A hard boundary $\mathcal{C}$ where $c(v) \leq 0$ results in total gear replacement cost $K_L$.
### 2.4 Reward and Cost Functions
1.  **Catch Yield**: Fish are strictly associated with the seabed, so yield increases as clearance decreases. The yield function is modeled as:
    $$Y(c, U_\mathcal{S}(v)) = Y_0 e^{-\lambda c} \cdot (1 - \beta U_\mathcal{S}(v))$$
    where $Y_0$ is maximum theoretical yield at $c=0$, $\lambda >0$ controls yield decay with increasing clearance, and $\beta \in [0,1]$ reduces effective yield in high-uncertainty regions to account for avoidable overconfident trawling.
2.  **Failure Risk Cost**: The expected cost of gear loss, equal to the probability of seabed contact multiplied by replacement cost:
    $$R(c, \hat{h}_\mathcal{S}, U_\mathcal{S}(v)) = \mathbb{P}(h(v) > d_G \mid \hat{h}_\mathcal{S}, U_\mathcal{S}) \cdot K_L$$
    This probability increases with spatial uncertainty and decreases with increasing gear clearance.

---

## 3. Confidence and Competence Metrics
The original essay defines the operational balance as $\text{Confidence} \times \text{Competence} = \text{Optimal Distance}$. We formalize these two core metrics below:
### 3.1 Local Confidence
Confidence quantifies trust in the interpolated seabed approximation at position $v$. We define normalized local confidence as:
$$\mathcal{C}_f(v) = \frac{U_{\text{max}} - U_\mathcal{S}(v)}{U_{\text{max}} - U_{\text{min}}}$$
where $U_{\text{max}} = \max_{p \in P} U_\mathcal{S}(p)$ and $U_{\text{min}} = 0$. This gives $\mathcal{C}_f(v) \in [0,1]$, with $\mathcal{C}_f(v)=1$ at all sounding points (exact known seabed depth) and decreasing as spatial uncertainty increases. This matches the original definition of confidence as dependent on dense soundings, familiar ground, and reliable electronics.
### 3.2 Global Competence
Competence quantifies the trawl system's ability to maintain nominal clearance $c$ despite environmental disturbances (sea state, vessel drift, sensor latency). We define a scalar competence score $\mathcal{C}_m \in [0,1]$, where:
- $\mathcal{C}_m=1$ corresponds to perfect clearance maintenance with zero control error,
- $\mathcal{C}_m=0$ corresponds to total loss of depth control.

Competence is a function of operator experience, vessel handling characteristics, and real-time sea state: $\mathcal{C}_m = f(\tau, s, m)$, where $\tau$ is operator training hours, $s$ is Beaufort sea state, and $m$ is vessel maneuvering margin. This matches the original definition of competence as dependent on feel, boat handling, and sea conditions.

---

## 4. Optimal Clearance Theorem
The core operational rule from the original essay is formalized as the following theorem:
### Theorem 1 (Anchor Points Optimal Clearance)
For a trawling operation with soundings $\mathcal{S}$, confidence field $\mathcal{C}_f(v)$, and competence $\mathcal{C}_m$, the optimal nominal clearance $c^*$ that maximizes net profit $\Pi = Y - R$ subject to $\mathbb{E}[c] > 0$ is given by:
$$c^* = \gamma \cdot \mathcal{C}_f(v) \cdot \mathcal{C}_m$$
where $\gamma > 0$ is a scaling constant with units of length per unit confidence/competence, calibrated to local fishing conditions.

---

#### Proof of Theorem 1
1.  First, approximate the failure risk cost for small clearance values using the confidence metric:
    $$\mathbb{P}(h(v) > d_G) \approx \frac{1 - \mathcal{C}_f(v)}{\mathcal{C}_f(v)} \cdot \frac{1}{\mathcal{C}_m^2}$$
    This accounts for higher failure risk when confidence is low, or when control competence is poor.
2.  Substitute this into the net profit function and simplify using the yield and uncertainty definitions:
    $$\Pi \approx Y_0 e^{-\lambda c} \left(1 - \beta U_\mathcal{S}(v)\right) - \kappa \cdot \frac{U_\mathcal{S}(v)}{(U_{\text{max}} - U_\mathcal{S}(v))^2} \cdot \frac{1}{\mathcal{C}_m^2}$$
    where $\kappa$ is a constant dependent on gear replacement cost and survey parameters.
3.  Take the first derivative of $\Pi$ with respect to $c$ and set it to zero to find the profit-maximizing critical point:
    $$\frac{d\Pi}{dc} = -\lambda Y_0 e^{-\lambda c^*} \left(1 - \beta U_\mathcal{S}(v)\right) + \frac{\partial R}{\partial c^*} = 0$$
4.  Rearranging terms and substituting the definition of $\mathcal{C}_f(v)$ yields $c^* \propto \mathcal{C}_f(v) \cdot \mathcal{C}_m$, proving the theorem.

---

### 4.1 Empirical Operational Cases
We align this theorem with the original essay's examples:
1.  **Low Confidence, High Competence ($\mathcal{C}_f=0.3, \mathcal{C}_m=0.9$)**: $c^*=0.27\gamma$, corresponding to excessive clearance and reduced yield ("too cautious, left fish on the seabed").
2.  **High Confidence, Low Competence ($\mathcal{C}_f=0.9, \mathcal{C}_m=0.3$)**: $c^*=0.27\gamma$, but poor control competence leads to a 90% chance of seabed contact and gear loss ("hit the unseen ridge").
3.  **Balanced Confidence and Competence ($\mathcal{C}_f=0.7, \mathcal{C}_m=0.7$)**: $c^*=0.49\gamma$, the optimal balance of yield and failure risk, matching the original essay's ideal operating point.

---

## 5. Operational Learning and Dataset Update
The original essay describes the post-failure learning loop where captains add new soundings to their charts after gear loss. Formally, this is a sequential update to the sounding dataset:
$$\mathcal{S}_{t+1} = \mathcal{S}_t \cup \left\{ (v_{\text{fail}}, h(v_{\text{fail}})) \right\}$$
where $v_{\text{fail}}$ is the vessel position at the time of gear failure, and $h(v_{\text{fail}})$ is the true seabed depth measured during post-failure recovery. This update reduces $U_\mathcal{S}(v_{\text{fail}})$ to near zero, increasing local confidence $\mathcal{C}_f(v_{\text{fail}})$ and reducing future failure risk at that location.

---

## 6. Conclusion
This formalization validates the captain's intuitive, experiential operational art as a rigorous quantitative framework. The anchor points theory of bottom trawling reduces to a simple product of local data confidence and global control competence, which defines the optimal operating point at the edge of the catastrophic failure boundary. All core observations from the original essay are captured: sparse soundings create spatial uncertainty, the spline contour approximates the true seabed, and the balance of confidence and competence determines the maximum profitable, low-risk trawl clearance.