/**
 * Componente reutilizable de cuadrícula de laberinto.
 *
 * Responsabilidades (solo visualización e interacción, sin lógica de búsqueda):
 *  - Renderizar una cuadrícula a partir de un grid de 0/1.
 *  - Edición: pintar/borrar muros (arrastrando), fijar inicio y meta.
 *  - Visualización: resaltar la ruta y animar el orden de exploración
 *    (visited_order) que devuelve el backend.
 *
 * El backend usa coordenadas { row, col } con origen arriba-izquierda.
 */
class MazeGrid {
  /**
   * @param {HTMLElement} container
   * @param {Object} options
   * @param {boolean} [options.editable=true]
   * @param {Function} [options.onChange] callback cuando cambia el estado.
   */
  constructor(container, options = {}) {
    this.container = container;
    this.editable = options.editable !== false;
    this.onChange = options.onChange || (() => {});

    this.grid = [];
    this.start = null;
    this.goal = null;
    this.tool = "wall"; // wall | start | goal

    this.cells = []; // matriz de referencias a los nodos DOM
    this._animTimer = null;
    this._painting = false;
    this._paintValue = 1;

    this.container.classList.add("maze-grid");
    this._bindGlobalPointerUp();
  }

  /** Crea una cuadrícula vacía de rows x cols con inicio y meta por defecto. */
  initEmpty(rows, cols) {
    const grid = Array.from({ length: rows }, () => Array(cols).fill(0));
    const start = { row: 0, col: 0 };
    const goal = { row: rows - 1, col: cols - 1 };
    this.setState({ grid, start, goal });
  }

  /** Carga un estado completo { grid, start, goal }. */
  setState({ grid, start, goal }) {
    this.cancelAnimation();
    this.grid = grid.map((r) => r.slice());
    this.start = start ? { ...start } : null;
    this.goal = goal ? { ...goal } : null;
    this._render();
    this.onChange(this.getState());
  }

  /** Devuelve una copia del estado actual. */
  getState() {
    return {
      grid: this.grid.map((r) => r.slice()),
      start: this.start ? { ...this.start } : null,
      goal: this.goal ? { ...this.goal } : null,
    };
  }

  get rows() {
    return this.grid.length;
  }

  get cols() {
    return this.grid[0] ? this.grid[0].length : 0;
  }

  setTool(tool) {
    this.tool = tool;
  }

  /** Quita muros (deja inicio y meta). */
  clearWalls() {
    this.cancelAnimation();
    this.grid = this.grid.map((row) => row.map(() => 0));
    this._render();
    this.onChange(this.getState());
  }

  // ---------------------------------------------------------------------------
  // Renderizado
  // ---------------------------------------------------------------------------
  _render() {
    const { rows, cols } = this;
    this.container.style.setProperty("--cols", cols);
    this.container.style.setProperty("--rows", rows);
    this.container.innerHTML = "";
    this.cells = [];

    for (let r = 0; r < rows; r++) {
      const rowRefs = [];
      for (let c = 0; c < cols; c++) {
        const cell = document.createElement("div");
        cell.className = "cell";
        cell.dataset.row = r;
        cell.dataset.col = c;
        this._applyBaseClass(cell, r, c);
        if (this.editable) this._attachCellEvents(cell, r, c);
        this.container.appendChild(cell);
        rowRefs.push(cell);
      }
      this.cells.push(rowRefs);
    }
  }

  _applyBaseClass(cell, r, c) {
    cell.classList.remove("cell--wall", "cell--start", "cell--goal");
    if (this.grid[r][c] === 1) cell.classList.add("cell--wall");
    if (this.start && this.start.row === r && this.start.col === c) {
      cell.classList.add("cell--start");
    }
    if (this.goal && this.goal.row === r && this.goal.col === c) {
      cell.classList.add("cell--goal");
    }
  }

  _refreshCell(r, c) {
    const cell = this.cells[r] && this.cells[r][c];
    if (cell) this._applyBaseClass(cell, r, c);
  }

  // ---------------------------------------------------------------------------
  // Interacción de edición
  // ---------------------------------------------------------------------------
  _attachCellEvents(cell, r, c) {
    cell.addEventListener("pointerdown", (e) => {
      e.preventDefault();
      this.cancelAnimation();
      this._handlePointer(r, c, true);
    });
    cell.addEventListener("pointerenter", () => {
      if (this._painting) this._handlePointer(r, c, false);
    });
  }

  _handlePointer(r, c, isStart) {
    if (this.tool === "wall") {
      if (this._isStart(r, c) || this._isGoal(r, c)) return;
      if (isStart) {
        this._painting = true;
        this._paintValue = this.grid[r][c] === 1 ? 0 : 1;
      }
      if (this.grid[r][c] !== this._paintValue) {
        this.grid[r][c] = this._paintValue;
        this._refreshCell(r, c);
        this.onChange(this.getState());
      }
    } else if (this.tool === "start" && isStart) {
      if (this.grid[r][c] === 1 || this._isGoal(r, c)) return;
      const prev = this.start;
      this.start = { row: r, col: c };
      if (prev) this._refreshCell(prev.row, prev.col);
      this._refreshCell(r, c);
      this.onChange(this.getState());
    } else if (this.tool === "goal" && isStart) {
      if (this.grid[r][c] === 1 || this._isStart(r, c)) return;
      const prev = this.goal;
      this.goal = { row: r, col: c };
      if (prev) this._refreshCell(prev.row, prev.col);
      this._refreshCell(r, c);
      this.onChange(this.getState());
    }
  }

  _isStart(r, c) {
    return this.start && this.start.row === r && this.start.col === c;
  }

  _isGoal(r, c) {
    return this.goal && this.goal.row === r && this.goal.col === c;
  }

  _bindGlobalPointerUp() {
    this._onUp = () => {
      this._painting = false;
    };
    window.addEventListener("pointerup", this._onUp);
  }

  // ---------------------------------------------------------------------------
  // Visualización de resultados
  // ---------------------------------------------------------------------------
  clearOverlays() {
    for (const row of this.cells) {
      for (const cell of row) {
        cell.classList.remove("cell--visited", "cell--path");
      }
    }
  }

  cancelAnimation() {
    if (this._animTimer) {
      clearInterval(this._animTimer);
      this._animTimer = null;
    }
  }

  _markVisited(r, c) {
    if (this._isStart(r, c) || this._isGoal(r, c)) return;
    const cell = this.cells[r] && this.cells[r][c];
    if (cell) cell.classList.add("cell--visited");
  }

  _markPath(r, c) {
    if (this._isStart(r, c) || this._isGoal(r, c)) return;
    const cell = this.cells[r] && this.cells[r][c];
    if (cell) {
      cell.classList.remove("cell--visited");
      cell.classList.add("cell--path");
    }
  }

  /** Pinta de inmediato (sin animación) el orden visitado y la ruta. */
  showResultInstant(visitedOrder = [], path = []) {
    this.cancelAnimation();
    this.clearOverlays();
    for (const p of visitedOrder) this._markVisited(p.row, p.col);
    for (const p of path) this._markPath(p.row, p.col);
  }

  /**
   * Anima el orden de exploración y luego dibuja la ruta.
   * @returns {Promise<void>} resuelve cuando termina la animación.
   */
  animateResult(visitedOrder = [], path = [], { speed = 18 } = {}) {
    this.cancelAnimation();
    this.clearOverlays();

    return new Promise((resolve) => {
      let i = 0;
      const stepMs = Math.max(4, speed);

      this._animTimer = setInterval(() => {
        if (i >= visitedOrder.length) {
          this.cancelAnimation();
          for (const p of path) this._markPath(p.row, p.col);
          resolve();
          return;
        }
        const p = visitedOrder[i++];
        this._markVisited(p.row, p.col);
      }, stepMs);
    });
  }

  destroy() {
    this.cancelAnimation();
    window.removeEventListener("pointerup", this._onUp);
  }
}

window.MazeGrid = MazeGrid;
