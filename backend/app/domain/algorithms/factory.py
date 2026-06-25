"""Factory para seleccionar la estrategia de búsqueda por nombre.

Centraliza el registro de algoritmos disponibles. Añadir uno nuevo solo
requiere registrarlo aquí, sin tocar los servicios ni los endpoints.
"""

from __future__ import annotations

from typing import Dict, List

from app.core.exceptions import UnsupportedAlgorithmError
from app.domain.algorithms.astar import AStarStrategy
from app.domain.algorithms.base import SearchStrategy
from app.domain.algorithms.bfs import BFSStrategy
from app.domain.algorithms.dfs import DFSStrategy

# Registro de estrategias disponibles (una instancia reutilizable por algoritmo).
_REGISTRY: Dict[str, SearchStrategy] = {
    BFSStrategy.name: BFSStrategy(),
    DFSStrategy.name: DFSStrategy(),
    AStarStrategy.name: AStarStrategy(),
}


def get_strategy(name: str) -> SearchStrategy:
    """Devuelve la estrategia asociada a `name` (case-insensitive)."""
    key = name.strip().lower()
    strategy = _REGISTRY.get(key)
    if strategy is None:
        raise UnsupportedAlgorithmError(
            f"Algoritmo no soportado: '{name}'. "
            f"Disponibles: {', '.join(available_algorithms())}."
        )
    return strategy


def available_algorithms() -> List[str]:
    """Lista los nombres de los algoritmos registrados."""
    return list(_REGISTRY.keys())
