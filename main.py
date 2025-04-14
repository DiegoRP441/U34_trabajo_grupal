from matriz import leer_matriz
from metodos_directos import (
    calcular_determinante,
    inversa_2x2,
    transpuesta_manual,
    sumar_matrices,
    restar_matrices,
    multiplicar_matrices
)

def mostrar_menu():
    print("\n--- MENÚ DE OPERACIONES ---")
    print("1. Calcular determinante")
    print("2. Calcular inversa (solo 2x2)")
    print("3. Transpuesta")
    print("4. Sumar otra matriz")
    print("5. Restar otra matriz")
    print("6. Multiplicar por otra matriz")
    print("0. Salir")

def main():
    matriz = leer_matriz()
    if matriz is None:
        return

    while True:
        mostrar_menu()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            print("Determinante:", calcular_determinante(matriz))

        elif opcion == "2":
            if matriz.shape != (2, 2):
                print("Solo se puede calcular la inversa de una matriz 2x2.")
            else:
                inversa = inversa_2x2(matriz)
                if inversa is not None:
                    print("Inversa:\n", inversa)

        elif opcion == "3":
            print("Transpuesta:\n", transpuesta_manual(matriz))

        elif opcion in ("4", "5", "6"):
            print("Introduce la segunda matriz (debe ser compatible):")
            otra = leer_matriz()
            if otra is None:
                continue
            try:
                if opcion == "4":
                    print("Suma:\n", sumar_matrices(matriz, otra))
                elif opcion == "5":
                    print("Resta:\n", restar_matrices(matriz, otra))
                elif opcion == "6":
                    print("Multiplicación:\n", multiplicar_matrices(matriz, otra))
            except ValueError as e:
                print("Error:", e)

        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()
