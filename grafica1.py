import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Longitudes de los eslabones
L1, L2 = 1.0, 0.7

# Generar trayectorias en círculo
t = np.linspace(0, 2*np.pi, 100)
x_pie = 0.5 + 0.3 * np.cos(t)  
y_pie = 0.5 + 0.3 * np.sin(t)  

# Función de cinemática inversa (resuelve los ángulos de las articulaciones)
def inverse_kinematics(x, y):
    c2 = (x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2)
    s2 = np.sqrt(1 - c2**2)  # Selección de la solución positiva
    theta2 = np.arctan2(s2, c2)
    
    k1 = L1 + L2 * np.cos(theta2)
    k2 = L2 * np.sin(theta2)
    theta1 = np.arctan2(y, x) - np.arctan2(k2, k1)
    
    return theta1, theta2

# Calcular los ángulos para toda la trayectoria
theta1_vals, theta2_vals = zip(*[inverse_kinematics(x, y) for x, y in zip(x_pie, y_pie)])

# Configuración de la animación
fig, ax = plt.subplots()
ax.set_xlim(-1.5, 1.5)
ax.set_ylim(-1.5, 1.5)
line, = ax.plot([], [], 'o-', lw=2)

def init():
    line.set_data([], [])
    return line,

def update(i):
    theta1, theta2 = theta1_vals[i], theta2_vals[i]
    
    x1 = L1 * np.cos(theta1)
    y1 = L1 * np.sin(theta1)
    x2 = x1 + L2 * np.cos(theta1 + theta2)
    y2 = y1 + L2 * np.sin(theta1 + theta2)
    
    line.set_data([0, x1, x2], [0, y1, y2])
    return line,

ani = animation.FuncAnimation(fig, update, frames=len(t), init_func=init, blit=True, interval=50)
plt.show()
