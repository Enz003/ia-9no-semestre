import heapq
import time


MOVIMIENTOS = [
    (-1, 0, 10),   # arriba
    (1, 0, 10),    # abajo
    (0, -1, 10),   # izquierda
    (0, 1, 10),    # derecha
    (-1, -1, 14),  # diagonal superior izquierda
    (-1, 1, 14),   # diagonal superior derecha
    (1, -1, 14),   # diagonal inferior izquierda
    (1, 1, 14),    # diagonal inferior derecha
]


class Nodo:
    """Un nodo del arbol de busqueda: celda + de donde vino + g(n)."""

    def __init__(self, celda, padre=None, g=0):
        self.celda = celda
        self.padre = padre
        self.g = g

    def camino(self):
        """Cadena de celdas desde el inicio hasta este nodo."""
        ruta, actual = [], self
        while actual is not None:
            ruta.append(actual.celda)
            actual = actual.padre
        return ruta[::-1]


class Explorador:
    """Agente que busca el camino de menor costo dentro de un Espacio.

    Con `usar_heuristica=True` corre A* (f = g + h, distancia octil).
    Con `usar_heuristica=False` la heuristica es 0 y el algoritmo se
    comporta como Dijkstra (f = g), reutilizando la misma implementacion
    tal como sugiere la guia para comparar ambos.
    """

    def __init__(self, espacio, usar_heuristica=True, traza=False):
        self.espacio = espacio
        self.usar_heuristica = usar_heuristica
        self.traza = traza
        self.pasos = []  # traza de nodos expandidos: {paso, celda, g, h, f}

    def heuristica(self, celda):
        """Distancia octil hasta la meta (0 si se usa como Dijkstra)."""
        if not self.usar_heuristica:
            return 0
        fila, columna = celda
        meta_fila, meta_columna = self.espacio.meta
        dx = abs(fila - meta_fila)
        dy = abs(columna - meta_columna)
        return 10 * max(dx, dy) + 4 * min(dx, dy)

    def _movimiento_valido(self, celda, dfila, dcolumna):
        """Vecino resultante de aplicar el movimiento, o None si no es valido.

        Ademas de limites/obstaculos, en diagonal exige que las dos celdas
        ortogonales adyacentes esten libres: si ambas estan bloqueadas no
        se puede "cortar" la esquina de forma irreal (regla 7 de la guia).
        """
        vecino = (celda[0] + dfila, celda[1] + dcolumna)
        if not self.espacio.es_transitable(vecino):
            return None

        if dfila != 0 and dcolumna != 0:
            lateral_1 = (celda[0] + dfila, celda[1])
            lateral_2 = (celda[0], celda[1] + dcolumna)
            if not self.espacio.es_transitable(lateral_1) or not self.espacio.es_transitable(lateral_2):
                return None

        return vecino

    def sucesores(self, nodo):
        """Genera hasta 8 nodos hijos aplicando los movimientos permitidos."""
        hijos = []
        for dfila, dcolumna, costo in MOVIMIENTOS:
            vecino = self._movimiento_valido(nodo.celda, dfila, dcolumna)
            if vecino is not None:
                hijos.append(Nodo(vecino, padre=nodo, g=nodo.g + costo))
        return hijos

    def buscar(self):
        """Ejecuta la busqueda y devuelve el resultado con metricas.

        Se detiene cuando la meta se EXTRAE de OPEN (no cuando se genera),
        lo que garantiza optimalidad. `mejor_g` guarda el mejor costo real
        conocido para cada celda, y se actualiza si se descubre un camino
        mas barato hacia una celda ya vista pero aun no expandida.
        """
        inicio_reloj = time.perf_counter()
        orden = 0  # desempate estable en el heap
        inicio, meta = self.espacio.inicio, self.espacio.meta

        frontera = [(self.heuristica(inicio), orden, Nodo(inicio))]  # OPEN
        mejor_g = {inicio: 0}
        cerrados = set()  # CLOSED
        self.pasos = []
        paso = 0

        while frontera:
            _, _, nodo = heapq.heappop(frontera)

            if nodo.celda in cerrados:
                continue
            cerrados.add(nodo.celda)

            paso += 1
            h = self.heuristica(nodo.celda)
            self.pasos.append({"paso": paso, "celda": nodo.celda, "g": nodo.g, "h": h, "f": nodo.g + h})
            if self.traza:
                print(f"PASO {paso}\nNodo seleccionado: {nodo.celda}\n"
                      f"g(n) = {nodo.g}\nh(n) = {h}\nf(n) = {nodo.g + h}\n")

            if nodo.celda == meta:
                camino = nodo.camino()
                return {
                    "camino": camino,
                    "costo": nodo.g,
                    "movimientos": len(camino) - 1,
                    "nodos_explorados": len(cerrados),
                    "celdas_camino": len(camino),
                    "tiempo": time.perf_counter() - inicio_reloj,
                }

            for hijo in self.sucesores(nodo):
                if hijo.celda in cerrados:
                    continue
                if hijo.g < mejor_g.get(hijo.celda, float("inf")):
                    mejor_g[hijo.celda] = hijo.g
                    orden += 1
                    f = hijo.g + self.heuristica(hijo.celda)
                    heapq.heappush(frontera, (f, orden, hijo))

        return {
            "camino": None,
            "costo": float("inf"),
            "movimientos": 0,
            "nodos_explorados": len(cerrados),
            "celdas_camino": 0,
            "tiempo": time.perf_counter() - inicio_reloj,
        }
