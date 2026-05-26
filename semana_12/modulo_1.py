import struct
import random
import os



FORMATO_REGISTRO = '<i30s24s16sB'
TAM_REGISTRO     = struct.calcsize(FORMATO_REGISTRO)
TAM_DNI          = 4 
TAM_APELLIDO     = 30
TAM_NOMBRE       = 24
TAM_TELEFONO     = 16
TAM_PRIORIDAD    = 1


#consiga A)

def empaquetar_pacientes(dni, apellido, nombre, telefono, prioridad):
    apellido_b = apellido.encode('utf-8')[:TAM_APELLIDO]
    nombre_b = nombre.encode('utf-8')[:TAM_NOMBRE]
    telefono_b = telefono.encode('utf-8')[:TAM_TELEFONO]
    return struct.pack(FORMATO_REGISTRO, dni, apellido_b, nombre_b, telefono_b, prioridad)

def desempaquetar_pacientes(registro_bytes):
    dni, apellido_b, nombre_b, telefono_b, prioridad = struct.unpack(FORMATO_REGISTRO, registro_bytes)
    return {
        "dni": dni,
        "apellido": apellido_b.rstrip(b'\x00').decode('utf-8'),
        "nombre": nombre_b.rstrip(b'\x00').decode('utf-8'),
        "telefono": telefono_b.rstrip(b'\x00').decode('utf-8'),
        "prioridad": prioridad
    }


#consiga B)

def crear_archivo_paciente(ruta, lista_pacientes):
    with open(ruta, 'wb') as f:
        for paciente in lista_pacientes:
            registro = empaquetar_pacientes(
                paciente['dni'],
                paciente['apellido'],
                paciente['nombre'],
                paciente['telefono'],
                paciente['prioridad']
            )
            f.write(registro)

def leer_paciente(archivo, k):
    with open(archivo, 'rb') as f:
        f.seek(k * TAM_REGISTRO)
        registro_bytes = f.read(TAM_REGISTRO)
        if len(registro_bytes) < TAM_REGISTRO:
            raise IndexError("Índice fuera de rango")
        return desempaquetar_pacientes(registro_bytes)
    
