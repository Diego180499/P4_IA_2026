/** Vista de búsqueda: editor de laberinto + ejecución de un algoritmo (POST /search). */
(function () {
  const { initShell, toast, formatMs } = window.RoboMazeUI;
  initShell();

  const mazeHost = document.getElementById("maze");
  const grid = new MazeGrid(mazeHost, { editable: true });

  // Estado inicial: cargar selección previa (desde "laberintos") o uno por defecto.
  const selected = window.RoboMazeStorage.getSelectedMaze();
  if (selected && selected.grid) {
    grid.setState(selected);
    document.getElementById("rows-input").value = selected.grid.length;
    document.getElementById("cols-input").value = selected.grid[0].length;
    window.RoboMazeStorage.clearSelectedMaze();
    toast(`Laberinto "${selected.name || "cargado"}" listo.`, "success", 1800);
  } else {
    grid.initEmpty(10, 10);
  }

  // --- Herramientas de edición ---
  const toolGroup = document.getElementById("tool-group");
  toolGroup.addEventListener("click", (e) => {
    const btn = e.target.closest(".tool-btn");
    if (!btn) return;
    toolGroup.querySelectorAll(".tool-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    grid.setTool(btn.dataset.tool);
  });

  // --- Tamaño / limpiar ---
  document.getElementById("resize-btn").addEventListener("click", () => {
    const rows = clampInt(document.getElementById("rows-input").value, 2, 40, 10);
    const cols = clampInt(document.getElementById("cols-input").value, 2, 40, 10);
    grid.initEmpty(rows, cols);
    resetResults();
  });

  document.getElementById("clear-btn").addEventListener("click", () => {
    grid.clearWalls();
    resetResults();
  });

  // --- Predefinidos (carga sin salir de la página) ---
  loadPresets();

  document.getElementById("preset-select").addEventListener("change", async (e) => {
    const id = e.target.value;
    if (!id) return;
    try {
      const maze = await window.RoboMazeAPI.getMaze(id);
      grid.setState({ grid: maze.grid, start: maze.start, goal: maze.goal });
      document.getElementById("rows-input").value = maze.grid.length;
      document.getElementById("cols-input").value = maze.grid[0].length;
      resetResults();
      toast(`"${maze.name}" cargado.`, "success", 1500);
    } catch (err) {
      toast(err.detail || err.message, "error");
    } finally {
      e.target.value = "";
    }
  });

  // --- Ejecutar búsqueda ---
  const runBtn = document.getElementById("run-btn");
  runBtn.addEventListener("click", runSearch);

  async function runSearch() {
    const state = grid.getState();
    if (!state.start || !state.goal) {
      toast("Define el inicio y la meta antes de buscar.", "error");
      return;
    }

    const algorithm = document.getElementById("algorithm").value;
    runBtn.disabled = true;
    runBtn.textContent = "Buscando…";

    try {
      const res = await window.RoboMazeAPI.search({
        grid: state.grid,
        start: state.start,
        goal: state.goal,
        algorithm,
      });
      await renderResult(res);
    } catch (err) {
      grid.clearOverlays();
      resetResults();
      toast(err.detail || err.message, "error", 6000);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = "Ejecutar búsqueda";
    }
  }

  async function renderResult(res) {
    const banner = document.getElementById("result-banner");
    document.getElementById("result-placeholder").classList.add("hidden");

    document.getElementById("st-algo").textContent = res.algorithm.toUpperCase();
    document.getElementById("st-len").textContent = res.found ? res.path_length : "—";
    document.getElementById("st-nodes").textContent = res.nodes_explored;
    document.getElementById("st-time").textContent = formatMs(res.execution_time_ms);

    if (res.found) {
      banner.className = "result-banner ok";
      banner.innerHTML = `${check()} Ruta encontrada: ${res.path_length} pasos, ${res.nodes_explored} nodos explorados.`;
    } else {
      banner.className = "result-banner fail";
      banner.innerHTML = `${cross()} No existe ruta entre el inicio y la meta. Se exploraron ${res.nodes_explored} nodos.`;
    }

    const animate = document.getElementById("animate").checked;
    if (animate && res.visited_order && res.visited_order.length) {
      const speed = 64 - Number(document.getElementById("speed").value); // mayor valor = más rápido
      await grid.animateResult(res.visited_order, res.found ? res.path : [], { speed });
    } else {
      grid.showResultInstant(res.visited_order || [], res.found ? res.path : []);
    }
  }

  function resetResults() {
    document.getElementById("result-banner").innerHTML = "";
    document.getElementById("result-banner").className = "";
    document.getElementById("result-placeholder").classList.remove("hidden");
    ["st-algo", "st-len", "st-nodes", "st-time"].forEach(
      (id) => (document.getElementById(id).textContent = "—")
    );
  }

  async function loadPresets() {
    try {
      const mazes = await window.RoboMazeAPI.listMazes();
      const sel = document.getElementById("preset-select");
      mazes.forEach((m) => {
        const opt = document.createElement("option");
        opt.value = m.id;
        opt.textContent = m.name;
        sel.appendChild(opt);
      });
    } catch {
      /* si falla, el selector queda solo con la opción por defecto */
    }
  }

  function clampInt(value, min, max, fallback) {
    const n = parseInt(value, 10);
    if (Number.isNaN(n)) return fallback;
    return Math.min(max, Math.max(min, n));
  }

  function check() {
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>';
  }
  function cross() {
    return '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M18 6 6 18M6 6l12 12"/></svg>';
  }
})();
