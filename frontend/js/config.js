/**
 * Configuración global del frontend de RoboMaze.
 *
 * API_BASE: URL base donde corre el microservicio backend (FastAPI).
 * Cambiala aquí si el backend corre en otro host/puerto.
 */
window.ROBOMAZE_CONFIG = {
  API_BASE: "http://localhost:8001",
  API_PREFIX: "/api/v1",
};
