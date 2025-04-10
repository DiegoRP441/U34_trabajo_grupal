from matriz import leer_matriz
import numpy as np
import numpy as np

# Determinante para una matriz 2x2
def det_2x2(matriz):
    return matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]

# Determinante para una matriz 3x3
def det_3x3(matriz):
    a, b, c = matriz[0]
    d, e, f = matriz[1]
    g, h, i = matriz[2]
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)

# Función principal para calcular el determinante
def calcular_determinante(matriz):
    if matriz.shape == (2, 2):
        return det_2x2(matriz)
    elif matriz.shape == (3, 3):
        return det_3x3(matriz)
    else:
        print("Solo se soportan matrices de 2x2 o 3x3.")
        return None

# Inversa de una 2X2 
def inversa_2x2(m):
    det = det_2x2(m)
    if det == 0:
        print("La matriz no es invertible.")
        return None
    inv = (1/det) * np.array([[m[1][1], -m[0][1]],
                              [-m[1][0], m[0][0]]])
    return inv

# Intercambio de filas 
def intercambiar_filas(matriz, fila1, fila2):
    matriz[[fila1, fila2]] = matriz[[fila2, fila1]]
    return matriz

A = np.array([[1, 2, 3],
              [4, 5, 6],
              [7, 8, 9]])

print("Antes del cambio:\n", A)
intercambiar_filas(A, 0, 2)
print("Después del cambio:\n", A)

def multiplicar_fila_por_escalar(matriz, fila, escalar):
    matriz[fila] = matriz[fila] * escalar
    return matriz

print(multiplicar_fila_por_escalar(A,1,2))

def operar_filas(matriz, fila_destino, fila_origen, escalar):
    matriz[fila_destino] = matriz[fila_destino] + escalar * matriz[fila_origen]
    return matriz

def sumar_matrices(A, B):
    if A.shape != B.shape:
        raise ValueError("Las matrices deben tener el mismo tamaño.")
    return A + B

def restar_matrices(A, B):
    if A.shape != B.shape:
        raise ValueError("Las matrices deben tener el mismo tamaño.")
    return A - B

def multiplicar_matrices(A, B):
    if A.shape[1] != B.shape[0]:
        raise ValueError("El número de columnas de A debe ser igual al número de filas de B.")
    return np.dot(A, B)  # O A @ B


def transpuesta_manual(matriz):
    filas, columnas = matriz.shape
    resultado = np.zeros((columnas, filas))

    for i in range(filas):
        for j in range(columnas):
            resultado[j][i] = matriz[i][j]
    
    return resultado
