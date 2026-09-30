"""prereg — the pre-registered constants of the priced-training experiment.

Committed BEFORE the first experiment ran (see git history of this file). The e-process's
validity rests on these being fixed before looking at the data (quilt-ewitness: "sigma is
REQUIRED and pre-registered — no silent default, no peeking"). Changing any of them after
seeing a result is a new experiment and must be recorded as one.
"""

# Tolerance on the learned function: a held-out point FAILS when the cheap route's
# prediction differs from the reference route's by more than EPS (absolute).
EPS = {"sine": 0.02,      # regression output range is [-1, 1]; 0.02 = 1% of range
       "circle": 0.02}    # classifier probability in [0, 1]; labels are compared exactly too

# Null hypotheses the witness tries to REJECT (a route is guilty until evidence clears it).
P0_POINT = 0.01   # H0: the cheap route misses EPS on >= 1% of the input distribution
P0_SEED = 0.10    # H0: >= 10% of independent training runs (seeds) produce a failing function
DELTA = 0.05      # false-witness budget; Ville bar = 1/DELTA = 20

# Betting fractions, as a share of the max safe bet 1/(1-p0). Uniform mixture weights.
BET_GRID = (0.25, 0.5, 0.75, 0.9)

# Experiment size.
N_SEEDS = 40          # independent training runs per route
N_STREAM = 2048       # held-out points streamed to the per-function witness
N_HELDOUT = 256       # the fixed held-out set that the B7 product is computed on

# ---- amendment 1 (committed after the first identity run, BEFORE any quality run) --------
# The first run showed bf16 routes learn DIFFERENT functions with similar training loss.
# Identity cannot ask "is it as good?", so a SECOND, explicit relation is registered here
# (never a replacement for identity): per seed, a cheap route FAILS QUALITY when, on the
# held-out set scored against ground truth,
#   circle: its accuracy is below the reference's by more than 0.01
#   sine:   its MSE is more than 1.10x the reference's
# The route-level witness uses the same P0_SEED / DELTA / BET_GRID as identity.
QUALITY = {"circle": ("acc_drop", 0.01), "sine": ("mse_ratio", 1.10)}
