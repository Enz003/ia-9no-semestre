# IA - Entorno de trabajo

Scaffolding del entorno para las tareas de la materia Inteligencia Artificial.
Gestionado con [uv](https://docs.astral.sh/uv/).

## Activar el entorno

`uv` crea y gestiona el entorno virtual (`.venv/`) automáticamente. No hace
falta activarlo a mano: alcanza con anteponer `uv run` a cualquier comando.

```
uv sync
```

Si preferís activarlo manualmente en la shell:

```
.venv\Scripts\activate
```

## Agregar paquetes

```
uv add <paquete>
uv add --dev <paquete>   # dependencias de desarrollo
```

## Correr un notebook

```
uv run jupyter lab
```

Los notebooks van en `notebooks/`.

## Correr un script

```
uv run python src/archivo.py
```

## Estructura

- `src/` - código fuente (módulos, funciones auxiliares)
- `notebooks/` - notebooks de Jupyter
- `data/` - datos (ignorado por git salvo `.gitkeep`)
- `tests/` - tests (pytest)

## Tests y linting

```
uv run pytest
uv run ruff check .
```
