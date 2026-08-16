# Búsqueda Informada: "Primero el Mejor" y A*

> Guía de estudio para Unidad II — Resolución de problemas mediante búsqueda (IA, FP-UNA).
> Basada en el material de clase + el enfoque de Russell & Norvig.

---

## 1. ¿Por qué "informada"?

En la **búsqueda no informada** (Profundidad, Amplitud, Costo Uniforme, Dijkstra) el algoritmo es ciego: no tiene ni idea de dónde está la meta. Solo sabe qué nodos existen y cuánto cuesta lo que ya recorrió.

En la **búsqueda informada** le damos al algoritmo un dato extra sobre el problema: una **estimación de cuán lejos está cada nodo del objetivo**. Ese dato extra es la *heurística*.

**Analogía:** estás en Fernando de la Mora y querés llegar a Ciudad del Este.

- **No informada** → probás calles al azar (o por orden sistemático) hasta llegar. Funciona, pero explorás medio país.
- **Informada** → mirás la brújula. Sabés que Ciudad del Este está al este, así que priorizás las calles que van hacia allá. No es infalible (puede haber un río en el medio), pero recorta muchísimo la búsqueda.

La heurística es esa brújula: **no dice la verdad exacta, dice una estimación razonable.**

---

## 2. Las tres funciones que tenés que tener clarísimas

Este es el 90% de la unidad. Si entendés estas tres, entendés todo.

| Función | Nombre | Qué mide | ¿De dónde sale? |
|---|---|---|---|
| **g(n)** | Función de costo | Costo **real ya gastado** desde el nodo inicial hasta `n` | Se **calcula** sumando las aristas del camino recorrido |
| **h(n)** | Función heurística | Costo **estimado** desde `n` hasta el objetivo | Se **estima** con conocimiento del dominio (ej: distancia en línea recta) |
| **f(n)** | Función de evaluación | Estimación del **costo total** del camino que pasa por `n` | `f(n) = g(n) + h(n)` |

Visualmente:

```
   inicio ────────── g(n) ────────► [ n ] ┄┄┄┄┄ h(n) ┄┄┄┄┄► meta
           (pasado, real, conocido)          (futuro, estimado)

   └───────────────────── f(n) = g(n) + h(n) ─────────────────────┘
```

### Punto clave sobre h(n)

- `h(n) = 0` cuando `n` **es** el nodo objetivo (ya llegaste, no falta nada).
- `h(n)` **nunca es negativo**.
- En el ejemplo de Rumania: `h(n)` = distancia **en línea recta** de la ciudad `n` a Bucarest.
  ¿Por qué en línea recta? Porque es lo único que podés saber sin recorrer las rutas, y **nunca puede ser mayor** que la distancia real por ruta (las rutas dan vueltas, la recta no). Esto último es fundamental — lo retomamos en la sección 6.

### Regla común a los dos algoritmos

> **Siempre se expande el nodo de la frontera con el menor valor de la función de evaluación.**

La única diferencia entre "Primero el Mejor" y A* es **qué función de evaluación usan**.

---

## 3. Búsqueda Primero el Mejor (Greedy Best-First)

### Definición

Función de evaluación: **f(n) = h(n)**

Es decir: **ignora completamente g(n)**. No le importa cuánto gastaste para llegar hasta acá. Solo mira cuál nodo *parece* estar más cerca de la meta.

Por eso en inglés se llama *greedy* (voraz/glotón): siempre agarra el bocado que se ve más apetitoso ahora mismo, sin pensar en el costo acumulado.

### Algoritmo

```
1. Crear una cola con prioridad (frontera) con el nodo inicial.
2. Mientras la frontera no esté vacía:
     a. Extraer el nodo n con MENOR h(n).
     b. Si n es el objetivo → TERMINAR, devolver el camino.
     c. Marcar n como visitado.
     d. Para cada hijo de n no visitado:
          calcular h(hijo) y agregarlo a la frontera.
3. Si la frontera se vacía → no hay solución.
```

### Ejemplo: Arad → Bucarest (mapa de Rumania)

Valores de `h` (distancia en línea recta a Bucarest):

```
Arad 366 | Bucarest   0 | Craiova 160 | Fagaras 176 | Oradea 380
Pitesti 100 | Rimnicu Vilcea 193 | Sibiu 253 | Timisoara 329 | Zerind 374
```

**Paso 1 — Expandir Arad**

| Hijo | h(n) |
|---|---|
| **Sibiu** | **253** ← menor |
| Timisoara | 329 |
| Zerind | 374 |

Elegimos **Sibiu**.

**Paso 2 — Expandir Sibiu**

| Hijo | h(n) |
|---|---|
| **Fagaras** | **176** ← menor |
| Rimnicu Vilcea | 193 |
| Arad | 366 |
| Oradea | 380 |

Elegimos **Fagaras**.

**Paso 3 — Expandir Fagaras**

| Hijo | h(n) |
|---|---|
| **Bucarest** | **0** ← ¡objetivo! |
| Sibiu | 253 |

**Resultado:** `Arad → Sibiu → Fagaras → Bucarest`

**Costo real:** 140 + 99 + 211 = **450 km**

### El problema

El camino óptimo real es `Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucarest` = **418 km**.

Primero el Mejor encontró un camino **32 km peor**. ¿Por qué?

Porque en el Paso 2 miró solamente `h`: Fagaras (176) parecía estar más cerca de Bucarest que Rimnicu (193), y se fue por ahí. Pero **nunca consideró que llegar a Fagaras costaba más** y que desde Rimnicu, aunque parezca estar "más lejos", el tramo restante es mucho más barato.

> **Moraleja: mirar solo el futuro estimado y olvidar el pasado real te lleva a caminos subóptimos.**

### Desempeño

| Propiedad | Respuesta |
|---|---|
| **¿Completa?** | No en general (puede entrar en bucles o callejones sin salida). Sí si se controlan los estados repetidos y el espacio es finito. |
| **¿Óptima?** | **No.** Como acabamos de ver. |
| **Tiempo** | O(b^m) en el peor caso, pero **en la práctica suele ser muy rápida** con buena heurística. |
| **Espacio** | O(b^m) — guarda todos los nodos en memoria. |

**Ventaja real:** es rápida y usa pocas expansiones. Si necesitás *una* solución razonable ya, sirve.

---

## 4. Búsqueda A* (A estrella)

### Definición

Función de evaluación: **f(n) = g(n) + h(n)**

A* corrige exactamente el defecto de Primero el Mejor: **suma el costo real ya recorrido**.

Interpretación de `f(n)`: *"el costo total más barato estimado de una solución que pase por n"*.

Si estoy buscando la solución más barata, es razonable probar primero el nodo cuyo camino completo estimado sea el más barato. Eso es todo A*.

### Algoritmo

```
1. Frontera = cola con prioridad con el nodo inicial (g=0, f=h(inicio)).
2. Mientras la frontera no esté vacía:
     a. Extraer el nodo n con MENOR f(n).
     b. Si n es el objetivo → TERMINAR.
     c. Marcar n como visitado (lista cerrada).
     d. Para cada hijo m de n:
          g_nuevo = g(n) + costo(n, m)
          f_nuevo = g_nuevo + h(m)
          Si m no está en la frontera → agregarlo.
          Si m YA está en la frontera con un g mayor → ACTUALIZAR con el mejor.
3. Si la frontera se vacía → no hay solución.
```

> ⚠️ El paso 2.d ("actualizar si encontré un camino mejor") es el que más se olvida en los exámenes. Sin él, A* deja de ser óptimo.

### Ejemplo: Arad → Bucarest con A*

Costos de las rutas: Arad–Sibiu 140, Arad–Timisoara 118, Arad–Zerind 75, Sibiu–Fagaras 99, Sibiu–Rimnicu 80, Sibiu–Oradea 151, Rimnicu–Pitesti 97, Rimnicu–Craiova 146, Fagaras–Bucarest 211, Pitesti–Bucarest 101.

**Paso 0 — Nodo inicial**

`Arad`: g=0, h=366 → **f = 366**

**Paso 1 — Expandir Arad**

| Nodo | g(n) | h(n) | f(n) |
|---|---|---|---|
| **Sibiu** | 140 | 253 | **393** ← menor |
| Timisoara | 118 | 329 | 447 |
| Zerind | 75 | 374 | 449 |

Elegimos **Sibiu (393)**.

**Paso 2 — Expandir Sibiu (g=140)**

| Nodo | g(n) | h(n) | f(n) |
|---|---|---|---|
| **Rimnicu Vilcea** | 140+80 = 220 | 193 | **413** ← menor |
| Fagaras | 140+99 = 239 | 176 | 415 |
| Timisoara | 118 | 329 | 447 |
| Zerind | 75 | 374 | 449 |
| Arad | 140+140 = 280 | 366 | 646 |
| Oradea | 140+151 = 291 | 380 | 671 |

Elegimos **Rimnicu Vilcea (413)**.

> 👀 **Acá está la diferencia con Primero el Mejor.** Greedy había elegido Fagaras porque h=176 < h=193. A* elige Rimnicu porque **413 < 415**: el costo acumulado inclina la balanza.

**Paso 3 — Expandir Rimnicu Vilcea (g=220)**

| Nodo | g(n) | h(n) | f(n) |
|---|---|---|---|
| **Fagaras** | 239 | 176 | **415** ← menor |
| Pitesti | 220+97 = 317 | 100 | 417 |
| Timisoara | 118 | 329 | 447 |
| Craiova | 220+146 = 366 | 160 | 526 |
| Sibiu | 220+80 = 300 | 253 | 553 (peor que el ya conocido, se descarta) |

Elegimos **Fagaras (415)**.

**Paso 4 — Expandir Fagaras (g=239)**

| Nodo | g(n) | h(n) | f(n) |
|---|---|---|---|
| **Pitesti** | 317 | 100 | **417** ← menor |
| Bucarest | 239+211 = 450 | 0 | 450 |
| Timisoara | 118 | 329 | 447 |

⚠️ **Bucarest ya apareció con f=450, pero NO paramos.** A* solo se detiene cuando el objetivo es **extraído** de la frontera, no cuando es *generado*. Si parábamos acá, devolvíamos el mismo camino subóptimo que greedy.

Elegimos **Pitesti (417)**.

**Paso 5 — Expandir Pitesti (g=317)**

| Nodo | g(n) | h(n) | f(n) |
|---|---|---|---|
| **Bucarest** | 317+101 = **418** | 0 | **418** ← mejora el 450 anterior |
| Craiova | 455 | 160 | 615 |
| Rimnicu | 414 | 193 | 607 |

Bucarest se **actualiza** de 450 a 418.

**Paso 6 —** Extraemos Bucarest con f=418 → **es el objetivo → TERMINAR.**

**Resultado:** `Arad → Sibiu → Rimnicu Vilcea → Pitesti → Bucarest` = **418 km** ✅ **óptimo**

> 📌 Nota: en las diapositivas de clase aparecen f(Fagaras)=417 y f(Oradea)=661. Recalculando con los costos del mapa dan 415 y 671. Son erratas de la diapo; el orden de expansión y la conclusión final no cambian.

### Desempeño

| Propiedad | Respuesta |
|---|---|
| **¿Completa?** | Sí (si b es finito y los costos de paso tienen un mínimo > 0). |
| **¿Óptima?** | **Sí**, si h es admisible (en árboles) o consistente (en grafos). |
| **Tiempo** | Exponencial en el peor caso, pero **muchísimo mejor** que las no informadas con buena h. |
| **Espacio** | Su mayor debilidad: guarda **todos** los nodos generados en memoria. |

---

## 5. Comparación directa

| | Primero el Mejor | A* |
|---|---|---|
| Función de evaluación | `f(n) = h(n)` | `f(n) = g(n) + h(n)` |
| ¿Considera el costo ya recorrido? | ❌ No | ✅ Sí |
| ¿Considera la distancia estimada a la meta? | ✅ Sí | ✅ Sí |
| ¿Completa? | No garantizada | Sí |
| ¿Óptima? | **No** | **Sí** (con h admisible) |
| Velocidad típica | Muy rápida | Más lenta, más expansiones |
| Memoria | Alta | Alta (peor) |
| Resultado en Rumania | 450 km | **418 km** |

### Cómo encaja con lo no informado

Fijate que A* es en realidad la **generalización** de lo que ya viste:

| Algoritmo | Función de evaluación | Equivalencia |
|---|---|---|
| Costo Uniforme / Dijkstra | `f(n) = g(n)` | A* con `h(n) = 0` para todo n |
| Primero el Mejor | `f(n) = h(n)` | A* sin el término g |
| **A\*** | `f(n) = g(n) + h(n)` | El caso general |

Esto es muy útil para el examen: **si te ponen h(n) = 0 en todos los nodos, A\* se degrada exactamente a Costo Uniforme.** Sigue siendo óptimo, pero pierde toda la ventaja de la heurística.

---

## 6. Cuándo A* garantiza el óptimo: admisibilidad y consistencia

A* no es mágico. Su optimalidad depende de que la heurística cumpla ciertas condiciones.

### Heurística admisible (optimista)

> `h(n) ≤ costo real de n hasta la meta`, para todo n.

O sea: **h nunca sobreestima**. Puede decir "faltan 100" cuando en realidad faltan 150, pero **nunca** puede decir "faltan 200" cuando faltan 150.

**Por qué la distancia en línea recta es admisible:** la recta es el camino más corto entre dos puntos. Cualquier ruta real es igual o más larga. Imposible sobreestimar.

**Qué pasa si NO es admisible:** A* puede descartar prematuramente el camino óptimo porque su `f` estimado parecía muy caro. Deja de garantizar la solución óptima.

### Heurística consistente (o monótona)

> `h(n) ≤ costo(n, n') + h(n')`, para todo hijo n' de n.

Es la desigualdad triangular. Significa que la estimación **no puede mejorar bruscamente** al dar un paso.

- Consistencia ⟹ admisibilidad (toda h consistente es admisible; lo inverso no siempre).
- Con h consistente, los valores de `f` **nunca decrecen** a lo largo de un camino, y A* en grafos es óptimo sin necesidad de reabrir nodos ya cerrados.

### Resumen práctico para el examen

| Condición | Garantía |
|---|---|
| h admisible | A* óptimo en **búsqueda en árbol** |
| h consistente | A* óptimo en **búsqueda en grafo** (con lista cerrada) |
| h = 0 | A* = Costo Uniforme (óptimo, pero lento) |
| h no admisible | Sin garantía de optimalidad |

### Calidad de la heurística

Entre dos heurísticas admisibles `h1` y `h2`, si `h2(n) ≥ h1(n)` para todo n, se dice que **h2 domina a h1** y A* con h2 expandirá menos nodos. **La mejor heurística admisible es la que más se acerca al costo real sin pasarse.**

---

## 7. Ejercicio resuelto: Málaga → Santiago (el de la diapositiva)

### Datos

Rutas (km):

```
Málaga–Granada 125    Málaga–Madrid 513     Granada–Madrid 423
Granada–Valencia 491  Madrid–Salamanca 203  Madrid–Santiago 599
Madrid–Valencia 355   Madrid–Zaragoza 313   Madrid–Santander 437
Madrid–Sevilla 514    Madrid–Barcelona 603  Salamanca–Santiago 390
Valencia–Barcelona 346  Valencia–Zaragoza 309
Zaragoza–Barcelona 296  Zaragoza–Santander 394
```

Heurística `h(n)` = distancia en línea recta hasta Santiago:

```
Santiago 0 | Salamanca 326 | Santander 404 | Madrid 482 | Sevilla 633
Zaragoza 658 | Granada 737 | Málaga 763 | Valencia 771 | Barcelona 876
```

---

### 7.1 — Con Primero el Mejor `f(n) = h(n)`

**Paso 1 — Expandir Málaga**

| Hijo | h(n) |
|---|---|
| **Madrid** | **482** ← menor |
| Granada | 737 |

Elegimos **Madrid**.

**Paso 2 — Expandir Madrid**

| Hijo | h(n) |
|---|---|
| **Santiago** | **0** ← ¡objetivo! |
| Salamanca | 326 |
| Santander | 404 |
| Sevilla | 633 |
| Zaragoza | 658 |
| Granada | 737 |
| Valencia | 771 |
| Barcelona | 876 |

**Resultado:** `Málaga → Madrid → Santiago`
**Costo real:** 513 + 599 = **1112 km**
**Nodos expandidos:** solo 2. Rapidísimo.

---

### 7.2 — Con A* `f(n) = g(n) + h(n)`

**Paso 0:** `Málaga`: g=0, h=763 → **f = 763**

**Paso 1 — Expandir Málaga (g=0)**

| Nodo | g | h | f |
|---|---|---|---|
| **Granada** | 125 | 737 | **862** ← menor |
| Madrid | 513 | 482 | 995 |

Elegimos **Granada (862)**.

**Paso 2 — Expandir Granada (g=125)**

| Nodo | g | h | f |
|---|---|---|---|
| **Madrid** | 513 (por Málaga directo) | 482 | **995** ← menor |
| Valencia | 125+491 = 616 | 771 | 1387 |

> Ojo: por Granada, Madrid daría g = 125+423 = **548**, peor que los 513 que ya teníamos. **Nos quedamos con el menor g** → Madrid sigue en 513/f=995.

Elegimos **Madrid (995)**.

**Paso 3 — Expandir Madrid (g=513)**

| Nodo | g | h | f |
|---|---|---|---|
| **Salamanca** | 513+203 = 716 | 326 | **1042** ← menor |
| Santiago | 513+599 = 1112 | 0 | 1112 |
| Santander | 513+437 = 950 | 404 | 1354 |
| Valencia | 616 (ya mejor por Granada) | 771 | 1387 |
| Zaragoza | 513+313 = 826 | 658 | 1484 |
| Sevilla | 513+514 = 1027 | 633 | 1660 |
| Barcelona | 513+603 = 1116 | 876 | 1992 |

⚠️ Santiago ya está generado con f=1112, **pero no es el menor de la frontera** → no paramos.

Elegimos **Salamanca (1042)**.

**Paso 4 — Expandir Salamanca (g=716)**

| Nodo | g | h | f |
|---|---|---|---|
| **Santiago** | 716+390 = **1106** | 0 | **1106** ← mejora el 1112 |

Santiago se **actualiza** de 1112 a 1106.

**Paso 5 —** Extraemos Santiago con f=1106 → **objetivo → TERMINAR.**

**Resultado:** `Málaga → Madrid → Salamanca → Santiago`
**Costo real:** 513 + 203 + 390 = **1106 km** ✅ **óptimo**

---

### 7.3 — Comparación de resultados

| | Primero el Mejor | A* |
|---|---|---|
| Camino | Málaga → Madrid → Santiago | Málaga → Madrid → Salamanca → Santiago |
| Costo | 1112 km | **1106 km** |
| Nodos expandidos | 2 | 4 |
| ¿Óptimo? | No | **Sí** |

**Conclusión del ejercicio:** Primero el Mejor fue más rápido (expandió la mitad de nodos) pero devolvió un camino 6 km más largo. Se fue directo a Santiago desde Madrid porque `h(Santiago)=0` era irresistible, sin notar que el desvío por Salamanca (203 + 390 = 593) es más barato que el tramo directo Madrid–Santiago (599).

Es la misma solución que da Costo Uniforme en la diapositiva anterior (Santiago con 1106) — coherente, porque **ambos son óptimos**. La diferencia es que A* llegó ahí expandiendo muchos menos nodos que UCS.

---

## 8. Errores típicos que se cobran en el examen

1. **Parar cuando el objetivo se *genera*.** En A* hay que parar cuando el objetivo se **extrae** de la frontera (es el de menor f). Si parás al generarlo, perdés la optimalidad — se ve clarito en los dos ejemplos de arriba.
2. **Olvidar actualizar g cuando aparece un camino mejor.** Si un nodo ya está en la frontera y llegás con menor g, hay que reemplazar el valor.
3. **Sumar h al camino recorrido.** `g` es puro costo real de aristas. `h` nunca se acumula, se recalcula desde cero en cada nodo.
4. **Confundir h(n) con el costo de la arista.** `h(n)` es del nodo a la **meta**, no al nodo siguiente.
5. **Aplicar Primero el Mejor y esperar el camino óptimo.** No lo garantiza. Si el enunciado pide "el camino más corto", el algoritmo correcto es A* (o UCS).
6. **No marcar los nodos visitados**, y quedarse en un bucle Arad → Sibiu → Arad → Sibiu…

---

## 9. Implementación de referencia (Python)

Sirve para verificar los ejercicios a mano.

```python
import heapq

def a_estrella(grafo, h, inicio, meta, usar_g=True):
    """
    grafo: dict {nodo: [(vecino, costo), ...]}
    h:     dict {nodo: valor heuristico}
    usar_g=False  -> Primero el Mejor (greedy)
    usar_g=True   -> A*
    """
    # (f, g, nodo, camino)
    frontera = [(h[inicio], 0, inicio, [inicio])]
    mejor_g = {inicio: 0}
    visitados = set()

    while frontera:
        f, g, nodo, camino = heapq.heappop(frontera)

        if nodo == meta:                 # se detiene al EXTRAER la meta
            return camino, g

        if nodo in visitados:
            continue
        visitados.add(nodo)

        for vecino, costo in grafo[nodo]:
            if vecino in visitados:
                continue
            g_nuevo = g + costo
            # solo se agrega si mejora el mejor g conocido
            if g_nuevo < mejor_g.get(vecino, float('inf')):
                mejor_g[vecino] = g_nuevo
                f_nuevo = (g_nuevo + h[vecino]) if usar_g else h[vecino]
                heapq.heappush(frontera, (f_nuevo, g_nuevo, vecino, camino + [vecino]))

    return None, float('inf')


# --- Ejercicio Málaga -> Santiago ---
grafo = {
    'Malaga':    [('Granada', 125), ('Madrid', 513)],
    'Granada':   [('Malaga', 125), ('Madrid', 423), ('Valencia', 491)],
    'Madrid':    [('Malaga', 513), ('Granada', 423), ('Salamanca', 203),
                  ('Santiago', 599), ('Valencia', 355), ('Zaragoza', 313),
                  ('Santander', 437), ('Sevilla', 514), ('Barcelona', 603)],
    'Salamanca': [('Madrid', 203), ('Santiago', 390)],
    'Santiago':  [('Madrid', 599), ('Salamanca', 390)],
    'Valencia':  [('Granada', 491), ('Madrid', 355), ('Barcelona', 346), ('Zaragoza', 309)],
    'Zaragoza':  [('Madrid', 313), ('Valencia', 309), ('Barcelona', 296), ('Santander', 394)],
    'Santander': [('Madrid', 437), ('Zaragoza', 394)],
    'Barcelona': [('Madrid', 603), ('Valencia', 346), ('Zaragoza', 296)],
    'Sevilla':   [('Madrid', 514)],
}

h = {'Santiago': 0, 'Salamanca': 326, 'Santander': 404, 'Madrid': 482,
     'Sevilla': 633, 'Zaragoza': 658, 'Granada': 737, 'Malaga': 763,
     'Valencia': 771, 'Barcelona': 876}

print(a_estrella(grafo, h, 'Malaga', 'Santiago', usar_g=False))  # Primero el Mejor
print(a_estrella(grafo, h, 'Malaga', 'Santiago', usar_g=True))   # A*
```

Salida esperada:

```
(['Malaga', 'Madrid', 'Santiago'], 1112)
(['Malaga', 'Madrid', 'Salamanca', 'Santiago'], 1106)
```

---

## 10. Chuleta final

```
BÚSQUEDA NO INFORMADA          BÚSQUEDA INFORMADA
─────────────────────          ──────────────────
Profundidad   (LIFO)           Primero el Mejor   f = h(n)
Amplitud      (FIFO)           A*                 f = g(n) + h(n)
Costo Uniforme (f = g)
Dijkstra
```

**Las tres preguntas para identificar cualquier algoritmo:**

1. ¿Qué estructura usa la frontera? (pila / cola / cola con prioridad)
2. ¿Por qué valor ordena la cola con prioridad? (g / h / g+h)
3. ¿Es óptimo? (solo si considera g **y** la heurística no sobreestima)

---

### Bibliografía

- Russell, S. & Norvig, P. — *Inteligencia Artificial: un enfoque moderno* (cap. 3 y 4).
- García Serrano, A. — *Inteligencia Artificial: fundamentos, práctica y aplicaciones*.
