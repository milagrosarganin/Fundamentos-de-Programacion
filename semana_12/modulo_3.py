import struct
from modulo_1 import desempaquetar_pacientes

FORMATO_REGISTRO = '<i30s24s16sB'
TAM_REGISTRO = struct.calcsize(FORMATO_REGISTRO)

def merge_sort(secuencia, criterio):
    """Ordena una secuencia comparándola por divide y vencerás.

    Precondición: secuencia es una lista de elementos comparables entre sí.
    Postcondición: devuelve una nueva lista con los mismos elementos en
                   orden no decreciente; secuencia no se modifica.
    Complejidad: O(n log n) en tiempo, O(n) en espacio auxiliar.
    """
    # --- Prólogo: caso base de la recursión -------------------------
    if len(secuencia) <= 1:
        return list(secuencia)             # copia defensiva

    # --- Resolución: dividir, recurrir, combinar --------------------
    medio = len(secuencia) >> 1            # división por 2 a nivel ALU
    mitad_izq = merge_sort(secuencia[:medio], criterio)
    mitad_der = merge_sort(secuencia[medio:], criterio)
    resultado = _fusionar(mitad_izq, mitad_der, criterio)

    # --- Epílogo: devolver la solución del problema -----------------
    return resultado

def _fusionar(izq, der, criterio):
    """Fusiona dos listas ordenadas en una sola lista ordenada y estable."""
    resultado = []
    i, j = 0, 0
    n_izq, n_der = len(izq), len(der)

    while i < n_izq and j < n_der:
        # Comparamos directamente el valor dentro del diccionario del paciente
        if izq[i][criterio] <= der[j][criterio]: 
            resultado.append(izq[i])
            i += 1
        else:
            resultado.append(der[j])
            j += 1
    resultado.extend(izq[i:])
    resultado.extend(der[j:])

    return resultado

def listar_pacientes_ordenados(ruta, criterio):
    pacientes = []
    with open(ruta, 'rb') as f:
        registro_bytes = f.read(TAM_REGISTRO)
        while len(registro_bytes) == TAM_REGISTRO:
            pacientes.append(desempaquetar_pacientes(registro_bytes))
            registro_bytes = f.read(TAM_REGISTRO)
            
    if criterio == "apellido":
        return merge_sort(pacientes, "apellido")
    elif criterio == "prioridad":
        pacientes_por_apellido = merge_sort(pacientes, "apellido")
        return merge_sort(pacientes_por_apellido, "prioridad")


#consigna F)

'''(f) Implementar listar_pacientes_ordenados(ruta, criterio) que devuelva una lista de diccionarios con los datos de los pacientes ordenados por el criterio indicado (apellido o prioridad). En caso de empate en prioridad, ordenar por apellido.

este programa debe leer el archivo binario, desempaquetar los registros, ordenarlos por el criterio indicado y devolver la lista ordenada. Para ordenar, se puede usar cualquier algoritmo de ordenamiento eficiente (como merge sort) o la función sorted() de Python con una función clave personalizada.'''