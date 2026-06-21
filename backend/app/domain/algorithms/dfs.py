"""Depth-First Search (DFS) — implementación con lógica pura.

Explora en profundidad usando una pila LIFO (lista de Python). Se implementa
de forma ITERATIVA para evitar desbordamiento de pila en laberintos grandes.
DFS no garantiza la ruta más corta; es útil para comparar comportamiento.

Restricción del enunciado: no se usan librerías que resuelvan la búsqueda
automáticamente; solo estructuras de datos estándar.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from app.domain.algorithms.base import SearchStrategy
from app.domain.models.maze import Maze, Position
from app.domain.models.search_result import SearchResult


class DFSStrategy(SearchStrategy):
    name = "dfs"

    def search(self, maze: Maze, start: Position, goal: Position) -> SearchResult:
        return self._timed_search(lambda: self._run(maze, start, goal))

    def _run(self, maze: Maze, start: Position, goal: Position) -> SearchResult:
        stack: List[Position] = [start]
        visited: set[Position] = set()
        parents: Dict[Position, Optional[Position]] = {start: None}
        visited_order: List[Position] = []

        while stack:
            current = stack.pop()  # LIFO

            # Un mismo nodo puede entrar a la pila más de una vez; lo saltamos
            # si ya fue procesado.
            if current in visited:
                continue
            visited.add(current)
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
                    # Registramos el padre la primera vez que se descubre.
                    if neighbor not in parents:
                        parents[neighbor] = current
                    stack.append(neighbor)

        return SearchResult(
            algorithm=self.name,
            found=False,
            path=[],
            visited_order=visited_order,
        )
