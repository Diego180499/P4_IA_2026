"""Endpoints de laberintos predefinidos."""

from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from app.api.v1.mappers import position_to_dto
from app.domain.models.maze import Position
from app.domain.services.maze_service import MazeService
from app.schemas.maze import PredefinedMazeDTO

router = APIRouter(prefix="/mazes", tags=["mazes"])


def get_maze_service() -> MazeService:
    return MazeService()


def _to_dto(maze) -> PredefinedMazeDTO:
    return PredefinedMazeDTO(
        id=maze.id,
        name=maze.name,
        description=maze.description,
        grid=maze.grid,
        start=position_to_dto(Position(*maze.start)),
        goal=position_to_dto(Position(*maze.goal)),
    )


@router.get("", response_model=List[PredefinedMazeDTO], summary="Lista los laberintos predefinidos")
def list_mazes(service: MazeService = Depends(get_maze_service)) -> List[PredefinedMazeDTO]:
    return [_to_dto(m) for m in service.list_mazes()]


@router.get("/{maze_id}", response_model=PredefinedMazeDTO, summary="Obtiene un laberinto predefinido")
def get_maze(maze_id: str, service: MazeService = Depends(get_maze_service)) -> PredefinedMazeDTO:
    return _to_dto(service.get_maze(maze_id))
