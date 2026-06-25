"""Servicio de aplicación que orquesta la ejecución de las búsquedas.

Convierte las entradas en entidades de dominio, valida posiciones, selecciona
la estrategia mediante la factory y produce el/los resultado(s). No conoce
nada de HTTP ni de FastAPI.
"""

from __future__ import annotations

from typing import Dict, List

from app.domain.algorithms.factory import get_strategy
from app.domain.models.maze import Maze, Position
from app.domain.models.search_result import SearchResult


class SearchService:
    """Casos de uso relacionados con la búsqueda de rutas."""

    def run(
        self,
        grid: List[List[int]],
        start: Position,
        goal: Position,
        algorithm: str,
    ) -> SearchResult:
        """Ejecuta un único algoritmo sobre el laberinto dado."""
        maze = Maze(grid)
        maze.validate_position(start, "inicial")
        maze.validate_position(goal, "objetivo")

        strategy = get_strategy(algorithm)
        return strategy.search(maze, start, goal)

    def compare(
        self,
        grid: List[List[int]],
        start: Position,
        goal: Position,
        algorithms: List[str],
    ) -> Dict[str, SearchResult]:
        """Ejecuta varios algoritmos sobre el mismo laberinto y los devuelve.

        El laberinto se valida una sola vez; cada algoritmo se ejecuta de
        forma independiente.
        """
        maze = Maze(grid)
        maze.validate_position(start, "inicial")
        maze.validate_position(goal, "objetivo")

        results: Dict[str, SearchResult] = {}
        for name in algorithms:
            strategy = get_strategy(name)
            results[strategy.name] = strategy.search(maze, start, goal)
        return results

    @staticmethod
    def build_comparison(results: Dict[str, SearchResult]) -> Dict[str, str | None]:
        """Resume cuál algoritmo gana en cada métrica (solo entre los que hallaron ruta)."""
        found = {name: r for name, r in results.items() if r.found}
        if not found:
            return {
                "shorter_path": None,
                "fewer_nodes_explored": None,
                "faster": None,
            }
        return {
            "shorter_path": min(found, key=lambda n: found[n].path_length),
            "fewer_nodes_explored": min(found, key=lambda n: found[n].nodes_explored),
            "faster": min(found, key=lambda n: found[n].execution_time_ms),
        }
