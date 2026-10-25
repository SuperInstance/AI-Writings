import numpy as np

class TemporalSignatureAnalyzer:
    """
    Analyzes pixel intensity temporal signatures to detect 
    impending escalation patterns (Pre-Strikes).
    """

    def __init__(self, acceleration_threshold: float, vertical_velocity_threshold: float):
        """
        Initialize with detection thresholds.
        
        :param acceleration_threshold: Minimum intensity acceleration required for a pre-strike.
        :param vertical_velocity_threshold: Minimum vertical approach velocity required for a pre-strike.
        """
        self.acceleration_threshold = acceleration_threshold
        self.vertical_velocity_threshold = vertical_velocity_threshold

    def analyze_escalation(self, window_data: np.ndarray) -> float:
        """
        Calculates derivatives of pixel intensity and returns a probability score.
        
        :param window_data: A 2D numpy array (N, 2) representing [intensity, vertical_velocity] 
                           over a discrete time window.
        :return: Probability score (0.0 to 1.0) representing escalation likelihood.
        """
        if len(window_data) < 3:
            return 0.0

        # Extract signals
        intensities = window_data[:, 0]
        vertical_velocities = window_data[:, 1]

        # Calculate first derivative (Velocity) of intensity
        # Using np.diff: v[i] = x[i+1] - x[i]
        intensity_velocity = np.diff(intensities)

        # Calculate second derivative (Acceleration) of intensity
        # a[i] = v[i+1] - v[i]
        intensity_acceleration = np.diff(intensity_velocity)

        # We look at the most recent values (the end of the window)
        latest_acceleration = intensity_acceleration[-1]
        latest_v_velocity = vertical_velocities[-1]

        # Pre-Strike Condition:
        # 1. intensity acceleration > threshold
        # 2. vertical approach velocity > threshold
        is_pre_strike = (latest_acceleration > self.acceleration_threshold and 
                         latest_v_velocity > self.vertical_velocity_threshold)

        # Probability score:
        # In a production system, this would be a sigmoid function of the deltas.
        # For this implementation, we'll use a simplified linear mapping.
        if is_pre_strike:
            # Scale based on how much they exceed thresholds
            accel_factor = min(latest_acceleration / (self.acceleration_threshold * 2), 1.0)
            vel_factor = min(latest_v_velocity / (self.vertical_velocity_threshold * 2), 1.0)
            return float(0.5 + (0.5 * (accel_factor + vel_factor) / 2))
        
        return 0.0

if __name__ == "__main__":
    # Quick Test
    analyzer = TemporalSignatureAnalyzer(acceleration_threshold=2.0, vertical_velocity_threshold=5.0)
    
    # Case 1: Normal state
    normal_data = np.array([[10, 1], [11, 1.2], [10.5, 1.1]])
    print(f"Normal Score: {analyzer.analyze_escalation(normal_data)}")

    # Case 2: Escalation (Increasing intensity acceleration + high vertical velocity)
    # Intensities: 10 -> 12 (v=2) -> 17 (v=5, a=3)
    # Vertical velocities: 1 -> 6 -> 7
    escalation_data = np.array([[10, 1.0], [12, 6.0], [17, 7.0]])
    print(f"Escalation Score: {analyzer.analyze_escalation(escalation_data)}")
