# Reimportar librerías tras el reinicio
import numpy as np
import pandas as pd

# Clase del filtro de Kalman 2D (posición, velocidad, aceleración)
class KalmanFilter2D:
    def __init__(self, dt, process_noise_std, measurement_noise_std, initial_pos):
        # Estado: [x, y, vx, vy, ax, ay]
        self.dt = dt
        self.x = np.array([
            [initial_pos[0]],  # x
            [initial_pos[1]],  # y
            [0],               # vx
            [0],               # vy
            [0],               # ax
            [0]                # ay
        ])

        dt2 = 0.5 * dt**2
        self.A = np.array([
            [1, 0, dt, 0, dt2, 0],
            [0, 1, 0, dt, 0, dt2],
            [0, 0, 1, 0, dt, 0],
            [0, 0, 0, 1, 0, dt],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 1]
        ])

        self.H = np.array([
            [1, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0]
        ])

        self.P = np.eye(6) * 1000

        q_pos, q_vel, q_acc = process_noise_std
        self.Q = np.diag([
            q_pos**2, q_pos**2,
            q_vel**2, q_vel**2,
            q_acc**2, q_acc**2
        ])

        r = measurement_noise_std
        self.R = np.diag([r**2, r**2])

    def predict(self):
        self.x = self.A @ self.x
        self.P = self.A @ self.P @ self.A.T + self.Q

    def update(self, z):
        z = np.reshape(z, (2, 1))
        y = z - self.H @ self.x
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ y
        I = np.eye(self.A.shape[0])
        self.P = (I - K @ self.H) @ self.P

    def get_state(self):
        return self.x.flatten()

# Crear filtro con parámetros y simular uso
kf = KalmanFilter2D(
    dt=1.0,
    process_noise_std=(1, 5, 50),
    measurement_noise_std=3.0,
    initial_pos=(0, 0)
)

# Datos simulados de posición
positions = [(0, 0), (1, 2), (3.1, 4.2), (6.1, 6.1), (10.0, 8.2)]
states = []

for z in positions:
    kf.predict()
    kf.update(z)
    states.append(kf.get_state())

# Mostrar resultados
#from ace_tools import display_dataframe_to_user
df_states = pd.DataFrame(states, columns=["x", "y", "vx", "vy", "ax", "ay"])

