class Espacio:
    """Espacio de busqueda: cuadricula con obstaculos, inicio y meta."""

    def __init__(self, filas, columnas, obstaculos, inicio, meta):
        self.filas = filas
        self.columnas = columnas
        self.obstaculos = set(obstaculos)
        self.inicio = inicio
        self.meta = meta

        # Reglas minimas de la guia: celdas dentro de la cuadricula,
        # inicio y meta distintos, y que ninguno sea un obstaculo.
        for nombre, celda in (("inicio", inicio), ("meta", meta)):
            if not self.dentro_de_limites(celda):
                raise ValueError(f"{nombre} {celda} esta fuera de la cuadricula")
            if celda in self.obstaculos:
                raise ValueError(f"{nombre} {celda} coincide con un obstaculo")

        if inicio == meta:
            raise ValueError("inicio y meta deben ser diferentes")

    def dentro_de_limites(self, celda):
        fila, columna = celda
        return 0 <= fila < self.filas and 0 <= columna < self.columnas

    def es_obstaculo(self, celda):
        return celda in self.obstaculos

    def es_transitable(self, celda):
        return self.dentro_de_limites(celda) and not self.es_obstaculo(celda)
