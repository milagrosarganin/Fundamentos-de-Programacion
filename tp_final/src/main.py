# =============================================================================
#  Proyecto Final Integrador  -  Fundamentos de Programacion / Algoritmos y
#  Programacion I  -  Carrera de Informatica  -  FIUBA
#
#  Dominio B: Gestor de inventario de un deposito
#
#  Politica ante salida que excede el stock: RECHAZO.
#  El sistema no permite registrar una salida que generaria stock negativo.
#  Fundamento: un deposito no puede entregar mercaderia inexistente; el
#  registro de faltantes requiere una operacion administrativa separada.
#
#  Modulos del proyecto:
#    config.py      — constantes globales (rutas, formatos, separadores)
#    archivos.py    — persistencia binaria y helpers de codificacion
#    operaciones.py — logica de negocio (altas, movimientos, consultas)
#    main.py        — menu de consola y flujo principal  ← este archivo
# =============================================================================

from config import TITULO, SEPARADOR
from archivos import inicializar_archivos, cargar_indice
from operaciones import (
    agregar_producto,
    registrar_entrada,
    registrar_salida,
    alertas_reposicion,
    listar_inventario,
    ver_historial,
    valorizar_inventario,
    estadisticas_inventario,
    reporte_rotacion,
)


# =============================================================================
#  MENU
# =============================================================================

def mostrar_menu():
    '''
    Descripcion: Imprime el menu principal con todas las opciones disponibles.
    Precondicion: Ninguna.
    Postcondicion: El menu queda visible en la consola; no modifica ningun
        estado del programa ni de los archivos.
    '''
    print()
    print(SEPARADOR)
    print(f"  {TITULO}")
    print(SEPARADOR)
    print("    1. Agregar producto")
    print("    2. Registrar entrada de mercaderia")
    print("    3. Registrar salida de mercaderia")
    print("    4. Alertas de reposicion")
    print("    5. Listar inventario ordenado")
    print("    6. Ver historial de un producto")
    print("    7. Valorizacion del inventario")
    print("    8. Estadisticas del deposito")
    print("    9. Reporte de mayor rotacion")
    print("    0. Salir")
    print(SEPARADOR)


# =============================================================================
#  SECCION ALGORITMICA  (programa principal)
#  Prologo — Resolucion — Epilogo
# =============================================================================

# --- Prologo ---

print(SEPARADOR)
print(f"  {TITULO}")
print(f"  FIUBA  -  Fundamentos de Programacion")
print(SEPARADOR)

inicializar_archivos()
indice = cargar_indice()
print(f"  Inventario cargado: {len(indice)} producto(s).")

# --- Resolucion ---

opcion = ""
while opcion != "0":
    mostrar_menu()
    opcion = input("  Seleccione una opcion: ").strip()

    if opcion == "1":
        agregar_producto(indice)
    elif opcion == "2":
        registrar_entrada(indice)
    elif opcion == "3":
        registrar_salida(indice)
    elif opcion == "4":
        alertas_reposicion(indice)
    elif opcion == "5":
        listar_inventario(indice)
    elif opcion == "6":
        ver_historial(indice)
    elif opcion == "7":
        valorizar_inventario(indice)
    elif opcion == "8":
        estadisticas_inventario(indice)
    elif opcion == "9":
        reporte_rotacion()
    elif opcion != "0":
        print("  Opcion no valida. Intente nuevamente.")

# --- Epilogo ---

print()
print(SEPARADOR)
print("  Sistema cerrado. Hasta luego.")
print(SEPARADOR)
