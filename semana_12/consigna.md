# Bloque C — Problema integrador (resolución en equipo)

El Problema 5 es un problema integrador complejo, de resolución en equipo durante la clase práctica, que demanda combinar múltiples estructuras de datos y algoritmos en un único programa. A diferencia de los problemas de los bloques anteriores —cada uno enfocado en una técnica— este problema exige decidir qué técnica aplicar a cada parte y articular las partes en una solución modular coherente. Funciona como ensayo general del proyecto final: el equipo enfrenta, en pequeña escala y con el enunciado ya dado, el mismo tipo de trabajo de integración que deberá hacer en las Semanas 13 a 16 sobre un problema de su propia elección.

## Problema 5: Sistema de turnos de un consultorio médico

### Enunciado

Desarrollar, en equipos de 2 o 3 integrantes, un sistema de gestión de turnos para un consultorio médico. El sistema persiste los datos en un archivo binario de registros de longitud fija, mantiene índices en memoria mediante diccionarios, produce reportes ordenados, resuelve búsquedas eficientes por distintos criterios, y asigna turnos a una agenda diaria mediante backtracking. El problema se descompone en cuatro módulos; se sugiere repartir su desarrollo entre los integrantes del equipo y luego integrarlos.

### Módulo 1 — Persistencia binaria de pacientes

Diseñar el registro de paciente de longitud fija y sus operaciones de lectura y escritura. El registro tiene la siguiente estructura:

| Campo | Tipo struct | Tamaño |
|---|---|---|
| `dni` | `i` (int32) | 4 bytes |
| `apellido` | `30s` | 30 bytes |
| `nombre` | `24s` | 24 bytes |
| `telefono` | `16s` | 16 bytes |
| `prioridad` | `B` (uint8) | 1 byte |

**(a)** Declarar `FORMATO = '<i30s24s16sB'` y `TAM_REGISTRO = struct.calcsize(FORMATO)` como constantes globales (fuente única de verdad). Implementar `empaquetar_paciente` y `desempaquetar_paciente`, con codificación UTF-8, truncado de cadenas largas y removido del relleno de ceros al desempaquetar. El campo prioridad es un entero de 1 (alta) a 3 (baja).

**(b)** Implementar `crear_archivo_pacientes(ruta, lista_pacientes)` y `leer_paciente(archivo, k)` con acceso directo por offset (`seek(k * TAM_REGISTRO)`). Usar el context manager `with` en todo acceso a archivo.

### Módulo 2 — Índices en memoria

**(c)** Implementar `construir_indices(ruta)` que recorra una sola vez el archivo binario y devuelva dos diccionarios: `indice_por_dni` (clave: DNI, valor: posición k del registro en el archivo) e `indice_por_apellido` (clave: apellido, valor: lista de posiciones, porque puede haber apellidos repetidos).

**(d)** Implementar `buscar_por_dni(archivo, indice_por_dni, dni)` que resuelva la búsqueda en O(1) promedio consultando el diccionario y leyendo un único registro. Comparar conceptualmente, en la docstring, con el costo de una búsqueda secuencial O(n) sobre el archivo sin índice.

### Módulo 3 — Reportes ordenados

**(e)** Implementar `listar_pacientes_ordenados(ruta, criterio)` que lea todos los pacientes del archivo y devuelva la lista ordenada según el criterio indicado: `"apellido"` (alfabético) o `"prioridad"` (de 1 a 3, y dentro de cada prioridad, por apellido). Reutilizar la implementación de `merge_sort` del Problema 1 —que es estable— para el ordenamiento por prioridad con desempate por apellido.

**(f)** Justificar por escrito por qué la estabilidad del algoritmo de ordenamiento es relevante para el criterio `"prioridad"`: describir el procedimiento de dos pasadas (ordenar por apellido y luego por prioridad) y explicar qué se rompería si el segundo ordenamiento no fuera estable.

### Módulo 4 — Asignación de la agenda diaria por backtracking

El consultorio tiene una agenda de franjas horarias (por ejemplo, 8 franjas de 30 minutos). Algunos pacientes tienen restricciones de disponibilidad: una lista de las franjas en las que cada uno puede asistir. El problema es asignar cada paciente de una lista del día a una franja, respetando que (1) cada franja recibe a lo sumo un paciente y (2) cada paciente queda en una franja compatible con su disponibilidad.

**(g)** Implementar `asignar_agenda(pacientes_del_dia, franjas, disponibilidad)` mediante backtracking. El estado parcial es la asignación construida hasta el momento (un diccionario franja → paciente, o paciente → franja). La poda descarta asignar un paciente a una franja ya ocupada o no disponible para él. La función devuelve una asignación válida, o `None` si no existe ninguna.

**(h)** Probar con un caso que tenga solución y con un caso sobre-restringido que no la tenga (más pacientes que franjas compatibles). Para el caso con solución, verificar que la asignación devuelta respeta todas las restricciones. Discutir: ¿cuántas asignaciones posibles habría que revisar por fuerza bruta, y cuántas evita la poda?

### Integración

**(i)** Escribir un programa principal que articule los cuatro módulos en un flujo completo: crear el archivo de pacientes, construir los índices, ofrecer un menú de consulta (buscar por DNI, listar ordenado por apellido o prioridad) y resolver la agenda del día. El programa principal no debe contener lógica de los módulos: sólo coordinarlos. Cada módulo se entrega con sus funciones documentadas y con sus propios casos de prueba.

### Orientaciones para la resolución

* **Análisis:** El problema no es "un" problema sino cuatro subproblemas de naturaleza distinta —persistencia binaria, indexación, ordenamiento y búsqueda combinatoria— que comparten un mismo dominio. El trabajo de análisis central es reconocer qué técnica del curso resuelve cada subproblema: archivos binarios de longitud fija para la persistencia (Semana 8), diccionarios para los índices (Semana 10), merge sort estable para los reportes (Semanas 6 y 12), y backtracking para la agenda (Semana 12).
* **Diseño:** La descomposición en módulos es a la vez una estrategia de diseño y una estrategia de trabajo en equipo: cada integrante puede tomar uno o dos módulos y avanzar en paralelo, siempre que las interfaces entre módulos —qué recibe y qué devuelve cada función— estén acordadas de antemano. Conviene escribir primero las firmas de las funciones con sus docstrings (precondición y postcondición) y recién después codificar los cuerpos. El programa principal de integración debe escribirse al final, cuando los módulos ya pasan sus pruebas individuales.
* **Evaluación:** Cada módulo se valida por separado con sus propios casos antes de integrar. Para el Módulo 1, verificar que `os.path.getsize(ruta)` coincide con `cantidad_de_pacientes * TAM_REGISTRO`. Para el Módulo 2, comprobar que toda búsqueda por DNI devuelve el registro correcto. Para el Módulo 3, contrastar el resultado contra `sorted()` con la misma clave. Para el Módulo 4, verificar manualmente que la asignación devuelta respeta disponibilidad y unicidad de franja. La integración recién se prueba cuando los cuatro módulos están validados.
* **Conexión integradora:** Este problema reúne, en un único programa, contenidos de las Semanas 6, 8, 10 y 12. Es deliberadamente un ensayo general del proyecto final: la misma exigencia de descomponer un problema realista en módulos, repartir el trabajo, acordar interfaces e integrar. La diferencia es que aquí el enunciado está dado; en el proyecto, el equipo elegirá su propio problema.