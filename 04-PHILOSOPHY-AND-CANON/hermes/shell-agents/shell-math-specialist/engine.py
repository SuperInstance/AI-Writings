import numpy as np

class PredictiveSonarEngine:
    def __init__(self, dt=0.1):
        self.dt = dt
        self.history_depth = 5
        self.intensity_history = []
        self.position_history = []

    def calculate_intensity_derivative(self, current_intensity):
        """
        Calculates dI/dt using a backward difference method.
        """
        self.intensity_history.append(current_intensity)
        if len(self.intensity_history) < 2:
            return 0.0
        
        if len(self.intensity_history) > self.history_depth:
            self.intensity_history.pop(0)
            
        di = self.intensity_history[-1] - self.intensity_history[-2]
        return di / self.dt

    def calculate_trajectory_vector(self, current_position, current_intensity_derivative):
        """
        Estimates the trajectory vector (dx, dy) based on:
        1. Change in position (velocity component)
        2. Change in intensity
        """
        self.position_history.append(np.array(current_position))
        if len(self.position_history) < 2:
            return np.array([0.0, 0.0]), 1.0

        if len(self.position_history) > self.history_depth:
            self.position_history.pop(0)

        dpos = self.position_history[-1] - self.position_history[-2]
        velocity = dpos / self.dt
        
        confidence = min(abs(current_intensity_derivative) / 10.0 + 0.5, 1.0)
        
        return velocity, confidence

    def predict_next_position(self, current_position, velocity, dt_future=1.0):
        """
        Simple linear extrapolation for prediction.
        """
        return current_position + velocity * dt_future
