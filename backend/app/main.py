"""Punto de entrada de la aplicación FastAPI (RoboMaze API).

Crea la app, configura CORS, registra los manejadores de error de dominio
e incluye los routers de la versión 1.

Ejecución local:
    uvicorn app.main:app --reload
Documentación interactiva: http://localhost:8000/docs
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import RoboMazeError, robomaze_exception_handler


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.DESCRIPTION,
        version=settings.VERSION,
    )

    # CORS para permitir el consumo desde el frontend web.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Manejo centralizado de errores de dominio.
    app.add_exception_handler(RoboMazeError, robomaze_exception_handler)

    # Routers de la API v1.
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)

    @app.get("/", tags=["root"], summary="Información básica del servicio")
    def root() -> dict[str, str]:
        return {
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
            "docs": "/docs",
        }

    return app


app = create_app()
