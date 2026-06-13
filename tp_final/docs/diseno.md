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

### 1.2. Datos de entrada

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

### 1.4. Casos de análisis

> Construir casos exhaustivos: escenarios normales, casos límite y casos
> extremos. Cada caso indica una entrada concreta y la salida que debería
> producir. Estos casos se usan luego para probar el programa.

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
| [codificar]  | [Vuelve una cadena a bytes de longitud fija]           | [Milagros Argañin] |
| [decodificar]| [Convierte bytes a cadena eliminando bytes de relleno]           | [Milagros Argañin] |
| [es_flotante_valido]  | [Verifica que una cadena sea un número real no negativo]           | [Milagros Argañin] |
| [inicializar_archivos]  | [Crea el directorio y los archivos binarios si faltan]           | [Tomás Rodriguez] |
| [cargar_indice]  | [Transforma el binario de productos en diccionario para acceder en O(1)]           | [Tomás Rodriguez] |
| [leer_producto_en]  | [Busca el producto en el archivo binario por su "indice" y lo decodifica]           | [Tomás Rodriguez] |
| [escribir_producto_en]  | [Actualizar o escribir un registro de producto en una posición específica del archivo binario]           | [Milagros Argañin] |
| [agregar_producto_al_archivo]  | [Se añade al archivo binario el producto añadido en la funcion agregar_producto]           | [Milagros Argañin] |
| [guardar_movimiento]  | [Añade un registro de movimiento al final de binario de historial]           | [Milagros Argañin] |
| [agregar_producto]  | [Se solicita la información para un nuevo producto y si es valido se lo añade al archivo binario a traves de la funcion agregar_producto_al_archivo]           | [Tomás Rodriguez] |
| [registrar_entrada]  | [Incrementa en stock en el archivo binario y registra la entrada en el historial]           | [Milagros Argañin] |
| [registrar_salida]  | [Si la salida es mayor que la cantidad se rechaza la salida sino se registra la salida]           | [Milagros Argañin] |
| [alertas_reposicion]  | [Recorre los productos y dice cuales estan por debajo de su mínimo]           | [Tomás Rodriguez] |
| [ver_historial]  | [Ver todos los movimientos de entrada y salidad de UN producto]           | [Tomás Rodriguez] |
| [ordenamiento_insercion]  | [Ordena una lista de tuplas a traves del algoritmo de insercion]           | [Milagros Argañin] |
| [listar_inventario]  | [Desde el archivo binario carga los productos ordenados segun un criterio dado]           | [Milagros Argañin] |
| [valorizar_inventario]  | [Calcula cuanto vale el total del inventarío]           | [Tomás Rodriguez] |
| [estadisticas_inventario]  | [Clasifica el stock dependiendo su cantidad entr normal, critico o sin existencia]           | [Tomás Rodriguez] |
| [reporte_rotacion]  | [Lee el historial de movimientos y y genera un ranking de movimientos]           | [Tomás Rodriguez] |
| [mostrar_menu]  | [Imprime el menu con todas las condiciones]           | [Milagros Argañin] |

### 2.4. Pseudocódigo

> Diseño del algoritmo en pseudocódigo (en español) o en literate programming,
> antes de codificar. El pseudocódigo permite razonar la solución sin la
> distracción de la sintaxis.

```
  =============================================================================
   FUNCIONES AUXILIARES DE CODIFICACION
  =============================================================================

  FUNCION codificar(texto, longitud)

      // Convertir el texto a bytes UTF-8
      bytes_texto ← convertir_a_bytes_UTF8(texto)

      // Truncar a la longitud máxima permitida
      bytes_texto ← primeros(longitud, bytes_texto)

      // Completar con bytes nulos hasta alcanzar la longitud deseada
      MIENTRAS longitud(bytes_texto) < longitud HACER
          agregar_byte_nulo(bytes_texto)
      FIN MIENTRAS

      RETORNAR bytes_texto

  FIN FUNCION

  FUNCION decodificar(datos)

      // Convertir los bytes a texto UTF-8
      texto ← convertir_a_texto_UTF8(datos)

      // Eliminar bytes nulos del final
      texto ← eliminar_caracteres_finales(texto, '\0')

      // Eliminar espacios al inicio y al final
      texto ← eliminar_espacios_extremos(texto)

      RETORNAR texto

  FIN FUNCION

  FUNCION es_flotante_valido(cadena)

      SI cadena está vacía ENTONCES
          RETORNAR FALSO
      FIN SI

      // Eliminar la primera aparición de un punto decimal
      sin_punto ← reemplazar_primera_ocurrencia(cadena, ".", "")

      // Verificar que el resto sean dígitos y que haya como máximo un punto
      SI es_numerico(sin_punto) Y contar_ocurrencias(cadena, ".") ≤ 1 ENTONCES
          RETORNAR VERDADERO
      SINO
          RETORNAR FALSO
      FIN SI

  FIN FUNCION

  =============================================================================
   FUNCIONES DE INICIALIZACION
  =============================================================================

  FUNCION inicializar_archivos
 
      SI el directorio de datos no existe ENTONCES
          crear el directorio de datos
      FIN SI
 
      SI el archivo de productos no existe ENTONCES
          crear un archivo binario vacío de productos
      FIN SI
 
      SI el archivo de movimientos no existe ENTONCES
          crear un archivo binario vacío de movimientos
      FIN SI
 
  FIN FUNCION

  =============================================================================
   FUNCIONES DE PERSISTENCIA — ARCHIVO DE PRODUCTOS
  =============================================================================

  FUNCION cargar_indice
 
      indice ← diccionario vacío
      offset ← 0
 
      abrir archivo de productos en modo lectura binaria
      dato ← leer un registro de tamaño TAMANO_PRODUCTO
 
      MIENTRAS dato no esté vacío HACER
 
          campos ← desempaquetar dato según FORMATO_PRODUCTO
          codigo ← decodificar el primer campo
 
          indice[codigo] ← offset
 
          offset ← offset + TAMANO_PRODUCTO
          dato ← leer siguiente registro
 
      FIN MIENTRAS
 
      cerrar archivo
 
      RETORNAR indice
 
  FIN FUNCION

  FUNCION leer_producto_en(offset)
 
      abrir archivo de productos en modo lectura binaria
 
      posicionarse en offset
      dato ← leer un registro de tamaño TAMANO_PRODUCTO
 
      cerrar archivo
 
      campos ← desempaquetar dato según FORMATO_PRODUCTO
 
      RETORNAR (
          decodificar código,
          decodificar descripción,
          stock,
          mínimo,
          precio
      )
 
  FIN FUNCION

  FUNCION escribir_producto_en(producto, offset)
 
      dato ← empaquetar:
          código codificado
          descripción codificada
          stock
          mínimo
          precio
 
      abrir archivo de productos en modo lectura/escritura binaria
 
      posicionarse en offset
      escribir dato
 
      cerrar archivo
 
  FIN FUNCION

  FUNCION agregar_producto_al_archivo(producto)
 
      dato ← empaquetar:
          código codificado
          descripción codificada
          stock
          mínimo
          precio
 
      offset ← tamaño actual del archivo de productos
 
      abrir archivo de productos en modo agregar binario
 
      escribir dato al final del archivo
 
      cerrar archivo
 
      RETORNAR offset
 
  FIN FUNCION

  =============================================================================
   FUNCIONES DE PERSISTENCIA — ARCHIVO DE MOVIMIENTOS
  =============================================================================

  FUNCION guardar_movimiento(codigo, tipo, cantidad)
 
      dato ← empaquetar:
          código codificado
          tipo codificado
          cantidad
 
      abrir archivo de movimientos en modo agregar binario
 
      escribir dato al final del archivo
 
      cerrar archivo
 
  FIN FUNCION

  =============================================================================
   FUNCIONES DE GESTION DE PRODUCTOS
  =============================================================================

  FUNCION agregar_producto(indice)
 
      mostrar título "AGREGAR PRODUCTO"
 
      codigo ← ingresar código del producto
 
      SI codigo está vacío ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      SI codigo existe en indice ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      descripcion ← ingresar descripción del producto
 
      SI descripcion está vacía ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      stock_str ← ingresar cantidad en stock inicial
      stock_min_str ← ingresar stock mínimo
      precio_str ← ingresar precio unitario
 
      enteros_validos ← stock_str y stock_min_str contienen solo dígitos
      precio_valido ← verificar si precio_str representa un flotante válido
 
      SI NO (enteros_validos Y precio_valido) ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      producto ← (
          codigo,
          descripcion,
          convertir stock_str a entero,
          convertir stock_min_str a entero,
          convertir precio_str a real
      )
 
      offset ← agregar_producto_al_archivo(producto)
 
      indice[codigo] ← offset
 
      mostrar mensaje de éxito
 
  FIN FUNCION

  =============================================================================
   FUNCIONES DE MOVIMIENTOS DE MERCADERIA
  =============================================================================

  FUNCION registrar_entrada(indice)
 
      mostrar título "REGISTRAR ENTRADA DE MERCADERÍA"
 
      codigo ← ingresar código del producto
      cantidad_str ← ingresar cantidad a ingresar
 
      cantidad_invalida ← cantidad_str no es numérico
                           O cantidad_str convertido a entero ≤ 0
 
      SI cantidad_invalida ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      SI codigo no existe en indice ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      cantidad ← convertir cantidad_str a entero
      offset ← indice[codigo]
 
      producto ← leer_producto_en(offset)
 
      nuevo_stock ← stock actual + cantidad
 
      actualizado ← (
          codigo,
          descripcion,
          nuevo_stock,
          stock_minimo,
          precio
      )
 
      escribir_producto_en(actualizado, offset)
 
      guardar_movimiento(codigo, "E", cantidad)
 
      mostrar mensaje de éxito con nuevo_stock
 
  FIN FUNCION

  FUNCION registrar_salida(indice)
 
      mostrar título "REGISTRAR SALIDA DE MERCADERÍA"
 
      codigo ← ingresar código del producto
      cantidad_str ← ingresar cantidad a retirar
 
      cantidad_invalida ← cantidad_str no es numérico
                           O cantidad_str convertido a entero ≤ 0
 
      SI cantidad_invalida ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      SI codigo no existe en indice ENTONCES
          mostrar mensaje de error
          TERMINAR FUNCION
      FIN SI
 
      cantidad ← convertir cantidad_str a entero
      offset ← indice[codigo]
 
      producto ← leer_producto_en(offset)
 
      SI stock actual < cantidad ENTONCES
          mostrar mensaje de rechazo por stock insuficiente
          mostrar stock disponible y cantidad solicitada
          TERMINAR FUNCION
      FIN SI
 
      nuevo_stock ← stock actual - cantidad
 
      actualizado ← (
          codigo,
          descripcion,
          nuevo_stock,
          stock_minimo,
          precio
      )
 
      escribir_producto_en(actualizado, offset)
 
      guardar_movimiento(codigo, "S", cantidad)
 
      mostrar mensaje de éxito con nuevo_stock
 
      SI nuevo_stock < stock_minimo ENTONCES
          mostrar advertencia de stock por debajo del mínimo
      FIN SI
 
  FIN FUNCION

  =============================================================================
   FUNCIONES DE CONSULTA Y ALERTA
  =============================================================================

  FUNCION alertas_reposicion(indice)
 
      mostrar título "ALERTAS DE REPOSICIÓN"
 
      contador ← 0
 
      PARA CADA codigo EN indice HACER
 
          producto ← leer_producto_en(indice[codigo])
 
          SI stock actual < stock mínimo ENTONCES
              mostrar datos del producto
              contador ← contador + 1
          FIN SI
 
      FIN PARA
 
      SI contador = 0 ENTONCES
          mostrar mensaje indicando que todos los productos
          presentan niveles óptimos de stock
      FIN SI
 
  FIN FUNCION

  FUNCION ver_historial(indice)
 
      mostrar título "HISTORIAL DE MOVIMIENTOS"
 
      codigo ← ingresar código del producto
 
      SI codigo no existe en indice ENTONCES
          mostrar mensaje de error
          RETORNAR
      FIN SI
 
      encontrado ← FALSO
      numero ← 1
 
      mostrar encabezado del historial
 
      abrir archivo de movimientos en modo lectura binaria
 
      dato ← leer un registro de tamaño TAMANO_MOVIMIENTO
 
      MIENTRAS dato no esté vacío HACER
 
          campos ← desempaquetar dato según FORMATO_MOVIMIENTO
 
          cod_mov ← decodificar código del movimiento
          tipo ← decodificar tipo de movimiento
          cant ← cantidad del movimiento
 
          SI cod_mov = codigo ENTONCES
 
              SI tipo = "E" ENTONCES
                  tipo_texto ← "Entrada"
              SINO
                  tipo_texto ← "Salida"
              FIN SI
 
              mostrar numero, tipo_texto y cant
 
              encontrado ← VERDADERO
              numero ← numero + 1
 
          FIN SI
 
          dato ← leer siguiente registro
 
      FIN MIENTRAS
 
      cerrar archivo
 
      SI encontrado = FALSO ENTONCES
          mostrar mensaje indicando que no existen movimientos
          para el producto
      FIN SI
 
  FIN FUNCION

  =============================================================================
   FUNCIONES DE ORDENAMIENTO Y LISTADO
  =============================================================================

  FUNCION ordenamiento_insercion(lista, clave)
 
      ordenada ← copia de lista
 
      i ← 1
 
      MIENTRAS i < longitud(ordenada) HACER
 
          actual ← ordenada[i]
          j ← i - 1
 
          MIENTRAS j ≥ 0 Y ordenada[j][clave] > actual[clave] HACER
 
              ordenada[j + 1] ← ordenada[j]
              j ← j - 1
 
          FIN MIENTRAS
 
          ordenada[j + 1] ← actual
 
          i ← i + 1
 
      FIN MIENTRAS
 
      RETORNAR ordenada
 
  FIN FUNCION

  FUNCION listar_inventario(indice)
 
      mostrar título "LISTADO DE INVENTARIO"
 
      mostrar opciones de ordenamiento
 
      criterio ← ingresar criterio
 
      SI criterio no es "1" Y criterio no es "2" ENTONCES
          mostrar mensaje de error
          RETORNAR
      FIN SI
 
      SI indice está vacío ENTONCES
          mostrar mensaje indicando que el inventario está vacío
          RETORNAR
      FIN SI
 
      productos ← lista vacía
 
      PARA CADA codigo EN indice HACER
 
          agregar leer_producto_en(indice[codigo]) a productos
 
      FIN PARA
 
      SI criterio = "1" ENTONCES
          clave ← 1
      SINO
          clave ← 2
      FIN SI
 
      ordenados ← ordenamiento_insercion(productos, clave)
 
      mostrar encabezado del listado
 
      PARA CADA producto EN ordenados HACER
 
          mostrar código, descripción, stock, mínimo y precio
 
      FIN PARA
 
      mostrar cantidad total de productos
 
  FIN FUNCION

  =============================================================================
   FUNCIONES DE EXTENSION
  =============================================================================

  FUNCION valorizar_inventario(indice)
 
      mostrar título "VALORIZACIÓN DEL INVENTARIO"
 
      SI indice está vacío ENTONCES
          mostrar mensaje indicando que el inventario está vacío
          RETORNAR
      FIN SI
 
      valor_total ← 0
 
      mostrar encabezado de la tabla
 
      PARA CADA codigo EN indice HACER
 
          producto ← leer_producto_en(indice[codigo])
 
          valor_item ← stock × precio_unitario
 
          valor_total ← valor_total + valor_item
 
          mostrar código, descripción, stock,
          precio unitario y valor_item
 
      FIN PARA
 
      mostrar línea separadora
 
      mostrar valor_total
 
  FIN FUNCION

  FUNCION estadisticas_inventario(indice)
 
      mostrar título "ESTADÍSTICAS DEL DEPÓSITO"
 
      normal ← 0
      critico ← 0
      sin_stock ← 0
 
      PARA CADA codigo EN indice HACER
 
          producto ← leer_producto_en(indice[codigo])
 
          SI stock = 0 ENTONCES
              sin_stock ← sin_stock + 1
 
          SINO SI stock < stock_minimo ENTONCES
              critico ← critico + 1
 
          SINO
              normal ← normal + 1
          FIN SI
 
      FIN PARA
 
      mostrar cantidad de productos con stock óptimo
      mostrar cantidad de productos en nivel crítico
      mostrar cantidad de productos sin existencias
      mostrar total de productos
 
  FIN FUNCION

  FUNCION reporte_rotacion()
 
      mostrar título "REPORTE DE MAYOR ROTACIÓN"
 
      rotacion ← diccionario vacío
 
      abrir archivo de movimientos en modo lectura binaria
 
      dato ← leer un registro de tamaño TAMANO_MOVIMIENTO
 
      MIENTRAS dato no esté vacío HACER
 
          campos ← desempaquetar dato según FORMATO_MOVIMIENTO
 
          codigo ← decodificar código
          cantidad ← cantidad del movimiento
 
          SI codigo existe en rotacion ENTONCES
              rotacion[codigo] ← rotacion[codigo] + cantidad
          SINO
              rotacion[codigo] ← cantidad
          FIN SI
 
          dato ← leer siguiente registro
 
      FIN MIENTRAS
 
      cerrar archivo
 
      SI rotacion está vacío ENTONCES
          mostrar mensaje indicando que no existen movimientos
          RETORNAR
      FIN SI
 
      pares ← lista de pares (codigo, total_movido)
 
      i ← 1
 
      MIENTRAS i < longitud(pares) HACER
 
          actual ← pares[i]
          j ← i - 1
 
          MIENTRAS j ≥ 0 Y pares[j].total_movido < actual.total_movido HACER
 
              pares[j + 1] ← pares[j]
              j ← j - 1
 
          FIN MIENTRAS
 
          pares[j + 1] ← actual
 
          i ← i + 1
 
      FIN MIENTRAS
 
      mostrar encabezado del reporte
 
      PARA CADA (codigo, total) EN pares HACER
 
          mostrar codigo y total
 
      FIN PARA
 
  FIN FUNCION

  =============================================================================
   MENU PRINCIPAL
  =============================================================================

  FUNCION mostrar_menu()
 
      mostrar línea en pantalla
 
      mostrar título del sistema
 
      mostrar línea en pantalla
 
      mostrar "1. Agregar producto"
      mostrar "2. Registrar entrada de mercadería"
      mostrar "3. Registrar salida de mercadería"
      mostrar "4. Alertas de reposición"
      mostrar "5. Listar inventario ordenado"
      mostrar "6. Ver historial de un producto"
      mostrar "7. Valorización del inventario"
      mostrar "8. Estadísticas del depósito"
      mostrar "9. Reporte de mayor rotación"
      mostrar "0. Salir"
 
      mostrar línea en pantalla
 
  FIN FUNCION
```

---

 # 3. Análisis de complejidad

[completar — análisis de la complejidad temporal (y espacial, si es relevante)
de la solución diseñada, con la notación Big-O. Identificar el o los puntos
del programa que dominan el costo.]

---

## 4. Revisión entre pares

> Espacio para registrar la devolución recibida en la revisión entre pares de
> la Semana 13 y los ajustes que se hicieron al diseño a partir de ella.

Luego de la revisión entre pares de la semana 13, decidimos hacer un commit cada integrante, aunque trabajemos juntos por meet e incorporar de inmediato al archivo registro_ia.md lo que le preguntamos a la ia y no hacerlo al finla del proyecto. 
Para la observación de afianzar los casos editamos la seccion 1.4 del archivo diseno.md

---

*Proyecto Final Integrador · Fundamentos de Programación · FIUBA*
