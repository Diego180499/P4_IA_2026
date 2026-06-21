"""Interfaz común para los algoritmos de búsqueda (patrón Strategy).

Todas las estrategias (BFS, DFS, A*) implementan `search`, lo que permite
intercambiarlas sin modificar el código que las consume.
"""

from __future__ import annotations

import time
from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from app.domain.models.maze import Maze, Position
from app.domain.models.search_result import SearchResult


class SearchStrategy(ABC):
    """Estrategia abstracta de búsqueda de rutas."""

    #: Nombre identificador del algoritmo (p. ej. "bfs").
    name: str = "base"

    @abstractmethod
    def search(self, maze: Maze, start: Position, goal: Position) -> SearchResult:
        """Busca una ruta de `start` a `goal` dentro de `maze`."""
        raise NotImplementedError

    # ------------------------------------------------------------------ #
    # Utilidades compartidas
    # ------------------------------------------------------------------ #
    @staticmethod
    def reconstruct_path(
        parents: Dict[Position, Optional[Position]], goal: Position
    ) -> List[Position]:
        """Reconstruye la ruta desde `goal` hacia atrás usando los padres."""
        if goal not in parents:
            return []
        path: List[Position] = []
        node: Optional[Position] = goal
        while node is not None:
            path.append(node)
            node = parents[node]
        path.reverse()
        return path

    def _timed_search(self, fn) -> SearchResult:
        """Ejecuta `fn` midiendo el tiempo de cómputo puro en milisegundos."""
        start_time = time.perf_counter()
        result = fn()
        elapsed_ms = (time.perf_counter() - start_time) * 1000.0
        result.execution_time_ms = round(elapsed_ms, 4)
        return result
