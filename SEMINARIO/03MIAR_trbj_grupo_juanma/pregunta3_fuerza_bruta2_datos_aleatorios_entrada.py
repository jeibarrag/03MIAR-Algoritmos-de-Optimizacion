from itertools import permutations
from fractions import Fraction
import random


# ============================================================
# DATOS GENERALES DEL PROBLEMA
# ============================================================
#
# Disponemos de las cifras del 1 al 9, excluyendo el cero, 
# y de los cuatro operadores básicos: +, -, *, /
# Cada expresión usa: 
#   - 5 cifras distintas
#   - 4 operadores distintos
# Ejemplo: 4+2-6/3*1
# ============================================================

# Cifras disponibles.
digitos = range(1, 10)


# Operadores disponibles.
# Cada expresión válida deberá utilizar estos cuatro operadores solo una vez
operadores = ['+', '-', '*', '/']


# ============================================================
# FUNCIÓN PARA EVALUAR UNA EXPRESIÓN
# ============================================================

def evaluar_expresion(cifras, ops):
    """
    Evalúa una expresión respetando la prioridad habitual

    La función recibe dos elementos:
    - cifras: una tupla con 5 cifras. Ejemplo: (4, 2, 6, 3, 1)
    - ops: una tupla con 4 operadores. Ejemplo: ('+', '-', '/', '*')
    
    Con esos datos, la expresión representada sería: 4 + 2 - 6 / 3 * 1

    También se utiliza Fraction para evitar errores de precisión en las divisiones.
    """

    # Un término se cierra cuando aparece una suma o una resta.
    terminos = []

    # Esta lista guarda los signos de los términos.
    # El primer término siempre empieza con signo positivo.
    signos = [1]

    # Inicialmente, el término actual es la primera cifra.
    termino_actual = Fraction(cifras[0])

    # Recorremos al mismo tiempo los operadores y las cifras restantes.
    # Cada pareja representa "operador y cifra siguiente".
    for operador, cifra in zip(ops, cifras[1:]):

        # Convertimos cada cifra a Fraction para que todas las operaciones sean exactas.
        cifra = Fraction(cifra)

        # Si el operador es multiplicación, no cerramos el término.
        # Simplemente actualizamos el término actual.
        if operador == '*':
            termino_actual *= cifra

        # Si el operador es división, tampoco cerramos el término, solo actualizamos el término actual.
        elif operador == '/':
            termino_actual /= cifra

        # Si el operador es suma, significa que el término actual termina..
        elif operador == '+':
            terminos.append(termino_actual)
            signos.append(1)
            termino_actual = cifra

        # Si el operador es resta, también se cierra el término actual.
        elif operador == '-':
            terminos.append(termino_actual)
            signos.append(-1)
            termino_actual = cifra

    # Al terminar el bucle, queda un último término que todavía no se ha añadido.
    # Por eso lo añadimos aquí.
    terminos.append(termino_actual)

    # Finalmente sumamos todos los términos, teniendo en cuenta sus signos.
    resultado = sum(
        signo * termino
        for signo, termino in zip(signos, terminos)
    )

    return resultado


# ============================================================
# FUNCIÓN PARA CONSTRUIR LA EXPRESIÓN COMO TEXTO
# ============================================================

def construir_expresion(cifras, ops):
    """
    Esta función transforma las cifras y operadores en una cadena legible.
    Por ejemplo:  cifras = (4, 2, 6, 3, 1) y ops = ('+', '-', '/', '*')
    devuelve: "4+2-6/3*1"
    """

    # Empezamos con una cadena vacía.
    expresion = ""

    # Añadimos cifra y operador de forma alterna.
    for i in range(4):
        expresion += str(cifras[i]) + ops[i]

    # Al final añadimos la quinta cifra, la expresión tiene 5 cifras y 4 operadores.
    expresion += str(cifras[4])

    return expresion


# ============================================================
# FUNCIÓN PRINCIPAL DE FUERZA BRUTA
# ============================================================

def generar_soluciones():
    """
    Genera todas las expresiones válidas y guarda una expresión
    para cada resultado entero obtenido.

    1. Todas las permutaciones de 5 cifras distintas tomadas de 1 a 9.
    2. Todas las permutaciones de los 4 operadores.
    3. Evaluar todas las expresiones generadas.
    4. Guardar los resultados enteros.

    Guardamos expresión que produce cada valor.
    Para ello usamos un diccionario llamado soluciones:
        - la clave será el resultado entero;
        - el valor será una expresión que produce ese resultado.
    """

    # Diccionario donde se guardará una expresión por cada resultado entero.
    soluciones = {}

    # permutations(digitos, 5) genera todas las formas de elegir y ordenar
    # 5 cifras diferentes entre las 9 disponibles. Esto garantiza que no se repiten cifras.
    for cifras in permutations(digitos, 5):

        # Para cada grupo de cifras, generamos todas las formas de ordenar los cuatro operadores.
        # permutations(operadores, 4) genera las 24 ordenaciones posibles de: '+', '-', '*', '/'
        # Esto garantiza que cada operador se utiliza exactamente una vez.
        for ops in permutations(operadores, 4):

            # Evaluamos la expresión formada por esas cifras y esos operadores.
            valor = evaluar_expresion(cifras, ops)

            # Solo nos interesan los resultados enteros.
            #
            # Como valor es un Fraction, podemos comprobar si es entero mirando
            # si el denominador es 1.
            if valor.denominator == 1:

                # Convertimos el Fraction a entero normal de Python.
                valor_entero = int(valor)

                # Guardamos una expresión para este valor solo si todavía no habíamos guardado ninguna.
                if valor_entero not in soluciones:
                    soluciones[valor_entero] = construir_expresion(cifras, ops)

    # Devolvemos el diccionario completo de soluciones.
    return soluciones


# ============================================================
# PREGUNTA 10: FUNCIÓN PARA GENERAR EL JUEGO DE DATOS DE ENTRADA ALEATORIO
# ============================================================

def generar_datos_entrada_aleatorios(minimo, maximo, cantidad, semilla=27):
    """
    Genera un juego de datos de entrada aleatorio, valores objetivo.
    Cada valor objetivo representa un número que queremos intentar obtener mediante una expresión válida.

    Parámetros:
    - minimo: menor valor del intervalo donde se generan los datos.
    - maximo: mayor valor del intervalo donde se generan los datos.
    - cantidad: número de valores aleatorios que queremos generar.
    - semilla: número usado para que la generación sea reproducible.

    Devuelve:
    - Una lista de valores enteros aleatorios.
    """

    # Fijamos la semilla del generador aleatorio.
    random.seed(semilla)

    # Creamos una lista vacía donde iremos guardando los valores generados.
    datos_entrada = []

    # Repetimos el proceso tantas veces como indique "cantidad".
    for _ in range(cantidad):

        # Generamos un entero aleatorio dentro del intervalo [minimo, maximo].
        valor = random.randint(minimo, maximo)

        # Añadimos el valor generado a la lista.
        datos_entrada.append(valor)

    # Devolvemos el juego de datos completo.
    return datos_entrada


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

# ------------------------------------------------------------
# 1. GENERAR TODAS LAS SOLUCIONES POSIBLES
# ------------------------------------------------------------
#
# Primero ejecutamos el algoritmo de fuerza bruta una sola vez.
#
# Esto genera un diccionario que contiene una expresión válida
# para cada resultado entero alcanzable.

soluciones = generar_soluciones()


# ------------------------------------------------------------
# 2. GENERAR EL JUEGO DE DATOS ALEATORIO
# ------------------------------------------------------------
#
# Sabemos por el análisis previo del problema que los valores enteros
# alcanzables están entre -69 y 77.
#
# Por tanto, generamos valores objetivo dentro de ese intervalo.
#
# La cantidad de datos generados será 15.
#
# La semilla será 27 para que el resultado sea reproducible.
datos_entrada = generar_datos_entrada_aleatorios(
    minimo=-69,
    maximo=77,
    cantidad=20,
    semilla=1
)


# Mostramos el juego de datos generado.
print("Juego de datos aleatorio generado:")
print(datos_entrada)

print()


# ------------------------------------------------------------
# 3. APLICAR EL ALGORITMO AL JUEGO DE DATOS
# ------------------------------------------------------------
#
# Ahora recorremos cada valor objetivo de la lista datos_entrada.
# Para cada objetivo, buscamos si aparece en el diccionario soluciones.
#
# Esta parte responde a la pregunta 11.
print("Aplicación del algoritmo al juego de datos:")
print()

for objetivo in datos_entrada:

    # Si el objetivo está en el diccionario, tenemos una expresión válida.
    if objetivo in soluciones:
        print(objetivo, "->", soluciones[objetivo])

    # Si no está en el diccionario, no hay solución encontrada para ese valor.
    else:
        print(objetivo, "-> No se ha encontrado solución")