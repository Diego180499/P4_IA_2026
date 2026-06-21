"""Entidades del dominio: Position y Maze.

Estas clases representan el laberinto como un grafo implícito sobre una
cuadrícula 2D. NO dependen de FastAPI ni de Pydantic: son lógica pura,
de modo que pueden probarse de forma aislada y reutilizarse.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, List

from app.core.exceptions import InvalidMazeError, InvalidPositionError

# Valores permitidos dentro de la cuadrícula.
FREE = 0  # Celda transitable.
WALL = 1  # Obstáculo / muro.

# Vecinos en 4-conectividad, en orden fijo y determinista
# (arriba, abajo, izquierda, derecha) para que los resultados sean reproducibles.
_DELTAS: tuple[tuple[int, int], ...] = ((-1, 0), (1, 0), (0, -1), (0, 1))


@dataclass(frozen=True)
class Position:
    """Una posición (fila, columna) dentro del laberinto.

    Es inmutable y hashable para poder usarse en conjuntos y diccionarios.
    """

    row: int
    col: int

    def as_tuple(self) -> tuple[int, int]:
        return (self.row, self.col)


class Maze:
    """Laberinto representado como una matriz de celdas (0 libre, 1 muro)."""

    def __init__(self, grid: List[List[int]]) -> None:
        self._validate_grid(grid)
        self.grid: List[List[int]] = grid
        self.rows: int = len(grid)
        self.cols: int = len(grid[0])

    # ------------------------------------------------------------------ #
    # Validación
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_grid(grid: List[List[int]]) -> None:
        if not grid or not grid[0]:
            raise InvalidMazeError("El laberinto no puede estar vacío.")

        width = len(grid[0])
        for r, fila in enumerate(grid):
            if len(fila) != width:
                raise InvalidMazeError(
                    f"Todas las filas deben tener el mismo ancho "
                    f"(fila {r} difiere)."
                )
            for c, celda in enumerate(fila):
                if celda not in (FREE, WALL):
                    raise InvalidMazeError(
                        f"Valor de celda inválido en ({r}, {c}): {celda}. "
                        f"Solo se permiten {FREE} (libre) o {WALL} (muro)."
                    )

    def validate_position(self, pos: Position, label: str) -> None:
        """Verifica que una posición exista y sea transitable."""
        if not self.in_bounds(pos):
            raise InvalidPositionError(
                f"La posición {label} ({pos.row}, {pos.col}) está fuera "
                f"de los límites del laberinto."
            )
        if self.is_wall(pos):
            raise InvalidPositionError(
                f"La posición {label} ({pos.row}, {pos.col}) está sobre "
                f"un obstáculo."
            )

    # ------------------------------------------------------------------ #
    # Consultas
    # ------------------------------------------------------------------ #
    def in_bounds(self, pos: Position) -> bool:
        return 0 <= pos.row < self.rows and 0 <= pos.col < self.cols

    def is_wall(self, pos: Position) -> bool:
        return self.grid[pos.row][pos.col] == WALL

    def is_walkable(self, pos: Position) -> bool:
        return self.in_bounds(pos) and not self.is_wall(pos)

    def neighbors(self, pos: Position) -> Iterator[Position]:
        """Devuelve los vecinos transitables en orden fijo (arriba, abajo, izq, der)."""
        for d_row, d_col in _DELTAS:
            candidate = Position(pos.row + d_row, pos.col + d_col)
            if self.is_walkable(candidate):
                yield candidate
