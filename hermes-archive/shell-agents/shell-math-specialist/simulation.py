import numpy as np
from engine import PredictiveSonarEngine

def run_simulation():
    # Simulation parameters
    dt = 0.1
    total_time = 5.0
    steps = int(total_time / dt)
    
    # Target: Accelerating heat mass
    # Position: x(t) = 0.5 * a * t^2, y(t) = vt
    accel = 2.0
    v0_y = 1.0
    
    engine = PredictiveSonarEngine(dt=dt)
    
    print(f"Starting Simulation: Accelerating mass (a={accel}, v0_y={v0_y})")
    print("Time | True Pos | Detected Pos | Velocity | Prediction")
    print("------------------------------------------------------")

    for i in range(steps):
        t = i * dt
        
        # True state
        true_x = 0.5 * accel * (t**2)
        true_y = v0_y * t
        true_pos = np.array([true_x, true_y])
        
        # Intensity: inversely proportional to distance squared (simplified)
        # For an accelerating mass, let's also simulate increasing intensity as it approaches or heats up
        # Here we'll just assume intensity increases with speed to simulate 'thermal signature' boost
        intensity = 10.0 * (accel * t)
        
        # Engine processing
        di_dt = engine.calculate_intensity_derivative(intensity)
        velocity, confidence = engine.calculate_trajectory_vector(true_pos, di_dt)
        prediction = engine.predict_next_position(true_pos, velocity, dt_future=dt)

        if i % 10 == 0:
            print(f"{t:4.1f} | {true_pos} | {true_pos} | {velocity} | {prediction}")

    print("\nSimulation Complete.")

if __name__ == '__main__':
    run_simulation()
