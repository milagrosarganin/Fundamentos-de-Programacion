#Problema 1

'''Genere una lista ordenada de  n enteros distintos usando  random.sample(range(1, 10 * 
n), n) seguido de sort(), con n = 1000. Fijar la semilla con random.seed(42).'''

import random
data = random.seed(42) #fijo la semilla

def ordenar(n):
    """
    Genera una lista ordenada de n enteros distintos elegidos aleatoriamente.
    
    Precondición: n debe ser un número entero positivo.
    Postcondición: Retorna una lista de longitud n con enteros aleatorios 
                   únicos ordenados de forma ascendente.
    """
    lista = random.sample(range(1, 10*n), n) #creo la lista
    lista.sort() #ordeno la lista
    return lista

prueba= ordenar(1000)
print(prueba)   


#problema 2

'''Para cada función de búsqueda, busque 10 claves: 5 presentes en la lista (elegidas con `random.sample(datos, 5)`) y 5 ausentes (enteros negativos). Verificar que ambas funciones retornan los mismos resultados.'''

# def encontrar_numero(numero, lista):
#     """
#     Verifica si un número se encuentra dentro de una lista.
    
#     Precondición: lista es una secuencia y numero es el valor a buscar.
#     Postcondición: Retorna True si el número está presente en la lista, 
#                    de lo contrario retorna False.
#     """
#     if numero in lista:
#         return True
#     else:
#         return False

# def busqueda_lineal(numero, lista, contar=False):
#     """
#     Busca un número en una lista validando primero su existencia.
    
#     Precondición: lista es una secuencia y numero es el valor a buscar.
#     Postcondición: Retorna el índice de la primera ocurrencia del número 
#                    en la lista, o -1 si no se encuentra.
#     """
#     condición = encontrar_numero(numero, lista)
#     print(condición)    
#     if condición:
#         posicion = lista.index(numero)
#         return posicion
#     else:
#         return -1

def busqueda_lineal_enumerate(numero, lista, contar=False):
    """
    Busca un número en una lista utilizando búsqueda lineal iterativa.
    
    Precondición: lista es una secuencia y numero es el valor a buscar.
    Postcondición: Retorna el índice del número en la lista si lo encuentra, 
                   o -1 si el número no está presente.
    """
    for indice, valor in enumerate(lista):
        if valor == numero:
            if contar:
                return indice, indice - 1
            else:
                return indice 
    return -1  # Si termina el bucle y no lo encontró


def busqueda_binaria(numero, lista, contar=False):
    """
    Busca un número en una lista utilizando el algoritmo de búsqueda binaria.
    
    Precondición: lista debe ser una secuencia ordenada.
    Postcondición: Retorna el índice donde se encuentra el número, o -1 
                   si no está presente en la lista.
    """
    lista.sort()  # La lista DEBE estar ordenada
    inicio = 0
    fin = len(lista) - 1
    contador = 0
    while inicio <= fin:
        medio = (inicio + fin) // 2
        valor_medio = lista[medio]
        contador +=1

        if valor_medio == numero:
            if contar:
                return medio, contador
            else:   
                return medio  # Encontrado! Devolvemos la posición
        
        if numero < valor_medio:
            fin = medio - 1  # Buscamos en la mitad izquierda
        else:
            inicio = medio + 1  # Buscamos en la mitad derecha

    return -1  # No se encontró


prueba2 = int(input("ingrese un numero a buscar: "))

print(busqueda_lineal_enumerate(prueba2, prueba, contar = True))
print(busqueda_binaria(prueba2, prueba, contar = True))


#bloque b problema 2

'''1. Reutilice la lista ordenada del Problema 1 (misma semilla, mismo `n`).
2. Busque las mismas 10 claves del Problema 1 con la versión recursiva y verifique que los resultados son idénticos a los de la versión iterativa.
3. Para tres valores de `n` (100, 1000, 10000), medir la profundidad máxima de recursión alcanzada (usar un parámetro `nivel` que se incrementa en cada llamada) y compararla con ⌈log₂(n)⌉.'''


def busqueda_binaria_rec(lista, numero, inicio, fin, nivel=0, contar=False):
    # Caso base: región vacía
    if inicio > fin:
        if contar:
            return -1, nivel
        else:
            return -1

    medio = (inicio + fin) // 2
    # Caso base: encontrado
    if lista[medio] == numero:

        if contar:
            return medio, nivel
        else:
            return medio
    # Caso recursivo: buscar en la mitad correspondiente
    elif numero < lista[medio]:
        return busqueda_binaria_rec(lista, numero, inicio, medio - 1, nivel=nivel+1, contar=True)
    else:
        return busqueda_binaria_rec(lista, numero, medio + 1, fin, nivel=nivel+1, contar=True)
    
prueba_3 = int(input("ingrese un numero a buscar: "))

print(busqueda_binaria_rec(prueba, prueba_3, 0, len(prueba) - 1, contar=True))