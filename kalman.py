import numpy as np

# Parámetro de tiempo
vart = 1
Xkanterior = 1
Vxkanterior = 2
axkanterior = 3
ykanterior = 4
Vykanterior = 5
aykanterior = 6

# Matriz A (modelo de movimiento con aceleración constante en 2D)
A = np.array([
    [1, vart, (vart**2)/2, 0,    0,           0],
    [0,   1,      vart,    0,    0,           0],
    [0,   0,        1,     0,    0,           0],
    [0,   0,        0,     1,  vart, (vart**2)/2],
    [0,   0,        0,     0,    1,         vart],
    [0,   0,        0,     0,    0,           1]
])

# Estado anterior (posición, velocidad, aceleración en x e y)
valores_Xk_anterior = np.array([
    [Xkanterior],
    [Vxkanterior],
    [axkanterior],
    [ykanterior],
    [Vykanterior],
    [aykanterior]
])

# Predicción del estado siguiente Xk = A @ Xk-1
Prediccion_Xk = A @ valores_Xk_anterior
#Mediciones 
Matriz_H = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0],
])

#datos sensor entradad 

Matriz_Entrada = np.array([
    [valorxdedo],
    [0],
    [0],
    [valorydedo],
    [0],
    [0],
])

print(Prediccion_Xk)
