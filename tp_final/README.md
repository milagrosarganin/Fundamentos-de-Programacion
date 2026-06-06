[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/1_hh46l6)
# Proyecto Final Integrador

> Plantilla del repositorio del proyecto final.
> Cada equipo debe **completar todas las secciones marcadas con `[completar]`** y
> eliminar este bloque de cita una vez hecho.

---

## 1. El problema

**Título del proyecto:** Gestor de inventario de un depósito

**Descripción del problema:** 

**Por qué es un proyecto integrador:** A este se lo puede considerar un proyecto integrador porque abarca alrededor de un 75% de los contenidos de la materia, tratados en las semanas, 3, 4, 5, 8, 10, 11, 12.

---

## 2. El equipo

| Integrante (apellido, nombre) | Usuario de GitHub | Rol / módulos a cargo |
|-------------------------------|-------------------|-----------------------|
| Argañin Milagros              | milagrosarganin   | SubCordinador         |
| Rodriguez Tomás Ezequiel      | terodriguez-fiuba | Cordinador            |

**Coordinador del equipo:** Tomás Ezequiel Rodriguez

---

## 3. Cómo ejecutar el programa

**Requisitos:** Python 3.x (sin dependencias externas, salvo que se indique lo
contrario en esta sección).

**Ejecución:**

```
python src/main.py
```

[completar — describir qué entradas espera el programa (por teclado, desde un
archivo, etc.), qué archivos de entrada hace falta tener, y qué produce como
salida. Si hay parámetros o modos de uso, detallarlos aquí.]

---

## 4. Estructura del proyecto

[completar — describir brevemente qué hace cada archivo o módulo. Mantener esta
tabla actualizada a medida que el proyecto crece.]

| Archivo / carpeta        | Responsabilidad                                      |
|--------------------------|------------------------------------------------------|
| `src/main.py`            | Programa principal: Prólogo, Resolución, Epílogo.    |
| `src/[modulo].py`        | [completar — qué funciones agrupa y para qué.]       |
| `docs/registro_ia.md`    | Registro de interacciones con IA generativa.         |
| `docs/diseno.md`         | Diseño del algoritmo (pseudocódigo / casos).         |

---

## 5. Casos de análisis

- **Caso normal:** registrar una entrada de mercadería; verificar que el stock del producto aumenta en la cantidad correspondiente.
- **Caso límite:** registrar una salida que deja el stock exactamente en el mínimo o por debajo; respectivamente el producto aún no debe aparecer como «a reponer» o si debe hacerlo.
- **Caso extremo:** registrar una salida mayor que el stock disponible; el sistema debe aplicar la política definida sin interrumpirse.

---

## 6. Estado del proyecto

[completar — opcional pero recomendado: una breve nota de en qué fase está el
proyecto. Útil para el seguimiento docente semanal.]

- [ ] Semana 13 — Análisis y diseño
- [ ] Semana 14 — Codificación e integración
- [ ] Semana 15 — Evaluación y optimización
- [ ] Semana 16 — Presentación y defensa

---

*Proyecto Final Integrador · Fundamentos de Programación · Algoritmos y
Programación I · Carrera de Informática · FIUBA*
