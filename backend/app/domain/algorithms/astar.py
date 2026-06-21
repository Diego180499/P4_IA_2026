"""A* — implementación opcional con lógica pura.

Búsqueda informada que usa una cola de prioridad (heapq, librería estándar)
y la distancia Manhattan como heurística admisible. Permite comparar
resultados frente a BFS y DFS.

No se usa ninguna librería de pathfinding: solo estructuras estándar.
"""

from __future__ import annotations

import heapq
import itertools
from typing import Dict, List, Optional

from app.domain.algorithms.base import SearchStrategy
from app.domain.models.maze import Maze, Position
from app.domain.models.search_result import SearchResult


def _manhattan(a: Position, b: Position) -> int:
    return abs(a.row - b.row) + abs(a.col - b.col)


class AStarStrategy(SearchStrategy):
    name = "astar"

    def search(self, maze: Maze, start: Position, goal: Position) -> SearchResult:
        return self._timed_search(lambda: self._run(maze, start, goal))

    def _run(self, maze: Maze, start: Position, goal: Position) -> SearchResult:
        counter = itertools.count()  # desempate estable en el heap
        open_heap: list[tuple[int, int, Position]] = []
        heapq.heappush(open_heap, (_manhattan(start, goal), next(counter), start))

        g_score: Dict[Position, int] = {start: 0}
        parents: Dict[Position, Optional[Position]] = {start: None}
        visited: set[Position] = set()
        visited_order: List[Position] = []

        while open_heap:
            _, _, current = heapq.heappop(open_heap)

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
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float("inf")):
                    g_score[neighbor] = tentative_g
                    parents[neighbor] = current
                    f_score = tentative_g + _manhattan(neighbor, goal)
                    heapq.heappush(open_heap, (f_score, next(counter), neighbor))

        return SearchResult(
            algorithm=self.name,
            found=False,
            path=[],
            visited_order=visited_order,
        )
