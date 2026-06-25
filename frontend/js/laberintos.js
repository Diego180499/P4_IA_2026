/** Vista de laberintos predefinidos: consume GET /api/v1/mazes y los muestra como galería. */
(function () {
  const { initShell, toast } = window.RoboMazeUI;
  initShell();

  const statusEl = document.getElementById("gallery-status");
  const galleryEl = document.getElementById("gallery");
  const errorEl = document.getElementById("gallery-error");
  const errorMsgEl = document.getElementById("gallery-error-msg");

  document.getElementById("retry-btn").addEventListener("click", load);

  load();

  async function load() {
    show(statusEl);
    hide(galleryEl);
    hide(errorEl);

    try {
      const mazes = await window.RoboMazeAPI.listMazes();
      renderGallery(mazes);
      hide(statusEl);
      show(galleryEl);
    } catch (err) {
      hide(statusEl);
      errorMsgEl.textContent = err.detail || err.message;
      show(errorEl);
    }
  }

  function renderGallery(mazes) {
    galleryEl.innerHTML = "";
    mazes.forEach((maze) => galleryEl.appendChild(buildTile(maze)));
  }

  function buildTile(maze) {
    const rows = maze.grid.length;
    const cols = maze.grid[0].length;
    const walls = maze.grid.flat().filter((v) => v === 1).length;

    const tile = document.createElement("article");
    tile.className = "maze-tile";
    tile.innerHTML = `
      <div class="maze-tile-preview"><div class="preview-grid"></div></div>
      <div class="maze-tile-body">
        <h3>${escapeHtml(maze.name)}</h3>
        <p>${escapeHtml(maze.description)}</p>
        <div class="maze-meta">
          <span>Tamaño <b>${rows}×${cols}</b></span>
          <span>Muros <b>${walls}</b></span>
          <span>ID <b>${escapeHtml(maze.id)}</b></span>
        </div>
        <div class="maze-tile-actions">
          <button class="btn btn-primary" data-act="search">Buscar ruta</button>
          <button class="btn btn-ghost" data-act="compare">Comparar</button>
        </div>
      </div>`;

    // Vista previa (solo lectura) usando el componente de cuadrícula.
    const previewHost = tile.querySelector(".preview-grid");
    const preview = new MazeGrid(previewHost, { editable: false });
    previewHost.classList.add("readonly");
    preview.setState({ grid: maze.grid, start: maze.start, goal: maze.goal });

    const payload = { grid: maze.grid, start: maze.start, goal: maze.goal, name: maze.name };
    tile.querySelector('[data-act="search"]').addEventListener("click", () => {
      window.RoboMazeStorage.setSelectedMaze(payload);
      toast(`"${maze.name}" cargado. Abriendo búsqueda…`, "success", 1500);
      setTimeout(() => (location.href = "buscar.html"), 350);
    });
    tile.querySelector('[data-act="compare"]').addEventListener("click", () => {
      window.RoboMazeStorage.setSelectedMaze(payload);
      toast(`"${maze.name}" cargado. Abriendo comparación…`, "success", 1500);
      setTimeout(() => (location.href = "comparar.html"), 350);
    });

    return tile;
  }

  function show(el) { el.classList.remove("hidden"); }
  function hide(el) { el.classList.add("hidden"); }

  function escapeHtml(str) {
    return String(str).replace(/[&<>"']/g, (c) => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
    }[c]));
  }
})();
