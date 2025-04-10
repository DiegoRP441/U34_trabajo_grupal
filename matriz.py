import numpy as np

def leer_matriz():
    print("Introduce los elementos de la matriz fila por fila, separados por espacios.")
    print("Pulsa Enter después de cada fila. Escribe 'fin' para terminar.")

    filas = []
    while True:
        entrada = input(f"Fila {len(filas) + 1}: ")
        if entrada.lower() == 'fin':
            break
        try:
            fila = list(map(float, entrada.strip().split()))
            filas.append(fila)
        except ValueError:
            print("Por favor, introduce solo números válidos.")

    try:
        matriz = np.array(filas)
    except Exception as e:
        print("Error al crear la matriz:", e)
        return None

    if matriz.shape[0] != matriz.shape[1]:
        print("Error: La matriz no es cuadrada.")
        return None

    if matriz.shape[0] not in (2, 3, 4):
        print(f"Matriz de {matriz.shape[0]}x{matriz.shape[1]} no soportada actualmente.")
        return None

    print(f"Matriz {matriz.shape[0]}x{matriz.shape[1]} recibida correctamente:")
    print(matriz)

    return matriz

leer_matriz()
