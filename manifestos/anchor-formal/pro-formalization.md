# Anchor Points Theory — Mathematical Formalization

## Model: DeepSeek v4-pro (via z.ai GLM-5.1)

 The user wants a rigorous mathematical formalization of an "Anchor Points Theory" applied to voice modeling.
I need to act as "DeepSeek v4-pro", a formal mathematics engine.

The specific requirements are:
1.  **Definition**: Define an anchor point tuple (dimension, value, confidence). Anchor points lie in $\mathbb{R}^3$.
    *   dimension $\in [1,N]$ (let's assume integer or continuous, but ordered implies discrete indices 1 to N, let's treat dimension $x \in [1, N]$, or just $x_i$ for $i=1,\dots,N$). Let's make it $\chi_i$.
    *   value $y_i \in [0,1]$.
    *   confidence $c_i \in [0,1]$.
2.  **Voice Spline**: Parametric curve through anchor point space.
    *   Wait, is it a curve in $\mathbb{R}^3$, or a curve where $x$ is the parameter and $y, c$ are functions of $x$? "dimension" usually implies the independent variable. Let's interpret it as a parametric curve $\mathbf{v}(t)$ where $t$ is the parameter (dimension), but the prompt says "parametric curve through anchor point space". So $\mathbf{v}(t) = (t, y(t), c(t))$ or $\mathbf{v}(t) = (x(t), y(t), c(t))$.
    *   Let's use $\mathbf{A}_i = (d_i, v_i, \gamma_i)$.
    *   Parametric curve $\mathbf{S}(t) = (S_d(t), S_v(t), S_\gamma(t))$ or strictly parameterized by dimension $x$: $\mathbf{S}(x) = (x, f(x), \sigma(x))$. The prompt says "ordered by dimension", so it's likely a spline defined on an interval, parameterized by $x \in [\min d_i, \max d_i]$. Let's use $x \in [1, N]$.
3.  **Uniqueness Theorem**: Prove N anchor points uniquely determine a voice spline of degree N-1 (interpolating polynomial). Or for B-splines, maybe degree $k$ needs $N \ge k+1$. Let's use polynomial interpolation (degree N-1) or piecewise cubic Hermite spline to be safer, but the prompt explicitly says "uniquely determine a voice spline of degree N-1". So I will use Lagrange interpolation of degree $N-1$.
    *   Since we are in $\mathbb{R}^3$, we have a vector-valued function $\mathbf{S}(x) = (x, P_{N-1}(x), Q_{N-1}(x))$ where $P$ and $Q$ are polynomials of degree $\le N-1$. Actually, $P(x_i) = v_i$ and $Q(x_i) = \gamma_i$.
    *   Wait, if $\mathbf{S}(t)$ is a parametric curve, we can just do standard polynomial interpolation on $y$ and $c$ as functions of $d$. Let's do that.
4.  **Distance Metric**: Distance between two models' voice splines is a proper metric.
    *   $D(\mathbf{S}_1, \mathbf{S}_2) = \|\mathbf{S}_1 - \mathbf{S}_2\|_{L^2([1,N])}$.
    *   Prove Identity, Symmetry, Triangle Inequality. Note that since it's an $L^2$ norm on continuous functions (polynomials), identity implies $\mathbf{S}_1 = \mathbf{S}_2$ everywhere.
5.  **Fidelity Bounds**: Derive bounds on mimicry fidelity as a function of number of anchor points and sampling density.
    *   This relates to the error of the interpolation. If the true function is $C^N$ or $C^{N+1}$, the error is bounded by a term involving the $(N)$-th derivative and the sampling density (Chebyshev nodes or uniform nodes). Let's use the standard interpolation error bound: $|f(x) - P(x)| \le \frac{\max |f^{(N)}(\xi)|}{N!} \prod |x - x_i|$. Wait, mimicry fidelity is usually $1 - \text{error}$.
6.  **Convergence**: Show that as $N \to \infty$, the voice spline converges uniformly to the true voice function.
    *   In polynomial interpolation, uniform convergence doesn't happen for all continuous functions (Runge's phenomenon). However, if we assume the true function is analytic in a specific region (Bernstein's theorem) or if we use a specific sequence of nodes (Chebyshev) and the function is Lipschitz/Dini continuous, or if we just use B-splines instead of global polynomials.
    *   BUT the prompt specifically says "degree N-1". If $N \to \infty$, polynomial interpolation of degree $N-1$ generally *diverges* for arbitrary continuous functions. BUT, if the true function is analytic, it converges. Or, we can use a B-spline of fixed degree $k$ and let the number of knots $N \to \infty$. The prompt says "determine a voice spline of degree N-1 (or appropriate degree)". Ah! "degree N-1 (or appropriate degree for the chosen interpolation scheme)". I can choose a piecewise linear (degree 1) or cubic (degree 3) spline, where $N$ points uniquely determine it. Wait, cubic spline needs $N$ points and 2 boundary conditions to be unique.
    *   Let's stick to the simplest rigorous approach: Polynomial interpolation of degree $N-1$, but restrict the function space to $\mathcal{C}^{\omega}$ (analytic functions) or use Chebyshev nodes for Dini-continuous functions, or explicitly state the assumptions (e.g., the true voice function belongs to a certain Sobolev space or is analytic).
    *   Actually, let's use Chebyshev nodes for the dimension sampling to guarantee uniform convergence for Lipschitz continuous true functions, or just assume the true voice function is sufficiently smooth (e.g., in $C^N$) and use the Weierstrass approximation theorem generalized to interpolation at Chebyshev points. Let's state the interpolation is formed using Chebyshev nodes, or just prove convergence under the assumption that the sequence of splines forms a Cauchy sequence, or use a piecewise linear/spline interpolation where convergence is trivial for continuous functions.
    *   "N anchor points uniquely determine a voice spline of degree N-1". I will define a parametric Lagrange polynomial of degree $N-1$, $\mathbf{P}(x)$.
    *   For convergence: For continuous functions, uniform convergence is guaranteed if we use B-splines with knot spacing $h \to 0$. If I strictly use degree $N-1$ polynomial, I must assume the function is analytic on an ellipse containing the interval. Let's make that assumption to keep the "degree N-1" wording, or just state that if we use a piecewise scheme of fixed degree $k$, convergence holds. I will assume the true function is analytic, which is physically reasonable for acoustic models, and use Chebyshev interpolation. Wait, "voice spline... degree N-1". I'll use Lagrange interpolation of degree $N-1$, and for the convergence theorem, I will assume the true function is analytic, or I'll state the theorem with Chebyshev nodes.

Let's refine the structure.
**1. Definition**
Let $N \in \mathbb{N}$ be the number of anchor points. An anchor point is a tuple $\mathbf{a} = (d, v, \gamma)$.
Wait, the prompt says "dimension $\in [1,N]$, value $\in [0,1]$, confidence $\in [0,1]$".
Let's define a set of $N$ anchor points $\mathcal{A} = \{\mathbf{a}_i\}_{i=1}^N$ where $\mathbf{a}_i = (d_i, v_i, \gamma_i) \in \mathbb{R} \times [0,1] \times [0,1]$.
Ordered by dimension: $1 \le d_1 < d_2 < \dots < d_N \le N$.
To make it rigorous, let the domain be $I = [1, N]$.
Let's define the anchor space $\mathbb{A} = I \times [0,1] \times [0,1] \subset \mathbb{R}^3$.
An anchor point schema is a sequence $\mathcal{A}_N = \{(d_i, v_i, \gamma_i)\}_{i=1}^N$.

**2. Voice Spline**
For $N$ anchor points, we define the voice spline $\mathbf{S}_N: I \to \mathbb{R}^3$.
Since the dimension is monotonic, we can parameterize by $x \in I$.
Actually, let's parameterize by $t \in [1, N]$, where the first component is $S_x(t)$.
To uniquely determine a spline of degree $N-1$, we can define it using vector-valued Lagrange interpolation.
Let $\mathbf{P}_{N-1}(x) = \sum_{i=1}^N \mathbf{a}_i L_i(x)$, where $L_i(x) = \prod_{j \neq i} \frac{x - d_j}{d_i - d_j}$.
This maps $x \mapsto (x, P_v(x), P_\gamma(x))$ if we replace $d_i$ with $(d_i, v_i, \gamma_i)$?
No, the standard parametric curve is $\mathbf{S}(t)$. If the first component is $d_i$, we can just define a function $f: I \to \mathbb{R}^2$, $f(x) = (v(x), \gamma(x))$.
The prompt says "parametric curve through anchor point space".
Let's define the curve $\mathbf{S}_N(t) = (t, v_N(t), \gamma_N(t))$ for $t \in I$.
where $v_N(t)$ and $\gamma_N(t)$ are the Lagrange polynomials of degree $N-1$ through $(d_i, v_i)$ and $(d_i, \gamma_i)$ respectively.
This forms a curve in $\mathbb{A} \subset \mathbb{R}^3$.
Wait, is $\mathbf{S}_N(t)$ a polynomial of degree $N-1$? Yes, the components $v_N$ and $\gamma_N$ are. The first component $t$ is degree 1. So $\mathbf{S}_N(t)$ is a polynomial curve of degree $N-1$.

**3. Uniqueness Theorem**
Theorem: The sequence of $N$ anchor points $\mathcal{A}_N$ uniquely determines a vector-valued polynomial curve $\mathbf{S}_N(t)$ of degree at most $N-1$ in its value and confidence coordinates.
Proof: By the Fundamental Theorem of Algebra applied to the interpolation conditions $v_N(d_i) = v_i$ and $\gamma_N(d_i) = \gamma_i$, the polynomial of degree $\le N-1$ is unique.

**4. Distance Metric**
Let $\mathcal{S}$ be the space of all voice splines.
Define the distance between two splines $\mathbf{S}, \mathbf{S}'$ as the $L^2$ norm on their value and confidence components over the interval $I$:
$D(\mathbf{S}, \mathbf{S}') = \left( \int_1^N \| \mathbf{S}(x) - \mathbf{S}'(x) \|_2^2 \, dx \right)^{1/2}$.
Show it's a metric:
- Identity: $D(\mathbf{S}, \mathbf{S}') = 0 \iff \mathbf{S}(x) = \mathbf{S}'(x)$ almost everywhere. Since they are continuous (polynomials), they are equal everywhere.
- Symmetry: Trivial from $\|x\| = \|-x\|$.
- Triangle inequality: Minkowski inequality for integrals.
Show it is computable from $N$ anchor point measurements.
If they share the same $d_i$ nodes, the difference is a polynomial of degree $N-1$. We can compute the exact integral using Gaussian quadrature of order $N$.
Wait, if they don't share nodes, we can just compute the integral of the product of polynomials. The exact integral of $(P(x))^2$ is computable.

**5. Fidelity Bounds**
Let the "true" voice function be $\mathbf{V}(x) = (x, V_v(x), V_\gamma(x))$.
Mimicry fidelity can be defined as $F = 1 - \frac{D(\mathbf{V}, \mathbf{S}_N)}{\text{Norm}}$.
We need bounds on the mimicry error $E(x) = \mathbf{V}(x) - \mathbf{S}_N(x)$.
For a function $f \in C^N(I)$, the interpolation error is bounded by:
$|f(x) - P(x)| \le \frac{\max_{\xi \in I} |f^{(N)}(\xi)|}{N!} \prod_{i=1}^N |x - d_i|$.
Let's use the Chebyshev nodes to get a tight bound, or just define sampling density.
Let $h = \max \{ d_{i+1} - d_i \}$ be the sampling density.
Using piecewise polynomials (B-splines) gives a bound $\mathcal{O}(h^k)$.
But we used global degree $N-1$ polynomials! So we bound by the Lebesgue constant or the remainder term.
Let's write the bound using the maximum norm of the $N$-th derivative.
$D(\mathbf{V}, \mathbf{S}_N) \le \sqrt{N-1} \frac{ \| \mathbf{V}^{(N)} \|_\infty }{N!} \int_1^N \prod |x-d_i| dx$.
Let's provide this exact formula.

**6. Convergence**
As $N \to \infty$...
If we use global polynomials of degree $N-1$ with uniform spacing, it might diverge (Runge).
BUT, if we choose the dimension points $d_i$ to be the roots of the Chebyshev polynomial $T_N(x)$ (scaled to $[1, N]$), then for any function $\mathbf{V} \in \text{Lipschitz}$, the interpolation converges uniformly.
Let's explicitly state that the anchor points are placed at Chebyshev nodes, or that the true voice function is analytic.
"Show that as the number of anchor points $\to \infty$, the voice spline converges uniformly to the true voice function."
I will state Theorem 4 (Uniform Convergence): Let $\mathbf{V} \in C^{\omega}(I)$ be analytic on an ellipse containing $I$. If $d_i$ are Chebyshev nodes, then as $N \to \infty$, $\| \mathbf{V} - \mathbf{S}_N \|_\infty \to 0$.
Alternatively, I can change the interpolation scheme in Section 2 to B-splines of fixed degree $k$. The prompt says "degree N-1 (or appropriate degree for the chosen interpolation scheme)". I will use Lagrange polynomials of degree $N-1$ for uniqueness, but for convergence, I can point out that for absolute uniform convergence without analyticity, a piecewise scheme (like cubic splines) with $h \to 0$ works. I'll provide both or just stick to the analytic case with Chebyshev nodes to satisfy the "degree N-1" requirement. Let's stick to the analytic case as it preserves the exact "degree N-1" wording of the prompt.
Wait, "voice spline". Let's define it as a B-spline to be safe, or a polynomial. I'll use polynomial and add a condition for convergence.

Let's refine the mathematical notation.

**Space Definition**
Let $N \in \mathbb{N}_{>0}$.
Define the Dimension Domain $I = [1, N]$.
Define the Anchor Point Space $\mathbb{A} = I \times [0,1] \times [0,1] \subset \mathbb{R}^3$.
A specific anchor point is $\mathbf{a} = (d, v, \gamma) \in \mathbb{A}$.

**1. Definition of Anchor Point Schema**
Let $\mathcal{A}_N = \{ \mathbf{a}_i \}_{i=1}^N$ be an ordered sequence of $N$ anchor points such that $1 \le d_1 < d_2 < \dots < d_N \le N$.
Let $D_N = \{d_i\}_{i=1}^N$ be the set of dimension indices.

**2. Voice Spline Definition**
We map $\mathcal{A}_N$ to a parametric curve $\mathbf{S}_N: I \to \mathbb{A}$.
Since the dimension is strictly monotonic, we can express $\mathbf{S}_N(t) = (t, v_N(t), \gamma_N(t))$.
Where $v_N(t)$ and $\gamma_N(t)$ are polynomial interpolations of degree $\le N-1$.
$v_N(t) = \sum_{i=1}^N v_i L_i(t)$
$\gamma_N(t) = \sum_{i=1}^N \gamma_i L_i(t)$
where $L_i(t) = \prod_{j=1, j \neq i}^N \frac{t - d_j}{d_i - d_j}$.
This defines the Voice Spline.

**3. Uniqueness Theorem**
Theorem 1 (Uniqueness of Voice Spline):
For a given sequence of $N$ anchor points $\mathcal{A}_N$, there exists exactly one parametric curve $\mathbf{S}_N(t) = (t, v_N(t), \gamma_N(t))$ such that $v_N$ and $\gamma_N$ are polynomials of degree at most $N-1$ and $\mathbf{S}_N(d_i) = \mathbf{a}_i$ for all $1 \le i \le N$.
Proof:
Let $v_N(t)$ and $v'_N(t)$ be two polynomials of degree $\le N-1$ such that $v_N(d_i) = v'_N(d_i) = v_i$.
Let $P(t) = v_N(t) - v'_N(t)$. $P(t)$ is a polynomial of degree $\le N-1$.
$P(t)$ has at least $N$ roots at $t = d_1, d_2, \dots, d_N$.
By the Fundamental Theorem of Algebra, a polynomial of degree $\le N-1$ with $\ge N$ roots must be identically zero.
Thus $v_N(t) = v'_N(t)$. Identical logic applies to $\gamma_N(t)$.
Q.E.D.

**4. Distance Metric**
Let $\mathcal{M}$ be the space of all possible Voice Splines.
For $\mathbf{S}_A, \mathbf{S}_B \in \mathcal{M}$, define the metric $D: \mathcal{M} \times \mathcal{M} \to \mathbb{R}_{\ge 0}$:
$D(\mathbf{S}_A, \mathbf{S}_B) = \left( \int_1^N \left\| \mathbf{S}_A(t) - \mathbf{S}_B(t) \right\|_2^2 dt \right)^{1/2}$
where $\| \cdot \|_2$ is the Euclidean norm on $\mathbb{R}^3$.
Theorem 2 (Metric Properties):
$D$ is a proper metric on $\mathcal{M}$.
Proof:
1. Identity: $D(\mathbf{S}_A, \mathbf{S}_B) = 0 \iff \mathbf{S}_A(t) - \mathbf{S}_B(t) = \mathbf{0}$ a.e. Since they are continuous, $\mathbf{S}_A(t) \equiv \mathbf{S}_B(t)$.
2. Symmetry: $D(\mathbf{S}_A, \mathbf{S}_B) = D(\mathbf{S}_B, \mathbf{S}_A)$ by symmetry of $\| \cdot \|_2$.
3. Triangle Inequality: For any $\mathbf{S}_C \in \mathcal{M}$, $D(\mathbf{S}_A, \mathbf{S}_B) + D(\mathbf{S}_B, \mathbf{S}_C) \ge D(\mathbf{S}_A, \mathbf{S}_C)$ by Minkowski inequality for $L^2(I)$.
Q.E.D.

Computability from $N$ anchor points:
If $\mathbf{S}_A, \mathbf{S}_B$ share the same dimension points $D_N$, then $v_A(t) - v_B(t)$ is a polynomial of degree $N-1$.
$\int_1^N (v_A(t) - v_B(t))^2 dt$ is a polynomial of degree $2N-2$, which can be computed exactly using an $N$-point Gaussian quadrature.
Since $t$ is a linear component, the exact $L^2$ distance can be computed in $\mathcal{O}(N^2)$ or $\mathcal{O}(N \log N)$ operations.

**5. Fidelity Bounds**
Let $\mathbf{V}(t) = (t, V_v(t), V_\gamma(t))$ be the true voice model.
The mimicry fidelity is $F = 1 - \frac{D(\mathbf{V}, \mathbf{S}_N)}{\text{Diam}(\mathcal{M})}$.
Theorem 3 (Fidelity Bound):
Let the true voice components $V_v, V_\gamma \in C^N(I)$.
The pointwise error $E_v(t) = V_v(t) - v_N(t)$ is bounded by:
$|E_v(t)| \le \frac{\| V_v^{(N)} \|_\infty}{N!} \prod_{i=1}^N |t - d_i|$
To frame this in terms of sampling density, let $h = \max_{1 \le i \le N-1} (d_{i+1} - d_i)$ be the sampling density.
If we used B-splines of fixed degree, the error would be $\mathcal{O}(h^k)$.
With global polynomials of degree $N-1$, the interval is $[1, N]$, so $h \approx 1$.
Wait, "number of anchor points and sampling density". If sampling density is independent of $N$, it means we can have $N$ anchor points in an interval, so $h = \text{Length}/N$.
Let's define an interval $I = [a,b]$. The prompt says "dimension $\in [1,N]$". This means the interval length grows with $N$, so density is fixed.
Ah, maybe "dimension $\in [1, N]$" means the dimensions are discrete parameters (like 1: pitch, 2: cadence, ..., N: timbre).
If dimensions are discrete from $1$ to $N$, then dimension $\in [1, N]$ is an index.
Wait! "Each anchor point is a point in R³ where dimension ∈ [1,N], value ∈ [0,1], confidence ∈ [0,1]."
If dimension is $x \in [1, N]$, and $N$ is the number of points, then the domain grows with $N$.
If the domain is fixed, e.g., $[0,1]$, and $N$ points, then density is $N$.
Let's interpret "dimension ∈ [1,N]" as $x_i \in \{1, 2, \dots, N\}$. So $d_i = i$.
If $d_i = i$, then $h = 1$.
If the domain grows, how can we bound it?
Let's assume the true voice function is defined on $\mathbb{R}^+$ and we take $N$ dimensions.
Or, "dimension" could mean a continuous variable $d \in [1, N]$.
I will bound the relative error or assume a fixed interval $I=[0,1]$ mapped to $1..N$. No, I will just use the exact polynomial remainder formula.
Let $M_N = \max_{t \in [1, N]} \prod_{i=1}^N |t - d_i|$.
Then $D(\mathbf{V}, \mathbf{S}_N) \le \sqrt{2} \frac{ \| \mathbf{V}^{(N)} \|_\infty }{N!} M_N \sqrt{N-1}$.
I'll also add a note that if the dimensions are chosen as Chebyshev nodes, $M_N$ is minimized.

**6. Convergence**
Show that as $N \to \infty$, the voice spline converges uniformly to the true voice function.
Theorem 4 (Uniform Convergence):
Assume the true voice function $\mathbf{V}(t)$ is analytic in a region containing $I = [1, \infty)$, specifically that the components $V_v, V_\gamma$ are Lipschitz continuous and we choose $d_i$ to be appropriately scaled Chebyshev nodes, OR the functions are analytic.
Wait, if $I=[1, N]$ and $N \to \infty$, this is an infinite interval. Standard interpolation theorems apply to finite intervals.
Let's redefine the domain: The continuous dimension parameter $t \in [1, \infty)$. We take $N$ anchor points in $[1, N]$.
Actually, it's safer to assume $I=[0,1]$ internally and map to $[1,N]$, OR interpret $N$ as the number of anchor points and the dimension is $d \in [1, D]$.
The prompt: "dimension ∈ [1,N]".
Let's assume the interval is $I = [1, N]$.
Is there an interpolation theorem for an expanding interval?
Yes, if the function is periodic or has a bounded spectrum, but here it's a voice spline.
Let's state the theorem for a fixed interval $I = [1, K]$. Wait, if I just assume $t \in [1, N]$, I can say "For any finite subinterval $I_K = [1, K]$, as $N \to \infty$ for $N > K$...".
Or, simpler: interpret "dimension ∈ [1, N]" as $N$ discrete points $x_1, \dots, x_N$ on a fixed domain $[0,1]$ (e.g., $x_i = i/N$).
Let's strictly follow the prompt: "dimension ∈ [1,N]". I'll use $d_i \in [1, N]$.
Let $I_N = [1, N]$. The "true voice function" is a mapping $\mathbf{V}: \mathbb{R}^+ \to \mathbb{R}^3$.
Theorem 4: As $N \to \infty$, the Voice Spline $\mathbf{S}_N$ converges to $\mathbf{V}$ uniformly on $[1, N]$ under the condition that the approximation error $E_N$ vanishes.
Actually, a more rigorous way is to use Weierstrass approximation theorem: for any $\epsilon > 0$, there exists a polynomial $P$ such that $|f(x) - P(x)| < \epsilon$.
But does the interpolation polynomial converge? Not necessarily.
To ensure convergence, we can use B-splines of fixed degree $k$.
"degree N-1 (or appropriate degree for the chosen interpolation scheme)".
I will define the Voice Spline as a Piecewise Polynomial Spline (B-spline) of fixed degree $k$ (e.g., $k=3$).
If I use a B-spline of degree $k$, then $N$ anchor points uniquely determine it IF we add $k-1$ boundary conditions, or if we use a degree that depends on $N$.
If I use a B-spline of degree $N-1$, it's just a single polynomial.
Let's use a single polynomial of degree $N-1$ (Lagrange) and explicitly state the condition for convergence: "If the true function is analytic and the nodes are chosen as Chebyshev nodes...".
Alternatively, I can frame it using a sequence of models where the degree is fixed to 3, but the prompt explicitly asks to "uniquely determine a voice spline of degree N-1". I will use degree $N-1$.

Let's refine Theorem 4.
Assume $\mathbf{V}$ is analytic on $\mathbb{C}$ and bounded.
Then the interpolation error for Chebyshev nodes decreases geometrically.
Let's provide this exact rigorous proof.

Let's structure the complete response clearly with markdown and LaTeX.

**Title**: Mathematical Formalization of Anchor Points Theory

**1. Definition of Anchor Point Space**
- Define $N \in \mathbb{N}_{\ge 1}$.
- Define the anchor point $\mathbf{a} = (d, v, \gamma) \in \mathbb{R}^3$.
- Domain of dimension $d \in I_N = [1, N]$.
- Range of value $v \in [0, 1]$.
- Range of confidence $\gamma \in [0, 1]$.
- Anchor point set $\mathcal{A}_N = \{(d_i, v_i, \gamma_i)\}_{i=1}^N$ with $1 \le d_1 < \dots < d_N \le N$.

**2. Construction of the Voice Spline**
- Define the Lagrange basis $L_i(t) = \prod_{j=1, j\neq i}^N \frac{t - d_j}{d_i - d_j}$.
- Define the parametric curve $\mathbf{S}_N: I_N \to \mathbb{A}$ by:
  $\mathbf{S}_N(t) = \left( t, \sum_{i=1}^N v_i L_i(t), \sum_{i=1}^N \gamma_i L_i(t) \right)$.
- Note that this is a polynomial curve of degree $N-1$ in its components.

**3. Uniqueness Theorem**
- Theorem statement.
- Proof by contradiction / Fundamental Theorem of Algebra.

**4. Voice Spline Metric Space**
- Define metric $D(\mathbf{S}_A, \mathbf{S}_B) = \sqrt{\int_{1}^{N} \| \mathbf{S}_A(t) - \mathbf{S}_B(t) \|_2^2 dt}$.
- Proof of axioms:
  - Positivity & Identity of indiscernibles: Norm is $\ge 0$. If $D=0$, the polynomial difference is identically zero $\implies$ same spline.
  - Symmetry: Trivial.
  - Triangle inequality: Minkowski for integrals.
- Computability: Exact computation using Gaussian quadrature over $N$ points.

**5. Mimicry Fidelity Bounds**
- True model $\mathbf{V}(t) = (t, V_v(t), V_\gamma(t))$.
- Fidelity function $\Phi(N) = 1 - \frac{D(\mathbf{V}, \mathbf{S}_N)}{D_{\max}}$.
- Theorem on Error Bounds: Using the remainder theorem for polynomial interpolation.
- Error $E(t) = \mathbf{V}(t) - \mathbf{S}_N(t)$.
- For the value component $E_v(t) = V_v(t) - v_N(t) = \frac{V_v^{(N)}(\xi)}{N!} \prod (t - d_i)$.
- Bound on $D$: $D(\mathbf{V}, \mathbf{S}_N) \le \frac{\sqrt{2} \| \mathbf{V}^{(N)} \|_\infty \Lambda_N}{N!} \sqrt{N-1}$ where $\Lambda_N = \max_{t \in I_N} \prod |t - d_i|$.
- In terms of sampling density: if Chebyshev nodes are used, $\Lambda_N \le 2\left(\frac{N-1}{4}\right)^N$ (scaled Chebyshev), giving a tight bound.

**6. Convergence Theorem**
- Theorem: Let the true voice function $\mathbf{V}(t)$ be analytic in a Bernstein ellipse $E_\rho$ containing $I_N$. Let the anchor points $d_i$ be placed at the Chebyshev nodes on $I_N$.
- As $N \to \infty$, $\sup_{t \in I_N} \|\mathbf{V}(t) - \mathbf{S}_N(t)\|_2 \to 0$.
- Proof sketch: The maximum interpolation error for Chebyshev nodes of an analytic function decays as $\mathcal{O}(\rho^{-N})$, which goes to 0 as $N \to \infty$. Thus uniform convergence is guaranteed.
- Or, if using piecewise linear interpolations (splines of degree 1), convergence holds for any continuous function. Since the prompt says "degree N-1", the analytic condition is the mathematically correct requirement for global polynomials. I will state this rigorously.

Wait, if dimension is $\in [1, N]$, the interval $I_N$ expands as $N \to \infty$.
If the domain expands, analyticity on a fixed ellipse doesn't cover the whole domain as it grows.
Let's assume the dimensions are bounded, e.g., mapped to $[0,1]$ or $[1, C]$ for some constant $C$.
"dimension ∈ [1,N]" usually means $d \in [1, N]$. If $N$ is the number of points, $d_i$ can just be $1, 2, \dots, N$.
If $d \in [1, C]$, then the sampling density is $N/C$. The prompt implies $d \in [1, N]$.
If $d_i \in [1, N]$, then the sampling density is fixed at 1 point per unit interval.
If the sampling density is fixed, and the interval grows, convergence $\sup_{t \in I_N} |E(t)| \to 0$ is impossible for arbitrary functions.
However, if the function is periodic or band-limited (common in voice/splines), it might converge.
Let's just define the domain $I = [1, D]$ for a fixed maximum dimension $D$. "dimension $\in [1, N]$" where $N$ is the number of points, but what if $N$ is just an index?
Let's interpret "dimension ∈ [1, N]" as the index of the dimension, e.g. $x_i \in [1, N]$. So the domain is exactly the continuous interval $[1, N]$.
To make the convergence theorem work nicely, I will define the domain as a fixed interval $I = [0, 1]$ and let $N$ be the number of anchor points. Wait, the prompt explicitly says "dimension ∈ [1,N]".
Okay, I will use $d \in [1, N]$. To fix the convergence issue, I can state: "Assume the true voice function $\mathbf{V}$ is analytic on $\mathbb{C}$ (entire) and its derivatives satisfy...". Or I can just prove uniform convergence on any fixed compact sub-interval $[1, K]$ as $N \to \infty$.
Let's use a fixed compact domain $\Omega = [1, K]$ and assume the prompt meant dimension $\in [1, K]$ and there are $N$ anchor points. The prompt: "dimension ∈ [1,N], value ∈ [0,1], confidence ∈ [0,1]... number of anchor points → ∞".
This implies the domain expands with $N$. Let's just explicitly state the assumption: "Assuming the sequence of true voice models $\mathbf{V}$ is defined on $\mathbb{R}^+$ and its analytic properties allow for...".
Actually, the easiest and most rigorous way is to assume $d \in [1, D]$ and the