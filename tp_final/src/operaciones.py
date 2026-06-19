# =============================================================================
#  operaciones.py — Logica de negocio del gestor de inventario
#  Contiene todas las operaciones del dominio: altas, movimientos, consultas
#  y reportes. Cada funcion recibe el indice en memoria y delega la
#  persistencia en el modulo archivos.
#  Importa: config (constantes de pantalla), archivos (I/O binario).
# =============================================================================

import struct

from config import (
    LINEA, SEPARADOR,
    ARCHIVO_MOVIMIENTOS, FORMATO_MOVIMIENTO, TAMANO_MOVIMIENTO,
)
from archivos import (
    codificar, decodificar, es_flotante_valido,
    leer_producto_en, escribir_producto_en,
    agregar_producto_al_archivo, guardar_movimiento,
)


# =============================================================================
#  ORDENAMIENTO
# =============================================================================

def ordenamiento_insercion(lista, clave):
    '''
    Descripcion: Ordena una lista de tuplas de productos de menor a mayor
        segun el indice de campo indicado, usando el algoritmo de insercion.
    Precondicion: lista es una lista de tuplas (codigo, descripcion, stock,
        minimo, precio); clave es 1 (descripcion) o 2 (stock).
    Postcondicion: Retorna una nueva lista ordenada; la lista original no se
        modifica.
    '''
    ordenada = list(lista)
    i = 1
    while i < len(ordenada):
        actual = ordenada[i]
        j      = i - 1
        while j >= 0 and ordenada[j][clave] > actual[clave]:
            ordenada[j + 1] = ordenada[j]
            j -= 1
        ordenada[j + 1] = actual
        i += 1
    return ordenada


# =============================================================================
#  GESTION DE PRODUCTOS
# =============================================================================

def agregar_producto(indice):
    '''
    Descripcion: Solicita los datos de un nuevo producto al usuario, valida
        los campos y lo persiste en el archivo binario y en el indice.
    Precondicion: indice es el diccionario {codigo: offset} actualmente
        cargado en memoria.
    Postcondicion: Si los datos son validos y el codigo no existia, el
        producto queda guardado en el archivo y el indice se actualiza;
        de lo contrario se informa el error sin modificar el estado.
    '''
    print(LINEA)
    print("  AGREGAR PRODUCTO")
    print(LINEA)
    codigo = input("  Codigo (hasta 10 caracteres): ").strip()[:10]

    if not codigo:
        print("  Error: el codigo no puede estar vacio.")
        return

    if codigo in indice:
        print(f"  Error: ya existe un producto con el codigo '{codigo}'.")
        return

    descripcion = input("  Descripcion (hasta 50 caracteres): ").strip()[:50]
    if not descripcion:
        print("  Error: la descripcion no puede estar vacia.")
        return

    stock_str     = input("  Cantidad en stock inicial:         ").strip()
    stock_min_str = input("  Stock minimo:                      ").strip()
    precio_str    = input("  Precio unitario:                   ").strip()

    enteros_validos = stock_str.isdigit() and stock_min_str.isdigit()
    precio_valido   = es_flotante_valido(precio_str)

    if not (enteros_validos and precio_valido):
        print("  Error: los valores numericos ingresados no son validos.")
        return

    producto = (codigo, descripcion, int(stock_str), int(stock_min_str), float(precio_str))
    offset   = agregar_producto_al_archivo(producto)
    indice[codigo] = offset
    print(f"  Producto '{codigo}' agregado correctamente.")


# =============================================================================
#  MOVIMIENTOS DE MERCADERIA
# =============================================================================

def registrar_entrada(indice):
    '''
    Descripcion: Solicita codigo y cantidad; incrementa el stock del producto
        en el archivo binario y registra el movimiento en el historial.
    Precondicion: indice es el diccionario {codigo: offset} actualizado.
    Postcondicion: El stock del producto aumenta en la cantidad indicada y
        queda un registro de tipo 'E' en ARCHIVO_MOVIMIENTOS.
    '''
    print(LINEA)
    print("  REGISTRAR ENTRADA DE MERCADERIA")
    print(LINEA)
    codigo       = input("  Codigo del producto:  ").strip()
    cantidad_str = input("  Cantidad a ingresar:  ").strip()

    cantidad_invalida = (not cantidad_str.isdigit() or int(cantidad_str) <= 0)
    if cantidad_invalida:
        print("  Error: la cantidad debe ser un entero mayor a cero.")
        return

    if codigo not in indice:
        print(f"  Error: no existe un producto con el codigo '{codigo}'.")
        return

    cantidad    = int(cantidad_str)
    offset      = indice[codigo]
    producto    = leer_producto_en(offset)
    nuevo_stock = producto[2] + cantidad
    actualizado = (producto[0], producto[1], nuevo_stock, producto[3], producto[4])

    escribir_producto_en(actualizado, offset)
    guardar_movimiento(codigo, "E", cantidad)
    print(f"  Entrada registrada. Stock actualizado: {nuevo_stock} unidades.")


def registrar_salida(indice):
    '''
    Descripcion: Solicita codigo y cantidad; si el stock es suficiente,
        descuenta la cantidad y registra el movimiento. Si el stock es
        insuficiente, aplica la politica de RECHAZO y no modifica nada.
    Precondicion: indice es el diccionario {codigo: offset} actualizado.
    Postcondicion: Si hay stock suficiente, el stock disminuye y queda un
        registro de tipo 'S' en ARCHIVO_MOVIMIENTOS. Si no hay stock
        suficiente, la operacion se rechaza sin modificar ningun archivo.
    '''
    print(LINEA)
    print("  REGISTRAR SALIDA DE MERCADERIA")
    print(LINEA)
    codigo       = input("  Codigo del producto:  ").strip()
    cantidad_str = input("  Cantidad a retirar:   ").strip()

    cantidad_invalida = (not cantidad_str.isdigit() or int(cantidad_str) <= 0)
    if cantidad_invalida:
        print("  Error: la cantidad debe ser un entero mayor a cero.")
        return

    if codigo not in indice:
        print(f"  Error: no existe un producto con el codigo '{codigo}'.")
        return

    cantidad = int(cantidad_str)
    offset   = indice[codigo]
    producto = leer_producto_en(offset)

    if producto[2] < cantidad:
        print("  Operacion rechazada: stock insuficiente (politica: RECHAZO).")
        print(f"  Stock disponible: {producto[2]}  |  Cantidad solicitada: {cantidad}")
        return

    nuevo_stock = producto[2] - cantidad
    actualizado = (producto[0], producto[1], nuevo_stock, producto[3], producto[4])

    escribir_producto_en(actualizado, offset)
    guardar_movimiento(codigo, "S", cantidad)
    print(f"  Salida registrada. Stock actualizado: {nuevo_stock} unidades.")

    if nuevo_stock < producto[3]:
        print(f"  ATENCION: el stock cayo por debajo del minimo ({producto[3]} unidades).")


# =============================================================================
#  CONSULTAS Y ALERTAS
# =============================================================================

def alertas_reposicion(indice):
    '''
    Descripcion: Recorre el indice y muestra los productos cuyo stock es
        estrictamente menor que su stock minimo.
    Precondicion: indice es el diccionario {codigo: offset} actualizado.
    Postcondicion: Imprime por pantalla los productos a reponer; si todos
        superan su minimo informa que el stock esta en niveles optimos.
    '''
    print(LINEA)
    print("  ALERTAS DE REPOSICION")
    print(LINEA)
    contador = 0
    for codigo in indice:
        producto = leer_producto_en(indice[codigo])
        if producto[2] < producto[3]:
            print(f"  {producto[0]:<12} | {producto[1]:<32} "
                  f"| Stock: {producto[2]:>6} | Minimo: {producto[3]:>6}")
            contador += 1

    if contador == 0:
        print("  Todos los productos presentan niveles optimos de stock.")


def ver_historial(indice):
    '''
    Descripcion: Solicita un codigo de producto y muestra todos sus movimientos
        de entrada y salida registrados en el archivo de historial.
    Precondicion: indice es el diccionario {codigo: offset}; ARCHIVO_MOVIMIENTOS
        existe.
    Postcondicion: Imprime los movimientos del producto o informa que no hay
        registros para ese codigo.
    '''
    print(LINEA)
    print("  HISTORIAL DE MOVIMIENTOS")
    print(LINEA)
    codigo = input("  Codigo del producto: ").strip()

    if codigo not in indice:
        print(f"  Error: no existe un producto con el codigo '{codigo}'.")
        return

    encontrado = False
    numero     = 1
    print(f"  Movimientos del producto '{codigo}':")
    print(f"  {'N':>4}  {'Tipo':<10}  {'Cantidad':>10}")
    print(f"  {'-' * 30}")

    with open(ARCHIVO_MOVIMIENTOS, "rb") as archivo:
        dato = archivo.read(TAMANO_MOVIMIENTO)
        while dato:
            campos  = struct.unpack(FORMATO_MOVIMIENTO, dato)
            cod_mov = decodificar(campos[0])
            tipo    = decodificar(campos[1])
            cant    = campos[2]

            if cod_mov == codigo:
                tipo_texto = "Entrada" if tipo == "E" else "Salida"
                print(f"  {numero:>4}  {tipo_texto:<10}  {cant:>10}")
                encontrado = True
                numero    += 1

            dato = archivo.read(TAMANO_MOVIMIENTO)

    if not encontrado:
        print("  No se encontraron movimientos para este producto.")


# =============================================================================
#  LISTADO Y EXTENSION
# =============================================================================

def listar_inventario(indice):
    '''
    Descripcion: Carga todos los productos desde el archivo, solicita al
        usuario el criterio de ordenamiento y muestra el inventario ordenado.
    Precondicion: indice es el diccionario {codigo: offset} actualizado.
    Postcondicion: Imprime el inventario completo ordenado segun el criterio
        elegido (descripcion o cantidad en stock).
    '''
    print(LINEA)
    print("  LISTADO DE INVENTARIO")
    print(LINEA)
    print("  Ordenar por:")
    print("    1. Descripcion")
    print("    2. Cantidad en stock")
    criterio = input("  Criterio (1 o 2): ").strip()

    if criterio not in ("1", "2"):
        print("  Error: criterio invalido.")
        return

    if not indice:
        print("  El inventario esta vacio.")
        return

    productos = []
    for codigo in indice:
        productos.append(leer_producto_en(indice[codigo]))

    clave    = 1 if criterio == "1" else 2
    ordenados = ordenamiento_insercion(productos, clave)

    print()
    print(f"  {'Codigo':<12} {'Descripcion':<32} {'Stock':>7} {'Minimo':>7} {'Precio':>10}")
    print(f"  {LINEA}")
    for p in ordenados:
        print(f"  {p[0]:<12} {p[1]:<32} {p[2]:>7} {p[3]:>7} {p[4]:>10.2f}")

    print(f"\n  Total de productos: {len(ordenados)}")


def valorizar_inventario(indice):
    '''
    Descripcion: Calcula el valor total del inventario acumulando el producto
        de stock por precio unitario de cada producto (patron acumulador).
    Precondicion: indice es el diccionario {codigo: offset} actualizado.
    Postcondicion: Imprime el detalle de valorizacion por producto y el total
        acumulado del inventario completo.
    '''
    print(LINEA)
    print("  VALORIZACION DEL INVENTARIO")
    print(LINEA)

    if not indice:
        print("  El inventario esta vacio.")
        return

    valor_total = 0.0
    print(f"  {'Codigo':<12} {'Descripcion':<30} {'Stock':>7} {'Precio':>10} {'Valor':>12}")
    print(f"  {LINEA}")

    for codigo in indice:
        p            = leer_producto_en(indice[codigo])
        valor_item   = p[2] * p[4]
        valor_total += valor_item
        print(f"  {p[0]:<12} {p[1]:<30} {p[2]:>7} {p[4]:>10.2f} {valor_item:>12.2f}")

    print(f"  {LINEA}")
    print(f"  Valor total del inventario:  $ {valor_total:>12.2f}")


def estadisticas_inventario(indice):
    '''
    Descripcion: Recorre todos los productos y los clasifica por estado de
        stock: normal, critico (por debajo del minimo) o sin existencias.
    Precondicion: indice es el diccionario {codigo: offset} actualizado.
    Postcondicion: Imprime un resumen con la cantidad de productos en cada
        categoria de estado de stock.
    '''
    print(LINEA)
    print("  ESTADISTICAS DEL DEPOSITO")
    print(LINEA)

    estado = {"normal": 0, "critico": 0, "sin_stock": 0}

    for codigo in indice:
        p = leer_producto_en(indice[codigo])
        if p[2] == 0:
            estado["sin_stock"] += 1
        elif p[2] < p[3]:
            estado["critico"] += 1
        else:
            estado["normal"] += 1

    print(f"  Productos con stock optimo:      {estado['normal']:>5}")
    print(f"  Productos en nivel critico:      {estado['critico']:>5}")
    print(f"  Productos sin existencias:       {estado['sin_stock']:>5}")
    print(f"  Total de productos:              {len(indice):>5}")


def reporte_rotacion():
    '''
    Descripcion: Lee el historial de movimientos, acumula la cantidad total
        movida por producto y muestra un ranking de mayor a menor rotacion.
    Precondicion: ARCHIVO_MOVIMIENTOS existe.
    Postcondicion: Imprime la lista de productos ordenada por volumen total
        de movimientos (entradas + salidas acumuladas).
    '''
    print(LINEA)
    print("  REPORTE DE MAYOR ROTACION")
    print(LINEA)

    rotacion = {}
    with open(ARCHIVO_MOVIMIENTOS, "rb") as archivo:
        dato = archivo.read(TAMANO_MOVIMIENTO)
        while dato:
            campos = struct.unpack(FORMATO_MOVIMIENTO, dato)
            codigo = decodificar(campos[0])
            cant   = campos[2]
            if codigo in rotacion:
                rotacion[codigo] += cant
            else:
                rotacion[codigo] = cant
            dato = archivo.read(TAMANO_MOVIMIENTO)

    if not rotacion:
        print("  No hay movimientos registrados aun.")
        return

    pares = ordenamiento_insercion(
        [(cod, tot) for cod, tot in rotacion.items()], 1
    )
    pares.reverse()

    print(f"  {'Codigo':<12} {'Total movido':>14}")
    print(f"  {'-' * 28}")
    for codigo, total in pares:
        print(f"  {codigo:<12} {total:>14}")
