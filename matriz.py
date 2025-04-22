import numpy as np

def leer_matriz():
    print("INSTRUCCIONES:")
    print("Introduce una matriz cuadrada de 2x2, 3x3 o 4x4 o superior.")
    print("Introduce los elementos de la matriz fila por fila, separados por espacios.")
    print("Pulsa Enter después de cada fila. La entrada finalizará automáticamente cuando completes las filas necesarias.")

    filas = []
    while True:
        try:
            entrada = input(f"Fila {len(filas) + 1}: ")
            fila = list(map(float, entrada.strip().split()))
            filas.append(fila)

            # Verificar si la matriz es cuadrada y si se completaron las filas necesarias
            if len(filas) == len(filas[0]):
                break
            elif len(filas) > len(filas[0]):
                print("Error: La matriz no es cuadrada. Vuelve a intentarlo.")
                return None
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

    if matriz.shape[0] not in (2, 3) and matriz.shape[0] < 4:
        print(f"Matriz de {matriz.shape[0]}x{matriz.shape[1]} no soportada actualmente.")
        return None

    print(f"Matriz {matriz.shape[0]}x{matriz.shape[1]} recibida correctamente:")
    print(matriz)

    return matriz
