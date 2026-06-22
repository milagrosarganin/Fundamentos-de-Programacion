# =============================================================================
#  archivos.py — Persistencia y codificacion binaria
#  Maneja toda la interaccion con los archivos binarios del sistema.
#  Importa: config (constantes de formato y ruta).
# =============================================================================

import struct
import os

from config import (
    ARCHIVO_PRODUCTOS, ARCHIVO_MOVIMIENTOS,
    FORMATO_PRODUCTO, TAMANO_PRODUCTO,
    FORMATO_MOVIMIENTO, TAMANO_MOVIMIENTO,
)


# =============================================================================
#  HELPERS DE CODIFICACION
# =============================================================================

def codificar(texto, longitud):
    '''
    Descripcion: Convierte una cadena a bytes de longitud fija, truncando si
        excede la longitud y rellenando con bytes nulos si es mas corta.
    Precondicion: texto es una cadena; longitud es un entero positivo.
    Postcondicion: Retorna un objeto bytes de exactamente longitud bytes.
    '''
    return texto.encode("utf-8")[:longitud].ljust(longitud, b"\x00")


def decodificar(datos):
    '''
    Descripcion: Convierte bytes a cadena eliminando el relleno de bytes nulos.
    Precondicion: datos es un objeto bytes.
    Postcondicion: Retorna la cadena decodificada sin bytes nulos al final.
    '''
    return datos.decode("utf-8").rstrip("\x00").strip()


def es_flotante_valido(cadena):
    '''
    Descripcion: Verifica si una cadena representa un numero real no negativo
        sin recurrir a try/except.
    Precondicion: cadena es una cadena de texto.
    Postcondicion: Retorna True si cadena puede interpretarse como float >= 0.
    '''
    if not cadena:
        return False
    sin_punto = cadena.replace(".", "", 1)
    return sin_punto.isdigit() and cadena.count(".") <= 1


# =============================================================================
#  INICIALIZACION
# =============================================================================

def inicializar_archivos():
    '''
    Descripcion: Crea el directorio de datos y los archivos binarios si
        todavia no existen en el sistema de archivos.
    Precondicion: Las constantes de ruta estan definidas correctamente.
    Postcondicion: El directorio data/ existe y ambos archivos binarios
        estan presentes (pueden estar vacios).
    '''
    try:
        _dir_datos = os.path.dirname(ARCHIVO_PRODUCTOS)
        if not os.path.exists(_dir_datos):
            os.makedirs(_dir_datos)

        if not os.path.exists(ARCHIVO_PRODUCTOS):
            with open(ARCHIVO_PRODUCTOS, "wb") as _archivo:
                pass

        if not os.path.exists(ARCHIVO_MOVIMIENTOS):
            with open(ARCHIVO_MOVIMIENTOS, "wb") as _archivo:
                pass

    except OSError as e:
        print(f"  Error al inicializar los archivos del sistema: {e}")
        print("  Verifique los permisos de la carpeta data/.")


# =============================================================================
#  ARCHIVO DE PRODUCTOS
# =============================================================================

def cargar_indice():
    '''
    Descripcion: Lee el archivo binario de productos de principio a fin y
        construye el diccionario indice {codigo: offset} que permite
        localizar cualquier registro en tiempo O(1).
    Precondicion: ARCHIVO_PRODUCTOS existe (puede estar vacio).
    Postcondicion: Retorna un diccionario con los codigos de producto como
        claves y los desplazamientos en bytes como valores. Si ocurre un
        error de lectura retorna un diccionario vacio.
    '''
    indice = {}
    offset = 0
    try:
        with open(ARCHIVO_PRODUCTOS, "rb") as archivo:
            dato = archivo.read(TAMANO_PRODUCTO)
            while dato:
                campos = struct.unpack(FORMATO_PRODUCTO, dato)
                codigo = decodificar(campos[0])
                indice[codigo] = offset
                offset += TAMANO_PRODUCTO
                dato = archivo.read(TAMANO_PRODUCTO)
    except OSError as e:
        print(f"  Error al leer el archivo de productos: {e}")
    except struct.error as e:
        print(f"  Error: el archivo de productos contiene datos corruptos: {e}")
    return indice


def leer_producto_en(offset):
    '''
    Descripcion: Lee y decodifica el registro de producto ubicado en el
        desplazamiento indicado del archivo binario.
    Precondicion: offset es un multiplo no negativo de TAMANO_PRODUCTO;
        el archivo tiene datos en esa posicion.
    Postcondicion: Retorna una tupla (codigo, descripcion, stock, minimo,
        precio) con todos los campos decodificados, o None si ocurre un error.
    '''
    try:
        with open(ARCHIVO_PRODUCTOS, "rb") as archivo:
            archivo.seek(offset)
            dato = archivo.read(TAMANO_PRODUCTO)
        campos = struct.unpack(FORMATO_PRODUCTO, dato)
        return (decodificar(campos[0]), decodificar(campos[1]),
                campos[2], campos[3], campos[4])
    except OSError as e:
        print(f"  Error al leer el archivo de productos: {e}")
    except struct.error as e:
        print(f"  Error: registro corrupto en offset {offset}: {e}")
    return None


def escribir_producto_en(producto, offset):
    '''
    Descripcion: Codifica y escribe un registro de producto en el
        desplazamiento indicado del archivo binario.
    Precondicion: producto es (codigo, descripcion, stock, minimo, precio);
        offset es un multiplo no negativo de TAMANO_PRODUCTO; el archivo existe.
    Postcondicion: El registro queda actualizado en la posicion offset del
        archivo binario de productos. Si ocurre un error informa al usuario.
    '''
    try:
        dato = struct.pack(
            FORMATO_PRODUCTO,
            codificar(producto[0], 10),
            codificar(producto[1], 50),
            producto[2],
            producto[3],
            producto[4]
        )
        with open(ARCHIVO_PRODUCTOS, "r+b") as archivo:
            archivo.seek(offset)
            archivo.write(dato)
    except OSError as e:
        print(f"  Error al escribir en el archivo de productos: {e}")
    except struct.error as e:
        print(f"  Error al codificar el registro del producto: {e}")


def agregar_producto_al_archivo(producto):
    '''
    Descripcion: Codifica y agrega un nuevo registro de producto al final
        del archivo binario.
    Precondicion: producto es (codigo, descripcion, stock, minimo, precio);
        el archivo ARCHIVO_PRODUCTOS existe.
    Postcondicion: El registro queda escrito al final del archivo; retorna
        el offset donde comienza ese registro, o -1 si ocurre un error.
    '''
    try:
        dato = struct.pack(
            FORMATO_PRODUCTO,
            codificar(producto[0], 10),
            codificar(producto[1], 50),
            producto[2],
            producto[3],
            producto[4]
        )
        offset = os.path.getsize(ARCHIVO_PRODUCTOS)
        with open(ARCHIVO_PRODUCTOS, "ab") as archivo:
            archivo.write(dato)
        return offset
    except OSError as e:
        print(f"  Error al guardar el producto en el archivo: {e}")
    except struct.error as e:
        print(f"  Error al codificar el producto: {e}")
    return -1


# =============================================================================
#  ARCHIVO DE MOVIMIENTOS
# =============================================================================

def guardar_movimiento(codigo, tipo, cantidad):
    '''
    Descripcion: Codifica y agrega un registro de movimiento al final del
        archivo binario de historial.
    Precondicion: codigo tiene hasta 10 caracteres; tipo es 'E' o 'S';
        cantidad es un entero positivo.
    Postcondicion: El movimiento queda persistido al final de
        ARCHIVO_MOVIMIENTOS. Si ocurre un error informa al usuario.
    '''
    try:
        dato = struct.pack(
            FORMATO_MOVIMIENTO,
            codificar(codigo, 10),
            codificar(tipo, 1),
            cantidad
        )
        with open(ARCHIVO_MOVIMIENTOS, "ab") as archivo:
            archivo.write(dato)
    except OSError as e:
        print(f"  Advertencia: no se pudo guardar el movimiento en el historial: {e}")
    except struct.error as e:
        print(f"  Advertencia: error al codificar el movimiento: {e}")
