# =============================================================================
#  config.py — Constantes globales del sistema
#  Fuente unica de verdad: rutas, formatos binarios y constantes de pantalla.
#  No importa ningun modulo propio del proyecto.
# =============================================================================

import struct
import os

TITULO = "Gestor de Inventario de un Deposito"

_DIR_RAIZ  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_DIR_DATOS = os.path.join(_DIR_RAIZ, "data")

ARCHIVO_PRODUCTOS   = os.path.join(_DIR_DATOS, "inventario.bin")
ARCHIVO_MOVIMIENTOS = os.path.join(_DIR_DATOS, "movimientos.bin")

# Registro de producto: codigo(10s) | descripcion(50s) | stock(i) | minimo(i) | precio(d)
# Prefijo '=' desactiva el relleno de alineacion → tamano fijo y portable
FORMATO_PRODUCTO = "=10s50siid"
TAMANO_PRODUCTO  = struct.calcsize(FORMATO_PRODUCTO)

# Registro de movimiento: codigo(10s) | tipo(1s) | cantidad(i)
# tipo: b'E' = entrada, b'S' = salida
FORMATO_MOVIMIENTO = "=10s1si"
TAMANO_MOVIMIENTO  = struct.calcsize(FORMATO_MOVIMIENTO)

LINEA     = "-" * 62
SEPARADOR = "=" * 62
