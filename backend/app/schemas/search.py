"""Esquemas Pydantic (DTOs) para las peticiones y respuestas de búsqueda."""

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from app.schemas.maze import MazeDTO, PositionDTO


class SearchRequest(BaseModel):
    """Petición para ejecutar un único algoritmo de búsqueda."""

    maze: MazeDTO
    start: PositionDTO
    goal: PositionDTO
    algorithm: str = Field(
        "bfs",
        description="Algoritmo a ejecutar: 'bfs', 'dfs' o 'astar'.",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "maze": {
                    "grid": [
                        [0, 0, 0, 1, 0],
                        [1, 1, 0, 1, 0],
                        [0, 0, 0, 0, 0],
                        [0, 1, 1, 1, 0],
                        [0, 0, 0, 0, 0],
                    ]
                },
                "start": {"row": 0, "col": 0},
                "goal": {"row": 4, "col": 4},
                "algorithm": "bfs",
            }
        }
    }


class CompareRequest(BaseModel):
    """Petición para comparar varios algoritmos sobre el mismo laberinto."""

    maze: MazeDTO
    start: PositionDTO
    goal: PositionDTO
    algorithms: List[str] = Field(
        default_factory=lambda: ["bfs", "dfs"],
        description="Lista de algoritmos a comparar.",
    )


class SearchResultDTO(BaseModel):
    """Resultado de un algoritmo, con todas las métricas exigidas."""

    algorithm: str
    found: bool
    path: List[PositionDTO]
    path_length: int
    nodes_explored: int
    execution_time_ms: float
    visited_order: List[PositionDTO]


class CompareResponse(BaseModel):
    """Resultados de varios algoritmos más un resumen comparativo."""

    results: Dict[str, SearchResultDTO]
    comparison: Dict[str, Optional[str]]
