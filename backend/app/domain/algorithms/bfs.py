"""Breadth-First Search (BFS) — implementación con lógica pura.

Explora el grafo por niveles usando una cola FIFO (collections.deque).
Con costo uniforme (1 por movimiento), BFS garantiza la ruta más corta
en número de pasos.

Restricción del enunciado: no se usan librerías que resuelvan la búsqueda
automáticamente; solo estructuras de datos estándar.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Optional

from app.domain.algorithms.base import SearchStrategy
from app.domain.models.maze import Maze, Position
from app.domain.models.search_result import SearchResult


class BFSStrategy(SearchStrategy):
    name = "bfs"

    def search(self, maze: Maze, start: Position, goal: Position) -> SearchResult:
        return self._timed_search(lambda: self._run(maze, start, goal))

    def _run(self, maze: Maze, start: Position, goal: Position) -> SearchResult:
        queue: deque[Position] = deque([start])
        visited: set[Position] = {start}
        parents: Dict[Position, Optional[Position]] = {start: None}
        visited_order: List[Position] = []

        while queue:
            current = queue.popleft()  # FIFO
            visited_order.append(current)

            if current == goal:
                path = self.reconstruct_path(parents, goal)
                return SearchResult(
                    algorithm=self.name,
                    found=True,
                    path=path,
                    visited_order=visited_order,
                )

            for neighbor in maze.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = current
                    queue.append(neighbor)

        # Cola agotada sin alcanzar la meta: no existe ruta.
        return SearchResult(
            algorithm=self.name,
            found=False,
            path=[],
            visited_order=visited_order,
        )
