/** Vista de comparación: editor + POST /search/compare con tabla y tableros lado a lado. */
(function () {
  const { initShell, toast, formatMs } = window.RoboMazeUI;
  initShell();

  const mazeHost = document.getElementById("maze");
  const grid = new MazeGrid(mazeHost, { editable: true });

  const ALGO_LABEL = { bfs: "BFS", dfs: "DFS", astar: "A*" };
  const boardGrids = {}; // id -> MazeGrid de cada tablero

  // Estado inicial: selección previa o por defecto.
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

  // --- Herramientas ---
  const toolGroup = document.getElementById("tool-group");
  toolGroup.addEventListener("click", (e) => {
    const btn = e.target.closest(".tool-btn");
    if (!btn) return;
    toolGroup.querySelectorAll(".tool-btn").forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    grid.setTool(btn.dataset.tool);
  });

  // --- Checkboxes de algoritmos ---
  const algoOptions = document.getElementById("algo-options");
  algoOptions.addEventListener("change", (e) => {
    const chip = e.target.closest(".algo-chip");
    if (chip) chip.classList.toggle("checked", e.target.checked);
  });

  // --- Tamaño / limpiar / predefinidos ---
  document.getElementById("resize-btn").addEventListener("click", () => {
    const rows = clampInt(document.getElementById("rows-input").value, 2, 40, 10);
    const cols = clampInt(document.getElementById("cols-input").value, 2, 40, 10);
    grid.initEmpty(rows, cols);
    hideResults();
  });

  document.getElementById("clear-btn").addEventListener("click", () => {
    grid.clearWalls();
    hideResults();
  });

  loadPresets();
  document.getElementById("preset-select").addEventListener("change", async (e) => {
    const id = e.target.value;
    if (!id) return;
    try {
      const maze = await window.RoboMazeAPI.getMaze(id);
      grid.setState({ grid: maze.grid, start: maze.start, goal: maze.goal });
      document.getElementById("rows-input").value = maze.grid.length;
      document.getElementById("cols-input").value = maze.grid[0].length;
      hideResults();
      toast(`"${maze.name}" cargado.`, "success", 1500);
    } catch (err) {
      toast(err.detail || err.message, "error");
    } finally {
      e.target.value = "";
    }
  });

  // --- Ejecutar comparación ---
  const runBtn = document.getElementById("run-btn");
  runBtn.addEventListener("click", runCompare);

  async function runCompare() {
    const state = grid.getState();
    if (!state.start || !state.goal) {
      toast("Define el inicio y la meta antes de comparar.", "error");
      return;
    }

    const algorithms = Array.from(
      algoOptions.querySelectorAll("input:checked")
    ).map((i) => i.value);

    if (algorithms.length < 2) {
      toast("Selecciona al menos dos algoritmos para comparar.", "error");
      return;
    }

    runBtn.disabled = true;
    runBtn.textContent = "Comparando…";

    try {
      const data = await window.RoboMazeAPI.compare({
        grid: state.grid,
        start: state.start,
        goal: state.goal,
        algorithms,
      });
      renderComparison(data, state);
    } catch (err) {
      toast(err.detail || err.message, "error", 6000);
    } finally {
      runBtn.disabled = false;
      runBtn.textContent = "Comparar";
    }
  }

  function renderComparison(data, state) {
    const { results, comparison } = data;
    const ids = Object.keys(results);

    document.getElementById("compare-placeholder").classList.add("hidden");
    document.getElementById("compare-results").classList.remove("hidden");

    renderSummaryTable(results, comparison, ids);
    renderBoards(results, state, ids);
  }

  function renderSummaryTable(results, comparison, ids) {
    const winner = {
      path_length: comparison.shorter_path,
      nodes_explored: comparison.fewer_nodes_explored,
      execution_time_ms: comparison.faster,
    };

    const header =
      "<thead><tr><th>Métrica</th>" +
      ids.map((id) => `<th>${badge(id)}</th>`).join("") +
      "</tr></thead>";

    const rows = [
      metricRow("¿Ruta encontrada?", ids, (r) => (r.found ? "Sí" : "No"), null, results),
      metricRow("Longitud de ruta", ids, (r) => (r.found ? r.path_length : "—"), winner.path_length, results),
      metricRow("Nodos explorados", ids, (r) => r.nodes_explored, winner.nodes_explored, results),
      metricRow("Tiempo de ejecución", ids, (r) => formatMs(r.execution_time_ms), winner.execution_time_ms, results),
    ].join("");

    document.getElementById("summary-table").innerHTML = header + "<tbody>" + rows + "</tbody>";
  }

  function metricRow(label, ids, valueFn, winnerId, results) {
    const cells = ids
      .map((id) => {
        const isWin = winnerId && winnerId === id;
        const tag = isWin ? '<span class="tag-win">Mejor</span>' : "";
        return `<td class="${isWin ? "winner" : ""}">${valueFn(results[id])}${tag}</td>`;
      })
      .join("");
    return `<tr><th>${label}</th>${cells}</tr>`;
  }

  function renderBoards(results, state, ids) {
    const boardsEl = document.getElementById("boards");
    boardsEl.innerHTML = "";
    Object.keys(boardGrids).forEach((k) => delete boardGrids[k]);

    ids.forEach((id) => {
      const r = results[id];
      const card = document.createElement("div");
      card.className = "board-card";
      card.innerHTML = `
        <h3>${ALGO_LABEL[id] || id.toUpperCase()} ${badge(id)}</h3>
        <div class="board-grid"></div>
        <div class="mini-stats">
          <div class="mini-stat"><div class="v">${r.found ? r.path_length : "—"}</div><div class="l">Ruta</div></div>
          <div class="mini-stat"><div class="v">${r.nodes_explored}</div><div class="l">Nodos</div></div>
          <div class="mini-stat"><div class="v">${formatMs(r.execution_time_ms)}</div><div class="l">Tiempo</div></div>
        </div>
        ${r.found ? "" : '<p class="muted mt-1">Este algoritmo no encontró ruta.</p>'}`;

      boardsEl.appendChild(card);

      const host = card.querySelector(".board-grid");
      host.classList.add("readonly");
      const boardGrid = new MazeGrid(host, { editable: false });
      boardGrid.setState({ grid: state.grid, start: state.start, goal: state.goal });
      boardGrid.showResultInstant(r.visited_order || [], r.found ? r.path : []);
      boardGrids[id] = boardGrid;
    });
  }

  function badge(id) {
    const cls = id === "bfs" ? "badge-bfs" : id === "dfs" ? "badge-dfs" : "badge-astar";
    return `<span class="algo-badge ${cls}">${ALGO_LABEL[id] || id}</span>`;
  }

  function hideResults() {
    document.getElementById("compare-results").classList.add("hidden");
    document.getElementById("compare-placeholder").classList.remove("hidden");
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
      /* opcional */
    }
  }

  function clampInt(value, min, max, fallback) {
    const n = parseInt(value, 10);
    if (Number.isNaN(n)) return fallback;
    return Math.min(max, Math.max(min, n));
  }
})();
