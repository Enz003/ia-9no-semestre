# IA — 9no Semestre (FP-UNA)

Código, notebooks y material de la materia **Inteligencia Artificial**.

> 📌 **Voy a estar subiendo acá todo el material y los algoritmos de la
> materia a medida que avancemos.** Cada unidad nueva, cada ejercicio resuelto
> y cada implementación va a aparecer en este repositorio. Conviene que
> actualicen su copia antes de cada clase y sobre todo antes de los parciales,
> porque lo que bajaron hace dos semanas ya puede estar viejo.

Está abierto para toda la clase: pueden bajarlo, usarlo y modificarlo en sus
computadoras libremente.

---

## Cómo bajarlo a tu computadora

Hay dos formas. Si nunca usaste Git, andá directo a la Opción A.

### Opción A — Sin instalar nada (descarga directa)

No necesitás cuenta de GitHub ni instalar ningún programa.

1. Entrá a **https://github.com/Enz003/ia-9no-semestre**
2. Botón verde **`< > Code`** (arriba a la derecha del listado de archivos)
3. **Download ZIP**
4. Descomprimí la carpeta donde quieras

Listo, ya tenés todo.

⚠️ **La contra:** el ZIP es una foto del momento en que lo bajaste. Cuando yo
suba material nuevo, tu carpeta **no se entera sola** — tenés que volver a
bajar el ZIP. Y si trabajaste sobre los archivos, guardá tu versión aparte
antes de descomprimir la nueva, porque si no la pisás.

### Opción B — Con Git (recomendada si vas a seguir el semestre entero)

**Aclaración importante: Git y GitHub no son lo mismo.** Git es un programa
que se instala en tu computadora; GitHub es el sitio web donde está guardado
este repositorio. Para bajar el material y mantenerlo actualizado **solo
necesitás Git — no hace falta tener cuenta de GitHub**.

Instalar Git: https://git-scm.com/downloads

Después, en la terminal, parado en la carpeta donde quieras guardarlo:

```bash
git clone https://github.com/Enz003/ia-9no-semestre.git
```

Y cada vez que quieras traer lo último que subí, desde adentro de la carpeta:

```bash
git pull
```

Eso es todo. Un comando y tenés el material actualizado, sin volver a bajar
nada a mano.

---

## Cómo correr el código

El proyecto usa [**uv**](https://docs.astral.sh/uv/), que se encarga solo de
instalar Python y todas las librerías (numpy, pandas, jupyter, networkx…).
**No hace falta que tengas Python instalado de antes**: uv lo instala él mismo
si no lo encuentra.

### 1. Instalar uv (una sola vez)

En Windows, abrí **PowerShell** y pegá:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

En macOS o Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Cerrá y volvé a abrir la terminal para que tome el cambio.

### 2. Instalar las dependencias del proyecto

Parado dentro de la carpeta del repositorio:

```bash
uv sync
```

Esto crea el entorno virtual (`.venv/`) e instala exactamente las mismas
versiones de las librerías que uso yo, así a todos nos funciona igual.

### 3. Abrir los notebooks

```bash
uv run jupyter lab
```

Se abre en el navegador. Los notebooks están en `notebooks/`.

### 4. Correr un script suelto

```bash
uv run python src/mi_script.py
```

> 💡 El `uv run` adelante reemplaza al típico "activar el entorno". No hace
> falta hacer `activate` ni nada: `uv run <comando>` ya lo corre adentro del
> entorno correcto.

---

## Qué hay adentro

| Carpeta | Contenido |
|---|---|
| `src/` | Implementaciones de los algoritmos, listas para importar |
| `notebooks/` | Notebooks de Jupyter con los ejercicios resueltos y propuestos |
| `Unidad 2/Material/` | Material de cátedra y guías de estudio |
| `data/` | Datos (el contenido no se sube al repo, solo la carpeta) |
| `tests/` | Tests con pytest |

### Contenido actual

**Unidad II — Búsqueda informada**

- `src/helpers/algoritmos.py` — clase `Nodo`, función sucesora `expandir()`,
  **Primero el Mejor** (`f = h`) y **A\*** (`f = g + h`), las dos con
  parámetro `traza=True` para ver paso a paso qué nodo se expande y con qué
  valores.
- `notebooks/unidad-2-ejemplo-resuelto.ipynb` — el mapa de Rumania
  (Arad → Bucarest) resuelto con los dos algoritmos.
- `notebooks/unidad-2-ejercicio-propuesto.ipynb` — el mapa de España
  (Málaga → Santiago).

Ejemplo de uso:

```python
from helpers.algoritmos import primero_el_mejor, a_estrella

primero_el_mejor("Arad", "Bucarest", MAPA_RUMANIA, H_RUMANIA, traza=True)
# (['Arad', 'Sibiu', 'Fagaras', 'Bucarest'], 450)

a_estrella("Arad", "Bucarest", MAPA_RUMANIA, H_RUMANIA, traza=True)
# (['Arad', 'Sibiu', 'RimnicuVilcea', 'Pitesti', 'Bucarest'], 418)
```

---

## Si encontrás un error o querés aportar algo

Copiá, modificá y usá lo que quieras en tu máquina — para eso está.

Ahora, para que un cambio entre **a este repositorio**, el repo está
configurado así: **nadie tiene permiso de escritura directa, ni siquiera yo.**
Todo cambio entra por *Pull Request* y **yo lo tengo que aprobar**. Es a
propósito, para que el material no se rompa ni se pise entre varios.

Si querés proponer algo:

1. **La forma fácil:** avisame por WhatsApp o abrí un *Issue* acá arriba en la
   pestaña **Issues** contando qué encontraste. Yo lo subo.
2. **Con Pull Request** (necesitás cuenta de GitHub): apretá **Fork** arriba a
   la derecha, hacé el cambio en tu copia, y desde ahí abrí un *Pull Request*
   hacia este repositorio. Me llega la notificación y lo reviso.

---

## Problemas comunes

| Síntoma | Qué pasa |
|---|---|
| `uv: command not found` | No instalaste uv, o no cerraste y volviste a abrir la terminal después de instalarlo |
| `ModuleNotFoundError: helpers` | El notebook necesita `sys.path.append("./../src")` en la primera celda, y tenés que abrir Jupyter desde la raíz del proyecto |
| Editaste un `.py` y el notebook sigue usando la versión vieja | Reiniciá el kernel, o agregá `%load_ext autoreload` y `%autoreload 2` en la primera celda |
| `git pull` tira conflicto | Modificaste un archivo que yo también cambié. Guardá tu versión aparte, hacé `git stash`, `git pull`, y después reincorporá tus cambios |
