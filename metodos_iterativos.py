import numpy as np
from matriz import leer_matriz

def criterio_convergencia(A):
    """
    Verifica si una matriz cumple con el criterio de convergencia para métodos iterativos.
    Para que converja, la matriz debe ser diagonalmente dominante.
    """
    n = A.shape[0]
    for i in range(n):
        suma = sum(abs(A[i, j]) for j in range(n) if j != i)
        if abs(A[i, i]) <= suma:
            return False
    return True

def verificar_sistema(A, b):
    """
    Verifica si el sistema Ax = b es adecuado para métodos iterativos.
    """
    if A.shape[0] != A.shape[1]:
        raise ValueError("La matriz A debe ser cuadrada")
    
    if A.shape[0] != b.shape[0]:
        raise ValueError("Las dimensiones de A y b no son compatibles")
    
    if not criterio_convergencia(A):
        print("ADVERTENCIA: La matriz no cumple el criterio de convergencia (no es diagonalmente dominante).")
        print("Los métodos iterativos podrían no converger.")

def leer_vector_b():
    """
    Lee el vector de términos independientes b para el sistema Ax = b.
    """
    n = int(input("Introduce el tamaño del vector b: "))
    b = np.zeros(n)
    print("Introduce los elementos del vector b:")
    for i in range(n):
        b[i] = float(input(f"b[{i}]: "))
    return b

def jacobi(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Implementa el método iterativo de Jacobi para resolver el sistema Ax = b.
    
    Parámetros:
    - A: Matriz de coeficientes
    - b: Vector de términos independientes
    - x0: Vector inicial (si no se proporciona, se usa un vector de ceros)
    - tol: Tolerancia para la convergencia
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x: Vector solución
    - iter_count: Número de iteraciones realizadas
    - error_hist: Historial de errores
    """
    verificar_sistema(A, b)
    
    # Dimensión del sistema
    n = A.shape[0]
    
    # Si no se proporciona vector inicial, usar ceros
    if x0 is None:
        x0 = np.zeros(n)
    
    # Inicializar vector solución
    x = x0.copy()
    
    # Historial de errores
    error_hist = []
    
    # Iterar hasta convergencia o máximo de iteraciones
    for k in range(max_iter):
        x_new = np.zeros(n)
        
        # Calcular nuevos valores
        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    suma += A[i, j] * x[j]
            x_new[i] = (b[i] - suma) / A[i, i]
        
        # Calcular error
        error = np.linalg.norm(x_new - x) / np.linalg.norm(x_new)
        error_hist.append(error)
        
        # Actualizar vector solución
        x = x_new.copy()
        
        # Verificar convergencia
        if error < tol:
            return x, k+1, error_hist
    
    print(f"El método de Jacobi no convergió después de {max_iter} iteraciones.")
    return x, max_iter, error_hist

def gauss_seidel(A, b, x0=None, tol=1e-6, max_iter=100):
    """
    Implementa el método iterativo de Gauss-Seidel para resolver el sistema Ax = b.
    
    Parámetros:
    - A: Matriz de coeficientes
    - b: Vector de términos independientes
    - x0: Vector inicial (si no se proporciona, se usa un vector de ceros)
    - tol: Tolerancia para la convergencia
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - x: Vector solución
    - iter_count: Número de iteraciones realizadas
    - error_hist: Historial de errores
    """
    verificar_sistema(A, b)
    
    # Dimensión del sistema
    n = A.shape[0]
    
    # Si no se proporciona vector inicial, usar ceros
    if x0 is None:
        x0 = np.zeros(n)
    
    # Inicializar vector solución
    x = x0.copy()
    
    # Historial de errores
    error_hist = []
    
    # Iterar hasta convergencia o máximo de iteraciones
    for k in range(max_iter):
        x_old = x.copy()
        
        # Calcular nuevos valores
        for i in range(n):
            suma1 = 0  # Suma de los términos ya calculados (índices menores que i)
            suma2 = 0  # Suma de los términos no calculados (índices mayores que i)
            
            for j in range(0, i):
                suma1 += A[i, j] * x[j]
                
            for j in range(i+1, n):
                suma2 += A[i, j] * x_old[j]
                
            x[i] = (b[i] - suma1 - suma2) / A[i, i]
        
        # Calcular error
        error = np.linalg.norm(x - x_old) / np.linalg.norm(x)
        error_hist.append(error)
        
        # Verificar convergencia
        if error < tol:
            return x, k+1, error_hist
    
    print(f"El método de Gauss-Seidel no convergió después de {max_iter} iteraciones.")
    return x, max_iter, error_hist

def resolver_sistema_iterativo():
    """
    Función principal para resolver un sistema utilizando métodos iterativos.
    Pide al usuario seleccionar el método y los parámetros.
    """
    print("\n--- RESOLVER SISTEMA ITERATIVO ---")
    print("Primero, vamos a ingresar la matriz de coeficientes A:")
    A = leer_matriz()
    if A is None:
        return None, None, None
    
    print("\nAhora, ingresa el vector de términos independientes b:")
    b = leer_vector_b()
    
    if b.shape[0] != A.shape[0]:
        print(f"Error: El vector b debe tener {A.shape[0]} elementos para ser compatible con A.")
        return None, None, None
    
    print("\nSelecciona el método iterativo:")
    print("1. Jacobi")
    print("2. Gauss-Seidel")
    
    metodo = input("Método: ")
    
    # Pedir parámetros adicionales
    tol = float(input("Tolerancia (por defecto 1e-6): ") or "1e-6")
    max_iter = int(input("Máximo de iteraciones (por defecto 100): ") or "100")
    
    # Opcionalmente, pedir vector inicial
    usar_x0 = input("¿Deseas proporcionar un vector inicial? (s/n): ").lower() == 's'
    x0 = None
    if usar_x0:
        x0 = np.zeros(A.shape[0])
        print("Introduce los elementos del vector inicial x0:")
        for i in range(A.shape[0]):
            x0[i] = float(input(f"x0[{i}]: "))
    
    if metodo == "1":
        print("\nResolviendo sistema con el método de Jacobi...")
        x, iteraciones, errores = jacobi(A, b, x0, tol, max_iter)
    elif metodo == "2":
        print("\nResolviendo sistema con el método de Gauss-Seidel...")
        x, iteraciones, errores = gauss_seidel(A, b, x0, tol, max_iter)
    else:
        print("Opción no válida.")
        return None, None, None
    
    return x, iteraciones, errores

def mostrar_resultados_iterativos(x, iteraciones, errores):
    """
    Muestra los resultados de los métodos iterativos.
    """
    if x is None:
        return
    
    print("\n--- RESULTADOS ---")
    print(f"Solución después de {iteraciones} iteraciones:")
    for i, valor in enumerate(x):
        print(f"x{i} = {valor:.6f}")
    
    print(f"\nConvergencia: Error final = {errores[-1]:.8e}")
    
    print("\nHistorial de errores:")
    for i, error in enumerate(errores[:min(10, len(errores))]):
        print(f"Iteración {i+1}: {error:.8e}")
    
    if len(errores) > 10:
        print("...")