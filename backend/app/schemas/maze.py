"""Esquemas Pydantic (DTOs) para posiciones y laberintos.

Estos modelos definen el contrato HTTP y desacoplan la API del dominio.
La validación estructural (tipos, rangos, celdas) ocurre aquí.
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field, model_validator

from app.core.config import settings


class PositionDTO(BaseModel):
    """Una posición (fila, columna) dentro del laberinto."""

    row: int = Field(..., ge=0, description="Fila (0 en la parte superior).")
    col: int = Field(..., ge=0, description="Columna (0 a la izquierda).")

    model_config = {"json_schema_extra": {"example": {"row": 0, "col": 0}}}


class MazeDTO(BaseModel):
    """Cuadrícula del laberinto: 0 = libre, 1 = obstáculo."""

    grid: List[List[int]] = Field(
        ...,
        description="Matriz de enteros (0 libre, 1 muro). Todas las filas del mismo ancho.",
    )

    @model_validator(mode="after")
    def _validate_grid(self) -> "MazeDTO":
        grid = self.grid
        if not grid or not grid[0]:
            raise ValueError("El laberinto no puede estar vacío.")

        rows, cols = len(grid), len(grid[0])
        if rows > settings.MAX_DIMENSION or cols > settings.MAX_DIMENSION:
            raise ValueError(
                f"El laberinto excede el tamaño máximo permitido "
                f"({settings.MAX_DIMENSION}x{settings.MAX_DIMENSION})."
            )

        for r, fila in enumerate(grid):
            if len(fila) != cols:
                raise ValueError(f"La fila {r} no coincide con el ancho del laberinto.")
            for c, celda in enumerate(fila):
                if celda not in (0, 1):
                    raise ValueError(
                        f"Celda inválida en ({r}, {c}): {celda}. Use 0 o 1."
                    )
        return self

    @property
    def rows(self) -> int:
        return len(self.grid)

    @property
    def cols(self) -> int:
        return len(self.grid[0])


class PredefinedMazeDTO(BaseModel):
    """Laberinto predefinido devuelto por la API."""

    id: str
    name: str
    description: str
    grid: List[List[int]]
    start: PositionDTO
    goal: PositionDTO
