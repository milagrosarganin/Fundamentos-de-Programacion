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

[completar — qué enfoque se eligió para resolver el problema y por qué.
¿Iterativo, recursivo, divide y vencerás, backtracking? Justificar la elección.]

### 2.2. Estructuras de datos

[completar — qué estructuras de datos se usan (listas, tuplas, diccionarios,
conjuntos, archivos) y por qué cada una es la adecuada para lo que representa.
La elección de la estructura es una decisión de diseño que se evalúa.]

### 2.3. Descomposición modular

[completar — en qué funciones se descompone el problema. Para cada función:
nombre, qué subtarea resuelve, y qué integrante la tiene a cargo. Una buena
descomposición reparte el trabajo y reduce los conflictos de fusión.]

| Función      | Subtarea que resuelve | A cargo de  |
|--------------|-----------------------|-------------|
| [completar]  | [completar]           | [completar] |
| [completar]  | [completar]           | [completar] |

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
