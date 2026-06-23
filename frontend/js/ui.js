/**
 * Utilidades de interfaz compartidas por todas las vistas:
 *  - Inyección de la barra de navegación (fuente única, DRY).
 *  - Indicador de conexión con el backend.
 *  - Notificaciones tipo "toast".
 *  - Pequeños helpers de formato.
 */

const NAV_LINKS = [
  { href: "index.html", label: "Inicio", icon: "home" },
  { href: "laberintos.html", label: "Laberintos", icon: "grid" },
  { href: "buscar.html", label: "Buscar ruta", icon: "search" },
  { href: "comparar.html", label: "Comparar", icon: "compare" },
];

const ICONS = {
  home: '<path d="M3 11.5 12 4l9 7.5"/><path d="M5 10v10h14V10"/>',
  grid: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  search: '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
  compare: '<path d="M12 3v18"/><path d="M5 8 2 11l3 3"/><path d="m19 8 3 3-3 3"/><path d="M2 11h7"/><path d="M15 11h7"/>',
  robot: '<rect x="4" y="8" width="16" height="12" rx="2"/><path d="M12 8V4"/><circle cx="9" cy="14" r="1.2"/><circle cx="15" cy="14" r="1.2"/><path d="M2 13v3M22 13v3"/>',
};

function svgIcon(name, size = 20) {
  return `<svg class="icon" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">${ICONS[name] || ""}</svg>`;
}

/** Construye la barra de navegación y la inserta en <header id="app-header">. */
function renderNavbar() {
  const header = document.getElementById("app-header");
  if (!header) return;

  const current = location.pathname.split("/").pop() || "index.html";
  const links = NAV_LINKS.map((link) => {
    const active = link.href === current ? " active" : "";
    return `<a class="nav-link${active}" href="${link.href}">${svgIcon(link.icon, 18)}<span>${link.label}</span></a>`;
  }).join("");

  header.innerHTML = `
    <div class="nav-inner">
      <a class="brand" href="index.html">
        <span class="brand-mark">${svgIcon("robot", 22)}</span>
        <span class="brand-text">Robo<strong>Maze</strong></span>
      </a>
      <nav class="nav-links">${links}</nav>
      <div class="nav-status">
        <span id="conn-badge" class="conn-badge conn-checking">
          <span class="conn-dot"></span><span class="conn-label">Conectando…</span>
        </span>
      </div>
    </div>`;
}

/** Consulta /health y actualiza el indicador de conexión del navbar. */
async function refreshConnectionBadge() {
  const badge = document.getElementById("conn-badge");
  if (!badge) return;
  const label = badge.querySelector(".conn-label");

  badge.className = "conn-badge conn-checking";
  label.textContent = "Conectando…";

  try {
    const data = await window.RoboMazeAPI.health();
    const ok = data && data.status === "ok";
    badge.className = `conn-badge ${ok ? "conn-online" : "conn-offline"}`;
    label.textContent = ok ? `Backend en línea · v${data.version || "?"}` : "Backend con problemas";
  } catch {
    badge.className = "conn-badge conn-offline";
    label.textContent = "Backend desconectado";
  }
}

/** Muestra una notificación temporal. type: "info" | "success" | "error". */
function toast(message, type = "info", timeout = 4000) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    container.className = "toast-container";
    document.body.appendChild(container);
  }

  const el = document.createElement("div");
  el.className = `toast toast-${type}`;
  el.textContent = message;
  container.appendChild(el);

  requestAnimationFrame(() => el.classList.add("show"));
  setTimeout(() => {
    el.classList.remove("show");
    setTimeout(() => el.remove(), 300);
  }, timeout);
}

/** Formatea milisegundos con precisión adaptativa. */
function formatMs(ms) {
  if (ms == null || Number.isNaN(ms)) return "—";
  if (ms < 1) return `${ms.toFixed(4)} ms`;
  if (ms < 100) return `${ms.toFixed(3)} ms`;
  return `${ms.toFixed(2)} ms`;
}

/** Inicializa la cabecera y el indicador de conexión al cargar la página. */
function initShell() {
  renderNavbar();
  refreshConnectionBadge();
  const badge = document.getElementById("conn-badge");
  if (badge) badge.addEventListener("click", refreshConnectionBadge);
}

window.RoboMazeUI = {
  initShell,
  renderNavbar,
  refreshConnectionBadge,
  toast,
  formatMs,
  svgIcon,
};
