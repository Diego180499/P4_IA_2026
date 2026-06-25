/** Lógica de la página de inicio: shell, mini-laberinto decorativo y estado del backend. */
(function () {
  const { initShell } = window.RoboMazeUI;
  initShell();

  buildHeroArt();
  loadBackendInfo();

  const recheck = document.getElementById("recheck-btn");
  if (recheck) {
    recheck.addEventListener("click", () => {
      window.RoboMazeUI.refreshConnectionBadge();
      loadBackendInfo();
    });
  }

  /** Dibuja un mini-laberinto estático 6x6 con una ruta de ejemplo (solo decorativo). */
  function buildHeroArt() {
    const art = document.getElementById("hero-art");
    if (!art) return;
    // 0 libre, 1 muro, s inicio, g meta, p ruta
    const layout = [
      ["s", "p", "p", 1, 0, 0],
      [0, 1, "p", 1, 0, 1],
      [0, 1, "p", "p", "p", 0],
      [1, 0, 1, 1, "p", 1],
      [0, 0, 0, 1, "p", "p"],
      [0, 1, 0, 0, 1, "g"],
    ];
    const classFor = { s: "s", g: "g", p: "p", 1: "w" };
    art.innerHTML = "";
    for (const row of layout) {
      for (const cell of row) {
        const span = document.createElement("span");
        if (classFor[cell]) span.classList.add(classFor[cell]);
        art.appendChild(span);
      }
    }
  }

  /** Consulta la info del servicio y la muestra. */
  async function loadBackendInfo() {
    const detail = document.getElementById("backend-detail");
    if (!detail) return;
    detail.textContent = "Comprobando conexión con el microservicio…";

    try {
      const [info, health] = await Promise.all([
        window.RoboMazeAPI.info(),
        window.RoboMazeAPI.health(),
      ]);
      const ok = health && health.status === "ok";
      detail.innerHTML = ok
        ? `Conectado a <strong>${info.service}</strong> versión <strong>${info.version}</strong>. Documentación interactiva disponible en <code>${window.ROBOMAZE_CONFIG.API_BASE}/docs</code>.`
        : "El backend respondió, pero el estado no es saludable.";
    } catch (err) {
      detail.innerHTML = `No se pudo conectar con el backend en <code>${window.ROBOMAZE_CONFIG.API_BASE}</code>. Inicia el microservicio (<code>uvicorn app.main:app --reload</code>) y vuelve a comprobar.`;
    }
  }
})();
