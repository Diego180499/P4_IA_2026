"""Endpoints de búsqueda de rutas (ejecución individual y comparación)."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.api.v1.mappers import dto_to_position, result_to_dto
from app.domain.services.search_service import SearchService
from app.schemas.search import (
    CompareRequest,
    CompareResponse,
    SearchRequest,
    SearchResultDTO,
)

router = APIRouter(prefix="/search", tags=["search"])


def get_search_service() -> SearchService:
    return SearchService()


@router.post(
    "",
    response_model=SearchResultDTO,
    summary="Ejecuta un algoritmo de búsqueda (BFS, DFS o A*)",
)
def search(
    request: SearchRequest,
    service: SearchService = Depends(get_search_service),
) -> SearchResultDTO:
    result = service.run(
        grid=request.maze.grid,
        start=dto_to_position(request.start),
        goal=dto_to_position(request.goal),
        algorithm=request.algorithm,
    )
    return result_to_dto(result)


@router.post(
    "/compare",
    response_model=CompareResponse,
    summary="Ejecuta y compara varios algoritmos (por defecto BFS y DFS)",
)
def compare(
    request: CompareRequest,
    service: SearchService = Depends(get_search_service),
) -> CompareResponse:
    results = service.compare(
        grid=request.maze.grid,
        start=dto_to_position(request.start),
        goal=dto_to_position(request.goal),
        algorithms=request.algorithms,
    )
    comparison = service.build_comparison(results)
    return CompareResponse(
        results={name: result_to_dto(r) for name, r in results.items()},
        comparison=comparison,
    )
