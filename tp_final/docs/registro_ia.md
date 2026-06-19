# Registro de interacciones con IA generativa

> Este registro es parte del proyecto final y se entrega versionado dentro del
> repositorio. No es una formalidad: es una herramienta de aprendizaje y, a la
> vez, lo que permite al docente entender el proceso real de elaboracion.
> 
>*Criterio del curso:* todo el codigo que el equipo entrega debe ser codigo
> que el equipo puede explicar y defender linea por linea. La IA generativa es
> una herramienta —como una biblioteca de terceros o una consulta a una
> documentacion—; lo que se incorpora a la solucion es responsabilidad del
> equipo.
> 
>*Cómo usar este archivo:* registrar *cada uso significativo* de IA
> generativa copiando el bloque de la plantilla de abajo. Hacerlo en el momento,
> no al final: el registro reconstruido a posteriori pierde su valor. Hacer
> commit del registro junto con el código al que se refiere.

---

## Plantilla de entrada

> Copiar este bloque para cada interacción y completarlo. Borrar esta cita.

### Entrada N — [fecha] — [integrante que la realizó]

*Contexto:* [en qué parte del proyecto se estaba trabajando y qué se
necesitaba resolver.]

*Herramienta utilizada:* [qué herramienta de IA generativa.]

*Prompt exacto:*


[el prompt tal como se escribió.]


*Respuesta obtenida:* [la respuesta, o su esencia si fue muy extensa. Si fue
código, puede incluirse aquí o resumirse.]

*Análisis crítico:* [qué se tomó de la respuesta y qué se descartó, y por qué.
¿La respuesta era correcta? ¿Tenía errores? ¿Se adaptaba a la estructura y la
metodología del proyecto, o hubo que reescribirla?]

*Aprendizaje:* [qué entendió mejor el equipo a partir de esta interacción.
¿Qué concepto quedó más claro? ¿Qué se haría distinto la próxima vez?]

---

## Registro

> A partir de aquí van las entradas reales del equipo, de la más antigua a la
> más reciente.

---

### Entrada 1 — 2026-06-13 — [integrante]

*Contexto:* Redacción de la sección 2.1 (Estrategia general) del documento de diseño. El equipo ya había decidido usar un enfoque iterativo con un diccionario en memoria como índice, y quería una segunda opinión sobre si la justificación estaba bien armada antes de escribirla en el documento.

*Herramienta utilizada:* Claude (claude.ai)

*Prompt exacto:*


Estamos diseñando un sistema de stock para un depósito. Decidimos usar un
enfoque iterativo porque ninguna operación necesita recursión: registrar
entradas, buscar productos y recorrer el archivo son todas tareas de bucle.
También elegimos mantener un diccionario en memoria {codigo: offset} que se
construye al inicio leyendo el archivo una sola vez, y después todas las
búsquedas son O(1) sin volver a recorrerlo. ¿La justificación es sólida o
le falta algo?


*Respuesta obtenida:*


La justificación es sólida. El razonamiento sobre la recursión es correcto:
forzarla en un problema sin subestructura recursiva natural solo agrega
complejidad de pila sin ningún beneficio. El enfoque iterativo es el natural
para este dominio.

El punto sobre el diccionario también está bien planteado. Un detalle para
reforzar la justificación: aclará que el diccionario y el archivo no son
redundantes, sino que resuelven problemas distintos. El archivo garantiza
persistencia (los datos sobreviven al cierre del programa); el diccionario
garantiza velocidad de búsqueda durante la ejecución. Esa separación de
responsabilidades es la clave del diseño.

Un punto que podría quedar más explícito en el documento: mencioná que el
"divide y vencerás" sí aparece, pero a nivel arquitectónico, en la
descomposición en funciones. Así cubrís los tres enfoques del enunciado y
queda claro por qué se descartó cada uno a nivel de flujo de datos.


*Análisis crítico:* La respuesta confirmó que el razonamiento era correcto. Se incorporó la aclaración sobre la separación de responsabilidades entre diccionario y archivo, que el equipo no había explicitado. Se descartó la sugerencia de mencionar los tres enfoques por separado porque alargaba innecesariamente el texto; se sintetizó en una sola oración.

*Aprendizaje:* La distinción entre "persistencia" y "velocidad de búsqueda" como dos responsabilidades diferentes ayudó a articular mejor por qué se usan dos estructuras en lugar de una sola.

---

### Entrada 2 — 2026-06-13 — [integrante]

*Contexto:* Redacción de la sección 2.2 (Estructuras de datos). El equipo ya tenía elegidas las cuatro estructuras (archivo binario de productos, diccionario índice, archivo de historial, lista temporal para ordenar) y quería validar que las justificaciones eran correctas y suficientes antes de escribirlas en el documento.

*Herramienta utilizada:* Claude (claude.ai)

*Prompt exacto:*


Para nuestro sistema de inventario elegimos estas estructuras y estas
justificaciones. ¿Están bien o hay algo incorrecto?

- Archivo binario de registros fijos: para persistir los productos. Lo
  elegimos porque con registros de longitud fija podemos calcular la posición
  de cualquier registro con offset = numero_registro * tamaño y hacer seek()
  directo.
- Diccionario {codigo: offset}: índice en memoria para búsqueda O(1). El
  valor es el offset en bytes, no el registro completo.
- Archivo binario para historial: append secuencial de movimientos, se lee
  de corrido cuando se consulta el historial de un producto.
- Lista temporal de tuplas: solo para ordenar y mostrar el inventario, no
  se persiste.


*Respuesta obtenida:*


Todo está correcto. Las justificaciones son precisas y cada estructura está
bien emparejada con su caso de uso.

Un detalle sobre el diccionario: está bien que el valor sea el offset en
bytes y no el registro completo. Si guardaras el registro completo, el
diccionario crecería con el tamaño de los datos y habría que sincronizarlo
manualmente cada vez que el archivo cambia. Guardar solo el offset lo mantiene
liviano y siempre consistente con el archivo, que es la fuente de verdad.

Sobre la lista temporal: es una decisión correcta no persistirla. El archivo
ya tiene el orden de inserción como orden "natural"; el orden para mostrar es
una vista, no un estado del sistema. Si la persistieras ordenada, tendrías que
mantener dos representaciones sincronizadas, lo cual es una fuente de bugs.

No veo nada incorrecto. Lo único que agregaría es aclarar explícitamente en
el documento que la lista temporal solo existe durante la ejecución de
listar_inventario() y que no modifica el archivo.


*Análisis crítico:* La respuesta confirmó que las justificaciones eran correctas. Se incorporó al documento la aclaración sobre por qué el diccionario guarda el offset y no el registro completo, porque el equipo no lo había argumentado explícitamente. La observación sobre "vista vs. estado" también se agregó en la justificación de la lista temporal.

*Aprendizaje:* La distinción entre "vista" y "estado" del sistema es útil para justificar por qué ciertas estructuras no se persisten. Aplicarlo al diseño evita duplicar datos innecesariamente.

---

### Entrada 3 — 2026-06-13 — [integrante]

*Contexto:* Implementación de cargar_indice. La función se escribió, el programa corría sin errores, pero al buscar un producto existente por código el sistema devolvía "no encontrado" siempre. Revisamos la lógica varias veces y no encontrábamos el error porque nos parecía correcta.

*Herramienta utilizada:* Claude (claude.ai)

*Prompt exacto:*


Esta función construye el índice en memoria leyendo el archivo de productos.
La lógica nos parece correcta: abrimos el archivo, leemos registro por
registro y guardamos en el diccionario el código como clave y la posición
del registro como valor. Pero cuando después hacemos seek() con ese offset
y leemos, obtenemos el registro siguiente al que queríamos, no el correcto.
No encontramos el error.

def cargar_indice(archivo):
    indice = {}
    archivo.seek(0)
    while True:
        datos = archivo.read(TAMAÑO_REGISTRO)
        if not datos:
            break
        registro = struct.unpack(FORMATO, datos)
        indice[registro[0]] = archivo.tell()
    return indice


*Respuesta obtenida:*


El error está en esta línea:

    indice[registro[0]] = archivo.tell()

archivo.tell() se llama DESPUÉS de archivo.read(). En ese momento el cursor
ya avanzó TAMAÑO_REGISTRO bytes, así que tell() devuelve la posición del
inicio del SIGUIENTE registro, no del actual.

Para guardar la posición del registro que acabás de leer, tenés que capturar
tell() ANTES de leer:

def cargar_indice(archivo):
    indice = {}
    archivo.seek(0)
    while True:
        posicion = archivo.tell()          # posición ANTES de leer
        datos = archivo.read(TAMAÑO_REGISTRO)
        if not datos:
            break
        registro = struct.unpack(FORMATO, datos)
        indice[registro[0]] = posicion     # offset correcto
    return indice

Con este cambio, cuando hagas seek(indice[codigo]) vas a posicionarte
exactamente al inicio del registro que querés leer.


*Análisis crítico:* El error era exactamente el que describió: tell() después de read() da la posición siguiente. La corrección es mínima (mover una línea antes del read) y resuelve el problema completamente. Se aplicó directamente al código.

*Aprendizaje:* El orden de tell() y read() importa, porque si necesitás la posición de lo que estás por leer, siempre capturá tell() antes del read(). Es un error fácil de no ver porque la lógica "parece" correcta al leerla.

---

### Entrada 4 — 2026-06-18 — [integrante]

**Contexto:** Semana 15 — modularización. El equipo decidió dividir el único archivo `main.py` en cuatro módulos: `config.py`, `archivos.py`, `operaciones.py` y `main.py`. Antes de empezar a mover código, se quiso validar que la cadena de dependencias elegida era correcta y no iba a generar problemas de importación.

**Herramienta utilizada:** Claude (claude.ai)

**Prompt exacto:**

```
Vamos a dividir nuestro proyecto en cuatro módulos Python. Pensamos esta
cadena de dependencias:

  config.py      → no importa nada del proyecto
  archivos.py    → importa config
  operaciones.py → importa config y archivos
  main.py        → importa config, archivos y operaciones

¿Esta estructura tiene algún problema? ¿Las dependencias van en la
dirección correcta?
```

**Respuesta obtenida:**

```
La estructura es correcta y no tiene ningún problema. Las dependencias van
en una sola dirección (de arriba hacia abajo), lo cual evita el mayor
problema de los sistemas modulares: las importaciones circulares.

Una importación circular ocurre cuando el módulo A importa a B y B importa
a A. Python no puede resolver eso porque para cargar A necesita cargar B,
pero para cargar B necesita cargar A. El resultado es un ImportError.

En su cadena eso no puede pasar: config no importa a nadie, archivos solo
mira hacia config, operaciones mira hacia abajo (config y archivos), y main
mira a todos. Ninguno mira hacia arriba.

Un detalle práctico: para que Python encuentre los módulos cuando ejecutás
main.py, todos los archivos tienen que estar en la misma carpeta (src/ en
su caso). Si ejecutás desde otra carpeta, el intérprete no va a encontrar
config.py y va a tirar ModuleNotFoundError. Siempre ejecutá con:

    python3 src/main.py

desde la raíz del proyecto, o bien:

    cd src
    python3 main.py
```

**Análisis crítico:** La respuesta confirmó que la arquitectura era correcta. El aviso sobre el directorio de ejecución era nuevo para el equipo y resultó ser exactamente el problema que apareció en la entrada siguiente. Se incorporó al flujo de trabajo ejecutar siempre desde la raíz con `python3 src/main.py`.

**Aprendizaje:** Las importaciones circulares son el error más común al modularizar. La regla para evitarlas es simple: las dependencias siempre deben ir en una sola dirección, de los módulos más generales (config) a los más específicos (main).

---

### Entrada 5 — 2026-06-18 — [integrante]

**Contexto:** Semana 15 — primera ejecución después de dividir el código en módulos. Al correr el programa apareció un error que no entendíamos porque el código en sí no había cambiado, solo lo habíamos separado en archivos distintos.

**Herramienta utilizada:** Claude (claude.ai)

**Prompt exacto:**

```
Separamos el código en cuatro archivos dentro de la carpeta src/:
config.py, archivos.py, operaciones.py y main.py. Cuando corremos el
programa desde la carpeta tp_final/ con "python3 src/main.py" sale este
error:

  File "src/main.py", line 3, in <module>
    from config import TITULO, SEPARADOR
ModuleNotFoundError: No module named 'config'

El archivo config.py existe, está en src/. No entendemos por qué no
lo encuentra si está en la misma carpeta que main.py.
```

**Respuesta obtenida:**

```
El problema es cómo Python busca módulos cuando ejecutás un script.

Cuando corrés "python3 src/main.py", Python agrega al path de búsqueda
la carpeta donde está el script, que en este caso es src/. Entonces
debería encontrar config.py sin problema.

Pero hay un detalle: si en algún momento corriste el programa parado
dentro de src/ y después te moviste, o si tenés algún __pycache__ de
una ejecución anterior desde otro directorio, puede quedar una caché
inconsistente.

Probá estas dos cosas en orden:

1. Borrá los directorios __pycache__ que haya dentro de src/:
      find src/ -name __pycache__ -type d
      rm -rf src/__pycache__

2. Ejecutá siempre parado en la raíz del proyecto (tp_final/):
      python3 src/main.py

Si el error persiste, verificá que el archivo se llama exactamente
"config.py" (sin mayúsculas, sin espacios) con:
      ls src/

Python distingue mayúsculas de minúsculas en los nombres de archivo,
incluso en Windows en algunos casos.
```

**Análisis crítico:** El problema era la caché `__pycache__` de una ejecución previa desde el directorio equivocado. Después de borrarla y ejecutar desde la raíz con `python3 src/main.py` el error desapareció. La respuesta fue precisa y la solución funcionó al primer intento.

**Aprendizaje:** Al modularizar, el directorio desde el que se ejecuta el programa importa. Los `__pycache__` de ejecuciones anteriores pueden generar errores confusos si se corrió el programa desde distintos directorios. La práctica correcta es ejecutar siempre desde la raíz del proyecto.

---

### Entrada 6 — 2026-06-18 — [integrante]

**Contexto:** Semana 15 — revisión del código de `reporte_rotacion` después de moverlo a `operaciones.py`. Se notó que la función tenía su propio bucle de ordenamiento (idéntico en lógica al de `ordenamiento_insercion`) en vez de llamar a esa función. Se quiso verificar si la refactorización propuesta era correcta antes de tocar el código.

**Herramienta utilizada:** Claude (claude.ai)

**Prompt exacto:**

```
La función reporte_rotacion tiene este bloque de ordenamiento propio:

    pares = list(rotacion.items())
    i = 1
    while i < len(pares):
        actual = pares[i]
        j = i - 1
        while j >= 0 and pares[j][1] < actual[1]:
            pares[j + 1] = pares[j]
            j -= 1
        pares[j + 1] = actual
        i += 1

Ya tenemos ordenamiento_insercion(lista, clave) en el mismo módulo.
Queremos reemplazar ese bloque por:

    pares = ordenamiento_insercion(
        [(cod, tot) for cod, tot in rotacion.items()], 1
    )
    pares.reverse()

¿La lógica es equivalente? ¿El resultado va a ser el mismo?
```

**Respuesta obtenida:**

```
La lógica es equivalente con un matiz importante que hay que verificar.

El bloque original ordena de mayor a menor (descendente) porque la
condición de comparación es pares[j][1] < actual[1]: mueve elementos
hacia la derecha cuando el actual es MAYOR que el de la izquierda.

ordenamiento_insercion ordena de menor a mayor (ascendente) porque la
condición es ordenada[j][clave] > actual[clave]: mueve elementos cuando
el de la izquierda es MAYOR que el actual.

Tu propuesta compensa eso con .reverse() al final, lo que invierte la
lista ya ordenada de menor a mayor a mayor a menor. Eso es correcto.

El resultado final es idéntico: ranking de productos de mayor a menor
volumen de movimientos.

Una ventaja adicional de tu refactorización: elimina código duplicado.
Si en el futuro cambian la implementación de ordenamiento_insercion
(por ejemplo, para agregar estabilidad o cambiar el algoritmo), el
reporte de rotación se actualiza automáticamente sin tener que tocar
su propio bloque.
```

**Análisis crítico:** La respuesta confirmó que la equivalencia era correcta y explicó por qué el `.reverse()` era necesario (la dirección del ordenamiento original era descendente, no ascendente). Se aplicó la refactorización. Se descartó la sugerencia de agregar un parámetro `descendente=True` a `ordenamiento_insercion` porque añadía complejidad innecesaria para un caso puntual.

**Aprendizaje:** Antes de refactorizar código de ordenamiento hay que prestar atención a la dirección (ascendente vs. descendente) porque los dos bucles pueden verse casi idénticos pero producir resultados invertidos. El `.reverse()` explícito hace visible esa intención.