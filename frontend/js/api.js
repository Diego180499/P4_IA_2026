/**
 * Cliente de la API REST de RoboMaze.
 *
 * Centraliza todas las llamadas al backend para que las vistas no tengan
 * que repetir lógica de fetch. Cada método devuelve una promesa que resuelve
 * con el cuerpo JSON ya parseado, o lanza un ApiError con el detalle del backend.
 */

const { API_BASE, API_PREFIX } = window.ROBOMAZE_CONFIG;

/** Error enriquecido con el código HTTP y el detalle devuelto por el backend. */
class ApiError extends Error {
  constructor(message, { status = 0, type = "ApiError", detail = "" } = {}) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.type = type;
    this.detail = detail;
  }
}

/**
 * Realiza una petición y normaliza el manejo de errores.
 * El backend devuelve errores de dominio como { error, detail } y errores de
 * validación de FastAPI como { detail: [...] }.
 */
async function request(path, { method = "GET", body } = {}) {
  const url = `${API_BASE}${path}`;
  let response;

  try {
    response = await fetch(url, {
      method,
      headers: body ? { "Content-Type": "application/json" } : undefined,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (networkError) {
    throw new ApiError(
      "No se pudo conectar con el backend. Verifica que el servicio esté en ejecución.",
      { type: "NetworkError" }
    );
  }

  let data = null;
  const text = await response.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { detail: text };
    }
  }

  if (!response.ok) {
    throw new ApiError(parseErrorDetail(data), {
      status: response.status,
      type: data?.error || "HTTPError",
      detail: parseErrorDetail(data),
    });
  }

  return data;
}

/** Extrae un mensaje legible de los distintos formatos de error del backend. */
function parseErrorDetail(data) {
  if (!data) return "Error desconocido del servidor.";
  if (typeof data.detail === "string") return data.detail;
  if (Array.isArray(data.detail)) {
    return data.detail
      .map((d) => d.msg || JSON.stringify(d))
      .join(" · ");
  }
  if (data.error) return `${data.error}`;
  return "Error desconocido del servidor.";
}

const RoboMazeAPI = {
  ApiError,

  /** GET / — información básica del servicio. */
  info() {
    return request("/");
  },

  /** GET /api/v1/health — salud del servicio. */
  health() {
    return request(`${API_PREFIX}/health`);
  },

  /** GET /api/v1/mazes — lista de laberintos predefinidos. */
  listMazes() {
    return request(`${API_PREFIX}/mazes`);
  },

  /** GET /api/v1/mazes/{id} — un laberinto predefinido. */
  getMaze(mazeId) {
    return request(`${API_PREFIX}/mazes/${encodeURIComponent(mazeId)}`);
  },

  /** POST /api/v1/search — ejecuta un algoritmo sobre un laberinto. */
  search({ grid, start, goal, algorithm = "bfs" }) {
    return request(`${API_PREFIX}/search`, {
      method: "POST",
      body: { maze: { grid }, start, goal, algorithm },
    });
  },

  /** POST /api/v1/search/compare — compara varios algoritmos. */
  compare({ grid, start, goal, algorithms = ["bfs", "dfs"] }) {
    return request(`${API_PREFIX}/search/compare`, {
      method: "POST",
      body: { maze: { grid }, start, goal, algorithms },
    });
  },
};

window.RoboMazeAPI = RoboMazeAPI;
