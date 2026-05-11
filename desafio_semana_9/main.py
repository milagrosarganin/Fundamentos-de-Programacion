import random
import itertools

def combinaciones_rec(elementos, k):
    """
    Genera todas las combinaciones de k elementos de una lista dada y cuenta las hojas del árbol de recursión.
    
    Esta función utiliza un enfoque recursivo para calcular las combinaciones. Cada llamada recursiva
    representa un nodo en el árbol de recursión, y las hojas corresponden a los casos base donde k=0.
    
    Parámetros:
    elementos (list): Lista de elementos de los cuales se generan las combinaciones.
    k (int): Número de elementos en cada combinación.
    
    Retorna:
    tuple: Una tupla con dos elementos:
        - list: Lista de tuplas, cada una representando una combinación.
        - int: Número total de hojas en el árbol de recursión (casos base alcanzados).
    """
    # Caso base: si k es 0, retornamos una lista con una tupla vacía y 1 hoja
    if k == 0:
        return [()], 1
    
    # Caso de rechazo: si no hay suficientes elementos, retornamos lista vacía y 0 hojas
    if len(elementos) < k:
        return [], 0
    
    # Inicializamos la lista de resultados y el contador de hojas
    resultado = []
    total_hojas = 0
    
    # Iteramos sobre cada elemento posible como primer elemento de la combinación
    for i in range(len(elementos)):
        elemento_actual = elementos[i]
        
        # Llamada recursiva para obtener combinaciones del resto de elementos con k-1
        combinaciones_restantes, hojas = combinaciones_rec(elementos[i+1:], k-1)
        
        # Acumulamos el número de hojas de esta rama recursiva
        total_hojas += hojas
        
        # Para cada combinación restante, agregamos el elemento actual al inicio
        for combinacion in combinaciones_restantes:
            tupla = tuple([elemento_actual])
            resultado.append(tupla + combinacion)
    
    # Retornamos las combinaciones encontradas y el total de hojas
    return resultado, total_hojas

# Ejemplo de uso: generar combinaciones de 2 elementos de la lista ["1","2","3","4"]
resultado, hojas = combinaciones_rec(["1","2","3","4"], 2)
print(f"Combinaciones: {resultado}")
print(f"Hojas del árbol de recursión: {hojas}")

# Comparación con la función built-in de    
print(list(itertools.combinations(["1","2","3","4"], 2)))