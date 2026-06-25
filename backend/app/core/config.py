"""Configuración central de la aplicación.

Mantiene en un solo lugar los parámetros de la app (título, versión, CORS).
No se usa base de datos: todo el estado vive en memoria.
"""

from __future__ import annotations


class Settings:
    """Parámetros de configuración de la aplicación."""

    PROJECT_NAME: str = "RoboMaze API"
    DESCRIPTION: str = (
        "API REST para la búsqueda de rutas en laberintos mediante "
        "algoritmos de búsqueda en espacios de estados (BFS y DFS)."
    )
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    # Orígenes permitidos para CORS. El frontend web consume esta API.
    # Se usa "*" por simplicidad académica; en producción se restringiría.
    CORS_ORIGINS: list[str] = ["*"]

    # Límite defensivo para el tamaño del laberinto (evita abusos / cuelgues).
    MAX_DIMENSION: int = 100


settings = Settings()
