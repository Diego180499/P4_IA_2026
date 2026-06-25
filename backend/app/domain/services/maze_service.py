"""Servicio de aplicación para los laberintos predefinidos."""

from __future__ import annotations

from typing import List

from app.data.predefined_mazes import PredefinedMaze
from app.repositories.maze_repository import MazeRepository


class MazeService:
    """Casos de uso relacionados con los laberintos predefinidos."""

    def __init__(self, repository: MazeRepository | None = None) -> None:
        self._repository = repository or MazeRepository()

    def list_mazes(self) -> List[PredefinedMaze]:
        return self._repository.list_all()

    def get_maze(self, maze_id: str) -> PredefinedMaze:
        return self._repository.get_by_id(maze_id)
