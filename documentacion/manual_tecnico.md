# Manual Técnico — RoboMaze

**Proyecto:** RoboMaze · Búsqueda de rutas en laberintos (Práctica 4 · Búsqueda en espacios de estados)
**Versión:** 1.0.0
**Componentes:** Frontend web (HTML/CSS/JavaScript) + Backend API REST (Python + FastAPI)

---

## Índice

1. [Descripción general del sistema](#1-descripción-general-del-sistema)
2. [Documentación técnica del Frontend](#2-documentación-técnica-del-frontend)
   - 2.1 Tecnologías usadas
   - 2.2 Patrón de diseño usado
   - 2.3 Responsabilidad de cada vista
   - 2.4 Distribución de carpetas
   - 2.5 Tecnología usada para consumir la API REST
   - 2.6 Paleta de colores
   - 2.7 Aportes técnicos adicionales
3. [Documentación técnica del Backend](#3-documentación-técnica-del-backend)
   - 3.1 Tecnologías usadas
   - 3.2 Patrón de diseño usado
   - 3.3 Detalle de cada endpoint
   - 3.4 Distribución de carpetas
   - 3.5 Hechos y reglas para el manejo lógico (Prolog)
   - 3.6 Responsabilidades de Prolog
   - 3.7 Responsabilidades de Python
   - 3.8 Pasos para iniciar el backend en local
   - 3.9 Aportes técnicos adicionales
4. [Despliegue conjunto con Docker](#4-despliegue-conjunto-con-docker)

---

## 1. Descripción general del sistema

RoboMaze es una aplicación web que permite visualizar cómo un agente encuentra
su camino dentro de un laberinto usando algoritmos clásicos de búsqueda en
espacios de estados: **BFS** (búsqueda en anchura), **DFS** (búsqueda en
profundidad) y, de forma opcional, **A\*** (búsqueda informada con heurística
Manhattan).

El sistema está separado en dos componentes desacoplados:

- **Backend (FastAPI):** expone una API REST que recibe el laberinto, las
  posiciones de inicio y meta, y el algoritmo a ejecutar. Toda la lógica de
  búsqueda se ejecuta aquí, con lógica pura (sin librerías de pathfinding y sin
  base de datos: el estado vive en memoria).
- **Frontend (HTML/CSS/JS):** interfaz web que permite dibujar el laberinto,
  configurar inicio/meta, ejecutar la búsqueda y visualizar la ruta, el orden de
  exploración y las métricas. El frontend **solo interactúa y visualiza**: no
  resuelve la búsqueda.

La convención de la cuadrícula es: `0` = celda libre, `1` = obstáculo (muro).
Las coordenadas son `(row, col)` con origen `(0, 0)` en la esquina superior
izquierda.

---

## 2. Documentación técnica del Frontend

### 2.1 Tecnologías usadas

El frontend está construido íntegramente con tecnologías web nativas, **sin
frameworks y sin ningún paso de compilación** (no hay Node, ni bundlers, ni
transpiladores):

| Tecnología | Uso en el proyecto |
|------------|--------------------|
| **HTML5** | Estructura de las 4 vistas (multipágina, no SPA). |
| **CSS3** | Estilos globales en un único archivo `styles.css`. Uso intensivo de variables CSS (`:root`), CSS Grid y Flexbox para el layout, y `clamp()` para tipografía responsiva. |
| **JavaScript (ES6+, vanilla)** | Toda la lógica de interfaz: clases (`class`), módulos por IIFE, `fetch` con `async/await`, `Promise`, plantillas literales, eventos `pointer`. No se usan librerías externas. |
| **Fetch API** | Comunicación con el backend (cliente REST). |
| **SVG inline** | Iconografía de la navbar, tarjetas y banners (sin dependencias de iconos). |
| **sessionStorage** | Paso del laberinto seleccionado entre vistas. |
| **Nginx** (despliegue) | Sirve el sitio estático dentro del contenedor Docker. |

> Nota: el frontend es un sitio **estático multipágina**. Cada `.html` carga
> únicamente los scripts que necesita mediante etiquetas `<script>` (no hay
> sistema de módulos ES; el código se comparte vía objetos globales en `window`).

### 2.2 Patrón de diseño usado

El frontend aplica una combinación de patrones organizados por responsabilidad:

- **Module Pattern (IIFE):** cada archivo de lógica de página (`home.js`,
  `buscar.js`, `comparar.js`, `laberintos.js`) es una función autoejecutable
  `(function () { ... })()` que encapsula su estado y no contamina el ámbito
  global. Solo se exponen utilidades compartidas a través de espacios de nombres
  en `window` (`window.RoboMazeAPI`, `window.RoboMazeUI`, `window.MazeGrid`,
  `window.RoboMazeStorage`).

- **Separación por capas (Separation of Concerns):** la responsabilidad está
  claramente repartida:
  - `config.js` → configuración (URL base del backend).
  - `api.js` → capa de acceso a datos / cliente REST.
  - `storage.js` → persistencia ligera entre vistas.
  - `ui.js` → utilidades de interfaz transversales (navbar, toasts, formato).
  - `maze-grid.js` → componente de presentación reutilizable.
  - `*.js` por página → controlador/orquestador de cada vista.

- **Componente reutilizable (orientado a objetos):** `MazeGrid` es una **clase**
  que encapsula el renderizado y la interacción de la cuadrícula. Se reutiliza en
  todas las vistas en dos modos (`editable: true` para editar, `editable: false`
  para previsualizar/mostrar resultados). Es el equivalente a un "componente" de
  UI hecho a mano.

- **Patrón Fachada (Facade) en el cliente API:** `RoboMazeAPI` ofrece un método
  por endpoint (`listMazes`, `getMaze`, `search`, `compare`, `health`, `info`) y
  oculta los detalles de `fetch`, serialización JSON y normalización de errores
  detrás de una interfaz simple.

### 2.3 Responsabilidad de cada vista

El sitio está organizado **por tareas**: cada vista consume un servicio concreto
del backend y se enfoca en una acción.

| Vista | Archivo HTML / JS | Servicio backend consumido | Responsabilidad |
|-------|-------------------|----------------------------|-----------------|
| **Inicio** | `index.html` / `home.js` | `GET /` y `GET /api/v1/health` | Página de aterrizaje. Muestra la navegación por tareas (tarjetas), un mini-laberinto decorativo y el **estado de conexión con el backend** (servicio, versión y enlace a `/docs`). Permite volver a comprobar la conexión. |
| **Laberintos predefinidos** | `laberintos.html` / `laberintos.js` | `GET /api/v1/mazes` | Galería que lista los 5 laberintos de prueba del backend. Renderiza una previsualización (solo lectura) de cada uno y permite cargarlo directamente en *Buscar* o *Comparar*. Maneja estados de carga, error y reintento. |
| **Buscar una ruta** | `buscar.html` / `buscar.js` | `POST /api/v1/search` (+ `GET /api/v1/mazes/{id}`) | Editor interactivo del laberinto: dibujo de muros (clic y arrastre), colocación de inicio/meta, ajuste de tamaño, carga de predefinidos y selección de algoritmo. Ejecuta **un** algoritmo y visualiza la ruta, el orden de exploración (animado o instantáneo) y las métricas (longitud, nodos explorados, tiempo). |
| **Comparar algoritmos** | `comparar.html` / `comparar.js` | `POST /api/v1/search/compare` | Ejecuta **varios** algoritmos sobre el mismo laberinto. Muestra una tabla resumen que resalta el ganador en cada métrica (ruta más corta, menos nodos, más rápido) y tableros lado a lado con el resultado de cada algoritmo. |

Vistas auxiliares compartidas (no son páginas, son módulos): la **navbar** y el
**indicador de conexión** son inyectados por `ui.js` en todas las páginas
(fuente única, principio DRY).

### 2.4 Distribución de carpetas

```
frontend/
├── index.html          # Vista Inicio (navegación + estado del backend)
├── laberintos.html     # Vista Galería de laberintos predefinidos
├── buscar.html         # Vista Editor + ejecución de un algoritmo
├── comparar.html       # Vista Comparación de algoritmos
├── css/
│   └── styles.css      # Hoja de estilos global (paleta, layout, componentes)
├── js/
│   ├── config.js       # Configuración: URL base y prefijo del backend
│   ├── api.js          # Cliente de la API REST (un método por endpoint)
│   ├── storage.js      # Paso del laberinto seleccionado entre vistas (sessionStorage)
│   ├── ui.js           # Navbar, indicador de conexión, toasts, helpers de formato
│   ├── maze-grid.js    # Componente clase MazeGrid (edición + animación + render)
│   ├── home.js         # Lógica/controlador de index.html
│   ├── laberintos.js   # Lógica/controlador de laberintos.html
│   ├── buscar.js       # Lógica/controlador de buscar.html
│   └── comparar.js     # Lógica/controlador de comparar.html
├── Dockerfile          # Imagen Nginx que sirve el sitio estático
├── nginx.conf          # Configuración de Nginx (multipágina, no-cache de .js)
├── .dockerignore
└── README.md
```

**Criterio de organización:** los archivos `.html` son las vistas; `css/`
contiene la presentación; `js/` separa el código en utilidades transversales
(`config`, `api`, `storage`, `ui`, `maze-grid`) y un controlador por página
(`home`, `laberintos`, `buscar`, `comparar`). El orden de carga de los `<script>`
en cada HTML garantiza que las dependencias globales existan antes de usarse
(`config` → `api` → `storage` → `ui` → `maze-grid` → controlador de la página).

### 2.5 Tecnología usada para consumir la API REST del backend

El consumo de la API se realiza con la **Fetch API** nativa del navegador,
centralizada en `js/api.js`. Aspectos clave de la implementación:

- **Configuración externa:** la URL base (`API_BASE`) y el prefijo
  (`API_PREFIX = /api/v1`) viven en `js/config.js` (objeto
  `window.ROBOMAZE_CONFIG`), de modo que cambiar el host/puerto del backend no
  requiere tocar el cliente.

- **Función `request()` única:** todas las llamadas pasan por una función
  interna que:
  - construye la URL, define el método y serializa el cuerpo a JSON;
  - añade la cabecera `Content-Type: application/json` solo cuando hay cuerpo;
  - usa `async/await` y devuelve el JSON ya parseado;
  - **normaliza los errores** del backend en una clase propia `ApiError` que
    captura el código HTTP, el tipo de error y un mensaje legible.

- **Manejo de los formatos de error del backend:** la función `parseErrorDetail()`
  entiende tanto los errores de dominio (`{ error, detail }`) como los de
  validación de FastAPI (`{ detail: [...] }`), y produce un mensaje único para
  mostrar al usuario.

- **Errores de red:** si `fetch` falla por conexión, se lanza un `ApiError` de
  tipo `NetworkError` con un mensaje claro ("No se pudo conectar con el
  backend...").

- **Interfaz tipo fachada `RoboMazeAPI`** con un método por endpoint:

  | Método JS | Llamada HTTP |
  |-----------|--------------|
  | `RoboMazeAPI.info()` | `GET /` |
  | `RoboMazeAPI.health()` | `GET /api/v1/health` |
  | `RoboMazeAPI.listMazes()` | `GET /api/v1/mazes` |
  | `RoboMazeAPI.getMaze(id)` | `GET /api/v1/mazes/{id}` |
  | `RoboMazeAPI.search({grid, start, goal, algorithm})` | `POST /api/v1/search` |
  | `RoboMazeAPI.compare({grid, start, goal, algorithms})` | `POST /api/v1/search/compare` |

El backend tiene **CORS abierto** (`*`), por lo que el navegador consume la API
directamente sin necesidad de proxy.

### 2.6 Paleta de colores

La paleta se define como variables CSS en `:root` dentro de `css/styles.css`. Se
compone de tres colores de marca (azules) más colores funcionales añadidos para
diferenciar con claridad los estados del laberinto.

**Colores de marca:**

| Nombre | Variable CSS | Hex | Uso principal |
|--------|--------------|-----|---------------|
| Azul Imperial | `--azul-imperial` | `#2455A6` | Acción principal (botones), ruta solución. |
| Azul Costanero | `--azul-costanero` | `#2E847C` | Acento secundario, *eyebrows*, ganador. |
| Azul Índigo | `--azul-indigo` | `#182C8E` | Chrome oscuro (cabecera/héroe), muros. |

**Variantes de marca:** `--azul-imperial-600 #1D4790`, `--azul-imperial-300 #6F95CF`,
`--azul-costanero-300 #76B3AC`, `--azul-indigo-900 #122073`.

**Colores funcionales (estados del laberinto y UI):**

| Concepto | Variable CSS | Hex | Uso |
|----------|--------------|-----|-----|
| Inicio | `--start` | `#16A36B` (verde) | Celda de inicio. |
| Meta | `--goal` | `#E0533D` (rojo/ámbar) | Celda de meta. |
| Explorado | `--visited` | `#BCD2F1` (azul claro) | Nodos visitados durante la búsqueda. |
| Ruta | `--path` | `#2455A6` (= Azul Imperial) | Ruta solución encontrada. |

**Colores de superficie y texto:**

| Concepto | Variable | Hex |
|----------|----------|-----|
| Fondo | `--bg` | `#EEF2F8` |
| Superficie | `--surface` | `#FFFFFF` |
| Superficie 2 | `--surface-2` | `#F6F8FC` |
| Borde | `--border` | `#DBE3EF` |
| Texto | `--text` | `#16223A` |
| Texto suave | `--text-soft` | `#5A6781` |
| Texto tenue | `--text-faint` | `#8A96AD` |

> Justificación de diseño documentada en el propio CSS: se partió de la paleta de
> marca (tres azules) y se añadieron **verde** para el inicio y **rojo/ámbar**
> para la meta, buscando mejor legibilidad y accesibilidad al distinguir estados.

### 2.7 Aportes técnicos adicionales

- **Componente `MazeGrid` con animación:** además de renderizar la cuadrícula y
  permitir la edición por *pointer events* (compatibles con mouse y táctil),
  anima el `visited_order` devuelto por el backend mediante `setInterval`, con
  velocidad configurable, y luego pinta la ruta. Expone `cancelAnimation()`,
  `showResultInstant()` y `animateResult()` (este último devuelve una `Promise`).

- **Sistema de notificaciones (toasts)** y **indicador de conexión** en tiempo
  real con el backend (consulta periódica de `/health`), centralizados en `ui.js`.

- **Manejo correcto del caso "sin ruta":** el backend responde HTTP `200` con
  `found: false`; el frontend lo interpreta como resultado válido (no como error)
  y lo informa, mientras que los errores `400/404/422` sí se muestran como
  notificaciones de error.

- **Accesibilidad/responsividad:** layout fluido con CSS Grid/Flexbox,
  tipografía responsiva con `clamp()` y atributos `aria-hidden` en elementos
  puramente decorativos.

---

## 3. Documentación técnica del Backend

### 3.1 Tecnologías usadas

El backend es un **microservicio exclusivamente en Python**. La búsqueda se
implementa con lógica pura, sin librerías de pathfinding y sin base de datos.

| Tecnología | Versión | Uso en el proyecto |
|------------|---------|--------------------|
| **Python** | 3.10+ (imagen Docker: 3.12-slim) | Lenguaje del backend. |
| **FastAPI** | 0.115.6 | Framework web para construir la API REST. Genera la documentación interactiva (Swagger/ReDoc) automáticamente. |
| **Uvicorn** | 0.34.0 | Servidor ASGI que ejecuta la aplicación. |
| **Pydantic** | 2.10.4 | Validación y serialización de datos (DTOs / esquemas del contrato HTTP). |
| **pytest** | 8.3.4 | Pruebas unitarias y de integración. |
| **httpx** | 0.28.1 | Cliente HTTP usado por los tests (`TestClient`). |
| **Librería estándar** | — | `collections.deque` (BFS), `heapq` + `itertools` (A\*), listas (DFS), `time.perf_counter` (medición), `dataclasses`, `abc`. |

### 3.2 Patrón de diseño usado

El backend **no usa el patrón MVC**. Aplica una **Arquitectura por Capas
(Layered Architecture)** muy cercana a *Clean Architecture* / diseño guiado por
el dominio, combinada con varios patrones de diseño GoF. A continuación se
detalla cada uno y el porqué de su elección.

**Arquitectura por capas (de afuera hacia adentro):**

1. **Capa de presentación / API** (`app/api/`, `app/schemas/`): routers,
   endpoints, mappers y DTOs Pydantic. Conoce HTTP, pero no la lógica de
   búsqueda.
2. **Capa de aplicación / servicios** (`app/domain/services/`): orquesta los
   casos de uso (validar, seleccionar algoritmo, ejecutar, comparar). No conoce
   HTTP.
3. **Capa de dominio** (`app/domain/models/`, `app/domain/algorithms/`): lógica
   pura (entidades `Maze`, `Position`, `SearchResult` y los algoritmos). No
   depende de FastAPI ni de Pydantic.
4. **Capa de datos** (`app/repositories/`, `app/data/`): acceso a los laberintos
   predefinidos almacenados en memoria.

*¿Por qué arquitectura por capas?* Porque desacopla la lógica de búsqueda (el
corazón académico de la práctica) del framework web. El dominio puede probarse de
forma aislada (sin levantar el servidor) y se podría cambiar FastAPI por otro
framework, o la API por una CLI, sin reescribir los algoritmos.

**Patrones de diseño concretos empleados:**

- **Strategy (Estrategia)** — `app/domain/algorithms/`. Cada algoritmo (BFS, DFS,
  A\*) implementa la interfaz abstracta `SearchStrategy.search(maze, start, goal)`.
  *¿Por qué?* Permite intercambiar el algoritmo de búsqueda sin modificar el
  código que lo consume (los servicios y endpoints son idénticos para los tres),
  cumpliendo el principio Abierto/Cerrado.

- **Factory (Fábrica)** — `app/domain/algorithms/factory.py`. La función
  `get_strategy(name)` devuelve la instancia de estrategia correspondiente a un
  nombre (`"bfs"`, `"dfs"`, `"astar"`) a partir de un registro central.
  *¿Por qué?* Centraliza la creación y el registro de algoritmos. Añadir uno
  nuevo solo requiere registrarlo en un punto, sin tocar servicios ni endpoints.

- **Repository (Repositorio)** — `app/repositories/maze_repository.py`. Abstrae
  el acceso a los laberintos predefinidos (hoy un diccionario en memoria).
  *¿Por qué?* Aísla a los servicios del origen de los datos; si mañana se usara
  una base de datos o un archivo, solo cambiaría el repositorio.

- **DTO + Mapper** — `app/schemas/` y `app/api/v1/mappers.py`. Los esquemas
  Pydantic definen el contrato HTTP y los mappers convierten entre DTOs y
  entidades de dominio. *¿Por qué?* Desacopla el contrato externo (la API) del
  modelo interno; cada uno puede evolucionar por separado.

- **Manejo centralizado de excepciones** — `app/core/exceptions.py`. Excepciones
  de dominio (`InvalidPositionError`, `InvalidMazeError`,
  `UnsupportedAlgorithmError`, `MazeNotFoundError`) con un *exception handler*
  registrado en FastAPI que las traduce a respuestas JSON consistentes.

### 3.3 Detalle de cada endpoint

Prefijo de la API: `/api/v1`. Todos los cuerpos son JSON. Convención de la
cuadrícula: `0` = libre, `1` = muro; coordenadas `(row, col)` con origen
`(0,0)` arriba-izquierda.

---

#### 3.3.1 `GET /`

- **URL:** `/`
- **Path/Query params:** ninguno.
- **Request Body:** ninguno.
- **Response Body:**
  ```json
  { "service": "RoboMaze API", "version": "1.0.0", "docs": "/docs" }
  ```
- **Responsabilidad:** endpoint raíz; devuelve información básica del servicio
  (nombre, versión y ruta de la documentación).

---

#### 3.3.2 `GET /api/v1/health`

- **URL:** `/api/v1/health`
- **Path/Query params:** ninguno.
- **Request Body:** ninguno.
- **Response Body:**
  ```json
  { "status": "ok", "service": "RoboMaze API", "version": "1.0.0" }
  ```
- **Responsabilidad:** verifica que el servicio está activo (*health check*). Lo
  consume el indicador de conexión del frontend y el `HEALTHCHECK` de Docker.

---

#### 3.3.3 `GET /api/v1/mazes`

- **URL:** `/api/v1/mazes`
- **Path/Query params:** ninguno.
- **Request Body:** ninguno.
- **Response Body:** lista de laberintos predefinidos (`PredefinedMazeDTO`):
  ```json
  [
    {
      "id": "simple",
      "name": "Simple abierto",
      "description": "Pocos obstáculos y ruta directa. Verifica correctitud básica.",
      "grid": [[0,0,0,0,0],[0,1,1,0,0],[0,0,0,0,0],[0,0,1,1,0],[0,0,0,0,0]],
      "start": { "row": 0, "col": 0 },
      "goal":  { "row": 4, "col": 4 }
    }
  ]
  ```
- **Responsabilidad:** lista los 5 laberintos de prueba almacenados en memoria
  (`simple`, `zigzag`, `sin_solucion`, `estrecho`, `grande`).

---

#### 3.3.4 `GET /api/v1/mazes/{maze_id}`

- **URL:** `/api/v1/mazes/{maze_id}`
- **Path param:** `maze_id` (string) — identificador del laberinto
  (`simple` | `zigzag` | `sin_solucion` | `estrecho` | `grande`).
- **Query params:** ninguno.
- **Request Body:** ninguno.
- **Response Body:** un único `PredefinedMazeDTO` (misma forma que un elemento de
  la lista anterior).
- **Errores:** `404 MazeNotFoundError` si el `maze_id` no existe.
- **Responsabilidad:** devuelve un laberinto predefinido concreto por su id, para
  cargarlo en el editor.

---

#### 3.3.5 `POST /api/v1/search`

- **URL:** `/api/v1/search`
- **Path/Query params:** ninguno.
- **Request Body** (`SearchRequest`):
  ```json
  {
    "maze": {
      "grid": [
        [0,0,0,1,0],
        [1,1,0,1,0],
        [0,0,0,0,0],
        [0,1,1,1,0],
        [0,0,0,0,0]
      ]
    },
    "start": { "row": 0, "col": 0 },
    "goal":  { "row": 4, "col": 4 },
    "algorithm": "bfs"
  }
  ```
  - `maze.grid`: matriz de `0/1` (todas las filas del mismo ancho; máximo
    100×100).
  - `start`, `goal`: posiciones `{ row, col }` (≥ 0).
  - `algorithm`: `"bfs"` (por defecto) | `"dfs"` | `"astar"`.
- **Response Body** (`SearchResultDTO`):
  ```json
  {
    "algorithm": "bfs",
    "found": true,
    "path": [ { "row": 0, "col": 0 }, { "row": 0, "col": 1 } ],
    "path_length": 8,
    "nodes_explored": 17,
    "execution_time_ms": 0.42,
    "visited_order": [ { "row": 0, "col": 0 } ]
  }
  ```
- **Errores:** `422 InvalidMazeError` (cuadrícula mal formada/excede tamaño),
  `422 InvalidPositionError` (inicio/meta fuera de límites o sobre un muro),
  `400 UnsupportedAlgorithmError` (algoritmo inexistente).
- **Responsabilidad:** ejecuta **un** algoritmo de búsqueda sobre el laberinto y
  devuelve la ruta, el orden de exploración y las métricas (longitud, nodos
  explorados, tiempo). El caso "no existe ruta" se devuelve con `200` y
  `found: false`.

---

#### 3.3.6 `POST /api/v1/search/compare`

- **URL:** `/api/v1/search/compare`
- **Path/Query params:** ninguno.
- **Request Body** (`CompareRequest`):
  ```json
  {
    "maze": { "grid": [[0,0],[0,0]] },
    "start": { "row": 0, "col": 0 },
    "goal":  { "row": 1, "col": 1 },
    "algorithms": ["bfs", "dfs"]
  }
  ```
  - `algorithms`: lista de algoritmos a comparar (por defecto `["bfs", "dfs"]`).
- **Response Body** (`CompareResponse`):
  ```json
  {
    "results": {
      "bfs": { "algorithm": "bfs", "found": true, "path": [], "path_length": 2,
               "nodes_explored": 4, "execution_time_ms": 0.10, "visited_order": [] },
      "dfs": { "algorithm": "dfs", "found": true, "path": [], "path_length": 2,
               "nodes_explored": 3, "execution_time_ms": 0.08, "visited_order": [] }
    },
    "comparison": {
      "shorter_path": "bfs",
      "fewer_nodes_explored": "dfs",
      "faster": "dfs"
    }
  }
  ```
- **Errores:** los mismos que `POST /search` (validación de laberinto, posiciones
  y algoritmos).
- **Responsabilidad:** ejecuta y compara **varios** algoritmos sobre el mismo
  laberinto. El bloque `comparison` indica qué algoritmo gana en cada métrica
  (ruta más corta, menos nodos explorados, más rápido), considerando solo los que
  hallaron ruta.

---

### 3.4 Distribución de carpetas

```
backend/
├── app/
│   ├── main.py                     # Punto de entrada: crea la app FastAPI, CORS,
│   │                               #   registra handlers de error e incluye routers
│   ├── core/
│   │   ├── config.py               # Configuración central (nombre, versión, CORS, límites)
│   │   └── exceptions.py           # Excepciones de dominio + exception handler JSON
│   ├── api/
│   │   └── v1/
│   │       ├── router.py           # Agrupa todos los routers de la v1
│   │       ├── mappers.py          # Conversión entidad de dominio <-> DTO
│   │       └── endpoints/
│   │           ├── health.py       # GET /health
│   │           ├── mazes.py        # GET /mazes, GET /mazes/{id}
│   │           └── search.py       # POST /search, POST /search/compare
│   ├── schemas/                    # DTOs Pydantic (contrato HTTP)
│   │   ├── maze.py                 # PositionDTO, MazeDTO, PredefinedMazeDTO
│   │   └── search.py               # SearchRequest, CompareRequest, SearchResultDTO, CompareResponse
│   ├── domain/                     # Lógica pura (independiente de FastAPI)
│   │   ├── models/
│   │   │   ├── maze.py             # Entidades Maze y Position (grafo implícito)
│   │   │   └── search_result.py    # Value object SearchResult + métricas
│   │   ├── algorithms/
│   │   │   ├── base.py             # SearchStrategy (interfaz Strategy) + utilidades
│   │   │   ├── bfs.py              # BFSStrategy (cola FIFO / deque)
│   │   │   ├── dfs.py              # DFSStrategy (pila LIFO, iterativo)
│   │   │   ├── astar.py            # AStarStrategy (heapq + heurística Manhattan)
│   │   │   └── factory.py          # get_strategy(name): registro y selección
│   │   └── services/
│   │       ├── maze_service.py     # Casos de uso de laberintos predefinidos
│   │       └── search_service.py   # Orquesta búsqueda y comparación
│   ├── repositories/
│   │   └── maze_repository.py      # Repositorio en memoria (patrón Repository)
│   └── data/
│       └── predefined_mazes.py     # 5 laberintos predefinidos (datos en memoria)
├── tests/
│   ├── test_algorithms.py          # Pruebas de los algoritmos (dominio)
│   ├── test_api.py                 # Pruebas de integración de la API
│   └── test_no_path.py             # Caso "no existe ruta"
├── Dockerfile                      # Imagen Python + Uvicorn
├── requirements.txt                # Dependencias
└── README.md
```

**Criterio de organización:** la estructura refleja las capas de la arquitectura.
La dirección de las dependencias va siempre hacia el dominio: `api` depende de
`domain`, pero `domain` no conoce a `api`. Los DTOs (`schemas`) y los mappers
mantienen la frontera entre el mundo HTTP y el modelo interno.

### 3.5 Hechos y reglas para el manejo lógico (Prolog)

> **Aclaración importante sobre el estado real del proyecto:** tras revisar todo
> el código fuente del backend, **este proyecto no utiliza Prolog**. No existe
> ningún archivo `.pl`, ni integración con un motor de lógica (por ejemplo
> `pyswip` / SWI-Prolog), ni dependencias de Prolog en `requirements.txt`. Toda
> la lógica del sistema está implementada **en Python puro**.

Por tanto, no hay "hechos" (`hechos`) ni "reglas" (`reglas`) declarados en
sintaxis Prolog. Lo que cumple el rol de la base de hechos y reglas en esta
implementación es lo siguiente, expresado en Python:

**Equivalente a los "hechos" (datos del problema):**

- La **cuadrícula** (`grid`) del laberinto: cada celda es un hecho del tipo
  "la posición (r, c) es libre" (`0`) u "obstáculo/muro" (`1`).
- Los 5 **laberintos predefinidos** en `app/data/predefined_mazes.py` (sus
  cuadrículas, inicio y meta).
- Las posiciones de **inicio** y **meta** que envía el usuario.

**Equivalente a las "reglas" (relaciones lógicas / restricciones):**

Implementadas en `app/domain/models/maze.py` y en los algoritmos:

- *Una posición es transitable* si está dentro de los límites y no es muro
  (`is_walkable` = `in_bounds` ∧ ¬`is_wall`).
- *Vecindad (4-conectividad):* dos celdas son adyacentes si difieren en una sola
  unidad arriba, abajo, izquierda o derecha (`neighbors`, deltas fijos
  `(-1,0),(1,0),(0,-1),(0,1)`).
- *Validez del laberinto:* la cuadrícula no puede estar vacía, todas las filas
  deben tener el mismo ancho y cada celda debe ser `0` o `1`.
- *Validez de posición:* inicio y meta deben existir y no estar sobre un muro.
- *Existe ruta* de inicio a meta si los algoritmos de búsqueda (BFS/DFS/A\*)
  encuentran una secuencia de celdas transitables adyacentes que conecta ambas.

Si en una iteración futura del proyecto se quisiera implementar realmente con
Prolog, los hechos serían del estilo `pared(R, C).`, `inicio(R, C).`,
`meta(R, C).`, y las reglas serían `adyacente/2`, `transitable/1` y
`camino/3` (búsqueda recursiva con acumulador de visitados). **En el estado
actual, este punto se cumple mediante Python, no Prolog.**

### 3.6 Responsabilidades de Prolog

En este proyecto **Prolog no tiene responsabilidades**, porque no se utiliza.

La práctica se resolvió íntegramente con Python (ver sección 3.7). Toda la
responsabilidad que en un enfoque lógico-declarativo habría recaído sobre Prolog
—representar hechos/reglas y resolver la búsqueda por inferencia— está aquí
asumida por el código Python del dominio (entidades + algoritmos de búsqueda en
espacios de estados).

> Si el enunciado de la práctica exige Prolog, esto representa una desviación de
> la implementación actual que conviene revisar con el equipo: el backend cumple
> el requisito funcional (resolver laberintos con BFS/DFS/A\*) pero lo hace con
> Python en lugar de Prolog.

### 3.7 Responsabilidades de Python

Python concentra **el 100% de la lógica** del backend. Sus responsabilidades, por
capa:

- **Exponer la API REST (FastAPI):** definir rutas, validar el contrato de
  entrada/salida con Pydantic, configurar CORS y traducir las excepciones de
  dominio a respuestas HTTP/JSON consistentes (`app/main.py`, `app/api/`,
  `app/schemas/`, `app/core/`).

- **Representar el dominio:** modelar el laberinto como un **grafo implícito**
  sobre una cuadrícula 2D mediante las entidades `Maze` y `Position`
  (inmutable/hashable), y el resultado con `SearchResult` (`app/domain/models/`).

- **Resolver la búsqueda en espacios de estados (núcleo algorítmico):**

  | Algoritmo | Estructura | Garantía | Archivo |
  |-----------|------------|----------|---------|
  | **BFS** | Cola FIFO (`collections.deque`) | Ruta más corta (costo uniforme) | `bfs.py` |
  | **DFS** | Pila LIFO (lista), **iterativo** | No garantiza ruta más corta | `dfs.py` |
  | **A\*** | Cola de prioridad (`heapq`) + heurística Manhattan | Ruta óptima con heurística admisible | `astar.py` |

  Todos implementan la interfaz `SearchStrategy` (Strategy), reconstruyen la ruta
  a partir de los padres y reportan `visited_order` para la animación.

- **Medir métricas:** tiempo de cómputo puro con `time.perf_counter`
  (en milisegundos), número de nodos explorados y longitud de la ruta.

- **Orquestar casos de uso:** validar entradas, seleccionar la estrategia vía
  `factory`, ejecutar y, en la comparación, determinar el ganador por métrica
  (`app/domain/services/`).

- **Gestionar los datos en memoria:** servir los laberintos predefinidos a través
  del repositorio (`app/repositories/`, `app/data/`).

- **Validar y manejar errores:** garantizar laberintos y posiciones válidos, y
  responder adecuadamente cuando no existe ruta o cuando la entrada es inválida.

- **Pruebas:** verificar algoritmos, API y el caso "sin ruta" con `pytest`
  (`tests/`).

### 3.8 Pasos para iniciar el backend en local

**Requisito previo:** Python 3.10 o superior instalado.

1. **Ubicarse en la carpeta del backend:**
   ```bash
   cd backend
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Linux / macOS
   source .venv/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Levantar el servidor (Uvicorn):**
   ```bash
   uvicorn app.main:app --reload
   ```
   Esto inicia la API en `http://localhost:8000`.

   > Si vas a usar el frontend tal como está configurado (`js/config.js` apunta a
   > `http://localhost:8001`), levanta el backend en ese puerto:
   > ```bash
   > uvicorn app.main:app --reload --port 8001
   > ```

5. **Comprobar que funciona:**
   - Documentación interactiva (Swagger): `http://localhost:8000/docs`
     (o `:8001/docs`).
   - Documentación alternativa (ReDoc): `http://localhost:8000/redoc`.
   - Health check: `GET http://localhost:8000/api/v1/health`.

6. **Ejecutar las pruebas (opcional):**
   ```bash
   pytest -v
   ```

### 3.9 Aportes técnicos adicionales

- **Sin base de datos:** todo el estado vive en memoria; el repositorio abstrae
  el origen de datos por si se quisiera persistir en el futuro.
- **Determinismo y reproducibilidad:** el orden fijo de vecinos
  `(arriba, abajo, izquierda, derecha)` y el desempate estable en el heap de A\*
  (`itertools.count`) hacen que los resultados sean reproducibles.
- **DFS iterativo:** se implementa con pila explícita en lugar de recursión para
  evitar desbordamiento de pila en laberintos grandes.
- **Límite defensivo de tamaño:** `MAX_DIMENSION = 100` evita laberintos
  desproporcionados que puedan colgar el servicio (validado en `MazeDTO`).
- **Documentación automática:** FastAPI + Pydantic generan Swagger/ReDoc sin
  esfuerzo adicional, con ejemplos incluidos en los esquemas.
- **Contenerización:** `Dockerfile` con imagen `python:3.12-slim`, capa cacheable
  de dependencias y `HEALTHCHECK` integrado contra `/api/v1/health`.

---

## 4. Despliegue conjunto con Docker

El repositorio incluye un `docker-compose.yml` que levanta ambos servicios con un
solo comando, desde la raíz del proyecto:

```bash
docker compose up --build
```

- **Frontend:** `http://localhost:8080` (servido por Nginx, puerto interno 80).
- **Backend / API docs:** `http://localhost:8001/docs` (Uvicorn, puerto interno
  8001).

> El frontend (`js/config.js`) apunta a `http://localhost:8001`. Como ese código
> corre en el **navegador del usuario**, `localhost` es la máquina del host; por
> eso el backend se publica en el puerto `8001` del host y el frontend lo
> encuentra sin cambios.

---

*Manual técnico generado a partir del análisis del código fuente del repositorio
RoboMaze (frontend + backend).*
