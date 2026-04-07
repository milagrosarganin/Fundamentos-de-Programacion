'''
## Problema 4: Búsqueda por interpolación vs. búsqueda binaria

#### Enunciado
Implementar la función `busqueda_interpolacion(datos, clave)` según el algoritmo presentado en la clase teórica. La función debe retornar el índice (o `−1`) y la cantidad de comparaciones realizadas.

Escribir un programa que compare búsqueda binaria vs. interpolación en tres escenarios con listas de `n = 10.000` elementos:

* **Escenario A — Distribución uniforme:** generar la lista con `datos = sorted(random.sample(range(1, 100001), n))`. Buscar 500 claves presentes elegidas al azar.
* **Escenario B — Distribución exponencial (sesgada):** los valores están concentrados cerca de cero con cola larga. Generar la lista garantizando `n` elementos únicos:
  ```python
  vals = set()
  while len(vals) < n:
      vals.add(int(random.expovariate(1) * 10000))
  datos = sorted(vals)
  ```
  Buscar 500 claves presentes elegidas al azar con `random.sample(datos, 500)`.
* **Escenario C — Distribución con clusters:** 5 grupos de 2000 elementos separados por vacíos. Generar la lista con exactamente `n/5` elementos únicos por cluster:
  ```python
  centros =
  vals = set()
  for c in centros:
      cluster = set()
      while len(cluster) < n // 5:
          cluster.add(random.randint(c - 2500, c + 2500))
      vals |= cluster
  datos = sorted(vals)
  ```
  Buscar 500 claves presentes elegidas al azar. Los grandes vacíos entre clusters (~15.000–20.000 unidades) provocan estimaciones erráticas en la búsqueda por interpolación.

Para cada escenario, informar: promedio de comparaciones por búsqueda para cada algoritmo, y cuál es más eficiente.'''