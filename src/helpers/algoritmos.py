"""Busqueda informada - Unidad II.

El arbol de busqueda NO se guarda en ninguna estructura: se genera al expandir.
Los hijos de un nodo son los vecinos de esa ciudad en el grafo del mapa, y eso
es lo unico que hay que definir a mano (`MAPA_RUMANIA` + `H_RUMANIA`).
"""

import heapq


class Nodo:
    """Un nodo del arbol de busqueda: estado + de donde vino + g(n)."""

    def __init__(self, ciudad, padre=None, costo=0):
        self.ciudad = ciudad
        self.padre = padre  # para reconstruir el camino al final
        self.costo = costo  # g(n): costo real acumulado

    def camino(self):
        """Cadena de ciudades desde el inicio hasta este nodo."""
        ruta, actual = [], self
        while actual is not None:
            ruta.append(actual.ciudad)
            actual = actual.padre
        return ruta[::-1]

    def en_el_camino(self, ciudad):
        """True si la ciudad ya aparece en la rama actual (evita ciclos)."""
        actual = self
        while actual is not None:
            if actual.ciudad == ciudad:
                return True
            actual = actual.padre
        return False

    def __repr__(self):
        return f"Nodo({self.ciudad}, g={self.costo})"


def expandir(nodo, grafo):
    """Genera los hijos de un nodo: los vecinos de su ciudad en el grafo.

    Esta es la funcion sucesora. No hay que declarar los hijos nodo por nodo:
    se derivan consultando la lista de adyacencia.
    """
    return [
        Nodo(vecino, padre=nodo, costo=nodo.costo + km)
        for vecino, km in grafo[nodo.ciudad].items()
    ]


def primero_el_mejor(inicio, meta, grafo, h, traza=False):
    """Busqueda Primero el Mejor (greedy): f(n) = h(n).

    Devuelve (camino, costo_real) o (None, inf) si no hay solucion.
    Usa lista cerrada (`visitados`), o sea busqueda en GRAFO: sin eso
    entraria en el bucle Arad -> Sibiu -> Arad -> Sibiu...
    """
    orden = 0  # desempate estable: evita que heapq compare objetos Nodo
    frontera = [(h[inicio], orden, Nodo(inicio))]
    visitados = set()

    while frontera:
        _, _, nodo = heapq.heappop(frontera)

        if nodo.ciudad == meta:
            return nodo.camino(), nodo.costo

        if nodo.ciudad in visitados:
            continue
        visitados.add(nodo.ciudad)

        hijos = [x for x in expandir(nodo, grafo) if x.ciudad not in visitados]
        if traza:
            print(f"Expandir {nodo.ciudad}:",
                  ", ".join(f"{x.ciudad}({h[x.ciudad]})"
                            for x in sorted(hijos, key=lambda x: h[x.ciudad])))

        for hijo in hijos:
            orden += 1
            heapq.heappush(frontera, (h[hijo.ciudad], orden, hijo))

    return None, float("inf")


def a_estrella(inicio, meta, grafo, h, traza=False):
    """Busqueda A*: f(n) = g(n) + h(n).

    Devuelve (camino, costo_real) o (None, inf) si no hay solucion.
    Dos detalles que hacen que sea optima y que son los que mas se olvidan:

    1. Se detiene cuando la meta se EXTRAE de la frontera, no cuando se genera.
       Bucarest aparece con f=450 al expandir Fagaras, pero recien se devuelve
       cuando sale del heap con f=418.
    2. Si se llega a una ciudad con un g menor al ya conocido, se ACTUALIZA
       (`mejor_g`); si el g nuevo es peor, el hijo se descarta.
    """
    orden = 0  # desempate estable: evita que heapq compare objetos Nodo
    frontera = [(h[inicio], orden, Nodo(inicio))]
    mejor_g = {inicio: 0}  # mejor costo real conocido para llegar a cada ciudad
    visitados = set()

    while frontera:
        _, _, nodo = heapq.heappop(frontera)

        if nodo.ciudad == meta:
            return nodo.camino(), nodo.costo

        if nodo.ciudad in visitados:
            continue
        visitados.add(nodo.ciudad)

        generados = []
        for hijo in expandir(nodo, grafo):
            # solo entra a la frontera si mejora el mejor g conocido
            if hijo.costo < mejor_g.get(hijo.ciudad, float("inf")):
                mejor_g[hijo.ciudad] = hijo.costo
                orden += 1
                f = hijo.costo + h[hijo.ciudad]
                heapq.heappush(frontera, (f, orden, hijo))
                generados.append((f, hijo))

        if traza:
            print(f"Expandir {nodo.ciudad} (g={nodo.costo}):",
                  ", ".join(f"{x.ciudad}(g={x.costo}+h={h[x.ciudad]}={f})"
                            for f, x in sorted(generados, key=lambda t: t[0]))
                  or "sin hijos que mejoren")

    return None, float("inf")
