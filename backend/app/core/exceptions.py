"""Excepciones de dominio y sus manejadores para FastAPI.

Centraliza el manejo de errores para devolver respuestas HTTP consistentes,
cumpliendo el requisito de "manejo de errores cuando no exista una ruta válida"
y ante entradas inválidas.
"""

from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse


class RoboMazeError(Exception):
    """Excepción base del dominio."""

    status_code: int = 400

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(message)


class InvalidPositionError(RoboMazeError):
    """La posición de inicio o meta es inválida (fuera de límites u obstáculo)."""

    status_code = 422


class InvalidMazeError(RoboMazeError):
    """El laberinto está mal formado (dimensiones o celdas inválidas)."""

    status_code = 422


class UnsupportedAlgorithmError(RoboMazeError):
    """Se solicitó un algoritmo que no existe."""

    status_code = 400


class MazeNotFoundError(RoboMazeError):
    """No existe un laberinto predefinido con el identificador dado."""

    status_code = 404


async def robomaze_exception_handler(
    _request: Request, exc: RoboMazeError
) -> JSONResponse:
    """Convierte cualquier excepción de dominio en una respuesta JSON."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.__class__.__name__, "detail": exc.message},
    )
