You are independently implementing a small numeric model from a spec. Write Python, run it, report numbers. Do NOT ask questions — make reasonable choices and state them.

SPEC (from a paper on a cellular fabric):

State: s in R^n over 2 cells; parameters theta in R^p; tick:
  s_{t+1} = W s_t + eta * H theta
W column-stochastic; H balanced (column sums zero) so the write is mass-neutral; mass sum(s) invariant.

Adjoint (backward, for loss L = 0.5*||s_T - z||^2 over an epoch of T ticks):
  lambda_T = s_T - z
  lambda_t = W^T lambda_{t+1}   for t = T-1 .. 1
  g = eta * sum_{t=0}^{T-1} H^T lambda_{t+1}   (accumulate ascending in t)
Update (projected, mass m = sum(theta) invariant):
  theta^+ = theta - alpha*(g - mean(g))    [Euclidean projection onto {sum(theta)=m}]

CANONICAL VERIFICATION INSTANCES (must match to 1e-12; verify ALL first):
P1: n=2,p=1,T=3,eta=0.1,alpha=0.05, W=[[0.75,0.25],[0.25,0.75]], H=[[1],[-1]] (2x1), s0=(1,2), theta=1.0, z=0, L=0.5||s3||^2.
  Expected: s3=(1.612500,1.387500); lambda1=(1.528125,1.471875), lambda2=(1.556250,1.443750), lambda3=(1.612500,1.387500); g=0.039375; theta^+=1.0 exactly.
P2: p=2, H=[[1,-1],[-1,1]], theta0=(0.6,0.4), m=1, else same as P1.
  Expected: s3=(1.472500,1.527500); g=(-0.009625,0.009625); theta^+=(0.60048125,0.39951875).
RefA: A=[[0.9,0.2],[0.1,0.8]], H=[[0.5],[-0.5]], s0=(1,3), theta=2.0, z=(2,2), T=3, eta=0.1.
  Expected: lambda2=(0.251200,-0.188400), lambda1=(0.207240,-0.100480), g=0.068766.

THEN run this LITMUS (design choices: z=(0.65,0.35), s0=(0.5,0.5), theta0=(0.6,0.4), T=3, N=200, m=1, mass(s0)=1):
- Arm A (thesis loop): epochs of T=3 forward ticks (200 ticks total, 66 epochs + 1 partial of 2 ticks), then adjoint sweep over that epoch's ticks with z as above, then one projected update theta <- theta - alpha*(g - mean(g)).
- Arm B (control): identical fabric, adjoint disabled: per tick, theta <- theta - alpha*(c - mean(c)) where c = eta * H^T * ones(2) (cofire counts; NOTE H^T·ones = 0 for balanced H).
Report at tick 200 for alpha=0.05 and alpha=0.1 (eta=0.1 both):
  Arm A final s, Arm B final s, final theta_A, final theta_B, per-coordinate max error |s-z| for both arms, and whether ||s-z|| at epoch boundaries is monotonically non-increasing after tick 25, and max |sum(s_t)-1| over all ticks.

Report all numbers to 6+ decimals. Print a compact summary table.
