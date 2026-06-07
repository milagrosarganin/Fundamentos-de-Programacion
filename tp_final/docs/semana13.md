# Fase 1 — Semana 13: Análisis y Diseño

## 1. Descripción del problema

**Dominio:** Gestor de inventario de un depósito.

El sistema permite registrar productos con su stock, anotar entradas y salidas de mercadería,
detectar productos que requieren reposición y consultar el historial de movimientos.
La interacción es completamente por consola; la persistencia se realiza mediante archivos binarios.

**Política ante salida que excede el stock:** RECHAZO.
El sistema no permite registrar una salida que generaría stock negativo. Un depósito no puede
entregar mercadería inexistente; el registro de faltantes requiere una operación administrativa
separada.

---

## 2. Núcleo obligatorio implementado

- Persistencia de productos en archivo binario de registros de longitud fija.
- Registro de movimientos de entrada y salida con efecto sobre el stock.
- Índice en memoria (`diccionario`) para localizar un producto por código en O(1).
- Detección de productos cuyo stock cayó por debajo del mínimo.
- Listado del inventario ordenado por descripción o por cantidad en stock.
- Menú de consola que articula todas las operaciones.

## 3. Extensiones implementadas

- Valorización del inventario (suma de `stock × precio` de cada producto).
- Historial de movimientos persistente con consulta por producto.
- Reporte de productos de mayor rotación a partir del historial.
- Rechazo de salidas que exceden el stock (política documentada).
- Estadísticas del depósito por estado de stock.

---

## 4. Estructuras de datos

| Estructura | Uso | Justificación |
|---|---|---|
| Archivo binario (`inventario.bin`) | Persistencia de productos | Registros de longitud fija permiten acceso directo por offset |
| Archivo binario (`movimientos.bin`) | Historial de movimientos | Solo se necesita agregar al final; sin modificaciones posteriores |
| Diccionario `{codigo: offset}` | Índice en memoria | Búsqueda O(1) por código sin recorrer el archivo completo |
| Tupla `(codigo, descripcion, stock, minimo, precio)` | Representación de un producto en memoria | Inmutable y de tamaño fijo; se reconstruye al leer del archivo |

---

## 5. Descomposición modular

| Función | Subtarea que resuelve | A cargo de |
|---|---|---|
| `inicializar_archivos()` | Crea directorio y archivos si no existen | [completar] |
| `cargar_indice()` | Lee el archivo binario y construye el diccionario de índice | [completar] |
| `leer_producto_en(offset)` | Lee y decodifica un registro por su posición en el archivo | [completar] |
| `escribir_producto_en(producto, offset)` | Sobreescribe un registro existente en su posición | [completar] |
| `_agregar_producto_al_archivo(producto)` | Agrega un registro nuevo al final del archivo | [completar] |
| `guardar_movimiento(codigo, tipo, cantidad)` | Persiste un movimiento en el historial binario | [completar] |
| `agregar_producto(indice)` | Valida y registra un nuevo producto | [completar] |
| `registrar_entrada(indice)` | Incrementa el stock y guarda el movimiento tipo E | [completar] |
| `registrar_salida(indice)` | Descuenta el stock (si hay suficiente) y guarda el movimiento tipo S | [completar] |
| `alertas_reposicion(indice)` | Detecta y muestra productos por debajo del mínimo | [completar] |
| `ver_historial(indice)` | Muestra todos los movimientos de un producto dado | [completar] |
| `ordenamiento_insercion(lista, clave)` | Ordena una lista de productos por un campo dado | [completar] |
| `listar_inventario(indice)` | Muestra el inventario completo ordenado por criterio elegido | [completar] |
| `valorizar_inventario(indice)` | Calcula y muestra el valor total del stock | [completar] |
| `estadisticas_inventario(indice)` | Clasifica productos por estado de stock | [completar] |
| `reporte_rotacion()` | Muestra ranking de productos por volumen de movimientos | [completar] |
| `mostrar_menu()` | Imprime el menú principal de opciones | [completar] |

---

## 6. Pseudocódigo

```
FUNCIÓN Principal()
    Imprimir encabezado del sistema
    Llamar inicializar_archivos()
    indice = Llamar cargar_indice()
    Imprimir cantidad de productos cargados

    opcion = ""
    MIENTRAS opcion != "0":
        Llamar mostrar_menu()
        Leer opcion

        SI opcion == "1": Llamar agregar_producto(indice)
        SI opcion == "2": Llamar registrar_entrada(indice)
        SI opcion == "3": Llamar registrar_salida(indice)
        SI opcion == "4": Llamar alertas_reposicion(indice)
        SI opcion == "5": Llamar listar_inventario(indice)
        SI opcion == "6": Llamar ver_historial(indice)
        SI opcion == "7": Llamar valorizar_inventario(indice)
        SI opcion == "8": Llamar estadisticas_inventario(indice)
        SI opcion == "9": Llamar reporte_rotacion()
        SI opcion != "0": Imprimir "Opción no válida"
    FIN MIENTRAS

    Imprimir mensaje de cierre
FIN FUNCIÓN

FUNCIÓN agregar_producto(indice)
    Leer codigo
    SI codigo vacío O codigo ya en indice: Imprimir error y RETORNAR
    Leer descripcion, stock_str, stock_min_str, precio_str
    SI algún valor numérico no es válido: Imprimir error y RETORNAR
    producto = (codigo, descripcion, stock, minimo, precio)
    offset = Llamar _agregar_producto_al_archivo(producto)
    indice[codigo] = offset
FIN FUNCIÓN

FUNCIÓN registrar_entrada(indice)
    Leer codigo y cantidad
    SI cantidad no es entero positivo: RETORNAR
    SI codigo no está en indice: RETORNAR
    producto = Llamar leer_producto_en(indice[codigo])
    nuevo_stock = producto.stock + cantidad
    Llamar escribir_producto_en(producto actualizado, offset)
    Llamar guardar_movimiento(codigo, "E", cantidad)
FIN FUNCIÓN

FUNCIÓN registrar_salida(indice)
    Leer codigo y cantidad
    SI cantidad no es entero positivo: RETORNAR
    SI codigo no está en indice: RETORNAR
    producto = Llamar leer_producto_en(indice[codigo])
    SI producto.stock < cantidad:
        Imprimir "RECHAZO: stock insuficiente" y RETORNAR
    nuevo_stock = producto.stock - cantidad
    Llamar escribir_producto_en(producto actualizado, offset)
    Llamar guardar_movimiento(codigo, "S", cantidad)
    SI nuevo_stock < producto.minimo: Imprimir advertencia
FIN FUNCIÓN

FUNCIÓN listar_inventario(indice)
    Leer criterio (1=descripcion, 2=stock)
    productos = lista de todos los productos leídos del archivo
    clave = 1 si criterio "1", sino 2
    ordenados = Llamar ordenamiento_insercion(productos, clave)
    Imprimir tabla formateada de ordenados
FIN FUNCIÓN

FUNCIÓN ordenamiento_insercion(lista, clave)
    ordenada = copia de lista
    i = 1
    MIENTRAS i < longitud(ordenada):
        actual = ordenada[i]
        j = i - 1
        MIENTRAS j >= 0 Y ordenada[j][clave] > actual[clave]:
            ordenada[j+1] = ordenada[j]
            j = j - 1
        FIN MIENTRAS
        ordenada[j+1] = actual
        i = i + 1
    FIN MIENTRAS
    RETORNAR ordenada
FIN FUNCIÓN
```

---

## 7. Casos de análisis

| # | Tipo | Entrada | Salida esperada | Observaciones |
|---|---|---|---|---|
| 1 | Normal | Registrar entrada de 50 unidades del producto "ABC" con stock inicial 20 | Stock pasa a 70; se registra movimiento tipo E | [completar] |
| 2 | Límite | Registrar salida de exactamente el stock disponible (stock = cantidad solicitada) | Stock queda en 0; no aparece alerta de mínimo si mínimo es 0 | [completar] |
| 3 | Límite | Registrar salida que deja el stock igual al mínimo | Stock igual a mínimo; no aparece en alertas de reposición | [completar] |
| 4 | Límite | Registrar salida que deja el stock por debajo del mínimo (pero no en cero) | Salida registrada; producto aparece en alertas de reposición | [completar] |
| 5 | Extremo | Registrar salida mayor que el stock disponible | RECHAZO: "stock insuficiente"; archivo sin modificar | Política de rechazo |
| 6 | Extremo | Agregar producto con código duplicado | Error: "ya existe un producto con ese código" | [completar] |
| 7 | Extremo | Ingresar cantidad no numérica (ej. "abc") | Error: "los valores numéricos no son válidos" | [completar] |

---

## 8. Avance del módulo principal

- `main.py` contiene la implementación completa del sistema.
- Todos los casos del núcleo obligatorio están operativos.
- Las cinco extensiones opcionales están implementadas.

---

## 9. Inicio del registro de uso de IA

Ver [`docs/registro_ia.md`](registro_ia.md).
