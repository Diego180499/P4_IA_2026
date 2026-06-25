# RoboMaze — Frontend

Interfaz web del proyecto **RoboMaze** (Práctica 4). Está construida con
**HTML5, CSS3 y JavaScript puro** (sin frameworks ni paso de compilación) y
consume la API REST del microservicio backend (FastAPI). Toda la lógica de
búsqueda (BFS, DFS, A\*) vive en el backend; el frontend **solo interactúa y
visualiza** resultados, tal como exige el enunciado.

## Estructura

```
frontend/
├── index.html          # Inicio / panel: navegación + estado del backend
├── laberintos.html     # Galería de laberintos predefinidos (GET /mazes)
├── buscar.html         # Editor + ejecución de un algoritmo (POST /search)
├── comparar.html       # Comparación de algoritmos (POST /search/compare)
├── css/
│   └── styles.css      # Estilos y paleta de marca
└── js/
    ├── config.js       # URL base del backend (configurable)
    ├── api.js          # Cliente de la API REST (un método por endpoint)
    ├── storage.js      # Pasa el laberinto seleccionado entre vistas
    ├── ui.js           # Navbar, indicador de conexión, toasts, helpers
    ├── maze-grid.js    # Componente de cuadrícula (edición + animación)
    ├── home.js         # Lógica de index.html
    ├── laberintos.js   # Lógica de laberintos.html
    ├── buscar.js       # Lógica de buscar.html
    └── comparar.js     # Lógica de comparar.html
```

## Vistas

| Vista | Archivo | Servicio del backend que consume |
|-------|---------|----------------------------------|
| Inicio | `index.html` | `GET /` y `GET /api/v1/health` |
| Laberintos predefinidos | `laberintos.html` | `GET /api/v1/mazes` |
| Buscar ruta | `buscar.html` | `POST /api/v1/search` (+ `GET /api/v1/mazes/{id}`) |
| Comparar algoritmos | `comparar.html` | `POST /api/v1/search/compare` |

## Requisitos previos

El backend debe estar en ejecución. Desde la carpeta `backend/`:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Esto levanta la API en `http://localhost:8001` (documentación viva en `/docs`).

## Cómo ejecutar el frontend

Como es un sitio estático, basta con servir la carpeta `frontend/` por HTTP.
Se recomienda **no** abrir los `.html` con doble clic (`file://`), porque algunas
peticiones `fetch` pueden bloquearse; usa un servidor estático:

**Opción A — Python (incluido en la mayoría de sistemas):**

```bash
cd frontend
python -m http.server 5500
```

Luego abre `http://localhost:5500`.

**Opción B — VS Code + extensión Live Server:**

Clic derecho sobre `index.html` → *Open with Live Server*.

> El backend tiene **CORS abierto** (`*`), por lo que el navegador puede
> consumirlo directamente sin proxy.

## Configuración

Si el backend corre en otro host o puerto, edita `js/config.js`:

```js
window.ROBOMAZE_CONFIG = {
  API_BASE: "http://localhost:8001",
  API_PREFIX: "/api/v1",
};
```

## Uso rápido

1. Abre **Inicio** y verifica que el indicador del backend esté «en línea».
2. En **Laberintos**, previsualiza los 5 laberintos de prueba y carga uno en
   *Buscar* o *Comparar*.
3. En **Buscar ruta**: dibuja muros (clic y arrastre), coloca inicio/meta con
   las herramientas, elige el algoritmo y pulsa *Ejecutar búsqueda*. Activa
   *Animar exploración* para ver el orden de visita (`visited_order`).
4. En **Comparar**: selecciona dos o más algoritmos y pulsa *Comparar* para ver
   la tabla con el ganador de cada métrica y los tableros lado a lado.

## Paleta de colores

Basada en la paleta de marca indicada para el proyecto:

| Color | Hex | Uso principal |
|-------|-----|---------------|
| Azul Imperial | `#2455A6` | Acción principal, ruta solución |
| Azul Costanero | `#2E847C` | Acento secundario, ganador, inicio |
| Azul Índigo | `#182C8E` | Cabecera/héroe, muros |

Para diferenciar con claridad los estados del laberinto se añadieron dos colores
funcionales sobre la marca: **verde** para el inicio y **rojo/ámbar** para la
meta (mejor legibilidad y accesibilidad).

## Notas

- El caso «no existe ruta» llega como HTTP `200` con `found: false`; el frontend
  lo interpreta correctamente y lo informa sin tratarlo como error.
- Los errores de validación del backend (`422`, `400`, `404`) se muestran como
  notificaciones con el detalle devuelto por la API.
