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

<<<<<<< HEAD
En el caso de los datos Persistentes el programa los reibe de archivos Binarios, pero para el caso de las funciones el programa recibe datos interactivamente desde el teclado a través de un menú de consola. Los datos esperados según la operación son:

**Agregar producto:**
- Código de producto (cadena, máximo 10 caracteres, no puede estar vacío)
- Descripción (cadena, máximo 50 caracteres, no puede estar vacía)
- Stock inicial (entero no negativo)
- Stock mínimo (entero no negativo)
- Precio unitario (número decimal no negativo)

**Registrar entrada o salida:**
- Código del producto existente (cadena)
- Cantidad (entero positivo > 0)

**Ver historial:**
- Código del producto (cadena)

**Operaciones sin entrada adicional:**
- Alertas de reposición, listado de inventario, valorización, estadísticas, reporte de rotación: se ejecutan sin parámetros adicionales (operan sobre el inventario cargado)

Todas las entradas numéricas se validan antes de procesarse; aquellas que no cumplan con los requisitos generan un mensaje de error y se rechaza la operación.


### 1.3. Resultados esperados

El programa genera salidas por consola y persiste datos en archivos binarios:

**Salidas por consola:**
- Menú interactivo con opciones numeradas (0 a 9)
- Mensajes de confirmación o error al ejecutar cada operación
- Listados con formato de tabla (productos ordenados por descripción o stock)
- Historial de movimientos (tipo, cantidad) de un producto específico
- Alertas de productos bajo stock mínimo
- Valor total del inventario
- Estadísticas de stock (cantidad de productos en stock normal, crítico, sin existencias)
- Ranking de productos por rotación (entrada/salida)

**Persistencia en archivos binarios:**
- `inventario.bin`: registros de productos (código, descripción, stock, stock mínimo, precio)
- `movimientos.bin`: historial de entradas y salidas (código, tipo, cantidad)

**Índice en memoria:**
- Diccionario {código: offset} que se carga al iniciar y permite localizar productos en O(1)
=======
El programa recibe datos por dos medios:

**Por teclado (interacción con el usuario):**

| Dato | Tipo | Restricciones |
|---|---|---|
| Opción de menú | entero | Entre 1 y 7; se rechaza cualquier valor fuera de rango |
| Código de producto | entero | Debe ser positivo; se valida que exista en el índice antes de operar |
| Cantidad de entrada o salida | entero | Debe ser mayor a cero; para salidas no puede superar el stock disponible |
| Criterio de ordenamiento | entero (1 o 2) | 1 = por descripción, 2 = por cantidad en stock |

**Por archivo binario (`inventario.bin`):**

Registros de longitud fija empaquetados con `struct`. Cada registro contiene: código (int), descripción (string de longitud fija), cantidad en stock (int), stock mínimo (int) y precio unitario (float). El archivo se lee al iniciar el programa para construir el índice en memoria.

**Por archivo binario (`historial.bin`):**

Registros de longitud fija con: código de producto (int), tipo de movimiento (char: 'E' o 'S') y cantidad (int). Se lee al consultar el historial de un producto y se escribe al registrar cualquier movimiento.

### 1.3. Resultados esperados

El programa produce los siguientes resultados, todos presentados por consola:

| Operación | Resultado |
|---|---|
| Registrar entrada | Confirmación con el nuevo stock del producto |
| Registrar salida | Confirmación con el nuevo stock, o mensaje de error si el stock es insuficiente |
| Alertas de reposición | Listado de productos con `stock ≤ stock_mínimo`, con código, descripción, stock actual y mínimo |
| Listado de inventario | Tabla de todos los productos ordenada por descripción o por cantidad, según el criterio elegido |
| Valorización | Valor total del inventario (suma de `cantidad × precio` para cada producto) |
| Historial de un producto | Lista de movimientos del producto indicado con tipo ('E'/'S') y cantidad |
| Estadísticas | Cantidad de productos en estado normal, a reponer y sin stock |

Adicionalmente, el programa escribe en `historial.bin` cada movimiento registrado (efecto persistente que no se muestra directamente al usuario).
>>>>>>> 2d8ae34 (registro y s¿diseno sem 14 y correccione sem 13)

### 1.4. Casos de análisis

> Construir casos exhaustivos: escenarios normales, casos límite y casos
> extremos. Cada caso indica una entrada concreta y la salida que debería
> producir. Estos casos se usan luego para probar el programa.

<<<<<<< HEAD
| # | Tipo     | Entrada      | Salida esperada | Observaciones |
|---|----------|--------------|-----------------|---------------|
| 1 | Normal   | Agregar producto: código="PROD001", descripción="Tornillos acero", stock=100, mínimo=20, precio=5.50 | Mensaje de confirmación: "Producto 'PROD001' agregado correctamente." El producto se persiste en inventario.bin y se actualiza el índice en memoria. | Caso típico de alta de producto con datos válidos y completos. Verifica persistencia binaria. |
| 2 | Límite   | Registrar entrada: código="PROD001", cantidad=1 (cantidad mínima válida) | Stock de PROD001 aumenta de 100 a 101. Se registra movimiento 'E' en movimientos.bin. Mensaje: "Entrada registrada. Stock actualizado: 101 unidades." | Prueba el caso límite inferior de cantidad válida (> 0). Una entrada de 1 unidad debe procesarse sin rechazo. |
| 3 | Extremo  | Registrar salida: código="PROD001", cantidad=150 (mayor que stock disponible de 101) | Mensaje de error: "Operacion rechazada: stock insuficiente (politica: RECHAZO). Stock disponible: 101 | Cantidad solicitada: 150". El stock no cambia, no se registra movimiento. | Verifica la política de rechazo ante salida que excede stock. El sistema rechaza la operación sin modificar archivos. |
| 4 | Normal   | Alertas de reposición: inventario contiene productos donde stock < stock_mínimo | Muestra tabla de productos por debajo del mínimo con código, descripción, stock actual y stock mínimo. Ejemplo: "PROD002 | Tuercas | Stock: 8 | Minimo: 15" | Caso de flujo normal: al menos un producto requiere reposición. Verifica detección e impresión del listado de alertas. |
| 5 | Límite   | Ver historial: código="PROD001" que tiene exactamente 2 movimientos (1 entrada + 1 salida) | Tabla con 2 filas: "1 | Entrada | 100" y "2 | Salida | 50". Mensaje de encabezado confirma el código solicitado. | Prueba historial con mínima cantidad de movimientos registrados. Verifica que solo se muestren movimientos del producto buscado. |
| 6 | Extremo  | Ver historial: código="NOEXISTE" que no existe en el inventario | Mensaje de error: "Error: no existe un producto con el codigo 'NOEXISTE'." | Verifica validación: código inexistente rechaza la consulta sin procesar el historial. |
| 7 | Normal   | Valorización del inventario: 3 productos con stock y precios variados (ej: PROD001 stock=101 precio=5.50, PROD002 stock=50 precio=2.00, PROD003 stock=20 precio=10.00) | Tabla detallada con valor por producto (cantidad × precio) y suma total: "Valor total del inventario: $ 755.50" (101×5.50 + 50×2.00 + 20×10.00 = 555.50 + 100 + 200 = 855.50) | Verifica acumulador con patrón multiplicativo. Suma correcta de valorización parcial y total. |
| 8 | Límite   | Estadísticas del inventario: inventario con productos distribuidos en 3 estados (normal, crítico, sin stock) | Resumen: "Productos con stock optimo: 2 | Productos en nivel critico: 1 | Productos sin existencias: 0 | Total de productos: 3" | Frontera entre categorías: stock==mínimo (normal), stock<mínimo (crítico), stock==0 (sin existencias). |
| 9 | Extremo  | Listar inventario ordenado: inventario vacío (sin productos) | Mensaje: "El inventario esta vacio." Sin impresión de tabla. | Caso extremo: operación sobre colección vacía. Verifica control de flujo y evita errores de acceso. |
=======
| # | Tipo | Entrada | Salida esperada | Observaciones |
|---|---|---|---|---|
| 1 | Normal | Registrar entrada: código=101, cantidad=50 (producto existe, stock actual=20) | "Entrada registrada. Stock actualizado: 70 unidades." | Caso típico de reposición de mercadería |
| 2 | Normal | Registrar salida: código=101, cantidad=30 (stock actual=70) | "Salida registrada. Stock actualizado: 40 unidades." | El stock resultante queda por encima del mínimo |
| 3 | Normal | Alertas de reposición con 3 productos: uno con stock=5/mín=10, otro con stock=20/mín=10, otro con stock=0/mín=5 | Lista con los productos de código 1 y 3; el producto 2 no aparece | Solo se listan los que tienen stock ≤ mínimo |
| 4 | Normal | Listado ordenado por descripción con 4 productos cargados | Tabla impresa en orden alfabético por nombre | Verifica el algoritmo de ordenamiento |
| 5 | Normal | Valorización con 3 productos: 10u×$50, 5u×$200, 0u×$300 | "Valor total del inventario: $1500.00" | Acumulador: 500 + 1000 + 0 |
| 6 | Límite | Registrar salida: código=202, cantidad=15 (stock actual=15, mínimo=10) | "Salida registrada. Stock actualizado: 0 unidades." + aparece en alerta de reposición | Stock queda en 0, que es ≤ mínimo |
| 7 | Límite | Registrar salida: código=202, cantidad=10 (stock actual=10, mínimo=10) | "Salida registrada. Stock actualizado: 0 unidades." | Stock queda exactamente en el mínimo; el producto pasa a alerta |
| 8 | Límite | Registrar entrada: código=303, cantidad=1 (cantidad mínima válida) | "Entrada registrada. Stock actualizado: [stock anterior + 1] unidades." | Cantidad mínima aceptable |
| 9 | Límite | Historial de producto con un único movimiento registrado | Se muestra ese único movimiento | Caso borde de lista con un solo elemento |
| 10 | Extremo | Registrar salida: código=101, cantidad=100 (stock actual=20) | "Error: stock insuficiente. Existencias actuales: 20 unidades." | El sistema rechaza la operación; el stock no se modifica |
| 11 | Extremo | Buscar producto con código=999 (no existe en el sistema) | "El producto no se encuentra registrado." | El índice no tiene la clave; no se accede al archivo |
| 12 | Extremo | Ingresar opción de menú = 0 o = 8 | "Opción no válida. Intente nuevamente." | Validación del menú fuera de rango |
| 13 | Extremo | Ingresar cantidad = 0 al registrar un movimiento | "Error: la cantidad debe ser mayor a cero." | Validación de entrada antes de operar |
| 14 | Extremo | Consultar alertas de reposición con todos los productos en stock óptimo | "Todos los productos presentan niveles óptimos de stock." | Recorrido completo sin productos que reportar |
| 15 | Extremo | Iniciar el programa con `inventario.bin` vacío (primer uso) | El menú carga correctamente; el índice queda vacío | `cargar_indice` debe manejar archivo vacío sin error |
>>>>>>> 2d8ae34 (registro y s¿diseno sem 14 y correccione sem 13)

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
