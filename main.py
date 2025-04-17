from matriz import leer_matriz
from metodos_directos import (
    calcular_determinante,
    inversa_2x2,
    transpuesta_manual,
    sumar_matrices,
    restar_matrices,
    multiplicar_matrices
)
from metodos_iterativos import resolver_sistema_iterativo, mostrar_resultados_iterativos
from metodos_no_lineales import (
    resolver_ecuacion_no_lineal, 
    mostrar_resultados_newton_1var,
    resolver_sistema_no_lineal,
    mostrar_resultados_newton_sistema
)

def mostrar_menu_principal():
    print("\n=== MENÚ PRINCIPAL ===")
    print("1. Operaciones con métodos directos")
    print("2. Resolver sistema con métodos iterativos (Jacobi/Gauss-Seidel)")
    print("3. Resolver ecuación no lineal (Newton-Raphson)")
    print("4. Resolver sistema no lineal (Newton-Raphson)")
    print("0. Salir")

def mostrar_menu_metodos_directos():
    print("\n--- MENÚ DE OPERACIONES DIRECTAS ---")
    print("1. Calcular determinante")
    print("2. Calcular inversa (solo 2x2)")
    print("3. Transpuesta")
    print("4. Sumar otra matriz")
    print("5. Restar otra matriz")
    print("6. Multiplicar por otra matriz")
    print("0. Volver al menú principal")

def metodos_directos_menu():
    matriz = leer_matriz()
    if matriz is None:
        return

    while True:
        mostrar_menu_metodos_directos()
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
            print("Volviendo al menú principal.")
            break
        else:
            print("Opción no válida.")

def main():
    print("Bienvenido al programa de Métodos Numéricos")
    print("Este programa permite trabajar con métodos directos, iterativos y no lineales.")
    
    while True:
        mostrar_menu_principal()
        opcion = input("Elige una opción: ")

        if opcion == "1":
            metodos_directos_menu()
            
        elif opcion == "2":
            # Resolver sistema con métodos iterativos
            x, iteraciones, errores = resolver_sistema_iterativo()
            mostrar_resultados_iterativos(x, iteraciones, errores)
            
        elif opcion == "3":
            # Resolver ecuación no lineal con Newton-Raphson
            resultados = resolver_ecuacion_no_lineal()
            if resultados[0] is not None:
                raiz, iteraciones, x_hist, errores, expr_f = resultados
                mostrar_resultados_newton_1var(raiz, iteraciones, x_hist, errores, expr_f)
            
        elif opcion == "4":
            # Resolver sistema no lineal con Newton-Raphson
            resultados = resolver_sistema_no_lineal()
            if resultados[0] is not None:
                sol, iteraciones, sol_hist, errores, expr_F = resultados
                mostrar_resultados_newton_sistema(sol, iteraciones, sol_hist, errores, expr_F)
            
        elif opcion == "0":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    main()