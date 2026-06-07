# Fase 3 — Semana 15: Optimización e Informe Final

## Informe escrito

---

### 1. Descripción del problema y alcance abordado

**Dominio:** Gestor de inventario de un depósito industrial.

El sistema controla el stock de productos: registra entradas y salidas de mercadería, mantiene
actualizadas las existencias en disco y alerta sobre los productos que requieren reposición.
La interacción es completamente por consola; no incluye interfaz gráfica, base de datos ni
acceso por red.

**Núcleo implementado:**
- Persistencia de productos en archivo binario de registros de longitud fija.
- Registro de movimientos de entrada y salida con efecto sobre el stock.
- Índice en memoria (diccionario) para localizar un producto por código en O(1).
- Detección de productos cuyo stock cayó por debajo del mínimo.
- Listado del inventario ordenado por descripción o por cantidad en stock, con Insertion Sort.
- Menú de consola que articula todas las operaciones.

**Extensiones implementadas (las cinco disponibles):**
- Valorización del inventario.
- Historial de movimientos persistente con consulta por producto.
- Reporte de productos de mayor rotación.
- Política de rechazo ante salidas que exceden el stock.
- Estadísticas del depósito por estado de stock.

---

### 2. Diseño de la solución

#### 2.1. Estrategia general

El sistema sigue un modelo de **acceso directo a archivos binarios indexado en memoria**.
Al iniciar, se lee el archivo `inventario.bin` completo para construir un diccionario
`{codigo: offset}`. A partir de ese momento, toda operación sobre un producto usa el offset
para posicionarse directamente en el archivo sin recorrerlo desde el principio.

Esta estrategia combina la persistencia durable de los archivos con la velocidad de los
diccionarios en memoria, sin necesidad de cargar todos los productos en una lista.

#### 2.2. Estructuras de datos

| Estructura | Uso | Justificación |
|---|---|---|
| Archivo binario `inventario.bin` | Persistencia de productos | Registros de longitud fija permiten `seek()` directo por offset |
| Archivo binario `movimientos.bin` | Historial de movimientos | Solo se agrega al final; no requiere modificar registros existentes |
| Diccionario `{codigo: offset}` | Índice en memoria | Búsqueda O(1); se actualiza al agregar un producto sin reescribir el archivo |
| Tupla `(codigo, descripcion, stock, minimo, precio)` | Producto en memoria | Inmutable y de tamaño fijo; se reconstruye cada vez que se lee del archivo |

**Formato binario del producto:** `=10s50siid`
- `=` desactiva el relleno de alineación → tamaño fijo y portable entre plataformas.
- Cada registro ocupa exactamente `struct.calcsize("=10s50siid")` bytes.

#### 2.3. Descomposición modular

| Función | Subtarea que resuelve |
|---|---|
| `inicializar_archivos()` | Crea directorio y archivos si no existen |
| `cargar_indice()` | Construye el diccionario `{codigo: offset}` al inicio |
| `leer_producto_en(offset)` | Lee y decodifica un registro por su posición |
| `escribir_producto_en(producto, offset)` | Sobreescribe un registro en su posición |
| `_agregar_producto_al_archivo(producto)` | Agrega un registro nuevo al final |
| `guardar_movimiento(codigo, tipo, cantidad)` | Persiste un movimiento en el historial |
| `agregar_producto(indice)` | Valida y registra un nuevo producto |
| `registrar_entrada(indice)` | Incrementa el stock y graba el movimiento tipo E |
| `registrar_salida(indice)` | Descuenta el stock (si hay suficiente) y graba el movimiento tipo S |
| `alertas_reposicion(indice)` | Detecta productos con stock menor al mínimo |
| `ver_historial(indice)` | Muestra todos los movimientos de un producto |
| `ordenamiento_insercion(lista, clave)` | Ordena una lista de productos por un campo dado |
| `listar_inventario(indice)` | Muestra el inventario ordenado por criterio elegido |
| `valorizar_inventario(indice)` | Calcula el valor total del stock |
| `estadisticas_inventario(indice)` | Clasifica productos por estado de stock |
| `reporte_rotacion()` | Ranking de productos por volumen total de movimientos |
| `mostrar_menu()` | Imprime el menú principal |

#### 2.4. Algoritmo de ordenamiento elegido: Insertion Sort

Se eligió **Insertion Sort** por tres razones:

1. El inventario de un depósito es pequeño (decenas o cientos de productos, no millones).
   Para n pequeño, O(n²) es perfectamente aceptable.
2. Es **estable**: dos productos con el mismo stock conservan el orden relativo anterior.
3. Tiene comportamiento **O(n) en listas casi ordenadas**: si el inventario ya estaba
   ordenado y solo se agregó un producto, lo inserta rápidamente sin recorrer todo.

Alternativas descartadas:
- **Merge Sort / Quick Sort**: complejidad O(n log n), pero para n pequeño el overhead
  de la recursión y la memoria auxiliar no justifica la mejora.
- **Bubble Sort**: similar a Insertion Sort en complejidad pero con más intercambios
  en promedio y sin ventaja sobre listas casi ordenadas.

---

### 3. Casos de análisis

Ver [`semana14.md`](semana14.md) para la tabla completa con entradas, salidas esperadas
y resultados obtenidos.

---

### 4. Análisis de complejidad

| Operación | Complejidad temporal | Complejidad espacial | Observaciones |
|---|---|---|---|
| `cargar_indice()` | O(n) | O(n) | Lee los n registros del archivo una sola vez al inicio |
| `leer_producto_en(offset)` | O(1) | O(1) | Acceso directo por `seek()` |
| `escribir_producto_en(producto, offset)` | O(1) | O(1) | Sobreescritura en posición fija |
| `_agregar_producto_al_archivo(producto)` | O(1) | O(1) | Append al final del archivo |
| `agregar_producto(indice)` | O(1) | O(1) | Dominado por el acceso al archivo |
| `registrar_entrada(indice)` | O(1) | O(1) | Lookup en diccionario + seek |
| `registrar_salida(indice)` | O(1) | O(1) | Igual que entrada |
| `alertas_reposicion(indice)` | O(n) | O(1) | Recorre los n productos del índice |
| `ver_historial(indice)` | O(m) | O(1) | m = cantidad total de movimientos en el historial |
| `ordenamiento_insercion(lista, clave)` | O(n²) peor / O(n) mejor | O(n) | Lista auxiliar de n productos |
| `listar_inventario(indice)` | O(n²) peor | O(n) | Dominado por el ordenamiento |
| `valorizar_inventario(indice)` | O(n) | O(1) | Patrón acumulador sobre n productos |
| `estadisticas_inventario(indice)` | O(n) | O(1) | Recorrido único |
| `reporte_rotacion()` | O(m + k²) | O(k) | m = movimientos totales; k = productos distintos con movimientos |

**Operación dominante:** `listar_inventario` con O(n²) en el peor caso.
Para el dominio de un depósito (n pequeño), esto no representa un cuello de botella.

---

### 5. Mejora algorítmica de la Fase 3

[completar — describir qué se optimizó, por qué y con qué efecto medible.
Ejemplo de posibles mejoras:
- Reemplazar el Insertion Sort de `reporte_rotacion` por llamada a `ordenamiento_insercion`
  para eliminar código duplicado.
- Agregar búsqueda binaria si el índice se mantiene ordenado.
- Implementar Merge Sort para el listado y comparar tiempos con Insertion Sort.]

**Qué se cambió:** [completar]

**Por qué se eligió esa mejora:** [completar]

**Efecto observado:** [completar]

---

### 6. Análisis crítico del uso de IA generativa

Ver [`docs/registro_ia.md`](registro_ia.md) para el registro detallado de interacciones.

[completar — responder estas preguntas en forma de párrafo:
- ¿En qué etapas del proyecto se usó IA?
- ¿Qué aportes fueron útiles y cuáles fueron incorrectos o superficiales?
- ¿Cómo distinguieron una respuesta confiable de una que requería verificación?
- ¿Qué decisiones tomaron de forma completamente independiente?]

---

### 7. Reflexión final del equipo

[completar — una reflexión honesta sobre el proceso de aprendizaje:
- ¿Qué fue lo más difícil del proyecto?
- ¿Qué cambiarían si empezaran de nuevo?
- ¿Qué concepto de la materia les resultó más útil en la práctica?
- ¿Cómo impactó tener el diseño listo antes de codificar?]

---

## Autoevaluación y coevaluación

[completar según el formulario que indique la cátedra.]
