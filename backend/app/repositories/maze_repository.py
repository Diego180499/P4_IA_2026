"""Repositorio en memoria de laberintos predefinidos (patrón Repository).

No se usa base de datos: el almacén es un diccionario en memoria. Esta capa
abstrae el acceso a los datos para que los servicios no dependan de su origen.
"""

from __future__ import annotations

from typing import List

from app.core.exceptions import MazeNotFoundError
from app.data.predefined_mazes import PREDEFINED_MAZES, PredefinedMaze


class MazeRepository:
    """Acceso de solo lectura a los laberintos predefinidos."""

    def list_all(self) -> List[PredefinedMaze]:
        return list(PREDEFINED_MAZES.values())

    def get_by_id(self, maze_id: str) -> PredefinedMaze:
        maze = PREDEFINED_MAZES.get(maze_id)
        if maze is None:
            raise MazeNotFoundError(
                f"No existe un laberinto predefinido con id '{maze_id}'."
            )
        return maze
