"""Conversión entre entidades de dominio y DTOs de la API."""

from __future__ import annotations

from app.domain.models.maze import Position
from app.domain.models.search_result import SearchResult
from app.schemas.maze import PositionDTO
from app.schemas.search import SearchResultDTO


def position_to_dto(pos: Position) -> PositionDTO:
    return PositionDTO(row=pos.row, col=pos.col)


def dto_to_position(dto: PositionDTO) -> Position:
    return Position(row=dto.row, col=dto.col)


def result_to_dto(result: SearchResult) -> SearchResultDTO:
    return SearchResultDTO(
        algorithm=result.algorithm,
        found=result.found,
        path=[position_to_dto(p) for p in result.path],
        path_length=result.path_length,
        nodes_explored=result.nodes_explored,
        execution_time_ms=result.execution_time_ms,
        visited_order=[position_to_dto(p) for p in result.visited_order],
    )
