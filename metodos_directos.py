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


def multiplicar_fila_por_escalar(matriz, fila, escalar):
    matriz[fila] = matriz[fila] * escalar
    return matriz


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

def gauss_eliminacion(matriz, vector):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando eliminación de Gauss.
    
    Parámetros:
    - matriz: Matriz de coeficientes (numpy array de tamaño n x n).
    - vector: Vector de términos independientes (numpy array de tamaño n).
    
    Retorna:
    - Un numpy array con la solución del sistema x.
    """
    n = len(vector)
    A = np.array(matriz, dtype=float)
    b = np.array(vector, dtype=float)

    # Eliminación hacia adelante
    for i in range(n):
        # Verificar si el pivote es cero
        if A[i, i] == 0:
            raise ValueError("El sistema no tiene solución única (pivote cero).")
        
        # Normalizar la fila actual dividiendo por el pivote
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]
            b[j] -= factor * b[i]

    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

    return x

def gauss_eliminacion_solo_matriz(matriz):
    """
    Aplica el método de eliminación de Gauss para transformar una matriz en su forma escalonada.
    
    Parámetros:
    - matriz: Matriz de coeficientes (numpy array de tamaño n x n).
    
    Retorna:
    - La matriz transformada en forma escalonada.
    """
    n = matriz.shape[0]
    A = np.array(matriz, dtype=float)

    # Eliminación hacia adelante
    for i in range(n):
        # Verificar si el pivote es cero
        if A[i, i] == 0:
            # Buscar una fila para intercambiar
            for k in range(i + 1, n):
                if A[k, i] != 0:
                    A[[i, k]] = A[[k, i]]  # Intercambiar filas
                    break
            else:
                raise ValueError("El sistema no tiene solución única (pivote cero).")
        
        # Normalizar la fila actual dividiendo por el pivote
        for j in range(i + 1, n):
            factor = A[j, i] / A[i, i]
            A[j, i:] -= factor * A[i, i:]

    return A


 # Ejemplo con la matriz problemática
matriz = np.array([
    [1, 2, 3, 4],
    [0, 1, 2, 4],
    [2, 3, 4, 5],
    [2, 0, 1, 2]
])

resultado = gauss_eliminacion_solo_matriz(matriz)
print("\nResultado final:")
print(resultado)