# Fase 2 — Semana 14: Integración y Pruebas

## 1. Estado del código

El código está integrado en `src/main.py`. Todas las funciones están documentadas con
precondición y postcondición. El sistema corre sin errores desde la línea de comandos con:

```
python src/main.py
```

---

## 2. Ejecución de los casos de análisis

Para cada caso se indica la secuencia de entradas por teclado y la salida obtenida en consola.

### Caso 1 — Normal: registrar entrada de mercadería

**Preparación:** inventario con producto código `"ABC"`, stock inicial 20.

**Entradas:**
```
Opción: 2
Código del producto: ABC
Cantidad a ingresar: 50
```

**Salida esperada:**
```
Entrada registrada. Stock actualizado: 70 unidades.
```

**Resultado obtenido:** [completar — copiar la salida real del programa]

**Verificación:** [completar — ejecutar opción 5 (listar) y confirmar que ABC figura con stock 70]

---

### Caso 2 — Límite: salida que deja el stock exactamente en cero

**Preparación:** producto código `"DEF"`, stock = 30, mínimo = 0.

**Entradas:**
```
Opción: 3
Código del producto: DEF
Cantidad a retirar: 30
```

**Salida esperada:**
```
Salida registrada. Stock actualizado: 0 unidades.
```
No debe aparecer advertencia de mínimo (stock == mínimo == 0).

**Resultado obtenido:** [completar]

---

### Caso 3 — Límite: salida que deja el stock igual al mínimo

**Preparación:** producto código `"GHI"`, stock = 10, mínimo = 5.

**Entradas:**
```
Opción: 3
Código del producto: GHI
Cantidad a retirar: 5
```

**Salida esperada:**
```
Salida registrada. Stock actualizado: 5 unidades.
```
No debe aparecer advertencia (stock igual a mínimo, no por debajo).

**Resultado obtenido:** [completar]

---

### Caso 4 — Límite: salida que deja el stock por debajo del mínimo

**Preparación:** producto código `"JKL"`, stock = 10, mínimo = 8.

**Entradas:**
```
Opción: 3
Código del producto: JKL
Cantidad a retirar: 5
```

**Salida esperada:**
```
Salida registrada. Stock actualizado: 5 unidades.
ATENCION: el stock cayo por debajo del minimo (8 unidades).
```

**Resultado obtenido:** [completar]

---

### Caso 5 — Extremo: salida mayor que el stock disponible

**Preparación:** producto código `"MNO"`, stock = 10.

**Entradas:**
```
Opción: 3
Código del producto: MNO
Cantidad a retirar: 50
```

**Salida esperada:**
```
Operacion rechazada: stock insuficiente (politica: RECHAZO).
Stock disponible: 10  |  Cantidad solicitada: 50
```
El archivo no debe modificarse.

**Resultado obtenido:** [completar]

---

### Caso 6 — Extremo: agregar producto con código duplicado

**Preparación:** producto código `"ABC"` ya existe.

**Entradas:**
```
Opción: 1
Código: ABC
```

**Salida esperada:**
```
Error: ya existe un producto con el codigo 'ABC'.
```

**Resultado obtenido:** [completar]

---

### Caso 7 — Extremo: ingreso de cantidad no numérica

**Entradas:**
```
Opción: 2
Código del producto: ABC
Cantidad a ingresar: abc
```

**Salida esperada:**
```
Error: la cantidad debe ser un entero mayor a cero.
```

**Resultado obtenido:** [completar]

---

## 3. Avance del análisis de uso de IA

Ver [`docs/registro_ia.md`](registro_ia.md).

[completar — describir brevemente en qué etapas se usó IA hasta esta semana
y qué decisiones se tomaron de forma independiente.]
