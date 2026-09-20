# Predictive Sonar Engine: Mathematical Drivers

## Objective
Finalize the mathematical implementation of the 'Intensity Derivative' and 'Trajectory Vector' components to enable accurate prediction of moving heat masses.

## Core Mathematical Components
1. **Intensity Derivative (dI/dt):** Calculates the rate of change of signal intensity to distinguish between static noise and moving targets.
2. **Trajectory Vector (V_traj):** Estimates the velocity and direction of the target based on the temporal evolution of signal intensity and centroid position.

## Task Steps
1. Define the core mathematical functions in `engine.py`.
2. Implement a simulation environment in `simulation.py` that generates a synthetic 'accelerating heat mass' signal.
3. Verify the engine's ability to track and predict the trajectory of the accelerating mass.
