# Diseño del algoritmo

> Documento de diseño del proyecto final. Sigue las fases de Pólya a escala de
> proyecto. Se construye principalmente en la Semana 13 (Análisis y diseño) y se
> ajusta a medida que el proyecto avanza.
>
> Completar las secciones marcadas con `[completar]` y eliminar este bloque.

---

## 1. Análisis del problema

### 1.1. Enunciado

Un sistema que controla el stock de productos de un depósito: registra entradas y salidas de mercadería, mantiene actualizadas las existencias y alerta sobre los productos que requieren reposición.
Núcleo obligatorio
● Persistencia de los productos en un archivo binario de registros de longitud fija (código, descripción, cantidad en stock, stock mínimo, precio unitario).
● Registro de movimientos de entrada y de salida de mercadería, cada uno con su efecto sobre el stock del producto correspondiente.
● Índice en memoria (diccionario) para localizar un producto por su código en tiempo O(1).
● Detección de los productos cuyo stock cayó por debajo de su stock mínimo (productos a reponer).
● Listado del inventario ordenado por descripción o por cantidad en stock, con un algoritmo de ordenamiento implementado por el equipo.
● Menú de consola que articule todas las operaciones. Extensiones opcionales (elegir al menos una)
● Valorización del inventario: cálculo del valor total del stock (suma de cantidad por precio de cada producto).
● Historial de movimientos persistente, con consulta de los movimientos de un producto dado.
● Reporte de los productos de mayor rotación a partir del historial de movimientos.
● Registro de una salida que excede el stock disponible: el sistema debe rechazarla o registrar el faltante, según una política definida y documentada por el equipo.
● Estadísticas del depósito: cantidad de productos por rango de precio o por estado de stock.
Contenidos del curso involucrados
Archivos binarios y módulo struct (S8); diccionarios como índice (S10); algoritmos de ordenamiento (S6, S12); búsqueda (S5); patrón de recorrido con acumulador para la valorización (S3, S11); modularización (S4).
Cota de alcance
El proyecto no incluye interfaz gráfica (la interacción es por consola), ni base de datos (la persistencia es mediante archivos), ni acceso por red ni integración con sistemas de facturación.

### 1.2. Datos de entrada

[completar — qué datos recibe el programa, de qué tipo, con qué restricciones,
y por qué medio (teclado, archivo, etc.).]

### 1.3. Resultados esperados

[completar — qué produce el programa y en qué forma se presenta.]

### 1.4. Casos de análisis

> Construir casos exhaustivos: escenarios normales, casos límite y casos
> extremos. Cada caso indica una entrada concreta y la salida que debería
> producir. Estos casos se usan luego para probar el programa.

| # | Tipo     | Entrada      | Salida esperada | Observaciones |
|---|----------|--------------|-----------------|---------------|
| 1 | Normal   | [completar]  | [completar]     | [completar]   |
| 2 | Límite   | [completar]  | [completar]     | [completar]   |
| 3 | Extremo  | [completar]  | [completar]     | [completar]   |

---

## 2. Diseño de la solución

### 2.1. Estrategia general

Se eligió un enfoque **iterativo y modular**. El programa gira en torno a un bucle de menú principal que delega cada operación a una función especializada. No se usa recursión porque el problema no tiene estructura recursiva natural (no hay árboles ni backtracking). El principio "divide y vencerás" se aplica a nivel arquitectónico: cada operación del sistema queda encapsulada en su propia función, lo que reduce la complejidad de cada unidad y facilita el reparto del trabajo entre los integrantes.

La decisión central del diseño es mantener un **índice en memoria** (diccionario código → posición en el archivo) que se carga al inicio del programa. Esto separa la responsabilidad de búsqueda rápida (O(1) con el diccionario) de la responsabilidad de persistencia (archivo binario de registros fijos). Para el listado ordenado, los registros se vuelcan a una lista en memoria y se ordenan con el algoritmo propio del equipo, ya que el volumen de un depósito real cabe en RAM y no justifica una estrategia externa.

### 2.2. Estructuras de datos

| Estructura | Rol en el sistema | Justificación |
|---|---|---|
| Archivo binario de registros fijos (`inventario.bin`) | Persistencia de productos (código, descripción, stock, stock mínimo, precio) | Los registros de longitud fija permiten acceso aleatorio por offset: conocida la posición, la lectura/escritura es O(1) sin recorrer el archivo completo. |
| Diccionario en memoria `{codigo: offset}` | Índice para localizar un producto por código | Cumple el requisito explícito del enunciado: búsqueda O(1). Se reconstruye al iniciar el programa y se actualiza en cada alta. |
| Archivo binario de registros fijos (`historial.bin`) | Historial de movimientos de entrada y salida | Append secuencial natural para un log de auditoría; el formato binario fijo permite escaneo eficiente al consultar el historial de un producto. |
| Lista temporal de tuplas | Ordenamiento e impresión del inventario | Se carga desde el archivo solo para mostrar el listado ordenado; no se persiste. Permite aplicar el algoritmo de ordenamiento del equipo sobre datos en memoria. |

### 2.3. Descomposición modular

| Función      | Subtarea que resuelve | A cargo de  |
|--------------|-----------------------|-------------|
| [codificar]  | [Vuelve una cadena a bytes de longitud fija]           | [Tomás Rodriguez] |
| [decodificar]| [Convierte bytes a cadena eliminando bytes de relleno]           | [Milagros Argañin] |
| [es_flotante_valido]  | [Verifica que una cadena sea un número real no negativo]           | [Tomás Rodriguez] |
| [inicializar_archivos]  | [Crea el directorio y los archivos binarios si faltan]           | [Milagros Argañin] |
| [cargar_indice]  | [Transforma el binario de productos en diccionario para acceder en O(1)]           | [Tomás Rodriguez] |
| [leer_producto_en]  | [Busca el producto en el archivo binario por su "indice" y lo decodifica]           | [completar] |
| [escribir_producto_en]  | [completar]           | [completar] |
| [agregar_producto_al_archivo]  | [Se añade al archivo binario el producto añadido en la funcion agregar_producto]           | [completar] |
| [guardar_movimiento]  | [Añade un registro de movimiento al final de binario de historial]           | [completar] |
| [agregar_producto]  | [Se solicita la información para un nuevo producto y si es valido se lo añade al archivo binario a traves de la funcion agregar_producto_al_archivo]           | [completar] |
| [registrar_entrada]  | [Incrementa en stock en el archivo binario y registra la entrada en el historial]           | [completar] |
| [registrar_salida]  | [Si la salida es mayor que la cantidad se rechaza la salida sino se registra la salida]           | [completar] |
| [alertas_reposicion]  | [Recorre los productos y dice cuales estan por debajo de su mínimo]           | [completar] |
| [ver_historial]  | [Ver todos los movimientos de entrada y salidad de UN producto]           | [completar] |
| [ordenamiento_insercion]  | [Ordena una lista de tuplas a traves del algoritmo de insercion]           | [completar] |
| [listar_inventario]  | [Desde el archivo binario carga los productos ordenados segun un criterio dado]           | [completar] |
| [valorizar_inventario]  | [Calcula cuanto vale el total del inventarío]           | [completar] |
| [estadisticas_inventario]  | [Clasifica el stock dependiendo su cantidad entr normal, critico o sin existencia]           | [completar] |
| [reporte_rotacion]  | [Lee el historial de movimientos y y genera un ranking de movimientos]           | [completar] |
| [mostrar_menu]  | [Imprime el menu con todas las condiciones]           | [completar] |



### 2.4. Pseudocódigo

> Diseño del algoritmo en pseudocódigo (en español) o en literate programming,
> antes de codificar. El pseudocódigo permite razonar la solución sin la
> distracción de la sintaxis.

```
FUNCIÓN Principal()
    opcion = 0
    bucle mientras opcion != 7:
        Mostrar "=== GESTOR DE INVENTARIO ==="
        Mostrar "1. Registrar Entrada de Mercadería"
        Mostrar "2. Registrar Salida de Mercadería"
        Mostrar "3. Mostrar Alertas de Reposición"
        Mostrar "4. Ver Historial de Movimientos de un Producto"
        Mostrar "5. Valorización del Inventario"
        Mostrar "6. Estadísticas del Inventario"
        Mostrar "7. Salir"
        Leer opcion

        SI opcion == 1:
            Llamar Registrar_Entrada()
        SINO SI opcion == 2:
            Llamar Registrar_Salida()
        SINO SI opcion == 3:
            Llamar Alertas_Reposicion()
        SINO SI opcion == 4:
            Llamar Ver_Historial()
        SINO SI opcion == 5:
            Llamar Valorizacion_Inventario()
        SINO SI opcion == 6:
            Llamar Estadisticas_Inventario()
        SINO SI opcion == 7:
            Mostrar "Cerrando el sistema..."
        SINO:
            Mostrar "Opción no válida. Intente nuevamente."
        FIN SI
    fin bucle
FIN FUNCIÓN

FUNCIÓN Registrar_Entrada()
    Leer codigo_producto
    Leer cantidad_ingresada
    
    SI cantidad_ingresada <= 0:
        Mostrar "Error: La cantidad debe ser mayor a cero."
        RETORNAR
    FIN SI

    Abrir archivo_inventario en modo lectura/escritura binaria
    posicion = Buscar_Producto(archivo_inventario, codigo_producto)

    SI posicion != NO_ENCONTRADO:
        Leer registro en posicion
        registro.cantidad_en_stock = registro.cantidad_en_stock + cantidad_ingresada
        Escribir registro actualizado en posicion
        
        // Persistencia de la extensión: registrar en historial
        Llamar Guardar_Movimiento(codigo_producto, 'E', cantidad_ingresada)
        Mostrar "Entrada registrada e historial actualizado con éxito."
    SINO:
        Mostrar "El código de producto no existe en el sistema."
    FIN SI

    Cerrar archivo_inventario
FIN FUNCIÓN

FUNCIÓN Registrar_Salida()
    Leer codigo_producto
    Leer cantidad_solicitada

    SI cantidad_solicitada <= 0:
        Mostrar "Error: La cantidad debe ser mayor a cero."
        RETORNAR
    FIN SI

    Abrir archivo_inventario en modo lectura/escritura binaria
    posicion = Buscar_Producto(archivo_inventario, codigo_producto)

    SI posicion != NO_ENCONTRADO:
        Leer registro en posicion
        SI registro.cantidad_en_stock >= cantidad_solicitada:
            registro.cantidad_en_stock = registro.cantidad_en_stock - cantidad_solicitada
            Escribir registro actualizado en posicion
            
            // Persistencia de la extensión: registrar en historial
            Llamar Guardar_Movimiento(codigo_producto, 'S', cantidad_solicitada)
            Mostrar "Salida procesada e historial guardado de forma exitosa."
        SINO:
            Mostrar "Error: Stock insuficiente. Existencias actuales: ", registro.cantidad_en_stock
        FIN SI
    SINO:
        Mostrar "El producto buscado no se encuentra registrado."
    FIN SI

    Cerrar archivo_inventario
FIN FUNCIÓN

FUNCIÓN Alertas_Reposicion()
    Abrir archivo_inventario en modo lectura binaria
    Contador_Alertas = 0
    Mostrar "--- ALERTA DE PRODUCTOS QUE REQUIEREN REPOSICIÓN ---"
    
    Ir al inicio del archivo_inventario
    bucle mientras no sea fin de archivo:
        Leer registro
        SI registro.cantidad_en_stock <= registro.stock_minimo:
            Mostrar "Código: ", registro.codigo, " | Desc: ", registro.descripcion, " | Stock: ", registro.cantidad_en_stock, " | Mínimo: ", registro.stock_minimo
            Contador_Alertas = Contador_Alertas + 1
        FIN SI
    fin bucle

    SI Contador_Alertas == 0:
        Mostrar "Todos los productos presentan niveles óptimos de stock."
    FIN SI

    Cerrar archivo_inventario
FIN FUNCIÓN

FUNCIÓN Valorizacion_Inventario()
    Abrir archivo_inventario en modo lectura binaria
    valor_total_inventario = 0

    Ir al inicio del archivo_inventario
    bucle mientras no sea fin de archivo:
        Leer registro
        // Patrón acumulador multiplicando existencias por precio
        valor_producto = registro.cantidad_en_stock * registro.precio_unitario
        valor_total_inventario = valor_total_inventario + valor_producto
    fin bucle

    Mostrar "El valor total acumulado del inventario asciende a: $", valor_total_inventario
    Cerrar archivo_inventario
FIN FUNCIÓN

FUNCIÓN Estadisticas_Inventario()
    Abrir archivo_inventario en modo lectura binaria
    
    // Inicialización de diccionario contador
    estado_stock = {"Normal": 0, "A reponer": 0, "Sin stock": 0}

    Ir al inicio del archivo_inventario
    bucle mientras no sea fin de archivo:
        Leer registro
        SI registro.cantidad_en_stock == 0:
            estado_stock["Sin stock"] = estado_stock["Sin stock"] + 1
        SINO SI registro.cantidad_en_stock <= registro.stock_minimo:
            estado_stock["A reponer"] = estado_stock["A reponer"] + 1
        SINO:
            estado_stock["Normal"] = estado_stock["Normal"] + 1
        FIN SI
    fin bucle

    Mostrar "--- ESTADÍSTICAS GENERALES DEL DEPÓSITO ---"
    Mostrar "Artículos con Stock Óptimo (Normal): ", estado_stock["Normal"]
    Mostrar "Artículos en Nivel Crítico (A reponer): ", estado_stock["A reponer"]
    Mostrar "Artículos sin Existencias (Sin stock): ", estado_stock["Sin stock"]

    Cerrar archivo_inventario
FIN FUNCIÓN

FUNCIÓN Ver_Historial()
    Leer codigo_buscado
    Abrir archivo_historial en modo lectura binaria
    movimientos_encontrados = FALSO

    Mostrar "--- HISTORIAL DE MOVIMIENTOS - PRODUCTO: ", codigo_buscado, " ---"
    Ir al inicio del archivo_historial

    bucle mientras no sea fin de archivo:
        Leer registro_historial
        SI registro_historial.codigo_producto == codigo_buscado:
            Mostrar "Tipo: ", registro_historial.tipo_movimiento, " | Cantidad: ", registro_historial.cantidad
            movimientos_encontrados = VERDADERO
        FIN SI
    fin bucle

    SI movimientos_encontrados == FALSO:
        Mostrar "No constan registros de movimientos para el código solicitado."
    FIN SI

    Cerrar archivo_historial
FIN FUNCIÓN

FUNCIÓN Buscar_Producto(archivo, codigo_buscado)
    Ir al inicio del archivo
    posicion_actual = 0

    bucle mientras no sea fin de archivo:
        Leer registro
        SI registro.codigo == codigo_buscado:
            Devolver posicion_actual
        FIN SI
        posicion_actual = posicion_actual + TAMAÑO_REGISTRO_PRODUCTO
    fin bucle

    Devolver NO_ENCONTRADO
FIN FUNCIÓN

FUNCIÓN Guardar_Movimiento(codigo, tipo, cantidad)
    Abrir archivo_historial en modo anexar/escritura binaria
    registro_historial.codigo_producto = codigo
    registro_historial.tipo_movimiento = tipo
    registro_historial.cantidad = cantidad
    Escribir registro_historial al final del archivo_historial
    Cerrar archivo_historial
FIN FUNCIÓN
```

---

## 3. Análisis de complejidad

[completar — análisis de la complejidad temporal (y espacial, si es relevante)
de la solución diseñada, con la notación Big-O. Identificar el o los puntos
del programa que dominan el costo.]

---

## 4. Revisión entre pares

> Espacio para registrar la devolución recibida en la revisión entre pares de
> la Semana 13 y los ajustes que se hicieron al diseño a partir de ella.

[completar.]

---

*Proyecto Final Integrador · Fundamentos de Programación · FIUBA*
