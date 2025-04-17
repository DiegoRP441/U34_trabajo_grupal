import numpy as np
import re

def derivada_numerica(f, x, h=1e-6):
    """
    Calcula la derivada numérica de una función en un punto.
    Usa la fórmula de diferencia central para mayor precisión.
    
    Parámetros:
    - f: Función de la cual calcular la derivada
    - x: Punto en el que calcular la derivada
    - h: Tamaño del paso
    
    Retorna:
    - Valor numérico de la derivada en el punto x
    """
    return (f(x + h) - f(x - h)) / (2 * h)

def crear_funcion(expresion):
    """
    Convierte una expresión de texto en una función lambda.
    Más limitado que SymPy pero funciona para expresiones básicas.
    
    Parámetros:
    - expresion: String con la expresión matemática
    
    Retorna:
    - Función lambda que evalúa la expresión
    """
    # Limpiar la expresión
    expr = expresion.strip()
    
    try:
        # Crear una función lambda que evalúa la expresión
        funcion = eval(f"lambda x: {expr}")
        
        # Probar la función con un valor para verificar que funciona
        funcion(1.0)
        
        return funcion
    except Exception as e:
        print(f"Error al crear la función: {e}")
        return None

def input_funcion():
    """
    Permite al usuario ingresar una función mediante texto.
    Retorna la función en formato lambda.
    """
    print("\n--- INGRESO DE FUNCIÓN ---")
    print("Introduce una función de una variable x (por ejemplo: x**2 - 4)")
    expresion = input("f(x) = ")
    
    # Convertir la expresión a una función lambda
    try:
        funcion = crear_funcion(expresion)
        
        if funcion is None:
            return None, None, expresion
        
        # Crear una función para la derivada usando diferenciación numérica
        def derivada(x):
            return derivada_numerica(funcion, x)
        
        print("Función ingresada correctamente:")
        print(f"f(x) = {expresion}")
        print("La derivada se calculará numéricamente.")
        
        return funcion, derivada, expresion
    
    except Exception as e:
        print(f"Error al procesar la función: {e}")
        return None, None, None

def input_sistema_no_lineal():
    """
    Permite al usuario ingresar un sistema de ecuaciones no lineales.
    """
    print("\n--- INGRESO DE SISTEMA NO LINEAL ---")
    print("Introduce un sistema de ecuaciones no lineales de dos variables x e y.")
    print("Por ejemplo, para el sistema:")
    print("  x^2 + y^2 = 25")
    print("  x*y = 12")
    print("Debes escribir:")
    print("  x**2 + y**2 - 25")
    print("  x*y - 12")
    
    ecuaciones = []
    expresiones = []
    
    for i in range(2):  # Sistema de 2 ecuaciones
        expr = input(f"Ecuación {i+1}: ")
        expresiones.append(expr)
        
        try:
            # Convertir a función lambda
            funcion = eval(f"lambda x, y: {expr}")
            # Probar la función
            funcion(1.0, 1.0)
            ecuaciones.append(funcion)
        except Exception as e:
            print(f"Error al procesar la ecuación {i+1}: {e}")
            return None, None, None
    
    # Crear funciones para las derivadas parciales usando diferencias finitas
    def J11(x, y, h=1e-6):
        return (ecuaciones[0](x + h, y) - ecuaciones[0](x - h, y)) / (2 * h)
    
    def J12(x, y, h=1e-6):
        return (ecuaciones[0](x, y + h) - ecuaciones[0](x, y - h)) / (2 * h)
    
    def J21(x, y, h=1e-6):
        return (ecuaciones[1](x + h, y) - ecuaciones[1](x - h, y)) / (2 * h)
    
    def J22(x, y, h=1e-6):
        return (ecuaciones[1](x, y + h) - ecuaciones[1](x, y - h)) / (2 * h)
    
    print("\nSistema ingresado correctamente:")
    print(f"F1(x,y) = {expresiones[0]}")
    print(f"F2(x,y) = {expresiones[1]}")
    
    print("\nJacobiano se calculará numéricamente.")
    
    return ecuaciones, expresiones, [J11, J12, J21, J22]

def newton_raphson_1var(f, df, x0, tol=1e-6, max_iter=100):
    """
    Implementa el método de Newton-Raphson para encontrar raíces de una ecuación no lineal.
    
    Parámetros:
    - f: Función de la cual encontrar las raíces
    - df: Derivada de la función
    - x0: Punto inicial
    - tol: Tolerancia para la convergencia
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - raiz: Aproximación a la raíz
    - iter_count: Número de iteraciones realizadas
    - x_hist: Historial de aproximaciones
    - error_hist: Historial de errores
    """
    x = x0
    x_hist = [x]
    error_hist = []
    
    for i in range(max_iter):
        # Evaluar función y derivada
        f_x = f(x)
        df_x = df(x)
        
        # Verificar si la derivada es muy cercana a cero
        if abs(df_x) < 1e-10:
            print(f"La derivada es casi cero en x = {x}. No se puede continuar.")
            return x, i, x_hist, error_hist
        
        # Calcular siguiente aproximación
        x_new = x - f_x / df_x
        
        # Calcular error
        error = abs(x_new - x)
        error_hist.append(error)
        
        # Actualizar valor
        x = x_new
        x_hist.append(x)
        
        # Verificar convergencia
        if error < tol:
            return x, i+1, x_hist, error_hist
    
    print(f"El método de Newton-Raphson no convergió después de {max_iter} iteraciones.")
    return x, max_iter, x_hist, error_hist

def newton_raphson_sistema(F, J, x0, tol=1e-6, max_iter=100):
    """
    Implementa el método de Newton-Raphson para sistemas de ecuaciones no lineales.
    
    Parámetros:
    - F: Lista de funciones del sistema [F1, F2]
    - J: Lista de funciones del Jacobiano [J11, J12, J21, J22]
    - x0: Vector inicial [x0, y0]
    - tol: Tolerancia para la convergencia
    - max_iter: Número máximo de iteraciones
    
    Retorna:
    - sol: Vector solución [x, y]
    - iter_count: Número de iteraciones realizadas
    - sol_hist: Historial de aproximaciones
    - error_hist: Historial de errores
    """
    x, y = x0
    sol_hist = [[x, y]]
    error_hist = []
    
    J11, J12, J21, J22 = J  # Funciones del Jacobiano
    
    for i in range(max_iter):
        # Evaluar funciones
        F1 = F[0](x, y)
        F2 = F[1](x, y)
        
        # Evaluar Jacobiano
        j11 = J11(x, y)
        j12 = J12(x, y)
        j21 = J21(x, y)
        j22 = J22(x, y)
        
        # Calcular el determinante del Jacobiano
        det_J = j11*j22 - j12*j21
        
        # Verificar si el determinante es muy cercano a cero
        if abs(det_J) < 1e-10:
            print(f"El determinante del Jacobiano es casi cero en [x,y] = [{x},{y}]. No se puede continuar.")
            return [x, y], i, sol_hist, error_hist
        
        # Calcular siguiente aproximación resolviendo el sistema lineal J * Δx = -F
        dx = (-j22*F1 + j12*F2) / det_J
        dy = (j21*F1 - j11*F2) / det_J
        
        # Actualizar valores
        x_new = x + dx
        y_new = y + dy
        
        # Calcular error
        error = np.sqrt(dx**2 + dy**2)
        error_hist.append(error)
        
        # Actualizar valores
        x, y = x_new, y_new
        sol_hist.append([x, y])
        
        # Verificar convergencia
        if error < tol:
            return [x, y], i+1, sol_hist, error_hist
    
    print(f"El método de Newton-Raphson no convergió después de {max_iter} iteraciones.")
    return [x, y], max_iter, sol_hist, error_hist

def resolver_ecuacion_no_lineal():
    """
    Función principal para resolver una ecuación no lineal con Newton-Raphson.
    Pide al usuario ingresar la función y los parámetros.
    """
    f, df, expr_f = input_funcion()
    if f is None:
        return None, None, None, None, None
    
    # Pedir punto inicial
    x0 = float(input("\nIngrese el punto inicial x0: "))
    
    # Pedir parámetros adicionales
    tol = float(input("Tolerancia (por defecto 1e-6): ") or "1e-6")
    max_iter = int(input("Máximo de iteraciones (por defecto 100): ") or "100")
    
    print("\nResolviendo ecuación con el método de Newton-Raphson...")
    raiz, iteraciones, x_hist, errores = newton_raphson_1var(f, df, x0, tol, max_iter)
    
    return raiz, iteraciones, x_hist, errores, expr_f

def resolver_sistema_no_lineal():
    """
    Función principal para resolver un sistema de ecuaciones no lineales con Newton-Raphson.
    Pide al usuario ingresar las funciones y los parámetros.
    """
    F, expr_F, J = input_sistema_no_lineal()
    if F is None:
        return None, None, None, None, None
    
    # Pedir punto inicial
    print("\nIngrese el punto inicial [x0, y0]:")
    x0 = float(input("x0: "))
    y0 = float(input("y0: "))
    
    # Pedir parámetros adicionales
    tol = float(input("Tolerancia (por defecto 1e-6): ") or "1e-6")
    max_iter = int(input("Máximo de iteraciones (por defecto 100): ") or "100")
    
    print("\nResolviendo sistema con el método de Newton-Raphson...")
    sol, iteraciones, sol_hist, errores = newton_raphson_sistema(F, J, [x0, y0], tol, max_iter)
    
    return sol, iteraciones, sol_hist, errores, expr_F

def mostrar_resultados_newton_1var(raiz, iteraciones, x_hist, errores, expr_f):
    """
    Muestra los resultados del método de Newton-Raphson para 1 variable.
    """
    if raiz is None:
        return
    
    print("\n--- RESULTADOS NEWTON-RAPHSON ---")
    print(f"Raíz encontrada: x = {raiz:.8f}")
    
    # Crear la función a partir de la expresión para evaluar
    f = crear_funcion(expr_f)
    if f is not None:
        valor_f = f(raiz)
        print(f"Valor de f(x) en la raíz: {valor_f:.8e}")
    
    print(f"Convergencia en {iteraciones} iteraciones")
    
    print("\nHistorial de aproximaciones:")
    for i, xi in enumerate(x_hist[:min(10, len(x_hist))]):
        if i < len(errores):
            print(f"Iteración {i}: x = {xi:.8f}, error = {errores[i]:.8e}")
        else:
            print(f"Iteración {i}: x = {xi:.8f}")
    
    if len(x_hist) > 10:
        print("...")

def mostrar_resultados_newton_sistema(sol, iteraciones, sol_hist, errores, expr_F):
    """
    Muestra los resultados del método de Newton-Raphson para sistemas.
    """
    if sol is None:
        return
    
    print("\n--- RESULTADOS NEWTON-RAPHSON PARA SISTEMAS ---")
    print(f"Solución encontrada: x = {sol[0]:.8f}, y = {sol[1]:.8f}")
    
    # Evaluar funciones en la solución
    F1 = crear_funcion(expr_F[0].replace('y', str(sol[1])))
    F2 = crear_funcion(expr_F[1].replace('y', str(sol[1])))
    
    if F1 is not None and F2 is not None:
        valor_F1 = F1(sol[0])
        valor_F2 = F2(sol[0])
        print(f"Valor de F1(x,y) en la solución: {valor_F1:.8e}")
        print(f"Valor de F2(x,y) en la solución: {valor_F2:.8e}")
    
    print(f"Convergencia en {iteraciones} iteraciones")
    
    print("\nHistorial de aproximaciones:")
    for i, punto in enumerate(sol_hist[:min(10, len(sol_hist))]):
        if i < len(errores):
            print(f"Iteración {i}: [x,y] = [{punto[0]:.6f}, {punto[1]:.6f}], error = {errores[i]:.8e}")
        else:
            print(f"Iteración {i}: [x,y] = [{punto[0]:.6f}, {punto[1]:.6f}]")
    
    if len(sol_hist) > 10:
        print("...")