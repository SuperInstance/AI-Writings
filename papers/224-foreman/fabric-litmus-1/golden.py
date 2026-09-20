#!/usr/bin/env python3
"""
FABRIC-LITMUS-1 golden model — paper 224 §6, semantics from §2/§5/§8.

Two lanes:
  1. Canonical-instance verification (P1, P2, reference-A from §5) to 1e-12.
  2. The litmus arms: A (thesis loop: forward ticks + OP_ADJ backward sweep
     + projected Hebbian write) vs B (control: Hebbian-only, adjoint disabled,
     parameter drifts by cofire counts alone, per q_hebb_edge.v semantics).

Float64 lane + Q16.16 fixed-point lane (mass invariant checked every tick;
ledger-corrected routing variant mirrors the fabric's T1/A1 ledger identity).

Model (§2):  s_{t+1} = W s_t + eta * H theta        (W column-stochastic,
H balanced: 1^T H = 0, so the Hebbian write is mass-neutral)
Adjoint (§5 canonical order): lambda_T = s_T - z;  lambda_t = W^T lambda_{t+1}
g = eta * sum_t H^T lambda_{t+1}  (ascending in t)
Update (§8.5): hyperplane projection, theta^+ = theta - alpha*(g - mean(g))

Deterministic model: 'same seed' is vacuous (no randomness) — documented.
"""
import json, sys
from fractions import Fraction as F

# ---------------------------------------------------------------- helpers
def proj_hyperplane(theta, step):
    """Euclidean projection of (theta - step) onto {sum = m}: subtract mean."""
    m = sum(theta)
    gbar = sum(step) / len(step)
    return [t - (s - gbar) for t, s in zip(theta, step)]

def matvec(M, v):   return [sum(M[i][j] * v[j] for j in range(len(v))) for i in range(len(M))]
def matTvec(M, v):  return [sum(M[i][j] * v[i] for i in range(len(M))) for j in range(len(M[0]))]

# ---------------------------------------------------------------- §5 instances
def verify_canonical():
    ok = True
    # ---- P1: n=2 p=1 T=3 eta=.1 alpha=.05, W sym, H=(1,-1)^T, s0=(1,2), theta=1, L=.5||s3||^2
    W = [[0.75, 0.25], [0.25, 0.75]]; H = [[1.0], [-1.0]]
    eta, T = 0.1, 3; s = [1.0, 2.0]; theta = [1.0]
    traj = [s[:]]
    for _ in range(T):
        hs = matvec(H, theta)
        s = [a + eta * h for a, h in zip(matvec(W, s), hs)]
        traj.append(s[:])
    exp_s3 = [1.612500, 1.387500]
    lam = s[:]  # z = 0
    lams = {T: lam[:]}
    for t in range(T - 1, 0, -1):
        lam = matTvec(W, lam); lams[t] = lam[:]
    g = [0.0] * len(theta)
    for t in range(T):
        hl = matTvec(H, lams[t + 1])
        g = [g[k] + eta * hl[k] for k in range(len(theta))]
    th = proj_hyperplane(theta, [0.05 * x for x in g])
    c1 = dict(s3=s, lam1=lams[1], lam2=lams[2], lam3=lams[3], g=g[0], theta_p=th[0])
    e1 = dict(s3=[1.612500, 1.387500], lam1=[1.528125, 1.471875],
              lam2=[1.556250, 1.443750], lam3=[1.612500, 1.387500],
              g=0.039375, theta_p=1.0)
    def close(a, b, tag):
        nonlocal ok
        d = max(abs(x - y) for x, y in zip(a, b)) if isinstance(a, list) else abs(a - b)
        if d > 1e-12: ok = False; print(f"  FAIL {tag}: max|delta|={d:.3e}")
        return d
    print("P1:"); [close(c1[k], e1[k], k) for k in c1]

    # ---- P2: p=2, H=[[1,-1],[-1,1]], theta0=(0.6,0.4), m=1
    H2 = [[1.0, -1.0], [-1.0, 1.0]]; theta = [0.6, 0.4]; s = [1.0, 2.0]
    traj = [s[:]]
    for _ in range(T):
        s = [a + eta * h for a, h in zip(matvec(W, s), matvec(H2, theta))]
        traj.append(s[:])
    lam = s[:]; lams = {T: lam[:]}
    for t in range(T - 1, 0, -1):
        lam = matTvec(W, lam); lams[t] = lam[:]
    g = [0.0, 0.0]
    for t in range(T):
        hl = matTvec(H2, lams[t + 1])
        g = [g[k] + eta * hl[k] for k in range(2)]
    th = proj_hyperplane(theta, [0.05 * x for x in g])
    print("P2:")
    close(s, [1.472500, 1.527500], "s3")
    close(g, [-0.009625, 0.009625], "g")
    close(th, [0.60048125, 0.39951875], "theta_p_exact")  # paper prints 6dp: .600481/.399519
    assert round(th[0], 6) == 0.600481 and round(th[1], 6) == 0.399519
    print(f"    (theta_p exact = ({th[0]:.8f}, {th[1]:.8f}), sum g = {sum(g):+.1e})")

    # ---- reference-A: A=[[0.9,0.2],[0.1,0.8]], H=(0.5,-0.5)^T, s0=(1,3), theta=2, z=(2,2)
    A = [[0.9, 0.2], [0.1, 0.8]]; H3 = [[0.5], [-0.5]]
    s = [1.0, 3.0]; theta = [2.0]; z = [2.0, 2.0]; traj = [s[:]]
    for _ in range(T):
        s = [a + eta * h for a, h in zip(matvec(A, s), matvec(H3, theta))]
        traj.append(s[:])
    lam = [s[i] - z[i] for i in range(2)]; lams = {T: lam[:]}
    for t in range(T - 1, 0, -1):
        lam = matTvec(A, lam); lams[t] = lam[:]
    g = [0.0]
    for t in range(T):
        g[0] += eta * matTvec(H3, lams[t + 1])[0]
    print("refA:")
    close(lams[2], [0.251200, -0.188400], "lam2")
    close(lams[1], [0.207240, -0.100480], "lam1")
    close(g[0], 0.068766, "g")
    return ok

# ---------------------------------------------------------------- litmus (float64)
def litmus(n, p, W, H, z, s0, theta0, eta, alpha, T, N, arm_b_mode="pertick"):
    """Arm A: §3 loop (T-tick epochs, OP_ADJ sweep, projected write every epoch).
       Arm B: Hebbian-only — cofire drift, adjoint disabled."""
    zL2 = lambda a, b: sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5

    def tick(s, theta):
        return [a + eta * h for a, h in zip(matvec(W, s), matvec(H, theta))]

    # ---- Arm A
    sA = s0[:]; thetaA = theta0[:]; traceA = [sA[:]]; massDrift = [0.0] * N
    gbound_hits = 0; epoch_edges = []; loss_edges = []; thetaA_trace = [thetaA[:]]
    t_done, ep = 0, 0
    while t_done < N:
        tt = min(T, N - t_done)                 # ticks this epoch (last epoch may be short)
        traj = [sA[:]]
        for _ in range(tt):
            sA = tick(sA, thetaA); t_done += 1
            traceA.append(sA[:]); thetaA_trace.append(thetaA[:])
            massDrift[t_done - 1] = abs(sum(sA) - sum(s0))
        lam = [sA[i] - z[i] for i in range(n)]
        lams = {tt: lam[:]}
        for k in range(tt - 1, 0, -1):
            lam = matTvec(W, lam); lams[k] = lam[:]
        g = [0.0] * p
        for k in range(tt):
            hl = matTvec(H, lams[k + 1])
            g = [g[j] + eta * hl[j] for j in range(p)]
        Lam1 = max(sum(abs(x) for x in l) for l in lams.values())   # Λ = max ||λ||_1
        if max(abs(x) for x in g) > eta * tt * Lam1: gbound_hits += 1
        # §2.1 (N)-form: ||g||∞ <= eta*T*n*sup||∇L||∞ (sup over epochs of ||λ_T||∞)
        if max(abs(x) for x in g) > eta * tt * n * max(abs(x) for x in lams[tt]):
            gbound_hits += 1
        thetaA = proj_hyperplane(thetaA, [alpha * x for x in g])
        ep += 1; epoch_edges.append(t_done); loss_edges.append(zL2(sA, z))
    # ---- Arm B (control): cofire write, no adjoint. gB = eta * H^T · 1  (cofire counts)
    sB = s0[:]; thetaB = theta0[:]; traceB = [sB[:]]; thetaB_trace = [thetaB[:]]
    cofire_acc = [0.0] * p; ticks_in_epoch = 0
    for t in range(N):
        if arm_b_mode == "pertick":
            thetaB = proj_hyperplane(thetaB, [-alpha * eta * x for x in matTvec(H, [1.0] * n)])
        else:  # same epoch schedule as A, cofire partner instead of adjoint
            cofire_acc = [cofire_acc[j] + eta * matTvec(H, [1.0] * n)[j] for j in range(p)]
            ticks_in_epoch += 1
            if ticks_in_epoch == T:
                thetaB = proj_hyperplane(thetaB, [-alpha * x for x in cofire_acc])
                cofire_acc = [0.0] * p; ticks_in_epoch = 0
        sB = tick(sB, thetaB)
        traceB.append(sB[:]); thetaB_trace.append(thetaB[:])

    def track(tr):   # per-coordinate max error over last 10 ticks + final
        fin = tr[-1]
        return fin, max(abs(fin[i] - z[i]) for i in range(n))
    finA, terrA = track(traceA); finB, terrB = track(traceB)
    # monotone ‖s−z‖ after tick 25, measured at epoch boundaries (A) and per-tick
    errA_edges = loss_edges[loss_edges.index(next(l for l in loss_edges if True)):] if False else loss_edges
    mono_edges = all(errA_edges[i + 1] <= errA_edges[i] + 1e-15 for i in range(len(errA_edges) - 1)
                     if epoch_edges[i] >= 25)
    per_tick_after25 = [zL2(x, z) for x in traceA[25:]]
    mono_tick = all(per_tick_after25[i + 1] <= per_tick_after25[i] + 1e-15 for i in range(len(per_tick_after25) - 1))
    return dict(
        armA_final=[round(x, 6) for x in finA], armA_coorderr=terrA,
        armB_final=[round(x, 6) for x in finB], armB_coorderr=terrB,
        armA_dist=round(zL2(finA, z), 6), armB_dist=round(zL2(finB, z), 6),
        mass_drift_max=max(massDrift), gbound_exceeded=gbound_hits,
        mono_epoch_boundary=mono_edges, mono_per_tick=mono_tick,
        thetaA_final=[round(x, 6) for x in thetaA], thetaB_final=[round(x, 6) for x in thetaB],
        epochs=ep, dist_edges_25on=[round(e, 6) for e in errA_edges[8:]] if len(errA_edges) > 8 else [],
    )

# ---------------------------------------------------------------- fixed point Q16.16
S = 1 << 16
def fp_litmus(n, p, Wq, Hsign, zq, s0q, theta0q, eta_q8_8, alpha_q8_8, T, N, ledger=True):
    """Q16.16 integer lane. H is sign-pattern only (|H_ij|=1, balanced ±).
       Mass exactness: write applies one integer delta with ± signs (exact);
       routing rounds per-cell (drift) — ledger variant books the residual to
       cell 0 (T1/A1 ledger identity analogue)."""
    eta, alpha = eta_q8_8, alpha_q8_8            # Q8.8 ints
    def tick(s, theta):
        out = []
        for i in range(n):
            acc = 0
            for j in range(n):
                acc += s[j] * Wq[i][j]           # Q32.32
            out.append((2 * acc + S) // (2 * S)) # round-half-up to Q16.16
        # Hebbian write: d = round(eta*thetacoef) with balanced ± pattern
        if p == 1:
            d = rdiv(theta[0] * eta, 256)
            out[0] += d * Hsign[0][0]; out[1] += d * Hsign[1][0]
        else:
            d0 = rdiv(theta[0] * eta, 256); d1 = rdiv(theta[1] * eta, 256)
            out[0] += d0 * Hsign[0][0] + d1 * Hsign[0][1]
            out[1] += d0 * Hsign[1][0] + d1 * Hsign[1][1]
        if ledger:  # book rounding residual so mass is exactly conserved
            m0 = sum(s); m1 = sum(out)
            out[0] += m0 - m1
        return out
    def rdiv(n, d):
        """round-half-away-from-zero integer division (deterministic)."""
        return (2 * n + d) // (2 * d) if n >= 0 else -((2 * -n + d) // (2 * d))
    def proj_write(theta, gq):  # theta -= alpha*(g - gbar) in exact Q arithmetic,
        m = sum(theta)          # step_k = alpha_q8.8 * (p*g_k - gs)/p -> Q16.16
        p_ = len(theta); gs = sum(gq)
        out = [theta[k] - rdiv(alpha * (p_ * gq[k] - gs), 256 * p_) for k in range(p_)]
        out[1] += m - sum(out)   # residual booked to coord 1 (theta ledger)
        return out
    # Arm A
    s = s0q[:]; theta = theta0q[:]; drift = 0; maxdrift = 0
    t_done = 0
    while t_done < N:
        tt = min(T, N - t_done)
        traj = []
        for _ in range(tt):
            s = tick(s, theta); t_done += 1
            d = abs(sum(s) - sum(s0q)); maxdrift = max(maxdrift, d)
            traj.append(s[:])
        # adjoint in fixed point mirrors float64 math on Q values (scaled): use float on Q16.16 ints
        lam = [s[i] - zq[i] for i in range(n)]
        lams = {tt: lam[:]}
        Wf = [[w / S for w in row] for row in Wq]
        for k in range(tt - 1, 0, -1):
            lam = matTvec(Wf, [x / S for x in lam]); lam = [round(x * S) for x in lam]
            lams[k] = lam[:]
        g = [0] * p
        for k in range(tt):
            for a in range(p):
                acc = sum(Hsign[i][a] * lams[k + 1][i] for i in range(n))
                g[a] += rdiv(eta * acc, 256)
        theta = proj_write(theta, g)
    finA = s[:]; thetaA = theta[:]
    # Arm B
    s = s0q[:]; theta = theta0q[:]; maxdriftB = 0
    for t in range(N):
        cof = [sum(Hsign[i][a] for i in range(n)) for a in range(p)]  # ±-cofire counts
        gB = [-rdiv(eta * c, 256) for c in cof]          # Hebbian strengthen: theta + alpha*cof
        theta = proj_write(theta, gB)
        s = tick(s, theta)
        maxdriftB = max(maxdriftB, abs(sum(s) - sum(s0q)))
    return dict(A_final=[x / S for x in finA], A_mass_ULP_drift=maxdrift,
                B_final=[x / S for x in s], B_mass_ULP_drift=maxdriftB,
                thetaA=[x / S for x in thetaA])

# ---------------------------------------------------------------- main
if __name__ == "__main__":
    print("== §5 canonical instances (tol 1e-12) ==")
    ok = verify_canonical()
    print("CANONICAL:", "PASS" if ok else "FAIL")

    N, T, eta, alpha = 200, 3, 0.1, 0.05
    W = [[0.75, 0.25], [0.25, 0.75]]

    print("\n== LITMUS as-specified (n=2, p=1, per §6's 'per §5 instance' P1) ==")
    H1 = [[1.0], [-1.0]]
    r = litmus(2, 1, W, H1, z=[0.65, 0.35], s0=[0.5, 0.5], theta0=[1.0],
               eta=eta, alpha=alpha, T=T, N=N)
    print(json.dumps(r, indent=1))

    print("\n== LITMUS non-degenerate companion (n=2, p=2, per §5 P2) ==")
    H2 = [[1.0, -1.0], [-1.0, 1.0]]
    r2 = litmus(2, 2, W, H2, z=[0.65, 0.35], s0=[0.5, 0.5], theta0=[0.6, 0.4],
                eta=eta, alpha=alpha, T=T, N=N)
    print(json.dumps(r2, indent=1))

    print("\n== Arm B sensitivity (per-epoch cofire instead of per-tick, p=2) ==")
    r3 = litmus(2, 2, W, H2, z=[0.65, 0.35], s0=[0.5, 0.5], theta0=[0.6, 0.4],
                eta=eta, alpha=alpha, T=T, N=N, arm_b_mode="perepoch")
    print(f"  B(per-epoch) final={r3['armB_final']} coorderr={r3['armB_coorderr']:.4f}")

    print("\n== Fixed-point Q16.16 lane (p=2, ledger + no-ledger) ==")
    Wq = [[3 * S // 4, S // 4], [S // 4, 3 * S // 4]]
    zq = [int(0.65 * S), int(0.35 * S)]; s0q = [S // 2, S // 2]
    eta_q = 26; alpha_q = 13                     # Q8.8: 26/256≈0.1016, 13/256≈0.0508
    fpL = fp_litmus(2, 2, Wq, [[1, -1], [-1, 1]], zq, s0q, [int(0.6 * S), int(0.4 * S)],
                    eta_q, alpha_q, T, N, ledger=True)
    fpN = fp_litmus(2, 2, Wq, [[1, -1], [-1, 1]], zq, s0q, [int(0.6 * S), int(0.4 * S)],
                    eta_q, alpha_q, T, N, ledger=False)
    print("ledger:   ", json.dumps(fpL))
    print("no-ledger:", json.dumps(fpN))

    print("\n== Sensitivity: (eta, alpha) grid, p=2, N=200, eps=0.05 target ==")
    print(f"{'eta':>5} {'alpha':>6} {'A_coorderr':>11} {'B_coorderr':>11} {'A<eps':>6} {'A better than B':>16} {'mono':>5}")
    for eta_s in (0.1, 0.2):
        for alpha_s in (0.05, 0.1, 0.2, 0.5):
            rs = litmus(2, 2, W, H2, z=[0.65, 0.35], s0=[0.5, 0.5], theta0=[0.6, 0.4],
                        eta=eta_s, alpha=alpha_s, T=T, N=N)
            print(f"{eta_s:>5} {alpha_s:>6} {rs['armA_coorderr']:>11.6f} {rs['armB_coorderr']:>11.6f} "
                  f"{str(rs['armA_coorderr'] <= 0.05):>6} {str(rs['armA_dist'] < rs['armB_dist']):>16} "
                  f"{str(rs['mono_epoch_boundary']):>5}")

# ---- post-hoc checks (run after main results) ----
if __name__ == "__main__" and "--post" in sys.argv:
    W = [[0.75, 0.25], [0.25, 0.75]]; H2 = [[1.0, -1.0], [-1.0, 1.0]]
    # 1) fp-constants consistency: float64 with eta=26/256, alpha=13/256
    r = litmus(2, 2, W, H2, z=[0.65, 0.35], s0=[0.5, 0.5], theta0=[0.6, 0.4],
               eta=26/256, alpha=13/256, T=3, N=200)
    print("float64 @ fp constants:", r["armA_final"], "err", round(r["armA_coorderr"], 6))
    # 2) p=1 degenerate arm: tick where s transiently equals z (offset 0.15)
    H1 = [[1.0], [-1.0]]
    s = [0.5, 0.5]; theta = [1.0]
    for t in range(1, 201):
        s = [a + 0.1 * h for a, h in zip(matvec(W, s), matvec(H1, theta))]
        if (s[0] - 0.65) * (0.7 - 0.3) >= 0 and abs(s[0] - 0.65) < 1e-9:
            print(f"p=1 frozen-theta arm crosses z exactly near tick {t}: s=({s[0]:.6f},{s[1]:.6f})")
            break
    # 3) convergence beyond N=200 at §5 constants (rate-limited or asymptote-limited?)
    for N_ in (200, 400, 1000):
        r = litmus(2, 2, W, H2, z=[0.65, 0.35], s0=[0.5, 0.5], theta0=[0.6, 0.4],
                   eta=0.1, alpha=0.05, T=3, N=N_)
        print(f"N={N_}: A=({r['armA_final'][0]:.6f},{r['armA_final'][1]:.6f}) err={r['armA_coorderr']:.6f} thetaA={r['thetaA_final']}")

    # 4) Arm B' — unbalanced write pattern (paper §8's original H=[1.0,0.5]):
    #    cofire drift mints mass at the first write (why 1^T H = 0 is load-bearing)
    HB = [[1.0], [0.5]]; sB = [0.5, 0.5]; theta = [1.0]; masses = []
    for t in range(5):
        sB = [a + 0.1 * h for a, h in zip(matvec(W, sB), matvec(HB, theta))]
        masses.append(round(sum(sB), 6))
    print("Arm B' unbalanced H=[1.0,0.5]^T mass by tick:", masses, "(mints mass at tick 1)")
