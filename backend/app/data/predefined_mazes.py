"""Laberintos predefinidos (mínimo 5) para pruebas de funcionamiento.

Cada laberinto define su cuadrícula (0 = libre, 1 = muro), las posiciones
de inicio y meta, y una breve descripción. Los datos viven en memoria;
no se usa base de datos.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List


@dataclass(frozen=True)
class PredefinedMaze:
    id: str
    name: str
    description: str
    grid: List[List[int]]
    start: tuple[int, int]
    goal: tuple[int, int]


# 1) Simple abierto: ruta directa, pocos obstáculos.
_SIMPLE = PredefinedMaze(
    id="simple",
    name="Simple abierto",
    description="Pocos obstáculos y ruta directa. Verifica correctitud básica.",
    grid=[
        [0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ],
    start=(0, 0),
    goal=(4, 4),
)

# 2) Zigzag: obliga a rodear muros; evidencia diferencias BFS vs DFS.
_ZIGZAG = PredefinedMaze(
    id="zigzag",
    name="Zigzag",
    description="Muros en zigzag que obligan a rodear. Resalta BFS vs DFS.",
    grid=[
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0],
    ],
    start=(0, 0),
    goal=(6, 6),
)

# 3) Sin solución: la meta está encerrada por muros.
_NO_SOLUTION = PredefinedMaze(
    id="sin_solucion",
    name="Sin solución",
    description="La meta queda encerrada por obstáculos. Prueba el manejo de 'no existe ruta'.",
    grid=[
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0],
    ],
    start=(0, 0),
    goal=(2, 2),
)

# 4) Pasillo estrecho: un único camino válido.
_NARROW = PredefinedMaze(
    id="estrecho",
    name="Pasillo estrecho",
    description="Un único camino serpenteante. Prueba de exploración exhaustiva.",
    grid=[
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 1, 1, 0],
    ],
    start=(0, 0),
    goal=(4, 4),
)

# 5) Grande (15x15): diferencias notables de tiempo y nodos explorados.
_LARGE = PredefinedMaze(
    id="grande",
    name="Laberinto grande",
    description="Cuadrícula 15x15 con obstáculos. Mide diferencias de rendimiento.",
    grid=[
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ],
    start=(0, 0),
    goal=(14, 14),
)


# Diccionario en memoria con todos los laberintos predefinidos.
PREDEFINED_MAZES: Dict[str, PredefinedMaze] = {
    m.id: m
    for m in (_SIMPLE, _ZIGZAG, _NO_SOLUTION, _NARROW, _LARGE)
}
