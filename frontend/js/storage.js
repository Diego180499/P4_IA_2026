/**
 * Almacenamiento ligero en el navegador para pasar un laberinto entre vistas.
 *
 * No es persistencia de negocio (el backend no usa base de datos): solo sirve
 * para que al elegir un laberinto en una vista, otra vista (buscar/comparar)
 * pueda recogerlo. Usa sessionStorage para no contaminar entre sesiones.
 */
const RoboMazeStorage = {
  KEY: "robomaze.selectedMaze",

  /** Guarda el laberinto seleccionado: { grid, start, goal, name? }. */
  setSelectedMaze(maze) {
    try {
      sessionStorage.setItem(this.KEY, JSON.stringify(maze));
    } catch {
      /* almacenamiento no disponible: se ignora silenciosamente */
    }
  },

  /** Devuelve el laberinto seleccionado o null si no hay. */
  getSelectedMaze() {
    try {
      const raw = sessionStorage.getItem(this.KEY);
      return raw ? JSON.parse(raw) : null;
    } catch {
      return null;
    }
  },

  /** Limpia la selección una vez consumida. */
  clearSelectedMaze() {
    try {
      sessionStorage.removeItem(this.KEY);
    } catch {
      /* noop */
    }
  },
};

window.RoboMazeStorage = RoboMazeStorage;
