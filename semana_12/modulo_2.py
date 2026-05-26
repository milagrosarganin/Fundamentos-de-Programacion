import struct
import random
import os
from modulo_1 import desempaquetar_pacientes, leer_paciente


FORMATO_REGISTRO = '<i30s24s16sB'
TAM_REGISTRO     = struct.calcsize(FORMATO_REGISTRO)
TAM_DNI          = 4 
TAM_APELLIDO     = 30
TAM_NOMBRE       = 24
TAM_TELEFONO     = 16
TAM_PRIORIDAD    = 1

#consiga C)

def construir_indices(ruta):
    indice_por_dni = {}
    indice_por_apellido = {}
    
    with open(ruta, 'rb') as f:
        k = 0
        registro_bytes = f.read(TAM_REGISTRO)
        while len(registro_bytes) == TAM_REGISTRO:
            paciente = desempaquetar_pacientes(registro_bytes) 
            dni = paciente['dni']
            apellido = paciente['apellido']
            
            # Índice por DNI
            indice_por_dni[dni] = k
            
            # Índice por apellido
            if apellido not in indice_por_apellido:
                indice_por_apellido[apellido] = []
            indice_por_apellido[apellido].append(k)
            
            k += 1
            # Siguiente lectura
            registro_bytes = f.read(TAM_REGISTRO)
            
    return indice_por_dni, indice_por_apellido

#consiga D)

def buscar_por_dni(archivo, indice_por_dni, dni):
    if dni not in indice_por_dni:
        return None
    k = indice_por_dni[dni]
    return leer_paciente(archivo, k)  


     