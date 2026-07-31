from itertools import permutations
from fractions import Fraction


# DATOS DEL PROBLEMA

# Cifras disponibles: del 1 al 9. (excluido el cero).
digitos = range(1, 10)

# Operadores disponibles: usar estos cuatro operadores solo una vez en cada expresión.
operadores = ['+', '-', '*', '/']


# Función para evaluar una expresión
def evaluar_expresion(cifras, ops):
    """
    Evalúa una expresión formada por 5 cifras y 4 operadores.
    Se utiliza Fraction para evitar errores de precisión en las divisiones.
    """

    # Lista donde iremos guardando los términos ya cerrados.
    terminos = []

    # Lista de signos asociados a los términos.
    # El primer término es positivo.
    signos = [1]

    # Primer término con la primera cifra.
    termino_actual = Fraction(cifras[0])

    # Recorremos los operadores junto con las cifras restantes.
    # Si cifras = (4, 2, 6, 3, 1) y ops = ('+', '-', '/', '*')
    # entonces zip(ops, cifras[1:]) produce:
    #   ('+', 2), ('-', 6), ('/', 3), ('*', 1)
    for operador, cifra in zip(ops, cifras[1:]):

        # Convertimos la cifra a Fraction para que todas las operaciones se hagan con aritmética exacta.
        cifra = Fraction(cifra)

        # Si el operador es multiplicación, actualizamos el término actual.
        # No cerramos el término porque puede seguir habiendo multiplicaciones o divisiones a continuación.
        if operador == '*':
            termino_actual = termino_actual * cifra

        # Si el operador es división, hacemos lo mismo.
        elif operador == '/':
            termino_actual = termino_actual / cifra

        # Si aparece una suma, significa que el término actual ya queda cerrado.
        # Lo guardamos y empezamos un nuevo término positivo.
        elif operador == '+':
            terminos.append(termino_actual)
            signos.append(1)
            termino_actual = cifra

        # Si aparece una resta, también cerramos el término actual.
        # El nuevo término tendrá signo negativo.
        elif operador == '-':
            terminos.append(termino_actual)
            signos.append(-1)
            termino_actual = cifra

    # Al terminar el bucle, queda el último término pendiente de guardar.
    terminos.append(termino_actual)

    # Sumamos todos los términos teniendo en cuenta sus signos.
    resultado = sum(signo * termino for signo, termino in zip(signos, terminos))

    return resultado


# Funcion para construir la expresión como texto
def construir_expresion(cifras, ops):
    """
    Construye una cadena de texto a partir de las cifras y operadores.
    """

    expresion = ""

    # Añadimos cifra y operador de forma alterna.
    for i in range(4):
        expresion += str(cifras[i]) + ops[i]

    # Añadimos la última cifra.
    expresion += str(cifras[4])

    return expresion


# Algoritmo de Fuerza Bruta

def resolver_por_fuerza_bruta():
    """
    Función que resuelve el problema probando todas las expresiones válidas.
    - Genera todas las permutaciones de 5 cifras distintas.
    - Genera todas las permutaciones de los 4 operadores.
    - Construye y evalúa cada expresión.
    - Guarda los resultados enteros.
    - Calcula el mínimo, el máximo y comprueba si están todos los enteros entre ambos.
    """

    # Conjunto donde almacenaremos los resultados enteros obtenidos.
    # Usamos set porque evita duplicados automáticamente.
    resultados_enteros = set()

    # Inicializamos mínimo y máximo.
    minimo = float('inf')
    maximo = float('-inf')

    # Variables para guardar una expresión que produzca el mínimo y el máximo.
    expresion_minimo = ""
    expresion_maximo = ""

    # Contador de expresiones evaluadas.
    contador_expresiones = 0

    # Generamos todas las permutaciones de 5 cifras distintas.
    # Usando permutations(digitos, 5) que genera todas las formas posibles
    # de elegir y ordenar 5 cifras diferentes entre 1 y 9.
    # Como son permutaciones, no se repiten cifras dentro de la tupla.
    for cifras in permutations(digitos, 5):

        # Para cada grupo de cifras, generamos todas las formas de ordenar los cuatro operadores.
        # Usamos otra vez permutations(operadores, 4) que genera las 24 formas posibles
        # de ordenar '+', '-', '*' y '/' sin repetir ninguno.
        for ops in permutations(operadores, 4):

            # Cada combinación de cifras y operadores representa una expresión válida.
            contador_expresiones += 1

            # Evaluamos la expresión.
            valor = evaluar_expresion(cifras, ops)

            # Solo estamos interesados en los resultados enteros.
            # Como valor es Fraction, es entero si su denominador es 1.
            if valor.denominator == 1:

                # Convertimos el resultado a entero.
                valor_entero = int(valor)

                # Guardamos el resultado en el conjunto.
                resultados_enteros.add(valor_entero)

                # Construimos la expresión como texto, para poder mostrarla si es mínimo o máximo.
                expresion = construir_expresion(cifras, ops)

                # Actualizamos el mínimo si corresponde.
                if valor_entero < minimo:
                    minimo = valor_entero
                    expresion_minimo = expresion

                # Actualizamos el máximo si corresponde.
                if valor_entero > maximo:
                    maximo = valor_entero
                    expresion_maximo = expresion

    # Comprobación de los valores enteros entre mínimo y máximo
    # Lista para guardar los enteros que falten, si es que falta alguno.
    faltan = []

    # Recorremos todos los enteros entre minimo y maximo.
    for numero in range(minimo, maximo + 1):

        # Si un número no está en el conjunto de resultados, significa que no se ha podido obtener.
        if numero not in resultados_enteros:
            faltan.append(numero)

    # Devolvemos todos los resultados relevantes en un diccionario.
    return {
        "contador_expresiones": contador_expresiones,
        "minimo": minimo,
        "maximo": maximo,
        "expresion_minimo": expresion_minimo,
        "expresion_maximo": expresion_maximo,
        "resultados_enteros": resultados_enteros,
        "faltan": faltan
    }


# PROGRAMA PRINCIPAL

# Ejecutamos el algoritmo de fuerza bruta.
resultado = resolver_por_fuerza_bruta()

# Mostramos los resultados principales.
print("Número total de expresiones evaluadas:")
print(resultado["contador_expresiones"])

print()

print("Valor mínimo encontrado:")
print(resultado["minimo"])

print("Expresión que genera el mínimo:")
print(resultado["expresion_minimo"])

print()

print("Valor máximo encontrado:")
print(resultado["maximo"])

print("Expresión que genera el máximo:")
print(resultado["expresion_maximo"])

print()

print("Cantidad de valores enteros distintos obtenidos:")
print(len(resultado["resultados_enteros"]))

print()

# Comprobamos si están todos los enteros entre mínimo y máximo.
if len(resultado["faltan"]) == 0:
    print("Sí, se pueden obtener todos los valores enteros entre el mínimo y el máximo.")
else:
    print("No se pueden obtener todos los valores enteros entre el mínimo y el máximo.")
    print("Valores que faltan:")
    print(resultado["faltan"])