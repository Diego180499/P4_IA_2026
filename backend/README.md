# RoboMaze — Backend

Microservicio en **Python + FastAPI** que resuelve la búsqueda de rutas en
laberintos mediante algoritmos de búsqueda en espacios de estados: **BFS**,
**DFS** y, de forma opcional, **A\***. Toda la lógica de búsqueda se ejecuta en
el backend con lógica pura (sin librerías de pathfinding ni base de datos).

## Requisitos

- Python 3.10 o superior.

## Instalación

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Ejecución

```bash
uvicorn app.main:app --reload
```

El servicio queda disponible en `http://localhost:8000`.

- Documentación interactiva (Swagger): `http://localhost:8000/docs`
- Documentación alternativa (ReDoc): `http://localhost:8000/redoc`

## Endpoints principales

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET`  | `/api/v1/health` | Estado del servicio |
| `GET`  | `/api/v1/mazes` | Lista los laberintos predefinidos (≥5) |
| `GET`  | `/api/v1/mazes/{id}` | Devuelve un laberinto predefinido |
| `POST` | `/api/v1/search` | Ejecuta un algoritmo (BFS, DFS o A\*) |
| `POST` | `/api/v1/search/compare` | Compara varios algoritmos |

### Ejemplo de petición — `POST /api/v1/search`

```json
{
  "maze": {
    "grid": [
      [0, 0, 0, 1, 0],
      [1, 1, 0, 1, 0],
      [0, 0, 0, 0, 0],
      [0, 1, 1, 1, 0],
      [0, 0, 0, 0, 0]
    ]
  },
  "start": { "row": 0, "col": 0 },
  "goal":  { "row": 4, "col": 4 },
  "algorithm": "bfs"
}
```

### Respuesta

```json
{
  "algorithm": "bfs",
  "found": true,
  "path": [ { "row": 0, "col": 0 }, "..." ],
  "path_length": 8,
  "nodes_explored": 17,
  "execution_time_ms": 0.42,
  "visited_order": [ { "row": 0, "col": 0 }, "..." ]
}
```

Convención de la cuadrícula: `0` = celda libre, `1` = obstáculo. Las coordenadas
son `(row, col)` con origen `(0, 0)` en la esquina superior izquierda.

## Pruebas

```bash
cd backend
pytest -v
```

## Arquitectura

Arquitectura por capas con patrones **Strategy** (algoritmos intercambiables),
**Factory** (selección por nombre) y **Repository** (laberintos en memoria).

```
app/
├── main.py            # App FastAPI, CORS, manejadores de error
├── core/              # Configuración y excepciones
├── api/v1/            # Routers, endpoints y mappers
├── schemas/           # DTOs Pydantic (contrato HTTP)
├── domain/
│   ├── models/        # Maze, Position, SearchResult
│   ├── algorithms/    # BFS, DFS, A* (lógica pura) + factory
│   └── services/      # Casos de uso
├── repositories/      # Almacén en memoria
└── data/              # Laberintos predefinidos
```

## Restricciones cumplidas

- BFS y DFS implementados con lógica pura (solo estructuras estándar).
- Backend exclusivamente en Python; toda la búsqueda corre aquí.
- Sin base de datos: el estado vive en memoria.
- Sin servicios externos de IA generativa.
- Manejo de errores ante rutas inexistentes y entradas inválidas.
- 5 laberintos predefinidos para pruebas.
