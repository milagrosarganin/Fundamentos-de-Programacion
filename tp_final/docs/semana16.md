# Fase 4 — Semana 16: Cierre y Defensa

## 1. Checklist de cierre del repositorio

Antes de la defensa verificar que todo esto esté en orden:

- [ ] `src/main.py` es la versión final, sin código comentado ni prints de debug
- [ ] `README.md` tiene todas las secciones `[completar]` resueltas
- [ ] `docs/semana13.md` — diseño completo (pseudocódigo, casos, módulos)
- [ ] `docs/semana14.md` — todos los casos de análisis con resultados obtenidos completados
- [ ] `docs/semana15.md` — informe completo (mejora, análisis IA, reflexión)
- [ ] `docs/registro_ia.md` — registro de uso de IA actualizado hasta el cierre
- [ ] `docs/diseno.md` — secciones `[completar]` resueltas o reemplazadas por referencia a semana13
- [ ] El programa corre con `python src/main.py` sin errores desde cero (sin archivos previos)
- [ ] El directorio `data/` está en `.gitignore` o los archivos `.bin` no están commiteados
- [ ] El historial de commits es legible: cada commit describe qué se cambió y por qué

---

## 2. Preparación de la defensa oral

### Preguntas probables sobre el código

**Sobre archivos binarios:**
- ¿Por qué usaron registros de longitud fija y no JSON o CSV?
- ¿Qué hace el prefijo `=` en el formato de `struct`?
- ¿Qué pasa si el programa termina a mitad de una escritura?

**Sobre el índice:**
- ¿Por qué el índice es un diccionario y no una lista?
- ¿Cuándo se actualiza el índice? ¿Y cuándo se reconstruye desde cero?
- ¿Qué pasaría si el índice en memoria y el archivo en disco se desincronizaran?

**Sobre el ordenamiento:**
- ¿Por qué eligieron Insertion Sort y no Merge Sort o Quick Sort?
- ¿Cuál es la complejidad de Insertion Sort en el mejor caso? ¿Y en el peor?
- ¿Qué significa que un algoritmo sea estable?

**Sobre la política de rechazo:**
- ¿Por qué rechazar en lugar de registrar el faltante?
- ¿Cómo modificarían el sistema para soportar ambas políticas?

**Sobre la complejidad:**
- ¿Cuál es la operación más costosa del sistema?
- ¿Cómo escalaría el sistema si el inventario tuviera 100.000 productos?

### Preguntas probables sobre el proceso

- ¿Qué fue lo más difícil de implementar?
- ¿Qué cambiarían si empezaran de nuevo?
- ¿Cómo usaron IA generativa y cómo verificaron sus respuestas?
- ¿Cómo se dividieron el trabajo entre los integrantes?

---

## 3. Demo sugerida para la defensa

Secuencia recomendada para mostrar el sistema en vivo:

1. Ejecutar el programa desde cero (sin archivos previos) → muestra que `inicializar_archivos` funciona
2. Agregar dos o tres productos con distintos stocks y precios
3. Registrar entradas y salidas → mostrar un rechazo por stock insuficiente
4. Mostrar alertas de reposición → verificar que aparecen los productos correctos
5. Listar inventario ordenado por descripción y luego por stock → mostrar el ordenamiento
6. Ver historial de un producto → mostrar los movimientos registrados
7. Mostrar valorización y estadísticas
8. Mostrar reporte de rotación

---

## 4. Integrantes y roles

| Integrante | Rol | Módulos a cargo |
|---|---|---|
| Argañin, Milagros | SubCordinadora | [completar] |
| Rodriguez, Tomás Ezequiel | Coordinador | [completar] |
