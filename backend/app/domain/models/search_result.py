"""Value object con el resultado de una búsqueda y sus métricas."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from app.domain.models.maze import Position


@dataclass
class SearchResult:
    """Resultado de ejecutar un algoritmo de búsqueda sobre un laberinto.

    Contiene todas las métricas exigidas por el enunciado: la ruta encontrada,
    la cantidad de nodos explorados y el tiempo de ejecución.
    """

    algorithm: str
    found: bool
    path: List[Position] = field(default_factory=list)
    visited_order: List[Position] = field(default_factory=list)
    execution_time_ms: float = 0.0

    @property
    def path_length(self) -> int:
        """Número de pasos de la ruta (aristas). 0 si no hay ruta."""
        return max(len(self.path) - 1, 0)

    @property
    def nodes_explored(self) -> int:
        """Cantidad de nodos que el algoritmo procesó durante la búsqueda."""
        return len(self.visited_order)
